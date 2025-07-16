# MySQL · 捉虫动态 · long semaphore waits

**Date:** 2014/08
**Source:** http://mysql.taobao.org/monthly/2014/08/05/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2014 / 08
 ](/monthly/2014/08)

 * 当期文章

 MySQL · 参数故事 · timed_mutexes
* MySQL · 参数故事 · innodb_flush_log_at_trx_commit
* MySQL · 捉虫动态 · Count(Distinct) ERROR
* MySQL · 捉虫动态 · mysqldump BUFFER OVERFLOW
* MySQL · 捉虫动态 · long semaphore waits
* MariaDB · 分支特性 · 支持大于16K的InnoDB Page Size
* MariaDB · 分支特性 · FusionIO特性支持
* TokuDB · 性能优化 · Bulk Fetch
* TokuDB · 数据结构 · Fractal-Trees与LSM-Trees对比
* TokuDB·社区八卦·TokuDB团队

 ## MySQL · 捉虫动态 · long semaphore waits 
 Author: 

 **现象描述：**

Innodb引擎，父表和子表通过foreign constraint进行关联，因为在更新数据时需要check外键constraint，当父表被大量的子表referenced时候，那么在open Innodb数据字典的时候，需要open所有的child table和所有的foreign constraint，导致持有dict_sys->mutex时间过长，产生long semaphore wait, 然后innodb crash了。

case复现

`CREATE TABLE `t1` (
`f1` int(11) NOT NULL,
PRIMARY KEY (`f1`)
) ENGINE=InnoDB
CREATE TABLE `fk_1` (
`f1` int(11) NOT NULL,
PRIMARY KEY (`f1`),
CONSTRAINT `pc1` FOREIGN KEY (`f1`) REFERENCES `t1` (`f1`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
......
`
这里建了fk_[0-10000]张表。

**分析过程**

1. 数据字典

 innodb使用系统表空间保存表相关的数据字典，系统的数据字典包括：

 SYS_TABLES
 SYS_INDEXES
 SYS_COLUMNS
 SYS_FIELDS
 SYS_FOREIGN
 SYS_FOREIGN_COLS
 SYS_STATS
 在load某个表的时候，分别从这些表中把表相关的index,column, index_field, foreign, foreign_col数据保存到dictionary cache中。 对应的内存对象分别是：dict_col_struct，dict_field_struct，dict_index_struct，dict_table_struct，dict_foreign_struct。
2. open过程

 dict_load_table：

 通过sys_tables系统表，load table相关的定义
3. 通过sys_indexes系统表，根据table_id load 所有相关index
4. 通过sys_columns系统表，根据table_id load 所有的columns
5. 通过sys_fields系统表，根据index_id load 所有index的field
6. 通过sys_foreign系统表，load所有关联的表和foreign key

 load foreign的详细过程

 3.1 根据表名t1 查找sys_foreign.

 而sys_foreign表上一共有三个索引： 　　　　

 ` index_1(id): cluster_index
 index_2(for_name): secondary_index
 index_3(ref_name): secondary_index
` 
 所以，根据for_name=’t1’, ref_name=’t1’检索出来所有相关的foreign_id.

 3.2 加入cache

 因为没有专门的cache，foreign分别加入到for_name->foreign_list, ref_name->referenced_list。 问题的关键：因为foreign是全局唯一的，但foreign又与两个表关联，所以，有可能在open 其它表的时候已经打开过，所以，create foreign对象后，需要判断以下四个list，是否已经存在，如果存在就直接使用。

 dict_foreign_find：分别查询这四个list，如果已经存在，则free新建的foreign对象，引用已经存在的。

 ` for_name->foreign_list
 for_name->referenced_list
 ref_name->foreign_list
 ref_name->referenced_list
` 

 如果不存在，把新建的foreign加入到for_name->foreign_list，ref_name->referenced_list链表中。

 问题的原因：

 因为第一次load，所以find都没有找到，但这四个都是list，随着open的越来越多，检索的代价越来越大。 而整个过程中，都一直持有trx_sys->mutex，最终导致了long semaphore wait。

 问题改进方法：

在MySQL 5.5.39版本中，进行了修复，修复的方法就是，除了foreign_list，referenced_list。 另外又增加了两个red_black tree，如下源码所示：

`struct dict_table_struct{
table_id_t id; 　　/*!< id of the table */
mem_heap_t* heap; /*!< memory heap */
char* name; 　　　　/*!< table name */
UT_LIST_BASE_NODE_T(dict_foreign_t)
foreign_list;　　　　　　　　　　/*!< list of foreign key constraints in the table; these refer to columns in other tables */
UT_LIST_BASE_NODE_T(dict_foreign_t)
referenced_list;/*!< list of foreign key constraints which refer to this table */
ib_rbt_t* foreign_rbt; /*!< a rb-tree of all foreign keys listed in foreign_list, sorted by foreign->id */
ib_rbt_t* referenced_rbt; /*!< a rb-tree of all foreign keys listed in referenced_list, sorted by foreign->id */
}
`

这样dict_foreign_find的过程中，通过red_black tree进行检索，时间复杂度降到O(log n).

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)