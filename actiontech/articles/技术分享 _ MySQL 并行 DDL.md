# 技术分享 | MySQL 并行 DDL

**原文链接**: https://opensource.actionsky.com/20220125-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-02-10T18:33:33-08:00

---

作者：李鹏博
爱可生 DBA 团队成员，会变身，主要负责 MySQL 故障处理和 SQL 审核优化。对技术执着，为客户负责。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
随着 MySQL 版本的不断更新，对 DDL 操作的支持也在不断的完善和更新：比如从 MySQL 5.6 引入 Online DDL ，在 MySQL 5.7 对 Online DDL 进一步完善，到现在的 8.0 版本，则对 DDL 的实现重新进行了设计，比如 DDL 操作支持原子特性，在 MySQL 8.0.27 引入并行 DDL 。本篇就来探究一下 MySQL 8.0.27 的并行 DDL 对于 DDL 操作速度的提升。
MySQL 8.0.14 引入了 innodb_parallel_read_threads 变量来控制扫描聚簇索引的并行线程。MySQL 8.0.27 引入了 innodb_ddl_threads 变量来控制用于创建二级索引时的并行线程数量，此参数一般和一并引入的 innodb_ddl_buffer_size 一起使用，innodb_ddl_buffer_size 用于指定进行并行 DDL 操作时能够使用的 buffer 大小，buffer 是在所有的 DDL 并行线程中平均分配的，所以一般如果调大 innodb_ddl_threads 变量时，也需要调大 innodb_ddl_buffer_size 的大小。
innodb_ddl_threads 、innodb_ddl_buffer_size 和 innodb_parallel_read_threads 的默认大小分别为：
`mysql> select @@global.innodb_ddl_threads;
+-----------------------------+
| @@global.innodb_ddl_threads |
+-----------------------------+
|                           4 |
+-----------------------------+
1 row in set (0.00 sec)
mysql> select @@global.innodb_ddl_buffer_size;
+---------------------------------+
| @@global.innodb_ddl_buffer_size |
+---------------------------------+
|                         1048576 |
+---------------------------------+
1 row in set (0.00 sec)
mysql> select @@global.innodb_parallel_read_threads;
+---------------------------------------+
| @@global.innodb_parallel_read_threads |
+---------------------------------------+
|                                     4 |
+---------------------------------------+
1 row in set (0.00 sec)
`
接下来测试一下调大 innodb_ddl_threads 、innodb_ddl_buffer_size 和 innodb_parallel_read_threads 参数值对 DDL 操作的性能提升。
首先创建一张 5000 万的表：
`-- 数据库版本为8.0.28
mysql> select @@version;
+----------+
| @@version|
+----------+
| 8.0.28   |
+----------+
1 row in set (0.00 sec)
-- buffer pool大小为24G
mysql> select @@global.innodb_buffer_pool_size;
+----------------------------------+
| @@global.innodb_buffer_pool_size |
+----------------------------------+
|                      25769803776 |
+----------------------------------+
1 row in set (0.001 sec)
mysql> create database action;
Query OK, 1 row affected (0.01 sec)
# sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-socket=/data/mysql/data/3306/mysqld.sock  --mysql-user=root --mysql-password='123' --mysql-db=action --tables=1 --table-size=50000000 --report-interval=1 --threads=8 prepare
mysql> select count(*) from action.sbtest1;
+----------+
| count(*) |
+----------+
| 50000000 |
+----------+
1 row in set (21.64 sec)
-- 表空间大小为12G
# ll -h
total 12G
-rw-r-----. 1 mysql mysql 12G Jan 20 17:38 sbtest1.ibd
`
分别测试不同的线程数量和缓冲区大小的 DDL 操作时间，例如：
`-- 设置并发DDL线程为1
mysql> set innodb_ddl_threads = 1;
Query OK, 0 rows affected (0.01 sec)
-- 设置buffer大小为512M
mysql> set innodb_ddl_buffer_size = 536870912;
Query OK, 0 rows affected (0.00 sec)
-- 设置并行索引扫描线程为1
mysql> set innodb_parallel_read_threads = 1;
Query OK, 0 rows affected (0.01 sec)
-- 执行DDL操作
mysql> alter table action.sbtest1 add index idx_c(c);
Query OK, 0 rows affected (6 min 54.21 sec)
Records: 0  Duplicates: 0  Warnings: 0
-- 查看DDL的内存最大占用
mysql> select event_name,CURRENT_NUMBER_OF_BYTES_USED/1024/1024 from performance_schema.memory_summary_global_by_event_name where event_name='memory/innodb/ddl';
+-------------------+----------------------------------------+
| event_name        | CURRENT_NUMBER_OF_BYTES_USED/1024/1024 |
+-------------------+----------------------------------------+
| memory/innodb/ddl |                           513.08750916 |
+-------------------+----------------------------------------+
1 row in set (0.00 sec)
`
通过不断调整相关参数得到以下结果：
| innodb_ddl_threads | innodb_ddl_buffer_size | innodb_parallel_read_threads | DDL 占用最大内存 | DDL 时间 |
| --- | --- | --- | --- | --- |
| 1 | 512M | 1 | 513M | 6 min 54.21 sec |
| 2 | 1G | 2 | 1230M | 4 min 12.08 sec |
| 4 | 2G | 4 | 2735M | 3 min 43.01 sec |
| 8 | 4G | 8 | 5791M | 3 min 19.63 sec |
| 16 | 8G | 16 | 5975M | 3 min 12.33 sec |
| 32 | 16G | 32 | 6084M | 3 min 11.11 sec |
可以看到，随着并发线程的增多和 buffer 的增加，DDL 操作所占用的资源也越多，而 DDL 操作所花费的时间则越少。不过通过对比资源的消耗和 DDL 速度的提升比例，最合理的并行线程数量为4-8个，而 buffer 大小可以根据情况进行调整。
参考链接：https://dev.mysql.com/doc/refman/8.0/en/online-ddl-parallel-thread-configuration.html