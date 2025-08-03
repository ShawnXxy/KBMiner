# 故障分析 | MySQL 使用 Mysqldump 备份导入数据导致主从异常

**原文链接**: https://opensource.actionsky.com/20211214-mysqldump/
**分类**: MySQL 新特性
**发布时间**: 2021-12-13T18:43:57-08:00

---

作者：雷文霆
爱可生华东交付服务部  DBA 成员，主要负责Mysql故障处理及相关技术支持。爱好看书，电影。座右铭，每一个不曾起舞的日子，都是对生命的辜负。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 1 环境
> 
Mysql版本：5.7
架构：2套，1主1从
复制模式：基于GTID
`有两套Mysql主从，开发侧的需求是进行某个数据库的迁移(可以理解为数据库替换)，操作为drop database test01，然后备份远程数据库test01,最后进行本地数据库恢复。
备份工具: Mysqldump
恢复方式：source 备份文件
第1套的备份参数：--single-transaction  --add-drop-table 
第2套的备份参数：--single-transaction  --add-drop-table --set-gtid-purged=off
以上备份参数是在故障处理时收集的背景信息，
对于Mysqldump建议加上 --single-transaction和--master-data=2。前者可实现innodb一致性备份,后者可以记录备份信息。
参数解释：
--single-transaction 将事务隔离级别设置为RR，并在备份数据之前向服务器发送SQL语句，显示开启一个事务快照。
--add-drop-table  默认开启， Add a DROP TABLE before each create。会在创建表前添加drop table语句(一般在追加表中数据时使用,比如归档)
# 备份文件类似：
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test` (
--set-gtid-purged  默认为ON
是否在导出的sql 文件头部添加 set global gtid_purged='xxx:xxx' 信息。
# 默认为ON时，备份文件开头类似：
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0; # 需要重点关注的地方(导入不记录binlog)
-- GTID state at the beginning of the backup 
SET @@GLOBAL.GTID_PURGED='xxx:1-100';
# 使用 --set-gtid-purged=off 的特点
1.不用reset master就可以直接导入。
2.会在本地生成新的事务信息。(导入记录binlog)
`
## 2 问题描述
> 
DBA接到应用迁移需求后，在主库上执行了drop database操作，直到备份前复制都是正常的。
`第1套主从：没有添加--set-gtid-purged=off 选项
在主库source 备份文件之后，由于备份文件中[包含SET @@SESSION.SQL_LOG_BIN= 0;]，导入的数据没有记录binlog。
导致从库没有备份文件中的数据，之后复制会报SQL线程1146,数据不存在。
第2套主从：添加--set-gtid-purged=off 选项
在主库source 备份文件之后，由于备份文件中[不包含SET @@SESSION.SQL_LOG_BIN= 0;]导入的数据记录binlog。
`
## 3 复现步骤
`第1套：
# 在主库上创建数据
create database test01;
use test01;
create table table01(id int primary key);
# 模拟备份操作：
mysqldump -h172.20.134.2 -uadmin -P3306 -p123456   --single-transaction  --databases test01  > /opt/test01_set-gtid-purgedis_on.sql
## 备份文件内容：
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;
SET @@GLOBAL.GTID_PURGED='7b3a89d7-4866-11ec-b99b-0242ac148602:1-659286,
7b3adf4b-4866-11ec-b9e0-0242ac148604:1-3338';
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test01` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
USE `test01`;
--
-- Table structure for table `table01`
--
DROP TABLE IF EXISTS `table01`;
CREATE TABLE `table01` (
`id` int(11) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
LOCK TABLES `table01` WRITE;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
# 模拟迁移操作
在主库执行：
drop database test01;这个是DBA 帮助执行的
source /opt/test01_set-gtid-purgedis_on.sql;
# 登录从库检查复制状态 [正常的，因为还没有主库没有涉及到这个库的操作]
mysql> show slave status\G
*************************** 1. row ***************************
Slave_IO_State: Waiting for master to send event
Master_Host: 172.20.134.2
Master_User: universe_op
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.000002
Read_Master_Log_Pos: 34139867
Relay_Log_File: mysql-relay.000003
Relay_Log_Pos: 1646803
Relay_Master_Log_File: mysql-bin.000002
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
# 在主库模拟正常的业务操作
insert into table01(id)values(1);
select * from table01;
+----+
| id |
+----+
|  1 |
+----+
# 从库异常信息(SQL线程异常，显示操作的表不存在，原因是导入的数据没有记录到binlog)
show slave status\G
*************************** 1. row ***************************
Slave_IO_State: Waiting for master to send event
Master_Host: 172.20.134.2
Master_User: universe_op
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.000002
Read_Master_Log_Pos: 34704375
Relay_Log_File: mysql-relay.000003
Relay_Log_Pos: 2180665
Relay_Master_Log_File: mysql-bin.000002
Slave_IO_Running: Yes
Slave_SQL_Running: No
Replicate_Do_DB:
Replicate_Ignore_DB:
Replicate_Do_Table:
Replicate_Ignore_Table:
Replicate_Wild_Do_Table:
Replicate_Wild_Ignore_Table:
Last_Errno: 1146
Last_Error: Coordinator stopped because there were error(s) in the worker(s). The most recent failure being: Worker 1 failed executing transaction '7b3a89d7-4866-11ec-b99b-0242ac148602:662273' at master log mysql-bin.000002, end_log_pos 34674016. See error log and/or performance_schema.replication_applier_status_by_worker table for more details about this failure or others, if any.
select * from performance_schema.replication_applier_status_by_worker\G
*************************** 1. row ***************************
CHANNEL_NAME:
WORKER_ID: 1
THREAD_ID: NULL
SERVICE_STATE: OFF
LAST_SEEN_TRANSACTION: 7b3a89d7-4866-11ec-b99b-0242ac148602:662273
LAST_ERROR_NUMBER: 1146
LAST_ERROR_MESSAGE: Worker 1 failed executing transaction '7b3a89d7-4866-11ec-b99b-0242ac148602:662273' at master log mysql-bin.000002, end_log_pos 34674016; Error executing row event: 'Table 'test01.table01' doesn't exist'
LAST_ERROR_TIMESTAMP: 2021-11-22 16:27:10
第2套：
# 模拟备份操作：
mysqldump -h172.20.134.2 -uadmin -P3306 -p123456   --single-transaction --set-gtid-purged=off  --databases test01  > /opt/test01_set-gtid-purgedis_off.sql
备份文件内容：
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test01` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
USE `test01`;
DROP TABLE IF EXISTS `table01`;
CREATE TABLE `table01` (
`id` int(11) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
LOCK TABLES `table01` WRITE;
INSERT INTO `table01` VALUES (1),(2),(3),(4);
UNLOCK TABLES;
# 模拟迁移操作
在主库执行：
drop database test01; #这个是DBA 帮助执行的
(小插曲：)
source /opt/test01_set-gtid-purgedis_on.sql; # 此处导入了第一次的备份，发现有如下报错，才添加了--set-gtid-purged=off备份参数(这就是为什么在主库的binlog中看到了，两个事务，均执行了相同的drop database 操作)
ERROR 1840 (HY000): @@GLOBAL.GTID_PURGED can only be set when @@GLOBAL.GTID_EXECUTED is empty.
binlog的异常现象：(出现了)
SET @@SESSION.GTID_NEXT= '7b3a89d7-4866-11ec-b99b-0242ac148602:660309'
drop database test01  # 执行者是DBA
----中间无创建语句----
SET @@SESSION.GTID_NEXT= '7b3a89d7-4866-11ec-b99b-0242ac148602:666084'
drop database test01  # 执行者是迁移人员
source /opt/test01_set-gtid-purgedis_off.sql; 再次执行了导入操作，主库写入了数据，并记录到了binlog中
# 从库异常信息(SQL线程异常，显示操作的库不存在,原因是第一次导入的数据没有记录binlog,加了--set-gtid-purged=off备份参数之后，记录了binlog。第一次导入的数据对从库是不可见的，所以主库在执行完第一次导入之后的drop database 在从库就会显示不存在这个库)
Slave_IO_State: Waiting for master to send event
Master_Host: 172.20.134.2
Master_User: universe_op
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.000002
Read_Master_Log_Pos: 36372942
Relay_Log_File: mysql-relay.000004
Relay_Log_Pos: 1696956
Relay_Master_Log_File: mysql-bin.000002
Slave_IO_Running: Yes
Slave_SQL_Running: No
Replicate_Do_DB:
Replicate_Ignore_DB:
Replicate_Do_Table:
Replicate_Ignore_Table:
Replicate_Wild_Do_Table:
Replicate_Wild_Ignore_Table:
Last_Errno: 1008
Last_Error: Coordinator stopped because there were error(s) in the worker(s). The most recent failure being: Worker 1 failed executing transaction '7b3a89d7-4866-11ec-b99b-0242ac148602:666084' at master log mysql-bin.000002, end_log_pos 36372942. See error log and/or performance_schema.replication_applier_status_by_worker table for more details about this failure or others, if any.
select * from performance_schema.replication_applier_status_by_worker\G
*************************** 1. row ***************************
CHANNEL_NAME:
WORKER_ID: 1
THREAD_ID: NULL
SERVICE_STATE: OFF
LAST_SEEN_TRANSACTION: 7b3a89d7-4866-11ec-b99b-0242ac148602:666084
LAST_ERROR_NUMBER: 1008
LAST_ERROR_MESSAGE: Worker 1 failed executing transaction '7b3a89d7-4866-11ec-b99b-0242ac148602:666084' at master log mysql-bin.000002, end_log_pos 36372942; Error 'Can't drop database 'test01'; database doesn't exist' on query. Default database: 'test01'. Query: 'drop database test01'
LAST_ERROR_TIMESTAMP: 2021-11-22 17:15:50
`
## 4 分析过程
`第1套：
1.记录从库复制异常信息，报错为记录不存在，属于数据不一致。
2.咨询，各方的操作记录。
3.解析主库的binlog文件，验证数据的导入情况。[从迁移开始到应用服务开启，之间没有数据记录]
4.检查备份命令和备份文件内容。[这里就会发现数据是不记录binlog的方式导入的]
第2套：
和第1套不同的是，在主库的binlog中两条连续事务，记录了相同的drop database 操作[在现场]。
第一次删除为DBA执行的，迁移人员导入之后，发现有报错，为了方便第二次导入，执行了第二次删除。均属于正常操作。
`
## 5 结论
> 
对于&#8211;set-gtid-purged参数
`1.Mysqldump中sql_log_bin默认是关闭的。
如果数据要导入主库，可以通过--set-gtid-purged=off备份参数，不会在备份文件中记录SET @@GLOBAL.GTID_PURGED的值。
不需要reset master可直接导入。
2.全备的情况下不添加，--set-gtid-purged 默认为ON(常用于重做主从)，部分备份时添加 --set-gtid-purged=off(可在主上做部分恢复，在从上不推荐使用，即便是通过SET @@SESSION.SQL_LOG_BIN= 0;source alldb.sql;的方式导入，之后的数据更新可能会导致复制出现数据已存在的异常。也不适应与备份文件较大的情况。)
`正确的操作是导入从库之后，主从数据可以保持一致，然后reset master;set @@global.gtid_purged='gtid段'; change master to重建复制。`
3.备份文件默认，库是不存在就创建，表是存在就删除重建。
4.对于需要导入主库的场景，建议开启set-gtid-purged=off参数，导入数据时，记录binlog(更新事务号和Position)，不影响复制。
5.对于需要导入从库的场景，建议保持默认或是不设置此参数，导入数据时，不记录binlog。
# 以下摘自官网：[link]https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html#option_mysqldump_master-data
The --set-gtid-purged option has the following effect on binary logging when the dump file is reloaded:
--set-gtid-purged=OFF: SET @@SESSION.SQL_LOG_BIN=0; is not added to the output.
--set-gtid-purged=ON: SET @@SESSION.SQL_LOG_BIN=0; is added to the output.
--set-gtid-purged=AUTO: SET @@SESSION.SQL_LOG_BIN=0; is added to the output if GTIDs are enabled on the server you are backing up (that is, if AUTO evaluates to ON).
`
## 6 解决办法
`第1套：因为备份文件是不记录binlog的，所以可以在从库执行同样的source /opt/test01_set-gtid-purgedis_on.sql;
补齐数据
之后重启SQL线程：
stop slave SQL_THREAD;
start slave SQL_THREAD;
第2套：因为第一次导入的数据不会传输到从库，且已手动删除。所以只需要处理第二次导入的数据，是记录binlog的。报错信息是因为从库没有这个库。我们需要跳过SET @@SESSION.GTID_NEXT= '7b3a89d7-4866-11ec-b99b-0242ac148602:666084'
drop database test01  # 执行者是迁移人员，逃过这个事物。
# 确认从库执行的数据信息：
show master status\G
*************************** 1. row ***************************
File: mysql-bin.000002
Position: 27756998
Binlog_Do_DB:
Binlog_Ignore_DB:
Executed_Gtid_Set: 7b3a89d7-4866-11ec-b99b-0242ac148602:1-666083,
7b3adf4b-4866-11ec-b9e0-0242ac148604:1-3338
Retrieved_Gtid_Set: 7b3a89d7-4866-11ec-b99b-0242ac148602:657353-666084
Executed_Gtid_Set: 7b3a89d7-4866-11ec-b99b-0242ac148602:1-666083,
7b3adf4b-4866-11ec-b9e0-0242ac148604:1-3338
stop slave;
SET @@SESSION.GTID_NEXT= '7b3a89d7-4866-11ec-b99b-0242ac148602:666084';
BEGIN; COMMIT;# 将该gtid设为空事务
show variables like '%gtid_next%';
+---------------+-----------+
| Variable_name | Value     |
+---------------+-----------+
| gtid_next     | AUTOMATIC |
+---------------+-----------+
start slave;
`
## 7 使用建议
`# 导入Mysqldump备份时，我们需要评估导入方式。
1.source 还是 mysql客户端方式。
2.导入的主机是 主库 or 从库。
3.导入前后记录数据库的状态信息，方便问题排查。
`