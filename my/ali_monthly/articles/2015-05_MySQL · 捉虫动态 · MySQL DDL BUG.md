# MySQL · 捉虫动态 · MySQL DDL BUG

**Date:** 2015/05
**Source:** http://mysql.taobao.org/monthly/2015/05/06/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2015 / 05
 ](/monthly/2015/05)

 * 当期文章

 MySQL · 引擎特性 · InnoDB redo log漫游
* MySQL · 专家投稿 · MySQL数据库SYS CPU高的可能性分析
* MySQL · 捉虫动态 · 5.6 与 5.5 InnoDB 不兼容导致 crash
* MySQL · 答疑解惑 · InnoDB 预读 VS Oracle 多块读
* PgSQL · 社区动态 · 9.5 新功能BRIN索引
* MySQL · 捉虫动态 · MySQL DDL BUG
* MySQL · 答疑解惑 · set names 都做了什么
* MySQL · 捉虫动态 · 临时表操作导致主备不一致
* TokuDB · 引擎特性 · zstd压缩算法
* MySQL · 答疑解惑 · binlog 位点刷新策略

 ## MySQL · 捉虫动态 · MySQL DDL BUG 
 Author: 冷香 

 ## 背景
MySQL保存了两份元数据，一份在server层，保存在FRM文件中，另外一份在引擎层，比如InnoDB的数据字典中，这样也就造成了DDL语句经常导致元数据不一致的情况，下面介绍两个近期出现的因为DDL产生的bug。

### rename 外键引用的column

**BUG复现过程**

`CREATE TABLE t1 (a INT NOT NULL,
 b INT NOT NULL,
 INDEX idx(a)) ENGINE=InnoDB;

CREATE TABLE t2 (a INT KEY, b INT, INDEX ind(b),
 FOREIGN KEY (b) REFERENCES t1(a)
 ON DELETE CASCADE
 ON UPDATE CASCADE) ENGINE=InnoDB;

ALTER TABLE t1 CHANGE a id INT;
`

在DEBUG版本下，MySQL实例是crash的，crash在 `handler0alter.cc` line 5643。

**BUG原因分析**

在做alter语句的时候，因为rename的column关联有foreign key，所以需要在数据字典中更改这个foreign key，但在数据字典缓存中还保留了一份foreign对象，代码只做了持久化的更改，在重新`dict_load_foreigns()`的时候，和缓存中的foreign key冲突，导致函数报错。

**BUG修复方法**

BUG修复也比较简单，在rename的过程中，先更改数据字典，然后调用`dict_foreign_remove_from_cache`函数清理内存中的对象，这样在重新`dict_load_foreigns`的时候，就一切正常了。

MySQL官方版本在5.6.23修复了这个问题。

## alter 添加和删除索引导致不一致

**BUG复现过程**

`CREATE TABLE t1(id INT, col1 INT, col2 INT, KEY(col1))ENGINE=InnoDB;
alter table t1 add key(col2), drop key col1;
`

复现此BUG的时候需要使用DEBUG_SYNC，在alter table的过程中，add key(col2)步骤成功，而在drop key的时候InnoDB报失败。
然后导致MySQL server层对表t1的定义和InnoDB层的定义不一致。

**BUG原因分析**
在drop key报引擎失败的时候，MySQL server层开始回滚整个DDL语句，server层这时回滚了FRM的定义，而InnoDB成功添加的key(col2)却没有回滚。

**BUG修复方法**
在alter的过程中，记录每一个阶段成功的调用，在语句结束的时候，如果遇到需要回滚的statement，需要同时回滚引擎层和server层。

因为MySQL保存了两份元数据，也造成在DDL变更的过程中，无法保证数据的一致性。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)