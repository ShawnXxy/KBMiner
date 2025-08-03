# 技术译文 | MySQL InnoDB Online DDL 算法更新

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e8%af%91%e6%96%87-mysql-innodb-online-ddl-%e7%ae%97%e6%b3%95%e6%9b%b4%e6%96%b0/
**分类**: MySQL 新特性
**发布时间**: 2024-04-02T01:07:16-08:00

---

在 MySQL [8.0.12](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-12.html) 中，我们引入了一种新的 DDL 算法，该算法在更改表的定义时不会阻塞表。第一个即时操作是在表格末尾添加一列，这是来自腾讯游戏的贡献。
然后在 MySQL [8.0.29](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-29.html) 中，我们添加了在表中任意位置添加（或删除）列的可能性。
在这篇文章中，我想重点讨论盲目使用此功能时可能发生的一些危险。
# 默认算法
从 MySQL 8.0.12 开始，对于任何支持的 DDL，默认算法是 **INSTANT**。这意味着 *ALTER* 语句只会修改数据字典中表的元数据。在操作的准备和执行阶段，不会对表进行独占元数据锁，表数据不受影响，使得操作是即时的。
另外两种算法是 **COPY** 和 **INPLACE**，[Online DDL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) 操作参见手册。
然而，即使支持操作，Online DDL 也存在限制：一个表支持 64 次即时更改。到限制后，需要“重建”该表。
如果在 *ALTER* 语句（DDL 操作）期间未指定算法，则会默默地选择适当的算法。当然，如果没有预料到，这可能会导致生产中出现噩梦般的情况。
# 始终指定算法
因此，第一个建议始终是指定算法，即使它是执行 DDL 时的默认算法。当指定算法时，如果 MySQL 无法使用它，它将抛出错误，而不是使用其他算法执行操作：
`SQL > ALTER TABLE t1 DROP col1, ALGORITHM=INSTANT;
ERROR: 4092 (HY000): Maximum row versions reached for table test/t1.
No more columns can be added or dropped instantly. Please use COPY/INPLACE.
`
# 监控即时变化
第二个建议也是监视对表执行的即时更改的数量。
MySQL 在 `information_schema` 表中保留行版本：
`SQL > SELECT NAME, TOTAL_ROW_VERSIONS
FROM INFORMATION_SCHEMA.INNODB_TABLES WHERE NAME LIKE 'test/t1';
+---------+--------------------+
| NAME    | TOTAL_ROW_VERSIONS |
+---------+--------------------+
| test/t1 |                 63 |
+---------+--------------------+
`
在上面的示例中，DBA 将能够执行一项额外的 INSTANT DDL 操作，但在此之后，MySQL 将无法执行另一项操作。
作为 DBA，监视所有表并决定何时需要重建表（以重置该计数器）是一个很好的做法。
这是添加到监控工具的建议查询的示例：
`SQL > SELECT NAME, TOTAL_ROW_VERSIONS, 64-TOTAL_ROW_VERSIONS AS
"REMAINING_INSTANT_DDLs",
ROUND(TOTAL_ROW_VERSIONS/64 * 100,2) AS "DDLs %"
FROM INFORMATION_SCHEMA.INNODB_TABLES
WHERE TOTAL_ROW_VERSIONS > 0 ORDER BY 2 DESC;
+--------------------------+--------------------+------------------------+--------+
| NAME                     | TOTAL_ROW_VERSIONS | REMAINING_INSTANT_DDLs | DDLs % |
+--------------------------+--------------------+------------------------+--------+
| test/t1                  |                 63 |                      1 |  98.44 |
| test/t                   |                  4 |                     60 |   6.25 |
| test2/t1                 |                  3 |                     61 |   4.69 |
| sbtest/sbtest1           |                  2 |                     62 |   3.13 |
| test/deprecation_warning |                  1 |                     63 |   1.56 |
+--------------------------+--------------------+------------------------+--------+
`
要重置计数器并重建表，可以使用 `OPTIMIZE TABLE <table>` 或 `ALTER TABLE <table> ENGINE=InnoDB`
# 结论
总之，MySQL 8.0 引入的 DDL 操作 INSTANT 算法通过避免阻塞更改彻底改变了模式更改。然而，由于 64 次即时更改的限制，在需要重建表之前，在 *ALTER* 语句期间显式指定算法以避免意外行为至关重要。还建议通过 `information_schema` 监视即时更改的数量，以避免在不知不觉中达到即时更改限制而出现意外情况，并仔细计划将表重建。
享受 MySQL！