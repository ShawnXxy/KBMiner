# 新特性解读 | MySQL 8.0 索引特性4-不可见索引

**原文链接**: https://opensource.actionsky.com/20190528-mysql8-index4/
**分类**: MySQL 新特性
**发布时间**: 2019-05-28T17:54:19-08:00

---

## MySQL 8.0 新特性
MySQL 8.0 实现了索引的隐藏属性。当然这个特性很多商业数据库早就有了，比如ORACLE，在11g中就实现了。我来介绍下这个小特性。
#### 介绍
INVISIBLE INDEX，不可见索引或者叫隐藏索引。就是对优化器不可见，查询的时候优化器不会把她作为备选。其实以前要想彻底不可见，只能用开销较大的drop index；现在有了新的方式，可以改变索引的属性，让其不可见，这一操作只更改metadata，开销非常小。
#### 使用场景
我大概描述下有可能使用隐藏索引的场景：
1.比如我有张表t1，本来已经有索引idx_f1，idx_f2，idx_f3。我通过数据字典检索到idx_f3基本没有使用过，那我是不是可以判断这个索引直接删掉就好了？那如果删掉后突然有新上的业务要大量使用呢？难道我要频繁的drop index/add index吗？这个时候选择开销比较小的隐藏索引就好了。
2.我的业务只有一个可能每个月固定执行一次的SQL用到这个索引，那选择隐藏索引太合适不过了。
3.又或者是我想要测试下新建索引对我整个业务的影响程度。如果我直接建新索引，那我既有业务涉及到这个字段的有可能会收到很大影响。那这个时候隐藏索引也是非常合适的。
#### 举例
下面我来简单举例如何使用隐藏索引
表结构
```
mysql> create table f1 (id serial primary key, f1 int,f2 int );
Query OK, 0 rows affected (0.11 sec)
```
创建两个索引，默认可见。
索引1，
```
mysql> alter table f1 add key idx_f1(f1), add key idx_f2(f2);
Query OK, 0 rows affected (0.12 sec)
Records: 0  Duplicates: 0  Warnings: 0
```
索引2，
```
mysql> show create table f1\G
*************************** 1. row ***************************
Table: f1
Create Table: CREATE TABLE `f1` (
`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
`f1` int(11) DEFAULT NULL,
`f2` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `id` (`id`),
KEY `idx_f1` (`f1`),
KEY `idx_f2` (`f2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```
简单写个造数据的存储过程。
```
DELIMITER $$
USE `ytt`$$
CREATE PROCEDURE `sp_generate_data_f1`(
IN f_cnt INT
)
BEGIN
DECLARE i,j INT DEFAULT 0;
SET @@autocommit=0;
WHILE i < f_cnt DO
SET i = i + 1;
IF j = 100 THEN
SET j = 0;
COMMIT;
END IF;
SET j = j + 1;
INSERT INTO f1 (f1,f2) SELECT CEIL(RAND()*100),CEIL(RAND()*100);
END WHILE;
COMMIT;
SET @@autocommit=1;
END$$
DELIMITER ;
```
生成1W条记录。
```
mysql> call sp_generate_data_f1(10000);
Query OK, 0 rows affected (5.42 sec)
```
我们把f2列上的索引变为不可见，结果瞬间完成。
```
mysql> alter table f1 alter index idx_f2 invisible;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
```
在看下表结构，此时索引标记为Invisible。
```
mysql> show create table f1 \G
*************************** 1. row ***************************
Table: f1
Create Table: CREATE TABLE `f1` (
`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
`f1` int(11) DEFAULT NULL,
`f2` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `id` (`id`),
KEY `idx_f1` (`f1`),
KEY `idx_f2` (`f2`) /*!80000 INVISIBLE */
) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```
给一条有f2列过滤的SQL， 发现优化器用不到这个索引了。
```
mysql> explain select count(*) from f1 where f2 = 52\G
*************************** 1. row ***************************
id: 1
select_type: SIMPLE
table: f1
partitions: NULL
type: ALL
possible_keys: NULL
key: NULL
key_len: NULL
ref: NULL
rows: 9991
filtered: 1.00
Extra: Using where
1 row in set, 1 warning (0.00 sec)
```
用force index 强制使用，直接报错。
```
mysql> explain select count(*) from f1 force index (idx_f2) where f2 = 52\G
ERROR 1176 (42000): Key 'idx_f2' doesn't exist in table 'f1'
```
那 MySQL 8.0 的优化器开关里可以告诉它，有的时候可以用隐藏索引。来打开看看。
```
mysql> set @@optimizer_switch = 'use_invisible_indexes=on';
Query OK, 0 rows affected (0.00 sec)
```
那这条SQL 现在可以用idx_f2了。
```
mysql> explain select count(*) from f1 where f2 = 52\G
*************************** 1. row ***************************
id: 1
select_type: SIMPLE
table: f1
partitions: NULL
type: ref
possible_keys: idx_f2
key: idx_f2
key_len: 5
ref: const
rows: 121
filtered: 100.00
Extra: Using index
1 row in set, 1 warning (0.00 sec)
```
#### 总结
总结下，INVISIBLE INDEX 的确是一个很有用的小特性，给索引增加了第三个额外的开关选项。想要了解更多的建议阅读MySQL手册。
##### 社区近期动态
[![](.img/dfabe8a3.jpg)](https://i.loli.net/2019/05/28/5cecd1ad59d4c73631.jpg)
**报名详情 ↓**
**[6月15日 上海站 | 分布式中间件DBLE用户见面会](http://https://event.31huiyi.com/1633790994)**
本次举办的DBLE用户见面会，是自2017年10月24日数据库中间件DBLE发布以来，**首次线下互动式分享会议**。
来爱可生总部研发中心，与研发、测试、产品、社区团队面对面，遇到志同道合的朋友，更有丰富精美的周边产品等着你！
**会议时间：2019年06月15日13:00—17:00
会议地点：爱可生研发中心，上海市徐汇区虹梅路1905号远中科研楼甲幢7层**