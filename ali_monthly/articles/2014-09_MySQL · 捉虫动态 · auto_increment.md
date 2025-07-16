# MySQL · 捉虫动态 · auto_increment

**Date:** 2014/09
**Source:** http://mysql.taobao.org/monthly/2014/09/06/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2014 / 09
 ](/monthly/2014/09)

 * 当期文章

 MySQL · 捉虫动态 · GTID 和 DELAYED
* MySQL · 限制改进 · GTID和升级
* MySQL · 捉虫动态 · GTID 和 binlog_checksum
* MySQL · 引擎差异·create_time in status
* MySQL · 参数故事 · thread_concurrency
* MySQL · 捉虫动态 · auto_increment
* MariaDB · 性能优化 · Extended Keys
* MariaDB · 主备复制 · CREATE OR REPLACE
* TokuDB · 参数故事 · 数据安全和性能
* TokuDB · HA方案 · TokuDB热备

 ## MySQL · 捉虫动态 · auto_increment 
 Author: 

 **背景：**

　　Innodb引擎使用B_tree结构保存表数据，这样就需要一个唯一键表示每一行记录(比如二级索引记录引用)。

　　Innodb表定义中处理主键的逻辑是：

　　1.如果表定义了主键，就使用主键唯一定位一条记录

　　2.如果没有定义主键，Innodb就生成一个全局唯一的rowid来定位一条记录

auto_increment的由来:

　　1.Innodb强烈推荐在设计表中自定义一个主键，因为rowid是全局唯一的，所以如果有很多表没有定义主键，就会在生成rowid上产生争用。

`/* Dictionary system struct */
struct dict_sys_struct{
mutex_t mutex;
row_id_t row_id;
......
}
`
　　row_id由mutex保护，并在每次checkpoint的时候，写入到数据字典的文件头。

　　2.当用户自定义了主键后，由于大部分实际应用部署的分布式，所以主键值的生成上，采用集中式的方式，更容易实现唯一性，所以auto_increment非常合适。

　　auto_increment也带来两个好处：

　　1. auto_increment的值是表级别的，不会在db级别上产生争用

　　2. 由于auto_increment的顺序性，减少了随机读的可能，保证了写入的page的缓冲命中。（不可否认，写入的并发足够大时，会产生热点块的争用）

auto_increment引起的bug：

　　环境：MySQL 5.6.16版本, binlog_format=row

　　case复现：

`create table test.kkk ( c int(11) default null, id int(11) not null auto_increment, d int(11) default null, primary key (id), unique key d (d) )
engine=innodb default charset=latin1;
insert into test.kkk values(5, 27,4);
replace into test.kkk(c, id, d) values(6, 35, 4);
commit; 
`

show create table时：
主库：auto_increment=36
备库：auto_increment=28

　　当进行主备切换后，导致主键冲突，slave恢复异常。

　　同样insert on duplication update 语句同样存在这样的问题。

**aliyun rds分支bug修复**

　　问题的原因：Innodb对于auto_increment的处理，当语句是insert时，会进行递增，而update，delete语句则不更新。

　　当replace语句在主库的执行时：

　　1. 先按照insert语句执行，发现uk冲突。

　　2. 演变成update语句进行更新。

　　这样在主库，虽然insert失败，但auto_increment也递增上去了。但到备库，row格式下，只产生了一个update row event，

　　备库无法知道主库是一个replace语句，而且insert还失败了， 所以auto_increment在备库没有递增。

　　修复方式：在备库，对于update进行auto_increment递增，可能会产生副作用，即auto_increment的浪费，但不会产生主键冲突。

**那些年经历的auto_increment坑：**

　　1. 实例重启，主键冲突：

　　内存中的autoinc值，在系统重启后，使用select max(id) from table来初始化。所以，如果你设计的业务表，存在delete操作，那么一旦你的实例crash过，重启后，可能会复用以前使用过的id值。如果你需要持续对这个表进行逻辑备份，那么就可能会碰到主键冲突的问题。

　　2. load file阻塞：

　　在设置innodb_autoinc_lock_mode=1的时候，MySQL为了维护单个statement语句的id连续性，当不确定插入条数的时候，会在语句整个执行过程中

　　持有LOCK_AUTO_INC, /* locks the auto-inc counter of a table in an exclusive mode */

　　这个锁是表级别的，使用互斥模式。

　　所以，在繁忙的表上，如果要导入数据，小心可能阻塞正常的业务写入，并发写入在这个时候也会阻塞的。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)