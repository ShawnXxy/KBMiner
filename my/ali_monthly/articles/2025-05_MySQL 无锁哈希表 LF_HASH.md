# MySQL 无锁哈希表 LF_HASH

**Date:** 2025/05
**Source:** http://mysql.taobao.org/monthly/2025/05/02/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2025 / 05
 ](/monthly/2025/05)

 * 当期文章

 FTS 源码阅读
* MySQL 无锁哈希表 LF_HASH

 ## MySQL 无锁哈希表 LF_HASH 
 Author: 谢榕彪(归墨) 

 本篇文章主要用代码代码结合一些图来看。

实现一个 无锁哈希表，一共需要考虑实现以下几点：

* 无锁动态数组
* 线程间如何管理内存，避免释放
* 无锁链表

下面我们先一一介绍 MySQL 是如何实现的，最后介绍无锁哈希表实现。

## 1 无锁动态数组 LF_DYNARRAY

LF_DYNARRAY 总共 分为 4 层，每层能容纳的元素是指数级别增加的，如第 0 层能存储 255 个元素，每个 n + 1 层包含 255 个 n 层顶长数组。这样来支持不同纬度的内存扩展。最长支持 4311810304 个元素。LF_HASH 几乎所有涉及数组部分都是基于 LF_DYNARRAY。

`typedef struct {
 std::atomic<void *> level[LF_DYNARRAY_LEVELS]; // 每个 level 的数组其实地址
 uint size_of_element; // 数组 element 占据的内存大小
} LF_DYNARRAY;
void lf_dynarray_init(LF_DYNARRAY *array, uint element_size);
`
几个数组操作重要的函数：

`// 按 idx 索引数组元素，不存在就申请空间，返回申请空间的位置
void *lf_dynarray_lvalue(LF_DYNARRAY *array, uint idx);
// 遍历数组元素，调用传入的回调 func，自定义的 func 需要处理每个 level 0 的 256 个元素
int lf_dynarray_iterate(LF_DYNARRAY *array, lf_dynarray_func func, void *arg);
`

最重要我们来看看 lf_dynarray_lvalue，按 idx 索引数组元素，不存在就申请空间，返回申请空间的位置。主要流程是：

* 先确定第 idx 的元素在哪个层级
* 从对应层级逐层向下找到存储 第 idx 元素存储的位置，把每个层级数组空间申请出来
* 申请第 0 层真实的元素大小的空间

`void *lf_dynarray_lvalue(LF_DYNARRAY *array, uint idx) {
 void *ptr;
 int i;

 // 找到 idx 所在层级，即包含 level i-1 之前所有元素，又小于 level i 的所有元素之和
 for (i = LF_DYNARRAY_LEVELS - 1; idx < dynarray_idxes_in_prev_levels[i]; i--)
 /* no-op */;
 
 std::atomic<void *> *ptr_ptr = &array->level[i];
 idx -= dynarray_idxes_in_prev_levels[i];
 // 第 idx 的元素一定在第 0 层，只不过是 level i 索引的，所以需要从 level i 逐层向下把索引到 idx 元素的数组的空间都申请出来
 for (; i > 0; i--) {
 if (!(ptr = *ptr_ptr)) {
 void *alloc = my_malloc(key_memory_lf_dynarray,
 LF_DYNARRAY_LEVEL_LENGTH * sizeof(void *),
 MYF(MY_WME | MY_ZEROFILL));
 if (unlikely(!alloc)) {
 return (NULL);
 }
 // 避免其他线程也在申请，用 CAS 做验证，已经申请了就主动释放
 if (atomic_compare_exchange_strong(ptr_ptr, &ptr, alloc)) {
 ptr = alloc;
 } else {
 my_free(alloc);
 }
 }
 ptr_ptr =
 ((std::atomic<void *> *)ptr) + idx / dynarray_idxes_in_prev_level[i];
 idx %= dynarray_idxes_in_prev_level[i];
 }
 // 到第 0 层了，idx 在 255 内，需要把真实存储元素的空间给申请出来，多申请了一些空间为了对齐，并把申请空间的基址存在了 data 前一个元素，方便释放
 if (!(ptr = *ptr_ptr)) {
 uchar *alloc, *data;
 alloc = static_cast<uchar *>(
 my_malloc(key_memory_lf_dynarray,
 LF_DYNARRAY_LEVEL_LENGTH * array->size_of_element +
 MY_MAX(array->size_of_element, sizeof(void *)),
 MYF(MY_WME | MY_ZEROFILL)));
 if (unlikely(!alloc)) {
 return (NULL);
 }
 /* reserve the space for free() address */
 data = alloc + sizeof(void *);
 {
 /* alignment */
 intptr mod = ((intptr)data) % array->size_of_element;
 if (mod) {
 data += array->size_of_element - mod;
 }
 }
 ((void **)data)[-1] = alloc; /* free() will need the original pointer */
 if (atomic_compare_exchange_strong(ptr_ptr, &ptr,
 static_cast<void *>(data))) {
 ptr = data;
 } else {
 my_free(alloc);
 }
 }
 return ((uchar *)ptr) + array->size_of_element * idx;
}
`

## 2 LF_PINS 和 LF_PINBOX

**线程如何管理自己访问的内存呢？**

MySQL 使用 LF_PINS 来 pin 住当前线程使用的内存，避免被其他线程释放。 LF_PINS 支持 pin 住 4 个地址。LF_PINS 是从 LF_PINBOX 中申请的，LF_PINBOX 管理了所有从其申请的 LF_PINS。

为了方便描述，我们混用 address 来表述线程访问的内存对象地址。

LF_PINBOX 管理了所有线程申请的 LF_PINS，当要释放一个 address 时，需要扫描 LF_PINBOX 中所有 LF_PINS，判断是否可以释放，为了减少遍历次数，每个 LF_PINS free 时先加入 purgatory 链表，个数到 10 之后再去做真正的释放。

`struct LF_PINS {
 std::atomic<void *> pin[LF_PINBOX_PINS]; // pin 住的地址数组
 LF_PINBOX *pinbox; // 申请的
 void *purgatory; // 存放临时的要 free 的 address
 uint32 purgatory_count;
 std::atomic<uint32> link; // 串联 pinbox 的 free 列表
 /* we want sizeof(LF_PINS) to be 64 to avoid false sharing */
#if SIZEOF_INT * 2 + SIZEOF_CHARP * (LF_PINBOX_PINS + 2) != 64
 char pad[64 - sizeof(uint32) * 2 - sizeof(void *) * (LF_PINBOX_PINS + 2)];
#endif
};

typedef struct {
 LF_DYNARRAY pinarray; // 存储所有的 LF_PINS，包括已经回收的
 lf_pinbox_free_func *free_func; // 释放 address 时的回调函数
 void *free_func_arg; // free_func 的参数
 uint free_ptr_offset; // 当 address 释放时，不再使用的内存位置，加入 purgatory 时，用作串联链表
 std::atomic<uint32> pinstack_top_ver; /* this is a versioned pointer */
 std::atomic<uint32> pins_in_array; /* number of elements in array */
} LF_PINBOX;
void lf_pinbox_init(LF_PINBOX *pinbox, uint free_ptr_offset,
 lf_pinbox_free_func *free_func, void *free_func_arg);
`

LF_PINS 对于 pin 和解 pin 很简单，只需要原子修改 pin 数组即可。

`static inline void lf_pin(LF_PINS *pins, int pin, void *addr) {
 pins->pin[pin].store(addr);
}

static inline void lf_unpin(LF_PINS *pins, int pin) {
 pins->pin[pin].store(nullptr);
}
`

**那么 LF_PINBOX 如何管理 LF_PINS 呢**？

LF_PINBOX 的 pinarray 存储了所有的 LF_PINS，包括已经回收的，最多 65536 个。原因是 pinbox 维护了 pinstack_top_ver 用于存储回收的 LF_PINS 的栈， pinstack_top_ver 只有低 16 位用于存储栈顶空闲 LF_PINS 所在 pinarray 的序号，高 16 位存储版本，每次更新 pinstack_top_ver 后加 1，防止 ABA 问题。

**当从 pinbox 申请一个 LF_PINS 时**：先从 pinstack_top_ver 申请，再从 pinarray 申请。

`LF_PINS *lf_pinbox_get_pins(LF_PINBOX *pinbox) {
 ...
 top_ver = pinbox->pinstack_top_ver;
 do {
 if (!(pins = top_ver % LF_PINBOX_MAX_PINS)) {
 /* 序号 0 代表栈为空，从 pinarray 申请 LF_PINS */
 pins = pinbox->pins_in_array.fetch_add(1) + 1;
 if (unlikely(pins >= LF_PINBOX_MAX_PINS)) {
 return 0;
 }
 
 el = (LF_PINS *)lf_dynarray_lvalue(&pinbox->pinarray, pins);
 if (unlikely(!el)) {
 return 0;
 }
 break;
 }
 el = (LF_PINS *)lf_dynarray_value(&pinbox->pinarray, pins);
 next = el->link;
 } while (!atomic_compare_exchange_strong(
 &pinbox->pinstack_top_ver, &top_ver,
 top_ver - pins + next + LF_PINBOX_MAX_PINS)); // 加 LF_PINBOX_MAX_PINS 相当于 高 16 位 加一了
 ...
}
`

**当归还一个 LF_PINS 给 pinbox 时**：free 掉 purgatory 中所有的 address 后才能回收，可能需要等待 pin 住该 address 的其他线程结束。

`void lf_pinbox_put_pins(LF_PINS *pins) {

 // free 所有当前 pin 的 purgatory 中所有的 address 列表
 while (pins->purgatory_count) {
 lf_pinbox_real_free(pins);
 if (pins->purgatory_count) {
 my_thread_yield();
 }
 }
 // 加入 pinstack_top_ver 栈，等待复用
 top_ver = pinbox->pinstack_top_ver;
 do {
 pins->link = top_ver % LF_PINBOX_MAX_PINS; // pins 下一个是 pinstack_top_ver
 } while (!atomic_compare_exchange_strong(
 &pinbox->pinstack_top_ver, &top_ver,
 top_ver - pins->link + nr + LF_PINBOX_MAX_PINS));
}
`

**当要 free 一个 pin 住的 address 时**，先加入 purgatory，到 10 个后再开始真正 free。

`void lf_pinbox_free(LF_PINS *pins, void *addr) {
 add_to_purgatory(pins, addr);
 // 超过 10 个才真正做 free
 if (pins->purgatory_count % LF_PURGATORY_SIZE == 0) {
 lf_pinbox_real_free(pins);
 }
}

static void lf_pinbox_real_free(LF_PINS *pins) {
 // 清空 LF_PINS 的 purgatory，在遍历 pinbox pinarray 时候会把无法 free 的重新加入
 struct st_match_and_save_arg arg = {pins, pinbox, pins->purgatory};
 pins->purgatory = NULL;
 pins->purgatory_count = 0;

 lf_dynarray_iterate(&pinbox->pinarray, match_and_save, &arg);

 // 剩下的 old_purgatory 是真正没被 pin 住的 address，直接调用 free_func 回调去处理
 if (arg.old_purgatory) {
 ...
 pinbox->free_func(arg.old_purgatory, last, pinbox->free_func_arg);
 }
}
`

## 3 内存管理 LF_ALLOCATOR

前面介绍了如何申请和管理 LF_PINS，以及如何用 LF_PINS 去 pin, unpin，以及 free 内存。

MySQL 基于上述流程实现了一个内存管理器 LF_ALLOCATOR。

其包含一个 LF_PINBOX，当需要操作从 LF_ALLOCATOR 分配的内存，都需要从 LF_PINBOX 申请一个 LF_PINS。空闲内存也是由一个栈管理，管理模式和前面介绍的 purgatory 类似，都是复用 address 中空闲部分，用于链接不同分配的内存。剩下就是一些元信息包括内存分配大小和回调函数。

`struct LF_ALLOCATOR {
 LF_PINBOX pinbox; // 管理操作内存涉及的 LF_PINS
 std::atomic<uchar *> top; // free 栈顶，维护了 free 的内存链表，在每个 address 使用了 purgatory 的相同的 free_ptr_offset 来串起来
 uint element_size; // 每次申请内存的大小
 std::atomic<uint32> mallocs; // 记录向系统申请内存的次数
 lf_allocator_func *constructor; // 每次申请内存的回调，复用内存不调用
 lf_allocator_func *destructor; // 每次释放内存回调
};
void lf_alloc_init2(LF_ALLOCATOR *allocator, uint size, uint free_ptr_offset,
 lf_allocator_func *ctor, lf_allocator_func *dtor);
`

* **当申请一个内存 address 时**，会从 LF_ALLOCATOR 的 pinbox 申请一个 LF_PINS，因为 LF_ALLOCATOR 存在了 LF_PINS 的 free_func_arg 中，所以直接就能通过 LF_PINS 去申请内存。

```
void *lf_alloc_new(LF_PINS *pins) {
 LF_ALLOCATOR *allocator = (LF_ALLOCATOR *)(pins->pinbox->free_func_arg);
 uchar *node;
 for (;;) { 
 // 先看 LF_ALLOCATOR 中的 free 栈中是否空闲
 do {
 // 有先拿出来 pin 住，防止在修改 free 栈时被其他线程 free 了
 node = allocator->top;
 lf_pin(pins, 0, node);
 } while (node != allocator->top && LF_BACKOFF);
 if (!node) {
 // free 栈是空的，向系统申请
 node = static_cast<uchar *>(
 my_malloc(key_memory_lf_node, allocator->element_size, MYF(MY_WME)));
 if (likely(node != 0)) {
 // 每次申请都调用构造初始化
 if (allocator->constructor) {
 allocator->constructor(node);
 }

 ++allocator->mallocs;
 }
 break;
 }
 // 如果是从 free 栈拿的，修改 free 栈成下一个，修改失败，说明其他线程拿走了，重新拿一个
 if (atomic_compare_exchange_strong(&allocator->top, &node,
 anext_node(node).load())) {
 break;
 }
 }
 // unpin 掉
 lf_unpin(pins, 0);
 return node;
}

```

* 因为内存释放是由 pinbox 来管理的，所以 LF_ALLOCATOR 只需要提供每次内存释放的回调即可，这回调也比较简单，主要也是把释放的内存链接（即 pinbox 每次释放是按一个 LF_PINS，会提供一个 purgatory 链表）加入到 LF_ALLOCATOR 的 free stack 中。

 看到这里，对的，之前 pinbox 真正释放的内存也没有真正释放，还存在 LF_ALLOCATOR 的 free stack 中。

`static void alloc_free(void *v_first, void *v_last, void *v_allocator) {
 uchar *first = static_cast<uchar *>(v_first);
 uchar *last = static_cast<uchar *>(v_last);
 LF_ALLOCATOR *allocator = static_cast<LF_ALLOCATOR *>(v_allocator);
 uchar *node = allocator->top;
 do {
 anext_node(last) = node; // double check，修改到 purgatory 的 last 指向到当前的 free stack
 } while (!atomic_compare_exchange_strong(&allocator->top, &node, first) &&
 LF_BACKOFF);
}
`

* 真正内存释放是在释放 LF_ALLOCATOR 时，此时需要确保没有线程访问 LF_ALLOCATOR 了，这样所有的申请的内存都在 free stack 上。

```
void lf_alloc_destroy(LF_ALLOCATOR *allocator) {
 uchar *node = allocator->top;
 while (node) {
 uchar *tmp = anext_node(node);
 if (allocator->destructor) {
 allocator->destructor(node);
 }
 my_free(node);
 node = tmp;
 }
 lf_pinbox_destroy(&allocator->pinbox);
 allocator->top = 0;
}

```

## 4 无锁链表 LF_SLIST

为了实现遍历同一个 bucket 的多个节点，MySQL 实现了 LF_SLIST 的无锁链表，

`struct LF_SLIST {
 std::atomic<LF_SLIST *>
 link; /* 指向链表的下一个元素 */
 uint32 hashnr; /* reversed hash number, for sorting */
 const uchar *key;
 size_t keylen;
 /*
 实际存储数据的部分，紧接在 LF_SLIST 的内存后
 */
};
`

LF_SLIST 的搜索是基于 CURSOR 的，

`typedef struct {
 std::atomic<LF_SLIST *> *prev;
 LF_SLIST *curr, *next;
} CURSOR;

cursor->next | cursor->curr | nullptr | nullptr

static int my_lfind(std::atomic<LF_SLIST *> *head, CHARSET_INFO *cs,
 uint32 hashnr, const uchar *key, size_t keylen,
 CURSOR *cursor, LF_PINS *pins, hash_walk_action callback) {
...
retry:
 cursor->prev = head;
 /* pin 住第一个 dummy node */
 do
 {
 cursor->curr = (LF_SLIST *)(*cursor->prev);
 lf_pin(pins, 1, cursor->curr);
 } while (*cursor->prev != cursor->curr && LF_BACKOFF);
 
 for (;;) {
 if (unlikely(!cursor->curr)) {
 return 0; /* end of the list */
 }
 do {
 /* double check 的方式 pin 住 curr 的 next 指针 */
 link = cursor->curr->link.load();
 cursor->next = PTR(link);
 lf_pin(pins, 0, cursor->next);
 } while (link != cursor->curr->link && LF_BACKOFF);
 cur_hashnr = cursor->curr->hashnr;
 cur_key = cursor->curr->key;
 cur_keylen = cursor->curr->keylen;
 if (*cursor->prev != cursor->curr) {
 /* 保证 prev 和 curr 是相连的，避免 prev 是 delete mark 的，
 这样才能把 delete mark 的 curr 进行 free*/
 (void)LF_BACKOFF;
 goto retry;
 }
 if (!DELETED(link)) {
 if (unlikely(callback != NULL)) {
 if (cur_hashnr & 1 && callback(cursor->curr + 1, (void *)key))
 return 1;
 } else if (cur_hashnr >= hashnr) {
 int r = 1;
 if (cur_hashnr > hashnr ||
 (r = my_strnncoll(cs, cur_key, cur_keylen, key, keylen)) >= 0) {
 return !r;
 }
 }
 cursor->prev = &(cursor->curr->link);
 lf_pin(pins, 2, cursor->curr);
 } else {
 /*
 we found a deleted node - be nice, help the other thread
 and remove this deleted node
 */
 if (atomic_compare_exchange_strong(cursor->prev, &cursor->curr,
 cursor->next)) {
 lf_pinbox_free(pins, cursor->curr);
 } else {
 (void)LF_BACKOFF;
 goto retry;
 }
 }
 cursor->curr = cursor->next;
 lf_pin(pins, 1, cursor->curr);
 }
}

`

## 5 LF_HASH

下面我们来看，基于 LF_DYNARRAY，LF_PINS，LF_ALLOCATOR 是如何实现无锁哈希表的。

`struct LF_HASH {
 LF_DYNARRAY array; /* hash itself */
 LF_ALLOCATOR alloc; /* allocator for elements */
 hash_get_key_function get_key; /* see HASH */
 CHARSET_INFO *charset; /* see HASH */
 lf_hash_func *hash_function; /* see HASH */
 uint key_offset, key_length; /* see HASH */
 uint element_size; /* size of memcpy'ed area on insert */
 uint flags; /* LF_HASH_UNIQUE, etc */
 std::atomic<int32> size; /* size of array */
 std::atomic<int32> count; /* number of elements in the hash */
 int max_load; /* average number of elements in a bucket */
 /**
 "Initialize" hook - called to finish initialization of object provided by
 LF_ALLOCATOR (which is pointed by "dst" parameter) and set element key
 from object passed as parameter to lf_hash_insert (pointed by "src"
 parameter). Allows to use LF_HASH with objects which are not "trivially
 copyable".
 NULL value means that element initialization is carried out by copying
 first element_size bytes from object which provided as parameter to
 lf_hash_insert.
 */
 lf_hash_init_func *initialize;
};
void lf_hash_init2(LF_HASH *hash, uint element_size, uint flags,
 uint key_offset, uint key_length,
 hash_get_key_function get_key, CHARSET_INFO *charset,
 lf_hash_func *hash_function, lf_allocator_func *ctor,
 lf_allocator_func *dtor, lf_hash_init_func *init);
`

```
static int initialize_bucket(LF_HASH *hash, std::atomic<LF_SLIST *> *node,
 uint bucket, LF_PINS *pins) {
 uint parent = my_clear_highest_bit(bucket);
 LF_SLIST *dummy =
 (LF_SLIST *)my_malloc(key_memory_lf_slist, sizeof(LF_SLIST), MYF(MY_WME));
 if (unlikely(!dummy)) {
 return -1;
 }
 LF_SLIST *tmp = 0, *cur;
 std::atomic<LF_SLIST *> *el = static_cast<std::atomic<LF_SLIST *> *>(
 lf_dynarray_lvalue(&hash->array, parent));
 if (unlikely(!el)) {
 my_free(dummy);
 return -1;
 }
 if (el->load() == nullptr && bucket &&
 unlikely(initialize_bucket(hash, el, parent, pins))) {
 my_free(dummy);
 return -1;
 }
 dummy->hashnr = my_reverse_bits(bucket) | 0; /* dummy node */
 dummy->key = dummy_key;
 dummy->keylen = 0;
 if ((cur = linsert(el, hash->charset, dummy, pins, LF_HASH_UNIQUE))) {
 my_free(dummy);
 dummy = cur;
 }
 atomic_compare_exchange_strong(node, &tmp, dummy);
 /*
 note that if the CAS above failed (after linsert() succeeded),
 it would mean that some other thread has executed linsert() for
 the same dummy node, its linsert() failed, it picked up our
 dummy node (in "dummy= cur") and executed the same CAS as above.
 Which means that even if CAS above failed we don't need to retry,
 and we should not free(dummy) - there's no memory leak here
 */
 return 0;
}

```

insert 逻辑。

`int lf_hash_insert(LF_HASH *hash, LF_PINS *pins, void *data) {
 int csize, bucket, hashnr;
 LF_SLIST *node;
 std::atomic<LF_SLIST *> *el;

 node = (LF_SLIST *)lf_alloc_new(pins); // 使用 LF_ALLOCATOR 申请一个节点内存
 if (unlikely(!node)) {
 return -1;
 }
 uchar *extra_data =
 (uchar *)(node + 1); // 插入的数据存放在 LF_SLIST 后面，有初始化函数，调用初始化函数，否则直接 copy 插入数据。
 if (hash->initialize) {
 (*hash->initialize)(extra_data, (uchar*)data);
 } else {
 memcpy(extra_data, data, hash->element_size);
 }
 // 计算 hash 的 key 值，有指定 get_key，调用 get_key，否则直接用 data 部分。
 node->key = hash_key(hash, (uchar *)(node + 1), &node->keylen); 
 
 hashnr = calc_hash(hash, node->key, node->keylen);
 bucket = hashnr % hash->size;
 el = static_cast<std::atomic<LF_SLIST *> *>(
 lf_dynarray_lvalue(&hash->array, bucket));
 if (unlikely(!el)) {
 lf_pinbox_free(pins, node);
 return -1;
 }
 if (el->load() == nullptr &&
 unlikely(initialize_bucket(hash, el, bucket, pins))) {
 lf_pinbox_free(pins, node);
 return -1;
 }
 node->hashnr = my_reverse_bits(hashnr) | 1; /* normal node */
 if (linsert(el, hash->charset, node, pins, hash->flags)) {
 lf_pinbox_free(pins, node);
 return 1;
 }
 csize = hash->size;
 if ((hash->count.fetch_add(1) + 1.0) / csize > hash->max_load) {
 atomic_compare_exchange_strong(&hash->size, &csize, csize * 2);
 }
 return 0;
}
`

[1] [【MySQL源码分析】MDL之LF_HASH [1]](https://kernelmaker.github.io/MySQL_lf_allocator)

[2] [MySQL · 源码剖析 · LF_HASH无锁实现](https://zhuanlan.zhihu.com/p/452849776)

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)