# 记一次 MySQL semaphore crash 的分析（有彩蛋）

**原文链接**: https://opensource.actionsky.com/20180913-mysql-semaphore-crash/
**分类**: MySQL 新特性
**发布时间**: 2018-09-13T00:00:50-08:00

---

DBA应该对InnoDB: Semaphore wait has lasted > 600 seconds. We intentionally crash the server because it appears to be hung. 一点都不陌生，MySQL后台线程srv_error_monitor_thread发现存在阻塞超过600s的latch锁时，如果连续10次检测该锁仍没有释放，就会触发panic避免服务持续hang下去。
发生了什么
![记一次 MySQL semaphore crash 的分析（有彩蛋）](.img/d1472a6b.png) 
**
**
**版本号：MySQL 5.5.40**
- 
日志中持续输出线程等待数据字典锁，位置是dict0dict.c line 305，等待时间超过了900s。
- 
持有锁的线程是 139998697924352 ，其十六进制是7f53fca8a700。
&#8211;Thread 139998393616128 has waited at dict0dict.c line 305 for 934.00 seconds the semaphore:
X-lock on RW-latch at 0x105a1b8 created in file dict0dict.c line 748
a writer (thread id 139998697924352) has reserved it in mode  exclusive
number of readers 0, waiters flag 1, lock_word: 0
Last time read locked in file dict0dict.c line 302
Last time write locked in file /pb2/build/sb_0-13157587-1410170252.03/rpm/BUILD/mysql-5.5.40/mysql-5.5.40/storage/innobase/dict/dict0dict.c line 305
**上锁线程 139998697924352 的事务信息，查询数据字典表的操作。**
**
**
&#8212;TRANSACTION 0, not started updating table statistics：
MySQL thread id 14075, OS thread handle 0x7f53fca8a700, query id 110414021 21.14.5.139 jzjkusr
SELECT ROUND(SUM(DATA_LENGTH+INDEX_LENGTH+DATA_FREE)/1024/1024/1024) AS MY_DB_TOTAL_SIZE FROM information_schema.TABLES
**检查下持锁线程 139998697924352 是否存在其他锁等待。**
**发现线程 139998697924352 ，self-lock 在 btr0sea.c line 1134，该锁结构和 AHI 相关。**
&#8211;Thread 139998697924352 has waited at btr0sea.c line 1134 for 934.00 seconds the semaphore:
X-lock (wait_ex) on RW-latch at 0x1eb06448 created in file btr0sea.c line 178
a writer (thread id 139998697924352) has reserved it in mode  wait exclusive
number of readers 1, waiters flag 1, lock_word: ffffffffffffffff
Last time read locked in file btr0sea.c line 1057
Last time write locked in file /pb2/build/sb_0-13157587-1410170252.03/rpm/BUILD/mysql-5.5.40/mysql-5.5.40/storage/innobase/btr/btr0sea.c line 1134
**接下来看下两处锁结构分别在哪个函数内：**
- 
dict0dict.c line 305在dict_table_stats_lock函数内
- 
btr0sea.c line 1134在btr_search_drop_page_hash_index函数内
**什么情况会调用这些函数？**
- 
启用 innodb_table_monitor，输出日志时调用 dict_table_stats_lock 上 X 锁，本案例未开启。
启用 innodb_stats_on_metadata 时，查询数据字典表会触发统计信息的更新操作，会调用 dict_table_stats_lock 上 X 锁。这与持锁线程的事务信息匹配。
- 
Adaptive hash index(AHI) 是 InnoDB 用来加速索引页查找的 hash 表结构。当页面访问次数满足一定条件后，这个页面的地址将存入一个 hash 表中，减少 B 树查询的开销。
MySQL 5.5 版本 AHI 是由全局锁 btr_search_latch 维护 hash 表修改的一致性。
- 
InnoDB buffer pool 状态显示 free buffer 基本保持0空闲。InnoDB buffer pool 驱逐数据页时，会调用 btr_search_drop_page_hash_index 函数，从 AHI 中清理该数据页。
&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;
BUFFER POOL AND MEMORY
&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211;
Total memory allocated 17582522368; in additional pool allocated 0
Dictionary memory allocated 4289681
Buffer pool size   1048576
Free buffers       0
Database pages     1040831
Old database pages 384193
Modified db pages  0
小结     
![记一次 MySQL semaphore crash 的分析（有彩蛋）](.img/057d66b4.png) 
AHI 的全局锁 btr_search_latch 经常会是竞争热点影响性能，5.7版本后有所改善与 InnoDB buffer 一样做了多实例拆分。本案例在开启 Innodb_stats_on_metadata 参数，查询元数据信息时触发统计信息更新，上锁数据字典，阻塞了了大量业务操作，又由于 buffer pool 空间不足，导致表驱逐旧页触发 AHI 的 btr_search_latch 锁竞争，最终导致信号量超时 crash。  
![记一次 MySQL semaphore crash 的分析（有彩蛋）](.img/e4efaee3.png)
**！！   彩蛋    ！！**
**
**
在动辄几兆的日志中分析 Semaphore crash，寻找锁、线程、事务之间的关系，相当令人抓狂的。借助 sed、awk、grep 三大法宝，虽有效率提升，但仍不够高效。
为了偷懒写了一个小程序，帮助DBA快速梳理出这些关系。
**它的用法是这样的：**
> 
hongbin@MBP ~> mysqldba doctor -f /Users/hongbin/workbench/mysqld_safe.log
**目标版本，查代码时找对应版本：**
**
**
> 
MySQL Server Version: &#8216;5.7.16-log’   
**日志中出现的 semaphore crash 次数和 mysql 启动次数，如果启动次数大于 crash 次数说明可能是正常启动或其他 crash 造成：**
**
**
********** MySQL service start count **********
MySQL Semaphore crash -> 3 times [&#8220;2018-08-13 23:12:18&#8221; &#8220;2018-08-14 12:13:43&#8221; &#8220;2018-08-16 13:42:36&#8221;]
MySQL Service start -> 3 times [&#8220;2018-08-13 23:12:59&#8221; &#8220;2018-08-14 12:15:20&#8221; &#8220;2018-08-16 13:46:37&#8221;]
**线程主要在等待哪些 RW-latch，内容包括：锁位置、出现次数、线程 id (出现次数)，重点关注出现次数较多的：**
**
**
********** Which thread waited lock **********
row0purge.cc:861 ->  58  140477266503424:(57) 140617703745280:(1)
gi.cc:14791 ->   1  140477035656960:(1)
trx0undo.ic:171 ->   1  140617682765568:(1)
ha_innodb.cc:14791 -> 620  140617389913856:(58) 140202719565568:(58) 140202716903168:(57) 140477029533440:(56) 140617407219456:(55) 140477035656960:(52) 140477035124480:(29) 140477108467456:(29) 140477025539840:(26) 140477031130880:(25) 140477027669760:(22) 140617634944768:(21) 140617634146048:(21) 140477019948800:(21) 140477026604800:(20) 140477022078720:(18) 140477018883840:(16) 140477038585600:(15) 140477028734720:(10) 140477022877440:(9) 140477034325760:(1) 140477031663360:(1)
srv0srv.cc:1968 -> 208  140477276993280:(185) 140617714235136:(23)
ha_innodb.cc:5510 -> 601  140617398167296:(57) 140617409615616:(55) 140617392043776:(53) 140477110597376:(52) 140617395771136:(50) 140617636275968:(45) 140617632548608:(40) 140617634146048:(33) 140617639675648:(32) 140617397102336:(28) 140617639409408:(23) 140617635743488:(21) 140617637811968:(18) 140617638610688:(16) 140617399232256:(12) 140617638344448:(10) 140617638078208:(10) 140477033793280:(10) 140477029267200:(10) 140617397368576:(9) 140617635211008:(6) 140617393641216:(5) 140617637545728:(3) 140617402693376:(2) 140477037254400:(1)
dict0dict.cc:1239 -> 136  140477122623232:(50) 140617392842496:(35) 140202726487808:(26) 140477123688192:(12) 140477038851840:(5) 140477030065920:(4) 140617634412288:(4)
row0trunc.cc:1835 ->   1  140477109798656:(1)
**上述锁被哪些写线程持有 X 锁，重点关注出现次数较多的：**
**
**
********** Which writer threads block at **********
140616681907968 ->   1  trx0undo.ic:171:(1)
140477173069568 -> 243  srv0srv.cc:1968:(185) row0purge.cc:861:(57) row0trunc.cc:1835:(1)
140617682765568 ->  29  srv0srv.cc:1968:(23) ha_innodb.cc:5510:(5) row0purge.cc:861:(1)
**写线程对应的事务信息，也可能存在日志记录没有输出事务信息：**
**
**
********** These writer threads trx state **********
MySQL thread id 83874, OS thread handle 140477173069568, query id 13139674 10.0.1.146 aml deleting from reference tables
**
**
**统计写线程持有 S 锁情况：**
**
**
****These writer threads at last time reads locked ****
140477173069568 -> 243  row0purge.cc:861:(243)
140617682765568 ->  24  row0purge.cc:861:(24)
140616681907968 ->   1  trx0undo.ic:190:(1)
**统计写线程持有 X 锁情况：**
**
**
****These writer threads at last time write locked ****
140477173069568 -> 243  dict0stats.cc:2366:(243)
140617682765568 ->  24  dict0stats.cc:2366:(24)
140616681907968 ->   1  buf0flu.cc:1198:(1)
通过事后日志分析，有可能出现线程的事务信息没有输出到日志中的情况，无法获知事务具体执行了什么操作。应对这种情况，小程序加入了事中采集事务信息。
用法是这样的：
> 
hongbin@MBP ~> mysqldba -uxxx -pxxx doctor -w
它会监视目标 mysql 的错误日志，一旦出现“a writer (thread id 140616681907968) has reserved it in mode” 关键字就查询 ps 中的事务信息，并保存下来。
以上只是小程序一个用法，作为一个为DBA服务的小程序，还有其他功能等你去发现。欢迎与我交流你的想法。
> 
https://github.com/kevinbin/mysqldba
<
p style=&#8221;line-height: 1.75em;&#8221;>