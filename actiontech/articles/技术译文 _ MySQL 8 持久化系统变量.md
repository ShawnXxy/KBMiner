# 技术译文 | MySQL 8 持久化系统变量

**原文链接**: https://opensource.actionsky.com/20201118-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-11-18T00:41:12-08:00

---

作者：Arunjith Aravindan
翻译：管长龙
本文来源：https://www.percona.com/blog/2020/10/27/using-mysql-8-persisted-system-variables/
MySQL 8 之前，使用的动态变量不是永久性的，并且在重启后会重置。可在运行时使用 SET 语句更改这些变量，以影响当前实例的操作，但是我们必须手动更新 my.cnf 配置文件以使其持久化。
在许多情况下，从服务端更新 my.cnf 并不是一个方便的选择，并且使变量仅被更新才能在后续重新启动时动态还原，而没有任何历史记录。
持久化系统变量是 MySQL 8 中引入的功能之一。新功能可帮助 DBA 动态更新变量并注册它们，而无需从服务器端访问配置文件。
**如何持久化全局系统变量？**
与 **SET GLOBAL** 一样，**SET PERSIST** 是可用于在运行时更新系统变量并使它们在重新启动后保持不变的命令。当我们使用 PERSIST 关键字时，变量更改将更新到数据目录中的 mysqld-auto.cnf 选项文件。mysqld-auto.cnf 是仅在第一次执行 **PERSIST** 或 **PERSIST_ONLY** 语句时创建的 JSON 格式文件。
让我们以更新最大连接数为例，看看此功能的工作原理。- 
- 
- 
- 
- 
- 
`mysql> SET PERSIST max_connections = 1000;``Query OK, 0 rows affected (0.00 sec)``mysql> select @@max_connections\G``*************************** 1. row ***************************``@@max_connections: 1000``1 row in set (0.00 sec)`
生成的 mysqld-auto.cnf 如下所示：- 
- 
- 
- 
- 
```
cat /var/lib/mysql/mysqld-auto.cnf`{ "Version" : 1 , "mysql_server" : {``     "max_connections" : {``         "Value" : "1000" , "Metadata" : {``             "Timestamp" : 1602543199335909 , "User" : "root" , "Host" : "localhost" } } } }
```
**如何保留只读的系统变量？**
当需要更改只读变量时，我们需要使用 **PERSIST_ONLY** 关键字。该子句更新 mysqld-auto.cnf 文件中的更改，但不适用于 MySQL，在下一次 MySQL 重新启动时继续存在。这使得 **PERSIST_ONLY** 适合配置只能在服务器启动时设置的只读系统变量。- 
- 
- 
- 
mysql>  SET PERSIST innodb_log_file_size=50331648*2;``ERROR 1238 (HY000): Variable 'innodb_log_file_size' is a read-only variable``mysql> set persist_only innodb_log_file_size=50331648*2;``Query OK, 0 rows affected (0.01 sec)`
**如何清除永久系统变量设置？**
我们可以使用 **RESET PERSIST** 命令从 mysqld-auto.cnf 中删除持久设置。运行不带特定变量名的命令时要小心，因为它将从配置文件中删除所有设置。实际上，它从 mysqld-auto.cnf 中删除了持久设置，但没有从 MySQL中 删除。
看几个例子：- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> RESET PERSIST;``Query OK, 0 rows affected (0.00 sec)``cat /var/lib/mysql/mysqld-auto.cnf``{ "Version" : 1 , "mysql_server" : {  } }``
``mysql> select @@max_connections;``+-------------------+``| @@max_connections |``+-------------------+``|              1000 |``+-------------------+``1 row in set (0.01 sec)`
如果想清除特定变量而不是清除配置文件中的所有设置，则以下示例向我们展示了如何执行此操作。如果我们尝试删除 mysqld-auto.cnf 中不存在的变量，则会导致错误，如下所示，我们可以使用 **IF EXISTS** 子句来抑制该错误。- 
- 
- 
- 
- 
- 
- 
- 
- 
```
mysql> RESET PERSIST max_connections;`Query OK, 0 rows affected (0.00 sec)``mysql> RESET PERSIST innodb_max_dirty_pages_pct;``ERROR 3615 (HY000): Variable innodb_max_dirty_pages_pct does not exist in persisted config file``mysql>``mysql> RESET PERSIST IF EXISTS innodb_max_dirty_pages_pct;``Query OK, 0 rows affected, 1 warning (0.00 sec)``mysql> show warnings;``| Warning | 3615 | Variable innodb_max_dirty_pages_pct does not exist in persisted config file |
```
**有没有办法禁用持久性？**
是的，**persisted_globals_load** 参数用于启用或禁用持久化的系统变量。禁用后，服务器启动顺序将忽略 mysqld-auto.cnf 文件。手动更改为 mysqld-auto.cnf 文件可能会在服务器启动时导致解析错误。在这种情况下，服务器报告错误并退出。如果发生此问题，则必须在禁用 persisted_globals_load 系统变量或使用以下示例中提供的 **&#8211;****-no-defaults** 选项的情况下启动服务器。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
mysql> select @@persisted_globals_load ;``+-------------------------------------+``| @@persisted_globals_load            |``+-------------------------------------+``|                 1                   |``+-------------------------------------+``1 row in set (0.00 sec)``
``grep -i persisted_globals_load /etc/my.cnf``persisted_globals_load=0``
``mysql> restart;``Query OK, 0 rows affected (0.00 sec)``
``mysql>  select @@persisted_globals_load ;``+-----------------------------------+``|    @@persisted_globals_load       |``+-----------------------------------+``|                 0                 |``+----------------------------------+``1 row in set (0.00 sec)``
``mysql> select @@max_connections;``+-------------------+``| @@max_connections |``+-------------------+``|               500 |``+-------------------+``1 row in set (0.00 sec)`
**需要什么授权？**
考虑到安全性，正确用户的正确权限绝对是最佳实践。SYSTEM_VARIABLES_ADMIN 和 PERSIST_RO_VARIABLES_ADMIN 是用户使用 SET PERSIST_ONLY 将全局系统变量持久保存到 mysqld-auto.cnf 的必需特权。
用户还需要具有 SHUTDOWN 特权才能使用 RESTART 命令。它提供了一种从客户端会话重新启动 MySQL 的方法，而无需在服务器主机上进行命令行访问。- 
- 
- 
- 
- 
`mysql> CREATE USER 'admin_persist'@'localhost' IDENTIFIED BY '*********';``Query OK, 0 rows affected (0.02 sec)``
``mysql> GRANT SYSTEM_VARIABLES_ADMIN, PERSIST_RO_VARIABLES_ADMIN, SHUTDOWN on *.* to 'admin_persist'@'localhost';``Query OK, 0 rows affected (0.03 sec)`
**如何监视变量？**
要列出使用 PERSIST 选项更新的变量，我们可以查询 performance_schema.persisted_variables 表以及其他几个表，如下所示。这是一个如何从 MySQL 端监视变量的简单示例，您可以根据需要修改查询。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> select v.VARIABLE_NAME,g.VARIABLE_VALUE current_value,p.VARIABLE_VALUE as persist_value,SET_TIME,SET_USER,VARIABLE_SOURCE,VARIABLE_PATH from performance_schema.variables_info v JOIN performance_schema.persisted_variables p USING(VARIABLE_NAME) JOIN performance_schema.global_variables g USING(VARIABLE_NAME)\G``*************************** 1. row ***************************``  VARIABLE_NAME: innodb_log_file_size``  current_value: 50331648``  persist_value: 100663296``       SET_TIME: 2020-10-12 18:54:35.725177``       SET_USER: arun``VARIABLE_SOURCE: COMPILED``  VARIABLE_PATH:``
``*************************** 2. row ***************************``  VARIABLE_NAME: max_connections``  current_value: 1000``  persist_value: 1000``       SET_TIME: 2020-10-12 18:53:19.336115``       SET_USER: root``VARIABLE_SOURCE: DYNAMIC``  VARIABLE_PATH:``2 rows in set (0.06 sec)``
``mysql> restart;``Query OK, 0 rows affected (0.01 sec)``
``select v.VARIABLE_NAME,g.VARIABLE_VALUE current_value,p.VARIABLE_VALUE as persist_value,SET_TIME,SET_USER,VARIABLE_SOURCE,VARIABLE_PATH from performance_schema.variables_info v JOIN performance_schema.persisted_variables p USING(VARIABLE_NAME) JOIN performance_schema.global_variables g USING(VARIABLE_NAME)\G``*************************** 1. row ***************************``  VARIABLE_NAME: innodb_log_file_size``  current_value: 100663296``  persist_value: 100663296``       SET_TIME: 2020-10-12 18:54:35.725177``       SET_USER: arun``VARIABLE_SOURCE: PERSISTED``  VARIABLE_PATH: /var/lib/mysql/mysqld-auto.cnf``
``*************************** 2. row ***************************``  VARIABLE_NAME: max_connections``  current_value: 1000``  persist_value: 1000``       SET_TIME: 2020-10-12 18:53:19.335909``       SET_USER: root``VARIABLE_SOURCE: PERSISTED``  VARIABLE_PATH: /var/lib/mysql/mysqld-auto.cnf``2 rows in set (0.16 sec)`
相关推荐：
[技术译文 | MySQL 8 中检查约束的使用](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247490230&idx=1&sn=0fb2403090593092cf96bc73ba7879a3&chksm=fc96f829cbe1713f70c6225c4a6cf8f65b2c027d2e1b4b5d5d97d490eb69b129934f6a7418a8&scene=21#wechat_redirect)
[技术译文 | MySQL 8 需要多大的 innodb_buffer_pool_instances 值（上）](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247489115&idx=1&sn=33e88824346ce39fc95354b994ce889a&chksm=fc96f4c4cbe17dd2e5aa25a9f3e4f6cc1a27ace44b05b618a12f4d4e5d88a0417f0c49e241bb&scene=21#wechat_redirect)
[技术译文 | MySQL 8 需要多大的 innodb_buffer_pool_instances 值（下）](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247489134&idx=1&sn=75eb33be84a16206fdc06e2386932c0b&chksm=fc96f4f1cbe17de75c7f90e5885f59a913634081159f4794434bcb32aae80c422707dfeba852&scene=21#wechat_redirect)