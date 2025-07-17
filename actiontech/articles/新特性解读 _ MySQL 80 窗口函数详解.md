# 新特性解读 | MySQL 8.0 窗口函数详解

**原文链接**: https://opensource.actionsky.com/20190625-mysql8-window/
**分类**: MySQL 新特性
**发布时间**: 2019-06-25T01:45:40-08:00

---

## 背景
一直以来，MySQL 只有针对聚合函数的汇总类功能，比如MAX, AVG 等，没有从 SQL 层针对聚合类每组展开处理的功能。不过 MySQL 开放了 UDF 接口，可以用 C 来自己写UDF，这个就增加了功能行难度。
这种针对每组展开处理的功能就叫窗口函数，有的数据库叫分析函数。
在 MySQL 8.0 之前，我们想要得到这样的结果，就得用以下几种方法来实现：
**1. session 变量**
**2. group_concat 函数组合**
**3. 自己写 store routines**
接下来我们用经典的 **学生/课程/成绩** 来做窗口函数演示
## 准备
**学生表**
mysql> show create table student \G
*************************** 1. row ***************************
Table: student
Create Table: CREATE TABLE student (
sid int(10) unsigned NOT NULL,
sname varchar(64) DEFAULT NULL,
PRIMARY KEY (sid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
**课程表**
mysql> show create table course\G
*************************** 1. row ***************************
Table: course
Create Table: CREATE TABLE `course` (
`cid` int(10) unsigned NOT NULL,
`cname` varchar(64) DEFAULT NULL,
PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
**成绩表**
mysql> show create table score\G
*************************** 1. row ***************************
Table: score
Create Table: CREATE TABLE `score` (
`sid` int(10) unsigned NOT NULL,
`cid` int(10) unsigned NOT NULL,
`score` tinyint(3) unsigned DEFAULT NULL,
PRIMARY KEY (`sid`,`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
**测试数据**
mysql> select * from student;
+-----------+--------------+
| sid | sname |
+-----------+--------------+
| 201910001 | 张三 |
| 201910002 | 李四 |
| 201910003 | 武松 |
| 201910004 | 潘金莲 |
| 201910005 | 菠菜 |
| 201910006 | 杨发财 |
| 201910007 | 欧阳修 |
| 201910008 | 郭靖 |
| 201910009 | 黄蓉 |
| 201910010 | 东方不败 |
+-----------+--------------+
10 rows in set (0.00 sec)
mysql> select * from score;;
+-----------+----------+-------+
| sid | cid | score |
+-----------+----------+-------+
| 201910001 | 20192001 | 50 |
| 201910001 | 20192002 | 88 |
| 201910001 | 20192003 | 54 |
| 201910001 | 20192004 | 43 |
| 201910001 | 20192005 | 89 |
| 201910002 | 20192001 | 79 |
| 201910002 | 20192002 | 97 |
| 201910002 | 20192003 | 82 |
| 201910002 | 20192004 | 85 |
| 201910002 | 20192005 | 80 |
| 201910003 | 20192001 | 48 |
| 201910003 | 20192002 | 98 |
| 201910003 | 20192003 | 47 |
| 201910003 | 20192004 | 41 |
| 201910003 | 20192005 | 34 |
| 201910004 | 20192001 | 81 |
| 201910004 | 20192002 | 69 |
| 201910004 | 20192003 | 67 |
| 201910004 | 20192004 | 99 |
| 201910004 | 20192005 | 61 |
| 201910005 | 20192001 | 40 |
| 201910005 | 20192002 | 52 |
| 201910005 | 20192003 | 39 |
| 201910005 | 20192004 | 74 |
| 201910005 | 20192005 | 86 |
| 201910006 | 20192001 | 42 |
| 201910006 | 20192002 | 52 |
| 201910006 | 20192003 | 36 |
| 201910006 | 20192004 | 58 |
| 201910006 | 20192005 | 84 |
| 201910007 | 20192001 | 79 |
| 201910007 | 20192002 | 43 |
| 201910007 | 20192003 | 79 |
| 201910007 | 20192004 | 98 |
| 201910007 | 20192005 | 88 |
| 201910008 | 20192001 | 45 |
| 201910008 | 20192002 | 65 |
| 201910008 | 20192003 | 90 |
| 201910008 | 20192004 | 89 |
| 201910008 | 20192005 | 74 |
| 201910009 | 20192001 | 73 |
| 201910009 | 20192002 | 42 |
| 201910009 | 20192003 | 95 |
| 201910009 | 20192004 | 46 |
| 201910009 | 20192005 | 45 |
| 201910010 | 20192001 | 58 |
| 201910010 | 20192002 | 52 |
| 201910010 | 20192003 | 55 |
| 201910010 | 20192004 | 87 |
| 201910010 | 20192005 | 36 |
+-----------+----------+-------+
50 rows in set (0.00 sec)
mysql> select
## MySQL 8.0 之前
比如我们求成绩排名前三的学生排名，我来举个用 session 变量和 group_concat 函数来分别实现的例子：
**session 变量方式**
每组开始赋一个初始值序号和初始分组字段。
SELECT 
b.cname,
a.sname,
c.score, c.ranking_score
FROM
student a,
course b,
(
SELECT
c.*,
IF(
@cid = c.cid,
@rn := @rn + 1,
@rn := 1
) AS ranking_score,
@cid := c.cid AS tmpcid
FROM
(
SELECT
*
FROM
score
ORDER BY cid,
score DESC
) c,
(
SELECT
@rn := 0 rn,
@cid := ''
) initialize_table 
) c
WHERE a.sid = c.sid
AND b.cid = c.cid
AND c.ranking_score <= 3
ORDER BY b.cname,c.ranking_score;
+------------+-----------+-------+---------------+
| cname | sname | score | ranking_score |
+------------+-----------+-------+---------------+
| dble | 张三 | 89 | 1 |
| dble | 欧阳修 | 88 | 2 |
| dble | 菠菜 | 86 | 3 |
| mongodb | 潘金莲 | 99 | 1 |
| mongodb | 欧阳修 | 98 | 2 |
| mongodb | 郭靖 | 89 | 3 |
| mysql | 李四 | 100 | 1 |
| mysql | 潘金莲 | 81 | 2 |
| mysql | 欧阳修 | 79 | 3 |
| oracle | 武松 | 98 | 1 |
| oracle | 李四 | 97 | 2 |
| oracle | 张三 | 88 | 3 |
| postgresql | 黄蓉 | 95 | 1 |
| postgresql | 郭靖 | 90 | 2 |
| postgresql | 李四 | 82 | 3 |
+------------+-----------+-------+---------------+
15 rows in set, 5 warnings (0.01 sec)
**group_concat 函数方式**
利用 findinset 内置函数来返回下标作为序号使用。
SELECT
*
FROM
(
SELECT
b.cname,
a.sname,
c.score,
FIND_IN_SET(c.score, d.gp) score_ranking
FROM
student a,
course b,
score c,
(
SELECT
cid,
GROUP_CONCAT(
score
ORDER BY score DESC SEPARATOR ','
) gp
FROM
score
GROUP BY cid
ORDER BY score DESC
) d
WHERE a.sid = c.sid
AND b.cid = c.cid
AND c.cid = d.cid
ORDER BY d.cid,
score_ranking
) ytt
WHERE score_ranking <= 3；
+------------+-----------+-------+---------------+
| cname | sname | score | score_ranking |
+------------+-----------+-------+---------------+
| dble | 张三 | 89 | 1 |
| dble | 欧阳修 | 88 | 2 |
| dble | 菠菜 | 86 | 3 |
| mongodb | 潘金莲 | 99 | 1 |
| mongodb | 欧阳修 | 98 | 2 |
| mongodb | 郭靖 | 89 | 3 |
| mysql | 李四 | 100 | 1 |
| mysql | 潘金莲 | 81 | 2 |
| mysql | 欧阳修 | 79 | 3 |
| oracle | 武松 | 98 | 1 |
| oracle | 李四 | 97 | 2 |
| oracle | 张三 | 88 | 3 |
| postgresql | 黄蓉 | 95 | 1 |
| postgresql | 郭靖 | 90 | 2 |
| postgresql | 李四 | 82 | 3 |
+------------+-----------+-------+---------------+
15 rows in set (0.00 sec)
## MySQL 8.0 窗口函数
MySQL 8.0 后提供了原生的窗口函数支持，语法和大多数数据库一样，比如还是之前的例子：
用 row_number() over () 直接来检索排名。
mysql>
 SELECT
*
FROM
(
SELECT
b.cname,
a.sname,
c.score,
row_number() over (
PARTITION BY b.cname
ORDER BY c.score DESC
) score_rank
FROM
student AS a,
course AS b,
score AS c
WHERE a.sid = c.sid
AND b.cid = c.cid
) ytt
WHERE score_rank <= 3;
+------------+-----------+-------+------------+
| cname | sname | score | score_rank |
+------------+-----------+-------+------------+
| dble | 张三 | 89 | 1 |
| dble | 欧阳修 | 88 | 2 |
| dble | 菠菜 | 86 | 3 |
| mongodb | 潘金莲 | 99 | 1 |
| mongodb | 欧阳修 | 98 | 2 |
| mongodb | 郭靖 | 89 | 3 |
| mysql | 李四 | 100 | 1 |
| mysql | 潘金莲 | 81 | 2 |
| mysql | 欧阳修 | 79 | 3 |
| oracle | 武松 | 98 | 1 |
| oracle | 李四 | 97 | 2 |
| oracle | 张三 | 88 | 3 |
| postgresql | 黄蓉 | 95 | 1 |
| postgresql | 郭靖 | 90 | 2 |
| postgresql | 李四 | 82 | 3 |
+------------+-----------+-------+------------+
15 rows in set (0.00 sec)
那我们再找出课程 MySQL 和 DBLE 里不及格的倒数前两名学生名单。
mysql> 
SELECT
*
FROM
(
SELECT
b.cname,
a.sname,
c.score,
row_number () over (
PARTITION BY b.cid
ORDER BY c.score ASC
) score_ranking
FROM
student AS a,
course AS b,
score AS c
WHERE a.sid = c.sid
AND b.cid = c.cid
AND b.cid IN (20192005, 20192001)
AND c.score < 60
) ytt
WHERE score_ranking < 3;
+-------+--------------+-------+---------------+
| cname | sname | score | score_ranking |
+-------+--------------+-------+---------------+
| mysql | 菠菜 | 40 | 1 |
| mysql | 杨发财 | 42 | 2 |
| dble | 武松 | 34 | 1 |
| dble | 东方不败 | 36 | 2 |
+-------+--------------+-------+---------------+
4 rows in set (0.00 sec)
到此为止，我们只是演示了row_number() over() 函数的使用方法，其他的函数有兴趣的朋友可以自己体验体验，方法都差不多。
## 
**                                                近期社区动态**
**
**
[**第三期 社区技术内容征稿**](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247484778&idx=2&sn=0050d6c324e4d958950d34a29c2f8994&chksm=fc96e7f5cbe16ee3eb36d47a15e19a89ed459c8d24588a080d1bb849dc6d5f0816a72aafe35f&scene=21#wechat_redirect)
**所有稿件，一经采用，均会为作者署名。**
**征稿主题：**MySQL、分布式中间件DBLE、数据传输组件DTLE相关的技术内容
**活动时间：**2019年6月11日 &#8211; 7月11日
**本期投稿奖励**
投稿成功：京东卡200元*1
优秀稿件：京东卡200元*1+社区定制周边（包含：定制文化衫、定制伞、鼠标垫）
**优秀稿件评选，文章获得****“好看****”****数量排名前三****的稿件为本期优秀稿件。**
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/征稿海报.jpg)