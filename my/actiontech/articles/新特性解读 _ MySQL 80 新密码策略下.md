# 新特性解读 | MySQL 8.0 新密码策略（下）

**原文链接**: https://opensource.actionsky.com/20211223-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-12-22T22:08:55-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
今天我们来继续介绍 MySQL 8.0 的新密码策略， 分别为双密码策略和内置随机密码生成。
##### 第一，双密码策略：
首先来解释下什么是双密码策略？ 双密码策略就是在日常运维中，需要定期更改指定用户密码，同时又需要旧密码暂时保留一定时长的一种策略。其作用是延迟应用与数据库之间的用户新旧密码对接时间，进而平滑应用的操作感知。可以在如下场景中使用：
在 MySQL 数据库里我们部署最多也是最成熟的架构：一主多从。比如说此架构做了读写分离，主负责处理前端的写流量，读负责处理前端的读流量，为了安全起见，需要定期对应用连接数据库的用户更改密码。有了双密码机制，对用户密码的更改在应用端可以有一定的缓冲延迟，避免业务中断风险以及开发人员的抱怨。应用端依然可以使用旧密码来完成对数据库的检索，等待合适时机再使用管理员发来的新密码检索数据库。
**双密码机制包含主密码与备密码，当备密码不再使用时，告知管理员丢弃备密码，此时用户的主密码即是唯一密码。**
具体如何使用呢？ 用法如下：
管理员先创建一个新用户 ytt ，密码是 root_old ，完了更改他的密码为 root_new 。此时 root_new 即为主密码，而 root_old 即为备密码。
`mysql:(none)>create user ytt identified by 'root_old';
Query OK, 0 rows affected, 2 warnings (0.24 sec)
mysql:(none)>alter user ytt identified by 'root_new' retain current password;
Query OK, 0 rows affected (0.17 sec)
`
接下来用户 ytt 分别使用备密码与主密码连接 MySQL 并且执行一条简单的 SQL 语句：
备密码连接数据库：
`root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -P 3306 -uytt -proot_old -e "select 'hello world'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
`
主密码连接数据库：
`root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -P 3306 -uytt -proot_new -e "select 'hello world'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
`
可以发现在管理员没有丢弃旧密码前，两个密码都能正常使用。
相关业务更改完成后，即可告知管理员丢弃备密码：
`root@ytt-ubuntu:/home/ytt# mysql -S /opt/mysql/mysqld.sock
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 27
Server version: 8.0.27 MySQL Community Server - GPL
...
mysql:(none)>alter user ytt discard old password;
Query OK, 0 rows affected (0.02 sec)
mysql:(none)>\q
Bye
`
###### 双密码策略有以下需要注意的事项：
- 
如果用户本身已经有双密码策略，再次更改新密码时没有带 retain current password 子句，那之前的主密码被替换成新改的密码，但是备密码不会被替换。比如更改新密码为 root_new_new ，此时备密码依然是 root_old ，并非之前的主密码 root_new 。下面例子中输入密码 root_old 依然可以连接数据库，而输入密码 root_new 则被数据库拒绝连接：
` mysql:(none)>alter user ytt identified by 'root_new_new';
Query OK, 0 rows affected (0.16 sec)
root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -u ytt -proot_old -e "select 'hello world'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -u ytt -proot_new -e "select 'hello world'"
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'ytt'@'ytt-ubuntu' (using password: YES)
`
还有一点需要注意的细节，如果不带 retain current password  子句，并且更改新密码为空串，那么主备密码则会统一更改为空串。下面例子中数据库拒绝之前的备密码连接：
`mysql:(none)>alter user ytt identified by '';
Query OK, 0 rows affected (0.80 sec)
root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -u ytt -proot_old -e "select 'hello world'"
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'ytt'@'ytt-ubuntu' (using password: YES)
root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -u ytt  -e "select 'hello world'"
+-------------+
| hello world |
+-------------+
| hello world |
+-------------+
`
- 
新密码为空，不允许使用备用密码。
` mysql:(none)>alter user ytt identified by '' retain current password;
ERROR 3895 (HY000): Current password can not be retained for user 'ytt'@'%' because new password is empty.
`
- 
使用双密码策略时，不能更改用户的认证插件。
` mysql:(none)>alter user ytt identified with sha256_password by 'root_new' retain current password;
ERROR 3894 (HY000): Current password can not be retained for user 'ytt'@'%' because authentication plugin is being changed.
`
##### 第二，随机密码生成：
以往旧版本有生成随机密码的需求，在 MySQL 端无法直接设定，除非封装用户密码设定逻辑，并且在代码里实现随机密码生成。比如用存储过程，脚本等等。
MySQL 8.0 直接可以设置用户随机密码
`mysql:(none)>create user ytt_new identified by random password;
+---------+------+----------------------+-------------+
| user    | host | generated password   | auth_factor |
+---------+------+----------------------+-------------+
| ytt_new | %    | >h<m3[bnigz%*f/SnLfp |           1 |
+---------+------+----------------------+-------------+
1 row in set (0.02 sec)
`
也可以用 set password 子句来设置随机密码
`mysql:(none)>set password for ytt_new to random;
+---------+------+----------------------+-------------+
| user    | host | generated password   | auth_factor |
+---------+------+----------------------+-------------+
| ytt_new | %    | 5wzZ+0[27cd_CW/]<ua, |           1 |
+---------+------+----------------------+-------------+
1 row in set (0.04 sec)
`
另外，随机密码的长度由参数 generated_random_password_length 调整，默认为 20 个。
#### 总结
双密码策略能让应用和DBA沟通起来更加协调；随机密码设置能让数据库系统更加安全。