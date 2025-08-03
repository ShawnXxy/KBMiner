# 技术分享 | SQL 优化：ICP 的缺陷

**原文链接**: https://opensource.actionsky.com/20221207-sql/
**分类**: 技术干货
**发布时间**: 2022-12-06T17:50:02-08:00

---

作者：胡呈清
爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：https://www.jianshu.com/u/a95ec11f67a8，欢迎讨论。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
##### 什么是ICP（Index Condition Pushdown）
ICP全称 Index Condition Pushdown，也就是常说的索引条件下推，在之前的一篇文章中介绍过它：explain 执行计划详解2&#8211;Extra
使用二级索引查找数据时，where 子句中属于索引的一部分但又无法使用索引的条件，MySQL会把这部分条件下推到存储引擎层，筛选之后再进行回表，这样回表的次数就减少了。
比如有这样一个索引`idx_test(birth_date,first_name,hire_date)`
查询语句`select * from employees where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22'; `的执行过程：
1.根据 `birth_date >= '1957-05-23' and birth_date <='1960-06-01'` 这个条件从 idx_test 索引中查找数据，假设返回数据 10万行；
2. 查找出来的10万行数据包含 hire_date 字段，MySQL会把 `hire_date>'1998-03-22'` 这个条件下推到存储引擎，进一步筛选数据，假设还剩1000行；
3. 由于要查询所有字段的值，而前面查到的 1000 行数据只包含 birth_date,first_name,hire_date 三个字段，所以需要回表查出所有字段的值。回表的过程就是将这 1000 行数据的主键值拿出来，一个一个到主键索引上去查找（也可以开启 mrr，拿一批主键值回表），回表次数是 1000。如果没有ICP，则回表次数是 10 万。
很显然在执行阶段 ICP 可以减少回表的次数，在基于代价的优化器中，也就是能减少执行的成本。但是，优化器在优化阶段选择最优的执行计划时真的能考虑到 ICP 可以减少成本吗？下面我们通过一个实验来回答这个问题。
#### 实验
先准备一些数据，下载 Employees Sample Database 并导入到 MySQL 中：https://dev.mysql.com/doc/employee/en/employees-installation.html
还是上面那个例子，创建一个组合索引：
alter table employees add index idx_test(birth_date,first_name,hire_date);
执行下面这个SQL：
SELECT *
FROM employees
WHERE birth_date >= '1957-05-23'
AND birth_date <= '1960-06-01'
AND hire_date > '1998-03-22';
执行计划如下：
mysql [localhost:5735] {msandbox} (employees) > explain select * from employees where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22';
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------------+
| id | select_type | table     | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra       |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------------+
|  1 | SIMPLE      | employees | NULL       | ALL  | idx_test      | NULL | NULL    | NULL | 298980 |    15.74 | Using where |
+----+-------------+-----------+------------+------+---------------+------+---------+------+--------+----------+-------------+
可以看到并没有使用 `idx_test` 索引，但如果加 hint 强制走 `idx_test` 索引，我们知道可以使用 ICP，执行计划如下：
mysql [localhost:5735] {msandbox} (employees) > explain select * from employees force index(idx_test) where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22';
+----+-------------+-----------+------------+-------+---------------+----------+---------+------+--------+----------+-----------------------+
| id | select_type | table     | partitions | type  | possible_keys | key      | key_len | ref  | rows   | filtered | Extra                 |
+----+-------------+-----------+------------+-------+---------------+----------+---------+------+--------+----------+-----------------------+
|  1 | SIMPLE      | employees | NULL       | range | idx_test      | idx_test | 3       | NULL | 141192 |    33.33 | Using index condition |
+----+-------------+-----------+------------+-------+---------------+----------+---------+------+--------+----------+-----------------------+
1 row in set, 1 warning (0.00 sec)
再让我们打开 slow log 看下真实的执行效率：
- 全表扫描需要扫描 300024 行，执行时间 0.15 秒
- 走 idx_test 索引需要扫描 141192 行（Rows_examined: 1065 是个 bug，这显然不是扫描行数，扫描行数我们可以从执行计划看出，在这个例子中执行计划里的 rows 是真实的扫描行数，不是估算值，这个知识点不影响理解本文）。因为没有其他条件，从返回结果行数我们也能知道回表次数就是 1065，执行时间只要 0.037 秒
# Time: 2022-11-24T18:02:01.001734+08:00
# Query_time: 0.146939  Lock_time: 0.000850 Rows_sent: 1065  Rows_examined: 300024
SET timestamp=1669284095;
select * from employees where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22';
# Time: 2022-11-24T18:01:09.001223+08:00
# Query_time: 0.037211  Lock_time: 0.001649 Rows_sent: 1065  Rows_examined: 1065
SET timestamp=1669284032;
select * from employees force index(idx_test) where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22';
很显然走 idx_test 索引比全表扫描效率更高，那为什么优化器不选择走 idx_test 索引呢？一个不会犯错的说法是优化器有它的算法，并不以人类认为的时间快慢为标准来进行选择。这次我们打破砂锅问到底，优化器的算法是什么？
答案是成本，优化器在选择最优的执行计划时会计算所有可用的执行计划的成本，然后选择成本最小的那个。而成本有明确的计算方法，也能通过 explain format=json 展示执行计划的成本，因此我们用这一点来证明 ICP 能否影响执行计划的成本。关于 explain format=json 的详细输出解释可以参考：explain format=json 详解，本文不过多展开。
#### 成本计算
1.I/O成本
表的数据和索引都存储到磁盘上，当我们想查询表中的记录时，需要先把数据或者索引加载到内存中然后再操作。这个从磁盘到内存这个加载的过程损耗的时间称之为I/O成本。
2. CPU成本
读取以及检测记录是否满足对应的搜索条件、对结果集进行排序等这些操作损耗的时间称之为CPU成本。
3. 成本常数
对于InnoDB存储引擎来说，页是磁盘和内存之间交互的基本单位，MySQL5.7 中规定读取一个页面花费的成本默认是1.0，读取以及检测一条记录是否符合搜索条件的成本默认是0.2。1.0、0.2这些数字称之为成本常数（不同版本可能不一样，可以通过 mysql.server_cost、mysql.engine_cost 查看）。
不加干涉时，优化器选择全表扫描，总成本为 &#8220;query_cost&#8221;: &#8220;60725.00&#8221;，计算公式：
- IO成本：929*1 = 929 （929 是主键索引的页数，通过表的统计信息中的 Data_length/pagesize 得到）
- CPU 成本：298980*0.2 = 59796（298980是扫描行数，全表扫描时这是一个估算值，也就是表的统计信息中的 Rows）
- 总成本 = IO成本 + CPU 成本 = 929 + 59796 = 60725
mysql [localhost:5735] {msandbox} (employees) > explain format=json select * from employees  where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22'\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "60725.00"
},
"table": {
"table_name": "employees",
"access_type": "ALL",
"possible_keys": [
"idx_test"
],
"rows_examined_per_scan": 298980,
"rows_produced_per_join": 47059,
"filtered": "15.74",
"cost_info": {
"read_cost": "51313.14",
"eval_cost": "9411.86",
"prefix_cost": "60725.00",
"data_read_per_join": "6M"
},
"used_columns": [
"emp_no",
"birth_date",
"first_name",
"last_name",
"gender",
"hire_date"
],
"attached_condition": "((`employees`.`employees`.`birth_date` >= '1957-05-23') and (`employees`.`employees`.`birth_date` <= '1960-06-01') and (`employees`.`employees`.`hire_date` > '1998-03-22'))"
}
}
}
1 row in set, 1 warning (0.00 sec)
hint 走 idx_test 索引时，总成本为 &#8220;query_cost&#8221;: &#8220;197669.81&#8221;，计算公式：
- 访问 idx_test 索引的成本：
IO 成本=1*1=1（优化器认为读取索引的一个范围区间的I/O成本和读取一个页面是相同的，而条件中只有 birth_date >= &#8216;1957-05-23&#8242; and birth_date <=&#8217;1960-06-01&#8217; 这一个范围）
- CPU 成本 = 141192*0.2 = 28238.4（扫描行数 &#8220;rows_examined_per_scan&#8221;: 141192）
- 回表的成本（不会考虑索引条件下推的作用，因此回表次数等于索引扫描行数）：
回表 IO 成本 = 141192*1 = 141192
- 回表 CPU 成本 = 141192*0.2 = 28238.4
- 总成本：1+28238.4+141192+28238.4=197669.8
mysql [localhost:5735] {msandbox} (employees) > explain format=json select * from employees force index(idx_test) where birth_date >= '1957-05-23' and birth_date <='1960-06-01' and hire_date>'1998-03-22'\G
*************************** 1. row ***************************
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "197669.81"
},
"table": {
"table_name": "employees",
"access_type": "range",
"possible_keys": [
"idx_test"
],
"key": "idx_test",
"used_key_parts": [
"birth_date"
],
"key_length": "3",
"rows_examined_per_scan": 141192,
"rows_produced_per_join": 47059,
"filtered": "33.33",
"index_condition": "((`employees`.`employees`.`birth_date` >= '1957-05-23') and (`employees`.`employees`.`birth_date` <= '1960-06-01') and (`employees`.`employees`.`hire_date` > '1998-03-22'))",
"cost_info": {
"read_cost": "188257.95",
"eval_cost": "9411.86",
"prefix_cost": "197669.81",
"data_read_per_join": "6M"
},
"used_columns": [
"emp_no",
"birth_date",
"first_name",
"last_name",
"gender",
"hire_date"
]
}
}
}
1 row in set, 1 warning (0.00 sec)
#### 结论
从上一步的成本结果来看，全表扫描的成本是 60725，而走 idx_test 索引的成本是 197669.81，因此优化器选择全表扫描。
实际上 ICP 可以减少回表次数，走 idx_test 索引时的真实回表次数是 1065，成本应该是：
- IO成本：1065*1 = 1065
- CPU成本：1065*0.2 = 213
但是优化器在计算回表成本时，显然没有考虑 ICP，直接将扫描索引的行数 141192 当作了回表的次数，所以得到的回表成本巨大，总成本远远大于全表扫描的成本。
因此，我们可以得到的结论是：ICP可以在执行阶段提高执行效率，但是在优化阶段并不能改善执行计划。