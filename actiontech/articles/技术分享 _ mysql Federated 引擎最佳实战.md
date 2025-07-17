# 技术分享 | mysql Federated 引擎最佳实战

**原文链接**: https://opensource.actionsky.com/20210517-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-05-17T00:56:08-08:00

---

作者：马文斌MySQL OCP 认证，PostgresSQL PGCA 认证，擅长 MySQL、PostgreSQL、dble 等开源数据库相关产品的备份恢复、读写分离、SQL 调优、监控运维、高可用架构设计等。目前任职于月亮小屋(中国)有限公司。本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 1. 背景
- 本地 MySQL 数据库要访问远程 MySQL 数据库的表中的数据，又不想用数据同步方式去实现，所以就考虑 FEDERATED 存储引擎来实现。
- 要允许这个存储引擎，当构建 MySQL 时使用 &#8211;with-federated-storage-engine 来 configure。
#### 2. Federated 引擎架构：
当客户端发出引用 FEDERATED 表的 SQL 语句时，本地服务器（执行 SQL 语句的地方）和远程服务器（实际存储数据的地方）之间的信息流如下：
- 存储引擎将遍历 FEDERATED 表具有的每一列，并构造一个引用远程表的适当 SQL 语句。
- 该语句使用 MySQL 客户端 API 发送到远程服务器。
- 远程服务器处理该语句，本地服务器检索该语句产生的任何结果（受影响的行数或结果集）。
- 如果该语句产生结果集，则每一列都将转换为 FEDERATED 引擎期望的内部存储引擎格式，并可用于将结果显示给发出原始语句的客户端。
- 架构图如下：
![](.img/fe246c06.png)											
#### 3. 相关特性
- 支持的语法：
- 在内部，实现使用 SELECT， INSERT， UPDATE，和 DELETE，但不会 HANDLER。
- 该 FEDERATED 存储引擎支持 SELECT， INSERT， UPDATE， DELETE， TRUNCATE TABLE，和索引。除之外，它不支持 ALTER TABLE、DROP TABLE 或任何直接影响表结构的数据定义语言语句。当前实现不使用准备好的语句。
- FEDERATED 接受 INSERT &#8230; ON DUPLICATE KEY UPDATE 语句，但是如果发生重复键冲突，该语句将失败并显示错误。
- 不支持的语法：
- FEDERATED 执行批量插入处理，以便将多行批量发送到远程表，从而提高了性能。另外，如果远程表是事务性的，则它可以使远程存储引擎在发生错误时正确执行语句回滚。此功能具有以下限制：1） 插入的大小不能超过服务器之间的最大数据包大小。如果插入超过此大小，它将被分成多个数据包，并可能发生回滚问题。2） 不会进行批量插入处理 INSERT &#8230; ON DUPLICATE KEY UPDATE。
- 如果远程表已经改变，对 FEDERATED 引擎而言是没有办法知道的。这样做的原因是，该表必须像数据文件一样工作，除了数据库系统以外，其他任何文件都不能写入。如果远程数据库发生任何更改，则可能会破坏本地表中数据的完整性。
- 使用 CONNECTION 字符串时，不能在密码中使用 “ @” 字符。您可以通过使用 CREATE SERVER 语句创建服务器连接来解决此限制。
- 在 insert_id 和 timestamp 选项都不会传播到数据提供者。
- DROP TABLE 针对 FEDERATED 表发出的任何语句仅删除本地表，而不删除远程表。
- FEDERATED 表不适用于查询缓存。
- FEDERATED 表不支持用户定义的分区。
#### 4. 环境
两个 mysql-5.7.26 实例
| ip | 端口 | 备注 |
| --- | --- | --- |
| 192.168.234.204 | 3306 | server-1 |
| 192.168.234.204 | 3310 | server-2 |
#### 5. 引擎设置
- 在配置文件制定开启 Federated 存储引擎
`配置文件中添加 federated 引擎就可以，两个实例都要添加
vim /etc/my.cnf
[mysqld]
federated
`- 查看 Federated 是否开启 [ FEDERATED 中 Support 状态 NO 表明引擎未开启]
```
mysql> show engines;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| FEDERATED          | YES     | Federated MySQL storage engine                                 | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
9 rows in set (0.00 sec)
 FEDERATED          | YES  说明已经开启了FEDERATED 引擎
```
#### 6. 部署
- 在 server-1 上有一个数据库 db1，在 server-2 上有数据库 db2，要在 server-2 的数据库 db2 上建立 server-1 的数据库 db1 上的表 tb1 的数据表链接 remote_tb1，通过普通用户 test 连接。
- 在 server-1 上建立测试的数据库数据库、表
`create database db1;
use db1;
create table tb1(
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT
)ENGINE=INNODB;
插入数据：
insert into tb1 select NULL;
insert into tb1 select NULL;
insert into tb1 select NULL;
查看数据
mysql> select * from tb1;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.00 sec)
`- 在 server-1 上建立测试的账号
```
create user 'test'@'192.168.%' IDENTIFIED BY '123456';
grant select,update,insert,delete on db1.* to 'test'@'192.168.%';
flush privileges;
```
- 在 server-2 上建立远程访问的数据库和表
```
create database db2;
use db2;
create table remote_tb1(
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT
)ENGINE=FEDERATED
CONNECTION='mysql://test:123456@192.168.234.204:3306/db1/tb1';
create table tb2(
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
name varchar(20)
)ENGINE=INNODB;
插入数据：
insert into tb2(name) select 'a';
insert into tb2(name) select 'b';
insert into tb2(name) select 'c';
mysql> select * from db2.tb2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
3 rows in set (0.00 sec)
```
- 在 server-2 中查询 server-1 中的 db1.tb1 是否有数据
```
mysql> select * from db2.remote_tb1;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.00 sec)
说明是关联上了，
测试下join：
select t2.* from db2.remote_tb1 as t1 join 
db2.tb2 as t2 on t1.id=t2.id 
where t2.name='c';
mysql> select t2.* from db2.remote_tb1 as t1 join
    -> db2.tb2 as t2 on t1.id=t2.id
    -> where t2.name='c';
+----+------+
| id | name |
+----+------+
|  3 | c    |
+----+------+
1 row in set (0.00 sec)
说明本地表和远程表关联也是可以的。
```
- 测试 server-2 操作下 DML， 观察 binlog 是否会写 GTID 事务
```
mysql> delete from db2.remote_tb1 where id =3;
Query OK, 1 row affected (0.00 sec)
mysql> select * from db2.remote_tb1;
+----+
| id |
+----+
|  1 |
|  2 |
+----+
2 rows in set (0.00 sec)
```
- /usr/local/mysql-5.7.26/bin/mysqlbinlog -vvv mysql-bin.000884 |grep -C 10 remote_tb1
```
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 40057515
#210415 14:25:53 server id 2342042  end_log_pos 40057586 CRC32 0x82abe215  Query thread_id=53 exec_time=0 error_code=0
SET TIMESTAMP=1618467953/*!*/;
SET @@session.sql_mode=1411383296/*!*/;
/*!\C utf8 *//*!*/;
SET @@session.character_set_client=33,@@session.collation_connection=33,@@session.collation_server=45/*!*/;
BEGIN
/*!*/;
# at 40057586
#210415 14:25:53 server id 2342042  end_log_pos 40057638 CRC32 0xddbc9dfc  Table_map: `db2`.`remote_tb1` mapped to number 416
# at 40057638
#210415 14:25:53 server id 2342042  end_log_pos 40057678 CRC32 0x5c28d0d0  Delete_rows: table id 416 flags: STMT_END_F
BINLOG '
cdx3YBOavCMANAAAACY7YwIAAKABAAAAAAEAA2RiMgAKcmVtb3RlX3RiMQABAwAA/J283Q==
cdx3YCCavCMAKAAAAE47YwIAAKABAAAAAAEAAgAB//4DAAAA0NAoXA==
'/*!*/;
### DELETE FROM `db2`.`remote_tb1`
### WHERE
###   @1=3 /* INT meta=0 nullable=0 is_null=0 */
# at 40057678
#210415 14:25:53 server id 2342042  end_log_pos 40057750 CRC32 0xb37fe7b3  Query thread_id=53 exec_time=0 error_code=0
SET TIMESTAMP=1618467953/*!*/;
COMMIT
/*!*/;
从 binlog SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/; 是可以看出，链接端操作DML是把GTID 事务隐藏了。
```
- server-2 服务器观察 remote_tb2 相关文件
.frm 表定义文件　[ Federated链接库本地不产生数据文件 ]
`[root@EOS_DB04 db2]# pwd
/mysqlData/3310_data/data/db2
[root@EOS_DB04 db2]# ll
total 128
-rw-r----- 1 mysql mysql    67 Apr 15 14:11 db.opt
-rw-r----- 1 mysql mysql  8556 Apr 15 14:11 remote_tb1.frm
-rw-r----- 1 mysql mysql  8586 Apr 15 14:18 tb2.frm
-rw-r----- 1 mysql mysql 98304 Apr 15 14:18 tb2.ibd`
## 总结
对比其他的数据同步产品，这种建立 链接 跨 ip 跨库查询会显轻便一些，搭建起来很方便。
**文章推荐：**
[技术分享 | 基于 GTID 的多源复制](https://opensource.actionsky.com/20201103-mysql/)