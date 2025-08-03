# 08 期 | 二阶段提交 (2) commit 阶段

**原文链接**: https://opensource.actionsky.com/08-%e6%9c%9f-%e4%ba%8c%e9%98%b6%e6%ae%b5%e6%8f%90%e4%ba%a4-2-commit-%e9%98%b6%e6%ae%b5/
**分类**: 技术干货
**发布时间**: 2024-03-08T01:34:15-08:00

---

这篇文章是二阶段提交的 commit 子阶段的前奏，聊聊 commit 子阶段相关的一些概念。
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 刷盘这件事
操作系统为文件提供了缓冲区，称为 `page cache`。
程序写入内容到磁盘文件，实际上是先写入 page cache，再由操作系统把 page cache 中的内容写入磁盘文件。
把 page cache 中的内容写入磁盘文件这个操作，我们通常口语化的称为**刷盘**。
刷盘有两种方式：
- 一种是操作系统的后台线程异步刷盘。
- 另一种是程序主动触发操作系统的同步刷盘。
## 2. commit 阶段
二阶段提交的 commit 阶段，分为三个子阶段。
**flush 子阶段**，要干两件事：
`第 1 件`，触发操作系统把 prepare 阶段及之前产生的 redo 日志刷盘。
事务执行过程中，改变（插入、更新、删除）表中数据产生的 redo 日志、prepare 阶段修改 undo 段状态产生的 redo 日志，都会由后台线程先写入 page cache，再由操作系统把 page cache 中的 redo 日志刷盘。
等待操作系统把 page cache 中的 redo 日志刷盘，这个时间存在不确定性，InnoDB 会在需要时主动触发操作系统马上把 page cache 中的 redo 日志刷盘。
上一篇文章，我们介绍过，二阶段提交的 prepare 阶段不会主动触发操作系统把 page cache 中的 redo 日志刷盘。这个刷盘操作会留到 flush 子阶段进行。
`第 2 件`，把事务执行过程中产生的 binlog 日志写入 binlog 日志文件。
这个写入操作，也是先写入 page cache，至于操作系统什么时候把 page cache 中的 binlog 日志刷盘，flush 子阶段就不管了。
**sync 子阶段**，根据系统变量 sync_binlog 的值决定是否要触发操作系统马上把 page cache 中的 binlog 日志刷盘。
**commit 子阶段**，完成 InnoDB 的事务提交。
## 3. 组提交
flush 子阶段会触发 redo 日志刷盘，sync 子阶段`可能`会触发 binlog 日志刷盘，都涉及到磁盘 IO。
TP 场景，`比较常见`的情况是事务只改变（插入、更新、删除）表中少量数据，产生的 redo 日志、binlog 日志也比较少。
我们把这种事务称为`小事务`。
以 redo 日志为例，一个事务产生的 redo 日志少，操作系统的一个页就有可能存放多个事务产生的 redo 日志。
如果每个事务提交时都把自己产生的 redo 日志刷盘，共享操作系统同一个页存放 redo 日志的多个事务，就会触发操作系统把这个页多次刷盘。
数据库闲的时候，把操作系统的同一个页多次刷盘，也没啥问题，反正磁盘闲着也是闲着。
数据库忙的时候，假设某个时间点有 1 万个小事务要提交，每 10 个小事务共享操作系统的一个页用于存放 redo 日志，总共需要操作系统的 1000 个页。
1 万个事务各自提交，就要触发操作系统把这 1000 个数据页刷盘 10000 次。
根据上面假设的这个场景，我们可以看到，这些事务都在某个时间点提交，可以等到共享操作系统同一个页的事务把 redo 日志都写入到 page cache 之后，再触发操作系统把 page cache 的这一个页刷盘。
这样一来，1000 个数据页，只刷盘 1000 次就可以了，刷盘次数只有原来的十分之一，效率大大的提高了。
上面是以 redo 日志为例描述操作系统的同一个页重复刷盘的问题，binlog 日志也有同样的问题。
某个时间点提交的多个事务触发操作系统的同一个页重复刷盘，这是个问题，为了解决这个问题，InnoDB 引入了**组提交**。
## 4. 队列和互斥量
组提交，就是把一组事务攒到一起提交，InnoDB 使用**队列**把多个事务攒到一起。
commit 阶段的 3 个子阶段都有自己的队列，分别为 flush 队列、sync 队列、commit 队列。
每个队列都会选出一个队长，负责管理这个队列，选队长的规则很简单，先到先得。
对于每个队列，第一个加入该队列的用户线程就是**队长**，第二个及以后加入该队列的都是**队员**。
> 代码里把队长称为 `leader`，队员称为 `follower`。
我们生活中，不管当什么级别的队长，总会有点什么不一样，比如：有点钱、有点权、有点面子。
当选队长的用户线程，会有什么不一样吗？
这个当然是有的，队长有个特权，就是**多干活**。
每个子阶段的队长，都会把自己和所有队员在对应子阶段要干的事全都干了。队员只需要在旁边当吃瓜群众就好。
> commit 子阶段有点不一样，到时候会介绍。
以 flush 子阶段为例，我们假设 flush 队列的队长为 `A 队长`，A 队长收编一些队员之后，它会带领这帮队员从 flush 队列挪走，并且开始给自己和所有队员干活，队员们就在一旁当吃瓜群众。
A 队长带领它的队员挪走之后，flush 队列就变成空队列了。
接下来第一个进入 flush 队列的用户线程，又成为下一组的队长，我们称它为 `B 队长`。
A 队长正在干活，还没干完呢。B 队长收编了一些队员之后，也带领这帮队员从 flush 子阶段的队列挪走，并且也要开始给自己和所有队员干活了。
如果 A 队长和 B 队长都把自己和各自队员产生的 binlog 日志写入 binlog 日志文件，相互交叉写入，那是会出乱子的。
为了避免 flush 子阶段出现两个队长同时干活导致出乱子，InnoDB 给 flush 子阶段引入了一个互斥量，名字是 `LOCK_log`。
sync 子阶段、commit 子阶段也需要避免出现多个队长同时干活的情况，这两个子阶段也有各自的互斥量，分别是 `LOCK_sync`、`LOCK_commit`。
## 5. 总结
二阶段提交的 commit 阶段分为三个子阶段：flush 子阶段、sync 子阶段、commit 子阶段。
flush 子阶段会把 prepare 阶段及之前产生的 redo 日志都刷盘，把事务执行过程中产生的 binlog 日志写入 binlog 日志文件。
sync 子阶段会根据系统变量 sync_binlog 的值决定是否把 binlog 日志刷盘。
为了避免每个事务各自提交，触发操作系统对同一个页频繁的重复刷盘，InnoDB 引入了组提交。
为了避免每个子阶段出现多个队长同时干活的情况，InnoDB 还引入了三个互斥量：LOCK_log、LOCK_sync、LOCK_commit。
> **本期问题**：关于本期内容，如有问题，欢迎留言交流。
**下期预告**：MySQL 核心模块揭秘 | 09 期 | 二阶段提交 (3) flush、sync、commit 子阶段。
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
以下代码中，ha_prepare_low() 会调用 binlog 和 InnoDB 处理 prepare 逻辑的方法。
`int MYSQL_BIN_LOG::prepare(THD *thd, bool all) {
...
thd->durability_property = HA_IGNORE_DURABILITY;
...
int error = ha_prepare_low(thd, all);
...
}
`
调用 ha_prepare_low() 之前，用户线程对象的 `durability_property` 属性值会被设置为 `HA_IGNORE_DURABILITY`。
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
二阶段提交时，all = true，不会命中分支 `if (!all)`。也就是说，在 prepare 阶段，binlog 什么也不会干。
### 2.2 InnoDB prepare
二阶段提交的 prepare 阶段，InnoDB 主要做五件事。
**第 1 件**，把分配给事务的所有 undo 段的状态从 `TRX_UNDO_ACTIVE` 修改为 `TRX_UNDO_PREPARED`。
进入二阶段提交的事务，都至少改变过（插入、更新、删除）一个用户表的一条记录，最少会分配 1 个 undo 段，最多会分配 4 个 undo 段。
> 具体什么情况分配多少个 undo 段，后续关于 undo 模块的文章会有详细介绍。
不管 InnoDB 给事务分配了几个 undo 段，它们的状态都会被修改为 TRX_UNDO_PREPARED。
**第 2 件**，把事务 Xid 写入所有 undo 段中当前提交事务的 undo 日志组头信息。
InnoDB 给当前提交事务分配的每个 undo 段中，都会有一组 undo 日志属于这个事务，事务 Xid 就写入 undo 日志组的头信息。
对于第 1、2 件事，如果事务改变了用户普通表的数据，修改 undo 段状态、把事务 Xid 写入 undo 日志组头信息，都会产生 redo 日志。
**第 3 件**，把内存中的事务对象状态从 `TRX_STATE_ACTIVE` 修改为 `TRX_STATE_PREPARED`。
前面修改 undo 状态，是为了事务提交完成之前，MySQL 崩溃了，下次启动时，能够从 undo 段中恢复崩溃之前的事务状态。
这里修改事务对象状态，用于 MySQL 正常运行过程中，标识事务已经进入二阶段提交的 prepare 阶段。
**第 4 件**，如果当前提交事务的隔离级别是**读未提交**（`READ-UNCOMMITTED`）或**读已提交**（`READ-COMMITTED`)，InnoDB 会释放事务给记录加的共享、排他 GAP 锁。
虽然读未提交、读已提交隔离级别一般都只加普通记录锁，不加 GAP 锁，但是，外键约束检查、插入记录重复值检查这两个场景下，还是会给相应的记录加 GAP 锁。
**第 5 件**，调用 trx_flush_logs()，处理 redo 日志刷盘的相关逻辑。
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
从名字上看，trx_flush_logs() 的作用是把事务产生的 redo 日志刷盘。
前面介绍过，MYSQL_BIN_LOG::prepare() 调用 `ha_prepare_low()` 之前，就已经把当前事务所属用户线程对象的 `durability_property` 属性设置为 `HA_IGNORE_DURABILITY` 了。
从上面的代码可以看到，用户线程对象的 `durability_property` 属性值为 `HA_IGNORE_DURABILITY`，prepare 阶段并不会把 redo 日志刷盘。
## 3. 总结
开启 binlog 的情况下，用户事务需要使用二阶段提交来保证 binlog 和 InnoDB 表的数据一致性。
binlog prepare 什么也不会干。
InnoDB prepare 会把分配给事务的所有 undo 段的状态修改为 TRX_UNDO_PREPARED，把事务 Xid 写入 undo 日志组的头信息，把内存中事务对象的状态修改为 TRX_STATE_PREPARED。
> **本期问题**：二阶段提交的 prepare 阶段为什么不把 redo 日志刷盘？欢迎大家留言交流。
**下期预告**：MySQL 核心模块揭秘 | 08 期 | 二阶段提交 (2) commit 阶段。