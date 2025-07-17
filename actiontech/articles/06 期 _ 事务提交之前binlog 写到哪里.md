# 06 期 | 事务提交之前，binlog 写到哪里？

**原文链接**: https://opensource.actionsky.com/06-%e6%9c%9f-%e4%ba%8b%e5%8a%a1%e6%8f%90%e4%ba%a4%e4%b9%8b%e5%89%8d%ef%bc%8cbinlog-%e5%86%99%e5%88%b0%e5%93%aa%e9%87%8c%ef%bc%9f/
**分类**: 技术干货
**发布时间**: 2024-02-21T01:36:40-08:00

---

事务提交时，才会把产生的 binlog 一次性写入 binlog 日志文件。事务执行过程中，会一直产生 binlog，这些 binlog 会暂存到哪里？
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 准备工作
参数配置：
`binlog_format = ROW
binlog_rows_query_log_events = OFF
`
创建测试表：
`CREATE TABLE `t_binlog` (
`id` int unsigned NOT NULL AUTO_INCREMENT,
`i1` int DEFAULT '0',
`str1` varchar(32) DEFAULT '',
PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
`
示例 SQL：
`BEGIN;
INSERT INTO `t_binlog` (`i1`, `str1`)
VALUES (100, 'MySQL 核心模块揭秘');
COMMIT;
`
## 2. 解析 binlog
执行示例 SQL 之后，我们可以用下面的命令解析事务产生的 binlog 日志：
`cd <binlog 日志文件目录>
mysqlbinlog binlog.000395 \
--base64-output=decode-rows -vv
`
解析 binlog 日志之后，我们可以得到 4 个 binlog event。
按照这些 binlog event 在 binlog 日志文件中的顺序，简化之后的内容如下：
- Query_log_event
`# at 1233
# Query    thread_id=8
BEGIN
`
- Table_map_log_event
```
# at 1308
Table_map: `test`.`t_binlog` mapped to number 95
```
- Write_rows_log_event
```
# at 1369
Write_rows: table id 95 flags: STMT_END_F
INSERT INTO `test`.`t_binlog`
SET
@1=1 /* INT meta=0 nullable=0 is_null=0 */
@2=100 /* INT meta=0 nullable=1 is_null=0 */
@3='MySQL 核心模块揭秘' /* VARSTRING(96) meta=96 nullable=1 is_null=0 */
```
- Xid_log_event
```
# at 1438
Xid = 32
COMMIT/*!*/;
```
示例 SQL 中，只有两条 SQL 会产生 binlog event：
- BEGIN：不会产生 binlog event。
- INSERT：产生三个 binlog event。
Query_log_event。
- Table_map_log_event。
- Write_rows_log_event。
- COMMIT：产生 Xid_log_event。
## 3. binlog cache
我们使用 mysqlbinlog 分析 binlog 日志的时候，可以发现这么一个现象：同一个事务产生的 binlog event，在 binlog 日志文件中是连续的。
保证同一个事务的 binlog event 在 binlog 日志文件中的连续性，不管是 MySQL 从库回放 binlog，还是作为用户的我们，都可以很方便的定位到一个事务的 binlog 从哪里开始，到哪里结束。
一个事务会产生多个 binlog event，很多个事务同时执行，怎么保证同一个事务产生的 binlog event 写入到 binlog 日志文件中是连续的？
这就是 cache 发挥用武之地的时候了，每个事务都有两个 binlog cache：
- stmt_cache：改变（插入、更新、删除）**不支持事务**的表，产生的 binlog event，临时存放在这里。
- trx_cache：改变（插入、更新、删除）**支持事务**的表，产生的 binlog event，临时存放在这里。
因为我们只介绍 InnoDB 存储引擎，后面会忽略 stmt_cache，直接介绍 trx_cache。
事务执行过程中，产生的所有 binlog event，都会先写入 trx_cache。trx_cache 分为两级：
- 第一级：**内存**，也称为 **buffer**，它的大小用 **buffer_length** 表示，由系统变量 `binlog_cache_size` 控制，默认为 32K。
- 第二级：**临时文件**，位于操作系统的 tmp 目录下，文件名以 **ML** 开头。
buffer_length 加上临时文件中已经写入的 binlog 占用的字节数，也有一个上限，由系统变量 `max_binlog_cache_size` 控制。
## 4. 产生 binlog
如果一条 SQL 语句改变了（插入、更新、删除）表中的数据，server 层会为这条 SQL 语句产生一个包含表名和表 ID 的 `Table_map_log_event`。
每次调用存储引擎的方法写入一条记录到表中之后，server 层都会为这条记录产生 binlog。
这里没有写成 binlog event，是因为记录中各字段内容都很少的时候，多条记录可以共享同一个 binlog event ，并不需要为每条记录都产生一个新的 binlog event。
多条记录产生的 binlog 共享同一个 binlog event 时，这个 binlog event 最多可以存放多少字节的内容，由系统变量 `binlog_row_event_max_size` 控制，默认为 8192 字节。
如果一条记录产生的 binlog 超过了 8192 字节，它的 binlog 会独享一个 binlog event，这个 binlog event 的大小就不受系统变量 `binlog_row_event_max_size` 控制了。
在 binlog 日志文件中，Table_map_log_event 位于 SQL 语句改变表中数据产生的 binlog event 之前。
示例 SQL 对应的事务中，INSERT 是改变表中数据的第一条 SQL 语句，它插入第一条（也是唯一一条）记录到 t_binlog 表之后，server 层会为这条记录产生 binlog event。
插入记录对应的 binlog event 是 `Write_rows_log_event`。
产生 Write_rows_log_event 之前，server 层会先为 INSERT 构造一个 `Table_map_log_event`。
构造 Table_map_log_event 之前，server 层发现一个问题：示例 SQL 对应的事务，还没有初始化 binlog cache。
那么，第一步就要为这个事务初始化 binlog cache，包括 stmt_cache 和 trx_cache。初始化完成之后，这两个 cache 都是空的。
在 binlog 日志文件中，一个事务以内容为 BEGIN 的 `Query_log_event` 开始。
刚刚初始化完成的 trx_cache 是空的，写入其它 binlog event 之前，要先写入一个内容为 BEGIN 的 Query_log_event。
写入 Query_log_event 之后，就可以写入内容为表名和表 ID 的 `Table_map_log_event` 了。
写入 Table_map_log_event 之后，接下来写入的 binlog event 就是包含插入记录所有字段的 `Write_rows_log_event` 了。
最后，执行 COMMIT 语句时，会产生内容为 `COMMIT` 的 `Xid_log_event`，并写入 trx_cache。
## 5. 怎么写入 trx_cache？
事务执行过程中，所有 binlog event 都会先写入 trx_cache 的 **buffer**，buffer 大小默认为 32K。
如果 buffer 剩余空间不够写入一个 binlog event，buffer 和临时文件怎么协同合作，来完成这个 binlog event 的写入操作？
接下来，我们就来聊聊，写入一个 binlog event 到 trx_cache 的流程：
- 判断 buffer 剩余空间是否足够写入这个 binlog event。
- 如果**足够**，直接把 binlog event 写入 buffer，流程结束。
- 如果**不够**，用 binlog event 前面的部分内容填满 buffer，然后，把 buffer 中所有内容写入临时文件，再清空 buffer，以备复用。
- 接着判断 binlog event 剩余内容是否大于等于 **4096 字节**（IO_SIZE）。
- 如果剩余内容**大于等于** 4096 字节，则把剩余内容前面的 **N * 4096** 字节写入临时文件。
对于剩余内容字节数不能被 4096 整除的情况，最后还会剩下不足 4096 字节的内容，这部分内容会写入 buffer。
- 如果剩余内容**小于** 4096 字节，直接把 binlog event 中剩余的所有内容都写入 buffer。
## 6. 总结
trx_cache 分为两级：内存（buffer）、临时文件。
事务执行过程中，产生的所有 binlog event 都要写入 trx_cache。
binlog event 写入 trx_cache，通常情况下，都会先写入 buffer，写满 buffer 之后，再把 buffer 中所有内容都写入临时文件，最后清空 buffer。
> **本期问题**：如果 buffer 是空的，接下来要写入一个 86K 的 binlog event 到 trx_cache，写入流程是什么样的？欢迎大家留言交流。
**下期预告**：MySQL 核心模块揭秘 | 07 期 | 二阶段提交 (1) prepare 阶段。