# 新特性解读 | 8.0 新增 DML 语句（TABLE &#038; VALUES）

**原文链接**: https://opensource.actionsky.com/20200325-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-03-25T00:34:57-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**背景**
MySQL 8.0.19 release 发布了两条新的 DML 语句。一条 TABLE 语句，一条 VALUES 语句。这里不要把这两条语句混淆了。
TABLE 不是广义的表，而仅仅是一条语句，应用于需要全表扫描的场景。
还有 VALUES 语句也不要混淆为 INSERT&#8230;VALUES&#8230;这样的传统插入语句。VALUES 是一个全新的模拟记录集的语句，类似于其他数据库比如 PGSQL 的 ROW 语句。
**一、应用场景**
1. TABLE 语句- 具体用在小表的全表扫描，比如路由表、配置类表、简单的映射表等。
- 用来替换是被当做子查询的这类小表的 SELECT 语句。
2. VALUES 语句- VALUES 类似于其他数据库的 ROW 语句，造数据时非常有用。
**二、语法使用**
那现在针对这两类 DML 语句，结合实际例子说明下其具体用途。
2.1 TABLE 语句
**具体语法：**- `TABLE table_name [ORDER BY column_name] [LIMIT number [OFFSET number]]`
其实从语法上看，可以排序，也可以过滤记录集，不过比较简单，没有 SELECT 那么强大。
**示例 1**
简单的建一张很小的表 y1，记录数为 10 条。
表 t1，插入 10 条记录- `mysql-(ytt/3305)->create table t1 (r1 int,r2 int);`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `mysql-(ytt/3305)->insert into t1`
- `    with recursive aa(a,b) as (`
- `    select 1,1`
- `    union all`
- `    select a+1,ceil(rand()*20) from aa where a < 10`
- `    ) select * from aa;`
- `Query OK, 10 rows affected (0.00 sec)`
- `Records: 10  Duplicates: 0  Warnings: 0`
简单全表扫描- `mysql-(ytt/3305)->select * from t1;`
- `+------+------+`
- `| r1   | r2   |`
- `+------+------+`
- `|    1 |    1 |`
- `|    2 |    9 |`
- `|    3 |    9 |`
- `|    4 |   17 |`
- `|    5 |   17 |`
- `|    6 |   16 |`
- `|    7 |    6 |`
- `|    8 |    1 |`
- `|    9 |   10 |`
- `|   10 |    3 |`
- `+------+------+`
- `10 rows in set (0.00 sec)`
TABLE 结果- `mysql-(ytt/3305)->table t1;`
- `+------+------+`
- `| r1   | r2   |`
- `+------+------+`
- `|    1 |    1 |`
- `|    2 |    9 |`
- `|    3 |    9 |`
- `|    4 |   17 |`
- `|    5 |   17 |`
- `|    6 |   16 |`
- `|    7 |    6 |`
- `|    8 |    1 |`
- `|    9 |   10 |`
- `|   10 |    3 |`
- `+------+------+`
- `10 rows in set (0.00 sec)`
看下 table 的执行计划- `mysql-(ytt/3305)->explain table t1 order by r1 limit 2\G`
- `*************************** 1. row ***************************`
- `           id: 1`
- `  select_type: SIMPLE`
- `        table: t1`
- `   partitions: NULL`
- `         type: ALL`
- `possible_keys: NULL`
- `          key: NULL`
- `      key_len: NULL`
- `          ref: NULL`
- `         rows: 10`
- `     filtered: 100.00`
- `        Extra: Using filesort`
- `1 row in set, 1 warning (0.00 sec)`
其实可以看到 TABLE 内部被 MySQL 转换为 SELECT 了。- `mysql-(ytt/3305)->show warnings\G`
- `*************************** 1. row ***************************`
- `  Level: Note`
- `   Code: 1003`
- `Message: /* select#1 */ select `ytt`.`t1`.`r1` AS `r1`,`ytt`.`t1`.`r2` AS `r2` from `ytt`.`t1` order by `ytt`.`t1`.`r1` limit 2`
- `1 row in set (0.00 sec)`
那其实从上面简单的例子可以看到 TABLE 在内部被转成了普通的 SELECT 来处理。
**示例 2**应用于子查询里的子表。这里要注意，内表的字段数量必须和外表过滤的字段数量一致。
克隆表 t1 结构- `mysql-(ytt/3305)->create table t2 like t1;`
- `Query OK, 0 rows affected (0.02 sec)`
克隆表 t1 数据- `mysql-(ytt/3305)->insert into t2 table t1;`
- `Query OK, 10 rows affected (0.00 sec)`
- `Records: 10  Duplicates: 0  Warnings: 0`
table t1 被当做内表，表 t1 有两个字段，必须同时满足 t2 检索时过滤的字段也是两个。
- `mysql-(ytt/3305)->select * from t2 where (r1,r2) in (table t1);`
- `+------+------+`
- `| r1   | r2   |`
- `+------+------+`
- `|    1 |    1 |`
- `|    2 |    9 |`
- `|    3 |    9 |`
- `|    4 |   17 |`
- `|    5 |   17 |`
- `|    6 |   16 |`
- `|    7 |    6 |`
- `|    8 |    1 |`
- `|    9 |   10 |`
- `|   10 |    3 |`
- `+------+------+`
- `10 rows in set (0.00 sec)`
注意：这里如果过滤的字段数量和子表数量不一致，则会报错。
2.2 VALUES 语句
**具体语法：**- `VALUES row_constructor_list`
- `[ORDER BY column_designator]`
- `[LIMIT BY number] row_constructor_list:`
- `    ROW(value_list)[, ROW(value_list)][, ...]`
- `value_list:`
- `    value[, value][, ...]`
- `column_designator:`
- `    column_index`
VALUES 语句，用做功能展示或者快速造数据场景，结果列名字以 COLUMN_0 开头，以此类推，举个简单例子。
单条 VALUES 语句- `mysql-(ytt/3305)->values row(1,2,3);`
- `+----------+----------+----------+`
- `| column_0 | column_1 | column_2 |`
- `+----------+----------+----------+`
- `|        1|        2|        3|`
- `+----------+----------+----------+`
- `1 row inset(0.00 sec)`
多条 VALUES 语句- `mysql-(ytt/3305)->values row(1,2,3),row(10,9,8);`
- `+----------+----------+----------+`
- `| column_0 | column_1 | column_2 |`
- `+----------+----------+----------+`
- `|        1 |        2 |        3 |`
- `|       10 |        9 |        8 |`
- `+----------+----------+----------+`
- `2 rows in set (0.00 sec)`
多条 VALUES 联合 UNION ALL- `mysql-(ytt/3305)->values row(1,2,3),row(10,9,8) union all values \`
- `    row(-1,-2,0),row(10,29,30),row(100,20,-9);`
- `+----------+----------+----------+`
- `| column_0 | column_1 | column_2 |`
- `+----------+----------+----------+`
- `|        1 |        2 |        3 |`
- `|       10 |        9 |        8 |`
- `|       -1 |       -2 |        0 |`
- `|       10 |       29 |       30 |`
- `|      100 |       20 |       -9 |`
- `+----------+----------+----------+`
- `5 rows in set (0.00 sec)`
根据字段下标排序，从 1 开始- `mysql-(ytt/3305)->values row(1,2,3),row(10,9,8) union all values \`
- `    row(-1,-2,0),row(10,29,30),row(100,20,-9) order by 1 desc ;`
- `+----------+----------+----------+`
- `| column_0 | column_1 | column_2 |`
- `+----------+----------+----------+`
- `|      100 |       20 |       -9 |`
- `|       10 |        9 |        8 |`
- `|       10 |       29 |       30 |`
- `|        1 |        2 |        3 |`
- `|       -1 |       -2 |        0 |`
- `+----------+----------+----------+`
- `5 rows in set (0.00 sec)`
类型可以任意组合：bit,json,datetime,int,decimal 等- `mysql-(ytt/3305)->values row(100,200,300),\`
- `    row('2020-03-10 12:14:15','mysql','test'), \`
- `    row(16.22,TRUE,b'1'), \`
- `    row(left(uuid(),8),'{"name":"lucy","age":"28"}',hex('dble'));`
- `+---------------------+----------------------------+--------------------+`
- `| column_0            | column_1                   | column_2           |`
- `+---------------------+----------------------------+--------------------+`
- `| 100                 | 200                        | 0x333030           |`
- `| 2020-03-10 12:14:15 | mysql                      | 0x74657374         |`
- `| 16.22               | 1                          | 0x01               |`
- `| c86fd1a7            | {"name":"lucy","age":"28"} | 0x3634363236433635 |`
- `+---------------------+----------------------------+--------------------+`
- `4 rows in set (0.00 sec)`
新建表 t3，把刚才这些记录写进去- `mysql-(ytt/3305)->create table t3 (r1 varchar(100),r2 varchar(100),r3 varchar(100));`
- `Query OK, 0 rows affected (0.02 sec)`
写入到表 t3- `mysql-(ytt/3305)->insert into t3 values row(100,200,300), \`
- `    row('2020-03-10 12:14:15','mysql','test'), \`
- `    row(16.22,TRUE,b'1'),\`
- `    row(left(uuid(),8),'{"name":"lucy","age":"28"}',hex('dble'));`
- `Query OK, 4 rows affected (0.00 sec)`
- `Records: 4  Duplicates: 0  Warnings: 0`
**总结**
这里介绍了 MySQL 8.0.19 里发布后新增的两条 DML 语句 TABLE 和 VALUES，希望对大家有帮助。