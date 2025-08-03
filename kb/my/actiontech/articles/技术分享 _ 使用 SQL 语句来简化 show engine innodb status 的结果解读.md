# 技术分享 | 使用 SQL 语句来简化 show engine innodb status 的结果解读

**原文链接**: https://opensource.actionsky.com/20221208-sql/
**分类**: 技术干货
**发布时间**: 2022-12-07T18:01:12-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
熟悉 MySQL 的同学，一定对如何实时监控InnoDB表内部计数器非常了解。 就一条命令：show engine innodb status ；这条命令非常简单，但是其结果的可读性却比较差！ 那如何能简化输出，并且增加其结果的可读性呢？
MySQL 本身有一张表，在元数据字典库里，表名为innodb_metrics。这张表用来记录 InnoDB 表内部的计数器：目前 MySQL 8.0.31 最新版有314个计数器模块。
<mysql:8.0.31:information_schema>select count(*) as metrics_module_total from innodb_metrics;
+----------------------+
| metrics_module_total |
+----------------------+
|                  314 |
+----------------------+
1 row in set (0.00 sec)
那这些计数器跟我们开头说的 show engine innodb status 有没有关系？答案是有！比如我们打印一下 show engine innodb status 的部分结果：InnoDB Buffer Pool 部分（截取片段 BUFFER POOL AND MEMORY），我把频繁关注的几条数据做了简单注释。
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 0
Dictionary memory allocated 480465 
Buffer pool size   8192 -- InnoDB Buffer Pool 大小，以PAGE为单位，一个PAGE默认16KB。
Free buffers       7144 -- FREE 链表的总页数。
Database pages     1042 -- LRU 链表的总页数。
Old database pages 404
Modified db pages  0  
Pending reads      0 
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 0, not young 0
0.00 youngs/s, 0.00 non-youngs/s
Pages read 884, created 142, written 187
215.80 reads/s, 34.66 creates/s, 45.65 writes/s
Buffer pool hit rate 942 / 1000, young-making rate 0 / 1000 not 0 / 1000
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read ahead 0.00/s
LRU len: 1026, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
Buffer pool size ：8192是以PAGE为单位的统计，经过换算后 8192*16/1024 刚好是128MB。 可以非常方便的编写SQL直接从表innodb_metrics 中查询出结果。
mysql:8.0.31:information_schema>select name,concat(truncate(max_count/1024/1024,2),' MB') innodb_buffer_pool_size from innodb_metrics where name ='buffer_pool_size';
+------------------+-------------------------+
| name             | innodb_buffer_pool_size |
+------------------+-------------------------+
| buffer_pool_size | 128.00 MB               |
+------------------+-------------------------+
1 row in set (0.00 sec)
Database pages ：同样经过换算结果为 1042*16/1024=16.28MB，同样的方法，写条SQL，得出结果。
<mysql:8.0.31:information_schema>select name,concat(truncate(max_count/1024/1024,2),' MB') 'databases_pages_size' from innodb_metrics where name  = 'buffer_pool_bytes_data';
+------------------------+----------------------+
| name                   | databases_pages_size |
+------------------------+----------------------+
| buffer_pool_bytes_data | 16.28 MB             |
+------------------------+----------------------+
1 row in set (0.00 sec)
Free buffers ： 经过换算为111.62MB，写SQL也是非常方便的得出结果。
mysql:8.0.31:information_schema>select name,concat(truncate(max_count*16/1024,2),' MB') 'free buffers size' from innodb_metrics where name  ='buffer_pool_pages_free';
+------------------------+-------------------+
| name                   | free buffers size |
+------------------------+-------------------+
| buffer_pool_pages_free | 111.62 MB         |
+------------------------+-------------------+
1 row in set (0.00 sec) 
以上几个计数器，还有对应的注释在表innodb_metrics里，不用专门记住，必需时，只要查询对应字段即可（字段名：comment）。
Show engine innodb status  结果相关计数器在表innodb_metrics里默认开启，也即字段status的值为enabled。
<mysql:8.0.31:information_schema>select count(*) from innodb_metrics where status='enabled';
+----------+
| count(*) |
+----------+
|       74 |
+----------+
1 row in set (0.00 sec)
为了避免对MySQL的性能造成影响，还有200多个计数器开关默认是关闭的。比如最简单的，我们想查 MySQL 进程对 CPU 消耗相关的计数器，得手动开启。
<mysql:8.0.31:information_schema>select name,count,comment,status from innodb_metrics where name in ('cpu_n','cpu_utime_abs','cpu_stime_abs');
+---------------+-------+-----------------------------+----------+
| name          | count | comment                     | status   |
+---------------+-------+-----------------------------+----------+
| cpu_utime_abs |     0 | Total CPU user time spent   | disabled |
| cpu_stime_abs |     0 | Total CPU system time spent | disabled |
| cpu_n         |     0 | Number of cpus              | disabled |
+---------------+-------+-----------------------------+----------+
3 rows in set (0.00 sec)
开启这些计数器：通过变量 innodb_monitor_enable 来依次开启。
mysql:8.0.31:information_schema>set global innodb_monitor_enable='cpu_n'; -- 总CPU核数。
Query OK, 0 rows affected (0.00 sec)
<mysql:8.0.31:information_schema>set global innodb_monitor_enable='cpu_utime_abs'; -- 用户态CPU 总花费时间。
Query OK, 0 rows affected (0.00 sec)
<mysql:8.0.31:information_schema>set global innodb_monitor_enable='cpu_stime_abs'; -- 内核态CPU 总花费时间。
Query OK, 0 rows affected (0.00 sec)
接下来就能很方便的写SQL查出这些值：
<mysql:8.0.31:information_schema>select name,max_count,comment, status from innodb_metrics where name in ('cpu_n','cpu_utime_abs','cpu_stime_abs');
+---------------+-----------+-----------------------------+---------+
| name          | max_count | comment                     | status  |
+---------------+-----------+-----------------------------+---------+
| cpu_utime_abs |       106 | Total CPU user time spent   | enabled |
| cpu_stime_abs |         1 | Total CPU system time spent | enabled |
| cpu_n         |        32 | Number of cpus              | enabled |
+---------------+-----------+-----------------------------+---------+
3 rows in set (0.00 sec)
等需求实现后，就可以随时关闭这些计数器：
mysql:8.0.31:information_schema>set global innodb_monitor_disable='cpu_stime_abs';
Query OK, 0 rows affected (0.00 sec)
<mysql:8.0.31:information_schema>set global innodb_monitor_disable='cpu_utime_abs';
Query OK, 0 rows affected (0.00 sec)
<mysql:8.0.31:information_schema>set global innodb_monitor_disable='cpu_n';
Query OK, 0 rows affected (0.00 sec)