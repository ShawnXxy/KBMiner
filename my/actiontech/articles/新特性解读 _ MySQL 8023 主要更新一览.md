# 新特性解读 | MySQL 8.0.23 主要更新一览

**原文链接**: https://opensource.actionsky.com/20210119-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-01-19T00:36:35-08:00

---

作者：管长龙爱可生交付服务部 DBA，主要负责 MySQL 及 Redis 的日常问题处理，参与公司数据库培训的教研授课及开源社区的运营工作。
本文来源：原创投稿* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
> 欢迎关注爱可生开源社区《MySQL 8.0 新特性》专栏，技术专家不定期发布新功能文章。
MySQL 8.0.23 已于昨日发布，目前发布频率稳定保持 3 个月一次。本次发布是维护版本，除了修复一些 Bug，此版本还增添了一些新功能。
## 一、不可见列
列可以定义为不可见，例如：
`# 创建表时，可使其不可见（ALTER TABLE 也支持）
mysql> CREATE TABLE t1 (col1 INT, col2 INT INVISIBLE);
mysql> INSERT INTO t1 (col1, col2) VALUES(1, 2), (3, 4);
# SQL 语句通过显式引用它来使用不可见列
mysql> SELECT * FROM t1;
+------+
| col1 |
+------+
|    1 |
|    3 |
+------+
# 如果未引用不可见的列，则该列将不会出现在结果中
mysql> SELECT col1, col2 FROM t1;
+------+------+
| col1 | col2 |
+------+------+
|    1 |    2 |
|    3 |    4 |
+------+------+
`https://dev.mysql.com/doc/refman/8.0/en/invisible-columns.html
## 二、查询属性
允许应用程序为其查询设置每个查询元数据。
`mysql> query_attributes n1 v1 n2 v2;
mysql> SELECT
mysql_query_attribute_string('n1') AS 'attr 1',
mysql_query_attribute_string('n2') AS 'attr 2',
mysql_query_attribute_string('n3') AS 'attr 3';
+--------+--------+--------+
| attr 1 | attr 2 | attr 3 |
+--------+--------+--------+
| v1     | v2     | NULL   |
+--------+--------+--------+
`https://dev.mysql.com/doc/refman/8.0/en/query-attribute-udfs.html#udf_mysql-query-attribute-string
## 三、安全
### Doublewrite 文件页加密
InnoDB 自动加密属于加密表空间的 Doublewrite 文件页面，无需采取任何措施。使用相关表空间的加密密钥对 Doublewrite 文件页进行加密。同一表空间中被写入数据的加密页面也会被写入 Doublewrite 文件。属于未加密表空间的 Doublewrite 文件页面保持未加密状态。在恢复过程中，加密的 Doublewrite 文件页面是未加密状态并检查是否损坏。
https://dev.mysql.com/doc/refman/8.0/en/innodb-data-encryption.html
### 提高账户确定性
为了让 TCP 连接匹配账户更具确定性，在匹配主机名指定的账户前，匹配账户的主机名部分将以以下顺序检查使用主机 IP 地址指定账户。
`# 指定 IP 地址的帐户
mysql> CREATE USER 'user_name'@'127.0.0.1';
mysql> CREATE USER 'user_name'@'198.51.100.44';
# 使用 CIDR 表示法指定为 IP 地址的帐户
mysql> CREATE USER 'user_name'@'192.0.2.21/8';
mysql> CREATE USER 'user_name'@'198.51.100.44/16';
# 使用带子网掩码格式的指定为 IP 地址的账户
mysql> CREATE USER 'user_name'@'192.0.2.0/255.255.255.0';
mysql> CREATE USER 'user_name'@'198.51.0.0/255.255.0.0';
`https://dev.mysql.com/doc/refman/8.0/en/connection-access.html
### 更精准的 FLUSH 权限
授予 RELOAD 权限的用户可以执行各种操作。在某些情况下，为了使 DBA 避免授予 RELOAD 并使用户权限更接近允许的操作，已对 FLUSH 操作的更精细的特权控制，以使客户可以执行 FLUSH OPTIMIZER_COSTS，FLUSH STATUS，FLUSH USER_RESOURCES 和 FLUSH TABLES 语句，无需 RELOAD 权限。
https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_reload
## 四、InnoDB
### 优化 TRUNCATE / DROP
当用户对 InnoDB 表空间 TRUNCATE 或 DROP 操作：
- 对有庞大缓冲池(>32GB)实例上的大表删除
- 对具有自适应哈希索引引用大量页面的表空间
- TRUNCATE 临时表空间
以上情况，MySQL 现在将其标记为已删除，然后从缓冲池懒惰地释放属于已删除表空间的所有页面，或者像释放页面一样重用它们。
### 新增表空间 AUTOEXTEND_SIZE 属性
InnoDB 常规表 CREATE / ALTER TABLESPACE 子句和独立表空间的 CREATE / ALTER TABLE 子句新增自动扩展属性。原表空间的增长大小已在 InnoDB 内部硬编码为 1MB [默认]（page_size * 一个范围内的页面数）。设置后，表空间的增长大小可以由用户决定。
`# 创建或修改表时指定扩展空间大小
mysql> CREATE TABLE t1 (c1 INT) AUTOEXTEND_SIZE = 4M;
mysql> ALTER TABLE t1 AUTOEXTEND_SIZE = 4M;
# 查询该属性值
mysql> SELECT NAME, AUTOEXTEND_SIZE FROM INFORMATION_SCHEMA.INNODB_TABLESPACES 
WHERE NAME LIKE 'test/t1';
+---------+-----------------+
| NAME    | AUTOEXTEND_SIZE |
+---------+-----------------+
| test/t1 |         4194304 |
+---------+-----------------+
`https://dev.mysql.com/doc/refman/8.0/en/innodb-tablespace-autoextend-size.html
## 新增 temptable_max_mmap 变量
新变量定义了 TempTable 存储引擎在开始将内部临时表数据存储到 InnoDB 磁盘内部临时表之前，被允许从内存映射文件分配的最大内存量。temptable_max_mmap = 0 设置将禁用从内存映射文件的分配。
https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_temptable_max_mmap
## 五、复制
### 术语替换
不推荐使用 CHANGE MASTER TO 语句，改用别名 CHANGE REPLICATION SOURCE TO。该语句的参数还具有别名，该别名用术语 SOURCE 代替术语 MASTER。例如，现在可以将 MASTER_HOST 和 MASTER_PORT 输入为 SOURCE_HOST 和 SOURCE_PORT。START REPLICA | SLAVE 语句的参数 MASTER_LOG_POS 和 MASTER_LOG_FILE 现在具有别名 SOURCE_LOG_POS 和 SOURCE_LOG_FILE。语句的工作方式与以前相同，只是每个语句使用的术语已更改。如果使用旧版本，则会发出弃用警告。
### 直接从禁用 GTID 的主机复制到启用 GTID 的从机
CHANGE REPLICATION SOURCE TO 语句新增选项：ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS = [OFF，LOCAL，<UUID>]
允许数据在非 GTID 实例和 GTID 实例之间传输。
https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-assign-anon.html
### 在 MTS 死锁检测基础结构中包含 MDL 和 ACL 锁
将提供多线程的 REPLICA 所需的线程序列化基础结构与 MDL 和 ACL 访问序列化基础结构集成在一起，该多线程 REPLICA 与 SOURCE 保持相同的提交顺序。其动机是能够在 REPLICA 主动处理变更流时在 REPLICA 上执行任何客户端语句。此类语句可能会创建死锁，必须对其进行检测，并最终将其破坏以继续执行。
## 组复制
异步复制通道的自动连接故障转移，将确保接收方的发送方列表与组复制成员身份更改同步。
## 六、X 协议
经典的 MySQL 协议，如果 SQL 查询使用元数据锁定或睡眠功能，则将定期检查与服务器的连接以验证其是否仍然有效。如果不是，则可以停止查询，以便它不会继续消耗资源。以前，X 协议不执行这些检查，并假定连接仍然有效。现在已为 X 协议添加了检查。
从 MySQL 8.0.23 开始，服务器将通知所有客户端有关它是刚刚关闭连接还是自行关闭的信息。客户端可以使用此信息来决定重新连接是否有意义，然后重试。
## 七、其他
优化哈希联接的哈希表的实现。目的是提高性能，使用更少的内存并改善内存控制。
用标准 C++11 替换了部分旧的 InnoDB 代码。加强代码中使用原子性的规则和语义，从而使代码更符合标准。
## 八、弃用和移除
弃用 relay_log_info_repository 和 master_info_repository 。当用户设置或读取 relay_log_info_repository 或 master_info_repository 变量的值时，将出现弃用警告。未来，用于存储复制配置和元数据的唯一选项将在事务系统表中。
不赞成使用 FLUSH HOSTS 语句，而建议使用 TRUNCATE performance_schema.host_cache，并将在以后的 MySQL 版本中删除。
## 文章参考
> MySQL 8.0.23 Release Notes:
https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-23.html
The MySQL 8.0.23 Maintenance Release is Generally Available
https://mysqlserverteam.com/the-mysql-8-0-23-maintenance-release-is-generally-available/
**文章推荐：**
[新特性解读 | 高效获取不连续主键区间](https://opensource.actionsky.com/20210112-mysql/)
[新特性解读 | MySQL 8.0.22 任意格式数据导入](https://opensource.actionsky.com/20201110-mysql/)
[新特性解读 | MySQL 8.0.22 新特性 Async Replication Auto failover](https://opensource.actionsky.com/20201102-mysql/)