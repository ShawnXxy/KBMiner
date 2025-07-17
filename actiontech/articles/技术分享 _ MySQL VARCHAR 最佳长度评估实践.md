# 技术分享 | MySQL VARCHAR 最佳长度评估实践

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-mysql-varchar-%e6%9c%80%e4%bd%b3%e9%95%bf%e5%ba%a6%e8%af%84%e4%bc%b0%e5%ae%9e%e8%b7%b5/
**分类**: MySQL 新特性
**发布时间**: 2024-05-08T00:28:51-08:00

---

你的 VARCHAR 长度合适么？
> 作者：官永强，爱可生 DBA 团队成员，擅长 MySQL 运维方面的技能。热爱学习新知识，亦是个爱打游戏的宅男。
作者：李富强，爱可生 DBA 团队成员，熟悉 MySQL，TiDB，OceanBase 等数据库。相信持续把对的事情做好一点，会有不一样的收获。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 2200 字，预计阅读需要 8 分钟。
# 背景描述
有客户反馈，他们对一个 **VARCHAR** 类型的字段进行长度扩容。第一次可以很快就可以修改好，但是第二次却需要执行很久。比较疑惑明明表中的数据量是差不多的，**为什么从 `VARCHAR(20)` 调整为 `VARCHAR(50)` 就比较快，但是从 `VARCHAR(50)` 调整为 `VARCHAR(100)` 就需要执行很久呢？** 于是我们对该情况进行场景复现并进行问题分析。
# 环境信息
本次验证涉及到的产品及版本信息如下：
| 产品 | 版本 |
| --- | --- |
| MySQL | 5.7.25-log MySQL Community Server (GPL) |
| Sysbench | sysbench 1.0.17 |
# 场景复现
## 3.1 数据准备
`mysql> show create table test.sbtest1;
+---------+----------------------------------------+
| Table   | Create Table                           |
+---------+----------------------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
`pad` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+----------------------------------------+
1 row in set (0.00 sec)
mysql> select count(*) from test.sbtest1;
+----------+
| count(*) |
+----------+
|  1000000 |
+----------+
1 row in set (0.10 sec)
`
## 3.2 问题验证
模拟客户的描述，我们对字段 `c` 进行修改，将 `VARCHAR(20)` 修改为 `VARCHAR(50)` 后再修改为 `VARCHAR(100)`，并观察其执行所需时间，以下是相关的操作命令以及执行结果：
`mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(50);
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> show create table test.sbtest1;
+---------+-------------------------------+
| Table   | Create Table                  |
+---------+-------------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
`pad` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+--------------------------------------------------------+
1 row in set (0.00 sec)
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(100);
Query OK, 1000000 rows affected (4.80 sec)
Records: 1000000  Duplicates: 0  Warnings: 0
mysql> show create table test.sbtest1;
+---------+---------------------------+
| Table   | Create Table              |
+---------+---------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
`pad` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+------------------------------------------------------------------------+
1 row in set (0.00 sec)
`
通过验证发现，该问题会稳定复现，故继续尝试去修改，最终发现在修改 `VARCHAR(63)` 为 `VARCHAR(64)` 时需要执行很久，但在 64 之后继续进行长度扩容发现可以很快完成。
`mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(63);
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(64);
Query OK, 1000000 rows affected (4.87 sec)
Records: 1000000  Duplicates: 0  Warnings: 0
mysql> show create table test.sbtest1;
+---------+---------------+
| Table   | Create Table  |
+---------+---------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
`pad` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(65);
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(66);
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
## 3.3 问题分析
对于 `VARCHAR(63)` 修改为 `VARCHAR(64)` 需要执行很久的这个情况进行分析。通过查阅[官方文档](https://dev.mysql.com/doc/refman/5.7/en/storage-requirements.html#data-types-storage-reqs-strings) 发现，由于 `VARCHAR` 字符类型在字节长度为 1 时可存储的字符为 0~255。当前字符集类型为 UTF8MB4，由于 UTF8MB4 为四字节编码字符集，即一个字节长度可存储 63.75（255/4）个字符，所以当我们将 `VARCHAR(63)` 修改为 `VARCHAR(64)` 时，需要增加一个字节去进行数据的存储，就要通过建立临时表的方式去完成本次长度扩容，故需要花费大量时间。
# 拓展验证
## 4.1 数据准备
`mysql> show create table test_utf8.sbtest1;
+---------+----------------------------------------+
| Table   | Create Table                           |
+---------+----------------------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(20) NOT NULL DEFAULT '',
`pad` varchar(20) NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8 |
+---------+------------------+
1 row in set (0.00 sec)
mysql> select count(*) from test_utf8.sbtest1;
+----------+
| count(*) |
+----------+
|  1000000 |
+----------+
1 row in set (0.10 sec)
`
## 4.2 UTF8 场景验证
由于 UTF8 为三字节编码字符集，即一个字节可存储 85（255/3=85）个字符。
本次修改顺序：VARCHAR(20)→VARCHAR(50)→VARCHAR(85)，并观察其执行所需时间，以下是相关的操作命令以及执行结果：
`mysql>  ALTER TABLE test_utf8.sbtest1 MODIFY c VARCHAR(50) ,algorithm=inplace,lock=none;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> ALTER TABLE test_utf8.sbtest1 MODIFY c VARCHAR(85) ,algorithm=inplace,lock=none;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> show create table test_utf8.sbtest1;
+---------+-------------------------------+
| Table   | Create Table                  |
+---------+-------------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(85) DEFAULT NULL,
`pad` varchar(20) NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8 |
+---------+--------------------------------------------------+
1 row in set (0.00 sec)
`
修改顺序：VARCHAR(85)→VARCHAR(86)→VARCHAR(100)，此时我们会观察到执行的 SQL 语句直接返回报错。于是我们删除 `algorithm=inplace ,lock=none` 这两个参数，即允许本次 SQL 创建临时表以及给目标表上锁，然后重新执行 SQL，以下是相关的操作命令以及执行结果：
`mysql> ALTER TABLE test_utf8.sbtest1 MODIFY c VARCHAR(86) ,algorithm=inplace,lock=none;
ERROR 1846 (0A000): ALGORITHM=INPLACE is not supported. Reason: Cannot change column type INPLACE. Try ALGORITHM=COPY.
mysql> ALTER TABLE test_utf8.sbtest1 MODIFY c VARCHAR(86);
Query OK, 1000000 rows affected (4.94 sec)
Records: 1000000  Duplicates: 0  Warnings: 0
mysql> show create table test_utf8.sbtest1;
+---------+-------------------------------+
| Table   | Create Table                  |
+---------+-------------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(86) DEFAULT NULL,
`pad` varchar(20) NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8 |
+---------+--------------------------------------------------+
1 row in set (0.00 sec)
mysql> ALTER TABLE test_utf8.sbtest1 MODIFY c VARCHAR(100) ,algorithm=inplace,lock=none;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
## 4.3 UTF8MB4 场景验证
由于 UTF8MB4 为四字节编码字符集，即一个字节长度可存储 63（255/4=63.75）个字符。
本次修改顺序：VARCHAR(20)→VARCHAR(50)→VARCHAR(63)，并观察其执行所需时间，以下是相关的操作命令以及执行结果：
`mysql>  ALTER TABLE test.sbtest1 MODIFY c VARCHAR(50) ,algorithm=inplace,lock=none;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(63) ,algorithm=inplace,lock=none;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> show create table test.sbtest1;
+---------+-------------------------+
| Table   | Create Table           |
+---------+-------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(63) COLLATE utf8mb4_bin DEFAULT NULL,
`pad` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+-------------------------------------------------------------------------+
1 row in set (0.00 sec)
`
本次修改顺序：VARCHAR(63)→VARCHAR(64)→VARCHAR(100)，此时我们会观察到执行的 SQL 语句直接返回报错。于是我们删除 `algorithm=inplace, lock=none` 这两个参数，即允许本次 SQL 创建临时表以及给目标表上锁，然后重新执行 SQL，以下是相关的操作命令以及执行结果：
`mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(64) ,algorithm=inplace,lock=none;
ERROR 1846 (0A000): ALGORITHM=INPLACE is not supported. Reason: Cannot change column type INPLACE. Try ALGORITHM=COPY.
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(64) ;
Query OK, 1000000 rows affected (4.93 sec)
Records: 1000000  Duplicates: 0  Warnings: 0
mysql> show create table test.sbtest1;
+---------+--------------------------+
| Table   | Create Table             |
+---------+--------------------------+
| sbtest1 | CREATE TABLE `sbtest1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`k` int(11) NOT NULL DEFAULT '0',
`c` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
`pad` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+-------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> ALTER TABLE test.sbtest1 MODIFY c VARCHAR(100) ,algorithm=inplace,lock=none;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
## 4.4 对比分析
| 字符长度修改 | UTF8(MB3) | UTF8MB4 |
| --- | --- | --- |
| 20->50 | online ddl (inplace) | online ddl (inplace) |
| 50->100 | online ddl (copy) | online ddl (copy) |
| X->Y | 当Y*3<256 时，inplace
当X*3>=256，inplace | 当 Y*4<256 时，inplace
当 X*4>=256，inplace |
| 备注 | 一个字符最大占用 3 个字节 | 一个字符最大占用 4 个字节 |
# 结论
**当一个字段的最大字节长度 >=256 字符时，需要 2 个字节来表示字段长度。**
使用 UTF8MB4 举例：
- 对于字段的最大字节长度在 256 字符内变化 (即 x*4<256 且 Y*4<256)，online ddl 走 inplace 模式，效率高。
- 对于字段的最大字节长度在 256 字符外变化 (即 x*4>=256 且 Y*4>=256) ，online ddl 走 inplace 模式，效率高。
- 否则，online ddl 走 copy 模式，效率低.
- UTF8(MB3) 同理。
# 建议
为避免由于后期字段长度扩容，online ddl 走效率低的 copy 模式，建议：
- 对于 UTF8(MB3) 字符类型：
字符个数小于 50 个，建议设置为 VARCHAR(50) 或更小的字符长度。
- 字符个数接近 84（256/3=83.33）个，建议设置为varchar(84)或更大的字符长度。
- 对于 UTF8MB4 字符类型：
字符个数小于 50 个，建议设置为 VARCHAR(50)，或更小的字符长度。
- 字符个数接近 64（256/4=64）个，建议设置为 VARCHAR(64) 或更大的字符长度。
*本次验证结果仅供参考，若您需要在生产环境中进行操作，请结合实际情况合理定义 VARCHAR 的长度，避免造成经济损失。*