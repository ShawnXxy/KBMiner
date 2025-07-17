# 技术分享 | MySQL 碎片问题

**原文链接**: https://opensource.actionsky.com/20190708-mysql-optimize/
**分类**: MySQL 新特性
**发布时间**: 2019-07-08T00:07:30-08:00

---

MySQL 的碎片是 MySQL 运维过程中比较常见的问题，碎片的存在十分影响数据库的性能，本文将对 MySQL 碎片进行一次讲解。
**判断方法：**
MySQL 的碎片是否产生，通过查看
show table status from db_name\G; 
这个命令中 Data_free 字段，如果该字段不为 0，则产生了数据碎片。
**产生的原因：**
**1. 经常进行 delete 操作**
经常进行 delete 操作，产生空白空间，如果进行新的插入操作，MySQL将尝试利用这些留空的区域，但仍然无法将其彻底占用，久而久之就产生了碎片；
**演示：**
创建一张表，往里面插入数据，进行一个带有 where 条件或者 limit 的 delete 操作，删除前后对比一下 Data_free 的变化。
删除前：
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图1.png)											
删除后：
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图2.png)											
Data_free 不为 0，说明有碎片；
**2. update 更新**
update 更新可变长度的字段(例如 varchar 类型)，将长的字符串更新成短的。之前存储的内容长，后来存储是短的，即使后来插入新数据，那么有一些空白区域还是没能有效利用的。
**演示：**
创建一张表，往里面插入一条数据，进行一个 update 操作，前后对比一下 Data_free 的变化。
CREATE TABLE `t1` ( `k` varchar(3000) DEFAULT NULL ) ENGINE=MyISAM DEFAULT CHARSET=utf8; 
更新语句：update t1 set k=&#8217;aaa&#8217;;
更新前长度：223 Data_free：0
更新后长度：3 Data_free：204
Data_free 不为 0，说明有碎片；
**产生影响：**
1. 由于碎片空间是不连续的，导致这些空间不能充分被利用；
2. 由于碎片的存在，导致数据库的磁盘 I/O 操作变成离散随机读写，加重了磁盘 I/O 的负担。
**清理办法：**
- MyISAM：optimize table 表名；（OPTIMIZE 可以整理数据文件,并重排索引）
- Innodb：
1. ALTER TABLE tablename ENGINE=InnoDB；(重建表存储引擎，重新组织数据) 
2. 进行一次数据的导入导出
**碎片清理的性能对比：**
引用我之前一个生产库的数据，对比一下清理前后的差异。
**空间对比：**
| 库名 | 清理前大小 | 清理后大小 |
| --- | --- | --- |
| facebook | 2.2G | 1.1G |
| instagram | 40G | 22G |
| linkedin | 555M | 208M |
| googleplus | 19G | 8.4G |
| twitter | 107G | 44G |
SQL执行速度：
select count(*) from test.twitter_11; 
修改前：1 row in set (7.37 sec)
修改后：1 row in set (1.28 sec)
**结论：**
通过对比，可以看到碎片清理前后，节省了很多空间，SQL执行效率更快。所以，**在日常运维工作中，应对碎片进行定期清理，保证数据库有稳定的性能。**
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)