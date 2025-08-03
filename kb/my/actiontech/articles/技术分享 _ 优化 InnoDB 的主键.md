# 技术分享 | 优化 InnoDB 的主键

**原文链接**: https://opensource.actionsky.com/20190904-innodb/
**分类**: 技术干货
**发布时间**: 2019-09-04T00:30:32-08:00

---

> 作者：Yves Trudeau
**前言**作为 Percona 的首席架构师，我的主要职责之一是对客户的数据库进行性能方面的优化，这使得工作复杂且非常有趣。在这篇文章中，我想讨论一个最重要的问题：**选择最佳的 InnoDB 主键。**
**InnoDB 主键有什么特别之处？**InnoDB 被称为索引组织型的存储引擎。主键使用的 B-Tree 来存储数据，即表行。这意味着 **InnoDB 必须使用主键**。如果表没有主键，InnoDB 会向表中添加一个隐藏的自动递增的 6 字节计数器，并使用该隐藏计数器作为主键。InnoDB 的隐藏主键存在一些问题。您应该始终在表上定义显式主键，并通过主键值访问所有 InnoDB 行。InnoDB 的二级索引也是一个B-Tree。搜索关键字由索引列组成，存储的值是匹配行的主键。通过二级索引进行搜索通常会导致主键的隐式搜索。
什么是 B-Tree？一个 B-Tree 是一种针对在块设备上优化操作的数据结构。块设备或磁盘有相当重要的数据访问延迟，尤其是机械硬盘。在随机位置检索单个字节并不比检索更大的数据花费的时间更少。这是 B-Tree 的基本原理，InnoDB 使用的数据页为 16KB。让我们尝试简化 B-Tree 的描述。B-Tree 是围绕这键来组织的数据结构。键用于搜索 B-Tree 内的数据。B-Tree 通常有多个级别。数据仅存储在最底层，即叶子节点。其他级别的页面（节点）仅包含下一级别的页面的键和指针。如果要访问键值的数据，则从顶级节点-根节点开始，将其包含的键与搜索值进行比较，并找到要在下一级访问的页面。重复这个过程，直到你达到最后一个级别，即叶子节点。理论上，每个 B-Tree 级别的读取都需要一次磁盘读取操作。在实践中，总是有内存缓存节点，因为它们数量较少且经常访问，因此适合缓存。
![](.img/253ea84d.png)											
一个简单的三级 B-Tree 结构
有序的插入示例
让我们考虑以下 sysbench 表：- `mysql> show create table sbtest1\G`
- `*************************** 1. row ***************************`
- `       Table: sbtest1`
- `Create Table: CREATE TABLE `sbtest1` (`
- `  `id` int(11) NOT NULL AUTO_INCREMENT,`
- `  `k` int(11) NOT NULL DEFAULT '0',`
- `  `c` char(120) NOT NULL DEFAULT '',`
- `  `pad` char(60) NOT NULL DEFAULT '',`
- `  PRIMARY KEY (`id`),`
- `  KEY `k_1` (`k`)`
- `) ENGINE=InnoDB AUTO_INCREMENT=3000001 DEFAULT CHARSET=latin1`
- `1 row in set (0.00 sec)`
- 
- `mysql> show table status like 'sbtest1'\G`
- `*************************** 1. row ***************************`
- `           Name: sbtest1`
- `         Engine: InnoDB`
- `        Version: 10`
- `     Row_format: Dynamic`
- `           Rows: 2882954`
- ` Avg_row_length: 234`
- `    Data_length: 675282944`
- `Max_data_length: 0`
- `   Index_length: 47775744`
- `      Data_free: 3145728`
- ` Auto_increment: 3000001`
- `    Create_time: 2018-07-13 18:27:09`
- `    Update_time: NULL`
- `     Check_time: NULL`
- `      Collation: latin1_swedish_ci`
- `       Checksum: NULL`
- ` Create_options:`
- `        Comment:`
- `1 row in set (0.00 sec)`
Data_length 值是 B-Tree 主键的大小。B-Tree 的二级索引，即 k_1 索引，Index_length 是其大小。因为 ID 主键自增，所以 sysbench 表数据是顺序插入的。当按主键顺序插入时，即使 `innodb_fill_factor` 设为 100，InnoDB 最多使用 15KB 的数据填充空间。这导致在初始插入数据之后，需要拆分页面。页面中还有一些页眉和页脚。如果页面太满且无法添加更多数据，则页面将拆分为两个。同样，如果两个相邻页面的填充率低于 50％，InnoDB 将合并它们。
例如，这是以 ID 顺序插入的 sysbench 表：- `mysql> select count(*), TABLE_NAME,INDEX_NAME, avg(NUMBER_RECORDS), avg(DATA_SIZE) from information_schema.INNODB_BUFFER_PAGE`
- `    -> WHERE TABLE_NAME='`sbtest`.`sbtest1`' group by TABLE_NAME,INDEX_NAME order by count(*) desc;`
- `+----------+--------------------+------------+---------------------+----------------+`
- `| count(*) | TABLE_NAME         | INDEX_NAME | avg(NUMBER_RECORDS) | avg(DATA_SIZE) |`
- `+----------+--------------------+------------+---------------------+----------------+`
- `|    13643 | `sbtest`.`sbtest1` | PRIMARY    |             75.0709 |     15035.8929 |`
- `|       44 | `sbtest`.`sbtest1` | k_1        |           1150.3864 |     15182.0227 |`
- `+----------+--------------------+------------+---------------------+----------------+`
- `2 rows in set (0.09 sec)`
- 
- `mysql> select PAGE_NUMBER,NUMBER_RECORDS,DATA_SIZE,INDEX_NAME,TABLE_NAME from information_schema.INNODB_BUFFER_PAGE`
- `    -> WHERE TABLE_NAME='`sbtest`.`sbtest1`' order by PAGE_NUMBER limit 1;`
- `+-------------+----------------+-----------+------------+--------------------+`
- `| PAGE_NUMBER | NUMBER_RECORDS | DATA_SIZE | INDEX_NAME | TABLE_NAME         |`
- `+-------------+----------------+-----------+------------+--------------------+`
- `|           3 |             35 |       455 | PRIMARY    | `sbtest`.`sbtest1` |`
- `+-------------+----------------+-----------+------------+--------------------+`
- `1 row in set (0.04 sec)`
- 
- `mysql> select PAGE_NUMBER,NUMBER_RECORDS,DATA_SIZE,INDEX_NAME,TABLE_NAME from information_schema.INNODB_BUFFER_PAGE`
- `    -> WHERE TABLE_NAME='`sbtest`.`sbtest1`' order by NUMBER_RECORDS desc limit 3;`
- `+-------------+----------------+-----------+------------+--------------------+`
- `| PAGE_NUMBER | NUMBER_RECORDS | DATA_SIZE | INDEX_NAME | TABLE_NAME         |`
- `+-------------+----------------+-----------+------------+--------------------+`
- `|          39 |           1203 |     15639 | PRIMARY    | `sbtest`.`sbtest1` |`
- `|          61 |           1203 |     15639 | PRIMARY    | `sbtest`.`sbtest1` |`
- `|          37 |           1203 |     15639 | PRIMARY    | `sbtest`.`sbtest1` |`
- `+-------------+----------------+-----------+------------+--------------------+`
- `3 rows in set (0.03 sec)`
该表不适合缓冲池，但查询为我们提供了很好的解释。 B-Tree 主键的页面平均有 75 条记录，并存储少于 15KB 的数据。sysbench 以随机顺序插入索引 k_1。sysbench 在插入行之后创建索引并且 InnoDB 使用排序文件来创建它。您可以轻松估算 InnoDB B-Tree 中的级别数。上表需要大约 40K 页（3M / 75）。当主键是四字节整数时，每个节点页面保持大约 1200 个指针。因此叶子上层大约有 35 页，然后在 B-Tree 上的根节点（PAGE_NUMBER = 3）我们总共有三个层级。
一个随机插入的例子如果你是一个敏锐的观察者，你意识到以主键的随机顺序插入页面通常是不连续的，平均填充系数仅为 65-75％ 左右。我修改了 sysbench 以随机的 ID 顺序插入并创建了一个表，也有 3M行。
结果表格要大得多：- `mysql> show table status like 'sbtest1'\G`
- `*************************** 1. row ***************************`
- `           Name: sbtest1`
- `         Engine: InnoDB`
- `        Version: 10`
- `     Row_format: Dynamic`
- `           Rows: 3137367`
- ` Avg_row_length: 346`
- `    Data_length: 1088405504`
- `Max_data_length: 0`
- `   Index_length: 47775744`
- `      Data_free: 15728640`
- ` Auto_increment: NULL`
- `    Create_time: 2018-07-19 19:10:36`
- `    Update_time: 2018-07-19 19:09:01`
- `     Check_time: NULL`
- `      Collation: latin1_swedish_ci`
- `       Checksum: NULL`
- ` Create_options:`
- `        Comment:`
- `1 row in set (0.00 sec)`
虽然以 ID 的顺序插入 B-Tree 主键的大小是 644MB，但是以随机顺序插入的大小约为 1GB，多了 60％。
显然，我们的页面填充系数较低：- `mysql> select count(*), TABLE_NAME,INDEX_NAME, avg(NUMBER_RECORDS), avg(DATA_SIZE) from information_schema.INNODB_BUFFER_PAGE`
- `    -> WHERE TABLE_NAME='`sbtestrandom`.`sbtest1`'group by TABLE_NAME,INDEX_NAME order by count(*) desc;`
- `+----------+--------------------------+------------+---------------------+----------------+`
- `| count(*) | TABLE_NAME               | INDEX_NAME | avg(NUMBER_RECORDS) | avg(DATA_SIZE) |`
- `+----------+--------------------------+------------+---------------------+----------------+`
- `|     4022 | `sbtestrandom`.`sbtest1` | PRIMARY    |             66.4441 |     10901.5962 |`
- `|     2499 | `sbtestrandom`.`sbtest1` | k_1        |           1201.5702 |     15624.4146 |`
- `+----------+--------------------------+------------+---------------------+----------------+`
- `2 rows in set (0.06 sec)`
随机顺序插入时，主键页现在只填充了大约 10KB 的数据（~66％）这是正常和预期的结果。对于某些工作负载情况而言，这很糟糕。
**确定工作负载类型**第一步是确定工作负载类型。当您有一个插入密集型工作负载时，很可能顶级查询是在一些大型表上插入的，并且数据库会大量写入磁盘。如果在 MySQL 客户端中重复执行“**show processlist;**”，则会经常看到这些插入。这是典型的应用程序记录大量数据。有许多数据收集器，他们都等待插入数据。如果等待时间过长，可能会丢失一些数据。如果您在插入时间上有严格的等级协议，而在读取时间上有松弛的等级协议，那么您显然有一个面向插入的工作负载，您应该按主键的顺序插入行。也可以在大型表上具有不错的插入速率，但这些插入是按批处理排队并执行的。没有人真的在等待这些插入完成，服务器可以轻松跟上插入的数量。对于您的应用程序而言，重要的是大量的读取查询将进入大型表，而不是插入。您已经完成了查询调优，即使您有良好的索引，数据库也会以非常高的速率从磁盘读取数据。当您查看 MySQL 进程列表时，您会在大表上看到多次相同的选择查询表单。唯一的选择似乎是添加更多内存来降低磁盘读取次数，但是这些表正在快速增长，并且您无法永久地添加内存。如果您无法确定是否存在插入量大或读取繁重的工作负载，那么您可能只是没有大的工作量。在这种情况下，默认是使用有序插入，而使用 MySQL 实现此目的的最佳方法是通过自动增量整数主键。这是许多 ORM 的默认行为。
读密集型工作负载我曾看到了很多读密集型工作负载，主要是在线游戏和社交网络应用程序。最重要的是，一些游戏具有社交网络功能，例如：在游戏进行过程中观看朋友的分数。在我们进一步讨论之前，我们首先需要确认读取效率低下。当读取效率低下时，顶部选择查询表单将访问许多不同的 InnoDB 页面，这些页面接近于检查的行数。用 pt-query-digest 工具对 MySQL 慢日志进行分析，详细级别包括 “InnoDB” 时，会暴露这两个数量。
这是一个示例输出（我删除了一些行）：- `# Query 1: 2.62 QPS, 0.00x concurrency, ID 0x019AC6AF303E539E758259537C5258A2 at byte 19976`
- `# This item is included in the report because it matches --limit.`
- `# Scores: V/M = 0.00`
- `# Time range: 2018-07-19T20:28:02 to 2018-07-19T20:28:23`
- `# Attribute    pct   total     min     max     avg     95%  stddev  median`
- `# ============ === ======= ======= ======= ======= ======= ======= =======`
- `# Count         48      55`
- `# Exec time     76    93ms   637us     3ms     2ms     2ms   458us     2ms`
- `# Lock time    100    10ms    72us   297us   182us   247us    47us   176us`
- `# Rows sent    100   1.34k      16      36   25.04   31.70    4.22   24.84`
- `# Rows examine 100   1.34k      16      36   25.04   31.70    4.22   24.84`
- `# Rows affecte   0       0       0       0       0       0       0       0`
- `# InnoDB:`
- `# IO r bytes     0       0       0       0       0       0       0       0`
- `# IO r ops       0       0       0       0       0       0       0       0`
- `# IO r wait      0       0       0       0       0       0       0       0`
- `# pages distin 100   1.36k      18      35   25.31   31.70    3.70   24.84`
- `# EXPLAIN /*!50100 PARTITIONS*/`
- `select * from friends where user_id = 1234\G`
该 friends 表的定义是：- `CREATE TABLE `friends` (`
- `  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,`
- `  `user_id` int(10) unsigned NOT NULL,`
- `  `friend_user_id` int(10) unsigned NOT NULL,`
- `  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,`
- `  `active` tinyint(4) NOT NULL DEFAULT '1',`
- `  PRIMARY KEY (`id`),`
- `  UNIQUE KEY `uk_user_id_friend` (`user_id`,`friend_user_id`),`
- `  KEY `idx_friend` (`friend_user_id`)`
- `) ENGINE=InnoDB AUTO_INCREMENT=144002 DEFAULT CHARSET=latin1`
我在测试服务器上构建了这个简单的例子。该表很容易适合内存，因此没有磁盘读取。这里重要的是“page distin”和“Rows Examine”之间的关系。如您所见，该比率接近 1 。这意味着 InnoDB 很少每页访问一行。对于给定的 user_id 值，匹配的行分散在 B-Tree 主键上。
我们可以通过查看示例查询的输出来确认这一点：- `mysql> select * from friends where user_id = 1234 order by id limit 10;`
- `+-------+---------+----------------+---------------------+--------+`
- `| id    | user_id | friend_user_id | created             | active |`
- `+-------+---------+----------------+---------------------+--------+`
- `|   257 |    1234 |             43 | 2018-07-19 20:14:47 |      1 |`
- `|  7400 |    1234 |           1503 | 2018-07-19 20:14:49 |      1 |`
- `| 13361 |    1234 |            814 | 2018-07-19 20:15:46 |      1 |`
- `| 13793 |    1234 |            668 | 2018-07-19 20:15:47 |      1 |`
- `| 14486 |    1234 |           1588 | 2018-07-19 20:15:47 |      1 |`
- `| 30752 |    1234 |           1938 | 2018-07-19 20:16:27 |      1 |`
- `| 31502 |    1234 |            733 | 2018-07-19 20:16:28 |      1 |`
- `| 32987 |    1234 |           1907 | 2018-07-19 20:16:29 |      1 |`
- `| 35867 |    1234 |           1068 | 2018-07-19 20:16:30 |      1 |`
- `| 41471 |    1234 |            751 | 2018-07-19 20:16:32 |      1 |`
- `+-------+---------+----------------+---------------------+--------+`
- `10 rows in set (0.00 sec)`
行通常由数千个 ID 值分开。虽然行很小，大约 30 个字节，但 InnoDB 页面不包含超过 500行。随着应用程序变得流行，用户越来越多，表大小也越来越接近用户数的平方。一旦表格超过 InnoDB 缓冲池限制，MySQL 就开始从磁盘读取。更糟糕的情况是，没有缓存，我们需要每个 friend 的 IOPS。如果这些要求的速率是平均 300条/秒而言，每个用户有 100 个朋友，则 MySQL 需要每秒访问多达 30000 个页面。显然，这不符合长期规划。
我们需要确定访问表的所有条件。为此，我使用 pt-query-digest 并且我提高了返回的查询表单数量的限制。假设我发现：- 93％ 访问 userid
- 5％ 访问 friendid
- 2％ 访问 id
上述比例非常普遍。当存在显性访问模式时，我们可以做一些事情。朋友表关系是多对多的。
使用 InnoDB，我们应该将这些表定义为：- `CREATE TABLE `friends` (`
- `  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,`
- `  `user_id` int(10) unsigned NOT NULL,`
- `  `friend_user_id` int(10) unsigned NOT NULL,`
- `  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,`
- `  `active` tinyint(4) NOT NULL DEFAULT '1',`
- `  PRIMARY KEY (`user_id`,`friend_user_id`),`
- `  KEY `idx_friend` (`friend_user_id`),`
- `  KEY `idx_id` (`id`)`
- `) ENGINE=InnoDB AUTO_INCREMENT=144002 DEFAULT CHARSET=latin1`
现在，行在 B-Tree 主键由 user_id 排序分组，但按随机顺序插入。换句话说，我们减慢了插入速度，使得表中的 select 语句受益。要插入一行，InnoDB 可能需要一个磁盘读取来获取新行所在的页面和一个磁盘写入以将其保存回磁盘。我们使表变得更大，InnoDB 页数不够多，二级索引更大，因为主键更大。我们还添加了二级索引。现在我们 InnoDB 的缓冲池中数据更少了。我们会因为缓冲池中的数据较少而感到恐慌吗？不，因为现在当 InnoDB 从磁盘读取页面时，它不会只获得一个匹配的行，而是获得数百个匹配的行。IOPS 的数量不再与朋友数量与 select 语句的速率相关联。它现在只是 select 语句传入速率的一个因素。没有足够的内存来缓存所有表的影响大大减少了。只要存储可以执行比 select 语句的速率更多的 IOPS 次数。
使用修改后的表，pt-query-digest 输出的相关行：- `# Attribute    pct   total     min     max     avg     95%  stddev  median`
- `# ============ === ======= ======= ======= ======= ======= ======= =======`
- `# Rows examine 100   1.23k      16      34   23.72   30.19    4.19   22.53`
- `# pages distin 100     111       2       5    2.09    1.96    0.44    1.96`
使用新的主键，而不是读 30k 的 IOPS，MySQL 只需要执行大约读 588 次的 IOPS（~300 * 1.96）。这是一个更容易处理的工作量。插入的开销更大，但如果它们的速率为100次/秒，则在最坏的情况下它意味着读 100次 的 IOPS 和写入 100次的 IOPS。
当存在明确的访问模式时，上述策略很有效。最重要的是，这里有一些其他例子，其中通常有显着的访问模式：- 游戏排行榜（按用户）
- 用户偏好（按用户）
- 消息应用程序（来自或来自）
- 用户对象存储（按用户）
- 喜欢物品（按项目）
- 项目评论（按项目）
当您没有显性访问模式时，您可以做些什么？一种选择是使用覆盖指数。覆盖索引需要涵盖所有必需的列。列的顺序也很重要，因为第一个必须是分组值。另一种选择是使用分区在数据集中创建易于缓存的热点。
我们在本文中看到了用于解决读密集型工作负载的常用策略。此策略不能始终有效 &#8211; 您必须通过通用模式访问数据。但是当它工作时，你选择了好的 InnoDB 主键，你就成了此刻的英雄！
原文链接：https://www.percona.com/blog/2018/07/26/tuning-innodb-primary-keys/
**社区近期动态**
**No.1**
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
**No.2**
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