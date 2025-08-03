# MySQL 深潜 - 重构后的 ROLLUP 实现

**Date:** 2024/05
**Source:** http://mysql.taobao.org/monthly/2024/05/01/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2024 / 05
 ](/monthly/2024/05)

 * 当期文章

 MySQL 深潜 - 重构后的 ROLLUP 实现
* MySQL查询优化分析 - 常用分析方法
* InnoDB 全文索引：基本概念，插入和删除

 ## MySQL 深潜 - 重构后的 ROLLUP 实现 
 Author: 李博(泊歌) 

 # ROLLUP 功能简述

ROLLUP 可以在普通的 GROUP BY 聚合的情况下，增加更多层次的聚集输出。比如以下这条 SQL：

`SELECT year, country, product,
 SUM(profit) AS profit
FROM sales
GROUP BY year, country, product
WITH ROLLUP;
`

除了计算按照年份、国家、产品分组的利润总和，也会计算按照年份、国家(GROUP BY year, country)，按照年份(GROUP BY year)和所有(No GROUP BY)的利润总和。结果如下：

`+------+---------+------------+--------+
| year | country | product | profit | rollup level
+------+---------+------------+--------+
| 2000 | Finland | Computer | 1500 | 3 <-- GROUP BY year, country, product
| 2000 | Finland | Phone | 100 | 3
| 2000 | Finland | NULL | 1600 | 2 <-- GROUP BY year, country
| 2000 | India | Calculator | 150 | 3
| 2000 | India | Computer | 1200 | 3
| 2000 | India | NULL | 1350 | 2 <-- GROUP BY year, country
| 2000 | USA | Calculator | 75 | 3
| 2000 | USA | Computer | 1500 | 3
| 2000 | USA | NULL | 1575 | 2 <-- GROUP BY year, country
| 2000 | NULL | NULL | 4525 | 1 <-- GROYP BY year
| 2001 | Finland | Phone | 10 | 3
| 2001 | Finland | NULL | 10 | 2 <-- GROUP BY year, country
| 2001 | USA | Calculator | 50 | 3
| 2001 | USA | Computer | 2700 | 3
| 2001 | USA | TV | 250 | 3
| 2001 | USA | NULL | 3000 | 2 <-- GROUP BY year, country
| 2001 | NULL | NULL | 3010 | 1 <-- GROUP BY year
| NULL | NULL | NULL | 7535 | 0 <-- No GROUP BY
+------+---------+------------+--------+
`

MySQL 会将不同的聚集结果定义为不同的 rollup level，总计的层次为 0，GROUP BY 后有几列层次便为多少。由于所有层次的聚合结果是一块输出的，低层次的结果在未聚集的列上会用 NULL 替代。

` GROUP BY year, country, product
 | | | |
rollup level 0 1 2 3
`

MySQL 对 ROLLUP 的实现是采用流式聚集的方式，将输入数据排序后计算；不支持临时表聚集的原因可能是根据键值查找和写入临时表的代价比较高，因为每读到一行数据，都需要按照不同的聚集层次查找和写入临时表。

流式聚集实现 ROLLUP 的过程中主要需要处理的有两个方面，第一个是同时维护多层 rollup 的聚集函数计算，第二个是确定是否应该输出低层次的 rollup 聚集结果。

# 总体代码流程

`SELECT_LEX::prepare
 |--SELECT_LEX::mark_item_as_maybe_null_if_rollup_item // 将all_fields里的表达式标记maybe_null为true，防止常量表达式被优化掉，比如IS NULL
 |--SELECT_LEX::resolve_rollup() // 遍历all_fields，对聚集函数和分组列进行封装，加入到all_fields中，保持base_ref_items不变
 |--create_rollup_switcher // 拷贝多份聚集函数，封装在Item_rollup_sum_switcher
 |--resolve_rollup_item() // 将参数里的分组列封装在Item_rollup_group_item
 ｜--如果有split_sum_func加入到all_fields中的聚集函数
 |--create_rollup_switcher() // 补充wrapper

JOIN::optimize
 |--JOIN::optimize_rollup() // 设置allow_group_via_temp_table为false，强制ROLLUP走流式聚集
 |--JOIN::make_tmp_tables_info()
 |--make_group_fields() // 创建分组列比较用的Cached_item
 |--setup_copy_fields() // 创建分组列和表达式计算的Copy_field和Item_copy
 |--JOIN::make_func_list // 将所有聚集函数的switcher通过sum_funcs数组串起来

AggregateIterator::Read
 |--state为LAST_ROW_STARTED_NEW_GROUP
 |--copy_fields_and_funcs() // 拷贝和计算分组列和基于分组列的函数
 |--Item_rollup_sum_switcher::reset_and_add_for_rollup // 对低层次的聚集，对高层次的重置并聚集
 |--state为READING_ROWS
 |--Item_rollup_sum_switcher::aggregator_add_all // 持续累加所有ROLLUP层次的聚集函数
 |--state为OUTPUTTING_ROLLUP_ROWS
 |--从高层次到低层次输出对应的rollup结果行
 |--Item_copy::copy() //重新计算由于分组列为NULL的函数值
`

# 多层 ROLLUP 聚集函数的封装

对于 SQL 语句中的每一个聚集函数，都需要同时计算多层 rollup 的结果，MySQL 使用了一个特殊的派生于 Item_sum 的封装类 Item_rollup_sum_switcher 来实现。对于每一个聚集函数，都会创建一个新的 Item_rollup_sum_switcher，然后将原聚集函数比如 Item_sum_count 拷贝多份放入 Item_rollup_sum_switcher 的参数列表中(总计 N+1 份，N 为 GROUP BY 的列数)，参数下标对应 rollup 的层次 0, 1, 2, 3。这个过程在 create_rollup_switcher 中实现。

每当有新的聚集函数被添加到 all_fields 中，都需要用 Item_rollup_sum_switcher 来封装，保证可以同时计算多层聚集函数的结果。

# 表达式中出现分组列的封装

ROLLUP 的输出有一个特点是，原本不可能为 NULL 的分组列，由于不包含在低层次的分组列中而变成 NULL，所以基于这些列的表达式进而都可能为 NULL，我们需要一个函数在特定的输出行上返回 NULL 的结果。MySQL 在 Item_rollup_group_item 函数里实现这一过程，会递归遍历所有的表达式，将所有在分组列中的表达式参数都用 Item_rollup_group_item 进行封装，然后替换原参数，并且标记原表达式的 maybe_null 为 true。

根据表达式在分组列中的位置(以 0 开始的序号)，初始化 m_min_rollup_level 参数，在输出结果时，只有当前的 rollup level 小于等于 m_min_rollup_level 时，Item_rollup_group_item 的结果直接输出 NULL，否则正常计算原表达式的值。

比如表达式为上述例子中的 year 时，m_min_rollup_level 为 0，只有当输出最后一行全部的总和时，year 列上的输出才为 NULL。这个过程在 SELECT_LEX::resolve_rollup -> SELECT_LEX::resolve_rollup_item 中实现。

# 流式聚集的计算

MySQL 的流式聚集是依赖于一层特殊的 slice(REF_SLICE_ORDERED_GROUP_BY) 来做的，这样的方式在 8.0.23 中重构掉了(dd2cf5a945529)，但是和 ROLLUP 相关的整体思路是不变的。

## 准备工作
流式聚集计算需要在 JOIN::make_tmp_tables_info 中给每一个分组列创建对应的 Cached_item 按照反序放入 JOIN::group_fields 中，这样在读到下一行的值，通过 Cached_item::cmp 比较和当前组的缓存值是否一样时，如果发现相同就不用继续比较了，因为数据是按照分组列正序有序的；发现分组列的值发现变化，就直接将当前的值存入缓存，并返回 GROUP BY 列第一个变化组的序号 first_changed_idx(从 0 开始)。

此外在 setup_copy_fields 中会将 all_fields 中的分组列和非聚集函数表达式创建对应的 Copy_field 和 Item_copy 放入 Temp_table_param::copy_fields 和 grouped_expressions 中，由于在同一个分组时，这些表达式的结果是相同的，所以只需要在遇到新的分组时由 copy_fields_and_funcs 计算一次即可。setup_copy_fields 也会生成 REF_SLICE_ORDERED_GROUP_BY slice 输出对应的 all_fields 列表，由新生成的 Item_field、Item_copy 和保持原样的聚集函数、包含聚集函数的表达式构成。

## 计算过程

AggregateIterator::Read 中遇到一个新的分组时，会将当前组的组值和聚集函数值输出，由第一个发生变化的分组列序号决定要输出多少低层次的 ROLLUP 结果行。比如第一个变化的列是 product，那么我们只需输出普通 GROUP BY 的聚合值；如果第一个变化的是 year 值，那么既需要输出 year 维度的聚集值，也需要输出 year, country 维度的聚合值。

以上面举例，如果 first_changed_idx 小于 2，那么标记下次进入 AggregateIterator 时的状态为 OUTPUTTING_ROLLUP_ROWS。m_current_rollup_position 从 country 对应的 2 开始递减，输出低层次的 ROLLUP 结果。在输出前，需要遍历 SELECT_LEX 中将所有 Item_rollup_group_item 和 Item_rollup_sum_switcher 串起来的链表 rollup_group_items 和 rollup_sums，将他们的 m_current_rollup_level 设置为 m_current_rollup_position，从而决定 Item_rollup_group_item 的输出是否为 NULL，和 Item_rollup_sum_switcher 从哪一层的聚集函数取值。对于在 grouped_expressions 中包含了当前层为 NULL 值列的函数，需要重新计算函数值。

直到 m_current_rollup_position 小于最后一个没有变化值的分组列位置时，结束 ROLLUP 低层次结果的输出，进入新一组的累加。在 Item_rollup_sum_switcher::reset_and_add_for_rollup 过程中，会继续累加没有输出的低层次聚集函数值；重置并累加已经输出过的高层次的 ROLLUP 聚集值。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)