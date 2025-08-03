# 07 期 | 二阶段提交 (1) prepare 阶段

**原文链接**: https://opensource.actionsky.com/07-%e6%9c%9f-%e4%ba%8c%e9%98%b6%e6%ae%b5%e6%8f%90%e4%ba%a4-1-prepare-%e9%98%b6%e6%ae%b5/
**分类**: 技术干货
**发布时间**: 2024-02-28T21:51:38-08:00

---

二阶段提交的 prepare 阶段，binlog 和 InnoDB 各自会有哪些动作？
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 二阶段提交
二阶段提交，顾名思义，包含两个阶段，它们是：
- prepare 阶段。
- commit 阶段。
我们只考虑 SQL 语句操作 InnoDB 表的场景，对于用户事务，是否使用二阶段提交，取决于是否开启了 binlog。
因为 MySQL 把 binlog 也看作一个存储引擎，开启 binlog，SQL 语句改变（插入、更新、删除）InnoDB 表的数据，这个 SQL 语句执行过程中，就涉及到两个存储引擎。
使用二阶段提交，就是为了保证两个存储引擎的数据一致性。
用户事务提交分为两种场景，如果开启了 binlog，它们都会使用二阶段提交。
**场景 1**：通过 BEGIN 或其它开始事务的语句，显式开始一个事务，用户手动执行 COMMIT 语句提交事务。
**场景 2**：没有显式开始的事务，一条 SQL 语句执行时，InnoDB 会隐式开始一个事务，SQL 语句执行完成之后，自动提交事务。
如果没有开启 binlog，SQL 语句改变表中数据，不产生 binlog，不用保证 binlog 和表中数据的一致性，用户事务也就不需要使用二阶段提交了。
InnoDB 内部事务是个特例，不管是否开启了 binlog，改变表中数据都不会产生 binlog 日志，所以内部事务不需要使用二阶段提交。
## 2. prepare 阶段
以下代码中，ha_prepare_low () 会调用 binlog 和 InnoDB 处理 prepare 逻辑的方法。
`int MYSQL_BIN_LOG::prepare(THD *thd, bool all) {
...
thd->durability_property = HA_IGNORE_DURABILITY;
...
int error = ha_prepare_low(thd, all);
...
}
`
调用 ha_prepare_low () 之前，用户线程对象的 `durability_property` 属性值会被设置为 `HA_IGNORE_DURABILITY`。
这个属性和 redo 日志刷盘有关，InnoDB prepare 会用到。
### 2.1 binlog prepare
binlog 被看作一种存储引擎，它也有 prepare 阶段，代码如下：
`// sql/binlog.cc
static int binlog_prepare(handlerton *, THD *thd, bool all) {
DBUG_TRACE;
if (!all) {
thd->get_transaction()->store_commit_parent(
mysql_bin_log.m_dependency_tracker.get_max_committed_timestamp());
}
return 0;
}
`
二阶段提交时，all = true，不会命中分支 `if (!all)`。也就是说，在 prepare 阶段，binlog 什么也不会干。
### 2.2 InnoDB prepare
二阶段提交的 prepare 阶段，InnoDB 主要做五件事。
**第 1 件**，把分配给事务的所有 undo 段的状态从 `TRX_UNDO_ACTIVE` 修改为 `TRX_UNDO_PREPARED`。
进入二阶段提交的事务，都至少改变过（插入、更新、删除）一个用户表的一条记录，最少会分配 1 个 undo 段，最多会分配 4 个 undo 段。
> 具体什么情况分配多少个 undo 段，后续关于 undo 模块的文章会有详细介绍。
不管 InnoDB 给事务分配了几个 undo 段，它们的状态都会被修改为 TRX_UNDO_PREPARED。
**第 2 件**，把事务 Xid 写入所有 undo 段中当前提交事务的 undo 日志组头信息。
InnoDB 给当前提交事务分配的每个 undo 段中，都会有一组 undo 日志属于这个事务，事务 Xid 就写入 undo 日志组的头信息。
对于第 1、2 件事，如果事务改变了用户普通表的数据，修改 undo 段状态、把事务 Xid 写入 undo 日志组头信息，都会产生 redo 日志。
**第 3 件**，把内存中的事务对象状态从 `TRX_STATE_ACTIVE` 修改为 `TRX_STATE_PREPARED`。
前面修改 undo 状态，是为了事务提交完成之前，MySQL 崩溃了，下次启动时，能够从 undo 段中恢复崩溃之前的事务状态。
这里修改事务对象状态，用于 MySQL 正常运行过程中，标识事务已经进入二阶段提交的 prepare 阶段。
**第 4 件**，如果当前提交事务的隔离级别是**读未提交**（`READ-UNCOMMITTED`）或**读已提交**（`READ-COMMITTED`)，InnoDB 会释放事务给记录加的共享、排他 GAP 锁。
虽然读未提交、读已提交隔离级别一般都只加普通记录锁，不加 GAP 锁，但是，外键约束检查、插入记录重复值检查这两个场景下，还是会给相应的记录加 GAP 锁。
**第 5 件**，调用 trx_flush_logs ()，处理 redo 日志刷盘的相关逻辑。
`static void trx_flush_logs(trx_t *trx, lsn_t lsn) {
...
switch (thd_requested_durability(trx->mysql_thd)) {
case HA_IGNORE_DURABILITY:
/* We set the HA_IGNORE_DURABILITY
during prepare phase of binlog group commit
to not flush redo log for every transaction here. 
So that we can flush prepared records
of transactions to redo log in a group
right before writing them to binary log
during flush stage of binlog group commit. */
break;
case HA_REGULAR_DURABILITY:
...
trx_flush_log_if_needed(lsn, trx);
}
}
`
从名字上看，trx_flush_logs () 的作用是把事务产生的 redo 日志刷盘。
前面介绍过，MYSQL_BIN_LOG::prepare () 调用 `ha_prepare_low()` 之前，就已经把当前事务所属用户线程对象的 `durability_property` 属性设置为 `HA_IGNORE_DURABILITY` 了。
从上面的代码可以看到，用户线程对象的 `durability_property` 属性值为 `HA_IGNORE_DURABILITY`，prepare 阶段并不会把 redo 日志刷盘。
## 3. 总结
开启 binlog 的情况下，用户事务需要使用二阶段提交来保证 binlog 和 InnoDB 表的数据一致性。
binlog prepare 什么也不会干。
InnoDB prepare 会把分配给事务的所有 undo 段的状态修改为 TRX_UNDO_PREPARED，把事务 Xid 写入 undo 日志组的头信息，把内存中事务对象的状态修改为 TRX_STATE_PREPARED。
> **本期问题**：二阶段提交的 prepare 阶段为什么不把 redo 日志刷盘？欢迎大家留言交流。
> **下期预告**：MySQL 核心模块揭秘 | 08 期 | 二阶段提交 (2) commit 阶段。