# 技术分享 | MySQL 史上最快逻辑备份工具

**原文链接**: https://opensource.actionsky.com/20200804-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-08-03T19:17:54-08:00

---

作者：洪斌
爱可生南区负责人兼技术服务总监，MySQL  ACE，擅长数据库架构规划、故障诊断、性能优化分析，实践经验丰富，帮助各行业客户解决 MySQL 技术问题，为金融、运营商、互联网等行业客户提供 MySQL 整体解决方案。
本文来源：转载自公众号-玩转MySQL
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL Shell 8.0.21 增加了一种新的逻辑备份恢复方法，有更快的备份恢复效率，支持zstd实时压缩，支持分块并行导出，load data并行导入，还能备份到OCI的对象存储。
- **util.dumpInstance() 用于备份整个实例**
- **util.dumpSchemas()** 用于**备份指定schema**
- **util.loadDump() 用于恢复备份**
做了个对比测试，在零负载下mysql配置参数不变，备份/恢复相同 schema，其中混合了大表和小表，看下这几种方式的实际效果如何。
**对比结果**
![](https://opensource.actionsky.com/wp-content/uploads/2020/08/微信截图_20200804110351.png)											
**结论**
- mysql shell
使用默认参数zstd压缩+32M chunk并行导出，恢复时单表可以并行load data，其备份和恢复速度均优于非压缩+非分块。测试中发现，若禁用压缩，也会禁用分块。
-  mysqldump
备份和恢复都是单线程执行，不压缩的备份效率更快，zstd的实时备份速度比gzip更快，恢复速度最慢。
- mysqlpump 
备份支持并行速度也很快，但是单线程恢复是硬伤。
- mydumper 
默认用gzip协议，备份速度与mysqldump基本一样，看来瓶颈在压缩上。在非压缩非分块备份速度会更快。恢复速度中等，单表无法并行。
综合上述测试结果，mysql shell新的备份恢复方式是最快的，得益于使用了zstd实时压缩算法，备份恢复均可以并行，对于单个大表也可以并行。
下面是部分测试过程供参考：
**MySQL Shell****utli.dumpSchemas/utli.loadDump**
- 备份
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysqlsh> util.dumpSchemas(["test"],"test1")``Acquiring global read lock``All transactions have been started``Locking instance for backup``Global read lock has been released``Writing global DDL files``Preparing data dump for table `test`.`customer1```Writing DDL for schema `test```Writing DDL for table `test`.`sbtest1```Writing DDL for table `test`.`customer1```Writing DDL for table `test`.`sbtest10```Data dump for table `test`.`customer1` will be chunked using column `c_w_id```Preparing data dump for table `test`.`sbtest1```Data dump for table `test`.`sbtest1` will be chunked using column `id```Preparing data dump for table `test`.`sbtest10```Data dump for table `test`.`sbtest10` will be chunked using column `id```Preparing data dump for table `test`.`sbtest2```Data dump for table `test`.`sbtest2` will be chunked using column `id```Preparing data dump for table `test`.`sbtest4```Data dump for table `test`.`sbtest4` will be chunked using column `id```Preparing data dump for table `test`.`sbtest6```Data dump for table `test`.`sbtest6` will be chunked using column `id```Preparing data dump for table `test`.`sbtest8```Data dump for table `test`.`sbtest8` will be chunked using column `id```Running data dump using 4 threads.``NOTE: Progress information uses estimated values and may not be accurate.``Writing DDL for table `test`.`sbtest2```Writing DDL for table `test`.`sbtest4```Writing DDL for table `test`.`sbtest6```Writing DDL for table `test`.`sbtest8```Data dump for table `test`.`customer1` will be written to 3 files``Data dump for table `test`.`sbtest10` will be written to 1 file``Data dump for table `test`.`sbtest2` will be written to 1 file``Data dump for table `test`.`sbtest4` will be written to 1 file``Data dump for table `test`.`sbtest6` will be written to 1 file``Data dump for table `test`.`sbtest8` will be written to 1 file``Data dump for table `test`.`sbtest1` will be written to 160 files``1 thds dumping - 98% (10.46M rows / ~10.62M rows), 589.52K rows/s, 115.55 MB/s uncompressed, 51.66 MB/s compressed``Duration: 00:00:18s``Schemas dumped: 1``Tables dumped: 7``Uncompressed data size: 2.06 GB``Compressed data size: 922.35 MB``Compression ratio: 2.2``Rows written: 10464999``Bytes written: 922.35 MB``Average uncompressed throughput: 109.46 MB/s``Average compressed throughput: 48.97 MB/s`
- 恢复
- 
- 
- 
- 
- 
- 
- 
- 
- 
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
util.loadDump("test1")`Loading DDL and Data from 'instance' using 4 threads.``Target is MySQL 8.0.21. Dump was produced from MySQL 8.0.21``Checking for pre-existing objects...``Executing common preamble SQL``Executing DDL script for schema `test```Executing DDL script for `test`.`sbtest1```Executing DDL script for `test`.`sbtest4```Executing DDL script for `test`.`sbtest2```Executing DDL script for `test`.`sbtest8```Executing DDL script for `test`.`sbtest10```Executing DDL script for `test`.`sbtest6```Executing DDL script for `test`.`customer1```...``[Worker000] test@sbtest1@158.tsv.zst: Records: 65736  Deleted: 0  Skipped: 0  Warnings: 0``Executing common postamble SQL``
``168 chunks (10.46M rows, 2.06 GB) for 7 tables in 1 schemas were loaded in 1 min 26 sec (avg throughput 23.97 MB/s)
```
**mysqldump**
- 备份
- 
- 
- 
/usr/bin/time mysqldump -umsandbox -pmsandbox -h127.0.0.1 -P8021 test | gzip > db.sql.gz``mysqldump: [Warning] Using a password on the command line interface can be insecure.``      169.40 real        24.65 user         1.34 sys`
- 恢复
- 
- 
` /usr/bin/time gzip -d < db.sql.gz | ./use test``      257.11 real         9.74 user         0.55 sys`
**mysqlpump**
- 备份
- 
- 
- 
- 
`/usr/bin/time mysqlpump --default-parallelism=4 -umsandbox -pmsandbox -h127.0.0.1  -P8021 test | gzip > db2.sql.gz``Dump progress: 6/7 tables, 10421749/10406264 rows``Dump completed in 185352``      185.50 real        31.18 user         6.34 sys`
- 恢复
- 
- 
`/usr/bin/time gzip -d < db2.sql.gz | ./use test``      121.17 real         9.66 user         0.76 sys`
**mydumper/myloader**
- 备份
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`/usr/bin/time mydumper -u msandbox -p msandbox -h 127.0.0.1 -P 8021 -B test -t 4 -v 3 -c -o dumper``** Message: 21:44:55.958: Connected to a MySQL server``** Message: 21:44:56.319: Started dump at: 2020-07-24 21:44:56``
``** Message: 21:44:56.341: Written master status``** Message: 21:44:56.420: Thread 1 connected using MySQL connection ID 22``** Message: 21:44:56.537: Thread 2 connected using MySQL connection ID 23``** Message: 21:44:56.651: Thread 3 connected using MySQL connection ID 24``** Message: 21:44:56.769: Thread 4 connected using MySQL connection ID 25``** Message: 21:44:56.878: Non-InnoDB dump complete, unlocking tables``** Message: 21:44:56.878: Thread 4 dumping data for `test`.`sbtest10```** Message: 21:44:56.878: Thread 1 dumping data for `test`.`customer1```** Message: 21:44:56.878: Thread 3 dumping data for `test`.`sbtest1```** Message: 21:44:56.878: Thread 2 dumping data for `test`.`sbtest2```** Message: 21:44:57.139: Thread 2 dumping data for `test`.`sbtest4```** Message: 21:44:57.143: Thread 4 dumping data for `test`.`sbtest6```** Message: 21:44:57.396: Thread 2 dumping data for `test`.`sbtest8```** Message: 21:44:57.398: Thread 4 dumping schema for `test`.`customer1```** Message: 21:44:57.409: Thread 4 dumping schema for `test`.`sbtest1```** Message: 21:44:57.419: Thread 4 dumping schema for `test`.`sbtest10```** Message: 21:44:57.430: Thread 4 dumping schema for `test`.`sbtest2```** Message: 21:44:57.441: Thread 4 dumping schema for `test`.`sbtest4```** Message: 21:44:57.453: Thread 4 dumping schema for `test`.`sbtest6```** Message: 21:44:57.464: Thread 4 dumping schema for `test`.`sbtest8```** Message: 21:44:57.475: Thread 4 shutting down``** Message: 21:44:57.636: Thread 2 shutting down``** Message: 21:45:03.706: Thread 1 shutting down``** Message: 21:47:40.297: Thread 3 shutting down``** Message: 21:47:40.307: Finished dump at: 2020-07-24 21:47:40``      164.54 real       167.58 user         2.28 sys`注：使用的并行备份线程数与dumpSchema相同。
- 恢复
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
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
/usr/bin/time myloader -u msandbox -p msandbox -h 127.0.0.1 -P 8021 -B test -t 4 -v 3  -d dumper/`** Message: 23:54:39.961: 4 threads created``** Message: 23:54:39.973: Creating table `test`.`sbtest4```** Message: 23:54:40.055: Creating table `test`.`sbtest10```** Message: 23:54:40.127: Creating table `test`.`customer1```** Message: 23:54:40.201: Creating table `test`.`sbtest8```** Message: 23:54:40.273: Creating table `test`.`sbtest2```** Message: 23:54:40.346: Creating table `test`.`sbtest6```** Message: 23:54:40.423: Creating table `test`.`sbtest1```** Message: 23:54:40.488: Thread 2 restoring `test`.`sbtest2` part 0``** Message: 23:54:40.488: Thread 3 restoring `test`.`sbtest6` part 0``** Message: 23:54:40.488: Thread 4 restoring `test`.`sbtest8` part 0``** Message: 23:54:40.488: Thread 1 restoring `test`.`sbtest4` part 0``** Message: 23:54:40.833: Thread 2 restoring `test`.`sbtest1` part 0``** Message: 23:54:40.833: Thread 4 restoring `test`.`sbtest10` part 0``** Message: 23:54:40.834: Thread 3 restoring `test`.`customer1` part 0``** Message: 23:54:40.834: Thread 1 shutting down``** Message: 23:54:41.070: Thread 4 shutting down``** Message: 23:54:50.407: Thread 3 shutting down``** Message: 23:57:46.425: Thread 2 shutting down`      187.10 real        14.24 user         1.97 sys
```