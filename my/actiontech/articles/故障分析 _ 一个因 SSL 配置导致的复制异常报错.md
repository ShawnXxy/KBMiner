# 故障分析 | 一个因 SSL 配置导致的复制异常报错

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-%e4%b8%80%e4%b8%aa%e5%9b%a0-ssl-%e9%85%8d%e7%bd%ae%e5%af%bc%e8%87%b4%e7%9a%84%e5%a4%8d%e5%88%b6%e5%bc%82%e5%b8%b8%e6%8a%a5%e9%94%99/
**分类**: 技术干货
**发布时间**: 2023-06-08T01:16:34-08:00

---

在构建 MySQL 复制过程中，IO 线程始终连接不上主库，反复确认复制账号的权限、账号密码都没问题，最终定位为 SSL 配置的问题。
> 作者：木板。某全国性股份制银行 DBA。擅长 DB2，MySQL 和 Oracle 数据库的运行维护和调优、排错。
本文来源：原创投稿
- 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# 故障背景
> 在做 MySQL 同构的数据迁移过程中，我们通常只需要按流程搭建主从保持数据同步即可。一般构建复制只要网络没问题，基本都能顺利构建成功。而这次踩了一个小坑，记录一下。
同事反馈做完 `change master` 后，IO 线程始终显示连接不上主库，已经反复确认该复制账号的权限、账号密码都没问题，且也验证了通过 MySQL 客户端的命令行输入相同的账号密码能正常连接到主库，已经做了以下场景的排除工作：
- 排除了账号密码错误的问题
- 排除了账号权限不足的问题
- 排除了网络不通的问题
# 故障分析
- 通过源端主库的错误日志也能持续观测到该复制用户频繁的尝试连接但都失败,错误日志的报错仅告知用了密码但访问受限，比较常规的报错信息。
2021-06-07T16:56:54.812721+08:00 121 [ERROR] [MY-010584] [Repl] Slave I/O for channel '': error connecting to master 'repl@10.186.61.27:3310' - retry-time: 60 retries: 1 message: Access denied for user 'repl'@'10.186.61.27' (using password: YES), Error_code: MY-001045
2021-06-07T16:57:54.817711+08:00 121 [ERROR] [MY-010584] [Repl] Slave I/O for channel '': error connecting to master 'repl@10.186.61.27:3310' - retry-time: 60 retries: 2 message: Access denied for user 'repl'@'10.186.61.27' (using password: YES), Error_code: MY-001045
通过 `mysql.user` 表观测复制用户的权限细节，观测到该用户有一个特殊的属性设置，`ssl_type=ANY` 该设置引起了注意。基于官方文档得知，该选项是用来控制用户是否开启 SSL 方式登录。如果为 `ANY` 则表示用该用户连接时，必须使用 SSL 方式，否则无法登录。
> MySQL 客户端在 5.7 以后默认就开启 SSL，所以正常情况下无需明确指定即是 SSL 方式。
10.186.61.27:3310  SQL > select user,host,ssl_type from mysql.user;
+------------------+-----------+----------+
| user             | host      | ssl_type |
+------------------+-----------+----------+
| repl             | %         | ANY      |
| root             | %         |          |
| zhenxing         | %         |          |
| sysbench         | 10.186.%  |          |
| mysql.infoschema | localhost |          |
| mysql.session    | localhost |          |
| mysql.sys        | localhost |          |
| root             | localhost |          |
+------------------+-----------+----------+
CHANGE MASTER TO
MASTER_HOST='10.186.61.27',
MASTER_USER='repl',
MASTER_PASSWORD='xxxx',
MASTER_PORT=3310,
MASTER_AUTO_POSITION=1;
Last_IO_Errno: 1045
Last_IO_Error: error connecting to master 'repl@10.186.61.27:3310' - retry-time: 60 retries: 1 message: Access denied for user 'repl'@'10.186.61.27' (using password: YES)
# 问题复现
尝试复现验证是否为该属性导致，在用 MySQL 登录数据库时明确的关闭 SSL 尝试 `mysql --ssl-mode=disable`，结果如预期的一样，报错无法连接，但并没有报错是因为 SSL 的原因。
[root@10-186-61-27 ~]# mysql -h10.186.61.27 -urepl -p -P3310
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 29
Server version: 8.0.22-commercial MySQL Enterprise Server - Commercial
Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
repl@10.186.61.27[(none)]>
-- --ssl-mode=disable
[root@10-186-61-27 ~]# mysql -h10.186.61.27 -urepl -p -P3310 --ssl-mode=disable ERROR 1045 (28000): Access denied for user 'repl'@'10.186.61.27' (using password: YES) 
# 问题总结
- 默认情况下，复制构建是不使用 SSL 的，除非明确的指定 SSL 相关的参数。具体配置方式可参考[官方文档](https://dev.mysql.com/doc/refman/8.0/en/replication-encrypted-connections.html)。
- 用户连接异常的情况，不仅涉及权限、密码等问题，对于用户的连接控制属性也需要进行观测，如 `mysql.user` 表的以下字段 ： ssl_type
- max_questions
- max_updates
- max_connections
- max_user_connections
- plugin
- password_expired
- password_lifetime
- account_locked
- 1045 `ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)` 常见报错场景： 用户名不正确
- 数据库用户受到连接主机限制，当前主机不允许连接
- 密码错误密码填写错误
- 当密码出现在 Shell 脚本中，并且包含特殊字符如 `$`，`#`，`!` 等时
- 当密码出现在配置文件中，并且包含特殊字符 `#` 时，需要用双引号将密码括起来
- 开启了 SSL 连接属性
- DNS 服务器解析主机名异常
- 指定的数据库 IP 错误
- 使用了外部的认证方式，（如 AD、PAM、LDAP 等），但配置不正确
# 解决办法
- 关闭该用户强制需要 SSL 连接的属性 `alter user xxx REQUIRE NONE;`
- `change master` 操作时，明确指定 `MASTER_SSL` 等 SSL 参数配置
CHANGE MASTER TO
MASTER_HOST='10.186.61.27',
MASTER_USER='repl',
MASTER_PASSWORD='xxxx',
MASTER_PORT=3310,
MASTER_AUTO_POSITION=1,
MASTER_SSL=1;