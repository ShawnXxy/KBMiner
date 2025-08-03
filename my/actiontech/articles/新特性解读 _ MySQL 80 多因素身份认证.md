# 新特性解读 | MySQL 8.0 多因素身份认证

**原文链接**: https://opensource.actionsky.com/20220315-mysql8-0/
**分类**: MySQL 新特性
**发布时间**: 2022-03-15T00:15:16-08:00

---

作者：金长龙
爱可生测试工程师，负责DMP产品的测试工作
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 8.0.27 增加了多因素身份认证(MFA)功能，可以为一个用户指定多重的身份校验。为此还引入了新的系统变量 authentication_policy ，用于管理多因素身份认证功能。
我们知道在 MySQL 8.0.27 之前，create user 的时候可以指定一种认证插件，在未明确指定的情况下会取系统变量 default_authentication_plugin的值。default_authentication_plugin 的有效值有3个，分别是 mysql_native_password ，sha256_password ，caching_sha2_password ，这个3个认证插件是内置的、不需要注册步骤的插件。
## 一、系统变量 authentication_policy
在 MySQL 8.0.27 中由 authentication_policy 来管理用户的身份认证，先启个 mysql
`root@ubuntu:~# docker run --name mysql-1 -e MYSQL_ROOT_PASSWORD=123 -d --ip 172.17.0.2 mysql:8.0.27
`
同时查看下 authentication_policy 和 default_authentication_plugin 的值
`root@ubuntu:~# docker run -it --rm mysql:8.0.27 mysql -h172.17.0.2 -uroot -p123
......
mysql> show global variables like 'authentication_policy';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| authentication_policy | *,,   |
+-----------------------+-------+
1 row in set (0.02 sec)
mysql> show global variables like 'default_authentication_plugin';
+-------------------------------+-----------------------+
| Variable_name                 | Value                 |
+-------------------------------+-----------------------+
| default_authentication_plugin | caching_sha2_password |
+-------------------------------+-----------------------+
1 row in set (0.00 sec)
`
我们看到 authentication_policy 的默认值是*,,
第1个元素值是星号（*），表示可以是任意插件，默认值取 default_authentication_plugin 的值。如果该元素值不是星号（*），则必须设置为 mysql_native_password ，sha256_password ，caching_sha2_password 中的一个。
第2，3个元素值为空，这两个位置不能设置成内部存储的插件。如果元素值为空，代表插件是可选的。
建个用户看一下，不指定插件名称时，自动使用默认插件 caching_sha2_password
`mysql> create user 'wei1'@'localhost' identified by '123';
Query OK, 0 rows affected (0.01 sec)
mysql> select user,host,plugin from mysql.user where user='wei1';
+------+-----------+-----------------------+
| user | host      | plugin                |
+------+-----------+-----------------------+
| wei1  | localhost | caching_sha2_password |
+------+-----------+-----------------------+
1 row in set (0.00 sec)
`
指定插件名称时，会使用到对应的插件
`mysql> create user 'wei2'@'localhost' identified with mysql_native_password by '123';
Query OK, 0 rows affected (0.01 sec)
mysql> select user,host,plugin from mysql.user where user='wei2';
+------+-----------+-----------------------+
| user | host      | plugin                |
+------+-----------+-----------------------+
| wei2 | localhost | mysql_native_password |
+------+-----------+-----------------------+
1 row in set (0.01 sec)
`
尝试变更一下 authentication_policy 第一个元素的值，设置为 sha256_password
`mysql> set global authentication_policy='sha256_password,,';
Query OK, 0 rows affected (0.00 sec)
mysql> show global variables like 'authentication_policy';
+-----------------------+-------------------+
| Variable_name         | Value             |
+-----------------------+-------------------+
| authentication_policy | sha256_password,, |
+-----------------------+-------------------+
1 row in set (0.00 sec)
`
再次创建一个用户，不指定插件的名称
`mysql> create user 'wei3'@'localhost' identified by '123';
Query OK, 0 rows affected (0.01 sec)
mysql> select user,host,plugin from mysql.user where user='wei3';
+------+-----------+-----------------+
| user | host      | plugin          |
+------+-----------+-----------------+
| wei3 | localhost | sha256_password |
+------+-----------+-----------------+
1 row in set (0.00 sec)
`
可以看到默认使用的插件是 sha256_password ，说明当 authentication_policy 第一个元素指定插件名称时，default_authentication_plugin 被弃用了。
## 二、多重身份验证的用户
首先我们恢复 authentication_policy 至默认值
`mysql> set global authentication_policy='*,,';
Query OK, 0 rows affected (0.01 sec)
mysql> show global variables like 'authentication_policy';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| authentication_policy | *,,   |
+-----------------------+-------+
1 row in set (0.01 sec)
`
创建一个双重认证的用户。如下创建失败了，因为不可以同时用2种内部存储插件。
`mysql> create user 'wei3'@'localhost' identified by '123' and identified with mysql_native_password by '123';
ERROR 4052 (HY000): Invalid plugin "mysql_native_password" specified as 2 factor during "CREATE USER".
`
那我们来装一个可插拔插件 Socket Peer-Credential
`mysql> INSTALL PLUGIN auth_socket SONAME 'auth_socket.so';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%socket%';
+-------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+-------------+---------------+
| auth_socket | ACTIVE        |
+-------------+---------------+
1 row in set (0.00 sec)
`
再创建一个双重认证的用户
`mysql> create user 'wei4'@'localhost' identified by '123' and identified with auth_socket as 'root';
Query OK, 0 rows affected (0.05 sec)
mysql> select user,host,plugin,User_attributes from mysql.user where user='wei4';
+------+-----------+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| user | host      | plugin                | User_attributes                                                                                                                              |
+------+-----------+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| wei4 | localhost | caching_sha2_password | {"multi_factor_authentication": [{"plugin": "auth_socket", "passwordless": 0, "authentication_string": "root", "requires_registration": 0}]} |
+------+-----------+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
`
创建成功，之后用户&#8217;wei4&#8217;@&#8217;localhost&#8217;必须提供正确的密码，且同时本地主机的登录用户为 root 时，才会验证通过。
来试一下，以主机 root 用户身份，提供正确的密码 123 ，登录成功。
`root@ubuntu:~# docker exec -it mysql-1 bash
root@1d118873f98e:/# mysql -uwei4 --password1=123 --password2
mysql: [Warning] Using a password on the command line interface can be insecure.
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 8.0.27 MySQL Community Server - GPL
Copyright (c) 2000, 2021, Oracle and/or its affiliates.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
`
修改一下，将&#8217;wei4&#8217;@&#8217;localhost&#8217;要求的主机登录用户修改为wei4
`mysql> alter user 'wei4'@'localhost' modify 2 factor identified with auth_socket as 'wei4';
Query OK, 0 rows affected (0.16 sec)
mysql> select user,host,plugin,User_attributes from mysql.user where user='wei4';
+------+-----------+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| user | host      | plugin                | User_attributes                                                                                                                              |
+------+-----------+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| wei4 | localhost | caching_sha2_password | {"multi_factor_authentication": [{"plugin": "auth_socket", "passwordless": 0, "authentication_string": "wei4", "requires_registration": 0}]} |
+------+-----------+-----------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
`
再次以主机 root 用户身份，提供正确的密码 123 ，登录失败
`root@ubuntu:~# docker exec -it mysql-1 bash 
root@1d118873f98e:/# mysql -uwei4 --password1=123 --password2 
mysql: [Warning] Using a password on the command line interface can be insecure. 
Enter password: 
ERROR 1698 (28000): Access denied for user 'wei4'@'localhost'  
root@1d118873f98e:/#
`
因此可以认定双重身份认证机制是生效的。MySQL 8.0.27 最多可以对一个用户设置三重的身份认证，这里不再做展示说明。
简单总结下，已有的密码口令身份验证很适合网站或者应用程序的访问，但是在特定的情况下 如网络在线金融交易方面可能还是不够安全。多因素身份认证(MFA)功能的引入，可以在一定程度上提升数据库系统的安全性。
#### 参考资料：
https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_authentication_policy