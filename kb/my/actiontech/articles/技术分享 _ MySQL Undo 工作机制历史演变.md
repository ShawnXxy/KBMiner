# 技术分享 | MySQL Undo 工作机制历史演变

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-mysql-undo-%e5%b7%a5%e4%bd%9c%e6%9c%ba%e5%88%b6%e5%8e%86%e5%8f%b2%e6%bc%94%e5%8f%98/
**分类**: MySQL 新特性
**发布时间**: 2024-09-03T22:06:21-08:00

---

前几天遇到一个关于 Undo 变大的 CASE，为了方便后续排查问题，于是系统的梳理 Undo 表空间的相关知识，希望对读者朋友有所帮助。
> 作者：杨奇龙，网名“北在南方”，资深 DBA，主要负责数据库架构设计和运维平台开发工作，擅长数据库性能调优、故障诊断。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 1700 字，预计阅读需要 6 分钟。
## 前言
前几天遇到一个关于 Undo 变大的 CASE（*大致的场景参见文章末尾*），为了方便后续排查问题，于是系统的梳理 Undo 表空间的相关知识，希望对读者朋友有所帮助。
## Undo 工作机制
### 保障事务原子性,提供数据回滚
当数据库崩溃时或者事务回滚时，InnoDB 事务系统可以利用 Undo Log 来进行数据回滚。
### 多版本并发控制（MVCC）- 隔离性
**InnoDB 存储引擎中 MVCC 的实现是通过 Undo Log 来实现的。**
当事务 A 读取某一行记录时，若该记录已经被其他事务 B 占用，当前事务 A 可以通过 Undo Log 读取之前的行版本信息，以此实现非锁定读取（如果有长时间的查询，会导致历史的 Undo 不能及时清理，进而导致 Undo Log 膨胀）。
## UNDO 表空间管理发展史
### 3.1 MySQL 5.6 版本之前
Undo Tablespace 是在 ibdata 中与系统表空间一起。比较常见的问题是由于大事务不提交导致 ibdata 膨胀，而且事务提交之后不能回收空间，进而浪费大量的空间甚至把磁盘打爆，同时也增加了数据库物理备份的时间。
此时，**重建数据库是唯一的解决方法。**
### 3.2 MySQL 5.6 版本
InnoDB 支持设置独立的 Undo Tablespace，也即 Undo Log 可以存储于 ibdata 文件之外。但是该特性存在一定的限制：
- 使用者必须在 初始化实例的时候，通过设置 `innodb_undo_tablespaces` 的值来实现 Undo Tablespace 独立，而且在初始化完成后不可更改。默认值为 0，表示不独立设置 Undo 的 Tablespace，默认记录到 ibdata 中。
- 修改 `innodb_undo_tablespaces` 的值会导致数据库无法启动。
- Undo Tablepsace 的 Space ID 必须从 1 开始，无法增加或者删除 Undo Tablespace。
### 3.3 MySQL 5.7 版本
引入一个 让 DBA 开心的功能 &#8212; **在线 truncate undo tablespace**。 该功能通过 `innodb_undo_log_truncate` 参数来控制。
### 3.4 MySQL 8.0 版本
MySQL 对 Undo Tablespace 进一步优化。
- 在 8.0 版本中，独立 Undo Tablespace 特性默认打开。从 8.0.3 版本开始，默认 Undo Tablespace 的个数从 0 调整为 2。
- 支持动态在线增加/删除 Undo Tablespace 。
- Undo Tablespace 的命名从 `undoNNN` 修改为 `undo_NNN` 。
- 在 8.0 之前只能创建 128个 回滚段，而在 8.0 版本开始，每个 Undo Tablespace 可以创建 128 个回滚段。共有 `innodb_rollback_segments` * `innodb_undo_tablespaces` 个回滚段。在高并发下可以显著的减少因为分配到同一个回滚段内的事务间产生的锁冲突，从而提高系统并行性能。
- `Innodb_undo_truncate` 参数默认打开， Undo Tablespace 大小超过 `innodb_max_undo_log_size` 来控制时，就会触发 Online Truncate。
- 支持 Undo Tablespace 加密。
## Undo 表空间维护
我们通过模拟 Undo 文件增大、手动添加 Undo 表空间和文件的过程，来学习 Undo 表空间的管理操作。基本思路是：
- 一般默认 MySQL 实例有 2 个 Undo Tablespace。
- 添加新的 Undo 表空间 A。
- 设置老的 Undo 表空间 B 为 inactive，系统基于 `innodb_undo_log_truncate =ON` 自动回收 Undo 文件空间。
- 设置老的 Undo 表空间 B 位 active。
- 次数可以保留新的 Undo 表空间 A 或者设置 Undo 表空间 A 为 inactive ，然后删除。
接下来我们根据以上的思路进行测试。
#### 1. 查看当前 Undo 表空间和状态
`mysql > SELECT NAME, STATE 
> FROM INFORMATION_SCHEMA.INNODB_TABLESPACES 
> WHERE NAME LIKE '%undo%';
+-----------------+--------+
| NAME            | STATE  |
+-----------------+--------+
| innodb_undo_001 | active |
| innodb_undo_002 | active |
+-----------------+--------+
2 rows in set (0.02 sec)
`
#### 2. 添加新的 Undo 表空间
系统默认会分配 2 个 `innodb` 开头的表空间。 如果手工新增 Undo 表空间，创建 `innodb` 开头的表空间名称会报错，提示以 `innodb` 开头的表空间名称被系统占用。
`mysql > create undo tablespace innodb_undo_003 add datafile 'undo_003.ibu';
ERROR 3119 (42000): InnoDB: Tablespace names starting with `innodb_` are reserved.
`
文件必须是 `.ibu` 结尾，否则也是会报错。
#### 3. 创建 Undo Tablespace
创建 Undo Tablespace 文件 `undo_003`。
`mysql > create undo tablespace undo_003 add datafile 'undo_003.ibu';
Query OK, 0 rows affected (0.14 sec)
mysql > SELECT NAME, STATE 
> FROM INFORMATION_SCHEMA.INNODB_TABLESPACES 
> WHERE NAME LIKE '%undo%';
+-----------------+--------+
| NAME            | STATE  |
+-----------------+--------+
| innodb_undo_001 | active |
| innodb_undo_002 | active |
| undo_003        | active |
+-----------------+--------+
3 rows in set (0.00 sec)
`
#### 4. 自动回收 Undo 文件空间
设置 `innodb_undo_002` 为 inactive ，让系统自动收缩 Undo 文件。
`mysql > ALTER UNDO TABLESPACE innodb_undo_002 SET INACTIVE;
Query OK, 0 rows affected (0.00 sec)
mysql > SELECT NAME, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE NAME LIKE '%undo%';
+-----------------+--------+
| NAME            | STATE  |
+-----------------+--------+
| innodb_undo_001 | active |
| innodb_undo_002 | empty  | ## 状态为 empty 时即可触发系统 undo表空间回收
| undo_003        | active |
+-----------------+--------+
3 rows in set (0.00 sec)
`
我们不能删除系统默认创建 `innodb` 开头的 Undo 表空间，系统会提示 **该空间位系统保留空间**。
`mysql > DROP UNDO TABLESPACE  innodb_undo_002;
ERROR 3119 (42000): InnoDB: Tablespace names starting with `innodb_` are reserved.
mysql >ALTER UNDO TABLESPACE innodb_undo_002 SET ACTIVE;
Query OK, 0 rows affected (0.00 sec)
`
#### 5. 删除新的 Undo 表空间
```
mysql > ALTER UNDO TABLESPACE undo_003 SET INACTIVE;
Query OK, 0 rows affected (0.00 sec)
mysql > SELECT NAME, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE NAME LIKE '%undo%';
+-----------------+--------+
| NAME            | STATE  |
+-----------------+--------+
| innodb_undo_001 | active |
| innodb_undo_002 | active |
| undo_003        | empty  |
+-----------------+--------+
3 rows in set (0.00 sec)
mysql >DROP UNDO TABLESPACE undo_003;
Query OK, 0 rows affected (0.01 sec)
mysql > SELECT NAME, STATE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE NAME LIKE '%undo%';
+-----------------+--------+
| NAME            | STATE  |
+-----------------+--------+
| innodb_undo_001 | active |
| innodb_undo_002 | active |
+-----------------+--------+
2 rows in set (0.00 sec)
```
## UNDO 相关参数
- **innodb_undo_directory**：存储 Undo 文件的目录。
- **innodb_undo_log_truncate**：用于打开/关闭 Truncate Undo 特性，可动态调整。MySQL 8.0 默认开启。
- **innodb_undo_tablespaces**：默认为 2，用于初始化实例时设置 Undo Tablespace 的个数，该参数可以动态调整。要实现在线 Truncate Undo，该参数需要大于等于 2，因为在 Truncate 一个 Undo Log 文件时，需要保证另外一个是可用的。手动维护的时候可以设置为 3 或者更大。
- **innodb_purge_rseg_truncate_frequency**：默认最大值 128，用于控制 purge 回滚段的频率。也就是 128 次后才会触发一次 Undo 的 Truncate，而每次清理的 Undo Page 由 `innodb_purge_batch_size` 参数决定。`innodb_purge_batch_size` 默认为 300，也即 300×128 个 Undo 批次清理后才会触发 Undo 表空间的收缩操作。该参数越小，Undo 表空间被尝试 Truncate 的频率越高。
- **innodb_max_undo_log_size**：控制 Undo 表空间文件的大小，超过这个阈值时才会去尝试 Truncate。Truncate 后的大小默认为 10M。
## 学以致用
纸上来得终觉浅，绝知此事要躬行。
前面介绍了 Undo 的理论知识，现在 DBA 小明遇到一个问题：一套 MySQL 生产实例（8.0 版本），其架构为一主多从，其中一个备库承担只读服务。Undo 文件在一天内暴涨到 270G 左右。大家有什么思路帮助小明来解决 Undo 表空间回收的问题？