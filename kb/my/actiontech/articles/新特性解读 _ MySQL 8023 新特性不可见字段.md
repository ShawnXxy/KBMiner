# 新特性解读 | MySQL 8.0.23 新特性不可见字段

**原文链接**: https://opensource.actionsky.com/20210615-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-06-15T23:50:34-08:00

---

作者：王福祥
爱可生DBA团队成员，负责客户的数据库故障处理以及调优。擅长故障排查及性能优化。对数据库相关技术有浓厚的兴趣，喜欢分析各种逻辑。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
在 MySQL 8.0.23 版本中新添加了一个功能：可以给字段附加不可见属性。对于非指定字段的查询语句默认隐藏不可见字段的内容。该功能可适用于需要给表添加字段并需要对已有的业务系统隐藏时使用以及给表添加主键字段或索引字段时使用。
## 特性描述
MySQL 从 8.0.23 版本之前，所有表的字段均为可见字段，在 8.0.23 版本之后，可以给字段添加不可见属性。默认对 select * 等操作隐藏，只有当 sql 语句中指定该字段值时才会显示
官网连接：https://dev.mysql.com/doc/refman/8.0/en/invisible-columns.html
## 特性展示
1、新建一张表，给当中字段赋予不可见属性（INVISIBLE）
`mysql> CREATE TABLE t1 (id INT, name varchar(10) ,age INT INVISIBLE);
Query OK, 0 rows affected (0.02 sec)
`
2、建表语句以及表结构中均可以查看到不可见字段的字段信息
`| t1    | CREATE TABLE `t1` (
`id` int DEFAULT NULL,
`name` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
`age` int DEFAULT NULL /*!80023 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-------------+------+-----+---------+-----------+
| Field | Type        | Null | Key | Default | Extra     |
+-------+-------------+------+-----+---------+-----------+
| id    | int         | YES  |     | NULL    |           |
| name  | varchar(10) | YES  |     | NULL    |           |
| age   | int         | YES  |     | NULL    | INVISIBLE |
+-------+-------------+------+-----+---------+-----------+
`
3、在系统表 INFORMATION_SCHEMA.COLUMNS 中的 EXTRA 字段值中也可以查看到表字段值的不可见属性。
`mysql>  select TABLE_NAME, COLUMN_NAME, EXTRA from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='t1';
+------------+-------------+-----------+
| TABLE_NAME | COLUMN_NAME | EXTRA     |
+------------+-------------+-----------+
| t1         | id          |           |
| t1         | name        |           |
| t1         | age         | INVISIBLE |
+------------+-------------+-----------+
3 rows in set (0.00 sec)
`
## 注意事项
1、每张表必须要有至少一个可见字段。
2、不可见字段允许被定义为主键或创建2级索引，也可以定义自增属性。适合给已有的表添加主键或者索引。
3、使用 DML 语句时，如果涉及到不可见字段的值，需要在sql语句中显示指定该不可见字段。否则会按照默认方式，忽略不可见字段进行DML语句的解析和处理。同理 create table as select，insert into select 等，不可见字段需要明文指定，否则按默认不做处理。
`mysql> insert into t1  values(2,'mqd',23);
ERROR 1136 (21S01): Column count doesn't match value count at row 1
mysql> insert into t1  values(2,'mqd');
Query OK, 1 row affected (0.01 sec)
mysql> select * from t1;
+------+------+
| id   | name |
+------+------+
|    1 | wfx  |
|    2 | mqd  |
+------+------+
2 rows in set (0.00 sec)
mysql> select id,name,age from t1;
+------+------+------+
| id   | name | age  |
+------+------+------+
|    1 | wfx  |   25 |
|    2 | mqd  | NULL |
+------+------+------+
2 rows in set (0.00 sec)
`
4、使用 select&#8230;outfile 以及 load data 方式导入导出含不可见字段表时，默认对不可见列不做处理。如果需要导出不可见列的数据或者将数据导入至不可见列中，也需要明文指定字段名。
`mysql> load data infile "/tmp/t1.sql" into table t1;
ERROR 1262 (01000): Row 1 was truncated; it contained more data than there were input columns
mysql> load data infile "/tmp/t1.sql" into table t1 (id,name,age);
Query OK, 2 rows affected (0.02 sec)
Records: 2  Deleted: 0  Skipped: 0  Warnings: 0
`
5、允许给已有的字段附件不可见属性
`mysql> ALTER TABLE t1 MODIFY COLUMN name varchar(10) INVISIBLE;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc t1;
+-------+-------------+------+-----+---------+-----------+
| Field | Type        | Null | Key | Default | Extra     |
+-------+-------------+------+-----+---------+-----------+
| id    | int         | YES  |     | NULL    |           |
| name  | varchar(10) | YES  |     | NULL    | INVISIBLE |
| age   | int         | YES  |     | NULL    | INVISIBLE |
+-------+-------------+------+-----+---------+-----------+
3 rows in set (0.01 sec)
`
6、使用 mysqldump 备份时，逻辑备份文件自带不可见字段的建表语句，并明文指定了插入数据的字段值。
`DROP TABLE IF EXISTS `t1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t1` (
`id` int DEFAULT NULL,
`name` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
`age` int DEFAULT NULL /*!80023 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Dumping data for table `t1`
--
LOCK TABLES `t1` WRITE;
/*!40000 ALTER TABLE `t1` DISABLE KEYS */;
INSERT INTO `t1` (`id`, `name`, `age`) VALUES (1,'wfx',25),(2,'mqd',NULL);
/*!40000 ALTER TABLE `t1` ENABLE KEYS */;
UNLOCK TABLES;
`
7、binlog 会记录 DDL 的不可见列字段属性。当 binlog 为 STATEMENT 模式时，原始 DML 语句会被记录，当 binlog 为 ROW 模式时，不可见列如果有值，也会被记录。
`### INSERT INTO `test`.`t1`
### SET
###   @1=1 /* INT meta=0 nullable=1 is_null=0 */
###   @2='wfx' /* VARSTRING(40) meta=40 nullable=1 is_null=0 */
###   @3=25 /* INT meta=0 nullable=1 is_null=0 */
### INSERT INTO `test`.`t1`
### SET
###   @1=2 /* INT meta=0 nullable=1 is_null=0 */
###   @2='mqd' /* VARSTRING(40) meta=40 nullable=1 is_null=0 */
###   @3=NULL /* INT meta=0 nullable=1 is_null=1 */
`
## 结论
不可见字段这项新功能是对 mysql 表结构体系的一种补充。不仅允许用户对已使用的表做结构变更并且兼顾业务侧的需要。弥补了业务初期创建错误表结构这样的问题点。一定程度上提升了mysql 在使用上的容错率。