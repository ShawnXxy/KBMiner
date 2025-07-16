# MySQL · 参数故事 · innodb_flush_log_at_trx_commit

**Date:** 2014/08
**Source:** http://mysql.taobao.org/monthly/2014/08/02/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2014 / 08
 ](/monthly/2014/08)

 * 当期文章

 MySQL · 参数故事 · timed_mutexes
* MySQL · 参数故事 · innodb_flush_log_at_trx_commit
* MySQL · 捉虫动态 · Count(Distinct) ERROR
* MySQL · 捉虫动态 · mysqldump BUFFER OVERFLOW
* MySQL · 捉虫动态 · long semaphore waits
* MariaDB · 分支特性 · 支持大于16K的InnoDB Page Size
* MariaDB · 分支特性 · FusionIO特性支持
* TokuDB · 性能优化 · Bulk Fetch
* TokuDB · 数据结构 · Fractal-Trees与LSM-Trees对比
* TokuDB·社区八卦·TokuDB团队

 ## MySQL · 参数故事 · innodb_flush_log_at_trx_commit 
 Author: 

 **背景**

　　innodb_flush_log_at_trx_commit 这个参数可以说是InnoDB里面最重要的参数之一，它控制了重做日志（redo log）的写盘和落盘策略。 具体的参数意义见手册

　　简单说来，可选值的安全性从0->2->1递增，分别对应于mysqld 进程crash可能丢失 -> OS crash可能丢失 -> 事务安全。

　　以上是路人皆知的故事，并且似乎板上钉钉，无可八卦。

**innodb_use_global_flush_log_at_trx_commit**

　　直到2010年的某一天，Percona的CTO Vadim同学觉得这种一刀切的风格不够灵活，最好把这个变量设置成session级别，每个session自己控制。

　　但同时为了保持Super权限对提交行为的控制，同时增加了innodb_use_global_flush_log_at_trx_commit参数。 这两个参数的配合逻辑为：

　　1、若innodb_use_global_flush_log_at_trx_commit为OFF，则使用session.innodb_flush_log_at_trx_commit;

　　2、若innodb_use_global_flush_log_at_trx_commit为ON,则使用global .innodb_flush_log_at_trx_commit（此时session中仍能设置，但无效）

　　3、每个session新建时，以当前的global.innodb_flush_log_at_trx_commit 为默认值。

**业务应用**

　　这个特性可以用在一些对表的重要性做等级定义的场景。比如同一个实例下，某些表数据有外部数据备份，或允许丢失部分事务的情况，对这些表的更新，可以设置 Session.innodb_flush_log_at_trx_commit为非1值。

　　在阿里云RDS服务中，我们对数据可靠性和可用性要求更高，将 innodb_use_global_flush_log_at_trx_commit设置为ON，因此修改session.innodb_flush_log_at_trx_commit也没有作用，统一使用 global.innodb_flush_log_at_trx_commit = 1。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)