# MySQL · 文件结构 · 告别frm文件

**Date:** 2014/10
**Source:** http://mysql.taobao.org/monthly/2014/10/07/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2014 / 10
 ](/monthly/2014/10)

 * 当期文章

 MySQL · 5.7重构 · Optimizer Cost Model
* MySQL · 系统限制 · text字段数
* MySQL · 捉虫动态 · binlog重放失败
* MySQL · 捉虫动态 · 从库OOM
* MySQL · 捉虫动态 · 崩溃恢复失败
* MySQL · 功能改进 · InnoDB Warmup特性
* MySQL · 文件结构 · 告别frm文件
* MariaDB · 新鲜特性 · ANALYZE statement 语法
* TokuDB · 主备复制 · Read Free Replication
* TokuDB · 引擎特性 · 压缩

 ## MySQL · 文件结构 · 告别frm文件 
 Author: 

 **提要**

长久以来，server层和InnoDB层都保存了表的元数据，server使用frm文件保存了column，data_types等信息，而InnoDB使用data dictionary来保存meta data。

由于server层使用文件系统，而InnoDB使用事务引擎，所以经常会存在两者不一致的情况，比如：

`create table的过程中实例crash
alter table过程中实例crash
`
具体可以参见：[http://dev.mysql.com/doc/refman/5.6/en/innodb-troubleshooting-datadict.html](http://dev.mysql.com/doc/refman/5.6/en/innodb-troubleshooting-datadict.html) 包括相关的解决方法。

**改进**

MySQL 后续的版本准备做相关的改进：

1. 使用native InnoDB-based Data Dictionary保存meta data，不再需要frm文件
2. 使用InnoDB引擎保存MySQL的系统表，比如privileges和timezones相关的表

使用new Data Dictionary，去掉frm文件，目前还在MySQL lab版本中。

而在MySQL 5.7的版本中，以下的系统表已不再使用MyISAM，而使用InnoDB引擎保存数据：

* help_category
* help_keyword
* help_relation
* help_topic
* time_zone
* time_zone_leap_second
* time_zone_name
* time_zone_transition,
* time_zone_transition_type

**变化**

1. 由于使用具有ACID特性的InnoDB引擎，由crash导致的元数据不一致情况将不再出现。
2. 对于information_schema中元数据的查询，系统将暴露一个基表上的view出来，供查询。
3. 由于使用InnoDB引擎来保存数据，–skip-innodb的参数将不再有意义，5.7版本中做删除处理。

**问题**

1. 系统表切换到InnoDB引擎上，对于版本升级或者降级需要对脚本特殊处理。
2. 去掉frm文件，系统如何平滑的进行升级？
3. 第三方引擎怎么办？oracle后续的打算是如何？这是一个很大的问题。

由于去掉frm文件使用native InnoDB-based Data Dictionary的特性还在lab环境中酝酿，期待中。

无论如何，提升failure recovery的水平，对于使用者来说，终归是好事情！

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)