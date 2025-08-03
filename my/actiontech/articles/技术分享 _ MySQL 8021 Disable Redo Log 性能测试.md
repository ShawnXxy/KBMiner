# 技术分享 | MySQL 8.0.21 Disable Redo Log 性能测试

**原文链接**: https://opensource.actionsky.com/20200727-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-07-29T00:57:24-08:00

---

作者：洪斌
爱可生南区负责人兼技术服务总监，MySQL  ACE，擅长数据库架构规划、故障诊断、性能优化分析，实践经验丰富，帮助各行业客户解决 MySQL 技术问题，为金融、运营商、互联网等行业客户提供 MySQL 整体解决方案。
本文来源：转载自公众号-玩转MySQL
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
记得 5 年前我们在某银行客户做大数据量 load data 测试时，为了能在要求的时间内完成数据加载，尽管优化了各种参数，但还是避免不了在日志的 IO 开销。在商业数据库 DB2、Oracle 都有 nologging table 功能，对于有大量数据加载需求的系统，就可以不记录日志，减少 IO 的开销。这对用惯了商业数据库的用户来说，首测尝试开源数据库，感觉各种不适应。最后只好拆分更多实例，增加并行度来提高 load data 效率，来满足时效性要求。MySQL 一直在改善自身的扩展性，这对于企业级数据库是必须的，不能仅靠拆分打天下，一味的拆分使用体验太差，也会阻碍用户大规模使用，维护分布式架构的复杂性远比集中式复杂的多。昨天发布的 MySQL 8.0.21 ，我们看到了 disable redo log 功能，这对 load data 场景太有吸引力了，我们简单测试下看实际效果如何。
**简单对比测试**
对比禁用与启用 redo log 两种场景下的执行效率，处理 100w 记录（1.8G）文件，sysbench 标准表结构。
![](https://opensource.actionsky.com/wp-content/uploads/2020/07/表格.png)											
**从实际测试情况来看，禁用与启用 redo log 有 10%~30% 的执行时间差异。**
禁用 redo log load data- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql [localhost:8021] {msandbox} (test) > ALTER INSTANCE DISABLE INNODB REDO_LOG;``Query OK, 0 rows affected (0.10 sec)``
``mysql [localhost:8021] {msandbox} (test) > load data infile 'sbtest.txt' into table sbtest1;``Query OK, 10000000 rows affected (2 min 39.66 sec)``Records: 10000000  Deleted: 0  Skipped: 0  Warnings: 0``
``mysql [localhost:8021] {msandbox} (test) > truncate sbtest1;``Query OK, 0 rows affected (0.36 sec)``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=0;set global innodb_flush_log_at_trx_commit=0;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``mysql [localhost:8021] {msandbox} (test) > load data infile 'sbtest.txt' into table sbtest1;``Query OK, 10000000 rows affected (2 min 30.61 sec)``Records: 10000000  Deleted: 0  Skipped: 0  Warnings: 0`
启用 redo log load data
****- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql [localhost:8021] {msandbox} (test) > ALTER INSTANCE ENABLE INNODB REDO_LOG;``Query OK, 0 rows affected (0.09 sec)``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=1;set global innodb_flush_log_at_trx_commit=1;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > load data infile 'sbtest.txt' into table sbtest1;``Query OK, 10000000 rows affected (3 min 37.55 sec)``Records: 10000000  Deleted: 0  Skipped: 0  Warnings: 0``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=0;set global innodb_flush_log_at_trx_commit=0;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > truncate sbtest1;``Query OK, 0 rows affected (0.34 sec)``
``mysql [localhost:8021] {msandbox} (test) > load data infile 'sbtest.txt' into table sbtest1;``Query OK, 10000000 rows affected (2 min 49.84 sec)``Records: 10000000  Deleted: 0  Skipped: 0  Warnings: 0`
禁用 redo log add index
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql [localhost:8021] {msandbox} (test) > ALTER INSTANCE DISABLE INNODB REDO_LOG;``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=1;set global innodb_flush_log_at_trx_commit=1;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > alter table sbtest1 add index idx_c(c);``Query OK, 0 rows affected (38.96 sec)``Records: 0  Duplicates: 0  Warnings: 0``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=0;set global innodb_flush_log_at_trx_commit=0;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > alter table sbtest1 drop index idx_c;``Query OK, 0 rows affected (0.05 sec)``Records: 0  Duplicates: 0  Warnings: 0``
``mysql [localhost:8021] {msandbox} (test) > alter table sbtest1 add index idx_c(c);``Query OK, 0 rows affected (35.13 sec)``Records: 0  Duplicates: 0  Warnings: 0`
启用 redo log add index
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql [localhost:8021] {msandbox} (test) > ALTER INSTANCE ENABLE INNODB REDO_LOG;``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=1;set global innodb_flush_log_at_trx_commit=1;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > alter table sbtest1 add index idx_c(c);``Query OK, 0 rows affected (47.05 sec)``Records: 0  Duplicates: 0  Warnings: 0``
``mysql [localhost:8021] {msandbox} (test) > set global sync_binlog=0;set global innodb_flush_log_at_trx_commit=0;``Query OK, 0 rows affected (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)``
``mysql [localhost:8021] {msandbox} (test) > alter table sbtest1 drop index idx_c;``Query OK, 0 rows affected (0.00 sec)``Records: 0  Duplicates: 0  Warnings: 0``
``mysql [localhost:8021] {msandbox} (test) > alter table sbtest1 add index idx_c(c);``Query OK, 0 rows affected (47.32 sec)``Records: 0  Duplicates: 0  Warnings: 0`
**总结一下**
- 禁用 redo log 不影响 binlog 功能，可以正常同步。
- 禁用 redo log 是实例级，不支持表级。
- 禁用 redo log 若发生 crash 是无法 recovery 的，OLTP 系统谨慎使用。
- 适用于大量数据导入场景。