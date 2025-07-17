# 技术分享 | MySQL 8.0 代理用户使用

**原文链接**: https://opensource.actionsky.com/20211028-proxy/
**分类**: 技术干货
**发布时间**: 2021-10-27T23:54:51-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 背景
某天有人问了我一个有关 MySQL PROXY 用户该如何使用的问题。
原问题是这样的：MySQL 版本从 5.5 升级到 8.0 后，proxy 用户怎么无法使用了？我之前是按照你博客上写的方法使用的，但是在升级后，安装插件提示如下错误：
`mysql:(none)>install plugin test_plugin_server soname 'auth_test_plugin.so';
ERROR 1126 (HY000): Can't open shared library 'auth_test_plugin.so' (errno: 0 API version for AUTHENTICATION plugin is too different)
`
这个咋回事？
我给了一个大家都很讨厌的答案： 去看 MySQL8.0 官方手册吧。
## 正文
#### 其实MySQL版本发展到8.0，已经完全没有必要使用 proxy  用户这个功能了，可以用角色完美替代。
auth_test_plugin.so 是 MySQL 5.5 的插件，仅限于测试环境，不推荐线上使用，仅限功能演示。之后的一系列大版本安装包里都不包含这个插件，所以使用方法有些差异。
#### 下面我对 proxy 用户在 MySQL 8.0 下如何使用做下简单演示。
我在下面示例中使用插件 mysql_native_password ，这个插件自带 proxy 用户功能，所以需要在配置文件里开启对应的开关，并重启 MySQL 实例：（如果使用 sha256_password ， 应该把参数 sha256_password_proxy_users=ON 也加到配置文件里。）
`[mysqld] 
check_proxy_users=ON 
mysql_native_password_proxy_users=ON 
`
**使用 proxy 用户功能之前，需要安装 mysql_no_login 插件，阻止隐藏在 proxy 用户下的真实用户登录 MySQL 。**
`mysql:(none)>install plugin mysql_no_login soname 'mysql_no_login.so';
Query OK, 0 rows affected (0.10 sec)
`
创建一个 proxy 用户 ytt_fake ，使用认证插件 mysql_native_password ：
`mysql:(none)>create user ytt_fake identified with mysql_native_password by 'ytt';
Query OK, 0 rows affected (0.32 sec)
`
##### 创建真实用户，并且认证插件使用 mysql_no_login ，禁止此用户登录 MySQL ，并且赋予他操作数据库ytt的所有权限。
`mysql:(none)>create user ytt_real identified with mysql_no_login by 'ytt';
Query OK, 0 rows affected (0.02 sec)
mysql:(none)>grant all on ytt.* to ytt_real;
Query OK, 0 rows affected (0.16 sec)
`
##### 授权 proxy 用户。
`mysql:(none)>grant proxy on ytt_real to ytt_fake;
Query OK, 0 rows affected (0.08 sec)
`
使用 Proxy 用户登录 MySQL ：
`root@ytt-ubuntu:~# mysql -u ytt_fake -pytt -hytt-ubuntu
...
Your MySQL connection id is 10
Server version: 8.0.26 MySQL Community Server - GPL
...
`
确认下变量 proxy_user 的值是不是 ytt_fake ：
`mysql:ytt>select @@proxy_user;
+----------------+
| @@proxy_user   |
+----------------+
| 'ytt_fake'@'%' |
+----------------+
1 row in set (0.00 sec)
`
使用 proxy 用户登录后，查看当前登录用户信息：用户实际上是 ytt_real 。
`mysql:(none)>select user(),current_user();
+---------------------+----------------+
| user()              | current_user() |
+---------------------+----------------+
| ytt_fake@ytt-ubuntu | ytt_real@%     |
+---------------------+----------------+
1 row in set (0.00 sec)
`
确认下权限：具有真实用户的所有权限。
`mysql:(none)>show grants;
+---------------------------------------------------+
| Grants for ytt_real@%                             |
+---------------------------------------------------+
| GRANT USAGE ON *.* TO `ytt_real`@`%`              |
| GRANT ALL PRIVILEGES ON `ytt`.* TO `ytt_real`@`%` |
+---------------------------------------------------+
2 rows in set (0.00 sec)
`
用 proxy 用户创建表、插入记录、查询、销毁表：
`mysql:ytt>create table fake1( id int primary key);
Query OK, 0 rows affected (0.23 sec)
mysql:ytt>insert fake1 select 1;
Query OK, 1 row affected (0.28 sec)
Records: 1  Duplicates: 0  Warnings: 0
mysql:ytt>table fake1;
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.00 sec)
mysql:ytt>drop table fake1;
Query OK, 0 rows affected (0.29 sec)
`
由于真实用户 ytt_real 使用认证插件 mysql_no_login ，MySQL 不允许此用户登录：
`root@ytt-ubuntu:~# mysql -uytt_real -pytt -h ytt-ubuntu
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'ytt_real'@'ytt-ubuntu' (using password: NO)
`
##### PROXY 用户有以下两个限制：
- 
隐藏在 proxy 用户后面的真实用户不能是匿名用户、也不能给用户赋予一个匿名 PROXY 用户。MySQL 这种场景只通过语法检测，不实际应用。
- 
多个用户可以共用一个 proxy 用户，但是不推荐！多个用户共用一个 proxy 用户，结果和预想有很大差异，也就是结果有不确定性特征。 比如用户 ytt_real 使用 proxy 用户 ytt_fake ，用户 ytt_real_other 也想使用 ytt_fake ，此时用户 ytt_fake 连接 MySQL 后，真实用户依然是 ytt_real ，直到用户 ytt_real 被删除，才会轮到第二个用户。