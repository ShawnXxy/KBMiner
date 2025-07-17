# 新特性解读 | MySQL 8.0 新密码策略（中）

**原文链接**: https://opensource.actionsky.com/20211214-mysql8-0_2/
**分类**: MySQL 新特性
**发布时间**: 2021-12-13T23:08:14-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本篇继续介绍 MySQL 8.0 的新密码验证策略。
假设有这样的需求： 管理员分别创建了一个开发用户与运维用户，并且要求这两个用户必须满足如下需求，
- 
开发用户要求定期更改密码，并且密码不能与近期更改过的密码重叠，也即不能复用历史密码，这里限定历史密码个数为3；
- 
运维用户同样要求定期更改密码，并且密码不能与某段时间内更改过的密码重叠，也即同样不能复用历史密码，这里限定时间段为一个礼拜。
以上两种改密码需求，在数据库侧暂时无法实现，只能拿个**”小本子记住历史密码保留个数、历史密码保留天数“**，在用户每次更改密码前，先检测小本子上有没有和新密码重叠的历史密码。
**MySQL 8.0 对以上这两种改密码需求，直接从数据库端实现，用户可以扔掉“小本子”了。**
我来分两部分讲解在 MySQL 8.0 版本里对以上改密码需求的具体实现。
##### 第一，在配置文件里写上全局参数
参数 password_history 表示最近使用的密码保留次数；
参数 password_reuse_interval 表示最近使用的密码保留天数。
###### 先来实现开发用户的需求：保留历史密码个数为3。
管理员用户登录，设置全局参数：
`mysql:(none)>set persist password_history=3;
Query OK, 0 rows affected (0.00 sec)
`
退出重连，创建用户 ytt_dev :
`root@ytt-ubuntu:/home/ytt# mysql -S /opt/mysql/mysqld.sock
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 33
Server version: 8.0.27 MySQL Community Server - GPL
...
mysql:(none)>create user ytt_dev identified by 'root123';
Query OK, 0 rows affected (0.15 sec)
`
退出连接，用户 ytt_dev 重新连接数据库，并且更改两次密码：
`root@ytt-ubuntu:/home/ytt# mysql -uytt_dev -hytt-ubuntu -proot123
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 34
Server version: 8.0.27 MySQL Community Server - GPL
...
mysql:(none)>
mysql:(none)>alter user ytt_dev identified by 'root456';
Query OK, 0 rows affected (0.03 sec)
mysql:(none)>alter user ytt_dev identified by 'root789';
Query OK, 0 rows affected (0.17 sec)
`
加上原始密码，也就是3次密码，再来更改一次密码，此时不允许更改密码，错误提示和密码历史策略冲突：
`mysql:(none)>alter user ytt_dev identified by 'root123';
ERROR 3638 (HY000): Cannot use these credentials for 'ytt_dev@%' because they contradict the password history policy
`
接下来，选择一个与历史密码不冲突的新密码进行修改，此时密码修改成功：
`mysql:(none)>alter user ytt_dev identified by 'rootnew';
Query OK, 0 rows affected (0.04 sec)
`
###### 再来实现运维用户的需求：保留密码天数为7天。
同样，管理员用户登录 MySQL ，并且设置全局参数：
`mysql:(none)>set persist password_reuse_interval = 7;
Query OK, 0 rows affected (0.00 sec)
mysql:(none)>set persist password_history=default;
Query OK, 0 rows affected (0.00 sec)
`
退出重新连接，创建运维用户 ytt_dba :
`mysql:(none)>create user ytt_dba identified by 'root123';
Query OK, 0 rows affected (0.01 sec)
mysql:(none)>\q
Bye
`
以用户 ytt_dba 登录数据库，并且改了五次密码：
`root@ytt-ubuntu:/home/ytt# mysql -uytt_dba -hytt-ubuntu -proot123
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 39
Server version: 8.0.27 MySQL Community Server - GPL
...
mysql:(none)>alter user ytt_dba identified by 'root456';
Query OK, 0 rows affected (0.15 sec)
mysql:(none)>alter user ytt_dba identified by 'root789';
Query OK, 0 rows affected (0.08 sec)
mysql:(none)>alter user ytt_dba identified by 'root000';
Query OK, 0 rows affected (0.02 sec)
mysql:(none)>alter user ytt_dba identified by 'root888';
Query OK, 0 rows affected (0.02 sec)
mysql:(none)>alter user ytt_dba identified by 'root999';
Query OK, 0 rows affected (0.12 sec)
`
接下来验证历史密码验证策略，由于我们设置了密码历史保留天数，任何在设定时间内的历史密码，均不能作为新密码使用：MySQL 拒绝用户更改密码，错误提示与密码历史策略冲突：
`mysql:(none)>alter user ytt_dba identified by 'root123';
ERROR 3638 (HY000): Cannot use these credentials for 'ytt_dba@%' because they contradict the password history policy
mysql:(none)>alter user ytt_dba identified by 'root456';
ERROR 3638 (HY000): Cannot use these credentials for 'ytt_dba@%' because they contradict the password history policy
mysql:(none)>
`
选择一个非最近更改过的新密码，改密成功：
`mysql:(none)>alter user ytt_dba identified by 'rootnew';
Query OK, 0 rows affected (0.10 sec)
`
如果有一个用户同时需要具备开发用户和运维用户的密码限制条件，可以把两个全局参数一起修改即可：历史密码保留天数为7天、同时历史密码保留个数为3次。
`mysql:(none)>set persist password_reuse_interval = 7;
Query OK, 0 rows affected (0.00 sec)
mysql:(none)>set persist password_history=3;
Query OK, 0 rows affected (0.00 sec)
`
##### 第二， 管理员在创建用户或者更改用户属性时可以对单个用户定义密码验证策略
把全局参数重置为默认，也即关闭密码验证策略：
`mysql:(none)>set persist password_reuse_interval = default;
Query OK, 0 rows affected (0.00 sec)
mysql:(none)>set persist password_history=default;
Query OK, 0 rows affected (0.00 sec)
`
管理员退出连接重新进入，创建两个用户 ytt_dev1 和 ytt_dba1 :
`mysql:(none)>create user ytt_dev1 identified by 'root123';
Query OK, 0 rows affected (0.04 sec)
mysql:(none)>create user ytt_dba1 identified by 'root123';
Query OK, 0 rows affected (0.02 sec)
`
更改两个用户的密码历史保留策略：
`mysql:(none)>alter user ytt_dev1 password history 3;
Query OK, 0 rows affected (0.01 sec)
mysql:(none)>alter user ytt_dba1 password reuse interval 7 day;
Query OK, 0 rows affected (0.02 sec)
`
检索 mysql.user 表，看看是否更改成功：
`mysql:(none)>select user,password_reuse_history,password_reuse_time from mysql.user where password_reuse_history is not null or password_reuse_time is not null;
+----------+------------------------+---------------------+
| user     | password_reuse_history | password_reuse_time |
+----------+------------------------+---------------------+
| ytt_dba1 |                   NULL |                   7 |
| ytt_dev1 |                      3 |                NULL |
+----------+------------------------+---------------------+
2 rows in set (0.00 sec)
`
具体验证方法类似全局参数设置部分，此处省略。
#### 总结：
MySQL 8.0 推出的历史密码验证策略是对用户密码安全机制的另外一个全新的改进，可以省去此类需求非数据侧的繁琐实现。