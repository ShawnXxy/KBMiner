# MySQL 8.0.18 GA 正式发布!

**原文链接**: https://opensource.actionsky.com/2019-10-15-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-15T23:33:24-08:00

---

MySQL Server 8.0.18、5.7.28 和 5.6.46 已于昨日正式发布。MySQL 开发团队也第一时间发布了更新说明文章。以下是原文翻译。> 原文：《The MySQL 8.0.18 Maintenance Release is Generally Available》
[The MySQL 8.0.18 Maintenance Release is Generally Available](https://mysqlserverteam.com/the-mysql-8-0-18-maintenance-release-is-generally-available/)
作者：Geir Hoydalsvik
MySQL 开发团队非常高兴地宣布，MySQL 8.0.18 现在可以从 dev.mysql.com 下载了。除了 bug 修复，此版本中还添加了一些新功能。请从 dev.mysql.com 或 Yum、APT、SUSE 库等途径下载 8.0.18。源代码在GitHub上。您可以在 8.0.18 发行说明中找到更改和 bug 修复的完整列表。以下是重点！
**SQL（语句）****Hash Join** (WL＃2241) 此功能由 Erik Froseth 实现，为在 MySQL 中执行内部等价联接的一种方式。例如：`SELECT*FROM t1 JOIN t2 ON t1.col1=t2.col1;`可以在 8.0.18 中作为 Hash Join 执行。Hash Join 不需要任何索引来执行，并且在大多数情况下比当前的块嵌套循环算法更有效。**EXPLAIN ANALYZE** (WL＃4168) 此功能由 Steinar H. Gunderson实现。EXPLAIN ANALYZE 将运行查询，然后生成 EXPLAIN 输出，以及有关优化程序估计如何与实际执行相匹配的其他信息。EXPLAIN ANALYZE 在新的迭代器执行程序的基础上构建，并在实际迭代器的顶部实现定时迭代器，从而提供有关每次调用的精确信息。对于每个迭代器，我们提供估计的执行成本，估计的返回行数，返回第一行的时间，返回所有行的时间（即实际成本），此迭代器返回的行数以及循环次数。整个查询执行以树形结构表示，其中节点是迭代器。**Iterator UNION** (WL#13000) 此功能由 Steinar H. Gunderson 实现。UNION，UNION ALL，WITH RECURSIVE 和不合格 SELECT COUNT(*) 会在新的迭代框架执行。**将类型转换节点注入到项目树中，以避免数据类型不匹配** (WL＃ 12108) 此功能由 Catalin Besleaga 实现。将表达式和条件内的隐式类型转换操作添加到项目树中，判断这些表达式和条件在提供的参数的数据类型与预期数据之间是否存在不匹配类型。此方法对用户没有可见的影响。
**GIS（地理信息系统）**
**任何几何类型值之间的椭球模型 ST_Distance** (WL＃12216) 此功能由 Torje Digernes 实现。对地理几何的距离测量，从单点到多个点的支持 (WL＃9347) 扩展到单点，线，多边形，多个点，多个线，多个多边形的几乎所有几何组合的集合 (WL＃12216)。
**Only OpenSSL（SSL类型库）**
**从 MySQL 代码库中删除对 wolfSSL 和 yaSSL 的支持** (WL＃13290 和 WL＃13289) 此功能由 Kristofer Älvring 实现。展望未来，MySQL 将仅使用 OpenSSL 作为其 SSL / TLS 库。
**Password（加密）**
**创建用户可用随机密码** (WL＃11772) 此功能由 KristoferÄlvring 实现。CREATE USER / ALTER USER / SET PASSWORD 语句添加语法，以生成强随机密码，并将其作为结果集行返回给客户端。此功能使用户更容易创建强密码。添加的语法是：- `CREATE USER user IDENTIFIED BY RANDOM PASSWORD;`
- `ALTER USER user IDENTIFIED BY RANDOM PASSWORD;`
- `SET PASSWORD [FOR user] TO RANDOM;`
## Compression（压缩）
**压缩协议可在配置中指定** (WL＃12475 和 WL＃12039) 此功能由 Bharathy Satish 和 Thayumanavar X 撰写。Sachithanantha 扩展了MySQL 协议，以处理更多的客户端-服务器压缩选项，而不仅仅是 zlib。客户端和服务器之间的初始握手连接将基于新的功能标志选择两者都支持的最佳压缩方法。压缩方法将由客户端和服务器选项的交集定义。两者都可以是 zlib，zstd 和 uncompressed 的任何组合。压缩的优先顺序为 zlib，zstd，uncompressed。即，如果服务器具有“uncompressed ，zstd”，而客户端具有“ zlib，zstd，uncompressed”，则将使用 zstd 协议。也可以指定 zstd 的压缩级别。此功能基于 Facebook 的贡献，请参见 bug＃88567。
**Replication（复制）**
**具有受限特权的复制** (WL＃12966) Pedro Figueiredo，Abhinav Agarwal 和 Neha Kumari 在复制通道上实现了特权检查。其动机是实现从不受信任的源到受信任的目标之间的安全复制，即建立从安全边界的“外部”到“内部”的复制流。
**Group Replication****（组复制）****将 OFFLINE_MODE 添加到** `group_replication_exit_state_action` (WL＃12895) 此功能由 Nuno Carvalho 实现。该 `group_replication_exit_state_action` 选项用于指定当服务器无意离开组时组复制的行为。新 OFFLINE_MODE 行为将关闭所有连接，并禁止不具有 CONNECTION_ADMIN 或 SUPER 特权的用户建立新连接，否则它的行为类似于现有 READ_ONLY 模式。**TLS 1.3支持** (WL＃12990) 由 Tiago Jorge 和 Tiago Vale 在 GCS / XCom 层中实现了 TLS 1.3 支持。这样就可以在组复制中的所有组成员之间使用 TLS 1.3 来确保通信的安全。**传递消息服务** (WL＃12896) 由 Anibal Pinto 实现。MySQL 模块可以使用该服务通过组复制的现有组通信连接，将带有标识标签的通用消息传输给所有组成员。此方法对用户没有可见的影响。
**Router（路由）****前置的 MySQL 路由密钥环** (WL＃12974) 由 Jan Kneschke 实现。它允许 Router 管理用户列出存储在密钥环中的帐户，从密钥环中删除帐户，更改密钥环中帐户的密码以及更改密钥。主密钥环中的文件名位置。**在路由日志中添加可选的时间戳解析度** (WL＃11194) 由 Thomas Nielsen 实现了路由日志文件亚秒级的时间戳精度。时间戳精度可以使用路由配置文件进行配置。
**MTR（**测试套件**）**
**将测试用例移动到单独的 .test 文件，将需要 MyISAM 中的 rpl 套件** (WL＃13053) 中，由 Pooja Lamba实现。这使 MTR 测试套件可以在没有MyISAM 引擎的情况下在服务器上运行。
**Other（其它）**
**InnoDB：****添加新选项以在空闲时控制写 IOPS** (WL＃13115) Mayank Prasad 实现了新选项 innodb_idle_flush_pct，该选项在 InnoDB 空闲时控制写 IOPS。目的是减少写 IO，以延长闪存的寿命。此功能基于 Facebook 的贡献，请参见 bug＃88566 。**动态链接 Protobuf**(WL＃13126) Tor Didriksen 改变了 Protobuf 与服务器的链接方式。SQL 开发人员希望在 XPlugin 之外（例如在复制中）使用 Protobuf。这是不可能的，因为 Protobuf 不能与一个以上的组件进行静态链接，因为它保持内部状态。解决方案是动态链接它。**加大 max_prepared_stmt_count**** 最大值** (WL＃13342) Tor Didriksen 增加了最大值 `max_prepared_stmt_count` 从 1048576 到 4194304。默认为 16K。**将 sys Schema 移至 mysql server中** (WL＃12673) Christopher Powers 将 sys Schema 的源代码移至主服务器存储库中，并且通常将 sys Schema 实现与服务器集成在一起。这是内部简化，没有外部影响。**错误消息参数的编译时检查** (WL＃13110) Jens EvenBlomsøy 实现了CMake 配置选项，可在编译时检查错误消息参数的数量和类型。默认情况下，选项 `-DCHECK_ERRMSG_FORMAT` 为 OFF。其动机是使开发人员能够在编译时检测错误，而不是在运行时获取意外错误。
**Deprecation and Removal****（弃用和移除）****MySQL 8.0.18 不会删除任何功能，但会将某些功能标记为 8.0 中已弃用。****不推荐使用的功能将在将来的主要版本中删除。****在libmysql中弃用 MYSQL_PWD 环境变量的使用**(WL#13449) Georgi Kodinov 实现，即如果没有提供密码，libmysql 将从 OS 环境变量 MYSQL_PWD 中读取密码。不鼓励使用此功能，因为环境变量可以由本地用户检查。要求用户使用其他更安全的机制来存储密码。**弃用** `--relay-log-info-file` 和 `--master-info-file` (WL＃11031)LuísSoares 解决了这两个选项缺少弃用警告的事实。这些应该已经分别与其“父”选项 `relay_log_info_repository=FILE` 和 `master_info_repository=FILE` 一起弃用。**弃用** `slave-rows-search-algorithms` (WL＃12892) 选项 slave-rows-search-algorithms 选项控制复制应用程序在应用 UPDATE 或 DELETE 行事件时如何查找表中的行。从 8.0 开始，此选项的默认值为 HASH_SCAN 和 INDEX_SCAN，这对于性能和正确性而言始终是最佳的。因此，最好不要使用替代算法。**弃用** `log_bin_use_v1_row_events` (WL＃12926) 当用户设置或读取log_bin_use_v1_row_events的值时弃用警告。当前默认值为 V2 行事件。V2 是 MySQL 5.6 中引入的，从那时起，MySQL 可以解析和解释 v1 和 v2 行事件。**弃用** WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS函数（WL＃13178）当用户使用 WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS函数时，实现了弃用警告。该警告指出，用户应使用 WAIT_FOR_EXECUTED_GTID_SET 而不是 WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS。前者取代后者。
**感谢您使用 MySQL！**
**社区近期动态**
**No.1**
**10.26 DBLE 用户见面会 北京站**
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/默认标题_横版海报_2019.09.16.jpg)											
爱可生开源社区将在 2019 年 10 月 26 日迎来在北京的首场 DBLE 用户见面会，以线下**互动分享**的会议形式跟大家见面。
时间：10月26日 9:00 &#8211; 12:00 AM
地点：HomeCafe 上地店（北京市海淀区上地二街一号龙泉湖酒店对面）
重要提醒：
1. 同日下午还有 dbaplus 社群举办的沙龙：聚焦数据中台、数据架构与优化。
2. 爱可生开源社区会在每年10.24日开源一款高质量产品。本次在 dbaplus 沙龙会议上，爱可生的资深研发工程师闫阿龙，将为大家带来《金融分布式事务实践及txle概述》，并在现场开源。
**No.2**
**「3306π」成都站 Meetup**
知数堂将在 2019 年 10 月 26 日在成都举办线下会议，本次会议中邀请了五位数据库领域的资深研发/DBA进行主题分享。
时间：2019年10月26日 13:00-18:00
地点：成都市高新区天府三街198号腾讯成都大厦A座多功能厅
**No.3**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
- 技术交流群，进群后可提问
QQ群（669663113）
- 社区通道，邮件&电话
osc@actionsky.com
- 现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.4**
**社区技术内容征稿**
征稿内容：
- 格式：.md/.doc/.txt
- 主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
- 要求：原创且未发布过
- 奖励：作者署名；200元京东E卡+社区周边
投稿方式：
- 邮箱：osc@actionsky.com
- 格式：[投稿]姓名+文章标题
- 以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系