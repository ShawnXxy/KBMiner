# MySQL · 引擎特性 · 初探 Clone Plugin

**Date:** 2019/09
**Source:** http://mysql.taobao.org/monthly/2019/09/02/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2019 / 09
 ](/monthly/2019/09)

 * 当期文章

 MySQL · 引擎特性 · 临时表改进
* MySQL · 引擎特性 · 初探 Clone Plugin
* MySQL · 引擎特性 · 网络模块优化
* MySQL · 引擎特性 · Multi-Valued Indexes 简述
* AliSQL · 引擎特性 · Statement Queue
* Database · 理论基础 · Palm Tree
* AliSQL · 引擎特性 · Returning
* PgSQL · 最佳实践 · 回归测试探寻
* MongoDB · 最佳实践 · 哈希分片为什么分布不均匀
* PgSQL · 应用案例 · PG有standby的情况下为什么停库可能变慢？

 ## MySQL · 引擎特性 · 初探 Clone Plugin 
 Author: weixiang 

 MySQL8.0.17推出了一个重量级的功能：clone plugin。允许用户可以将当前实例进行本地或者远程的clone。这在某些场景尤其想快速搭建复制备份或者在group replication里加入新成员时非常有用。本文主要试玩下该功能，并试图阐述下其实现的机制是什么。

我们以本地clone为例，因为去除网络部分，理解起来会相对简单点。 也不会过度接触代码部分，仅仅做简单的原理性阐述

## 示例

### 本地 clone
本地clone无需启动额外mysqld, 只要在实例上执行一条sql语句，指定下目标目录即可:

`CLONE LOCAL DATA DIRECTORY [=] 'clone_dir';

root@test 03:49:43>SELECT STAGE, STATE, END_TIME FROM performance_schema.clone_progress;
+-----------+-------------+----------------------------+
| STAGE | STATE | END_TIME |
+-----------+-------------+----------------------------+
| DROP DATA | Completed | 2019-07-26 12:07:12.285611 |
| FILE COPY | Completed | 2019-07-26 12:07:18.270998 |
| PAGE COPY | Completed | 2019-07-26 12:07:18.472560 |
| REDO COPY | Completed | 2019-07-26 12:07:18.673061 |
| FILE SYNC | Completed | 2019-07-26 12:07:32.090219 |
| RESTART | Not Started | NULL |
| RECOVERY | Not Started | NULL |
+-----------+-------------+----------------------------+
7 rows in set (0.00 sec)
`

需要BACKUP_ADMIN权限

### 远程 clone
`CLONE INSTANCE FROM USER@HOST:PORT
IDENTIFIED BY 'password'
[DATA DIRECTORY [=] 'clone_dir']
[REQUIRE [NO] SSL];

mysql> SET GLOBAL clone_valid_donor_list = 'example.donor.host.com:3306';
mysql> CLONE INSTANCE FROM clone_user@example.donor.host.com:3306 IDENTIFIED BY 'password';
mysql> CLONE INSTANCE FROM user_name@example.donor.host.com:3306 IDENTIFIED BY 'password' DATA DIRECTORY = '/path/to/clone_dir';
`
* 需要指定绝对路径，并且路径目录必须不存在
* 在接受机器上启动mysqld，执行上述语句连接到目标机器，就能从目标机器上clone数据到本地，注意如果没有指定data directory的话，就默认配置的目录，已有的文件会被清理掉，并在clone完成后重启
* 两个实例上都需要安装clone plugin
* 必须有相同的字符集设置

官方文档列出的一些限制：

1. ddl包括truncate table在clone期间不允许执行 //被block住
2. An instance cannot be cloned from a different MySQL server version. The donor and recipient must have the same MySQL server version.
3. the X Protocol port specified by mysqlx_port is not supported for remote cloning operations
4. The clone plugin does not support cloning of MySQL server configurations
5. 不支持clone binlog
6. The clone plugin only clones data stored in InnoDB. Other storage engine data is not cloned
7. Connecting to the donor MySQL server instance through MySQL Router is not supported.
8. Local cloning operations do not support cloning of general tablespaces that were created with an absolute path. A cloned tablespace file with the same path as the source tablespace file would cause a conflict.

### 主要流程
主要流程包含如下几个过程：
[INIT] —> [FILE COPY] —> [PAGE COPY] —> [REDO COPY] -> [Done]

#### INIT 阶段
需要持有backup lock, 阻止ddl进行

#### FILE COPY 阶段
按照文件进行拷贝，同时开启page tracking功能，记录在拷贝过程中修改的page, 此时会设置buf_pool->track_page_lsn为当前lsn，track_page_lsn在flush page阶段用到:

`buf_flush_page:

if (!fsp_is_system_temporary(bpage->id.space()) &&
 buf_pool->track_page_lsn != LSN_MAX) {
 page_t *frame;
 lsn_t frame_lsn;

 frame = bpage->zip.data;

 if (!frame) {
 frame = ((buf_block_t *)bpage)->frame;
 }
 frame_lsn = mach_read_from_8(frame + FIL_PAGE_LSN); //对于在track_page_lsn之后的page, 如果frame_Lsn大于track_page_lsn, 表示已经记录下page id了，无需重复记录

 arch_page_sys->track_page(bpage, buf_pool->track_page_lsn, frame_lsn,
 false); // 将page id记录下来，表示在track_page_lsn后修改过的page
}

会创建一个后套线程page_archiver_thread()，将内存记录的page id flush到disk上
`

#### PAGE COPY
这里有两个动作

* 开启redo archiving功能，从当前点开始存储新增的redo log，这样从当前点开始所有的增量修改都不会丢失
* 同时上一步在page track的page被发送到目标端。确保当前点之前所做的变更一定发送到目标端

关于redo archiving，实际上这是官方早就存在的功能，主要用于官方的企业级备份工具，但这里clone利用了该特性来维持增量修改产生的redo。 在开始前会做一次checkpoint， 开启一个后台线程log_archiver_thread()来做日志归档。当有新的写入时(notify_about_advanced_write_lsn)也会通知他去archive

当arch_log_sys处于活跃状态时，他会控制日志写入以避免未归档的日志被覆盖(log_writer_wait_on_archiver), 注意如果log_writer等待时间过长的话， archive任务会被中断掉

#### Redo Copy
停止Redo Archiving”, 所有归档的日志被发送到目标端，这些日志包含了从page copy阶段开始到现在的所有日志，另外可能还需要记下当前的复制点，例如最后一个事务提交时的binlog位点或者gtid信息，在系统页中可以找到

#### Done
目标端重启实例，通过crash recovery将redo log应用上去。

## 参考文档
[官方博客:Clone: Create MySQL instance replica](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fmysqlserverteam.com%2Fclone-create-mysql-instance-replica%2F)

[The Clone Plugin](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fdev.mysql.com%2Fdoc%2Frefman%2F8.0%2Fen%2Fclone-plugin.html)

[WL#9209: InnoDB: Clone local replica](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fdev.mysql.com%2Fworklog%2Ftask%2F%3Fid%3D9209)

[WL#9210: InnoDB: Clone remote replica](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fdev.mysql.com%2Fworklog%2Ftask%2F%3Fid%3D9210)

[WL#9682: InnoDB: Support cloning encrypted and compressed database](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fdev.mysql.com%2Fworklog%2Ftask%2F%3Fid%3D9682)

[WL#9211: InnoDB: Clone Replication Coordinates](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fdev.mysql.com%2Fworklog%2Ftask%2F%3Fid%3D9211)

[WL#11636: InnoDB: Clone Remote provisioning](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.769fa136vqfqE7&url=https%3A%2F%2Fdev.mysql.com%2Fworklog%2Ftask%2F%3Fid%3D11636)

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)