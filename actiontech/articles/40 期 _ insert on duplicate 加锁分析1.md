# 40 期 | insert on duplicate 加锁分析（1）

**原文链接**: https://opensource.actionsky.com/40-%e6%9c%9f-c/
**分类**: 技术干货
**发布时间**: 2024-12-09T22:43:32-08:00

---

插入记录导致主键冲突，on duplicate key update 更新唯一索引字段值的加锁情况分析。
> 
作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 准备工作
创建测试表：
`CREATE TABLE `t4` (
`id` int unsigned NOT NULL AUTO_INCREMENT,
`i1` int DEFAULT '0',
`i2` int DEFAULT '0',
PRIMARY KEY (`id`) USING BTREE,
UNIQUE KEY `uniq_i1` (`i1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
`
插入测试数据：
`INSERT INTO `t4` (`id`, `i1`, `i2`) VALUES
(1, 11, 21), (2, 12, 22), (3, 13, 23),
(4, 14, 24), (5, 15, 25), (6, 16, 26);
`
## 2. 可重复读
把事务隔离级别设置为 REPEATABLE-READ（如已设置，忽略此步骤）：
`SET transaction_isolation = 'REPEATABLE-READ';
-- 确认设置成功
SHOW VARIABLES like 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
`
执行以下 insert 语句（**主键索引冲突，更新其它字段值**）：
`begin;
insert into t4 (id, i1, i2) values (2, 120, 220)
on duplicate key update i1 = values(i1), i2 = values(i2);
`
查看加锁情况：
`select
engine_transaction_id, object_name, index_name,
lock_type, lock_mode, lock_status, lock_data
from performance_schema.data_locks
where object_name = 't4'
and lock_type = 'RECORD'\G
***************************[ 1. row ]***************************
engine_transaction_id | 250919
object_name           | t4
index_name            | PRIMARY
lock_type             | RECORD
lock_mode             | X,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 2
`
lock_data = 2、lock_mode = X,REC_NOT_GAP 表示对主键索引中  的记录加了排他普通记录锁。
insert 语句想要插入一条  的记录，首先要找到插入记录的目标位置。
对于主键索引，经过一番不太费力的寻找，找到的目标位置是主键索引中已经存在的  的记录后面。
insert 语句发现这条记录和即将插入的新记录的主键字段（id）值都是 2，要是继续插入新记录就会违反主键索引的唯一约束。
这可怎么办，就这样轻易放弃吗？
轻易放弃是不可能的，insert 语句还会进一步确认新记录是否真的和主键索引中  的记录冲突。
因为对于主键索引，如果这条记录已经被标记删除了，就不会和新记录冲突，新记录可以继续插入。
insert 语句的确认操作会读取这条记录的删除标志，读取删除标志之前，需要对这条记录加锁。
按理来说，读操作对记录加锁，本来应该加共享锁，insert 语句却加了排他锁。
这是因为 insert 语句带了个小尾巴（on duplicate key update），这个小尾巴的作用是发现冲突记录时执行更新操作，更新操作需要加排他锁，所以读取删除标志之前，就直接加了排他锁。
根据主键字段值读取主键索引中的一条记录，只需要加普通记录锁就可以了。
基于以上逻辑，insert 语句对主键索引中  的记录加了排他普通记录锁。
以上只是 insert 语句对主键索引中  的记录第 1 次加锁。
第 1 次加锁之后，insert 语句发现这条记录是正常记录，没有被标记删除，接下来就会执行更新操作，也就是用 on duplicate key update 子句中各字段值更新这条记录。
更新之前，需要先读取  的完整记录，这个过程也需要对主键索引加排他普通记录锁。
这是 insert 语句第 2 次对主键索引中  的记录加锁。
第 2 次加锁时，发现之前已经加过同样的锁了，可以直接复用之前加的锁。
## 3. 读已提交
把事务隔离级别设置为 READ-COMMITTED（如已设置，忽略此步骤）：
`SET transaction_isolation = 'READ-COMMITTED';
-- 确认设置成功
SHOW VARIABLES like 'transaction_isolation';
+-----------------------+----------------+
| Variable_name         | Value          |
+-----------------------+----------------+
| transaction_isolation | READ-COMMITTED |
+-----------------------+----------------+
`
执行以下 insert 语句（**主键索引冲突，更新其它字段值**）：
`begin;
insert into t4 (id, i1, i2) values (2, 120, 220)
on duplicate key update i1 = values(i1), i2 = values(i2);
`
查看加锁情况：
`select
engine_transaction_id, object_name, index_name,
lock_type, lock_mode, lock_status, lock_data
from performance_schema.data_locks
where object_name = 't4'
and lock_type = 'RECORD'\G
***************************[ 1. row ]***************************
engine_transaction_id | 250921
object_name           | t4
index_name            | PRIMARY
lock_type             | RECORD
lock_mode             | X,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 2
`
lock_data = 2、lock_mode = X,REC_NOT_GAP 表示对主键索引中  的记录加了排他普通记录锁。
加锁流程和可重复读隔离级别一样，这里不再赘述。
## 4. 总结
insert on duplicate key update 语句，新插入记录和主键索引中已有记录冲突，可重复读和读已提交两个隔离级别下，加锁流程和加锁结果相同。
> 
**留一个小问题：**如果主键索引中和新插入记录冲突的那条记录已经被标记删除了，但是执行标记删除操作的事务还没有提交，加锁情况会有什么变化？欢迎评论区留言交流。