# MySQL · 源码分析 · innodb 空间索引实现

**Date:** 2022/08
**Source:** http://mysql.taobao.org/monthly/2022/08/04/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2022 / 08
 ](/monthly/2022/08)

 * 当期文章

 PolarDB MySQL·HTAP·浅析IMCI的列存数据压缩
* MySQL · 行业洞察 · 长路漫漫, 从Blink-tree 到Bw-tree (上)
* PolarDB MySQL · 引擎特性 · 内核原生的全局索引支持
* MySQL · 源码分析 · innodb 空间索引实现

 ## MySQL · 源码分析 · innodb 空间索引实现 
 Author: yunqian 

 ## innodb空间索引介绍
innodb支持空间索引，但很少有关于innodb关于空间索引的实现的介绍文章，本篇文章主要目的是介绍innodb关于空间索引的源码介绍，知其所以然。空间索引本质上是二级索引中的一种，基于R树实现。

innodb索引主要是基于B+树实现，B+树是一棵平衡树，是把一维直线分为若干段线段，当我们查找满足某个要求的点的时候，只要去查找它所属的线段即可。这种思想其实就是先找一个大的空间，再逐步缩小所要查找的空间，最终在一个自己设定的最小不可分空间内找出满足要求的解。B+树是解决低纬度数据（通常一维，也就是一个数据维度上进行比较），R树很好的解决了高维空间搜索问题。它把B树的思想很好的扩展到了多维空间，采用了B树分割空间的思想（如果B树在一维的线段进行分割，R树就是在二维甚至多维度的空间），并在添加、删除操作时采用合并、分解结点的方法，保证树的平衡性。因此，R树就是一棵用来存储高维数据的平衡树。R树的介绍我们在此不过多展开介绍，详细可查询相关文档。

## 源码实现分析
innodb空间索引的代码实现主要聚集在这几个文件：include/gis0geo.h include/gis0rtree.h include/gis0tree.ic include/gis0type.h gis/gis0geo.cc gis/gis0rtee.cc gis/gis0sea.cc，代码量不大，大概是几千行，相对比较容易阅读。本篇文章下面围绕空间索引rec的定位，查询，插入，更新，删除等来做介绍，主要介绍核心代码逻辑。代码基于mysql 8.0.30。

### **rec定位**
空间索引的rec定位不仅是在查询的时候使用，在其他DML操作前也需要将cursor定位到对应的rec位置，代码实现上主要是结合数据结构rtr_info_t，由函数btr_cur_search_to_nth_level进行逐层迭代查询，在非叶子节点调用rtr_cur_search_with_match函数，遍历对应level的page上所有rec，将cursor定位到匹配的rec，进而往下层继续遍历，在叶子节点，调用page_cur_search_with_match函数，类似其他索引使用二分法定位。我们在此着重说明数据结构rtr_info_t和函数btr_cur_search_to_nth_level和rtr_cur_search_with_match在空间索引定位上的实现。

#### **rtr_info_t数据结构介绍**
`// rtr_info_t数据结构主要用来记录定位rec过程中匹配的page或者rec信息，
// 主要被使用在btr_cur_t中跟踪cursor定位rtree中的一些信息，以及用在
// dict_index_t中跟踪所有当前rtree在进行的查询请求相关信息rtr_info_track_t
typedef struct rtr_info {
 rtr_node_path_t *path; // vector保存所有匹配的内部节点page 
 rtr_node_path_t *parent_path; // vector 保存查询中匹配的 parent pages
 matched_rec_t *matches; // 保存所有匹配的叶子节点记录
 ib_mutex_t rtr_path_mutex; /*!< mutex protect the "path" vector */
 buf_block_t *tree_blocks[RTR_MAX_LEVELS + RTR_LEAF_LATCH_NUM];
 /*!< tracking pages that would be locked at leaf level, for future free */
 ulint tree_savepoints[RTR_MAX_LEVELS + RTR_LEAF_LATCH_NUM];
 /*!< savepoint used to release latches/blocks on each level and leaf level */
 rtr_mbr_t mbr; /*!< the search MBR */
 que_thr_t *thr; /*!< the search thread */
 mem_heap_t *heap; /*!< memory heap */
 btr_cur_t *cursor; /*!< cursor used for search */
 dict_index_t *index; /*!< index it is searching */
 bool need_prdt_lock; /*!< whether we will need predicate lock the tree */
 bool need_page_lock; /*!< whether we will need predicate page lock the tree */
 bool allocated; /*!< whether this structure is allocate or on stack */
 bool mbr_adj; /*!< whether mbr will need to be enlarged for an insertion operation */
 bool fd_del; /*!< found deleted row */
 const dtuple_t *search_tuple; /*!< search tuple being used */
 page_cur_mode_t search_mode; /*!< current search mode */
 bool *is_dup; /*!< whether the current rec is a duplicate record. */
} rtr_info_t;
`

#### **btr_cur_search_to_nth_level 函数关于空间索引rtree定位**
```
// btr_cur_search_to_nth_level 函数是Btree定位rec的关键函数，
// 空间索引实现的Rtree在逐层迭代上同Btree类似，所以也由该函数完成各种的遍历
// 主要是一些初始化，search mode调整，谓词锁添加，判断是否要调整rtr_inof.mbr，
// 及将每层对应page的定位交给rtr_cur_search_with_match 和 page_cur_search_with_match
// 该函数非空间索引相关实现可参考http://mysql.taobao.org/monthly/2021/07/02/
// 下面是该函数的注释版本，主要是空间索引相关的关键代码
void btr_cur_search_to_nth_level(
 dict_index_t *index, /*!< in: index */
 ulint level, /*!< in: the tree level of search */
 const dtuple_t *tuple, /*!< in: data tuple; NOTE: n_fields_cmp in
 tuple must be set so that it cannot get
 compared to the node ptr page number field! */
 page_cur_mode_t mode, /*!< in: PAGE_CUR_L, ...;
 Inserts should always be made using
 PAGE_CUR_LE to search the position! */
 ...)
{
 const space_id_t space = dict_index_get_space(index);
 const page_size_t page_size(dict_table_page_size(index->table));
 /* Start with the root page. */
 page_id_t page_id(space, dict_index_get_page(index));

// 循环、逐层的查找，直至达到传入的层数 level，一般是0（即叶子节点）
// 此处只分析空间索引Spatial index的部分
search_loop:
 //获取每层对应page
 page = buf_block_get_frame(block);

 // root节点，进行一些初始化操作
 // 对空间索引rtree split sequence no rtr_ssn进行初始化
 // 将待定位记录的MBR保存到cursor rtr_info
 if (UNIV_UNLIKELY(height == ULINT_UNDEFINED)) {
 if (dict_index_is_spatial(index)) {
 node_seq_t seq_no = rtr_get_current_ssn_id(index);
 /* If SSN in memory is not initialized, fetch
 it from root page */
 if (seq_no < 1) {
 node_seq_t root_seq_no;
 root_seq_no = page_get_ssn_id(page);
 mutex_enter(&(index->rtr_ssn.mutex));
 index->rtr_ssn.seq_no = root_seq_no + 1;
 mutex_exit(&(index->rtr_ssn.mutex));
 }
 /* Save the MBR */
 cursor->rtr_info->thr = cursor->thr;
 rtr_get_mbr_from_tuple(tuple, &cursor->rtr_info->mbr);
 }
 }

 // search mode调整:
 // 目标level，叶子节点调整为PAGE_CUR_LE
 // 非目标level搜索所有子树，看是否“contain”相应查询MBR
 if (dict_index_is_spatial(index)) {
 /* Remember the page search mode */
 search_mode = page_mode;
 // 查询定位 search mode调整
 if (page_mode == PAGE_CUR_RTREE_LOCATE && level == height) {
 if (level == 0) {
 page_mode = PAGE_CUR_LE;
 } else {
 page_mode = PAGE_CUR_RTREE_GET_FATHER;
 }
 }
 // 插入记录定位 search mode调整
 if (page_mode == PAGE_CUR_RTREE_INSERT) {
 page_mode = (level == height) ? PAGE_CUR_LE : PAGE_CUR_RTREE_INSERT;
 }
 }

 // page内定位记录
 // 非目标level使用rtr_cur_search_with_match
 // 目标level使用page_cur_search_with_match
 if (dict_index_is_spatial(index) && page_mode >= PAGE_CUR_CONTAIN) {
 //非目标level搜索定位
 found = rtr_cur_search_with_match(block, index, tuple, page_mode,
 page_cursor, cursor->rtr_info);
 /* Need to use BTR_MODIFY_TREE to do the MBR adjustment */
 if (search_mode == PAGE_CUR_RTREE_INSERT && cursor->rtr_info->mbr_adj) {
 if (latch_mode & BTR_MODIFY_LEAF) {
 /* Parent MBR needs updated, should retry
 with BTR_MODIFY_TREE */
 goto func_exit;
 } else if (latch_mode & BTR_MODIFY_TREE) {
 rtree_parent_modified = true;
 cursor->rtr_info->mbr_adj = false;
 mbr_adj = true;
 } else {
 ut_d(ut_error);
 }
 }
 if (found && page_mode == PAGE_CUR_RTREE_GET_FATHER) {
 cursor->low_match = DICT_INDEX_SPATIAL_NODEPTR_SIZE + 1;
 }
 } else {
 // 目标level搜索定位
 /* Search for complete index fields. */
 up_bytes = low_bytes = 0;
 page_cur_search_with_match(block, index, tuple, page_mode, &up_match,
 &low_match, page_cursor,
 need_path ? cursor->rtr_info : nullptr);
 }

 // 在serializable isolation时添加谓词锁Predicate lock
 if (dict_index_is_spatial(index) && cursor->rtr_info->need_prdt_lock &&
 mode != PAGE_CUR_RTREE_INSERT && mode != PAGE_CUR_RTREE_LOCATE &&
 mode >= PAGE_CUR_CONTAIN) {
 trx_t *trx = thr_get_trx(cursor->thr);
 lock_prdt_t prdt;
 trx_mutex_enter(trx);
 lock_init_prdt_from_mbr(&prdt, &cursor->rtr_info->mbr, mode,
 trx->lock.lock_heap);
 trx_mutex_exit(trx);
 if (rw_latch == RW_NO_LATCH && height != 0) {
 rw_lock_s_lock(&block->lock, UT_LOCATION_HERE);
 }
 lock_prdt_lock(block, &prdt, index, LOCK_S, LOCK_PREDICATE, cursor->thr);
 if (rw_latch == RW_NO_LATCH && height != 0) {
 rw_lock_s_unlock(&(block->lock));
 }
 }

 if (level != height) {
 node_ptr = page_cur_get_rec(page_cursor);

 if (dict_index_is_spatial(index)) {
 // supremum rec 直接返回
 if (page_rec_is_supremum(node_ptr)) {
 cursor->low_match = 0;
 cursor->up_match = 0;
 goto func_exit;
 }

 /* If we are doing insertion or record locating,
 remember the tree nodes we visited */
 if (page_mode == PAGE_CUR_RTREE_INSERT ||
 (search_mode == PAGE_CUR_RTREE_LOCATE &&
 (latch_mode != BTR_MODIFY_LEAF))) {

 /* Store the parent cursor location */
 rtr_store_parent_path(block, cursor, latch_mode, height + 1, mtr);
 if (page_mode == PAGE_CUR_RTREE_INSERT) {
 btr_pcur_t *r_cursor =
 rtr_get_parent_cursor(cursor, height + 1, true);
 node_ptr = r_cursor->get_rec();
 }
 }
 page_mode = search_mode;
 }

 // 往下层继续查找
 page_id.reset(space, btr_node_ptr_get_child_page_no(node_ptr, offsets));

 if (dict_index_is_spatial(index) && page_mode >= PAGE_CUR_CONTAIN &&
 page_mode != PAGE_CUR_RTREE_INSERT) {
 rtr_node_path_t *path = cursor->rtr_info->path;
 if (!path->empty() && found) {
 path->pop_back();
 }
 }

 goto search_loop;
 }

 /* For spatial index, remember what blocks are still latched */
 if (dict_index_is_spatial(index) &&
 (latch_mode == BTR_MODIFY_TREE || latch_mode == BTR_MODIFY_LEAF)) {
 for (ulint i = 0; i < n_releases; i++) {
 cursor->rtr_info->tree_blocks[i] = nullptr;
 cursor->rtr_info->tree_savepoints[i] = 0;
 }

 for (ulint i = n_releases; i <= n_blocks; i++) {
 cursor->rtr_info->tree_blocks[i] = tree_blocks[i];
 cursor->rtr_info->tree_savepoints[i] = tree_savepoints[i];
 }
 }

func_exit:

 if (mbr_adj) {
 /* remember that we will need to adjust parent MBR */
 cursor->rtr_info->mbr_adj = true;
 }
}

```

#### **rtr_cur_search_with_match 空间索引page内rec定位**
```
/** Searches the right position in rtree for a page cursor.*/
// rtr_cur_search_with_match 函数是定位rtree page内位置的主要函数，其实现就是遍历page内
// 所有rec，判断遍历到的rec和要查询定位的rec的mbr是否满足某种关系，然后将page cursor定位到
// 查询定位到的rec，并更新一些数据结构
bool rtr_cur_search_with_match(const buf_block_t *block, dict_index_t *index,
 const dtuple_t *tuple, page_cur_mode_t mode,
 page_cur_t *cursor, rtr_info_t *rtr_info) {
 // 判断是不是到叶子节点，初始rec为第一个rec
 page = buf_block_get_frame(block);
 is_leaf = page_is_leaf(page);
 level = btr_page_get_level(page);
 if (mode == PAGE_CUR_RTREE_LOCATE) {
 mode = PAGE_CUR_WITHIN;
 }
 rec = page_dir_slot_get_rec(page_dir_get_nth_slot(page, 0));
 last_rec = rec;
 best_rec = rec;
 if (page_rec_is_infimum(rec)) {
 rec = page_rec_get_next_const(rec);
 }

 // 从前往后循环遍历所有rec来定位rec，直到supremum rec
 while (!page_rec_is_supremum(rec)) {
 // 非叶子节点定位rec
 if (!is_leaf) {
 switch (mode) {
 ... ...
 // 非叶子节点，插入rec场景，找到所有rec中让mbr增加最小的rec
 case PAGE_CUR_RTREE_INSERT:
 cmp = cmp_dtuple_rec_with_gis(tuple, rec, offsets, PAGE_CUR_WITHIN,
 index->rtr_srs.get());
 if (cmp != 0) {
 double area{0.0};
 increase = rtr_rec_cal_increase(tuple, rec, offsets, &area,
 index->rtr_srs.get());
 if (increase < least_inc) {
 least_inc = increase;
 best_rec = rec;
 } else if (best_rec && best_rec == first_rec) {
 /* if first_rec is set,
 we will try to avoid it */
 least_inc = increase;
 best_rec = rec;
 }
 }
 break;
 case PAGE_CUR_RTREE_GET_FATHER:
 cmp = cmp_dtuple_rec_with_gis_internal(tuple, rec, offsets,
 index->rtr_srs.get());
 break;
 default:
 //有前面mode调整知查询定位rec走到这里，判断对应rec的mbr是否包含要查询的rec
 cmp = cmp_dtuple_rec_with_gis(tuple, rec, offsets, mode,
 index->rtr_srs.get());
 }
 } else {
 cmp = cmp_dtuple_rec_with_gis(tuple, rec, offsets, mode,
 index->rtr_srs.get());
 }

 //匹配到对应rec
 if (cmp == 0) {
 found = true;
 // 如果定位到，非叶子节点则将匹配的node/rec 添加到rtr_info->path
 // 叶子节点则添加到rtr_info->matches
 if (rtr_info && mode != PAGE_CUR_RTREE_INSERT) {
 if (!is_leaf) {
 is_loc = (orig_mode == PAGE_CUR_RTREE_LOCATE ||
 orig_mode == PAGE_CUR_RTREE_GET_FATHER);
 page_no = btr_node_ptr_get_child_page_no(rec, offsets);
 rtr_non_leaf_stack_push(rtr_info->path, page_no, new_seq, level - 1,
 0, nullptr, 0);
 if (is_loc) {
 rtr_non_leaf_insert_stack_push(index, rtr_info->parent_path, level,
 page_no, block, rec, 0);
 }
 } else {
 rtr_leaf_push_match_rec(rec, rtr_info, offsets, page_is_comp(page));
 }
 last_match_rec = rec;
 } else {
 /* This is the insertion case, it will break
 once it finds the first MBR that can accomodate
 the inserting rec */
 break;
 }
 }

 last_rec = rec;
 //取下一条rec记录继续往后遍历
 rec = page_rec_get_next_const(rec);
 } //循环结束

 // 页上所有rec都比较后，定位cursor到对应rec 
 if (page_rec_is_supremum(rec)) {
 if (!is_leaf) {
 if (!found) {
 /* No match case, if it is for insertion,
 then we select the record that result in
 least increased area */
 if (mode == PAGE_CUR_RTREE_INSERT) {
 child_no = btr_node_ptr_get_child_page_no(best_rec, offsets);
 rtr_non_leaf_insert_stack_push(index, rtr_info->parent_path, level,
 child_no, block, best_rec, least_inc);
 page_cur_position(best_rec, block, cursor);
 rtr_info->mbr_adj = true;
 } else {
 /* Position at the last rec of the
 page, if it is not the leaf page */
 page_cur_position(last_rec, block, cursor);
 }
 } else {
 /* There are matching records, position
 in the last matching records */
 if (rtr_info) {
 rec = last_match_rec;
 page_cur_position(rec, block, cursor);
 }
 }
 } else if (rtr_info) {
 /* Leaf level, no match, position at the
 last (supremum) rec */
 if (!last_match_rec) {
 page_cur_position(rec, block, cursor);
 goto func_exit;
 }

 /* There are matched records */
 matched_rec_t *match_rec = rtr_info->matches;
 test_rec = match_rec->matched_recs->back();
 /* Pop the last match record and position on it */
 match_rec->matched_recs->pop_back();
 page_cur_position(test_rec.r_rec, &match_rec->block, cursor);
 }
 } else {
 if (mode == PAGE_CUR_RTREE_INSERT) {
 child_no = btr_node_ptr_get_child_page_no(rec, offsets);
 rtr_non_leaf_insert_stack_push(index, rtr_info->parent_path, level,
 child_no, block, rec, 0);
 } else if (rtr_info && found && !is_leaf) {
 rec = last_match_rec;
 }
 page_cur_position(rec, block, cursor);
 }

func_exit:
 return (found);
}

```

### **插入**
向有空间索引的表中插入数据时，主要的代码路径和其他普通记录基本一致，即先更新主键，然后再更新二级索引，空间索引是二级索引的一种，空间索引插入数据的代码主要是在row_ins_sec_index_entry_low，cursor定位到的位置是有足够的空间来存放插入的数据，则直接插入数据返回即可，如果没有足够的空间插入数据，则会导致rtree的split，rtree的split代码实现主要是函数rtr_page_split_and_insert。我们主要分析函数row_ins_sec_index_entry_low和rtr_page_split_and_insert实现

#### **row_ins_sec_index_entry_low 空间索引插入数据**
`// row_ins_sec_index_entry_low是完成二级索引数据插入的主要函数
dberr_t row_ins_sec_index_entry_low(uint32_t flags, ulint mode,
 dict_index_t *index,
 mem_heap_t *offsets_heap, mem_heap_t *heap,
 dtuple_t *entry, ... ...) {
 // 初始化rtr_info，及定位rec
 if (dict_index_is_spatial(index)) {
 cursor.index = index;
 // 初始化rtr_info并保存到cursor中，
 rtr_init_rtr_info(&rtr_info, false, &cursor, index, false);
 rtr_info_update_btr(&cursor, &rtr_info);
 
 //通过btr_cur_search_to_nth_level定位cursor到对应rec
 btr_cur_search_to_nth_level(index, 0, entry, PAGE_CUR_RTREE_INSERT,
 search_mode, &cursor, 0, __FILE__, __LINE__,
 &mtr);

 // 需要改为悲观插入时，调整search mode重新定位rec
 if (mode == BTR_MODIFY_LEAF && rtr_info.mbr_adj) {
 mtr_commit(&mtr);
 rtr_clean_rtr_info(&rtr_info, true);
 rtr_init_rtr_info(&rtr_info, false, &cursor, index, false);
 rtr_info_update_btr(&cursor, &rtr_info);

 mtr_start(&mtr);
 search_mode &= ~BTR_MODIFY_LEAF;
 search_mode |= BTR_MODIFY_TREE;
 btr_cur_search_to_nth_level(index, 0, entry, PAGE_CUR_RTREE_INSERT,
 search_mode, &cursor, 0, __FILE__, __LINE__,
 &mtr);
 mode = BTR_MODIFY_TREE;
 }
 }

 if (row_ins_must_modify_rec(&cursor)) {
 // 通过修改去掉已有rec的delete mark插入数据
 err = row_ins_sec_index_entry_by_modify(
 flags, mode, &cursor, &offsets, offsets_heap, heap, entry, thr, &mtr);

 if (err == DB_SUCCESS && dict_index_is_spatial(index) && rtr_info.mbr_adj) {
 // 插入后调整插入路径节点的mbr范围
 err = rtr_ins_enlarge_mbr(&cursor, &mtr);
 }
 } else {
 rec_t *insert_rec;
 big_rec_t *big_rec;

 if (mode == BTR_MODIFY_LEAF) {
 // 乐观插入
 err = btr_cur_optimistic_insert(flags, &cursor, &offsets, &offsets_heap,
 entry, &insert_rec, &big_rec, thr, &mtr);
 if (err == DB_SUCCESS && dict_index_is_spatial(index) &&
 rtr_info.mbr_adj) {
 // 插入后调整插入路径节点的mbr范围
 err = rtr_ins_enlarge_mbr(&cursor, &mtr);
 }
 } else {
 // 先尝试乐观插入，失败后再尝试悲观插入
 err = btr_cur_optimistic_insert(flags, &cursor, &offsets, &offsets_heap,
 entry, &insert_rec, &big_rec, thr, &mtr);
 if (err == DB_FAIL) {
 err = btr_cur_pessimistic_insert(flags, &cursor, &offsets, &offsets_heap,
 entry, &insert_rec, &big_rec, thr, &mtr);
 }
 if (err == DB_SUCCESS && dict_index_is_spatial(index) &&
 rtr_info.mbr_adj) {
 // 插入后调整插入路径节点的mbr范围
 err = rtr_ins_enlarge_mbr(&cursor, &mtr);
 }
 }
 }

func_exit:
 if (dict_index_is_spatial(index)) {
 // 清除rtr_info
 rtr_clean_rtr_info(&rtr_info, true);
 }

 return err;
}

`

#### **rtr_page_split_and_insert rtree page split实现**
```
// rtr_page_split_and_insert 函数将page上的recs分为两个组，
// 新申请一个page，将一组recs留在旧page，将二组recs移动到新page
rec_t *rtr_page_split_and_insert(
 uint32_t flags, /*!< in: undo logging and locking flags */
 btr_cur_t *cursor, /*!< in/out: cursor at which to insert; when the
 function returns, the cursor is positioned
 on the predecessor of the inserted record */
 ulint **offsets, /*!< out: offsets on inserted record */
 mem_heap_t **heap, /*!< in/out: pointer to memory heap, or NULL */
 const dtuple_t *tuple, /*!< in: tuple to insert */
 mtr_t *mtr) /*!< in: mtr */
{

func_start:
 // 将page上recs分为两组
 n_recs = page_get_n_recs(page) + 1;
 end_split_node = rtr_split_node_array + n_recs;
 first_rec_group = split_rtree_node(
 rtr_split_node_array, static_cast<int>(n_recs),
 static_cast<int>(total_data), static_cast<int>(insert_size), 0, 2, 2,
 &buf_pos, SPDIMS, static_cast<uchar *>(first_rec),
 cursor->index->rtr_srs.get());

 // 分配一个新的page
 direction = FSP_UP;
 hint_page_no = page_no + 1;
 new_block = btr_page_alloc(cursor->index, hint_page_no, direction, page_level,
 mtr, mtr);
 new_page_zip = buf_block_get_page_zip(new_block);
 btr_page_create(new_block, new_page_zip, cursor->index, page_level, mtr);
 new_page = buf_block_get_frame(new_block);

 /* Set new ssn to the new page and page. */
 page_set_ssn_id(new_block, new_page_zip, current_ssn, mtr);
 next_ssn = rtr_get_new_ssn_id(cursor->index);
 page_set_ssn_id(block, page_zip, next_ssn, mtr);

 // 第一个group的recs留在旧page，将第二个group的rec移动到新page，主要在函数rtr_split_page_move_rec_list操作实现
 // 如果新page为压缩页，且压缩操作失败，则在下面将所有rec拷贝到新page，然后分别删除新旧page上多余的rec
 if (false || !rtr_split_page_move_rec_list(rtr_split_node_array, first_rec_group,
 new_block, block, first_rec,
 cursor->index, *heap, mtr)) {

 /* For some reason, compressing new_page failed,
 even though it should contain fewer records than
 the original page. Copy the page byte for byte
 and then delete the records from both pages
 as appropriate. Deleting will always succeed. */
 ... ...
 }

 /* Insert the new rec to the proper page. */
 cur_split_node = end_split_node - 1;
 if (cur_split_node->n_node != first_rec_group) {
 insert_block = new_block;
 } else {
 insert_block = block;
 }

 /* Reposition the cursor for insert and try insertion */
 page_cursor = btr_cur_get_page_cur(cursor);
 page_cur_search(insert_block, cursor->index, tuple, PAGE_CUR_LE, page_cursor);

 // 插入数据
 rec = page_cur_tuple_insert(page_cursor, tuple, cursor->index, offsets, heap,
 mtr);

 /* If insert did not fit, try page reorganization.
 For compressed pages, page_cur_tuple_insert() will have
 attempted this already. */
 if (rec == nullptr) {
 if (!page_cur_get_page_zip(page_cursor) &&
 btr_page_reorganize(page_cursor, cursor->index, mtr)) {
 rec = page_cur_tuple_insert(page_cursor, tuple, cursor->index, offsets,
 heap, mtr);
 }
 /* If insert fail, we will try to split the insert_block
 again. */
 }

 // 更新mbr、ssn等信息
 /* Calculate the mbr on the upper half-page, and the mbr on
 original page. */
 rtr_page_cal_mbr(cursor->index, block, &mbr, *heap);
 rtr_page_cal_mbr(cursor->index, new_block, &new_mbr, *heap);
 prdt.data = &mbr;
 new_prdt.data = &new_mbr;

 /* Check any predicate locks need to be moved/copied to the
 new page */
 lock_prdt_update_split(block, new_block, &prdt, &new_prdt);

 /* Adjust the upper level. */
 rtr_adjust_upper_level(cursor, flags, block, new_block, &mbr, &new_mbr, mtr);

 /* Save the new ssn to the root page, since we need to reinit
 the first ssn value from it after restart server. */
 root_block = btr_root_block_get(cursor->index, RW_SX_LATCH, mtr);
 page_zip = buf_block_get_page_zip(root_block);
 page_set_ssn_id(root_block, page_zip, next_ssn, mtr);

 /* Insert fit on the page: update the free bits for the
 left and right pages in the same mtr */
 if (page_is_leaf(page)) {
 ibuf_update_free_bits_for_two_pages_low(block, new_block, mtr);
 }

 /* If the new res insert fail, we need to do another split
 again. */
 if (!rec) {
 /* We play safe and reset the free bits for new_page */
 ... ...
 goto func_start;
 }
 MONITOR_INC(MONITOR_INDEX_SPLIT);
 return (rec);
}

```

### **读取**
读取数据，分为一致性读和锁定读。事务利用MVCC进行读取操作称为一致性读（Consistent Read），或者一致性无锁读（也称快照读），所有普通的SELECT语句在READ COMMITTED、 REPEATABLE READ隔离级别下都是一致性读。一致性读并不会对表中任何记录进行加锁操作，其他事务可以自由底对表中的记录进行改动。在一致性读场景下空间索引和普通索引没有区别，只是定位rec的方法不同（rtree定位rec见上面分析），在锁定读，serializable isolation隔离级别时空间索引加的是predicate lock，关于加锁读这里也不再展开。

### **更新及删除**
空间索引更新删除操作同普通二级索引更新擅长操作代码路径基本一致，主要在函数row_upd_sec_index_entry_low中实现，该函数中空间索引部分和普通索引除了定位rec有区别，其他基本一致，所以不再详细说明。删除操作可以看作是更新操作的一种，删除操作是将原来record更新添加delete mark标记，实际record的删除是在undo purge的时候，这时可能会导致进行page的merge，此处也不再展开说明。

## 总结
innodb基于rtree的空间索引实现，和基于B+树实现的二级索引，主要代码路径基本一致，空间索引在MVCC，事务等特性上和普通二级索引一致。只是在定位、插入、更新及删除rec时，涉及rtree的一些基本信息及rtree的操作有些不同，还有就是在serializable isolation隔离级别时使用了predicate lock，相对一般二级索引有所不同。空间索引是二级索引基于rtree的一个特殊实现版本。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)