# 新特性解读 | MySQL 8.0 窗口函数一次疑问解答

**原文链接**: https://opensource.actionsky.com/20220328-mysql8-0/
**分类**: MySQL 新特性
**发布时间**: 2022-03-27T22:03:16-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
记起来有一次去讲 MySQL 8.0 开发相关特性，在 QA 环节，有人对 MySQL 的几个非常用窗口函数有些困惑，当时现场给了一些示范并且做了详细的解答，今天我用几个简单例子分享下具体的用法。
有困惑的是这四个窗口函数（其实是因为我PPT里仅写了这四个窗口函数）：frist_value、last_value、nth_value、ntile 。
谈到这四个窗口函数的具体用法，特别是前两个，得先熟悉 MySQL 窗口函数的框架用法。这里提到的窗口函数框架，其实就是定义一个分组窗口的边界，边界可以是具体的行号，也可以是具体的行内容，以这个边界为起点或者终点，来展现分组内的过滤数据。详情见我之前的发稿：https://opensource.actionsky.com/20210125-mysql/
接下来我们来看看这四个窗口函数如何使用。
- 
##### first_value： 用来返回一个分组窗口里的第一行记录，也即排名第一的那行记录。
我们用表t1来示范，这张表里只有12行记录，其中每6行记录按照字段r1来分组。
`   localhost:ytt_new>select id,r1,r2 from t1;
+----+------+------+
| id | r1   | r2   |
+----+------+------+
|  1 |   10 |   20 |
|  2 |   10 |   30 |
|  3 |   10 |   40 |
|  4 |   10 |   50 |
|  5 |   10 |    2 |
|  6 |   10 |    3 |
|  7 |   11 |  100 |
|  8 |   11 |  101 |
|  9 |   11 |    1 |
| 10 |   11 |    3 |
| 11 |   11 |   10 |
| 12 |   11 |   20 |
+----+------+------+
12 rows in set (0.00 sec)
`
比如想拿到每个分组里的第一名（升序），可以用row_number()函数，我们来回顾下：
`   localhost:ytt_new>select r1,r2 from (select r1,r2,row_number() over(partition by r1 order by r2) as rn from t1) T where T.rn = 1;
+------+------+
| r1   | r2   |
+------+------+
|   10 |    2 |
|   11 |    1 |
+------+------+
2 rows in set (0.00 sec)
`
此时如果用first_value来实现，写法会更加简单：
`      localhost:ytt_new>select distinct r1,first_value(r2) over(partition by r1 order by r2) as first_r2 from t1;
+------+----------+
| r1   | first_r2 |
+------+----------+
|   10 |        2 |
|   11 |        1 |
+------+----------+
2 rows in set (0.00 sec)
`
- 
##### last_value： 和first_value相反，用来返回分组窗口里的最后一行记录，也即倒数第一的那行记录。
比如我取出对应分组内最后一行 r2 的值，如果用 last_value 函数，非常好实现，可结果和预期不一致：返回与字段 r2 本身等值的记录。
`   localhost:ytt_new>select distinct r1,last_value(r2) over(partition by r1 order by r2) 'last_r2' from  t1; +------+---------+
| r1   | last_r2 |
+------+---------+
|   10 |       2 |
|   10 |       3 |
|   10 |      20 |
|   10 |      30 |
|   10 |      40 |
|   10 |      50 |
|   11 |       1 |
|   11 |       3 |
|   11 |      10 |
|   11 |      20 |
|   11 |     100 |
|   11 |     101 |
+------+---------+
12 rows in set (0.01 sec)
`
究其原因是函数last_value的默认框架是 rows between unbounded preceding and current row 。这里默认框架意思是：限制窗口函数的取值边界为当前行和上限无穷大，所以对应的值就是当前行自己。
那正确的框架应该是什么样呢？正确的框架应该是让边界锁定整个分组的上下边缘，也即整个分组的上限与下限之间。所以正确的写法如下：
`   localhost:ytt_new>select distinct r1,last_value(r2) over(partition by r1 order by r2 RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as 'last_r2' from t1;
+------+---------+
| r1   | last_r2 |
+------+---------+
|   10 |      50 |
|   11 |     101 |
+------+---------+
2 rows in set (0.00 sec)
`
- 
##### nth_value： 用来返回分组内指定行的记录。
比如用nth_value函数来求分组内排名第一的记录：
`   localhost:ytt_new>select * from (select distinct r1,nth_value(r2,1) over(partition by r1 order by r2) 'first_r2' from  t1) T where T.first_r2 is not null;
+------+----------+
| r1   | first_r2 |
+------+----------+
|   10 |        2 |
|   11 |        1 |
+------+----------+
2 rows in set (0.00 sec)
`
这个函数的功能基本和函数row_number一致。不同的是row_number用来展示排名，而nth_value用来输入排名。
- 
##### ntile： 用来在分组内继续二次分组。
比如我想取出分组内排名前50%的记录，可以这样写：
`   localhost:ytt_new>select id,r1,r2 from (select id,r1,r2, ntile(2) over(partition by r1 order by r2) 'ntile
' from t1) T where T.ntile=1;
+----+------+------+
| id | r1   | r2   |
+----+------+------+
|  5 |   10 |    2 |
|  6 |   10 |    3 |
|  1 |   10 |   20 |
|  9 |   11 |    1 |
| 10 |   11 |    3 |
| 11 |   11 |   10 |
+----+------+------+
6 rows in set (0.00 sec)
`
这四个窗口函数，特别是 last_value 需要注意。 不过在大多数场景下，记住几个常用的窗口函数即可，比如 row_number()，rank() 等等。