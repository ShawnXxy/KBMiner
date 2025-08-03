# 故障分析 | 奇怪！内存明明够用，MySQL 却出现了 OOM

**原文链接**: https://opensource.actionsky.com/20210408-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-04-08T01:11:58-08:00

---

作者：刘开洋爱可生交付服务部团队北京 DBA，主要负责处理 MySQL 的 troubleshooting 和我司自研数据库自动化管理平台 DMP 的日常运维问题，对数据库及周边技术有浓厚的学习兴趣，喜欢看书，追求技术。本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 问题
前几天遇到一个奇怪的问题，服务器内存明明够用，结果在对 MySQL 进行测压的时候却出现了 OOM，是 Linux 内核出错了吗？
具体现象如下：使用 sysbench 对 mysql 进行压测，并发 50、80 均正常输出，当并发达到 100 时开始报 OOM。
`[root@BJDB-01 ~]# sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-host=BJDB-02 --mysql-port=3306 --mysql-user=root --mysql-password=*** --mysql-db=test --table-size=100000 --tables=5 --threads=100 --db-ps-mode=disable --auto_inc=off --report-interval=3 --max-requests=0 --time=360 --percentile=95 --skip_trx=off --mysql-ignore-errors=6002,6004,4012,2013,4016,1062 --create_secondary=off run
sysbench 1.0.17 (using system LuaJIT 2.0.4)
 
Running the test with following options:
Number of threads: 100
Report intermediate results every 3 second(s)
Initializing random number generator from current time
 
Initializing worker threads...
 
 
FATAL: mysql_store_result() returned error 5(Out of memory (Needed 48944 bytes))
FATAL: 'thread_run' function failed: /usr/share/sysbench/oltp_common.lua:432: SQL error，errno = 5, state = 'HY000': Out of memory (Needed 48944 bytes)
FATAL: mysql_store_result() returned error 5(Out of memory (Needed 48944 bytes))
FATAL: 'thread_run' function failed: /usr/share/sysbench/oltp_common.lua:432: SQL error，errno = 5, state = 'HY000': Out of memory (Needed 48944 bytes)`
MySQL 中 error log 的报错为：
`······
2021-03-16T09:13:00.692622+08:00 343 [ERROR] [MY-010934] [Server] Out of memory (Needed 708628 bytes)
2021-03-16T09:13:00.692702+08:00 343 [ERROR] [MY-010934] [Server] Out of memory; check if mysqld or some other process uses all available memory; if not, you may have to use 'ulimit' to allow mysqld to use more memory or you can add more swap space
2021-03-16T09:13:59.832037+08:00 374 [ERROR] [MY-000000] [InnoDB] InnoDB: Assertion failure: ut0ut.cc:678:!m_fatal
InnoDB: thread 140375101384448
InnoDB: We intentionally generate a memory trap.
InnoDB: Submit a detailed bug report to http://bugs.mysql.com.
InnoDB: If you get repeated assertion failures or crashes, even
InnoDB: immediately after the mysqld startup, there may be
InnoDB: corruption in the InnoDB tablespace. Please refer to
InnoDB: http://dev.mysql.com/doc/refman/8.0/en/forcing-innodb-recovery.html
InnoDB: about forcing recovery.
01:13:59 UTC - mysqld got signal 6 ;`
## 分析
对 MySQL OOM 我们一步步进行分析，首先应该查看 ulimit 限制，
`[root@BJDB-02 ~]# ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 23045
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 23045
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited`
系统并没有对 ulimit 进行限制，100 个并发量在我们的配置之内，那就不是 ulimit 配置的问题，接下来分析下内存的使用情况，
在复现 MySQL OOM 的过程中，查看对应内存使用，通过 top 和 free 命令进行监控，得到以下信息，
`[root@BJDB-02 ~]# free -m
              total        used        free      shared  buff/cache   available
Mem:          16047        1958        8956         8        5132       13920
Swap:          5119           0        5119
  
[root@BJDB-02 ~]# top
top - 17:21:30 up 32 min,  4 users,  load average: 0.00, 0.04, 0.11
Tasks: 226 total,   2 running, 224 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.2 us,  0.6 sy,  0.0 ni, 97.2 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  16432236 total,  9164596 free,  2012156 used,   5255484 buff/cache
KiB Swap:        5242876 total,    5242876 free,        0 used.  14247508 avail Mem
 
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 7654 root      20   0   13.7g   1.7g  14312 S   1.3 10.3   0:00.27 mysqld`
这里看我们的内存使用很正常，free 和 available 都很多，swap 都没有使用，唯一存在异常的是虚拟内存有点高，我们接着分析：
进一步查看一下 /proc/meminfo，具体分析一下内存的使用情况，其中以下两个参数引起了注意：
`[root@BJDB-02 ~]# cat /proc/meminfo | grep Commit
CommitLimit:     13458992 kB
Committed_AS:    13244484 kB`
一般来说 CommitLimit 的值是要比 Committed_AS 的值要小的，结合现在内存的使用，我们应该注意到一个 OS kernel 参数。
`[root@BJDB-02 ~]# cat /etc/sysctl.conf |grep vm.overcommit_memory
vm.overcommit_memory=2
`将 vm.overcommit_memory 调整为 0，压测时 MySQL OOM 消失了。
这三个参数值是什么意思呢？它和内存使用的关系是什么？内存真的够用吗？通过翻看 Linux 的内核文档我们来进行详细说明。
**分析 vm.overcommit_memory 的使用**
首先解释下 overcommit 的意思是指操作系统承诺给进程的内存大小超过了实际可用的内存。
**从内核版本 2.5.30 开始，这个参数的解释为：**
overcommit_memory：This value contains a flag that enables memory overcommitment.
- When this flag is 0, Heuristic overcommit handling, the kernel attempts to estimate the amount of free memory left when userspace requests more memory. Obvious overcommits of address space are refused. Used for a typical system. It ensures a seriously wild allocation fails while allowing overcommit to reduce swap usage. root is allowed to allocate slightly more memory in this mode. This is the default.
- When this flag is 1, Always overcommit, the kernel pretends there is always enough memory until it actually runs out. Appropriate for some scientific applications. Classic example is code using sparse arrays and just relying on the virtual memory consisting almost entirely of zero pages.
- When this flag is 2, Don&#8217;t overcommit, the kernel uses a &#8220;never overcommit&#8221; policy that attempts to prevent any overcommit of memory. The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM. Depending on the amount you use, in most situations this means a process will not be killed while accessing pages but will receive errors on memory allocation as appropriate.
中文释义：
- 当这个标志为 0 时，表示试探性的 overcommit，当用户空间请求更多内存时，OS kernel 会预估剩余的空闲内存量，如果内存申请特别大就会被拒绝。例如 malloc() 一次性申请的内存大小就超过了 swap 和 physical RAM 的和，就会遭到 kernel 拒绝 overcommit。
- 当这个标志为 1 时，kernel 会假装一直有足够的内存，直到实际用完为止。
- 当这个标志为 2 时，kernel 使用“永不过度提交”的策略，试图阻止任何内存的过度提交。
从含义中分析，如果我们将 vm.overcommit_memory 的值设为 2，就很有可能出现内存申请的值超过我们的阈值，就会受到禁止。该阈值是通过内核参数 vm.overcommit_ratio 或 vm.overcommit_kbytes 间接设置的，从对应参数解释中得到公式如下：
`CommitLimit = Physical RAM * vm.overcommit_ratio + Swap                  // vm.overcommit_ratio 是内核参数，默认值是 50，表示物理内存的 50%。
`测试环境中 Physical RAM 的值约为 16G，Swap 的值约为 5G，计算下来可正对应 CommitLimit 的值 13G。
/proc/meminfo 中的 Committed_AS 表示所有进程已经申请的内存总大小，而我们查询的 free 和 top 下的内存则是进程已经分配的内存。
Committed_AS 是 OS kernel 对所有进程在最坏情况下需要多少 RAM/swap 的预估，才能保证工作负载不会出现 OOM，因此会存在过度申请提交内存的现象。
这个值是系统所有运行的程序所申请的内存大小，并不代表着分配使用的大小，而且各个程序申请的内存是可共享的。
虽然 Committed_AS 的数值与虚拟内存 VIRT 的大小很相似，目前没有找到官方说明他们之间的联系，经过多次测试，它的大小和虚拟内存并没有关系。
## 总结
如果 Committed_AS 超过 CommitLimit 就表示发生了overcommit，超出越多表示 overcommit 越严重，kernel 的 killer 进程会挑一部分进程干掉，如果内存不够还会继续被 killer 干掉，MySQL 在内存使用中占用最大，首当其冲。
测试环境查看 Committed_AS 和 CommitLimit 的参数值为：**CommitLimit: 13458992 kB**、**Committed_AS: 13244484 kB**。两者已经十分接近，在vm.overcommit_memory=2 的情况下非常容易发生 MySQL 的 OOM，因此需要将 vm.overcommit_memory 的值设为 0，具体需要根据环境变更。
附：还有两个参数与我们这次的内存分配有关系，不过影响不大，有兴趣的同学可以自行谷歌：admin_reserve_kbytes 和 user_reserve_kbytes。
> **参考：**
https://www.kernel.org/doc/Documentation/vm/overcommit-accounting
https://www.kernel.org/doc/Documentation/sysctl/vm.txt
http://lwn.net/Articles/28345/
https://www.win.tue.nl/~aeb/linux/lk/lk-9.html#ss9.6
**文章推荐：**
[故障分析 | 如何提高 MHA 的网络容忍能力？（下）](https://opensource.actionsky.com/20210322-mha-%e7%9a%84%e7%bd%91%e7%bb%9c%e5%ae%b9%e5%bf%8d%e8%83%bd%e5%8a%9b%ef%bc%9f%ef%bc%88%e4%b8%8b%ef%bc%89/)
[故障分析 | 如何提高 MHA 的网络容忍能力？（上）](https://opensource.actionsky.com/20210315-mha/)