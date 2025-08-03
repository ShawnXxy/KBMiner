# 技术分享 | MySQL 的 join_buffer_size 在内连接上的应用

**原文链接**: https://opensource.actionsky.com/20191101-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-11-01T01:20:04-08:00

---

本文详细介绍了 MySQL 参数 join_buffer_size 在 INNER JOIN 场景的使用，OUTER JOIN 不包含。在讨论这个 BUFFER 之前，我们先了解下 MySQL 的 INNER JOIN 分类。
如果按照检索的性能方式来细分，那么无论是两表 INNER JOIN 还是多表 INNER JOIN，都大致可以分为以下几类：
1. JOIN KEY 有索引，主键2. JOIN KEY 有索引，二级索引3. JOIN KEY 无索引今天主要针对第三种场景来分析，也是就全表扫的场景。
**回过头来看看什么是 join_buffer_size？**
JOIN BUFFER 是 MySQL 用来缓存以上第二、第三这两类 JOIN 检索的一个 BUFFER 内存区域块。一般建议设置一个很小的 GLOBAL 值，完了在 SESSION 或者 QUERY 的基础上来做一个合适的调整。
比如，默认的值为 512K， 想要临时调整为 1G。那么，
- `mysql>set session join_buffer_size = 1024 * 1024 * 1024;`
- `mysql>select * from ...;`
- `mysql>set session join_buffer_size=default;`
- `或者`
- `mysql>select /*+  set_var(join_buffer_size=1G) */ * from ...;`
接下来详细看下 JOIN BUFFER 的用法。
那么 MySQL 里针对 INNER JOIN 大致有以下几种算法，
**1. Nested-Loop Join 翻译过来就是嵌套循环连接，简称 NLJ。**
这种是 MySQL 里最简单、最容易理解的表关联算法。
比如，拿语句  select * from p1 join p2 using(r1)  来说，
先从表 p1 里拿出来一条记录 ROW1，完了再用 ROW1 遍历表 p2 里的每一条记录，并且字段 r1 来做匹配是否相同，以便输出；再次循环刚才的过程，直到两表的记录数对比完成为止。
那看下实际 SQL 的执行计划，
- `mysql> explain format=json select * from p1 inner join p2 as b using(r1)\G`
- `*************************** 1. row ***************************`
- `EXPLAIN: {`
- ` "query_block": {`
- `   "select_id": 1,`
- `   "cost_info": {`
- `     "query_cost": "1003179606.87"`
- `   },`
- `   "nested_loop": [`
- `     {`
- `       "table": {`
- `         "table_name": "b",`
- `         "access_type": "ALL",`
- `         "rows_examined_per_scan": 1000,`
- `         "rows_produced_per_join": 1000,`
- `         "filtered": "100.00",`
- `         "cost_info": {`
- `           "read_cost": "1.00",`
- `           "eval_cost": "100.00",`
- `           "prefix_cost": "101.00",`
- `           "data_read_per_join": "15K"`
- `         },`
- `         "used_columns": [`
- `           "id",`
- `           "r1",`
- `           "r2"`
- `         ]`
- `       }`
- `     },`
- `     {`
- `       "table": {`
- `         "table_name": "p1",`
- `         "access_type": "ALL",`
- `         "rows_examined_per_scan": 9979810,`
- `         "rows_produced_per_join": 997981014,`
- `         "filtered": "10.00",`
- `         "cost_info": {`
- `           "read_cost": "5198505.87",`
- `           "eval_cost": "99798101.49",`
- `           "prefix_cost": "1003179606.87",`
- `           "data_read_per_join": "14G"`
- `         },`
- `         "used_columns": [`
- `           "id",`
- `           "r1",`
- `           "r2"`
- `         ],`
- `         "attached_condition": "(`ytt_new`.`p1`.`r1` = `ytt_new`.`b`.`r1`)"`
- `       }`
- `     }`
- `   ]`
- ` }`
- `}`
- `1 row in set, 1 warning (0.00 sec)`
从上面的执行计划来看，表 p2 为第一张表（驱动表或者叫外表），第二张表为 p1，那 p2 需要遍历的记录数为 1000，同时 p1 需要遍历的记录数大概 1000W 条，那这条 SQL 要执行完成，就得对表 p1（内表）匹配 1000 次，对应的 read_cost 为 5198505.87。那如何才能减少表 p1 的匹配次数呢？那这个时候 JOIN BUFFER 就派上用处了
**2. Block Nested-Loop Join ，块嵌套循环，简称 BNLJ**
那 BNLJ 比 NLJ 来说，中间多了一块 BUFFER 来缓存外表的对应记录从而减少了外表的循环次数，也就减少了内表的匹配次数。还是那上面的例子来说，假设 join_buffer_size 刚好能容纳外表的对应 JOIN KEY 记录，那对表 p2 匹配次数就由 1000 次减少到 1 次，性能直接提升了 1000 倍。我们看下用到 BNLJ 的执行计划，- `mysql> explain format=json select * from p1 inner join p2 as b using(r1)\G`
- `*************************** 1. row ***************************`
- `EXPLAIN: {`
- ` "query_block": {`
- `   "select_id": 1,`
- `   "cost_info": {`
- `     "query_cost": "997986300.01"`
- `   },`
- `   "nested_loop": [`
- `     {`
- `       "table": {`
- `         "table_name": "b",`
- `         "access_type": "ALL",`
- `         "rows_examined_per_scan": 1000,`
- `         "rows_produced_per_join": 1000,`
- `         "filtered": "100.00",`
- `         "cost_info": {`
- `           "read_cost": "1.00",`
- `           "eval_cost": "100.00",`
- `           "prefix_cost": "101.00",`
- `           "data_read_per_join": "15K"`
- `         },`
- `         "used_columns": [`
- `           "id",`
- `           "r1",`
- `           "r2"`
- `         ]`
- `       }`
- `     },`
- `     {`
- `       "table": {`
- `         "table_name": "p1",`
- `         "access_type": "ALL",`
- `         "rows_examined_per_scan": 9979810,`
- `         "rows_produced_per_join": 997981014,`
- `         "filtered": "10.00",`
- `         "using_join_buffer": "Block Nested Loop",`
- `         "cost_info": {`
- `           "read_cost": "5199.01",`
- `           "eval_cost": "99798101.49",`
- `           "prefix_cost": "997986300.01",`
- `           "data_read_per_join": "14G"`
- `         },`
- `         "used_columns": [`
- `           "id",`
- `           "r1",`
- `           "r2"`
- `         ],`
- `         "attached_condition": "(`ytt_new`.`p1`.`r1` = `ytt_new`.`b`.`r1`)"`
- `       }`
- `     }`
- `   ]`
- ` }`
- `}`
- `1 row in set, 1 warning (0.00 sec)`
**上面的执行计划有两点信息，****第一：多了一条 &#8220;using_join_buffer&#8221;: &#8220;Block Nested Loop&#8221;****第二：read_cost 这块由之前的 5198505.87 减少到 5199.01**
**3. 最近 MySQL 8.0.18 发布，终于推出了新的 JOIN 算法 — HASH JOIN。******
MySQL 的 HASH JOIN 也是用了 JOIN BUFFER 来做缓存，但是和 BNLJ 不同的是，它在 JOIN BUFFER 中以外表为基础建立一张哈希表，内表通过哈希算法来跟哈希表进行匹配，hash join 也就是进一步减少内表的匹配次数。当然官方并没有说明详细的算法描述，以上仅代表个人臆想。那还是针对以上的 SQL，我们来看下执行计划。- `mysql> explain format=tree select * from p1 inner join p2 as b using(r1)\G`
- `*************************** 1. row ***************************`
- `EXPLAIN: -> Inner hash join (p1.r1 = b.r1)  (cost=997986300.01 rows=997981015)`
- `   -> Table scan on p1  (cost=105.00 rows=9979810)`
- `   -> Hash`
- `       -> Table scan on b  (cost=101.00 rows=1000)`
- 
- `1 row in set (0.00 sec)`
通过上面的执行计划看到，针对表 p2 建立一张哈希表，然后针对表 p1 来做哈希匹配。目前仅仅支持简单查看是否用了 HASH JOIN，而没有其他更多的信息展示。总结下，本文主要讨论 MySQL 的内表关联在没有任何索引的低效场景。其他的场景另外开篇。
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
技术交流群，进群后可提问
QQ群（669663113）
社区通道，邮件&电话
osc@actionsky.com
现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
格式：.md/.doc/.txt
主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
要求：原创且未发布过
奖励：作者署名；200元京东E卡+社区周边
投稿方式：
邮箱：osc@actionsky.com
格式：[投稿]姓名+文章标题
以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系