# MySQL Binlog GTID

**Date:** 2023/11
**Source:** http://mysql.taobao.org/monthly/2023/11/02/
**Images:** 2 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2023 / 11
 ](/monthly/2023/11)

 * 当期文章

 聊聊日志即数据库
* MySQL Binlog GTID

 ## MySQL Binlog GTID 
 Author: 枫明 

 GTID标识了Binlog事务的全局唯一性，保证事务在集群的每个实例上有且只执行了一次。开启Binlog和GTID后，MySQL会为每个事务绑定一个GTID，该事务执行成功后，对应的GTID会被记录在Binlog中。因此MySQL可以通过GTID的状态来判断状态机状态，在搭建复制时，根据GTID判断上下游复制节点的事务执行状态，上游就可以将下游没有的事务同步到下游。

开启GTID需要设置[enforce_gtid_consistency=ON](https://dev.mysql.com/doc/refman/8.0/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency) 和[gtid_mode=ON](https://dev.mysql.com/doc/refman/8.0/en/replication-options-gtids.html#sysvar_gtid_mode)，前者保证了该语句能安全的以GTID事务的形式记录，举个例子，有些表不支持事务操作，若用GTID记录了对该表的操作，若语句执行失败，又无法回滚到执行前的状态，那么GTID无法决定该语句的原子性了，也就无法通过GTID判断主从节点状态是否一致。此外gtid_mode还有几种其他的参数：ON_PERMISSIVE、OFF_PERMISSIVE、OFF，描述了主从节点产生的Binlog事务是否记录GTID。

 本文内容基于 MySQL Community 8.0.13 Version

## 意义

在上下游复制时用到GTID，下游将自己的GTID集合发给上游，上游据此同步数据。在change master语句中可以指定使用GTID复制。使用GTID复制需要source的gtid_mode=ON，replica的gtid_mode不是OFF，replica在change master语句中设置MASTER_AUTO_POSITION=1，比如：

* change master to

`CHANGE MASTER TO 
MASTER_HOST='',
MASTER_USER='',
MASTER_PASSWORD='',
MASTER_AUTO_POSITION=1,
MASTER_PORT=,
MASTER_HEARTBEAT_PERIOD=;
`

此时replica将自己的[gtid_executed](https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_executed) 发给source以计算出同步Binlog的起始位置。该集合记录了replica已经收到的或者是执行过的事务GTID。主节点可以借此判断slave执行到什么状态。注意为了保证最终的状态一致，replica的gtid_executed集合必须为主节点gtid_executed和正在执行事务GTID的子集。如果replica的gtid_executed包含一些source没有的gtid，为了能成功建立连接，可以设置source的gtid_purged全局变量来让source看起来更新，或者使用reset master命令重置replica的GTID状态。具体解决方式视情况而定。

## 产生

GTID的产生有2种，系统生成和用户自定义。

* 系统生成

在事务commit时，会为其生成GTID，对应函数generate_automatic_gtid，gtid的组成格式是server_uuid:gno，server_uuid可以通过show global variables like “%uuid%”查看，gno是顺序递增的数字，MySQL顺序给每个在提交的binlog事务分配gno，为了避免分配给两个binlog事务一样的gno，会将分配好的gtid会存到gitd_owend集合，直到事务提交，该gtid才从gitd_owend删除，并加入gtid_executed集合，若事务回滚，已经分配的gtid也会从gitd_owend集合删除并给分配给新的事务。

相关函数：generate_automatic_gtid、update_gtids_impl_own_gtid

* 用户指定

通过SET GTID_NEXT 语句，在事务开启前设定GTID。注意如果已经为该事务设定gtid，不要再次设定，相关函数set_gtid_next，使用demo如下：

`SET GTID_NEXT= 
BEGIN;
...
COMMIT;
`

* 不开gtid

如果不开启GTID，也会为每个Binlog事务申请一个anonymous gtid占位。

## 存储

### 内存

GTID在内存中主要以下面几个集合的形式存在：

* executed_gtids

记录所有已经执行过的binlog事务， 通过@@GLOBAL.gtid_executed查看该集合，该全局变量是只读的。

* lost_gtids

记录所有已被执行且不在Binlog中的事务，所以它是executed_gtids的子集。通过@@GLOBAL.gtid_purged查看该集合。Binlog中所有事务的GTID就是这两个集合的差集。 [GTID_SUBTRACT(@@GLOBAL.gtid_executed, @@GLOBAL.gtid_purged)](https://dev.mysql.com/doc/refman/8.0/en/gtid-functions.html#function_gtid-subtract)，注意它并不一定等于第一个Binlog文件的previous_gtids event记录的gtid，它包括了[三种情况](https://dev.mysql.com/doc/refman/8.0/en/replication-options-gtids.html#sysvar_gtid_purged)。

* owned_gtids

记录处于生成和提交过程之间的gtid（order commit的flush阶段和commit阶段之间），gtid生成时会和线程id绑定并写入该集合，提交时会从该集合删除，并写入gtid_executed集合。对应变量@@GLOBAL.GTID_OWNED

* previous_gtids_logged

记录最后一个Binlog中的previous GTIDs event的gtid set。

* gtids_only_in_table

记录不在binlog中，但在executed_gtids table中的gtid，具体是什么可以参考lost_gtids。

### Gtid_set

上面这5个集合都离不开Gtid_set类，它是gtid集合的内存数据结构。

该结构有三个重要的成员。

* Prealloced_array<Interval *, 8> m_intervals;

m_intervals的结构如图，是一个数组，每个slot挂了一个interval链表，每个interval存的是连续的gno区间。interval的结构如下，回想下gtid的gno，大家看到的xxxxxxxxx:1-20，这个1-20是这样存储的。前面的server_uuid通过sid_map存储，接下来会介绍。

` struct Interval {
 public:
 /// The first GNO of this interval.
 rpl_gno start;
 /// The first GNO after this interval.
 rpl_gno end;
 /// Return true iff this interval is equal to the given interval.
 bool equals(const Interval &other) const {
 return start == other.start && end == other.end;
 }
 /// Pointer to next interval in list.
 Interval *next;
 };
`

![img](.img/6246e4ea9244_1701406310347-0acaa448-5607-49d0-bf01-0d212fe2f20a.png)

* sid_map

记录server_uuid与sidno的映射关系，sid是server_uuid。sidno是interval所在m_intervals数组槽位下标+1。MySQL保存了一份全局的sid_map（global_sid_map），诸如executed_gtids等这些Gtid_set会直接共用global_sid_map，这样查找sid_map就能找到sidno，进而去各个Gtid_set的m_intervals数组中获取gno。

* Interval *free_intervals;

保存空闲interval的链表，每次删除m_intervals中的interval会加到其中，需要新的interval时也会从这里申请。

其他结构诸如Interval_iterator是遍历interval数组的迭代器，Interval_chunk用于在free_intervals不够用时，申请新的intervals空间。

### 持久化

​在MySQL5.7.5以前GTID不会持久化到表中，而是每次从Binlog构建，但是为了让有些情况也能用到gtid，例如slave没开binlog，或者master的binlog丢失。MySQL将gtid_executed集合持久化保存在gtid executed table中，其他gtid内存集合例如gtid_purged等不需要持久化，因为即使binlog丢了也能通过gtid_executed计算得到。

​可以理解gtid只存在2个地方，一个是gtid executed table，一个是Binlog中。其中gtid executed table反映了这个server从出生到现在所有在开启Binlog和gtid的情况下执行事务的gtid集合，通过RESET MASTER可以清理这个集合，同时也会清理Binlog和index文件，这个实例好像回到了开启Binlog前的状态。为了支持clone功能，mysql8.0.17将其持久化下推到innodb。使其可以脱离对Binlog的依赖，试想一下，如果下游通过复制上游的redo log也可以复制到gtid会发生什么。gtid反应了提交的Binlog事务，那么recover时是不是通过redo也能判断Binlog事务是否提交。

​下面介绍gtid executed table和Binlog中GTID的存储。

* Binlog

Binlog中的previous_gtids event记录了前一个Binlog的Previous_gtids event中的GTID set + 前一个Binlog中所有事务的GTID。依次递归，最后一个Binlog的Previous_gtids event记录了前面所有Binlog中的GTID，包括了已经被purge的Binlog。

* gtid executed table（8.0.17以前）

​事务提交时更新executed_gtids内存集合，在Binlog文件rotate和sever shutdown时将executed_gtids持久化到mysql.gtid_executed表(save_gtids_of_last_binlog_into_table)，server crash可能导致mysql.gtid_executed表不完整，所以sever初始化会扫描最后一个binlog的gtid，并在内存中构建executed_gtids结构并更新mysql.gtid_executed表。

* gtid executed table（8.0.17以后）

​在8.0.17，为了支持clone功能，事务gtid会写入InnoDB的undo日志中，同时维护了后台线程clone_gtid_thread，周期性持久化事务gtid到gtid_executed表。undo的purge也会受到该线程的制约，包含未持久化GTID的UNDO不会被purge。有了这个功能以后，在主备场景中，如果主的Binlog丢失，gtid_executed表又不全，备库依然能与主重新建立连接，因为对于Binlog的状态，只要能从主获取gtid_executed表和undo日志并构建出executed_gtids就能知道主当前的Binlog状态，进而能继续从主拉取Binlog。8.0.17以前使用xtrabackup重搭备库也需要将主的gtid_executed信息复制到备库以重新建立Binlog连接，但是遇到这种情况就束手无策了。

## 初始化

在master server启动时会初始化executed_gtids等这些集合。需从mysql.gtid_executed表中读取持久化的gtid与最后一个binlog中记录的gtid一起构建executed_gtids内存结构。注意在此之前会做Binlog和innodb的recover，删除未提交的Binlog事务并创建一个新的Binlog文件。最后一个Binlog不是指这个新的Binlog，而是指server crash时的最后一个Binlog文件。随后也会构建lost_gtids、previous_gtids_logged和gtids_only_in_table这些集合，最后会构建prev_gtids_ev并写入recover出的新binlog文件。

* server启动构建gtid

`mysqld_main(){
 read_gtid_executed_from_table();
 init_gtid_sets();
 build executed_gtids/gtids_only_in_table/lost_gtids/previous_gtids_logged;
 mysql_bin_log.write_event_to_binlog_and_sync(&prev_gtids_ev);
}
`

如果是8.0.17，会在innodb recovery的时候从undo中构建executed_gtids。详见函数trx_undo_gtid_read_and_persist。

## 参考

[MySQL · 引擎特性 · 基于GTID复制实现的工作原理](http://mysql.taobao.org/monthly/2020/05/09/)

[Global Transaction ID System Variables](https://dev.mysql.com/doc/refman/8.0/en/replication-options-gtids.html)

[GTID Format and Storage](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html)

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)