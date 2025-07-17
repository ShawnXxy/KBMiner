# 故障分析 | MySQL convert 函数导致的字符集报错处理

**原文链接**: https://opensource.actionsky.com/20230209-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-02-08T18:51:47-08:00

---

作者：徐耀荣
爱可生南区交付服务部 DBA 团队成员，主要负责MySQL故障处理以及相关技术支持。爱好电影，游戏，旅游以及桌球。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一、问题背景
有客户之前遇到一个 mysql8.0.21 实例中排序规则的报错，是在调用视图时抛出，报错信息如下：
`ERROR 1267 (HY000): Illegal mix of collations (utf8mb4_general_ci,IMPLICIT) and (utf8mb4_0900_ai_ci,IMPLICIT) for operation '='`
#### 二、问题模拟
mysql> show create table t1\G;
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`name1` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
1 row in set (0.00 sec)
mysql> show create table t2\G;
*************************** 1. row ***************************
Table: t2
Create Table: CREATE TABLE `t2` (
`name2` varchar(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
mysql> CREATE VIEW t3 as select * from t1,t2 where `t1`.`name1`= `t2`.`name2`;
Query OK, 0 rows affected (0.06 sec)
mysql> select * from t3;
ERROR 1267 (HY000): Illegal mix of collations (utf8mb4_general_ci,IMPLICIT) and (utf8mb4_0900_ai_ci,IMPLICIT) for operation '='
#### 三、问题分析
通过查看视图定义，可以发现由于视图中涉及到的两张表字符集不同，所以创建视图时 MySQL 会自动使用 convert 函数转换字符集。
mysql> show create view t3\G;
*************************** 1. row ***************************
View: t3
Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `t3` AS select `t1`.`name1` AS `name1`,`t2`.`name2` AS `name2` from (`t1` join `t2`) where (`t1`.`name1` = convert(`t2`.`name2` using utf8mb4))
character_set_client: utf8mb4
collation_connection: utf8mb4_general_ci
1 row in set (0.00 sec)
在 MySQL 8.0 中 utf8mb4 的默认排序规则为 utf8mb4_0900_ai_ci ，而在 t1 表的排序规则为 utf8mb4_general_ci ，那么我们试着将排序规则相关的参数修改后再执行 SQL 看看，修改后的环境参数如下
mysql> show variables like '%collat%';
+-------------------------------+--------------------+
| Variable_name                 | Value              |
+-------------------------------+--------------------+
| collation_connection          | utf8mb4_general_ci |
| collation_database            | utf8mb4_bin        |
| collation_server              | utf8mb4_bin        |
| default_collation_for_utf8mb4 | utf8mb4_general_ci |
+-------------------------------+--------------------+
再次执行 sql 发现还是会报一样的错。
mysql> select * from t1,t2 where `t1`.`name1`=convert(`t2`.`name2` using utf8mb4);
ERROR 1267 (HY000): Illegal mix of collations (utf8mb4_general_ci,IMPLICIT) and (utf8mb4_0900_ai_ci,IMPLICIT) for operation '='
通过 show collation 来查看 utf8mb4 字符集对应的默认排序规则，输出显示默认规则为 utf8mb4_general_ci ，并不是 utf8mb4_0900_ai_ci 。
mysql> show collation like '%utf8mb4%';
+----------------------------+---------+-----+---------+----------+---------+---------------+
| Collation                  | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+----------------------------+---------+-----+---------+----------+---------+---------------+
| utf8mb4_general_ci         | utf8mb4 |  45 | Yes     | Yes      |       1 | PAD SPACE     |
+----------------------------+---------+-----+---------+----------+---------+---------------+
mysql> show character set like '%utf8mb4%';
+---------+---------------+--------------------+--------+
| Charset | Description   | Default collation  | Maxlen |
+---------+---------------+--------------------+--------+
| utf8mb4 | UTF-8 Unicode | utf8mb4_general_ci |      4 |
+---------+---------------+--------------------+--------+
1 row in set (0.00 sec)
继续排查发现元数据中的字符集默认排序规则如下，默认规则为 utf8mb4_0900_ai_ci 。
mysql>  select * from INFORMATION_SCHEMA.COLLATIONS where IS_DEFAULT='Yes' and CHARACTER_SET_NAME='utf8mb4'\G;
*************************** 1. row ***************************
COLLATION_NAME: utf8mb4_0900_ai_ci
CHARACTER_SET_NAME: utf8mb4
ID: 255
IS_DEFAULT: Yes
IS_COMPILED: Yes
SORTLEN: 0
PAD_ATTRIBUTE: NO PAD
1 row in set (0.00 sec)
检查参数发现，元数据信息中 utf8mb4 字符集默认排序规则是 utf8mb4_0900_ai_ci ，show collation/show character 输出的都是 utf8mb4_general_ci 。为什么 show 显示的结果和 INFORMATION_SCHEMA.COLLATIONS 表查到的信息还不一样呢？此处我们暂且按下不表，咱们先看看官方文档中 convert 函数用法，其中有下面这段原文：
> If you specify CHARACTER SET charset_name as just shown, the character set and collation of the result are charset_name and the default collation of charset_name. If you omit CHARACTER SET charset_name, the character set and collation of the result are defined by the character_set_connection and collation_connection system variables that determine the default connection character set and collation (see Section 10.4, “Connection Character Sets and Collations”).
从上述原文可知如果 convert 只指定了字符集，那么该结果的排序规则就是所指定字符集的默认规则，由之前的测试情况可知，convert 使用的是 INFORMATION_SCHEMA.COLLATIONS 的排序规则，而不是 default_collation_for_utf8mb4 指定的 utf8mb4_general_ci ，那我们来看看 default_collation_for_utf8mb4 参数主要作用场景：
- SHOW COLLATION and SHOW CHARACTER SET.
- CREATE TABLE and ALTER TABLE having a CHARACTER SET utf8mb4 clause without a COLLATION clause, either for the table character set or for a column character set.
- CREATE DATABASE and ALTER DATABASE having a CHARACTER SET utf8mb4 clause without a COLLATION clause.
- Any statement containing a string literal of the form _utf8mb4&#8217;some text&#8217; without a COLLATE clause.
其中，第一点解释了为什么 show 查到的信息和元数据中信息不一样，default_collation_for_utf8mb4 修改后影响 show COLLATION and SHOW CHARACTER SET 的查询结果，并不会改变字符集的默认排序规则，所以utf8mb4 的默认规则还是 utf8mb4_0900_ai_ci ，sql 执行依然会报错。
将 convert 函数指定为 t1.name1 字段的排序规则后，sql 执行正常。
mysql> select * from t1,t2 where `t1`.`name1` = convert(`t2`.`name2` using utf8mb4) collate utf8mb4_general_ci;
+-------+-------+
| name1 | name2 |
+-------+-------+
| jack  | jack  |
+-------+-------+
1 row in set (0.00 sec)
另外，下面测试可以验证 default_collation_for_utf8mb4 的第四个场景。
mysql> select * from INFORMATION_SCHEMA.COLLATIONS where IS_DEFAULT='Yes' and CHARACTER_SET_NAME='utf8mb4'\G;
*************************** 1. row ***************************
COLLATION_NAME: utf8mb4_0900_ai_ci
CHARACTER_SET_NAME: utf8mb4
ID: 255
IS_DEFAULT: Yes
IS_COMPILED: Yes
SORTLEN: 0
PAD_ATTRIBUTE: NO PAD
1 row in set (0.00 sec)
mysql> show variables like '%default_collation%';
+-------------------------------+--------------------+
| Variable_name                 | Value              |
+-------------------------------+--------------------+
| default_collation_for_utf8mb4 | utf8mb4_general_ci |
+-------------------------------+--------------------+
1 row in set (0.01 sec)
mysql> set @s1 = _utf8mb4 'jack',@s2 = _utf8mb4 'jack';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT @s1 = @s2;
+-----------+
| @s1 = @s2 |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
_utf8mb4声明的@s1和@s2排序规则是default_collation_for_utf8mb4参数值，为utf8mb4_general_ci
mysql> SELECT @s1 = CONVERT(@s2 USING utf8mb4);
ERROR 1267 (HY000): Illegal mix of collations (utf8mb4_general_ci,IMPLICIT) and (utf8mb4_0900_ai_ci,IMPLICIT) for operation '='
此时，经过CONVERT函数处理的@s2排序规则是utf8mb4_0900_ai_ci，所以会报错
mysql> SELECT @s1 = CONVERT(@s2 USING utf8mb4) collate utf8mb4_general_ci;
+-------------------------------------------------------------+
| @s1 = CONVERT(@s2 USING utf8mb4) collate utf8mb4_general_ci |
+-------------------------------------------------------------+
|                                                                 1 |
+-------------------------------------------------------------+
1 row in set (0.00 sec)
#### 四、问题总结
运维中为避免字符集引起的报错问题，有如下建议可供参考：（具体参数值根据业务需求选择）
- 创建数据库实例时需指定参数 character_set_database（默认值：utf8mb4），character_set_server（默认值：utf8mb4）。
- 当需要创建非默认字符集 database / table 时，需要在 sql 中明确指定字符集和排序规则。
- 使用convert函数转换字符集时，当字段排序规则不是转换后字符集的默认排序规则，需要指定具体的排序规则。SELECT @s1 = CONVERT(@s2 USING utf8mb4) collate utf8mb4_general_ci
- MySQL 5.7迁移至MySQL 8.0时，需注意MySQL 5.7版本中utf8mb4默认排序规则是 utf8mb4_general_ci，MySQL 8.0中 utf8mb4 默认排序规则是 utf8mb4_0900_ai_ci 。
#### 参考
[https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html)
[https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html)
[https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert)