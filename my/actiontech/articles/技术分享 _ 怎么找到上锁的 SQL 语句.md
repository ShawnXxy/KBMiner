# 技术分享 | 怎么找到上锁的 SQL 语句

**原文链接**: https://opensource.actionsky.com/20200806-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-08-06T00:33:34-08:00

---

作者：岳明强
爱可生北京分公司 DBA 团队成员，负责数据库管理平台的运维和 MySQL 问题处理。擅长对 MySQL 的故障定位。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 问题
有的时候 SQL 语句被锁住了，可是通过 show processlist 找不到加锁的的 SQL 语句，这个时候应该怎么排查呢
## 前提
`performance_schema = on;`
## 实验
1、建一个表，插入三条数据
`mysql> use test1;
Database changed
mysql> create table action1(id int);
Query OK, 0 rows affected (0.11 sec)
mysql> insert into action1 values(1),(2),(3);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
mysql> select * from action1;
+------+
| id   |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)`
2、开启一个事务，删除掉一行记录，但不提交```
mysql> begin;
Query OK, 0 rows affected (0.00 sec)
mysql> delete from action1 where id = 3;
Query OK, 1 row affected (0.00 sec)
```
3、另开启一个事务，更新这条语句，会被锁住```
mysql> update action1 set id = 7 where id = 3;
```
4、通过 show processlist 只能看到一条正在执行的 SQL 语句```
mysql> show processlist;
| 22188 | root        | localhost          | test1 | Sleep   |  483 |          | NULL                                   |
| 22218 | root        | localhost          | NULL  | Query   |    0 | starting | show processlist                       |
| 22226 | root        | localhost          | test1 | Query   |    3 | updating | update action1 set id = 7 where id = 3 |
+-------+-------------+--------------------+-------+---------+------+----------+----------------------------------------+
```
5、接下来就是我们知道的，通过 information_schema 库里的 INNODBTRX、INNODBLOCKS 、INNODBLOCK_WAITS 获得的一个锁信息```
mysql> select * from INNODB_LOCK_WAITS;
+-------------------+-------------------+-----------------+------------------+
| requesting_trx_id | requested_lock_id | blocking_trx_id | blocking_lock_id |
+-------------------+-------------------+-----------------+------------------+
| 5978292           | 5978292:542:3:2   | 5976374         | 5976374:542:3:2  |
+-------------------+-------------------+-----------------+------------------+
1 row in set, 1 warning (0.00 sec)
mysql> select * from INNODB_LOCKs;
+-----------------+-------------+-----------+-----------+-------------------+-----------------+------------+-----------+----------+----------------+
| lock_id         | lock_trx_id | lock_mode | lock_type | lock_table        | lock_index      | lock_space | lock_page | lock_rec | lock_data      |
+-----------------+-------------+-----------+-----------+-------------------+-----------------+------------+-----------+----------+----------------+
| 5978292:542:3:2 | 5978292     | X         | RECORD    | `test1`.`action1` | GEN_CLUST_INDEX |        542 |         3 |        2 | 0x00000029D504 |
| 5976374:542:3:2 | 5976374     | X         | RECORD    | `test1`.`action1` | GEN_CLUST_INDEX |        542 |         3 |        2 | 0x00000029D504 |
+-----------------+-------------+-----------+-----------+-------------------+-----------------+------------+-----------+----------+----------------+
2 rows in set, 1 warning (0.00 sec)
mysql> select trx_id,trx_started,trx_requested_lock_id,trx_query,trx_mysql_thread_id from INNODB_TRX;
+---------+---------------------+-----------------------+----------------------------------------+---------------------+
| trx_id  | trx_started         | trx_requested_lock_id | trx_query                              | trx_mysql_thread_id |
+---------+---------------------+-----------------------+----------------------------------------+---------------------+
| 5978292 | 2020-07-26 22:55:33 | 5978292:542:3:2       | update action1 set id = 7 where id = 3 |               22226 |
| 5976374 | 2020-07-26 22:47:33 | NULL                  | NULL                                   |               22188 |
+---------+---------------------+-----------------------+----------------------------------------+---------------------+
```
6、从上面可以看出来是 thread_id 为 22188 的执行的 SQL 语句锁住了后面的更新操作，但是我们从上文中 show processlist 中并未看到这条事务，测试环境我们可以直接 kill 掉对应的线程号，但如果是生产环境中，我们需要找到对应的 SQL 语句，根据相应的语句再考虑接下来应该怎么处理
7、需要结合 performance_schema.threads 找到对应的事务号
`mysql> select * from performance_schema.threads where processlist_ID = 22188\G
*************************** 1. row ***************************
THREAD_ID: 22225  //perfoamance_schema中的事务计数器
NAME: thread/sql/one_connection
TYPE: FOREGROUND
PROCESSLIST_ID: 22188  //从show processlist中看到的id
PROCESSLIST_USER: root
PROCESSLIST_HOST: localhost
PROCESSLIST_DB: test1
PROCESSLIST_COMMAND: Sleep
PROCESSLIST_TIME: 1527
PROCESSLIST_STATE: NULL
PROCESSLIST_INFO: NULL
PARENT_THREAD_ID: NULL
ROLE: NULL
INSTRUMENTED: YES
HISTORY: YES
CONNECTION_TYPE: Socket
THREAD_OS_ID:8632
1 row in set (0.00 sec)`
8、找到事务号，可以从 events_statements_current 找到对应的 SQL 语句：SQL_TEXT```
mysql> select * from events_statements_current where THREAD_ID = 22225\G
*************************** 1. row ***************************
THREAD_ID: 22225
EVENT_ID: 14
END_EVENT_ID: 14
EVENT_NAME: statement/sql/delete
SOURCE:
TIMER_START: 546246699055725000
TIMER_END: 546246699593817000
TIMER_WAIT: 538092000
LOCK_TIME: 238000000
SQL_TEXT: delete from action1 where id = 3  //具体的sql语句
DIGEST: 8f9cdb489c76ec0e324f947cc3faaa7c
DIGEST_TEXT: DELETE FROM `action1` WHERE `id` = ?
CURRENT_SCHEMA: test1
OBJECT_TYPE: NULL
OBJECT_SCHEMA: NULL
OBJECT_NAME: NULL
OBJECT_INSTANCE_BEGIN: NULL
MYSQL_ERRNO: 0
RETURNED_SQLSTATE: 00000
MESSAGE_TEXT: NULL
ERRORS: 0
WARNINGS: 0
ROWS_AFFECTED: 1
ROWS_SENT: 0
ROWS_EXAMINED: 3
CREATED_TMP_DISK_TABLES: 0
CREATED_TMP_TABLES: 0
SELECT_FULL_JOIN: 0
SELECT_FULL_RANGE_JOIN: 0
SELECT_RANGE: 0
SELECT_RANGE_CHECK: 0
SELECT_SCAN: 0
SORT_MERGE_PASSES: 0
SORT_RANGE: 0
SORT_ROWS: 0
SORT_SCAN: 0
NO_INDEX_USED: 0
NO_GOOD_INDEX_USED: 0
NESTING_EVENT_ID: NULL
NESTING_EVENT_TYPE: NULL
NESTING_EVENT_LEVEL: 0
1 row in set (0.00 sec)
```
9、可以看到是一条 delete 阻塞了后续的 update，生产环境中可以拿着这条 SQL 语句询问开发，是不是有 kill 的必要。