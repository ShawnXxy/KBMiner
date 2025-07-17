# 新特性解读 | MySQL 8.0 索引特性3 -倒序索引

**原文链接**: https://opensource.actionsky.com/20190520-mysql8-0-index3/
**分类**: MySQL 新特性
**发布时间**: 2019-05-20T00:18:18-08:00

---

我们今天来介绍下MySQL 8.0 引入的新特性：倒序索引。
MySQL长期以来对索引的建立只允许正向asc存储，就算建立了desc，也是忽略掉。比如对于以下的查询，无法发挥索引的最佳性能。
- 查询一
`select * from tb1 where f1 = ... order by id desc;`
- 查询二
`select * from tb1 where f1 = ... order by f1 asc , f2 desc;`
那对于上面的查询，尤其是数据量和并发到一定峰值的时候，则对OS的资源消耗非常大。一般这样的SQL在查询计划里面会出现using filesort等状态。
比如针对下面的表t1，针对字段rank1有两个索引，一个是正序的，一个是反序的。不过在MySQL 8.0 之前的版本都是按照正序来存储。
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片1.png)											
按照rank1 正向排序的执行计划，
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片2.png)											
按照rank1 反向排序的执行计划，
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片3-1024x353.png)											
从执行计划来看，反向比正向除了extra里多了Using temporary; Using filesort这两个，其他的一模一样。这两个就代表中间用到了临时表和排序，一般来说，凡是执行计划里用到了这两个的，性能几乎都不咋地。除非我这个临时表不太大，而用于排序的buffer 也足够大，那性能也不至于太差。那这两个选项到底对性能有多大影响呢？
我们分别执行这两个查询，并且查看MySQL的session级的status就大概能看出些许不同。
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片4-5.jpg)											
通过以上两张图，我们发现反向的比正向的多了很多个计数，比如通过扫描的记录数增加了10倍，而且还伴有10倍的临时表的读和写记录数。那这个开销是非常巨大的。那以上的查询是在MySQL5.7上运行的。
MySQL 8.0 给我们带来了倒序索引（Descending Indexes），也就是说反向存储的索引。 这里不要跟搜索引擎中的倒排索引混淆了，MySQL这里只是反向排序存储而已。不过这个倒序存储已经解决了很大的问题。我们再看下之前在MySQL5.7上运行的例子。
我们把数据导入到MySQL 8.0，
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片6.png)											
再把原来的索引变为倒序索引，
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片7.png)											
再次看下第二个SQL的查询计划，
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图片8-1024x378.png)											
很显然，用到了这个倒序索引 idx_rank1_desc，而这里的临时表等的信息消失了。
当然了，这里的组合比较多，比如我这张表的字段rank1,rank2两个可以任意组合，
- 组合一
`(rank1 asc,rank2 asc);`
- 组合二
`(rank1 desc,rank2 desc);`
- 组合三
`(rank1 asc,rank2 desc);`
- 组合四
`(rank1 desc,rank2 asc);`
我把这几个加上，
适合的查询比如
- 查询一
`Select * from t1 where rank1 = 11 order by rank2;`
- 查询二
`Select * from t1 where 1 order by rank1,rank2;`
- 查询三
Select * from t1 where 1 order by rank1 desc,rank2;
&#8230;
等等，我就不一一示范了。
**开源分布式中间件DBLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dble
技术交流群：669663113
**开源数据传输中间件DTLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dtle
技术交流群：852990221