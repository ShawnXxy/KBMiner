# 技术分享 | 数据校验工具 pt-table-checksum

**原文链接**: https://opensource.actionsky.com/20201229-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-12-29T00:39:57-08:00

---

作者：耿进
爱可生 DBA 团队成员，负责公司 DMP 产品的运维和客户 MySQL 问题的处理。对数据库技术有着浓厚的兴趣。你见过凌晨四点 MySQL 的 error 吗？
本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
> 
参考文档：
https://www.percona.com/doc/percona-toolkit/LATEST/pt-table-checksum.html
**1. 概述**
pt-table-checksum 是 Percona-Toolkit 的组件之一，用于检测 MySQL 主、从库的数据是否一致。其原理是在主库执行基于 statement 的 SQL 语句来生成主库数据块的checksum，把相同的 SQL 语句传递到从库执行，并在从库上计算相同数据块的 checksum，最后，比较主从库上相同数据块的 checksum 值，由此判断主从数据是否一致。它能在非常大的表上工作的一个原因是，它把每个表分成行块，并检查每个块与单个替换。选择查询。它改变块的大小，使校验和查询在所需的时间内运行。分块表的目的是确保校验和不受干扰，并且不会在服务器上造成太多复制延迟或负载，而不是使用单个大查询处理每个表。这就是为什么默认情况下每个块的目标时间是 0.5 秒。
**2. 场景**
pt-table-checksum 默认情况下可以应对绝对部分场景，官方说，即使上千个库、上万亿的行，它依然可以很好的工作，这源自于设计很简单，一次检查⼀个表，不需要太多的内存和多余的操作；必要时，pt-table-checksum 会根据服务器负载动态改变 chunk 大小，减少从库的延迟。为了减少对数据库的干预，pt-table-checksum 还会⾃动侦测并连接到从库，当然如果失败，可以指定 &#8211;recursion-method 选项来告诉从库在哪里。它的易用性还体现在，复制若有延迟，在从库 checksum 会暂停直到赶上主库的计算时间点（也通过选项 &#8212; 设定一个可容忍的延迟最大值，超过这个值也认为不一致）。
**3. 保障措施**
pt-table-checksum 有许多其他的安全措施，以确保它不会⼲扰任何服务器的操作，包括副本。为了做到这⼀点，pt-table-checksum 检测副本并⾃动连接到它们。(如果失败，可以使⽤递归⽅法选项给它⼀个提示。)该工具持续监控副本。如果任何副本在复制过程中远远落后，pt 表校验和会暂停以使其赶上来。如果任何副本有错误，或者复制停止，pt-table 校验和将暂停并等待。此外，pt-table-checksum 查找问题的常见原因，比如复制过滤器，并且拒绝操作，除⾮您强迫它这样做。复制筛选器是危险的，因为 pt-table-checksum 执行的查询可能与它们发生冲突，并导致复制失败。pt-table 校验和验证块是否太大而不能安全校验和。它对每个块执行解释查询，并跳过可能大于所需行数的块。您可以使用 &#8211;chunk-size-limit 选项配置此保护措施的敏感性。如果一个表因为行数少而要在单个块中对其进行校验，那么 pt-table-checksum 将额外验证该表在副本上是否过大。这避免了以下场景：表在主服务器上是空的，但在副本上非常大，并且在一个大型查询中进行检查，这会导致复制过程中出现非常长的延迟。还有⼀些其他的保障措施。例如，pt-table-checksum 将它的会话级 innodb_lock_wait_timeout 设置为 1 秒，这样，如果存在锁等待，它将成为受害者，而不是导致其他查询超时。另一个安全措施检查数据库服务器上的负载，如果负载过高则暂停。对于如何做到这一点，没有一个正确的答案，但是默认情况下，如果有超过 25 个并发执行的查询，pt-table-checksum 将暂停。您可能应该使用 &#8211;max-load 选项为服务器设置一个合理的值。校验和通常是一个低优先级的任务，应该让位给服务器上的其他⼯作。然而，一个必须经常重启的共工具是很难使用的。因此，pt 表校验和对错误具有很强的弹性。例如，如果数据库管理员出于任何原因需要杀死 pt-table-checksum 的查询，这就不是一个致命错误。⽤户经常运行 pt-kill 来终止任何长时间运行的校验和查询。该工具将重试一次已杀死的查询，如果再次失败，它将移动到该表的下一个块。如果存在锁等待超时，则应用相同的行为。如果发生这样的错误，工具将打印一个警告，但每个表只打印一次。如果到任何服务器的连接失败，pt-table-checksum 将尝试重新连接并继续⼯作。
**4. 操作步骤**
1. 创建主从架构
![](https://opensource.actionsky.com/wp-content/uploads/2020/12/微信截图_20201229133002.png)											
安装 mysql（略）- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`# 创建复制⽤户（⽅便切换，从库也创建）``master82 >GRANT REPLICATION SLAVE ON *.* TO repl@'10.186.63.%' IDENTIFIED BY '123';``Query OK, 0 rows affected, 1 warning (0.01 sec)``# 建⽴复制``slave83 >change master to``master_host='10.186.63.82',master_port=4380,master_user='repl',master_password='123',MASTER_AUTO_POSITION=1;``Query OK, 0 rows affected, 2 warnings (0.01 sec)``slave83 >start slave;``Query OK, 0 rows affected (0.04 sec)``slave83 >show slave status\G``*************************** 1. row ***************************`` Slave_IO_State: Waiting for master to send event`` Master_Host: 10.186.63.82`` Master_User: repl`` Master_Port: 4380`` Connect_Retry: 60`` Master_Log_File: mysql-bin.000004`` Read_Master_Log_Pos: 220764474`` Relay_Log_File: mysql-relay.000002`` Relay_Log_Pos: 24944`` Relay_Master_Log_File: mysql-bin.000004`` Slave_IO_Running: Yes`` Slave_SQL_Running: Yes`
2. 造数据
使用 sysbench 造表，并且会同步至从库。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`[root@node01 ~]# sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-host=10.186.63.82 \``--mysql-port=4380 --mysql-user=gengjin --mysql-password=123 --mysql-db=test \``--table-size=1000000 --tables=10 --threads=50 --report-interval=3 --time=20 prepare``sysbench 1.0.17 (using system LuaJIT 2.0.4)``Initializing worker threads...``Creating table 'sbtest3'...``Creating table 'sbtest6'...``Creating table 'sbtest5'...``Creating table 'sbtest8'...``Creating table 'sbtest1'...``Creating table 'sbtest9'...``Creating table 'sbtest7'...``Creating table 'sbtest4'...``Creating table 'sbtest2'...``Creating table 'sbtest10'...``Inserting 1000000 records into 'sbtest1'``Inserting 1000000 records into 'sbtest8'``Inserting 1000000 records into 'sbtest9'``Inserting 1000000 records into 'sbtest6'``Inserting 1000000 records into 'sbtest7'``Inserting 1000000 records into 'sbtest5'``Inserting 1000000 records into 'sbtest4'``Inserting 1000000 records into 'sbtest3'``Inserting 1000000 records into 'sbtest2'``Inserting 1000000 records into 'sbtest10'``master82 >use test;``Reading table information for completion of table and column names``You can turn off this feature to get a quicker startup with -A``Database changed``master82 >show tables;``+----------------+``| Tables_in_test |``+----------------+``| sbtest1 |``| sbtest10 |``| sbtest2 |``| sbtest3 |``| sbtest4 |``| sbtest5 |``| sbtest6 |``| sbtest7 |``| sbtest8 |``| sbtest9 |``+----------------+``10 rows in set (0.00 sec)``master82 >``slave83 >use test;``Reading table information for completion of table and column names``You can turn off this feature to get a quicker startup with -A``Database changed``slave83 >show tables;``+----------------+``| Tables_in_test |``+----------------+``| sbtest1 |``| sbtest10 |``| sbtest2 |``| sbtest3 |``| sbtest4 |``| sbtest5 |``| sbtest6 |``| sbtest7 |``| sbtest8 |``| sbtest9 |``+----------------+``10 rows in set (0.00 sec)``slave83 >`
3. 校验
**3.1 下载安装 pt 工具**- 
- 
- 
- 
- 
- 
- 
- 
`#下载``wget https://www.percona.com/downloads/percona-toolkit/3.1.0/binary/tarball/percona-toolkit-``3.1.0_x86_64.tar.gz``yum -y install perl-devel perl-Digest-MD5 perl-DBI perl-DBD-MySQL perl-IO-Socket-SSL.noarch perl-Time-HiRes``cd percona-toolkit-3.1.0/``perl Makefile.PL PREFIX=/usr/local/``make``make install`
**3.2 参数**
&#8211;replicate-check：执行完 checksum 查询在 percona.checksums 表中，不⼀定⻢上查看结果呀 —— yes 则马上比较 chunk 的 crc32 值并输出 DIFFS 列，否则不输出。默认 yes，如果指定为 &#8211;noreplicate-check，一般后续使用下面的 &#8211;replicate-check-only 去输出 DIFF 结果。
&#8211;replicate-check-only：不在主从库做 checksum 查询，只在原有 percona.checksums 表中查询结果，并输出数据不⼀致的信息。周期性的检测⼀致性时可能⽤到。
&#8211;nocheck-binlog-format：不检测日志格式。这个选项对于 ROW 模式的复制很重要，因为 pt-table-checksum 会在 Master 和 Slave 上设置 binlog_format=STATEMENT（确保从库也会执行 checksum SQL），MySQL 限制从库是无法设置的，所以假如行复制从库，再作为主库复制出新从库时（A->B->C），B 的 checksums 数据将无法传输。
&#8211;replicate= 指定 checksum 计算结果存到哪个库表⾥，如果没有指定，默认是 percona.checksums 。
**3.3 执行校验**
1）场景 1- 标准端口
- 检查某库下某表
- ⼀主⼀从
- 从库 binlog 不是 ROW 格式
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`[root@node01 percona-toolkit-3.1.0]# pt-table-checksum h=10.186.63.82,u=gengjin,p='123',P=3306 --`` databases=test --tables=sbtest1,sbtest2 --nocheck-replication-filters``Checking if all tables can be checksummed ...``Starting checksum ...`` TS ERRORS DIFFS ROWS DIFF_ROWS CHUNKS SKIPPED TIME TABLE``12-21T09:42:57 0 0 1000000 0 8 0 3.859 test.sbtest1``12-21T09:43:02 0 0 1000000 0 6 0 5.122 test.sbtest2``...``#会⾃动创建校验库表``master82 >show tables;``+-------------------+``| Tables_in_percona |``+-------------------+``| checksums |``+-------------------+``mysql> select * from checksums`` -> ;``+------+---------+-------+------------+-------------+----------------+----------------+----------+----------``+------------+------------+---------------------+``| db | tbl | chunk | chunk_time | chunk_index | lower_boundary | upper_boundary | this_crc | this_cnt``| master_crc | master_cnt | ts |``+------+---------+-------+------------+-------------+----------------+----------------+----------+----------``+------------+------------+---------------------+``| test | sbtest1 | 1 | 0.004363 | PRIMARY | 1 | 1000 | 949e9d20 | 1000``| 949e9d20 | 1000 | 2020-12-22 03:26:13 |``| test | sbtest1 | 2 | 0.282387 | PRIMARY | 1001 | 115598 | daeb5f19 | 114598``| daeb5f19 | 114598 | 2020-12-22 03:26:13 |``| test | sbtest1 | 3 | 0.382239 | PRIMARY | 115599 | 317495 | d748771b | 201897``| d748771b | 201897 | 2020-12-22 03:26:14 |``| test | sbtest1 | 4 | 0.462463 | PRIMARY | 317496 | 559251 | 2b9cc322 | 241756``| 2b9cc322 | 241756 | 2020-12-22 03:26:14 |``| test | sbtest1 | 5 | 0.43845 | PRIMARY | 559252 | 810981 | 1bef4fe1 | 251730``| 1bef4fe1 | 251730 | 2020-12-22 03:26:15 |``| test | sbtest1 | 6 | 0.337617 | PRIMARY | 810982 | 1000000 | 6daaef2b | 189019``| 6daaef2b | 189019 | 2020-12-22 03:26:15 |``| test | sbtest1 | 7 | 0.002212 | PRIMARY | NULL | 1 | 0 | 0``| 0 | 0 | 2020-12-22 03:26:15 |``| test | sbtest1 | 8 | 0.011642 | PRIMARY | 1000000 | NULL | 0 | 0``| 0 | 0 | 2020-12-22 03:26:15 |``| test | sbtest2 | 1 | 0.447947 | PRIMARY | 1 | 262120 | d454c57a | 262120``| d454c57a | 262120 | 2020-12-22 03:26:18 |``| test | sbtest2 | 2 | 0.507594 | PRIMARY | 262121 | 554699 | 221a4326 | 292579``| 221a4326 | 292579 | 2020-12-22 03:26:19 |``| test | sbtest2 | 3 | 0.497652 | PRIMARY | 554700 | 844644 | b47933a4 | 289945``| b47933a4 | 289945 | 2020-12-22 03:26:20 |``| test | sbtest2 | 4 | 0.286117 | PRIMARY | 844645 | 1000000 | 7246a964 | 155356``| 7246a964 | 155356 | 2020-12-22 03:26:20 |``| test | sbtest2 | 5 | 0.002235 | PRIMARY | NULL | 1 | 0 | 0``| 0 | 0 | 2020-12-22 03:26:20 |``| test | sbtest2 | 6 | 0.002173 | PRIMARY | 1000000 | NULL | 0 | 0``| 0 | 0 | 2020-12-22 03:26:20 |``+------+---------+-------+------------+-------------+----------------+----------------+----------+----------``+------------+------------+---------------------+``14 rows in set (0.01 sec)``mysql>`2）场景 2（dsn）
- 非标准端口（主从端口不⼀致）
- 一主多从
- 全实例校验
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`# 创建校验库表``master82 >CREATE DATABASE IF NOT EXISTS percona; ``Query OK, 1 row affected (0.00 sec)``master82 >CREATE TABLE IF NOT EXISTS percona.checksums ( db CHAR(64) NOT NULL, tbl CHAR(64) NOT NULL, chunk``INT NOT NULL, chunk_time FLOAT NULL, chunk_index VARCHAR(200) NULL, lower_boundary TEXT NULL, upper_boundary``TEXT NULL, this_crc CHAR(40) NOT NULL, this_cnt INT NOT NULL, master_crc CHAR(40) NULL, master_cnt INT NULL,``ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (db,tbl,chunk),``INDEX ts_db_tbl(ts,db,tbl) ) ENGINE=InnoDB; ``Query OK, 0 rows affected (0.06 sec)``# 创建dsn表``master82 >CREATE DATABASE IF NOT EXISTS percona; ``Query OK, 1 row affected, 1 warning (0.00 sec)``master82 >CREATE TABLE percona.dsns ( id int(11) NOT NULL AUTO_INCREMENT, parent_id int(11) DEFAULT NULL,``dsn varchar(255) NOT NULL, PRIMARY KEY (id) );``Query OK, 0 rows affected (0.01 sec)``master82 >show tables;``+-------------------+``| Tables_in_percona |``+-------------------+``| checksums |``| dsns |``+-------------------+``2 rows in set (0.00 sec)``# 添加从库信息``master82 >insert into percona.dsns(dsn) values('h=10.186.63.83,P=4380,u=gengjin,p=123');``Query OK, 1 row affected (0.00 sec)``master82 >``# 校验``root@node01 percona-toolkit-3.1.0]# pt-table-checksum --replicate=percona.checksums --nocheck-replicationfilters --no-check-binlog-format --max-load Threads_connected=600 h=10.186.63.82,u=gengjin,p='123',P=4380 --``recursion-method dsn=h=10.186.63.83,u=gengjin,p='123',P=4380,D=percona,t=dsns --function MD5``Checking if all tables can be checksummed ...``Starting checksum ...``# A software update is available:`` TS ERRORS DIFFS ROWS DIFF_ROWS CHUNKS SKIPPED TIME TABLE``12-21T09:03:19 0 0 0 0 1 0 0.358 mysql.columns_priv``12-21T09:03:19 0 0 10 0 1 0 0.497 mysql.db``12-21T09:03:20 0 0 2 0 1 0 0.497 mysql.engine_cost``12-21T09:03:20 0 0 0 0 1 0 0.497 mysql.event``12-21T09:03:21 0 0 0 0 1 0 0.497 mysql.func``12-21T09:03:21 0 0 41 0 1 0 0.498 mysql.help_category``12-21T09:03:22 0 0 699 0 1 0 0.497 mysql.help_keyword``12-21T09:03:22 0 0 1413 0 1 0 0.497 mysql.help_relation``12-21T09:03:23 0 0 643 0 1 0 0.497 mysql.help_topic``12-21T09:03:23 0 0 0 0 1 0 0.498 mysql.ndb_binlog_index``12-21T09:03:24 0 0 0 0 1 0 0.498 mysql.plugin``12-21T09:03:24 0 0 48 0 1 0 0.494 mysql.proc``12-21T09:03:25 0 0 0 0 1 0 0.501 mysql.procs_priv``12-21T09:03:25 0 0 2 0 1 0 0.492 mysql.proxies_priv``12-21T09:03:26 0 0 6 0 1 0 0.498 mysql.server_cost``12-21T09:03:26 0 0 0 0 1 0 0.498 mysql.servers``12-21T09:03:27 0 0 2 0 1 0 0.497 mysql.tables_priv``12-21T09:03:27 0 0 0 0 1 0 0.498 mysql.time_zone``12-21T09:03:28 0 0 0 0 1 0 0.496 mysql.time_zone_leap_second``12-21T09:03:28 0 0 0 0 1 0 0.497 mysql.time_zone_name``12-21T09:03:29 0 0 0 0 1 0 0.499 mysql.time_zone_transition``12-21T09:03:30 0 0 0 0 1 0 0.510 mysql.time_zone_transition_type``12-21T09:03:30 0 1 8 0 1 0 0.481 mysql.user``12-21T09:03:30 0 0 1 0 1 0 0.485 percona.dsns``12-21T09:03:31 0 0 6 0 1 0 0.485 sys.sys_config``12-21T09:03:42 0 0 1000000 0 11 0 11.002 test.sbtest1``12-21T09:03:53 0 0 1000000 0 10 0 10.662 test.sbtest10``12-21T09:04:02 0 0 1000000 0 9 0 9.797 test.sbtest2``12-21T09:04:14 0 0 1000000 0 10 0 11.497 test.sbtest3``12-21T09:04:24 0 0 1000000 0 10 0 10.495 test.sbtest4``12-21T09:04:33 0 0 1000000 0 9 0 8.996 test.sbtest5``12-21T09:04:42 0 0 1000000 0 9 0 8.198 test.sbtest6``12-21T09:04:51 0 0 1000000 0 9 0 9.302 test.sbtest7``12-21T09:05:00 0 0 1000000 0 9 0 9.141 test.sbtest8``12-21T09:05:08 0 0 1000000 0 9 0 8.345 test.sbtest9``12-21T09:05:09 0 0 1 0 1 0 0.490 universe.u_delay``查看checksums表数据（略）`
相关推荐：
[技术分享 | 如何写一个自己的 bcc 工具观测 MySQL？](https://opensource.actionsky.com/20201228-mysql/)
[技术分享 | 使用 pt-query-digest 分析慢日志](https://opensource.actionsky.com/20200922-percona/)
[技术分享 | MySQL 监控利器之 Pt-Stalk](https://opensource.actionsky.com/20200522-mysql/)