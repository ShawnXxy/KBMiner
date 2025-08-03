# 技术分享 | MySQL 设置管理员密码无法生效一例

**原文链接**: https://opensource.actionsky.com/20220601-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-06-01T01:09:12-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
昨天某位客户向我咨询这样一个问题：他通过本地 MySQL 命令行连接数据库发现管理员不需要验证密码即可进行后续操作。为了查明原因，他尝试过修改管理员密码，依然无效。为了对比，他还特意创建了一个带密码的新用户，通过 MySQL 命令行可以正常进行密码验证。
经过对他遇到的问题做了详细了解后，我大概知道问题出在哪，不过还需要继续验证。
##### 此类问题大致会有如下几种原因：
- 此用户本身并没有设置密码。
- 配置文件里开启 skip-grant-tables 跳过授权表。
- 配置文件里有明文 password 选项来跳过密码。
- 用户的认证插件有可能使用 auth_socket 。
我先来大致复现下这个问题。现象如下：MySQL 命令行客户端打印“hello world ”不需要验证密码。
root@ytt-large:/home/ytt# mysql -e "select 'hello world'"
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
换个用户就必需验证密码后方可正常打印字符串：
root@ytt-large:/home/ytt# mysql -uadmin -e "select 'hello world'"
ERROR 1045 (28000): Access denied for user 'admin'@'localhost' (using password: NO)
root@ytt-large:/home/ytt# mysql -uadmin -p -e "select 'hello world'"
Enter password: 
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
尝试修改管理员密码，依然不需要验证密码即可执行命令：看结果好像是修改密码无效。
root@ytt-large:~# mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 35
Server version: 8.0.29 MySQL Community Server - GPL
...
mysql> alter user root@localhost identified by 'root';
Query OK, 0 rows affected (0.00 sec)
mysql> exit
Bye
root@ytt-large:/home/ytt# mysql -e "select 'hello world'"
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
##### 那接下来基于我复现的场景以及我开头想到的可能原因来逐步判断到底问题出在哪里。
- 此用户本身并没有设置密码。
这个原因可以快速排除掉！已经执行过一次 alter user 改密码的操作，所以不可能没有密码。
- 配置文件里开启 skip-grant-tables 跳过授权表。
这个原因也可以快速排除掉！ 如果是因为开启这个选项，那必定所有用户都不会验证密码，而不只是针对管理员账号本身。
- 配置文件里有明文 password 选项来跳过密码。
有可能是这个原因。 可以用工具 my_print_defaults 来打印相关配置、或者直接手动检查配置文件有没有[client] 、[mysql] 等段里包含有 password 明文选项。例如：
root@ytt-large:/home/ytt# my_print_defaults /etc/mysql/my.cnf client mysql--password=*****
结果确实是设置了 password 选项，但是仔细想想，有点站不住脚。 如果是因为这个原因，那修改密码后，为什么依然不验证新密码？ 因此这个可能性也被排除掉。
- 用户的认证插件有可能使用 auth_socket 。
极有可能是这个原因！
插件 auth_socket MySQL 官网全称为：Socket Peer-Credential Pluggable Authentication（套接字对等凭据可插拔的身份验证）。
官方文档地址：https://dev.mysql.com/doc/refman/8.0/en/socket-pluggable-authentication.html
阅读官方文档后可以得出的结论为**插件 auth_socket 不需要验证密码即可进行本地认证！**它有两个认证条件：
- *客户端通过本地 unix socket 文件连接 MySQL 服务端。*
- *通过 socket 的选项 SO_PEERCRED 来获取运行客户端的 OS 用户名，随后判断 OS 用户名是否在 mysql.user 表里。*
另外，想了解更多关于 socket 的选项 SO_PEERCRED 可以参考这个网址：https://man7.org/linux/man-pages/man7/unix.7.html
那我们接下来验证结论是否正确。查看当前登录用户是不是**root@localhost**： 确认无疑。
root@ytt-large:/home/ytt# mysql  -e "select user(),current_user()"
+----------------+----------------+
| user()         | current_user() |
+----------------+----------------+
| root@localhost | root@localhost |
+----------------+----------------+
检查 mysql.user 表记录：检查字段 plugin、authentication_string（此字段有可能不为空）。
mysql> select plugin,authentication_string from mysql.user where user = 'root' ;
+-------------+-----------------------+
| plugin      | authentication_string |
+-------------+-----------------------+
| auth_socket |                       |
+-------------+-----------------------+
1 row in set (0.01 sec)
确认管理员账号插件为 auth_socket ，难怪改密码无效。接下来把插件改为非 auth_socket 即可。
mysql> alter user root@localhost identified with mysql_native_password by 'root';
Query OK, 0 rows affected (0.04 sec)
再次执行 MySQL 命令行：无密码正常报错，输入正确密码后执行成功。
root@ytt-large:/home/ytt# mysql -p -e "select 'hello world'"
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
root@ytt-large:/home/ytt# mysql -proot -e "select 'hello world'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
#### 结语：
一般在遇到 MySQL 问题时，建议对 MySQL 系统函数、数据库内部对象等进行检索而不是直接打印字符串，有时候可能对快速定位问题原因有帮助。