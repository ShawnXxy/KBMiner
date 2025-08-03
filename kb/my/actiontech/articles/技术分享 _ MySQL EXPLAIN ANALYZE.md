# 技术分享 | MySQL EXPLAIN ANALYZE

**原文链接**: https://opensource.actionsky.com/20191025-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-25T02:06:39-08:00

---

> 作者：Norvald H. Ryeng  译：徐轶韬
**本文转载自公众号：****MySQL解决方案工程师**
MySQL 8.0.18 刚刚发布，它包含一个全新的功能 EXPLAIN ANALYZE，用来分析和理解查询如何执行。
**EXPLAIN ANALYZE 是什么？**EXPLAIN ANALYZE 是一个用于查询的分析工具，它向用户显示 MySQL 在查询上花费的时间以及原因。它将产生查询计划，并对其进行检测和执行，同时计算行数并度量执行计划中不同点上花费的时间。执行完成后，EXPLAIN ANALYZE 将输出计划和度量结果，而不是查询结果。这项新功能建立在常规的 EXPLAIN 基础之上，可以看作是 MySQL 8.0 之前添加的 EXPLAIN FORMAT = TREE 的扩展。EXPLAIN 除了输出查询计划和估计成本之外，EXPLAIN ANALYZE 还会输出执行计划中各个迭代器的实际成本。
## 如何使用？
我们将使用 Sakila 样本数据库中的数据和一个查询举例说明，该查询列出了每个工作人员在 2005 年 8 月累积的总金额。查询非常简单：- `mysql>SELECT first_name, last_name, SUM(amount) AS total`
- `FROM staff INNER JOIN payment`
- `  ON staff.staff_id = payment.staff_id`
- `     AND`
- `     payment_date LIKE '2005-08%'`
- `GROUP BY first_name, last_name;`
- 
- `+------------+-----------+----------+`
- `| first_name | last_name | total    |`
- `+------------+-----------+----------+`
- `| Mike       | Hillyer   | 11853.65 |`
- `| Jon        | Stephens  | 12218.48 |`
- `+------------+-----------+----------+`
- `2 rows in set (0,02 sec)`
只有两个人，Mike 和 Jon，我们在 2005 年 8 月获得了他们的总数。
EXPLAIN FORMAT = TREE 将向我们显示查询计划和成本估算：
- `mysql>EXPLAIN FORMAT=TREE`
- `mysql>SELECT first_name, last_name, SUM(amount) AS total`
- `FROM staff INNER JOIN payment`
- `  ON staff.staff_id = payment.staff_id`
- `     AND`
- `     payment_date LIKE '2005-08%'`
- `GROUP BY first_name, last_name;`
- 
- `-> Table scan on <temporary>`
- `    -> Aggregate using temporary table`
- `        -> Nested loop inner join  (cost=1757.30 rows=1787)`
- `            -> Table scan on staff  (cost=3.20 rows=2)`
- `            -> Filter: (payment.payment_date like '2005-08%')  (cost=117.43 rows=894)`
- `                -> Index lookup on payment using idx_fk_staff_id (staff_id=staff.staff_id)  (cost=117.43 rows=8043)`
但这并不能表明这些估计是否正确，或者查询计划实际上是在哪些操作上花费的时间。EXPLAIN ANALYZE 将执行以下操作：- `mysql>EXPLAIN ANALYZE`
- `mysql>SELECT first_name, last_name, SUM(amount) AS total`
- `FROM staff INNER JOIN payment`
- `  ON staff.staff_id = payment.staff_id`
- `     AND`
- `     payment_date LIKE '2005-08%'`
- `GROUP BY first_name, last_name;`
- 
- `-> Table scan on <temporary>  (actual time=0.001..0.001 rows=2 loops=1)`
- `    -> Aggregate using temporary table  (actual time=58.104..58.104 rows=2 loops=1)`
- `        -> Nested loop inner join  (cost=1757.30 rows=1787) (actual time=0.816..46.135 rows=5687 loops=1)`
- `            -> Table scan on staff  (cost=3.20 rows=2) (actual time=0.047..0.051 rows=2 loops=1)`
- `            -> Filter: (payment.payment_date like '2005-08%')  (cost=117.43 rows=894) (actual time=0.464..22.767 rows=2844 loops=2)`
- `                -> Index lookup on payment using idx_fk_staff_id (staff_id=staff.staff_id)  (cost=117.43 rows=8043) (actual time=0.450..19.988 rows=8024 loops=2)`
这里有几个新的度量：
- 获取第一行的实际时间（以毫秒为单位）
- 获取所有行的实际时间（以毫秒为单位）
- 实际读取的行数
- 实际循环数
让我们看一个具体的示例，使用过滤条件的迭代器成本估算和实际度量，该迭代器过滤 2005 年 8 月的数据（上面 EXPLAIN ANALYZE 输出中的第 13 行）。- `Filter: (payment.payment_date like '2005-08%')`
- `(cost=117.43 rows=894)`
- `(actual time=0.464..22.767 rows=2844 loops=2)`
我们的过滤器的估计成本为 117.43，并且估计返回 894 行。这些估计是由查询优化器根据可用统计信息在执行查询之前进行的。该信息也会在 EXPLAIN FORMAT = TREE 输出中。
我们将从最后面的循环数开始。此过滤迭代器的循环数为 2。这是什么意思？要了解此数字，我们必须查看查询计划中过滤迭代器上方的内容。在第 11 行上，有一个嵌套循环联接，在第 12 行上，是在staff 表上进行表扫描。这意味着我们正在执行嵌套循环连接，在其中扫描 staff 表，然后针对该表中的每一行，使用索引查找和过滤的付款日期来查找 payment 表中的相应条目。由于 staff 表中有两行（Mike 和 Jon），因此我们在第 14 行的索引查找上获得了两个循环迭代。
对于许多人来说，EXPLAIN ANALYZE 提供的最有趣的新信息是实际时间“ 0.464..22.767”，这意味着平均花费 0.464 毫秒读取第一行，而花费 22.767 毫秒读取所有行。平均时间？是的，由于存在循环，我们必须对该迭代器进行两次计时，并且报告的数字是所有循环迭代的平均值。这意味着过滤的实际执行时间是这些数字的两倍。如果我们看一下在嵌套循环迭代器（第 11 行）中上一级接收所有行的时间，为 46.135 毫秒，这是运行一次过滤迭代器的时间的两倍多。
这个时间反映了整个子树在执行过滤操作时的根部时间，即，使用索引查找迭代器读取行，然后评估付款日期为 2005 年 8 月的时间。如果我们查看索引循环迭代器（第 14 行），我们看到相应的数字分别为 0.450 和 19.988ms。这意味着大部分时间都花在了使用索引查找来读取行上，并且与读取数据相比，实际的过滤成本相对低廉。
实际读取的行数为 2844，而估计为 894 行。优化器错过了 3 倍的因素。同样，由于循环，估计值和实际值都是所有循环迭代的平均值。如果我们查看 schema，发现 payment_date 列上没有索引或直方图，因此提供给优化器的统计信息是有限的。如果使用更好的统计信息可以得出更准确的估计值，我们可以再次查看索引查找迭代器。我们看到该索引提供了更加准确的统计信息：估计 8043 行与 8024 实际读取行。发生这种情况是因为索引附带了额外的统计信息，而这些数据对于非索引列是不存在的。
那么用户可以使用这些信息做什么？需要一定的练习，用户才可以分析查询并理解为什么它们表现不佳。但是，这里有一些帮助入门的简单提示：
- 如果疑惑为何花费这么长时间，请查看时间。执行时间花在哪里？
- 如果您想知道为什么优化器选择了该计划，请查看行计数器。如果估计的行数与实际的行数之间存在较大差异（即，几个数量级或更多），需要仔细看一下。优化器根据估算值选择计划，但是查看实际执行情况可能会告诉您，另一个计划会更好。
EXPLAIN ANALYZE 是 MySQL 查询分析工具里面的一个新工具：- 检查查询计划：EXPLAIN FORMAT = TREE
- 分析查询执行：EXPLAIN ANALYZE
- 了解计划选择：OPTIMIZER TRACE
希望您喜欢这个新功能，EXPLAIN ANALYZE 将帮助您分析和了解缓慢的查询。
**社区近期动态**
**No.1**
**DBLE 用户见面会 北京站**
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/默认标题_横版海报_2019.09.16.jpg)											
爱可生开源社区将在 2019 年 10 月 26 日迎来在北京的首场 DBLE 用户见面会，以线下**互动分享**的会议形式跟大家见面。
时间：10月26日 9:00 &#8211; 12:00 AM
地点：HomeCafe 上地店（北京市海淀区上地二街一号龙泉湖酒店对面）
重要提醒：
1. 同日下午还有 dbaplus 社群举办的沙龙：聚焦数据中台、数据架构与优化。
2. 爱可生开源社区会在每年10.24日开源一款高质量产品。本次在 dbaplus 沙龙会议上，爱可生的资深研发工程师闫阿龙，将为大家带来《金融分布式事务实践及txle概述》，并在现场开源。
**No.2**
**「3306π」成都站 Meetup**
知数堂将在 2019 年 10 月 26 日在成都举办线下会议，本次会议中邀请了五位数据库领域的资深研发/DBA进行主题分享。
时间：2019年10月26日 13:00-18:00
地点：成都市高新区天府三街198号腾讯成都大厦A座多功能厅
**No.3**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
- 技术交流群，进群后可提问
QQ群（669663113）
- 社区通道，邮件&电话
osc@actionsky.com
- 现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.4**
**社区技术内容征稿**
征稿内容：
- 格式：.md/.doc/.txt
- 主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
- 要求：原创且未发布过
- 奖励：作者署名；200元京东E卡+社区周边
投稿方式：
- 邮箱：osc@actionsky.com
- 格式：[投稿]姓名+文章标题
- 以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系