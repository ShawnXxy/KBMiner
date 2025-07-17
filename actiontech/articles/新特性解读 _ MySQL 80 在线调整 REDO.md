# 新特性解读 | MySQL 8.0 在线调整 REDO

**原文链接**: https://opensource.actionsky.com/20220802-mysql8-0/
**分类**: MySQL 新特性
**发布时间**: 2022-08-03T00:07:17-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 最新版本 8.0.30 的发布带来一个与 REDO 日志文件有关的新功能点： 在线调整 REDO 日志文件的大小！极大的简化了运维的工作量（经历过的同学都懂）！
通常一台 MySQL 实例部署完后，REDO 日志文件大小一般不会保持默认值，DBA 同学会根据数据的写入量以及频率来调整其为合适的值。与业务匹配的 REDO 日志文件大小能让数据库获得最佳的性能（如何让 REDO 日志文件的大小匹配现有业务不在本篇讨论范围）。
下面对 MySQL 8.0.30 之前以及之后的版本，对比 REDO 日志文件的更改过程，体验下最新版本的易用性。
#### 8.0.30 之前，如何更改 REDO 日志文件大小？
针对这些版本，修改 REDO 日志文件大小的步骤比较繁琐。假设需要更改其大小为 2G ，步骤如下：
###### 1、 REDO 日志文件的更改涉及两个传统参数：其最终大小是这两个参数的值相乘。
（1） innodb_log_files_in_group： REDO 日志磁盘上的文件个数，默认为2。
（2） innodb_log_file_size： REDO 日志磁盘上单个文件的大小，默认为48M。
（3）当前的日志大小为单个48M，两个组，也就是一共96M。
root@ytt-large:~/sandboxes/msb_5_7_34/data# ls -sihl ib_logfile*
3277012  48M -rw-r----- 1 root root  48M 7月  29 16:18 ib_logfile0
3277013  48M -rw-r----- 1 root root  48M 7月  29 16:18 ib_logfile1
###### 2、“关闭”快速停实例参数：innodb_fast_shutdown = 0 以确保 InnoDB 刷新所有脏页到磁盘（需要了解此参数的其他值请参见官方手册）：
<mysql:(none):5.7.34-log>set global innodb_fast_shutdown=0;
Query OK, 0 rows affected (0.00 sec)
###### 3、等步骤二执行完后，停掉MySQL实例。
###### 4、删掉数据目录下旧日志文件：
root@ytt-large:~/sandboxes/msb_5_7_34/data# rm -rf ib_logfile*
###### 5、在配置文件 my.cnf 里修改参数 innodb_log_file_size ，由于有两个组，设置这个参数为 1G 即可。
[mysqld]
innodb_log_file_size=1G
###### 6、启动 MySQL 实例（如果没有报错，代表更改成功）。
###### 7、查看新的日志文件大小：
root@ytt-large:~/sandboxes/msb_5_7_34/data# ls -sihl ib_logfile*
3277898 1.1G -rw-r----- 1 root root 1.0G 7月  29 16:31 ib_logfile0
3277923 1.1G -rw-r----- 1 root root 1.0G 7月  29 16:31 ib_logfile1
#### 8.0.30 之后，如何更改 REDO 日志文件大小？
最新版本 MySQL 8.0.30 发布后，使用新参数**innodb_redo_log_capacity**来代替之前的两个参数（目前设置这两个参数依然有效）。使用新参数调整大小非常简单，直接设置为要调整的值就行。比如调整其大小为2G：
调整之前，默认100M：
<mysql:(none):8.0.30>select @@innodb_redo_log_capacity;
+----------------------------+
| @@innodb_redo_log_capacity |
+----------------------------+
|                  104857600 |
+----------------------------+
1 row in set (0.00 sec)
调整其大小为2G：
<mysql:(none):8.0.30>set persist innodb_redo_log_capacity=2*1024*1024*1024;
Query OK, 0 rows affected (0.20 sec)
新增对应的状态变量**innodb_redo_log_capacity_resized**，方便在 MySQL 侧监控当前 REDO 日志文件大小：
<mysql:(none):8.0.30>show status like 'innodb_redo_log_capacity_resized';
+----------------------------------+------------+
| Variable_name                    | Value      |
+----------------------------------+------------+
| Innodb_redo_log_capacity_resized | 2147483648 |
+----------------------------------+------------+
1 row in set (0.00 sec)
**同时磁盘文件的存储形式不再是类似 ib_logfileN 这样的文件，而是替代为 #ib_redoN 这样新文件形式。这些新的文件默认存储在数据目录下的子目录&#8217;#innodb_redo&#8217; 里。**
1、这样的文件一共有32个，按照参数 innodb_redo_log_capacity 来平均分配。
root@ytt-large:/var/lib/mysql/#innodb_redo# ls |wc -l
32
2、有两类文件：一类是不带 _tmp 后缀的，代表正在使用的日志文件；带 _tmp 后缀的代表多余的日志文件，等正在使用的文件写满后，再接着使用它。如下所示： 正在使用的日志文件有15个，未使用的有17个。
root@ytt-large:/var/lib/mysql/#innodb_redo# ls | grep -v '_tmp' |wc -l15
root@ytt-large:/var/lib/mysql/#innodb_redo# ls | grep '_tmp' |wc -l17
同时 performance_schema 库里新增表**innodb_redo_log_files**：获取当前使用的 REDO 日志文件 LSN 区间、实际写入大小、是否已满等统计数据。例如当前15个 REDO 日志文件的统计数据如下：一目了然！
<mysql:performance_schema:8.0.30>select * from innodb_redo_log_files;
+---------+---------------------------+------------+------------+---------------+---------+----------------+
| FILE_ID | FILE_NAME                 | START_LSN  | END_LSN    | SIZE_IN_BYTES | IS_FULL | CONSUMER_LEVEL |
+---------+---------------------------+------------+------------+---------------+---------+----------------+
|       7 | ./#innodb_redo/#ib_redo7  |  552208896 |  619315712 |      67108864 |       1 |              0 |
...
|      21 | ./#innodb_redo/#ib_redo21 | 1491704320 | 1558811136 |      67108864 |       0 |              0 |
+---------+---------------------------+------------+------------+---------------+---------+----------------+
15 rows in set (0.00 sec)
#### 总结：
MySQL 8.0 新版本带来越来越多的功能点，来简化开发和运维的工作，如果可能请尽快升级吧。