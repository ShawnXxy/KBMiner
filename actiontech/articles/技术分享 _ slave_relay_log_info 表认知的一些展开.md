# 技术分享 | slave_relay_log_info 表认知的一些展开

**原文链接**: https://opensource.actionsky.com/20191016-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-16T00:55:37-08:00

---

slave_relay_log_info 表是这样的：- `mysql> select * from mysql.slave_relay_log_info\G`
- 
- ` *************************** 1. row ***************************`
- `  Number_of_lines: 7`
- `   Relay_log_name: ./mysql-relay.000015`
- `    Relay_log_pos: 621`
- `  Master_log_name: mysql-bin.000001`
- `   Master_log_pos: 2407`
- `        Sql_delay: 0`
- `Number_of_workers: 16`
- `               Id: 1`
- `     Channel_name:`
slave_relay_log_info 表存储 slave sql thread 的工作位置。
在从库启动的时候时，读取 slave_relay_log_info 表中存储的位置，并把值传给 &#8220;show slave status&#8221; 中的 Relay_Log_File、Relay_Log_Pos，下次 &#8220;start slave&#8221; 是从这个位置开始继续回放 relay log。slave_relay_log_info 表存储的是持久化的状态、show slave status 输出的是内存中的状态：
- 两者输出的位置可能不一样
- stop slave 或者正常关闭 mysqld，都会将内存中的状态持久化到磁盘上（slave_relay_log_info表中）
- 启动 mysqld 时会读取磁盘状态，初始化给内存状态
- start slave 时生效的是内存状态
slave io thread 按照 Master_Log_File、Read_Master_Log_Pos 位置读取主库的 binlog，并写入到本地 relay log（注意这两个位点信息保存在 slave_master_info 表中）；slave sql thread 按照 Relay_Log_Name、Relay_Log_Pos 位置进行 realy log 的回放。
但是同一个事务在从库 relay log 中的 position 和主库 binlog 中的 position 是不相等的，slave_relay_log_info 表通过 Master_log_name、Master_log_pos 这两个字段记录了 relay log 中事务对应在主库 binlog 中的 position。
我们得知道如果 slave io thread 重复、遗漏的读取主库 binlog 写入到 relay log 中，sql thread 也会重复、遗漏地回放这些 relay log。**也就是说从库的数据是否正确，io thread 的位置是否正确也非常重要。**
在 MySQL 5.6 以前，复制位点信息只能存储在数据目录的 master.info 文件中，在回放事务后更新到文件中（默认每次回放10000个事务更新，受参数 sync_relay_log_info 控制）。即使每个事务都更新文件，意外宕机时也没法保证持久性一致性。
MySQL 5.6 开始，可以设置 &#8211;relay-log-info-repository=TABLE，将 slave sql thread 的工作位置存储在 mysql.slave_relay_log_info 表中，如果这个表是 InnoDB 这样的支持事务的引擎，则从库每回放一个事务时都会在这个事务里同时更新 mysql.slave_relay_log_info 表，使得 sql thread 的位置与数据保持一致。事实上在 5.6.0-5.6.5 的版本，slave_relay_log_info 表默认使用的是 MyISAM 引擎，之后的版本才改为 InnoDB，不过再考虑到 MySQL 5.6.10 才 GA，这个坑踩过的人应该不多。
**更新机制**
引用手册：- `sync_relay_log_info = 0`
- `  If relay_log_info_repository is set to FILE, the MySQL server performs no synchronization of the relay-  log.info file to disk; instead, the server relies on the operating system to flush its contents periodically as with any other file.`
- `  If relay_log_info_repository is set to TABLE, and the storage engine for that table is transactional, the table is updated after each transaction. (Thesync_relay_log_info setting is effectively ignored in this case.)`
- `  If relay_log_info_repository is set to TABLE, and the storage engine for that table is not transactional, the table is never updated.`
- 
- `sync_relay_log_info = N > 0`
- `  If relay_log_info_repository is set to FILE, the slave synchronizes its relay-log.info file to disk (using fdatasync()) after every N transactions.`
- `  If relay_log_info_repository is set to TABLE, and the storage engine for that table is transactional, the table is updated after each transaction. (Thesync_relay_log_info setting is effectively ignored in this case.)`
- `  If relay_log_info_repository is set to TABLE, and the storage engine for that table is not transactional, the table is updated after every N events.`
一般的运维规范都会要求 relay_log_info_repository=TABLE，默认值 sync_relay_log_info=10000 此时会失效，变成每回放一个事务都会在这个事务里同时更新 mysql.slave_relay_log_info 表，保证持久性，以最终保证复制的数据一致。当然 InooDB 的持久性需要 innodb_flush_log_at_trx_commit=1 来保证。
前面有一句话“也就是说从库的数据是否正确，io thread 的位置是否正确也非常重要”。简单来说 io thread 位置保存在 slave_master_info 表中，其实设置和 relay_log_info_repository 类似，不同的是它的持久化保障通常与性能冲突很大：
- 必须设置 master_info_repository = TABLE 和 sync_master_info=1，刷盘的单位是 binlog event 而不是事务，写放大很严重，性能损耗大
所以通常 sync_master_info 使用默认值 10000， io thread 的位置无法保证持久化，也就没法保证正确。MySQL 有另一个参数 relay_log_recovery 提供一种机制来保证 mysqld crash 后 io thread 位置的准确性，稍后进行介绍。
**master_auto_position**
master_auto_position 的作用是根据从库的 Executed_Gtid_Set 自动寻找主库上对应 binlog 位置，这是在 GTID 出现后的一个功能。
这里思考一个问题：开启 master_auto_position 后，slave io thread 能直接根据从库的 Executed_Gtid_Set 定位主库上 binlog 的位置吗？还需要 slave_relay_log_info、slave_master_info 表中记录的位点信息吗？
其实 slave_relay_log_info、slave_master_info 表依然发挥作用：
- 当第一次或者 reset slave 后，执行 start slave，io thread 将从库的 Executed_Gtid_Set 发往主库，获取到对应的 File、Position，之后更新到从库的 slave_relay_log_info、slave_master_info 表中
- 当 slave_relay_log_info、slave_master_info 表中存在位置信息后，此后无论是重启复制还是重启 mysqld，都是直接从这两个地方获取 File、Position，并从这里开始读取 binlog 和回放 relay log
注意：执行 &#8220;reset slave&#8221; 会删除从库上的 relay log，并且重置 slave_relay_log_info 表，即重置复制位置。如果 master_auto_position=0，下次启动复制时会从新开始获取并回放主库的 binlog，造成错误。
**relay_log_recovery**
当启用 relay_log_recovery，mysqld 启动时，recovery 过程会生成一个新的 relay log，并初始化 slave sql thread 的位置，表现为：
- slave_relay_log_info 表的 Relay_Log_Name 值更新为最新的日志名， Relay_Log_Pos 值更新为一个固定值 4（应该是头部固定信息占 4个偏移量）
- 内存状态即 show slave status 输出中的 Relay_Log_File、Relay_Log_Pos，也更新成上面一样的
并且 slave io thread 的位置也会初始化，表现为：- slave_master_info 表中的 Master_log_name、Master_log_pos 不会改变
- 内存状态即 show slave status 输出中的 Master_Log_File、Read_Master_Log_Pos，会更新为 slave_relay_log_info 表中 Master_Log_Name、Master_Log_Pos
io thread 这个位置的初始化思路就是：既然以前记录的位置不确定是否准确，那就直接不要了。sql thread 回放到哪，我就从哪开始重新拿主库的 binlog，这样准没错。一个事务在 relay log 中的 position 对应到主库 binlog 的 position 是这样来确定的：- slave_relay_log_info 表中的 Relay_log_name 与 Master_log_name，Relay_Log_Pos 与 Master_Log_Pos 始终一一对应，代表同一个事务的位置。
所以，即使 sync_master_info 表的持久化无法保证，relay_log_recovery 也会将 io thread 重置到已经回放的那个位置。
relay_log_recovery 的另一个作用是防止 relay log 的损坏，因为默认 relay log 是不保证持久化的（也不推荐设置 sync_relay_log=1），当操作系统或者 mysqld crash 后，sql thread 可能会因为 relay log 的损坏、丢失导致错误。
**一些结论**
- 当开启 GTID 和 master_auto_position，并设置 relay_log_recovery=1，即使 relay_log_info_repository 设置为 file，操作系统或者 mysqld crash 后，mysqld 下次重启启动复制都能保证数据与主库一致。即使 slave_relay_log_info 表中记录的位置不是最新的，sql thread 可能会重复回放一部分事务，但是从库已经存在这些事务的 GTID，这部分重复的事务会被跳过。
- 当未开启 GTID 和 master_auto_position，必须要设置 relay_log_info_repository=table、relay_log_recovery=1，操作系统或者 mysqld crash 后，mysqld 下次重启启动复制才能保证数据与主库一致。
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