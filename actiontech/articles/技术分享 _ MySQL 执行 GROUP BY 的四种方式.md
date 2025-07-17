# 技术分享 | MySQL 执行 GROUP BY 的四种方式

**原文链接**: https://opensource.actionsky.com/20190813-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-08-13T00:39:20-08:00

---

> 作者：Peter Zaitsev
在日常查询中，索引或其他数据查找的方法可能不是查询执行中最高昂的部分，例如：MySQL GROUP BY 可能负责查询执行时间 90% 还多。MySQL 执行 GROUP BY 时的主要复杂性是计算 GROUP BY 语句中的聚合函数。UDF 聚合函数是一个接一个地获得构成单个组的所有值。这样，它可以在移动到另一个组之前计算单个组的聚合函数值。当然，问题在于，在大多数情况下，源数据值不会被分组。来自各种组的值在处理期间彼此跟随。因此，我们需要一个特殊的步骤。
**处理 MySQL GROUP BY**让我们看看之前看过的同一张table：- `    mysql> show create table tbl \G`
- `    *************************** 1. row ***************************`
- `          Table: tbl`
- `    Create Table: CREATE TABLE `tbl` (`
- `     `id` int(11) NOT NULL AUTO_INCREMENT,`
- `     `k` int(11) NOT NULL DEFAULT '0',`
- `     `g` int(10) unsigned NOT NULL,`
- `     PRIMARY KEY (`id`),`
- `     KEY `k` (`k`)`
- `    ) ENGINE=InnoDB AUTO_INCREMENT=2340933 DEFAULT CHARSET=latin1`
- `    1 row in set (0.00 sec)`
并且以不同方式执行相同的 GROUP BY 语句：
**1、MySQL中 的 Index Ordered GROUP BY**- `    mysql> select k, count(*) c from tbl group by k order by k limit 5;`
- `    +---+---+`
- `    | k | c |`
- `    +---+---+`
- `    | 2 | 3 |`
- `    | 4 | 1 |`
- `    | 5 | 2 |`
- `    | 8 | 1 |`
- `    | 9 | 1 |`
- `    +---+---+`
- `    5 rows in set (0.00 sec)`
- 
- `    mysql> explain select k, count(*) c from tbl group by k order by k limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: index`
- `    possible_keys: k`
- `             key: k`
- `         key_len: 4`
- `             ref: NULL`
- `            rows: 5`
- `        filtered: 100.00`
- `           Extra: Using index`
- `    1 row in set, 1 warning (0.00 sec)`
在这种情况下，我们在 GROUP BY 的列上有一个索引。这样，我们可以逐组扫描数据并动态执行 GROUP BY（低成本）。当我们使用 LIMIT 限制我们检索的组的数量或使用“覆盖索引”时，特别有效，因为顺序索引扫描是一种非常快速的操作。如果您有少量组，并且没有覆盖索引，索引顺序扫描可能会导致大量 IO。所以这可能不是最优化的计划。
**2、MySQL 中的外部排序 GROUP BY**- `    mysql> explain select SQL_BIG_RESULT g, count(*) c from tbl group by g limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: ALL`
- `    possible_keys: NULL`
- `             key: NULL`
- `         key_len: NULL`
- `             ref: NULL`
- `            rows: 998490`
- `        filtered: 100.00`
- `           Extra: Using filesort`
- `    1 row in set, 1 warning (0.00 sec)`
- 
- 
- `    mysql> select SQL_BIG_RESULT g, count(*) c from tbl group by g limit 5;`
- `    +---+---+`
- `    | g | c |`
- `    +---+---+`
- `    | 0 | 1 |`
- `    | 1 | 2 |`
- `    | 4 | 1 |`
- `    | 5 | 1 |`
- `    | 6 | 2 |`
- `    +---+---+`
- `    5 rows in set (0.88 sec)`
如果我们没有允许我们按组顺序扫描数据的索引，我们可以通过外部排序（在 MySQL 中也称为“filesort”）来获取数据。你可能会注意到我在这里使用 SQL_BIG_RESULT 提示来获得这个计划。没有它，MySQL 在这种情况下不会选择这个计划。一般来说，MySQL 只有在我们拥有大量组时才更喜欢使用这个计划，因为在这种情况下，排序比拥有临时表更有效（我们将在下面讨论）。
**3、MySQL中 的临时表 GROUP BY**- `    mysql> explain select  g, sum(g) s from tbl group by g limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: ALL`
- `    possible_keys: NULL`
- `             key: NULL`
- `         key_len: NULL`
- `             ref: NULL`
- `            rows: 998490`
- `        filtered: 100.00`
- `           Extra: Using temporary`
- `    1 row in set, 1 warning (0.00 sec)`
- 
- 
- `    mysql> select  g, sum(g) s from tbl group by g order by null limit 5;`
- `    +---+------+`
- `    | g | s    |`
- `    +---+------+`
- `    | 0 |    0 |`
- `    | 1 |    2 |`
- `    | 4 |    4 |`
- `    | 5 |    5 |`
- `    | 6 |   12 |`
- `    +---+------+`
- `    5 rows in set (7.75 sec)`
在这种情况下，MySQL 也会进行全表扫描。但它不是运行额外的排序传递，而是创建一个临时表。此临时表每组包含一行，并且对于每个传入行，将更新相应组的值。很多更新！虽然这在内存中可能是合理的，但如果结果表太大以至于更新将导致大量磁盘 IO，则会变得非常昂贵。在这种情况下，外部分拣计划通常更好。请注意，虽然 MySQL 默认选择此计划用于此用例，但如果我们不提供任何提示，它几乎比我们使用 SQL_BIG_RESULT 提示的计划慢 10 倍 。您可能会注意到我在此查询中添加了“ ORDER BY NULL ”。这是为了向您展示“清理”临时表的唯一计划。没有它，我们得到这个计划：- `    mysql> explain select  g, sum(g) s from tbl group by g limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: ALL`
- `    possible_keys: NULL`
- `             key: NULL`
- `         key_len: NULL`
- `             ref: NULL`
- `            rows: 998490`
- `        filtered: 100.00`
- `           Extra: Using temporary; Using filesort`
- `    1 row in set, 1 warning (0.00 sec)`
在其中，我们获得了 temporary 和 filesort “两最糟糕的”提示。MySQL 5.7 总是返回按组顺序排序的 GROUP BY 结果，即使查询不需要它（这可能需要昂贵的额外排序传递）。ORDER BY NULL 表示应用程序不需要这个。您应该注意，在某些情况下 &#8211; 例如使用聚合函数访问不同表中的列的 JOIN 查询 &#8211; 使用 GROUP BY 的临时表可能是唯一的选择。如果要强制 MySQL 使用为 GROUP BY 执行临时表的计划，可以使用 SQL_SMALL_RESULT 提示。
**4、MySQL 中的索引基于跳过扫描的 GROUP BY**前三个 GROUP BY 执行方法适用于所有聚合函数。然而，其中一些人有第四种方法。- `    mysql> explain select k,max(id) from tbl group by k \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: range`
- `    possible_keys: k`
- `             key: k`
- `         key_len: 4`
- `             ref: NULL`
- `            rows: 2`
- `        filtered: 100.00`
- `           Extra: Using index for group-by`
- `    1 row in set, 1 warning (0.00 sec)`
- 
- `    mysql> select k,max(id) from tbl group by k;`
- `    +---+---------+`
- `    | k | max(id) |`
- `    +---+---------+`
- `    | 0 | 2340920 |`
- `    | 1 | 2340916 |`
- `    | 2 | 2340932 |`
- `    | 3 | 2340928 |`
- `    | 4 | 2340924 |`
- `    +---+---------+`
- `    5 rows in set (0.00 sec)`
此方法仅适用于非常特殊的聚合函数：MIN() 和 MAX()。这些并不需要遍历组中的所有行来计算值。他们可以直接跳转到组中的最小或最大组值（如果有这样的索引）。如果索引仅建立在 (K) 列上，如何找到每个组的 MAX(ID) 值？这是一个 InnoDB 表。记住 InnoDB 表有效地将 PRIMARY KEY 附加到所有索引。(K) 变为 (K,ID)，允许我们对此查询使用 Skip-Scan 优化。仅当每个组有大量行时才会启用此优化。否则，MySQL 更倾向于使用更传统的方法来执行此查询（如方法＃1中详述的索引有序 GROUP BY）。虽然我们使用 MIN() / MAX() 聚合函数，但其他优化也适用于它们。例如，如果您有一个没有 GROUP BY 的聚合函数（实际上所有表都有一个组），MySQL 在统计分析阶段从索引中获取这些值，并避免在执行阶段完全读取表：- `    mysql> explain select max(k) from tbl \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: NULL`
- `      partitions: NULL`
- `            type: NULL`
- `    possible_keys: NULL`
- `             key: NULL`
- `         key_len: NULL`
- `             ref: NULL`
- `            rows: NULL`
- `        filtered: NULL`
- `           Extra: Select tables optimized away`
- `    1 row in set, 1 warning (0.00 sec)`
**过滤和分组**
我们已经研究了 MySQL 执行 GROUP BY 的四种方式。为简单起见，我在整个表上使用了 GROUP BY，没有应用过滤。当您有 WHERE 子句时，相同的概念适用：- `    mysql> explain select  g, sum(g) s from tbl where k>4 group by g order by NULL limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: range`
- `    possible_keys: k`
- `             key: k`
- `         key_len: 4`
- `             ref: NULL`
- `            rows: 1`
- `        filtered: 100.00`
- `           Extra: Using index condition; Using temporary`
- `    1 row in set, 1 warning (0.00 sec)`
对于这种情况，我们使用K列上的范围进行数据过滤/查找，并在有临时表时执行 GROUP BY。在某些情况下，方法不会发生冲突。但是，在其他情况下，我们必须选择使用 GROUP BY 的一个索引或其他索引进行过滤：- `    mysql> alter table tbl add key(g);`
- `    Query OK, 0 rows affected (4.17 sec)`
- `    Records: 0  Duplicates: 0  Warnings: 0`
- 
- `    mysql> explain select  g, sum(g) s from tbl where k>1 group by g limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: index`
- `    possible_keys: k,g`
- `             key: g`
- `         key_len: 4`
- `             ref: NULL`
- `            rows: 16`
- `        filtered: 50.00`
- `           Extra: Using where`
- `    1 row in set, 1 warning (0.00 sec)`
- 
- `    mysql> explain select  g, sum(g) s from tbl where k>4 group by g limit 5 \G`
- `    *************************** 1. row ***************************`
- `              id: 1`
- `     select_type: SIMPLE`
- `           table: tbl`
- `      partitions: NULL`
- `            type: range`
- `    possible_keys: k,g`
- `             key: k`
- `         key_len: 4`
- `             ref: NULL`
- `            rows: 1`
- `        filtered: 100.00`
- `           Extra: Using index condition; Using temporary; Using filesort`
- `    1 row in set, 1 warning (0.00 sec)`
根据此查询中使用的特定常量，我们可以看到我们对 GROUP BY 使用索引顺序扫描（并从索引中“放弃”以解析 WHERE 子句），或者使用索引来解析 WHERE 子句（但使用临时表来解析 GROUP BY）。根据我的经验，这就是 MySQL GROUP BY 并不总是做出正确选择的地方。您可能需要使用 FORCE INDEX 以您希望的方式执行查询。
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/活动海报v4.jpg)