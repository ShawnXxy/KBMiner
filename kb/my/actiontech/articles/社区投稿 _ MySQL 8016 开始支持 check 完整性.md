# 社区投稿 | MySQL 8.0.16 开始支持 check 完整性

**原文链接**: https://opensource.actionsky.com/20190506-mysql8-0-check/
**分类**: MySQL 新特性
**发布时间**: 2019-05-06T01:13:32-08:00

---

一直以来MySQL都只实现了实体完整性、域完整性、引用完整性、唯一键约束。
唯独 **check 完整性**迟迟没有到来，MySQL 8.0.16(2019-04-25 GA) 版本为这个画上了句号。
## 没有 check 完整性约束会怎样
**1、没有 check 完整性约束可能会影响到数据的质量。**
`   -- 创建一个 person 表来保存名字，年龄这个两个基本信息
CREATE TABLE person ( NAME VARCHAR ( 16 ), age INT );
-- 这种情况下可以插入一个年龄为 -32 的行，负的年龄明显是没有意义的
INSERT INTO person ( NAME, age ) 
VALUE
( '张三岁',- 32 );
select * from person;
+-----------+------+
| name      | age  |
+-----------+------+
| 张三岁    |  -32 |
+-----------+------+
1 row in set (0.00 sec)
`
**2、如果单单只是不能容忍负值，我们可以换一种非负整数类型来克服一下。**
`   -- 先删除之前的 person 定义
drop table if exists person;
Query OK, 0 rows affected (0.01 sec)
-- 创建一个新的 person 表
create table if not exists person(name varchar(16),age int unsigned);
Query OK, 0 rows affected (0.01 sec)
-- 声明的时候说明了 age 只能是正数，所以插入负数就会报错
insert into person(name,age) value('张三岁',-32);
ERROR 1264 (22003): Out of range value for column 'age' at row 1
`
上面的这种解决方案其实就是通过域完整性来实现的数据验证，域完整性的能力还是有边界的。
比如说,要求age一定要18岁之上它是做不到的，而这种需求正是check完整性大显身手的地方。
## 看用 check 如何解决
**1、MySQL 8.0.16+版本，check 完整性解决age要大于18的问题。**
`   select @@version;                                                                          
+-----------+
| @@version |
+-----------+
| 8.0.16    |
+-----------+
1 row in set (0.00 sec)
-- 先删除之前定义的表
drop table if exists person;
Query OK, 0 rows affected (0.01 sec)
-- 创建新的表，并对 age 列进行验证，要求它一定要大于 18 
create table if not exists person(
name varchar(16),
age int,
constraint ck_person_001 check (age > 18) -- 加一个 check 约束条件
);
Query OK, 0 rows affected (0.02 sec)
-- 查看表的定义
show create table person;                                                                  
+--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table  | Create Table                                                                                                                                                                                                  |
+--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| person | CREATE TABLE `person` (
`name` varchar(16) DEFAULT NULL,
`age` int(11) DEFAULT NULL,
CONSTRAINT `ck_person_001` CHECK ((`age` > 18))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
-- 插入的数据如果不能通过 check 约束就会报错
insert into person(name,age) value('张三岁',-32);
ERROR 3819 (HY000): Check constraint 'ck_person_001' is violated.
insert into person(name,age) values('张三岁',17);
ERROR 3819 (HY000): Check constraint 'ck_person_001' is violated.
insert into person(name,age) values('张三岁',19);
Query OK, 1 row affected (0.01 sec)
`
**2、MySQ 8.0.16 以下版本的 MySQL 会怎样？**
`   select @@version;  
+-----------+
| @@version |
+-----------+
| 8.0.15    |
+-----------+
1 row in set (0.00 sec)
drop table if exists person;
Query OK, 0 rows affected (0.00 sec)
create table if not exists person(
name varchar(16),
age int,
constraint ck_person_001 check (age > 18) -- 加一个 check 约束条件
);
Query OK, 0 rows affected (0.01 sec)
-- 可以看到在低版本下 check 约束被直接无视了，也就是说低版本是没有 check 约束的
show create table person;
+--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table  | Create Table                                                                                                                                                                          |
+--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| person | CREATE TABLE `person` (
`name` varchar(16) COLLATE utf8mb4_general_ci DEFAULT NULL,
`age` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci |
+--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
-- 
insert into person(name,age) value('张三岁',-32);
Query OK, 1 row affected (0.00 sec)
`
**可以看到在 MySQL 8.0.16 以下的版本中，check直接被忽略。**
> 
新版本在CHECK Constraints功能上的完善提高了对非法或不合理数据写入的控制能力。
除了以上示例中的列约束之外，CHECK Constraints还支持表约束。
想要了解更多关于CHECK Constraints 的详细语法规则和注意事项，请参考MySQL官网文档
[https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)
**开源分布式中间件DBLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dble
技术交流群：669663113
**开源数据传输中间件DTLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dtle
技术交流群：852990221
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/默认标题_宣传单_2019.05.06-1-223x300.jpg)