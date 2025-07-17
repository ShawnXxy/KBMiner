# 新特性解读 | MySQL 8.0 轻松改配置，云上友好

**原文链接**: https://opensource.actionsky.com/20191011-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-11T00:18:24-08:00

---

**背景**
MySQL 5.7 及之前版本下修改配置，如果能动态修改的，可以用 **set global** 语法，不能动态修改的，只能修改 `/etc/my.cnf` 配置文件，之后重启生效。如果需要持久化动态修改的参数，也只能同时修改 `/etc/my.cnf` 配置文件。
这个对云上环境不友好，毕竟云数据库上，大家无法直接远程底层虚拟机修改配置文件。针对如何持久化参数配置，在 MySQL 8.0，有一个新特性，可以实现轻松修改配置文件，那就是 **set persist **和 **set persist_only** 语法。前者用于修改并持久化动态参数，后者用于持久化静态参数。
**修改并持久化动态参数一例**- `mysql> show variables like '%innodb_buffer_pool_size%';`
- `+-------------------------+-----------+`
- `| Variable_name           | Value     |`
- `+-------------------------+-----------+`
- `| innodb_buffer_pool_size | 134217728 |`
- `+-------------------------+-----------+`
- `1 row in set (0.01 sec)`
- 
- `mysql> set persist innodb_buffer_pool_size=134217728*2;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> show variables like '%innodb_buffer_pool_size%';`
- `+-------------------------+-----------+`
- `| Variable_name           | Value     |`
- `+-------------------------+-----------+`
- `| innodb_buffer_pool_size | 268435456 |`
- `+-------------------------+-----------+`
- `1 row in set (0.00 sec)`
在数据目录里，会生成一个持久化参数的 json 格式文件，内容如下：- `[root@pxc1 data]# cat mysqld-auto.cnf |jq`
- `{`
- `  "Version": 1,`
- `  "mysql_server": {`
- `    "innodb_buffer_pool_size": {`
- `      "Value": "268435456",`
- `      "Metadata": {`
- `        "Timestamp": 1570678719890919,`
- `        "User": "root",`
- `        "Host": "localhost"`
- `      }`
- `    }`
- `}`
**点评：****居然有时间戳，还有谁修改了参数！**
**持久化静态参数一例**- `# 我们先模拟没有权限`
- `mysql> revoke SYSTEM_VARIABLES_ADMIN, PERSIST_RO_VARIABLES_ADMIN on *.* from 'root'@'localhost';`
- `Query OK, 0 rows affected, 1 warning (0.01 sec)`
- 
- `mysql> show variables like 'innodb_log_file_size';`
- `+----------------------+----------+`
- `| Variable_name        | Value    |`
- `+----------------------+----------+`
- `| innodb_log_file_size | 50331648 |`
- `+----------------------+----------+`
- `1 row in set (0.01 sec)`
- 
- `mysql> set persist innodb_log_file_size=50331648*2;`
- `ERROR 1238 (HY000): Variable 'innodb_log_file_size' is a read only variable`
- 
- `# 因缺少SYSTEM_VARIABLES_ADMIN 和 PERSIST_RO_VARIABLES_ADMIN 权限而报错`
- `mysql> set persist_only innodb_log_file_size=50331648*2;`
- `ERROR 3630 (42000): Access denied; you need SYSTEM_VARIABLES_ADMIN and PERSIST_RO_VARIABLES_ADMIN privileges for this operation`
- 
- `# 增加授权`
- `mysql> grant SYSTEM_VARIABLES_ADMIN, PERSIST_RO_VARIABLES_ADMIN on *.* to 'root'@'localhost';`
- `Query OK, 0 rows affected, 1 warning (0.01 sec)`
- 
- `# 修改成功`
- `mysql> set persist_only innodb_log_file_size=50331648*2;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `# 重启，MySQL8.0支持在数据库里重启操作，云友好！`
- `mysql> restart;`
- `Query OK, 0 rows affected (0.00 sec)`
**mysql> restart；****ERROR 3707 (HY000): Restart server failed (mysqld is not managed by supervisor process).****注意：要求 mysqld 运行在 mysqld_safe 下。**
**清空 persist 持久化参数**
- `mysql> RESET PERSIST;`
- `Query OK, 0 rows affected (0.00 sec)`
人手删除此文件或人手清空此文件内容，也可以达到相同效果。当然了，云数据库上只能用 `RESET PERSIST` 了。
**相关 performance_schema 表**
1. 查看数据库启动后载入的 PERSIST 相关参数在重启数据库后，我们可以通过表 `performance_schema.variables_info` 查看我们从哪些 `mysqld-auto.cnf` 载入了哪些参数。
- `mysql> select * from performance_schema.variables_info where variable_source like 'PERSISTED'\G`
- `*************************** 1. row ***************************`
- `  VARIABLE_NAME: innodb_buffer_pool_size`
- `VARIABLE_SOURCE: PERSISTED`
- `  VARIABLE_PATH: /data/mysql/mysql3308/data/mysqld-auto.cnf`
- `      MIN_VALUE: 5242880`
- `      MAX_VALUE: 9223372036854775807`
- `       SET_TIME: 2019-10-10 11:38:39.890919`
- `       SET_USER: root`
- `       SET_HOST: localhost`
- `*************************** 2. row ***************************`
- `  VARIABLE_NAME: innodb_log_file_size`
- `VARIABLE_SOURCE: PERSISTED`
- `  VARIABLE_PATH: /data/mysql/mysql3308/data/mysqld-auto.cnf`
- `      MIN_VALUE: 4194304`
- `      MAX_VALUE: 18446744073709551615`
- `       SET_TIME: 2019-10-10 11:21:12.623177`
- `       SET_USER: root`
- `       SET_HOST: localhost`
- `2 rows in set (0.02 sec)`
2. 查看变量都来自于哪里
- `mysql> SELECT t1.VARIABLE_NAME, VARIABLE_VALUE, VARIABLE_SOURCE`
- `    -> FROM performance_schema.variables_info t1`
- `    -> JOIN performance_schema.global_variables t2`
- `    -> ON t2.VARIABLE_NAME=t1.VARIABLE_NAME`
- `    -> WHERE t1.VARIABLE_SOURCE != 'COMPILED';`
- `+--------------------------------------+-------------------------------------+-----------------+`
- `| VARIABLE_NAME                        | VARIABLE_VALUE                      | VARIABLE_SOURCE |`
- `+--------------------------------------+-------------------------------------+-----------------+`
- `| auto_increment_increment             | 1                                   | EXPLICIT        |`
- `| auto_increment_offset                | 1                                   | EXPLICIT        |`
- `...`
- `| binlog_format                        | ROW                                 | DYNAMIC         |`
- `| binlog_rows_query_log_events         | ON                                  | EXPLICIT        |`
- `| foreign_key_checks                   | ON                                  | DYNAMIC         |`
- `| gtid_executed_compression_period     | 1000                                | EXPLICIT        |`
- `| innodb_buffer_pool_size              | 268435456                           | PERSISTED       |`
- `| innodb_change_buffer_max_size        | 25                                  | EXPLICIT        |`
- `| innodb_log_file_size                 | 100663296                           | PERSISTED       |`
- `| innodb_log_files_in_group            | 2                                   | EXPLICIT        |`
- `| pid_file                             | /data/mysql/mysql3308/data/pxc1.pid | COMMAND_LINE    |`
- `| port                                 | 3308                                | EXPLICIT        |`
- `+--------------------------------------+-------------------------------------+-----------------+`
- `73 rows in set (0.01 sec)`
**EXPLICIT 来自于参数配置文件 my.cnf********COMMAND_LINE 来自于启动 mysqld 时额外的 command_line******
**PERSISTED 来自于数据目录下 mysqld-auto.cnf******
**DYNAMIC 来自于 SESSION 变量（包括 GLOBAL 变量的继承）**
3. 查看动态修改的 session 变量（包括 GLOBAL 变量的继承）- `mysql> set session binlog_format='Mixed';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> set global read_only=1;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> SELECT t1.VARIABLE_NAME, VARIABLE_VALUE, VARIABLE_SOURCE FROM performance_schema.variables_info t1 JOIN performance_schema.session_variables t2 ON t2.VARIABLE_NAME=t1.VARIABLE_NAME WHERE t1.VARIABLE_SOURCE = 'DYNAMIC';`
- `+--------------------+----------------+-----------------+`
- `| VARIABLE_NAME      | VARIABLE_VALUE | VARIABLE_SOURCE |`
- `+--------------------+----------------+-----------------+`
- `| binlog_format      | MIXED          | DYNAMIC         |`
- `| foreign_key_checks | ON             | DYNAMIC         |`
- `| read_only          | ON             | DYNAMIC         |`
- `+--------------------+----------------+-----------------+`
- `2 rows in set (0.01 sec)`
**吐槽**
MySQL 8.0 对于 `all` 这个权限没之前直观了。
- `mysql> create user fander@'%' identified by 'password';`
- `Query OK, 0 rows affected (0.03 sec)`
- 
- `mysql> grant all on *.* to fander@'%';`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `mysql> show grants for fander@'%';`
- `+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| Grants for fander@%                                                                                                                                                                                                                                                                                                                                                                                                                                                    |`
- `+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, ALTER, SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, CREATE TABLESPACE, CREATE ROLE, DROP ROLE ON *.* TO `fander`@`%`                                                                                       |`
- `| GRANT APPLICATION_PASSWORD_ADMIN,AUDIT_ADMIN,BACKUP_ADMIN,BINLOG_ADMIN,BINLOG_ENCRYPTION_ADMIN,CLONE_ADMIN,CONNECTION_ADMIN,ENCRYPTION_KEY_ADMIN,GROUP_REPLICATION_ADMIN,INNODB_REDO_LOG_ARCHIVE,PERSIST_RO_VARIABLES_ADMIN,REPLICATION_SLAVE_ADMIN,RESOURCE_GROUP_ADMIN,RESOURCE_GROUP_USER,ROLE_ADMIN,SERVICE_CONNECTION_ADMIN,SESSION_VARIABLES_ADMIN,SET_USER_ID,SYSTEM_USER,SYSTEM_VARIABLES_ADMIN,TABLE_ENCRYPTION_ADMIN,XA_RECOVER_ADMIN ON *.* TO `fander`@`%` |`
- `+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `2 rows in set (0.01 sec)`
**潜台词：我还得数一数权限是否足够。**
作为对比，以下是 5.7 的显示方式：
- `mysql> create user fander@'%' identified by 'password';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> grant all on *.* to fander@'%';`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> show grants for fander@'%';`
- `+---------------------------------------------+`
- `| Grants for fander@%                         |`
- `+---------------------------------------------+`
- `| GRANT ALL PRIVILEGES ON *.* TO 'fander'@'%' |`
- `+---------------------------------------------+`
- `1 row in set (0.00 sec)`
**参考链接：**
https://lefred.be/content/mysql-8-0-changing-configuration-easily-and-cloud-friendly/
https://lefred.be/content/what-configuration-settings-did-i-change-on-my-mysql-server/
**社区近期动态**
**No.1**
**10.26 DBLE 用户见面会 北京站**
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/默认标题_横版海报_2019.09.16.jpg)											
爱可生开源社区将在 2019 年 10 月 26 日迎来在北京的首场 DBLE 用户见面会，以线下**互动分享**的会议形式跟大家见面。
时间：10月26日 9:00 &#8211; 12:00 AM
地点：HomeCafe 上地店（北京市海淀区上地二街一号龙泉湖酒店对面）
重要提醒：
1. 同日下午还有 dbaplus 社群举办的沙龙：聚焦数据中台、数据架构与优化。
2. 爱可生开源社区会在每年10.24日开源一款高质量产品。本次在 dbaplus 沙龙会议上，爱可生的资深研发工程师闫阿龙，将为大家带来《金融分布式事务实践及txle概述》，并在现场开源。
**No.2**
**「3306π」成都站 Meetup**
知数堂将在 2019 年 10 月 26 日在成都举办线下会议，本次会议中邀请了五位数据库领域的资深研发/DBA进行主题分享。
时间：2019年10月26日 13:00-18:00
地点：成都市高新区天府三街198号腾讯成都大厦A座多功能厅
**No.3**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
- 技术交流群，进群后可提问
QQ群（669663113）
- 社区通道，邮件&电话
osc@actionsky.com
- 现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.4**
**社区技术内容征稿**
征稿内容：
- 格式：.md/.doc/.txt
- 主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
- 要求：原创且未发布过
- 奖励：作者署名；200元京东E卡+社区周边
投稿方式：
- 邮箱：osc@actionsky.com
- 格式：[投稿]姓名+文章标题
- 以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系