# 技术分享 | 细说 MySQL 用户安全加固策略

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e7%bb%86%e8%af%b4-mysql-%e7%94%a8%e6%88%b7%e5%ae%89%e5%85%a8%e5%8a%a0%e5%9b%ba%e7%ad%96%e7%95%a5/
**分类**: MySQL 新特性
**发布时间**: 2023-12-20T00:05:09-08:00

---

这是一篇关于如何加强 MySQL 用户安全的文章，通读全文您可以了解密码复杂度策略、连接控制插件以及密码变更策略的相关知识。本文内容仅供参考，请在操作时以实际环境为准，避免造成经济损失。
> 
作者：余振兴，爱可生 DBA 团队成员，热衷技术分享、编写技术文档。
作者：官永强，爱可生 DBA 团队成员，擅长 MySQL 运维方面的技能。热爱学习新知识，亦是个爱打游戏的宅男。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 4000 字，预计阅读需要 10 分钟。
# 背景
基于安全的背景下，客户对 MySQL 的用户安全上提出了一系列需求，希望能对 MySQL 进行安全加固，具体的需求如下：
## 用户密码类
- 密码需要至少 25 个字符
密码必须包含至少 2 个大写字母
- 密码必须包含至少 2 个小写字母
- 密码必须包含至少 2 个数字
- 密码必须包含至少 2 个特殊字符
- 密码中不能包含用户名
- 密码不能是简单的重复字符（例如：AAA，wuwuwuwu, dsadsadsa, 111）
- 密码需要有过期时间，需要 365 天修改一次，否则过期并锁定用户
- 密码不得使用历史 5 次内曾用过的老密码
- 密码在 24 小时内最多只能修改一次
- 密码不能包含指定的字符，如公司名称、业务名称等
## 用户连接类
- 登录时如果连续 10 次失败，需要等待 10 分钟且每次失败持续增加等待时间
# 需求分析
基于背景描述我们可以把需求分为三大块：
- 密码复杂度策略
- 连接控制的策略
- 密码变更的策略
MySQL 有以下功能插件/组件、配置可实现以上需求：
- 密码校验插件/组件
- 连接控制插件
- 用户密码属性配置
## 环境信息
MySQL 版本：8.0.33、5.7.41
# 安装配置
## 1. 密码校验组件配置
MySQL 5.7 版本为密码校验插件，虽然安装方式和变量有语法有些许差异，但功能基本相同。以下操作仅以 MySQL 8.0 版本操作为例，具体细节可参考[官方文档](https://dev.mysql.com/doc/refman/8.0/en/validate-password.html)。
`## 8.0 版本安装密码校验组件
INSTALL COMPONENT 'file://component_validate_password';
## 查看插件默认配置
show variables like 'validate_password%';
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |    ## 密码不能包含用户名
| validate_password.dictionary_file    |        |    ## 指定密码匹配字典文件，在文件中的字符串不能包含在设置的密码中，在 policy 为 STRONG 时有效
| validate_password.length             | 8      |    ## 密码最小长度，默认至少 8 位长
| validate_password.mixed_case_count   | 1      |    ## 密码至少包含 1 个大小写字母
| validate_password.number_count       | 1      |    ## 密码至少包含一个数字
| validate_password.policy             | MEDIUM |    ## 密码默认复杂度策略
| validate_password.special_char_count | 1      |    ## 密码至少包含一个特殊字符
+--------------------------------------+--------+
7 rows in set (0.0042 sec)
## 修改配置以便符合背景需求
set global validate_password.length=25;
set global validate_password.mixed_case_count=2;
set global validate_password.number_count=2;
set global validate_password.special_char_count=2;
## 查看调整后的配置（动态生效）
show variables like 'validate_password%';
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |
| validate_password.dictionary_file    |        |
| validate_password.length             | 25     |
| validate_password.mixed_case_count   | 2      |
| validate_password.number_count       | 2      |
| validate_password.policy             | MEDIUM |
| validate_password.special_char_count | 2      |
+--------------------------------------+--------+
7 rows in set (0.0056 sec)
## 持久化配置到 my.cnf 配置文件（永久生效）
## 在 [mysqld] 标签下增加配置
vim /data/mysql/3306/my.cnf.3306 
[mysqld]
## 密码校验组件参数配置
validate_password.check_user_name     = ON
validate_password.policy              = MEDIUM
validate_password.length              = 25
validate_password.mixed_case_count    = 2
validate_password.number_count        = 2
validate_password.special_char_count  = 2
`
## 2. 连接控制插件配置
连接控制插件在 MySQL 5.7 和 MySQL 8.0 基本无变化，均以插件形式提供。以下操作仅以 MySQL 8.0 版本操作为例，具体细节可参考[官方文档](https://dev.mysql.com/doc/refman/8.0/en/connection-control.html)。
`## 连接控制插件安装
INSTALL PLUGIN CONNECTION_CONTROL SONAME 'connection_control.so';
INSTALL PLUGIN CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS SONAME 'connection_control.so';
## 查看插件默认配置
show variables like 'connection_control%';
+-------------------------------------------------+------------+
| Variable_name                                   | Value      |
+-------------------------------------------------+------------+
| connection_control_failed_connections_threshold | 3          | ## 运行登录失败尝试的次数，默认为 3，表示当连接失败 3 次后启用连接控制，0 表示不开启
| connection_control_max_connection_delay         | 2147483647 | ## 响应延迟的最大时间，默认约25天
| connection_control_min_connection_delay         | 1000       | ## 登录失败后响应延迟的最小时间，默认 1000 毫秒，1 秒，每失败一次逐步累加，直到最大值
+-------------------------------------------------+------------+
## 修改配置以便符合背景需求,响应延迟的最大时间设置为 1 天
set global connection_control_max_connection_delay=24*60*60*1000;
## 查看调整后的配置（动态生效）
show variables like 'connection_control%';
+-------------------------------------------------+-------+
| Variable_name                                   | Value |
+-------------------------------------------------+-------+
| connection_control_failed_connections_threshold | 3     |
| connection_control_max_connection_delay         | 86400000 | ## 调整为最大一天
| connection_control_min_connection_delay         | 1000  |
+-------------------------------------------------+-------+
## 持久化配置到 my.cnf 配置文件（永久生效）
## 在 [mysqld] 标签下增加配置
vim /data/mysql/3306/my.cnf.3306 
[mysqld]
## 连接控制插件配置
connection-control                                     = FORCE
connection-control-failed-login-attempts               = FORCE
connection_control_min_connection_delay                = 1000
connection_control_max_connection_delay                = 86400000
connection_control_failed_connections_threshold        = 3
`
## 3. 密码变更策略配置
MySQL 密码变更策略配置记录在 `mysql.user` 表中，5.7 和 8.0 版本支持的配置略有差异，具体细节可参考官方文档中 `CREATE USER` 和 `ALTER USER` 语法中 `password_option` 部分[属性说明](https://dev.mysql.com/doc/refman/8.0/en/create-user.html)。
### 相关配置参数含义说明
#### MySQL 5.7 版本下仅支持：
*default_password_lifetime*
：密码有效期（默认为 0 或 NULL），表示密码永久有效。
> 
注意：线上环境配置密码过期策略虽然可提升安全性，但如果没及时更新密码会导致业务中断问题，需要综合评估后配置！
#### MySQL 8.0 版本支持：
*default_password_lifetime*：密码有效期（默认为 0 或 NULL），表示密码永久有效。
> 
注意：线上环境配置密码过期策略虽然可提升安全性，但如果没及时更新密码会导致业务中断问题，需要综合评估后配置！
*password_history*：历史密码可重用的循环，表示记录历史上前多少次密码不允许被重复使用，历史密码信息记录在 `mysql.password_history` 表中。
*password_reuse_interval*：指定历史密码要经过多长时间才能被重用，单位为天。
> 
关于 `default_password_lifetime、password_history` 以及 `password_reuse_interval` 在 my.cnf 配置后，创建用户默认属性不生效的问题，提了 MySQL [Bug](https://bugs.mysql.com/bug.php?id=112128)，待官方反馈是否符合预期。
**结论：不是 Bug，对参数的理解有误。** 
以密码过期配置为示例说明，`password_reuse_interval`、`password_history` 均为相同逻辑。
- ALTER USER eee PASSWORD EXPIRE;
eee 用户密码立即过期，mysql.user 表中 password_expired 字段标记为 Y
- ALTER USER eee PASSWORD EXPIRE DEFAULT;
eee 用户密码过期策略采用全局参数 default_password_lifetime 指定的值作为过期策略，mysql.user 表中的 password_lifetime 字段为 NULL
- ALTER USER eee PASSWORD EXPIRE NEVER;
eee 用户密码过期策略设置为永不过期，mysql.user 表中的 password_lifetime 字段值为 0
- ALTER USER eee PASSWORD EXPIRE INTERVAL 3 DAY;
eee 用户密码过期策略设置为指定 3 天后过期，mysql.user 表中的 password_lifetime 字段值为 3
![点击放大](.img/4485ba89.png)
> 
关于 `password_history` 和 `password_reuse_interval` 参数同时使用时，实际只有 `password_reuse_interval` 参数有效的问题，提了 MySQL [Bug](https://bugs.mysql.com/bug.php?id=112132)，待官方反馈是否符合预期。
`################## 以5.7版本为例 ##################
## 1. 修改当前默认密码策略为需求所需配置(动态生效）
set global default_password_lifetime=365;
## 2. 查看当前密码有效期配置。这里一定注意，表中的password_lifetime为NULL不是表示无策略，而是表示使用default_password_lifetime参数指定的全局策略
select user,host,password_lifetime from mysql.user where user not in  ('mysql.session','mysql.sys');
+----------+-----------+-------------------+
| user     | host      | password_lifetime |
+----------+-----------+-------------------+
| root     | localhost |              NULL |
| zhenxing | %         |              NULL |
| sysbench | %         |              NULL |
| aaa      | %         |              NULL |
| bbb      | %         |              NULL |
+----------+-----------+-------------------+
## 3. 持久化当前默认密码策略为需求所需配置（永久生效）
## 在[mysqld]标签下增加配置
vim /data/mysql/3306/my.cnf.3306 
[mysqld]
## 密码策略配置
default_password_lifetime = 365
################## 以8.0版本为例 ##################
## 1. 修改当前默认密码策略为需求所需配置(动态生效）
set global default_password_lifetime=365;
set global password_history=5;
set global password_reuse_interval=1;
## 2. 查看当前已存在用户的密码策略配置（默认均为NULL，表示使用default_password_lifetime、password_history、password_reuse_interval参数指定的全局策略）
select user,host,password_lifetime,Password_reuse_history,Password_reuse_time from mysql.user where user not in ('mysql.infoschema','mysql.session','mysql.sys');
+----------+-----------+-------------------+------------------------+---------------------+
| user     | host      | password_lifetime | Password_reuse_history | Password_reuse_time |
+----------+-----------+-------------------+------------------------+---------------------+
| aaa      | %         |              NULL |                   NULL |                NULL |
| sysbench | %         |              NULL |                   NULL |                NULL |
| zhenxing | %         |              NULL |                   NULL |                NULL |
| backup   | 127.0.0.1 |              NULL |                   NULL |                NULL |
| backup   | localhost |              NULL |                   NULL |                NULL |
| root     | localhost |              NULL |                   NULL |                NULL |
+----------+-----------+-------------------+------------------------+---------------------
## 3. 持久化当前默认密码策略为需求所需配置（永久生效）
## 在[mysqld]标签下增加配置
vim /data/mysql/3306/my.cnf.3306 
[mysqld]
## 密码策略配置
default_password_lifetime = 365
password_history          = 5
password_reuse_interval   = 1
`
# 功能验证
## 1. 密码校验组件
MySQL 5.7 版本为密码校验插件，安装方式和变量有语法差异，功能基本相同，以下操作仅以 5.7 版本操作为例。
`################## 以5.7版本为例 ##################
##1.查看当前密码校验插件配置信息
mysql> show variables like 'validate%';
+--------------------------------------+-----------------------+
| Variable_name                        | Value                 |
+--------------------------------------+-----------------------+
| validate_password_check_user_name    | ON                    |
| validate_password_dictionary_file    | /usr/share/dict/words |
| validate_password_length             | 25                    |
| validate_password_mixed_case_count   | 2                     |
| validate_password_number_count       | 2                     |
| validate_password_policy             | STRONG                |
| validate_password_special_char_count | 2                     |
+--------------------------------------+-----------------------+
7 rows in set (0.00 sec)
## 2. 进行验证
## 2.1 验证密码不符合 validate_password_mixed_case_count≥2 时，是否可以成功新建用户
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'1234567890@#$tyuiopasdfg';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
## 2.2 验证密码不符合 validate_password_number_count≥2 时，是否可以成功新建用户
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'qazwsxEDCRFVtgb%$#ujmnbgf';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
## 2.3 验证密码不符合 validate_password_special_char_count≥2 时，是否可以成功新建用户
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'1qazWSXEDCdsa321321321dsadwq';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
## 2.4 验证密码不符合 validate_password_length≥25 时，是否可以成功新建用户
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'123!@#qazWWSX';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
## 2.5 关闭大小写字母数量验证功能，验证使用的密码记录在密码字典中时（2167sags$er24sfwjdtegcfaskvc），是否可以成功新建用户
[root@10-186-60-13 dict]# cat words 
12!@qwqw
12qw!@qw
2167sags$er24sfwjdtegcfaskvc
mysql> set global validate_password_mixed_case_count=0;
Query OK, 0 rows affected (0.00 sec)
mysql> show variables like 'validate%';
+--------------------------------------+-----------------------+
| Variable_name                        | Value                 |
+--------------------------------------+-----------------------+
| validate_password_check_user_name    | ON                    |
| validate_password_dictionary_file    | /usr/share/dict/words |
| validate_password_length             | 25                    |
| validate_password_mixed_case_count   | 0                     |
| validate_password_number_count       | 2                     |
| validate_password_policy             | STRONG                |
| validate_password_special_char_count | 2                     |
+--------------------------------------+-----------------------+
7 rows in set (0.00 sec)
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'2167sags$er24sfwjdtegcfaskvc';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
mysql> set global validate_password_mixed_case_count=2;
Query OK, 0 rows affected (0.00 sec)
mysql> show variables like 'validate%';
+--------------------------------------+-----------------------+
| Variable_name                        | Value                 |
+--------------------------------------+-----------------------+
| validate_password_check_user_name    | ON                    |
| validate_password_dictionary_file    | /usr/share/dict/words |
| validate_password_length             | 25                    |
| validate_password_mixed_case_count   | 2                     |
| validate_password_number_count       | 2                     |
| validate_password_policy             | STRONG                |
| validate_password_special_char_count | 2                     |
+--------------------------------------+-----------------------+
7 rows in set (0.00 sec)
`
## 2. 连接控制插件
MySQL 5.7 版本为连接控制插件，功能基本相同，以下操作仅以 5.7 版本操作为例。
`################## 以5.7版本为例 ##################
## 1. 查看当前连接插件配置信息
mysql> show variables like 'connection_control%';
+-------------------------------------------------+-------+
| Variable_name                                   | Value |
+-------------------------------------------------+-------+
| connection_control_failed_connections_threshold | 3     |
| connection_control_max_connection_delay         | 86400 |
| connection_control_min_connection_delay         | 1000  |
+-------------------------------------------------+-------+
3 rows in set (0.00 sec)
## 2. 新建测试用户后，尝试三次连接失败，观察等待时间，观察到等待反馈登录失败的时间会越来越长
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'1qaz@WSX#EDC4rfv5tgb6yhnZVAF';
Query OK, 0 rows affected (0.00 sec)
mysql> ^DBye
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p -S /opt/mysql/data/3306/mysqld.sock
Enter password: 
ERROR 1045 (28000): Access denied for user 'test33'@'localhost' (using password: YES)
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p -S /opt/mysql/data/3306/mysqld.sock
Enter password: 
ERROR 1045 (28000): Access denied for user 'test33'@'localhost' (using password: YES)
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p -S /opt/mysql/data/3306/mysqld.sock
Enter password: 
ERROR 1045 (28000): Access denied for user 'test33'@'localhost' (using password: YES)
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p -S /opt/mysql/data/3306/mysqld.sock
Enter password: 
ERROR 1045 (28000): Access denied for user 'test33'@'localhost' (using password: YES)
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p -S /opt/mysql/data/3306/mysqld.sock
Enter password: 
ERROR 1045 (28000): Access denied for user 'test33'@'localhost' (using password: YES)
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p -S /opt/mysql/data/3306/mysqld.sock
Enter password:
`
## 3. 密码变更策略
MySQL 密码变更策略配置记录在 `mysql.user` 表中，5.7 和 8.0 版本支持的配置略有差异，以下将展示两个版本的测试过程和测试结果。
`################## 以5.7版本为例 ##################
## 1. 检查当前密码变更策略相关信息
mysql> select @@default_password_lifetime\G
*************************** 1. row ***************************
@@default_password_lifetime: 365
1 row in set (0.00 sec)
## 2. 新建 test33 用户，设置其密码过期时间为一天，修改机器时间重启再使用该用户进行登录操作，观察到提示密码过期
mysql> CREATE USER 'test33'@'%'
-> IDENTIFIED WITH 'mysql_native_password' 
-> BY
-> '1qaz@WSX#EDC4rfv5tgb6yhnZVAF'
-> REQUIRE NONE 
-> PASSWORD EXPIRE INTERVAL 1 DAY;
Query OK, 0 rows affected (0.00 sec)
mysql> select user,host,password_lifetime from mysql.user where host!='localhost' and user not in ('mysql.infoschema','mysql.session','mysql.sys');
+-------------+-----------+-------------------+
| user        | host      | password_lifetime |
+-------------+-----------+-------------------+
| root        | 127.0.0.1 |              NULL |
| universe_op | %         |              NULL |
| test4       | %         |              NULL |
| tt          | %         |              NULL |
| test33      | %         |                 1 |
+-------------+-----------+-------------------+
5 rows in set (0.00 sec)
[root@10-186-60-13 dict]# date
Tue Aug 22 16:53:22 CST 2023
[root@10-186-60-13 dict]# timedatectl set-time '2023-8-23 16:53:20'
[root@10-186-60-13 dict]# date
Wed Aug 23 16:53:20 CST 2023
[root@10-186-60-13 ~]# /opt/mysql/base/5.7.25/bin/mysql -utest33 -p1qaz@WSX#EDC4rfv5tgb6yhnZVAF -S /opt/mysql/data/3306/mysqld.sock
mysql> select now();
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
################## 以8.0版本为例 ##################
##1.检查当前密码变更策略相关信息
mysql> select @@default_password_lifetime,@@password_history,@@password_reuse_interval,@@password_require_current\G
*************************** 1. row ***************************
@@default_password_lifetime: 365
@@password_history: 5
@@password_reuse_interval: 1
@@password_require_current: 1
1 row in set (0.00 sec)
## 2. 进行验证
## 2.1 密码过期验证参考 5.7 此处不再赘述
## 2.2 新建 test33 用户，并进行密码修改，测试当使用近 5 次密码时，是否能修改密码成功
mysql> create user test33@'%' identified WITH 'mysql_native_password' by'1qaz@WSX#EDC4rfv5tgb6yhnZVAF';
mysql> alter user test33@'%' identified WITH 'mysql_native_password' by'1qaz@WSX#EDC4rfv5tgb6yhnZVAF';
ERROR 3638 (HY000): Cannot use these credentials for 'test33@%' because they contradict the password history policy
mysql> alter user test33@'%' identified WITH 'mysql_native_password' by'1qaz@WSX#EDC4rfv5tgb6yhnZVAG';
Query OK, 0 rows affected (0.00 sec)
mysql> alter user test33@'%' identified WITH 'mysql_native_password' by'1qaz@WSX#EDC4rfv5tgb6yhnZVAF';
ERROR 3638 (HY000): Cannot use these credentials for 'test33@%' because they contradict the password history policy
`
# 知识补充
关于 `validate_password.dictionary_file` 的配置说明。
`validate_password.dictionary_file` 参数指定的密码字典文件采用以下逻辑：
- 该文件**最大为 1M**，一行作为一个字符串
- 该文件仅在 `validate_password.policy` 参数设置为 2 或者 STRONG 时生效 
- 每行至少 4 位长，最多 100 位长，低于或高于长度均不生效
- 该文件中英文字母必须均为小写，但**匹配密码时会忽略大小写**
- 对文件中每行字符采用**模糊匹配**，也就是密码中不允许出现这串字符串，如，文件中一行为 zhenxing，则适配规则如下：
```
-- 密码字段文件内容
cat /data/mysql/3306/tmp/password_list.txt
zhenxing
create user demo identified by 'aaBB11__zhenxing';   -- 不支持，包含完整的 zhenxing 字符串
create user demo identified by 'aaBB1zhenxing1__';   -- 不支持，包含完整的 zhenxing 字符串
create user demo identified by 'zhenxingaaBB11__';   -- 不支持，包含完整的 zhenxing 字符串
create user demo identified by 'aaBB1zhen00xing1__';  -- 支持，
```
- 对该文件新增或删除数据都需要重新配置才可动态生效，如：先调整为默认值再重新设置为指定文件值。
`set global validate_password.dictionary_file=default;`
- `set global validate_password.dictionary_file='/data/mysql/3306/tmp/password_list.txt';`
- 可以观测 `show global status like 'validate_password.dictionary_file%';` 的输出查看文件最新生效时间
- 该文件主要功能实际类似背景需求中的场景：【密码不能包含指定的字符，如公司名称、业务名称等】，可以将公司名称、业务名称等在该文件中配置
# 总结
- 在使用以上功能前需确定不同 MySQL 版本支持度
- MySQL 5.7 版本上的部分插件到 MySQL 8.0 后调整为了组件，使用时需注意语法和参数名称的变化
- MySQL 8.0 版本对密码进行了更精细化的配置，如增加了 `password_history`、`password_reuse_interval` 等配置
- 在对 MySQL 配置 `default_password_lifetime` 时需要注意对业务的影响，防止密码过期导致业务中断的风险
- 连接控制插件的使用需要注意避免大量错误异常导致账号连接等待时间拉长，具体是否启用也需结合业务场景和安全性综合判断
## 需求中未实现的功能
- 密码在 24 小时内最多只能修改一次
- 密码不能是简单的重复字符（例如：AAA，wuwuwuwu, dsadsadsa, 111）