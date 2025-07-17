# 故障分析 | MySQL 迁移后 timestamp 列 cannot be null

**原文链接**: https://opensource.actionsky.com/20211028-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-10-27T23:40:50-08:00

---

作者：秦福朗
爱可生 DBA 团队成员，负责项目日常问题处理及公司平台问题排查。热爱互联网，会摄影、懂厨艺，不会厨艺的 DBA 不是好司机，didi~
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来>源。
## 背景
一个业务系统刚迁移完，笔者刚回到家，开发那边就遇到了业务报错”Column ‘create_time’ cannot be null”，从字面意思可以理解为表字段’create_time’想插入null值，但报错该字段不能为null。由此引发了对explicit_defaults_for_timestamp这个有关时间参数的思考。
## 概念概述
### 1. TIMESTAMP和DATETIME
提 explicit_defaults_for_timestamp 参数，首先就要简单解释下时间数据类型 TIMESTAMP 和 DATETIME ：
- 
TIMESTAMP 是一个时间戳，范围是&#8217;1970-01-01 00:00:01.000000&#8217;UTC 到&#8217;2038-01-19 03:14:07.999999&#8217;UTC。
- 
DATETIME是日期和时间的组合，范围是&#8217;1000-01-01 00:00:00.000000&#8217;到 &#8216;9999-12-31 23:59:59.999999&#8217;。
TIMESTAMP 和 DATETIME 列都可以自动初始化并且可以更新为当前的日期和时间，列还可以将当前的时间戳指定为默认值、自动更新的值或者两个同时使用都可以。
### 2. explicit_defaults_for_timestamp
这个系统变量决定了 MySQL 是否为 TIMESTAMP 列的默认值和 NULL 值的处理启用某些非标准的行为。在 MySQL5.7 的默认情况下，explicit_defaults_for_timestamp 是禁用的，这将启用非标准的行为。在 MySQL8.0 的默认值是开启的。本文默认在 MySQL5.7 场景下。
## 看场景
![Image](.img/70460912.png)
业务报错”Column ‘create_time’ cannot be null”，该列不能插入 null 值，查看一下表结构：
`#只展示部分时间相关列
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` timestamp NULL DEFAULT NULL COMMENT '更新时间',
`
可以看到 create_time 列的属性是 not null ，按照惯性思维想，此列不应该插入 null ，为何之前的环境是没有问题的呢？经检查参数发现问题出在 explicit_defaults_for_timestamp 参数上，在迁移前系统没有单独设置该参数值，从 MySQL5.7 的官方文档可知，此时使用默认值为 OFF ，在迁移后的新系统使用的爱可生的 DMP 数据库运维平台的默认 MySQL5.7 配置文件，此时配置文件是配置了该参数值为 ON 。
现场进行参数关闭，改为 OFF ，测试插入正常。那么参数值具体为何能操纵 TIMESTAMP 列的默认值和 null 值呢？继续测试分析。
## 测试分析
1.首先是看一下官网对 explicit_defaults_for_timestamp 详细解释：
（1）如果 explicit_defaults_for_timestamp=OFF ，服务器会启用非标准行为，并按以下方式处理 TIMESTAMP 列：
- 
没有明确使用NULL属性声明的TIMESTAMP列会自动使用NOT NULL属性声明。给这样的列分配一个NULL的值是允许的，并将该列设置为current timestamp。
- 
表中的第一个TIMESTAMP列，如果没有明确地用NULL属性，DEFAULT属性或ON UPDATE属性声明，将自动用DEFAULT CURRENT_TIMESTAMP和ON UPDATE CURRENT_TIMESTAMP属性声明。
- 
在第一个列之后的TIMESTAMP列，如果没有明确地用NULL属性或明确的DEFAULT属性来声明，就会自动声明为DEFAULT &#8216;0000-00-00 00:00:00&#8217; 。对于插入的行，如果没有为该列指定明确的值，那么该列将被分配为&#8217;0000-00-00 00:00:00&#8217;，并且不会发生警告。根据是否启用了严格的SQL mode或包含NO_ZERO_DATE的SQL mode，默认值&#8217;0000-00-00 00:00:00&#8217;可能是不被允许的。
另外需要知道的是这种非标准行为已被废弃；预计将在MySQL的未来版本中被删除。
（2）如果 explicit_defaults_for_timestamp=ON ，服务器将禁用非标准行为并按如下方式处理 TIMESTAMP 列：
- 
不能实现给 TIMESTAMP 列插入一个 NULL 的值，然后自动设置为当前的时间戳。想要插入当前的时间戳，需要将该列设置为 CURRENT_TIMESTAMP 或一个同义词，比如 NOW() 。
- 
没有明确地用 NOT NULL 属性声明的 TIMESTAMP 列会自动用 NULL 属性声明，并允许 NULL 值。给这样的列插入一个 NULL 值，会把它设置为 NULL 值，而不是当前的时间戳。
- 
用 NOT NULL 属性声明的 TIMESTAMP 列不允许NULL值。对于列指定插入 NULL ，如果启用严格的 SQL mode ，其结果是单行插入报错，或者在禁用严格的 SQL 模式下，多行插入的结果是&#8217;0000-00-00 00:00:00&#8217;。在任何情况下，给该列赋值为 NULL 都不会将其设置为当前的时间戳。
- 
用 NOT NULL 属性明确声明的 TIMESTAMP 列，如果没有明确的 DEFAULT 属性，将被视为没有默认值。对于插入的行，如果没有为这样的列指定明确的值，其结果取决于 SQL mode 。如果启用了严格的 SQL mode ，会报错。如果没有启用严格的 SQL mode ，该列则被声明为隐含的默认值 &#8220;0000-00-00 00:00:00&#8243;，并发出 warning 。这与 MySQL 处理其他时间类型（如 DATETIME ）的方式相似。
### 2.做个测试就可以看出来：
**（1）explicit_defaults_for_timestamp=OFF ：**
`mysql> show variables like "%explicit_defaults_for_timestamp%";
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| explicit_defaults_for_timestamp | OFF   |
+---------------------------------+-------+
1 row in set (0.00 sec)
`
创建一个带有timestamp列的表：
`mysql> create table time_off(id int,time timestamp);
Query OK, 0 rows affected (0.02 sec)
mysql> show create table time_off;
+----------+------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------ ------------------------------+
| Table    | Create Table                                                                                                                                                                                           |
+----------+------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------ ------------------------------+
| time_off | CREATE TABLE `time_off` (
`id` int(11) DEFAULT NULL,
`time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+----------+------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------ ------------------------------+
1 row in set (0.00 sec)
`
可以看到此时 timestamp 列会有默认属性‘NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP’。
向该表插入NULL值试试看：
`mysql> insert into time_off values (1,null);
Query OK, 1 row affected (0.00 sec)
mysql> select * from time_off;
+------+---------------------+
| id   | time                |
+------+---------------------+
|    1 | 2021-10-12 01:05:28 |
+------+---------------------+
1 row in set (0.00 sec)
mysql> update time_off set id=2 where id=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> select * from time_off;
+------+---------------------+
| id   | time                |
+------+---------------------+
|    2 | 2021-10-12 01:06:30 |
+------+---------------------+
1 row in set (0.00 sec)
`
发现当 timestamp 列插入 null 值时会正常插入，并自动转换为当前时间戳。更新其他列时也会依据‘ON UPDATE CURRENT_TIMESTAMP’来更新为当前的时间戳。
**（2）explicit_defaults_for_timestamp=ON ：**
`mysql> show variables like "%explicit_defaults_for_timestamp%";
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| explicit_defaults_for_timestamp | ON    |
+---------------------------------+-------+
1 row in set (0.01 sec)
`
创建一个带有 timestamp 列的表：
`mysql> create table time_on(id int,time timestamp);
Query OK, 0 rows affected (0.01 sec)
mysql>  show create table time_on;
+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table   | Create Table                                                                                                                                           |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| time_on | CREATE TABLE `time_on` (
`id` int(11) DEFAULT NULL,
`time` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
`
可以看到此时 timestamp 列会有默认属性‘NULL DEFAULT NULL’。
向该表插入 NULL 值试试看：
`mysql> insert into time_on values (1,null);
Query OK, 1 row affected (0.00 sec)
mysql> select * from time_on;
+------+------+
| id   | time |
+------+------+
|    1 | NULL |
+------+------+
1 row in set (0.00 sec)
`
会发现能够成功插入，插入的为 NULL 值，而非当前的时间戳。
那么在该参数下，向参数值为 OFF 时创建的表 time_off 里插入 null 值会有什么情况呢：
`mysql> insert into time_off values (3,null);
ERROR 1048 (23000): Column 'time' cannot be null
`
会发现此时插入报错’Column &#8216;time&#8217; cannot be null’，符合官方文档对该参数的说明，也证明了业务测试报错的原因是 explicit_defaults_for_timestamp 的参数值设置为 ON ，导致业务插入数据失败。
## 结语
关于该参数，实际上是规范了 MySQL 时间相关的操作，使之更加严格，是有助于MySQL的规范化使用的，所以 MySQL 后续也废弃掉该参数。
细节决定成败，很多同学对迁移工作觉得是轻车熟路，但是没有合理的迁移规划，没有经过严谨的业务测试，确实不太好说迁移的整个过程会是顺顺利利的，有时候坑就在小的细节点上。