# 新特性解读 | MySQL 8.0 通用表达式（WITH）深入用法

**原文链接**: https://opensource.actionsky.com/20210520-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-05-19T19:10:42-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 8.0 发布已经好几年了，之前介绍过 WITH 语句（通用表达式）的简单用途以及使用场景，类似如下的语句：
**with tmp(a) as (select 1 union all select 2) select * from tmp;**
正巧之前客户就咨询我，WITH 有没有可能和 UPDATE、DELETE 等语句一起来用？或者说有没有可以简化日常 SQL 的其他用法，有点迷惑，能否写几个例子简单说明下？
其实 WITH 表达式除了和 SELECT 一起用， 还可以有下面的组合：
insert with 、with update、with delete、with  with、with recursive(可以模拟数字、日期等序列)、WITH 可以定义多张表
我们来一个一个看看：
**1. 用 WITH 表达式来造数据**
用 WITH 表达式来造数据，非常简单，比如下面例子：给表 y1 添加100条记录，日期字段要随机。
`localhost:ytt>create table y1 (id serial primary key, r1 int,log_date date);
Query OK, 0 rows affected (0.09 sec)
localhost:ytt>INSERT y1 (r1,log_date)
-> WITH recursive tmp (a, b) AS
-> (SELECT
->   1,
->   '2021-04-20'
-> UNION
-> ALL
-> SELECT
->   ROUND(RAND() * 10),
->   b - INTERVAL ROUND(RAND() * 1000) DAY
-> FROM
->   tmp
-> LIMIT 100) TABLE tmp;
Query OK, 100 rows affected (0.03 sec)
Records: 100  Duplicates: 0  Warnings: 0
localhost:ytt>table y1 limit 10;
+----+------+------------+
| id | r1   | log_date   |
+----+------+------------+
|  1 |    1 | 2021-04-20 |
|  2 |    8 | 2020-04-02 |
|  3 |    5 | 2019-05-26 |
|  4 |    1 | 2018-01-21 |
|  5 |    2 | 2016-09-08 |
|  6 |    9 | 2016-06-14 |
|  7 |    7 | 2016-02-06 |
|  8 |    6 | 2014-03-18 |
|  9 |    6 | 2011-08-25 |
| 10 |    9 | 2010-02-02 |
+----+------+------------+
10 rows in set (0.00 sec)`
**2. 用 WITH 表达式来更新表数据**
WITH 表达式可以与 UPDATE 语句一起，来执行要更新的表记录：
`localhost:ytt>WITH recursive tmp (a, b, c) AS
-> (SELECT
->   1,
->   1,
->   '2021-04-20'
-> UNION ALL
-> SELECT
->   a + 2,
->   100,
->   DATE_SUB(
->     CURRENT_DATE(),
->     INTERVAL ROUND(RAND() * 1000, 0) DAY
->   )
-> FROM
->   tmp
-> WHERE a  UPDATE
->   tmp AS a,
->   y1 AS b
-> SET
->   b.r1 = a.b
-> WHERE a.a = b.id;
Query OK, 49 rows affected (0.02 sec)
Rows matched: 50  Changed: 49  Warnings: 0
localhost:ytt>table y1 limit 10;
+----+------+------------+
| id | r1   | log_date   |
+----+------+------------+
|  1 |    1 | 2021-04-20 |
|  2 |    8 | 2019-12-26 |
|  3 |  100 | 2018-06-12 |
|  4 |    8 | 2017-07-11 |
|  5 |  100 | 2016-08-10 |
|  6 |    9 | 2015-09-14 |
|  7 |  100 | 2014-12-19 |
|  8 |    2 | 2014-08-13 |
|  9 |  100 | 2014-08-05 |
| 10 |    8 | 2011-11-12 |
+----+------+------------+
10 rows in set (0.00 sec)`
**3. 用 WITH 表达式来删除表数据**
比如删除 ID 为奇数的行，可以用 WITH DELETE 形式的删除语句：
`localhost:ytt>WITH recursive tmp (a) AS
-> (SELECT
->   1
-> UNION
-> ALL
-> SELECT
->   a + 2
-> FROM
->   tmp
-> WHERE a  DELETE FROM y1 WHERE id IN (TABLE tmp);
Query OK, 50 rows affected (0.02 sec)
localhost:ytt>table y1 limit 10;
+----+------+------------+
| id | r1   | log_date   |
+----+------+------------+
|  2 |    6 | 2019-05-16 |
|  4 |    8 | 2015-12-07 |
|  6 |    2 | 2014-05-14 |
|  8 |    7 | 2010-05-07 |
| 10 |    3 | 2007-03-27 |
| 12 |    6 | 2006-12-14 |
| 14 |    3 | 2004-04-22 |
| 16 |    7 | 2001-09-16 |
| 18 |    7 | 2001-01-04 |
| 20 |    7 | 2000-02-12 |
+----+------+------------+
10 rows in set (0.00 sec)
`
与 DELETE 一起使用，要注意一点：WITH 表达式本身数据为只读，所以多表 DELETE 中不能包含 WITH 表达式。比如把上面的语句改成多表删除形式会直接报 WITH 表达式不可更新的错误。
`localhost:ytt>WITH recursive tmp (a) AS
->  (SELECT
->    1
->  UNION
->  ALL
->  SELECT
->    a + 2
->  FROM
->    tmp
->  WHERE a   delete a,b from y1 a join tmp b where a.id = b.a;
ERROR 1288 (HY000): The target table b of the DELETE is not updatable`
**4. WITH 和 WITH 一起用**
前提条件：WITH 表达式不能在同一个层级，一个层级只允许一个 WITH 表达式
`localhost:ytt>SELECT * FROM  
->   (
->     WITH tmp1 (a, b, c) AS 
->     (
->       VALUES
->         ROW (1, 2, 3),
->         ROW (3, 4, 5),
->         ROW (6, 7, 8)
->     ) SELECT  * FROM
->         (
->           WITH tmp2 (d, e, f) AS (
->             VALUES
->               ROW (100, 200, 300),
->               ROW (400, 500, 600)
->             ) TABLE tmp2
->         ) X
->           JOIN tmp1 Y
->   ) Z ORDER BY a;
+-----+-----+-----+---+---+---+
| d   | e   | f   | a | b | c |
+-----+-----+-----+---+---+---+
| 400 | 500 | 600 | 1 | 2 | 3 |
| 100 | 200 | 300 | 1 | 2 | 3 |
| 400 | 500 | 600 | 3 | 4 | 5 |
| 100 | 200 | 300 | 3 | 4 | 5 |
| 400 | 500 | 600 | 6 | 7 | 8 |
| 100 | 200 | 300 | 6 | 7 | 8 |
+-----+-----+-----+---+---+---+
6 rows in set (0.01 sec)`
**5. WITH 多个表达式来 JOIN**
用上面的例子，改写多个 WITH 为一个 WITH：
`localhost:ytt>WITH 
-> tmp1 (a, b, c) AS 
-> (
-> VALUES
-> ROW (1, 2, 3),
-> ROW (3, 4, 5),
-> ROW (6, 7, 8)
-> ),
-> tmp2 (d, e, f) AS (
->     VALUES
->       ROW (100, 200, 300),
->       ROW (400, 500, 600)
-> )
-> SELECT * FROM  tmp2,tmp1 ORDER BY a;
+-----+-----+-----+---+---+---+
| d   | e   | f   | a | b | c |
+-----+-----+-----+---+---+---+
| 400 | 500 | 600 | 1 | 2 | 3 |
| 100 | 200 | 300 | 1 | 2 | 3 |
| 400 | 500 | 600 | 3 | 4 | 5 |
| 100 | 200 | 300 | 3 | 4 | 5 |
| 400 | 500 | 600 | 6 | 7 | 8 |
| 100 | 200 | 300 | 6 | 7 | 8 |
+-----+-----+-----+---+---+---+
6 rows in set (0.00 sec)`
**6. with 生成日期序列**
用 WITH 表达式生成日期序列，类似于 POSTGRESQL 的 generate_series 表函数，比如，从 ‘2020-01-01’ 开始，生成一个月的日期序列：
`localhost:ytt>WITH recursive seq_date (log_date) AS
->      (SELECT
->        '2020-01-01'
->      UNION
->      ALL
->      SELECT
->        log_date + INTERVAL 1 DAY
->      FROM
->        seq_date
->      WHERE log_date + INTERVAL 1 DAY       SELECT
->        log_date
->      FROM
->        seq_date;
+------------+
| log_date   |
+------------+
| 2020-01-01 |
| 2020-01-02 |
| 2020-01-03 |
| 2020-01-04 |
| 2020-01-05 |
| 2020-01-06 |
| 2020-01-07 |
| 2020-01-08 |
| 2020-01-09 |
| 2020-01-10 |
| 2020-01-11 |
| 2020-01-12 |
| 2020-01-13 |
| 2020-01-14 |
| 2020-01-15 |
| 2020-01-16 |
| 2020-01-17 |
| 2020-01-18 |
| 2020-01-19 |
| 2020-01-20 |
| 2020-01-21 |
| 2020-01-22 |
| 2020-01-23 |
| 2020-01-24 |
| 2020-01-25 |
| 2020-01-26 |
| 2020-01-27 |
| 2020-01-28 |
| 2020-01-29 |
| 2020-01-30 |
| 2020-01-31 |
+------------+
31 rows in set (0.00 sec)`
**7. with 表达式做派生表**
使用刚才那个日期列表，
`localhost:ytt>SELECT
->        *
->      FROM
->        (
->          WITH recursive seq_date (log_date) AS
->          (SELECT
->            '2020-01-01'
->          UNION
->          ALL
->          SELECT
->            log_date + INTERVAL 1 DAY
->          FROM
->            seq_date
->          WHERE log_date+ interval 1 day    select * 
->          FROM
->            seq_date
->          ) X
->          LIMIT 10;
+------------+
| log_date   |
+------------+
| 2020-01-01 |
| 2020-01-02 |
| 2020-01-03 |
| 2020-01-04 |
| 2020-01-05 |
| 2020-01-06 |
| 2020-01-07 |
| 2020-01-08 |
| 2020-01-09 |
| 2020-01-10 |
+------------+
10 rows in set (0.00 sec)
`
WITH 表达式使用非常灵活，不同的场景可以有不同的写法，的确可以简化日常 SQL 的编写。