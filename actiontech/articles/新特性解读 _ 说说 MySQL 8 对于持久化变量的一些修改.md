# 新特性解读 | 说说 MySQL 8 对于持久化变量的一些修改

**原文链接**: https://opensource.actionsky.com/20200619-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-06-19T00:32:41-08:00

---

作者：姚嵩
爱可生南区交付服务部经理，爱好音乐，动漫，电影，游戏，人文，美食，旅游，还有其他。
虽然都很菜，但毕竟是爱好。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**MySQL 变量存在的介质及意义：**
MySQL 的变量存在于内存、以及配置文件中；
其中内存中的变量是在运行时生效，配置文件中的变量是在 mysqld 程序启动时加载到内存中；
**MySQL 8 版本以前为了保证修改后的变量的值在 MySQL 运行时及 MySQL 重启后生效，此时你需要分别修改内存和配置文件中变量的值：**
SET global/session 语句设置内存中全局/当前会话的变量的值，
通过 Linux 命令⼿⼯修改配置⽂件中变量的值，
此时你会发现，你的配置⽂件需要 通过 ps -ef | grep mysql 查看进程启动命令中带⼊的选项 &#8211;defaults-file，以确定配置⽂件，
如果启动命令没有带⼊选项 &#8211;defaults-file，那么默认配置⽂件为 /etc/my.cnf ；
你会发现修改配置⽂件时，需要确定配置⽂件，以及修改配置⽂件，这个步骤其实蛮繁琐的，
⽽且如果你⼀不小心写错了变量名或值，可能会直接导致启动 MySQL 失败，
如果此时 你有其他策略依赖 MySQL 的启动/重启，那么这个 MySQL 启动失败可能⼜会导致你策略判断不符合预期，造成其他不好的后果，
这可能是就是亚马逊飓风初始的那只蝴蝶的翅膀。
**MySQL 8 以后，对于持久化变量的值，有了其他方式：**
- SET PERSIST
语句可以修改内存中变量的值，并且将修改后的值写⼊数据⽬录中的 mysqld-auto.cnf 中。
- SET PERSIST_ONLY
语句不会修改内存中变量的值，只是将修改后的值写⼊数据⽬录中的 mysqld-auto.cnf 中。
**注意：**PERSIST 和 PERSIST_ONLY 设置的都是 Global 级别，不是 Session 级别；删除 mysqld-auto.cnf ⽂件 或设置 persisted_globals_load 为 off 都不会加载变量持久化的配置。通过语句 SET PERSIST / PERSIST_ONLY 去持久化变量的值到⽂件中，相较于直接修改配置⽂件⽽⾔，
使⽤语句修改的⽅式更安全，因为语句会校验变量&值的准确性，不会产⽣因为参数&值修改错误导致的 MySQL 启动失败的问题；因为 MySQL 启动期间，最后才读取 mysqld-auto.cnf ⽂件，也就是说 mysqld-auto.cnf ⽂件中的变量会覆盖配置⽂件中的变量的值，
所以你需要改正你的参数修改习惯，直接使⽤ SET PERSIST / PERSIST_ONLY 修改变量的值，
⽽不是⼿⼯修改配置⽂件，除⾮变量只能通过修改配置⽂件的⽅式修改；
**权限：**
- SET PERSIST
需要 system_variables_admin 权限
- SET PERSIST_ONLY
需要 system_variables_admin 和 persist_ro_variables_admin 权限
**权限补充说明：**
MySQL 安装完成后，root 账户是不存在 system_variables_admin、persist_ro_variables_admin 权限的；
但是 root 账户存在 WITH GRANT OPTION 权限，
所以 root 可以给自己/其他账户授予 system_variables_admin、persist_ro_variables_admin 权限；
GRANT system_variables_admin,persist_ro_variables_admin ON *.* TO user_name@&#8217;%&#8217; ;
**全局变量的修改会保存在两处：**
1. 数据⽬录下的 mysqld-auto.cnf持久化信息以 json 格式保存，metadata 记录了这次修改的用户及时间信息。文件中还区分了变量的类型：mysql_server（动态变量）和 mysql_server_static_options（只读变量）；在数据库启动时，会首先读取其他配置⽂件，最后才读取 mysqld-auto.cnf 文件。不建议⼿动修改 mysqld-auto.cnf ⽂件，其可能导致数据库在启动过程中因解析错误⽽失败。如果出现这种情况，可⼿动删除 mysqld-auto.cnf ⽂件或设置 persisted_globals_load 为 off 来避免该⽂件的加载。2. 表 performance_schema.persisted_variables
**常用语句：**
set persist max_connections=500 ;
# # persist 不仅修改了内存中的值，还会持久化到配置⽂件中
set @@persist.max_connections=500 ;
# 效果同上
set persist max_connections=default ;
# # 可以设置为变量为默认值
set persist_only back_log=500 ;
# # persist_only 只会将全局变量持久化到配置文件中，不会修改内存中的值
set @@persist_only.back_log=500 ;
# # 效果同上
set persist_only back_log=1000 ,persist max_connections=2000 ;
# # 同时设置多个变量的值
select * from performances_chema.persisted_variables ;
# # 查看已持久化的参数
reset persist back_log ;
# # 清除指定的已持久化的变量
reset persist if exists back_log ;
# # 清除指定的变量，如果变量没在持久化配置文件里，那么就会告警，而不是报错（幂等操作）
reset persist ;
# # 清除所有的已持久化的变量
**涉及****参数：**
persisted_globals_load = ON # 8.0.0 添加，默认是 ON，表示 MySQL 启动时，读取数据⽬录下的 mysqld-auto.cnf ⽂件中的变量，设置为 OFF 时，则不会读取文件中的变量；
**涉及文件：**
数据目录下的 mysqld-auto.cnf ⽂件，数据目录通过 select @@global.datadir；获取；
**举例：**
# # 查看 max_connections 的值
- `mysql> show variables like "max_connections";`
- `+-----------------+-------+`
- `| Variable_name | Value |`
- `+-----------------+-------+`
- `| max_connections | 200 |`
- `+-----------------+-------+`
- `1 row in set (0.00 sec)`
# # persist 不仅修改了内存中的值，还会持久化到 mysqld-auto.cnf ⽂件中
- `mysql> set persist max_connections=300 ;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> show variables like "max_connections";`
- `+-----------------+-------+`
- `| Variable_name | Value |`
- `+-----------------+-------+`
- `| max_connections | 300 |`
- `+-----------------+-------+`
- `1 row in set (0.00 sec)`
# # 把 max_connections 设置为默认值
- `mysql> set persist max_connections=default ;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> show variables like "max_connections";`
- `+-----------------+-------+`
- `| Variable_name | Value |`
- `+-----------------+-------+`
- `| max_connections | 151 |`
- `+-----------------+-------+`
- `1 row in set (0.01 sec)`
# # persist_only 只会将全局变量持久化到配置文件中，不会修改内存中的值
- `mysql> set persist_only max_connections=300 ;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> show variables like "max_connections";`
- `+-----------------+-------+`
- `| Variable_name | Value |`
- `+-----------------+-------+`
- `| max_connections | 151 |`
- `+-----------------+-------+`
- `1 row in set (0.00 sec)`
# # 查看已持久化的参数
- `mysql> select * from performance_schema.persisted_variables ;`
- `+-----------------+----------------+`
- `| VARIABLE_NAME | VARIABLE_VALUE |`
- `+-----------------+----------------+`
- `| max_connections | 300 |`
- `+-----------------+----------------+`
- `1 row in set (0.00 sec)`
# # 清除所有的已持久化的变量
- `mysql> reset persist ;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> select * from performance_schema.persisted_variables ;`
- `Empty set (0.00 sec)`
- `mysql> set session net_read_timeout=20;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> select @@global.net_read_timeout,@@session.net_read_timeout ;`
- `+---------------------------+----------------------------+`
- `| @@global.net_read_timeout | @@session.net_read_timeout |`
- `+---------------------------+----------------------------+`
- `| 30 | 20 |`
- `+---------------------------+----------------------------+`
- `1 row in set (0.00 sec)`
# # persist 只会设置变量的 global 值，不会设置变量的 session 值
- `mysql> set persist net_read_timeout=50 ;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> select @@global.net_read_timeout,@@session.net_read_timeout ;`
- `+---------------------------+----------------------------+`
- `| @@global.net_read_timeout | @@session.net_read_timeout |`
- `+---------------------------+----------------------------+`
- `| 50 | 20 |`
- `+---------------------------+----------------------------+`
- `1 row in set (0.00 sec)`
- `mysql> select * from performance_schema.persisted_variables ;`
- `+------------------+----------------+`
- `| VARIABLE_NAME | VARIABLE_VALUE |`
- `+------------------+----------------+`
- `| net_read_timeout | 50 |`
- `+------------------+----------------+`
- `1 row in set (0.00 sec)`
# # 你可以设置当前 session 的变量值为全局变量的值
- `mysql> set @@session.net_read_timeout=@@global.net_read_timeout ;`
- `Query OK, 0 rows affected (0.00 sec)`
- `mysql> select @@global.net_read_timeout,@@session.net_read_timeout ;`
- `+---------------------------+----------------------------+`
- `| @@global.net_read_timeout | @@session.net_read_timeout |`
- `+---------------------------+----------------------------+`
- `| 50 | 50 |`
- `+---------------------------+----------------------------+`
- `1 row in set (0.00 sec)`