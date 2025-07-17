# 13 期 | 回滚到 savepoint

**原文链接**: https://opensource.actionsky.com/mysql-%e6%a0%b8%e5%bf%83%e6%a8%a1%e5%9d%97%e6%8f%ad%e7%a7%98-13-%e6%9c%9f-%e5%9b%9e%e6%bb%9a%e5%88%b0-savepoint/
**分类**: MySQL 新特性
**发布时间**: 2024-04-17T23:49:34-08:00

---

不想回滚整个事务，可以选择回滚一部分，跟着本文了解一下部分回滚是怎么做到的。
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 准备工作
创建测试表：
`CREATE TABLE `t1` (
`id` int unsigned NOT NULL AUTO_INCREMENT,
`i1` int DEFAULT '0',
PRIMARY KEY (`id`) USING BTREE,
KEY `idx_i1` (`i1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
`
插入测试数据：
`INSERT INTO `t1` (`id`, `i1`) VALUES
(10, 101), (20, 201),
(30, 301), (40, 401);
`
示例 SQL：
`/* 1 */ begin;
/* 2 */ insert into t1(id, i1)
values(50， 501);
/* 3 */ insert into t1(id, i1)
values(60， 601);
/* 4 */ rollback;
`
每条 SQL 前面的数字是它的编号，4 条 SQL 分别为 SQL 1、SQL 2、SQL 3、SQL 4，其中，SQL 4 是本文的主角。
SQL 2 插入记录  产生的 undo 日志编号为 0。
SQL 3 插入记录  产生的 undo 日志编号为 1。
## 2. binlog 回滚
示例 SQL 的两条 insert 语句执行过程中，会产生 binlog 日志，存放到 trx cache 中。
回滚整个事务时，事务执行过程中改变（插入、更新、删除）的数据都不要了，产生的 binlog 日志也就没有用了。
回滚整个事务，首先要进行的步骤就是 binlog 回滚。从这个步骤的名字来看，我们预期 MySQL 会在这一步把 trx cache 中的 binlog 日志都清除。
不过，我们要失望了，因为这一步什么都没干。
下面是 binlog 回滚的代码：
`static int binlog_rollback(handlerton *, THD *thd, bool all) {
DBUG_TRACE;
int error = 0;
if (thd->lex->sql_command == SQLCOM_ROLLBACK_TO_SAVEPOINT)
error = mysql_bin_log.rollback(thd, all);
return error;
}
`
从代码可以看到，只有 thd->lex->sql_command 为 SQLCOM_ROLLBACK_TO_SAVEPOINT 才会调用 `mysql_bin_log.rollback(thd, all)` 执行 binlog 回滚操作。
然而，执行 rollback 语句时，`thd->lex->sql_command` 为 SQLCOM_ROLLBACK，不满足 if 条件，上面的代码就什么都不会干了。
那么，trx cache 中的 binlog 日志什么时候会清除？
别急，后面会有专门的小节介绍。
## 3. InnoDB 回滚
binlog 回滚操作结束之后，接下来就是 InnoDB 回滚了。
InnoDB 回滚操作，会读取并解析事务产生的所有 undo 日志，并执行产生这些 undo 日志的操作的反向操作，也就是**回滚**。
回滚过程中，会根据 undo 日志产生的时间，从后往前读取并解析日志，再执行这条日志对应的回滚操作。
示例 SQL 中，执行了两条 insert 语句，会产生两条 undo 日志，编号分别为 0、1。以主键索引为例，回滚过程如下：
- 读取最新的 undo 日志（编号为 1）。
- 解析 undo 日志得到 `<id = 60>`。
- 删除 t1 表中 id = 60 的记录。
- 读取上一条 undo 日志（编号为 0）。
- 解析 undo 日志得到 `<id = 50>`。
- 删除 t1 表中 id = 50 的记录。
- 读取上一条 undo 日志，没有了，InnoDB 回滚操作结束。
## 4. 提交事务
InnoDB 回滚操作完成之后，接下来要怎么办？
这其实取决于回滚操作是怎么进行的。
我最初理解的回滚操作，是把事务执行过程中改变（插入、更新、删除）的记录恢复原样，就像事务什么都没干过一样。
然而，实际情况没有这么理想。
事务执行过程中改变过的那些记录，回滚之后：
- 从逻辑上来看，恢复了原样，确实就像事务什么都没干过一样。
- 从物理上来看，可能已经发生了变化，因为记录的位置有可能和修改之前不一样。
唠叨这么多，就是想说清楚一件事：事务的回滚操作，不是原地撤销对数据页的修改，而是通过再次修改数据页实现的。
既然修改了数据页，那就需要执行提交操作，才能让这些修改生效。
接下来，要执行的操作，就是把 InnoDB 回滚操作过程中对数据页的修改提交了，也就是提交事务。
不过，这里的提交事务和 commit 语句提交事务不一样。
执行 commit 语句时，因为有 binlog 和 InnoDB 两个存储引擎，需要使用二阶段提交。
事务执行过程中改变（插入、更新、删除）记录，会产生 binlog 日志。
回滚时，要把记录再修改回原来的样子。从逻辑上来看，记录就像是从来没有发生过变化，binlog 日志也就不需要了。
所以，InnoDB 回滚完成之后提交事务，不需要把 trx cache 中的 binlog 日志写入 binlog 日志文件并刷盘，只需要提交 InnoDB 事务就可以了。
关于提交 InnoDB 事务的具体逻辑，可以参照第 11 期《[InnoDB 提交事务，提交了什么？](https://mp.weixin.qq.com/s/4IHIUbPMwB81m3JIhYwkXg)》。
## 5. 清除 binlog 日志
trx cache 中的 binlog 日志有可能一部分存放在内存 buffer 中，另一部分存放在磁盘临时文件中。
清除操作需要同时清除 trx cache 内存 buffer 和磁盘临时文件中的 binlog 日志，分为两个步骤进行：
- 清空内存 buffer，让 trx cache 的 write_pos 指向内存 buffer 的开始处即可。
- 清空磁盘临时文件，首先会把文件的 seek offset 设置为 0，让文件本身的位置指针指向文件开头处，然后截断磁盘临时文件，释放文件占用的空间。
前面的 binlog 回滚步骤，没有清除事务执行过程中产生的 binlog 日志，而是留到 InnoDB 回滚步骤中提交事务完成之后才执行。这是因为：
- 清空磁盘临时文件中 binlog 日志的过程不可逆，如果中间出现问题，不能回退。
- InnoDB 回滚步骤中提交事务的容错性更好，回滚失败之后就不清除 binlog 日志了，也不损失什么。
## 6. 总结
回滚整个事务，主要分为三大步骤。
**第 1 步**，执行 binlog 回滚操作，其实什么也没干。
**第 2 步**，执行 InnoDB 回滚操作，会把事务执行过程中改变（插入、更新、删除）的记录恢复原样（至少从逻辑上来看是这样的）。
最后，还会提交 InnoDB 事务，让回滚操作对数据页的修改生效。
**第 3 步**，清除事务执行过程中产生的、临时存放于 trx cache 中的 binlog 日志。
> **本期问题**：关于本期内容，如有问题，欢迎留言交流。