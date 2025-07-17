# 技术分享 | MySQL 表空间碎片整理方法

**原文链接**: https://opensource.actionsky.com/20210628-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-07-01T20:56:04-08:00

---

作者：姚远
MySQL ACE，华为云 MVP ，专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6，5.7，8.0 OCP。现在鼎甲科技任技术顾问，为同事和客户提供数据库培训和技术支持服务。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 的表在进行了多次 delete 、update 和 insert 后，表空间会出现碎片。定期进行表空间整理，消除碎片可以提高访问表空间的性能。
# 检查表空间碎片
下面这个实验用于验证进行表空间整理后对性能的影响，首先检查这个有100万记录表的大小：
`mysql> analyze table sbtest1;
+----------------+---------+----------+-----------------------------+
| Table          | Op      | Msg_type | Msg_text                    |
+----------------+---------+----------+-----------------------------+
| sbtest.sbtest1 | analyze | status   | Table is already up to date |
+----------------+---------+----------+-----------------------------+
1 row in set (0.06 sec)
mysql> show table status like 'sbtest1'\G
*************************** 1. row ***************************
Name: sbtest1
Engine: MyISAM
Version: 10
Row_format: Fixed
Rows: 1000000
Avg_row_length: 729
Data_length: 729000000
Max_data_length: 205195258022068223
Index_length: 20457472
Data_free: 0
Auto_increment: 1000001
Create_time: 2021-05-31 18:54:22
Update_time: 2021-05-31 18:54:43
Check_time: 2021-05-31 18:55:05
Collation: utf8mb4_0900_ai_ci
Checksum: NULL
Create_options: 
Comment: 
1 row in set (0.00 sec)
mysql> system ls -l /var/lib/mysql/sbtest/sbtest1.*
-rw-r----- 1 mysql mysql 729000000 May 31 08:24 /var/lib/mysql/sbtest/sbtest1.MYD
-rw-r----- 1 mysql mysql  20457472 May 31 08:25 /var/lib/mysql/sbtest/sbtest1.MYI
`
命令 show table status 和从 OS 层看到的数据文件大小一致，这时的 Data_free 为零。
删除这个表三分之二的记录：
`mysql> delete from sbtest1 where id%3<>0;
Query OK, 666667 rows affected (51.72 sec)
`
重新收集这个表的统计信息后再查看表的状态：
`mysql> analyze table sbtest1;
+----------------+---------+----------+----------+
| Table          | Op      | Msg_type | Msg_text |
+----------------+---------+----------+----------+
| sbtest.sbtest1 | analyze | status   | OK       |
+----------------+---------+----------+----------+
1 row in set (0.13 sec)
mysql> show table status like 'sbtest1'\G
*************************** 1. row ***************************
Name: sbtest1
Engine: MyISAM
Version: 10
Row_format: Fixed
Rows: 333333
Avg_row_length: 729
Data_length: 729000000
Max_data_length: 205195258022068223
Index_length: 20457472
Data_free: 486000243
Auto_increment: 1000001
Create_time: 2021-05-31 18:54:22
Update_time: 2021-05-31 19:03:59
Check_time: 2021-05-31 18:55:05
Collation: utf8mb4_0900_ai_ci
Checksum: NULL
Create_options: 
Comment: 
1 row in set (0.01 sec)
mysql> select 486000243/729000000;
+---------------------+
| 486000243/729000000 |
+---------------------+
|              0.6667 |
+---------------------+
1 row in set (0.00 sec)
mysql> system ls -l /var/lib/mysql/sbtest/sbtest1.*
-rw-r----- 1 mysql mysql 729000000 May 31 08:33 /var/lib/mysql/sbtest/sbtest1.MYD
-rw-r----- 1 mysql mysql  20457472 May 31 08:34 /var/lib/mysql/sbtest/sbtest1.MYI
`
发现这个表中的三分之二的记录已经被删除，但数据文件的大小还和原来一样。因为被删除的记录只是被标记成删除，它们占用的存储空间并没有被释放。
进行全表扫描，看看性能：
`mysql> select count(*) from sbtest1 where c<>'aaa';
+----------+
| count(*) |
+----------+
|   333333 |
+----------+
1 row in set (0.82 sec)
`
发现这个全表扫描 SQL 用时0.82秒，查看 sys.session 视图中的 last_statement_latency 可以看到一样的用时。
# 整理表空间与性能提升
进行表空间整理：
`mysql> alter table sbtest1 force;
Query OK, 333333 rows affected (10.73 sec)
Records: 333333  Duplicates: 0  Warnings: 0
mysql> analyze table sbtest1;
+----------------+---------+----------+-----------------------------+
| Table          | Op      | Msg_type | Msg_text                    |
+----------------+---------+----------+-----------------------------+
| sbtest.sbtest1 | analyze | status   | Table is already up to date |
+----------------+---------+----------+-----------------------------+
1 row in set (0.04 sec)
mysql> show table status like 'sbtest1'\G
*************************** 1. row ***************************
Name: sbtest1
Engine: MyISAM
Version: 10
Row_format: Fixed
Rows: 333333
Avg_row_length: 729
Data_length: 242999757
Max_data_length: 205195258022068223
Index_length: 6820864
Data_free: 0
Auto_increment: 1000001
Create_time: 2021-05-31 19:10:35
Update_time: 2021-05-31 19:10:41
Check_time: 2021-05-31 19:10:45
Collation: utf8mb4_0900_ai_ci
Checksum: NULL
Create_options: 
Comment: 
1 row in set (0.48 sec)
mysql> system ls -l /var/lib/mysql/sbtest/sbtest1.*
-rw-r----- 1 mysql mysql 242999757 May 31 08:40 /var/lib/mysql/sbtest/sbtest1.MYD
-rw-r----- 1 mysql mysql   6820864 May 31 08:40 /var/lib/mysql/sbtest/sbtest1.MYI
`
经过整理后，硬盘空间占用剩下原来的三分之一，Data_free 又变成零，被删除的记录的硬盘空间都释放了。
再次执行全表扫描的 SQL 语句：
`mysql> select count(*) from sbtest1 where c<>'aaa';
+----------+
| count(*) |
+----------+
|   333333 |
+----------+
1 row in set (0.29 sec)
`
发现执行速度也提高到大约原来的三倍。这里使用的是 MyISAM 表进行测试，如果用 InnoDB 表，速度的提高没有这么明显，因为 InnoDB 的数据会缓存到 InnoDB 缓存中，MyISAM 表的数据 MySQL 不进行缓存，OS 可能会缓存，因此要得到准确的测试结果，在 Linux 系统上每次测试前要使用下面的命令释放系统的缓存：
`# echo 3 > /proc/sys/vm/drop_caches
`
使用 alter table force 进行表空间整理和 OPTIMIZE TABLE 命令的作用一样，这个命令适用于 InnoDB , MyISAM 和 ARCHIVE 三种引擎的表。但对于 InnoDB 的表，不支持 OPTIMIZE TABLE 命令，可以用 alter table sbtest1 engine=innodb 代替，例如：
`mysql> OPTIMIZE TABLE sbtest2;
+----------------+----------+----------+-------------------------------------------------------------------+
| Table          | Op       | Msg_type | Msg_text                                                          |
+----------------+----------+----------+-------------------------------------------------------------------+
| sbtest.sbtest2 | optimize | note     | Table does not support optimize, doing recreate + analyze instead |
| sbtest.sbtest2 | optimize | status   | OK                                                                |
+----------------+----------+----------+-------------------------------------------------------------------+
2 rows in set (1 min 25.24 sec)
mysql> alter table sbtest2 engine=innodb;
Query OK, 0 rows affected (1 min 3.06 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
# 使用 mysqlcheck 进行批量表空间优化
下面的命令可以找出表空间中可释放空间超过10M的最大10个表：
`mysql> select table_name,round(data_length/1024/1024) as data_length_mb,  round(data_free/1024/1024) as data_free_mb   
from information_schema.tables   where round(data_free/1024/1024) > 10  order by data_free_mb desc limit 10;
+------------+----------------+--------------+
| TABLE_NAME | data_length_mb | data_free_mb |
+------------+----------------+--------------+
| sbtest2    |            232 |          174 |
+------------+----------------+--------------+
1 row in set (0.02 sec)
`
可以使用 MySQL 自带的工具 mysqlcheck 的-o选项进行表空间优化，这个工具适合于在脚本中进行批量处理，可以被 Linux 中的 crontab 或 Windows 中的计划任务调用。
对单个表进行表空间优化的例子如下：
`$ mysqlcheck -o sbtest sbtest1
`
也可以使用下面的命令对某个数据库中的所有表进行表空间优化：
`$ mysqlcheck -o sbtest
`
还可以对整个实例中对所有数据库进行表空间优化：
`$ mysqlcheck -o --all-databases
`