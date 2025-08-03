# MySQL 8.0.21 GA！重点解读

**原文链接**: https://opensource.actionsky.com/20200714-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-07-14T00:29:56-08:00

---

本文来源：翻译 管长龙
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 8.0.21 版本已于昨日发布（dev.mysql.com），开始对一些术语如 Master / Slave 等做了替换。下面是来自官方团队对此版本的重点功能解读。
> 更详细的内容请参考：
https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-21.html
**InnoDB**
添加全局禁用 redo log 功能的配置项(WL#13795)支持动态启停 redo log，可使数据库写入速度更快，服务也更容易崩溃并丢失整个实例数据。- 
`ALTER INSTANCE ENABLE|DISABLE INNODB REDO_LOG;`主要适用在加载初始数据时，首先禁用 redo log，加载数据，再次开启。
表空间文件名验证变为可选项(WL#14008)
通过参数 &#8211;innodb-validate-tablespace-paths (ON|OFF) 可决定是否开启表空间文件名验证功能。在 HDD 系统中扫描表空间开销很大，在我们知道用户不会频繁移动文件的情况下，可以通过跳过验证减少启动时间。即使该参数设置为 OFF，依然可以使用 ALTER TABLESPACE 语法。
锁系统的优化(WL#10314) 
以往用单个闩锁保护保护所有队列的访问，扩展性很差，队列管理成为瓶颈，因此引入更细化的闩锁方法。将每个表和每一行都可以视为资源，并且事务可以请求对资源的访问权限。锁系统将 GRANTED 和 WAITING 的请求都存在一个队列中。为了允许队列并发操作，提供了一种安全快速锁定队列的方式。
将所有的 InnoDB 表空间限定为已知的目录 (WL#13065) 
将表空间文件的位置限定在已知目录(datadir, innodb_data_home_dir, innodb_directories, and innodb_undo_directory)。目的是限制可以在任何位置创建文件从而导致恢复过程出现意外的情况。
Undo DDL 支持 ACID (WL#11819)
改进 Undo 表空间性能和安全性，可对 Undo 表空间自动截断。对 Undo 表空间的 CREATE / TRUNCATE 操作都被记录到 redo log。优点是避免了之前解决方案在 Undo 截断过程中需要两个检查点，这些检查点可能阻塞系统。此修改还修复了几个影响到 Undo 的命令：CREATE、DROP 和 TRUNCATE。  
**JSON**
添加 JSON_VALUE 函数(WL#12228)目的是简化 JSON 值的索引创建，可以从给定的 JSON 值中获取指定位置的值，并作为指定类型返回。- 
`SELECT JSON_VALUE('{"name": "Evgen"}', '$.name')`以 VARCHAR(512) 返回的无引号字符串 Evgen，并带有 JSON 的默认排序规则。- 
```
SELECT JSON_VALUE('{"price": 123.45}', '$.price' RETURNING DECIMAL(5,2))
```
以 DECIMAL(5,2) 返回 123.45。
**SQL DDL**
CREATE TABLE…AS SELECT 语句成为原子语句(WL#13355)以往此举作为两个不同的事务执行（CREATE TABLE 和 SELECT INTO）进行处理，结果在某些情况下，已经提交 CREATE TABLE 但回滚了 SELECT INTO。目前解决了此问题并顺便修复了(Bug#47899)。
**优化器**
引入了新的优化器参数以禁用限制优化(WL#13929)prefer_ordering_index 默认开启，新的开关控制优化，存在限制子句时从非排序索引切换到分组依据和排序依据的排序索引。
半联接和单表 UPDATE / DELETE (WL#6057)
以往单表的快速查询绕过了优化器并直接执行，从而使得这些语句无法从更高级的优化（半联接）中受益。
- 
- 
- 
- 
- 
- 
`// 以往以下两句用不到 semijoin，较慢``UPDATE t1 SET x=y WHERE z IN (SELECT * FROM t2); ``DELETE FROM t1 WHERE z IN (SELECT * FROM t2);``
``//以下语句可以用到，较快``SELECT x FROM t1 WHERE z IN (SELECT * FROM t2);`优化后，以上 SQL 语句像其它查询一样通过优化器和执行器。不再需要在 UPDATE / DELETE 语句中添加无关表（多表 UPDATE / DELETE 可以使用 semijoin）。此外可在语句上执行 EXPLAIN FORMAT = TREE 和 EXLPAIN ANALYZE。目前解决了此问题并顺便修复了(Bug#96423)和(Bug##35794)。
**组复制**
降低缓存参数的最小值(WL#13979)group_replication_message_cache_size  从 1 GB 降低到 128 MB。这使 DBA 可以减少 XCom 缓存的大小，以便 InnoDB Cluster 可以成功地部署在具有少量内存（例如 16GB）和良好网络连接的主机上。
指定可以通过哪些端点恢复流量(WL#13767)
用于指定在分布式恢复期间用于组复制的 IP 和端口。目的是控制网络基础架构中流量的恢复，例如：出于稳定性或安全性原因。
以 C++ 编译 XCom (WL#13842)由于 C++ 的高级功能和更丰富的标准库，加速未来的发展。
将重要的  GP 日志消息分类为系统消息(WL#13769)
将某些组复制日志消息重新分类为系统消息。始终记录系统消息，而与服务器日志级别无关。目的是确保 DBA 可以观察组中的主要事件。
开启组复制语句以支持凭据作为参数(WL#13768)扩展 START GROUP_REPLICATION 命令，以将 USER，PASSWORD，DEFAULT_AUTH 和 PLUGIN_DIR 接受为恢复通道的可选参数。目的是避免将凭据存储在文件中，这在某些环境中可能是安全问题。
组成员尝试自动恢复参数默认值修改(WL#13706)group_replication_autorejoin_tries 默认值从 0 增加到 3。当该值为 0 时，组复制网络分区超过 5 秒钟会导致成员退出该组而不返回。导致需要执行手动操作以将成员带回。目标是提供“自动网络分区处理”，包括从网络分区中恢复，最有效的方法是将 group_replication_autorejoin_tries 设置大于 0。
组成员等待参数默认值修改(WL#13773)group_replication_member_expel_timeout 从 0 增加到 5。以降低速度较慢的网络上或出现瞬时网络故障时不必要的驱逐和主要故障转移的可能性。默认值的新值表示该成员将在无法访问后 10 秒钟被驱逐：在怀疑成员已离开组之前花了 5 秒钟等待，然后在驱逐该成员之前又等待了 5 秒钟。
支持二进制日志校验和(WL#9038)
支持组复制中二进制日志校验和。在进行此更改之前，组复制插件要求禁用 binlog-checksum，现在取消了此限制。Binlog 校验和的目的是通过自动计算和验证二进制日志事件的校验和来确保数据完整性。
**X 插件**
&#8211;mysqlx-bind-address 支持多值(WL#12715)允许用户使用多个 IP 地址（接口）配置 X Plugin 绑定地址，用户可以在其中跳过主机的不需要的接口。MySQL 8.0.13(WL#11652)中引入了对多个地址的绑定。
**路由器**
用户可配置的日志文件名(WL#13838)可将日志写入 mysqlrouter.log 以外的文件名，并将控制台消息重定向到 stdout 而不是 stderr。
支持从应用程序中隐藏节点(WL#13787)
增加了对每个实例元数据属性的支持，该属性指示给定实例是隐藏的，不应用作目标候选对象。MySQL Router 支持在 InnoDB Cluster 的各个节点之间分布连接。通常将负载分配给所有节点是一个很好的默认设置，并且可以预期，但是用户可能有理由将一个节点排除在接收负载之外。例如：用户可能希望从应用程序流量中排除给定的服务器实例，以便可以在不中断传入流量的情况下对其进行维护。
**其它**
创建 / 更改用户增加 JSON 描述（WL#13562）元数据以 JSON 对象的结构添加到 mysql.user 表的 user_attributes 列中。JSON 对象允许用户还将其用户帐户元数据存储到该列中，例如：- 
- 
- 
`ALTER USER foo ATTRIBUTE '{ "free_text" : "This is a free form text" }'; ``//将存储为 metadata``{"metadata": {"free_text": "This is a free form text"}}. `用户元数据在用户的信息架构表中公开。
为管理员连接端口支持单独的 TLS 证书集(WL#13850)
为用户端口和管理员端口使用不同的 TLS 证书。MySQL 支持用于管理连接的专用端口。以前，管理员连接端口和常规客户端-服务器连接端口都共享同一组 TLS 证书。在托管的托管环境中，这带来了挑战，因为：
1. 客户可能希望携带自己的证书
2. 内部和外部证书的证书轮换策略可能不同。
现在，我们为管理连接端口引入了一套单独的 TLS 证书以及其他相关的配置和状态参数，并对来自这两个不同端口的连接使用了单独的 SSL 上下文。
异步客户端的压缩协议(WL#13510)
8.0.16 中添加了对异步客户端的支持。8.0.18 添加了对同步客户端协议压缩的支持。最后一步确保异步客户端也支持协议压缩。目的是减少跨数据中心的网络流量。这项工作基于 Facebook 的贡献(BUG#88567)。
安全的客户端库 LOAD DATA LOCAL INFILE 路径/目录(WL#13168)
客户端配置将指定允许和不允许的内容。然后，当服务器请求文件时，客户端将检查规格并接受或拒绝请求。
**弃用**
在分区函数中弃用对前缀键的支持(WL#13588)如果表在 PARTITION BY KEY 子句中包含具有前缀键索引的列，则产生弃用警告。将来，该语法将给出错误消息。
**感谢您使用MySQL！**