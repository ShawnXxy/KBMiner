# 技术分享 | 盘点 MySQL 创建内部临时表的所有场景

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e7%9b%98%e7%82%b9-mysql-%e5%88%9b%e5%bb%ba%e5%86%85%e9%83%a8%e4%b8%b4%e6%97%b6%e8%a1%a8%e7%9a%84%e6%89%80%e6%9c%89%e5%9c%ba%e6%99%af/
**分类**: MySQL 新特性
**发布时间**: 2023-11-06T22:19:50-08:00

---

作者总结了 MySQL 中所有触发使用内部临时表的场景。
> 作者：刘嘉浩，爱可生团队 DBA 成员，重度竞技游戏爱好者。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 2000 字，预计阅读需要 5 分钟。
临时表属于是一种临时存放数据的表，这类表在会话结束时会被自动清理掉，但在 MySQL 中存在两种临时表，一种是外部临时表，另外一种是内部临时表。
外部临时表指的是用户使用 `CREATE TEMPORARY TABLE` 手动创建的临时表。而内部临时表用户是无法控制的，并不能像外部临时表一样使用 CREATE 语句创建，MySQL 的优化器会自动选择是否使用内部临时表。
那么由此引发一个问题，**MySQL 到底在什么时候会使用内部临时表呢？**
我们将针对 UNION、GROUP BY 等场景进行分析。
# UNION 场景
首先准备一个测试表。
`CREATE TABLE `employees` (
`id` int NOT NULL AUTO_INCREMENT,
`first_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
`last_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
`sex` enum('M','F') COLLATE utf8mb4_bin DEFAULT NULL,
`age` int DEFAULT NULL,
`birth_date` date DEFAULT NULL,
`hire_date` date DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `last_name` (`last_name`),
KEY `hire_date` (`hire_date`)
) ENGINE=InnoDB AUTO_INCREMENT=500002 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
`
准备插入数据的脚本。
`#! /usr/bin/python
#! coding=utf-8
import random
import pymysql
from faker import Faker
from datetime import datetime, timedelta
# 创建Faker实例
fake = Faker()
# MySQL连接参数
db_params = {
'host': 'localhost',
'user': 'root',
'password': 'root',
'db': 'db1',
'port': 3311
}
# 连接数据库
connection = pymysql.connect(**db_params)
# 创建一个新的Cursor实例
cursor = connection.cursor()
# 生成并插入数据
for i in range(5000):
id = (i+1)
first_name = fake.first_name()
last_name = fake.last_name()
sex = random.choice(['M', 'F'])
age = random.randint(20, 60)
birth_date = fake.date_between(start_date='-60y', end_date='-20y')
hire_date = fake.date_between(start_date='-30y', end_date='today')
query = f"""INSERT INTO employees (id, first_name, last_name, sex, age, birth_date, hire_date)
VALUES ('{id}', '{first_name}', '{last_name}', '{sex}', {age}, '{birth_date}', '{hire_date}');"""
cursor.execute(query)
# 每1000提交一次事务
if (i+1) % 1000 == 0:
connection.commit()
# 最后提交事务
connection.commit()
# 关闭连接
cursor.close()
connection.close()
`
在创建好测试数据后，执行一个带有 UNION 的语句。
`root@localhost:mysqld.sock[db1]> explain (select 5000 as res from dual) union (select id from employees order by id desc limit 2);
+----+--------------+------------+------------+-------+---------------+---------+---------+------+------+----------+----------------------------------+
| id | select_type  | table      | partitions | type  | possible_keys | key     | key_len | ref  | rows | filtered | Extra                            |
+----+--------------+------------+------------+-------+---------------+---------+---------+------+------+----------+----------------------------------+
|  1 | PRIMARY      | NULL       | NULL       | NULL  | NULL          | NULL    | NULL    | NULL | NULL |     NULL | No tables used                   |
|  2 | UNION        | employees  | NULL       | index | NULL          | PRIMARY | 4       | NULL |    2 |   100.00 | Backward index scan; Using index |
| NULL | UNION RESULT | <union1,2> | NULL       | ALL   | NULL          | NULL    | NULL    | NULL | NULL |     NULL | Using temporary                  |
+----+--------------+------------+------------+-------+---------------+---------+---------+------+------+----------+----------------------------------+
3 rows in set, 1 warning (0.00 sec)
`
可见第二行中 key 值是 PRIMARY，即第二个查询使用了主键 ID。第三行 extra 值是 Using temporary，表明在对上面两个查询的结果集做 UNION 的时候，使用了临时表。
UNION 操作是将两个结果集取并集，不包含重复项。要做到这一点，只需要先创建一个只有主键的内存内部临时表，并将第一个子查询的值插入进这个表中，这样就可以避免了重复的问题。因为值 5000 早已存在临时表中，而第二个子查询的值 5000 就会因为冲突无法插入，只能插入下一个值 4999。
UNION ALL 与 UNION 不同，并不会使用内存临时表，下列例子是使用 UNION ALL 的执行计划。
`root@localhost:mysqld.sock[db1]> explain (select 5000 as res from dual) union all (select id from employees order by id desc limit 2);
+----+-------------+-----------+------------+-------+---------------+---------+---------+------+------+----------+----------------------------------+
| id | select_type | table     | partitions | type  | possible_keys | key     | key_len | ref  | rows | filtered | Extra                            |
+----+-------------+-----------+------------+-------+---------------+---------+---------+------+------+----------+----------------------------------+
|  1 | PRIMARY     | NULL      | NULL       | NULL  | NULL          | NULL    | NULL    | NULL | NULL |     NULL | No tables used                   |
|  2 | UNION       | employees | NULL       | index | NULL          | PRIMARY | 4       | NULL |    2 |   100.00 | Backward index scan; Using index |
+----+-------------+-----------+------------+-------+---------------+---------+---------+------+------+----------+----------------------------------+
2 rows in set, 1 warning (0.01 sec)
`
因为 UNION ALL 并不需要去重，所以优化器不需要新建一个临时表做去重的动作，执行的时候只需要按顺序执行两个子查询并将子查询放在一个结果集里就好了。
可以看到，在实现 UNION 的语义上，临时表起到的是一个暂时存储数据并做去重的动作的这么一种作用的存在。
# GROUP BY
除了 UNION 之外，还有一个比较常用的子句 GROUP BY 也会使用到内部临时表。下列例子展示了一个使用 ID 列求余并进行分组统计，且按照余数大小排列。
`
root@localhost:mysqld.sock[db1]> explain select id%5 as complementation,count(*) from employees group by complementation order by 1;
+----+-------------+-----------+------------+-------+-----------------------------+-----------+---------+------+------+----------+----------------------------------------------+
| id | select_type | table     | partitions | type  | possible_keys               | key       | key_len | ref  | rows | filtered | Extra                                        |
+----+-------------+-----------+------------+-------+-----------------------------+-----------+---------+------+------+----------+----------------------------------------------+
|  1 | SIMPLE      | employees | NULL       | index | PRIMARY,last_name,hire_date | hire_date | 4       | NULL | 5000 |   100.00 | Using index; Using temporary; Using filesort |
+----+-------------+-----------+------------+-------+-----------------------------+-----------+---------+------+------+----------+----------------------------------------------+
1 row in set, 1 warning (0.00 sec)
`
可以看到 extra 的值是 using index、using temporary、using filesort; 这三个值分别是：使用索引、使用临时表、使用了排序。
> 注意：在 MySQL 5.7 版本中 GROUP BY 会默认按照分组字段进行排序，在 MySQL 8.0 版本中取消了默认排序功能，所以此处使用了 ORDER BY 进行复现。
对于 GROUP BY 来说，上述的语句执行后，会先创建一个内存内部临时表，存储 `complementation` 与 `count(*)` 的值，主键为 `complementation`。然后按照索引 `hire_date` 对应的 ID 值依次计算 id%5 的值记为 `x`，如果临时表中没有主键为 `x` 的值，那么将会在临时表中插入记录；如果存在则累加这一行的计数 `count(*)`。在遍历完成上述的操作后，再按照 ORDER BY 的规则对 `complementation` 进行排序。
在使用 GROUP BY 进行分组或使用 DISTINCT 进行去重时，MySQL 都给我们提供了使用 hint 去避免使用内存内部临时表的方法。
| hint | 解释 |
| --- | --- |
| SQL_BIG_RESULT | 显式指定该 SQL 语句使用磁盘内部临时表，适合大数据量的操作；适用于 InnoDB 引擎与 Memory 引擎。 |
| SQL_SMALL_RESULT | 显式指定该 SQL 语句使用内存内部临时表，速度更快，适合小数据量的操作；适用于 Memory 引擎。 |
下列是一个使用了 SQL_BIG_RESULT 的例子。
`root@localhost:mysqld.sock[db1]> explain select SQL_BIG_RESULT id%5 as complementation,count(*) from employees group by complementation order by 1;
+----+-------------+-----------+------------+-------+-----------------------------+-----------+---------+------+------+----------+-----------------------------+
| id | select_type | table     | partitions | type  | possible_keys               | key       | key_len | ref  | rows | filtered | Extra                       |
+----+-------------+-----------+------------+-------+-----------------------------+-----------+---------+------+------+----------+-----------------------------+
|  1 | SIMPLE      | employees | NULL       | index | PRIMARY,last_name,hire_date | hire_date | 4       | NULL | 5000 |   100.00 | Using index; Using filesort |
+----+-------------+-----------+------------+-------+-----------------------------+-----------+---------+------+------+----------+-----------------------------+
1 row in set, 1 warning (0.00 sec)
`
从执行计划中我们可以看出，使用了 SQL_BIG_RESULT 这个 hint 进行查询后，在 extra 列中 Using Temporary 字样已经不见了，即避免了使用内存内部临时表。
# 其他场景
当然，除了上述两个例子外，MySQL 还会在下列情况下创建内部临时表：
- 对于UNION语句的评估，但有一些后续描述中的例外情况。
- 对于某些视图的评估，例如使用 TEMPTABLE 算法、UNION 或聚合的视图。
- 对派生表的评估。
- 对公共表达式的评估。
- 用于子查询或半连接材料化的表。
- 对包含 ORDER BY 子句和不同 GROUP BY 子句的语句的评估，或者对于其中 ORDER BY 或 GROUP BY 子句包含来自连接队列中第一个表以外的表的列的语句。
- 对于 DISTINCT 与 ORDER BY 的组合，可能需要一个临时表。
- 对于使用 SQL_SMALL_RESULT 修饰符的查询，MySQL 使用内存中的临时表，除非查询还包含需要在磁盘上存储的元素。
- 为了评估从同一表中选取并插入的 INSERT … SELECT 语句，MySQL 创建一个内部临时表来保存 SELECT 的行，然后将这些行插入目标表中。
- 对于多表 UPDATE 语句的评估。
- 对于 GROUP_CONCAT() 或 COUNT(DISTINCT) 表达式的评估。
- 窗口函数的评估，根据需要使用临时表。
值得注意的是，某些查询条件 MySQL 不允许使用内存内部临时表，在这种情况下，服务器会使用磁盘内部临时表。
- 表中存在 BLOB 或 TEXT 列。MySQL 8.0 中用于内存内部临时表的默认存储引擎 TempTable 从 8.0.13 开始支持二进制大对象类型。
- 如果使用了 UNION 或 UNION ALL，SELECT 的列表中存在任何最大长度超过 512 的字符串列（对于二进制字符串为字节，对于非二进制字符串为字符）。
- SHOW COLUMNS 和 DESCRIBE 语句使用 BLOB 作为某些列的类型，因此用于此结果的临时表是将会是磁盘内部临时表。
## 参考资料
[1]: 丁奇 《MySQL45讲》 37.什么时候会使用内部临时表？
[2]: 8.4.4 Internal Temporary Table Use in MySQL URL:[https://dev.mysql.com/doc/refman/8.0/en/internal-temporary-tables.html](https://dev.mysql.com/doc/refman/8.0/en/internal-temporary-tables.html)