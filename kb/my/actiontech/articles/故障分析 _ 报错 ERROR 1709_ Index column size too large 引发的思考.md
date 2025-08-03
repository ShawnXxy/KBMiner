# 故障分析 | 报错 ERROR 1709: Index column size too large 引发的思考

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-%e6%8a%a5%e9%94%99-error-1709-index-column-size-too-large-%e5%bc%95%e5%8f%91%e7%9a%84%e6%80%9d%e8%80%83/
**分类**: 技术干货
**发布时间**: 2024-07-16T00:16:22-08:00

---

MySQL 5.6 升级遇到 1709 报错该怎么办？
> 作者：王田田，DBA，擅长发呆，偶尔热爱分享。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 1500 字，预计阅读需要 5 分钟。
## 背景
某日同事突然找到我说测试环境中有张表无法访问，SELECT、DML 和 DDL 执行均报错 `ERROR 1709 (HY000): Index column size too large. The maximum column size is 767 bytes.`。
其实看到 767 这个数字，大家可能会猜想这估计和 `compact/redundant` 行格式有关系，后续也确实证实了和这个有点关系。
问题发生了就要想办法处理，当时第一反应是能不能有些“特殊操作”调整一下元数据，但能力有限无法实现。由于是测试环境，数据没那么重要，而且还是单节点，后续处理无非是利用备份重做这套库；若不想重做，而且该表不重要，也可以直接废弃该表，但是 *xtrabackup* 备份可能会报错。
既然问题一旦发生，只能通过备份恢复来解决，那么我们应该探究一下如何提前避免该问题。
## 原因探究
以下为测试环境复现过程：
#### MySQL 5.6.21 原地升级至5 .7.20
先调整数据库配置文件，以下为简要升级步骤：
`shell>/mysql/mysql-5.7.20/bin/mysqld_safe ... &
shell>/mysql/mysql-5.7.20/bin/mysql_upgrade ...
mysql>shutdown;
shell>/mysql/mysql-5.7.20/bin/mysqld_safe ... &
`
#### MySQL 5.7.20 原地升级至 8.0.21
先调整数据库配置文件，以下为简要升级步骤：
`mysql>/mysql/mysql-8.0.21/bin/mysqld_safe ... &
mysql>shutdown;
shell>/mysql/mysql-8.0.21/bin/mysqld_safe ... &
`
#### 8.0.21 数据库添加字段并添加索引
*表默认字符集为 utf8*
`mysql> alter table sky.test add column test_col varchar(500);
Query OK, 0 rows affected (10.09 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> alter table sky.test add index idx_test_col(test_col);   
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
正常情况下，这个索引理应无法创建成功，会立即抛出错误 `ERROR 1071 (42000):Specified key was too long; max key length is 767 bytes`。当然一方面原因是 MySQL 5.7 及 8.0 默认行格式为 `dynamic`，另一方面即使显式指定 `row_format=compact`，也会立即抛出错误。示例如下：
`mysql>create table sky1 (id int);
Query OK, 0 rows affected (0.05 sec)
mysql>alter table sky1 add column test_col varchar(500);   
Query OK, 0 rows affected (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql>alter table sky1  add index idx_test_col(test_col); 
Query OK, 0 rows affected (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql>create table sky2(id int) row_format=compact;
Query OK, 0 rows affected (0.06 sec)
mysql>alter table sky2 add column test_col varchar(500); 
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql>alter table sky2 add index idx_test_col(test_col);
ERROR 1071 (42000): Specified key was too long; max key length is 767 bytes
`
数据库重启前，该表可正常访问。
#### 重启数据库
`systemctl stop mysqld_3306
systemctl start mysqld_3306
`
#### 查看表情况
```
mysql> select *from sky.test limit 1;
ERROR 1709 (HY000): Index column size too large. The maximum column size is 767 bytes.
mysql> alter table sky.test row_format=dynamic;
ERROR 1709 (HY000): Index column size too large. The maximum column size is 767 bytes.
mysql> alter table sky.test engine=innodb;
ERROR 1709 (HY000): Index column size too large. The maximum column size is 767 bytes.
mysql> check table sky.test ;
+------------------+--------+----------+--------------------------------------------------------------------+
| Table            | Op     | Msg_type | Msg_text                                                           |
+------------------+--------+----------+--------------------------------------------------------------------+
| sky.test         | check  | Error    | Index column size too large. The maximum column size is 767 bytes. |
| sky.test         | check  | Error    | Table 'sky.test' doesn't exist                                     |
| sky.test         | check  | error    | Corrupt                                                            |
+------------------+--------+----------+--------------------------------------------------------------------+
3 rows in set (0.01 sec)
```
#### 查看相关信息
```
mysql>select TABLE_SCHEMA,TABLE_NAME,ROW_FORMAT,CREATE_OPTIONS from information_schema.tables where table_schema='sky';
+--------------+------------+------------+--------------------+
| TABLE_SCHEMA | TABLE_NAME | ROW_FORMAT | CREATE_OPTIONS     |
+--------------+------------+------------+--------------------+
| sky          | test       | Compact    |                    |
| sky          | sky1       | Dynamic    |                    |
| sky          | sky2       | Compact    | row_format=COMPACT |
+--------------+------------+------------+--------------------+
```
#### 找不同的粗略猜想
`sky2` 表比 `test` 多了一个 `create_options` 选项，所以不会触发 bug。而且 `create_options` 是建表时显式指定的行格式 `compact`，而 `test` 表是在 5.6 版本隐式创建的行格式 `compact`；8.0默认创建表的行格式为 Dynamic（由 `innodb_default_row_format` 参数控制），Dynamic 行格式不会存在 767bytes 的限制。
碰到这样奇奇怪怪的问题，第一反应就是不走运碰到了 bug，因此先去 bug 库中搜索一番，果不其然搜到了[Bug #99791](https://bugs.mysql.com/bug.php?id=99791)，与我们测试环境的情况极为类似。
**Bug #99791** 中表明官方在 [MySQL 8.0.22](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-22.html) 版本修复了 *非显式定义的 redundant 行格式表允许创建的索引列大小超 767 bytes* 的 bug。实际上笔者在测试环境验证了一下 MySQL 8.0.22 确实已解决该问题，即隐式创建的 `compact` 行格式表在待创建的索引列超 767bytes 时直接返回错误 `ERROR 1071 (42000): Specified key was too long; max key length is 3072 bytes`。因此猜想虽然该 bug 行格式与笔者本次环境对不上，但应该解决的是同一个问题，都是为了解决因隐式定义compact/redundant行格式而导致的问题。
## 解决方案
综上所述，我们可以得出以下解决方案：
- MySQL 5.6 升级至 MySQL 8.0.21 时，避免使用原地升级的方案，可新建一个 MySQL 8.0.21 的环境，将数据逻辑导入并搭建复制关系；若 8.0.21 环境设置 `innodb_default_row_format=Dynamic` 参数，在逻辑导入/复制时新环境会自动将行格式转为 Dynamic。
- 升级时选择高于 MySQL 8.0.21 版本的数据库，避免触发该 bug。
- 若当前已经存在 MySQL 5.6 原地升级至 MySQL 8.0.21 的环境。
- 可通过以下 SQL 语句排查是否存在超过 767bytes 的问题表；若存在，可以趁现在数据库未重启，改造涉及的索引。
`select s.table_schema,s.table_name,s.index_name,s.column_name from information_schema.statistics s,information_schema.columns c,information_schema.tables i where s.table_name=c.table_name and s.table_schema=c.table_schema and c.column_name=s.column_name and s.table_name=i.table_name and s.table_schema=i.table_schema and i.row_format in ('Redundant','Compact') and (s.sub_part is null or s.sub_part>255) and c.character_octet_length >767;
`
- 筛选出隐式创建行格式为 `compact/redundant` 的表，并显式指定，如 `alter table xx row_format=dynamic/compact` 。相关 SQL 如下：
```
select TABLE_SCHEMA,TABLE_NAME,ROW_FORMAT,CREATE_OPTIONS from information_schema.tables where ROW_FORMAT in ('Compact','Redundant') and CREATE_OPTIONS='';
```
由于笔者能力实在有限，如有错误还望大家能够批评指正。