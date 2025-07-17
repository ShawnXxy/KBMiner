# 新特性解读 | MySQL 8.0 直方图

**原文链接**: https://opensource.actionsky.com/20190603-mysql8-histogram/
**分类**: MySQL 新特性
**发布时间**: 2019-06-03T17:52:18-08:00

---

MySQL 8.0 推出了histogram，也叫柱状图或者直方图。先来解释下什么叫直方图。
### 直方图的定义
我们知道，在DB中，优化器负责将SQL转换为很多个不同的执行计划，完了从中选择一个最优的来实际执行。但是有时候优化器选择的最终计划有可能随着DB环境的变化不是最优的，这就导致了查询性能不是很好。比如，优化器无法准确的知道每张表的实际行数以及参与过滤条件的列有多少个不同的值。那其实有时候有人就说了，索引不是可以解决这个问题吗？是的，不同类型的索引可以解决这个问题，但是你不能每个列都建索引吧？如果一张表有1000个字段，那全字段索引将会拖死对这张表的写入。而此时，直方图就是相对来说，开销较小的方法。
直方图就是在 MySQL 中为某张表的某些字段提供了一种数值分布的统计信息。比如字段NULL的个数，每个不同值出现的百分比，最大值，最小值等等。如果我们用过了 MySQL 的分析型引擎brighthouse，那对这个概念太熟悉了。
MySQL的直方图有两种，等宽直方图和等高直方图。等宽直方图每个桶（bucket）保存一个值以及这个值累积频率；等高直方图每个桶需要保存不同值的个数，上下限以及累计频率等。MySQL会自动分配用哪种类型的直方图，我们无需参与。
MySQL 定义了一张meta表column_statistics 来存储直方图的定义，每行记录对应一个字段的直方图，以json保存。同时，新增了一个参数histogram_generation_max_mem_size来配置建立直方图内存大小。
**不过直方图有以下限制：**
1.不支持几何类型以及json。
2.不支持加密表和临时表。
3.不支持列值完全唯一。
4.需要手工的进行键值分布。
那我们来举个简单的例子说明直方图对查询的效果提升。
### 举例
表相关定义以及行数信息等：
`mysql> show create table t2\G
*************************** 1. row ***************************
Table: t2
Create Table: CREATE TABLE `t2` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`rank1` int(11) DEFAULT NULL,
`rank2` int(11) DEFAULT NULL,
`rank3` int(11) DEFAULT NULL,
`log_date` date DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_rank1` (`rank1`),
KEY `idx_log_date` (`log_date`)
) ENGINE=InnoDB AUTO_INCREMENT=49140 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci STATS_PERSISTENT=1 STATS_AUTO_RECALC=0
1 row in set (0.00 sec)
mysql> select count(*) from t2;
+----------+
| count(*) |
+----------+
|    30940 |
+----------+
1 row in set (0.00 sec)
`
同时对t2克隆了一张表t3。
`mysql> create table t3 like t2;
Query OK, 0 rows affected (0.13 sec)
mysql> insert into t3 select * from t2;
Query OK, 30940 rows affected (1.94 sec)
Records: 30940  Duplicates: 0  Warnings: 0
`
给表t3列rank1和log_date 添加histogram。
`mysql> analyze table t3 update histogram on rank1,log_date;
+--------+-----------+----------+-----------------------------------------------------+
| Table  | Op        | Msg_type | Msg_text                                            |
+--------+-----------+----------+-----------------------------------------------------+
| ytt.t3 | histogram | status   | Histogram statistics created for column 'log_date'. |
| ytt.t3 | histogram | status   | Histogram statistics created for column 'rank1'.    |
+--------+-----------+----------+-----------------------------------------------------+
2 rows in set (0.19 sec)
`
我们来看看histogram的分布状况。
`mysql> select json_pretty(histogram)  result from information_schema.column_statistics where table_name = 't3' and column_name = 'log_date'\G
*************************** 1. row ***************************
result: {
"buckets": [
[
"2018-04-17",
"2018-04-20",
0.01050420168067227,
4
],
...
,
[
"2019-04-14",
"2019-04-16",
1.0,
3
]
],
"data-type": "date",
"null-values": 0.0,
"collation-id": 8,
"last-updated": "2019-04-17 03:43:01.910185",
"sampling-rate": 1.0,
"histogram-type": "equi-height",
"number-of-buckets-specified": 100
}
1 row in set (0.03 sec)
`
MySQL自动为这个字段分配了等高直方图，默认为100个桶。
SQL A：
`select count(*) from t2/t3 where (rank1 between 1 and 10) and log_date < '2018-09-01';
`
SQL A的执行结果：
`mysql> select count(*) from t2/t3 where (rank1 between 1 and 10) and log_date < '2018-09-01';
+----------+
| count(*) |
+----------+
|     2269 |
+----------+
1 row in set (0.01 sec)
`
**无histogram的执行计划。**
`mysql> explain format=json select count(*) from t2 where (rank1 between 1 and 10) and log_date < '2018-09-01'\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "2796.11"
},
"table": {
"table_name": "t2",
"access_type": "range",
"possible_keys": [
"idx_rank1",
"idx_log_date"
],
"key": "idx_rank1",
"used_key_parts": [
"rank1"
],
"key_length": "5",
"rows_examined_per_scan": 6213,
"rows_produced_per_join": 3106,
"filtered": "50.00",
"index_condition": "(`ytt`.`t2`.`rank1` between 1 and 10)",
"cost_info": {
"read_cost": "2485.46",
"eval_cost": "310.65",
"prefix_cost": "2796.11",
"data_read_per_join": "72K"
},
"used_columns": [
"rank1",
"log_date"
],
"attached_condition": "(`ytt`.`t2`.`log_date` < '2018-09-01')"
}
}
}
`
**有histogram的执行计划。**
`mysql> explain format=json select count(*) from t3 where (rank1 between 1 and 10) and log_date < '2018-09-01'\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "0.71"
},
"table": {
"table_name": "t3",
"access_type": "range",
"possible_keys": [
"idx_rank1",
"idx_log_date"
],
"key": "idx_log_date",
"used_key_parts": [
"log_date"
],
"key_length": "4",
"rows_examined_per_scan": 1,
"rows_produced_per_join": 1,
"filtered": "100.00",
"index_condition": "(`ytt`.`t3`.`log_date` < '2018-09-01')",
"cost_info": {
"read_cost": "0.61",
"eval_cost": "0.10",
"prefix_cost": "0.71",
"data_read_per_join": "24"
},
"used_columns": [
"rank1",
"log_date"
],
"attached_condition": "(`ytt`.`t3`.`rank1` between 1 and 10)"
}
}
}
1 row in set, 1 warning (0.00 sec)
`
我们看到两个执行计划的对比，有Histogram的执行计划cost比普通的sql快了好多倍。  上面文字可以看起来比较晦涩，贴上两张图，看起来就很简单了。
无histogram
![](https://opensource.actionsky.com/wp-content/uploads/2019/06/无-300x225.png)
有histogram
![](https://opensource.actionsky.com/wp-content/uploads/2019/06/有-300x281.png)
当然，我这里举得例子相对简单，有兴趣的朋友可以更深入学习其他复杂些的例子。
**近期社区动态**
[**6月15日 上海站**](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247484378&idx=1&sn=188de93431ba9461a2fb7072d125baa3&chksm=fc96e145cbe1685302a6a941300ca01f75ad3abd0ef58e650136883cb51163d4baf76ea720c9&scene=21#wechat_redirect)
**[分布式中间件DBLE用户见面会](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247484378&idx=1&sn=188de93431ba9461a2fb7072d125baa3&chksm=fc96e145cbe1685302a6a941300ca01f75ad3abd0ef58e650136883cb51163d4baf76ea720c9&scene=21#wechat_redirect) **
**本次举办的DBLE用户见面会，是自2017年10月24日数据库中间件DBLE发布以来，首次线下互动式分享会议**。 
来爱可生总部研发中心，与研发、测试、产品、社区团队面对面，遇到志同道合的朋友，更有丰富精美的周边产品等着你！ 
**会议时间：2019年06月15日13:00—17:00 **
**会议地点：爱可生研发中心，上海市徐汇区虹梅路1905号远中科研楼甲幢7层**  
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/默认标题_宣传单_2019.05.06-1-760x1024.jpg)