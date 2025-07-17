# 技术分享 | ProxySQL 搭配 MySQL HA （下）

**原文链接**: https://opensource.actionsky.com/20210106-proxysql/
**分类**: 技术干货
**发布时间**: 2022-01-05T22:08:20-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
通过上一章节的介绍，我们已经了解ProxySQL 如何基于 MySQL 主从以及组复制架构来构建读写分离、故障转移等功能点，但没有涵盖ProxySQL 相关配置表的工作细节。那本章就对上节遗漏的内容进行一个延伸讲解。
##### 先来了解下 ProxySQL 的内置数据库列表：
`ytt:admin> show databases;
+-----+---------------+-------------------------------------+
| seq | name          | file                                |
+-----+---------------+-------------------------------------+
| 0   | main          |                                     |
| 2   | disk          | /var/lib/proxysql/proxysql.db       |
| 3   | stats         |                                     |
| 4   | monitor       |                                     |
| 5   | stats_history | /var/lib/proxysql/proxysql_stats.db |
+-----+---------------+-------------------------------------+
5 rows in set (0.00 sec)
`
以上所列数据库中，main 代表 runtime ，也即运行时库；disk 代表持久化库；stats 代表统计数据库；monitor 代表监控数据库；stats_history 代表统计数据库归档。
对于储存 MySQL 主从、组复制、读写分离的几张配置表，在每个库里都存在，不同的库代表不同的运行范畴。
##### 第一，后端主机元数据库表
**mysql_servers**：该表为存储后端数据库相关元数据信息的基础表，所有的后续操作都需要访问并且更新这张表。
其中主要几个字段如下：
hostgroup_id， 后端MySQL实例的主机组标志，每个实例可以设置为一样的数值或者设置为不相同的数值，推荐一组实例设置为相同。
gtid_port， Proxy Binlog Reader 组件需要监听的端口。 不使用此组件可以保持默认即可。
status ，实例状态值。
- 
online ，默认选项，在线提供服务，也即正常状态；
- 
offline_soft ，非强制下线状态，也即处理完当前会话后停止接受新请求；
- 
offline_hard ，强制下线，强制关闭目所有会话，并且不再接受新的请求；
- 
shunned ，后端实例由于太多错误连接而暂时关闭的状态或者说由于超过设定的延迟时间而暂停处理新请求。
weight，一个组里的实例优先级，优先级越高的越有几率被选中。比如多个从实例，可以提升一个节点的优先级来保证流量分配优先。
compression ，是否压缩连接请求。默认不压缩，可以设置为1表示压缩。
max_connections ，通过 ProxySQL 流量端口的最大连接数限制。
max_replication_lag，指定实例状态被设置为 shunned 的延迟时间。 超过这个时间后，指定实例状态由 online 变为 shunned ，直到积压的请求处理完成。
比如下面 runtime 级别的 mysql_servers 表记录： 由于这几个节点都没有运行，状态都为 shunned ：
`ytt:admin> select hostgroup_id,hostname,port,status,max_connections from runtime_mysql_servers where hostgroup_id in (1,2);
+--------------+-----------+------+---------+-----------------+
| hostgroup_id | hostname  | port | status  | max_connections |
+--------------+-----------+------+---------+-----------------+
| 2            | 127.0.0.1 | 3341 | SHUNNED | 1000            |
| 2            | 127.0.0.1 | 3342 | SHUNNED | 1000            |
| 2            | 127.0.0.1 | 3340 | SHUNNED | 1000            |
+--------------+-----------+------+---------+-----------------+
3 rows in set (0.00 sec)
`
我启动这三个主从节点，对应状态自动更新为 online ：
`ytt:admin> select hostgroup_id,hostname,port,status,max_connections from runtime_mysql_servers where hostgroup_id in (1,2);
+--------------+-----------+------+--------+-----------------+
| hostgroup_id | hostname  | port | status | max_connections |
+--------------+-----------+------+--------+-----------------+
| 2            | 127.0.0.1 | 3341 | ONLINE | 1000            |
| 1            | 127.0.0.1 | 3341 | ONLINE | 1000            |
| 2            | 127.0.0.1 | 3342 | ONLINE | 1000            |
| 2            | 127.0.0.1 | 3340 | ONLINE | 1000            |
+--------------+-----------+------+--------+-----------------+
4 rows in set (0.00 sec)
`
同样，启动组复制实例，三个节点的状态如下：
`ytt:admin> select hostgroup_id,hostname,port,status from runtime_mysql_servers where hostgroup_id > 2;
+--------------+-----------+------+--------+
| hostgroup_id | hostname  | port | status |
+--------------+-----------+------+--------+
| 3            | 127.0.0.1 | 3343 | ONLINE |
| 5            | 127.0.0.1 | 3343 | ONLINE |
| 5            | 127.0.0.1 | 3344 | ONLINE |
| 5            | 127.0.0.1 | 3345 | ONLINE |
+--------------+-----------+------+--------+
4 rows in set (0.00 sec)
`
##### 第二，用户元数据表
**mysql_users**: 此表存储流量用户的授权数据。 有几个主要字段：
transaction_persistent ，用来指定事务整体是否被分流。 设置为1则代表以事务为粒度分流到到默认主机组；为0则代表按照事务内部 SQL 为粒度来分流。 除了只读事务，其他事务都应该作为一个整体，保持原有事务逻辑。
default_hostgroup ，默认主机组，没有配置查询规则的 SQL 统一分流到默认主机组。
frontend ,前端用户，针对 ProxySQL 实例。
backend ,后端用户，针对 MySQL 实例。
这两个字段默认都为1，通常定义一个后端 MySQL 实例用户，会自动映射到前端 ProxySQL 实例。
比如下面主从流量用户：从 mysql_users 表自动映射到 runtime_mysql_users 表，一个用户同时为前后端。
`ytt:admin> select username,active,default_hostgroup,frontend,backend from mysql_users where username = 'dev_user';
+----------+--------+-------------------+----------+---------+
| username | active | default_hostgroup | frontend | backend |
+----------+--------+-------------------+----------+---------+
| dev_user | 1      | 1                 | 1        | 1       |
+----------+--------+-------------------+----------+---------+
1 row in set (0.00 sec)
ytt:admin> select username,active,default_hostgroup,frontend,backend from runtime_mysql_users where username = 'dev_user';
+----------+--------+-------------------+----------+---------+
| username | active | default_hostgroup | frontend | backend |
+----------+--------+-------------------+----------+---------+
| dev_user | 1      | 1                 | 0        | 1       |
| dev_user | 1      | 1                 | 1        | 0       |
+----------+--------+-------------------+----------+---------+
2 rows in set (0.00 sec)
`
##### 第三，主从元数据表
**mysql_replication_hostgroups**： 此表配置主从实例主机组信息。
ProxySQL 根据这张表的内容来分流前端请求，并且配合 mysql_servers 表来达成主从自动故障转移目标。
writer_hostgroup ，写主机组 ID 。 比如我们的例子里设置为1，表示主机组 ID 为1的处理写请求。
reader_hostgroup ，读主机组 ID 。 比如我们的例子里设置为2，表示主机组 ID 为2的处理读请求。
check_type ，检查 MySQL 只读变量的值。在 read_only , innodb_read_only , super_read_only 这几个变量里选。
比如需要检测 super_read_only ， 如果为1，代表读；为0，则为写。
`ytt:admin> select * from mysql_replication_hostgroups;
+------------------+------------------+-----------------+---------------------------------+
| writer_hostgroup | reader_hostgroup | check_type      | comment                         |
+------------------+------------------+-----------------+---------------------------------+
| 1                | 2                | super_read_only | MySQL Replication failover test |
+------------------+------------------+-----------------+---------------------------------+
1 row in set (0.00 sec)
`
##### 第四，组复制元数据表
**mysql_group_replication_hostgroups**： 此表配置组复制主机组信息，同样配合 mysql_servers 表来完成组复制节点无感知容错功能，类似表 mysql_replication_hostgroups 。
writer_hostgroup ，reader_hostgroup ，这两个分别代表写和读流量组。
offline_hostgroup ，下线主机组，状态不正常的节点被放入这个组。
max_writers ，backup_writer_hostgroup ， 这两个用于多写模式，如果写实例数量多过max_writers 设置，则被放入主机组 backup_writer_hostgroup 。
max_transactions_behind ， 类似主从延迟流量停用功能。设置一个节点落后的事务数量，达到这个数量后，节点状态被设置为 shunned ，被完全处理完后，再变更为正常状态。
目前组复制环境的配置表如下：
`ytt:admin> select writer_hostgroup,backup_writer_hostgroup,reader_hostgroup from mysql_group_replication_hostgroups;
+------------------+-------------------------+------------------+
| writer_hostgroup | backup_writer_hostgroup | reader_hostgroup |
+------------------+-------------------------+------------------+
| 3                | 4                       | 5                |
+------------------+-------------------------+------------------+
1 row in set (0.00 sec)
`
##### 第五，读写分离元数据表
**mysql_query_rules**： 用来配置读写分离模式，非常灵活，可以配置统一端口匹配正则表达式或者根据不同端口来分流。（正则表达式依据的标准由参数 mysql-query_processor_regex 设置决定）几个主要的字段如下：
active ，是否激活这个匹配模式。
username ，流量用户名。
schemaname ，数据库名。
match_pattern ，具体的匹配模式。
除了上一章节介绍的依赖正则表达式来分流读写流量到同一端口外，还可以设置多个端口来区分不同的实例组。比如主从流量走端口 6401 ，组复制流量走 6402 ，那么可以直接这样适配：
先把 ProxySQL 要监听的端口添加到变量 mysql-interfaces 里，完了重启 ProxySQL 服务：
`ytt:admin> SET mysql-interfaces='0.0.0.0:6033;0.0.0.0:6401;0.0.0.0:6402';
Query OK, 1 row affected (0.00 sec)
ytt:admin> SAVE MYSQL VARIABLES TO DISK;
Query OK, 140 rows affected (0.02 sec)
`
再把这两个端口插入到这张表：
`ytt:admin> INSERT INTO mysql_query_rules (rule_id,active,proxy_port,destination_hostgroup,apply)
-> VALUES (1,1,6401,1,1), (2,1,6402,3,1);
Query OK, 2 rows affected (0.00 sec)
ytt:admin> LOAD MYSQL QUERY RULES TO RUNTIME;
Query OK, 0 rows affected (0.00 sec)
ytt:admin> SAVE MYSQL QUERY RULES TO DISK; 
Query OK, 0 rows affected (0.08 sec)
`
这张表现在内容如下：除了按照正则分流外，额外有两条记录来按照指定端口（6401 为主从分流端口，6402 为组复制分流端口）分流。
`ytt:admin> select rule_id,active,username,schemaname,match_pattern,destination_hostgroup,proxy_port from runtime_mysql_query_rules;
+---------+--------+--------------+------------+---------------+-----------------------+------------+
| rule_id | active | username     | schemaname | match_pattern | destination_hostgroup | proxy_port |
+---------+--------+--------------+------------+---------------+-----------------------+------------+
| 1       | 1      | NULL         | NULL       | NULL          | 1                     | 6401       |
| 2       | 1      | NULL         | NULL       | NULL          | 3                     | 6402       |
| 13      | 1      | dev_user     | ytt        | ^select       | 2                     | NULL       |
| 14      | 1      | dev_user_mgr | ytt        | ^select       | 4                     | NULL       |
+---------+--------+--------------+------------+---------------+-----------------------+------------+
4 rows in set (0.00 sec)
`
来验证下这个分流策略:  分别使用用户 dev_user 连接端口 6401 ，用户 dev_user_mgr 连接端口 6402 。
`root@ytt-ubuntu:~# mysql -udev_user -pdev_user -P6401 -h ytt-ubuntu -e "use ytt;select count(*) from t1";
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| count(*) |
+----------+
|        5 |
+----------+
root@ytt-ubuntu:~# mysql -udev_user_mgr -pdev_user_mgr -P6402 -h ytt-ubuntu -e "use ytt;select count(*) from t1";
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| count(*) |
+----------+
|        1 |
+----------+
`
进入 ProxySQL 管理端， 查看审计表： 以上不同用户、不同端口分流到具体的主机组里。
`ytt:admin> select hostgroup,schemaname,username,digest_text,count_star from stats_mysql_query_digest where schemaname = 'ytt';
+-----------+------------+--------------+-------------------------+------------+
| hostgroup | schemaname | username     | digest_text             | count_star |
+-----------+------------+--------------+-------------------------+------------+
| 3         | ytt        | dev_user_mgr | select count(*) from t1 | 1          |
| 1         | ytt        | dev_user     | select count(*) from t1 | 1          |
+-----------+------------+--------------+-------------------------+------------+
2 rows in set (0.00 sec)
`
到这里，对于 ProxySQL 来讲，如何与 MySQL HA 进行搭配，相信已经有了一定的了解。