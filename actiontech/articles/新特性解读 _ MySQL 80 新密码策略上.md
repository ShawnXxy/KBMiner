# 新特性解读 | MySQL 8.0 新密码策略（上）

**原文链接**: https://opensource.actionsky.com/20211214-mysql8-0/
**分类**: MySQL 新特性
**发布时间**: 2021-12-13T18:36:21-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 引言
这里来介绍下MySQL 8.0 版本自带的新密码验证策略。
## 正文
我们非常熟悉这样的模式： 用户想更改自己密码，需要提供原来密码或者追加手机验证码才可以， 这种模式在MySQL数据库里一直不存在。在MySQL 8.0 之前的版本，普通用户可以直接更改自己密码，不需要旧密码验证，也不需要知会管理员，比如用户ytt_admin 需要更改密码，在MySQL 5.7 下直接敲alter user 命令即可：
`root@ytt-ubuntu:~# mysql -uytt_admin -proot1234 -P5734 -h ytt-ubuntu -e "alter user ytt_admin identified by 'root'"
mysql: [Warning] Using a password on the command line interface can be insecure.
`
##### 这样的密码更改行为其实不是很安全，假设有下面的场景出现：
###### 用户ytt_admin 登录到MySQL服务后，做了些日常操作，完成后忘记退出；此时刚好有一个别有用心的用户ytt_fake 进入ytt_admin的登录环境，直接敲命令alter user 即可更改用户ytt_admin的密码，并且退出当前登录环境，用户ytt_admin本尊再次登录MySQL，就会提示密码错误，不允许登录，此时用户ytt_admin大脑肯定是懵的。
##### 为了防止这类不安全事件的发生，MySQL 8.0 发布了一系列密码验证策略。 这里介绍第一项：当前密码验证策略设置！
##### 当前密码验证策略有两种方法来给到具体用户。
###### 第一种，从管理员侧来设置单个用户的当前密码验证策略。
创建用户或者更改用户设置时使用子句： password require current（表示强制此用户满足当前密码验证策略） 。
`mysql:(none)>create user ytt_admin identified by 'root123' password require current;
Query OK, 0 rows affected (0.11 sec)
`
之后以用户ytt_admin 登录MySQL并且更改密码，提示需要提供旧密码才行。
`root@ytt-ubuntu:/home/ytt# mysql -h ytt-ubuntu -uytt_admin -proot123
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 33
Server version: 8.0.27 MySQL Community Server - GPL
mysql:(none)>alter user ytt_admin identified by 'root';
ERROR 3892 (HY000): Current password needs to be specified in the REPLACE clause in order to change it.
`
接下来，alter user 跟上子句replace 来让用户ytt_admin输入旧密码，成功更改新密码。
`mysql:(none)>alter user ytt_admin identified by 'root' replace 'root123';
Query OK, 0 rows affected (0.00 sec)
`
如果有的场景下需要保持MySQL旧版本的密码更改行为，管理员侧可以用子句： password require current optional 关闭新特性。
`-- (optional 关键词可用default 替代，参考全局密码验证参数设置)
mysql:(none)>alter user ytt_admin password require current optional;
Query OK, 0 rows affected (0.04 sec)
`
来再次验证下用户ytt_admin更改密码的行为：又变更为不安全的MySQL旧版本安全行为。
`mysql:(none)>alter user ytt_admin identified by 'root';
Query OK, 0 rows affected (0.01 sec)
`
###### 第二种，设置全局参数，来强制所有用户使用当前密码验证策略。
MySQL 8.0 新版本内置的参数password_require_current 定义一个全局密码策略，默认关闭。开启这个选项时，要求用户更改密码时必须提供旧密码。
开启全局参数：
`mysql:(none)>set persist password_require_current=on;
Query OK, 0 rows affected (0.00 sec)
`
创建另外一个新用户 ytt_usage：
`mysql:(none)>create user ytt_usage identified by 'root123';
Query OK, 0 rows affected (0.00 sec)
`
以用户ytt_usage登录MySQL更改自己密码： 直接拒绝更改，需要提供旧密码。
`root@ytt-ubuntu:~# mysql -uytt_usage -proot123 -h ytt-ubuntu
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 37
Server version: 8.0.27 MySQL Community Server - GPL
...
mysql:(none)>alter user ytt_usage identified by 'root';
ERROR 3892 (HY000): Current password needs to be specified in the REPLACE clause in order to change it.
mysql:(none)>
`
replace 子句提供旧密码再次成功更改新密码:
`mysql:(none)>alter user ytt_usage identified by 'root' replace 'root123';
Query OK, 0 rows affected (0.02 sec)
`
这里有一个需要注意的点：虽然全局参数开启，但是alter user 命令优先级更高，可以直接覆盖全局参数设置。下面是全局参数开启的环境下，用alter user命令来关闭用户ytt_usage的当前密码验证策略。
`mysql:(none)>alter user ytt_usage password require current optional;
Query OK, 0 rows affected (0.11 sec)
`
接下来用户ytt_usage 又恢复为MySQL旧版本的安全行为：
`mysql:(none)>alter user ytt_usage identified by 'rootnew';
Query OK, 0 rows affected (0.11 sec)
`
还有另外一个子句： password require current default ，具体行为由全局参数password_require_current 的设置决定，全局参数关闭，这个子句恢复MySQL旧版本安全行为；全局参数开启，这个子句使用MySQL 新版本安全行为。
`mysql:(none)>alter user ytt_usage password require current default;
Query OK, 0 rows affected (0.09 sec)
`
## 总结：
本文介绍的当前密码验证策略，使得MySQL 朝着更加安全的方向努力。