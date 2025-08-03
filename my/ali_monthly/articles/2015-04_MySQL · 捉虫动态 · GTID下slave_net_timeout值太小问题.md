# MySQL · 捉虫动态 · GTID下slave_net_timeout值太小问题

**Date:** 2015/04
**Source:** http://mysql.taobao.org/monthly/2015/04/06/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2015 / 04
 ](/monthly/2015/04)

 * 当期文章

 MySQL · 引擎特性 · InnoDB undo log 漫游
* TokuDB · 产品新闻 · RDS TokuDB小手册
* TokuDB · 特性分析 · 行锁(row-lock)与区间锁(range-lock)
* PgSQL · 社区动态 · 说一说PgSQL 9.4.1中的那些安全补丁
* MySQL · 捉虫动态 · 连接断开导致XA事务丢失
* MySQL · 捉虫动态 · GTID下slave_net_timeout值太小问题
* MySQL · 捉虫动态 · Relay log 中 GTID group 完整性检测
* MySQL · 答疑释惑 · UPDATE交换列单表和多表的区别
* MySQL · 捉虫动态 · 删被引用索引导致crash
* MySQL · 答疑释惑 · GTID下auto_position=0时数据不一致

 ## MySQL · 捉虫动态 · GTID下slave_net_timeout值太小问题 
 Author: 襄洛 

 ## 背景

官方 5.6 最新版本 5.6.24 有这样一个bugfix，当使用 GTID 协议进行复制，并且备库的 slave_net_timeout 值设置太小的话，备库的 slave io 线程会卡住，同时主库上的 binlog dump 线程数一直在涨，[官方的bug地址](http://bugs.mysql.com/bug.php?id=74607) 。

## bug分析

首先说明下几个概念：

1. slave_net_timeout，这个变量控制备库 IO 线程的连接超时，如果IO线程在指定时间内没有从主库收到数据的话，就断开重连，默认值是3600秒；
2. heartbeat 事件，主库在dump线程空闲的时候（dump线程已经把所有binlog都发给备库了，主库还没有更新操作），就隔断时间发一个 heartbeat 给备库，以免备库超时断开，这个时间间隔是备库在 change master 时传过来的，在 rpl_slave.cc 中可以看到，默认取 `min<float>(SLAVE_MAX_HEARTBEAT_PERIOD, (slave_net_timeout/2.0))`；
3. GTID 的 auto_position 协议，正是因为有了 GTID，才可以在 chang master 时不指定binlog坐标（filename, pos），但是主库dump线程在发给备库event的时候，还是需要从某个坐标开始的，只是这个过程通过 GTID 能自动搜出来罢了，关于如何找到要发送的第一个 binlog 可以看下之前的月报，找到后就需要从这个 binlog 开头开始扫描，找到第一个备库没有 GTID，然后开始发送。

问题的源头就出在 binlog 文件扫描上，官方 bug 的复现步骤中有这样一个条件，*use 1GB binlog file size. stop slave at high binlog position (>800MB)*，就是说主库的 binlog 要比较大，并且备库 IO 线程要停在这个 binlog 比较靠后的位置。这样备库 start slave 连上的时候，主库的 dump 线程就要从这个 binlog 开头往后扫，找到开始发送 binlog 的位置，如果文件比较大的话，这个扫描时间就会比较长。heartbeat 事件是在主库空闲的时候才会发送的，在扫描过种中是不会检查要不要发 heartbeat 的，如果备库的 slave_net_timeout 设置比较小的话，超过时间还没收到一个事件，这时备库 IO 就会停下，然后重连。

IO 线程重连会导致另外一个问题，我们知道一个主库是可以拖多个备库的，但是对每个备库只能有一个连接，如果已经连上来的备库再发一个 dump 请求的话，主库就会把当前备库老的 IO 连接置为 killed，具体函数是 sql/rpl_master.cc 中的 `kill_zombie_dump_threads`，但这个 kill 只是置了标志位，还需要老的 dump 线程自己判断，然后退出。dump 线程 killed 状态检测只在切换 binlog 和空闲的时候，如果这个时候老的 dump 线程还在扫 binlog，即使已经是killed了也不会退出。而同时新的 dump 线程依然要从头扫 binlog，重复上面的过程，导致备库 IO 又超时重连，因此在主库上show processlist的话，会看到 dump 线程慢慢堆积起来。

下面的结果就是备库 slave_net_timeout 设置为10s的测试结果，可以看到相邻 dump 线程差不多间隔10s。

`| 9 | root | localhost:46882 | NULL | Binlog Dump GTID | 159 | init | NULL |
| 10 | root | localhost:46929 | NULL | Binlog Dump GTID | 149 | init | NULL |
| 11 | root | localhost:46975 | NULL | Binlog Dump GTID | 138 | init | NULL |
| 12 | root | localhost:47023 | NULL | Binlog Dump GTID | 127 | init | NULL |
| 13 | root | localhost:47074 | NULL | Binlog Dump GTID | 115 | init | NULL |
| 14 | root | localhost:47143 | NULL | Binlog Dump GTID | 104 | init | NULL |
| 15 | root | localhost:47206 | NULL | Binlog Dump GTID | 93 | init | NULL |
| 16 | root | localhost:47255 | NULL | Binlog Dump GTID | 82 | init | NULL |
| 17 | root | localhost:47311 | NULL | Binlog Dump GTID | 71 | init | NULL |
| 18 | root | localhost:47362 | NULL | Binlog Dump GTID | 60 | init | NULL |
| 19 | root | localhost:47427 | NULL | Binlog Dump GTID | 49 | init | NULL |
`

如果在备库上 show slave status 的的话，会看到 IO 线程接收的 binlog 位点一直不更新，就像 hang 住了一样。

## bug修复

出现这个问题是因为主库 dump 线程检测 heartbeat_period 和 thd->killed 的粒度太大，都是 binlog 文件级别的，因此官方的改法就是把两者的检测粒度降为event级别，dump 线程每 read 一个 event，都会检测是否该发送 heartbeat 了，同时 thd 的 killed 标志是否被置上，是的话就退出。
具体的patch可以看[官方github](https://github.com/mysql/mysql-server/commit/9ab03d0d41b25b86978b7a0aaf12f4a77c96dc27)。

有了这个 patch 后，主库 dump 线程还是需要时间扫描binlog，备库的 IO 线程看起来依然像 hang 住一样，但是已经不会超时重连，主库的dump 线程也不会堆积。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)