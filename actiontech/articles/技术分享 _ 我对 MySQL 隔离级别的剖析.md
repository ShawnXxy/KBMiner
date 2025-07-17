# 技术分享 | 我对 MySQL 隔离级别的剖析

**原文链接**: https://opensource.actionsky.com/20190617-mysql-acid/
**分类**: MySQL 新特性
**发布时间**: 2019-06-17T20:38:41-08:00

---

术式之后皆为逻辑，一切皆为需求和实现。希望此文能从需求、现状和解决方式的角度帮大家理解隔离级别。
**
## 隔离级别的产生
在串型执行的条件下，数据修改的顺序是固定的、可预期的结果，但是并发执行的情况下，数据的修改是不可预期的，也不固定，为了实现数据修改在并发执行的情况下得到一个固定、可预期的结果，由此产生了隔离级别。
所以隔离级别的作用是用来平衡数据库并发访问与数据一致性的方法。
## 事务的4种隔离级别
`READ UNCOMMITTED       未提交读，可以读取未提交的数据。
READ COMMITTED         已提交读，对于锁定读(select with for update 或者 for share)、update 和 delete 语句，
InnoDB 仅锁定索引记录，而不锁定它们之间的间隙，因此允许在锁定的记录旁边自由插入新记录。
Gap locking 仅用于外键约束检查和重复键检查。
REPEATABLE READ        可重复读，事务中的一致性读取读取的是事务第一次读取所建立的快照。
SERIALIZABLE           序列化
`
> 
在了解了 4 种隔离级别的需求后，在采用锁控制隔离级别的基础上，我们需要了解加锁的对象(数据本身&间隙)，以及了解整个数据范围的全集组成。
## 
## 数据范围全集组成
SQL 语句根据条件判断不需要扫描的数据范围（不加锁）；
SQL 语句根据条件扫描到的可能需要加锁的数据范围；
以单个数据范围为例，数据范围全集包含：（数据范围不一定是连续的值，也可能是间隔的值组成）
- 数据已经填充了整个数据范围：（被完全填充的数据范围，不存在数据间隙）
整型，对值具有唯一约束条件的数据范围 1～5 ，
已有数据1、2、3、4、5，此时数据范围已被完全填充；
- 整型，对值具有唯一约束条件的数据范围 1 和 5 ，
已有数据1、5，此时数据范围已被完全填充；
- 数据填充了部分数据范围：（未被完全填充的数据范围，是存在数据间隙）
整型的数据范围 1～5 ，
已有数据 1、2、3、4、5，但是因为没有唯一约束，
所以数据范围可以继续被 1～5 的数据重复填充；
- 整型，具有唯一约束条件的数据范围 1～5 ，
已有数据 2，5，此时数据范围未被完全填充，还可以填充 1、3、4 ；
- 数据范围内没有任何数据（存在间隙）
如下：
整型的数据范围 1～5 ，数据范围内当前没有任何数据。
> 
在了解了数据全集的组成后，我们再来看看事务并发时，会带来的问题
## 
## 无控制的并发所带来的问题
并发事务如果不加以控制的话会带来一些问题，主要包括以下几种情况。
- 范围内已有数据更改导致的：
更新丢失：当多个事务选择了同一行，然后基于最初选定的值更新该行时，
由于每个事物不知道其他事务的存在，最后的更新就会覆盖其他事务所做的更新；
- 脏读： 一个事务正在对一条记录做修改，这个事务完成并提交前，这条记录就处于不一致状态。
这时，另外一个事务也来读取同一条记录，如果不加控制，
第二个事务读取了这些“脏”数据，并据此做了进一步的处理，就会产生提交的数据依赖关系。
这种现象就叫“脏读”。
- 范围内数据量发生了变化导致：
不可重复读：一个事务在读取某些数据后的某个时间，再次读取以前读过的数据，
却发现其读出的数据已经发生了改变，或者某些记录已经被删除了。
这种现象就叫“不可重复读”。
- 
幻读：一个事务按相同的查询条件重新读取以前检索过的数据，
却发现其他事务插入了满足其查询条件的新数据，这种现象称为“幻读”。
可以简单的认为满足条件的数据量变化了。
> 
因为无控制的并发会带来一系列的问题，这些问题会导致无法满足我们所需要的结果。
因此我们需要控制并发，以实现我们所期望的结果(隔离级别)。
## 
## MySQL 隔离级别的实现
InnoDB 通过加锁的策略来支持这些隔离级别。
行锁包含：
- Record Locks
索引记录锁，索引记录锁始终锁定索引记录，即使表中未定义索引，
这种情况下，InnoDB 创建一个隐藏的聚簇索引，并使用该索引进行记录锁定。
- 
Gap Locks
间隙锁是索引记录之间的间隙上的锁，或者对第一条记录之前或者最后一条记录之后的锁。
间隙锁是性能和并发之间权衡的一部分。
对于无间隙的数据范围不需要间隙锁，因为没有间隙。
- 
Next-Key Locks
索引记录上的记录锁和索引记录之前的 gap lock 的组合。
假设索引包含 10、11、13 和 20。
可能的next-key locks包括以下间隔，其中圆括号表示不包含间隔端点，方括号表示包含端点：
`(负无穷大, 10]
(10, 11]
(11, 13]
(13, 20]
(20, 正无穷大)    
对于最后一个间隔，next-key将会锁定索引中最大值的上方，
`
&#8220;上确界&#8221;伪记录的值高于索引中任何实际值。
上确界不是一个真正的索引记录，因此，实际上，这个 next-key 只锁定最大索引值之后的间隙。
基于此，当获取的数据范围中，数据已填充了所有的数据范围，那么此时是不存在间隙的，也就不需要 gap lock。
对于数据范围内存在间隙的，需要根据隔离级别确认是否对间隙加锁。
默认的 REPEATABLE READ 隔离级别，为了保证可重复读，除了对数据本身加锁以外，还需要对数据间隙加锁。
READ COMMITTED 已提交读，不匹配行的记录锁在 MySQL 评估了 where 条件后释放。
对于 update 语句，InnoDB 执行 &#8220;semi-consistent&#8221; 读取，这样它会将最新提交的版本返回到 MySQL，
以便 MySQL 可以确定该行是否与 update 的 where 条件相匹配。
> 
现在我们来验证以下 MySQL 对于隔离级别的实现是否符合预期。
### 
### 场景演示
下面整理几种场景，确定其所加锁：
数据准备：
`CREATE TABLE `t` (
`a` int(11) NOT NULL,
`b` int(11) DEFAULT NULL,
`c` int(11) DEFAULT NULL,
`d` int(11) DEFAULT NULL,
`e` int(11) DEFAULT NULL,
PRIMARY KEY (`a`),
UNIQUE KEY `c` (`c`,`d`,`e`),
KEY `b` (`b`)
);
insert into t values (1,2,1,2,3),(2,2,1,2,4),(3,3,1,2,5),(4,4,2,3,4),(5,5,3,3,5),(6,7,4,5,5),(7,10,5,6,7),(8,13,5,3,1),(9,20,6,9,10),(10,23,7,7,7) ;
`
说明：
`session A
SQL1
SQL2 
....
session B
SQLN
SQLN+1
...
上面的语句都是按照时间顺序排序。
`
> 
所有的测试数据都是基于数据准备好的原始数据，每次测试完成，请自我修复现场。
场景一**
- rr 模式 + 唯一索引筛选：
数据：
`数据范围已被数据完全填充（1）
已有数据的更改
session A
start transaction ;    
update t set a=11 where a=3 ;      # 持有Record Locks（a=3）
session B
update t set a=12 where a=3 ;      # 等待a=3的Record Locks，
直到session A将其释放/等锁超时
数据范围有数据，但未被完全填充（2）
已有数据的更改
session A
start transaction ;
update t set b=11 where a>=10 ;     # 持有Record Locks （a=10），
有Next-Key Locks(a>10)
session B
update t set b=12 where a=10 ;      # 等待a=10的Record Locks，
直到session A将其释放/等锁超时
间隙的填充
session A
start transaction ;
update t set b=11 where a>=10 ;     # 持有Record Locks （a=10），
有Next-Key Locks(a>10)
session B
insert into t values(11,1,21,1,1);  # 插入等待，
因为存在a>10的Next-Key Locks 
数据范围内没有数据（3）
间隙的填充
session A
start transaction ; 
update t set b=11 where a>=100 and a<=200 ;         # 存在Gap Locks
session B
insert into t values(150,1,21,1,1);    # 插入等待，
因为存在(10,无穷大)的Gap Locks，
a最大的一个值是10
insert into t values(11,1,1,2,2) ;     # 插入等待，
因为存在(10,无穷大)的Gap. Locks，
a最大的一个值是10
update t set b=8 where a=10 ;          # 更改成功，
因为session A并未持有Record Locks 
update t set b=23 where a=10 ;         # 恢复现场 `
场景二
- rc 模式 + 唯一索引筛选：
数据：
`数据范围已被数据完全填充（4）
已有数据的更改
session A
start transaction ;    
update t set a=11 where a=3 ;      # 持有Record Locks（a=3）
session B
update t set a=12 where a=3 ;      # 等待a=3的Record Locks，
直到session A将其释放/等锁超时
数据范围有数据，但未被完全填充（5）
已有数据的更改
session A
start transaction ;
update t set b=11 where a>=10 ;     # 持有Record Locks （a=10），
无Next-Key Locks(a>10)
session B
update t set b=12 where a=10 ;      # 等待a=10的Record Locks，
直到session A将其释放/等锁超时
间隙的填充
session A
start transaction ;
update t set b=11 where a>=10 ;     # 持有Record Locks （a=10），
无Next-Key Locks(a>10)
session B
insert into t values(11,1,21,1,1);  # 插入成功
delete from t where a=11 ;          # 恢复现场
数据范围内没有数据（6）
间隙的填充
session A
start transaction ; 
update t set b=11 where a>=100 and a<=200 ;  # 无对应的索引，
所以无Record Locks，
无Next-Key Locks
session B
insert into t values(150,1,21,1,1);                 # 插入成功
delete from t where a=150 ;                         # 恢复现场
`
场景三
- rr 模式 + 非唯一索引筛选：（非唯一索引筛选的情况下，不存在数据完全填充的场景）
数据：
`数据范围有数据，但未被完全填充（7） 
**已有数据的更改**
session A
start transaction ;
update t set e=7 where b=2 and e=4 ;    # 获取非唯一索引，命中b=2的索引值，
b=2的索引值对应多条记录。
此时有Record Locks，加在非唯一索引上
session B
update t set e=7 where b=2 and e=10 ; # session A已获取了b=2的 Record Locks ，
session B等待session A将其释放/等锁超时
即使该条件命中的是空记录
间隙的填充
session A
start transaction ;
update t set d=6 where b>=5 and b<=7 ;  # 获取了b=5和 b=7的 Record Locks，
和(5,7)的Gap Locks
session B
insert into t values(11,6,11,12,13) ;   # 插入b=6的记录，插入等待，
存在b的数据范围(5,7)的 Gap Locks。
数据范围内没有数据（8）
间隙的填充
session A
start transaction ;
update t set b=100 where b>=120  ;      # b>=120命中了空的数据范围，
所以无Record Locks，
但存在(23,正无穷)的Gap Locks
session B
insert into t values(200,200,200,200,200) ;  # 插入等待，
等待(23,正无穷)的Gap Locks的释放
insert into t values(100,24,3,4,60) ;        # 插入等待，
等待(23,正无穷)的Gap locks的释放
update t set b=12 where b=23 ;   # 更新成功，
因为session A并未获取Record Locks，
所以不会阻止已有行的更新
update t set b=23 where b=12 ;   # 恢复现场 
`
场景四
- rc 模式 + 非唯一索引筛选：（非唯一索引筛选的情况下，不存在数据完全填充的场景）
数据：
`数据范围有数据，但未被完全填充（9）
已有数据的更改
session A
start transaction ;
update t set e=7 where b=2 and e=4 ;   # 获取非唯一索引，命中b=2的索引值，
b=2的索引值对应多条记录。
此时有Record Locks，加在非唯一索引上
session B
update t set e=7 where b=2 and e=10 ;  # session A已获取了b=2的Record Locks ，
session B等待session A将其释放/等锁超时，
即使该条件命中的是空记录
间隙的填充
session A
start transaction ;
update t set d=6 where b>=5 and b<=7 ;  # 获取了b=5和 b=7的 Record Locks，
无Next-Key Locks
session B
insert into t values(11,6,11,12,13) ;   # 插入成功，因为无 Next-Key Locks
数据范围内没有数据（10）
间隙的填充
session A
start transaction ;
update t set b=100 where b>=120  ;      # b>=120命中了空的数据范围，
所以无Record Locks，
无Next-Key Locks
session B
insert into t values(200,200,200,200,200) ;   # 插入成功，因为无Next-Key Locks
`
场景五
- rr 模式 + 无索引筛选：（无索引筛选的情况下，不存在数据完全填充的场景）
数据：
`数据范围有数据，但未被完全填充（11）
已有数据的更改
session A
start transaction ;
update t set c=100 where d=2 ;      # d=2 对应a=1、a=2、a=3的记录，
因为where条件未使用索引，故只能全表扫描，
并对所有行加Record Locks，
并且在间隙中加上Gap Locks
session B
update t set b=100 where a=1 ;      # 等待session A获取的a=1的X锁
间隙的填充
因为where条件并未使用索引，所以最终加锁都回归到了对基表的聚簇索引加锁，
但是where条件未使用索引，自然更无唯一约束，
所以逻辑上可以认为除where命中的行以外的其他范围都是间隙。
而实际上因为通过聚簇索引加锁，所以在每两个聚簇索引之间才会加上Gap Locks。
session A
start transaction ;
update t set c=100 where d=2 ;      # d=2 对应a=1、a=2、a=3的记录，
因为where条件未使用索引，故只能全表扫描，
并对所有聚簇索引加Record Locks，
并且加上Next-Key Locks   
session B 
update t set b=50  where a=8 ;      # 等待session A获取的a=8的X锁
insert into t values(110,30,30,40,500);     # 等待Next-Key Locks          
数据范围内没有数据（12）
间隙的填充 
因为where条件并未使用索引，所以最终加锁都回归到了对基表的聚簇索引加锁，
但是where条件未使用索引，自然更无唯一约束，
所以逻辑上可以认为除where命中的行以外的其他范围都是间隙。
而实际上因为通过聚簇索引加锁，所以在每两个聚簇索引之间才会加上Gap Locks。
session A
start transaction ;
update t set c=100 where d=20 ;            #  因为where条件未使用索引，
故只能全表扫描，
并对所有聚簇索引加Record Locks，
并且加上Next-Key Locks   
session B 
update t set b=50  where a=8 ;             # 等待session A获取的a=8的X锁
insert into t values (100,3,100,20,4) ;    # 等待Next-Key Locks
`
场景六
- rc 模式 + 无索引筛选：（无索引筛选的情况下，不存在数据完全填充的场景）
数据：
`数据范围有数据，但未被完全填充（13）
已有数据的更改
session A
start transaction ;
update t set c=100 where d=2 ;      # 对应a=1、a=2、a=3的记录,
因为where条件未使用索引，故只能全表扫描，
并对a=1、a=2、a=3聚簇索引加Record Locks，
但是无Next-Key Locks 
session B
update t set b=100 where a=1 ;      # 等待session A获取的a=1的Record Locks
间隙的填充 
因为where条件并未使用索引，所以最终加锁都回归到了对基表的聚簇索引加锁，
但是where条件未使用索引，自然更无唯一约束，
所以逻辑上可以认为除where命中的行以外的其他范围都是间隙。
而实际上因为通过聚簇索引加锁，所以在每两个聚簇索引之间才会加上Gap Locks。
session A
start transaction ;
update t set c=100 where d=2 ;      # 对应a=1、a=2、a=3的记录，
因为where条件未使用索引，故只能全表扫描，
并对a=1、a=2、a=3聚簇索引加Record Locks，
但是无Next-Key Locks   
session B 
update t set b=50  where a=8 ;      # 成功，因为a=8并未被session A加锁
insert into t values(110,30,30,2,500);    # 成功，因为不存在Gap Locks & 
next-Key Locks
数据范围内没有数据（14）
间隙的填充* 
session A
start transaction ;
update t set c=100 where d=20 ;            # 无Record Locks，
也无Next-Key Locks       
session B 
insert into t values (100,3,100,20,4) ;    # 成功
delete from t where a=100 ;                # 恢复现场
`
## 
## 总结&延展：
唯一索引存在唯一约束，所以变更后的数据若违反了唯一约束的原则，则会失败。
当 where 条件使用二级索引筛选数据时，会对二级索引命中的条目和对应的聚簇索引都加锁；所以其他事务变更命中加锁的聚簇索引时，都会等待锁。
行锁的增加是一行一行增加的，所以可能导致并发情况下死锁的发生。
例如，在 session A 对符合条件的某聚簇索引加锁时，可能 session B 已持有该聚簇索引的 Record Locks，
而 session B 正在等待 session A 已持有的某聚簇索引的 Record Locks。
session A 和 session B 是通过两个不相干的二级索引定位到的聚簇索引。
session A 通过索引 id_A，session B通过索引 id_B 。
当 where 条件获取的数据无间隙时，无论隔离级别为 rc 或 rr，都不会存在间隙锁。
比如通过唯一索引获取到了已完全填充的数据范围，此时不需要间隙锁。
间隙锁的目的在于阻止数据插入间隙，所以无论是通过 insert 或 update 变更导致的间隙内数据的存在，都会被阻止。
rc 隔离级别模式下，查询和索引扫描将禁用 gap locking，此时 gap locking 仅用于外键约束检查和重复键检查（主要是唯一性检查）。
rr 模式下，为了防止幻读，会加上 Gap Locks。
事务中，SQL 开始则加锁，事务结束才释放锁。
就锁类型而言，应该有优化锁，锁升级等，例如rr模式未使用索引查询的情况下，是否可以直接升级为表锁。
就锁的应用场景而言，在回放场景中，如果确定事务可并发，则可以考虑不加锁，加快回放速度。
锁只是并发控制的一种粒度，只是一个很小的部分：
从不同场景下是否需要控制并发，(已知无交集且有序的数据的变更，MySQL 的 MTS 相同前置事务的多事务并发回放)
并发控制的粒度，(锁是一种逻辑粒度，可能还存在物理层和其他逻辑粒度或方式)
相同粒度下的优化，(锁本身存在优化，如IX、IS类型的优化锁)
粒度加载的安全&性能(如获取行锁前，先获取页锁，页锁在执行获取行锁操作后即释放，无论是否获取成功)等多个层次去思考并发这玩意。
#### 第三期 社区技术内容征稿
所有稿件，一经采用，均会为作者署名。
征稿主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关的技术内容
活动时间：2019年6月11日 &#8211; 7月11日
**本期投稿奖励**
投稿成功：京东卡200元*1
优秀稿件：京东卡200元*1+社区定制周边（包含：定制文化衫、定制伞、鼠标垫）
优秀稿件评选，文章获得“好看”数量排名前三的稿件为本期优秀稿件。
![](https://opensource.actionsky.com/wp-content/uploads/2019/06/第三期-社区征稿-海报-1.png)