# 技术分享 | MySQL 备库可以设置 sync_binlog 非 1 吗？

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-mysql-%e5%a4%87%e5%ba%93%e5%8f%af%e4%bb%a5%e8%ae%be%e7%bd%ae-sync_binlog-%e9%9d%9e-1-%e5%90%97%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2024-07-30T01:04:35-08:00

---

众所周知，防止断电丢失 Binlog、故障恢复过程丢失数据，MySQL 主库必须设置 `sync_binlog=1`。那么作为备库可以例外吗？
> 作者：胡呈清，爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：[简书 | 轻松的鱼]，欢迎讨论。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 1200 字，预计阅读需要 4 分钟。
众所周知，防止断电丢失 Binlog、故障恢复过程丢失数据，MySQL 主库必须设置 `sync_binlog=1`。那么作为备库可以例外吗？
我们的第一反应当然是不行，既然主库会丢数据，备库自然一样。但其实不然，**备库丢了数据是可以重新从主库上复制的，只要这个复制的位置和备库本身数据的位置一致就 OK 了，它们能一致吗？**本文将对这个问题进行讨论。
## 背景知识
为了更好的说明这个问题，下面赘述一下相关的知识点：
- InnoDB 的二阶段提交中，Prepare 阶段写 Redo Log，Commit 阶段写 Binlog，故障恢复时保证：
所有已提交事务的 Binlog 一定存在。
- 所有未提交事务一定不记录 Binlog。
- 备库设置 `relay_log_info_repository = table` 时，`slave_relay_log_info`（即备库回放位置）的更新与 Relay Log 回放的 SQL 在同一个事务中提交。
- GTID 持久化在 Binlog 中，备库在某些条件下启动复制时会从 *Executed_Gtid_Set* 开始到主库复制数据。
根据以上 3 点，备库如果设置 `sync_binlog` 不为 1，在做故障恢复时的就会发生以下情况。
- **事务状态：TRX_COMMITTED_IN_MEMORY、TRX_NOT_STARTED。**如果 Binlog 未落盘，事务会重做，数据将比 Binlog 多，`slave_relay_log_info` 表记录的复制位置也将领先 `Executed_Gtid_Set`。
- **事务状态：TRX_PREPARED。** 由于Binlog 未刷盘，Recovery 时会回滚事务，数据与 Binlog 是一致的，`slave_relay_log_info` 表记录的复制位置等于 *Executed_Gtid_Set*。
如果备库断电恢复后，启动复制时用的位置由 `slave_relay_log_info 决定`，则备库数据还是能正常复制数据，并且能与主库保持一致，只是 GTID 会出现跳号。
反之如果由 *Executed_Gtid_Set* 决定，则备库复制会因为重复回放事务而报错，需要进行修复。下面设计一个实验来进行验证。
## 实验过程
#### 1. 设置备库参数并制造“故障”
备库参数设置如下，主库用工具并发写入数据（这里用的 *mysqlslap*），然后备库强制关机（`reboot -f`）。
`sync_binlog = 1000
innodb_flush_log_at_trx_commit = 1
relay_log_info_repository = table  ##slave_relay_log_info 表为 innodb 表
relay_log_recovery = on
gtid_mode = on
`
#### 2. 重启备库
备库服务器开机后重启 MySQL，查看的信息如下。
`show master status 输出的 Executed_Gtid_Set 如下：
fb9b7d78-6eb5-11ec-985a-0242ac101704:1-167216 
mysql> select * from slave_relay_log_info\G
*************************** 1. row ***************************
Number_of_lines: 7
Relay_log_name: ./localhost-relay-bin.000004
Relay_log_pos: 4
Master_log_name: mysql-bin.000001
Master_log_pos: 48159613
Sql_delay: 0
Number_of_workers: 0
Id: 1
Channel_name:
1 row in set (0.00 sec)
`
根据输出内容可知，从库的数据确实回放到了 `mysql-bin.000001:48159613`，对应的 GTID 为：`fb9b7d78-6eb5-11ec-985a-0242ac101704:167222`，
只是从库的 Binlog 有丢失，GTID 为：`fb9b7d78-6eb5-11ec-985a-0242ac101704:1-167216`。
`...
SET @@SESSION.GTID_NEXT= 'fb9b7d78-6eb5-11ec-985a-0242ac101704:167222'/*!*/;
...
### INSERT INTO `mysqlslap`.`t`
### SET
###   @1=167216 /* INT meta=0 nullable=0 is_null=0 */
# at 48159586
#220407 14:10:34 server id 123456  end_log_pos 48159613         Xid = 169239
COMMIT/*!*/;
# at 48159613
...
`
从库已经有 167222 事务对应的数据。
`mysql> select * from t where id=167216;
+--------+
| id     |
+--------+
| 167216 |
+--------+
1 row in set (0.00 sec)
`
#### 3. 备库启动复制
Error Log 显示的起始位置和 `slave_relay_log_info` 内容一样，从主库的 `mysql-bin.000001:48159613` 开始，对应 GTID 为 167222+1。
> Slave I/O thread: Start asynchronous replication to master &#8216;repl@10.186.61.32:3308&#8217; in log &#8216;mysql-bin.000001&#8217; at position 48159613
但接下来 SQL 线程报错位置却是 `mysql-bin.000001:48158146`，比开始位置还靠前，这个位置对应的 GTID 为 167217（即167216+1）：
> 2022-04-07T06:33:18.611181-00:00 4 [ERROR] Slave SQL for channel &#8221;: Could not execute Write_rows event on table mysqlslap.t; Duplicate entry &#8216;167212&#8217; for key &#8216;PRIMARY&#8217;, Error_code: 1062; handler error HA_ERR_FOUND_DUPP_KEY; the event&#8217;s master log mysql-bin.000001, end_log_pos 48158146, Error_code: 1062
而且解析从库 Relay Log（因为设置了 `relay_log_recovery = on`，启动复制时会丢弃旧的未 Relay Log 重新到主库取 Binlog），第一个事务也是 `SET @@SESSION.GTID_NEXT= 'fb9b7d78-6eb5-11ec-985a-0242ac101704:167217'/*!*/;`，而不是 167223。这说明了启动复制的位置并不是 `slave_relay_log_info` 记录的位置，而是从库的 GTID。
#### 4. 重复以上测试
在启动从库复制前执行 `change master to master_auto_position=0;` 这回不报错，是从 167223 这个 GTID 开始复制数据，从库 GTID 会出现跳号。
`mysql> show master status;
+------------------+----------+--------------+------------------+-------------------------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                                           |
+------------------+----------+--------------+------------------+-------------------------------------------------------------+
| mysql-bin.000006 |  9976340 |              |                  | fb9b7d78-6eb5-11ec-985a-0242ac101704:1-167216:167223-200670 |
+------------------+----------+--------------+------------------+-------------------------------------------------------------+
1 row in set (0.01 sec)
`
## 结论
从库 `sync_binlog` 设置不为 1，发生断电会丢失 Binlog，因为 GTID 持久化在 Binlog 中，因此也会丢失 GTID。但是数据和 `slave_relay_log_info` 表中保存的 SQL 线程回放位置一致。
此时：
- 如果 `master_auto_position=0`，则从库重启复制时可以从正确的位置开始复制数据，从而与主库数据一致。不过从库会产生 GTID 跳号。
- 如果 `master_auto_position=1`，则从库重启复制时会从 GTID 处开始复制数据，由于 GTID 有丢失，所以会重复回放事务，产生报错。