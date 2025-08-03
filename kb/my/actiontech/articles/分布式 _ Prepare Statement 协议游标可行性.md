# 分布式 | Prepare Statement 协议游标可行性

**原文链接**: https://opensource.actionsky.com/20201210-dble/
**分类**: 技术干货
**发布时间**: 2020-12-10T00:37:09-08:00

---

作者：鲍凤其
爱可生 dble 团队开发成员，主要负责 dble 需求开发，故障排查和社区问题解答。少说废话，放码过来。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**背景**
MySQL JDBC 在执行查询语句时，默认把查询的所有结果全部取回放在内存中，如果遍历很大的表，则可能把内存撑爆。
办法 1
查询语句中使用 limit，offset；这样我们会发现取数据的越来越慢，原因是在设置了 offset 之后，MySQL 需要将读取位置移动到 offset 的位置，随着 offset 增大，取数据也越来越慢；
办法 2
用数据流的方式取数据，可以指定 fetch size，这样每次获取指定数量的数据行，从而避免 OOM。此种方式的使用方式和原理可以参见文章：prepare statement 协议
第 2 种方式实际是 MySQL 中的 server-side 游标，server-side 游标是使用 MySQL 内部临时表来实现的。初始的时候，内部临时表是个内存表，当这个表的大小超过  max_heap_table_size and tmp_table_size 两个系统变量的最小值的时候（两者的最小值），会被转换成 MyISAM 表，即落盘存储。
内部临时表的使用限制同样适用于游标的内部临时表。
**MySQL 中的两种临时表**
外部临时表用户通过 CREATE TEMPORARY TABLE 语句显式创建的临时表，这样的临时表称为**外部临时表**。外部临时表生命周期：创建后，只在当前会话中可见，当前会话结束的时候，该临时表也会被自动关闭。因此，两个会话可以存在同名的临时表，但若有同名的非临时表时，直到临时表被删除，这张表对用户是不可见的。
内部临时表
内部临时表是一种特殊轻量级的临时表，用来进行性能优化。这种临时表会被 MySQL 自动创建并用来存储某些操作的中间结果。这些操作可能包括在优化阶段或者执行阶段。这种内部表对用户来说是不可见的，但是通过 EXPLAIN 或者 SHOW STATUS 可以查看 MySQL 是否使用了内部临时表用来帮助完成某个操作。内部临时表在 SQL 语句的优化过程中扮演着非常重要的角色，MySQL 中的很多操作都要依赖于内部临时表来进行优化。但是使用内部临时表需要创建表以及中间数据的存取代价，所以用户在写 SQL 语句的时候应该尽量的去避免使用临时表。
内部临时表有两种类型
**1、HEAP 临时表**这种临时表的所有数据都会存在内存中，对于这种表的操作不需要 IO 操作。**2、OnDisk 临时表**顾名思义，这种临时表会将数据存储在磁盘上。OnDisk 临时表用来处理中间结果比较大的操作。如果 HEAP 临时表存储的数据大于 MAX_HEAP_TABLE_SIZE（参数参考链接），HEAP 临时表会被自动转换成 OnDisk 临时表。OnDisk 临时表在 5.7 中可以通过 INTERNAL_TMP_DISK_STORAGE_ENGINE 系统变量选择使用 MyISAM 引擎或者 InnoDB 引擎。
临时表的参数
**max_heap_table_size**用户创建 Memory 表允许的最大 size，这个值和 tmp_table_size 一起使用，限制内部临时表在内存中的大小。**tmp_table_size**内部临时内存表大小的最大值，不适用于用户自己创建的 Memory 表
MySQL 中没有找到限制临时表磁盘文件大小的参数。
**DBLE 中的设计**
DBLE 中可参考 MySQL 的临时表的实现，指定一个类似  MAX_HEAP_TABLE_SIZE 的参数。小于这个数值，存放在内存中直接存取，一旦达到这个阈值，同样落盘处理。> 官方文档：
https://dev.mysql.com/doc/refman/5.7/en/cursors.html
https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_tmp_table_size
https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_heap_table_size
相关推荐：
[分布式 | DBLE 分片算法之 hash 分片](https://opensource.actionsky.com/20201102-dble/)
[分布式 | Global 表 Left Join 拆分表实现原因探究](https://opensource.actionsky.com/20200629-dble/)
[分布式 | DBLE 之通过 explain 进行 SQL 优化](https://opensource.actionsky.com/20200616-dble/)