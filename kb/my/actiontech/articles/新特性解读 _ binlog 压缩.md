# 新特性解读 | binlog 压缩

**原文链接**: https://opensource.actionsky.com/20200520-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-05-19T21:15:41-08:00

---

作者：王福祥
爱可生 DBA 团队成员，负责客户的数据库故障处理以及调优。擅长故障排查及性能优化。对数据库相关技术有浓厚的兴趣，喜欢分析各种逻辑。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
二进制日志（binlog）是 MySQL 日志结构中重要的部分；记录了数据的更改操作，用于数据恢复、数据复制以及审计。然而在众多实际场景中经常发生高并发引起 binlog 暴涨的问题将挂载点空间占满以及主从网络带宽成为瓶颈时主从延时过大。8.0.20 版本推出 binlog 压缩功能，有效缓解甚至解决此类问题。
**一、特性描述**
MySQL 从 8.0.20 开始集成 ZSTD 算法，开启压缩功能后；以事务为单位进行压缩写入二进制日志文件，降低原文件占用的磁盘空间。压缩后的事务以压缩状态有效负载在复制流中发送到从库（MGR 架构中为组 member）或客户端（例如 mysqlbinlog）。
官网连接：[https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-20.html](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-20.html)
**二、原理分析**
1. 开启压缩功能后，通过 ZSTD 算法对每个事务进行压缩，写入二进制日志。
2. 新版本更改了 libbinlogevents，新增 Transaction_payload_event 作为压缩后的事务表示形式。
- `class Transaction_payload_event : public Binary_log_event {`
- ` protected:`
- `  const char *m_payload;`
- `  uint64_t m_payload_size;`
- `  transaction::compression::type m_compression_type;`
- `  uint64_t m_uncompressed_size;`
3. 新增 Transaction_payload_event 编码器/解码器，用于实现对压缩事务的编码和解码。
- `namespace binary_log {`
- `namespace transaction {`
- `namespace compression {`
- 
- `enum type {`
- `  /* No compression. */`
- `  NONE = 0,`
- 
- `  /* ZSTD compression. */`
- `  ZSTD = 1,`
- `};`
4. 在 mysqlbinlog 中设计和实现每个事务的解压缩和解码，读取出来的日志与未经压缩的原日志相同，并打印输出所用的压缩算法，事务形式，压缩大小和未压缩大小，作为注释。
- `#200505 16:24:24 server id 1166555110  end_log_pos 2123 CRC32 0x6add0216    Transaction_Payload     payload_size=863    compression_type=ZSTD   uncompressed_size=2184`
- `# Start of compressed events!`
5. 从库（或 MGR-member）在接收已压缩的 binlog 时识别 Transaction_payload_event，不进行二次压缩或解码。以原本的压缩状态写入中继日志；保持压缩状态。回放日志的解码和解压缩过程由 SQL 线程负责。
总结日志压缩过程为：
1）单位事务需要提交并记录 binlog。
2）压缩编码器在缓存中通过 ZSTD 算法压缩以及编码该事务。
3）将缓存中压缩好的事务写入日志中，落盘。
日志读取过程为：
客户端工具（mysqlbinlog、sql 线程）对压缩日志进行解压缩、解码。解压出原本未压缩的日志进行读取或回放。
**三、注意事项**
1. 压缩功能以事务为单位进行压缩，不支持非事务引擎。
2. 仅支持对 ROW 模式的 binlog 进行压缩。
3. 目前仅支持 ZSTD 压缩算法，但是，底层设计是开放式的，因此后续官方可能会根据需要添加其他压缩算法（例如 zlib 或 lz4）。
4. 压缩动作是并行进行的，并且发生在 binlog 落盘之前的缓存步骤中。
5. 压缩过程占用本机 CPU 及内存资源。在主从延迟的场景中，如果性能瓶颈时，网络带宽、压缩功能可以有效缓解主从延迟；但是如果性能瓶颈是本机自身处理能力，那么压缩功能反而可能加大主从延迟。
**四、特性测试**
MySQL 版本：8.0.20
架构：一主一从半同步
测试方案：
1. 搭建好 MySQL 8.0.20 的主从架构
2. 主从上开启压缩功能、并设置压缩等级，默认为 3，随着压缩级别的增加，数据压缩率也会增加，但同时 CPU 及内存的资源消耗也将增加。
- `mysql> set  binlog_transaction_compression=on;`
- `mysql> set  binlog_transaction_compression_level_zstd=10;`
3. 查看压缩前后相同 SQL 产生的 binlog 大小。
压缩前 binlog 大小约为 300M
- `-rw-r----- 1 mysql mysql 251M May  6 09:31 mysql-bin.000001`
- `-rw-r----- 1 mysql mysql  50M May  6 09:31 mysql-bin.000002`
压缩后 binlog 大小约 150M- `-rw-r----- 1 mysql mysql 148M May  6 09:32 mysql-bin.000004`
4. 查看压缩前后相同 SQL 在低主从带宽的网络环境中 tps 的比较。限制网络速率- `tc qdisc add dev eth0 root handle 1:0 netem delay 100ms`
- `tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate 256kbit buffer 1600 limit 3000`
压缩前压测结果：- `SQL statistics:`
- `    queries performed:`
- `        read:                            3976`
- `        write:                           1136`
- `        other:                           568`
- `        total:                           5680`
- `    transactions:                        284    (9.17 per sec.)`
- `    queries:                             5680   (183.32 per sec.)`
压缩后压测结果：- `SQL statistics:`
- `    queries performed:`
- `        read:                            4746`
- `        write:                           1356`
- `        other:                           678`
- `        total:                           6780`
- `    transactions:                        339    (10.15 per sec.)`
- `    queries:                             6780   (202.92 per sec.)`
**结论**
1. MySQL 新推出的 binlog 压缩功能，当压缩级别设置为 10 时，压缩率约为 50% 左右，能够较大程度减少 binlog 所占用的空间。
2. 压缩功能能够一定程度提升因网络带宽所带来的主从延迟，集群tps不降低，略微提升。