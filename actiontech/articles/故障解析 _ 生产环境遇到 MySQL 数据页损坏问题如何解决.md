# 故障解析 | 生产环境遇到 MySQL 数据页损坏问题如何解决？

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e8%a7%a3%e6%9e%90-%e7%94%9f%e4%ba%a7%e7%8e%af%e5%a2%83%e9%81%87%e5%88%b0-mysql-%e6%95%b0%e6%8d%ae%e9%a1%b5%e6%8d%9f%e5%9d%8f%e9%97%ae%e9%a2%98%e5%a6%82%e4%bd%95%e8%a7%a3%e5%86%b3/
**分类**: MySQL 新特性
**发布时间**: 2023-08-16T21:33:50-08:00

---

当数据页破坏，如何根据实例的健康状况选择不同的策略定位损坏文件并恢复。
> 作者：徐文梁
爱可生 DBA 成员，一个执着于技术的数据库工程师，主要负责数据库日常运维工作。擅长 MySQL，Redis 及其他常见数据库也有涉猎；喜欢垂钓，看书，看风景，结交新朋友。
本文来源：原创投稿
- 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# 问题背景
四月份的时候，遇到一次实例异常 crash 的问题。当时数据库自动重启，未对生产造成影响，未做处理，但是还是记录了下错误信息，错误日志中有如下信息:
`InnoDB: End of page dump
InnoDB: Page may be an index page where index id is 8196
2023-04-11T07:57:42.508371+08:00 0 [ERROR] [FATAL] InnoDB: Apparent corruption of an index page [page id: space=3859, page number=842530] to be written to data file. We intentionally crash the server to prevent corrupt data from ending up in data files.
2023-04-11 07:57:42 0x7fe4d42cf080 InnoDB: Assertion failure in thread 140620788985984 in file ut0ut.cc line 921
InnoDB: We intentionally generate a memory trap.
`
因为当时自动恢复了，并未重视这个问题，然后六月份的时候实例又 crash 了。查看报错信息，报错信息如下：
`2023-06-23T04:32:36.538380+08:00 0 [ERROR] InnoDB: Probable data corruption on page 673268. Original record on that page;
(compact record)2023-06-23T04:32:36.538426+08:00 0 [ERROR] InnoDB: Cannot find the dir slot for this record on that page;
(compact record)2023-06-23 04:32:36 0x7fe2bf68f080 InnoDB: Assertion failure in thread 140611850662016 in file page0page.cc line 153
InnoDB: We intentionally generate a memory trap.
`
两次的报错信息很相似，出现一次是偶然，两次就值得重视了。虽然之前很幸运未对生产造成影响，但是如果后面哪一天异常了导致实例无法启动，那不就是妥妥的一个生产故障嘛，作为 DBA 要有忧患意思，必须要提前准备好应对之策，针对此类问题，该如何排查以及解决？通过查阅资料和向前辈请教，也算有所收获，想着如果有其他同学遇到类似问题也可作为参考，于是有了此文。
# 问题分析
一般来说，数据页损坏，错误日志中都会显示具体的 **page number**，其他情况暂不考虑。在此前提下，根据实例状态可以将数据页损坏分为以下两种场景：
- 实例能正常启动
- 实例无法正常启动
场景不同，处理方法也略有不同，下面分别展开详细分析：
## 场景一：实例能正常启动
此时借助通过错误日志中的信息，可以通过查询元数据表获取数据页所属信息。考虑生产环境信息安全，在测试环境建立测试表进行展示。
测试环境表结构如下:
`mysql> use test;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> show create table t_user\G;
*************************** 1. row ***************************
Table: t_user
Create Table: CREATE TABLE `t_user` (
`id` bigint(20) NOT NULL AUTO_INCREMENT,
`name` varchar(255) DEFAULT NULL,
`age` tinyint(4) DEFAULT NULL,
`create_time` datetime DEFAULT NULL,
`update_time` datetime DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=178120 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
ERROR:
No query specified
`
根据错误信息中提示的 **page number** 信息来查看数据页信息，查询方式如下：
`mysql> use information_schema;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> select * from  INNODB_BUFFER_PAGE where PAGE_NUMBER=1156 limit 10;
+---------+----------+-------+-------------+-----------+------------+-----------+-----------+---------------------+---------------------+-------------+-----------------+------------+----------------+-----------+-----------------+------------+---------+--------+-----------------+
| POOL_ID | BLOCK_ID | SPACE | PAGE_NUMBER | PAGE_TYPE | FLUSH_TYPE | FIX_COUNT | IS_HASHED | NEWEST_MODIFICATION | OLDEST_MODIFICATION | ACCESS_TIME | TABLE_NAME      | INDEX_NAME | NUMBER_RECORDS | DATA_SIZE | COMPRESSED_SIZE | PAGE_STATE | IO_FIX  | IS_OLD | FREE_PAGE_CLOCK |
+---------+----------+-------+-------------+-----------+------------+-----------+-----------+---------------------+---------------------+-------------+-----------------+------------+----------------+-----------+-----------------+------------+---------+--------+-----------------+
|       0 |       64 |   126 |        1156 | INDEX     |          0 |         0 | NO        |                   0 |                   0 |           0 | `test`.`t_user` | idx_name   |            515 |     15965 |               0 | FILE_PAGE  | IO_NONE | NO     |               0 |
+---------+----------+-------+-------------+-----------+------------+-----------+-----------+---------------------+---------------------+-------------+-----------------+------------+----------------+-----------+-----------------+------------+---------+--------+-----------------+
1 row in set (0.18 sec)
`
> 注意：查询 [INNODB_BUFFER_PAGE 系统表](https://dev.mysql.com/doc/refman/5.7/en/information-schema-innodb-buffer-page-table.html) 会对性能有影响，因此不建议随意在生产环境执行。
另外，如果错误日志中有提示 `space id` 和 `index id` 相关信息，则也可以通过如下方式（涉及 [INNODB_SYS_INDEXES](https://dev.mysql.com/doc/refman/5.7/en/information-schema-innodb-sys-indexes-table.html) 和 [INNODB_SYS_TABLES](https://dev.mysql.com/doc/refman/5.7/en/information-schema-innodb-sys-tables-table.html) 系统表 ）进行查询：
`mysql> select b.INDEX_ID, a.NAME as TableName, a.SPACE as Space,b.NAME as IndexName from INNODB_SYS_TABLES a,INNODB_SYS_INDEXES b where a.SPACE =b.SPACE and a.SPACE=126 and b.INDEX_ID=225;
+----------+-------------+-------+-----------+
| INDEX_ID | TableName   | Space | IndexName |
+----------+-------------+-------+-----------+
|      225 | test/t_user |   126 | idx_name  |
+----------+-------------+-------+-----------+
1 row in set (0.01 sec)
`
根据上面的查询结果，确定损坏的页是属于主键还是辅助索引，如果属于主键索引，因为在 MySQL 中索引即数据，则可能会导致数据丢失，如果是辅助索引，删除索引重建即可。
## 场景二：实例无法正常启动
此时可以通过两种方式尝试拉起实例。
### 方法一
使用 [innodb_force_recovery](https://dev.mysql.com/doc/refman/5.7/en/forcing-innodb-recovery.html) 参数进行强制拉起 MySQL 实例。
正常情况下可以 `innodb_force_force_recovery` 值应该设置为 0。当紧急情况下实例无法正常启动时可以尝试将其设置为 >0 的值，强制拉起实例然后将数据逻辑备份导出进行恢复。`innodb_force_recovery` 值最高支持设置到 6，但是值为 4 或更大可能会永久损坏数据文件。因此当强制 InnoDB 恢复时，应始终以 `innodb_force_recovery=1` 开头，并仅在必要时递增该值。
### 方法二
使用 [inno_space](https://github.com/baotiao/inno_space) 工具进行数据文件进行修复。
> **inno_space** 是一个可以直接访问 InnoDB 内部文件的命令行工具，可以通过该工具查看 MySQL 数据文件的具体结构，修复 `corrupt page`。[更多参考](http://mysql.taobao.org/monthly/2021/11/02/)
如果 InnoDB 表文件中的 page 损坏，导致实例无法启动，可以尝试通过该工具进行修复，如果损坏的只是 `leaf page`，inno_space 可以将 `corrupt page` 跳过，从而保证实例能够启动，并且将绝大部分的数据找回。示例：
`# 假设 MySQL 错误日志中有类似报错如下：
[ERROR] [MY-030043] [InnoDB] InnoDB: Corrupt page resides in file: .test/t_user.ibd, offset: 163840, len: 16384
[ERROR] [MY-011906] [InnoDB] Database page corruption on disk or a failed file read of page [page id: space=126, page number=1158]. You may have to recover from a backup.
# 通过如下方式进行修复：
# 删除损坏的数据页中损坏部分。
./inno -f /opt/mysql/data/3307/test/t_user.ibd   -d 10
# 更新损坏的数据页中 checksum 值。
./inno -f /opt/mysql/data/3307/test/t_user.ibd   -u 10
启动 MySQL 服务。
`
# 问题总结
经过前面分析，了解数据页损坏场景的处理方式。哪怕极端场景下，也可以做到从容不慌，尽可能少丢数据甚至能够不丢数据。但是如果是生产环境，尤其是金融行业，是无法容忍丢失一条数据的，比较有可能这一条数据就涉及几个小目标呢，因此，重要的事情说三遍，**一定要备份！一定要备份！一定要备份！**