# MySQL 8.0.22 GA！

**原文链接**: https://opensource.actionsky.com/20201020-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-10-20T00:38:17-08:00

---

作者：Geir Hoydalsvik
翻译：管长龙
本文来源：原文翻译
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 开发团队非常高兴地宣布，MySQL 8.0.22 现在可以下载了。除了 Bug 的修复，此版本中还添加了一些新功能。可以在 8.0.22 发行说明中找到更改和错误修复的完整列表。以下是该版本主要更新。
**Perpared Statements**
**每个 DML 语句预处理一次（WL＃9384）**
Perpared 语句只在 Perpare 时准备一次，而不是在每次执行时准备一次。同样，存储过程中的语句也将在第一次执行时准备一次。
这项工作的好处是：
- 性能增强：避免每次执行时进行昂贵的准备；
- 简化代码：避免繁琐的准备结构回滚。
**SHOW PROCESSLIST**
**重新实现 SHOW PROCESSLIST（WL＃9090）**
SHOW PROCESSLIST 将作为 PERFORMANCE_SCHEMA 中 processlist 表的视图实现，从 Performance Schema 而不是线程管理器中查询活动线程数据。当前的实现在保持全局互斥的同时，从线程管理器中跨活动线程进行迭代，这在繁忙的系统上可能是令人讨厌的。从 Performance Schema 中聚合相同的信息不会以任何方式影响用户负载。
可以通过系统变量：**&#8211;****-performance-schema-show-processlist[={OFF|ON}]**，来决定 SHOW PROCESSLIST 的实现方式。
**TIMESTAMP**
**检索存储在表中的 UTC 时间戳值（WL＃12535）**
新增 AT TIME ZONE 运算符，该运算符可用于检索 UTC 时间中的 TIMESTAMP 值。
例如，当会话的时区为 CET 并且时间为 2020-04-29 16:43:19 时，获取的 UTC 时间结果将变为为 2020-04-29 14:43:19。
`SELECT cast( a AT TIME ZONE 'UTC' AS DATETIME ) FROM t1；`
**Read Only Schema**
**提供 Schema 只读选项（WL＃13369）**
这是一种禁止写入模式。引入了新的 Schema 选项 **READ ONLY**。可以在 ALTER SCHEMA 语句中设置它，但不能在 CREATE SCHEMA 语句中设置它，否则会导致语法错误。要更改此选项，在该 Schema 上需要 ALTER 权限。 
`ALTER {DATABASE | SCHEMA} [db_name]``    alter_option ...`` ``alter_option: {``    [DEFAULT] CHARACTER SET [=] charset_name``  | [DEFAULT] COLLATE [=] collation_name``  | [DEFAULT] ENCRYPTION [=] {'Y' | 'N'}``  | READ ONLY [=] {DEFAULT | 0 | 1}``}`
**Error Log**
**可以通过 Performance Schema 查询错误日志（WL＃13681）**
错误日志可通过 Performance Schema 的 error_log 表获得。服务器在启动时从文件中读取错误日志，并在执行时保留最后 N 个条目。这使用户可以访问错误日志信息，而无需在操作系统级别拥有帐户，在文件系统级别通过向 mysql 用户授予 SSH / READ 权限实现，或者适配监视工具。
**User Management**
**避免对 ACL 表读取的锁定（WL＃14087）**
在某些情况下放宽了用于读取访问控制列表（ACL）系统表的隔离语义。这样做的目的是避免非管理员用户可以通过简单地从这些表中读取（例如，使用 mysqldump）来阻止 ACL DDL。
**ACL DDL 锁改进（WL＃14084）**在其他连接在 ACL 表上保持锁的情况下，改善用户管理类 DDL 和 FLUSH 操作。
**数据库对象和定义对象的修改依赖（WL＃14073）**如果某用户定义的存储程序、视图或计划任务存在，则 DROP USER 和 RENAME USER 将失败。必须先删除此类数据库对象，然后才能删除或重命名某用户。
**Optimizer**
**条件下推到派生表（WL＃8084）**
通过将 WHERE 条件从外部选择下推到派生表中，来减少了需要处理的行数。例如以下这个转换。
- 
`SELECT * FROM(SELECT i,j FROM t1)as dt WHERE i> 10;`- 
```
SELECT * FROM(SELECT i,j FROM t1 WHERE i> 10)as dt;
```
**扩展 CAST 函数 YEAR 参数（WL＃14015）**扩展 CAST 函数，以允许使用 YEAR 参数。通过允许 CAST 函数使用 YEAR 参数，可以将任何数据类型（GEOMETRY 除外）的参数正确地转换为 YEAR 数据类型。示例如下：
- 
- 
- 
- 
- 
- 
`mysql> SELECT CONVERT("11:35:00", YEAR), CONVERT(TIME "11:35:00", YEAR);``+---------------------------+--------------------------------+``| CONVERT("11:35:00", YEAR) | CONVERT(TIME "11:35:00", YEAR) |``+---------------------------+--------------------------------+``|                      2011 |                           2020 |``+---------------------------+--------------------------------+`
**Replication**
**自动连接其他异步复制通道（WL＃12649）**
在异步复制中实现了一种机制，该机制使副本在当前源不可访问或失败是，自动尝试重新建立与其他源的异步复制连接。其动机是通过自动化到另一源的异步复制连接的重新建立过程来使部署具有容错能力。新来源会自动从系统中的其他来源列表中选取。
**SLAVE 的别名（WL＃14171）**START SLAVE;
STOP SLAVE;
SHOW SLAVE STATUS;
SHOW SLAVE HOSTS;
RESET SLAVE;
添加别名命令：
START REPLICA;
STOP REPLICA;
SHOW REPLICA STATUS;
SHOW REPLICAS;
RESET REPLICA;
**重命名和弃用变量（WL＃14175）**group_replication_ip_whitelist 推荐改为 group_replication_ip_allowlist。
**Router**
**扩展 Router 连接最大数（WL＃10703）**
重构了 Router 插件以处理更大量的传入连接。该设计从每个连接一个 OS 线程更改为每个可用 CPU 内核一个 OS 线程，从而提高了 MySQL Router 的效率。
**在引导程序上启用 REST 接口（WL＃13906）**在 Router 引导程序期间，配置 Router 的 REST API，从而更易于监视路由器。
**通过 systemd 通知同步测试消息（WL＃13707 和 WL＃13708）**这项工作减少了运行 Router 测试套件所需的时间。是通过利用 systemd 通知支持来消除测试启动过程中不必要的等待，而不是等待固定的时间。
**Other**
**数据定期存储，可选择输出或转储到文件（WL＃13926）**
提供了一种将数据定期写入存储设备的方法，以防止发生写入停顿。添加了三个 GLOBAL 变量可覆盖 SESSION。
- select_into_disk_sync (ON / OFF)：通过长时间运行的 SELECT INTO  OUTFILE 语句或 SELECT INTO DUMPFILE 语句，启动同步写入输出文件缓冲区。 
- select_into_buffer_size：控制 fsync 的缓冲区的大小。在每个 fsync 之后，您可以选择休眠。
- select_into_disk_sync_delay：在每个 fsync 之后，休眠的毫秒数。
**InnoDB 添加配置选项以在 Linux 上使用 fallocate()（WL＃13782）**新的动态选项 innodb_extend_and_initialize。设置为 TRUE，则服务器将分配空间并使用 NULL 对其进行初始化，并且将日志条目添加到重做日志中以进行恢复。设置为 FALSE，则服务器将分配空间而不用 NULL 初始化它，并且将日志条目添加到重做日志中以进行恢复。这样做的动机是通过使用 fallocate() 来使插入更快地用于数据加载。
**libmysql 对 DNS SRV 的支持（WL＃13905）**在 MySQL 客户端库中增加了对 DNS SRV（RFC 2782）的支持。在高可用性方案中，数据通常镜像到服务器群集中。当前，开发人员可以在这些服务器之间共享查询负载，但是他们必须在连接中列出每个服务器。这很麻烦，因为更改任何服务器主机名或 添加/删除 服务器可能涉及更改整个应用程序场中的代码或配置文件。DNS SRV 记录允许 DNS 管理员将单个 DNS 域映射到多个服务器，并且 DNS 管理员可以在中央位置对此进行更新。DNS SRV 记录已被广泛使用，并且是用于枚举给定主机，域的实施服务器列表的标准机制。
**Deprecation and Removal**
**弃用 INFORMATION_SCHEMA.TABLESPACES（WL＃14064）**
因为该表未被使用，该表将在将来的主要版本中删除。
**弃用 memcache 插件（WL＃14131）**
在 INSTALL PLUGIN 上添加了弃用警告。memcached 插件将在以后的主要版本中删除。
以上就是 MySQL 8.0.22 的主要更新。> **8.0.22 Release Notes：**https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-22.html