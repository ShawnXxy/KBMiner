# 09 期 | 二阶段提交 (3) flush、sync、commit 子阶段

**原文链接**: https://opensource.actionsky.com/mysql-%e6%a0%b8%e5%bf%83%e6%a8%a1%e5%9d%97%e6%8f%ad%e7%a7%98-09-%e6%9c%9f-%e4%ba%8c%e9%98%b6%e6%ae%b5%e6%8f%90%e4%ba%a4-3-flush%e3%80%81sync%e3%80%81commit-%e5%ad%90%e9%98%b6%e6%ae%b5/
**分类**: MySQL 新特性
**发布时间**: 2024-03-13T00:58:57-08:00

---

commit 阶段的 3 个子阶段（flush、sync、commit）都干了什么？
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源
## 1. 写在前面
经过上一篇文章的介绍，我们已经对 commit 阶段有了整体的认识。
这篇文章，我们一起进入各子阶段，看看它们都会干点什么，以及会怎么干。
为了方便理解，我们假设有 30 个事务，它们对应的用户线程编号也从 1 到 30。
## 2. flush 子阶段
用户线程 16 加入 flush 队列，成为 **flush 队长**，并且通过申请获得 LOCK_log 互斥量。
flush 队长收编用户线程 17 ~ 30 作为它的队员，队员们进入 flush 队列之后，就开始等待，收到 commit 子阶段的队长发来的通知才会结束等待。
flush 队长开始干活之前，会带领它的队员从 flush 队列挪出来，给后面进入二阶段提交的其它事务腾出空间。
从 flush 队列挪出来之后，flush 队长会触发操作系统，把截止目前产生的所有 redo 日志都刷盘。
这些 redo 日志，当然就包含了它和队员们在 prepare 阶段及之前产生的所有 redo 日志了。
触发 redo 日志刷盘之后，flush 队长会从它自己开始，把它和队员们产生的 binlog 日志写入 binlog 日志文件。
以队长为例，写入过程是这样的：
- 从事务对应的 trx_cache 中把 binlog 日志读出来，存放到 trx_cache 的内存 buffer 中。
每次读取 4096（对应代码里的 `IO_SIZE`）字节的 binlog 日志，最后一次读取剩余的 binlog 日志（**小于或等于** 4096 字节）。
- 把 trx_cache 内存 buffer 中的 binlog 日志写入 binlog 日志文件。
队员们产生的 binlog 日志写入 binlog 日志文件的过程，和队长一样。队长把自己和所有队员产生的 binlog 日志都写入 binlog 日志文件之后，flush 子阶段的活就干完了。
flush 队长写完 binlog 日志之后，如果发现 binlog 日志文件的大小**大于等于**系统变量 `max_binlog_size` 的值（默认为 1G），会设置一个标志（`rotate = true`），表示需要切换 binlog 日志文件。后面 commit 子阶段会用到。
到这里，用户线程 16 作为队长的 flush 子阶段，就结束了。
## 3. sync 子阶段
为了剧情需要，我们假设用户线程 6 ~ 15 此刻还在 sync 队列中，用户线程 6 最先进入队列，是 **sync 队长**，用户线程 7 ~ 15 都是队员。
用户线程 16（`flush 队长`）带领队员们来到 sync 子阶段，发现 sync 队列中已经有先行者了。
有点遗憾，用户线程 16 不能成为 sync 子阶段的队长，它和队员们都会变成 sync 子阶段的队员。
此时，用户线程 6 是 sync 队长，用户线程 7 ~ 30 是队员。
进入 sync 子阶段之后，用户线程 16（`flush 队长`）会释放它在 flush 子阶段获得的 LOCK_log 互斥量，flush 子阶段下一屇的队长就可以获得 LOCK_log 互斥量开始干活了。
交待完用户线程 16（`flush 队长`）在 sync 子阶段要干的活，该说说 sync 队长了。
sync 队长会申请 LOCK_sync 互斥量，获得互斥量之后，就开始准备给自己和队员们干 sync 子阶段的活了。
队员们依然在一旁当吃瓜群众，等待 sync 队长给它们干活。它们会一直等待，收到 commit 子阶段的队长发来的通知才会结束等待。
就在 sync 队长准备甩开膀子大干一场时，它发现前面还有一个关卡：**本次组提交能不能触发操作系统把 binlog 日志刷盘**。
sync 队长怎么知道自己能不能过这一关？
它会查看一个计数器的值（sync_counter），如果 `sync_counter + 1` **大于等于**系统变量 `sync_binlog` 的值，就说明自己可以过关。
否则，不能通过这一关，用户线程 6 作为队长的 sync 子阶段就到此结束了，它什么都不用干。
如果 sync 队长过关了，它会想：好不容易过关，我要再收编一些队员，才不枉费我的好运气。
sync 队长会带领队员们继续在 sync 队列中等待，以收编更多队员。这个等待过程是有期限的，满足以下两个条件之一，就结束等待：
- 已经等待了系统变量 `binlog_group_commit_sync_delay` 指定的时间（单位：微妙），默认值为 0。
- sync 队列中的用户线程数量（sync 队长和所有队员加在一起）达到了系统变量 `binlog_group_commit_sync_no_delay_count` 的值，默认值为 0。
等待结束之后，sync 队长会带领队员们从 sync 队列挪出来，给后面进入二阶段提交的其它事务腾出空间。
接下来，sync 队长终于可以大干一场了，它会触发操作系统把 binlog 日志刷盘，确保它和队员们产生的 binlog 日志写入到磁盘上的 binlog 日志文件中。
这样即使服务器突然异常关机，binlog 日志也不会丢失了。
刷盘完成之后，用户线程 6 作为队长的 sync 子阶段，就到此结束。
介绍完 sync 子阶段的主要流程，我们再来说说 `sync_counter`。
sync_counter 的值从 0 开始，某一次组提交的 sync 队长没有过关，不会触发操作系统把 binlog 日志刷盘，sync_counter 就加 1。
sync_counter 会一直累加，直到后续的某一次组提交，`sync_counter + 1` 大于等于系统变量 `sync_binlog` 的值，sync 队长会把 sync_counter 重置为 0，并且触发操作系统把 binlog 日志刷盘。
sync_counter 重置为 0 之后，sync 子阶段是否要触发操作系统把 binlog 日志刷盘，又会开始一个新的轮回。
## 4. commit 子阶段
同样，为了剧情需要，我们假设用户线程 1 ~ 5 此刻还在 commit 队列中，用户线程 1 最先进入队列，是 **commit 队长**，用户线程 2 ~ 5 都是队员。
用户线程 6（`sync 队长`）带领队员们来到 commit 子阶段，发现 commit 队列中也已经有先行者了。
用户线程 6 和队员们一起，都变成了 commit 子阶段的队员。
此刻，用户线程 1 是 commit 队长，用户线程 2 ~ 30 是队员。
进入 commit 子阶段之后，用户线程 6（`sync 队长`）会释放它在 sync 子阶段获得的 LOCK_sync 互斥量，sync 子阶段下一屇的队长就可以获得 LOCK_sync 互斥量开始干活了。
交待完用户线程 6（`sync 队长`）进入 commit 子阶段要干的活，该说说 commit 队长了。
commit 队长会申请 LOCK_commit 互斥量，获得互斥量之后，根据系统变量 `binlog_order_commits` 的值决定接下来的活要怎么干。
如果 binlog_order_commits = `true`，commit 队长会把它和队员们的 InnoDB 事务逐个提交，然后释放 LOCK_commit 互斥量。
提交 InnoDB 事务完成之后，commit 队长会通知它的队员们（用户线程 2 ~ 30）：所有活都干完了，你们都散了吧，别围观了，该干啥干啥去。
队员们收到通知之后，作鸟兽散，它们的二阶段提交也都结束了。
如果 binlog_order_commits = `false`，commit 队长不会帮助队员们提交 InnoDB 事务，它提交自己的 InnoDB 事务之后，就会释放 LOCK_commit 互斥量。
然后，通知所有队员（用户线程 2 ~ 30）：flush 子阶段、sync 子阶段的活都干完了，你们自己去提交 InnoDB 事务。
队员们收到通知之后，就各自提交自己的 InnoDB 事务，谁提交完成，谁的二阶段提交就结束了。
最后，commit 队长还要处理最后一件事。
如果用户线程 16（`flush 队长`）把 rotate 设置为 `true` 了，说明 binlog 日志文件已经达到了系统变量 `max_binlog_size` 指定的上限，需要切换 binlog 日志文件。
> 切换指的是关闭 flush 子阶段刚写入的 binlog 日志文件，创建新的 binlog 日志文件，以供后续事务提交时写入。
如果需要切换 binlog 日志文件，切换之后，还会根据系统变量 `binlog_expire_logs_auto_purge`、`binlog_expire_logs_seconds`、`expire_logs_days` 清理过期的 binlog 日志。
处理完切换 binlog 日志文件的逻辑之后，commit 队长的工作就此结束，它的二阶段提交就完成了。
## 5. 总结
flush 子阶段，flush 队长会把自己和队员在 prepare 阶段及之前产生的 redo 日志都刷盘，把事务执行过程中产生的 binlog 日志写入 binlog 日志文件。
sync 子阶段，如果 `sync_counter + 1` 大于等于系统变量 `max_binlog_size` 的值，sync 队长会把 binlog 日志刷盘。
commit 子阶段，如果系统变量 `binlog_order_commits` 的值为 true，commit 队长会把自己和队员们的 InnoDB 事务都提交，否则，commit 队长和队员各自提交自己的 InnoDB 事务。
> **本期问题**：commit 子阶段这种清理过期 binlog 日志的逻辑，会有什么问题吗？欢迎留言交流。
**下期预告**：MySQL 核心模块揭秘 | 10 期 | binlog 怎么写入日志文件？