# 17 期 | InnoDB 有哪几种行锁？

**原文链接**: https://opensource.actionsky.com/17-%e6%9c%9f-innodb-%e6%9c%89%e5%93%aa%e5%87%a0%e7%a7%8d%e8%a1%8c%e9%94%81%ef%bc%9f/
**分类**: 技术干货
**发布时间**: 2024-05-27T01:53:26-08:00

---

InnoDB 有哪几种行锁，其中比较特殊的插入意向锁为什么而存在？
> 
作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 准备工作
确认事务隔离级别为可重复读：
`show variables like 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
`
创建测试表：
`CREATE TABLE `t1` (
`id` int unsigned NOT NULL AUTO_INCREMENT,
`i1` int DEFAULT '0',
PRIMARY KEY (`id`) USING BTREE,
KEY `idx_i1` (`i1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
`
插入测试数据：
`INSERT INTO `t1` (`id`, `i1`) VALUES 
(10, 101), (20, 201), (30, 301), (40, 401);
`
准备查询加锁情况使用的 SQL 语句：
`select
engine_transaction_id, object_name,
lock_type, lock_mode, lock_status, lock_data
from performance_schema.data_locks
where object_name = 't1' and lock_type = 'RECORD'\G
`
## 2. 共享锁 & 排他锁
和表锁一样，InnoDB 行锁也分共享锁（S）、排他锁（X）。
和表锁不一样，行锁的共享锁（S）、排他锁（X）还可以继续细分为三类：
- 普通记录锁（LOCK_REC_NOT_GAP）。
- 间隙锁（LOCK_GAP）。
- Next-Key 锁（LOCK_ORDINARY）。
除了以上三类，排他锁（X）还包含另一类有点特殊的锁，就是插入意向锁（`LOCK_INSERT_INTENTION`）。
## 3. 普通记录锁
普通记录锁，只锁定记录本身，不锁定记录前面的间隙，用于避免多个事务同时对同一条记录进行读写导致冲突。
多个事务想同时对同一条记录加普通记录锁，可以同时加共享锁，但不能同时加排他锁，也不能同时加共享锁和排他锁。
共享普通记录锁是这样的：
`begin;
select * from t1 where id = 10
lock in share mode;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 10
`
lock_mode = S,REC_NOT_GAP, lock_data = 10 表示对 t1 表中 id = 10 的记录加了共享普通记录锁。
排他普通记录锁是这样的：
`begin;
select * from t1 where id = 10
for update;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 221456
object_name           | t1
lock_type             | RECORD
lock_mode             | X,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 10
`
lock_mode = X,REC_NOT_GAP, lock_data = 10 表示对 t1 表中 id = 10 的记录加了排他普通记录锁。
## 4. 间隙锁
可重复读（REPEATABLE-READ）、可串行化（SERIALIZABLE）两个事务隔离级别，都支持可重复读。
这两个事务隔离级别下，一个事务多次执行同一条 select 语句，得到的记录数量是相同的，各记录的字段值也是相同的。
要保证多次执行同一条 select 语句得到的记录数量相同，就需要保证 select 语句第一次执行时开始，最后一次执行完成时为止，过程中不允许其它事务插入记录到 select 语句 where 条件覆盖的范围内。
为了拥有这个能力，InnoDB 就引入了间隙锁。
间隙锁也分为共享锁和排他锁，共享间隙锁是这样的：
`begin;
select * from t1 where id < 10
lock in share mode;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S,GAP
lock_status           | GRANTED
lock_data             | 10
`
lock_mode = S,GAP, lock_data = 10 表示对 t1 表中 id = 10 的记录加了共享间隙锁。
排他间隙锁是这样的：
`begin;
update t1 set i1 = i1 + 66
where id < 10;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 221457
object_name           | t1
lock_type             | RECORD
lock_mode             | X,GAP
lock_status           | GRANTED
lock_data             | 10
`
lock_mode = X,GAP, lock_data = 10 表示对 t1 表中 id = 10 的记录加了排他间隙锁。
虽然间隙锁分为共享锁和排他锁，但是它们除了名字不同之外，就没有其它区别了。
对于同一条记录前面的间隙，多个事务可以同时加共享间隙锁，也可以同时加排他间隙锁，还可以同时加共享间隙锁和排他间隙锁。
我们开启三个会话，执行三个事务，同时对 t1 表中 id = 10 的记录前面的间隙加间隙锁：
`-- session 1
begin;
select * from t1 where id < 10
lock in share mode;
-- session 2
begin;
update t1 set i1 = i1 + 66
where id < 10;
-- session 3
begin;
update t1 set i1 = i1 + 88
where id < 10;
`
加锁情况如下：
`-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 221458
object_name           | t1
lock_type             | RECORD
lock_mode             | X,GAP
lock_status           | GRANTED
lock_data             | 10
***************************[ 2. row ]***************************
engine_transaction_id | 221455
object_name           | t1
lock_type             | RECORD
lock_mode             | X,GAP
lock_status           | GRANTED
lock_data             | 10
***************************[ 3. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S,GAP
lock_status           | GRANTED
lock_data             | 10
`
两条 update 语句所属的事务（`engine_transaction_id = 221458、221455`），都对 t1 表中 id = 10 的记录加了排他间隙锁。
select 语句所属的事务（`engine_transaction_id = 281479865470888`），对 t1 表中 id = 10 的记录加了共享间隙锁。
这就说明了共享间隙锁和排他间隙锁不会相互阻塞、多个排他间隙锁也不会相互阻塞。
## 5. Next-Key 锁
普通记录锁只会锁定记录本身，不会锁定记录前面的间隙。
间隙锁只会锁定记录前面的间隙，不会锁定记录本身。
如果我们既想锁定记录本身，又想锁定记录前面的间隙，怎么办？
此处应该有掌声，欢迎 Next-Key 锁上台。
**等。。。等。。。**
如果我们既想锁定记录本身，又想锁定记录前面的间隙，先加个普通记录锁，再加个间隙锁不就完事了，又弄来个 Next-Key 锁，也太复杂了吧？
本来两种锁就能搞定的事情，现在要用三种锁，表面上看确实是有点复杂。
不过，咱们往积极的方面想想，加锁是需要占用内存的，多加一个锁就多占用一份内存，弄个二合一的 Next-Key 锁，就能少占用点内存了。
况且，除了内存方面，可能背后还有我们不知道的原因，比如：用三种锁比用两种锁写的代码更少？
言归正传，和普通记录锁一样，Next-Key 锁的共享锁和排他锁是互斥的，多个排他锁之间也是互斥的。
共享 Next-Key 锁是这样的：
`begin;
select * from t1 where id <= 10
lock in share mode;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S
lock_status           | GRANTED
lock_data             | 10
`
lock_mode = S, lock_data = 10 表示对 t1 表中 id = 10 的记录加了共享 Next-Key 锁。
排他 Next-Key 锁是这样的：
`begin;
update t1 set i1 = i1 + 66
where id <= 10;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 221459
object_name           | t1
lock_type             | RECORD
lock_mode             | X
lock_status           | GRANTED
lock_data             | 10
`
lock_mode = X, lock_data = 10 表示对 t1 表中 id = 10 的记录加了排他 Next-Key 锁。
从普通记录锁、间隙锁、Next-Key 锁的 `lock_mode` 可以看到，虽然 Next-Key 锁兼具普通间隙锁和间隙锁的能力，但它并不是简单的等于普通间隙锁 + 间隙锁，而是一种独立的锁类型。
不过，有一种特殊情况：事务对记录加了普通记录锁之后，又想对该记录加 Next-Key 锁，InnoDB 只会给该记录加间隙锁，而不会加 Next-Key 锁。
这样一来，这条记录上的普通记录锁和间隙锁加起来，也具有了和 Next-Key 锁同等的保护能力。
我们来复现一下这种情况，先执行一条 select 语句，对 id = 10 的记录加共享普通记录锁：
`begin;
select * from t1 where id = 10
lock in share mode;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 10
`
再执行一条 select 语句，对 id = 10 的记录加共享 Next-Key 锁：
`-- 在同一个事务中执行以下 SQL
select * from t1 where id <= 10
lock in share mode;
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 10
***************************[ 2. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S,GAP
lock_status           | GRANTED
lock_data             | 10
`
从加锁情况可以看到，InnoDB 并没有给 id = 10 的记录加共享 Next-Key 锁，而是加了共享间隙锁。
## 6. 插入意向锁
插入意向锁其实也是一种间隙锁，只不过它的使用场景有点特殊，只有 insert 语句可能会用到。
事物插入记录时，如果目标插入位置（某条记录前面的间隙）被其它事务加了间隙锁或 Next-Key 锁，insert 语句就需要对这个间隙加插入意向锁，并且等待间隙锁或 Next-key 锁释放之后才能获得插入意向锁。
获得插入意向锁之后，才能继续插入记录到目标位置。
我们开启两个会话，执行两个事务，模拟插入记录被阻塞，加插入意向锁的场景：
`-- session 1
begin;
select * from t1 where id <= 10
lock in share mode;
-- session 2
begin;
insert into t1(id, i1)
values (5, 51);
-- 使用【1.准备工作】小节的 SQL 查看加锁情况
***************************[ 1. row ]***************************
engine_transaction_id | 221455
object_name           | t1
lock_type             | RECORD
lock_mode             | X,GAP,INSERT_INTENTION
lock_status           | WAITING
lock_data             | 10
***************************[ 2. row ]***************************
engine_transaction_id | 281479865470888
object_name           | t1
lock_type             | RECORD
lock_mode             | S
lock_status           | GRANTED
lock_data             | 10
`
select 语句所属的事务（`engine_transaction_id = 281479865470888`），对 id = 10 的记录加了共享 Next-Key 锁（`lock_mode = S`）。insert 语句不能插入记录到 id = 10 的记录前面的间隙。
insert 语句所属的事务（`engine_transaction_id = 221455`），已经申请对该间隙加插入意向锁（`lock_mode = X,GAP,INSERT_INTENTION`），并且处于等待获得锁的状态（`lock_status = WAITING`）。
lock_mode = X,GAP,INSERT_INTENTION，说明插入意向锁也是一种间隙锁，它只是在排他间隙锁的基础上加了个 INSERT_INTENTION 标志。
## 7. 总结
普通记录锁用于锁定记录本身，lock_mode 中包含 REC_NOT_GAP。共享锁和排他锁互斥，排他锁之间也互斥。
间隙锁用于锁定记录前面的间隙，lock_mode 中包含 GAP。共享锁和排他锁不互斥，排他锁之间也不互斥。
Next-Key 锁既锁定记录本身，又锁定记录前面的间隙，lock_mode 只有孤零零的 S 或 X。共享锁和排他锁互斥，排他锁之间也互斥。
插入意向锁，是一种特殊的间隙锁，lock_mode 中包含 INSERT_INTENTION。