# 新特性解读 | MySQL 8.0 语句摘要功能介绍

**原文链接**: https://opensource.actionsky.com/20200915-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-09-15T00:41:58-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**一、背景介绍**
在介绍 MySQL 8.0 的语句摘要函数之前，先来看看经典的慢日志过滤结果：
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`# mysqldumpslow  -s c -t 10 -g 'order by' debian-ytt1-slow.log``
``Reading mysql slow query log from debian-ytt1-slow.log``Count: 8  Time=10.41s (83s)  Lock=0.00s (0s)  Rows=2.0 (16), root[root]@localhost``  select * from p1 where id > N order by rand() limit N``
``Count: 2  Time=15.06s (30s)  Lock=0.00s (0s)  Rows=2.0 (4), root[root]@localhost``  select * from p1 where N order by rand() limit N``
``Count: 1  Time=6.35s (6s)  Lock=0.00s (0s)  Rows=2.0 (2), root[root]@localhost``  select * from p1 where id >N-N order by rand() limit N`
对慢日志进行过滤分析，按照执行次数排序，拿出前 10 条语句，比如第 1 条语句：
- 
`select * from p1 where id > N order by rand() limit N;`
这里的 N 代表数字，也就是说无论数字多少，都可以用这条语句来代替。举个例子，下面 3 条 SQL 都可以用上面的 SQL 来代替。
- 
- 
- 
- 
- 
`select * from p1 where id > 1000 order by rand() limit 2;``
``select * from p1 where id > 1000 order by rand() limit 10;``
``select * from p1 where id > 20000 order by rand() limit 100;`
用来代替这几条 SQL 的语句文本叫做**摘要文本**。
摘要文本提供了比较 SQL 语句不同分类的便利性。比如对于慢日志来说，用 mysqldumpslow 来分类查看慢语句结果就比直接看慢日志来的简单。
更进一步，如果语句很长，摘要文本也会很长，为了更加方便比较，MySQL 对摘要文本用哈希函数 SHA2 做了一个哈希，完了用此哈希值进行比较。这两个功能就是 MySQL 8.0 新增加的两个函数，statement_digest 和 statement_digest_text。
- statement_digest()：计算 SQL 语句的摘要哈希值。
- statement_digest_text()：返回 SQL 语句对应的摘要文本。
现在来用以上两个函数来计算下上面这 3 条 SQL 的摘要。结果和慢日志过滤分析的一样，不过数字 N 变为“?”，这 3 条语句为一个类型，摘要文本一样。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> select statement_digest_text('select * from p1 where id > 1000 order by rand() limit 2') digest_text;``+---------------------------------------------------------------+``| digest_text                                                   |``+---------------------------------------------------------------+``| SELECT * FROM `p1` WHERE `id` > ? ORDER BY `rand` ( ) LIMIT ? |``+---------------------------------------------------------------+``1 row in set (0.00 sec)``
``mysql> select statement_digest_text('select * from p1 where id > 1000 order by rand() limit 10') digest_text;``+---------------------------------------------------------------+``| digest_text                                                   |``+---------------------------------------------------------------+``| SELECT * FROM `p1` WHERE `id` > ? ORDER BY `rand` ( ) LIMIT ? |``+---------------------------------------------------------------+``1 row in set (0.00 sec)``
``mysql> select statement_digest_text('select * from p1 where id > 20000 order by rand() limit 100') digest_text;``+---------------------------------------------------------------+``| digest_text                                                   |``+---------------------------------------------------------------+``| SELECT * FROM `p1` WHERE `id` > ? ORDER BY `rand` ( ) LIMIT ? |``+---------------------------------------------------------------+``1 row in set (0.00 sec)`
对应的摘要哈希值：可以看到 3 条语句对应的摘要相同。所以在比较 3 条语句的执行次数，执行时间等指标时，可以用一个哈希值来比较。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> select statement_digest('select * from p1 where id > 1000 order by rand() limit 2') digest_has;``+------------------------------------------------------------------+``| digest_has                                                       |``+------------------------------------------------------------------+``| 32744c535a56acf37beb1702573cab41eff5f14953c9b1c2b73c7f1583e3eaf0 |``+------------------------------------------------------------------+``1 row in set (0.00 sec)``
``mysql> select statement_digest('select * from p1 where id > 1000 order by rand() limit 10') digest_hash;``+------------------------------------------------------------------+``| digest_hash                                                      |``+------------------------------------------------------------------+``| 32744c535a56acf37beb1702573cab41eff5f14953c9b1c2b73c7f1583e3eaf0 |``+------------------------------------------------------------------+``1 row in set (0.00 sec)``
``mysql> select statement_digest('select * from p1 where id > 20000 order by rand() limit 100') digest_hash;``+------------------------------------------------------------------+``| digest_hash                                                      |``+------------------------------------------------------------------+``| 32744c535a56acf37beb1702573cab41eff5f14953c9b1c2b73c7f1583e3eaf0 |``+------------------------------------------------------------------+``1 row in set (0.00 sec)`
摘要文本以及摘要哈希值的一致性来自于表或者过滤字段的不变性，如果表名或者过滤字段有变化，MySQL 将会归类这些查询语句为不同的摘要。
**二、 使用场景**
SQL 语句摘要可以用在MySQL的各个方面，比如 性能字典里对语句的分析，查询重写插件规则改写等等。
接下来依次看下语句摘要在这两方面的使用。
1. 性能字典
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> call sys.ps_setup_enable_consumer('statements');``+---------------------+``| summary             |``+---------------------+``| Enabled 4 consumers |``+---------------------+``1 row in set (0.00 sec)``
``Query OK, 0 rows affected (0.00 sec)`
开启后，执行几次之前的几条 SQL。
完后可以很方便的从 sys 库里分析这类语句的执行情况，包括执行次数，执行时间，扫描的记录数，锁定的时间，是否用到排序等等。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> SELECT * FROM sys.`statement_analysis` ``    > WHERE digest = statement_digest('select * from p1 where``    > id > 1000 order by rand() limit 2')\G``*************************** 1. row ***************************``           query: SELECT * FROM `p1` WHERE `id` > ? ORDER BY `rand` ( ) LIMIT ?``              db: ytt``       full_scan:``      exec_count: 4``       err_count: 0``      warn_count: 0``   total_latency: 46.08 s``     max_latency: 16.26 s``     avg_latency: 11.52 s``    lock_latency: 595.00 us``       rows_sent: 122``   rows_sent_avg: 31``   rows_examined: 36000126``rows_examined_avg: 9000032``   rows_affected: 0``rows_affected_avg: 0``      tmp_tables: 0`` tmp_disk_tables: 0``     rows_sorted: 122``sort_merge_passes: 0``          digest: 32744c535a56acf37beb1702573cab41eff5f14953c9b1c2b73c7f1583e3eaf0``      first_seen: 2020-08-17 13:34:58.676034``       last_seen: 2020-08-17 13:40:02.082039``1 row in set (0.00 sec)`
2.  查询重写插件
比如要阻止对表 p1 通过字段 r1 的删除动作，可以用查询重写插件在 MySQL 语句分析层直接转换，这时候就得用到摘要函数 statement_digest_text。
假设：表 p1 字段 id 值全部为正。
- 
`delete from p1 where id = 1000;`
要改写为，
- 
`delete from p1 where id = -1;`
利用函数 statement_digest_text 来定制这条 SQL 的重写规则。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> INSERT INTO query_rewrite.rewrite_rules (pattern, replacement,pattern_database)``   -> VALUES(``   -> statement_digest_text('delete from p1 where id = 1000') ,``   -> statement_digest_text('delete from p1 where id = -1'),``   -> 'ytt'``   -> );``Query OK, 1 row affected (0.01 sec)``
``mysql> CALL query_rewrite.flush_rewrite_rules();``Query OK, 1 row affected (0.02 sec)``
``mysql> select * from query_rewrite.rewrite_rules\G``*************************** 1. row ***************************``               id: 1``          pattern: DELETE FROM `p1` WHERE `id` = ?`` pattern_database: ytt``      replacement: DELETE FROM `p1` WHERE `id` = - ?``          enabled: YES``          message: NULL``   pattern_digest: a09b20197de495d603324d6ed617cb5d05fa0e3011bea8e9db7d2939df22940a``normalized_pattern: delete from `ytt`.`p1` where (`id` = ?)``1 row in set (0.00 sec)`
语句被查询重写后的效果：
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> delete from p1 where id = 20000;``Query OK, 0 rows affected, 1 warning (0.00 sec)``
``mysql> show warnings\G``*************************** 1. row ***************************`` Level: Note``  Code: 1105``Message: Query 'delete from p1 where id = 20000' rewritten to 'DELETE FROM `p1` WHERE `id` = - 20000' by a query rewrite plugin``1 row in set (0.00 sec)``
``mysql> select count(*) from p1;``+----------+``| count(*) |``+----------+``|  9000001 |``+----------+``1 row in set (1.59 sec)`
**总结**
MySQL 8.0 新增的语句摘要函数可以很方便的分析 SQL 语句执行的各个方面，比以前分析类似的场景要简单的多。
相关推荐：
[新特性解读 | mysql 8.0 memcached api 新特性](https://opensource.actionsky.com/20200706-mysql/)
[新特性解读 | GROUPING() 函数用法解析](https://opensource.actionsky.com/20200810-mysql/)