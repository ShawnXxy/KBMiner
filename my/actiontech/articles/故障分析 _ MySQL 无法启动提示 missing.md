# 故障分析 | MySQL 无法启动，提示 missing……

**原文链接**: https://opensource.actionsky.com/20201015-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-10-15T00:33:35-08:00

---

作者：姚远
专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6，5.7，8.0 OCP。现在鼎甲科技任顾问，为同事和客户提高数据库培训和技术支持服务。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**故障描述**
MySQL 数据库服务器的 CPU 和主板都换了，重新开机，发现 MySQL 无法启动！！！> **提示：**Ignoring the redo log due to missing MLOG_CHECKPOINT between the checkpoint  &#8230;. and &#8230;
**故障分析**
这个问题出现在 MySQL 5.7 之后的版本，主要的原因是 MySQL 会在最新的 checkpoint 完成后都会在 redo log 写一个一字节的 MLOG_CHECKPOINT  标记，用来标记在此之前的 redo 都已 checkpoint 完成。如果处于任何原因没有找到这个标记，那么整个 redo log 文件都会被忽略。出现这个错误的话，最好是有备份进行恢复，如果没有做好备份，那只能采取非常规的启动方式，**但可能造成数据丢失**。
**故障处理**
移除当前使用的 redo log 文件，然后可以试着启动数据库，结果启动失败！> **提示：**[ERROR] InnoDB: Page [page id: space=0, page number=0] log sequence number 178377412422 is in the future! Current system log sequence number 165909011496.
这样的错误，这是因为 MySQL writer 线程按照配置的时间间隔以 page 为单位刷新 buffer 数据到磁盘。当数据刷新到磁盘的时候，新写入磁盘的 page 包含了较新的 LSN，此时系统 system 表空间头的 LSN 并没有同步更新，通常这是检查点线程的工作。在正常的崩溃恢复中，MySQL 可以借助 redo log 来进行前滚和回滚，但是此时 redo log 已经被我们删掉了，MySQL 无法进行恢复操作。此时，我们设置 **innodb_force_recovery=3** 来强制启动 MySQL，仍然启动不成功，改成 4 后启动了！再使用 mysqldump 导出备份，结果噩梦又降临了！MySQL 又 crash 了。> 提示：InnDB: Failed to find tablespace for table&#8230;&#8230;
设置参数 **innodb_force_recovery=5**，数据库仍然启动失败，再设置成 6，启动成功！用 sqldump 顺利把数据备份出来了！再初始化数据库，把刚刚备份的数据库导入，数据库恢复成功完成！
**参数说明**
这里的关键是设置 innodb_force_recovery 参数，对应这个参数的说明如下：1. SRV_FORCE_IGNORE_CORRUPT：忽略检查到的 corrupt 页；2. SRV_FORCE_NO_BACKGROUND：阻止主线程的运行，如主线程需要执行 full purge 操作，会导致 crash；3. SRV_FORCE_NO_TRX_UNDO：不执行事务回滚操作；4. SRV_FORCE_NO_IBUF_MERGE：不执行插入缓冲的合并操作；5. SRV_FORCE_NO_UNDO_LOG_SCAN：不查看重做日志，InnoDB 存储引擎会将未提交的事务视为已提交；6. SRV_FORCE_NO_LOG_REDO：不执行前滚的操作。
相关推荐：
[技术分享 | 企业版监控工具 MEM 初探](https://opensource.actionsky.com/20200723-mem/)
[技术分享 | 只有.frm和.ibd文件时如何批量恢复InnoDB的表](https://opensource.actionsky.com/20200718-mysql/)
[技术分享 | MySQL 使用 MariaDB 审计插件](https://opensource.actionsky.com/20200908-mysql/)