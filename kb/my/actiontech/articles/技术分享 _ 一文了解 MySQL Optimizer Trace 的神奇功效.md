# 技术分享 | 一文了解 MySQL Optimizer Trace 的神奇功效

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e4%b8%80%e6%96%87%e4%ba%86%e8%a7%a3-mysql-optimizer-trace-%e7%9a%84%e7%a5%9e%e5%a5%87%e5%8a%9f%e6%95%88/
**分类**: MySQL 新特性
**发布时间**: 2023-05-30T01:43:12-08:00

---

作者：Mutlis
CSDN & 阿里云 & 知乎 等平台优质作者，擅长Oracle & MySQL等主流数据库系统的维护和管理等
本文来源：原创投稿
## 前言
对于 MySQL 5.6 以及之前的版本来说，查询优化器就像是一个黑盒子一样，你只能通过 `EXPLAIN` 语句查看到最后优化器决定使用的执行计划，却无法知道它为什么做这个决策。这对于一部分喜欢刨根问底的⼩伙伴来说简直是灾难：“我就觉得使用其他的执行方案⽐ `EXPLAIN` 输出的这种方案强，凭什么优化器做的决定和我想的不一样呢？”这篇文章主要介绍使用 `optimizer trace` 查看优化器生成执行计划的整个过程。
## optimizer trace 表的神奇功效
在 MySQL 5.6 以及之后的版本中，设计 MySQL 的大叔贴⼼的为这部分小伙伴提出了一个 `optimizer trace` 的功能，这个功能可以让我们方便的查看优化器生成执行计划的整个过程，这个功能的开启与关闭由系统变量 `optimizer_trace` 决定，我们看一下：
mysql> show variables like 'optimizer_trace';
+-----------------+--------------------------+
| Variable_name   | Value                    |
+-----------------+--------------------------+
| optimizer_trace | enabled=off,one_line=off |
+-----------------+--------------------------+
1 row in set (0.01 sec)
可以看到 `enabled` 值为 `off`，表明这个功能默认是关闭的。
> **小提示：**
`one_line` 的值是控制输出格式的，如果为 `on` 那么所有输出都将在一行中展示，不适合⼈阅读，所以我们就保持其默认值为 `off` 吧。
如果想打开这个功能，必须⾸先把 `enabled` 的值改为 `on`，就像这样：
mysql> SET optimizer_trace="enabled=on";
Query OK, 0 rows affected (0.00 sec)
然后我们就可以输入我们想要查看优化过程的查询语句，当该查询语句执行完成后，就可以到 `information_schema` 数据库下的 `OPTIMIZER_TRACE` 表中查看完整的优化过程。这个 `OPTIMIZER_TRACE` 表有 4 个列，分别是：
- `QUERY`：表示我们查询的语句；
- `TRACE`：表示优化过程的 JSON 格式⽂本；
- `MISSING_BYTES_BEYOND_MAX_MEM_SIZE`：由于优化过程可能会输出很多，如果超过某个限制时，多余的⽂本将不会被显示，这个字段展示了被忽略的⽂本字节数；
- `INSUFFICIENT_PRIVILEGES`：表示是否没有权限查看优化过程，默认值是 0，只有某些特殊情况下才会是 1，我们暂时不关心这个字段的值。
完整的使用 **optimizer trace** 功能的步骤总结如下：
**步骤一：** 打开 optimizer    trace 功能    (默认情况下它是关闭的)。
mysql> SET optimizer_trace="enabled=on";
Query OK, 0 rows affected (0.01 sec)
**步骤二：** 输入查询语句。
SELECT    ...;
**步骤三：** 从 `optimizer_trace` 表中查看上一个查询的优化过程。
SELECT * FROM information_schema.OPTIMIZER_TRACE;
**步骤四：** 可能你还要观察其他语句执行的优化过程，重复上边的第 2、3步。
**步骤五：** 当你停⽌查看语句的优化过程时，把 optimizer    trace 功能关闭。
mysql> SET optimizer_trace="enabled=off";
Query OK, 0 rows affected (0.01 sec)
现在我们有一个搜索条件比较多的查询语句，它的执行计划如下：
mysql> EXPLAIN SELECT * FROM s1 WHERE key1 > 'z' AND  key2 < 1000000 AND key3 IN ('aa', 'bb', 'cb') AND   common_field = 'abc';
+----+-------------+-------+------------+-------+----------------------------+----------+---------+------+------+----------+------------------------------------+
| id | select_type | table | partitions | type  | possible_keys              | key      | key_len | ref  | rows | filtered | Extra                              |
+----+-------------+-------+------------+-------+----------------------------+----------+---------+------+------+----------+------------------------------------+
|  1 | SIMPLE      | s1    | NULL       | range | idx_key2,idx_key1,idx_key3 | idx_key1 | 403     | NULL |    1 |     5.00 | Using index condition; Using where |
+----+-------------+-------+------------+-------+----------------------------+----------+---------+------+------+----------+------------------------------------+
1 row in set, 1 warning (0.00 sec)
可以看到该查询可能使用到的索引有3个，那么为什么优化器最终选择了`idx_key1`而不选择其他的索引或者直接全表扫描呢？这时候就可以通过`otpimzer trace` 功能来查看优化器的具体工作过程：
mysql> SET optimizer_trace="enabled=on";
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM s1 WHERE key1 > 'z' AND  key2 < 1000000 AND key3 IN ('aa', 'bb', 'cb') AND   common_field = 'abc';
Empty set (0.00 sec)
mysql> SELECT * FROM information_schema.OPTIMIZER_TRACE\G   
MySQL 可能会在之后的版本中添加更多的优化过程信息。不过杂乱之中其实还是蛮有规律的，优化过程大致分为了三个阶段：
- prepare 阶段
- optimize 阶段
- execute 阶段
我们所说的基于成本的优化主要集中在 `optimize` 阶段，对于单表查询来说，我们主要关注 `optimize` 阶段的 `"rows_estimation"` 这个过程。这个过程深入分析了对单表查询的各种执行方案的成本，对于多表连接查询来说，我们更多需要关注 `"considered_execution_plans"` 这个过程，这个过程里会写明各种不同的连接方式所对应的成本。反正优化器最终会选择成本最低的那种方案来作为最终的执行计划，也就是我们使用 `EXPLAIN` 语句所展现出的那种方案。
最后，我们为感兴趣的小伙伴展示一下通过查询 `OPTIMIZER_TRACE` 表得到的输出（我使用`#`后跟随注释的形式为大家解释了优化过程中的一些比较重要的点，建议用电脑屏幕观看）：
*************************** 1. row ***************************
# 分析的查询语句是什么
QUERY: SELECT * FROM s1 WHERE key1 > 'z' AND  key2 < 1000000 AND key3 IN ('aa', 'bb', 'cb') AND   common_field = 'abc'
# 优化的具体过程
TRACE: {
"steps": [
{
"join_preparation": {    # prepare阶段
"select#": 1,
"steps": [
{
"IN_uses_bisection": true
},
{
"expanded_query": "/* select#1 */ select `s1`.`id` AS `id`,`s1`.`key1` AS `key1`,`s1`.`key2` AS `key2`,`s1`.`key3` AS `key3`,`s1`.`key_part1` AS `key_part1`,`s1`.`key_part2` AS `key_part2`,`s1`.`key_part3` AS `key_part3`,`s1`.`common_field` AS `common_field` from `s1` where ((`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')) and (`s1`.`common_field` = 'abc'))"
}
]
}
},
{
"join_optimization": {  # optimize阶段
"select#": 1,
"steps": [
{
"condition_processing": { # 处理搜索条件
"condition": "WHERE",
# 原始搜索条件
"original_condition": "((`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')) and (`s1`.`common_field` = 'abc'))",
"steps": [
{
# 等值传递转换
"transformation": "equality_propagation",
"resulting_condition": "((`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')) and multiple equal('abc', `s1`.`common_field`))"
},
{
# 常量传递转换
"transformation": "constant_propagation",
"resulting_condition": "((`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')) and multiple equal('abc', `s1`.`common_field`))"
},
{
# 去除没用的条件
"transformation": "trivial_condition_removal",
"resulting_condition": "((`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')) and multiple equal('abc', `s1`.`common_field`))"
}
]
}
},
{
# 替换虚拟生成列
"substitute_generated_columns": {
}
},
{
# 表的依赖信息
"table_dependencies": [
{
"table": "`s1`",
"row_may_be_null": false,
"map_bit": 0,
"depends_on_map_bits": [
]
}
]
},
{
"ref_optimizer_key_uses": [
]
},
{
# 预估不同单表访问方法的访问成本
"rows_estimation": [
{
"table": "`s1`",
"range_analysis": {
"table_scan": {
"rows": 20250,
"cost": 2051.35
},
# 分析可能使用的索引
"potential_range_indexes": [
{
"index": "PRIMARY", # 主键不可用
"usable": false,
"cause": "not_applicable"
},
{
"index": "idx_key2",# idx_key2可能被使用
"usable": true,
"key_parts": [
"key2"
]
},
{
"index": "idx_key1", # idx_key1可能被使用
"usable": true,
"key_parts": [
"key1",
"id"
]
},
{
"index": "idx_key3", # idx_key3可能被使用
"usable": true,
"key_parts": [
"key3",
"id"
]
},
{
"index": "idx_key_part", # idx_key_part不可用
"usable": false,
"cause": "not_applicable"
}
],
"setup_range_conditions": [
],
"group_index_range": {
"chosen": false,
"cause": "not_group_by_or_distinct"
},
"skip_scan_range": {
"potential_skip_scan_indexes": [
{
"index": "idx_key2",
"usable": false,
"cause": "query_references_nonkey_column"
},
{
"index": "idx_key1",
"usable": false,
"cause": "query_references_nonkey_column"
},
{
"index": "idx_key3",
"usable": false,
"cause": "query_references_nonkey_column"
}
]
},
# 分析各种可能使用的索引的成本
"analyzing_range_alternatives": {
"range_scan_alternatives": [
{
# 使用idx_key2的成本分析
"index": "idx_key2",
# 使用idx_key2的范围区间
"ranges": [
"NULL < key2 < 1000000"
],
"index_dives_for_eq_ranges": true,# 是否使用index dive
"rowid_ordered": false,# 使用该索引获取的记录是否按照主键排序
"using_mrr": false, # 是否使用mrr
"index_only": false, # 是否是索引覆盖访问
"in_memory": 1,
"rows": 10125,# 使用该索引获取的记录条数
"cost": 3544.01,# 使用该索引的成本
"chosen": false,  # 使用该索引的成本
"cause": "cost" # 因为成本太大所以不选择该索引
},
{
# 使用idx_key1的成本分析
"index": "idx_key1",
# 使用idx_key1的范围区间
"ranges": [
"'z' < key1"
],
"index_dives_for_eq_ranges": true,# 同上
"rowid_ordered": false,# 同上
"using_mrr": false,# 同上
"index_only": false,# 同上
"in_memory": 1,
"rows": 1,# 同上
"cost": 0.61,# 同上
"chosen": true# 是否选择该索引
},
{
# 使用idx_key3的成本分析
"index": "idx_key3",
# 使用idx_key3的范围区间
"ranges": [
"key3 = 'aa'",
"key3 = 'bb'",
"key3 = 'cb'"
],
"index_dives_for_eq_ranges": true,# 同上
"rowid_ordered": false,# 同上
"using_mrr": false,# 同上
"index_only": false,# 同上
"in_memory": 1,
"rows": 3,# 同上
"cost": 1.81,# 同上
"chosen": false,# 同上
"cause": "cost"# 同上
}
],
# 分析使用索引合并的成本
"analyzing_roworder_intersect": {
"usable": false,
"cause": "too_few_roworder_scans"
}
},
# 对于上述单表查询s1最优的访问方法
"chosen_range_access_summary": {
"range_access_plan": {
"type": "range_scan",
"index": "idx_key1",
"rows": 1,
"ranges": [
"'z' < key1"
]
},
"rows_for_plan": 1,
"cost_for_plan": 0.61,
"chosen": true
}
}
}
]
},
{
# 分析各种可能的执行计划
#（对多表查询这可能有很多种不同的方案，单表查询的方案上边已经分析过了，直接选取idx_key1就好）
"considered_execution_plans": [
{
"plan_prefix": [
],
"table": "`s1`",
"best_access_path": {
"considered_access_paths": [
{
"rows_to_scan": 1,
"access_type": "range",
"range_details": {
"used_index": "idx_key1"
},
"resulting_rows": 1,
"cost": 0.71,
"chosen": true
}
]
},
"condition_filtering_pct": 100,
"rows_for_plan": 1,
"cost_for_plan": 0.71,
"chosen": true
}
]
},
{
"attaching_conditions_to_tables": {
"original_condition": "((`s1`.`common_field` = 'abc') and (`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')))",
"attached_conditions_computation": [
],
"attached_conditions_summary": [
{
"table": "`s1`",
"attached": "((`s1`.`common_field` = 'abc') and (`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')))"
}
]
}
},
{
# 尝试给查询添加一些其他的查询条件
"finalizing_table_conditions": [
{
"table": "`s1`",
"original_table_condition": "((`s1`.`common_field` = 'abc') and (`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')))",
"final_table_condition   ": "((`s1`.`common_field` = 'abc') and (`s1`.`key1` > 'z') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')))"
}
]
},
{
# 再稍稍的改进一下执行计划
"refine_plan": [
{
"table": "`s1`",
"pushed_index_condition": "(`s1`.`key1` > 'z')",
"table_condition_attached": "((`s1`.`common_field` = 'abc') and (`s1`.`key2` < 1000000) and (`s1`.`key3` in ('aa','bb','cb')))"
}
]
}
]
}
},
{
"join_execution": { # execute阶段
"select#": 1,
"steps": [
]
}
}
]
}
# 因优化过程文本太多而丢弃的文本字节大小，值为0时表示并没有丢弃
MISSING_BYTES_BEYOND_MAX_MEM_SIZE: 0
# 权限字段
INSUFFICIENT_PRIVILEGES: 0
1 row in set (0.01 sec)
ERROR: 
No query specified
大家看到这个输出的第一感觉就是这文本也太多了点吧，其实这只是优化器执行过程中的一小部分。
如果有小伙伴对使用 `EXPLAIN` 语句展示出的对某个查询的执行计划很不理解，大家可以尝试使用 `optimizer trace` 功能来详细了解每一种执行方案对应的成本，相信这个功能能让大家更深入的了解 MySQL 查询优化器。
## 关于 SQLE
爱可生开源社区的 SQLE 是一款面向数据库使用者和管理者，支持多场景审核，支持标准化上线流程，原生支持 MySQL 审核且数据库类型可扩展的 SQL 审核工具。
## SQLE 获取
| 类型 | 地址 |
| --- | --- |
| 版本库 | https://github.com/actiontech/sqle |
| 文档 | https://actiontech.github.io/sqle-docs-cn/ |
| 发布信息 | https://github.com/actiontech/sqle/releases |
| 数据审核插件开发文档 | https://actiontech.github.io/sqle-docs-cn/3.modules/3.7_auditplugin/auditplugin_development.html |
提交有效 pr，高质量 issue，将获赠面值 200-500 元（具体面额依据质量而定）京东卡以及爱可生开源社区精美周边！更多关于 SQLE 的信息和交流，请加入官方QQ交流群：637150065