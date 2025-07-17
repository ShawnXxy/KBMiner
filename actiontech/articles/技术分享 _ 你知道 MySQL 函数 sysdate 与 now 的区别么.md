# 技术分享 | 你知道 MySQL 函数 sysdate() 与 now() 的区别么？

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e4%bd%a0%e7%9f%a5%e9%81%93-mysql-%e5%87%bd%e6%95%b0-sysdate-%e4%b8%8e-now-%e7%9a%84%e5%8c%ba%e5%88%ab%e4%b9%88%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2023-12-20T00:03:46-08:00

---

作者对两个与时间相关的函数在运行机制和运维技巧上进行了全面的对比。
> 作者：余振兴，爱可生 DBA 团队成员，热衷技术分享、编写技术文档。
作者：陈伟，爱可生 DBA 团队成员，负责 MySQL 日常维护及故障处理。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 1400 字，预计阅读需要 4 分钟。
# 背景
在客户现场优化一批监控 SQL 时，发现一批 SQL 使用 `sysdate()` 作为统计数据的查询范围值，执行效率十分低下，查看执行计划发现不能使用到索引，而改为 `now()` 函数后则可以正常使用索引，以下是对该现象的分析。
> 内心小 ps 一下：`sysdate()` 的和 `now()` 的区别这是个⽼问题了。
# 函数 sysdate 与 now 的区别
下面我们来详细了解一下函数 `sysdate()` 与 `now()` 的区别，我们可以去[官方文档](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html) 查找他们两者之间的详细说明。
根据官方说明如下：
- `now()` 函数返回的是一个常量时间，该时间为语句开始执行的时间。即当存储函数或触发器中调用到 `now()` 函数时，`now()` 会返回存储函数或触发器语句开始执行的时间。
- `sysdate()` 函数则返回的是该语句执行的确切时间。
下面我们通过官方提供的案例直观展现两者区别。
`mysql> SELECT NOW(), SLEEP(2), NOW();
+---------------------+----------+---------------------+
| NOW()               | SLEEP(2) | NOW()               |
+---------------------+----------+---------------------+
| 2023-12-14 15:13:09 |        0 | 2023-12-14 15:13:09 |
+---------------------+----------+---------------------+
1 row in set (2.00 sec)
mysql> SELECT SYSDATE(), SLEEP(2), SYSDATE();
+---------------------+----------+---------------------+
| SYSDATE()           | SLEEP(2) | SYSDATE()           |
+---------------------+----------+---------------------+
| 2023-12-14 15:13:19 |        0 | 2023-12-14 15:13:21 |
+---------------------+----------+---------------------+
1 row in set (2.00 sec)
`
通过上面的两条 SQL 我们可以发现，当 SQL 语句两次调用 `now()` 函数时，前后两次 `now()` 函数返回的是相同的时间，而当 SQL 语句两次调用 `sysdate()` 函数时，前后两次 `sysdate()` 函数返回的时间在更新。
到这里我们根据官方文档的说明加上自己的推测大概可以知道，**函数`sysdate()` 之所以不能使用索引是因为 `sysdate()` 的不确定性导致索引不能用于评估引用它的表达式。**
# 测试示例
以下通过示例模拟客户类似场景。
我们先创建⼀张测试表，对 `create_time` 字段创建索引并插入数据，观测函数 `sysdate()` 和 `now()` 使⽤索引的情况。
`mysql> create table t1(
->   id int primary key auto_increment,
->   create_time datetime default current_timestamp,
->   uname varchar(20),
->   key idx_create_time(create_time)
-> );
Query OK, 0 rows affected (0.02 sec)
mysql> insert into t1(id) values(null),(null),(null);
Query OK, 3 rows affected (0.01 sec)
Records: 3  Duplicates: 0  Warnings: 0
mysql> insert into t1(id) values(null),(null),(null);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
mysql> select * from t1;
+----+---------------------+-------+
| id | create_time         | uname |
+----+---------------------+-------+
|  1 | 2023-12-14 15:34:30 | NULL  |
|  2 | 2023-12-14 15:34:30 | NULL  |
|  3 | 2023-12-14 15:34:30 | NULL  |
|  4 | 2023-12-14 15:34:37 | NULL  |
|  5 | 2023-12-14 15:34:37 | NULL  |
|  6 | 2023-12-14 15:34:37 | NULL  |
+----+---------------------+-------+
6 rows in set (0.00 sec)
`
先来看看函数 `sysdate()` 使⽤索引的情况。可以发现 `possible_keys` 和 `key` 均为 NULL，确实使⽤不了索引。
`mysql> explain select * from t1 where create_time<sysdate()\G
*************************** 1. row ***************************
id: 1
select_type: SIMPLE
table: t1
partitions: NULL
type: ALL
possible_keys: NULL
key: NULL
key_len: NULL
ref: NULL
rows: 6
filtered: 33.33
Extra: Using where
1 row in set, 1 warning (0.00 sec)
`
再来看看函数 `now()` 使⽤索引的情况，可以看到 `key` 使⽤到了 `idx_create_time` 这个索引。
`mysql> explain select * from t1 where create_time<now()\G
*************************** 1. row ***************************
id: 1
select_type: SIMPLE
table: t1
partitions: NULL
type: range
possible_keys: idx_create_time
key: idx_create_time
key_len: 6
ref: NULL
rows: 6
filtered: 100.00
Extra: Using index condition
1 row in set, 1 warning (0.00 sec)
`
# 示例详解
下面我们进一步通过 trace 去分析优化器对于函数 `now()` 和 `sysdate()` 具体是如何去优化的。
### 函数 sysdate() 部分关键 trace 输出
`"rows_estimation": [                  
## 估算使用各个索引进行范围扫描的成本
{
"table": "`t1`",
"range_analysis": {
"table_scan": {
"rows": 6,
"cost": 2.95
},
"potential_range_indexes": [
{
"index": "PRIMARY",
"usable": false,
"cause": "not_applicable"
},
{
"index": "idx_create_time",
"usable": true,
"key_parts": [
"create_time",
"id"
............................................
"setup_range_conditions": [
],
"group_index_range": {
"chosen": false,
"cause": "not_group_by_or_distinct"
},
"skip_scan_range": {
"chosen": false,
"cause": "disjuntive_predicate_present"
}
............................................
"considered_execution_plans": [       
## 对比各可行计划的代价，选择相对最优的执行计划
{
"plan_prefix": [
],
"table": "`t1`",
"best_access_path": {
"considered_access_paths": [
{
"rows_to_scan": 6,
"access_type": "scan",
"resulting_rows": 6,
"cost": 0.85,
"chosen": true
}
]
},
"condition_filtering_pct": 100,
"rows_for_plan": 6,
"cost_for_plan": 0.85,
"chosen": true
............................................
`
### 函数 now() 部分关键 trace 输出
```
"rows_estimation": [                  
## 估算使用各个索引进行范围扫描的成本
............................................
"analyzing_range_alternatives": {
"range_scan_alternatives": [
{
"index": "idx_create_time",
"ranges": [
"NULL < create_time < '2023-12-14 15:48:39'"
],
"index_dives_for_eq_ranges": true,
"rowid_ordered": false,
"using_mrr": false,
"index_only": false,
"in_memory": 1,
"rows": 6,
"cost": 2.36,
"chosen": true
}
],
............................................
},
"chosen_range_access_summary": {
"range_access_plan": {
"type": "range_scan",
"index": "idx_create_time",
"rows": 6,
"ranges": [
"NULL < create_time < '2023-12-14 15:48:39'"
]
},
"rows_for_plan": 6,
"cost_for_plan": 2.36,
"chosen": true
.............................................
"considered_execution_plans": [      
## 对比各可行计划的代价，选择相对最优的执行计划                            
{
"plan_prefix": [
],
"table": "`t1`",
"best_access_path": {
"considered_access_paths": [
{
"rows_to_scan": 6,
"access_type": "range",
"range_details": {
"used_index": "idx_create_time"
},
"resulting_rows": 6,
"cost": 2.96,
"chosen": true
}
]
},
"condition_filtering_pct": 100,
"rows_for_plan": 6,
"cost_for_plan": 2.96,
"chosen": true
.............................................
```
通过上述 trace 输出，我们可以发现对于函数 `now()`，优化器在 `rows_estimation` 时即估算使用各个索引进行范围扫描的成本这一步时可以将 `now()` 的值转换为一个常量，最终在 `considered_execution_plans` 这一步去对比各可行计划的代价，选择相对最优的执行计划。而通过函数 `sysdate()` 时则无法做到该优化，因为 `sysdate()` 是动态获取的时间。
# 总结
通过实际验证执行计划和 trace 记录并结合官方文档的说明，我们可以做以下理解。
- 函数 `now()` 是语句一开始执行时就获取时间（常量时间），优化器进行 SQL 解析时，已经能确认 `now()` 的具体返回值并可以将其当做一个已确定的常量去做优化。
- 函数 `sysdate()` 则是执行时动态获取时间（为该语句执行的确切时间），所以在优化器对 SQL 解析时是不能确定其返回值是多少，从而不能做 SQL 优化和评估，也就导致优化器只能选择对该条件做全表扫描。