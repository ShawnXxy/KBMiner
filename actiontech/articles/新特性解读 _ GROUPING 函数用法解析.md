# 新特性解读 | GROUPING() 函数用法解析

**原文链接**: https://opensource.actionsky.com/20200810-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-08-10T00:35:28-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 8.0 新增了 GROUPING() 函数，用来理清 GROUP BY with rollup 子句检索后所产生的每个分组汇总结果。 
grouping 可用在分组列，having 子句以及 order by 子句。在了解 grouping 函数如何使用之前，先来看看简单 group by with rollup 的检索是何种情形。
**GROUP BY WITH ROLLUP**
GROUP BY 子句 ROLLUP 可以为 GROUP BY 运行结果的每一个分组返回一个统计行，并且为所有分组返回一个总的统计行。
此文中所用的示例表 y1 结构：`mysql> show create table y1\G
*************************** 1. row ***************************
Table: y1
Create Table: CREATE TABLE `y1` (
`id` int NOT NULL,
`r1` int DEFAULT NULL,
`r2` int DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)`
按照字段 r1 r2 来正常检索，GROUP BY 的统计结果：```
mysql> SELECT r1, r2, COUNT(*)
-> FROM y1
-> GROUP BY r1, r2;
+------+------+----------+
| r1   | r2   | count(*) |
+------+------+----------+
|    1 |    2 |        2 |
|    2 |    5 |        2 |
|    1 |    4 |        1 |
|    4 |    3 |        4 |
|    2 |    2 |        3 |
|    4 |    4 |        2 |
|    5 |    5 |        1 |
|    4 |    5 |        1 |
|    3 |    1 |        1 |
|    5 |    2 |        1 |
|    4 |    2 |        1 |
|    3 |    2 |        1 |
+------+------+----------+
12 rows in set (0.00 sec)
```
当此条统计 SQL 加上 ROLLUP 子句后，会在每个分组后面加上一行统计值，其中统计行高位字段显示为 NULL，COUNT 结果用来计算分组内的总记录数。```
mysql> SELECT r1, r2, COUNT(*)
-> FROM y1
-> GROUP BY r1, r2 WITH ROLLUP;
+------+------+----------+
| r1   | r2   | count(*) |
+------+------+----------+
|    1 |    2 |        2 |
|    1 |    4 |        1 |
|    1 | NULL |        3 |
|    2 |    2 |        3 |
|    2 |    5 |        2 |
|    2 | NULL |        5 |
|    3 |    1 |        1 |
|    3 |    2 |        1 |
|    3 | NULL |        2 |
|    4 |    2 |        1 |
|    4 |    3 |        4 |
|    4 |    4 |        2 |
|    4 |    5 |        1 |
|    4 | NULL |        8 |
|    5 |    2 |        1 |
|    5 |    5 |        1 |
|    5 | NULL |        2 |
| NULL | NULL |       20 |
+------+------+----------+
18 rows in set (0.00 sec)
```
那表 y1 没有记录存储为 NULL，都是非 NULL 值，现在为表 y1 插入几条包含 NULL 的记录。```
mysql> insert into y1 values (21,null,null);
Query OK, 1 row affected (0.01 sec)
mysql> insert into y1 values (22,1,null);
Query OK, 1 row affected (0.01 sec)
mysql> insert into y1 values (23,2,null);
Query OK, 1 row affected (0.01 sec)
mysql> insert into y1 values (24,3,null);
Query OK, 1 row affected (0.01 sec)
mysql> insert into y1 values (25,4,null);
Query OK, 1 row affected (0.01 sec)
mysql> insert into y1 values (26,5,null);
Query OK, 1 row affected (0.01 sec)
```
此时再来看看 WITH ROLLUP 统计的结果。 ```
mysql> SELECT r1, r2, COUNT(*)
-> FROM y1
-> GROUP BY r1, r2 WITH ROLLUP;
+------+------+----------+
| r1   | r2   | count(*) |
+------+------+----------+
| NULL | NULL |        1 |
| NULL | NULL |        1 |
|    1 | NULL |        1 |
|    1 |    2 |        2 |
|    1 |    4 |        1 |
|    1 | NULL |        4 |
|    2 | NULL |        1 |
|    2 |    2 |        3 |
|    2 |    5 |        2 |
|    2 | NULL |        6 |
|    3 | NULL |        1 |
|    3 |    1 |        1 |
|    3 |    2 |        1 |
|    3 | NULL |        3 |
|    4 | NULL |        1 |
|    4 |    2 |        1 |
|    4 |    3 |        4 |
|    4 |    4 |        2 |
|    4 |    5 |        1 |
|    4 | NULL |        9 |
|    5 | NULL |        1 |
|    5 |    2 |        1 |
|    5 |    5 |        1 |
|    5 | NULL |        3 |
| NULL | NULL |       26 |
+------+------+----------+
25 rows in set (0.00 sec)
```
由于表 y1 本身包含了一系列包含 NULL 的记录，这条 SQL 有点分不清哪些是正常的 NULL，哪些是汇总的 NULL。
接下来 GROUPING() 函数准备上场……
**GROUPING() 函数**
GROUPING() 函数用来返回每个分组是否为 ROLLUP 结果，是为 1 否为 0。从结果中，很容易就能区分哪些 NULL 是正常记录，哪些是 ROLLUP 的结果。`mysql> SELECT r1
-> , if(GROUPING(r1) = 1, '汇总', '正常记录') AS grouping_r1
-> , r2
-> , if(GROUPING(r2) = 1, '汇总', '正常记录') AS grouping_r2
-> , COUNT(*)
-> FROM y1
-> GROUP BY r1, r2 WITH ROLLUP;
+------+--------------+------+--------------+----------+
| r1   | grouping_r1  | r2   | grouping_r2  | count(*) |
+------+--------------+------+--------------+----------+
| NULL | 正常记录     | NULL | 正常记录     |        1 |
| NULL | 正常记录     | NULL | 汇总         |        1 |
|    1 | 正常记录     | NULL | 正常记录     |        1 |
|    1 | 正常记录     |    2 | 正常记录     |        2 |
|    1 | 正常记录     |    4 | 正常记录     |        1 |
|    1 | 正常记录     | NULL | 汇总         |        4 |
|    2 | 正常记录     | NULL | 正常记录     |        1 |
|    2 | 正常记录     |    2 | 正常记录     |        3 |
|    2 | 正常记录     |    5 | 正常记录     |        2 |
|    2 | 正常记录     | NULL | 汇总         |        6 |
|    3 | 正常记录     | NULL | 正常记录     |        1 |
|    3 | 正常记录     |    1 | 正常记录     |        1 |
|    3 | 正常记录     |    2 | 正常记录     |        1 |
|    3 | 正常记录     | NULL | 汇总         |        3 |
|    4 | 正常记录     | NULL | 正常记录     |        1 |
|    4 | 正常记录     |    2 | 正常记录     |        1 |
|    4 | 正常记录     |    3 | 正常记录     |        4 |
|    4 | 正常记录     |    4 | 正常记录     |        2 |
|    4 | 正常记录     |    5 | 正常记录     |        1 |
|    4 | 正常记录     | NULL | 汇总         |        9 |
|    5 | 正常记录     | NULL | 正常记录     |        1 |
|    5 | 正常记录     |    2 | 正常记录     |        1 |
|    5 | 正常记录     |    5 | 正常记录     |        1 |
|    5 | 正常记录     | NULL | 汇总         |        3 |
| NULL | 汇总         | NULL | 汇总         |       26 |
+------+--------------+------+--------------+----------+
25 rows in set (0.00 sec)`
GROUPING() 函数不仅仅是针对单个字段来统计汇总值，还可以针对多个字段。把上面的 SQL 修改下，变为：
```
mysql> SELECT r1, r2, GROUPING(r1, r2) AS grouping_r1_r2
-> , COUNT(*)
-> FROM y1
-> GROUP BY r1, r2 WITH ROLLUP;
+------+------+----------------+----------+
| r1   | r2   | grouping_r1_r2 | COUNT(*) |
+------+------+----------------+----------+
| NULL | NULL |              0 |        1 |
| NULL | NULL |              1 |        1 |
|    1 | NULL |              0 |        1 |
|    1 |    2 |              0 |        2 |
|    1 |    4 |              0 |        1 |
|    1 | NULL |              1 |        4 |
|    2 | NULL |              0 |        1 |
|    2 |    2 |              0 |        3 |
|    2 |    5 |              0 |        2 |
|    2 | NULL |              1 |        6 |
|    3 | NULL |              0 |        1 |
|    3 |    1 |              0 |        1 |
|    3 |    2 |              0 |        1 |
|    3 | NULL |              1 |        3 |
|    4 | NULL |              0 |        1 |
|    4 |    2 |              0 |        1 |
|    4 |    3 |              0 |        4 |
|    4 |    4 |              0 |        2 |
|    4 |    5 |              0 |        1 |
|    4 | NULL |              1 |        9 |
|    5 | NULL |              0 |        1 |
|    5 |    2 |              0 |        1 |
|    5 |    5 |              0 |        1 |
|    5 | NULL |              1 |        3 |
| NULL | NULL |              3 |       26 |
+------+------+----------------+----------+
25 rows in set (0.00 sec)
```
此时会发现，GROUPING() 函数对多个字段结果并非只有 1 和 0，还有一个值为 3。在 GROUPING() 函数包含多个参数时，按照以下方式来返回结果：- GROUPING(r1,r2) 等价于 GROUPING(r2)  + GROUPING(r1) << 1
- GROUPING(r1,r2,r3,&#8230;) 等价于 GROUPING(r3) + GROUPING(r2) << 1 + GROUPING(r1) << 2
- 以此类推
再次来改下以上 SQL，用 (GROUPING(r2) + (GROUPING(r1) << 1)) 来替换 GROUPING(r1,r2)`mysql> SELECT r1, r2,(grouping(r2) + (grouping(r1) << 1)) grouping_r1_r2, count(*) FROM y1 GROUP BY r
1, r2 WITH ROLLUP;
+------+------+----------------+----------+
| r1   | r2   | grouping_r1_r2 | count(*) |
+------+------+----------------+----------+
| NULL | NULL |              0 |        1 |
| NULL | NULL |              1 |        1 |
|    1 | NULL |              0 |        1 |
|    1 |    2 |              0 |        2 |
|    1 |    4 |              0 |        1 |
|    1 | NULL |              1 |        4 |
|    2 | NULL |              0 |        1 |
|    2 |    2 |              0 |        3 |
|    2 |    5 |              0 |        2 |
|    2 | NULL |              1 |        6 |
|    3 | NULL |              0 |        1 |
|    3 |    1 |              0 |        1 |
|    3 |    2 |              0 |        1 |
|    3 | NULL |              1 |        3 |
|    4 | NULL |              0 |        1 |
|    4 |    2 |              0 |        1 |
|    4 |    3 |              0 |        4 |
|    4 |    4 |              0 |        2 |
|    4 |    5 |              0 |        1 |
|    4 | NULL |              1 |        9 |
|    5 | NULL |              0 |        1 |
|    5 |    2 |              0 |        1 |
|    5 |    5 |              0 |        1 |
|    5 | NULL |              1 |        3 |
| NULL | NULL |              3 |       26 |
+------+------+----------------+----------+
25 rows in set (0.00 sec)`这里和直接 GROUPING(r1, r2) 的结果一致。
GROUPING 语句还可以用在 HAVING 子句里，比如用 GROUPING 子句来过滤掉非 ROLLUP 的结果。```
mysql> SELECT r1, r2,count(*) FROM y1 GROUP BY r1, r2 WITH ROLLUP having grouping(r1) = 1 or grouping(r2) = 1;
+------+------+----------+
| r1   | r2   | count(*) |
+------+------+----------+
| NULL | NULL |        1 |
|    1 | NULL |        4 |
|    2 | NULL |        6 |
|    3 | NULL |        3 |
|    4 | NULL |        9 |
|    5 | NULL |        3 |
| NULL | NULL |       26 |
+------+------+----------+
7 rows in set (0.00 sec)
```
**总结**
这里介绍了 MySQL 8.0 的新函数 GROUPING(）的用法，如有不足欢迎批评指正。
相关文章推荐：
[新特性解读 | InnoDB-Cluster 扫盲-日常运维](https://opensource.actionsky.com/20200720-mysql/)
[新特性解读 | mysql 8.0 memcached api 新特性](https://opensource.actionsky.com/20200706-mysql/)