# 技术分享 | 聊聊 MySQL 关机的故事

**原文链接**: https://opensource.actionsky.com/20220328-mysql2/
**分类**: MySQL 新特性
**发布时间**: 2022-03-27T23:31:28-08:00

---

作者：莫善
某互联网公司高级 DBA。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
- 背景
- 一、环境介绍
- 二、测试演示
- 三、停服流程介绍
- 四、写在最后
### 背景
这两天看到一个 MySQL 群里在讨论一个有趣的话题，大家平时都是怎么关闭 MySQL 的，一个大佬还发起了一个投票。投票如下：
你是如何关闭 MySQL 数据库的？
- 
A、mysqladmin shutdown
- 
B、service mysqld stop（systemctl）
- 
C、kill mysqld_pid
- 
D、kill -9 mysqld_pid
投票结果如下：
| 选项 | 人数 | 占比 |
| --- | --- | --- |
| A | 141 | 33.9% |
| B | 243 | 58.4% |
| C | 15 | 3.6% |
| D | 17 | 4.1% |
生产环境中基本都是多实例部署，所以用A的方式关闭比较多，偶尔也会贪方便直接采用C的关闭方式，如果是单机单实例，用B也没毛病，但是为什么会有人选D选项呢，发起投票的大佬逐一问过后得知，都是因为当时 MySQL 已经不可用了，迫不得已才采用暴力关闭。
最后，大佬最终公布答案说，生产环境有且只有一种正确的关闭 MySQL 的方式，那就是D方式，所以在大佬看来，几乎团灭。
对这个公布结果我是持怀疑态度的，所以我带着怀疑做了下面的测试。
> 
仅对5.7的半同步场景做了测试，对于异步场景感觉没什么意义，所以没测。
### 一、环境介绍
环境架构采用 MySQL 5.7 增强半同步，搭建的一主一从，信息如下：
| 角色 | ip | 端口 | 版本 |
| --- | --- | --- | --- |
| master | 192.168.168.11 | 6666 | 5.7.26 |
| slave | 192.168.168.12 | 6666 | 5.7.26 |
#### 1、主库配置
`mysql> show variables like 'rpl%';
+-------------------------------------------+------------+
| Variable_name                             | Value      |
+-------------------------------------------+------------+
| rpl_semi_sync_master_enabled              | ON         |
| rpl_semi_sync_master_timeout              | 1000000    |
| rpl_semi_sync_master_trace_level          | 32         |
| rpl_semi_sync_master_wait_for_slave_count | 1          |
| rpl_semi_sync_master_wait_no_slave        | ON         |
| rpl_semi_sync_master_wait_point           | AFTER_SYNC |
| rpl_semi_sync_slave_enabled               | OFF        |
| rpl_semi_sync_slave_trace_level           | 32         |
| rpl_stop_slave_timeout                    | 31536000   |
+-------------------------------------------+------------+
9 rows in set (0.00 sec)
mysql> 
`
> 
rpl_semi_sync_master_timeout = 1000000 是为了避免半同步降级为异步。
#### 2、从库配置
`mysql> show variables like 'rpl%';
+-------------------------------------------+------------+
| Variable_name                             | Value      |
+-------------------------------------------+------------+
| rpl_semi_sync_master_enabled              | OFF        |
| rpl_semi_sync_master_timeout              | 1000000    |
| rpl_semi_sync_master_trace_level          | 32         |
| rpl_semi_sync_master_wait_for_slave_count | 1          |
| rpl_semi_sync_master_wait_no_slave        | ON         |
| rpl_semi_sync_master_wait_point           | AFTER_SYNC |
| rpl_semi_sync_slave_enabled               | ON         |
| rpl_semi_sync_slave_trace_level           | 32         |
| rpl_stop_slave_timeout                    | 31536000   |
+-------------------------------------------+------------+
9 rows in set (0.00 sec)
mysql> 
`
### 二、测试演示
- 
测试准备
登录主库准备测试数据
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.11 -P6666 -p123456
mysql> create database if not exists dbatest;
Query OK, 1 row affected, 1 warning (0.00 sec)
mysql> use dbatest
Database changed
mysql> create table t(id int not null auto_increment primary key,name varchar(10) default '') ;
Query OK, 0 rows affected (0.01 sec)
mysql> insert into t select 0,'mysql';
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0
mysql> insert into t select 0,'redis';
Query OK, 1 row affected (0.01 sec)
Records: 1  Duplicates: 0  Warnings: 0
mysql> select * from t;
+----+-------+
| id | name  |
+----+-------+
|  1 | mysql |
|  2 | redis |
+----+-------+
2 rows in set (0.00 sec)
mysql> 
`
登录从库检查测试数据
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.12 -P6666 -p123456
mysql> use dbatest
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> select * from t;
+----+-------+
| id | name  |
+----+-------+
|  1 | mysql |
|  2 | redis |
+----+-------+
2 rows in set (0.00 sec)
mysql> 
`
#### 1、安全关闭的场景
（1）停掉从库的复制
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.12 -P6666 -p123456
mysql> stop slave;
Query OK, 0 rows affected (0.01 sec)
mysql> 
`
> 
模拟半同步故障，为了更直观查阅测试结果。
（2）模拟业务更新
这个流程涉及两个操作，一是在主库发起一个更新请求，二是查看主库的processlist状态。
- 
操作一
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.11 -P6666 -p123456 dbatest -e "update t set name = 'tidb' where id = 1"
`
> 
这个操作回车后会卡着，因为这个请求会等从库的ACK。具体可以看【操作二】的查询结果。
- 
操作二
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.11 -P6666 -p123456
mysql> show processlist;
+----+------+----------------------+---------+---------+------+--------------------------------------+-----------------------------------------+
| Id | User | Host                 | db      | Command | Time | State                                | Info                                    |
+----+------+----------------------+---------+---------+------+--------------------------------------+-----------------------------------------+
|  8 | dba  | 192.168.168.13:49584 | dbatest | Query   |   49 | Waiting for semi-sync ACK from slave | update t set name = 'tidb' where id = 1 |
|  9 | root | localhost            | NULL    | Query   |    0 | starting                             | show processlist                        |
+----+------+----------------------+---------+---------+------+--------------------------------------+-----------------------------------------+
2 rows in set (0.00 sec)
mysql> 
`
（3）关闭主库的 MySQL
这个流程向主库提交 shutdown 命令来安全关闭 MySQL 。
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.11 -P6666 -p123456
mysql> shutdown;
Query OK, 0 rows affected (0.00 sec)
mysql> 
`
提交完 shutdown 操作后，【操作一】的更新请求会被提交。
> 
- 
在业务端看来，id=1 这行数据已经被修改，但是从库的id=1这行数据未改变。如果这个时候触发主从切换，那就丢数据了。由此看来，在特殊场景下，安全关闭MySQL可能导致数据丢失。
- 
这时候将主库重新拉起来，修好主从的半同步，被提交的事务还是会同步到从库的。
#### 2、暴力关闭的场景
（1）停掉从库的复制
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.12 -P6666 -p123456
mysql> stop slave;
Query OK, 0 rows affected (0.01 sec)
mysql> 
`
> 
模拟半同步故障，为了更直观查阅测试结果。
（2）模拟业务更新
这个流程涉及两个操作，一是在主库发起一个更新请求，二是查看主库的 processlist 状态。
- 
操作一
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.11 -P6666 -p123456 dbatest -e "update t set name = 'codis' where id = 2"
`
> 
这个操作回车后会卡着，因为这个请求会等从库的ACK。具体可以看【操作二】的查询结果。
- 
操作二
`# /opt/soft/mysql57/bin/mysql -u dba -h 192.168.168.11 -P6666 -p123456
mysql> show processlist;
+----+------+----------------------+---------+---------+------+--------------------------------------+-----------------------------------------+
| Id | User | Host                 | db      | Command | Time | State                                | Info                                    |
+----+------+----------------------+---------+---------+------+--------------------------------------+-----------------------------------------+
|  2 | dba  | 192.168.168.13:34698 | dbatest | Query   |   13 | Waiting for semi-sync ACK from slave | update t set name = 'codis' where id = 2 |
|  3 | root | localhost            | NULL    | Query   |    0 | starting                             | show processlist                        |
+----+------+----------------------+---------+---------+------+--------------------------------------+-----------------------------------------+
2 rows in set (0.00 sec)
mysql> 
`
（3）暴力关闭主库的 MySQL
这个操作向主库所在服务器的 MySQL 进程发送 kill -9 信号，来暴力关闭 MySQL 。
`# ps -ef|grep mysql|grep 6666
root     123194      1  0 15:45 pts/9    00:00:00 /bin/sh /opt/soft/mysql57/bin/mysqld_safe --defaults-file=//work/mysql6666/etc/my6666.cnf
mysql    124539 123194  4 15:45 pts/9    00:00:02 /opt/soft/mysql57/bin/mysqld --defaults-file=//work/mysql6666/etc/my6666.cnf --basedir=/opt/soft/mysql57 --datadir=/work/mysql6666/var --plugin-dir=/opt/soft/mysql57/lib/plugin --user=mysql --log-error=/work/mysql6666/log/mysql.err --open-files-limit=65535 --pid-file=/work/mysql6666/var/mysql.pid --socket=/work/mysql6666/tmp/mysql.sock --port=6666
# kill -9 124539 123194
# 
`
kill -9 操作后，【操作一】所在的会话会被终止，并提示【ERROR 2013 (HY000) at line 1: Lost connection to MySQL server during query】
> 
- 
在业务端看来，id=2这行数据没有被修改，所以数据是一致的。
### 三、停服流程介绍
本小节是通过阅读了 MySQL 官方文档后，简单介绍一下 MySQL 在接收了 SIGINT 信号后会做哪些事情，仅供参考。
> 
该部分文档连接 https://dev.mysql.com/doc/refman/5.7/en/server-shutdown.html
#### 1、停止接受新连接
为了预防在关闭系统过程再接收新任务，MySQL 会关闭 TCP/IP 端口、socket 等通道来阻止接受新的客户端连接。
#### 2、处理已经建立的连接
这个过程会处理已经建立的连接， 对于空闲连接会马上杀掉。对于当前正在处理任务的线程（会定期检查它们的状态），如果是正在执行的未完成的事务，会回滚（非事务的引擎会导致部分失败部分成功），所以这个过程需要更长的时间。
> 
针对这个我有一个疑问。在【安全关闭的测试场景】中，正在等待ACK的任务会被提交，那么跟这个流程就有出入，所以我猜测这个流程之前会先关闭【等待ACK的线程】，然后再处理已经建立的连接，这样就能说的通，在【安全关闭的测试场景】中正在等待ACK的事务被提交了。当然这个思路仅是通过 MySQL 错误日志（如下展示）记录得出的猜测，仅供参考。
`2022-03-25T17:17:58.165016+08:00 0 [Note] Giving 1 client threads a chance to die gracefully
2022-03-25T17:17:58.165059+08:00 0 [Note] Shutting down slave threads
2022-03-25T17:17:58.165070+08:00 3 [Warning] SEMISYNC: Forced shutdown. Some updates might not be replicated.
2022-03-25T17:17:58.165092+08:00 3 [Note] Semi-sync replication switched OFF.
2022-03-25T17:17:58.165654+08:00 0 [Note] Forcefully disconnecting 0 remaining clients
2022-03-25T17:17:58.165680+08:00 0 [Note] Event Scheduler: Purging the queue. 0 events
2022-03-25T17:17:58.165919+08:00 0 [Note] Binlog end
2022-03-25T17:17:58.167688+08:00 0 [Note] Shutting down plugin 'rpl_semi_sync_slave'
2022-03-25T17:17:58.167719+08:00 0 [Note] Shutting down plugin 'rpl_semi_sync_master'
2022-03-25T17:17:58.167745+08:00 0 [Note] Stopping ack receiver thread
2022-03-25T17:17:58.167831+08:00 0 [Note] unregister_replicator OK
2022-03-25T17:17:58.167843+08:00 0 [Note] Shutting down plugin 'ngram'
省略shutting down plugin
2022-03-25T17:17:58.167985+08:00 0 [Note] Shutting down plugin 'InnoDB'
2022-03-25T17:17:58.168053+08:00 0 [Note] InnoDB: FTS optimize thread exiting.
2022-03-25T17:17:58.168140+08:00 0 [Note] InnoDB: Starting shutdown...
2022-03-25T17:18:00.704250+08:00 0 [Note] InnoDB: Shutdown completed; log sequence number 63089498676
2022-03-25T17:18:00.705160+08:00 0 [Note] InnoDB: Removed temporary tablespace data file: "ibtmp1"
2022-03-25T17:18:00.705183+08:00 0 [Note] Shutting down plugin 'MEMORY'
省略shutting down plugin
2022-03-25T17:18:00.705547+08:00 0 [Note] Shutting down plugin 'binlog'
2022-03-25T17:18:00.706904+08:00 0 [Note] /opt/soft/mysql57/bin/mysqld: Shutdown complete
`
> 
可以看到 shutdown 的整个过程，其中有一个【Stopping ack receiver thread】
#### 3、关闭存储引擎
在这个阶段，服务器会刷新表缓存并关闭所有打开的表。
InnoDB 将其缓冲池刷新到磁盘（除非 innodb_fast_shutdown = 2），将当前 LSN 写入表空间，并终止其自己的内部线程。
#### 4、服务器关闭
进程退出，端口关闭。
### 四、写在最后
测试结果有点惊讶，曾经认为危险的操作命令却是安全的，曾经认为安全的操作命令反而会导致数据异常。即便如此，我觉得也不用太过纠结了，毕竟丢数据的场景还是很苛刻的。
最后需要提醒一下，在5.7版本以前，要慎用 kill -9 。生产环境十分复杂，请时刻保持敬畏之心，任何操作请充分测试。