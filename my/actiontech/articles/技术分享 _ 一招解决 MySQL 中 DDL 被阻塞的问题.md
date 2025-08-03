# 技术分享 | 一招解决 MySQL 中 DDL 被阻塞的问题

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e4%b8%80%e6%8b%9b%e8%a7%a3%e5%86%b3-mysql-%e4%b8%ad-ddl-%e8%a2%ab%e9%98%bb%e5%a1%9e%e7%9a%84%e9%97%ae%e9%a2%98/
**分类**: MySQL 新特性
**发布时间**: 2023-05-17T00:53:12-08:00

---

作者：许祥
爱可生 MySQL DBA 团队成员，负责处理客户 MySQL 及我司自研 DMP 平台日常运维中的问题。
本文来源：原创投稿
* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 背景
之前碰到客户咨询定位 DDL 阻塞的相关问题，整理了一下方法，如何解决 DDL 被阻塞的问题。
下面，就这个问题，整理了一下思路：
- 怎么判断一个 DDL 是不是被阻塞了？
- 当 DDL 被阻塞时，怎么找出阻塞它的会话？ 
## 1. 如何判断一个 DDL 是不是被阻塞了？
测试过程如下：
mysql> use test;
Database changed
mysql> CREATE TABLE `test` (
->   `id` int(11) AUTO_INCREMENT PRIMARY KEY,
->   `name` varchar(10)
-> );
Query OK, 0 rows affected (0.01 sec)
# 插入数据
mysql> insert into test values (1,'aaa'),(2,'bbb'),(3,'ccc'),(4,'ddd');
Query OK, 1 row affected (0.01 sec)
mysql> begin;
Query OK, 0 rows affected (0.01 sec)
mysql> select * from test;
+----+------+
| id | name |
+----+------+
|  1 | aaa  |
|  2 | bbb  |
|  3 | ccc  |
|  4 | ddd  |
+----+------+
4 rows in set (0.00 sec)
# 模拟元数据锁阻塞
# 会话 1
mysql> lock tables test read;
Query OK, 0 rows affected (0.00 sec)
# 会话 2
mysql> alter table test add c1 varchar(25);
阻塞中
# 会话 3
mysql> show processlist;
+-------+-------------+---------------------+------+------------------+--------+---------------------------------------------------------------+-------------------------------------+
| Id    | User        | Host                | db   | Command          | Time   | State                                                         | Info                                |
+-------+-------------+---------------------+------+------------------+--------+---------------------------------------------------------------+-------------------------------------+
|    1  | universe_op | 127.0.0.1:28904     | NULL | Sleep            |     12 |                                                               | NULL                                |
|    2  | universe_op | 127.0.0.1:28912     | NULL | Sleep            |     12 |                                                               | NULL                                |
|  5752 | universe_op | 10.186.64.180:51808 | NULL | Binlog Dump GTID | 605454 | Master has sent all binlog to slave; waiting for more updates | NULL                                |
| 28452 | root        | 10.186.65.110:10756 | test | Sleep            |     73 |                                                               | NULL                                |
| 28454 | root        | 10.186.64.180:45674 | test | Query            |      7 | Waiting for table metadata lock                               | alter table test add c1 varchar(25) |
| 28497 | root        | 10.186.64.180:47026 | test | Query            |      0 | starting                                                      | show processlist                    |
+-------+-------------+---------------------+------+------------------+--------+---------------------------------------------------------------+-------------------------------------+
DDL 一旦被阻塞了，后续针对该表的所有操作都会被阻塞，都会显示 **Waiting for table metadata lock**。
上述情况的解决方案：**Kill DDL 操作或 Kill 阻塞 DDL 的会话。**
下面对于 DDL 的操作，我们需要获取元数据库锁的阶段有两个方面：DDL 开始之初和 DDL 结束之前。如果是后者，就意味着之前的操作都要回滚，成本相对较高。所以，碰到类似情况，我们一般都会 Kill 阻塞 DDL 的会话。
## 2. 怎么知道是哪些会话阻塞了DDL？
`sys.schema_table_lock_waits` 是 MySQL 5.7 引入的，用来定位 DDL 被阻塞的问题。
针对上面这个情况。可以查看 `sys.schema_table_lock_waits` 的输出。
mysql> select * from sys.schema_table_lock_waits\G
*************************** 1. row ***************************
object_schema: test
object_name: test
waiting_thread_id: 28490
waiting_pid: 28454
waiting_account: root@10.186.64.180
waiting_lock_type: EXCLUSIVE
waiting_lock_duration: TRANSACTION
waiting_query: alter table test add c1 varchar(25)
waiting_query_secs: 179
waiting_query_rows_affected: 0
waiting_query_rows_examined: 0
blocking_thread_id: 28488
blocking_pid: 28452
blocking_account: root@10.186.65.110
blocking_lock_type: SHARED_READ_ONLY
blocking_lock_duration: TRANSACTION
sql_kill_blocking_query: KILL QUERY 28452
sql_kill_blocking_connection: KILL 28452
*************************** 2. row ***************************
object_schema: test
object_name: test
waiting_thread_id: 28490
waiting_pid: 28454
waiting_account: root@10.186.64.180
waiting_lock_type: EXCLUSIVE
waiting_lock_duration: TRANSACTION
waiting_query: alter table test add c1 varchar(25)
waiting_query_secs: 179
waiting_query_rows_affected: 0
waiting_query_rows_examined: 0
blocking_thread_id: 28490
blocking_pid: 28454
blocking_account: root@10.186.64.180
blocking_lock_type: SHARED_UPGRADABLE
blocking_lock_duration: TRANSACTION
sql_kill_blocking_query: KILL QUERY 28454
sql_kill_blocking_connection: KILL 28454
2 rows in set (0.00 sec)
只有一个 `alter` 操作，却产生了两条记录，而且两条记录的 Kill 对象还不一样。如果对表结构不熟悉或不仔细看记录内容的话，难免会 Kill 错对象。
两条记录的 `blocking_lock_type` 类型分别为 `SHARED_READ_ONLY` 和 `SHARED_UPGRADABLE`。我们需要 Kill 掉的是 `SHARED_READ_ONLY`。
在 DDL 操作被阻塞后，如果后续有多个查询被 DDL 操作堵塞，还会产生 2N 多个条记录。
在定位问题时，这 2N 条记录看起来就比较难以定位了。这个时候，我们需要对上述 2N 条记录进行过滤。过滤的关键是 `blocking_lock_type` 不等于 `SHARED_UPGRADABLE`。
`SHARED_UPGRADABLE` 是一个可升级的共享元数据锁，加锁期间，允许并发查询和更新。所以，阻塞 DDL 的不会是 `SHARED_UPGRADABLE`。
针对上面这个场景，我们可以通过下面这个查询来精确地定位出需要 Kill 的会话。
mysql> SELECT sql_kill_blocking_connection FROM sys.schema_table_lock_waits WHERE blocking_lock_type <> 'SHARED_UPGRADABLE' AND waiting_query = 'alter table test add c1 varchar(25)';
+------------------------------+
| sql_kill_blocking_connection |
+------------------------------+
| KILL 28452                   |
+------------------------------+
1 row in set (0.00 sec) 
## MySQL 5.7 中使用 sys.schema_table_lock_waits 的注意事项
`sys.schema_table_lock_waits` 视图依赖了一张 MDL 相关的表 `performance_schema.metadata_locks`。该表是 MySQL 5.7 引入的，会显示 MDL 的相关信息，包括作用对象、锁的类型及锁的状态等。
但在 MySQL 5.7 中，该表默认为空，因为与之相关的 `instrument` 默认没有开启，MySQL 8.0 才默认开启。
mysql> select * from performance_schema.setup_instruments where name='wait/lock/metadata/sql/mdl';
+----------------------------+---------+-------+
| NAME                       | ENABLED | TIMED |
+----------------------------+---------+-------+
| wait/lock/metadata/sql/mdl | NO      | NO    |
+----------------------------+---------+-------+
1 row in set (0.00 sec)
所以，在 MySQL 5.7 中，如果我们要使用 `sys.schema_table_lock_waits`，必须首先开启 MDL 相关的 instrument。
**开启方式：** 直接修改 `performance_schema.setup_instruments` 表即可。具体 SQL 如下。
mysql> UPDATE PERFORMANCE_SCHEMA.setup_instruments SET ENABLED = 'YES', TIMED = 'YES' WHERE NAME = 'wait/lock/metadata/sql/mdl';
但这种方式是临时生效，实例重启后，又会恢复为默认值。
> 建议：同步修改配置文件或者在部署 MySQL 集群时一开始配置文件的参数就修改成功。
[mysqld]
performance-schema-instrument ='wait/lock/metadata/sql/mdl=ON'
## 总结
- 执行 `show processlist`，如果 DDL 的状态是 `Waiting for table metadata lock` ，则意味着这个 DDL 被阻塞了。
- 定位导致 DDL 被阻塞的会话，常用的方法如下：
sys.schema_table_lock_waits
select sql_kill_blocking_connection from sys.schema_table_lock_waits WHERE blocking_lock_type <> 'SHARED_UPGRADABLE' and (waiting_query like 'alter%' OR waiting_query like 'create%' OR waiting_query like 'drop%' OR waiting_query like 'truncate%' OR waiting_query like 'rename%');
这种方法适用于 MySQL 5.7 和 8.0。
> 注意，MySQL 5.7 中，MDL 相关的 instrument 默认没有打开。
Kill DDL 之前的会话。
select concat('kill',i.trx_mysql_thread_id,';') from information_schema.innodb_trx i, ( select max(time) as max_time from information_schema.processlist where state = 'Waiting for table metadata lock' and (info like 'alter%' OR info like 'create%' OR info like 'drop%' OR info like 'truncate%' OR info like 'rename%')) p WHERE timestampdiff(second, i.trx_started ,now()) > p.max_time;
如果 MySQL 5.7 中 MDL 相关的 instrument 没有打开，可使用该方法。