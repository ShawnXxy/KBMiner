# MySQL 添加主键可以节省磁盘空间吗？

**原文链接**: https://opensource.actionsky.com/mysql-%e6%b7%bb%e5%8a%a0%e4%b8%bb%e9%94%ae%e5%8f%af%e4%bb%a5%e8%8a%82%e7%9c%81%e7%a3%81%e7%9b%98%e7%a9%ba%e9%97%b4%e5%90%97%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2024-03-04T01:06:18-08:00

---

MySQL 表定义主键不是必须的，并且直到今天（MySQL 版本 8.3.0）都是这样。不过，在 MGR 和 PXC 架构中不允许使用没有主键的表。如果数据表没有主键，会有许多众所周知的负面性能影响，其中最痛苦的是复制速度很糟糕。
今天，我想快速说明一下 **需要使用主键的另一个原因：磁盘空间！**
创建一个非常简单的示例表：
`mysql > show create table test1\G
*************************** 1. row ***************************
Table: test1
Create Table: CREATE TABLE `test1` (
`a` int NOT NULL,
`b` bigint DEFAULT NULL,
KEY `a` (`a`),
KEY `b` (`b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
`
填充 10M 测试行，需要 748M 磁盘空间。现在，假设我的测试表的 `a` 列具有唯一值：
`mysql > select count(*) from test1;
+----------+
| count(*) |
+----------+
| 10000000 |
+----------+
1 row in set (1.34 sec)
mysql > select count(DISTINCT(a)) from test1;
+--------------------+
| count(DISTINCT(a)) |
+--------------------+
|           10000000 |
+--------------------+
1 row in set (5.25 sec)
`
下面我将把索引类型更改为主键：
`mysql > alter table test1 add primary key(a), drop key a;
Query OK, 0 rows affected (48.90 sec)
Records: 0 Duplicates: 0 Warnings: 0
mysql > show create table test1\G
*************************** 1. row ***************************
Table: test1
Create Table: CREATE TABLE `test1` (
`a` int NOT NULL,
`b` bigint DEFAULT NULL,
PRIMARY KEY (`a`),
KEY `b` (`b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
`
结果，该表被重新创建，其磁盘大小减少到 588M，**非常显着！** 
为什么会发生这种情况？我们拥有完全相同的数据，并且在两种情况下都对两列都建立了索引！让我们检查一下更改前后该表的更多详细信息。
之前，在没有主键的情况下，当两列都通过辅助键建立索引时，我们可以看到以下内容：
`mysql > select SPACE,INDEX_ID,i.NAME as index_name, t.NAME as table_name, CLUST_INDEX_SIZE, OTHER_INDEX_SIZE from information_schema.INNODB_INDEXES i JOIN information_schema.INNODB_TABLESPACES t USING(space) JOIN information_schema.INNODB_TABLESTATS ts WHERE t.NAME=ts.NAME AND t.NAME='db1/test1'\G
*************************** 1. row ***************************
SPACE: 50
INDEX_ID: 232
index_name: a
table_name: db1/test1
CLUST_INDEX_SIZE: 24699
OTHER_INDEX_SIZE: 22242
*************************** 2. row ***************************
SPACE: 50
INDEX_ID: 231
index_name: b
table_name: db1/test1
CLUST_INDEX_SIZE: 24699
OTHER_INDEX_SIZE: 22242
*************************** 3. row ***************************
SPACE: 50
INDEX_ID: 230
index_name: GEN_CLUST_INDEX
table_name: db1/test1
CLUST_INDEX_SIZE: 24699
OTHER_INDEX_SIZE: 22242
3 rows in set (0.00 sec)
`
竟然还有第三个索引！通过 *innodb_ruby* 工具可以更详细地查看每个索引，可以看到它的大小是最大的（id=230）：
`$ innodb_space -f msb_8_3_0/data/db1/test1.ibd space-indexes
id      name  root        fseg        fseg_id     used        allocated   fill_factor
230           4           internal    3           27          27          100.00%    
230           4           leaf        4           24634       24672       99.85%      
231           5           internal    5           21          21          100.00%    
231           5           leaf        6           12627       12640       99.90%      
232           6           internal    7           13          13          100.00%    
232           6           leaf        8           9545        9568        99.76%
`
这就是 InnoDB 引擎的工作原理；如果没有定义明确的主键，它将添加一个名为 的内部主键 `GEN_CLUST_INDEX`。由于它包含整个数据行，因此其大小开销非常大。
将二级索引替换为显式主键后，就不再需要隐藏索引了。因此，我们总共剩下两个索引：
`mysql > select SPACE,INDEX_ID,i.NAME as index_name, t.NAME as table_name, CLUST_INDEX_SIZE,OTHER_INDEX_SIZE from information_schema.INNODB_INDEXES i JOIN information_schema.INNODB_TABLESPACES t USING(space) JOIN information_schema.INNODB_TABLESTATS ts WHERE t.NAME=ts.NAME AND t.NAME='db1/test1'\G
*************************** 1. row ***************************
SPACE: 54
INDEX_ID: 237
index_name: b
table_name: db1/test1
CLUST_INDEX_SIZE: 23733
OTHER_INDEX_SIZE: 13041
*************************** 2. row ***************************
SPACE: 54
INDEX_ID: 236
index_name: PRIMARY
table_name: db1/test1
CLUST_INDEX_SIZE: 23733
OTHER_INDEX_SIZE: 13041
2 rows in set (0.01 sec)
`
```
$ innodb_space -f msb_8_3_0/data/db1/test1.ibd space-indexes
id      name  root        fseg        fseg_id     used        allocated   fill_factor
236           4           internal    3           21          21          100.00%    
236           4           leaf        4           20704       23712       87.31%      
237           5           internal    5           17          17          100.00%    
237           5           leaf        6           11394       13024       87.48%
```
## GEN_CLUST_INDEX vs GIPK
每个 InnoDB 表都有一个聚集键，因此不定义聚集键不会节省任何磁盘空间，有时甚至相反，如上所示。因此，即使有问题的表中没有任何现有列是唯一的，最好还是添加另一个唯一列作为主键。内部 **GEN_CLUST_INDEX** 不暴露给 MySQL 上层，只有 InnoDB 引擎知道它，因此对于复制速度来说没有用处。因此，显式主键始终是更好的解决方案。
但是，如果由于遗留应用程序问题而无法添加新的主键列，建议使用不可见的主键（GIPK）来当作主键。这样，您将获得性能优势，同时对应用程序是不可见的。
`mysql > set sql_require_primary_key=1;
Query OK, 0 rows affected (0.00 sec)
mysql > create table nopk (a int);
ERROR 3750 (HY000): Unable to create or change a table without a primary key, when the system variable 'sql_require_primary_key' is set. Add a primary key to the table or unset this variable to avoid this message. Note that tables without a primary key can cause performance problems in row-based replication, so please consult your DBA before changing this setting.
mysql > set sql_generate_invisible_primary_key=1;
Query OK, 0 rows affected (0.00 sec)
mysql > create table nopk (a int);
Query OK, 0 rows affected (0.02 sec)
mysql > show create table nopk\G
*************************** 1. row ***************************
Table: nopk
Create Table: CREATE TABLE `nopk` (
`my_row_id` bigint unsigned NOT NULL AUTO_INCREMENT /*!80023 INVISIBLE */,
`a` int DEFAULT NULL,
PRIMARY KEY (`my_row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql > select * from nopk;
+------+
| a    |
+------+
|  100 |
+------+
1 row in set (0.00 sec)
`
因此，我们的应用程序根本不知道新列。但如果需要，我们仍然可以使用它，例如，轻松地将表读取或写入分成可预测的块：
`mysql > select my_row_id,a from nopk;
+-----------+------+
| my_row_id | a    |
+-----------+------+
|         1 |  100 |
+-----------+------+
1 row in set (0.00 sec)
`
请注意，对于缺少主键的架构，在强制执行变量 `sql_require_primary_key` 之前，最好首先启用 `sql_generate_invisible_primary_key` 并使用逻辑备份和恢复重新创建数据。简单的表优化不会增加不可见主键。无论如何，对于遗留的应用来说，拥有不可见主键（GIPK）应该是一个双赢的解决方案。