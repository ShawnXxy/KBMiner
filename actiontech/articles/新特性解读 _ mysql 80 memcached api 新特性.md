# 新特性解读 | mysql 8.0 memcached api 新特性

**原文链接**: https://opensource.actionsky.com/20200706-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-07-06T00:26:34-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文关键字：memcached
相关推荐文章：
[新特性解读 | 趋近完美的 Undo 空间](https://opensource.actionsky.com/20200420-mysql/)
[新特性解读 | 8.0 新增 DML 语句（TABLE & VALUES）](https://opensource.actionsky.com/20200325-mysql/)
**一款优秀的缓存系统**
memcache 本身是一款分布式的高速缓存系统，以 key-value 的形式常驻内存，一般用来做网站或者数据库的缓存使用。
特别是对以下场景非常适合用 memcache 来做缓存：
1. 频繁访问的数据2. 安全性要求比较低的数据3. 更新比较频繁的小表（用户状态表、物品库存等）
**MySQL memcached api **
MySQL 5.6 —— 开始支持
MySQL 5.6 把 memcache 功能以插件形式集成到 MySQL 数据库中，称为 memcached api。这样一来，memcache 的数据以 InnoDB 关系表的形式同步于磁盘，解决了 memcache 的几个问题：1. 解决了 memcache 的数据持久化的问题；2. 可以很方便的以 SQL 语句的形式直接访问 memcache 的数据；3. 不需要单独安装 memcache，安装 MySQL 即可使用。
MySQL 5.7 —— 深入优化
MySQL 5.7 对 memcached api 做了深入优化，官方数据显示使用 memcached api，在只读的场景中，QPS 提升到 100W。
MySQL 8.0 —— 新增特性
MySQL 8.0 发布后，又在功能上给 memcached api 增加了两个新特性。1. 批量获取 KEY相比原来一次只能读取一个 Key 来讲，减少了客户端与 MySQL 服务端的数据交互次数。2. 可以对 KEY 进行 RANGE 操作可以直接类似于 **select * from t1 where id between 10 and 20** 这样的范围检索语句。
**演示**
下面我们来演示下这两个新的特性，先把 memcached api 插件以及需要的示例表数据准备好。
**1. 导入元数据**
从 MySQL 相关目录导入 memcached api 元数据（包含配置，容器等）。- 
- 
`(localhost:ytt)<mysql>\. /usr/share/mysql-8.0/innodb_memcached_config.sql``Query OK, 1 row affected (0.05 sec)`
**2. 安装插件**
第一次需要手动安装 memcached 插件。- 
- 
`(localhost:test)<mysql>INSTALL PLUGIN daemon_memcached soname "libmemcached.so";``Query OK, 0 rows affected (0.08 sec)`再次确认 memcached 插件安装成功。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
(localhost:information_schema)<mysql>select * from information_schema.plugins where plugin_name = 'daemon_memcached'\G`*************************** 1. row ***************************``           PLUGIN_NAME: daemon_memcached``        PLUGIN_VERSION: 1.0``         PLUGIN_STATUS: ACTIVE``           PLUGIN_TYPE: DAEMON``   PLUGIN_TYPE_VERSION: 80020.0``        PLUGIN_LIBRARY: libmemcached.so``PLUGIN_LIBRARY_VERSION: 1.10``         PLUGIN_AUTHOR: Oracle Corporation``    PLUGIN_DESCRIPTION: Memcached Daemon``        PLUGIN_LICENSE: GPL``           LOAD_OPTION: ON``1 row in set (0.00 sec)
```
**3. 准备数据**
建立一张示例表 t1。 > 注意：表主键对应 memcached api 的 Key，除主键外的其他字段只能整型或者字符类型，剩下的 flags,cas,expiry 是规定死的字段。
- 
- 
- 
- 
- 
- 
- 
- 
- 
(localhost:ytt)<mysql>create table t1 (``  id serial primary key, ``  r1 int,``  r2 int,``  r3 varchar(20), ``  flags int,``  cas bigint unsigned, ``  expiry int);``Query OK, 0 rows affected (0.05 sec)`目前插入的一些示例数据。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
(localhost:ytt)<mysql>select * from t1;`+----+------+------+---------------------+-------+------+--------+``| id | r1   | r2   | r3                  | flags | cas  | expiry |``+----+------+------+---------------------+-------+------+--------+``|  1 |    2 |    9 | 2040-01-20 07:29:47 |     0 |    0 |      0 |``|  2 |    7 |    1 | 2037-12-25 22:43:52 |     0 |    0 |      0 |``|  3 |    2 |   18 | 2049-04-15 07:05:35 |     0 |    0 |      0 |``|  4 |    8 |    5 | 2048-08-17 23:38:39 |     0 |    0 |      0 |``|  6 |    9 |   11 | 2043-02-13 11:05:28 |     0 |    0 |      0 |``|  7 |    2 |    5 | 2049-03-25 20:27:01 |     0 |    0 |      0 |``|  8 |    7 |   13 | 2032-12-11 05:21:01 |     0 |    0 |      0 |``|  9 |    1 |    7 | 2028-03-29 03:06:18 |     0 |    0 |      0 |``| 13 |    6 |   12 | 2021-11-22 11:24:06 |     0 |    0 |      0 |``| 14 |    4 |   20 | 2035-12-14 13:23:55 |     0 |    0 |      0 |``| 15 |   10 |   15 | 2030-03-24 17:09:34 |     0 |    0 |      0 |``| 16 |    8 |   15 | 2022-10-21 09:31:45 |     0 |    0 |      0 |``| 17 |    3 |    3 | 2034-07-20 09:52:18 |     0 |    0 |      0 |``| 18 |    9 |   19 | 2020-06-25 05:08:37 |     0 |    0 |      0 |``| 19 |    1 |    7 | 2041-08-29 11:35:06 |     0 |    0 |      0 |``| 20 |    6 |   14 | 2031-04-25 01:05:20 |     0 |    0 |      0 |``+----+------+------+---------------------+-------+------+--------+``16 rows in set (0.00 sec)
```
**4. 使用插件**
让 memcached 插件能识别表 ytt.t1，插入一条记录到 memcache 容器表。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
(localhost:ytt)<mysql>insert into innodb_memcache.containers(``    name, ``    db_schema, ``    db_table, ``    key_columns, ``    value_columns, ``    flags, ``    cas_column, ``    expire_time_column, ``    unique_idx_name_on_key``  ) -> values (``    'default', ``    'ytt', ``    't1', ``    'id', ``    'r1|r2|r3',  ``    'flags',``    'cas',``    'expiry',``    'primary');``Query OK, 1 row affected (0.01 sec)`
**5. 读取数据**
重启 memcached 插件，让其识别刚才的数据。- 
- 
- 
- 
- 
`(localhost:ytt)<mysql>UNINSTALL PLUGIN daemon_memcached;``Query OK, 0 rows affected (2.02 sec)``
``(localhost:ytt)<mysql>INSTALL PLUGIN daemon_memcached soname "libmemcached.so";``Query OK, 0 rows affected (0.01 sec)`MySQL 5.7 操作 memcached api  ，只可以一次获取单个 key。比如要获取 id 为（1,2,3,4,5,6）的记录，需要重复 get 6 次。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
root@ytt-unbuntu:/data/mysql57/data# telnet localhost 11211`Trying 127.0.0.1...``Connected to localhost.``Escape character is '^]'.``get 1``VALUE 1 0 23``2|9|2040-01-20 07:29:47``END``get 2``VALUE 2 0 23``7|1|2037-12-25 22:43:52``END``get 3``VALUE 3 0 24``2|18|2049-04-15 07:05:35``END``get 4``VALUE 4 0 23``8|5|2048-08-17 23:38:39``END``get 5``END``get 6``VALUE 6 0 24``9|11|2043-02-13 11:05:28``END
```
想一次性获取多个 KEY，直接报错！- 
- 
```
get 1 2 3 4 5 6``We temporarily don't support multiple get option.
```
MySQL 8.0 操作 memcached api， 可以一次性获取多个 Key。比如同样要获取 id 为（1,2,3,4,5,6）的记录，只需要 get 1 次即可。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
root@ytt-unbuntu:/home/ytt# telnet localhost 11222``Trying 127.0.0.1...``Connected to localhost.``Escape character is '^]'.``
``get 1 2 3 4 5 6``VALUE 1 0 23``2|9|2040-01-20 07:29:47``VALUE 2 0 23``7|1|2037-12-25 22:43:52``VALUE 3 0 24``2|18|2049-04-15 07:05:35``VALUE 4 0 23``8|5|2048-08-17 23:38:39``VALUE 6 0 24``9|11|2043-02-13 11:05:28``END
```
也支持范围获取，比如同样 get id 为（1,2,3,4,5,6）的所有记录，只需要 get @<=6 即可：- 
```
get @<=6
```
再次获取 id 大于10 的记录：- 
```
get @>10
```
获取 ID 大于 10 并且小于 20 的记录：
- 
```
get @>10@<20
```
不过目前 MySQL 8.0 对 memcache 的范围支持比较简单，只支持最多一个范围，多个范围暂时不支持。- 
- 
```
get @>2@<3@<10   `END
```
这样的是没有结果的，MySQL 此时把这个检索变为 id 大于 2 并且小于 &#8220;3@<10&#8243;，这样很明显没有记录。
**总结**
本篇介绍了 MySQL memcached api 使用场景以及在 MySQL 8.0 下新特性使用例子，希望对大家有帮助。