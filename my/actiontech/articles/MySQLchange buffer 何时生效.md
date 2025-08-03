# MySQL：change buffer 何时生效

**原文链接**: https://opensource.actionsky.com/20220121-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-01-24T00:25:28-08:00

---

作者：胡呈清
爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：https://www.jianshu.com/u/a95ec11f67a8，欢迎讨论。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
已知 change buffer 的原理
参考资料：https://juejin.im/post/6844903875271475213
对于普通二级索引，当插入、修改、删除二级索引记录时，即使数据不在 innodb buffer pool 中，也不需要先把数据从磁盘读取到内存。只需要在 change buffer 中完成 DML 操作，下次读取时才会从磁盘读取数据页到内存，并与 change buffer 进行 merge，从而得到正确的数据。这减少了 DML 时的随机 IO。
## 疑问
按照上述原理，使用 change buffer 二级索引不需要读取磁盘，那 delete、update 是如何得到 affected rows 的？
## 答
不妨先作出假设：
- 
如果 delete、update 是以主键、唯一索引做为筛选条件，则读取磁盘或者 innodb buffer pool 中的主键、唯一索引来确定 affected rows。对于普通索引页上记录的删除或者修改，还是直接使用 change buffer，不需要单独将普通索引页从磁盘上读取到内存。
- 
如果 delete、update 是以普通二级索引做为筛选条件，以 delete 为例（update 内部实现是先 delete 再 insert）：delete from t where a=100; 如果索引页不在内存中，则需要先从磁盘读取 a 索引，找到 a = 100 的记录对应的 id（主键值），再从磁盘扫描主键索引（回表）将 id 满足条件的记录读取到内存。然后在 innodb buffer pool 中把对应的主键索引页、二级索引页中的记录删除。这里不使用 change buffer。
## 验证
接下来设计两个实验来验证上述假设。
#### 实验1-以主键为筛选条件做 delete
用 sysbench 造一张 100 万行的表，表中有一个主键和一个普通索引：
`CREATE TABLE `sbtest1` (
`id` int NOT NULL AUTO_INCREMENT,
`k` int NOT NULL DEFAULT '0',
`c` char(120) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
`pad` char(60) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_2` (`k`)
);
`
重启 mysqld ，清空 innodb buffer pool，注意参数：
`innodb_buffer_pool_size = 64M
innodb_buffer_pool_load_at_startup = 0
innodb_buffer_pool_dump_at_shutdown = 0
innodb_buffer_pool_dump_pct = 0
`
执行 delete，并使用`show engine innodb status\G`观察`INSERT BUFFER AND ADAPTIVE HASH INDEX` 部分信息，判断是否使用 change buffer：
`mysql> delete from sbtest1 where id=1;
Query OK, 1 row affected (0.00 sec)
mysql> show engine innodb status\G
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 29, seg size 31, 1 merges
merged operations:
insert 0, delete mark 1, delete 0
discarded operations:
insert 0, delete mark 0, delete 0
mysql> delete from sbtest1 where id=2;
Query OK, 1 row affected (0.00 sec)
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 29, seg size 31, 2 merges
merged operations:
insert 0, delete mark 2, delete 0
discarded operations:
insert 0, delete mark 0, delete 0
mysql> delete from sbtest1 where id=3;
Query OK, 1 row affected (0.00 sec) 
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 29, seg size 31, 3 merges
merged operations:
insert 0, delete mark 3, delete 0
discarded operations:
insert 0, delete mark 0, delete 0
mysql> select * from sbtest1 where id=4;
mysql> delete from sbtest1 where id=4;
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 29, seg size 31, 4 merges
merged operations:
insert 0, delete mark 4, delete 0
discarded operations:
insert 0, delete mark 0, delete 0
`
上述实验说明：如果 delete 是以主键做为筛选条件，对于普通索引k，如果索引页不在内存中（select * from sbtest1 where id=4 读取的只是主键索引页，不会读取k索引页），会使用 change buffer（每次 delete 后，delete mark 都增加1）。
#### 实验2-以普通索引为筛选条件做 delete
重新造数据，重启 mysqld 清空 buffer pool。下面实验结果说明：如果 delete 以普通索引做为筛选条件，对于普通索引k，如果索引页不在内存中，不会使用 change buffer。言外之意就是需要读取磁盘了。
`##delete where id=1，delete mark +1，说明使用了change buffer
mysql>  delete from sbtest1 where id=1;
Query OK, 1 row affected (0.01 sec)
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 29, seg size 31, 1 merges
merged operations:
insert 0, delete mark 1, delete 0
discarded operations:
insert 0, delete mark 0, delete 0
##delete where k=367246，delete mark 不变，说明没有使用change buffer
mysql> select * from sbtest1 where id=2;
+----+--------+-------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+
| id | k      | c                                                                                                                       | pad                                                         |
+----+--------+-------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+
|  2 | 367246 | 42909700340-70078987867-62357124096-35495169193-85675377266-14643719347-30417020186-80900182681-50382374444-66260611196 | 74781290517-41121402981-50604677924-34464478849-89102349959 |
+----+--------+-------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> delete from sbtest1 where k=367246;
Query OK, 1 row affected (0.01 sec)
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 29, seg size 31, 1 merges
merged operations:
insert 0, delete mark 1, delete 0
discarded operations:
insert 0, delete mark 0, delete 0
`