# 技术分享 | 咬文嚼字之驱动表 &#038; outer表

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e5%92%ac%e6%96%87%e5%9a%bc%e5%ad%97%e4%b9%8b%e9%a9%b1%e5%8a%a8%e8%a1%a8-outer%e8%a1%a8/
**分类**: 技术干货
**发布时间**: 2021-12-13T00:53:53-08:00

---

作者：胡呈清
爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：https://www.jianshu.com/u/a95ec11f67a8，欢迎讨论。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
什么是驱动表？
什么是 outer 表和 inner 表？
outer 表等同于驱动表吗？
## 在MySQL中这个问题的脉络
- 
MySQL的 join 算法：Nested-Loop 和其变种算法 Block Nested-Loop
MySQL8.0.18 引入的 hash join 其实可以算是对 Block Nested-Loop 的优化（MySQL8.0.20 之前 explain 输出显示的还是 Block Nested Loop，需要用 explain format=tree 才能看到使用了 hash join），直到 MySQL8.0.20 删除了 Block Nested-Loop，hash join 正式上位。
- 
Nested-Loop 算法：外循环和内循环
t1、t2 两表关联时，最简单的 Nested-Loop 的算法如下：
`for each row in t1 matching range {
for each row in t2 {
if row satisfies join conditions, send to client
}
}
`
这个算法的意思就是：每次将一行数据从外循环传递到内循环进行对比。而外循环中的表就叫 outer 表，内循环中的表就是 inner 表。
在 MySQL 文档中没有任何关于驱动表(drving table)的描述和定义，不过我们可以参考 Oracle 的这个帖子：https://asktom.oracle.com/pls/apex/f?p=100:11:0::::P11_QUESTION_ID:192812348072
`The 'driving' table is the table we will join FROM -- that is JOIN TO other tables.`
这意思多少有点抽象了，不过别急，我们再琢磨下上面的 Nested-Loop 算法，不就是 outer 表“驱动” inner 表的意思吗？所以啊，“驱动表” 其实就是 outer 表。
- 
Block Nested-Loop(BNL)的由来
按照 Nested-Loop 算法，如果 inner 表的关联字段有索引，则在内循环中 inner 表可以利用索引查找数据，查找次数等于 outer 表行数(满足其他条件)。但是如果 inner 表的关联字段没有索引，则每次 inner 表都需要全表扫描，为了减少 inner 表的全表扫描次数，每次从 outer 表中会取出多行数据存放到 join buffer 中，并把 join buffer 传递到内循环中，则可以将内循环 inner 表中读取的每一行与 join buffer 中的所有行进行比较。这样 inner 表的读取次数显著减少，如果 join buffer 能够放下 outer 表的所有行，则 inner 表只需要读取一次（一次全表扫描）。
注意：放进内存(join buffer)的是驱动表。
- 
Hash Join 的由来
BNL 算法在 join buffer 中维护的是一个无序数组，所以每次在 join buffer 中查找都要遍历所有行。不难看出 BNL 算法对比 Nested-Loop 减少的是 IO 成本，CPU 成本并没有降低，对比次数都等于 outer、inner 表行数的乘积。hash join 就是在此算法的基础上，在 join buffer 中维护一个哈希表，每次查找做一次判断就能找到数据，这样一来 CPU 成本也显著降低。
- 
outer 表、驱动表的选择
对于 left join、right join 来说，其语义已经固定了 outer 表的选择，没啥讨论空间（除非 where 子句中打破了其语义）。对于 inner join，outer 表的选择是由优化器说了算的，举例：
`select * from t1 join t2 on t1.a=t2.a;`
a. 如果 t1.a、t2.a 都有索引，且基数高，则效率最高的算法是 Nested-Loop，由于有索引，通常我们会改称其为 Index Nested-Loop，则会选择小表作为 outer 表，这样循环的次数会更少；
b. 如果t1.a、t2.a 都没有索引，基于成本的考虑，则优化器会选择 BNL 算法或者 hash join，由于 outer 表要放入 join buffer 中，而这块内存的大小是根据 join_buffer_size 参数指定的，容量有限，所以还是会选择小表作为 outer 表；
c. 当然也不一定都是选择小表作为 outer 表，如果 t1 表有 10 万行数据，t1.a 有索引；而 t2 表有 20 万行数据，t2.a 没有索引。则优化器很可能选择 t2 表作为 outer 表，因为 Index Nested-Loop 算法肯定比 BNL 算法成本更低，也可能比 hash join 算法成本低。
例子比较简单，实际情况会更复杂，比如 SQL 中多半还会有 where 子句，这时候小表的定义就不是t1、t2的整表大小了，而是 t1、t2 应用完 where 子句后的数据大小，本篇不做过多讨论。
## 其他数据库
从上文可以看出，outer 表脱胎于“外循环”，而外循环严格来说是 Nested-Loop 算法中的定义。翻阅多个数据库的文档（见下文），其实在描述其他 join 算法时（Hash Join、Merge Join）都没有出现“outer table”，所以不禁会产生一种疑问：如果不是 Nested-Loop 算法，会有 outer 表的说法吗？
但从上文也可以看出，其实 Hash Join 本质上还是一种“循环连接”算法，包括 MySQL 没有实现的 Merge Join 算法也一样，所以我个人观点是：
- 
在Join查询中，数据库扫描第一个表为驱动表，同时也是 outer table。
**informix 对于 outer table 的描述**
见链接：https://www.ibm.com/docs/sr/informix-servers/14.10?topic=plan-nested-loop-join
In a nested-loop join, the database server scans the first, or outer table, and then joins each of the rows that pass table filters to the rows found in the second, or inner table.
**sybase 对于 outer table 的描述**
见链接：https://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.infocenter.dc32300.1570/html/sqlug/sqlug153.htm
- 
Inner and outer tables
The terms outer table and inner table describe the placement of the tables in an outer join:
- 
In a left join, the outer table and inner table are the left and right tables respectively. The outer table and inner table are also referred to as the row-preserving and null-supplying tables, respectively.
In a right join, the outer table and inner table are the right and left tables, respectively.
#### Oracle 对于 outer table 的描述
**How Nested Loops Joins Work章节**
The inner loop is executed for every row of the outer loop. The employees table is the &#8220;outer&#8221; data set because it is in the exterior forloop. The outer table is sometimes called a driving table. Thedepartments table is the &#8220;inner&#8221; data set because it is in the interior for loop.
A nested loops join involves the following basic steps:
- 
The optimizer determines the driving row source and designates it as the outer loop.
The outer loop produces a set of rows for driving the join condition. The row source can be a table accessed using an index scan, a full table scan, or any other operation that generates rows.
The number of iterations of the inner loop depends on the number of rows retrieved in the outer loop. For example, if 10 rows are retrieved from the outer table, then the database must perform 10 lookups in the inner table. If 10,000,000 rows are retrieved from the outer table, then the database must perform 10,000,000 lookups in the inner table.
#### outer join 章节：
In ANSI syntax, the OUTER JOIN clause specifies an outer join. In the FROM clause, the left table appears to the left of the OUTER JOIN keywords, and the right table appears to the right of these keywords. The left table is also called the outer table, and the right table is also called the inner table.
#### Nested Loops Outer Joins 章节：
An outer join returns all rows that satisfy the join condition and also rows from one table for which no rows from the other table satisfy the condition. Thus, the result set of an outer join is the superset of an inner join.
In ANSI syntax, the OUTER JOIN clause specifies an outer join. In the FROM clause, the left table appears to the left of the OUTER JOIN keywords, and the right table appears to the right of these keywords. The left table is also called the outer table, and the right table is also called the inner table. For example, in the following statement the employees table is the left or outer table:
Outer joins require the outer-joined table to be the driving table. In the preceding example, employees is the driving table, and departments is the driven-to table.
#### Hash Join Outer Joins 章节：
The optimizer uses hash joins for processing an outer join when either the data volume is large enough to make a hash join efficient, or it is impossible to drive from the outer table to the inner table.
The cost determines the order of tables. The outer table, including preserved rows, may be used to build the hash table, or it may be used to probe the hash table.