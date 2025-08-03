# 新特性解读 | MySQL 8.0 对 GTID 的限制解除

**原文链接**: https://opensource.actionsky.com/20220713-mysql8-0/
**分类**: MySQL 新特性
**发布时间**: 2022-07-12T23:43:33-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
在 MySQL 5.6 以及MySQL 5.7 上使用 GTID ，一直以来都有几个硬性限制，特别是针对开发人员编写 SQL 的两条限制，官方文档对这两条限制详细描述如下：
> **CREATE TABLE &#8230; SELECT statements.** [`CREATE TABLE ... SELECT`](https://dev.mysql.com/doc/refman/5.7/en/create-table-select.html) statements are not allowed when using GTID-based replication. When [`binlog_format`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_binlog_format) is set to STATEMENT, a `CREATE TABLE ... SELECT` statement is recorded in the binary log as one transaction with one GTID, but if ROW format is used, the statement is recorded as two transactions with two GTIDs. If a source used STATEMENT format and a replica used ROW format, the replica would be unable to handle the transaction correctly, therefore the `CREATE TABLE ... SELECT` statement is disallowed with GTIDs to prevent this scenario.
**Temporary tables.** [`CREATE TEMPORARY TABLE`](https://dev.mysql.com/doc/refman/5.7/en/create-table.html) and [`DROP TEMPORARY TABLE`](https://dev.mysql.com/doc/refman/5.7/en/drop-table.html) statements are not supported inside transactions, procedures, functions, and triggers when using GTIDs (that is, when the [`enforce_gtid_consistency`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency) system variable is set to `ON`). It is possible to use these statements with GTIDs enabled, but only outside of any transaction, and only with [`autocommit=1`](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_autocommit).
以上大概意思讲的是对于这两条 SQL 语句，如果想在 GTID 模式下使用，为了不破坏事务一致性，是被严格限制而不允许使用的。 为了满足需求，一般我们会通过一些途径来绕过这些限制。这个硬性限制随着 MySQL 8.0 一些新特性的发布，连带着被间接取消掉。比如 MySQL 8.0 的 DDL 原子性！
##### 我们先来看下在 MySQL 5.7 下这一行为对事务的影响以及如何通过变通的方法绕过这些限制。
- create table &#8230; select &#8230; : 这条语句本身是懒人写法，语义上分别属于两个隐式事务（一条DDL语句，一条DML语句）。但在GTID开启后，单个语句只能给它分配一个GTID事务号，如果强制使用，会直接报语句违反GTID一致性。比如下面例子：直接执行这条语句就会报错。
mysql:ytt:5.7.34-log> create table trans1(id int primary key, log_date date);
Query OK, 0 rows affected (0.03 sec)
<mysql:ytt:5.7.34-log> insert trans1 values (1,'2022-01-02');
Query OK, 1 row affected (0.00 sec)
<mysql:ytt:5.7.34-log> create table trans2 as select * from trans1;
ERROR 1786 (HY000): Statement violates GTID consistency: CREATE TABLE ... SELECT.
既然理解了需求，就想办法变通下。针对这条语句，拆分为两条语句即可。
需要注意的是拆分后第一条 DDL 语句的后续工作，是延迟建立索引还是根本不需要索引？如果是延迟建立索引，那很简单，使用 MySQL 的 create table &#8230; like &#8230; 语法就行。虽然 create table &#8230; like &#8230; 语法是直接克隆原表，索引也是立即创建，不过最终目标是一致的。示例如下：
<mysql:ytt:5.7.34-log> reset master;
Query OK, 0 rows affected (0.02 sec)
mysql:ytt:5.7.34-log> create table trans2 like trans1;
Query OK, 0 rows affected (0.02 sec)
<mysql:ytt:5.7.34-log> insert trans2 select * from trans1;
Query OK, 1 row affected (0.02 sec)
Records: 1  Duplicates: 0  Warnings: 0
对应的 binlog 数据如下，拆分为两个 GTID 事务号：00020135-1111-1111-1111-111111111111:1-2
<mysql:ytt:5.7.34-log> show binlog events in 'mysql-bin.000001'\G
*************************** 1. row ***************************
...
*************************** 3. row ***************************
Log_name: mysql-bin.000001
Pos: 154
Event_type: Gtid
Server_id: 100
End_log_pos: 219
Info: SET @@SESSION.GTID_NEXT= '00020135-1111-1111-1111-111111111111:1'
*************************** 4. row ***************************
Log_name: mysql-bin.000001
Pos: 219
Event_type: Query
Server_id: 100
End_log_pos: 316
Info: use `ytt`; create table trans2 like trans1
*************************** 5. row ***************************
Log_name: mysql-bin.000001
Pos: 316
Event_type: Gtid
Server_id: 100
End_log_pos: 381
Info: SET @@SESSION.GTID_NEXT= '00020135-1111-1111-1111-111111111111:2'
*************************** 6. row ***************************
Log_name: mysql-bin.000001
Pos: 381
Event_type: Query
Server_id: 100
End_log_pos: 452
Info: BEGIN
*************************** 7. row ***************************
Log_name: mysql-bin.000001
Pos: 452
Event_type: Table_map
Server_id: 100
End_log_pos: 501
Info: table_id: 112 (ytt.trans2)
*************************** 8. row ***************************
Log_name: mysql-bin.000001
Pos: 501
Event_type: Write_rows
Server_id: 100
End_log_pos: 552
Info: table_id: 112 flags: STMT_END_F
*************************** 9. row ***************************
Log_name: mysql-bin.000001
Pos: 552
Event_type: Xid
Server_id: 100
End_log_pos: 583
Info: COMMIT /* xid=54 */
9 rows in set (0.00 sec)
如果是后一种，只需要复制表结构和数据，不要索引，那也可以用 create table &#8230; like &#8230; 语法创建好表结构，完了手工删除表索引。如果表比较多，可以写个简单脚本对索引批量删除。
- 对于显式临时表的创建与删除： 这样的 DDL 语句在 GTID 模式下也是禁止放在事务块里执行的（显式的 begin; commit; 或者存储过程、存储函数、触发器等大事务块）。 直接在事务块里执行会报错：
<mysql:ytt:5.7.34-log> begin;
Query OK, 0 rows affected (0.00 sec)
<mysql:ytt:5.7.34-log> create temporary table tmp(id int);
ERROR 1787 (HY000): Statement violates GTID consistency: CREATE TEMPORARY TABLE and DROP TEMPORARY TABLE can only be executed outside transactional context.  These statements are also not allowed in a function or trigger because functions and triggers are also considered to be multi-statement transactions.
这种如何解决呢？官方也给出建议：把此类 DDL 语句放在事务块外面或者直接使用基于磁盘表的 DDL 语句来替代它。比如下面示例：在事务块外创建临时表，事务块内部引用临时表数据就行。
<mysql:ytt:5.7.34-log> create temporary table tmp(id int,log_date date);
Query OK, 0 rows affected (0.00 sec)
<mysql:ytt:5.7.34-log> begin;
Query OK, 0 rows affected (0.01 sec)
<mysql:ytt:5.7.34-log> insert tmp values (100,'2022-10-21');
Query OK, 1 row affected (0.01 sec)
<mysql:ytt:5.7.34-log> insert trans1 select * from tmp;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0
<mysql:ytt:5.7.34-log> commit;
Query OK, 0 rows affected (0.00 sec)
<mysql:ytt:5.7.34-log> select * from trans1;
+-----+------------+
| id  | log_date   |
+-----+------------+
|   1 | 2022-01-02 |
| 100 | 2022-10-21 |
+-----+------------+
2 rows in set (0.00 sec)
##### MySQL 8.0 原生 DDL 原子性，所以连带就解除了这两个 GTID 的限制。
- 对于 create table &#8230; like &#8230; 语句，在 MySQL 8.0 版本里只会生成一个 GTID 事务号，见下面 binlog 内容：0228ca56-db2f-11ec-83d3-080027951c4a:1。
mysql:ytt:8.0.29>create table trans2 as select * from trans1;
Query OK, 1 row affected (0.08 sec)
Records: 1  Duplicates: 0  Warnings: 0
<mysql:ytt:8.0.29>show binlog events in 'binlog.000001'\G
*************************** 1. row ***************************
...
*************************** 3. row ***************************
Log_name: binlog.000001
Pos: 157
Event_type: Gtid
Server_id: 1
End_log_pos: 236
Info: SET @@SESSION.GTID_NEXT= '0228ca56-db2f-11ec-83d3-080027951c4a:1'
*************************** 4. row ***************************
Log_name: binlog.000001
Pos: 236
Event_type: Query
Server_id: 1
End_log_pos: 310
Info: BEGIN
*************************** 5. row ***************************
Log_name: binlog.000001
Pos: 310
Event_type: Query
Server_id: 1
End_log_pos: 476
Info: use `ytt`; CREATE TABLE `trans2` (
`id` int NOT NULL,
`log_date` date DEFAULT NULL
) START TRANSACTION
*************************** 6. row ***************************
Log_name: binlog.000001
Pos: 476
Event_type: Table_map
Server_id: 1
End_log_pos: 528
Info: table_id: 349 (ytt.trans2)
*************************** 7. row ***************************
Log_name: binlog.000001
Pos: 528
Event_type: Write_rows
Server_id: 1
End_log_pos: 571
Info: table_id: 349 flags: STMT_END_F
*************************** 8. row ***************************
Log_name: binlog.000001
Pos: 571
Event_type: Xid
Server_id: 1
End_log_pos: 602
Info: COMMIT /* xid=8833 */
8 rows in set (0.00 sec)
- 对于事务块里有显式临时表的 DDL 语句，可以正常执行：
<mysql:ytt:8.0.29>reset master;
Query OK, 0 rows affected (0.02 sec)
<mysql:ytt:8.0.29>begin;
Query OK, 0 rows affected (0.01 sec)
<mysql:ytt:8.0.29>create temporary table tmp(a int,b date);
Query OK, 0 rows affected (0.00 sec)
<mysql:ytt:8.0.29>insert into tmp values (10,'2022-12-31');
Query OK, 1 row affected (0.00 sec)
<mysql:ytt:8.0.29>insert trans1 select * from tmp;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0
<mysql:ytt:8.0.29>commit;
Query OK, 0 rows affected (0.01 sec)
<mysql:ytt:8.0.29>table trans1;
+----+------------+
| id | log_date   |
+----+------------+
|  1 | 2022-07-07 |
| 10 | 2022-12-31 |
+----+------------+
2 rows in set (0.00 sec)
这样生成的 GTID 事务号里（0228ca56-db2f-11ec-83d3-080027951c4a:1）只包含对磁盘表 trans1 的写入记录：
mysql:ytt:8.0.29>show binlog events in 'binlog.000001'\G
*************************** 1. row ***************************
...
*************************** 3. row ***************************
Log_name: binlog.000001
Pos: 157
Event_type: Gtid
Server_id: 1
End_log_pos: 236
Info: SET @@SESSION.GTID_NEXT= '0228ca56-db2f-11ec-83d3-080027951c4a:1'
*************************** 4. row ***************************
Log_name: binlog.000001
Pos: 236
Event_type: Query
Server_id: 1
End_log_pos: 310
Info: BEGIN
*************************** 5. row ***************************
Log_name: binlog.000001
Pos: 310
Event_type: Table_map
Server_id: 1
End_log_pos: 362
Info: table_id: 405 (ytt.trans1)
*************************** 6. row ***************************
Log_name: binlog.000001
Pos: 362
Event_type: Write_rows
Server_id: 1
End_log_pos: 405
Info: table_id: 405 flags: STMT_END_F
*************************** 7. row ***************************
Log_name: binlog.000001
Pos: 405
Event_type: Xid
Server_id: 1
End_log_pos: 436
Info: COMMIT /* xid=9374 */
7 rows in set (0.00 sec)
MySQL 8.0 已经发布好几年了，如果有需要这部分的功能改善，建议升级新版本。