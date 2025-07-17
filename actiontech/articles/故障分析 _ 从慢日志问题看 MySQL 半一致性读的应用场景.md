# 故障分析 | 从慢日志问题看 MySQL 半一致性读的应用场景

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-%e4%bb%8e%e6%85%a2%e6%97%a5%e5%bf%97%e9%97%ae%e9%a2%98%e7%9c%8b-mysql-%e5%8d%8a%e4%b8%80%e8%87%b4%e6%80%a7%e8%af%bb%e7%9a%84%e5%ba%94%e7%94%a8%e5%9c%ba%e6%99%af/
**分类**: MySQL 新特性
**发布时间**: 2023-06-28T01:02:26-08:00

---

作者通过一个慢日志问题，引出 MySQL 半一致性读的概念及实际应用场景。
> 
作者：龚唐杰
爱可生 DBA 团队成员，主要负责 MySQL 技术支持，擅长 MySQL、PG、国产数据库。
本文来源：原创投稿
- 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# 背景
某系统执行更新操作发现很慢，发现有大量慢日志，其中 Lock time 时间占比很高，MySQL 版本为 5.7.25，隔离级别为 RR。
# 分析
查看表结构以及 `UPDATE` 语句的执行计划：
`mysql> show create table test;
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| test | CREATE TABLE `test` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(30) COLLATE utf8mb4_bin DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2621401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> explain update test set name ='test' where name='a';
+----+-------------+-------+------------+-------+---------------+---------+---------+------+---------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
+----+-------------+-------+------------+-------+---------------+---------+---------+------+---------+----------+-------------+
| 1  | UPDATE      | test  | NULL       | index | NULL   | PRIMARY | 4 | NULL | 2355988 | 100.00 | Using where |
+----+-------------+-------+------------+-------+---------------+---------+---------+------+---------+----------+-------------+
1 row in set (0.00 sec)
`
通过执行计划发现，该 SQL 是走的主键全索引扫描，并且对于 `name` 列未加索引，当多个事务同时执行时，就会观察到有阻塞出现。
| 事务1 | 事务2 |
| --- | --- |
| mysql> begin;  Query OK, 0 rows affected (0.00 sec)  mysql> update test set name =&#8217;test&#8217; where name=&#8217;a&#8217;;  Query OK, 262144 rows affected (4.67 sec)  Rows matched: 262144 Changed: 262144 Warnings: 0 |  |
|  | mysql> begin;  Query OK, 0 rows affected (0.00 sec)  mysql> update test set name =&#8217;test1&#8242; where name=&#8217;b&#8217;; |
若 `name` 列的重复值不多，那么可以对 `name` 列添加索引即可解决该问题。因为 InnoDB 的行锁机制是基于索引列来实现的，如果 `UPDATE` 语句能使用到 `name` 列的索引，那么就不会产生阻塞，导致业务卡顿。
但若是 `name` 列的值的区分度很低，就会导致 SQL 不会走 `name` 列的索引，示例如下：
### 先添加索引
`mysql> alter table test add index tt(name);
Query OK, 0 rows affected (2.74 sec)
Records: 0 Duplicates: 0 Warnings: 0
`
然后查看执行计划，发现可能用到的索引有 `tt`，但是实际情况依然走的主键全索引扫描。
`mysql> explain update test set name ='test' where name='a';
+----+-------------+-------+------------+-------+---------------+---------+---------+------+---------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
+----+-------------+-------+------------+-------+---------------+---------+---------+------+---------+----------+-------------+
| 1 | UPDATE | test | NULL | index | tt | PRIMARY | 4 | NULL | 2355988 | 100.00 | Using where |
+----+-------------+-------+------------+-------+---------------+---------+---------+------+---------+----------+-------------+
1 row in set (0.00 sec)
`
因为 MySQL 的优化器是基于代价来评估的，我们可以通过 `optimizer trace` 来观察。
`mysql> show variables like 'optimizer_trace';
+-----------------+--------------------------+
| Variable_name | Value |
+-----------------+--------------------------+
| optimizer_trace | enabled=off,one_line=off |
+-----------------+--------------------------+
1 row in set (0.01 sec)
`
可以看到值为 `enabled=off`，表明这个功能默认是关闭的。
如果想打开这个功能，必须⾸先把 `enabled` 的值改为 `on`。
`mysql> set optimizer_trace="enabled=on";
Query OK, 0 rows affected (0.00 sec)
`
然后执行该 SQL，查看详细的信息，这里我们主要关注的是 **PREPARE** 阶段的成本计算。
`mysql> update test set name ='test' where name='a';
Query OK, 262144 rows affected (5.97 sec)
Rows matched: 262144 Changed: 262144 Warnings: 0
mysql> SELECT * FROM information_schema.OPTIMIZER_TRACE\G
`
详细结果如下。
`mysql> SELECT * FROM information_schema.OPTIMIZER_TRACE\G
*************************** 1. row ***************************
QUERY: update test set name ='test' where name='a'
TRACE: {
"steps": [
{
"substitute_generated_columns": {
}
},
{
"condition_processing": {
"condition": "WHERE",
"original_condition": "(`test`.`name` = 'a')",
"steps": [
{
"transformation": "equality_propagation",
"resulting_condition": "multiple equal('a', `test`.`name`)"
},
{
"transformation": "constant_propagation",
"resulting_condition": "multiple equal('a', `test`.`name`)"
},
{
"transformation": "trivial_condition_removal",
"resulting_condition": "multiple equal('a', `test`.`name`)"
}
]
}
},
{
"table": "`test`",
"range_analysis": {
"table_scan": {
"rows": 2355988,
"cost": 475206
},
"potential_range_indexes": [
{
"index": "PRIMARY",
"usable": true,
"key_parts": [
"id"
]
},
{
"index": "tt",
"usable": true,
"key_parts": [
"name",
"id"
]
}
],
"setup_range_conditions": [
],
"group_index_range": {
"chosen": false,
"cause": "no_join"
},
"analyzing_range_alternatives": {
"range_scan_alternatives": [
{
"index": "tt",
"ranges": [
"0x0100610000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 <= name <= 0x0100610000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
],
"index_dives_for_eq_ranges": true,
"rowid_ordered": true,
"using_mrr": false,
"index_only": false,
"rows": 553720,
"cost": 664465,
"chosen": false,
"cause": "cost"
}
],
"analyzing_roworder_intersect": {
"usable": false,
"cause": "too_few_roworder_scans"
}
}
}
}
]
}
MISSING_BYTES_BEYOND_MAX_MEM_SIZE: 0
INSUFFICIENT_PRIVILEGES: 0
1 row in set (0.00 sec)
`
可以发现执行全表扫描的成本为 **475206**，走索引 `tt` 的成本为 **664465**，所以 MySQL 选择了**全表扫描**。
### 那么如果是这种情况改怎么处理呢？
如果 InnoDB 隔离级别是 RR，数据库层面没有太好的方式，推荐应用端进行改造。
如果数据库隔离级别可以更改，那么可以改为 RC 来解决阻塞的问题。因为 RC 模式下支持半一致性读。
### 什么是半一致性读呢？
简单来说就是当要对行进行加锁时，会多一步判断该行是不是真的需要上锁。比如全表扫描更新的时候，我们只需要更新 `WHERE` 匹配到的行，如果是没有半一致性读就会把所有数据进行加锁，但是有了半一致性读，那么会判断是否满足 `WHERE` 条件，若不满足则不会加锁（提前释放锁）。
那么对于区分度低的字段就可以使用半一致性读特性来优化，这样更新不同的值就不会互相等待，导致业务卡顿。
| 事务1 | 事务2 |
| --- | --- |
| mysql> begin;  Query OK, 0 rows affected (0.00 sec)  mysql> update test set name =&#8217;test&#8217; where name=&#8217;a&#8217;;Query OK, 262144 rows affected (9.30 sec)Rows matched: 262144 Changed: 262144 Warnings: 0 |  |
|  | mysql> begin; Query OK, 0 rows affected (0.00 sec)mysql> update test set name =&#8217;test1&#8242; where name=&#8217;b&#8217;;Query OK, 262144 rows affected (8.46 sec)Rows matched: 262144 Changed: 262144 Warnings: 0 |
# 结论
- 行锁机制是基于索引列实现的，若没有使用到索引，则会进行全表扫描。
- 半一致性读是基于 RC 隔离级别的优化，可以减少锁冲突以及锁等待，提升并发。