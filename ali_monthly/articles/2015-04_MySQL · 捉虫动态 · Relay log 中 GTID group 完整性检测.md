# MySQL · 捉虫动态 · Relay log 中 GTID group 完整性检测

**Date:** 2015/04
**Source:** http://mysql.taobao.org/monthly/2015/04/07/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2015 / 04
 ](/monthly/2015/04)

 * 当期文章

 MySQL · 引擎特性 · InnoDB undo log 漫游
* TokuDB · 产品新闻 · RDS TokuDB小手册
* TokuDB · 特性分析 · 行锁(row-lock)与区间锁(range-lock)
* PgSQL · 社区动态 · 说一说PgSQL 9.4.1中的那些安全补丁
* MySQL · 捉虫动态 · 连接断开导致XA事务丢失
* MySQL · 捉虫动态 · GTID下slave_net_timeout值太小问题
* MySQL · 捉虫动态 · Relay log 中 GTID group 完整性检测
* MySQL · 答疑释惑 · UPDATE交换列单表和多表的区别
* MySQL · 捉虫动态 · 删被引用索引导致crash
* MySQL · 答疑释惑 · GTID下auto_position=0时数据不一致

 ## MySQL · 捉虫动态 · Relay log 中 GTID group 完整性检测 
 Author: 襄洛 

 ## bug背景

官方 5.7.6 版本对 gtid 有非常多的改进和bugfix，其中有一个 bugfix 是针对 relay log 中没有接收完整的 gtid 事务的。正常的relay log 中的 gtid 事务应该是像下面这样：

1. gtid event
2. query event (begin)
3. row event (write/update/delete)
4. query event (commit)

上面这 4 个 event 序列构成一个 group。因为 IO 线程从主库接收 binlog 时，是以 event 为单位的，如果在 group 中间，比如3之后，stop slave 停掉IO线程的话，relay log 中就会记录一个不完整的事务。我们知道，GTID 的 auto_position 协议是通过计算主备库之间 GTID 集合的差集，然后来确定哪些 binlog 是要从主发给备的，备库用的集合就是 Retrieved_Gtid_Set 和 gtid_executed 的并集。IO 线程收到一个 gtid event 就会把它加入到 Retrieved_Gtid_Set 中，所以如果这个时候 start slave的话，最后这个不完整的事务是不会重新发送的，因为根据协议，主库认为备库已经有了这个事务，不需要再发送了。

## 修复分析

之所以会出现这种问题，是因为 IO 线程在处理的时候，没有将 gtid_event 和后面的事件序列当作一个整体来看待，只要收到开头的 gtid event，就认为整个 group 都已经收到。

所以官方的修复就是加一个事务边界检查器（Transaction_boundary_parser），只有当 IO 线程收到完整的 group，才将 gtid 加入到 Retrieved_Gtid_Set；同样在 mysqld 重启从 relay log 中初始化 Retrieved_Gtid_Set 时，也利用边界检查器判断 realy log 中的 gtid 事务是否完整。

下面就看下这个边界检查器是如何做判断的：

将 relay log 中的 event 序列分为2种，DDL 和 DML。

`DDL 序列如下：
 DDL-1: GTID event
 DDL-2: User_var/Intvar/Rand event
 DDL-3: Query event

DML 序列如下:
 DML-1: GTID event
 DML-2: Query event(BEGIN)
 DML-3: Query event(除了 BEGIN/COMMIT/ROLLBACK) / Rows event / load event)
 DML-4: (Query event (COMMIT) | Query event(ROLLBACK) | Xid)
`

然后定义了5种状态，标识目前读到的 event 事件是在事务内还是事务外。

1. EVENT_PARSER_NONE // 在事务外，这个时候应该是读完 DDL-3 或者 DML-4
2. EVENT_PARSER_GTID // 读到了GTID event，处于事务中，这个时候应该是读到 DDL-1 或者 DDL-3
3. EVENT_PARSER_DDL // 处于事务中，读到 DDL-2
4. EVENT_PARSER_DML // 处于事务中，读到 DML-2 或者 DML-3
5. EVENT_PARSER_ERROR // 错误状态

边界检查器的实现是一个状态机，根据目前所处的状态和读到的event，确定下一步应该转移到什么状态。

比如对于下面这样的 event 序列：

1. gtid
2. begin
3. update rows
4. commit

状态是这样转移的，刚开始是 EVENT_PARSER_NONE，读到事件1，转为 EVENT_PARSER_GTID 状态，读到事件2，转为 EVENT_PARSER_DML 状态，读到事件3，转为EVENT_PARSER_DML状态，读到事件4，转为 EVENT_PARSER_NONE 状态。从EVENT_PARSER_NONE（事务外）最终又到 EVENT_PARSER_NONE，中间读了一个完整的事务。
详细的状态转移规则可以看[官方patch](https://github.com/mysql/mysql-server/commit/9dab9dad975d09b8f37f33bf3c522d36fdf1d0f9)。

有了这个边界检测器后，IO 线程就能准确判断当前是处于事务外还是事务内，从而决定要不要把GTID添加到 Retrieved_Gtid_Set 中。

## 相关bug
对于 relay log 部分事务的问题，官方[之前有个patch](https://github.com/mysql/mysql-server/commit/e7a4cbe6a6449989e483d46abe79169f717a0725)，其逻辑是对 relay log 中最后一个 gtid 做特殊处理。在 request dump 的时候，如果这个 gtid 不在备库的 gtid_executed 集合中的话，就把这个 gtid 从发送给主库的 gtid 集合里去掉，这样主库就会把这个最后的 gtid 事务重新发过来；如果这个 gtid 已经在备库的 gtid_executed 集合中的话，就不从发送给主库的 gtid 集合里去掉，这样主库库就不会重发。

但是这种修复方式依赖于 gtid_executed，并不是根据事务是否完整来决定要不要重拉事务，所以有的场景下会有问题，如 [bug#72392](https://bugs.mysql.com/bug.php?id=72392) 这种场景。

官方目前这种用边界检测的修复方式是比较好的，但是可能会有性能上的问题，因为每个的 event 都要用边界检查器判断下，像 query event 需要要进行字符串比较。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)