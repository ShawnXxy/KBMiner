# 技术分享 | Online DDL 工具 pt-osc

**原文链接**: https://opensource.actionsky.com/20200916-ddl/
**分类**: 技术干货
**发布时间**: 2020-09-16T00:43:58-08:00

---

作者：张洛丹
爱可生 DBA 团队成员，主要负责 MySQL 故障处理和公司自动化运维平台维护。对技术执着，为客户负责。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**Online DDL 工具：pt-osc**
对于 MySQL Online DDL 目前主流的有三种工具：
- 原生 Online DDL；
- pt-osc(online-schema-change)，
- gh-ost
本文主要讲解 pt-online-schema-change 的使用以及三种工具的简单对比。
**一、原理及限制**
**1.1 原理**
1. 创建一个与原表结构相同的空表，表名是 **_new** 后缀；
2. 修改步骤 1 创建的空表的表结构；
3. 在原表上加三个触发器：delete/update/insert，用于 copy 数据过程中，将原表中要执行的语句在新表中执行；
4. 将原表数据以数据块（chunk）的形式 copy 到新表；
5. rename 原表为 old 表，并把新表 rename 为原表名，然后删除旧表；
6. 删除触发器。
**1.2 限制**1. 原表上要有 primary key 或 unique index，因为当执行该工具时会创建一个 DELETE 触发器来更新新表；
> 注意：一个例外的情况是 **&#8211;alter** 指定的子句中是在原表中的列上创建 primary key 或 unique index，这种情况下将使用这些列用于 DELETE 触发器。
2. 不能使用 rename 子句来重命名表；
3. 列不能通过**删除 + 添加**的方式来重命名，这样将不会 copy 原有列的数据到新列；
4. 如果要添加的列是 not null，则必须指定默认值，否则会执行失败；
5. 删除外键约束（**DROP FOREIGN KEY constraint_name**），外键约束名前面必须添加一个下划线 &#8216;_&#8217;，即需要指定名称 **_constraint_name**，而不是原始的 **constraint_name**；
例如：
- 
`CONSTRAINT `fk_foo` FOREIGN KEY (`foo_id`) REFERENCES `bar` (`foo_id`)`必须指定 **&#8211;alter &#8220;DROP FOREIGN KEY _fk_foo&#8221;**。
**二、使用**
**2.1 语法**
- 
`pt-online-schema-change [OPTIONS] DSN`其中 DSN 是指 Data Source Name，是连接数据库的变量信息。格式为 key=value。
DSN 的 key 有：
- A：默认字符集
- D：数据库
- F：只从给定的文件中读取默认值
- P：端口号
- S：socket 文件
- h：主机 IP 或主机名
- p：密码
- t：要更新的表
- u：用户名
**2.2 参数字典（文末）**
**三、使用**
**3.1 安装**
- 
- 
- 
- 
`-- 安装 yum 仓库``yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm``-- 安装 percona toolkit``yum install percona-toolkit -y`
**3.2 使用示例**
> 本示例模拟修改列类型，将列类型由 char(20) 修改为 varchar(200)
版本信息：MySQL 5.7.25，percona-tool 3.2.0
数据量 200 万
准备
**3.2.1 创建用户**
- 
- 
- 
- 
- 
`GRANT SELECT, INSERT, UPDATE, DELETE, \``    CREATE, DROP, PROCESS, REFERENCES, \ ``    INDEX, ALTER, SUPER, LOCK TABLES, \``    REPLICATION SLAVE, TRIGGER ``ON *.* TO 'ptosc'@'%'`
**3.2.2 写 ALTER 语句**- 
```
modify c varchar(200) not null default ""
```
**3.2.3 环境检查**
> 说明：工具在执行时也会进行检查，如果遇到不能执行的情况，则报错，建议在执行前先进行 dry-run。
3.2.3.1 检查要变更的表上是否有主键或非空唯一键- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> desc sbtest1;``+-------+-----------+------+-----+---------+----------------+``| Field | Type      | Null | Key | Default | Extra          |``+-------+-----------+------+-----+---------+----------------+``|``| k     | int(11)   | NO   | MUL | 0       |                |``|``| pad   | char(60)  | NO   |     |         |                |``+-------+-----------+------+-----+---------+----------------+``4 rows in set (0.00 sec)`3.2.3.2 检查是否有其他表外键引用该表- 
- 
- 
- 
- 
- 
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
select * from information_schema.key_column_usage where referenced_table_schema='testdb' and referenced_table_name='sbtest1'\G`*************************** 1. row ***************************``           CONSTRAINT_CATALOG: def``            CONSTRAINT_SCHEMA: testdb``              CONSTRAINT_NAME: test2_ibfk_1``                TABLE_CATALOG: def``                 TABLE_SCHEMA: testdb``                   TABLE_NAME: test2``                  COLUMN_NAME: t_id``             ORDINAL_POSITION: 1``POSITION_IN_UNIQUE_CONSTRAINT: 1``      REFERENCED_TABLE_SCHEMA: testdb``        REFERENCED_TABLE_NAME: sbtest1``      REFERENCED_COLUMN_NAME: id``1 row in set (0.01 sec)
```
若有，则需要使用 **&#8211;alter-foreign-keys-method** 选项
3.2.3.3 检查表上是否有触发器- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
mysql> select * from information_schema.triggers where event_object_schema='testdb' and event_object_table='sbtest1'\G``*************************** 1. row ***************************``           TRIGGER_CATALOG: def``            TRIGGER_SCHEMA: testdb``              TRIGGER_NAME: trig1``        EVENT_MANIPULATION: INSERT``      EVENT_OBJECT_CATALOG: def``       EVENT_OBJECT_SCHEMA: testdb``        EVENT_OBJECT_TABLE: sbtest1``              ACTION_ORDER: 1``          ACTION_CONDITION: NULL``          ACTION_STATEMENT: INSERT INTO time VALUES(NOW())``        ACTION_ORIENTATION: ROW``             ACTION_TIMING: AFTER``ACTION_REFERENCE_OLD_TABLE: NULL``ACTION_REFERENCE_NEW_TABLE: NULL``  ACTION_REFERENCE_OLD_ROW: OLD``  ACTION_REFERENCE_NEW_ROW: NEW``                   CREATED: 2020-08-23 10:43:27.38``                  SQL_MODE: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION``                   DEFINER: root@localhost``      CHARACTER_SET_CLIENT: utf8``      COLLATION_CONNECTION: utf8_general_ci``        DATABASE_COLLATION: utf8mb4_bin``1 row in set (0.00 sec)`若有，则需指定 **&#8211;preserve-triggers** 选项，且在 percona tool 3.0.4 起，对于 MySQL 5.7.2 以上，支持原表上有触发器，建议使用前在测试环境进行测试。
> 官方 issue 链接：https://jira.percona.com/browse/PT-91
3.2.3.4 检查从库是否设置 change filter
- 
- 
- 
- 
- 
- 
- 
- 
`show slave status\G``...``              Replicate_Do_DB:``          Replicate_Ignore_DB:``           Replicate_Do_Table:``       Replicate_Ignore_Table:``      Replicate_Wild_Do_Table:``  Replicate_Wild_Ignore_Table:`如果设置了 change filter，则不会执行，除非指定 **&#8211;no-check-replication-filters**
**3.2.4 执行 dry run**
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`# pt-online-schema-change --print --statistics \``    --progress time,30 --preserve-triggers --user=ptosc \``    --password=ptosc --alter 'modify c varchar(200) not null default ""' \``    h=127.0.1.1,P=3306,D=testdb,t=sbtest1 \``    --pause-file=/tmp/aa.txt --max-load=threads_running=100,threads_connected=200 \``    --critical-load=threads_running=1000  --chunk-size=1000 \``    --alter-foreign-keys-method auto --dry-run``
``Operation, tries, wait:`` analyze_table, 10, 1`` copy_rows, 10, 0.25`` create_triggers, 10, 1`` drop_triggers, 10, 1``  swap_tables, 10, 1``  update_foreign_keys, 10, 1``Child tables:``  `testdb`.`test2` (approx. 1 rows)``Will automatically choose the method to update foreign keys.``Starting a dry run.  `testdb`.`sbtest1` will not be altered.  Specify --execute instead of --dry-run to alter the table.``
``Creating new table...``CREATE TABLE `testdb`.`_sbtest1_new` (``  `id` int(11) NOT NULL AUTO_INCREMENT,``  `k` int(11) NOT NULL DEFAULT '0',``  `c` char(120) COLLATE utf8mb4_bin NOT NULL DEFAULT '',``  `pad` char(60) COLLATE utf8mb4_bin NOT NULL DEFAULT '',``  PRIMARY KEY (`id`),``  KEY `k_1` (`k`)``) ENGINE=InnoDB AUTO_INCREMENT=2000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin``Created new table testdb._sbtest1_new OK.``
``Altering new table...``ALTER TABLE `testdb`.`_sbtest1_new` modify c varchar(200) not null default ""``Altered `testdb`.`_sbtest1_new` OK.``Not creating triggers because this is a dry run.``Not copying rows because this is a dry run.``
``INSERT LOW_PRIORITY IGNORE INTO `testdb`.`_sbtest1_new` (`id`, `k`, `c`, `pad`) SELECT `id`, `k`, `c`, `pad` FROM `testdb`.`sbtest1` FORCE INDEX(`PRIMARY`) WHERE ((`id` >= ?)) AND ((`id` <= ?)) LOCK IN SHARE MODE /*pt-online-schema-change 6337 copy nibble*/``SELECT /*!40001 SQL_NO_CACHE */ `id` FROM `testdb`.`sbtest1` FORCE INDEX(`PRIMARY`) WHERE ((`id` >= ?)) ORDER BY `id` LIMIT ?, 2 /*next chunk boundary*/``Not determining the method to update foreign keys because this is a dry run.``2020-08-23T13:24:19 Adding original triggers to new table.``Not swapping tables because this is a dry run.``Not updating foreign key constraints because this is a dry run.``Not dropping old table because this is a dry run.``Not dropping triggers because this is a dry run.``DROP TRIGGER IF EXISTS `testdb`.`pt_osc_testdb_sbtest1_del```DROP TRIGGER IF EXISTS `testdb`.`pt_osc_testdb_sbtest1_upd```DROP TRIGGER IF EXISTS `testdb`.`pt_osc_testdb_sbtest1_ins```2020-08-23T13:24:19 Dropping new table...``DROP TABLE IF EXISTS `testdb`.`_sbtest1_new`;``2020-08-23T13:24:19 Dropped new table OK.``# Event  Count``# ====== =====``# INSERT     0``Dry run complete.  `testdb`.`sbtest1` was not altered.`- **&#8211;print**：打印工具执行的 SQL 语句。
- **&#8211;statistics**：打印统计信息。
- **&#8211;pause-file**：当指定的文件存在时，终止执行。
- **&#8211;max-load**：超过指定负载时，暂定执行。
- **&#8211;critical-load**：超过指定负载时，终止执行。
- **&#8211;chunck-size**：指定每次复制的行数。
- **&#8211;alter-foreign-keys-method**：指定外键更新方式。
- **&#8211;progress**：copy 进度打印的频率。
**3.2.5 执行**
将 **&#8211;dry-run** 修改为 **&#8211;execute**- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`# pt-online-schema-change --print --statistics \``    --progress time,30 --preserve-triggers --user=ptosc \``    --password=ptosc --alter 'modify c varchar(200) not null default ""' \``    h=127.0.1.1,P=3306,D=testdb,t=sbtest1 \``    --pause-file=/tmp/aa.txt --max-load=threads_running=100,threads_connected=200 \``    --critical-load=threads_running=1000  --chunk-size=1000 \``    --alter-foreign-keys-method auto  --execute``Found 2 slaves:``10-186-64-51 -> 10.186.64.51:3306``10-186-64-48 -> 10.186.64.48:3306``Will check slave lag on:``10-186-64-51 -> 10.186.64.51:3306``10-186-64-48 -> 10.186.64.48:3306``Operation, tries, wait:``  analyze_table, 10, 1``  copy_rows, 10, 0.25``  create_triggers, 10, 1``  drop_triggers, 10, 1``  swap_tables, 10, 1``  update_foreign_keys, 10, 1``Child tables:``  `testdb`.`test2` (approx. 1 rows)``Will automatically choose the method to update foreign keys.``Altering `testdb`.`sbtest1`...``
``Creating new table...``CREATE TABLE `testdb`.`_sbtest1_new` (``  `id` int(11) NOT NULL AUTO_INCREMENT,``  `k` int(11) NOT NULL DEFAULT '0',``  `c` char(120) COLLATE utf8mb4_bin NOT NULL DEFAULT '',``  `pad` char(60) COLLATE utf8mb4_bin NOT NULL DEFAULT '',``  PRIMARY KEY (`id`),``  KEY `k_1` (`k`)``) ENGINE=InnoDB AUTO_INCREMENT=2000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin``Created new table testdb._sbtest1_new OK.``
``Altering new table...``ALTER TABLE `testdb`.`_sbtest1_new` modify c varchar(200) not null default ""``Altered `testdb`.`_sbtest1_new` OK.``2020-08-23T14:44:53 Creating triggers...``2020-08-23T14:44:53 Created triggers OK.``2020-08-23T14:44:53 Copying approximately 1972656 rows...``INSERT LOW_PRIORITY IGNORE INTO `testdb`.`_sbtest1_new` (`id`, `k`, `c`, `pad`) SELECT `id`, `k`, `c`, `pad` FROM `testdb`.`sbtest1` FORCE INDEX(`PRIMARY`) WHERE ((`id` >= ?)) AND ((`id` <= ?)) LOCK IN SHARE MODE /*pt-online-schema-change 15822 copy nibble*/``SELECT /*!40001 SQL_NO_CACHE */ `id` FROM `testdb`.`sbtest1` FORCE INDEX(`PRIMARY`) WHERE ((`id` >= ?)) ORDER BY `id` LIMIT ?, 2 /*next chunk boundary*/``
``Copying `testdb`.`sbtest1`:  52% 00:27 remain``Copying `testdb`.`sbtest1`:  99% 00:00 remain``2020-08-23T14:45:53 Copied rows OK.``2020-08-23T14:45:53 Max rows for the rebuild_constraints method: 4000``Determining the method to update foreign keys...``2020-08-23T14:45:53   `testdb`.`test2`: 1 rows; can use rebuild_constraints``2020-08-23T14:45:53 Adding original triggers to new table.``2020-08-23T14:45:53 Analyzing new table...``2020-08-23T14:45:53 Swapping tables...``RENAME TABLE `testdb`.`sbtest1` TO `testdb`.`_sbtest1_old`, `testdb`.`_sbtest1_new` TO `testdb`.`sbtest1```2020-08-23T14:45:54 Swapped original and new tables OK.``2020-08-23T14:45:54 Rebuilding foreign key constraints...``ALTER TABLE `testdb`.`test2` DROP FOREIGN KEY `test2_ibfk_1`, ADD CONSTRAINT `_test2_ibfk_1` FOREIGN KEY (`t_id`) REFERENCES `testdb`.`sbtest1` (`id`)``2020-08-23T14:45:54 Rebuilt foreign key constraints OK.``2020-08-23T14:45:54 Dropping old table...``DROP TABLE IF EXISTS `testdb`.`_sbtest1_old```2020-08-23T14:45:54 Dropped old table `testdb`.`_sbtest1_old` OK.``2020-08-23T14:45:54 Dropping triggers...``DROP TRIGGER IF EXISTS `testdb`.`pt_osc_testdb_sbtest1_del```DROP TRIGGER IF EXISTS `testdb`.`pt_osc_testdb_sbtest1_upd```DROP TRIGGER IF EXISTS `testdb`.`pt_osc_testdb_sbtest1_ins```2020-08-23T14:45:54 Dropped triggers OK.``# Event              Count``# ================== =====``# INSERT              2000``# rebuilt_constraint     1``Successfully altered `testdb`.`sbtest1`.`如上，输出比较简单，包括了每一步执行的 SQL。copy 数据期间打印了 copy 的进度以及预计剩余时间；最后打印出统计信息，比如 insert 的数据块数。
**3.2.6 执行后检查**
3.2.6.1 检查原表是否正确修改
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> show create table sbtest1\G``*************************** 1. row ***************************``       Table: sbtest1``Create Table: CREATE TABLE `sbtest1` (``  `id` int(11) NOT NULL AUTO_INCREMENT,``  `k` int(11) NOT NULL DEFAULT '0',``  `c` varchar(200) COLLATE utf8mb4_bin NOT NULL DEFAULT '',``  `pad` char(60) COLLATE utf8mb4_bin NOT NULL DEFAULT '',``  PRIMARY KEY (`id`),``  KEY `k_1` (`k`)``) ENGINE=InnoDB AUTO_INCREMENT=2000001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin``1 row in set (0.00 sec)``
``mysql> desc sbtest1;``+-------+--------------+------+-----+---------+----------------+``| Field | Type         | Null | Key | Default | Extra          |``+-------+--------------+------+-----+---------+----------------+``| id    | int(11)      | NO   | PRI | NULL    | auto_increment |``| k     | int(11)      | NO   | MUL | 0       |                |``| c     | varchar(200) | NO   |     |         |                |``| pad   | char(60)     | NO   |     |         |                |``+-------+--------------+------+-----+---------+----------------+``4 rows in set (0.01 sec)`3.2.6.2 检查引用该表的外键
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> show create table test2\G``*************************** 1. row ***************************``       Table: test2``Create Table: CREATE TABLE `test2` (``  `id` int(11) NOT NULL AUTO_INCREMENT,``  `t_id` int(11) DEFAULT NULL,``  PRIMARY KEY (`id`),``  KEY `_test2_ibfk_1` (`t_id`),``  CONSTRAINT `_test2_ibfk_1` FOREIGN KEY (`t_id`) REFERENCES `sbtest1` (`id`)``) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin``1 row in set (0.00 sec)`3.2.6.3 检查原表上触发器
- 
- 
- 
- 
- 
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
mysql> show triggers\G`*************************** 1. row ***************************``             Trigger: trig1``               Event: INSERT``               Table: sbtest1``           Statement: INSERT INTO time VALUES(NOW())``              Timing: AFTER``             Created: 2020-08-23 14:45:53.96``            sql_mode: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION``             Definer: root@localhost``character_set_client: utf8``collation_connection: utf8_general_ci``  Database Collation: utf8mb4_bin``1 row in set (0.00 sec)
```
**四、Online DDL 工具对比**
**4.1 原理对比**这里简单说一下另外两个工具：原生 Online DDL 和 gh-ost 的原理。
**4.1.1 MySQL 原生 DDL**
自 MySQL 5.6 起，MySQL 原生支持 Online DDL，即在执行 DDL 期间允许执行 DML(insert、update、delete)。了解 Online DDL 先了解一下之前 DDL 的 2 种算法 copy 和 inplace。
Copy：
1. 按照原表定义创建一个新的临时表2. 对原表加写锁（禁止 DML，允许 select）3. 步骤 1）建立的临时表执行 DDL4. 将原表中的数据 copy 到临时表5. 释放原表的写锁6. 将原表删除，并将临时表重命名为原表可见，采用 copy 方式期间需要锁表，禁止 DML，因此是非 Online 的。比如：删除主键、修改列类型、修改字符集，这些操作会导致行记录格式发生变化（无法通过全量 + 增量实现 Online）。Inplace：在原表上进行更改，不需要生成临时表，不需要进行数据 copy 的过程。根据是否行记录格式，分为两类：- rebuild：需要重建表（重新组织聚簇索引）。比如 optimize table、添加索引、添加/删除列、修改列 NULL/NOT NULL 属性等； 
- no-rebuild：不需要重建表，只需要修改表的元数据，比如删除索引、修改列名、修改列默认值、修改列自增值等。
对于 rebuild 方式实现 Online 是通过缓存 DDL 期间的 DML，待 DDL 完成之后，将 DML 应用到表上来实现的。例如，执行一个 **alter table A engine=InnoDB;** 重建表的 DDL 其大致流程如下：1. 建立一个临时文件，扫描表 A 主键的所有数据页；2. 用数据页中表 A 的记录生成 B+ 树，存储到临时文件中；3. 生成临时文件的过程中，将所有对 A 的操作记录在一个日志文件（row log）中；4. 临时文件生成后，将日志文件中的操作应用到临时文件，得到一个逻辑数据上与表 A 相同的数据文件；5. 用临时文件替换表 A 的数据文件。> 说明：1. 在 copy 数据到新表期间，在原表上是加的 MDL 读锁（允许 DML，禁止 DDL）2. 在应用增量期间对原表加 MDL 写锁（禁止 DML 和 DDL）3. 根据表A重建出来的数据是放在 tmp_file 里的，这个临时文件是 InnoDB 在内部创建出来的，整个 DDL 过程都在 InnoDB 内部完成。对于 server 层来说，没有把数据挪动到临时表，是一个原地操作，这就是“inplace”名称的来源。
**4.1.2 gh-ost**
主要原理如下：1. 创建幽灵表：_xxx_gho（和原表结构一致），_xxx_ghc（用于记录变更日志）2. 在步骤 1 中创建的幽灵表上执行 DDL 语句3. 模拟成备库连接到真正的主库或备库- 将数据从原表拷贝到幽灵表
- 应用 binlog events 到幽灵表
4. 进行切换（cut-over）关于 gh-ost 的详细使用方式可以看看这篇文章《Online DDL工具 gh-ost》> https://mp.weixin.qq.com/s/V3mfuv8EP8UB1fwtfVRHuQ
**4.2 如何选择**
从原理中，可以看出几个关键点：- 可以看到 pt-osc、gh-ost、原生 Online DDL copy 方式（实际上是非 Online），都是需要 copy 原表数据到一个新表，这个是非常耗时的；
- pt-osc 采用触发器实现应用 DDL 期间的 DML, gh-ost 通过 binlog 应用 DDL 期间的 DML，理论上触发器会有一定的负载，且 gh-ost 可以从从库上拉取binlog，对主库的影响更小；
- 原生 Online DDL 中 Inplace 方式，对于 no-rebuild 方式，不需要重建表，只需要修改表的元数据，这个是非常快的；
- 原生 Online DDL 中 Inplace 方式，对于 rebuild 方式，需要重建表，但是也是在 InnoDB 内部完成的，比 copy 的方式要快；
因此，总结以下几个选择工具的判断依据：1. 如果 MySQL 版本是 5.6 之前，不支持 Online DDL，选用第三方工具 pt-osc 或 gh-ost；2. 如果 MySQL 版本是 5.6 以上，对于使用 copy table 方式的 DDL，不支持 Online，使用第三方工具 pt-osc 或 gh-ost；3. 对于可以使用 Inplace no-rebuild 方式的 DDL，使用原生 Online DDL；4. 对于使用 Inplace rebuild table 方式的 DDL，如果想使 DDL 过程更加可控，且对从库延迟比较敏感，使用第三方工具 pt-osc 或 gh-ost，否则使用原生 Online DDL；5. 对于想减少对主库的影响，实时交互，可以选用 gh-ost；
**pt-osc 参数字典**
**① 常用基本**&#8211;dry-run- 相当于真正执行前的测试。不会对原表做更改，只会创建和修改新表（不执行创建触发器、复制数据或替换原始表）
&#8211;execute- 真正执行 DDL
&#8211;user, -u- 用于登录的用户名
&#8211;password, -p- 指定密码，如果密码中包含逗号，必须使用反斜杠转义。
&#8211;host, -h- 指定连接的主机。
&#8211;port, -P- 指定端口号。
&#8211;socket- -S，指定用于连接的 socket 文件
&#8211;ask-pass- 不在命令行中指定密码，连接到 MySQL 时，提示输入密码。
&#8211;alter “string”- 指定表结构变更语句。不需要 **ALTER TABLE** 关键字，可以指定多个更改，用逗号隔开。
&#8211;database, -D- 指定数据库
**② 控制输出形式**&#8211;print- 将工具执行的 SQL 语句打印到 STDOUT，可以和 **&#8211;dry-run** 同时使用。
&#8211;progress- type: array; default: time,30
- 在复制行时，将进度报告打印到 STDERR。该值是一个逗号分隔的列表，由两部分组成。第一部分可以是 percentage, time, iterations（每秒打印次数）；第二部分指定对应的数值，表示打印的频率。
&#8211;quiet, &#8211;    q- 表示不要将信息打印到标准输出（禁用 **&#8211;progress**）。错误和警告仍然打印到 STDERR。
&#8211;statistics- 打印统计信息。
**③ 表上行为控制**
&#8211;alter-foreign-keys-method &#8220;string&#8221;- 指定修改外键以使引用新表。
当该工具重命名原始表以让新表取而代之时，外键跟随被重命名的表，因此必须更改外键以引用新表。支持两种方式：**rebuild_constraints** 和 **drop_swap** 。
可选值：
**auto：**- 自动决定那种方式是最好的。如果可以使用 **rebuild_constraints **则使用，否则使用 **drop_swap**。
**rebuild_constraints**
此方法使用 ALTER TABLE 删除并重新添加引用新表的外键约束。这是首选的方式，除非子表（引用 DDL 表中列的表）太大，更改会花费太长时间。通过比较子表的行数和将行从旧表复制到新表的速度来确定是否使用该方式。- 如果估计可以在比 **&#8211;chunk-time **更短的时间内修改子表，那么它将使用这种方式。估计修改子表（引用被修改表）所需的时间方法：行复制率乘以 **&#8211;chunk-size-limit**，因为 MySQL alter table 通常比复制行过程快得多。
> **说明：**由于 MySQL 中的限制，外键在更改后不能与之前的名称相同。该工具在重新定义外键时必须重命名外键，通常在名称中添加一个前导下划线 &#8216;_&#8217; 。在某些情况下，MySQL 还会自动重命名外键所需的索引。
**drop_swap**
禁用外键检查（FOREIGH_KEY_CHECKS=0），先删除原始表，然后将新表重命名到原来的位置。这与交换新旧表的方法不同，后者使用的是客户端应用程序无法检测到的原子 **RENAME**。- 这种方式更快，但是有一些风险：在 drop 原表和 rename 临时表之间的一段时间，DDL 的表不存在，查询这个表的语句将会返回报错。如果 rename 执行失败，没有修改成原表名称，但是原表已经被永久删除。
- 这种方式强制使用 **&#8211;no-swap-tables** 和 **&#8211;no-drop-old-table**。
**none**
这种方式和 drop_swap 类似，但是没有 swap。任何引用原表的外键将会指向一个不存在的表，这样会造成外键违规，在 **show engine innodb status** 中将会有类似下面的输出：- 
- 
- 
- 
- 
- 
Trying to add to index `idx_fk_staff_id` tuple:``DATA TUPLE: 2 fields;``0: len 1; hex 05; asc  ;;``1: len 4; hex 80000001; asc     ;;``But the parent table `sakila`.`staff_old```or its .ibd file does not currently exist!`这是因为原始表（在本例中为 sakila.staff）被重命名为 sakila.staff_old，然后 drop 掉了。提供了这种处理外键约束的方法，以便数据库管理员可以根据需要禁用该工具的内置功能。
&#8211;only-same-schema-fks- 只在与原始表相同数据库的表上检查外键。这个选项是危险的，因为如果 fks 引用不同数据库中的表，将不会被检测到。
&#8211;null-to-not-null- 允许将允许空值的列修改为不允许空值的列。包含空值的行将被转换为定义的默认值。如果没有给出明确的默认值，MySQL 会根据数据类型指定一个默认值，例如数字数据类型为 0，字符串数据类型为空
&#8211;[no]analyze-before-swap- 默认值：yes
- 在与旧表 swap 之前，在新表上执行 **ANALYZE TABLE**。在 MySQL 5.6 及更高版本，**innodb_stats_persistent** 开启的情况下，默认是 yes。
> 说明：innodb_stats_persistent 为 ON，表示统计信息会持久化存储，OFF 表示统计信息只存储在内存。
&#8211;[no]drop-new-table
- 默认值：yes
- 如果复制原始表失败，则删除新表。
- 指定 **&#8211;no-drop-new-table** 和 **&#8211;no-swap-tables** 将保留表的新修改副本，而不修改原始表，见 **&#8211;new-table-name**。
- **&#8211;no-drop-new-table** 不能和 **&#8211;alter-foreign-keys-method drop_swap** 同时使用。
&#8211;[no]drop-old-table- 默认值：yes
- 重命名后删除原始表。在原表被成功重命名以让新表取而代之之后，如果没有错误，该工具将在默认情况下删除原表。如果有任何错误，该工具将保留原始表。如果指定了 **&#8211;no-swap-tables**，则不删除旧表。
&#8211;[no]swap-tables- 默认值：yes
- 交换原始表和修改后的新表。这一步通过使具有新模式的表取代原来的表，从而完成了在线模式更改过程。原始表变成旧表，工具会删除它，除非禁用 **&#8211;[no]drop-old-table**。
使用 **&#8211;no-swap-tables** 会运行整个过程，它会创建新表，复制所有行但最后会删除新表。它的目的是运行一个更现实的演练。
&#8211;[no]drop-triggers- 默认值：yes
- 指定在旧表上删除触发器。**&#8211;no-drop-old-table** 强制 **&#8211;no-drop-triggers**。
&#8211;preserve-triggers- 在指定时保留旧触发器。在 MySQL 5.7.2 中，可以为一个给定的表定义具有相同触发事件和动作时间的多个触发器。这允许我们添加 pt-online-schema-change 所需的触发器，即使表已经有了自己的触发器。如果启用了此选项，那么在开始从原始表复制行之前，pt-online-schema-change 将尝试将所有现有触发器复制到新表，以确保在修改表之后可以应用旧触发器。
例如：
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`CREATE TABLE test.t1 (``     id INT NOT NULL AUTO_INCREMENT,``     f1 INT,``     f2 VARCHAR(32),``     PRIMARY KEY (id)``);``
``CREATE TABLE test.log (``   ts  TIMESTAMP,``   msg VARCHAR(255)``);``
``CREATE TRIGGER test.after_update`` AFTER``   UPDATE ON test.t1``   FOR EACH ROW``     INSERT INTO test.log \``  VALUES (NOW(), CONCAT("updated row row with id ", OLD.id, " old f1:", OLD.f1, " new f1: ", NEW.f1 ));`- 对于这个表和触发器组合，不可能使用 **&#8211;preserve-triggers** 和 **&#8211;alter**  “DROP COLUMN f1”，因为触发器引用被删除的列，会导致触发器失败。
- 在测试触发器将在新表上工作之后，触发器将从新表中删除，直到所有行都被复制，然后它们被重新应用。
- **&#8211;preserve-triggers** 不能与 **&#8211;no-drop-triggers**，**&#8211;no-drop-old-table**，**&#8211;no-swap-tables** 这些参数一起使用，因为 **&#8211;preserve-triggers** 意味着旧的触发器应该被删除并在新表中重新创建。由于不可能有多个具有相同名称的触发器，因此必须删除旧的触发器，以便能够在新表中重新创建它们。
- 使用 **&#8211;preserve-trigger** 和 **&#8211;no-swap-tables** 将导致原始表的触发器仍然被定义。如果同时设置了 **&#8211;no-swap-tables** 和 **&#8211;no-drop-new-table**，那么触发器将保留在原始表上，并将复制到新表上（触发器将具有随机后缀，因为没有唯一的触发器名称）。
&#8211;new-table-name
- type: string; default: %T_new
- 在交换表之前新建表名。将 %T 替换为原始表名。当使用默认值时，将在名称前添加最多 10 个 &#8216;_&#8217;（下划线），以查找唯一的表名称。如果指定了表名，则不会将其作为前缀，因此该表必须不存在。
&#8211;force
- 在使用 **&#8211;alter-foreign-keys-method = none** 的情况下，这个选项会绕过确认。
&#8211;tries
- 类型：array
- 遇到错误时，尝试的次数。下面是重试操作，以及它们的默认尝试次数和尝试之间的等待时间（以秒为单位）。
![](https://opensource.actionsky.com/wp-content/uploads/2020/09/表格.png)											
例子：- 
`--tries create_triggers:5:0.5,drop_triggers:5:0.5`格式：- 
```
operation:tries:wait[,operation:tries:wait]
```
- 必须同时指定 3 个值：operation，tries，wait
注意：大多数操作只在 MySQL 5.5 和更新版本中受到 **lock_wait_timeout**（参见 **&#8211;set-vars**）的影响，因为元数据锁。对于创建和删除触发器，尝试的次数应用于每个触发器的 **create trigger** 和 **drop trigger** 语句。对于复制行，尝试的次数适用于每个块，不是整个 table。对于交换表，尝试的次数通常只应用一次，因为通常只有一个 **rename table** 语句。对于重新构建外键约束，每个语句都有相应的尝试次数（用于重新构建约束的 alter 语句：**&#8211;alter-foreign-keys-method**；**drop_swap** 方法的其他语句）下面这些错误出现时，将会重试，- 
- 
- 
- 
- 
```
Lock wait timeout (innodb_lock_wait_timeout and lock_wait_timeout)`Deadlock found``Query is killed (KILL QUERY <thread_id>)``Connection is killed (KILL CONNECTION <thread_id>)``Lost connection to MySQL
```
错误和重新尝试次数被记录在 **&#8211;statistics** 中。
**④ 负载相关**
&#8211;critical-load- 类型：Array；默认值：Threads_running=50
- 在复制每个 chunk 之后检查 **SHOW GLOBAL STATUS**，如果负载太高则终止。该选项接受以逗号分隔的 MySQL 状态变量和阈值列表。格式：variable=MAX_VALUE（或：MAX_VALUE）。如果没有给出，该工具通过在启动时检查默认并将其加倍来确定阈值。
- 参见 **&#8211;max-load** 了解更多细节。不同的是，超过此选项指定的值时终止执行而不是暂停。使用该选项，可以作为一种安全检查，以防当原始表上的触发器给服务器增加过多负载导致停机。
&#8211;max-flow-ctl
- 类型：float
- 有点类似于 **&#8211;max-lag**，但是是针对 PXC 集群的。检查用于流控制的集群平均暂停时间，如果超过选项中所示的百分比，则让工具暂停。当检测到任何流控制活动时，0 值将使工具暂停。默认是没有流控制检查。该选项可用于 PXC 版本 5.6 或更高版本。
&#8211;max-load
- type: Array; default: Threads_running=25
- 复制每个块后，检查 **SHOW GLOBAL STATUS**，如果任何状态变量高于其阈值，则暂停执行。格式：variable=MAX 值 ( 或：MAX 值)。如果没有指定，该工具通过检查当前值并将其增加 20% 来确定一个阈值。
&#8211;sleep
- 类型：float，默认值：0
- 指定 copy 完每个 chunck 后，sleep 多久。当无法通过 **&#8211;max-lag** 和 **&#8211;max-load** 进行节流时，此选项非常有用。应该使用较小的，sub-second 值，例如 0.1，否则工具将会花费较长的时间来拷贝大表。
**⑤ 配置类**
&#8211;charset &#8220;string&#8221;, -A- 指定默认字符集，连接到 MySQL 后执行 set names character。
&#8211;default-engine
- 使用系统默认的存储引擎创建新表。
- 默认情况下，创建的新表和原表 engine 相同。当指定该选项时，则去掉建表语句中的 engine 选项，使用系统默认的存储引擎创建新表。
&#8211;defaults-file, -F
- 指定配置文件，需指定绝对路径。
&#8211;data-dir
- 指定新表的数据文件所在目录。仅可在 5.6 及以上版本使用。如果与 **&#8211;remove-data-dir** 同时使用，则忽略该参数。
&#8211;remove-data-dir
- 如果原始表是使用 DATA DIRECTORY 指定了数据文件目录，删除它并在 MySQL 默认数据目录中创建新表，而不创建新的 isl 文件。
&#8211;set-vars
- 设置 MySQL 变量列表：variable=value，以逗号分隔。 
- 默认情况下，该工具设置下面几个默认变量：
- 
- 
- 
wait_timeout=10000``innodb_lock_wait_timeout=1``lock_wait_timeout=60`&#8211;config- 指定配置文件列表，用逗号分隔，如果指定这个选项，必须是命令行的第一个选项。
&#8211;pause-file &#8220;string&#8221;- 当此参数指定的文件存在时，将暂停执行 DDL。比如，当 DDL 影响业务时，可创建指定的文件，暂停 DDL。
- 
`Sleeping 60 seconds because /tmp/a.txt exists`
**⑥ 复制 chunk 类**&#8211;chunk-size
- 指定每个复制块的行数，默认值：1000。可指定单位：k，M，G。
- 默认复制块的行为是：动态地调整块大小，试图使块在 **&#8211;chunk-time** 秒内复制完成。当没有显式设置此选项时，将使用其默认值作为起点，之后将忽略此选项的值。当如果显示指定该选项时，将禁用动态调整复制块的行为。
&#8211;chunk-time- 指定复制每个数据块所需要的时间。类型：float；默认值：0.5。
- 使用该选项可动态调整块大小，通过跟踪复制率（每秒的行数），并在复制每个数据块之后调整块大小，以使复制下一个数据块执行该选项指定的时间（以秒为单位）。
- 如果将此选项设置为零，则块大小不会自动调整；因此复制每个数据块时间将会变化，但复制块大小不会变化。
&#8211;chunk-size-limit- 复制块的最大限制。类型：float；默认值：4.0。
- 当表没有唯一索引时，块大小可能不准确。此选项指定错误的最大可容忍限制。该工具使用 <EXPLAIN> 来估计块中有多少行。如果估计值超过了期望的块大小乘以限制，那么该工具将跳过该块。
- 这个选项的最小值是 1，这意味着任何块都不能大于 **&#8211;chunk-size**。可以通过指定值 0 来禁用过大块检查。
&#8211;chunk-index- 指定对表进行分块的索引（FORCE index），如果指定索引不存在，那么工具将使用默认的方式选择索引。
&#8211;chunk-index-columns- 指定只使用复合索引中最左边的这么多列。这在 MySQL 查询优化器中的一个 bug 导致它扫描大范围的行，而不是使用索引精确地定位起始点和结束点的情况下非常有用。
**⑦ slave 相关**&#8211;slave-user
- 类型：字符串
- 指定连接从库的用户。这个用户可以有很少的权限，但是用户一定要是存在的。
&#8211;slave-password- 类型：字符串
- 指定连接到从库的密码，可以和 **&#8211;slave-user** 一块使用，指定的用户和密码在所有从库上必须是一样的。
&#8211;channel- 指定使用复制通道连接到服务器时使用的通道名称。
- 适用场景：多源复制情况下，**show slave status** 会返回两行，使用此选项指定复制通道。
&#8211;max-lag- type: time; default: 1s
- 指定当从库复制延迟大于该值时，暂停 data copy，直到所有复制的延迟都小于这个值。
- 在复制完每个块后，该工具会连接到所有从库，查看其复制延迟(Seconds_Behind_Master)。如果任何从库的延迟时间超过此选项的值，则工具将休眠 **&#8211;check-interval** 指定的时间，然后再次检查所有从库。如果指定 **&#8211;check-slave-lag**，那么该工具只检查该服务器的延迟，而不是所有服务器。如果希望准确地控制该工具检测哪些服务器，可以使用 **&#8211;recursion-method** 指定 DSN 值。
- 该工具永远等待从实例停止延迟。如果任何从实例停止，该工具将永远等待，直到从实例启动。
&#8211;recurse- type: int
- 发现从实例时在层次结构中要递归的级别数。默认是无限的。
&#8211;recursion-method- type：array; 默认值：processlist,host
- 用于判断是否存在从库的方式，可以的方式有：
processlist：show processlist;
hosts：show slave hosts
dsn=DSN：DSNs from a table
none：不查找从库
**⑧ check 类**&#8211;check-interval
- 指定检查 **&#8211;max-lag** 的时间间隔，默认值 1。如果任何从库的延迟时间超过 **&#8211;max-lag** 的值，将休眠 **&#8211;check-interval** 指定的时间,然后再次检查。
&#8211;check-slave-lag- 指定检查延迟的从库，以DSN的方式指定。当延迟超过 **&#8211;max-lag** 时，将暂停 data copy。
&#8211;skip-check-slave-lag- 指定 DSN，跳过检查指定从库延迟，可以指定多个， 例如：
- 
`–skip-check-slave-lag h=127.0.0.1,P=12345 –skip-check-slave-lag h=127.0.0.1,P=12346`&#8211;[no]check-replication-filters- 检查从库是否设置 replication filter，如 binlog_ignore_db 和  replicate_do_db，默认值为 yes。如果设置了，则中止执行。因为如果更新的表 Master 上存在，而 Slave 上不存在，会导致复制失败。使用 **&#8211;no-check-replication-filters** 选项来禁用该检查。
&#8211;[no]check-alter- 解析 **&#8211;alter** 指定的值，并警告可能的意外行为，默认值：yes。目前，它检查的有：**列名：**该工具的早期版本中，用 CHANGE COLUMN name new_name 重命名列会导致该列的数据丢失。现在会尝试解析 alter 语句并捕捉这些情况，因此重命名的列应该具有与原始列相同的数据。但是，执行此操作的代码并不是一个成熟的 SQL 解析器，因此应该首先使用 **&#8211;dry-run **和 **&#8211;print** 运行该工具，并验证它是否正确地检测到重命名的列。**drop primary key：**如果 **&#8211;alter** 包含 DROP PRIMARY KEY（大小写和空格不敏感），则会打印警告并退出，除非指定 **&#8211;dry-run**。更改主键可能是危险的，但是工具可以处理它。工具触发器，特别是 DELETE 触发器，最容易受到主键更改的影响。因此应该首先使用 **&#8211;dry—run** 和 **&#8212; print** 运行该工具，并验证触发器是否正确。
&#8211;[no]check-plan- 检查 SQL 执行计划。默认值 yes，则在执行 SQL 前执行 EXPLAIN，如果 MySQL 选择了一个糟糕的执行计划，会导致访问很多行，该工具将跳过表的 chunk。
- 该工具使用很多个方式来决定执行计划是否糟糕。
&#8211;[no]check-unique-key-change- 默认值为 yes，如果 **&#8211;alter** 的指定语句试图添加惟一索引，将不会执行，并打印一个 select 语句用于检查列上是否有重复记录。
- 因为 pt-online-schema-change 使用 INSERT IGNORE 将行复制到新表，所以如果正在写入的行主键冲突，不会报错，数据将丢失。
&#8211;[no]version-check- 默认值：yes
- 检查 Percona Toolkit、MySQL 和其他程序的最新版本。
相关推荐：
[新特性解读 | MySQL 8.0 之原子 DDL](https://opensource.actionsky.com/20200709-mysql/)
[技术分享 | Online DDL 工具 gh-ost](https://opensource.actionsky.com/20200730-mysql/)
[技术译文 | MySQL 8.x DDL 和查询重写插件](https://opensource.actionsky.com/20200812-mysql/)