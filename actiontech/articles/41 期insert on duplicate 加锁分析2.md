# 41 期：insert on duplicate 加锁分析（2）

**原文链接**: https://opensource.actionsky.com/41-%e6%9c%9f%ef%bc%9ainsert-on-duplicate-%e5%8a%a0%e9%94%81%e5%88%86%e6%9e%90%ef%bc%882%ef%bc%89/
**分类**: 技术干货
**发布时间**: 2024-12-10T01:14:24-08:00

---

插入记录导致唯一索引冲突，on duplicate key update 更新非索引字段值的加锁情况分析。
> 
作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
**正文**
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
执行以下 insert 语句（**唯一索引冲突，不更新主键字段值**）：
`begin;
insert into t4 (id, i1, i2) values (7, 12, 220)
on duplicate key update i2 = values(i2);
`
查看加锁情况：
`select
engine_transaction_id, object_name, index_name,
lock_type, lock_mode, lock_status, lock_data
from performance_schema.data_locks
where object_name = 't4'
and lock_type = 'RECORD'\G
***************************[ 1. row ]***************************
engine_transaction_id | 250927
object_name           | t4
index_name            | uniq_i1
lock_type             | RECORD
lock_mode             | X
lock_status           | GRANTED
lock_data             | 12, 2
***************************[ 2. row ]***************************
engine_transaction_id | 250927
object_name           | t4
index_name            | PRIMARY
lock_type             | RECORD
lock_mode             | X,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 2
***************************[ 3. row ]***************************
engine_transaction_id | 250927
object_name           | t4
index_name            | PRIMARY
lock_type             | RECORD
lock_mode             | X
lock_status           | GRANTED
lock_data             | supremum pseudo-record
`
**lock_data = 12,2、lock_mode = X** 表示对唯一索引 uniq_i1 中 `<i1 = 12, id = 2>` 的记录加了排他 Next-Key 锁。
insert 语句执行过程中，先插入记录到主键索引，再逐个插入记录到二级索引。
对于示例 SQL，先插入 `<id = 7, i1 = 12, i2 = 220>` 的记录到主键索引，因为主键字段值（id = 7）和主键索引中已有记录不冲突，插入成功。
再插入 `<i1 = 12, id = 7>` 的记录到唯一索引 uniq_i1，插入记录之前，需要先找到插入记录的目标位置。
找到的目标位置是 uniq_i1 中 `<i1 = 12, id = 2>` 的记录后面。insert 语句发现即将插入的新记录和这条记录的 i1 字段值都是 12。
对于唯一索引，需要进行两项检查，以确认新记录是否和已有记录冲突。
**第 1 项**，检查新记录中是否有哪个字段值为 NULL。只要任何一个字段值为 NULL，InnoDB 就认为新记录和已有记录不冲突，新记录可以继续插入。
对于唯一索引，虽然从存储上来说，NULL 和 NULL 是相同的，但是从逻辑上来说，InnoDB 认为 NULL 和 NULL 不相等。
所以，唯一索引中可以插入唯一字段值为 NULL 的多条记录。
对于示例 SQL，意味着 uniq_i1 中可以插入 i1 字段值为 NULL 的多条记录。
**第 2 项**，检查已发现可能冲突的记录是否已经被标记删除。如果已经被标记删除，就不会和新记录冲突，新记录可以继续插入。
进行以上两项检查之前，insert 语句需要对表中可能冲突的记录加锁。
因为唯一索引允许插入唯一字段值为 NULL 的多条记录。为了防止其它事务往可能冲突的记录间隙插入记录，检查过程中，会对可能冲突的记录加 Next-Key 锁。
这和对主键索引中可能冲突的记录的加锁逻辑不同。
示例 SQL 包含 on duplicate key update 子句，如果确认新记录和已有记录冲突，会用这个子句中各字段值更新冲突记录，检查过程中没有加共享锁，而是直接加了排他锁。
以上就是对 uniq_i1 中 `<i1 = 12, id = 2>` 的记录加排他 Next-Key 锁的原因。
**lock_data = supremum pseudo-record、lock_mode = X** 表示对主键索引中某个数据页的 supremum 记录加了排他 Next-Key 锁。
supremum 记录和 insert 语句想要插入的记录，似乎隔着十万八千里，怎么还给它加了锁呢？
这个过程有点曲折，我们一步步来看。
insert 语句插入 `<id = 7, i1 = 12, i2 = 220>` 的记录到主键索引成功之后，接着插入 `<i1 = 12, id = 7>` 的记录到唯一索引 uniq_i1 中，发现并确认新记录和 uniq_i1 中已有 `<i1 = 12, id = 2>` 的记录冲突。 
新记录和 uniq_i1 中已有记录冲突，插入操作无法继续进行下去了，刚刚插入到主键索引的记录会被删除。
InnoDB 执行 insert 语句之前，会创建一个保存点，删除刚刚插入到主键索引的记录，就是通过回滚到这个保存点实现的。
回滚过程中，删除刚刚插入到主键索引中 `<id = 7>` 的记录之前，会把这条记录上的隐式锁转换为显式锁，锁模式为 `LOCK_X`，精确模式为 `LOCK_REC_NOT_GAP`。
按照 data_locks 表中 lock_mode 字段的显示格式是 `X,REC_NOT_GAP`。
隐式锁转换为显式锁之后，继续删除 `<id = 7>` 的记录。
但是，问题又来了，这条记录上现在有显式锁，删除这条记录之后，它上面的锁怎么办呢？
那就是只能顺延了，让它的下一条记录，也就是 supremum 记录继承它的锁。
下一条记录继承锁的时候，只会继承锁模式（`LOCK_X`），不会继承精确模式（`LOCK_REC_NOT_GAP`），然后加上自己的精确模式（`LOCK_GAP`）。
按照 data_lock 表中 lock_mode 字段的显示格式是 `X,GAP`。
然而，我们从 data_locks 表中查询出来的加锁情况，supremum 记录的 lock_mode 是 `X`，这又是为什么呢？
这是因为 InnoDB 对 supremum 记录做了特殊处理，所有事务对 supremum 记录加锁，不管原来的精确模式是什么，都会被改为 `LOCK_ORDINARY`（值为 0），也就是对 supreum 记录加的锁都会变成 Next-Key 锁。
**lock_data = 2, lock_mode = X,REC_NOT_GAP**，表示对主键索引中 `<id = 2>` 的记录加了排他普通记录锁。
回滚操作删除刚刚插入到主键索引中 `<id = 7>` 的记录之后，insert 语句接下来执行 on duplicate key update 子句的操作，用这个子句中指定的各字段值更新 uniq_i1 的冲突记录对应的表中记录，也就是 `<id = 2>` 的记录。
更新之前，需要先根据 uniq_i1 的冲突记录中保存的主键字段值，回表读取完整的主键索引记录，也就是读取主键索引中 `<id = 2>` 的完整记录。
读取记录过程中，需要对主键索引中 `<id = 2>` 的记录加锁。
按照主键字段值回表查询一条记录，加普通记录锁就可以满足要求。读取记录之后，接下来要更新记录，所以直接加了排他锁。
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
执行以下 insert 语句（**唯一索引冲突，不更新主键字段值**）：
`begin;
insert into t4 (id, i1, i2) values (7, 12, 220)
on duplicate key update i2 = values(i2);
`
查看加锁情况：
`select
engine_transaction_id, object_name, index_name,
lock_type, lock_mode, lock_status, lock_data
from performance_schema.data_locks
where object_name = 't4'
and lock_type = 'RECORD'\G
***************************[ 1. row ]***************************
engine_transaction_id | 250931
object_name           | t4
index_name            | uniq_i1
lock_type             | RECORD
lock_mode             | X
lock_status           | GRANTED
lock_data             | 12, 2
***************************[ 2. row ]***************************
engine_transaction_id | 250931
object_name           | t4
index_name            | PRIMARY
lock_type             | RECORD
lock_mode             | X,REC_NOT_GAP
lock_status           | GRANTED
lock_data             | 2
`
**lock_data = 12,2、lock_mode = X**，表示对唯一索引 uniq_i1 中 `<i1 = 12, id = 2>` 的记录加了排他 Next-Key 锁。
这条记录的加锁逻辑和可重复读隔离级别下一样，这里就不赘述了。
有一点需要说明的是，读已提交隔离级别本来不应该加 Next-Key 锁，这里却加了 Next-Key 锁。
这是因为唯一索引中允许存在唯一字段值为 NULL 的多条记录，确认新记录和表中已有记录是否冲突的过程中，为了避免其它事务插入唯一字段值为 NULL 的记录，所以这里加了 Next-Key 锁。
对于示例 SQL，虽然可能存在冲突的是唯一字段（i1）值等于 12 的记录，但是 InnoDB 没有针对唯一索引字段值是 NULL 或不是 NULL 做不同处理，而是简单粗暴的在这个场景下都加 Next-Key 锁。
**lock_data = 2、lock_mode = X,REC_NOT_GAP** 表示对主键索引中 `<id = 2>` 的记录加了排他普通记录锁。
这条记录的加锁逻辑和可重复读隔离级别下一样，也不再赘述了。
## 4. 总结
没有需要总结的内容了。