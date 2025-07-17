# 新特性解读 | 趋近完美的 Undo 空间

**原文链接**: https://opensource.actionsky.com/20200420-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-04-20T00:36:56-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
在说 Undo 表空间前，先来简单说下 Undo Log 的概念。
直白来讲，Undo Log 是 MySQL 用来记录事务操作的反方向逻辑日志。当确保事务提交成功后，MySQL 后台有专门的清理线程来清理掉这部分内容，确保 Undo Log 能循环使用。
**Undo 的相关概念**
- undo log segment(undo segment)Undo Logs 合集。undo segment 可以被重复使用，但是一次只能由一个事务占用。
- rollback segment也就是 Undo Logs 的物理存储区域。
- undo tablespacerollback segment 被从系统表空间里分离出来后的实际磁盘文件表现形式。
所以基本关系如下：undo log -> undo log segment-> rollback segment->undo tablespace
**Undo Log 发展史**
**MySQL 5.5 和之前的版本**Undo Log 一直存在共享的系统表空间里（ibdata1&#8230;)，但有两个问题：1. Undo 这块 IO 处理太集中，无法很好的监测单个瓶颈点2. 持续并发运行稍微大点的事务，会造成系统表空间持续增大，造成定期的重建系统表空间
**MySQL 5.6**
Undo Log 被分离出来，由单独的 Undo 表空间管理。可以避免 Undo 这块 IO 消耗过于集中，有助于分散 IO 的负载。
**MySQL 5.7**
解决了 Undo Log 一直以来物理空间膨胀，无法自动收缩的问题
**MySQL 8.0**
开始从 SQL 层面非常方便的管理 Undo 表空间
**MySQL 8.0 对 Undo Log 的改进说明**
**1、默认的表空间**MySQL 服务启动后，默认有两个 Undo 表空间：undo01,undo02- `root@ytt-pc:/var/lib/mysql/3304# ls -sihl undo*`
- `919027 14M -rw-r----- 1 mysql mysql 14M 3月  20 11:00 undo_001`
- `918943 12M -rw-r----- 1 mysql mysql 12M 3月  20 11:00 undo_002`
这两个默认产生的 Undo 表空间文件，不能在 SQL 层面来管理。直接删除会被 MySQL 阻止。- `mysql> drop undo tablespace innodb_undo_001;`
- `ERROR 3119 (42000): InnoDB: Tablespace names starting with `innodb_` are reserved.`
- 
- `mysql> show errors;`
- `+-------+------+----------------------------------------------------------------+`
- `| Level | Code | Message                                                        |`
- `+-------+------+----------------------------------------------------------------+`
- `| Error | 3119 | InnoDB: Tablespace names starting with `innodb_` are reserved. |`
- `| Error | 3119 | Incorrect tablespace name `innodb_undo_001`                    |`
- `+-------+------+----------------------------------------------------------------+`
- `2 rows in set (0.00 sec)`
**2、可设置回滚段数量的参数**
参数 innodb_rollback_segments 设置每个 undo 表空间的回滚段的数量。在 MySQL 5.7 这个参数被用来设置所有 Undo 表空间的回滚段数量。最大 128，就是说**一个 MySQL 实例最多 128 个回滚段。**注意高能时刻！MySQL 8.0 放开了这个限制，使得这个参数设置限制在每个表空间。也就是说**每个表空间**最多 128 个回滚段，可以设置多个表空间！也就解决了 MySQL 5.7 在持续高并发时，事务争抢回滚段不足造成的资源抢占，减少了相关的锁开销。
**3、自动收缩参数**
参数 innodb_undo_log_truncate 默认开启。开启这个参数的目的是让 MySQL 自动收缩 Undo 表空间，防止磁盘占用过大。
**4、废弃的参数**
额外的 Undo 表空间 SQL 层面动态管理参数 innodb_undo_tablespaces 被废弃。
**示例：Undo 表空间管理（不包括临时表空间）**
具体语法：- `CREATE [UNDO] TABLESPACE tablespace_name`
- `InnoDB and NDB:`
- `[ADD DATAFILE 'file_name']`
- `InnoDB only:`
- `[FILE_BLOCK_SIZE = value]`
- `[ENCRYPTION [=] {'Y' | 'N'}]`
- `NDB only:`
- `USE LOGFILE GROUP logfile_group`
- `[EXTENT_SIZE [=] extent_size]`
- `[INITIAL_SIZE [=] initial_size]`
- `[AUTOEXTEND_SIZE [=] autoextend_size]`
- `[MAX_SIZE [=] max_size]`
- `[NODEGROUP [=] nodegroup_id]`
- `[WAIT]`
- `[COMMENT [=] 'string']`
- `InnoDB and NDB:`
- `[ENGINE [=] engine_name]`
2、查看表空间
查看 Undo 表空间的元数据信息information_schema.innodb_tablesapces 表- `mysql> select * from information_schema.innodb_tablespaces where SPACE_TYPE='undo'\G`
- `*************************** 1. row ***************************`
- `        SPACE: 4294967279`
- `         NAME: innodb_undo_001`
- `         FLAG: 0`
- `   ROW_FORMAT: Undo`
- `    PAGE_SIZE: 16384`
- `ZIP_PAGE_SIZE: 0`
- `   SPACE_TYPE: Undo`
- `FS_BLOCK_SIZE: 0`
- `    FILE_SIZE: 0`
- `ALLOCATED_SIZE: 0`
- `SERVER_VERSION: 8.0.18`
- `SPACE_VERSION: 1`
- `   ENCRYPTION: N`
- `        STATE: active`
- `*************************** 2. row ***************************`
- `        SPACE: 4294967278`
- `         NAME: innodb_undo_002`
- `         FLAG: 0`
- `   ROW_FORMAT: Undo`
- `    PAGE_SIZE: 16384`
- `ZIP_PAGE_SIZE: 0`
- `   SPACE_TYPE: Undo`
- `FS_BLOCK_SIZE: 0`
- `    FILE_SIZE: 0`
- `ALLOCATED_SIZE: 0`
- `SERVER_VERSION: 8.0.18`
- `SPACE_VERSION: 1`
- `   ENCRYPTION: N`
- `        STATE: active`
- `*************************** 3. row ***************************`
- `        SPACE: 4294967277`
- `         NAME: undo_ts1`
- `         FLAG: 0`
- `   ROW_FORMAT: Undo`
- `    PAGE_SIZE: 16384`
- `ZIP_PAGE_SIZE: 0`
- `   SPACE_TYPE: Undo`
- `FS_BLOCK_SIZE: 0`
- `    FILE_SIZE: 0`
- `ALLOCATED_SIZE: 0`
- `SERVER_VERSION: 8.0.19`
- `SPACE_VERSION: 1`
- `   ENCRYPTION: N`
- `        STATE: active`
- `3 rows in set (0.00 sec)`
3、修改存放目录Undo 表空间，默认是保存在变量 innodb_undo_directory 指定的目录，如果这个目录没有指定，就放在数据目录下。- `# 默认在当前数据目录`
- `mysql> select @@innodb_undo_directory;`
- `+-------------------------+`
- `| @@innodb_undo_directory |`
- `+-------------------------+`
- `| ./                      |`
- `+-------------------------+`
- `1 row in set (0.00 sec)`
- 
- `# 刚建立的 undo_ts1.ibu.`
- `root@ytt-pc:/var/lib/mysql/3304# ls -sihl undo_ts1.ibu`
- `918978 10M -rw-r----- 1 mysql mysql 10M 3月  20 11:33 undo_ts1.ibu`
也可以把 Undo 表空间建立在非 innodb_undo_directory 指定的目录。- `# 指定undo 表空间目录/var/lib/mysql-files/，新建立一个undo_ts2.ibu.`
- 
- `mysql> create undo tablespace undo_ts2 add datafile '/var/lib/mysql-files/undo_ts2.ibu';`
- `Query OK, 0 rows affected (0.30 sec)`
**Undo 表空间的名字必须以 .ibu 为后缀**- `# 创建一个 undo 表空间 undo_ts3，没有带后缀，MySQL 拒绝创建。`
- `   mysql> create undo tablespace undo_ts3 add datafile 'undo_ts3';`
- `   ERROR 3121 (HY000): The ADD DATAFILE filepath must end with '.ibu'.`
- `   mysql> show errors;`
- `   +-------+------+-------------------------------------------------+`
- `   | Level | Code | Message                                         |`
- `   +-------+------+-------------------------------------------------+`
- `   | Error | 3121 | The ADD DATAFILE filepath must end with '.ibu'. |`
- `   | Error | 1528 | Failed to create UNDO TABLESPACE undo_ts3       |`
- `   | Error | 3121 | Incorrect File Name 'undo_ts3'.                 |`
- `   +-------+------+-------------------------------------------------+`
- `   3 rows in set (0.00 sec)`
4、删除表空间
删除表空间必须确保这个表空间没有被任何事务用到，也就是把这个表空间变为非激活状态，这样就能阻止任何事务进入这个表空间。- `mysql> alter undo tablespace undo_ts2 set inactive;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> drop undo tablespace undo_ts2;`
- `Query OK, 0 rows affected (0.01 sec)`
5、移动表空间
移动 Undo 表空间到其他位置，需要按照这样的步骤：1. 停掉 mysqld 服务；2. 设置参数 innodb_undo_directory 到新的目录；3. 移动 Undo 日志到上一步设置好的目录；4. 启动 mysqld 服务；
步骤 2&3 具体如下：设置变量 innodb_undo_directory，并且移动 Undo 表空间到这个目录- `mysql> select @@innodb_undo_directory;`
- `+-------------------------+`
- `| @@innodb_undo_directory |`
- `+-------------------------+`
- `| /var/lib/mysql-files    |`
- `+-------------------------+`
- `1 row in set (0.00 sec)`
一切完了后，检查移动后的 Undo 文件是否正常。
通过检索文件元数据表 information_schema.files 查看文件类型为 Undo Log 的记录。系统预留的两个表空间已经正确的在新目录下被识别了。- `mysql> select file_name,file_type,tablespace_name,status from files where file_type = 'undo log';`
- `+-------------------------------+-----------+-----------------+--------+`
- `| FILE_NAME                     | FILE_TYPE | TABLESPACE_NAME | STATUS |`
- `+-------------------------------+-----------+-----------------+--------+`
- `| /var/lib/mysql-files/undo_001 | UNDO LOG  | innodb_undo_001 | NORMAL |`
- `| /var/lib/mysql-files/undo_002 | UNDO LOG  | innodb_undo_002 | NORMAL |`
- `+-------------------------------+-----------+-----------------+--------+`
- `2 rows in set (0.00 sec)`
再创建一个新的 Undo 表空间。默认的位置已经变到新的目录下。- `mysql> create undo tablespace undo_ts_new add datafile 'undo_ts_new.ibu';`
- `Query OK, 0 rows affected (0.51 sec)`
- 
- `root@ytt-pc:/var/lib/mysql-files# ls -l undo*`
- `-rw-r----- 1 mysql mysql 10485760 3月  20 12:00 undo_001`
- `-rw-r----- 1 mysql mysql 10485760 3月  20 12:00 undo_002`
- `-rw-r----- 1 mysql mysql 10485760 3月  20 12:00 undo_ts_new.ibu`
**总结**
这里我对 MySQL 8.0 的 Undo 表空间在使用上的改进简要做了一个说明，可以看出来，MySQL 8.0 对 Undo 的改进已经非常成熟。