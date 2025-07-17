# 技术译文 | MySQL 8.x DDL 和查询重写插件

**原文链接**: https://opensource.actionsky.com/20200812-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-08-12T00:41:04-08:00

---

作者：Sri Sakthivel
翻译：管长龙
本文来源：https://www.percona.com/blog/2020/08/07/mysql-8-x-ddl-rewriter-and-query-rewriter-plugins-implementation-and-use-cases/
对 MySQL 查询重写以提高性能是每个 DBA 应该意识到的重要过程，以便他们可以在运行时修复错误的查询，而无需在应用程序端更改代码。
到目前为止，MySQL 社区提供了两个内置的查询重写插件来执行此任务。
- query rewriter plugin：它支持 INSERT / UPDATE / DELETE / REPLACE 语句，在  MySQL 8.0.12 引入。 
- ddl_rewritter plugin：它支持 CREATE TABLE 语句。在 MySQL 8.0.16 引入。
本文将解释实现和插件测试的完整过程。该测试基于 MySQL 8.x 功能。
**一、查询重写插件**
该插件将有助于修改服务器在执行之前接收到的 SQL 语句。在 MySQL 8.0.12 之前，该插件仅支持 SELECT。从 MySQL 8.0.12 起，该插件还支持 INSERT / UPDATE / DELETE / REPLACE。
1.1 准备环境
有两个 SQL 文件可以执行安装和卸载操作。这些文件位于共享目录下。
`mysql> show global variables like 'lc_messages_dir';
+-----------------+----------------------------+
| Variable_name   | Value                      |
+-----------------+----------------------------+
| lc_messages_dir | /usr/share/percona-server/ |
+-----------------+----------------------------+
1 row in set (0.01 sec)
[root@hercules7sakthi3 ~]# cd /usr/share/mysql-8.0/
[root@hercules7sakthi3 mysql-8.0]# ls -lrth | grep -i rewriter
-rw-r--r--. 1 root root 1.3K Mar 26 14:16 uninstall_rewriter.sql
-rw-r--r--. 1 root root 2.2K Mar 26 14:16 install_rewriter.sql`- 我们可以在运行时实现重写器插件；
- 加载 SQL 文件 &#8220;install_rewritter.sql&#8221; 时，它将安装插件 &#8220;rewriter.so&#8221;，并为操作创建其自己的数据库，表和函数。
通过加载安装程序SQL文件来安装插件：
`[root@hercules7sakthi3 mysql-8.0]# mysql -vv < install_rewriter.sql | grep -i 'create\|install\|drop'
CREATE DATABASE IF NOT EXISTS query_rewrite
CREATE TABLE IF NOT EXISTS query_rewrite.rewrite_rules (
INSTALL PLUGIN rewriter SONAME 'rewriter.so'
CREATE FUNCTION load_rewrite_rules RETURNS STRING
CREATE PROCEDURE query_rewrite.flush_rewrite_rules()
mysql> show schemas like 'query_rewrite';
+--------------------------+
| Database (query_rewrite) |
+--------------------------+
| query_rewrite            |
+--------------------------+
1 row in set (0.00 sec)
mysql> show tables from query_rewrite;
+-------------------------+
| Tables_in_query_rewrite |
+-------------------------+
| rewrite_rules           |
+-------------------------+
1 row in set (0.05 sec)
mysql> show create table query_rewrite.rewrite_rules\G
*************************** 1. row ***************************
Table: rewrite_rules
Create Table: CREATE TABLE `rewrite_rules` (
`id` int NOT NULL AUTO_INCREMENT,
`pattern` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
`pattern_database` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
`replacement` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
`enabled` enum('YES','NO') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT 'YES',
`message` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
`pattern_digest` varchar(64) DEFAULT NULL,
`normalized_pattern` varchar(100) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql> select plugin_name,plugin_status, plugin_version from information_schema.plugins where plugin_name='Rewriter';
+-------------+---------------+----------------+
| plugin_name | plugin_status | plugin_version |
+-------------+---------------+----------------+
| Rewriter    | ACTIVE        | 0.2            |
+-------------+---------------+----------------+
1 row in set (0.00 sec)`
1.2 测试案例
创建表 qrw8012，并做了一些记录以供测试。
`mysql> show create table qrw8012\G
*************************** 1. row ***************************
Table: qrw8012
Create Table: CREATE TABLE `qrw8012` (
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(16) DEFAULT NULL,
`dob` date DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
mysql> select * from qrw8012;
+----+--------+------------+
| id | name   | dob        |
+----+--------+------------+
|  1 | jc     | 0001-01-01 |
|  2 | sriram | 1993-06-17 |
|  3 | vijaya | 1969-11-23 |
|  4 | durai  | 1963-10-19 |
|  5 | asha   | 1992-06-26 |
|  6 | sakthi | 1992-07-13 |
+----+--------+------------+
6 rows in set (0.00 sec)`
1.3 需求描述
要求是将 name  列从 sakthi 更新为 hercules7sakthi，其中 id =6。来自应用程序的 UPDATE 查询如下所示：
`update qrw8012 set name='hercules7sakthi' where LOWER(name)='sakthi';`
从数据库的角度来看，所有的行都仅使用小写字母进行更新。因此，这里不需要 LOWER 功能。同样，在 WHERE 子句列上使用 LOWER 函数将隐藏该特定列的索引。在我们的例子中，查询将扫描整个表（FTS）。
`mysql> show create table qrw8012\G
……
KEY `idx_name` (`name`)
……
1 row in set (0.18 sec)
mysql> explain select * from qrw8012 where LOWER(name)='sakthi'\G
*************************** 1. row ***************************
id: 1
select_type: SIMPLE
table: qrw8012
partitions: NULL
type: ALL
possible_keys: NULL
key: NULL
key_len: NULL
ref: NULL
rows: 6
filtered: 100.00
Extra: Using where
1 row in set, 1 warning (0.00 sec)`
它将进行全表扫描（FTS）。
**注意：出于分析目的，我已将 UPDATE 转换为 SELECT。**
在上面的示例中，name 列有索引。但是，它仍然不能与 LOWER 功能一起使用。如果删除 LOWER 函数，则索引可用。让我们看看如何使用查询重写插件解决此问题。
第一步，我需要更新 rewrite_rules 表中的查询规则。以下是更新查询规则时要遵循的关键点。
- 我们必须使用查询摘要输出来配置查询规则；
- 修改规则表后，我们始终需要调用函数 flush_rewrite_rules；
- 如果错误地配置了查询规则，则会收到错误消息 &#8220;ERROR 1644（45000）：某些规则加载失败。&#8221; 在刷新函数调用期间；
- 我们可以检查警告消息以了解是否应用了查询规则。
`mysql> insert into rewrite_rules
-> (id,pattern_database,pattern,replacement) values
-> (1,'percona','update qrw8012 set name = ? where LOWER(name) = ?','update qrw8012 set name = ? where name = ?');
Query OK, 1 row affected (0.01 sec)
mysql> call query_rewrite.flush_rewrite_rules();
Query OK, 1 row affected (0.03 sec)
mysql> select id,pattern_database,pattern,replacement from rewrite_rules\G
*************************** 1. row ***************************
id: 1
pattern_database: percona
pattern: update qrw8012 set name = ? where LOWER(name) = ?
replacement: update qrw8012 set name = ? where name = ?
1 row in set (0.00 sec)`
我配置了查询规则，因此现在执行查询。
`mysql> update qrw8012 set name='hercules7sakthi' where LOWER(name)='sakthi';
Query OK, 1 row affected, 1 warning (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 1
mysql> show warnings\G
*************************** 1. row ***************************
Level: Note
Code: 1105
Message: Query 'update qrw8012 set name='hercules7sakthi' where LOWER(name)='sakthi'' rewritten to 'update qrw8012 set name = 'hercules7sakthi' where name = 'sakthi'' by a query rewrite plugin
1 row in set (0.00 sec)
Output from general log :
2020-06-22T11:20:36.952153Z   22 Query update qrw8012 set name = 'hercules7sakthi' where name = 'sakthi'`
要卸载该插件，您必须加载 SQL 文件 uninstall_rewriter.sql 。它将删除数据库，功能并卸载插件。
`[root@hercules7sakthi3 mysql]# cat /usr/share/mysql-8.0/uninstall_rewriter.sql
...
...
DROP DATABASE IF EXISTS query_rewrite;
DROP FUNCTION load_rewrite_rules;
UNINSTALL PLUGIN rewriter;`
**二、DDL 重写插件**
MySQL 社区团队在 MySQL 8.0.16 中引入了 ddl_rewriter 插件。该插件可用于修改服务器接收的 CREATE TABLE 语句。该插件将从 CREATE TABLE 语句中删除以下子句。
- ENCRYPTION
- DATA DIRECTORY
- INDEX DIRECTORY
2.1 环境准备
使用 安装插件命令配置插件。
`mysql> install plugin ddl_rewriter soname 'ddl_rewriter.so';
Query OK, 0 rows affected (0.04 sec)
mysql> select plugin_name,plugin_status, plugin_version from information_schema.plugins where plugin_name like '%ddl%';
+--------------+---------------+----------------+
| plugin_name  | plugin_status | plugin_version |
+--------------+---------------+----------------+
| ddl_rewriter | ACTIVE        | 1.0            |
+--------------+---------------+----------------+
1 row in set (0.01 sec)`
一旦安装了 ddl_rewriter，就可以使用 **&#8211;ddl-rewriter** 选项进行后续服务启动，以控制 ddl_rewriter 插件的激活。例如，要禁用该功能：
`[mysqld]
ddl-rewriter = OFF`
2.2 测试案例
不使用 ENCRYPTION，DATA DIRECTORY 和 INDEX DIRECTORY 将表结构从源迁移到目标。
2.3 需求描述
两个 MySQL 环境，分别称为“源”和“目标”。在源环境中，所有的表都配置了加密，并且某些表具有不同的数据合索引目录。
需要将表 ddl_rwtest ，从源迁移到目标。该表具有加密功能，并且具有不同的数据和索引目录。不需要在目的地进行加密以及将数据和索引目录分开。
从源头来看，表结构如下所示：
`create table ddl_rwtest
(id int primary key, name varchar(16),dob date,msg text)
ENCRYPTION='Y'
DATA DIRECTORY = '/mysql/data'
INDEX DIRECTORY = '/mysql/index';`
**过程**在第一步中，启用了 ddl_rewriter 插件，如实现部分所示。现在，将使用相同的 SQL 命令加载结构。
`mysql> create table ddl_rwtest
-> (id int primary key, name varchar(16),dob date,msg text)
-> ENCRYPTION='Y'
-> DATA DIRECTORY = '/mysql/data'
-> INDEX DIRECTORY = '/mysql/index';
Query OK, 0 rows affected, 1 warning (0.08 sec)
mysql> show warnings\G
*************************** 1. row ***************************
Level: Note
Code: 1105
Message: Query 'create table ddl_rwtest
(id int primary key, name varchar(16),dob date,msg text)
ENCRYPTION='Y'
DATA DIRECTORY = '/mysql/data'
INDEX DIRECTORY = '/mysql/index'' rewritten to 'create table ddl_rwtest
(id int primary key, name varchar(16),dob date,msg text) ' by a query rewrite plugin
1 row in set (0.00 sec)
mysql> show create table ddl_rwtest\G
*************************** 1. row ***************************
Table: ddl_rwtest
Create Table: CREATE TABLE `ddl_rwtest` (
`id` int NOT NULL,
`name` varchar(16) DEFAULT NULL,
`dob` date DEFAULT NULL,
`msg` text,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.01 sec)`从上面的日志中，ddl_rewriter 插件已从我的 SQL 命令中删除了那些加密和数据/索引目录。您可以验证警告消息以确认这一点。
该插件将真正帮助使用逻辑备份进行大规模数据结构迁移。
**结论**
MySQL 社区团队正在积极地进行 Query rewrite 插件的开发，因为我们有一个来自 MySQL 8.0.16 的新的 DDL rewriter 插件。目前，该插件仅支持 CREATE TABLE 语句，期待其他 DDL 语句的更多功能和支持。