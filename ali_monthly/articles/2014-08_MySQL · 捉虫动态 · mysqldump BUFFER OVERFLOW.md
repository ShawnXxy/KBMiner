# MySQL · 捉虫动态 · mysqldump BUFFER OVERFLOW

**Date:** 2014/08
**Source:** http://mysql.taobao.org/monthly/2014/08/04/
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

 ## MySQL · 捉虫动态 · mysqldump BUFFER OVERFLOW 
 Author: 

 **bug背景**

　　在上个月发布的新版本中，官方修复了一个mysqldump输入库名或表明长度越界的bug。

　　在MySQL的当前约束中，库名和表名字符串最大长度为NAME_LEN=192字节。在myqldump实现中，需要对输入的表名做处理，比如增加``防止表名中的特殊字符。这些临时处理的内存，声明为类似name_buff[NAME_LEN+3],这样在用户输入的库名或表名长度过长时，会造成数组越界读写，导致不可预期的错误。

　　这个修复的逻辑也比较简单，就是在开始dump前作参数检查，若发现长度超过NAME_LEN的库/表名，直接抛错返回“argument too long”。

**细节说明**

　　需要注意的是，该修复改变了mysqldump的行为。由于名字长度超过NAME_LEN的库/表肯定不存在，因此修复之前的逻辑，是报告该表不存在。“table not exists”这个逻辑是可以通过–force 跳过的。而“argument too long”则无视force参数，直接抛错返回。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)