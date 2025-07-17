# 故障分析 | replace into 导致主备不一致

**原文链接**: https://opensource.actionsky.com/20221208-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-12-06T17:48:52-08:00

---

作者：杨奇龙
网名“北在南方”，资深 DBA，主要负责数据库架构设计和运维平台开发工作，擅长数据库性能调优、故障诊断。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一 介绍
本章内容通过一个例子说明 replace into 带来的潜在的数据质量风险,当涉及 replace into 操作的表含有自增主键时，主备切换后会造成数据覆盖等不一致的情况发生。
#### 二 案例分析
在主库上操作
root@test 12:36:51>show create table t1 \G
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(20) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
root@test 12:37:41>insert into t1(name) values('a')
此时检查主备库上 t1 的表结构都是一样的，AUTO_INCREMENT 都是2.
root@test 12:37:51>show create table t1 \G
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(20) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
在主库上进行 replace into 操作
root@test 12:37:58>replace into t1(name) values('a');
root@test 12:38:40>replace into t1(name) values('a');
root@test 12:38:49>select * from t1;
+----+------+
| id | name |
+----+------+
| 3 | a |
+----+------+
1 row in set (0.00 sec)
此时检查主备库中 t1 表结构，请注意 AUTO_INCREMENT=4
root@test 12:38:51>show create table t1 \\G
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(20) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
从库上 t1 的表结构 ，**AUTO_INCREMENT=2**
oot@test 12:39:35>show create table t1 \G
*************************** 1. row ***************************
Table: t1
Create Table: CREATE TABLE `t1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(20) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
root@test 12:39:43>select * from t1;
+----+------+
| id | name |
+----+------+
| 3 | a |
+----+------+
1 row in set (0.00 sec)
#### 分析
表 t1 的表结构 AUTO_INCREMENT=2 而主库上的t1表结构的 AUTO_INCREMENT=4.原本 replace 操作是在自增主键的情况下，遇到唯一键冲突时执行的是 delete+insert ，但是在记录 binlog 时，却记录成了 update 操作，update操作不会涉及到 auto_increment 的修改。备库应用了 binlog 之后，备库的表的 auto_increment 属性不变。
#### 三 风险点:
如果主备库发生主从切换，备库变为原来的主库，按照原来的业务逻辑再往下会发生什么?
root@test 12:40:46>replace into t1(name) values('a');  
Query OK, 2 rows affected (0.00 sec)
root@test 12:40:48>select * from t1;
+----+------+
| id | name |
+----+------+
|  2 | a    |  ---id由原来的3变成了2.
+----+------+
1 row in set (0.00 sec)
如果 t1 表本来就存在多条记录 ，主从切换之后，应用写新的主库则会发生主键冲突，这个留给各位读者自己测试一下。^_^
#### 四 总结
由于 replace into 操作在遇到主键冲突的时候会修改主键的值，所以如果业务逻辑强依赖自增 ID ，绝对不要用 replace ，普通环境也不建议这样用，因为 replace into 操作可能会导致主键的重新组织。