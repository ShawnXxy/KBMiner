# 技术译文 | 那些 MySQL 8.0 中的隐藏特性

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e8%af%91%e6%96%87-%e9%82%a3%e4%ba%9b-mysql-8-0-%e4%b8%ad%e7%9a%84%e9%9a%90%e8%97%8f%e7%89%b9%e6%80%a7/
**分类**: MySQL 新特性
**发布时间**: 2023-08-06T23:23:40-08:00

---

在本文中，我想讨论 MySQL 8.0 中的几个相当新的特性，以及一个较老的特性。这些可能是您不知道的次要功能，但值得快速了解一下它们的工作方式以及在某些情况下可能的用途。
> 作者：Corrado Pandiani
本文来源：Percona 官网博客
- 爱可生开源社区出品。
与隐藏有关的特性：
- [隐藏列](https://dev.mysql.com/doc/refman/8.0/en/invisible-columns.html)
- [生成的隐藏主键](https://dev.mysql.com/doc/refman/8.0/en/create-table-gipks.html)
- [隐藏索引](https://dev.mysql.com/doc/refman/8.0/en/invisible-indexes.html)
下面让我们来看看。
# 隐藏列
8.0.23 新增隐藏列特性。什么是隐藏列？它基本上是一个表的常规列，具有自己的名称和数据类型。它像任何其他常规列一样处理和更新，唯一的区别是对应用程序不可见。换句话说，只有在 SELECT 语句中明确搜索它时，才能访问它；否则，它就像一个不存在的列。
这个定义看起来很奇怪，但如果提供一个这个特性的真实使用案例，一切都应该更清晰。
假设您的应用程序代码中有 **SELECT *** 查询。作为经验丰富的数据库开发人员，您应该知道这种查询不应存在于任何生产代码中。典型的问题是，当您需要更改表架构，添加或删除列，或者更糟的是在其他列中间添加新列时。抓取到你应用程序变量中的字段位置可能会完全打破应用程序或触发意外的错误行为。这就是您需要避免在应用程序中使用 **SELECT *** 的原因。
在这种情况下，如果您需要避免更改应用程序代码以匹配新表架构，可以将新列添加为隐藏列，它不会返回给客户端，因为您的查询没有明确搜索它。所以，您的应用程序不会失败或出现奇怪的行为。而这，就是隐藏列的用武之地。
您需要在列定义中使用 **INVISIBLE** 关键字。当您需要将列设置为可见时，需要使用 **VISIBLE** 关键字。让我们看一个例子。
我们创建一个表并插入一些行：
`mysql> CREATE TABLE articles (
id INT UNSIGNED AUTO_INCREMENT,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
article TEXT,
PRIMARY KEY(id)
);
Query OK, 0 rows affected (0.03 sec)
mysql> INSERT INTO articles(article) VALUES
("This is first article"),
("This is second article"),
("This is third article");
Query OK, 3 rows affected (0.01 sec)  
Records: 3  Duplicates: 0  Warnings: 0
mysql> SELECT * FROM articles;
+----+---------------------------+------------------------------+
| id | ts                  | article                |
+----+---------------------------+------------------------------+
|  1 | 2023-07-28 13:15:03 | This is first article  |
|  2 | 2023-07-28 13:15:03 | This is second article |
|  3 | 2023-07-28 13:15:03 | This is third article  |
+----+---------------------------+------------------------------+
`
有时，我们决定必须在 `ts` 列之后向表中添加一个新的字段 `title`。为了避免我们的应用程序因 **SELECT *** 和新添加的中间列等情况失效，我们必须将 `title` 列创建为 **INVISIBLE**。
`mysql> ALTER TABLE articles ADD COLUMN title VARCHAR(200) INVISIBLE AFTER ts;
Query OK, 0 rows affected (0.06 sec)  
Records: 0  Duplicates: 0  Warnings: 0
`
为新列提供一些值：
`mysql> UPDATE articles SET title='Title 1' WHERE id=1;
UPDATE articles SET title='Title 2' WHERE id=2; 
UPDATE articles SET title='Title 3' WHERE id=3;
`
现在看看表架构：
`CREATE TABLE `articles` (
`id` int unsigned NOT NULL AUTO_INCREMENT,
`ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
`title` varchar(200) DEFAULT NULL /*!80023 INVISIBLE */,
`article` text,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
`
你可以看到，该列被正确地标记了 **INVISIBLE** 关键字。
再试一次 **SELECT *** ：
`mysql> SELECT * FROM articles;
+----+---------------------------+------------------------------+
| id | ts                  | article                |
+----+---------------------------+------------------------------+
|  1 | 2023-07-28 13:15:03 | This is first article  |
|  2 | 2023-07-28 13:15:03 | This is second article |
|  3 | 2023-07-28 13:15:03 | This is third article  |
+----+---------------------------+------------------------------+
`
你看，该列没有返回。这允许 `schema` 改变后查询不会失败。
如果你想看 `title`，你必须明确寻址该字段：
`mysql> SELECT id, ts, title, article FROM articles;
+----+---------------------------+-----------+------------------------------+
| id | ts                  | title   | article                |
+----+---------------------------+-----------+------------------------------+
|  1 | 2023-07-28 13:15:03 | Title 1 | This is first article  |
|  2 | 2023-07-28 13:15:03 | Title 2 | This is second article |
|  3 | 2023-07-28 13:15:03 | Title 3 | This is third article  |
+----+---------------------------+-----------+------------------------------+
`
使用以下 DDL 将列设置为可见：
`mysql> ALTER TABLE articles MODIFY COLUMN title varchar(200) VISIBLE;
`
记住，隐藏列像任何其他常规列一样处理，所以您可以随时读取和更新它们。关于隐形性的元数据在 `information_schema` 中可用，**INVISIBLE/VISIBLE** 关键字在 binlog 中保留，以便正确复制所有更改。
# 生成的隐藏主键
这个特性在 MySQL 8.0.30 开始提供。生成的隐藏主键（GIPK）是一种特殊的隐藏列，仅适用于 InnoDB 表。
没有主键的情况下创建 InnoDB 表，往往不是一个好的选择。我们强烈建议您的表中始终创建显式主键。您可能还知道，如果您不提供主键，InnoDB 会创建一个隐藏的主键，但是 GIPK 提供的新特性使主键可以变得可用和最后可见。相反，隐含创建的早期隐藏主键既不能成为可用的也不能成为可见的。
该功能对于强制缺乏经验的用户的 InnoDB 表都具有显式主键很有用，即使是隐藏的。
让我们看看它是如何工作的。
默认情况下，此功能被禁用，因此 MySQL 将继续像过去一样运行。要启用 GIPK，您必须设置以下动态系统变量（它具有全局和会话作用域）：
`mysql> SET [PERSIST] sql_generate_invisible_primary_key=ON;
`
现在在不指定显式主键的情况下创建一个表：
`mysql> CREATE TABLE customer(name VARCHAR(50));
Query OK, 0 rows affected (0.03 sec)
`
检查模式：
`mysql> SHOW CREATE TABLE customerG
*************************** 1. row ***************************
Table: customer  
Create Table: CREATE TABLE `customer` (
`my_row_id` bigint unsigned NOT NULL AUTO_INCREMENT /*!80023 INVISIBLE */,
`name` varchar(50) DEFAULT NULL,
PRIMARY KEY (`my_row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
`
名为 **my_row_id** 的隐藏主键已经自动创建。
> 注意：
- GIPK 的名称始终为 `my_row_id`。您不能在表中有相同名称的列。
- GIPK 的数据类型始终为使用 AUTO_INCREMENT 的 BIGINT UNSIGNED。
有趣的是，您可以在查询中使用主键并在明确寻址时看到它，就像描述的隐藏列一样。
`mysql> INSERT INTO customer VALUES('Tim'),('Rob'),('Bob');
Query OK, 3 rows affected (0.00 sec)
Records: 3 Duplicates: 0 Warnings: 0
mysql> SELECT my_row_id, name FROM customer;
+--------------+-------+
| my_row_id | name |
+--------------+-------+
|         1 |  Tim |
|         2 |  Rob |
|         3 |  Bob |
+--------------+-------+
3 rows in set (0.00 sec)
mysql> SELECT my_row_id, name FROM customer WHERE my_row_id=2;
+--------------+-------+
| my_row_id | name |
+--------------+-------+
|         2 |  Rob |
+--------------+-------+
1 row in set (0.00 sec)
`
很显然。如果您执行 `SELECT *`，主键不会被返回：
`mysql> SELECT * FROM customer WHERE my_row_id=2;
+-------+
| name |
+-------+
| Rob  |
+-------+
`
在某些时候,您最终可以决定使其可见,并在需要时更改名称:
`mysql> ALTER TABLE customer MODIFY `my_row_id` bigint unsigned not null auto_increment VISIBLE;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> SHOW CREATE TABLE customerG  
*************************** 1. row ***************************
Table: customer
Create Table: CREATE TABLE `customer` (
`my_row_id` bigint unsigned NOT NULL AUTO_INCREMENT,
`name` varchar(50) DEFAULT NULL,
PRIMARY KEY (`my_row_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
`
# 隐藏索引
为了完成隐形事物的概述，我们也来讨论一下隐藏索引。这是最古老的隐形特性，在 MySQL 8.0 的第一个版本中就引入了。
您可以使索引对优化器不可见，以便测试如果该索引不存在，查询的性能会如何。不过，当索引不可见时，在针对表执行任何 DML 语句（INSERT、UPDATE、DELETE、REPLACE）时，它仍会得到更新。
您可以使用以下语句将索引设置为不可见和再次可见：
`ALTER TABLE mytable ALTER INDEX my_idx INVISIBLE;
ALTER TABLE mytable ALTER INDEX my_idx VISIBLE;
`
隐藏索引可以测试在不考虑它的情况下查询的执行计划。最大的优点是您不需要删除索引。请记住,索引删除几乎是瞬间完成的,但重建索引则不然。根据表的大小,重建索引可能需要大量时间并过载服务器。另一种选择是,您也可以使用 `IGNORE INDEX()` 索引提示,但在这种情况下,您可能会被迫在应用程序代码中的许多查询上添加索引提示。将索引设置为不可见将允许您在很短的时间内开始测试查询。并且您可以随时轻松地将其设置回可见,而不会丢失任何更新。
> 注意：
- 主键（PRIMARY Key）不能隐藏
- UNIQUE 索引可以隐藏，但仍会执行唯一性检查
- 有关索引不可见性的信息在 `information_schema` 中可用
- 索引不可见性会被正确复制
# 总结
从我的角度来看，你不应该使用隐藏列，因为最佳实践是不应在任何应用中部署**SELECT *** 查询。不过，在某些紧急情况下，此功能可能非常有用，可以飞快地解决问题。但是之后要记住修复你的代码并将隐藏列设置为可见会更好。
对 GIPK 来说，情况也差不多。只要记住为表提供显式主键，就不需要此功能。不过，它可以帮助一个创建时没有主键的表拥有一个适当的主键，这个主键可以方便地被使用和变得可见。
关于隐藏索引，这是一个非常简单的功能，在测试时非常有用，特别是在可能使用多个索引，和不确定优化器是否选择了最佳执行计划的情况中。