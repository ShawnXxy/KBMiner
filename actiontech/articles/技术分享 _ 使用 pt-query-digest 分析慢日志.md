# 技术分享 | 使用 pt-query-digest 分析慢日志

**原文链接**: https://opensource.actionsky.com/20200922-percona/
**分类**: 技术干货
**发布时间**: 2020-09-22T00:34:13-08:00

---

作者：张伟
爱可生北京分公司 DBA 团队成员，负责 MySQL 日常问题处理和 DMP 产品维护。喜爱技术和开源数据库，喜爱运动、读书、电影，花草树木。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**pt-query-digest 简介**
子曰：“工欲善其事，必先利其器”善于利用好的性能分析工具可以使运维效率事半功倍。pt-query-digest 属于 Percona Toolkit 工具集中较为常用的工具，用于分析 slow log，可以分析 MySQL 数据库的 binary log 、 general log 日志，同时也可以使用 show processlist 或从 tcpdump 抓取的 MySQL 协议数据来进行分析。
## 部署  Percona Toolkit 
下载最新版本的  Percona Toolkit - 
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
`[root@xxx ~]# wget https://www.percona.com/downloads/percona-toolkit/3.2.1/binary/redhat/7/x86_64/percona-toolkit-3.2.1-1.el7.x86_64.rpm``--2020-09-02 06:44:43--  https://www.percona.com/downloads/percona-toolkit/3.2.1/binary/redhat/7/x86_64/percona-toolkit-3.2.1-1.el7.x86_64.rpm``Resolving www.percona.com (www.percona.com)... 74.121.199.234``Connecting to www.percona.com (www.percona.com)|74.121.199.234|:443... connected.``HTTP request sent, awaiting response... 200 OK``Length: 17397876 (17M) [application/x-redhat-package-manager]``Saving to: ‘percona-toolkit-3.2.1-1.el7.x86_64.rpm’``
``100%[=====================================================================================================================================================>] 17,397,876  68.3KB/s   in 2m 37s``
``2020-09-02 06:47:27 (108 KB/s) - ‘percona-toolkit-3.2.1-1.el7.x86_64.rpm’ saved [17397876/17397876]``
``[root@xxx ~]# ls | grep percona-toolkit-3.2.1-1.el7.x86_64.rpm``percona-toolkit-3.2.1-1.el7.x86_64.rpm`
PT 工具是使用 Perl 语言编写和执行的，所以需要系统中有 Perl 环境。安装相关的依赖包，- 
- 
- 
- 
- 
```
[root@xxx ~]# yum install perl-DBI.x86_64`[root@xxx ~]# yum install perl-DBD-MySQL.x86_64``[root@xxx ~]# yum install perl-IO-Socket-SSL.noarch``[root@xxx ~]# yum install perl-Digest-MD5.x86_64``[root@xxx ~]# yum install perl-TermReadKey.x86_64
```
安装 Percona Toolkit - 
- 
- 
- 
- 
- 
- 
```
[root@xxx ~]# rpm -iv percona-toolkit-3.2.1-1.el7.x86_64.rpm``warning: percona-toolkit-3.2.1-1.el7.x86_64.rpm: Header V4 RSA/SHA256 Signature, key ID 8507efa5: NOKEY``Preparing packages...``percona-toolkit-3.2.1-1.el7.x86_64``
``[root@xxx ~]# rpm -qa | grep percona``percona-toolkit-3.2.1-1.el7.x86_64
```
工具目录安装路径：/usr/bin
## 检查慢日志的相关配置
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
mysql> show variables like '%slow%';``+---------------------------+-------------------------------------+``| Variable_name             | Value                               |``+---------------------------+-------------------------------------+``| log_slow_admin_statements | ON                                  |``| log_slow_slave_statements | ON                                  |``| slow_launch_time          | 2                                   |``| slow_query_log            | ON                                  |``| slow_query_log_file       | /opt/mysql/data/7777/mysql-slow.log |``+---------------------------+-------------------------------------+``5 rows in set (0.01 sec)``
``mysql> show variables like 'long_query_time';``+-----------------+----------+``| Variable_name   | Value    |``+-----------------+----------+``| long_query_time | 1.000000 |``+-----------------+----------+``1 row in set (0.01 sec)`
![](https://opensource.actionsky.com/wp-content/uploads/2020/09/表格1-1-1024x206.png)											
由于更好测试慢日志文件的输出，此处将慢日志执行时间阈值调小。
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
```
mysql>  set global long_query_time=0.001000;`Query OK, 0 rows affected (0.00 sec)``
``mysql> show variables like 'long_query_time';``+-----------------+----------+``| Variable_name   | Value    |``+-----------------+----------+``| long_query_time | 0.001000 |``+-----------------+----------+``1 row in set (0.00 sec)
```
## pt-query-digest 分析慢日志
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
- 
- 
- 
- 
- 
- 
```
[root@xxx 7777]# pt-query-digest   mysql-slow.log``
``# 3.6s user time, 100ms system time, 32.64M rss, 227.52M vsz``# Current date: Wed Sep  2 11:22:34 2020``# Hostname: xxx``# Files: mysql-slow.log``# Overall: 37.46k total, 17 unique, 576.26 QPS, 5.58x concurrency ________``# Time range: 2020-09-02T11:21:24 to 2020-09-02T11:22:29``# Attribute          total     min     max     avg     95%  stddev  median``# ============     ======= ======= ======= ======= ======= ======= =======``# Exec time           363s     1ms   183ms    10ms    23ms     8ms     8ms``# Lock time             1s       0    34ms    35us    38us   603us       0``# Rows sent        182.14k       0     100    4.98    0.99   21.06       0``# Rows examine     491.83k       0   1.02k   13.45   97.36   56.85       0``# Query size        19.82M       5 511.96k  554.80   72.65  16.25k    5.75``
``# Profile``# Rank Query ID                      Response time  Calls R/Call V/M   Ite``# ==== ============================= ============== ===== ====== ===== ===``#    1 0xFFFCA4D67EA0A788813031B8... 328.2315 90.4% 30520 0.0108  0.01 COMMIT``#    2 0xB2249CB854EE3C2AD30AD7E3...   8.0186  2.2%  1208 0.0066  0.01 UPDATE sbtest?``#    3 0xE81D0B3DB4FB31BC558CAEF5...   6.6346  1.8%  1639 0.0040  0.01 SELECT sbtest?``#    4 0xDDBF88031795EC65EAB8A8A8...   5.5093  1.5%   756 0.0073  0.02 DELETE sbtest?``# MISC 0xMISC                         14.6011  4.0%  3334 0.0044   0.0 <13 ITEMS>``
``# Query 1: 1.02k QPS, 10.94x concurrency, ID 0xFFFCA4D67EA0A788813031B8BBC3B329 at byte 26111916``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.01``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:29``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count         81   30520``# Exec time     90    328s     1ms   129ms    11ms    23ms     8ms     9ms``# Lock time      0       0       0       0       0       0       0       0``# Rows sent      0       0       0       0       0       0       0       0``# Rows examine   0       0       0       0       0       0       0       0``# Query size     0 178.83k       6       6       6       6       0       6``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  ###########################################################``# 100ms  #``#    1s``#  10s+``COMMIT\G``
``# Query 2: 41.66 QPS, 0.28x concurrency, ID 0xB2249CB854EE3C2AD30AD7E3079ABCE7 at byte 24161590``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.01``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:28``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count          3    1208``# Exec time      2      8s     1ms   115ms     7ms    24ms     9ms     3ms``# Lock time     38   518ms    17us    34ms   428us    73us     2ms    36us``# Rows sent      0       0       0       0       0       0       0       0``# Rows examine   0   1.18k       1       1       1       1       0       1``# Query size     0  46.01k      39      39      39      39       0      39``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  ##############``# 100ms  #``#    1s``#  10s+``# Tables``#    SHOW TABLE STATUS FROM `test` LIKE 'sbtest1'\G``#    SHOW CREATE TABLE `test`.`sbtest1`\G``UPDATE sbtest1 SET k=k+1 WHERE id=50313\G``# Converted for EXPLAIN``# EXPLAIN /*!50100 PARTITIONS*/``select  k=k+1 from sbtest1 where  id=50313\G``
``# Query 3: 56.52 QPS, 0.23x concurrency, ID 0xE81D0B3DB4FB31BC558CAEF5F387E929 at byte 22020829``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.01``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:28``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count          4    1639``# Exec time      1      7s     1ms    61ms     4ms    14ms     5ms     2ms``# Lock time      3    45ms    11us   958us    27us    44us    30us    23us``# Rows sent      0   1.60k       1       1       1       1       0       1``# Rows examine   0   1.60k       1       1       1       1       0       1``# Query size     0  57.62k      36      36      36      36       0      36``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  ######``# 100ms``#    1s``#  10s+``# Tables``#    SHOW TABLE STATUS FROM `test` LIKE 'sbtest1'\G``#    SHOW CREATE TABLE `test`.`sbtest1`\G``# EXPLAIN /*!50100 PARTITIONS*/``SELECT c FROM sbtest1 WHERE id=61690\G``
``# Query 4: 26.07 QPS, 0.19x concurrency, ID 0xDDBF88031795EC65EAB8A8A8BEEFF705 at byte 21045172``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.02``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:28``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count          2     756``# Exec time      1      6s     1ms   104ms     7ms    26ms    10ms     3ms``# Lock time     18   252ms    13us    19ms   333us    54us     2ms    26us``# Rows sent      0       0       0       0       0       0       0       0``# Rows examine   0     756       1       1       1       1       0       1``# Query size     0  25.10k      34      34      34      34       0      34``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  #################``# 100ms  #``#    1s``#  10s+``# Tables``#    SHOW TABLE STATUS FROM `test` LIKE 'sbtest1'\G``#    SHOW CREATE TABLE `test`.`sbtest1`\G``DELETE FROM sbtest1 WHERE id=50296\G``# Converted for EXPLAIN``# EXPLAIN /*!50100 PARTITIONS*/``select * from  sbtest1 WHERE id=50296\G
```
## 分析 pt-query-digest 输出结果
第一部分：输出结果的总体信息- 
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
```
# 3.6s user time, 100ms system time, 32.64M rss, 227.52M vsz ``说明：``执行过程中在用户中所花费的所有时间``执行过程中内核空间中所花费的所有时间``pt-query-digest进程所分配的内存大小``pt-query-digest进程所分配的虚拟内存大小``
``# Current date: Wed Sep  2 11:22:34 2020 ``说明：当前日期``
``# Hostname: xxx``说明：执行pt-query-digest的主机名``
``# Files: mysql-slow.log``说明：被分析的文件名``
``# Overall: 37.46k total, 17 unique, 576.26 QPS, 5.58x concurrency ________``说明：语句总数量，唯一语句数量，每秒查询量，查询的并发``
``# Time range: 2020-09-02T11:21:24 to 2020-09-02T11:22:29``说明：执行过程中日志记录的时间范围``
``# Attribute          total     min     max     avg     95%  stddev  median``说明：属性           总计     最小值  最大值  平均值   95%  标准差  中位数``# ============     ======= ======= ======= ======= ======= ======= =======``
``# Exec time           363s     1ms   183ms    10ms    23ms     8ms     8ms``说明：执行时间``# Lock time             1s       0    34ms    35us    38us   603us       0``说明：锁占用时间``# Rows sent        182.14k       0     100    4.98    0.99   21.06       0``说明：发送到客户端的行数``# Rows examine     491.83k       0   1.02k   13.45   97.36   56.85       0``说明：扫描的语句行数``# Query size        19.82M       5 511.96k  554.80   72.65  16.25k    5.75 ``说明：查询的字符数
```
第二部分：输出队列组的统计信息
- 
- 
- 
- 
- 
- 
- 
- 
- 
# Profile``说明：简况``# Rank Query ID                      Response time  Calls R/Call V/M   Ite``# ==== ============================= ============== ===== ====== ===== ===``#    1 0xFFFCA4D67EA0A788813031B8... 328.2315 90.4% 30520 0.0108  0.01 COMMIT``#    2 0xB2249CB854EE3C2AD30AD7E3...   8.0186  2.2%  1208 0.0066  0.01 UPDATE sbtest?``#    3 0xE81D0B3DB4FB31BC558CAEF5...   6.6346  1.8%  1639 0.0040  0.01 SELECT sbtest?``#    4 0xDDBF88031795EC65EAB8A8A8...   5.5093  1.5%   756 0.0073  0.02 DELETE sbtest?``# MISC 0xMISC                         14.6011  4.0%  3334 0.0044   0.0 <13 ITEMS>`
![](https://opensource.actionsky.com/wp-content/uploads/2020/09/表格2-1.png)											
第三部分：输出每列查询的详细信息
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
`# Query 1: 1.02k QPS, 10.94x concurrency, ID 0xFFFCA4D67EA0A788813031B8BBC3B329 at byte 26111916``说明：查询队列1：每秒查询量，查询的并发，队列1的ID值，26111916：表示文中偏移量（查看方法在下面‘偏1’中）``
``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.01``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:29``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count         81   30520``# Exec time     90    328s     1ms   129ms    11ms    23ms     8ms     9ms``# Lock time      0       0       0       0       0       0       0       0``# Rows sent      0       0       0       0       0       0       0       0``# Rows examine   0       0       0       0       0       0       0       0``# Query size     0 178.83k       6       6       6       6       0       6``说明：查询的详细说明，在第一部分/第二部分有相关参数说明``# String:``# Databases    test``说明：使用的数据库名称``# Hosts        10.186.60.147``说明：使用的主机IP``# Users        root``说明：使用的用户名``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  ###########################################################``# 100ms  #``#    1s``#  10s+``说明：查询时间分布``COMMIT\G``说明：执行的慢语句信息``# Query 2: 41.66 QPS, 0.28x concurrency, ID 0xB2249CB854EE3C2AD30AD7E3079ABCE7 at byte 24161590``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.01``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:28``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count          3    1208``# Exec time      2      8s     1ms   115ms     7ms    24ms     9ms     3ms``# Lock time     38   518ms    17us    34ms   428us    73us     2ms    36us``# Rows sent      0       0       0       0       0       0       0       0``# Rows examine   0   1.18k       1       1       1       1       0       1``# Query size     0  46.01k      39      39      39      39       0      39``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  ##############``# 100ms  #``#    1s``#  10s+``# Tables``#    SHOW TABLE STATUS FROM `test` LIKE 'sbtest1'\G``#    SHOW CREATE TABLE `test`.`sbtest1`\G``UPDATE sbtest1 SET k=k+1 WHERE id=50313\G``# Converted for EXPLAIN``# EXPLAIN /*!50100 PARTITIONS*/``select  k=k+1 from sbtest1 where  id=50313\G``
``# Query 3: 56.52 QPS, 0.23x concurrency, ID 0xE81D0B3DB4FB31BC558CAEF5F387E929 at byte 22020829``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.01``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:28``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count          4    1639``# Exec time      1      7s     1ms    61ms     4ms    14ms     5ms     2ms``# Lock time      3    45ms    11us   958us    27us    44us    30us    23us``# Rows sent      0   1.60k       1       1       1       1       0       1``# Rows examine   0   1.60k       1       1       1       1       0       1``# Query size     0  57.62k      36      36      36      36       0      36``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  ######``# 100ms``#    1s``#  10s+``# Tables``#    SHOW TABLE STATUS FROM `test` LIKE 'sbtest1'\G``#    SHOW CREATE TABLE `test`.`sbtest1`\G``# EXPLAIN /*!50100 PARTITIONS*/``SELECT c FROM sbtest1 WHERE id=61690\G``
``# Query 4: 26.07 QPS, 0.19x concurrency, ID 0xDDBF88031795EC65EAB8A8A8BEEFF705 at byte 21045172``# This item is included in the report because it matches --limit.``# Scores: V/M = 0.02``# Time range: 2020-09-02T11:21:59 to 2020-09-02T11:22:28``# Attribute    pct   total     min     max     avg     95%  stddev  median``# ============ === ======= ======= ======= ======= ======= ======= =======``# Count          2     756``# Exec time      1      6s     1ms   104ms     7ms    26ms    10ms     3ms``# Lock time     18   252ms    13us    19ms   333us    54us     2ms    26us``# Rows sent      0       0       0       0       0       0       0       0``# Rows examine   0     756       1       1       1       1       0       1``# Query size     0  25.10k      34      34      34      34       0      34``# String:``# Databases    test``# Hosts        10.186.60.147``# Users        root``# Query_time distribution``#   1us``#  10us``# 100us``#   1ms  ################################################################``#  10ms  #################``# 100ms  #``#    1s``#  10s+``# Tables``#    SHOW TABLE STATUS FROM `test` LIKE 'sbtest1'\G``#    SHOW CREATE TABLE `test`.`sbtest1`\G``DELETE FROM sbtest1 WHERE id=50296\G``# Converted for EXPLAIN``# EXPLAIN /*!50100 PARTITIONS*/``select * from  sbtest1 WHERE id=50296\G`
偏 1：
可以利用偏移量在慢查询日志文件中到查找到具体的 SQL 语句，查找方法如下：- 
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
`[root@xxx 7777]# tail -c +26111916 ./mysql-slow.log | head``# Time: 2020-09-02T11:22:21.062995-00:00``# User@Host: root[root] @  [10.186.60.147]  Id:  1177``# Query_time: 0.128524  Lock_time: 0.000000 Rows_sent: 0  Rows_examined: 0``SET timestamp=1599045741;``COMMIT;``# Time: 2020-09-02T11:22:21.063202-00:00``# User@Host: root[root] @  [10.186.60.147]  Id:  1179``# Query_time: 0.126925  Lock_time: 0.000000 Rows_sent: 0  Rows_examined: 0``SET timestamp=1599045741;``COMMIT;` 在生产环境中，可根据输出的慢 SQL 详情进行合理的语句调整。
## 参考文档
- https://www.percona.com/doc/percona-toolkit/LATEST/pt-query-digest.html
- https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html
小女不才，如有不足欢迎指正，告辞。
相关推荐：
[技术分享 | MySQL 监控利器之 Pt-Stalk](https://opensource.actionsky.com/20200522-mysql/)
[技术分享 | Xtrabackup 备份中 Xtrabackup_binlog_info 文件记录的 GTID 信息是否准确？](https://opensource.actionsky.com/20200309-mysql/)
[技术分享 | Percona Toolkit 使用场景分享](https://opensource.actionsky.com/20190108-percona/)