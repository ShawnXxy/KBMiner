# 技术译文 | MySQL 8.0.19 GA!

**原文链接**: https://opensource.actionsky.com/20190114-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-01-17T00:06:34-08:00

---

作者：Geir Hoydalsvik翻译：管长龙原文：https://mysqlserverteam.com/the-mysql-8-0-19-maintenance-release-is-generally-available/
MySQL 开发团队非常高兴地宣布，MySQL 8.0.19 现在可从 dev.mysql.com 下载。除了 bug 修复，此版本中还添加了一些新功能。以下是重点介绍！
# InnoDB ReplicaSet
继 InnoDB Cluster 作为我们基于组复制的第一个完全集成的 MySQL HA 解决方案之后，InnoDB ReplicaSet 提供了另一个完整的解决方案（基于MySQL 复制）。InnoDB ReplicaSet 的基本思想是对经典 MySQL 复制执行与 InnoDB Cluster 对组复制所做的相同操作。我们采用了一种非常强大但可能很复杂的技术，在 MySQL Shell 中为其提供了易于使用的 AdminAPI。
仅需几个易于使用的 Shell 命令，即可从头开始配置 MySQL 复制数据库体系结构，包括使用 CLONE 进行数据供应，设置复制并执行手动切换或故障切换。 MySQL Router 了解拓扑结构，并会自动进行负载平衡或流量重定向。
# Router
1. 在路由中添加对 InnoDB ReplicaSet 的支持(WL＃13188)。这意味着从元数据 schema 加载和缓存拓扑信息，以及定期更新设置的状态信息，以执行正确的路由操作。2. 处理路由中的元数据升级(WL＃13417)。3. 新的启动选项（–account）：允许重复使用现有帐户(WL＃13177)。指定 Router 与 Server 通讯时应使用的帐户。Router 需要一个服务器帐户才能与InnoDB Cluster 通信。到目前为止，该帐户始终在引导过程中自动创建。
# SQL
1. 实现 `ALTER TABLE…DROP / ALTER CONSTRAINT` 语法(WL＃12798)`SQL DROP CONSTRAINT` 和 `ALTER CONSTRAINT` 子句添加到 `ALTER TABLE` 语句中。这项工作是对(WL#929)的补充，并修复了Bug(＃3742)。2. 具有 JSON Schema 验证约束的表，应针对具体的行返回错误(WL＃13195)在诊断区域中添加了一个 SQL 条件，并带有错误代码&#8220;The JSON document location X failed requirement Y at JSON Schema location Z&#8221;。另请参阅下面的(WL＃13196)。3. TIMESTAMP / DATETIME 值可以包含时区详细信息(WL＃10828)时区详细信息将与 TIMESTAMP 值一起包含在内。如果没有明确的时区信息或偏移，则日期/时间可能存在在某些时区中定义不正确，例如夏时制将时间向后更改。这是来自 Booking.com(Bug＃83852)的功能请求。4. 在递归公用表表达式中支持 LIMIT(WL＃12534)CTE 中增加了对 LIMIT 的支持。LIMIT 是 CTE 中的总行数，而不是每次迭代可能产生的行数。另请参见(Bug＃92857)。5. 实现表值构造函数：VALUES() (WL＃10358)为表值构造函数实现了标准 SQL 语法。但是由于 VALUES() 函数与一种 MySQL 非标准功能的冲突，决定使用表值构造函数的 SQL 标准详细形式为：VALUES ROW(1、2),…   另请参见Bug(＃77639)。6. 在 `INSERT…ON DUPLICATE KEY UPDATE` 中引用 old/new row (WL＃6312)扩展了 INSERT…VALUES / SET…ON DUPLICATE KEY UPDATE 语法，从而可以为其中的新行和列声明别名该行，并在 UPDATE 表达式中引用这些别名。此新功能的目的是能够用行别名和列别名替换 VALUES(<expression>)子句。
**Optimizer**1. 增强按组进行的松散索引扫描(WL＃13066)
通过取消对查询中可能存在的中缀范围数（非分组列上的范围）的当前限制，改进了用于 GROUP BY 查询的松散索引扫描（LIS）。 
此功能基于Facebook(Bug＃90951)的贡献。
2. BKA 在迭代器执行器中(WL＃13002)
在迭代器执行器中实现了 BKA（批密钥访问）。 目前，仅支持内部联接，稍后将添加其他联接类型。
**Information Schema**角色的 INFORMATION_SCHEMA 视图(WL＃10895)。实现了 SQL Roles 的 SQL 标准信息架构视图。- APPLICABLE_ROLES 视图显示适用于当前用户的角色。
- ADMINISTRABLE_ROLE_AUTHORIZATIONS 视图显示了适用于当前用户的角色，也可以将其授予其他用户。 
- ENABLED_ROLES 视图显示为当前用户启用的角色。 
- ROLE_TABLE_GRANTS 视图显示为当前用户启用的角色的表授予。 
- ROLE_COLUMN_GRANTS 视图显示为当前用户启用的角色的列授予。
- ROLE_ROUTINE_GRANTS 视图显示了为当前用户启用的角色的例行授予。
**Security**1. 每位用户的 FAILED_LOGIN_ATTEMPTS / PASSWORD_LOCK_TIME 计数器功能(WL＃13515)
管理员可以配置用户帐户，这样由于密码错误导致的连续登录失败过多，将导致临时帐户锁定。 可以使用 CREATE USER 和 ALTER USER 语句的 FAILED_LOGIN_ATTEMPTS 和 PASSWORD_LOCK_TIME 选项对每个帐户配置所需的失败次数和锁定时间。请参阅创建用户密码管理选项。
2. 在密钥环中存储秘密数据(WL＃12859)增强了现有的密钥环插件，以支持一种称为 SECRET 的新型数据。这使用户可以存储，检索和管理密钥环中的任何不透明数据（最大16K）。密钥环后端不会解释秘密，而只是将其视为 BLOB。 此功能通常将用于存储秘密数据，例如密码和证书。
**InnoDB**1. 支持采样表数据以生成直方图(WL＃8777)
通过从聚集索引中采样数据页面并提供存储在这些页面中的记录来实现(WL＃9127)中定义的处理程序 API。
2. 分区表的区分大小写的名称(WL＃13352)解决了与分区名称和分隔符的字母大小写差异有关的用户问题。 解决方案是始终以不区分大小写的方式处理分区名称，分区分隔符（＃p＃），子分区名称和子分区分隔符（＃sp＃），以便区分大小写对文件名无关。 磁盘和存储在数据字典中的元数据。 这包括在导入期间处理分区表空间文件名。
**Replication**1. 配置基于行的复制(WL＃12968)
可确保复制通道仅接受基于行的复制。这允许限制在从属设备上执行的指令的类型。副作用是当与复制应用程序相关联时，限制用户所需的权限数量。
2. MTS：禁用 log-slave-updates / binlog 时 slave-preserve-commit-order(WL＃7846)即使工作线程未将更改记录到副本二进制日志中，也能实现更适当的提交顺序（ –log-slave-updates = off）。这样做的主要动机是能够在没有启用二进制日志的副本上打开并行复制，而在主服务器和从服务器之间没有不同的提交历史记录。换句话说，保留了复制提交流中观察到的事务提交历史记录，因为应用程序并行执行传入的事务，但是按照它们出现在流中的顺序来提交它们。
3. 对异步复制中的 TLS 1.3 的支持(WL＃13392)在MySQL客户端和服务器之间的连接中支持TLS 1.3(WL＃12361)。这项工作实现了 CHANGE MASTER 命令上的 MASTER_TLS_CIPHERSUITES 选项，group_replication_recovery_tls_version 插件选项和group_replication_recovery_tls_ciphersuites 插件选项。
# X Protocol
1. 连接压缩(WL＃9252)通过 X 协议实现了客户端-服务器数据压缩。压缩算法可根据服务器功能进行协商。2. 新增 Zstd 压缩(WL＃13442)
在 X 协议中实现了 zstd 压缩。X 协议现在支持三种压缩算法：deflate，lz4 和 zstd。已经发现 zstd 算法的性能比 deflate 更好，并且压缩率比 lz4 好得多。3. 为创建集合添加架构验证方法(WL＃12965)
在 X 插件中实现了文档架构验证器。从 DevAPI 的角度来看，用户调用 &#8220;var coll = schema.createCollection(&#8221; mycollection&#8221;,{validator:validationDoc})&#8221; 。createCollection() 在 X 插件中实现，并且通过调用 (WL＃11999) 引入的 JSON_SCHEMA_VALID(<json_schema>,<json_document>) 函数来扩展此实现。4. 具有 Json Schema 验证的集合必须返回具体行错误(WL＃13196)
通过标识文档违反架构约束的确切位置来扩展(WL＃12965)。
# MTR testsuite
将需要 MyISAM 的 binlog，sys_vars 和 funcs_1 套件中的测试用例，移到单独的 .test 文件中(WL＃13410 和 WL＃13241)
这使 MTR 测试套件可以在没有 MyISAM 引擎的情况下在服务器上运行。
# 其他
1. 对于交互式终端，默认情况下使 mysql 命令行工具的 –binary-as-hex 处于打开状态(WL＃13038)默认为在“交互模式”下运行的命令行工具启用 –binary-as-hex 选项。对于非交互式运行，将保留当前默认值 –binary-as-hex（OFF）。从历史上看，MySQL 命令行工具一直要求服务器将接收到的所有数据转换为文本，以便可以显示它们。但是对于某些数据（例如 GEOMETRY 数据类型），转换会生成二进制字符串，其中可能包含不可打印的符号，这些符号可能会使某些终端出现乱码。通过打印十六进制转储而不是文本可以避免这种情况。2. 在 UDF API 中指定字符集(WL＃12370)
扩展了用户定义函数（UDF）API，以允许 UDF 创建者指定在参数和返回值中使用哪些字符集。以前，UDF API 仅假定字符串参数和返回值均为 ASCII。3. Sys Schema 用本机函数替换存储的函数(WL＃13439)
在 Sys Schema 存储函数中，用 performance schema 函数替换存储函数。performance schema 函数为：format_bytes()，format_pico_time()，ps_current_thread_id() 和 ps_thread_id(connection_id)。原来的 Sys Schema 功能已被弃用，并将在将来的某些版本中删除。4. 为 Windows 启用 mysql 命令行命令 &#8220;system&#8221; (WL＃13391)
在 Windows 的 MySQL 命令行工具中启用系统命令。system 命令将其参数作为 OS 命令执行并显示结果。它过去一直在 Linux 上运行，并且由于 MSVC CRT 现在支持所有必需的 API，因此现在也应该在 Windows 上启用它。这修复了Bug(＃58680)。5. 组件服务以添加 &#8220;admin&#8221; 会话(WL＃13378)
允许其调用者创建不受 max_connection 限制的特殊类型的 SQL 会话。这样做是为了确保内部机制不受 max_connections 的限制。例如，当服务器达到 max_connections 限制时，组复制将无法运行。6. 向重建索引错误添加更多信息(WL＃12589)
扩展了 DUP_ENTRY_KEY 情况下给出的错误信息，以在错误消息中包括表名以及键名和键值。这项工作基于 Facebook（Bug＃92530）的贡献。另请参见Bug(＃47207)。7. 使用信号 SIGUSR1 刷新日志(WL＃13689)
信号 SIGUSR1 重新定义为 SIGHUP 的轻量版本。 SIGUSR1 将导致服务器刷新错误日志，常规日志和慢查询日志，但不发送 MySQL 状态报告。8. 拆分 errmgs-utf8.txt 文件(WL＃13423)将 errmgs-utf8.txt 文件拆分为一个文件，该文件用于向客户端发送消息，将另一个消息向错误日志发送消息（messages_to_clients.txt 和 messages_to_error_log.txt）。这是代码重构，可帮助开发人员区分客户端消息和错误日志消息。
# 弃用和移除
1. 弃用 YEAR 数据类型的显示宽度和 UNSIGNED(WL＃13537)弃用了语法YEAR(4)。请改用等效的 YEAR。这项工作还不建议在 YEAR 中使用 UNSIGNED。未记录 UNSIGNED 与 YEAR 一起使用，并且无效。2. 从 SHOW CREATE 输出中删除整数显示宽度(WL＃13528)
将 SHOW CREATE 更改为不输出整数显示宽度，除非也使用 ZEROFILL。如果没有 ZEROFILL，则整数显示宽度无效。这项工作是不赞成使用整数类型(WL＃13127)的显示宽度属性的逻辑结果。3. X Protocol：删除 Mysqlx.Sql.StmtExecute 消息中已弃用的名称空间(WL＃13057)
从支持的名称空间列表中删除了名称空间 xplugin。因此，xplugin 名称空间将成为未知标识符，并且不会处理在该名称空间内发送的任何管理命令。如果用户继续使用此命名空间，则会通过标准错误消息通知他们。从 5.7.14 开始，不推荐使用 Mysqlx.Sql.StmtExecute 消息中的 xplugin 命名空间。
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