# MySQL · Community · Congratulations on MySQL 8.0 GA

**Date:** 2018/05
**Source:** http://mysql.taobao.org/monthly/2018/05/01/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2018 / 05
 ](/monthly/2018/05)

 * 当期文章

 MySQL · Community · Congratulations on MySQL 8.0 GA
* MySQL · 社区动态 · Online DDL 工具 gh-ost 支持阿里云 RDS
* MySQL · 特性分析 · MySQL 8.0 资源组 (Resource Groups)
* MySQL · 引擎分析 · InnoDB行锁分析
* PgSQL · 特性分析 · 神奇的pg_rewind
* MSSQL · 最佳实践 · 阿里云RDS SQL自动化迁移上云的一种解决方案
* MongoDB · 引擎特性 · journal 与 oplog，究竟谁先写入？
* MySQL · RocksDB · MANIFEST文件介绍
* MySQL · 源码分析 · change master to
* PgSQL · 应用案例 · 阿里云 RDS PostgreSQL 高并发特性 vs 社区版本

 ## MySQL · Community · Congratulations on MySQL 8.0 GA 
 Author: 令猴 

 It’s great to see MySQL 8.0 has been GA. As a cloud provider in the world, Alibaba Cloud always keeps the pace with Oracle MySQL. We have provided ApsaraDB MySQL services based on MySQL 5.5, MySQL 5.6 and MySQL5.7. ApsaraDB MySQL services are the most popular for our customers. With MySQL 8.0 GA, we would like to start checking out the GA version and do some tests. Hope we can provide our service based on it soon.

MySQL 8.0 did a huge change. Not only so many new features were introduced but also basic structures such as redo log, undo tablespace etc. do a lot changes. Excellent work. Congratulations on Oracle MySQL team. Of course, such a huge change might give us some pressure on how to deal with upgrade. We will do some tests and see.

As a database service provider, it’s delighted to see MySQL 8.0 has a 1.8M QPS, which has a big performance improvement comparing to MySQL 5.7. UTF8mb4 makes MySQL support more and more character set. It’s also good to see NOWAIT idea from AliSQL has been admitted. There are so many new features we expected. Let’s take a look.

The biggest change in MySQL 8.0 is transactional system table. All of the system tables are stored in InnoDB storage engine. Such a movement can remove the replication problems caused by old MyISAM system tables, such as whole table lock thing etc. We truly believe we will easily develop more and more interesting features based on the transactional system table.

The atomic DDL has been expected for a long time. Before 8.0, DDL causes a lot of inconsistence problems during replication. Such a feature will make the DDL replication easier. This is a big enhancement. Someday, it’s better to see DDL to be transactional. Currently, in order solve this problem, we have to use some indirect solutions.

As you know, JSON is very popular for web users. The JSON_TABLE gives us a powerful way to convert between relational table and JSON. It’s an interesting feature. It will give the NOSQL users a new chance to move to MySQL.

Window functions and CTE are commonly used in other databases. Before 8.0, we always needs a complex work in order to simulate these things. Now, these two features will make our SQL life easier. They are so welcomed.

Histograms were introduced in MySQL 8.0 finally. We hope the cost model can work better. Currently, the histograms need to be created by user. It’s better to make it automatically.

More elegant hints are provided. So many new hints are introduced, which give the users more ways to adjust the query plan.

INVISIBLE Indexes is a very useful feature. It gives users another convenient method to test which query plan is good enough. It also gives the users a way to change the query plan to make one index invisible.

Error logs user defined filters make MySQL convenient to deal with the error log and show the interesting logs to users.

Performance schema is more and more powerful. We can get more internal detailed information in MySQL and monitor the MySQL behavior efficiently. Hope to see little performance regression if it turns on.

InnoDB storage plays more and more role in MySQL. We can see InnoDB does some big changes in MySQL 8.0. The new designed redo log and flexible undo tablespace management make InnoDB higher performance and concurrency.

As a MySQL contributor, the unified code style on server and InnoDB, refactored parser and optimizer make our development more convenient. We would always love to provide high qualified features to contribute MySQL community.

All in all, we can see MySQL is keeping optimizing the performance. We don’t list all the features we are interested in. However, from the above description, we can see the great effort Oracle MySQL did to make MySQL friendly to manage and use. We will do a lot of tests to see if the 8.0 is stable enough in short future. As we always doing, we will keep our focus on providing customers a safe, stable and high performance MySQL service.

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)