# 技术分享 | 可能是目前最全的 MySQL 8.0 新特性解读(上)

**原文链接**: https://opensource.actionsky.com/20230321-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-03-20T22:37:34-08:00

---

作者：马文斌
MySQL爱好者,任职于蓝月亮(中国)有限公司。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一、功能增强
##### 1.1-所有系统表更换为InnoDB引擎
系统表全部换成事务型的innodb表，默认的MySQL实例将不包含任何MyISAM表，除非手动创建MyISAM表。
##### 1.2-DDL原子化
InnoDB表的DDL支持事务完整性，要么成功要么回滚，将DDL操作回滚日志写入到data dictionary 数据字典表 mysql.innodb_ddl_log 中用于回滚操作，该表是隐藏的表，通过show tables无法看到。通过设置参数，可将ddl操作日志打印输出到mysql错误日志中。
mysql> set global log_error_verbosity=3;
mysql> set global innodb_print_ddl_logs=1;
##### 1.3-DDL秒加列
只有在 MySQL 8.0.12 以上的版本才支持
mysql> show create table sbtest1;
CREATE TABLE `sbtest1` (
`id` int NOT NULL AUTO_INCREMENT,
`k` int NOT NULL DEFAULT '0',
`c` char(120) NOT NULL DEFAULT '',
`pad` char(60) NOT NULL DEFAULT '',
`d` int NOT NULL DEFAULT '0',
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci 
1 row in set (0.00 sec)
mysql> alter table sbtest1 drop column d ;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> 
mysql> insert into sbtest1(k,c,pad) select k,c,pad from sbtest1;
Query OK, 1000000 rows affected (19.61 sec)
Records: 1000000  Duplicates: 0  Warnings: 0
mysql> insert into sbtest1(k,c,pad) select k,c,pad from sbtest1;
Query OK, 2000000 rows affected (38.25 sec)
Records: 2000000  Duplicates: 0  Warnings: 0
mysql> insert into sbtest1(k,c,pad) select k,c,pad from sbtest1;
Query OK, 4000000 rows affected (1 min 14.51 sec)
Records: 4000000  Duplicates: 0  Warnings: 0
mysql> select count(*) from sbtest1;
+----------+
| count(*) |
+----------+
|  8000000 |
+----------+
1 row in set (0.31 sec)
mysql> alter table sbtest1 add column d int not null default 0;
Query OK, 0 rows affected (1.22 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> alter table sbtest1 add column e int not null default 0;
Query OK, 0 rows affected (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 0
##### 1.4-公用表表达式（CTE：Common Table Expression）
CTE(Common Table Expression)可以认为是派生表(derived table)的替代，在一定程度上，CTE简化了复杂的join查询和子查询，另外CTE可以很方便地实现递归查询，提高了SQL的可读性和执行性能。CTE是ANSI SQL 99标准的一部分，在MySQL 8.0.1版本被引入。
##### 1.4.1-CTE优势
- 查询语句的可读性更好
- 在一个查询中，可以被引用多次
- 能够链接多个CTE
- 能够创建递归查询
- 能够提高SQL执行性能
- 能够有效地替代视图
##### 1.5-默认字符集由latin1变为utf8mb4
在8.0版本之前，默认字符集为latin1，utf8指向的是utf8mb3，8.0版本默认字符集为utf8mb4，utf8默认指向的也是utf8mb4。
##### 1.6-Clone插件
MySQL 8.0 clone插件提供从一个实例克隆出另外一个实例的功能，克隆功能提供了更有效的方式来快速创建MySQL实例，搭建主从复制和组复制。
##### 1.7-资源组
MySQL 8.0新增了一个资源组功能，用于调控线程优先级以及绑定CPU核。MySQL用户需要有 RESOURCE_GROUP_ADMIN权限才能创建、修改、删除资源组。在Linux环境下，MySQL进程需要有 CAP_SYS_NICE 权限才能使用资源组完整功能。
##### 1.8-角色管理
角色可以认为是一些权限的集合，为用户赋予统一的角色，权限的修改直接通过角色来进行，无需为每个用户单独授权。
# 创建角色
mysql>create role role_test;
QueryOK, 0rows affected (0.03sec)
# 给角色授予权限
mysql>grant select on db.*to 'role_test';
QueryOK, 0rows affected (0.10sec)
# 创建用户
mysql>create user 'read_user'@'%'identified by '123456';
QueryOK, 0rows affected (0.09sec)
# 给用户赋予角色
mysql>grant 'role_test'to 'read_user'@'%';
QueryOK, 0rows affected (0.02sec)
# 给角色role_test增加insert权限
mysql>grant insert on db.*to 'role_test';
QueryOK, 0rows affected (0.08sec)
# 给角色role_test删除insert权限
mysql>revoke insert on db.*from 'role_test';
QueryOK, 0rows affected (0.10sec)
# 查看默认角色信息
mysql>select * from mysql.default_roles;
# 查看角色与用户关系
mysql>select * from mysql.role_edges;
# 删除角色
mysql>drop role role_test;
##### 1.9-多值索引
从 MySQL 8.0.17 开始，InnoDB 支持创建多值索引，这是在存储值数组的 JSON 列上定义的二级索引，单个数据记录可以有多个索引记录。这样的索引使用关键部分定义，例如 CAST(data->’$.zipcode’ AS UNSIGNED ARRAY)。 MySQL 优化器自动使用多值索引来进行合适的查询，可以在 EXPLAIN 的输出中查看。
##### 1.10-函数索引
MySQL 8.0.13 以及更高版本支持函数索引（functional key parts），也就是将表达式的值作为索引的内容，而不是列值或列值前缀。 将函数作为索引键可以用于索引那些没有在表中直接存储的内容。
其实MySQL5.7中推出了虚拟列的功能，而MySQL8.0的函数索引也是依据虚拟列来实现的。
- 只有那些能够用于计算列的函数才能够用于创建函数索引。
- 函数索引中不允许使用子查询、参数、变量、存储函数以及自定义函数。
- SPATIAL 索引和 FULLTEXT 索引不支持函数索引。
##### 1.11-不可见索引
在MySQL 5.7版本及之前，只能通过显式的方式删除索引。此时，如果发现删除索引后出现错误，又只能通过显式创建索引的方式将删除的索引创建回来。如果数据表中的数据量非常大，或者数据表本身比较大，这种操作就会消耗系统过多的资源，操作成本非常高。
从MySQL 8.x开始支持隐藏索引（invisible indexes），只需要将待删除的索引设置为隐藏索引，使查询优化器不再使用这个索引（即使使用force index（强制使用索引），优化器也不会使用该索引）， 确认将索引设置为隐藏索引后系统不受任何响应，就可以彻底删除索引。 这种通过先将索引设置为隐藏索引，再删除索引的方式就是软删除 。
mysql> show create table t1\G
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`c1` int DEFAULT NULL,
`c2` int DEFAULT NULL,
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
KEY `idx_c1` (`c1`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
# 不可见的情况下是不会走索引的，key=null
mysql> explain select * from t1 where c1=3;
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    5 |    20.00 | Using where |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)
# 设置为索引可见，
mysql> alter table t1 alter index idx_c1 visible;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> show create table t1\G
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`c1` int DEFAULT NULL,
`c2` int DEFAULT NULL,
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
KEY `idx_c1` (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
# 可以走索引，key=idx_c1
mysql> explain select * from t1 where c1=3;
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
| id | select_type | table | partitions | type | possible_keys | key    | key_len | ref   | rows | filtered | Extra |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | t1    | NULL       | ref  | idx_c1        | idx_c1 | 5       | const |    1 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
1 row in set, 1 warning (0.00 sec)
##### 1.12-新增降序索引
MySQL在语法上很早就已经支持降序索引，但实际上创建的仍然是升序索引。从8.0开始，实际创建的为降序索引。
##### 1.13-SET_VAR 语法
在sql语法中增加SET_VAR语法，动态调整部分参数，有利于提升语句性能。
select /*+ SET_VAR(sort_buffer_size = 16M) */ id from test order id ;
insert /*+ SET_VAR(foreign_key_checks=OFF) */ into test(name) values(1);
##### 1.14-参数修改持久化
MySQL 8.0版本支持在线修改全局参数并持久化，通过加上PERSIST关键字，可以将修改的参数持久化到新的配置文件（mysqld-auto.cnf）中，重启MySQL时，可以从该配置文件获取到最新的配置参数。
例如执行：
set PERSIST expire_logs_days=10 ;
系统会在数据目录下生成一个包含json格式的 mysqld-auto.cnf 的文件，格式化后如下所示，当 my.cnf 和 mysqld-auto.cnf 同时存在时，后者具有更高优先级。
##### 1.15-innodb select for update跳过锁等待
select … for update，select … for share(8.0新增语法) 添加 NOWAIT、SKIP LOCKED语法，跳过锁等待，或者跳过锁定。
在5.7及之前的版本，select…for update，如果获取不到锁，会一直等待，直到innodb_lock_wait_timeout超时。
在8.0版本，通过添加nowait，skip locked语法，能够立即返回。如果查询的行已经加锁，那么nowait会立即报错返回，而skip locked也会立即返回，只是返回的结果中不包含被锁定的行。
##### 1.16-group by 不再隐式排序
目的是为了兼容sql的标准语法，方便迁移
mysql 5.7
mysql> select count(*),age from t5 group by age;
+----------+------+
| count(*) | age  |
+----------+------+
|        1 |   25 |
|        1 |   29 |
|        1 |   32 |
|        1 |   33 |
|        1 |   35 |
+----------+------+
5 rows in set (0.00 sec)
mysql 8.0
mysql> select count(*),age from t5 group by age;
+----------+------+
| count(*) | age  |
+----------+------+
|        1 |   25 |
|        1 |   32 |
|        1 |   35 |
|        1 |   29 |
|        1 |   33 |
+----------+------+
5 rows in set (0.00 sec)
可以看到，MySQL5.7 在group by中对分组字段进行了隐式排序，而MySQL8.0取消了隐式排序。如果要添加排序的话，需要显示增加，比如 select count(*),age from t5 group by age order by age;
##### 1.17-自增变量持久化
在8.0之前的版本，自增值是保存在内存中,自增主键AUTO_INCREMENT的值如果大于max(primary key)+1，在MySQL重启后，会重置AUTO_INCREMENT=max(primary key)+1。这种现象在某些情况下会导致业务主键冲突或者其他难以发现的问题。自增主键重启重置的问题很早就被发现(https://bugs.mysql.com/bug.php?id=199)，一直到8.0才被解决。8.0版本将会对AUTO_INCREMENT值进行持久化，MySQL重启后，该值将不会改变。
8.0开始，当前最大的自增计数器每当发生变化，值会被写入redo log中，并在每个检查点时候保存到private system table中。这一变化，对AUTO_INCREMENT值进行持久化,MySQL重启后，该值将不会改变。
- MySQL server重启后不再取消AUTO_INCREMENT = N表选项的效果。如果将自增计数器初始化为特定值，或者将自动递增计数器值更改为更大的值，新的值被持久化，即使服务器重启。
- 在回滚操作之后立即重启服务器将不再导致重新使用分配给回滚事务的自动递增值。
- 如果将AUTO_INCREMEN列值修改为大于当前最大自增值(例如，在更新操作中)的值，则新值将被持久化，随后的插入操作将从新的、更大的值开始分配自动增量值。
-- 确认下自己的版本
select VERSION()
/*
VERSION() |
----------+
5.7.26-log|
*/
-- 创建表
create table testincr(
id int auto_increment primary key,
name varchar(50)
)
-- 插入数据
insert into testincr(name) values
('刘备'),
('关羽'),
('张飞');
-- 查看当前的自增量
select t.`AUTO_INCREMENT` from information_schema.TABLES t where TABLE_NAME ='testincr'
/* 
AUTO_INCREMENT|
--------------+
4|
*/
-- 更改列值
update testincr set id=4 where id=3
-- 查看现在的表值
/*
id|name|
--+----+
1|刘备  |
2|关羽  |
4|张飞  |
*/
-- 插入新值 问题出现
insert into testincr(name) values('赵云');
/*
SQL 错误 [1062] [23000]: Duplicate entry '4' for key 'PRIMARY'
*/
-- 如果我们再次插入，它就是正常的，因为id到5了。。。
mysql> insert into testincr(name) values('赵云');
Query OK, 1 row affected (0.01 sec)
##### 1.18-binlog日志事务压缩
MySQL 8.0.20 版本增加了binlog日志事务压缩功能，将事务信息使用zstd算法进行压缩，然后再写入binlog日志文件，这种被压缩后的事务信息，在binlog中对应为一个新的event类型，叫做Transaction_payload_event。
##### 1.19-分区表改进
MySQL 8.0 对于分区表功能进行了较大的修改，在 8.0 之前，分区表在Server层实现，支持多种存储引擎，从 8.0 版本开始，分区表功能移到引擎层实现，目前MySQL 8.0 版本只有InnoDB存储引擎支持分区表。
##### 1.20-自动参数设置
将innodb_dedicated_server开启的时候，它可以自动的调整下面这四个参数的值：
innodb_buffer_pool_size 总内存大小
innodb_log_file_size redo文件大小
innodb_log_files_in_group redo文件数量
innodb_flush_method 数据刷新方法
只需将innodb_dedicated_server = ON 设置好，上面四个参数会自动调整，解决非专业人员安装数据库后默认初始化数据库参数默认值偏低的问题，让MySQL自适应的调整上面四个参数，前提是服务器是专用来给MySQL数据库的，如果还有其他软件或者资源或者多实例MySQL使用，不建议开启该参数，本文以MySQL8.0.19为例。
那么按照什么规则调整呢？MySQL官方给出了相关参数调整规则如下：
**1. innodb_buffer_pool_size自动调整规则：**
| 专用服务器内存大小 | buffer_pool_size大小 |
| --- | --- |
| 小于1G | 128MB （MySQL缺省值） |
| 1G to 4G | OS内存*0.5 |
| 大于4G | OS内存*0.75 |
**2. innodb_log_file_size自动调整规则：**
| buffer_pool_size大小 | log_file_size 大小 |
| --- | --- |
| 小于8G | 512MB |
| 8G to 128G | 1024MB |
| 大于128G | 2048MB |
**3. innodb_log_files_in_group自动调整规则：**
（innodb_log_files_in_group值就是log file的数量）
| buffer_pool_size大小 | log file数量 |
| --- | --- |
| 小于8G | ROUND(buffer pool size) |
| 8G to 128G | ROUND(buffer pool size * 0.75) |
| 大于128G | 64 |
说明：如果ROUND(buffer pool size)值小于2GB，那么innodb_log_files_in_group会强制设置为2。
**4. innodb_flush_method自动调整规则：**
该参数调整规则直接引用官方文档的解释：The flush method is set to O_DIRECT_NO_FSYNC when innodb_dedicated_server is enabled. If the O_DIRECT_NO_FSYNC setting is not available, the default innodb_flush_method setting is used.
如果系统允许设置为O_DIRECT_NO_FSYNC；如果系统不允许，则设置为InnoDB默认的Flush method。
##### 1.20.1-自适应参数的好处：
- 自动调整，简单方便，让DBA更省心
- 自带优化光环：没有该参数前，innodb_buffer_pool_size和log_file_size默认安装初始化后只有128M和48M，这对于一个生产环境来说是远远不够的，通常DBA都会手工根据服务器的硬件配置来调整优化，该参数出现后基本上可以解决入门人员安装MySQL后的性能问题。
- 云厂商，虚拟化等动态资源扩容或者缩容后，不必再操心MySQL参数配置问题。
##### 1.20.2-自适应参数的限制：
- 专门给MySQL独立使用的服务器
- 单机多实例的情况不适用
- 服务器上还跑着其他软件或应用的情况不适用
##### 1.21-窗口函数
从 MySQL 8.0 开始，新增了一个叫窗口函数的概念。
什么叫窗口?
它可以理解为记录集合，窗口函数也就是在满足某种条件的记录集合上执行的特殊函数。对于每条记录都要在此窗口内执行函数，有的函数随着记录不同，窗口大小都是固定的，这种属于静态窗口；有的函数则相反，不同的记录对应着不同的窗口，这种动态变化的窗口叫滑动窗口。
它可以用来实现若干新的查询方式。窗口函数与 SUM()、COUNT() 这种聚合函数类似，但它不会将多行查询结果合并为一行，而是将结果放回多行当中。即窗口函数不需要 GROUP BY。
![](.img/0766334f.png)
窗口函数内容太多，后期我会专门写一篇文章介绍窗口函数
##### 1.22-索引损坏标记
当遇到索引树损坏时，InnoDB会在redo日志中写入一个损坏标志，这会使损坏标志安全崩溃。InnoDB还将内存损坏标志数据写入每个检查点的私有系统表中。
在恢复的过程中，InnoDB会从这两个位置读取损坏标志，并合并结果，然后将内存中的表和索引对象标记为损坏。
##### 1.23-InnoDB memcached插件
InnoDB memcached插件支持批量get操作（在一个memcached查询中获取多个键值对）和范围查询。减少客户端和服务器之间的通信流量，在单个memcached查询中获取多个键、值对的功能可以提高读取性能。
##### 1.24-Online DDL
从 MySQL 8.0.12 开始（仅仅指InnoDB引擎），以下 ALTER TABLE 操作支持 ALGORITHM=INSTANT：
- 添加列。此功能也称为“即时添加列”。限制适用。
- 添加或删除虚拟列。
- 添加或删除列默认值。
- 修改 ENUM 或 SET 列的定义。
- 更改索引类型。
- 重命名表。
Online DDL的好处：
支持 ALGORITHM=INSTANT 的操作只修改数据字典中的元数据。表上没有元数据锁，表数据不受影响，操作是即时的，并不会造成业务抖动。这在一些服务级别要求比较高（7*24）的系统中，是非常方便的。该特性是由腾讯游戏DBA团队贡献的。
如果未明确指定，则支持它的操作默认使用 ALGORITHM=INSTANT。如果指定了 ALGORITHM=INSTANT 但不受支持，则操作会立即失败并出现错误。需要注意的是，在 MySQL 8.0.29 之前，一列只能作为表的最后一列添加。不支持将列添加到其他列中的任何其他位置。从 MySQL 8.0.29 开始，可以将即时添加的列添加到表中的任何位置。
##### 1.25-EXPLAIN ANALYZE
Explain 是我们常用的查询分析工具，可以对查询语句的执行方式进行评估，给出很多有用的线索。但他仅仅是评估，不是实际的执行情况，比如结果中的 rows，可能和实际结果相差甚大。
Explain Analyze 是 MySQL 8 中提供的新工具,可贵之处在于可以给出实际执行情况。Explain Analyze 是一个查询性能分析工具，可以详细的显示出 查询语句执行过程中，都在哪儿花费了多少时间。Explain Analyze 会做出查询计划，并且会实际执行，以测量出查询计划中各个关键点的实际指标，例如耗时、条数，最后详细的打印出来。
这项新功能建立在常规的EXPLAIN基础之上，可以看作是MySQL 8.0之前添加的EXPLAIN FORMAT = TREE的扩展。EXPLAIN除了输出查询计划和估计成本之外，EXPLAIN ANALYZE还会输出执行计划中各个迭代器的实际成本。
##### 1.26-ReplicaSet
InnoDB ReplicaSet 由一个主节点和多个从节点构成. 可以使用MySQL Shell的ReplicaSet对象和AdminAPI操作管理复制集, 例如检查InnoDB复制集的状态, 并在发生故障时手动故障转移到新的主服务器.
ReplicaSet 所有的节点必须基于GTID，并且数据复制采用异步的方式。使用复制集还可以接管既有的主从复制，但是需要注意，一旦被接管，只能通过AdminAPI对其进行管理。
##### 1.27-备份锁
在MySQL 8.0中，引入了一个轻量级的备份锁，这个锁可以保证备份一致性，而且阻塞的操作相对比较少，是一个非常重要的新特性。
在MySQL 8.0中，为了解决备份FTWRL的问题，引入了轻量级的备份锁；可以通过LOCK INSTANCE FOR BACKUP和UNLOCK INSTANCE，以获取和释放备份锁，执行该语句需要BACKUP_ADMIN权限。
backup lock不会阻塞读写操作。不过，backup lock会阻塞大部分DDL操作，包括创建/删除表、加/减字段、增/删索引、optimize/analyze/repair table等。
总的来说，备份锁还是非常实用的，毕竟其不会影响业务的正常读写；至于备份锁和DDL操作的冲突，还是有很多方法可以避免，比如错开备份和变更的时间、通过pt-online-schema-change/gh-ost避免长时间阻塞等等。随着备份锁的引入，Oracle官方备份工具MEB 8.0和Percona开源备份工具XtraBackup 8.0，也是更新了对backup lock的支持。
##### 1.28-Binlog增强
MySQL 8.0.20 版本增加了binlog日志事务压缩功能，将事务信息使用zstd算法进行压缩，然后再写入binlog日志文件，这种被压缩后的事务信息，在binlog中对应为一个新的event类型，叫做Transaction_payload_event。