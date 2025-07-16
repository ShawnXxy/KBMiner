# MySQL · 关于undo表空间的一些新变化

**Date:** 2019/04
**Source:** http://mysql.taobao.org/monthly/2019/04/05/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2019 / 04
 ](/monthly/2019/04)

 * 当期文章

 MySQL · 引擎特性 · 临时表那些事儿
* MSSQL · 最佳实践 · 使用SSL加密连接
* Redis · 引擎特性 · radix tree 源码解析
* MySQL · 引擎分析 · InnoDB history list 无法降到0的原因
* MySQL · 关于undo表空间的一些新变化
* MySQL · 引擎特性 · 新的事务锁调度VATS简介
* MySQL · 引擎特性 · 增加系统文件追踪space ID和物理文件的映射
* PgSQL · 应用案例 · PostgreSQL 9种索引的原理和应用场景
* PgSQL · 应用案例 · 任意字段组合查询
* PgSQL · 应用案例 · PostgreSQL 并行计算

 ## MySQL · 关于undo表空间的一些新变化 
 Author: yinfeng 

 基于版本为 MySQL8.0.3

InnoDB的undo log是其实现多版本的关键组件，在物理上以数据页的形式进行组织。在早期版本中(<5.6)，undo tablespace是在ibdata中，因此一个常见的问题是由于大事务不提交导致ibdata膨胀，这时候通常只有重建数据库一途来缩小空间。到了MySQL5.6版本， InnoDB开始支持独立的undo tablespace，也就是说，undo log可以存储于ibdata之外。但这个特性依然鸡肋：

1. 首先你必须在install实例的时候就指定好独立Undo tablespace, 在install完成后不可更改。
2. Undo tablepsace的space id必须从1开始，无法增加或者删除undo tablespace。

到2. 了MySQL5.7版本中，终于引入了一个期待已久的功能：即在线truncate undo tablespace。DBA终于摆脱了undo空间膨胀的苦恼。

在MySQL8.0，InnoDB再进一步，对undo log做了进一步的改进：

1. 无需从space_id 1开始创建undo tablespace，这样解决了In-place upgrade或者物理恢复到一个打开了Undo tablespace的实例所产生的space id冲突。不过依然要求undo tablespace的space id是连续分配的（fsp_is_undo_tablespace）, space id的范围为(0xFFFFFFF0UL - 128, 0xFFFFFFF0UL - 1) (Bug #23517560)
2. 从8.0.3版本开始，默认undo tablespace的个数从0调整为2，也就是在8.0版本中，独立undo tablespace被默认打开。修改该参数为0会报warning并在未来不再支持(WL#10583)
3. 允许动态的增加undo tablespace的个数，也就是说可以动态调整innodb_undo_tablespaces。当调大该参数时，会去创建新的undo tablespace。但如果设小该值，则仅仅是不实用多出来的Undo tablespace，目前不会去主动删除它们(innodb_undo_tablespaces_update), WL#9507
4. Undo tablespace的命名从undoNNN修改为undo_NNN
5. 和以前版本最大的不同之处就是，在8.0之前只能创建128个回滚段，而在8.0版本开始，每个Undo tablespace可以创建128个回滚段，也就是说，总共有innodb_rollback_segments * innodb_undo_tablespaces个回滚段。这个改变的好处是在高并发下可以显著的减少因为分配到同一个回滚段内的事务间产生的锁冲突
6. Innodb_undo_truncate参数默认打开，这意味着默认情况下，undo tablespace超过1GB（参数innodb_max_undo_log_size来控制）时，就会触发online truncate
7. 支持undo tablespace加密( 参考文档)
PS: 本文是本人在看代码过程中的粗略记录，不保证全面性
8.在ibdata中保留的32个slot原本用于临时表空间的回滚段，但事实上他们并没有做任何的持久化，因此在8.0中直接在内存中为其创建单独的内存结构，这32个slot可以用于持久化的undo回滚段(Bug #24462978!

主要代码commit(按照时间顺序由新到旧):

[Commit 1](https://github.com/mysql/mysql-server/commit/b26f8d6552d5464b80c938572412e7566505cd97?spm=a2c4e.11153940.blogcont341036.14.6b235440fWlXy0)

`WL#10583: Stop using rollback segments in the system tablespace

* Change the minimum value of innodb_undo_tablespaces to 2
* Fix code that allows and checks for innodb_undo_tablespaces=0
* Fix all testcases affected
`
[Commit 2](https://github.com/mysql/mysql-server/commit/53c923186ec76e93fefca575b43bdc718c24e49e?spm=a2c4e.11153940.blogcont341036.15.6b235440fWlXy0)

`WL#9507: Make innodb_undo_tablespaces variable dynamic
WL#10498: InnoDB: Change Default for innodb_undo_tablespaces from 0 to 2
WL#10499: InnoDB: Change Default for innodb_undo_log_truncate from OFF to ON

* Introduce innodb_undo_tablespace_update() and
srv_undo_tablespaces_update() for online updates.
* Introduce innodb_rollback_segments_update() for online updates.
* Introduce srv_undo_tablespaces_uprade() to convert 5.7 undo
tablespaces to 8.0.1.
* Introduce srv_undo_tablespaces_downgrade() in case the upgrade from
5.7 fails.
* Introduce trx_rseg_adjust_rollback_segments() and
trx_rseg_add_rollback_segments() to consolidate the creation and use of
rollback segments in any tablespace.
* Introduce a new file format for undo tablespaces including a reserved
range for undo space IDs and an RSEG_ARRAY page.
* Rename auto-generated undo tablespace names from undonnn to undo-nnn
* Expand the undo namespace to support new undo file format.
* Various changes to allow online creation of undo spaces and rollback
segments.
* Change round robin routine for supplying rsegs to transactions to
support rseg arrays in each tablespace.
* Handle conversions between undo space_id and undo space number.
* Introduce undo_settings.test
* Adjust and improve a lot of testcases.
`
[Commit 3](https://github.com/mysql/mysql-server/commit/3e0111b7841cae25cee910f83e5399d12ee6a21f?spm=a2c4e.11153940.blogcont341036.16.6b235440fWlXy0)

`WL#10322: Deprecate innodb_undo_logs in 5.7

* Add (deprecated) to innodb-undo-logs description and mention that it
is actually setting the number of rollback segments.
* Delete “(deprecated)” from innodb-rollback-segments message.
* Add a deprecation warning message when innodb_undo_logs is used
at runtime and also at startup in a config or the command line.
* Return a warning when innodb_undo_logs is used at runtime.
* Rename srv_undo_logs to srv_rollback_segments in code
* Rename innodb_undo_logs to innodb_rollback_segments in all collections
and testcases except sysvars.innodb_undo_logs_basic.
* Fix sysvars.innodb_undo_logs_basic to suppress the deprecation warning.
Add a restart to exercise the deprecation code for using it at startup.
`
[Commit 4](https://github.com/mysql/mysql-server/commit/1ccef6a3d19b9034b0225fcc60e093e6c47c446f?spm=a2c4e.11153940.blogcont341036.17.6b235440fWlXy0)

`Bug #25572279 WARNING ALLOCATED TABLESPACE ID N FOR INNODB_UNDO00N
OLD MAXIMUM WAS N

This extra bootstrap warning was introduced in rb#13164:
Bug#24462978: Free up 32 slots in TRX_SYS page for non-temp rsegs.

It occurs when the database is initialized with undo tablespaces > rollback
segments. In this case, only the first undo tablespaces associated with the
limited rollback segments will be used. The remaining undo tablespaces
cannot be used because the rollback segment slots are not available in the
TRX_SYS page. But when starting the server, we have to open all unused
undo tablespaces. Along with opening the unused undo tablespaces, the
max_assigned_id needs to be incremented to avoid the warning. The rb#13164
patch was not doing that.

The solution is simply to call to fil_set_max_space_id_if_bigger(space_id)
 in srv_undo_tablespaces_open() instead of the other three place it does now.
 This makes sure that the condition "id > fil_system->max_assigned_id" in
 fil_space_create() is false which will prevent the reported warning message.
`
[Commit 5](https://github.com/mysql/mysql-server/commit/7c1e99893f70d39bb1f4cbeb3fab34cdbd2ab55c?spm=a2c4e.11153940.blogcont341036.18.6b235440fWlXy0)

`Bug #25551311 BACKPORT BUG #23517560 REMOVE SPACE_ID
RESTRICTION FOR UNDO TABLESPACES

Description:
============
The restriction that required the first undo tablespace to use space_id 1
is removed. The first undo tablespace can now use a space_id other than 1.
space_id values for undo tablespaces are still assigned in a consecutive
sequence.
`
[Commit 6](https://github.com/mysql/mysql-server/commit/71e656a370072dad885736774a513e2d9feb65ff?spm=a2c4e.11153940.blogcont341036.19.6b235440fWlXy0)

```
WL#9289 InnoDB: Support Transparent Data Encryption for Undo Tablespaces
WL#9290 InnoDB: Support Transparent Data Encryption for Redo Log

Based on wl#8548, we provide encryption support for redo log and undo tablespaces.

For encrypting redo/undo log, as same as we did in wl#8548, we will en/decrypt the
redo log blocks/undo log pages in the I/O layer.
Which means, the en/decryption only happens when the redo/undo log read or
write from/to disk.

For redo log, encryption metadata will be stored in the header of first log file.
Same as wl#8548, there're 2 key levels here, master key and tablespace key.
Master key is stored in keyring plugin, and it's used to en/decrypt tablespace
key and iv. Tablespace key is for en/decrypt redo log blocks, and it will be
stored into the 3rd block of first redo log file(ib_logfile0).

For undo log, Same as regular tablespace, the encryption metadata will be stored
in the first page of data file.

We also added 2 new global variables innodb_redo_log_encrypt=ON/OFF,
innodb_undo_log_encrypt=ON/OFF for en/disable redo/undo log encryption.

```

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)