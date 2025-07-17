# 新特性解读 | MySQL 8.0 新增HINT模式

**原文链接**: https://opensource.actionsky.com/20190513-mysql8-0-hint/
**分类**: MySQL 新特性
**发布时间**: 2019-05-13T02:07:28-08:00

---

在开始演示之前，我们先介绍下两个概念。
#### 概念一，数据的可选择性基数，也就是常说的cardinality值。
查询优化器在生成各种执行计划之前，得先从统计信息中取得相关数据，这样才能估算每步操作所涉及到的记录数，而这个相关数据就是cardinality。简单来说，就是每个值在每个字段中的唯一值分布状态。
比如表t1有100行记录，其中一列为f1。f1中唯一值的个数可以是100个，也可以是1个，当然也可以是1到100之间的任何一个数字。这里唯一值越的多少，就是这个列的可选择基数。那看到这里我们就明白了，为什么要在基数高的字段上建立索引，而基数低的的字段建立索引反而没有全表扫描来的快。当然这个只是一方面，至于更深入的探讨就不在我这篇探讨的范围了。
#### 概念二，关于HINT的使用。
这里我来说下HINT是什么，在什么时候用。
HINT简单来说就是在某些特定的场景下人工协助MySQL优化器的工作，使她生成最优的执行计划。一般来说，优化器的执行计划都是最优化的，不过在某些特定场景下，执行计划可能不是最优化。
比如：表t1经过大量的频繁更新操作，（UPDATE,DELETE,INSERT），cardinality已经很不准确了，这时候刚好执行了一条SQL,那么有可能这条SQL的执行计划就不是最优的。为什么说有可能呢？
#### 具体演示
**譬如，以下两条SQL，**
&#8211; A：
`select * from t1 where f1 = 20;
`
- B：
```
select * from t1 where f1 = 30;
```
如果f1的值刚好频繁更新的值为30，并且没有达到MySQL自动更新cardinality值的临界值或者说用户设置了手动更新又或者用户减少了sample page等等，那么对这两条语句来说，可能不准确的就是B了。
这里顺带说下，MySQL提供了自动更新和手动更新表cardinality值的方法，因篇幅有限，需要的可以查阅手册。
那回到正题上，MySQL 8.0 带来了几个HINT，我今天就举个index_merge的例子。
**示例表结构：**
`mysql> desc t1;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| rank1      | int(11)      | YES  | MUL | NULL    |                |
| rank2      | int(11)      | YES  | MUL | NULL    |                |
| log_time   | datetime     | YES  | MUL | NULL    |                |
| prefix_uid | varchar(100) | YES  |     | NULL    |                |
| desc1      | text         | YES  |     | NULL    |                |
| rank3      | int(11)      | YES  | MUL | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
7 rows in set (0.00 sec)
`
**表记录数：**
`mysql> select count(*) from t1;
+----------+
| count(*) |
+----------+
|    32768 |
+----------+
1 row in set (0.01 sec)
`
**这里我们两条经典的SQL：**
&#8211; SQL C:
`select * from t1 where rank1 = 1 or rank2 = 2 or rank3 = 2;
`
- SQL D：
```
select * from t1 where rank1 =100  and rank2 =100  and rank3 =100;
```
那表t1实际上在rank1，rank2，rank3三列上分别有一个二级索引。
**那我们来看SQL C的查询计划。**
显然，好像没有用到任何索引。扫描的行数为32034，cost为3243.65。
`mysql> explain  format=json select * from t1  where rank1 =1 or rank2 = 2 or rank3 = 2\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "3243.65"
},
"table": {
"table_name": "t1",
"access_type": "ALL",
"possible_keys": [
"idx_rank1",
"idx_rank2",
"idx_rank3"
],
"rows_examined_per_scan": 32034,
"rows_produced_per_join": 115,
"filtered": "0.36",
"cost_info": {
"read_cost": "3232.07",
"eval_cost": "11.58",
"prefix_cost": "3243.65",
"data_read_per_join": "49K"
},
"used_columns": [
"id",
"rank1",
"rank2",
"log_time",
"prefix_uid",
"desc1",
"rank3"
],
"attached_condition": "((`ytt`.`t1`.`rank1` = 1) or (`ytt`.`t1`.`rank2` = 2) or (`ytt`.`t1`.`rank3` = 2))"
}
}
}
1 row in set, 1 warning (0.00 sec)
`
**我们加上HINT给相同的查询，再次看看查询计划。**
这个时候用到了index_merge，union了三个列。扫描的行数为1103，cost为441.09，明显比之前的快了好几倍。
`mysql> explain  format=json select /*+ index_merge(t1) */ * from t1  where rank1 =1 or rank2 = 2 or rank3 = 2\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "441.09"
},
"table": {
"table_name": "t1",
"access_type": "index_merge",
"possible_keys": [
"idx_rank1",
"idx_rank2",
"idx_rank3"
],
"key": "union(idx_rank1,idx_rank2,idx_rank3)",
"key_length": "5,5,5",
"rows_examined_per_scan": 1103,
"rows_produced_per_join": 1103,
"filtered": "100.00",
"cost_info": {
"read_cost": "330.79",
"eval_cost": "110.30",
"prefix_cost": "441.09",
"data_read_per_join": "473K"
},
"used_columns": [
"id",
"rank1",
"rank2",
"log_time",
"prefix_uid",
"desc1",
"rank3"
],
"attached_condition": "((`ytt`.`t1`.`rank1` = 1) or (`ytt`.`t1`.`rank2` = 2) or (`ytt`.`t1`.`rank3` = 2))"
}
}
}
1 row in set, 1 warning (0.00 sec)
`
**我们再看下SQL D的计划：**
- 不加HINT，
`mysql> explain format=json select * from t1 where rank1 =100 and rank2 =100 and rank3 =100\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "534.34"
},
"table": {
"table_name": "t1",
"access_type": "ref",
"possible_keys": [
"idx_rank1",
"idx_rank2",
"idx_rank3"
],
"key": "idx_rank1",
"used_key_parts": [
"rank1"
],
"key_length": "5",
"ref": [
"const"
],
"rows_examined_per_scan": 555,
"rows_produced_per_join": 0,
"filtered": "0.07",
"cost_info": {
"read_cost": "478.84",
"eval_cost": "0.04",
"prefix_cost": "534.34",
"data_read_per_join": "176"
},
"used_columns": [
"id",
"rank1",
"rank2",
"log_time",
"prefix_uid",
"desc1",
"rank3"
],
"attached_condition": "((`ytt`.`t1`.`rank3` = 100) and (`ytt`.`t1`.`rank2` = 100))"
}
}
}
1 row in set, 1 warning (0.00 sec)
`
- 加了HINT，
```
mysql> explain format=json select /*+ index_merge(t1)*/ * from t1 where rank1 =100 and rank2 =100 and rank3 =100\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "5.23"
},
"table": {
"table_name": "t1",
"access_type": "index_merge",
"possible_keys": [
"idx_rank1",
"idx_rank2",
"idx_rank3"
],
"key": "intersect(idx_rank1,idx_rank2,idx_rank3)",
"key_length": "5,5,5",
"rows_examined_per_scan": 1,
"rows_produced_per_join": 1,
"filtered": "100.00",
"cost_info": {
"read_cost": "5.13",
"eval_cost": "0.10",
"prefix_cost": "5.23",
"data_read_per_join": "440"
},
"used_columns": [
"id",
"rank1",
"rank2",
"log_time",
"prefix_uid",
"desc1",
"rank3"
],
"attached_condition": "((`ytt`.`t1`.`rank3` = 100) and (`ytt`.`t1`.`rank2` = 100) and (`ytt`.`t1`.`rank1` = 100))"
}
}
}
1 row in set, 1 warning (0.00 sec)
```
对比下以上两个，加了HINT的比不加HINT的cost小了100倍。
> 
总结下，就是说表的cardinality值影响这张的查询计划，如果这个值没有正常更新的话，就需要手工加HINT了。
相信MySQL未来的版本会带来更多的HINT。
**开源分布式中间件DBLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dble
技术交流群：669663113
**开源数据传输中间件DTLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dtle
技术交流群：852990221
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/默认标题_宣传单_2019.05.06-1-223x300.jpg)