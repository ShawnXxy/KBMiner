# 11 期 | InnoDB 提交事务，提交了什么？

**原文链接**: https://opensource.actionsky.com/mysql-%e6%a0%b8%e5%bf%83%e6%a8%a1%e5%9d%97%e6%8f%ad%e7%a7%98-11-%e6%9c%9f-innodb-%e6%8f%90%e4%ba%a4%e4%ba%8b%e5%8a%a1%ef%bc%8c%e6%8f%90%e4%ba%a4%e4%ba%86%e4%bb%80%e4%b9%88%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2024-03-27T22:41:55-08:00

---

二阶段提交 commit 阶段的 commit 子阶段，InnoDB 存储引擎层面提交事务，主要是做一些收尾工作，这些有收尾工作有哪些？
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 1. 关于缓存 undo 段
为了提升分配 undo 段的效率，事务提交过程中，InnoDB 会缓存一些 undo 段。
只要同时满足两个条件，insert undo 段或 update undo 段就能被缓存。
**条件 1**：undo 段中只有一个 undo 页。
**条件 2**：这个唯一的 undo 页中，已经使用的的空间必须小于数据页大小的四分之三。以默认大小 16K 的 undo 页为例，undo 页中已经使用的空间必须小于 12K。
如果 insert undo 段满足缓存条件，它会加入回滚段的 insert_undo_cached 链表头部。
如果 update undo 段满足缓存条件，它会加入回滚段的 update_undo_cached 链表头部。
## 2. InnoDB 提交事务
二阶段提交过程中，commit 阶段的 flush 子阶段，把 prepare 阶段及之前产生的 redo 日志都刷盘了，把事务执行过程中产生的 binlog 日志都写入 binlog 日志文件了。
sync 子阶段根据系统变量 sync_binlog 的值决定是否触发操作系统把 binlog 日志刷盘。
前两个子阶段，都只处理了日志，不涉及 InnoDB 的事务。这两个阶段完成之后，InnoDB 的事务还没有提交，事务还处于准备提交状态（`TRX_STATE_PREPARED`）。
commit 子阶段才会真正提交 InnoDB 的事务，这个阶段完成之后，事务就提交完成了。
commit 子阶段提交 InnoDB 的事务，要做的事情有这些：
- 修改 insert undo 段的状态。
- 生成事务提交号，用于 purge 线程判断是否能清理某些 update undo 日志组中的 undo 日志。
- 修改 update undo 段的状态。
- 把 update undo 段中的 undo 日志组加入回滚段的 history list 链表。purge 线程会从这个链表中获取需要清理的 update undo 日志组。
- 把事务状态修改为 `TRX_STATE_COMMITTED_IN_MEMORY`。
- 释放事务执行过程中 InnoDB 给表或记录加的锁。
- 重新初始化事务对象，以备当前线程后续使用。
### 2.1 修改 insert undo 段状态
如果事务插入记录到用户普通表，InnoDB 会为事务分配一个 insert undo 段。
如果事务插入记录到用户临时表，InnoDB 会为事务分配另一个 insert undo 段。
InnoDB 可能会给事务分配 0 ~ 2 个 insert undo 段。commit 子阶段会修分配给事务的所有 insert undo 段的状态。
如果 insert undo 段满足缓存条件，它的状态会被修改为 `TRX_UNDO_CACHED`，否则，它的状态会被修改为 `TRX_UNDO_TO_FREE`。
事务提交完成之后，InnoDB 会根据状态缓存或者释放 insert undo 段。
### 2.2 生成事务提交号
事务提交号是事务对象的 `no` 属性，通常用 `trx->no` 表示。
代码里，对事务提交号的注释是 `transaction serialization number`，直译成中文应该称为事务序列号，或者事务串行号。
因为 trx->no 是在事务提交时生成的，我们还是把它称为**事务提交号**更容易理解一些。
只有 update undo 段需要事务提交号。purge 线程清理 update undo 日志时，会根据 update undo 段的 undo 日志组中保存的事务提交号，决定是否能清理这个 undo 日志组中的 undo 日志。
修改 update undo 段的状态之前，InnoDB 会生成事务提交号，保存到事务对象的 `no` 属性中。
`// storage/innobase/trx/trx0trx.cc
static inline bool trx_add_to_serialisation_list(trx_t *trx) {
...
trx->no = trx_sys_allocate_trx_no();
...
}
`
trx_sys_allocate_trx_no() 调用 `trx_sys_allocate_trx_id_or_no()` 生成事务提交号。
`// storage/innobase/include/trx0sys.ic
// 生成事务 ID
inline trx_id_t trx_sys_allocate_trx_id() {
ut_ad(trx_sys_mutex_own());
return trx_sys_allocate_trx_id_or_no();
}
// 生成事务提交号
inline trx_id_t trx_sys_allocate_trx_no() {
ut_ad(trx_sys_serialisation_mutex_own());
return trx_sys_allocate_trx_id_or_no();
}
`
从上面的代码可以看到，生成事务 ID 和事务提交号调用的是同一个方法，`trx_sys_allocate_trx_id_or_no()` 的代码如下：
`// storage/innobase/include/trx0sys.ic
inline trx_id_t trx_sys_allocate_trx_id_or_no() {
...
// trx_sys_allocate_trx_id_or_no() 每次被调用
// trx_sys->next_trx_id_or_no 加 1
// trx_id 保存的是加 1 之前的值
trx_id_t trx_id = trx_sys->next_trx_id_or_no.fetch_add(1);
...
return trx_id;
}
`
`trx_sys->next_trx_id_or_no` 保存的是下一个事务 ID 或事务提交号，具体是哪个，取决于是生成事务 ID 还是生成事务提交号先调用 `trx_sys_allocate_trx_id_or_no()`。
也就是说，事务 ID 和事务提交号是同一条流水线上生产出来的。我们以 trx 1 和 trx 2 两个事务为例，来说明生成事务 ID 和事务提交号的流程。
假设此时 `trx_sys->next_trx_id_or_no` 的值为 100，trx 1、trx 2 启动和提交的顺序如下：
- trx 1 启动。
- trx 2 启动。
- trx 1 提交。
- trx 2 提交。
其于以上假设，生成事务 ID 和事务提交号的流程如下：
- trx 1 生成事务 ID，得到 100。`trx_sys->next_trx_id_or_no` 加 1，结果为 101。
- trx 2 生成事务 ID，得到 101。`trx_sys->next_trx_id_or_no` 加 1，结果为 102。
- trx 1 生成事务提交号，得到 102。`trx_sys->next_trx_id_or_no` 加 1，结果为 103。
- trx 2 生成事务提交号，得到 103。`trx_sys->next_trx_id_or_no` 加 1，结果为 104。
从以上流程可以看到，事务 ID 和事务提交号都来源于 `trx_sys->next_trx_id_or_no`，相互之间不会重复。
### 2.3 修改 update undo 段状态
如果事务更新或删除了用户普通表的记录，InnoDB 会为事务分配一个 update undo 段。
如果事务更新或删除了用户临时表的记录，InnoDB 会为事务分配另一个 update undo 段。
InnoDB 可能会给事务分配 0 ~ 2 个 update undo 段。commit 子阶段会修改分配给事务的所有 update undo 段的状态。
如果 update undo 段满足缓存条件，它的状态会被修改为 `TRX_UNDO_CACHED`，否则，它的状态会被修改为 `TRX_UNDO_TO_PURGE`。
### 2.4 undo 日志组加入 history list
修改完 update undo 段的状态，update undo 段的 undo 日志组会加入回滚段的 `history list` 链表。purge 线程会从这个链表中获取要清理的 undo 日志组。
前面已经生成了事务提交号，这里会把事务提交号写入 undo 日志组的头信息中。
如果 update undo 段的状态为 `TRX_UNDO_CACHED`，表示这个 undo 段需要缓存起来。它会加入回滚段的 `update_undo_cached` 链表头部，以备后续其它事务需要 update undo 段时，能够快速分配。
## 3. InnoDB 提交事务完成
前面的一系列操作完成之后，InnoDB 提交事务的操作就完成了。
现在，要把事务状态修改为 `TRX_STATE_COMMITTED_IN_MEMORY`。
修改之后，新启动的事务就能看到该事务插入或更新的记录，看不到当前事务删除的记录。
接下来，InnoDB 会释放事务执行过程中加的表锁、记录锁。
释放锁之后，还要处理 insert undo 段。
如果 insert undo 段的状态为 `TRX_UNDO_CACHED`，表示这个 undo 段需要缓存起来。它会加入回滚段的 `insert_undo_cached` 链表头部，以备后续其它事物需要 insert undo 段时，能够快速分配。
如果 insert undo 段的状态为 `TRX_UNDO_TO_FREE`，它会被释放，占用的 undo 页会还给 undo 表空间。
二阶段提交的 flush 子阶段，已经把 prepare 阶段及之前产生的 redo 日志都刷盘了。
commit 子阶段，修改 insert undo 段和 update undo 段的状态，还会产生 redo 日志。
InnoDB 不会主动触发操作系统把这些 redo 日志刷盘，而是由操作系统决定什么时候把这些 redo 日志刷盘。
InnoDB 敢这么做，是因为这些 redo 日志对于确定事务状态已经不重要了。即使这些 redo 日志刷盘之前，服务器突然异常关机，导致 undo 段的状态丢失。MySQL 下次启动时，也能正确的识别到事务已经提交完成了。
## 4. 重新初始化事务对象
到这里，InnoDB 提交事务该做的操作都已经做完了。提交事务完成之后，该做的事也都做了。
对于上一个事务，事务对象的使命已经结束。这里会把事务状态修改为 `TRX_STATE_NOT_STARTED`。
事务对象也会被重新初始化，但是它不会被释放。也就是说，事务对象不会回到事务池中，而是留给当前连接后续启动新事务时复用。
## 5. 总结
InnoDB 提交事务，就像我们填完一个表格之后，最后盖上的那个戳，总体上来说，要干 3 件事。
**第 1 件**，修改分配给事务的各 undo 段的状态。
如果数据库发生崩溃，重新启动后，undo 段的状态是影响事务提交还是回滚的因素之一。
**第 2 件**，修改事务对象的状态。
如果数据据库一直运行，不发生崩溃，就靠事务对象的状态来标识事务是否已提交。
**第 3 件**，把各 undo 段中的 undo 日志组加入 `history list` 链表。
其它事务都不再需要使用这些 undo 日志时，后台 purge 线程会清理这些 undo 日志组中的日志。
> **本期问题**：关于本期内容，如有问题，欢迎留言交流。
**下期预告**：MySQL 核心模块揭秘 | 12 期 | 创建 savepoint