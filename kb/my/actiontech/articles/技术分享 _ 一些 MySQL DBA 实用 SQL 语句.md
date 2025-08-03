# 技术分享 | 一些 MySQL DBA 实用 SQL 语句

**原文链接**: https://opensource.actionsky.com/20190115-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-01-15T02:32:03-08:00

---

**本文目录：**
- 一、连接相关
- 二、长事务
- 三、元数据锁
- 四、锁等待
- 五、全局读锁
- 六、内存使用监控
- 七、分区表
- 八、数据库信息概览
- 九、长时间未更新的表
- 十、主键、索引
- 十一、存储引擎
- 十二、实时负载
**阅读提示：**
1）本篇文章涉及到大量 SQL 语句，**可将图片放大查阅**。
2）SQL 基于 Oracle MySQL 5.7 版本，其它版本因数据源不同不完全适用。
3）SQL 使用场景包含**会话连接、元数据锁、全局锁、锁等待、长事务、内存监控、分区表、低频更新表、主键、索引、存储引擎、实时负载**属于工具型文章，建议收藏保存以便后续查看。
**一、连接相关**
> 查看某用户连接的会话级别参数设置及状态变量，用于观测其它会话连接行为，辅助定位连接类问题
- 例：查看用户连接 ID 为 19 的字符集设置，也可不指定 PROCESSLIST_ID 条件，查看所有用户连接
SELECT T1.VARIABLE_NAME,
       T1.VARIABLE_VALUE,
       T2.PROCESSLIST_ID,
       concat(T2.PROCESSLIST_USER,"@",T2.PROCESSLIST_HOST),
       T2.PROCESSLIST_DB,
       T2.PROCESSLIST_COMMAND
FROM PERFORMANCE_SCHEMA.VARIABLES_BY_THREAD T1,
     PERFORMANCE_SCHEMA.THREADS T2
WHERE T1.THREAD_ID = T2.THREAD_ID
  AND T1.VARIABLE_NAME LIKE 'character%'
  AND PROCESSLIST_ID ='19';
+--------------------------+----------------+----------------+-----------------------------------------------------+----------------+---------------------+
| VARIABLE_NAME            | VARIABLE_VALUE | PROCESSLIST_ID | concat(T2.PROCESSLIST_USER,"@",T2.PROCESSLIST_HOST) | PROCESSLIST_DB | PROCESSLIST_COMMAND |
+--------------------------+----------------+----------------+-----------------------------------------------------+----------------+---------------------+
| character_set_client     | gbk            |             19 | root@localhost                                      | db             | Query               |
| character_set_connection | gbk            |             19 | root@localhost                                      | db             | Query               |
| character_set_database   | utf8mb4        |             19 | root@localhost                                      | db             | Query               |
| character_set_filesystem | binary         |             19 | root@localhost                                      | db             | Query               |
| character_set_results    | gbk            |             19 | root@localhost                                      | db             | Query               |
| character_set_server     | utf8mb4        |             19 | root@localhost                                      | db             | Query               |
+--------------------------+----------------+----------------+-----------------------------------------------------+----------------+---------------------+
6 rows in set (0.01 sec)
- 例：发现用户 ID 为 254 的连接关闭了 sql_log_bin 设置
SELECT T1.VARIABLE_NAME,
       T1.VARIABLE_VALUE,
       T2.PROCESSLIST_ID,
       concat(T2.PROCESSLIST_USER,"@",T2.PROCESSLIST_HOST) AS 'User@Host',
       T2.PROCESSLIST_DB,
       T2.PROCESSLIST_COMMAND
FROM PERFORMANCE_SCHEMA.VARIABLES_BY_THREAD T1,
     PERFORMANCE_SCHEMA.THREADS T2
WHERE T1.THREAD_ID = T2.THREAD_ID
  AND T1.VARIABLE_NAME LIKE 'sql_log_bin';
+---------------+----------------+----------------+------------------+----------------+---------------------+
| VARIABLE_NAME | VARIABLE_VALUE | PROCESSLIST_ID | User@Host        | PROCESSLIST_DB | PROCESSLIST_COMMAND |
+---------------+----------------+----------------+------------------+----------------+---------------------+
| sql_log_bin   | OFF            |            254 | root@localhost   | NULL           | Sleep               |
| sql_log_bin   | ON             |            256 | root@localhost   | NULL           | Sleep               |
| sql_log_bin   | ON             |            257 | root@10.211.55.2 | NULL           | Sleep               |
| sql_log_bin   | ON             |            258 | root@10.211.55.2 | NULL           | Sleep               |
| sql_log_bin   | ON             |            259 | root@localhost   | NULL           | Query               |
| sql_log_bin   | ON             |            261 | root@localhost   | NULL           | Sleep               |
+---------------+----------------+----------------+------------------+----------------+---------------------+
4 rows in set (0.00 sec)
- 
例：查看用户连接 ID 为 24 的网络流量变化
SELECT T1.VARIABLE_NAME,
       T1.VARIABLE_VALUE,
       T2.PROCESSLIST_ID,
       concat(T2.PROCESSLIST_USER,"@",T2.PROCESSLIST_HOST) AS 'User@Host',
       T2.PROCESSLIST_DB,
       T2.PROCESSLIST_COMMAND
FROM PERFORMANCE_SCHEMA.STATUS_BY_THREAD T1,
     PERFORMANCE_SCHEMA.THREADS T2
WHERE T1.THREAD_ID = T2.THREAD_ID
  AND T2.PROCESSLIST_USER = 'root'
  AND PROCESSLIST_ID= 24
  AND VARIABLE_NAME LIKE 'Byte%';
+----------------+----------------+----------------+----------------+----------------+---------------------+
| VARIABLE_NAME  | VARIABLE_VALUE | PROCESSLIST_ID | User@Host      | PROCESSLIST_DB | PROCESSLIST_COMMAND |
+----------------+----------------+----------------+----------------+----------------+---------------------+
| Bytes_received | 224            |             24 | root@127.0.0.1 | NULL           | Sleep               |
| Bytes_sent     | 182            |             24 | root@127.0.0.1 | NULL           | Sleep               |
+----------------+----------------+----------------+----------------+----------------+---------------------+
2 rows in set (0.00 sec)
**二、长事务**
> 事务开启后，超过 5s 未提交的用户连接
SELECT trx_mysql_thread_id AS PROCESSLIST_ID,
       NOW(),
       TRX_STARTED,
       TO_SECONDS(now())-TO_SECONDS(trx_started) AS TRX_LAST_TIME ,
       USER,
       HOST,
       DB,
       TRX_QUERY
FROM INFORMATION_SCHEMA.INNODB_TRX trx
JOIN INFORMATION_SCHEMA.processlist pcl ON trx.trx_mysql_thread_id=pcl.id
WHERE trx_mysql_thread_id != connection_id()
  AND TO_SECONDS(now())-TO_SECONDS(trx_started) >= 5 ;
+----------------+---------------------+---------------------+---------------+------+-----------------+------+-----------+
| PROCESSLIST_ID | NOW()               | TRX_STARTED         | TRX_LAST_TIME | User | Host            | DB   | TRX_QUERY |
+----------------+---------------------+---------------------+---------------+------+-----------------+------+-----------+
|             24 | 2019-12-16 02:49:52 | 2019-12-16 02:41:15 |           517 | root | 127.0.0.1:58682 | db   | NULL      |
+----------------+---------------------+---------------------+---------------+------+-----------------+------+-----------+
1 row in set (0.01 sec)
**三、元数据锁**> MySQL 5.7 开启元数据锁追踪，以便追踪定位元数据锁相关的阻塞问题
// 临时开启，动态生效
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME ='global_instrumentation';
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES'
WHERE NAME ='wait/lock/metadata/sql/mdl';
// 配置文件中添加，重启生效
performance-schema-instrument = wait/lock/metadata/sql/mdl=ON
> 场景 1：杀掉持有 MDL 锁的会话，使 DDL 语句顺利执行。
- DDL 语句被阻塞通常因为存在获取资源后未及时提交释放的长事务。因此，查找 kill 掉事务运行时间大于 DDL 运行时间的会话即可使 DDL 语句顺利下发，SQL 语句如下：
// 查找事务运行时间 >= DDL等待时间的线程
SELECT trx_mysql_thread_id AS PROCESSLIST_ID,
       NOW(),
       TRX_STARTED,
       TO_SECONDS(now())-TO_SECONDS(trx_started) AS TRX_LAST_TIME ,
       USER,
       HOST,
       DB,
       TRX_QUERY
FROM INFORMATION_SCHEMA.INNODB_TRX trx
JOIN INFORMATION_SCHEMA.processlist pcl ON trx.trx_mysql_thread_id=pcl.id
WHERE trx_mysql_thread_id != connection_id()
  AND TO_SECONDS(now())-TO_SECONDS(trx_started) >=
    (SELECT MAX(Time)
     FROM INFORMATION_SCHEMA.processlist
     WHERE STATE='Waiting for table metadata lock'
       AND INFO LIKE 'alter%table%' OR INFO LIKE 'truncate%table%') ;
+----------------+---------------------+---------------------+---------------+------+-----------+------+-----------+
| PROCESSLIST_ID | NOW()               | TRX_STARTED         | TRX_LAST_TIME | User | Host      | DB   | TRX_QUERY |
+----------------+---------------------+---------------------+---------------+------+-----------+------+-----------+
|            253 | 2019-12-24 01:42:11 | 2019-12-24 01:41:24 |            47 | root | localhost | NULL | NULL      |
+----------------+---------------------+---------------------+---------------+------+-----------+------+-----------+
1 row in set (0.00 sec)
// kill掉长事务，释放持有的MDL资源
kill 253;
注：因 MySQL 元数据信息记录有限，此处可能误杀无辜长事务，且误杀无法完全避免。
- 当 kill 掉阻塞源后，可能存在 DDL 语句与被阻塞的 SQL 语句同时加锁的情况，此时会出现事务开始时间等于 DDL 开始时间连接，此类事务也需 kill。
//查找事务开始时间 = DDL语句事务开始时间的线程
SELECT trx_mysql_thread_id AS PROCESSLIST_ID,
       NOW(),
       TRX_STARTED,
       TO_SECONDS(now())-TO_SECONDS(trx_started) AS TRX_LAST_TIME ,
       USER,
       HOST,
       DB,
       TRX_QUERY
FROM INFORMATION_SCHEMA.INNODB_TRX trx
JOIN INFORMATION_SCHEMA.processlist pcl ON trx.trx_mysql_thread_id=pcl.id
WHERE trx_mysql_thread_id != connection_id()
  AND trx_started =
    (SELECT MIN(trx_started)
     FROM INFORMATION_SCHEMA.INNODB_TRX
     GROUP BY trx_started HAVING count(trx_started)>=2)
  AND TRX_QUERY NOT LIKE 'alter%table%'
  OR TRX_QUERY IS NULL;
+----------------+---------------------+---------------------+---------------+------+-----------+------+-----------+
| PROCESSLIST_ID | NOW()               | TRX_STARTED         | TRX_LAST_TIME | User | Host      | DB   | TRX_QUERY |
+----------------+---------------------+---------------------+---------------+------+-----------+------+-----------+
|            255 | 2019-12-24 01:42:44 | 2019-12-24 01:42:33 |            11 | root | localhost | NULL | NULL      |
+----------------+---------------------+---------------------+---------------+------+-----------+------+-----------+
1 row in set (0.00 sec)
//杀掉阻塞源
kill 255;
场景 2：kill 掉下发 DDL 语句的用户连接，取消 DDL 语句下发，保障业务不被阻塞。
// 查找DDL语句所在用户连接
SELECT *
FROM INFORMATION_SCHEMA.PROCESSLIST
WHERE INFO LIKE 'ALTER%TABLE%';
+-----+------+-----------+------+---------+------+---------------------------------+----------------------------------+
| ID  | USER | HOST      | DB   | COMMAND | TIME | STATE                           | INFO                             |
+-----+------+-----------+------+---------+------+---------------------------------+----------------------------------+
| 254 | root | localhost | NULL | Query   |  730 | Waiting for table metadata lock | alter table db.t1 add index (id) |
+-----+------+-----------+------+---------+------+---------------------------------+----------------------------------+
1 row in set (0.00 sec)
// 杀掉DDL语句所在用户连接
kill 254;
**四、锁等待**
> 查看锁等待相关的阻塞线程、被阻塞线程信息及相关用户、IP、PORT
SELECT locked_table,
       locked_index,
       locked_type,
       blocking_pid,
       concat(T2.USER,'@',T2.HOST) AS "blocking(user@ip:port)",
       blocking_lock_mode,
       blocking_trx_rows_modified,
       waiting_pid,
       concat(T3.USER,'@',T3.HOST) AS "waiting(user@ip:port)",
       waiting_lock_mode,
       waiting_trx_rows_modified,
       wait_age_secs,
       waiting_query
FROM sys.x$innodb_lock_waits T1
LEFT JOIN INFORMATION_SCHEMA.processlist T2 ON T1.blocking_pid=T2.ID
LEFT JOIN INFORMATION_SCHEMA.processlist T3 ON T3.ID=T1.waiting_pid;
+--------------+--------------+-------------+--------------+------------------------+--------------------+----------------------------+-------------+-----------------------+-------------------+---------------------------+---------------+---------------------------------+
| locked_table | locked_index | locked_type | blocking_pid | blocking(user@ip:port) | blocking_lock_mode | blocking_trx_rows_modified | waiting_pid | waiting(user@ip:port) | waiting_lock_mode | waiting_trx_rows_modified | wait_age_secs | waiting_query                   |
+--------------+--------------+-------------+--------------+------------------------+--------------------+----------------------------+-------------+-----------------------+-------------------+---------------------------+---------------+---------------------------------+
| `db`.`t1`    | PRIMARY      | RECORD      |          228 | dks@127.0.0.1:56724    | X                  |                          1 |         231 | root@127.0.0.1:50852  | S                 |                         0 |             1 | insert into db.t1(id) values(2) |
+--------------+--------------+-------------+--------------+------------------------+--------------------+----------------------------+-------------+-----------------------+-------------------+---------------------------+---------------+---------------------------------+
1 row in set, 3 warnings (0.00 sec)
- 若不关心阻塞相关的用户、IP、PORT，可直接查看 innodb_lock_waits 表信息。
select * from sys.x$innodb_lock_waits\G
*************************** 1. row ***************************
                wait_started: 2019-12-23 02:14:22
                    wait_age: 00:00:32
               wait_age_secs: 32
                locked_table: `db`.`t1`
                locked_index: PRIMARY
                 locked_type: RECORD
              waiting_trx_id: 7204404
         waiting_trx_started: 2019-12-23 02:14:18
             waiting_trx_age: 00:00:36
     waiting_trx_rows_locked: 1
   waiting_trx_rows_modified: 0
                 waiting_pid: 213
               waiting_query: delete from db.t1 where id=200
             waiting_lock_id: 7204404:1994:3:4
           waiting_lock_mode: X
             blocking_trx_id: 7204394
                blocking_pid: 207
              blocking_query: select * from   sys.x$innodb_lock_waits
            blocking_lock_id: 7204394:1994:3:4
          blocking_lock_mode: X
        blocking_trx_started: 2019-12-23 02:10:06
            blocking_trx_age: 00:04:48
    blocking_trx_rows_locked: 1
  blocking_trx_rows_modified: 1
     sql_kill_blocking_query: KILL QUERY 207
sql_kill_blocking_connection: KILL 207
1 row in set, 3 warnings (0.00 sec)
> 影响锁等待超时的参数
![](https://opensource.actionsky.com/wp-content/uploads/2020/01/表格.png)											
**五、全局读锁**
> PERFORMANCE_SCHEMA.METADATA_LOCKS 表 LOCK_DURATION 列为 EXPLICIT 状态表示 FTWRL 语句添加，OBJECT_TYPE 出现 COMMIT 状态表示已经加锁成功
- 场景 1：杀掉添加 FTWRL 的会话，恢复业务运行
SELECT processlist_id,
       mdl.OBJECT_TYPE,
       OBJECT_SCHEMA,
       OBJECT_NAME,
       LOCK_TYPE,
       LOCK_DURATION,
       LOCK_STATUS
FROM performance_schema.metadata_locks mdl
INNER JOIN performance_schema.threads thd ON mdl.owner_thread_id = thd.thread_id
AND processlist_id <> connection_id()
AND LOCK_DURATION='EXPLICIT';
+----------------+-------------+---------------+-------------+-----------+---------------+-------------+
| processlist_id | OBJECT_TYPE | OBJECT_SCHEMA | OBJECT_NAME | LOCK_TYPE | LOCK_DURATION | LOCK_STATUS |
+----------------+-------------+---------------+-------------+-----------+---------------+-------------+
|            231 | GLOBAL      | NULL          | NULL        | SHARED    | EXPLICIT      | GRANTED     |
|            231 | COMMIT      | NULL          | NULL        | SHARED    | EXPLICIT      | GRANTED     |
+----------------+-------------+---------------+-------------+-----------+---------------+-------------+
2 rows in set (0.00 sec)
// 杀掉添加FTWRL的用户连接
kill 231;
- 场景 2：杀掉语句执行时间大于 FTWRL 执行时间的线程，确保 FTWRL 下发成功
SELECT T2.THREAD_ID,
       T1.ID AS PROCESSLIST_ID,
       T1.User,
       T1.Host,
       T1.db,
       T1.Time,
       T1.State,
       T1.Info,
       T3.TRX_STARTED,
       TO_SECONDS(now())-TO_SECONDS(trx_started) AS TRX_LAST_TIME
FROM INFORMATION_SCHEMA.processlist T1
LEFT JOIN PERFORMANCE_SCHEMA.THREADS T2 ON T1.ID=T2.PROCESSLIST_ID
LEFT JOIN INFORMATION_SCHEMA.INNODB_TRX T3 ON T1.id=T3.trx_mysql_thread_id
WHERE T1.TIME >=
    (SELECT MAX(Time)
     FROM INFORMATION_SCHEMA.processlist
     WHERE INFO LIKE 'flush%table%with%read%lock')
  AND Info IS NOT NULL;
+-----------+----------------+------+-------------------+------+------+-------------------------+---------------------------------------------+---------------------+---------------+
| THREAD_ID | PROCESSLIST_ID | User | Host              | db   | Time | State                   | Info                                        | TRX_STARTED         | TRX_LAST_TIME |
+-----------+----------------+------+-------------------+------+------+-------------------------+---------------------------------------------+---------------------+---------------+
|       284 |            246 | root | localhost         | NULL |  364 | User sleep              | select * from db.t1 where sleep(1000000000) | 2019-12-23 14:57:23 |           364 |
|       286 |            248 | root | 10.211.55.2:55435 | NULL |  232 | Waiting for table flush | flush table with read lock                  | NULL                |          NULL |
+-----------+----------------+------+-------------------+------+------+-------------------------+---------------------------------------------+---------------------+---------------+
2 rows in set (0.00 sec)
**六、内存使用监控**> 默认只对 performance_schema 库进行内存统计，对全局内存统计需要手工开启
//动态开启，开启后开始统计
update performance_schema.setup_instruments set
enabled = 'yes' where name like 'memory%';
//配置文件中添加，重启生效
performance-schema-instrument='memory/%=COUNTED'
- 查看实例内存消耗分布，sys 库下有多张 memory 相关视图用于协助用户定位分析内存溢出类问题
SELECT event_name,
       current_alloc
FROM sys.memory_global_by_current_bytes
WHERE event_name LIKE 'memory%innodb%';
+-------------------------------------------+---------------+
| event_name                                | current_alloc |
+-------------------------------------------+---------------+
| memory/innodb/buf_buf_pool                | 134.31 MiB    |
| memory/innodb/log0log                     | 32.01 MiB     |
| memory/innodb/mem0mem                     | 15.71 MiB     |
| memory/innodb/lock0lock                   | 12.21 MiB     |
| memory/innodb/os0event                    | 8.37 MiB      |
| memory/innodb/hash0hash                   | 4.74 MiB      |
...
+-------------------------------------------+---------------+
42 rows in set (0.01 sec)
**七、分区表**- 查看实例中的分区表相关信息
SELECT TABLE_SCHEMA,
       TABLE_NAME,
       count(PARTITION_NAME) AS PARTITION_COUNT,
       sum(TABLE_ROWS) AS TABLE_TOTAL_ROWS,
       CONCAT(ROUND(SUM(DATA_LENGTH) / (1024 * 1024), 2),'M') DATA_LENGTH,
       CONCAT(ROUND(SUM(INDEX_LENGTH) / (1024 * 1024), 2),'M') INDEX_LENGTH,
       CONCAT(ROUND(ROUND(SUM(DATA_LENGTH + INDEX_LENGTH)) / (1024 * 1024),2),'M') TOTAL_SIZE
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_NAME NOT IN ('sys',
                         'mysql',
                         'INFORMATION_SCHEMA',
                         'performance_schema')
  AND PARTITION_NAME IS NOT NULL
GROUP BY TABLE_SCHEMA,
         TABLE_NAME
ORDER BY sum(DATA_LENGTH + INDEX_LENGTH) DESC ;
+--------------+------------------+-----------------+------------------+-------------+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME       | PARTITION_COUNT | TABLE_TOTAL_ROWS | DATA_LENGTH | INDEX_LENGTH | TOTAL_SIZE |
+--------------+------------------+-----------------+------------------+-------------+--------------+------------+
| db           | t1               |             365 |                0 | 5.70M       | 17.11M       | 22.81M     |
| db           | t2               |             391 |                0 | 6.11M       | 0.00M        | 6.11M      |
| db           | t3               |               4 |            32556 | 2.28M       | 0.69M        | 2.97M      |
| db           | t4               |              26 |                0 | 0.41M       | 2.44M        | 2.84M      |
| db           | t5               |               4 |                0 | 0.06M       | 0.00M        | 0.06M      |
| db           | t6               |               4 |                0 | 0.06M       | 0.00M        | 0.06M      |
+--------------+------------------+-----------------+------------------+-------------+--------------+------------+
6 rows in set (1.04 sec)
- 查看某分区表具体信息，此处以库名为 db、表名为 e 的分区表为例
SELECT TABLE_SCHEMA,
       TABLE_NAME,
       PARTITION_NAME,
       PARTITION_EXPRESSION,
       PARTITION_METHOD,
       PARTITION_DESCRIPTION,
       TABLE_ROWS,
       CONCAT(ROUND(DATA_LENGTH / (1024 * 1024), 2),'M') DATA_LENGTH,
       CONCAT(ROUND(INDEX_LENGTH / (1024 * 1024), 2),'M') INDEX_LENGTH,
       CONCAT(ROUND(ROUND(DATA_LENGTH + INDEX_LENGTH) / (1024 * 1024),2),'M') TOTAL_SIZE
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_SCHEMA NOT IN ('sys',
                         'mysql',
                         'INFORMATION_SCHEMA',
                         'performance_schema')
  AND PARTITION_NAME IS NOT NULL
  AND TABLE_SCHEMA='db'
  AND TABLE_NAME='e';
+--------------+------------+----------------+----------------------+------------------+-----------------------+------------+-------------+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | PARTITION_EXPRESSION | PARTITION_METHOD | PARTITION_DESCRIPTION | TABLE_ROWS | DATA_LENGTH | INDEX_LENGTH | TOTAL_SIZE |
+--------------+------------+----------------+----------------------+------------------+-----------------------+------------+-------------+--------------+------------+
| db           | e          | p0             | id                   | RANGE            | 50                    |       4096 | 0.20M       | 0.09M        | 0.30M      |
| db           | e          | p1             | id                   | RANGE            | 100                   |       6144 | 0.28M       | 0.13M        | 0.41M      |
| db           | e          | p2             | id                   | RANGE            | 150                   |       6144 | 0.28M       | 0.13M        | 0.41M      |
| db           | e          | p3             | id                   | RANGE            | MAXVALUE              |      16172 | 1.52M       | 0.34M        | 1.86M      |
+--------------+------------+----------------+----------------------+------------------+-----------------------+------------+-------------+--------------+------------+
4 rows in set (0.00 sec)
**八、数据库信息概览**- 统计实例中各数据库大小
SELECT TABLE_SCHEMA,
       round(SUM(data_length+index_length)/1024/1024,2) AS TOTAL_MB,
       round(SUM(data_length)/1024/1024,2) AS DATA_MB,
       round(SUM(index_length)/1024/1024,2) AS INDEX_MB,
       COUNT(*) AS TABLES
FROM INFORMATION_SCHEMA.tables
WHERE TABLE_SCHEMA NOT IN ('sys',
                           'mysql',
                           'INFORMATION_SCHEMA',
                           'performance_schema')
GROUP BY TABLE_SCHEMA
ORDER BY 2 DESC;
+--------------+----------+---------+----------+--------+
| TABLE_SCHEMA | TOTAL_MB | DATA_MB | INDEX_MB | TABLES |
+--------------+----------+---------+----------+--------+
| cloud        |   229.84 |  223.02 |     6.83 |     41 |
| db           |    66.42 |   30.56 |    35.86 |     31 |
| dks          |    14.41 |    9.70 |     4.70 |    621 |
| test         |     0.06 |    0.06 |     0.00 |      4 |
| db2          |     0.03 |    0.03 |     0.00 |      2 |
+--------------+----------+---------+----------+--------+
5 rows in set, 1 warning (0.91 sec)
- 统计某库下各表大小
SELECT TABLE_SCHEMA,
       TABLE_NAME TABLE_NAME,
                  CONCAT(ROUND(data_length / (1024 * 1024), 2),'M') data_length,
                  CONCAT(ROUND(index_length / (1024 * 1024), 2),'M') index_length,
                  CONCAT(ROUND(ROUND(data_length + index_length) / (1024 * 1024),2),'M') total_size,
                  engine
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA' ,
                           'performance_schema',
                           'sys',
                           'mysql')
  AND TABLE_SCHEMA='db'
ORDER BY (data_length + index_length) DESC LIMIT 10;
+--------------+-----------------------+-------------+--------------+------------+--------+
| TABLE_SCHEMA | table_name            | data_length | index_length | total_size | engine |
+--------------+-----------------------+-------------+--------------+------------+--------+
| db           | t1                    | 5.70M       | 22.81M       | 28.52M     | InnoDB |
| db           | t2                    | 15.19M      | 9.59M        | 24.78M     | InnoDB |
| db           | t3                    | 6.11M       | 0.00M        | 6.11M      | InnoDB |
| db           | t4                    | 2.28M       | 0.69M        | 2.97M      | InnoDB |
| db           | t5                    | 0.41M       | 2.44M        | 2.84M      | InnoDB |
| db           | t6                    | 0.17M       | 0.00M        | 0.17M      | InnoDB |
| db           | t7                    | 0.17M       | 0.00M        | 0.17M      | InnoDB |
| db           | t8                    | 0.02M       | 0.11M        | 0.13M      | InnoDB |
| db           | t9                    | 0.08M       | 0.00M        | 0.08M      | InnoDB |
| db           | t10                   | 0.05M       | 0.02M        | 0.06M      | InnoDB |
+--------------+-----------------------+-------------+--------------+------------+--------+
10 rows in set, 1 warning (0.01 sec)
- 查看某库下表的基本信息
SELECT TABLE_SCHEMA,
       TABLE_NAME,
       table_collation,
       engine,
       table_rows
FROM INFORMATION_SCHEMA.tables
WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA' ,
                           'sys',
                           'mysql',
                           'performance_schema')
  AND TABLE_TYPE='BASE TABLE'
  AND TABLE_SCHEMA='db'
ORDER BY table_rows DESC ;
+--------------+-----------------------+--------------------+--------+------------+
| TABLE_SCHEMA | table_name            | table_collation    | engine | table_rows |
+--------------+-----------------------+--------------------+--------+------------+
| db           | t1                    | utf8_general_ci    | InnoDB |     159432 |
| db           | t2                    | utf8mb4_general_ci | InnoDB |      32556 |
| db           | t3                    | utf8mb4_general_ci | InnoDB |       2032 |
...
| db           | t100                  | utf8mb4_general_ci | InnoDB |          0 |
| db           | t101                  | utf8mb4_general_ci | InnoDB |          0 |
+--------------+-----------------------+--------------------+--------+------------+
25 rows in set, 1 warning (0.01 sec)
**九、长时间未更新的表**> UPDATE_TIME 为 NULL 表示实例启动后一直未更新过
SELECT TABLE_SCHEMA,
       TABLE_NAME,
       UPDATE_TIME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA NOT IN ('SYS',
                           'MYSQL',
                           'INFORMATION_SCHEMA',
                           'PERFORMANCE_SCHEMA')
  AND TABLE_TYPE='BASE TABLE'
ORDER BY UPDATE_TIME ;
+--------------+-----------------------+---------------------+
| TABLE_SCHEMA | TABLE_NAME            | UPDATE_TIME         |
+--------------+-----------------------+---------------------+
| db           | t1                    | NULL                |
| db           | t2                    | NULL                |
| db           | t3                    | NULL                |
| db           | t4                    | 2019-12-16 07:45:29 |
| db           | t5                    | 2019-12-16 16:52:01 |
+--------------+-----------------------+---------------------+
22 rows in set, 1 warning (0.01 sec)
**十、主键、索引**> 无主键、唯一键及二级索引基表
- MySQL Innodb 存储引擎为索引组织表，因此设置合适的主键字段对性能至关重要
SELECT T1.TABLE_SCHEMA,
       T1.TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS T1 JOIN INFORMATION_SCHEMA.TABLES T2 ON T1.TABLE_SCHEMA=T2.TABLE_SCHEMA AND T1.TABLE_NAME=T2.TABLE_NAME
WHERE T1.TABLE_SCHEMA NOT IN ('SYS',
                           'MYSQL',
                           'INFORMATION_SCHEMA',
                           'PERFORMANCE_SCHEMA')
  AND T2.TABLE_TYPE='BASE TABLE'
  AND T1.TABLE_SCHEMA='db'
GROUP BY T1.TABLE_SCHEMA,
         T1.TABLE_NAME HAVING MAX(COLUMN_KEY)='';
> 无主键、唯一键，仅有二级索引表
- 该类型表因无高效索引，因此从库回放时容易导致复制延迟
SELECT T1.TABLE_SCHEMA,
       T1.TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS  T1 JOIN INFORMATION_SCHEMA.TABLES T2 ON T1.TABLE_SCHEMA=T2.TABLE_SCHEMA AND T1.TABLE_NAME=T2.TABLE_NAME
WHERE T1.TABLE_SCHEMA NOT IN ('SYS',
                           'MYSQL',
                           'INFORMATION_SCHEMA',
                           'PERFORMANCE_SCHEMA')
  AND T2.TABLE_TYPE='BASE TABLE'
  AND T1.COLUMN_KEY != ''
GROUP BY T1.TABLE_SCHEMA,
         T1.TABLE_NAME HAVING group_concat(COLUMN_KEY) NOT REGEXP 'PRI|UNI';
> 仅有主键、唯一键表
- 该类型表结构因无二级索引，可能导致应用 SQL 语句上线后频繁全表扫描出现性能抖动
SELECT T1.TABLE_SCHEMA,
       T1.TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS T1 JOIN INFORMATION_SCHEMA.TABLES T2 ON T1.TABLE_SCHEMA=T2.TABLE_SCHEMA AND T1.TABLE_NAME=T2.TABLE_NAME
WHERE T1.TABLE_SCHEMA NOT IN ('SYS',
                           'MYSQL',
                           'INFORMATION_SCHEMA',
                           'PERFORMANCE_SCHEMA')
  AND T2.TABLE_TYPE='BASE TABLE'
  AND T1.COLUMN_KEY != ''
  AND T1.TABLE_SCHEMA='db'
GROUP BY T1.TABLE_SCHEMA,
         T1.TABLE_NAME HAVING group_concat(COLUMN_KEY) NOT REGEXP 'MUL';
> 无主键、唯一键表
SELECT T1.TABLE_SCHEMA,
       T1.TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS T1 JOIN INFORMATION_SCHEMA.TABLES T2 ON T1.TABLE_SCHEMA=T2.TABLE_SCHEMA AND T1.TABLE_NAME=T2.TABLE_NAME
WHERE T1.TABLE_SCHEMA NOT IN ('SYS',
                           'MYSQL',
                           'INFORMATION_SCHEMA',
                           'PERFORMANCE_SCHEMA')
AND   T2.TABLE_TYPE='BASE TABLE'
GROUP BY T1.TABLE_SCHEMA,
         T1.TABLE_NAME HAVING group_concat(COLUMN_KEY) NOT REGEXP 'PRI|UNI';
**十一、存储引擎**
- 存储引擎分布
SELECT TABLE_SCHEMA,
       ENGINE,
       COUNT(*)
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA' ,
                           'PERFORMANCE_SCHEMA',
                           'SYS',
                           'MYSQL')
  AND TABLE_TYPE='BASE TABLE'
GROUP BY TABLE_SCHEMA,
         ENGINE;
- 非 INNODB 存储引擎表
SELECT TABLE_SCHEMA,
       TABLE_NAME,
       TABLE_COLLATION,
       ENGINE,
       TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA' ,
                           'SYS',
                           'MYSQL',
                           'PERFORMANCE_SCHEMA')
  AND TABLE_TYPE='BASE TABLE'
  AND ENGINE NOT IN ('INNODB')
ORDER BY TABLE_ROWS DESC ;
**十二、实时负载**
while true
do 
mysqladmin -uroot -pxxxxxxx extended-status -r -i 1 -c 30 --socket=/mysqldata/mysqld.sock 2>/dev/null|awk -F"|" "BEGIN{ count=0 ;}"'{ if($2 ~ /Variable_name/ && ++count == 1){\
    print "----------|---------|--- MySQL Command Status --|----- Innodb row operation ----|-- Buffer Pool Read --";\
    print "---Time---|---QPS---|select insert update delete|  read inserted updated deleted|   logical    physical";\
}\
else if ($2 ~ /Queries/){queries=$3;}\
else if ($2 ~ /Com_select /){com_select=$3;}\
else if ($2 ~ /Com_insert /){com_insert=$3;}\
else if ($2 ~ /Com_update /){com_update=$3;}\
else if ($2 ~ /Com_delete /){com_delete=$3;}\
else if ($2 ~ /Innodb_rows_read/){innodb_rows_read=$3;}\
else if ($2 ~ /Innodb_rows_deleted/){innodb_rows_deleted=$3;}\
else if ($2 ~ /Innodb_rows_inserted/){innodb_rows_inserted=$3;}\
else if ($2 ~ /Innodb_rows_updated/){innodb_rows_updated=$3;}\
else if ($2 ~ /Innodb_buffer_pool_read_requests/){innodb_lor=$3;}\
else if ($2 ~ /Innodb_buffer_pool_reads/){innodb_phr=$3;}\
else if ($2 ~ /Uptime / && count >= 2){\
  printf(" %s |%9d",strftime("%H:%M:%S"),queries);\
  printf("|%6d %6d %6d %6d",com_select,com_insert,com_update,com_delete);\
  printf("|%6d %8d %7d %7d",innodb_rows_read,innodb_rows_inserted,innodb_rows_updated,innodb_rows_deleted);\
  printf("|%10d %11d\n",innodb_lor,innodb_phr);\
}}' 
done
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
技术交流群，进群后可提问
QQ群（669663113）
社区通道，邮件&电话
osc@actionsky.com
现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
格式：.md/.doc/.txt
主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
要求：原创且未发布过
奖励：作者署名；200元京东E卡+社区周边
投稿方式：
邮箱：osc@actionsky.com
格式：[投稿]姓名+文章标题
以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系