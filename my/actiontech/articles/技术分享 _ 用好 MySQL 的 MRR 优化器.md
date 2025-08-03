# 技术分享 | 用好 MySQL 的 MRR 优化器

**原文链接**: https://opensource.actionsky.com/20200616-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-06-16T00:33:38-08:00

---

作者：蒋乐兴
MySQL DBA，擅长 python 和 SQL，目前维护着 github 的两个开源项目：mysqltools 、dbmc 以及独立博客：https://www.sqlpy.com。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**MRR 要解决的问题**
MRR 是 MySQL 针对特定查询的一种优化手段。假设一个查询有二级索引可用，读完二级索引后要回表才能查到那些不在当前二级索引上的列值，由于二级索引上引用的主键值不一定是有序的，因此就有可能造成大量的随机 IO，如果回表前把主键值给它排一下序，那么在回表的时候就可以用顺序 IO 取代原本的随机 IO。
## 环境准备
为了实验我们要准备一下表结构和数据。- `-- 创建表`
- `mysql> show create table t;`
- `+----------------------------------------------------------------------+`
- `| Table | Create Table                                                                                                                                                                                                                                                                                                                                                                               |`
- `+----------------------------------------------------------------------+`
- `| t     | CREATE TABLE `t` (`
- `  `id` int NOT NULL AUTO_INCREMENT,`
- `  `i0` int NOT NULL,`
- `  `i1` int NOT NULL,`
- `  `i2` int NOT NULL,`
- `  `i3` int NOT NULL,`
- `  `c0` varchar(128) NOT NULL,`
- `  `c1` varchar(128) NOT NULL,`
- `  `f0` float NOT NULL,`
- `  `f1` float NOT NULL,`
- `  PRIMARY KEY (`id`),`
- `  KEY `idx_i0` (`i0`)`
- `) ENGINE=InnoDB`
- `+----------------------------------------------------------------------+`
- `1 row in set (0.00 sec)`
- 
- `-- 造数据`
- `mysql> select count(*) from t;`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|  1120000 |`
- `+----------+`
- `1 row in set (0.77 sec)`
- 
- `--`
- `update t set i0 = id % 100;`
**MRR 的优化效果**
1. 有 MRR 优化（Using MRR）时 SQL 的耗时情况。
- `mysql> explain select i0,i3 from t where i0 between 1 and 2;`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+-------+----------+----------------------------------+`
- `| id | select_type | table | partitions | type  | possible_keys | key    | key_len | ref  | rows  | filtered | Extra                            |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+-------+----------+----------------------------------+`
- `|  1 | SIMPLE      | t     | NULL       | range | idx_i0        | idx_i0 | 4       | NULL | 43968 |   100.00 | Using index condition; Using MRR |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+-------+----------+----------------------------------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql> select i0,i3 from t where i0 between 1 and 2;`
- `22400 rows in set (0.80 sec)`
2. 关闭 MRR 优化。
- `set optimizer_switch = 'index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=off,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on';`
- 
- `mysql> explain select i0,i3 from t where i0 between 1 and 2;`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+-------+----------+-----------------------+`
- `| id | select_type | table | partitions | type  | possible_keys | key    | key_len | ref  | rows  | filtered | Extra                 |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+-------+----------+-----------------------+`
- `|  1 | SIMPLE      | t     | NULL       | range | idx_i0        | idx_i0 | 4       | NULL | 43968 |   100.00 | Using index condition |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+-------+----------+-----------------------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql> select i0,i3 from t where i0 between 1 and 2;`
- `22400 rows in set (2.56 sec)****`
> ******结论**就刚才的测试场景开启 MRR 优化可以得到 3 倍的性能提升。
## MRR 的优化器参数调整
如果想关闭 MRR 优化的话，就要把优化器开关 mrr 设置为 off。
默认只有在优化器认为 MRR 可以带来优化的情况下才会走 MRR，如果你想不管什么时候能走 MRR 的都走 MRR 的话，你要把 mrr_cost_based 设置为 off，不过最好不要这么干，因为这确实是一个坑，MRR 不一定什么时候都好，全表扫描有时候会更加快，如果在这种场景下走 MRR 就完成了。
开启 MRR 关闭基于开销的优化。
- `-- mrr=on,mrr_cost_based=off`
- `set optimizer_switch = 'index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on';`
- 
- `mysql> explain select i0,i3 from t where i0 between 1 and  10;`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+--------+----------+----------------------------------+`
- `| id | select_type | table | partitions | type  | possible_keys | key    | key_len | ref  | rows   | filtered | Extra                            |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+--------+----------+----------------------------------+`
- `|  1 | SIMPLE      | t     | NULL       | range | idx_i0        | idx_i0 | 4       | NULL | 218492 |   100.00 | Using index condition; Using MRR |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+--------+----------+----------------------------------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `select i0,i3 from t where i0 between 1 and  10;`
- `112000 rows in set (4.86 sec)`
开启 MRR 开启基于开销的优化。
- `-- mrr=on,mrr_cost_based=on`
- `set optimizer_switch = 'index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on';`
- 
- `mysql> explain select i0,i3 from t where i0 between 1 and  10;`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+`
- `| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows    | filtered | Extra       |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+`
- `|  1 | SIMPLE      | t     | NULL       | ALL  | idx_i0        | NULL | NULL    | NULL | 1121902 |    19.48 | Using where |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+`
- `1 row in set, 1 warning (0.00 sec)`
- 
- `mysql> select i0,i3 from t where i0 between 1 and  10;`
- `112000 rows in set (1.52 sec)`
可以看到当 mrr_cost_based = OFF 的情况下用时 4.86s，mrr_cost_based = ON 的情况下用时 1.52s，总的来说 mrr_cost_based 是非常关键的建议始终打开。
## MRR 的参数优化
MRR 要把主键排个序，这样之后对磁盘的操作就是由顺序读代替之前的随机读。从资源的使用情况上来看就是让 CPU 和内存多做点事，来换磁盘的顺序读。然而排序是需要内存的，这块内存的大小就由参数 read_rnd_buffer_size 来控制。
read_rnd_buffer_size 太小无法启用 MRR 功能。
- `mysql> select @@read_rnd_buffer_size;`
- `+------------------------+`
- `| @@read_rnd_buffer_size |`
- `+------------------------+`
- `|                 262144 |`
- `+------------------------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> explain select i0,i3 from t where i0 between 1 and  12;`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+`
- `| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows    | filtered | Extra       |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+`
- `|  1 | SIMPLE      | t     | NULL       | ALL  | idx_i0        | NULL | NULL    | NULL | 1121902 |    23.57 | Using where |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+---------+----------+-------------+`
- `1 row in set, 1 warning (0.00 sec)`
放大 read_rnd_buffer_size 让 MySQL 有足够的资源用于 MRR 。
- `mysql> set read_rnd_buffer_size = 32 * 1024 * 1024;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> explain select i0,i3 from t where i0 between 1 and  12;`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+--------+----------+----------------------------------+`
- `| id | select_type | table | partitions | type  | possible_keys | key    | key_len | ref  | rows   | filtered | Extra                            |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+--------+----------+----------------------------------+`
- `|  1 | SIMPLE      | t     | NULL       | range | idx_i0        | idx_i0 | 4       | NULL | 264436 |   100.00 | Using index condition; Using MRR |`
- `+----+-------------+-------+------------+-------+---------------+--------+---------+------+--------+----------+----------------------------------+`
- `1 row in set, 1 warning (0.00 sec)`