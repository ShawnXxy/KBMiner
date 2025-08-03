# 技术分享 | MySQL 一次奇怪的故障分析

**原文链接**: https://opensource.actionsky.com/20191014-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-14T00:37:00-08:00

---

**作者：****高鹏**文章末尾有他著作的《深入理解 MySQL 主从原理 32 讲》，深入透彻理解 MySQL 主从，GTID 相关技术知识。源码版本：5.7.22
水平有限，如有误请谅解
**一、问题来源**这是一个朋友问我的典型案例。整个故障现象表现为，MySQL 数据库频繁的出现大量的请求不能响应。下面是一些他提供的证据：
1. show processlist从状态信息来看出现如下情况：- insert 操作：状态为 update 
- update/delete 操作：状态为 updating
- select 操作：状态为 sending data
因此可以推断应该是语句执行期间出现了问题，由于篇幅原因只给出一部分，并且我将语句部分也做了相应截断：
- `show processlist----------------------------`
- `......`
- `11827639    root    dbmis   Execute 9   updating    UPDATE`
- `17224594    root    dbmis   Execute 8   Sending data    SELECT sum(exchange_coin) as exchange_coin FROM`
- `17224595    root    dbmis   Execute 8   update  INSERT INTO`
- `17224596    root    dg  Execute 8   update  INSERT INTO`
- `17224597    root    dbmis   Execute 8   update  INSERT INTO`
- `17224598    root    dbmis   Execute 7   update  INSERT INTO`
- `17224599    root    dbmis   Execute 7   Sending data    SELECT COUNT(*) AS tp_count FROM`
- `17224600    root    dg  Execute 7   update  INSERT INTO`
- `17224601    root    dbmis   Execute 6   update  INSERT INTO`
- `17224602    root    dbmis   Execute 6   Sending data    SELECT sum(exchange_coin) as exchange_coin FROM`
- `17224606    root    dbmis   Execute 5   update  INSERT INTO`
- `17224619    root    dbmis   Execute 2   update  INSERT INTO`
- `17224620    root    dbmis   Execute 2   update  INSERT INTO`
- `17224621    root    dbmis   Execute 2   Sending data    SELECT sum(exchange_coin) as exchange_coin`
- `17224622    root    dg  Execute 2   update  INSERT INTO`
- `17224623    root    dbmis   Execute 1   update  INSERT INTO`
- `17224624    root    dbmis   Execute 1   update  INSERT INTO`
- `17224625    root    dg  Execute 1   update  INSERT INTO`
- `17224626    root    dbmis   Execute 0   update  INSERT INTO`
2. 系统 IO/CPU从 vmstat 来看，CPU 使用不大，而 IO 也在可以接受的范围内（vmstat wa% 不高且 b 列为 0 ）如下：
- `vmstat--------------------------------------`
- `procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----`
- ` r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st`
- ` 2  0 927300 3057100      0 53487316    0    0     5   192    0    0  3  1 96  0  0`
- `iostat--------------------------------------`
- `Linux 3.10.0-693.el7.x86_64 (fang-data1)     09/23/2019  _x86_64_    (32 CPU)`
- 
- `avg-cpu:  %user   %nice %system %iowait  %steal   %idle`
- `           2.72    0.00    0.52    0.45    0.00   96.31`
- 
- `Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util`
- `sdb               9.73    11.28    3.93  264.54   415.23  2624.20    22.64     0.25    0.93    3.25    0.90   0.80  21.61`
- `sda              10.13    11.59    6.34  264.22   450.68  2624.20    22.73     0.01    0.05    2.55    1.00   0.93  25.19`
- `sdc              11.60    11.36    5.03  263.12   453.02  2592.44    22.71     0.17    0.62    5.08    0.53   0.81  21.60`
- `sde               0.01     0.10    0.11  160.45     6.69   920.23    11.55     0.16    1.01    1.80    1.01   0.83  13.32`
- `sdd              11.26    11.30    2.23  263.18   412.90  2592.44    22.65     0.17    0.65   10.37    0.56   0.82  21.78`
- `md126             0.00     0.00   11.30  468.80   164.79  5216.64    22.42     0.00    0.00    0.00    0.00   0.00   0.00`
- `dm-0              0.00     0.00    0.11   58.80     6.69   920.23    31.47     0.15    2.56    1.96    2.56   2.16  12.74`
- `dm-1              0.00     0.00    0.06    0.08     0.24     0.31     8.00     0.01   41.80    1.20   72.78   0.83   0.01`
- `dm-2              0.00     0.00   11.24  408.66   164.55  5216.33    25.63     0.14    0.32    1.02    0.30   0.46  19.29`
这就比较奇怪了，一般来说数据库不能及时响应请求很大可能是由于系统负载过高。如果说 DML 还可能是 Innodb 锁造成的堵塞，但是大量 sending data 状态下的 select 操作一般可能都和系统负载过高有联系，但是这里系统负载还在可以接受的范围内。
**二、pstack 分析**借助 pstack 查看线程的栈帧，查看 pstack 发现如下（由于篇幅限制只给出部分说明问题的部分）：
1. insert 线程：- `Thread 85 (Thread 0x7fbb0d42b700 (LWP 20174)):`
- `#0  0x00007fbfae164c73 in select () from /lib64/libc.so.6`
- `#1  0x0000000000987c0f in os_thread_sleep (tm=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/os/os0thread.cc:287`
- `#2  0x00000000009e4dea in srv_conc_enter_innodb_with_atomics (trx=trx@entry=0x7fba4802f9c8) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/srv/srv0conc.cc:276`
- `#3  srv_conc_enter_innodb (trx=trx@entry=0x7fba4802f9c8) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/srv/srv0conc.cc:511`
- `#4  0x000000000093b948 in innobase_srv_conc_enter_innodb (trx=0x7fba4802f9c8) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/handler/ha_innodb.cc:1280`
- `#5  ha_innobase::write_row (this=0x7fb8440ab260, record=0x7fb8440ab650 "") at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/handler/ha_innodb.cc:6793`
- `#6  0x00000000005b440f in handler::ha_write_row (this=0x7fb8440ab260, buf=0x7fb8440ab650 "") at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:7351`
- `#7  0x00000000006dd3a8 in write_record (thd=thd@entry=0x1d396c90, table=table@entry=0x7fb8440aa970, info=info@entry=0x7fbb0d429400, update=update@entry=0x7fbb0d429480) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_insert.cc:1667`
- `#8  0x00000000006e2541 in mysql_insert (thd=thd@entry=0x1d396c90, table_list=<optimized out>, fields=..., values_list=..., update_fields=..., update_values=..., duplic=DUP_REPLACE, ignore=false) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_insert.cc:1072`
- `#9  0x00000000006fa90a in mysql_execute_command (thd=thd@entry=0x1d396c90) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_parse.cc:3500`
2. update 线程
- `Thread 81 (Thread 0x7fbb24b67700 (LWP 27490)):`
- `#0  0x00007fbfae164c73 in select () from /lib64/libc.so.6`
- `#1  0x0000000000987c0f in os_thread_sleep (tm=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/os/os0thread.cc:287`
- `#2  0x00000000009e4dea in srv_conc_enter_innodb_with_atomics (trx=trx@entry=0x7fb94003c608) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/srv/srv0conc.cc:276`
- `#3  srv_conc_enter_innodb (trx=trx@entry=0x7fb94003c608) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/srv/srv0conc.cc:511`
- `#4  0x000000000093ae4e in innobase_srv_conc_enter_innodb (trx=0x7fb94003c608) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/handler/ha_innodb.cc:1280`
- `#5  ha_innobase::index_read (this=0x7fb95c05b540, buf=0x7fb95c2ae4f0 "\377\377\377", key_ptr=<optimized out>, key_len=<optimized out>, find_flag=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/handler/ha_innodb.cc:7675`
- `#6  0x00000000005ab6e0 in ha_index_read_map (find_flag=HA_READ_KEY_EXACT, keypart_map=3, key=0x7fb940017048 "7\307\017e\257h", buf=<optimized out>, this=0x7fb95c05b540) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:2753`
- `#7  handler::read_range_first (this=0x7fb95c05b540, start_key=<optimized out>, end_key=<optimized out>, eq_range_arg=<optimized out>, sorted=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:6717`
- `#8  0x00000000005aa206 in handler::multi_range_read_next (this=0x7fb95c05b540, range_info=0x7fbb24b65240) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:5871`
- `#9  0x0000000000804acb in QUICK_RANGE_SELECT::get_next (this=0x7fb94000f720) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/opt_range.cc:10644`
- `#10 0x000000000082ae2d in rr_quick (info=0x7fbb24b65410) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/records.cc:369`
- `#11 0x0000000000766e1b in mysql_update (thd=thd@entry=0x1d1f2250, table_list=<optimized out>, fields=..., values=..., conds=0x7fb9400009c8, order_num=``<optimized out>, order=<optimized out>, limit=18446744073709551615, handle_duplicates=DUP_ERROR, ignore=false, found_return=found_return@entry=0x7fbb24b65800, updated_return=updated_return@entry=0x7fbb24b65d60) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_update.cc:744`
3. select 线程
- `Thread 66 (Thread 0x7fbb3c355700 (LWP 16028)):`
- `#0  0x00007fbfae164c73 in select () from /lib64/libc.so.6`
- `#1  0x0000000000987c0f in os_thread_sleep (tm=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/os/os0thread.cc:287`
- `#2  0x00000000009e4dea in srv_conc_enter_innodb_with_atomics (trx=trx@entry=0x7fb988354858) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/srv/srv0conc.cc:276`
- `#3  srv_conc_enter_innodb (trx=trx@entry=0x7fb988354858) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/srv/srv0conc.cc:511`
- `#4  0x000000000093ae4e in innobase_srv_conc_enter_innodb (trx=0x7fb988354858) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/handler/ha_innodb.cc:1280`
- `#5  ha_innobase::index_read (this=0x7fb9880e33a0, buf=0x7fb988351b50 "\377\377\377\377", key_ptr=<optimized out>, key_len=<optimized out>, find_flag=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/storage/innobase/handler/ha_innodb.cc:7675`
- `#6  0x00000000005ab6e0 in ha_index_read_map (find_flag=HA_READ_AFTER_KEY, keypart_map=7, key=0x7fb988134a48 "", buf=<optimized out>, this=0x7fb9880e33a0) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:2753`
- `#7  handler::read_range_first (this=0x7fb9880e33a0, start_key=<optimized out>, end_key=<optimized out>, eq_range_arg=<optimized out>, sorted=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:6717`
- `#8  0x00000000005aa206 in handler::multi_range_read_next (this=0x7fb9880e33a0, range_info=0x7fbb3c353400) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/handler.cc:5871`
- `#9  0x0000000000804acb in QUICK_RANGE_SELECT::get_next (this=0x7fb988002050) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/opt_range.cc:10644`
- `#10 0x000000000082ae2d in rr_quick (info=0x7fb98809c210) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/records.cc:369`
- `#11 0x00000000006d44fd in sub_select (join=0x7fb98809a728, join_tab=0x7fb98809c180, end_of_records=<optimized out>) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_executor.cc:1259`
- `#12 0x00000000006d2823 in do_select (join=0x7fb98809a728) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_executor.cc:936`
- `#13 JOIN::exec (this=0x7fb98809a728) at /home/install/lnmp1.5/src/mysql-5.6.40/sql/sql_executor.cc:194`
好了有了这些栈帧视乎发现一些共同点他们都处于 innobase_srv_conc_enter_innodb 函数下，本函数正是下面参数实现的方式：- innodb_thread_concurrency
- innodb_concurrency_tickets
所以我随即告诉他检查这两个参数，如果设置了可以尝试取消。过后数据库故障得到解决。
**三、参数和相关说明**实际上涉及到的参数主要是 innodb_thread_concurrency 和 innodb_concurrency_tickets。将高压力下线程之间抢占 CPU 而造成线程上下文切换的情况尽量阻塞在 Innodb 层之外，这就需要 innodb_thread_concurrency 参数了。同时又要保证对于那些（长时间处理线程）不会长时间的堵塞（短时间处理线程），比如某些 select 操作需要查询很久，而某些 select 操作查询量很小，如果等待（长时间的 select 操作）结束后（短时间 select 操作）才执行，那么显然会出现（短时间 select 操作）饥饿问题，换句话说对（短时间 select 操作）是不公平的， 因此就引入了 innodb_concurrency_tickets 参数。
1. innodb_thread_concurrency同一时刻能够进入 Innodb 层的会话（线程）数。如果在 Innodb 层干活的会话（线程）数量超过这个参数的设置，新会话（线程）将不能从 MySQL 层进入到 Innodb 层，它们将进入一个短暂的睡眠状态。休眠多久则通过参数 innodb_thread_sleep_delay 参数指定，如果还设置了参数 innodb_adaptive_max_sleep_delay 那么 Innodb 将会自动调整休眠时间，具体的算法实际上就在 srv_conc_enter_innodb_with_atomics 函数中，感兴趣的可以执行查看。其次这种休眠实际上是一个定时醒来的时钟，通过 ::nanosleep 或者 select（多路 IO 转接函数）进行实现，定时唤醒后会话（线程）重新判断是否可以进入 Innodb 层。函数 os_thread_sleep 部分如下：
- `#elif defined(HAVE_NANOSLEEP)`
- `    struct timespec t;`
- 
- `    t.tv_sec = tm / 1000000;`
- `    t.tv_nsec = (tm % 1000000) * 1000;`
- 
- `    ::nanosleep(&t, NULL);`
- `#else`
- `    struct timeval  t;`
- 
- `    t.tv_sec = tm / 1000000;`
- `    t.tv_usec = tm % 1000000;`
- 
- `    select(0, NULL, NULL, NULL, &t);`
关于到底如何设置这个值，官方文档有如下建议：- `Use the following guidelines to help find and maintain an appropriate setting:`
- `- If the number of concurrent user threads for a workload is less than 64, set`
- `innodb_thread_concurrency=0.`
- `- If your workload is consistently heavy or occasionally spikes, start by setting`
- `innodb_thread_concurrency=128 and then lowering the value to 96, 80, 64, and so on, until`
- `you find the number of threads that provides the best performance. For example, suppose your`
- `system typically has 40 to 50 users, but periodically the number increases to 60, 70, or even 200.`
- `You find that performance is stable at 80 concurrent users but starts to show a regression above`
- `this number. In this case, you would set innodb_thread_concurrency=80 to avoid impacting`
- `performance.`
- `- If you do not want InnoDB to use more than a certain number of virtual CPUs for user threads`
- `(20 virtual CPUs, for example), set innodb_thread_concurrency to this number (or possibly`
- `lower, depending on performance results). If your goal is to isolate MySQL from other applications,`
- `you may consider binding the mysqld process exclusively to the virtual CPUs. Be aware,`
- `however, that exclusive binding could result in non-optimal hardware usage if the mysqld process`
- `is not consistently busy. In this case, you might bind the mysqld process to the virtual CPUs but`
- `also allow other applications to use some or all of the virtual CPUs.`
- `- innodb_thread_concurrency values that are too high can cause performance regression due`
- `to increased contention on system internals and resources.`
- `- In some cases, the optimal innodb_thread_concurrency setting can be smaller than the`
- `number of virtual CPUs.`
- `- Monitor and analyze your system regularly. Changes to workload, number of users, or computing`
- `environment may require that you adjust the innodb_thread_concurrency setting`
可以发现要合理的设置这个值并不那么容易并且要求较高。
2. innodb_concurrency_tickets实际上这里的 tickets 可以理解为 MySQL 层和 Innodb 层交互的次数，比如一个 select 一条数据就是需要 Innodb 层返回一条数据然后 MySQL 层进行 where 条件的过滤然后返回给客户端，抛开 where 条件过滤的情况，如果我们一条语句需要查询 100 条数据，那么实际上需要进入 Innodb 层 100 次，那么实际上消耗的 tickets 就是 100。当然对于 insert select 这种操作，需要的 tickets 是普通 select 的两倍，因为查询需要进入 Innodb 层一次，insert 需要再次进入 Innodb 层一次，后面我们就使用 insert select 的方式来模拟堵塞的情况，最后还会给出说明。这样我们也就理解为什么 innodb_concurrency_tickets 可以避免（长时间处理线程）长时间堵塞（短时间处理线程）的原因了。假设 innodb_concurrency_tickets 为 5000（默认值），有一个需要查询 100W 行数据的大 select 操作和一个需要查询 100 行数据的小 select 操作，大 select 操作先进行，但是当查询了 5000 行数据后将丢失CPU使用权，小 select 操作将会进行并且一次性完成。最后关于这里涉及的参数可以继续参考官方文档中的说明，我们线上并没有设置这些参数，因为感觉很难设置合适，如果设置不当反而会遇到问题，就如本案例一样。
3. 事务操作状态实际上如果是处于这种堵塞情况，我们完全可以在 information_schema.innodb_trx 和 show engine innodb status 中看到如下：
- `---TRANSACTION 162307, ACTIVE 133 sec sleeping before entering InnoDB （这里）`
- `mysql tables in use 2, locked 2`
- `767 lock struct(s), heap size 106968, 212591 row lock(s), undo log entries 15451`
- `MySQL thread id 14, OS thread handle 140736751912704, query id 1077 localhost root Sending data`
- `insert into testui select * from testui`
- `---TRANSACTION 162302, ACTIVE 320 sec, thread declared inside InnoDB 1`
- `mysql tables in use 2, locked 2`
- `2477 lock struct(s), heap size 336344, 609049 row lock(s), undo log entries 83582`
- `MySQL thread id 13, OS thread handle 140737153779456, query id 1050 localhost root Sending data`
- `insert into testti3 select * from testti3`
- 
- 
- `mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx \G`
- `*************************** 1. row ***************************`
- `                 trx_id: 84325`
- `              trx_state: RUNNING`
- `              trx_query: insert into  baguait4 select * from testgp`
- `    trx_operation_state: sleeping before entering InnoDB（这里）`
- `trx_concurrency_tickets: 0`
- `*************************** 2. row ***************************`
- `                 trx_id: 84319`
- `              trx_state: RUNNING`
- `              trx_query: insert into  baguait3 select * from testgp`
- `    trx_operation_state: sleeping before entering InnoDB`
- `trx_concurrency_tickets: 0`
我们可以看到事务操作状态被标记为 sleeping before entering InnoDB 。但是需要注意一点的是对于只读事务比如 select 操作而言，show engine innodb status 可能看不到。但是遗憾的是案例中朋友并没有采集 trx_operation_state 的值。
**四、模拟测试**这里我们简单模拟，我们一共启用3个事务，其中两个 insert select 操作，一个单纯的 select 操作，当然这里的都是耗时操作，涉及的表每个表都有大概 100W 的数据。
同时为了方便观察我们需要设置参数：
- innodb_thread_concurrency=1
- innodb_concurrency_tickets=10
操作步骤如下：
![](https://opensource.actionsky.com/wp-content/uploads/2019/10/表格2-1024x366.png)											
如果多观察几次你可以看到如下的现象：
- `mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx \G show processlist;`
- `*************************** 1. row ***************************`
- `                 trx_id: 84529`
- `              trx_state: RUNNING`
- `              trx_query: insert into  baguait4 select * from testgp`
- `    trx_operation_state: sleeping before entering InnoDB`
- `trx_concurrency_tickets: 0`
- `*************************** 2. row ***************************`
- `                 trx_id: 84524`
- `              trx_state: RUNNING`
- `              trx_query: insert into  baguait3 select * from testgp`
- `    trx_operation_state: inserting`
- `trx_concurrency_tickets: 1`
- `*************************** 3. row ***************************`
- `                 trx_id: 422211785606640`
- `              trx_state: RUNNING`
- `              trx_query: select * from baguait1`
- `    trx_operation_state: sleeping before entering InnoDB`
- `trx_concurrency_tickets: 0`
- `3 rows in set (0.00 sec)`
- 
- `+----+-----------------+-----------+---------+---------+------+------------------------+--------------------------------------------+-----------+---------------+`
- `| Id | User            | Host      | db      | Command | Time | State                  | Info                                       | Rows_sent | Rows_examined |`
- `+----+-----------------+-----------+---------+---------+------+------------------------+--------------------------------------------+-----------+---------------+`
- `|  1 | event_scheduler | localhost | NULL    | Daemon  | 3173 | Waiting on empty queue | NULL                                       |         0 |             0 |`
- `|  6 | root            | localhost | testmts | Query   |   70 | Sending data           | insert into  baguait3 select * from testgp |         0 |             0 |`
- `|  7 | root            | localhost | testmts | Query   |   68 | Sending data           | insert into  baguait4 select * from testgp |         0 |             0 |`
- `|  8 | root            | localhost | testmts | Query   |   66 | Sending data           | select * from baguait1                     |    120835 |             0 |`
- `|  9 | root            | localhost | NULL    | Query   |    0 | starting               | show processlist                           |         0 |             0 |`
- `+----+-----------------+-----------+---------+---------+------+------------------------+--------------------------------------------+-----------+---------------+`
- `5 rows in set (0.00 sec)`
- 
- `mysql>`
- `mysql>`
- `mysql>`
- `mysql>`
- `mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx \G show processlist;`
- `*************************** 1. row ***************************`
- `                 trx_id: 84529`
- `              trx_state: RUNNING`
- `              trx_query: insert into  baguait4 select * from testgp`
- `    trx_operation_state: sleeping before entering InnoDB`
- `trx_concurrency_tickets: 0`
- `*************************** 2. row ***************************`
- `                 trx_id: 84524`
- `              trx_state: RUNNING`
- `              trx_query: insert into  baguait3 select * from testgp`
- `    trx_operation_state: sleeping before entering InnoDB`
- `trx_concurrency_tickets: 0`
- `*************************** 3. row ***************************`
- `                 trx_id: 422211785606640`
- `              trx_state: RUNNING`
- `              trx_query: select * from baguait1`
- `    trx_operation_state: fetching rows`
- `trx_concurrency_tickets: 3`
- `3 rows in set (0.00 sec)`
- 
- `+----+-----------------+-----------+---------+---------+------+------------------------+--------------------------------------------+-----------+---------------+`
- `| Id | User            | Host      | db      | Command | Time | State                  | Info                                       | Rows_sent | Rows_examined |`
- `+----+-----------------+-----------+---------+---------+------+------------------------+--------------------------------------------+-----------+---------------+`
- `|  1 | event_scheduler | localhost | NULL    | Daemon  | 3177 | Waiting on empty queue | NULL                                       |         0 |             0 |`
- `|  6 | root            | localhost | testmts | Query   |   74 | Sending data           | insert into  baguait3 select * from testgp |         0 |             0 |`
- `|  7 | root            | localhost | testmts | Query   |   72 | Sending data           | insert into  baguait4 select * from testgp |         0 |             0 |`
- `|  8 | root            | localhost | testmts | Query   |   70 | Sending data           | select * from baguait1                     |    128718 |             0 |`
- `|  9 | root            | localhost | NULL    | Query   |    0 | starting               | show processlist                           |         0 |             0 |`
- `+----+-----------------+-----------+---------+---------+------+------------------------+--------------------------------------------+-----------+---------------+`
- `5 rows in set (0.00 sec)`
我们可以观察到 trx_operation_state 的状态 3 个操作都在交替的变化，但是总有 2 个处于sleeping before entering InnoDB 状态。并且我们可以观察到 trx_concurrency_tickets 总是不会大于 10 的。因此我们有理由相信在同一时刻只有一个操作进入了 Innodb 层。但是需要注意的是在 show engine innodb status 中观察不到 select 的操作如下：- `------------`
- `TRANSACTIONS`
- `------------`
- `Trx id counter 84538`
- `Purge done for trx's n:o < 84526 undo n:o < 0 state: running but idle`
- `History list length 356`
- `Total number of lock structs in row lock hash table 0`
- `LIST OF TRANSACTIONS FOR EACH SESSION:`
- `---TRANSACTION 422211785609424, not started`
- `0 lock struct(s), heap size 1160, 0 row lock(s)`
- `---TRANSACTION 422211785608032, not started`
- `0 lock struct(s), heap size 1160, 0 row lock(s)`
- `---TRANSACTION 84529, ACTIVE 103 sec inserting, thread declared inside InnoDB 6`
- `mysql tables in use 2, locked 1`
- `1 lock struct(s), heap size 1160, 0 row lock(s), undo log entries 111866`
- `MySQL thread id 7, OS thread handle 140737158833920, query id 80 localhost root Sending data`
- `insert into  baguait4 select * from testgp`
- `Trx read view will not see trx with id >= 84529, sees < 84524`
- `---TRANSACTION 84524, ACTIVE 105 sec sleeping before entering InnoDB`
- `mysql tables in use 2, locked 1`
- `1 lock struct(s), heap size 1160, 0 row lock(s), undo log entries 105605`
- `MySQL thread id 6, OS thread handle 140737159034624, query id 79 localhost root Sending data`
- `insert into  baguait3 select * from testgp`
- `Trx read view will not see trx with id >= 84524, sees < 84524`
但是我们还需要注意 show engine innodb status 有如下输出第一行说明了有 2 个会话（线程）堵塞在 Innodb 层以外。- `--------------`
- `ROW OPERATIONS`
- `--------------`
- `1 queries inside InnoDB, 2 queries in queue`
- `3 read views open inside InnoDB`
- `2 RW transactions active inside InnoDB`
**五、实现方法**前面我们已经描述了每次 MySQL 层和 Innodb 层的交互都会进行一次这样的判断，它用来决定会话（线程）是否能够进入 Innodb 层，下面就是大概的逻辑，由函数 innobase_srv_conc_enter_innodb 调入。- `->是否设置了参数innodb_thread_concurrency`
- `  ->是`
- `     ->是否tickets大于0`
- `        ->是、直接进入Innodb层并且tickets减1`
- `        ->否、调入函数srv_conc_enter_innodb`
- `           ->调入函数srv_conc_enter_innodb_with_atomics`
- `              ->开启死循环`
- `                 ->是否活跃线程数小于innodb_thread_concurrency设置`
- `                    ->是、增加活跃线程数，并且自动调整delay参数，退出死循环，满tickets进入Innodb层`
- `                    ->否、自动调整delay参数后设置事务操作状态为"sleeping before entering InnoDB"，然后进入休眠状态直到时间达到后重新醒来继续循环`
- `  ->否、直接进入Innodb层`
我们可以看到这个实现方式，在 Inndob 以外的会话（线程）会一直等待直到 Inndob 层内活跃的线程数小于 innodb_thread_concurrency 为止，并且每次进入 Innodb 层都会将 tickets 减 1。
**其他：关于 insert select 操作消耗 tickets 的说明**这里额外说明一下，因为我在测试的时候看了一下，对于一行数据而言首先需要 select 查询出来然后再 insert 插入到表中，这里实际上一行数据涉及到进入 Innodb 层两次，那么就需要消耗 2 个 tickets，下面留下两个栈帧供自己后面参考：
1. insert select 查询数据进入 Innodb 层
- `#0  innobase_srv_conc_enter_innodb (prebuilt=0x7ffedcb98d10) at /mysqldata/percona-server-locks-detail-5.7.22/storage/innobase/handler/ha_innodb.cc:1740`
- `#1  0x0000000001a53f7c in ha_innobase::general_fetch (this=0x7ffedcb9d760, buf=0x7ffedc9469b0 "\375\n", direction=1, match_mode=0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/storage/innobase/handler/ha_innodb.cc:9846`
- `#2  0x0000000001a545ee in ha_innobase::rnd_next (this=0x7ffedcb9d760, buf=0x7ffedc9469b0 "\375\n")`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/storage/innobase/handler/ha_innodb.cc:10083`
- `#3  0x0000000000f836d6 in handler::ha_rnd_next (this=0x7ffedcb9d760, buf=0x7ffedc9469b0 "\375\n") at /mysqldata/percona-server-locks-detail-5.7.22/sql/handler.cc:3146`
- `#4  0x00000000014e2a55 in rr_sequential (info=0x7ffedcb4f120) at /mysqldata/percona-server-locks-detail-5.7.22/sql/records.cc:521`
- `#5  0x0000000001581277 in sub_select (join=0x7ffedcb4ea20, qep_tab=0x7ffedcb4f0d0, end_of_records=false)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:1280`
- `#6  0x0000000001580be6 in do_select (join=0x7ffedcb4ea20) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:950`
- `#7  0x000000000157eaa2 in JOIN::exec (this=0x7ffedcb4ea20) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:199`
- `#8  0x0000000001620327 in handle_query (thd=0x7ffedc012960, lex=0x7ffedc014f90, result=0x7ffedcc46680, added_options=1342177280, removed_options=0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_select.cc:185`
- `#9  0x000000000180466d in Sql_cmd_insert_select::execute (this=0x7ffedcc46608, thd=0x7ffedc012960)`
2. insert select 插入数据进入 Innodb 层
- `#0  innobase_srv_conc_enter_innodb (prebuilt=0x7ffedcb9c6f0) at /mysqldata/percona-server-locks-detail-5.7.22/storage/innobase/handler/ha_innodb.cc:1740`
- `#1  0x0000000001a50587 in ha_innobase::write_row (this=0x7ffedc946470, record=0x7ffedcb78d00 "\375\n")`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/storage/innobase/handler/ha_innodb.cc:8341`
- `#2  0x0000000000f9041d in handler::ha_write_row (this=0x7ffedc946470, buf=0x7ffedcb78d00 "\375\n") at /mysqldata/percona-server-locks-detail-5.7.22/sql/handler.cc:8466`
- `#3  0x00000000018004b9 in write_record (thd=0x7ffedc012960, table=0x7ffedcb8f940, info=0x7ffedcc466c8, update=0x7ffedcc46740)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_insert.cc:1881`
- `#4  0x00000000018019b9 in Query_result_insert::send_data (this=0x7ffedcc46680, values=...) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_insert.cc:2279`
- `#5  0x00000000015853a8 in end_send (join=0x7ffedcb4ea20, qep_tab=0x7ffedcb4f248, end_of_records=false)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:2925`
- `#6  0x0000000001581f71 in evaluate_join_record (join=0x7ffedcb4ea20, qep_tab=0x7ffedcb4f0d0) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:1645`
- `#7  0x0000000001581372 in sub_select (join=0x7ffedcb4ea20, qep_tab=0x7ffedcb4f0d0, end_of_records=false)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:1297`
- `#8  0x0000000001580be6 in do_select (join=0x7ffedcb4ea20) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:950`
- `#9  0x000000000157eaa2 in JOIN::exec (this=0x7ffedcb4ea20) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:199`
- `#10 0x0000000001620327 in handle_query (thd=0x7ffedc012960, lex=0x7ffedc014f90, result=0x7ffedcc46680, added_options=1342177280, removed_options=0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_select.cc:185`
- `#11 0x000000000180466d in Sql_cmd_insert_select::execute (this=0x7ffedcc46608, thd=0x7ffedc012960)`
实际上插入数据正是在查询完数据后调用函数 evaluate_join_record 的时候，通过回调了函数 Query_result_insert::send_data 来实现，这点和单纯的 select 不一样单纯的 select 这里调入是函数 Query_result_send::send_data 如下：- `#0  Query_result_send::send_data (this=0x7ffedcc465f8, items=...) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_class.cc:2915`
- `#1  0x00000000015853a8 in end_send (join=0x7ffedcb4e930, qep_tab=0x7ffedcb4f4b0, end_of_records=false)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:2925`
- `#2  0x0000000001581f71 in evaluate_join_record (join=0x7ffedcb4e930, qep_tab=0x7ffedcb4f338) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:1645`
- `#3  0x0000000001581372 in sub_select (join=0x7ffedcb4e930, qep_tab=0x7ffedcb4f338, end_of_records=false)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:1297`
- `#4  0x0000000001580be6 in do_select (join=0x7ffedcb4e930) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:950`
- `#5  0x000000000157eaa2 in JOIN::exec (this=0x7ffedcb4e930) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_executor.cc:199`
- `#6  0x0000000001620327 in handle_query (thd=0x7ffedc012960, lex=0x7ffedc014f90, result=0x7ffedcc465f8, added_options=0, removed_options=0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_select.cc:185`
- `#7  0x00000000015d1f77 in execute_sqlcom_select (thd=0x7ffedc012960, all_tables=0x7ffedcc45cf0) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:5445`
最后推荐高鹏的专栏《深入理解 MySQL 主从原理 32 讲》，想要透彻了解学习 MySQL 主从原理的朋友不容错过。
作者微信：gp_22389860
![](.img/0aff2ace.jpg)											
**社区近期动态**
**No.1**
**10.26 DBLE 用户见面会 北京站**
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/默认标题_横版海报_2019.09.16.jpg)											
爱可生开源社区将在 2019 年 10 月 26 日迎来在北京的首场 DBLE 用户见面会，以线下**互动分享**的会议形式跟大家见面。
时间：10月26日 9:00 &#8211; 12:00 AM
地点：HomeCafe 上地店（北京市海淀区上地二街一号龙泉湖酒店对面）
重要提醒：
1. 同日下午还有 dbaplus 社群举办的沙龙：聚焦数据中台、数据架构与优化。
2. 爱可生开源社区会在每年10.24日开源一款高质量产品。本次在 dbaplus 沙龙会议上，爱可生的资深研发工程师闫阿龙，将为大家带来《金融分布式事务实践及txle概述》，并在现场开源。
**No.2**
**「3306π」成都站 Meetup**
知数堂将在 2019 年 10 月 26 日在成都举办线下会议，本次会议中邀请了五位数据库领域的资深研发/DBA进行主题分享。
时间：2019年10月26日 13:00-18:00
地点：成都市高新区天府三街198号腾讯成都大厦A座多功能厅
**No.3**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
- 技术交流群，进群后可提问
QQ群（669663113）
- 社区通道，邮件&电话
osc@actionsky.com
- 现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.4**
**社区技术内容征稿**
征稿内容：
- 格式：.md/.doc/.txt
- 主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
- 要求：原创且未发布过
- 奖励：作者署名；200元京东E卡+社区周边
投稿方式：
- 邮箱：osc@actionsky.com
- 格式：[投稿]姓名+文章标题
- 以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系