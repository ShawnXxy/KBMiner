# 技术分享 | innodb-cluster 扫盲-安装篇

**原文链接**: https://opensource.actionsky.com/20190820-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-08-20T00:20:47-08:00

---

本文介绍用 MySQL Shell 搭建 MGR 的详细过程。
**1、使用前，关掉防火墙，包括 selinux，firewalld，或者 MySQL 企业版的firewall（如果用了企业版的话）**
**2、两台机器：（4 台 MySQL 实例）**- `192.168.2.219 centos-ytt57-1 3311/3312`
- `192.168.2.229 centos-ytt57-2 3311/3312`
**3、安装 MySQL（两台都装）, MySQL Shell（任意一台）, mysqlrouter(任意一台，官方建议和应用程序装在一个服务器上)**- `yum install mysql-community-server mysql-shell mysql-router-community`
**4、搭建 InnoDB-Cluster（两台都装）**
1. 配置文件如下：- `shell>vi /etc/my.cnf`
- `master-info-repository=table`
- `relay-log-info-repository=table`
- `gtid_mode=ON`
- `enforce_gtid_consistency=ON`
- `binlog_checksum=NONE`
- `log_slave_updates=ON`
- `binlog_format=ROW`
- `transaction_write_set_extraction=XXHASH64`
2. 系统 HOSTS 配置（两台都配）
- `shell>vi /etc/hosts`
- 
- `127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4`
- `::1         localhost localhost.localdomain localhost6 localhost6.localdomain6`
- `192.168.2.219 centos-ytt57-2`
- `192.168.2.229 centos-ytt57-3`
用 MySQL coalesce 函数确认下 report-host 是否设置正确- `(root@localhost) : [(none)] >SELECT coalesce(@@report_host, @@hostname) as r;`
- `+----------------+`
- `| r              |`
- `+----------------+`
- `| centos-ytt57-1 |`
- `+----------------+`
- `1 row in set (0.00 sec)`
3. 创建管理员用户搭建 GROUP REPLICATION （四个节点都要）- `create user root identified by 'Root@123';`
- `grant all on *.* to root with grant option;`
- `flush privileges;`
4. MySQLsh 连接其中一台节点：- `[root@centos-ytt57-1 mysql]# mysqlsh root@localhost:3321`
5. 检查配置正确性：（如果这里不显示 OK，把对应的参数加到配置文件重启 MySQL 再次检查）
dba.checkInstanceConfiguration(&#8220;root@centos-ytt57-2:3311&#8221;);
dba.checkInstanceConfiguration(&#8220;root@centos-ytt57-2:3312&#8221;);
dba.checkInstanceConfiguration(&#8220;root@centos-ytt57-3:3311&#8221;);
dba.checkInstanceConfiguration(&#8220;root@centos-ytt57-3:3312&#8221;);
mysqlsh 执行检测- `[root@centos-ytt57-1 mysql]# mysqlsh --log-level=8 root@localhost:3311`
- 
- `MySQL  localhost:3311 ssl  JS > dba.checkInstanceConfiguration("root@centos-ytt57-2:3311")`
- `{`
- `  "status": "ok"`
- `}`
6. 创建集群，节点 1 上创建。（结果显示 Cluster successfully created 表示成功）- `MySQL  localhost:3311 ssl  JS > var cluster = dba.createCluster('ytt_mgr');`
- 
- `Cluster successfully created. Use Cluster.addInstance() to add MySQL instances.`
- `At least 3 instances are needed for the cluster to be able to withstand up to`
- `one server failure.`
7. 添加节点 2，3，4（全部显示 OK，表示添加成功）
- `MySQL  localhost:3311 ssl  JS >  cluster.addInstance('root@centos-ytt57-2:3312');`
- `MySQL  localhost:3311 ssl  JS >  cluster.addInstance('root@centos-ytt57-3:3311');`
- `MySQL  localhost:3311 ssl  JS >  cluster.addInstance('root@centos-ytt57-3:3312');`
8. 查看拓扑图：（describe 简单信息，status 详细描述）
- `MySQL  localhost:3311 ssl  JS > cluster.describe()`
- `{`
- `"clusterName": "ytt_mgr",`
- `"defaultReplicaSet": {`
- `  "name": "default",`
- `  "topology": [`
- `      {`
- `          "address": "centos-ytt57-2:3311",`
- `          "label": "centos-ytt57-2:3311",`
- `          "role": "HA",`
- `          "version": "8.0.17"`
- `      },`
- `      {`
- `          "address": "centos-ytt57-2:3312",`
- `          "label": "centos-ytt57-2:3312",`
- `          "role": "HA",`
- `          "version": "8.0.17"`
- `      },`
- `      {`
- `          "address": "centos-ytt57-3:3311",`
- `          "label": "centos-ytt57-3:3311",`
- `          "role": "HA",`
- `          "version": "8.0.17"`
- `      },`
- `      {`
- `          "address": "centos-ytt57-3:3312",`
- `          "label": "centos-ytt57-3:3312",`
- `          "role": "HA",`
- `          "version": "8.0.17"`
- `      }`
- `  ],`
- `  "topologyMode": "Single-Primary"`
- `}`
- `}`
- 
- `MySQL  localhost:3311 ssl  JS > cluster.status()`
- 
- `"clusterName": "ytt_mgr",`
- `"defaultReplicaSet": {`
- `  "name": "default",`
- `  "primary": "centos-ytt57-2:3311",`
- `  "ssl": "REQUIRED",`
- `  "status": "OK",`
- `  "statusText": "Cluster is ONLINE and can tolerate up to ONE failure.",`
- `  "topology": {`
- `      "centos-ytt57-2:3311": {`
- `          "address": "centos-ytt57-2:3311",`
- `          "mode": "R/W",`
- `          "readReplicas": {},`
- `          "role": "HA",`
- `          "status": "ONLINE",`
- `          "version": "8.0.17"`
- `      },`
- `      "centos-ytt57-2:3312": {`
- `          "address": "centos-ytt57-2:3312",`
- `          "mode": "R/O",`
- `          "readReplicas": {},`
- `          "role": "HA",`
- `          "status": "ONLINE",`
- `          "version": "8.0.17"`
- `      },`
- `      "centos-ytt57-3:3311": {`
- `          "address": "centos-ytt57-3:3311",`
- `          "mode": "R/O",`
- `          "readReplicas": {},`
- `          "role": "HA",`
- `          "status": "ONLINE",`
- `          "version": "8.0.17"`
- `      },`
- `      "centos-ytt57-3:3312": {`
- `          "address": "centos-ytt57-3:3312",`
- `          "mode": "R/O",`
- `          "readReplicas": {},`
- `          "role": "HA",`
- `          "status": "ONLINE",`
- `          "version": "8.0.17"`
- `      }`
- `  },`
- `  "topologyMode": "Single-Primary"`
- `},`
- `"groupInformationSourceMember": "centos-ytt57-2:3311"`
9. 简单测试下数据是否同步- `(root@localhost) : [(none)] >create database ytt;`
- `Query OK, 1 row affected (0.03 sec)`
- 
- `(root@localhost) : [(none)] >use ytt;`
- `Database changed`
- `(root@localhost) : [ytt] >create table p1(id int primary key, log_time datetime);`
- `Query OK, 0 rows affected (0.08 sec)`
- 
- `(root@localhost) : [ytt] >insert into p1 values (1,now());`
- `Query OK, 1 row affected (0.04 sec)`
- 
- `(root@localhost) : [ytt] >show master status;`
- `+---------------+----------+--------------+------------------+-------------------------------------------+`
- `| File          | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                         |`
- `+---------------+----------+--------------+------------------+-------------------------------------------+`
- `| mysql0.000001 |    25496 |              |                  | 6c7bb9db-b759-11e9-a9c0-0800276cf0fc:1-41 |`
- `+---------------+----------+--------------+------------------+-------------------------------------------+`
- `1 row in set (0.00 sec)`
查看其他三个节点- `(root@localhost) : [ytt] >show tables;`
- `+---------------+`
- `| Tables_in_ytt |`
- `+---------------+`
- `| p1            |`
- `+---------------+`
- `1 row in set (0.00 sec)`
- 
- `(root@localhost) : [ytt] >select * from p1;`
- `+----+---------------------+`
- `| id | log_time            |`
- `+----+---------------------+`
- `|  1 | 2019-08-05 16:44:20 |`
- `+----+---------------------+`
- `1 row in set (0.00 sec)`
停掉主节点：- `[root@centos-ytt57-2 mysql0]# systemctl stop mysqld@0`
现在查看，主节点已经变为本机 3312节点- `"centos-ytt57-2:3312": {`
- `   "address": "centos-ytt57-2:3312",`
- `   "mode": "R/W",`
- `   "readReplicas": {},`
- `   "role": "HA",`
- `   "status": "ONLINE"`
- `}`
10. 报错处理
错误日志里显示- `2019-08-05T09:01:35.125591Z 0 [ERROR] Plugin group_replication reported: 'The group name option is mandatory'`
- `2019-08-05T09:01:35.125622Z 0 [ERROR] Plugin group_replication reported: 'Unable to start Group Replication on boot'`
同时用 cluster.rescan() 扫描，发现- `The instance 'centos-ytt57-2:3311' is no longer part of the ReplicaSet.`
重新加入此节点到集群：- `cluster.rejoinInstance('centos-ytt57-2:3311')`
再次执行cluster.status()查看集群状态：&#8221;status&#8221;: &#8220;OK&#8221;,
11. 移除和加入- `cluster.removeInstance("centos-ytt57-3:3312");`
- `The instance 'centos-ytt57-3:3312' was successfully removed from the cluster.`
- `cluster.addInstance("centos-ytt57-3:3312");`
- `The instance 'centos-ytt57-3:3312' was successfully added to the cluster.`
12. 用 mysqlrouter 生成连接 MGR 相关信息。涉及到两个用户：&#8211;user=mysqlrouter 是使用mysqlrouter的系统用户自动创建的MySQL 用户是用来与MGR通信的用户。如果想查看这个用户的用户名以及密码，就加上&#8211;force-password-validation，不过一般也没有必要查看。- `[root@centos-ytt57-2 ytt]# mysqlrouter --bootstrap root@centos-ytt57-2:3311 --user=mysqlrouter --force-password-validation --report-host centos-ytt57-2`
- `Please enter MySQL password for root:`
- 
- `# Reconfiguring system MySQL Router instance...`
- 
- `- Checking for old Router accounts`
- `- Found old Router accounts, removing`
- `- Creating mysql account mysql_router1_rdr89tx20r0a@'%' for cluster management`
- `- Storing account in keyring`
- `- Adjusting permissions of generated files`
- ` - Creating configuration /etc/mysqlrouter/mysqlrouter.conf`
- 
- `# MySQL Router configured for the InnoDB cluster 'ytt_mgr'`
- 
- `After this MySQL Router has been started with the generated configuration`
- 
- `   $ /etc/init.d/mysqlrouter restart`
- `or`
- `   $ systemctl start mysqlrouter`
- `or`
- `   $ mysqlrouter -c /etc/mysqlrouter/mysqlrouter.conf`
- 
- `the cluster 'ytt_mgr' can be reached by connecting to:`
- 
- `## MySQL Classic protocol`
- 
- `- Read/Write Connections: centos-ytt57-2:6446`
- `- Read/Only Connections:  centos-ytt57-2:6447`
- 
- `## MySQL X protocol`
- 
- `- Read/Write Connections: centos-ytt57-2:64460`
- `- Read/Only Connections:  centos-ytt57-2:64470`
13. 启动 mysqlrouter，生效对应服务。
- `[root@centos-ytt57-2 mysqlrouter]# systemctl start mysqlrouter`
14. 使用 ROUTER 连接 MySQL创建一个普通用户使用 ROUTER (四个节点都建立，具体权限看个人)
- `[root@centos-ytt57-2 mysqlrouter]# /home/ytt/enter_mysql 80`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `Welcome to the MySQL monitor.  Commands end with ; or \g.`
- `Your MySQL connection id is 1779`
- `Server version: 8.0.17 MySQL Community Server - GPL`
- 
- `Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.`
- 
- `Oracle is a registered trademark of Oracle Corporation and/or its`
- `affiliates. Other names may be trademarks of their respective`
- `owners.`
- 
- `Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.`
- 
- `(root@centos-ytt57-2) : [(none)] >create user ytt_mysqlrouter;`
- `Query OK, 0 rows affected (0.12 sec)`
- 
- `(root@centos-ytt57-2) : [(none)] >alter user ytt_mysqlrouter identified by 'mysql_router';`
- `Query OK, 0 rows affected (0.09 sec)`
- 
- `(root@centos-ytt57-2) : [(none)] >grant all on ytt.* to ytt_mysqlrouter;`
- `Query OK, 0 rows affected (0.05 sec)`
- 
- `(root@centos-ytt57-2) : [(none)] >flush privileges;`
- `Query OK, 0 rows affected (0.07 sec)`
14.1 写入端口连接：- `[root@centos-ytt57-2 mysqlrouter]# mysql -uytt_mysqlrouter -pmysql_router -hcentos-ytt57-2 -P6446`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `Welcome to the MySQL monitor.  Commands end with ; or \g.`
- `Your MySQL connection id is 2030`
- `Server version: 8.0.17 MySQL Community Server - GPL`
- 
- `Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.`
- 
- `Oracle is a registered trademark of Oracle Corporation and/or its`
- `affiliates. Other names may be trademarks of their respective`
- `owners.`
- 
- `Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.`
- 
- `(ytt_mysqlrouter@centos-ytt57-2) : [(none)] >use ytt`
- `Reading table information for completion of table and column names`
- `You can turn off this feature to get a quicker startup with -A`
- 
- `Database changed`
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >insert into p1 values (200,now());`
- `Query OK, 1 row affected (0.04 sec)`
- 
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >select * from p1;`
- `+-----+---------------------+`
- `| id  | log_time            |`
- `+-----+---------------------+`
- `|   1 | 2019-08-05 23:15:38 |`
- `|   2 | 2019-08-05 23:15:42 |`
- `| 100 | 2019-08-05 23:52:58 |`
- `| 200 | 2019-08-05 23:56:23 |`
- `+-----+---------------------+`
- `4 rows in set (0.00 sec)`
- 
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >\q`
- `Bye`
- `[root@centos-ytt57-2 mysqlrouter]#`
14.2 读取端口连接：（默认循环选择读服务节点）- `[root@centos-ytt57-2 mysqlrouter]# mysql -uytt_mysqlrouter -pmysql_router -hcentos-ytt57-2 -P6447`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `Welcome to the MySQL monitor.  Commands end with ; or \g.`
- `Your MySQL connection id is 472`
- `Server version: 8.0.17 MySQL Community Server - GPL`
- 
- `Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.`
- 
- `Oracle is a registered trademark of Oracle Corporation and/or its`
- `affiliates. Other names may be trademarks of their respective`
- `owners.`
- 
- `Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.`
- 
- `(ytt_mysqlrouter@centos-ytt57-2) : [(none)] >use ytt`
- `Reading table information for completion of table and column names`
- `You can turn off this feature to get a quicker startup with -A`
- 
- `Database changed`
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >insert into p1 values (300,now());`
- `ERROR 1290 (HY000): The MySQL server is running with the --read-only option so it cannot execute this statement`
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >select * from p1;`
- `+-----+---------------------+`
- `| id  | log_time            |`
- `+-----+---------------------+`
- `|   1 | 2019-08-05 23:15:38 |`
- `|   2 | 2019-08-05 23:15:42 |`
- `| 100 | 2019-08-05 23:52:58 |`
- `| 200 | 2019-08-05 23:56:23 |`
- `+-----+---------------------+`
- `4 rows in set (0.00 sec)`
- 
- `## (ytt_mysqlrouter@centos-ytt57-2) : [ytt] >\s`
- 
- `mysql  Ver 8.0.17 for Linux on x86_64 (MySQL Community Server - GPL)`
- 
- `Connection id:          472`
- `Current database:       ytt`
- `Current user:           ytt_mysqlrouter@centos-ytt57-2`
- `SSL:                    Cipher in use is DHE-RSA-AES128-GCM-SHA256`
- `Current pager:          stdout`
- `Using outfile:          ''`
- `Using delimiter:        ;`
- `Server version:         8.0.17 MySQL Community Server - GPL`
- `Protocol version:       10`
- `Connection:             centos-ytt57-2 via TCP/IP`
- `Server characterset:    utf8mb4`
- `Db     characterset:    utf8mb4`
- `Client characterset:    utf8mb4`
- `Conn.  characterset:    utf8mb4`
- `TCP port:               6447`
- `Uptime:                 45 min 10 sec`
- 
- `## Threads: 5  Questions: 188  Slow queries: 0  Opens: 257  Flush tables: 3  Open tables: 161  Queries per second avg: 0.069`
- 
- 
- 
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >select @@server_id;`
- `+-------------+`
- `| @@server_id |`
- `+-------------+`
- `|           2 |`
- `+-------------+`
- `1 row in set (0.01 sec)`
- 
- `(ytt_mysqlrouter@centos-ytt57-2) : [ytt] >\q`
- `Bye`
15. 机器全挂了，重启 MGR
- `MySQL  localhost:3311 ssl  JS > dba.rebootClusterFromCompleteOutage()`
- `Reconfiguring the default cluster from complete outage...`
- 
- `The instance 'centos-ytt57-2:3312' was part of the cluster configuration.`
- `Would you like to rejoin it to the cluster? [y/N]: y`
- 
- `The instance 'centos-ytt57-3:3311' was part of the cluster configuration.`
- `Would you like to rejoin it to the cluster? [y/N]: y`
- 
- `The instance 'centos-ytt57-3:3312' was part of the cluster configuration.`
- `Would you like to rejoin it to the cluster? [y/N]: y`
- 
- `The safest and most convenient way to provision a new instance is through`
- `automatic clone provisioning, which will completely overwrite the state of`
- `'localhost:3311' with a physical snapshot from an existing cluster member. To`
- `use this method by default, set the 'recoveryMethod' option to 'clone'.`
- 
- `The incremental distributed state recovery may be safely used if you are sure`
- `all updates ever executed in the cluster were done with GTIDs enabled, there`
- `are no purged transactions and the new instance contains the same GTID set as`
- `the cluster or a subset of it. To use this method by default, set the`
- `'recoveryMethod' option to 'incremental'.`
- 
- `Incremental distributed state recovery was selected because it seems to be safely usable.`
- 
- `^C`
- `The cluster was successfully rebooted.`
- 
- `Script execution interrupted by user.`
- `MySQL  localhost:3311 ssl  JS > var cluster = dba.getCluster('ytt_mgr');`
- `MySQL  localhost:3311 ssl  JS > cluste.status();`
- `ReferenceError: cluste is not defined`
- `MySQL  localhost:3311 ssl  JS > cluster.status();`
- `{`
- `   "clusterName": "ytt_mgr",`
- `   "defaultReplicaSet": {`
- `       "name": "default",`
- `       "primary": "centos-ytt57-2:3311",`
- `       "ssl": "REQUIRED",`
- `       "status": "OK",`
- `       "statusText": "Cluster is ONLINE and can tolerate up to ONE failure.",`
- `       "topology": {`
- `           "centos-ytt57-2:3311": {`
- `               "address": "centos-ytt57-2:3311",`
- `               "mode": "R/W",`
- `               "readReplicas": {},`
- `               "role": "HA",`
- `               "status": "ONLINE",`
- `               "version": "8.0.17"`
- `           },`
- `           "centos-ytt57-2:3312": {`
- `               "address": "centos-ytt57-2:3312",`
- `               "mode": "R/O",`
- `               "readReplicas": {},`
- `               "role": "HA",`
- `               "status": "ONLINE",`
- `               "version": "8.0.17"`
- `           },`
- `           "centos-ytt57-3:3311": {`
- `               "address": "centos-ytt57-3:3311",`
- `               "mode": "R/O",`
- `               "readReplicas": {},`
- `               "role": "HA",`
- `               "status": "ONLINE",`
- `               "version": "8.0.17"`
- `           },`
- `           "centos-ytt57-3:3312": {`
- `               "address": "centos-ytt57-3:3312",`
- `               "mode": "R/O",`
- `               "readReplicas": {},`
- `               "role": "HA",`
- `               "status": "ONLINE",`
- `               "version": "8.0.17"`
- `           }`
- `       },`
- `       "topologyMode": "Single-Primary"`
- `   },`
- `   "groupInformationSourceMember": "centos-ytt57-2:3311"`
- `}`
## 社区近期动态
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)