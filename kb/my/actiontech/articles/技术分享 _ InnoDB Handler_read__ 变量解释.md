# 技术分享 | InnoDB Handler_read_* 变量解释

**原文链接**: https://opensource.actionsky.com/20191031-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-31T00:53:41-08:00

---

> **作者：****高鹏**文章末尾有他著作的《深入理解 MySQL 主从原理 32 讲》，深入透彻理解 MySQL 主从，GTID 相关技术知识。源码版本：percona 5.7.14
本文为学习记录，可能有误请谅解。
**本文建议PC端观看，效果更佳。**
**一、Handler_read_* 值的实质**内部表示如下：- `{"Handler_read_first",       (char*) offsetof(STATUS_VAR, ha_read_first_count),     SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
- `{"Handler_read_key",         (char*) offsetof(STATUS_VAR, ha_read_key_count),       SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
- `{"Handler_read_last",        (char*) offsetof(STATUS_VAR, ha_read_last_count),      SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
- `{"Handler_read_next",        (char*) offsetof(STATUS_VAR, ha_read_next_count),      SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
- `{"Handler_read_prev",        (char*) offsetof(STATUS_VAR, ha_read_prev_count),      SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
- `{"Handler_read_rnd",         (char*) offsetof(STATUS_VAR, ha_read_rnd_count),       SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
- `{"Handler_read_rnd_next",    (char*) offsetof(STATUS_VAR, ha_read_rnd_next_count),  SHOW_LONGLONG_STATUS,    SHOW_SCOPE_ALL},`
实际上这些变量都是 MySQL 层定义出来的，因为 MySQL 可以包含多个存储引擎。因此这些值如何增加需要在引擎层的接口中自行实现，也就是说各个引擎都有自己的实现，在 MySQL 层进行汇总，因此这些值不是某个引擎特有的，打个比方如果有 Innodb 和 MyISAM 引擎，那么这些值是两个引擎的总和。本文将以 Innodb 为主要学习对象进行解释。
**二、各个值的解释**
**1. Handler_read_key**
- 内部表示：ha_read_key_count
- Innodb 更改接口：ha_innobase::index_read
- 文档解释：The number of requests to read a row based on a key. If this value is high, it is a good indication that your tables are properly indexed for your queries.
- 源码函数解释：Positions an index cursor to the index specified in the handle. Fetches the row if any.
- 作者解释：这个函数是访问索引的时候定位到值所在的位置用到的函数，因为必须要知道读取索引的开始位置才能向下访问。
**2. Handler_read_next**
- 
内部表示：ha_read_next_count
- 
Innodb 更改接口：ha_innobase::index_next_same
- 
ha_innobase::index_next
- 
文档解释：The number of requests to read the next row in key order.
- 
This value is incremented if you are querying an index column with a range constraint or if you are doing an index scan.
- 
源码函数解释：
- 
index_next &#8211; Reads the next row from a cursor, which must have previously been positioned using index_read.
- 
index_next_same &#8211; Reads the next row matching to the key value given as the parameter.
- 
作者解释：访问索引的下一条数据封装的 ha_innobase::general_fetch 函数，index_next_same 和 index_next 不同在于访问的方式不一样，比如范围 range 查询需要用到和索引全扫描也会用到 index_next，而 ref 访问方式会使用 index_next_same
**3. Handler_read_first**- 内部表示：ha_read_first_count
- Innodb 更改接口：ha_innobase::index_first
- 文档解释：The number of times the first entry in an index was read. If this value is high, it suggests that the server is doing a lot of full index scans; for example, SELECT col1 FROM foo, assuming that col1 is indexed
- 源码函数解释：Positions a cursor on the first record in an index and reads the corresponding row to buf.
- 作者解释：定位索引的第一条数据，实际上也是封装的** ha_innobase::index_read **函数(如全表扫描/全索引扫描调用)
**4. Handler_read_rnd_next**- 内部表示：ha_read_rnd_next_count
- Innodb 更改接口：ha_innobase::rnd_next
- 文档解释：The number of requests to read the next row in the data file. This value is high if you are doing a lot of table scans. Generally this suggests that your tables are not properly indexed or that your queries are not written to take advantage of the indexes you have.
- 源码函数解释：Reads the next row in a table scan (also used to read the FIRST row in a table scan).
- 作者解释：全表扫描访问下一条数据，实际上也是封装的 **ha_innobase::general_fetch**，在访问之前会调用 ha_innobase::index_first
**5. Handler_read_rnd**
- 内部表示：ha_read_rnd_count
- Innodb 更改接口：ha_innobase::rnd_pos
- Memory 更改接口：ha_heap::rnd_pos
- 文档解释：The number of requests to read a row based on a fixed position. This value is high if you are doing a lot of queries that require sorting of the result. You probably have a lot of queries that require MySQL to scan entire tables or you have joins that do not use keys properly.
- 作者解释：这个状态值在我测试期间只发现对临时表做排序的时候会用到，而且是 Memory 引擎的，具体只能按照文档理解了。
**6. 其他**
最后 2 个简单说一下
- **Handler_read_prev**
Innodb 接口为 ha_innobase::index_prev 访问索引的上一条数据，实际上也是封装的**ha_innobase::general_fetch** 函数，用于 ORDER BY DESC 索引扫描避免排序，内部状态值 ha_read_prev_count 增加。
- **Handler_read_last**
Innodb 接口为 ha_innobase::index_last 访问索引的最后一条数据作为定位，实际上也是封装的 **ha_innobase::index_read **函数，用于 ORDER BY DESC 索引扫描避免排序，内部状态值 ha_read_last_count 增加。
**三、常用查询测试**
**1. 测试用例**
- `mysql> show create table z1;`
- `+-------+-------------------------------------------------------------------------------------------------------------------------------------------+`
- `| Table | Create Table                                                                                                                              |`
- `+-------+-------------------------------------------------------------------------------------------------------------------------------------------+`
- `| z1    | CREATE TABLE `z1` (`
- `  `a` int(11) DEFAULT NULL,`
- `  `name` varchar(20) DEFAULT NULL,`
- `  KEY `a` (`a`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=latin1 |`
- `+-------+-------------------------------------------------------------------------------------------------------------------------------------------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> show create table z10;`
- `+-------+------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| Table | Create Table                                                                                                                                   |`
- `+-------+------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| z10   | CREATE TABLE `z10` (`
- `  `a` int(11) DEFAULT NULL,`
- `  `name` varchar(20) DEFAULT NULL,`
- `  KEY `a_idx` (`a`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=latin1 |`
- `+-------+------------------------------------------------------------------------------------------------------------------------------------------------+`
- `1 row in set (0.00 sec)`
- `mysql> select count(*) from z1;`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|    56415 |`
- `+----------+`
- `1 row in set (5.27 sec)`
- 
- `mysql> select count(*) from z10;`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|       10 |`
- `+----------+`
- `1 row in set (0.00 sec)`
**2. 全表扫描**
- `mysql> desc select * from z1;`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+-------+----------+-------+`
- `| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows  | filtered | Extra |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+-------+----------+-------+`
- `|  1 | SIMPLE      | z1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 56650 |   100.00 | NULL  |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+-------+----------+-------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql> pager cat >>/dev/null`
- `PAGER set to 'cat >>/dev/null'`
- `mysql> flush status;`
- `Query OK, 0 rows affected (0.10 sec)`
- `mysql> select * from z1;`
- `56415 rows in set (4.05 sec)`
- `mysql> pager;`
- `Default pager wasn't set, using stdout.`
- `mysql> show status like 'Handler_read%';`
- `+-----------------------+-------+`
- `| Variable_name         | Value |`
- `+-----------------------+-------+`
- `| Handler_read_first    | 1     |`
- `| Handler_read_key      | 1     |`
- `| Handler_read_last     | 0     |`
- `| Handler_read_next     | 0     |`
- `| Handler_read_prev     | 0     |`
- `| Handler_read_rnd      | 0     |`
- `| Handler_read_rnd_next | 56416 |`
- `+-----------------------+-------+`
- `7 rows in set (0.01 sec)`
Handler_read_first 增加 1 次用于初次定位，Handler_read_key 增加 1 次，Handler_read_rnd_next 增加扫描行数。我们前面说过因为 ha_innobase::index_first 也是封装的** ha_innobase::index_read **因此都需要 +1。
**3. 全索引扫描**
- `mysql> desc select a from z1;`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-------------+`
- `| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows  | filtered | Extra       |`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-------------+`
- `|  1 | SIMPLE      | z1    | NULL       | index | NULL          | a    | 5       | NULL | 56650 |   100.00 | Using index |`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-------------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql> flush status;`
- `Query OK, 0 rows affected (0.12 sec)`
- 
- `mysql> pager cat >>/dev/null`
- `PAGER set to 'cat >>/dev/null'`
- `mysql> select a from z1;`
- `56415 rows in set (4.57 sec)`
- 
- `mysql> pager`
- `Default pager wasn't set, using stdout.`
- `mysql> show status like 'Handler_read%';`
- `+-----------------------+-------+`
- `| Variable_name         | Value |`
- `+-----------------------+-------+`
- `| Handler_read_first    | 1     |`
- `| Handler_read_key      | 1     |`
- `| Handler_read_last     | 0     |`
- `| Handler_read_next     | 56415 |`
- `| Handler_read_prev     | 0     |`
- `| Handler_read_rnd      | 0     |`
- `| Handler_read_rnd_next | 0     |`
- `+-----------------------+-------+`
- `7 rows in set (0.01 sec)`
Handler_read_first 增加1次用于初次定位，Handler_read_key 增加 1 次，Handler_read_next 增加扫描行数用于连续访问接下来的行。我们前面说过因为 ha_innobase::index_first 也是封装的**ha_innobase::index_read** 因此都需要 +1。
**4. 索引 ref 访问**
我这里因为是测试索引全是等于 10 的加上了 force index
- `mysql>  desc select  * from z1 force index(a) where a=10;`
- `+----+-------------+-------+------------+------+---------------+------+---------+-------+-------+----------+-------+`
- `| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref   | rows  | filtered | Extra |`
- `+----+-------------+-------+------------+------+---------------+------+---------+-------+-------+----------+-------+`
- `|  1 | SIMPLE      | z1    | NULL       | ref  | a             | a    | 5       | const | 28325 |   100.00 | NULL  |`
- `+----+-------------+-------+------------+------+---------------+------+---------+-------+-------+----------+-------+`
- `1 row in set, 1 warning (0.01 sec)`
- 
- `mysql> flush status;`
- `Query OK, 0 rows affected (0.13 sec)`
- 
- `mysql> pager cat >>/dev/null`
- `PAGER set to 'cat >>/dev/null'`
- `mysql> select  * from z1 force index(a) where a=10;`
- `56414 rows in set (32.39 sec)`
- `mysql> pager`
- `Default pager wasn't set, using stdout.`
- `mysql> show status like 'Handler_read%';`
- `+-----------------------+-------+`
- `| Variable_name         | Value |`
- `+-----------------------+-------+`
- `| Handler_read_first    | 0     |`
- `| Handler_read_key      | 1     |`
- `| Handler_read_last     | 0     |`
- `| Handler_read_next     | 56414 |`
- `| Handler_read_prev     | 0     |`
- `| Handler_read_rnd      | 0     |`
- `| Handler_read_rnd_next | 0     |`
- `+-----------------------+-------+`
- `7 rows in set (0.06 sec)`
Handler_read_key 增加 1 次这是用于初次定位，Handler_read_next 增加扫描行数次数用于接下来的数据访问。
**5. 索引 range 访问**
- `mysql> desc select  * from z1 force index(a) where a>9 and a<12;`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-----------------------+`
- `| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows  | filtered | Extra                 |`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-----------------------+`
- `|  1 | SIMPLE      | z1    | NULL       | range | a             | a    | 5       | NULL | 28325 |   100.00 | Using index condition |`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-----------------------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql>  pager cat >>/dev/null`
- `PAGER set to 'cat >>/dev/null'`
- `mysql> select  * from z1 force index(a) where a>9 and a<12;`
- `56414 rows in set (47.54 sec)`
- `mysql> show status like 'Handler_read%';`
- `7 rows in set (0.03 sec)`
- `mysql>  pager`
- `Default pager wasn't set, using stdout.`
- `mysql> show status like 'Handler_read%';`
- `+-----------------------+-------+`
- `| Variable_name         | Value |`
- `+-----------------------+-------+`
- `| Handler_read_first    | 0     |`
- `| Handler_read_key      | 1     |`
- `| Handler_read_last     | 0     |`
- `| Handler_read_next     | 56414 |`
- `| Handler_read_prev     | 0     |`
- `| Handler_read_rnd      | 0     |`
- `| Handler_read_rnd_next | 0     |`
- `+-----------------------+-------+`
- `7 rows in set (0.02 sec)`
Handler_read_key 增加 1 次这是用于初次定位，Handler_read_next 增加扫描行数次数用于接下来的数据访问。
**6. 被驱动表带索引访问**
- `mysql> desc select * from z1 STRAIGHT_JOIN z10 force index(a_idx) on z1.a=z10.a;`
- `+----+-------------+-------+------------+------+---------------+-------+---------+-----------+-------+----------+-------------+`
- `| id | select_type | table | partitions | type | possible_keys | key   | key_len | ref       | rows  | filtered | Extra       |`
- `+----+-------------+-------+------------+------+---------------+-------+---------+-----------+-------+----------+-------------+`
- `|  1 | SIMPLE      | z1    | NULL       | ALL  | a             | NULL  | NULL    | NULL      | 56650 |   100.00 | Using where |`
- `|  1 | SIMPLE      | z10   | NULL       | ref  | a_idx         | a_idx | 5       | test.z1.a |    10 |   100.00 | NULL        |`
- `+----+-------------+-------+------------+------+---------------+-------+---------+-----------+-------+----------+-------------+`
- `2 rows in set, 1 warning (0.01 sec)`
- 
- `mysql> flush status;`
- `Query OK, 0 rows affected (0.47 sec)`
- 
- `mysql> pager cat >> /dev/null`
- `PAGER set to 'cat >> /dev/null'`
- `mysql>  select * from z1 STRAIGHT_JOIN z10 force index(a_idx) on z1.a=z10.a;`
- `112828 rows in set (1 min 21.21 sec)`
- 
- `mysql> pager`
- `Default pager wasn't set, using stdout.`
- `mysql>  show status like 'Handler_read%';`
- `+-----------------------+--------+`
- `| Variable_name         | Value  |`
- `+-----------------------+--------+`
- `| Handler_read_first    | 1      |`
- `| Handler_read_key      | 56416  |`
- `| Handler_read_last     | 0      |`
- `| Handler_read_next     | 112828 |`
- `| Handler_read_prev     | 0      |`
- `| Handler_read_rnd      | 0      |`
- `| Handler_read_rnd_next | 56416  |`
- `+-----------------------+--------+`
- `7 rows in set (0.00 sec)`
Handler_read_first 增加一次作为驱动表 z1 全表扫描定位的开始，接下来 Handler_read_rnd_next 扫描全部记录，每次扫描一次在 z10 表通过索引 a_idx 定位一次 Handler_read_key 增加 1 次，然后接下来进行索引 a_idx 进行数据查找 Handler_read_next 增加为扫描的行数。
**7. 索引避免排序正向和反向**
- `mysql>  flush status;`
- `Query OK, 0 rows affected (0.05 sec)`
- 
- `mysql> pager cat >> /dev/null`
- `PAGER set to 'cat >> /dev/null'`
- `mysql> select * from z1 force index(a) order by a;`
- `56415 rows in set (27.39 sec)`
- 
- `mysql> pager`
- `Default pager wasn't set, using stdout.`
- `mysql> show status like 'Handler_read%';`
- `+-----------------------+-------+`
- `| Variable_name         | Value |`
- `+-----------------------+-------+`
- `| Handler_read_first    | 1     |`
- `| Handler_read_key      | 1     |`
- `| Handler_read_last     | 0     |`
- `| Handler_read_next     | 56415 |`
- `| Handler_read_prev     | 0     |`
- `| Handler_read_rnd      | 0     |`
- `| Handler_read_rnd_next | 0     |`
- `+-----------------------+-------+`
- `7 rows in set (0.01 sec)`
- 
- `mysql> flush status;`
- `Query OK, 0 rows affected (0.10 sec)`
- 
- `mysql> desc  select * from z1 force index(a) order by a desc;`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-------+`
- `| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows  | filtered | Extra |`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-------+`
- `|  1 | SIMPLE      | z1    | NULL       | index | NULL          | a    | 5       | NULL | 56650 |   100.00 | NULL  |`
- `+----+-------------+-------+------------+-------+---------------+------+---------+------+-------+----------+-------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql> pager cat >> /dev/null`
- `PAGER set to 'cat >> /dev/null'`
- `mysql>  select * from z1 force index(a) order by a desc;`
- `56415 rows in set (24.94 sec)`
- 
- `mysql> pager`
- `Default pager wasn't set, using stdout.`
- `mysql>  show status like 'Handler_read%';`
- `+-----------------------+-------+`
- `| Variable_name         | Value |`
- `+-----------------------+-------+`
- `| Handler_read_first    | 0     |`
- `| Handler_read_key      | 1     |`
- `| Handler_read_last     | 1     |`
- `| Handler_read_next     | 0     |`
- `| Handler_read_prev     | 56415 |`
- `| Handler_read_rnd      | 0     |`
- `| Handler_read_rnd_next | 0     |`
- `+-----------------------+-------+`
- `7 rows in set (0.01 sec)`
不用过多解释，可以看到 Handler_read_last 和 Handler_read_prev 的用途。
**四、总结**- Handler_read_rnd_next 通常代表着全表扫描。
- Handler_read_first 通常代表着全表或者全索引扫描。
- Handler_read_next 通常代表着合理的使用了索引或者全索引扫描。
- Handler_read_key 不管全表全索引或者正确使用的索引实际上都会增加，只是一次索引定位而已。
- Innodb 中全表扫描也是主键的全索引扫描。
- 顺序访问的一条记录实际上都是调用 **ha_innobase::general_fetch **函数，另外一个功能 innodb_thread_concurrency 参数的功能就在里面实现，下次再说。
**五、参考栈帧**
- `全表扫描`
- 
- `mysql> desc select * from z1 ;`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+-------+----------+-------+`
- `| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+-------+----------+-------+`
- `| 1 | SIMPLE | z1 | NULL | ALL | NULL | NULL | NULL | NULL | 56650 | 100.00 | NULL |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+-------+----------+-------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `第一次:`
- `#0 row_search_mvcc (buf=0x7fff2ccc9380 "\377", mode=PAGE_CUR_G, prebuilt=0x7fff2cd4bb40, match_mode=0, direction=0)`
- `at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/row/row0sel.cc:4479`
- `#1 0x00000000019b3051 in ha_innobase::index_read (this=0x7fff2cd32480, buf=0x7fff2ccc9380 "\377", key_ptr=0x0, key_len=0, find_flag=HA_READ_AFTER_KEY)`
- `at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9104`
- `#2 0x00000000019b4374 in ha_innobase::index_first (this=0x7fff2cd32480, buf=0x7fff2ccc9380 "\377")`
- `at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9551`
- `#3 0x00000000019b462c in ha_innobase::rnd_next (this=0x7fff2cd32480, buf=0x7fff2ccc9380 "\377")`
- `at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9656`
- `#4 0x0000000000f66fa2 in handler::ha_rnd_next (this=0x7fff2cd32480, buf=0x7fff2ccc9380 "\377") at /root/mysql5.7.14/percona-server-5.7.14-7/sql/handler.cc:3099`
- `#5 0x00000000014c61b6 in rr_sequential (info=0x7fff2c0026a0) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/records.cc:520`
- `#6 0x000000000155f2a4 in join_init_read_record (tab=0x7fff2c002650) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:2481`
- `#7 0x000000000155c381 in sub_select (join=0x7fff2c001f70, qep_tab=0x7fff2c002650, end_of_records=false)`
- `at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:1271`
- `#8 0x000000000155bd`
最后推荐高鹏的专栏《深入理解MySQL主从原理 32讲》，想要透彻了解学习MySQL 主从原理的朋友不容错过。作者微信：gp_22389860
![](.img/0aff2ace.jpg)											
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
技术交流群，进群后可提问
QQ群（669663113）
社区通道，邮件&电话
osc@actionsky.com
现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
格式：.md/.doc/.txt
主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
要求：原创且未发布过
奖励：作者署名；200元京东E卡+社区周边
投稿方式：
邮箱：osc@actionsky.com
格式：[投稿]姓名+文章标题
以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系