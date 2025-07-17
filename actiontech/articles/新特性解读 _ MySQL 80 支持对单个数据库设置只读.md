# 新特性解读 | MySQL 8.0 支持对单个数据库设置只读！

**原文链接**: https://opensource.actionsky.com/%e6%96%b0%e7%89%b9%e6%80%a7%e8%a7%a3%e8%af%bb-mysql-8-0-%e6%94%af%e6%8c%81%e5%af%b9%e5%8d%95%e4%b8%aa%e6%95%b0%e6%8d%ae%e5%ba%93%e8%ae%be%e7%bd%ae%e5%8f%aa%e8%af%bb%ef%bc%81/
**分类**: MySQL 新特性
**发布时间**: 2024-03-26T23:36:57-08:00

---

MySQL 8.0.22 支持对单个数据库设置只读，当一个实例中只需要迁移部分数据库时比较实用，避免数据库迁移过程中数据库及其对象被修改。
> 作者：李富强，爱可生 DBA 团队成员，熟悉 MySQL，TiDB，OceanBase 等数据库。相信持续把对的事情做好一点，会有不一样的收获。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 1600 字，预计阅读需要 5 分钟。
# 新特性概要
对单个数据库设置只读状态，可以通过 *ALTER DATABASE* 语句中的 `READ ONLY` 选项来实现，该选项在 [MySQL 8.0.22 版本](https://dev.mysql.com/doc/refman/8.0/en/alter-database.html#alter-database-read-only) 中引入，用于控制是否允许对数据库及其对象（包括其定义、数据和元数据）进行写入操作。
当只需要迁移一个实例当中的 **部分** 数据库时，对部分数据库开启 **READ ONLY**，不用担心数据库迁移期间这些数据库被修改。
# 使用方法
以设置数据库 *lfq* 为只读状态举例，可以观测到修改数据库只读状态对已建立连接的用户是立即生效的（即：*session1* 修改 *lfq* 数据库为只读，*session2* 中 *lfq* 的只读状态是立即生效的。）
`#session1
MySQL  localhost:3000 ssl  SQL > select version(),@@port,connection_id();
+-----------+--------+-----------------+
| version() | @@port | connection_id() |
+-----------+--------+-----------------+
| 8.0.22    |   3000 |              22 |
+-----------+--------+-----------------+
1 row in set (0.0015 sec)
#session2
MySQL  localhost:3000 ssl  SQL > select version(),@@port,connection_id();
+-----------+--------+-----------------+
| version() | @@port | connection_id() |
+-----------+--------+-----------------+
| 8.0.22    |   3000 |              24 |
+-----------+--------+-----------------+
1 row in set (0.0009 sec)
#session1，修改前查一下数据库的只读状态，OPTIONS值为空，代表数据库非只读状态
MySQL  localhost:3000 ssl  SQL > SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS WHERE SCHEMA_NAME = 'lfq';
+--------------+-------------+---------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS |
+--------------+-------------+---------+
| def          | lfq         |         |
+--------------+-------------+---------+
1 row in set (0.0057 sec)
#session1，修改数据库为只读状态
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 1;
Query OK, 1 row affected (0.0127 sec)
#session1，再次查一下数据库的只读状态，OPTIONS值为“READ ONLY=1”，数据库只读状态修改成功
MySQL  localhost:3000 ssl  SQL > SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS WHERE SCHEMA_NAME = 'lfq';
+--------------+-------------+-------------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS     |
+--------------+-------------+-------------+
| def          | lfq         | READ ONLY=1 |
+--------------+-------------+-------------+
1 row in set (0.0048 sec)
#session1，在lfq库中新建一张表测试下,数据库只读状态建表失败
MySQL  localhost:3000 ssl  SQL > create table lfq.t1(c1 int primary key,n1 varchar(20) );
ERROR: 3989 (HY000): Schema 'lfq' is in read only mode.
#session1，表lfq.my_table插入数据测试（my_table为提前建的表），数据库只读状态表插入数据失败
MySQL  localhost:3000 ssl  lfq  SQL > INSERT INTO my_table (name, age, email) VALUES ('LFQ', 18, 'lfq#actionsky.com');
ERROR: 3989 (HY000): Schema 'lfq' is in read only mode.
#session1，表lfq.my_table更新数据测试，数据库只读状态表更新数据失败
MySQL  localhost:3000 ssl  lfq  SQL > UPDATE my_table SET age = 30 WHERE name = 'LFQ';
ERROR: 3989 (HY000): Schema 'lfq' is in read only mode.
#session1，表lfq.my_table删除数据测试，数据库只读状态表删除数据失败
MySQL  localhost:3000 ssl  lfq  SQL > DELETE FROM my_table WHERE name = 'LFQ';
ERROR: 3989 (HY000): Schema 'lfq' is in read only mode.
#session2，查询数据库只读状态，数据库为只读状态，session1修改lfq数据库为只读，session2中lfq的只读状态是立即生效的
MySQL  localhost:3000 ssl  SQL > SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS WHERE SCHEMA_NAME = 'lfq';
+--------------+-------------+-------------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS     |
+--------------+-------------+-------------+
| def          | lfq         | READ ONLY=1 |
+--------------+-------------+-------------+
1 row in set (0.0016 sec)
#session2，在lfq库中新建一张表测试下,数据库为只读状态下建表失败
MySQL  localhost:3000 ssl  SQL > create table lfq.t1(c1 int primary key,n1 varchar(20) );
ERROR: 3989 (HY000): Schema 'lfq' is in read only mode.
`
# 查询 READ ONLY 状态
## 方法一
通过查询 *INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS* 表（在 MySQL 8.0.22 版本引入），输出结果中如果 *OPTIONS* 列的值为 `READ ONLY=1`，则说明数据库为只读状态，如果 *OPTIONS* 列的值为空，则说明数据库为非只读状态。
`MySQL  localhost:3000 ssl  SQL > select version(),@@port;
+-----------+--------+
| version() | @@port |
+-----------+--------+
| 8.0.22    |   3000 |
+-----------+--------+
1 row in set (0.0029 sec)
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 1;
Query OK, 1 row affected (0.0098 sec)
MySQL  localhost:3000 ssl  SQL >
MySQL  localhost:3000 ssl  SQL >
MySQL  localhost:3000 ssl  SQL >
MySQL  localhost:3000 ssl  SQL > SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS WHERE SCHEMA_NAME = 'lfq';
+--------------+-------------+-------------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS     |
+--------------+-------------+-------------+
| def          | lfq         | READ ONLY=1 |
+--------------+-------------+-------------+
1 row in set (0.0063 sec)
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 0;
Query OK, 1 row affected (0.0098 sec)
MySQL  localhost:3000 ssl  SQL > SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS WHERE SCHEMA_NAME = 'lfq';
+--------------+-------------+---------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS |
+--------------+-------------+---------+
| def          | lfq         |         |
+--------------+-------------+---------+
1 row in set (0.0017 sec)
`
## 方法二
通过 *SHOW CREATE DATABASE* 语句查看，如果输出结果中带关键字 `READ ONLY=1`，则表明数据库为只读状态。
`MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 1;
Query OK, 1 row affected (0.0118 sec)
MySQL  localhost:3000 ssl  SQL >  show create database lfq;
+----------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Database | Create Database                                                                                                                            |
+----------+--------------------------------------------------------------------------------------------------------------------------------------------+
| lfq      | CREATE DATABASE `lfq` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */ /* READ ONLY = 1 */ |
+----------+--------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.0011 sec)
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 0;
Query OK, 1 row affected (0.0108 sec)
MySQL  localhost:3000 ssl  SQL >  show create database lfq;
+----------+------------------------------------------------------------------------------------------------------------------------+
| Database | Create Database                                                                                                        |
+----------+------------------------------------------------------------------------------------------------------------------------+
| lfq      | CREATE DATABASE `lfq` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */ |
+----------+------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.0023 sec)
`
# 使用限制以及注意事项
- `READ ONLY` 选项不能用在 `mysql, information_schema, performance_schema` 等系统数据库上。
```
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA mysql READ ONLY = 1 ;
ERROR: 3552 (HY000): Access to system schema 'mysql' is rejected.
```
- *ALTER DATABASE* 语句不能同时指定多个不同值的 `READ ONLY` 选项，否则会报错。
```
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 1 READ ONLY = 0;
ERROR: 1302 (HY000): Conflicting declarations: 'READ ONLY=0' and 'READ ONLY=1'
```
- *ALTER DATABASE* 语句在 `READ ONLY` 选项和其他选项混用时且 `READ ONLY` 设置为 1，执行 *ALTER DATABASE* 语句前如果数据库的 `READ ONLY = 1`，则修改报错。
```
MySQL  localhost:3000 ssl  SQL > ALTER SCHEMA lfq READ ONLY = 1 ;
Query OK, 1 row affected (0.0141 sec)
MySQL  localhost:3000 ssl  SQL > SELECT * FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS WHERE SCHEMA_NAME = 'lfq';
+--------------+-------------+-------------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS     |
+--------------+-------------+-------------+
| def          | lfq         | READ ONLY=1 |
+--------------+-------------+-------------+
1 row in set (0.0069 sec)
MySQL  localhost:3000 ssl  SQL > ALTER DATABASE lfq READ ONLY = 1 DEFAULT COLLATE utf8mb4_bin;
ERROR: 3989 (HY000): Schema 'lfq' is in read only mode.
```
- *ALTER DATABASE* 语句会等待该数据库中正在更改的对象的并发事务都已提交后才能执行，反过来也一样，数据库中正在更改的对象的并发事务的执行，需要等待 *ALTER DATABASE* 语句执行完成。
- 对于只读数据库，*SHOW CREATE DATABASE* 生成的语句包含带注释的 `READ ONLY` 选项（/* READ ONLY = 1 */），使用逻辑备份工具 *mysqldump* 或者 *mysqlpump* 备份只读数据库，通过备份文件恢复出来的数据库不是只读的，如果恢复后需要只读，则需要手动执行 *ALTER DATABASE* 语句设置数据库为只读。
# 例外情况
*不受数据库只读状态的约束。*
- 作为 MySQL 服务初始化，重启，升级，复制功能中的一部分执行的语句。
- 在服务器启动时由 `init_file` 系统变量命名的文件中的语句。
- 可以在只读数据库中创建、更改、删除和写入临时表（*TEMPORARY* 表。）