# 新特性解读 | MySQL 8.0.18 有权限控制的复制

**原文链接**: https://opensource.actionsky.com/20191018-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-18T00:31:36-08:00

---

原文：Replication with restricted privileges
https://mysqlhighavailability.com/replication-with-restricted-privileges/
作者：Pedro Figueiredo
**背景****MySQL 8.0.18 以前**，从服务器都是在不检查权限的情况下执行复制事务的，这样做是为了能够让主服务器获取所有内容。实际上，这意味着从机完全信任主机机。但是，可能存在一些设置，其中更改跨越了主服务器和从服务器之间的安全边界。因此从服务器可能需要对复制流，进行强制执行数据访问约束。在这种情况下，用更严格、更安全的方式，执行来自主机的数据更改。**MySQL 8.0.18 开始**，引入了对从机应用程序线程的权限检查，从而允许在每个通道的上设置和检查用户权限。此功能在多源复制方案中特别有用，在这种情况下，需要从多个主服务器聚合数据，但希望保持对所应用数据的控制。换句话说，组织几个独立的数据库，需要以可控的方式聚合数据。对于已经在考虑如何将权限用作列级复制筛选的那些人，不能将具有受限权限的从机应用程序线程运行为筛选机制。在权限冲突的情况下，使从机应用程序线程停止，并停止复制。在这种情况下，会将适当的错误消息记录到错误日志中。为从机应用程序线程开启权限检查的三步骤：
1. 在从属节点上创建用户，可以使用现有用户。
2. 为目标用户设置所需的权限。
3. 为 **CHANGE MASTER TO** 使用新引入的选项，命名为 **PRIVILEGE_CHECKS_USER**，将预期的用户与从机应用程序线程权限的前后关联。
**在****从属节点上创建用户**创建一个到从服务器的客户端连接，并使用 **CREATE USER** 语句创建一个新用户：- `// On the slave`
- `mysql> CREATE USER 'rpl_applier_user'@'localhost';`
如果目标从机是我们启用权限检查拓扑结构中的唯一节点，并且已启用 `sql_log_bin`，那么在创建用户之前，请不要忘记禁用二进制日志记录：- `// On the slave`
- `mysql> SET @@session.sql_log_bin = 0;`
- `mysql> CREATE USER 'rpl_applier_user'@'localhost';`
- `mysql> SET @@session.sql_log_bin = 1;`
另一方面，如果我们有大量的从机并希望为所有从机启用权限检查，那么在主机创建用户并让语句被复制可能是完成它的一种好方法：- `// On the master`
- `mysql> CREATE USER 'rpl_applier_user'@'localhost';`
- `mysql> SET @@session.sql_log_bin = 0;`
- `mysql> DROP USER 'rpl_applier_user'@'localhost';`
- `mysql> SET @@session.sql_log_bin = 1;`
**设置用户的权限**除了我们可能需要或想要为用户赋予 **数据库/表/列** 级别的权限外，还需要应用程序线程才能正常运行的全局级别权限（或动态权限）：- **REPLICATIONAPPLIER**：动态权限，显式允许目标用户用作从机应用程序线程权限前后关联。需要此权限，以便被 **REPLICATION_SLAVE_ADMIN** 授予（能够执行 **CHANGE MASTER TO**…）但没有** GRANT** 权限的用户无法使用任何给定用户设置权限从机应用程序会话。
- **SESSION_VARIABLES_ADMIN**：需要设置在二进制日志中显式设置的会话变量。
- **FILE**：当且仅当使用基于语句的复制并在主数据库上执行 **LOAD DATA** 时才如此。
一组合理的授权语法是：- `// On the slave`
- `mysql> GRANT REPLICATION_APPLIER,SESSION_VARIABLES_ADMIN ON *.* TO 'rpl_applier_user'@'localhost';`
- `mysql> GRANT CREATE,INSERT,DELETE,UPDATE ON db1.* TO 'rpl_applier_user'@'localhost';`
同样，如果目标从机是我们启用权限检查拓扑结构中的唯一节点，并且已启用 `sql_log_bin`，那么在创建用户之前，请不要忘记禁用二进制日志记录：- `// On the slave`
- `mysql> SET @@session.sql_log_bin = 0;`
- `mysql> GRANT REPLICATION_APPLIER,SESSION_VARIABLES_ADMIN ON *.* TO 'rpl_applier_user'@'localhost';`
- `mysql> GRANT CREATE,INSERT,DELETE,UPDATE ON db1.* TO 'rpl_applier_user'@'localhost';`
- `mysql> SET @@session.sql_log_bin = 1;`
同样，如果我们想在整个拓扑中传递权限，只需在主服务器上运行命令：- `// On the master`
- `mysql> GRANT REPLICATION_APPLIER,SESSION_VARIABLES_ADMIN ON *.* TO 'rpl_applier_user'@'localhost';`
- `mysql> GRANT CREATE,INSERT,DELETE,UPDATE ON db1.* TO 'rpl_applier_user'@'localhost';`
- `mysql> SET @@session.sql_log_bin = 0;`
- `mysql> DROP USER 'rpl_applier_user'@'localhost';`
- `mysql> SET @@session.sql_log_bin = 1;`
角色也可以用于授予目标用户我们所需的权限。运行 **CHANGE MASTER TO**… 语句时不允许显式角色设置，但是我们可以使用默认角色来规避该设置。创建并设置角色：- `mysql> CREATE ROLE 'rpl_applier_role';`
- `mysql> GRANT REPLICATION_APPLIER,SESSION_VARIABLES_ADMIN ON *.* TO 'rpl_applier_role';`
- `mysql> GRANT 'rpl_applier_role' TO 'rpl_applier_user'@'localhost';`
对于我们希望用作从机应用程序线程权限前后用户的每个用户，请将角色分配为默认角色：- `mysql> SET DEFAULT ROLE 'rpl_applier_role' TO 'rpl_applier_user'@'localhost';`
如果需要，我们还可以向角色添加 **数据库/表/列** 级权限。**注意：**只有在重新启动线程后，在从机应用程序线程运行时（使用角色或直接授予权限时）执行的权限更改才会生效。
**将用户与从机应用程序权限前后关联**设置好用户之后，我们可以使用 **CHANGE MASTER TO**… 将用户与从机应用程序权限前后关联：- `// On the slave`
- `mysql> CHANGE MASTER TO PRIVILEGE_CHECKS_USER = 'rpl_applier_user'@'localhost';`
如果从机应用程序线程正在运行，我们需要将其停止以更改选项值：
- `// On the slave`
- `mysql> STOP SLAVE SQL_THREAD;`
- `mysql> CHANGE MASTER TO PRIVILEGE_CHECKS_USER = 'rpl_applier_user'@'localhost';`
- `mysql> START SLAVE SQL_THREAD;`
**可观察性**
与从机应用程序状态相关的 Performance Schema 表已得到增强，以显示新的 **CHANGE MASTER TO**&#8230; 语句选项 **PRIVILEGE_CHECKS_USER** 的状态：
- `// On the slave`
- `mysql> STOP SLAVE SQL_THREAD;`
- `mysql> CHANGE MASTER TO PRIVILEGE_CHECKS_USER = 'rpl_applier_user'@'localhost' FOR CHANNEL 'rpl_privileged_channel';`
- `mysql> START SLAVE SQL_THREAD;`
- `mysql> SELECT Channel_name, Privilege_checks_user FROM performance_schema.replication_applier_configuration;`
- `+------------------------+--------------------------------+`
- `| Channel_name           | Privilege_checks_user          |`
- `+------------------------+--------------------------------+`
- `| rpl_privileged_channel | 'rpl_applier_user'@'localhost' |`
- `+------------------------+--------------------------------+`
- `1 row in set (0.00 sec)`
**注意事项**
我们需要在使用带有权限检查的从机应用程序时或之前考虑一些规定：
- 运行具有特权检查的从机应用程序线程并不意味着要用作过滤机制，当权限检查失败时，将停止给定通道的复制，在这种情况下，会将适当的消息记录到错误日志中。
- 如果未完全信任复制源，则授予 **SESSION_VARIABLES_ADMIN** 可能是一个安全问题。
- 尽管我们可以授予列级权限，但是将禁用基于行的复制 `binlog_row_format=FULL` 时检查此类权限，因为二进制日志事件将不包含有关实际更改哪些列的信息。因此，仅在 `binlog_row_format=MINIMAL` 时才检查列级别权限。
- 由于复制应用程序必须执行更多工作，因此可能会观察到一些最小的吞吐量下降。
**简而言之**
在从服务器上，对先前配置的复制通道，设置最小的权限序列。
- `mysql> STOP SLAVE;`
- `mysql> CREATE USER u;`
- `mysql> GRANT REPLICATION_APPLIER,SESSION_VARIABLES_ADMIN,CREATE,INSERT,DELETE,UPDATE ON *.* TO u;`
- `mysql> CHANGE MASTER TO PRIVILEGE_CHECKS_USER = u;`
- `mysql> START SLAVE;`
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