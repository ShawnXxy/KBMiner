# 技术分享 | MySQL 突如其来的主从复制延迟

**原文链接**: https://opensource.actionsky.com/20211021-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-10-21T22:28:30-08:00

---

作者：刘开洋
爱可生交付服务团队北京 DBA，对数据库及周边技术有浓厚的学习兴趣，喜欢看书，追求技术。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
前几天来自生产上的一个问题，又涨知识了，今天拿来分享给大家。
## 现象与分析
现象是监控显示主从出现延迟，那我们就得登上数据库看看究竟出现了什么事？
`[root@localhost][(none)]> show slave status\G
*************************** 1. row ***************************
Slave_IO_State: Waiting for master to send event
Master_Host: 10.196.131.152
Master_User: universe_op
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.002805
Read_Master_Log_Pos: 929207906
Relay_Log_File: mysql-relay-bin.007053
Relay_Log_Pos: 588591867
Relay_Master_Log_File: mysql-bin.002805
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
Replicate_Do_DB:
Replicate_Ignore_DB:
Replicate_Do_Table:
Replicate_Ignore_Table:
Replicate_Wild_Do_Table:
Replicate_Wild_Ignore_Table:
Last_Errno: 0
Last_Error:
Skip_Counter: 0
Exec_Master_Log_Pos: 588591694
Relay_Log_Space: 929208373
Until_Condition: None
Until_Log_File:
Until_Log_Pos: 0
Master_SSL_Allowed: No
Master_SSL_CA_File:
Master_SSL_CA_Path:
Master_SSL_Cert:
Master_SSL_Cipher:
Master_SSL_Key:
Seconds_Behind_Master: 808           // 与主之间存在着808s的延迟，并且延迟还在增加
Master_SSL_Verify_Server_Cert: No
Last_IO_Errno: 0
Last_IO_Error:
Last_SQL_Errno: 0
Last_SQL_Error:
Replicate_Ignore_Server_Ids:
Master_Server_Id: 685734686
Master_UUID: 85d68147-e6a2-11ea-944a-0050568e99a5
Master_Info_File: mysql.slave_master_info
SQL_Delay: 0
SQL_Remaining_Delay: NULL
Slave_SQL_Running_State: Waiting for dependent transaction to commit
Master_Retry_Count: 1
Master_Bind:
Last_IO_Error_Timestamp:
Last_SQL_Error_Timestamp:
Master_SSL_Crl:
Master_SSL_Crlpath:
Retrieved_Gtid_Set: 85d68147-e6a2-11ea-944a-0050568e99a5:901602108-1056122204      // 收到的Gtid在增长，binlog dump Gtid线程正努力工作
Executed_Gtid_Set: 452dfe36-6508-11e9-85e2-00505694c5db:1-51354589,       // gtid一直在增大，说明从库持续在回放主库binlog，排除锁等待的情况
85d68147-e6a2-11ea-944a-0050568e99a5:1-1056051538
Auto_Position: 1
Replicate_Rewrite_DB:
Channel_Name:
Master_TLS_Version:
1 row in set (0.00 sec)
// 在processlist中也能看到并发线程长时间Waiting for an event from Coordinator的现象
[root@localhost][(none)]> show processlist;
+--------+-------------+----------------------+------+-----------------+---------+---------------------------------------------------------------+------------------+
| Id     | User        | Host                 | db   | Command         | Time    | State                                                         | Info             |
+--------+-------------+----------------------+------+-----------------+---------+---------------------------------------------------------------+------------------+
|      1 | system user |                      | NULL | Connect         | 3459230 | Waiting for master to send event                              | NULL             |
|      2 | system user |                      | NULL | Connect         |       0 | Waiting for dependent transaction to commit                   | NULL             |
|      3 | system user |                      | NULL | Connect         |     811 | Waiting for an event from Coordinator                         | NULL             |
|      4 | system user |                      | NULL | Connect         |     811 | Executing event                                               | NULL             |
|      5 | system user |                      | NULL | Connect         |     812 | Waiting for an event from Coordinator                         | NULL             |
|      6 | system user |                      | NULL | Connect         |     813 | Waiting for an event from Coordinator                         | NULL             |
|      7 | system user |                      | NULL | Connect         |     813 | Waiting for an event from Coordinator                         | NULL             |
|      8 | system user |                      | NULL | Connect         |     817 | Waiting for an event from Coordinator                         | NULL             |
|      9 | system user |                      | NULL | Connect         |     817 | Waiting for an event from Coordinator                         | NULL             |
|     10 | system user |                      | NULL | Connect         |     819 | Waiting for an event from Coordinator                         | NULL             |
| 705000 | zabbix_user | 10.195.129.195:27258 | NULL | Sleep           |       0 |                                                               | NULL             |
| 705003 | zabbix_user | 10.195.129.195:27286 | NULL | Binlog Dump Gtid|  141604 | Master has sent all binlog to slave; waiting for more updates | NULL             |
| 735026 | root        | localhost            | NULL | Query           |       0 | starting                                                      | show processlist |
+--------+-------------+----------------------+------+-----------------+---------+---------------------------------------------------------------+------------------+
25 rows in set (0.00 sec) 
// 看看innodb存储引擎层整体的输出
[root@localhost][(none)]> show engine innodb status\G
*************************** 1. row ***************************
Type: InnoDB
Name:
Status:
=====================================
2021-09-26 10:58:26 0x7f7964b63700 INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 3 seconds       // 过去3s内的计算数值
-----------------
BACKGROUND THREAD
-----------------
srv_master_thread loops: 3451511 srv_active, 0 srv_shutdown, 37 srv_idle
srv_master_thread log flush and writes: 3451269
----------
SEMAPHORES      // 通过下面的信号量说明事件计数器和当前等待线程的列表很高，waits很高，存在很高的工作负载。
----------
OS WAIT ARRAY INFO: reservation count 1997792220
OS WAIT ARRAY INFO: signal count 2815399081
RW-shared spins 0, rounds 2610682598, OS waits 181278068
RW-excl spins 0, rounds 93825427645, OS waits 1036416294   // 读写的锁计数器wait数量很高
RW-sx spins 1902710329, rounds 36619607564, OS waits 565415695
Spin rounds per wait: 2610682598.00 RW-shared, 93825427645.00 RW-excl, 19.25 RW-sx
······
`
之后我们来到操作系统层面看看能找到哪些蛛丝马迹。首先是 IO ，此时回顾之前的现象是从库执行的 Gtid 一直在涨，那此时是否有很高的 IO 写入呢？
`cn0013vm3813:~ # iostat -x 1
Linux 4.12.14-122.12-default (cn0013vm3813)     09/26/21        _x86_64_        (8 CPU)
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
5.51    0.00    6.77    4.64    0.00   83.08
Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
sdb             38.00 7235.00    316.00 249236.00     0.00   247.00   0.00   3.30    0.84    0.03  10.40     8.32    34.45   0.09  65.60
dm-0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
dm-1             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
dm-2             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
dm-3            37.00 7937.00    300.00 256372.00     0.00     0.00   0.00   0.00    1.84    1.36  10.87     8.11    32.30   0.08  64.40
dm-4             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
dm-5             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
dm-6             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
dm-7             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
sdc              0.00  398.00      0.00   6764.00     0.00    31.00   0.00   7.23    0.00    0.00   0.38     0.00    16.99   0.23   9.20
^C
cn0013vm3813:~ # top -p `pgrep mysqld`
top - 10:51:17 up 119 days,  6:39,  2 users,  load average: 2.05, 2.13, 2.35
Tasks: 251 total,   1 running, 250 sleeping,   0 stopped,   0 zombie
%Cpu(s): 17.3 us,  3.5 sy,  0.0 ni, 71.2 id,  6.8 wa,  0.0 hi,  1.3 si,  0.0 st
KiB Mem:  32742352 total, 32498472 used,   243880 free,   565520 buffers
KiB Swap:        0 total,        0 used,        0 free. 11892264 cached Mem
PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND                                                                                
5387 mysql     20   0 20.712g 0.017t  14000 S 166.4 56.59  24781:43 mysqld           
// sar、lsof 和 pidstat 均可以辅助诊断出现的问题
`
在 iostat 的输出和 top 定位中，确实存在很高的磁盘 IO ，正好对应数据库挂载的 Device ，说明此时存在很高的 MySQL 数据变更操作，但是还没达到瓶颈。
MySQL 出问题我们肯定是要去错误日志中看看有什么现象的，遇到问题翻日志肯定有意想不到的收获（建议参数 log-error-verbosity=3 ）：
`cn0013vm3813:/MYSQL/mdata/mysql_data # tail -f error.log
2021-09-26T11:10:44.341226+08:00 [Note] InnoDB: page_cleaner: 1000ms intended loop took 4504ms. The settings might not be optimal. (flushed=2006 and evicted=0, during the time.)
2021-09-26T11:10:49.450563+08:00 2 [Note] Multi-threaded slave statistics for channel '': seconds elapsed = 124; events assigned = 996024321; worker queues filled over overrun level = 3325; waited due a Worker queue full = 2; waited due the total size = 7479; waited at clock conflicts = 1074002060535300 waited (count) when Workers occupied = 603501 waited when Workers occupied = 1094588543400
2021-09-26T11:11:14.474659+08:00 0 [Note] InnoDB: page_cleaner: 1000ms intended loop took 4160ms. The settings might not be optimal. (flushed=2005 and evicted=0, during the time.)
2021-09-26T11:11:44.281841+08:00 735819 [Note] Got an error reading communication packets
2021-09-26T11:12:14.456899+08:00 735823 [Note] Got an error reading communication packets
2021-09-26T11:12:14.644479+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7481 times hitting slave_pending_jobs_size_max; current event size = 40906.
2021-09-26T11:12:14.797567+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7491 times hitting slave_pending_jobs_size_max; current event size = 40912.
2021-09-26T11:12:14.985773+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7501 times hitting slave_pending_jobs_size_max; current event size = 40916.
2021-09-26T11:12:15.145043+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7511 times hitting slave_pending_jobs_size_max; current event size = 40907.
2021-09-26T11:12:15.351211+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7521 times hitting slave_pending_jobs_size_max; current event size = 40897.
2021-09-26T11:12:15.827309+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7531 times hitting slave_pending_jobs_size_max; current event size = 40917.
2021-09-26T11:12:16.066707+08:00 2 [Note] Multi-threaded slave: Coordinator has waited 7541 times hitting slave_pending_jobs_size_max; current event size = 40910.
`
## 定位与结论
- 
在 page_cleaner 线程出现的一刻（ page_cleaner 线程每秒刷新一次，此时刷新了2005个页面，耗费了4.504s），我们就明白，此时脏页很多，刷脏线程全力刷脏，也从侧面说明了写入很高，从库压力大，硬件无法跟上配置的运行速率，因此需要降低 innodb_io_capacity_max 值；
- 
从 Multi-threaded 出现信息输出进一步说明从库的SQL并行复制压力较大，可以适当增加并行线程数量以降低工作队列满而导致的等待；
- 
MySQL error 日志在 MTS复制中出现了一个参数名 slave_pending_jobs_size_max，表示 Coordinator 在等了7000多次之后达到了 slave_pending_jobs_size_max 的最大值，这里也说明 MySQL 单条 SQL 很长，延长了 worker 线程的读取速度，去看看从库的 slave_pending_jobs_size_max 值。
`[root@localhost][(none)]> show variables like '%slave_pending_jobs_size_max%';
+-----------------------------+----------+
| Variable_name               | Value    |
+-----------------------------+----------+
| slave_pending_jobs_size_max | 16777216 |  = 16M
+-----------------------------+----------+
1 row in set (0.00 sec)
// 而此时主库的最大允许发送的数据包大小
[root@localhost][(none)]> show variables like 'max_allowed_packet';
+--------------------+------------+
| Variable_name      | Value      |
+--------------------+------------+
| max_allowed_packet | 1073741824 |  = 1G
+--------------------+------------+
1 row in set (0.00 sec)
`
下面是这两个参数导致主从延迟的官方解释：https://dev.mysql.com/doc/refman/5.7/en/replication-features-max-allowed-packet.html
> 
On a multi-threaded replica (slave_parallel_workers > 0), ensure that the system variable slave_pending_jobs_size_max is set to a value equal to or greater than the setting for the max_allowed_packet system variable on the source. The default setting for slave_pending_jobs_size_max, 128M, is twice the default setting for max_allowed_packet, which is 64M. max_allowed_packet limits the packet size that the source can send, but the addition of an event header can produce a binary log event exceeding this size. Also, in row-based replication, a single event can be significantly larger than the max_allowed_packet size, because the value of max_allowed_packet only limits each column of the table.
The replica actually accepts packets up to the limit set by its slave_max_allowed_packet setting, which default to the maximum setting of 1GB, to prevent a replication failure due to a large packet. However, the value of slave_pending_jobs_size_max controls the memory that is made available on the replica to hold incoming packets. The specified memory is shared among all the replica worker queues.
The value of slave_pending_jobs_size_max is a soft limit, and if an unusually large event (consisting of one or multiple packets) exceeds this size, the transaction is held until all the replica workers have empty queues, and then processed. All subsequent transactions are held until the large transaction has been completed. So although unusual events larger than slave_pending_jobs_size_max can be processed, the delay to clear the queues of all the replica workers and the wait to queue subsequent transactions can cause lag on the replica and decreased concurrency of the replica workers. slave_pending_jobs_size_max should therefore be set high enough to accommodate most expected event sizes.
师爷，翻译翻译，什么叫 slave_pending_jobs_size_max ······
> 
在多线程副本(slave_parallel_workers > 0)上，确保系统变量 slave_pending_jobs_size_max 的值等于或大于复制源中系统变量 max_allowed_packet 的设置。slave_pending_jobs_size_max 的默认设置应该是128M，是 max_allowed_packet 的默认设置(64M)的两倍。Max_allowed_packet 限制源端可以发送数据包的大小，但添加 event header 会产生超过这个大小的 binlog event 。另外在基于 ROW 模式的复制中，单个事件可能会显著大于 max_allowed_packet 的大小，因为 max_allowed_packet 的值只限制表中的每一列。
复制实际上接受的数据包不超过其 slave_max_allowed_packet 设置的限制，默认为最大设置1GB，以防止由于大数据包而导致复制失败。 但 slave_pending_jobs_size_max 的值控制了副本上可用来保存传入数据包的内存。指定的内存在所有复制工作队列中共享。slave_pending_jobs_size_max 的值是一个软限制，如果一个异常大的事件超过了这个大小，事务将被保持，直到所有的复制工作者都有空队列，然后处理。在大事务完成之前，将持有后续所有事务。因此可以处理大于 slave_pending_jobs_size_max 的异常事件，但清除所有副本工作人员队列的延迟和等待后续事务的队列会导致从库延迟，并降低副本工作线程的并发性。 因此 Slave_pending_jobs_size_max 应该设置得足够高，以适应大多数预期事件的大小。
看来 DBA 对于 MTS 的了解不足致使我们在数据库的参数配置中还有很大的优化空间，多翻翻官方文档还是能得到很多建议的。slave_pending_jobs_size_max 可以在线全局修改，但是需要重启复制才能生效。
> 
参考：
https://www.percona.com/blog/2017/07/19/multi-threaded-slave-statistics/
http://mysql.taobao.org/monthly/2015/08/09/?spm=a2c6h.13066369.0.0.40e2c637F8gChL
主从延迟可能出现问题的场景，DBA 接触最多的还是大事务和锁等待现象，其他相关知识大家了解：
## tips：MySQL的主从延迟
### 1、传输延迟
MySQL 的 master 使用 Binlog Dump 线程将二进制日志传输到 slave 中过程中产生的延迟。
传输延迟的大小就是主库 binlog 的生成位置 position 减去从库 binlog 传输的位置 position 。
#### 传输延迟的原因：
- 
dump 线程是单线程，可能没有那么强的能力取读速度如此之快的并发事务产生的 binlog 。
- 
交换机、路由器等硬件问题或网络带宽的限制导致的两台服务器之间的网络延迟。
- 
slave 上的 io 线程没有能力及时写入 relay log 。
#### 传输延迟的解决：
- 
避免 master 上大批量 DML 的执行。
- 
增加网络带宽或者更新网络硬件。
- 
增加 slave 的写能力，比如使用 raid 卡 + 写 flash 。
- 
增加 slave 进行物理读的能力，使用 Pcie 闪卡。
- 
换数据库。
### 2、应用延迟
而应用延迟是 MySQL 的 master 传到 slave 上进行回放 binlog 的延迟，即延迟大小等于 slave 中 Read_Master_Log_Pos &#8211; Exec_Master_Log_Pos 的值。有的同学就说了，我们都升级使用 Gtid 了，position 这种老土的方法，同理我们可以通过对比同一 UUID 下
Retrieved_Gtid_Set &#8211; Executed_Gtid_Set 的事务差值就是我们的延迟大小啦，不过是以事务为计量单位的。
#### 应用延迟的原因：
- 
应用延迟最根本的原因是 master 上多线程并行复制，slave 的单线程回放机制。
- 
再就是 MySQL 的 binlog 记录模式是 ROW 模式时，进行变更的表没有主键或者没有高效索引。
- 
事务中存在问题 SQL（慢 SQL ）。
#### 应用延迟的解决：
- 
MySQL 在 5.7 中开启组提交会很有帮助。
- 
建议业务人员在建表规范中将数据库中所有表都要有主键，dml 要走高效索引。
- 
如果业务在进行大批量跑批，可以选择临时关闭 binlog ，从库进行特殊处理（数据库备份恢复或者单独执行批量 DML 后加入集群）。
- 
使用多从库将业务分离。