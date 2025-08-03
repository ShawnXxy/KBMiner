# 技术分享 | ProxySQL 搭配 MySQL HA （上）

**原文链接**: https://opensource.actionsky.com/20211223-proxysql/
**分类**: 技术干货
**发布时间**: 2021-12-22T22:41:15-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
ProxySQL 是一个使用非常广泛并且较稳定的中间件，有很多功能点。 比如查询缓存，查询重写，读写分离，数据分片等等。
本篇要介绍的是 ProxySQL 和 MySQL Replication 以及 MySQL MGR 的初步结合，初步读写分离以及 failover 功能的体验。
在本机安装一个 ProxySQL 实例，六个 MySQL 实例；ProxySQL 和 MySQL 版本均是最新版。
ProxySQL: 管理端口6032，流量端口6033。
MySQL Replication：流量端口分别为：3340、3341、3342
MySQL MGR： 流量端口分别为：3343、3344、3345
##### 第一，ProxySQL 以及六个 MySQL 部署。
ProxySQL 安装比较简单，官网 apt/yum ，或者自己下载安装。装好六个 MySQL 实例，并且配置好 MySQL 主从以及组复制环境。
##### 第二，ProxySQL 记录 MySQL 实例相关信息。
进入 ProxySQL 管理端，把以上六个 MySQL 实例信息依次插入到表 mysql_servers ：主从实例的 hostgroup_id 统一设置为1， 为了不破坏后续 failover 相关 hostgroup_id 的连续性，组复制实例的 hostgroup_id 统一设置为3。
`Admin> select hostgroup_id, hostname,port,status from mysql_servers;
+--------------+-----------+------+--------+
| hostgroup_id | hostname  | port | status |
+--------------+-----------+------+--------+
| 1            | 127.0.0.1 | 3340 | ONLINE |
| 1            | 127.0.0.1 | 3341 | ONLINE |
| 1            | 127.0.0.1 | 3342 | ONLINE |
| 3            | 127.0.0.1 | 3343 | ONLINE |
| 3            | 127.0.0.1 | 3344 | ONLINE |
| 3            | 127.0.0.1 | 3345 | ONLINE |
+--------------+-----------+------+--------+
6 rows in set (0.00 sec)
`
##### 第三，MySQL 端创建 ProxySQL 所需的两类用户
ProxySQL 对 MySQL 来讲，有需要两类用户，这两类用户需要同时在主从和组复制环境创建。
###### 1， 监控用户：为了免去后面重复设置监控用户变量的工作，两种架构用户名和密码保持一致，用户名和密码都是 proxysql_monitor 。proxysql_monitor 需要 以下权限：
###### client,session_variables_admin,system_variables_admin,select
在 MySQL 主从以及组复制环境里分别执行下面SQL：
` MySQL  localhost:3343 ssl  SQL > create user proxysql_monitor@'127.0.0.1' identified by 'proxysql_monitor';
Query OK, 0 rows affected (0.0596 sec)
MySQL  localhost:3343 ssl  SQL > grant replication client,session_variables_admin,system_variables_admin,select on *.* to proxysql_monitor@'127.0.0.1';
Query OK, 0 rows affected (0.0103 sec)
`
进入 ProxySQL 管理端，设置监控用户：
`Admin> set mysql-monitor_username='proxysql_monitor';
Query OK, 1 row affected (0.00 sec)
Admin> set mysql-monitor_password='proxysql_monitor';
Query OK, 1 row affected (0.00 sec)
`
###### 2， 开发用户：对于主从和组复制环境，分别创建此类用户。
主从环境用户创建：用户名 dev_user
` MySQL  localhost:3343 ssl  SQL > create user dev_user@'127.0.0.1' identified by 'dev_user';
Query OK, 0 rows affected (0.1221 sec)
MySQL  localhost:3343 ssl  SQL > grant insert,delete,update,select,create on ytt.* to dev_user@'127.0.0.1';
Query OK, 0 rows affected (0.0359 sec)
`
组复制环境用户创建：用户名 dev_user_mgr
` MySQL  localhost:3343 ssl  SQL > create user dev_user_mgr@'127.0.0.1' identified by 'dev_user_mgr';
Query OK, 0 rows affected (0.1221 sec)
MySQL  localhost:3343 ssl  SQL > grant insert,delete,update,select,create on ytt.* to dev_user_mgr@'127.0.0.1';
Query OK, 0 rows affected (0.0359 sec)
`
进入 ProxySQL 管理端，分别插入主从以及组复制对应的开发用户到表 mysql_users 。**字段 transaction_persistent 为1代表事务不拆分，统一去主库检索。**
`Admin> insert into mysql_users(username,password,active,default_hostgroup,transaction_persistent) 
values 
('dev_user','dev_user',1,1,1),
('dev_user_mgr','dev_user_mgr',1,3,1);
Query OK, 1 row affected (0.00 sec)
Admin> select username,active,default_hostgroup from mysql_users;
+--------------+--------+-------------------+
| username     | active | default_hostgroup |
+--------------+--------+-------------------+
| dev_user     | 1      | 1                 |
| dev_user_mgr | 1      | 3                 |
+--------------+--------+-------------------+
2 rows in set (0.00 sec)
`
##### 第四，配置读写分离
进入 ProxySQL 管理端，插入之前创建的两个开发用户到表 mysql_query_rules ，定义最基本的读写分离策略，只要是 select 开头的语句都分流到从库。
`Admin> INSERT INTO mysql_query_rules(username,schemaname,active,match_pattern,destination_hostgroup,apply) VALUES
('dev_user','ytt',1,'^select',2,1),
('dev_user_mgr','ytt',1,'^select',4,1);
Query OK, 2 rows affected (0.00 sec)
Admin> select username,schemaname,active,match_pattern,destination_hostgroup,apply from mysql_query_rules;
+--------------+------------+--------+---------------+-----------------------+-------+
| username     | schemaname | active | match_pattern | destination_hostgroup | apply |
+--------------+------------+--------+---------------+-----------------------+-------+
| dev_user     | ytt        | 1      | ^select       | 2                     | 1     |
| dev_user_mgr | ytt        | 1      | ^select       | 4                     | 1     |
+--------------+------------+--------+---------------+-----------------------+-------+
2 rows in set (0.00 sec)
`
设置好相关信息后把以上所有更改加载到内存，并且持久化到磁盘。
`Admin> load mysql servers to runtime;
Query OK, 0 rows affected (0.01 sec)
Admin> load mysql users to runtime;
Query OK, 0 rows affected (0.00 sec)
Admin> load mysql variables to runtime;
Query OK, 0 rows affected (0.00 sec)
Admin> load mysql query rules to runtime;
Query OK, 0 rows affected (0.00 sec)
Admin> save mysql servers to disk;
Query OK, 0 rows affected (0.18 sec)
Admin> save mysql users to disk;
Query OK, 0 rows affected (0.13 sec)
Admin> save mysql variables to disk;
Query OK, 140 rows affected (0.17 sec)
Admin> save mysql query rules to disk;
Query OK, 0 rows affected (0.11 sec)
`
分别测试下主从和组复制两种架构的读写分离效果：开发用户**dev_user/dev_user_mgr**连接端口6033，创建一张表t1，插入一条记录，并且简单查询一次。
`-- 主从环境：
root@ytt-ubuntu:/home/ytt/scripts# mysql -u dev_user -p -h 127.0.0.1 -P 6033 -e " \
> use ytt;
> create table t1 (id int primary key,str1 varchar(100));
> insert t1 values (1,'replication');
> select * from t1;
> ";
Enter password: 
-- 组复制环境把用户dev_user和密码替换为dev_user_mgr和对应密码重复执行一次。
`
进入 ProxySQL 管理端，检索审计表 stats_mysql_query_digest ：写入请求和读取请求根据不同的用户被成功分发到 mysql_query_rules 表里对应的 hostgroup 上。
`Admin> select hostgroup,username,digest_text,count_star from stats_mysql_query_digest where schemaname = 'ytt';
+-----------+--------------+------------------------------------------------------+------------+
| hostgroup | username     | digest_text                                          | count_star |
+-----------+--------------+------------------------------------------------------+------------+
| 4         | dev_user_mgr | select * from t1                                     | 1          |
| 3         | dev_user_mgr | insert t1 values (?,?)                               | 1          |
| 3         | dev_user_mgr | create table t1 (id int primary key,str1 varchar(?)) | 1          |
| 2         | dev_user     | select * from t1                                     | 1          |
| 1         | dev_user     | insert t1 values (?,?)                               | 1          |
| 1         | dev_user     | create table t1 (id int primary key,str1 varchar(?)) | 1          |
+-----------+--------------+------------------------------------------------------+------------+
6 rows in set (0.00 sec)
`
##### 第五，配置主从自动 failover 功能：
进入 RroxySQL 管理端，把主从相关实例信息插入到表 mysql_replication_hostgroups 即可。
ProxySQL 通过实时监控 MySQL 系统变量（&#8217;read_only&#8217;,&#8217;innodb_read_only&#8217;,&#8217;super_read_only&#8217; ）开关与否来探测对应的 MySQL 实例是主库还是从库，完了自动更新 mysql_server 表主库对应的IP和端口来达到 failover 的目的。
`Admin> insert into  mysql_replication_hostgroups (writer_hostgroup,reader_hostgroup,check_type,comment)values(1,2,'super_read_only','MySQL Replication fa
ailover test');
Query OK, 1 row affected (0.00 sec)
Admin> select * from mysql_replication_hostgroups;
+------------------+------------------+-----------------+---------------------------------+
| writer_hostgroup | reader_hostgroup | check_type      | comment                         |
+------------------+------------------+-----------------+---------------------------------+
| 1                | 2                | super_read_only | MySQL Replication failover test |
+------------------+------------------+-----------------+---------------------------------+
1 row in set (0.01 sec)
Admin> load mysql servers to runtime;
Query OK, 0 rows affected (0.01 sec)
Admin> save mysql servers to disk;
Query OK, 0 rows affected (0.18 sec)
`
我用 MySQL Shell  操作副本集来手动进行主从切换，设置主库为端口3342。
` MySQL  localhost:3340 ssl  Py > rs = dba.get_replica_set()
You are connected to a member of replicaset 'rs1'. 
MySQL  localhost:3340 ssl  Py > rs.set_primary_instance('root@localhost:3342')
127.0.0.1:3342 will be promoted to PRIMARY of 'rs1'.
The current PRIMARY is 127.0.0.1:3340.
...
127.0.0.1:3342 was promoted to PRIMARY.
`
查看 ProxySQL 日志，已经感知到主从切换，新的主库自动变为127.0.0.1:3342
`2021-12-15 16:02:08 [INFO] Regenerating read_only_set1 with 1 servers
2021-12-15 16:02:08 [INFO] read_only_action() detected RO=0 on server 127.0.0.1:3342 for the first time after commit(), but no need to reconfigure
`
也可以进入 ProxySQL 管理端来查询表 mysql_servers 的字段 hostgroup_id=1 的匹配记录是否已经变更为新主库：
`Admin> select hostname,port from mysql_servers where hostgroup_id = 1;
+-----------+------+
| hostname  | port |
+-----------+------+
| 127.0.0.1 | 3342 |
+-----------+------+
1 row in set (0.00 sec)
`
##### 第六，配置组复制自动 failover 功能：
和主从配置类似，把组复制实例相关信息插入到表 mysql_replication_hostgroups 即可。
这里和主从有点不一样的地方：writer_hostgroup,backup_writer_hostgroup, reader_hostgroup, offline_hostgroup 这四个字段代表不同职责的 Hostgroup ，最好是设置不一样。
`Admin> insert into mysql_group_replication_hostgroups (writer_hostgroup,backup_writer_hostgroup, reader_hostgroup, offline_hostgroup,active,max_writers,writer_is_also_reader,max_transactions_behind) values (3,4,5,6,1,1,1,1000);
Query OK, 1 row affected (0.00 sec)
Admin> load mysql servers to runtime;
Query OK, 0 rows affected (0.01 sec)
Admin> save mysql servers to disk;
Query OK, 0 rows affected (0.19 sec)
`
进入 ProxySQL 管理端，查询组复制日志表 mysql_server_group_replication_log ，可以看到当前的组复制对应的实例数据，其中主库为：127.0.0.1:3343。
`Admin> select hostname, port,viable_candidate,read_only, transactions_behind, error from mysql_server_group_replication_log where port in (3343,3344,3345) order by time_start_us desc limit 3;
+-----------+------+------------------+-----------+---------------------+-------+
| hostname  | port | viable_candidate | read_only | transactions_behind | error |
+-----------+------+------------------+-----------+---------------------+-------+
| 127.0.0.1 | 3345 | YES              | YES       | 0                   | NULL  |
| 127.0.0.1 | 3344 | YES              | YES       | 0                   | NULL  |
| 127.0.0.1 | 3343 | YES              | NO        | 0                   | NULL  |
+-----------+------+------------------+-----------+---------------------+-------+
3 rows in set (0.00 sec)
`
同样用 MySQL Shell 来验证下组复制的主备角色切换后 ProxySQL 是否会自动感知： 把实例 127.0.0.1：3344 提升为主库。
`MySQL  localhost:3343 ssl  sys  Py > rc = dba.get_cluster();
MySQL  localhost:3343 ssl  sys  Py > rc.set_primary_instance('root@localhost:3344');
Setting instance 'localhost:3344' as the primary instance of cluster 'ytt_mgr'...
Instance '127.0.0.1:3343' was switched from PRIMARY to SECONDARY.
Instance '127.0.0.1:3344' was switched from SECONDARY to PRIMARY.
Instance '127.0.0.1:3345' remains SECONDARY.
WARNING: The cluster internal session is not the primary member anymore. For cluster management operations please obtain a fresh cluster handle using dba.get_cluster().
The instance 'localhost:3344' was successfully elected as primary.
MySQL  localhost:3343 ssl  sys  Py > 
`
进入 ProxySQL 管理端，查询组复制日志：127.0.0.1：3344 自动变更为主库。
`Admin> select hostname, port,viable_candidate,read_only, transactions_behind, error from mysql_server_group_replication_log where port in (3343,3344,3345) order by time_start_us desc limit 3;
+-----------+------+------------------+-----------+---------------------+-------+
| hostname  | port | viable_candidate | read_only | transactions_behind | error |
+-----------+------+------------------+-----------+---------------------+-------+
| 127.0.0.1 | 3345 | YES              | YES       | 0                   | NULL  |
| 127.0.0.1 | 3344 | YES              | NO        | 0                   | NULL  |
| 127.0.0.1 | 3343 | YES              | YES       | 0                   | NULL  |
+-----------+------+------------------+-----------+---------------------+-------+
3 rows in set (0.00 sec)
`
或者查询mysql_server表，查找hostgroup_id 为3的记录是否变更为新主库。
`Admin> select port from mysql_servers where hostgroup_id = 3;
+------+
| port |
+------+
| 3344 |
+------+
1 row in set (0.00 sec)
`
#### 总结
本篇简单介绍 ProxySQL 配置 MySQL HA 的相关配置与验证测试，更详细的配置与验证策略请关注后续。