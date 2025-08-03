# 技术分享 | 可能是目前最全的 MySQL 8.0 新特性解读(下)

**原文链接**: https://opensource.actionsky.com/20230322-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-03-21T21:34:13-08:00

---

作者：马文斌
MySQL爱好者,任职于蓝月亮(中国)有限公司。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
上一篇主要讲了第一部分：功能增强，感兴趣的亲请点击【[可能是史上最全的 MySQL 8.0 新特性解读(上)](https://mp.weixin.qq.com/s/AafVRpOrCTKA7Zg0E3eixQ)】，这一篇我们继续：
#### 二、性能提升
##### 2.1-基于竞争感知的事务调度
MySQL 在 8.0.3 版本引入了新的事务调度算法，基于竞争感知的事务调度，Contention-Aware Transaction Scheduling，简称CATS。在CATS算法之前，MySQL使用FIFO算法，先到的事务先获得锁，如果发生锁等待，则按照FIFO算法进行排队。CATS相比FIFO更加复杂，也更加聪明，在高负载、高争用的场景下，性能提升显著。
##### 2.2-基于WriteSet的并行复制
总的来说MySQL关于并行复制到目前为止经历过三个比较关键的时间结点“库间并发”，“组提交”，“写集合”；真可谓是江山代有人才出，前浪死在沙滩上；总的来说就后面的比前面的不知道高到哪里去了！
MySQL 8.0 版本引入了一个新的机制 WriteSet，来追踪事务之间的依赖性，这个特性被用于优化从库应用binlog的速度，在主库并发较低的场景下，能够显著提高从库回放binlog的速度，基于WriteSet 的并行复制方案，彻底解决了MySQL复制延迟问题。只需要设置这2个参数即可
binlog_transaction_dependency_tracking  = WRITESET                 #    COMMIT_ORDER     
transaction_write_set_extraction        = XXHASH64
##### 2.3-JSON特性增强
MySQL 8 大幅改进了对 JSON 的支持，添加了基于路径查询参数从 JSON 字段中抽取数据的 JSON_EXTRACT() 函数，以及用于将数据分别组合到 JSON 数组和对象中的 JSON_ARRAYAGG() 和 JSON_OBJECTAGG() 聚合函数。
在主从复制中，新增参数 binlog_row_value_options，控制JSON数据的传输方式，允许对于Json类型部分修改，在binlog中只记录修改的部分，减少json大数据在只有少量修改的情况下，对资源的占用。
##### 2.4-空间数据类型增强
MySQL 8 大幅改进了空间数据类型和函数，支持更多的空间分析函数和空间类型对象，空间分析功能和性能得到大幅提升。
##### 2.5-doublewrite改进
在MySQL 8.0.20 版本之前，doublewrite 存储区位于系统表空间，从 8.0.20 版本开始，doublewrite 有自己独立的表空间文件，这种变更，能够降低doublewrite的写入延迟，增加吞吐量，为设置doublewrite文件的存放位置提供了更高的灵活性。
##### 2.6-hash join
MySQL 8.0.18 版本引入 hash join 功能，对于没有走索引的等值 join 连接可以使用 hash join 进行优化。8.0.20 版本对 hash join 进行了加强，即使 join 连接没有使用等值条件也可以使用 hash join 优化，原来使用 BNL 算法的 join 连接将全部由 hash join 代替。
##### 2.6.1-NestLoopJoin算法
简单来说，就是双重循环，遍历外表(驱动表)，对于外表的每一行记录，然后遍历内表，然后判断join条件是否符合，进而确定是否将记录吐出给上一个执行节点。
从算法角度来说，这是一个M*N的复杂度。
##### 2.6.2-Hash Join
是针对equal-join场景的优化，基本思想是，将外表数据load到内存，并建立hash表，这样只需要遍历一遍内表，就可以完成join操作，输出匹配的记录。
如果数据能全部load到内存当然好，逻辑也简单，一般称这种join为CHJ(Classic Hash Join)，之前MariaDB就已经实现了这种HashJoin算法。
如果数据不能全部load到内存，就需要分批load进内存，然后分批join，下面具体介绍这几种join算法的实现。
##### 2.7-anti join（反连接）
MySQL 8.0.17版本引入了一个anti join的优化，这个优化能够将where条件中的not in(subquery)， not exists(subquery)，in(subquery) is not true，exists(subquery) is not true，在内部转化成一个anti join，以便移除里面的子查询subquery，这个优化在某些场景下，能够将性能提升20%左右。
anti join适用的场景案例通常如下：
- 找出在集合A且不在集合B中的数据
- 找出在当前季度里没有购买商品的客户
- 找出今年没有通过考试的学生
- 找出过去3年，某个医生的病人中没有进行医学检查的部分
##### 2.8-redo优化
mysql8.0一个新特性就是redo log提交的无锁化。在8.0以前，各个用户线程都是通过互斥量竞争，串行的写log buffer，因此能保证lsn的顺序无间隔增长。
mysql8.0通过redo log无锁化，解决了用户线程写redo log时竞争锁带来的性能影响。同时将redo log写文件、redo log刷盘从用户线程中剥离出来，抽成单独的线程，用户线程只负责将redo log写入到log buffer，不再关心redo log的落盘细节，只需等待log_writer线程或log_flusher线程的通知。
##### 2.9-直方图（统计信息）
优化器会利用column_statistics的数据，判断字段的值的分布，得到更准确的执行计划。
可以通过ANALYZE TABLE table_name [UPDATE HISTOGRAM on colume_name with N BUCKETS |DROP HISTOGRAM ON clo_name] 来收集或者删除直方图信息。
直方图统计了表中某些字段的数据分布情况，为优化选择高效的执行计划提供参考，直方图与索引有着本质的区别，维护一个索引有代价。每一次的insert、update、delete都需要更新索引，会对性能有一定的影响。而直方图一次创建永不更新，除非明确去更新它，因此不会影响insert、update、delete的性能。
##### 2.10-关闭QC（Query Cache ）
从 MySQL 8.0开始，不再使用查询缓存（Query Cache）。
随着技术的进步，经过时间的考验，MySQL的工程团队发现启用缓存的好处并不多。
首先，查询缓存的效果取决于缓存的命中率，只有命中缓存的查询效果才能有改善，因此无法预测其性能。
其次，查询缓存的另一个大问题是它受到单个互斥锁的保护。在具有多个内核的服务器上，大量查询会导致大量的互斥锁争用。
MySQL8.0取消查询缓存的另外一个原因是，研究表明，缓存越靠近客户端，获得的好处越大。MySQL8.0新增加了一些其他对性能干预的工具来支持。另外，还有像ProxySQL这样的第三方工具，也可以充当中间缓存。
#### 三、安全性增强
##### 3.1-死锁检测
可以使用一个新的动态变量 innodb_deadlock_detect 来禁用死锁检测。在高并发系统上，当多个线程等待同一个锁时，死锁检测会导致速度变慢。有时，禁用死锁检测并在发生死锁时依靠 innodb_lock_wait_timeout 设置进行事务回滚可能更有效。
##### 3.2-默认密码认证插件
MySQL 8.0.4 版本修改了默认的身份认证插件，从老的mysql_native_password插件变为新的caching_sha2_password，并将其作为默认的身份认证机制，同时客户端对应的libmysqlclient也默认使用新的认证插件。
##### 3.3-升级密码过期，历史密码使用规则
设置历史密码检测规则，防止反复重用旧密码。
- password_history
- password_reuse_interval
双密码机制，修改密码时，创建新的密码，同时旧的密码也可以使用，保留一定的缓冲时间进行检查确认。
当修改一个账户密码时，需要去验证当前的密码，通过参数password_require_current来控制，默认关闭，当打开该选项时，如果要修改账户密码，必须要提供当前的密码才允许修改。
##### 3.4-认值加密插件
老版本：认证方式为sha256_password
8.0 版本：在老版本的基础上，新增caching_sha2_password,可以使用缓存解决连接时的延时问题。
需要注意的问题是：如果客户端与服务端配置不同，无法进行连接，两者的加密认证方式需要一样。
##### 3.5-用户密码增强
**（1）密码的重复使用策略**
历史密码重复次数检测：新密码不能与最近最新的5个密码相同。
password_history = 5 ; 
时间间隔：新密码不能和过去90天内的密码相同。
password_reuse_interval = 90 ; 
**（2）修改密码必要的验证策略**
修改密码，要输入当前的密码。增加了用户的安全性。
## 默认为off；为on 时 修改密码需要用户提供当前密码 (开启后修改密码需要验证旧密码，root 用户不需要)
password_require_current = on 
**（3）双密码**
相比于一个用户只有一个密码最大优点就是:修改密码不会导致应用不可用。那么应用就可以自动使用副密码（副密码和当前密码保持一致）连接数据库库。确保了业务的不中断。修改密码不会导致应用不可用；应用就可以自动使用副密码连接数据库。
##### 3.6-角色功能
MySQL角色是指定权限集合。像用户账户一样，角色可以拥有授予和撤销的权限。
可以授予用户账户角色，授予该账户与每个角色相关的权限。
方便了用户权限管理和维护。很好地解决了多个用户使用相同的权限集。权限–》角色–》用户。
##### 3.7-redo & undo 日志加密
增加以下两个参数，用于控制redo、undo日志的加密。
innodb_redo_log_encryptinnodb_undo_log_encrypt
#### 四、优化器增强
##### 4.1-Cost Model改进
优化器能够感知到页是否存在缓冲池中。5.7其实已经开放接口，但是不对内存中的页进行统计，返回都是1.0.
##### 4.2-可伸缩的读写负载 Scaling Read/Write Workloads
8.0版本对于读写皆有和高写负载的拿捏恰到好处。在集中的读写均有的负载情况下，我们观测到在4个用户并发的情况下，对于高负载，和5.7版本相比有着两倍性能的提高。在5.7上我们显著了提高了只读情况下的性能，8.0则显著提高了读写负载的可扩展性。为MySQL提升了硬件性能的利用率，其改进是基于重新设计了InnoDB写入Redo日志的方法。对比之前用户线程之前互相争抢着写入其数据变更，在新的Redo日志解决方案中，现在Redo日志由于其写入和刷缓存的操作都有专用的线程来处理。用户线程之间不在持有Redo写入相关的锁，整个Redo处理过程都是时间驱动。
8.0版本允许马力全开的使用存储设备，比如使用英特尔奥腾闪存盘的时候，我们可以在IO敏感的负载情况下获得1百万的采样 QPS（这里说的IO敏感是指不在IBP中，且必须从二级存储设备中获取）。这个改观是由于我们摆脱了 `file_system_mutex`全局锁的争用。
##### 4.3-在高争用（热点数据）负载情况下的更优性能
Better Performance upon High Contention Loads (“hot rows”)
8.0版本显著地提升了高争用负载下的性能。高争用负载通常发生在许多事务争用同一行数据的锁，导致了事务等待队列的产生。在实际情景中，负载并不是平稳的，负载可能在特定的时间内爆发（80/20法则）。8.0版本针对短时间的爆发负载无论在每秒处理的事务数（换句话，延迟）还是95%延迟上都处理的更好。对于终端用户来说体现在更好的硬件资源利用率（效率）上。因为系统需要尽量使用榨尽硬件性能，才可以提供更高的平均负载。
#### 五、其他增强
##### 5.1-支持在线修改全局参数并持久化
通过加上PERSIST关键字，可以将修改的参数持久化到新的配置文件（mysqld-auto.cnf）中，重启MySQL时，可以从该配置文件获取到最新的配置参数。
系统会在数据目录下生成mysqld-auto.cnf 文件，该文件内容是以json格式存储的。当my.cnf 和mysqld-auto.cnf 同时存在时，后者优先级更高。
例如：
SET PERSIST max_connections = 1000;
SET @@PERSIST.max_connections = 1000;
此 SET 语法使您能够在运行时进行配置更改，这些更改也会在服务器重新启动后持续存在。与 SET GLOBAL 一样，SET PERSIST 设置全局变量运行时值，但也将变量设置写入 mysqld-auto.cnf 文件（如果存在则替换任何现有变量设置）。
##### 5.2-binlog日志过期时间精确到秒
之前是天，并且参数名称发生变化. 在8.0版本之前，binlog日志过期时间设置都是设置`expire_logs_days`参数，而在8.0版本中，MySQL默认使用binlog_expire_logs_seconds参数。
##### 5.3-undo空间自动回收
innodb_undo_log_truncate参数在8.0.2版本默认值由OFF变为ON，默认开启undo日志表空间自动回收。
innodb_undo_tablespaces参数在8.0.2版本默认为2，当一个undo表空间被回收时，还有另外一个提供正常服务。
innodb_max_undo_log_size参数定义了undo表空间回收的最大值，当undo表空间超过这个值，该表空间被标记为可回收。
##### 5.4-地理信息系统 GIS
8.0 版本提供对地形的支持，其中包括了对空间参照系的数据源信息的支持，SRS aware spatial数据类型，空间索引，空间函数。总而言之，8.0版本可以理解地球表面的经纬度信息，而且可以在任意受支持的5000个空间参照系中计算地球上任意两点之间的距离.
注意:升级前，一定要验证jdbc驱动是否匹配，是否需要随着升级。
##### 5.5-参数开关表
select @@optimizer_switch \G
mysql> select @@optimizer_switch \G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=on,hypergraph_optimizer=off,derived_condition_pushdown=on
session 开关
set session optimizer_switch="use_invisible_indexes=off";  
set session optimizer_switch="use_invisible_indexes=on";  
global 开关
set global optimizer_switch="use_invisible_indexes=off";  
set global optimizer_switch="use_invisible_indexes=on";