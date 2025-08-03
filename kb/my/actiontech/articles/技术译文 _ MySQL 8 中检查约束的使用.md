# 技术译文 | MySQL 8 中检查约束的使用

**原文链接**: https://opensource.actionsky.com/20201117-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-11-17T00:33:39-08:00

---

作者：Walter Garcia
翻译：管长龙
本文来源：https://www.percona.com/blog/2020/10/02/how-to-use-check-constraint-in-mysql-8/
大家好，在这篇小文章中，我们将介绍 MySQL 8 的一项新功能。
**什么是“检查约束”？**
这是一项新功能，用于指定在插入或更新到一行之前检查值的条件。如果表的任何行的搜索条件的结果为 FALSE，则约束可能返回错误（但如果结果为 UNKNOWN 或 TRUE，则约束不会返回错误）。
此功能开始在 MySQL 8.0.16 上运行，在以前的版本中，我们可以创建它，但它不起作用，这意味着支持语法，但不起作用。
**要牢记的使用规则：**- AUTO_INCREMENT 自增列不允许使用
- 引用另一个表中的另一列不允许使用
- 存储的函数和用户定义的函数不允许使用
- 存储过程和函数参数不允许使用
- 子查询不允许使用
- 在外键中用于后续操作（ON UPDATE，ON DELETE）的列不允许使用
- 为下一条语句 INSERT，UPDATE，REPLACE，LOAD DATA 和 LOAD XML 评估此次监测。此外，还会为 INSERT IGNORE，UPDATE IGNORE，LOAD DATA…IGNORE 和 LOAD XML…IGNORE 评估此监测约束。对于这些语句，如果约束的评估结果为 FALSE，则会发生警告。插入或更新被跳过。
**看一些例子**
我创建了下表来测试此功能。如示例所示，这非常简单：- 
- 
- 
- 
- 
- 
- 
- 
`CREATE TABLE users (``id int not null auto_increment,``firstname varchar(50) not null,``lastname varchar(50) not null,``age TINYINT unsigned not null CONSTRAINT `check_1` CHECK (age > 15),``gender ENUM('M', 'F') not null,``primary key (id)``) engine = innodb;`
在这个简单的测试中，仅当 **age > 15 **时，我们才能写入或更新行。
让我们看一个示例，尝试插入 **age < 15** 的行：- 
- 
`mysql> INSERT INTO users SET firstname = 'Name1', lastname = 'LastName1', age = 10, gender = 'M';``ERROR 3819 (HY000): Check constraint 'check_1' is violated.`
要删除，请使用下一个示例：- 
```
ALTER TABLE users DROP CHECK check_1;
```
让我们看另一个示例，向其中添加更多逻辑。我用下一个检查表更改了表：- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
ALTER TABLE users`ADD CONSTRAINT gender_male``CHECK (``    CASE``        WHEN gender = 'M'``        THEN``            CASE``                WHEN age >= 21``                THEN 1``                ELSE 0``            END``        ELSE 1``    END = 1``);``
``ALTER TABLE users``ADD CONSTRAINT gender_female``CHECK (``    CASE``        WHEN gender = 'F'``            THEN``                CASE``                    WHEN age >= 18``                    THEN 1``                    ELSE 0``                END``        ELSE 1``    END = 1``);
```
我们添加了更多逻辑，现在它取决于 **sex **和** age** 列。当且仅当表行的指定条件评估为 TRUE 或 UNKNOWN（对于 NULL 列值）时，才满足 CHECK 监测约束，否则违反约束。
让我们从前面的逻辑中看一个例子。- 
- 
- 
- 
- 
mysql> INSERT INTO users SET firstname = 'Name2', lastname = 'LastName2', age = 10, gender = 'F';``ERROR 3819 (HY000): Check constraint 'gender_female' is violated.``
``mysql> INSERT INTO users SET firstname = 'Name3', lastname = 'LastName3', age = 10, gender = 'M';``ERROR 3819 (HY000): Check constraint 'gender_male' is violated.`
如您在 ERROR 消息中所见，MySQL 正在显示 CHECK 约束名称。可以从应用程序源代码中使用它来调试错误并知道从哪个 CHECK 失败。
最后，这是表结构：- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`CREATE TABLE `users` (```id` int(11) NOT NULL AUTO_INCREMENT,```firstname` varchar(50) NOT NULL,```lastname` varchar(50) NOT NULL,```age` tinyint(3) unsigned NOT NULL,```gender` enum('M','F') NOT NULL,``PRIMARY KEY (`id`),``CONSTRAINT `gender_female` CHECK (((case when (`gender` = 'F') then (case when (`age` > 18) then 1 else 0 end) else 1 end) = 1)),``CONSTRAINT `gender_male` CHECK (((case when (`gender` = 'M') then (case when (`age` > 21) then 1 else 0 end) else 1 end) = 1))``) ENGINE=InnoDB AUTO_INCREMENT=4;`
我们可以使用此功能在表中添加更多的逻辑，但是根据我以前作为程序员的经验，我不建议在表中添加逻辑，因为除非您无法访问应用程序代码，否则很难找到或调试错误。
相关推荐：
[技术译文 | MySQL 8 需要多大的 innodb_buffer_pool_instances 值（上）](https://opensource.actionsky.com/20200817-mysql/)
[技术译文 | MySQL 8 需要多大的 innodb_buffer_pool_instances 值（下）](https://opensource.actionsky.com/20200818-mysql/)
[技术译文 | MySQL 8.x DDL 和查询重写插件](https://opensource.actionsky.com/20200812-mysql/)