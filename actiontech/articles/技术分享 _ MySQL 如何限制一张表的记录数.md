# 技术分享 | MySQL 如何限制一张表的记录数

**原文链接**: https://opensource.actionsky.com/20210906-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-09-06T00:04:43-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 背景
本文又是来源于客户咨询的问题： 能否控制单表在一个固定的记录数，比如说1W条，超过不让插入新记录或者说直接抛出错误？
关于这个问题，没有一个简化的答案，比如执行一条命令或者说简单设置一个参数都不能完美解决。接下来我给出一些可选解决方案。
## 正文
对数据库来讲，一般问题的解决方案无非有两种，一种是在应用端；另外一种是在数据库端。
#### 首先是在数据库端（假设表硬性限制为1W条记录）：
##### 一、触发器解决方案：
##### 触发器的思路很简单，每次插入新记录前，检查表记录数是否到达限定数量，数量未到，继续插入；数量达到，先插入一条新记录，再删除最老的记录，或者反着来也行。为了避免每次检测表总记录数全表扫，规划另外一张表，用来做当前表的计数器，插入前，只需查计数器表即可。要实现这个需求，需要两个触发器和一张计数器表。
t1为需要限制记录数的表，t1_count 为计数器表：
`mysql:ytt_new>create table t1(id int auto_increment primary key, r1 int);
Query OK, 0 rows affected (0.06 sec)
mysql:ytt_new>create table t1_count(cnt smallint unsigned);
Query OK, 0 rows affected (0.04 sec)
mysql:ytt_new>insert t1_count set cnt=0;
Query OK, 1 row affected (0.11 sec)
`
得写两个触发器，一个是插入动作触发：
`DELIMITER $$
USE `ytt_new`$$
DROP TRIGGER /*!50032 IF EXISTS */ `tr_t1_insert`$$
CREATE
/*!50017 DEFINER = 'ytt'@'%' */
TRIGGER `tr_t1_insert` AFTER INSERT ON `t1` 
FOR EACH ROW BEGIN
UPDATE t1_count SET cnt= cnt+1;
END;
$$
DELIMITER ;
`
另外一个是删除动作触发：
`DELIMITER $$
USE `ytt_new`$$
DROP TRIGGER /*!50032 IF EXISTS */ `tr_t1_delete`$$
CREATE
/*!50017 DEFINER = 'ytt'@'%' */
TRIGGER `tr_t1_delete` AFTER DELETE ON `t1` 
FOR EACH ROW BEGIN
UPDATE t1_count SET cnt= cnt-1;
END;
$$
DELIMITER ;
`
给表t1造1W条数据，达到上限：
`mysql:ytt_new>insert t1 (r1) with recursive tmp(a,b) as (select 1,1 union all select a+1,ceil(rand()*20) from tmp where a<10000 ) select b from tmp;
Query OK, 10000 rows affected (0.68 sec)
Records: 10000  Duplicates: 0  Warnings: 0
`
计数器表 t1_count 记录为1W。
`mysql:ytt_new>select cnt from t1_count;
+-------+
| cnt   |
+-------+
| 10000 |
+-------+
1 row in set (0.00 sec)
`
插入前需要判断计数器表是否到达限制，如果到了这个限制则删除老旧记录先。我写一个存储过程简单理下逻辑：
`DELIMITER $$
USE `ytt_new`$$
DROP PROCEDURE IF EXISTS `sp_insert_t1`$$
CREATE DEFINER=`ytt`@`%` PROCEDURE `sp_insert_t1`(
IN f_r1 INT
)
BEGIN
DECLARE v_cnt INT DEFAULT 0;
SELECT cnt INTO v_cnt FROM t1_count;
IF v_cnt >=10000 THEN
DELETE FROM t1 ORDER BY id ASC LIMIT 1;
END IF;
INSERT INTO t1(r1) VALUES (f_r1);          
END$$
DELIMITER ;
`
此时，调用存储过程即可实现：
`mysql:ytt_new>call sp_insert_t1(9999);
Query OK, 1 row affected (0.02 sec)
mysql:ytt_new>select count(*) from t1;
+----------+
| count(*) |
+----------+
|    10000 |
+----------+
1 row in set (0.01 sec)
`
这个存储过程的处理逻辑也可以继续优化为一次批量处理。 比如每次多缓存一倍的表记录数，判断逻辑变为在2W条以前，只插入新记录，并不删除老记录，当到达2W条后，一次性删除旧的1W条记录。
这种方案有以下几个缺陷：
- 
计数器表的记录更新是由insert/delete触发，如果对表进行truncate则计数器表不触发更新从而数据不一致。
- 
对表进行drop 操作则触发器也跟着删除，需要重建触发器，重置计数器表。
- 
对表写入只能是类似存储过程这样的单一入口，不能是其他入口。
##### 二、分区表解决方案
##### 建立一个 range 分区，第一个分区有1W条记录，第二个分区为默认分区，等表记录数达到限制后，删除第一个分区，重新调整分区定义即可。
分区表初始定义：
`mysql:ytt_new>create table t1(id int auto_increment primary key, r1 int) partition by range(id) (partition p1 values less than(10001), partition p_max values less than(maxvalue));
Query OK, 0 rows affected (0.45 sec)
`
查找第一个分区是否已满：
`mysql:ytt_new>select count(*) from t1 partition(p1);
+----------+
| count(*) |
+----------+
|    10000 |
+----------+
1 row in set (0.00 sec)
`
删除第一个分区，并且重新调整分区表：
`mysql:ytt_new>alter table t1 drop partition p1;
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql:ytt_new>alter table t1 reorganize partition p_max into (partition p1 values less than (20001), partition p_max values less than (maxvalue));
Query OK, 0 rows affected (0.60 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
这种方法的优势很明显：
- 
表插入入口可以很随机，INSERT语句、存储过程、导文件都行。
- 
删除第一个分区是一个DROP操作，非常快。
但也有缺点：表记录不能有空隙，如果有空隙，就得改变分区表定义。比如把分区p1的最大值改为20001，那即使在这个分区里有一半的记录不连续，也不影响检索分区里的总记录数。
##### 三、通用表空间解决方案
##### 提前计算好这张表1W条记录需要多少磁盘空间，之后在磁盘上划分一个区专门来存放这张表的数据。
挂载划好的分区，添加为 InnoDB 表空间的备选目录(/tmp/mysql/)。
`mysql:ytt_new>create tablespace ts1 add datafile '/tmp/mysql/ts1.ibd' engine innodb;
Query OK, 0 rows affected (0.11 sec)
mysql:ytt_new>alter table t1 tablespace ts1;
Query OK, 0 rows affected (0.12 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
我大致算了下，不是很准确，所以记录上可能有点误差，不过意思已经很明确：等表报 “TABLE IS FULL” 后即可。
`mysql:ytt_new>insert t1 (r1) values (200);
ERROR 1114 (HY000): The table 't1' is full
mysql:ytt_new>select count(*) from t1;
+----------+
| count(*) |
+----------+
|    10384 |
+----------+
1 row in set (0.20 sec)
`
表满后移除表空间，清空表，再插入新记录。
`mysql:ytt_new>alter table t1 tablespace innodb_file_per_table;
Query OK, 0 rows affected (0.18 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql:ytt_new>drop tablespace ts1;
Query OK, 0 rows affected (0.13 sec)
mysql:ytt_new>truncate table t1;
Query OK, 0 rows affected (0.04 sec)
`
#### 另外一个就是在应用端处理：
##### 可以提前在应用端缓存表数据，达到限定的记录数后再批量写入数据库端，写入数据库前，先清空表即可。
举个例子: 表t1数据缓存到文件t1.csv，当t1.csv到达1W行时，数据库端清空表数据，导入t1.csv。
# 结语
之前 MySQL 在 MyISAM 时代，表属性 max_rows 来预估表的记录数，但也不是硬性规定，类似我上面写的使用通用表空间来达到限制表记录数的作用；到了 InnoDB 时代就没有一个直观的方法，更多是靠以上列出来的方法来解决这个问题，具体选哪个方案，还是得看需求。