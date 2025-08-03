# 技术分享 | binlog 实用解析工具 my2sql

**原文链接**: https://opensource.actionsky.com/20210105-my2sql/
**分类**: 技术干货
**发布时间**: 2021-01-05T00:40:31-08:00

---

作者：赵黎明爱可生 MySQL DBA 团队成员，Oracle 10g OCM，MySQL 5.7 OCP，擅长数据库性能问题诊断、事务与锁问题的分析等，负责处理客户 MySQL 及我司自研 DMP 平台日常运维中的问题，对开源数据库相关技术非常感兴趣。本文来源：原创投稿* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 前言
大部分 DBA 应该都已经熟悉并使用过一些闪回工具，诸如：binlog2sql、MyFlash。今天要介绍的是另一款基于 Go 编写的 binlog 解析工具：my2sql，他的同门师兄还有 my2fback、binlog_inspector（binlog_rollback）。为什么不直接称其为闪回工具呢？因为闪回只是它其中一个功能，除此之外，还可用于从 binlog 中解析出执行过的 SQL 语句用于数据补偿，或者对线上执行的事务进行分析（捕获大/长事务）。
Github 地址：https://github.com/liuhr/my2sql
## 对比
- binlog2sql：Python 编写（执行时需要有 Python2.7、Python3.4+ 的环境），用于生成回滚/前滚 SQL 进行数据恢复/补偿
- MyFlash：C 语言编写（需要动态编译成二级制脚本后执行），用于生成反向 binlog 文件（二进制）进行数据恢复
- my2sql：Go 语言编写（可直接下载 linux 二进制版本执行），除了闪回，还提供了前滚和事务分析的功能
## 
## 主要参数
- -work-type：指定工作类型（前滚、闪回、事务分析），合法值分别为：2sql（默认）、rollback、stats
- -sql：过滤 DML 语句的类型，合法值为：insert、update、delete
- -ignorePrimaryKeyForInsert：对于 work-type 为 2sql 的 insert 操作，忽略主键（适合大量数据导入的场景）
- -big-trx-row-limit int：判定为大事务的阈值（默认 500 行），合法值区间：10-30000 行
- -long-trx-seconds int：判定为长事务的阈值（默认 300 秒），合法值区间：1-3600 秒
- -databases：过滤库，默认为全部库
- -tables：过滤表，默认为全部表
- -start-file：指定开始的 binlog 文件
- -start-pos：指定 binlog 文件中开始的点位
- -start-datetime：指定开始的时间
- -stop-datetime：指定结束的时间
- -output-dir：指定文件生成目录
- -output-toScreen：指定输出到屏幕
- -tl：指定时区（time location），默认为 local（Asia/Shanghai）
## 应用场景
#### 场景 1：闪回 DML 误操作数据
`-- 创建测试表
mysql> show create table t\G
*************************** 1. row ***************************
       Table: t
Create Table: CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
mysql> select count(*) from t;
+----------+
| count(*) |
+----------+
|    10000 |
+----------+
1 row in set (0.00 sec)
-- 查看测试表校验值
mysql> checksum table t;
+-------+------------+
| Table | Checksum   |
+-------+------------+
| zlm.t | 1966401574 |
+-------+------------+
1 row in set (0.02 sec)
-- 查看当前binlog
mysql> show master status;
+------------------+----------+--------------+------------------+----------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                            |
+------------------+----------+--------------+------------------+----------------------------------------------+
| mysql-bin.000003 | 15994082 |              |                  | 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-23123 |
+------------------+----------+--------------+------------------+----------------------------------------------+
1 row in set (0.00 sec)
-- 删除5000条记录
mysql> delete from t where id<5001;
Query OK, 5000 rows affected (0.04 sec)
-- 执行my2sql生成回滚语句（rollback模式）
04:38 PM dmp1 (master) ~# ./my2sql -user zlm -password zlm -host 10.186.60.62 -port 3332 -work-type rollback -start-file mysql-bin.000003 -start-pos 15994082 --add-extraInfo -output-dir /tmp/my2sql_test
[2020/12/25 16:38:17] [info] binlogsyncer.go:144 create BinlogSyncer with config {1113306 mysql 10.186.60.62 3332 zlm   utf8 false false <nil> false Local false 0 0s 0s 0 false false 0}
[2020/12/25 16:38:17] [info] events.go:58 start thread 1 to generate redo/rollback sql
[2020/12/25 16:38:17] [info] events.go:58 start thread 2 to generate redo/rollback sql
[2020/12/25 16:38:17] [info] events.go:208 start thread to write redo/rollback sql into file
[2020/12/25 16:38:17] [info] binlogsyncer.go:360 begin to sync binlog from position (mysql-bin.000003, 15994082)
[2020/12/25 16:38:17] [info] stats_process.go:166 start thread to analyze statistics from binlog
[2020/12/25 16:38:17] [info] repl.go:15 start to get binlog from mysql
[2020/12/25 16:38:17] [info] binlogsyncer.go:777 rotate to (mysql-bin.000003, 15994082)
[2020/12/25 16:38:17] [info] events.go:242 finish processing mysql-bin.000003 16002473
[2020/12/25 16:38:22] [info] repl.go:83 deadline exceeded.
[2020/12/25 16:38:22] [info] repl.go:17 finish getting binlog from mysql
[2020/12/25 16:38:22] [info] stats_process.go:266 exit thread to analyze statistics from binlog
[2020/12/25 16:38:22] [info] events.go:183 exit thread 1 to generate redo/rollback sql
[2020/12/25 16:38:22] [info] events.go:183 exit thread 2 to generate redo/rollback sql
[2020/12/25 16:38:22] [info] events.go:257 finish writing rollback sql into tmp files, start to revert content order of tmp files
[2020/12/25 16:38:22] [info] rollback_process.go:15 start thread 1 to revert rollback sql files
[2020/12/25 16:38:22] [info] rollback_process.go:41 start to revert tmp file /tmp/my2sql_test/.rollback.3.sql into /tmp/my2sql_test/rollback.3.sql
[2020/12/25 16:38:22] [info] rollback_process.go:156 finish reverting tmp file /tmp/my2sql_test/.rollback.3.sql into /tmp/my2sql_test/rollback.3.sql
[2020/12/25 16:38:22] [info] rollback_process.go:25 exit thread 1 to revert rollback sql files
[2020/12/25 16:38:22] [info] events.go:270 finish reverting content order of tmp files
[2020/12/25 16:38:22] [info] events.go:275 exit thread to write redo/rollback sql into file
-- 查看生成的文件
04:40 PM dmp1 /tmp/my2sql_test# ll
total 1228
-rw-r--r-- 1 root root     251 Dec 25 16:38 biglong_trx.txt
-rw-r--r-- 1 root root     288 Dec 25 16:38 binlog_status.txt
-rw-r--r-- 1 root root 1246880 Dec 25 16:38 rollback.3.sql
## 其中rollback.x.sql就是我们闪回数据需要的sql文件（x对应mysql-binlog.00000x的文件编号x），由于执行命令时只指定了binlog开始的位置，实例中后续执行的DML事务也都会被记录
## 另外2个文件分别是从binlog中获取到的binlog状态和事务信息，之后的案例会详细展示说明，此处略过
-- 查看生成的回滚SQL文本文件
04:42 PM dmp1 /tmp/my2sql_test# tail -5 rollback.3.sql 
INSERT INTO `zlm`.`t` (`id`,`k`,`c`,`pad`) VALUES (4,5027,'54133149494-75722987476-23015721680-47254589498-40242947469-55055884969-23675271222-20181439230-74473404563-55407972672','88488171626-98596569412-94026374972-58040528656-38000028170');
INSERT INTO `zlm`.`t` (`id`,`k`,`c`,`pad`) VALUES (3,4990,'51185622598-89397522786-28007882305-52050087550-68686337807-48942386476-96555734557-05264042377-33586177817-31986479495','00592560354-80393027097-78244247549-39135306455-88936868384');
INSERT INTO `zlm`.`t` (`id`,`k`,`c`,`pad`) VALUES (2,5025,'13241531885-45658403807-79170748828-69419634012-13605813761-77983377181-01582588137-21344716829-87370944992-02457486289','28733802923-10548894641-11867531929-71265603657-36546888392');
INSERT INTO `zlm`.`t` (`id`,`k`,`c`,`pad`) VALUES (1,5015,'68487932199-96439406143-93774651418-41631865787-96406072701-20604855487-25459966574-28203206787-41238978918-19503783441','22195207048-70116052123-74140395089-76317954521-98694025897');
# datetime=2020-12-25_16:33:30 database=zlm table=t binlog=mysql-bin.000003 startpos=15994218 stoppos=16002473
05:10 PM dmp1 /tmp/my2sql_test# cat rollback.3.sql |grep "INSERT INTO"|wc -l
5000
## 可以看到，该闪回SQL文件中有5000个INSERT语句，正好对应之前删除的5000条记录
## 闪回SQL文件中的“# datetime=...”这行的内容就是加了参数-add-extrainfo后加入的附加信息，可以获取每个语句执行的具体时间和点位
## 在实际情况中，从binlog中解析出来的事务会很复杂，为了便于分析，建议加上过滤库、表的参数-databases和-tables，这样生成的SQL文件也会小很多
-- 数据恢复（将误删数据导入）
05:17 PM dmp1 (master) ~# mysql32 < /tmp/my2sql_test/rollback.3.sql
mysql: [Warning] Using a password on the command line interface can be insecure.
05:19 PM dmp1 (master) ~# mysql32 -Ne "select count(*) from zlm.t;checksum table zlm.t;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-------+
| 10000 |
+-------+
+-------+------------+
| zlm.t | 1966401574 |
+-------+------------+
## 5000条删除的数据导入表后，表的checksum与删除前一致，说明该在表上没有进行过其他DML操作
## 如果记录数一致而checksum不一致，则认为恢复后的数据仍然是不一致的，需要确认是否需要做更多的闪回操作`
#### 场景 2：手动补偿主从异常切换后的数据不一致
`-- 用sysbench给一个持续写入
01:34 AM dmp1 /usr/local/sysbench/share/sysbench# sysbench /usr/local/sysbench/share/sysbench/oltp_read_write.lua --db-driver=mysql --tables=1 --table_size=10000 --mysql-host=10.186.60.62 --mysql-port=3332 --mysql-db=zlm --mysql-user=zlm --mysql-password=zlm --report-interval=2 --threads=10 --time=600 --skip-trx=on --mysql-ignore-errors=1062,1213 --db-ps-mode=disable run
sysbench 1.0.17 (using bundled LuaJIT 2.1.0-beta2)
Running the test with following options:
Number of threads: 10
Report intermediate results every 2 second(s)
Initializing random number generator from current time
Initializing worker threads...
Threads started!
[ 2s ] thds: 10 tps: 712.84 qps: 12964.69 (r/w/o: 10095.03/2855.81/13.85) lat (ms,95%): 27.17 err/s: 5.44 reconn/s: 0.00
[ 4s ] thds: 10 tps: 733.05 qps: 13289.89 (r/w/o: 10342.52/2939.79/7.57) lat (ms,95%): 28.16 err/s: 4.54 reconn/s: 0.00
... 略
-- 确认从库正常复制后停止IO线程
mysql> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.186.60.62
                  Master_User: zlm
                  Master_Port: 3332
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000013
          Read_Master_Log_Pos: 60687481
               Relay_Log_File: relay-bin.000009
                Relay_Log_Pos: 60685775
        Relay_Master_Log_File: mysql-bin.000013
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
          Exec_Master_Log_Pos: 60685562
              Relay_Log_Space: 594023093
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 623332
                  Master_UUID: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e
             Master_Info_File: /data/mysql/mysql3332/data/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Reading event from the relay log
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:58752-915239
            Executed_Gtid_Set: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-915235
                Auto_Position: 1
         Replicate_Rewrite_DB: 
                 Channel_Name: 
           Master_TLS_Version: 
1 row in set (0.00 sec)
mysql> stop slave io_thread;
Query OK, 0 rows affected (0.01 sec)
mysql> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: 
                  Master_Host: 10.186.60.62
                  Master_User: zlm
                  Master_Port: 3332
                Connect_Retry: 60
              Master_Log_File:mysql-bin.000013
          Read_Master_Log_Pos: 78769827
               Relay_Log_File: relay-bin.000009
                Relay_Log_Pos: 78770040
        Relay_Master_Log_File: mysql-bin.000013
             Slave_IO_Running: No
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
          Exec_Master_Log_Pos:78769827
              Relay_Log_Space: 612105439
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: NULL
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 623332
                  Master_UUID: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e
             Master_Info_File: /data/mysql/mysql3332/data/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:58752-941653
            Executed_Gtid_Set: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-941653
                Auto_Position: 1
         Replicate_Rewrite_DB: 
                 Channel_Name: 
           Master_TLS_Version: 
1 row in set (0.00 sec)
-- 停止sysbench写入
[ 120s ] thds: 10 tps: 820.27 qps: 14836.91 (r/w/o: 11540.32/3284.59/12.00) lat (ms,95%): 22.28 err/s: 4.00 reconn/s: 0.00
[ 122s ] thds: 10 tps: 718.49 qps: 13009.74 (r/w/o: 10126.80/2874.44/8.50) lat (ms,95%): 24.83 err/s: 4.50 reconn/s: 0.00
[ 124s ] thds: 10 tps: 781.74 qps: 14178.87 (r/w/o: 11029.89/3137.97/11.00) lat (ms,95%): 23.52 err/s: 6.50 reconn/s: 0.00
^C
## 此时主库的数据是比从库多的（可以看作是异步复制中的IO线程延迟），假设又正好发生了高可用切换，从库被切成了主库，我们需要手动补偿新主上缺失的这部分数据（如果高可用切换工具没有这部分实现逻辑的话）
-- 确认后续（缺失）事务的起始点位
从show slave status的输出，我们可以获知以下信息：
1、新主已执行过的事务集合：
1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-941653
2、对应旧主上的点位：
Master_Log_File:mysql-bin.000013
Exec_Master_Log_Pos: 78769827
-- 查看旧主当前GTID信息
mysql> show master status;
+------------------+-----------+--------------+------------------+------------------------------------------------+
| File             | Position  | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                              |
+------------------+-----------+--------------+------------------+------------------------------------------------+
| mysql-bin.000013 | 151283749 |              |                  | 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-1047585 |
+------------------+-----------+--------------+------------------+------------------------------------------------+
1 row in set (0.00 sec)
## 相差了105932个事务，binlog从77M增长到150M左右
-- 也可以离线解析binlog文件来确认file+pos的点位与GTID是否是对应
/usr/local/mysql5732/bin/mysqlbinlog -vv --base64-output=decode-rows mysql-bin.000013|less
... 略
#201226  1:36:31 server id 623332  end_log_pos 78769827 CRC32 0xe5032fcf        Xid = 4003981
COMMIT/*!*/;
# at78769827   //当1d7ef0f4-4593-11eb-9f04-02000aba3c3e:941653的事务COMMIT后，pos点位就停在这里，是一致的
#201226  1:36:31 server id 623332  end_log_pos 78769892 CRC32 0x6cec07fc        GTID    last_committed=115069   sequence_number=115070  rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= '1d7ef0f4-4593-11eb-9f04-02000aba3c3e:941654'/*!*/;
# at 78769892
#201226  1:36:31 server id 623332  end_log_pos 78769963 CRC32 0x0b9b5557        Query   thread_id=89    exec_time=0     error_code=0
SET TIMESTAMP=1608917791/*!*/;
BEGIN
/*!*/;
# at 78769963
#201226  1:36:31 server id 623332  end_log_pos 78770228 CRC32 0x75e40978        Rows_query
# INSERT INTO sbtest1 (id, k, c, pad) VALUES (5020, 5013, '79652507036-05590009094-10370692577-33401396318-81508361252-10613546461-82822929332-17272183925-71915791860-00345159222', '25450417435-19336936168-49193845527-09907338597-56878802246')
# at 78770228
#201226  1:36:31 server id 623332  end_log_pos 78770284 CRC32 0xfc0d0d16        Table_map: `zlm`.`sbtest1` mapped to number 204
# at 78770284
#201226  1:36:31 server id 623332  end_log_pos 78770509 CRC32 0xe1d44365        Write_rows: table id 204 flags: STMT_END_F
### INSERT INTO `zlm`.`sbtest1`
### SET
###   @1=5020 /* INT meta=0 nullable=0 is_null=0 */
###   @2=5013 /* INT meta=0 nullable=0 is_null=0 */
###   @3='79652507036-05590009094-10370692577-33401396318-81508361252-10613546461-82822929332-17272183925-71915791860-00345159222' /* STRING(360) meta=61032 nullable=0 is_null=0 */
###   @4='25450417435-19336936168-49193845527-09907338597-56878802246' /* STRING(180) meta=65204 nullable=0 is_null=0 */
# at 78770509
#201226  1:36:31 server id 623332  end_log_pos 78770540 CRC32 0x1adbcf14        Xid = 4003993
COMMIT/*!*/;
# at 78770540
#201226  1:36:31 server id 623332  end_log_pos 78770605 CRC32 0x52d9646f        GTID    last_committed=115070   sequence_number=115071  rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= '1d7ef0f4-4593-11eb-9f04-02000aba3c3e:941655'/*!*/;
# at 78770605
#201226  1:36:31 server id 623332  end_log_pos 78770676 CRC32 0x7ed98e8d        Query   thread_id=85    exec_time=0     error_code=0
SET TIMESTAMP=1608917791/*!*/;
BEGIN
/*!*/;
# at 78770676
#201226  1:36:31 server id 623332  end_log_pos 78770738 CRC32 0x28584bc5        Rows_query
# UPDATE sbtest1 SET k=k+1 WHERE id=6248
-- 生成前滚SQL（从mysql-bin.000013的78769827开始）
01:55 PM dmp1 (master) ~# ./my2sql -user zlm -password zlm -host 10.186.60.62 -port 3332 -work-type 2sql -start-file mysql-bin.000013 -start-pos78769827 --add-extraInfo -output-dir /tmp/my2sql_test
[2020/12/26 01:54:51] [info] binlogsyncer.go:144 create BinlogSyncer with config {1113306 mysql 10.186.60.62 3332 zlm   utf8 false false <nil> false Local false 0 0s 0s 0 false false 0}
[2020/12/26 01:54:51] [info] binlogsyncer.go:360 begin to sync binlog from position (mysql-bin.000013, 78769827)
[2020/12/26 01:54:51] [info] events.go:208 start thread to write redo/rollback sql into file
[2020/12/26 01:54:51] [info] events.go:58 start thread 1 to generate redo/rollback sql
[2020/12/26 01:54:51] [info] events.go:58 start thread 2 to generate redo/rollback sql
[2020/12/26 01:54:51] [info] stats_process.go:166 start thread to analyze statistics from binlog
[2020/12/26 01:54:51] [info] repl.go:15 start to get binlog from mysql
[2020/12/26 01:54:51] [info] binlogsyncer.go:777 rotate to (mysql-bin.000013, 78769827)
[2020/12/26 01:54:51] [info] events.go:242 finish processing mysql-bin.000013 78770509
[2020/12/26 01:54:52] [info] events.go:242 finish processing mysql-bin.000013 89256973
[2020/12/26 01:54:53] [info] events.go:242 finish processing mysql-bin.000013 99742835
[2020/12/26 01:54:54] [info] events.go:242 finish processing mysql-bin.000013 110229245
[2020/12/26 01:54:55] [info] events.go:242 finish processing mysql-bin.000013 120715455
[2020/12/26 01:54:56] [info] events.go:242 finish processing mysql-bin.000013 131201391
[2020/12/26 01:54:57] [info] events.go:242 finish processing mysql-bin.000013 141687468
[2020/12/26 01:55:03] [info] repl.go:83 deadline exceeded.
[2020/12/26 01:55:03] [info] repl.go:17 finish getting binlog from mysql
[2020/12/26 01:55:03] [info] stats_process.go:266 exit thread to analyze statistics from binlog
[2020/12/26 01:55:03] [info] events.go:183 exit thread 1 to generate redo/rollback sql
[2020/12/26 01:55:03] [info] events.go:183 exit thread 2 to generate redo/rollback sql
[2020/12/26 01:55:03] [info] events.go:272 finish writing redo/forward sql into file
[2020/12/26 01:55:03] [info] events.go:275 exit thread to write redo/rollback sql into file
-- 检查生成的新文件
01:54 AM dmp1 /tmp/my2sql_test# ll -lrt
total 25732
-rw-r--r-- 1 root root      107 Dec 26 01:54 biglong_trx.txt
-rw-r--r-- 1 root root 26339348 Dec 26 01:55 forward.13.sql
-rw-r--r-- 1 root root      432 Dec 26 01:55 binlog_status.txt
01:56 AM dmp1 /tmp/my2sql_test# cat binlog_status.txt 
binlog            starttime           stoptime            startpos   stoppos    inserts  updates  deletes  database        table               
mysql-bin.000013  2020-12-26_01:36:31 2020-12-26_01:37:00 78770228   143726338  23713    47466    23715    zlm             sbtest1             
mysql-bin.000013  2020-12-26_01:37:01 2020-12-26_01:37:04 143726770  151283718  2755     5530     2753     zlm             sbtest1             
01:57 AM dmp1 /tmp/my2sql_test# cat biglong_trx.txt 
binlog            starttime           stoptime            startpos   stoppos    rows     duration   tables
-- 计算事务个数
01:57 AM dmp1 /tmp/my2sql_test# mysql -Ne "select 23713+47466+23715+2755+5530+2753;"
+--------+
| 105932 |
+--------+
02:01 AM dmp1 /tmp/my2sql_test# cat forward.13.sql |grep INSERT|wc -l
26468
02:03 AM dmp1 /tmp/my2sql_test# cat forward.13.sql |grep UPDATE|wc -l
52996
02:03 AM dmp1 /tmp/my2sql_test# cat forward.13.sql |grep DELETE|wc -l
26468
02:04 AM dmp1 /tmp/my2sql_test# mysql32 -Ne "select 26468+52996+26468;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------+
| 105932 |
+--------+
01:56 AM dmp1 /tmp/my2sql_test# scp forward.13.sql 10.186.60.68:/tmp
forward.13.sql                                                                                                                                               100%   25MB 140.9MB/s   00:00
## 前滚SQL文件有26M，拷贝到新主（60.68）
## 查看生成的binlog_status.txt文件，会统计每个时间段（POS）区间内相关库表所产生的DML次数
## biglong_trx.txt文件记录的是大/长事务，此文件为空，说明没有大/长事务
## 由文件中记录的DML总执行次数可知，确实是执行了105932 个事务，与之前估算的一致
-- 将差异数据导入新主
02:05 AM dmp2 (master) ~# mysql32 < /tmp/forward.13.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
02:05 AM dmp2 (master) ~#
-- 查看从库的事务写入情况
mysql> show slave status\G
... 略 
           Retrieved_Gtid_Set: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:58752-941653
            Executed_Gtid_Set: 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-941653,
3f4e72ab-46af-11eb-9bac-02000aba3c44:1-105932    //新主写入了105932个事务，与之前统计的值一致
                Auto_Position: 1
         Replicate_Rewrite_DB: 
                 Channel_Name: 
           Master_TLS_Version: 
1 row in set (0.00 sec)
-- 校验旧主和新主的测试表
## 旧主
mysql> checksum table sbtest1;
+-------------+-----------+
| Table       | Checksum  |
+-------------+-----------+
| zlm.sbtest1 | 670442058 |
+-------------+-----------+
1 row in set (0.01 sec)
## 新主
mysql> checksum table zlm.sbtest1;
+-------------+-----------+
| Table       | Checksum  |
+-------------+-----------+
| zlm.sbtest1 | 670442058 |
+-------------+-----------+
1 row in set (0.02 sec)
## 由于本次测试中仅仅是对sbtest1表执行了DML操作，可以认为新主缺失的数据已经得到补偿
## 在真实环境中，补偿数据可能会比较麻烦一些，因为会涉及到很多库表的操作，但原理是一样的`
#### 场景 3：在线事务分析
**3.1 准备**
`-- 创建一张500w行的大表并持续写入
02:38 AM dmp1 /usr/local/sysbench/share/sysbench# sysbench /usr/local/sysbench/share/sysbench/oltp_read_write.lua --db-driver=mysql --tables=1 --table_size=5000000 --mysql-host=10.186.60.68 --mysql-port=3332 --mysql-db=zlm --mysql-user=zlm --mysql-password=zlm --report-interval=2 --threads=10 --time=600 --skip-trx=on --mysql-ignore-errors=1062,1213 --db-ps-mode=disable prepare
sysbench 1.0.17 (using bundled LuaJIT 2.1.0-beta2)
Initializing worker threads...
Creating table 'sbtest1'...
Inserting 5000000 records into 'sbtest1'
... 略
-- 查看主从延迟
## 主库正在执行的事务
mysql> show master status;
+------------------+-----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
| File             | Position  | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                                                                             |
+------------------+-----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
| mysql-bin.000018 | 215205384 |              |                  | 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-941653,
3f4e72ab-46af-11eb-9bac-02000aba3c44:1-1335429 |
+------------------+-----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
## 从库回放状态
11:22 AM dmp1 (master) ~# mysql32 -e "show slave status\G"|grep Running |grep -v "Running_State"|awk '{print $2}' && mysql32 -e "show slave status\G"|grep Behind |awk '{print $2}'
mysql: [Warning] Using a password on the command line interface can be insecure.
Yes
Yes
mysql: [Warning] Using a password on the command line interface can be insecure.
0
## 此时并没有发现SQL线程有延迟（Senconds_Behind_Master=0）
-- 用my2sql工具分析mysql-bin.000018这个binlog
11:30 AM dmp1 (master) ~# ./my2sql -user zlm -password zlm -host 10.186.60.68 -port 3332 -work-type stats -start-file mysql-bin.000018 -start-pos 194 -output-dir /tmp/my2sql_test
[2020/12/28 11:30:35] [info] binlogsyncer.go:144 create BinlogSyncer with config {1113306 mysql 10.186.60.68 3332 zlm   utf8 false false <nil> false Local false 0 0s 0s 0 false false 0}
[2020/12/28 11:30:35] [info] binlogsyncer.go:360 begin to sync binlog from position (mysql-bin.000018, 194)
[2020/12/28 11:30:35] [info] stats_process.go:166 start thread to analyze statistics from binlog
[2020/12/28 11:30:35] [info] repl.go:15 start to get binlog from mysql
[2020/12/28 11:30:35] [info] binlogsyncer.go:777 rotate to (mysql-bin.000018, 194)
[2020/12/28 11:30:44] [info] repl.go:83 deadline exceeded.
[2020/12/28 11:30:44] [info] repl.go:17 finish getting binlog from mysql
[2020/12/28 11:30:44] [info] stats_process.go:266 exit thread to analyze statistics from binlog
-- 查看生成文件的内容
11:32 AM dmp1 /tmp/my2sql_test# cat binlog_status.txt 
binlog            starttime           stoptime            startpos   stoppos    inserts  updates  deletes  database        table               
mysql-bin.000018  2020-12-28_11:24:43 2020-12-28_11:25:12 390        40472959   14704    29399    14703    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:25:13 2020-12-28_11:25:42 40473397   83094395   15482    30964    15481    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:25:43 2020-12-28_11:26:12 83094627   124446683  15020    30043    15020    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:26:13 2020-12-28_11:26:42 124446910  165109718  14771    29540    14771    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:26:43 2020-12-28_11:27:12 165110068  205873372  14806    29615    14807    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:27:13 2020-12-28_11:27:19 205873604  215205353  3391     6778     3390     zlm             sbtest1             
11:32 AM dmp1 /tmp/my2sql_test# cat biglong_trx.txt 
binlog            starttime           stoptime            startpos   stoppos    rows     duration   tables
## 在18的binlog中写入了大量的事务，从11:24:43（390）开始，到11:27:19（215205353），由于没有指定停止的位置，打印的内容就截止到执行my2sql的时间点
`**3.2 大事务分析**`-- 将主库上测试表的主键删除
mysql> show create table sbtest1\G
*************************** 1. row ***************************
       Table: sbtest1
Create Table: CREATE TABLE `sbtest1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=5000001 DEFAULT CHARSET=utf8
1 row in set (0.01 sec)
mysql> alter table sbtest1 modify id int not null,drop primary key;
Query OK, 5000000 rows affected (1 min 33.31 sec)
Records: 5000000  Duplicates: 0  Warnings: 0
mysql> show create table sbtest1\G
*************************** 1. row ***************************
       Table: sbtest1
Create Table: CREATE TABLE `sbtest1` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
-- 主库执行删除400万行记录
mysql> select count(*) from sbtest1;
+----------+
| count(*) |
+----------+
|  5000000 |
+----------+
1 row in set (3.05 sec)
mysql> delete from sbtest1 where id<4000001;
Query OK, 4000000 rows affected (3 min 7.85 sec)
-- 确定主库当前事务执行到的点位
mysql> show master status;select @@server_uuid;
+------------------+----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                                                                             |
+------------------+----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
| mysql-bin.000019 |      194 |              |                  | 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-941653,
3f4e72ab-46af-11eb-9bac-02000aba3c44:1-1398898 |
+------------------+----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
+--------------------------------------+
| @@server_uuid                        |
+--------------------------------------+
| 3f4e72ab-46af-11eb-9bac-02000aba3c44 |
+--------------------------------------+
1 row in set (0.00 sec)
## 很明显，这是一个大事务，主库执行查询全表记录用了3s，执行删除400w行记录用了3.785s
## 因为要模拟主从延迟，先把测试表的主键删除，再进行数据删除
-- 查看主从延迟
12:57 PM dmp1 (master) ~# mysql32 -e "show slave status\G"|grep Running |grep -v "Running_State"|awk '{print $2}' && mysql32 -e "show slave status\G"|grep Behind |awk '{print $2}'
mysql: [Warning] Using a password on the command line interface can be insecure.
Yes
Yes
mysql: [Warning] Using a password on the command line interface can be insecure.
281
... 略
12:58 PM dmp1 (master) ~# mysql32 -e "show slave status\G"|grep Running |grep -v "Running_State"|awk '{print $2}' && mysql32 -e "show slave status\G"|grep Behind |awk '{print $2}'
mysql: [Warning] Using a password on the command line interface can be insecure.
Yes
Yes
mysql: [Warning] Using a password on the command line interface can be insecure.
441
## 现在已经开始出现延迟，并且Seconds_Behind_Master的值会越来越大（当主库上的表没有主键或唯一键时，从库回放时需要全表扫描来定位每一行记录，记录越多，这个过程越慢，最终导致主从延迟）
-- 执行my2sql，指定工作模式为事务分析（指定10000为大事务阈值）
01:10 PM dmp1 (master) ~# ./my2sql -user zlm -password zlm -host 10.186.60.68 -port 3332 -work-type stats -start-file mysql-bin.000018 -big-trx-row-limit 10000 -output-dir /tmp/my2sql_test
[2020/12/28 13:11:18] [info] stats_process.go:166 start thread to analyze statistics from binlog
[2020/12/28 13:11:18] [info] binlogsyncer.go:144 create BinlogSyncer with config {1113306 mysql 10.186.60.68 3332 zlm   utf8 false false <nil> false Local false 0 0s 0s 0 false false 0}
[2020/12/28 13:11:18] [info] binlogsyncer.go:360 begin to sync binlog from position (mysql-bin.000018, 4)
[2020/12/28 13:11:18] [info] repl.go:15 start to get binlog from mysql
[2020/12/28 13:11:18] [info] binlogsyncer.go:777 rotate to (mysql-bin.000018, 4)
[2020/12/28 13:11:27] [info] binlogsyncer.go:777 rotate to (mysql-bin.000019, 4)
[2020/12/28 13:11:27] [info] binlogsyncer.go:777 rotate to (mysql-bin.000019, 4)
[2020/12/28 13:11:32] [info] repl.go:83 deadline exceeded.
[2020/12/28 13:11:32] [info] repl.go:17 finish getting binlog from mysql
[2020/12/28 13:11:32] [info] stats_process.go:266 exit thread to analyze statistics from binlog
-- 查看生成的文件内容
01:13 PM dmp1 /tmp/my2sql_test# ll
total 8
-rw-r--r-- 1 root root  260 Dec 28 13:11 biglong_trx.txt
-rw-r--r-- 1 root root 1440 Dec 28 13:11 binlog_status.txt
01:13 PM dmp1 /tmp/my2sql_test# cat binlog_status.txt 
binlog            starttime           stoptime            startpos   stoppos    inserts  updates  deletes  database        table               
mysql-bin.000018  2020-12-28_11:24:43 2020-12-28_11:25:12 390        40472959   14704    29399    14703    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:25:13 2020-12-28_11:25:42 40473397   83094395   15482    30964    15481    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:25:43 2020-12-28_11:26:12 83094627   124446683  15020    30043    15020    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:26:13 2020-12-28_11:26:42 124446910  165109718  14771    29540    14771    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:26:43 2020-12-28_11:27:12 165110068  205873372  14806    29615    14807    zlm             sbtest1             
mysql-bin.000018  2020-12-28_11:27:13 2020-12-28_11:27:19 205873604  215205353  3391     6778     3390     zlm             sbtest1             
mysql-bin.000018  2020-12-28_12:37:02 2020-12-28_12:37:31 215205990  249240812  30410    11715    5787     sbtest          sbtest1             
mysql-bin.000018  2020-12-28_12:37:32 2020-12-28_12:37:40 249241253  260168297  7263     5533     2758     sbtest          sbtest1             
mysql-bin.000018  2020-12-28_12:53:51 2020-12-28_12:53:51 260168687  1023424583 0        0        4000000  zlm             sbtest1             
01:13 PM dmp1 /tmp/my2sql_test# cat biglong_trx.txt 
binlog            starttime           stoptime            startpos   stoppos    rows     duration   tables
mysql-bin.000018  2020-12-28_12:53:51 2020-12-28_12:53:51 260168556  1023424614 4000000  0          [zlm.sbtest1(inserts=0, updates=0, deletes=4000000)]
## 由于主库仍然在写mysql-bin.000018这个binlog文件，还未切换，我们继续以它为起始位置分析
## 执行命令的时候用了-big-trx-row-limit 10000来指定超过1w行的DML为大事务；如果不指定该参数，默认超过500行就会被统计
## 由生成的结果文件得知，在12:53:51的时候，在zml.sbtest1表上有一个deletes=4000000的大事务操作，与之前的操作相对应
`**3.3 长事务分析**`-- 创建一个测试表，显式开启10s事务
mysql> show master status;
+------------------+----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                                                                             |
+------------------+----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
| mysql-bin.000019 |      380 |              |                  | 1d7ef0f4-4593-11eb-9f04-02000aba3c3e:1-941653,
3f4e72ab-46af-11eb-9bac-02000aba3c44:1-1398899 |
+------------------+----------+--------------+------------------+-----------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> create table t1(id int);
Query OK, 0 rows affected (0.01 sec)
mysql> begin;
Query OK, 0 rows affected (0.00 sec)
mysql> insert into t1(id) values(1);select sleep(10);commit;
Query OK, 1 row affected (0.00 sec)
+-----------+
| sleep(10) |
+-----------+
|         0 |
+-----------+
1 row in set (10.00 sec)
Query OK, 0 rows affected (0.00 sec)
mysql> select count(*) from t1;
+----------+
| count(*) |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
-- 执行my2sql，工作模式选择事务分析（指定5s为长事务阈值）
02:03 PM dmp1 (master) ~# ./my2sql -user zlm -password zlm -host 10.186.60.68 -port 3332 -work-type stats -start-file mysql-bin.000019 -long-trx-seconds 5 -output-dir /tmp/my2sql_test
[2020/12/28 14:10:01] [info] binlogsyncer.go:144 create BinlogSyncer with config {1113306 mysql 10.186.60.68 3332 zlm   utf8 false false <nil> false Local false 0 0s 0s 0 false false 0}
[2020/12/28 14:10:01] [info] binlogsyncer.go:360 begin to sync binlog from position (mysql-bin.000019, 4)
[2020/12/28 14:10:01] [info] stats_process.go:166 start thread to analyze statistics from binlog
[2020/12/28 14:10:01] [info] repl.go:15 start to get binlog from mysql
[2020/12/28 14:10:01] [info] binlogsyncer.go:777 rotate to (mysql-bin.000019, 4)
[2020/12/28 14:10:06] [info] repl.go:83 deadline exceeded.
[2020/12/28 14:10:06] [info] repl.go:17 finish getting binlog from mysql
[2020/12/28 14:10:06] [info] stats_process.go:266 exit thread to analyze statistics from binlog
-- 查看生成的文件内容
02:10 PM dmp1 /tmp/my2sql_test# ll
total 8
-rw-r--r-- 1 root root 249 Dec 28 14:10 biglong_trx.txt
-rw-r--r-- 1 root root 288 Dec 28 14:10 binlog_status.txt
02:10 PM dmp1 /tmp/my2sql_test# cat binlog_status.txt 
binlog            starttime           stoptime            startpos   stoppos    inserts  updates  deletes  database        table               
mysql-bin.000019  2020-12-28_14:09:02 2020-12-28_14:09:02 728        812        1        0        0        zlm             t1                  
02:10 PM dmp1 /tmp/my2sql_test# cat biglong_trx.txt 
binlog            starttime           stoptime            startpos   stoppos    rows     duration   tables
mysql-bin.000019  2020-12-28_14:09:02 2020-12-28_14:09:12 605        843        1        10         [zlm.t1(inserts=1, updates=0, deletes=0)]
## 首先，确定事务开始的binlog位置为mysql-bin.000019，从这个文件开始解析
## 用参数-long-trx-seconds指定长事务的阈值为10s，只要超过这个值的事务就会被统计；如果不指定该参数，默认执行超过5min的事务会被统计，建议实际使用的时候指定这个参数，并设置较小的阈值进行分析
## 生成的统计文件中记录了刚才执行的10s事务（即zlm.t1表上的insert操作）`
## 限制
- my2sql 是模拟一个从库去在线获取主库 binlog，然后进行解析，因此执行操作的数据库用户需要具有 SELECT，REPLICATION SALVE，REPLICATION CLIENT 的权限。
- 与 binlog2sql、MyFlash 差不多，my2sql 目前也不支持 8.0；闪回功能需要开启 binlog_format=row，binlog_row_image=full；只能闪回 DML 操作，不支持 DDL 的闪回。
- 无法离线解析 binlog（MyFlash 支持）。
- 不能以 GTID 事务为单位进行解析（MyFlash 支持），具体 file+pos 点位需要先通过手工解析 binlog 后确认。
- 闪回/前滚 SQL 中，没有提供具体的 begin/commit 的位置，使用时无法分隔事务，需要人工判断。
- 使用事务分析功能时，只能给出具体的大/长事务发生时间、点位、涉及的对象和操作类型，不能给出具体的 SQL 语句，完整的语句仍然需要去 binlog 中进行查看（需设置 binlog_rows_query_log_events=on）
## 总结
- my2sql 是一款比较实用的 binlog 解析工具，除了能闪回 DML 的误操作外，还能通过生成前滚 SQL 进行数据补偿、利用事务分析功能来排查主从延迟问题、捕捉长时间不提交的事务等
- my2sql 基于 Go 语言编写，直接提供了 Linux 二进制版本，对环境无依赖，使用便捷
- my2sql 性能较好，解析 binlog 时生成闪回/前滚 SQL 的效率较高（对比 binlog2sql），作者号称能达到 50-60 倍左右，有兴趣的朋友可进行一轮性能对比测试
- MyFlash 解析 binlog 的效率也比 binlog2sql 高，但生成的回滚文件仍然是二进制格式的，需要依赖 mysqlbinlog 来进行处理，同时，也无法直观地对反解析后的回滚内容进行业务验证，my2sql 的出现正好弥补了这两者的不足
**文章推荐：**
[技术分享 | 如何优雅地在 Windows 上从 MySQL 5.6 升级到 5.7](https://opensource.actionsky.com/20200715-mysql/)
[技术分享 | 什么是半一致性读？](https://opensource.actionsky.com/20200623-mysql/)
[技术分享 | MySQL binlog 压缩功能对性能的影响](https://opensource.actionsky.com/202011119-mysql/)