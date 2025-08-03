# MySQL · 参数故事 · timed_mutexes

**Date:** 2014/08
**Source:** http://mysql.taobao.org/monthly/2014/08/01/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2014 / 08
 ](/monthly/2014/08)

 * 当期文章

 MySQL · 参数故事 · timed_mutexes
* MySQL · 参数故事 · innodb_flush_log_at_trx_commit
* MySQL · 捉虫动态 · Count(Distinct) ERROR
* MySQL · 捉虫动态 · mysqldump BUFFER OVERFLOW
* MySQL · 捉虫动态 · long semaphore waits
* MariaDB · 分支特性 · 支持大于16K的InnoDB Page Size
* MariaDB · 分支特性 · FusionIO特性支持
* TokuDB · 性能优化 · Bulk Fetch
* TokuDB · 数据结构 · Fractal-Trees与LSM-Trees对比
* TokuDB·社区八卦·TokuDB团队

 ## MySQL · 参数故事 · timed_mutexes 
 Author: 

 **提要**

MySQL 5.5.39 Release版本正式从源码里删除了全局参数timed_mutexes。timed_mutexes原本用来控制是否对Innodb引擎的mutex wait进行计时统计，以方便进行性能诊断。为什么要删除这个参数呢？ 下面介绍下相关背景：

**Innodb的同步锁机制**

Innodb封装了mutex和rw_lock结构来保护内存的变量和结构,进行多线程同步，考虑可移植性， mutex使用lock_word或者OS mutex来保证原子操作，并使用event条件变量进行阻塞和唤醒操作。

`os_event_t event;
volatile lock_word_t lock_word;
os_fast_mutex_t os_fast_mutex;
`

**Innodb同步锁引入的数据结构和开销**

1. 全局mutex链表

Innodb引入了一个全局的链表ut_list_base_node_t mutex_list，并使用一个单独的mutex来保护链表。 所有的mutex在create或者free的时候来修改链表，有了全局链表，也使统计汇总有了可能性，参考命令“show engine innodb mutex”. 虽然需要维护一个全局的链表，但这并不会影响太多的性能，因为大部分的mutex的生命周期都是从Innodb启动一直到shutdown。

1. 统计信息

mutex的结构中，有几个统计信息：

`count_os_wait：请求mutex进入等待的次数
count_using: 请求mutex的次数
count_spin_loop: 请求mutex时spin的轮数
count_spin_rounds: 请求mutex的spin次数
count_os_yield:请求mutex spin失败后os等待次数
lspent_time: 统计等待mutex的时间
`
lock mutex的主要步骤：

1. 首先trylock mutex，如果没有获取到mutex，并不马上进行wait，而是进行spin。
2. 尝试spin，如果在SYNC_SPIN_ROUNDS次后，仍然没有lock，那么就进入等待队列，等待唤醒。
在MySQL5.5的版本里，非UNIV_DEBUG模式下，Innodb仅仅保留了count_os_wait的次数，这也是为了性能的考虑。所以5.5的版本后， timed_mutexes在Release下，其实已经不再起作用，所以5.5.39，以及5.6以后，源码里都不再保留timed_mutexes。 要么在debug模式下，启用这些统计，但上线版本又不可能使用DEBUG模式，所以对于mutex的统计，MySQL在后面的版本中使用了performance_schema的等待事件来代替，即:

`mysql> SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
-> WHERE TABLE_SCHEMA = 'performance_schema'
-> AND TABLE_NAME LIKE '%instances';
+------------------+
| TABLE_NAME |
+------------------+
| cond_instances |
| file_instances |
| mutex_instances |
| rwlock_instances |
+------------------+
`

1. 全局等待队列

Innodb为所有的等待状态的线程准备了一个队列，如果获取mutex失败，那么就申请一个cell，进入阻塞状态，等待signal。 sync_primary_wait_array，有了这个全局的队列，Innodb就可以对这些wait的线程进行统计，比如long semaphore waits就是根据这个队列进行的查询。

1. signal丢失

这里再讨论下signal丢失的情况，我们重新再看下lock mutex的步骤：

`线程1：
1. try lock mutex
2. fail，然后spin
3. fail，然后进入队列，然后wait event
线程2：
1.own mutex
2.free mutex
3.signal event
`
如果按照这个时序，在线程2 signal event后，线程1才进入队列，那么线程1就永远处在阻塞状态，无法唤醒。为了解决signal丢失的情况， Innodb启动了一个后台线程：sync_arr_wake_threads_if_sema_free，每隔1s就轮询wait数组，如果可以lock，就signal这个event来唤醒线程。

从上面来看，Innodb为了mutex和rwlock的移植性，以及为了监控和诊断，添加了多个全局的数据结构，这样实时的统计才有可能，但也带来了维护数据结构的开销。 而timed_mutexes控制的mutex wait时间统计，因为只在debug模式下进行编译，而且5.6以后使用performance schema的等待事件进行替代，所以参数做了删除处理。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)