# 故障分析 | 当 USAGE 碰到 GRANT OPTION

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-%e5%bd%93-usage-%e7%a2%b0%e5%88%b0-grant-option/
**分类**: 技术干货
**发布时间**: 2023-07-18T22:34:45-08:00

---

本文分享的是 MySQL 中权限搭配使用不当时可能引发的问题。
> 作者：佟宇航
爱可生南区交付服务部 DBA 团队成员，主要负责 MySQL 故障处理以及平台技术支持。
本文来源：原创投稿
- 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# 背景
近期客户反应数据库有些诡异，原本应该有部分库表访问权限的 MySQL 用户，现在可以看到权限外的一些库表信息。
猜测可能是权限设置有冲突，先了解一下客户环境的权限：
`mysql> show grants;
+------------------------------------------------------------------------+
| Grants for ttt@%                                                       |
+------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'ttt'@'%'                                        |
| GRANT USAGE ON `austin`.* TO 'ttt'@'%' WITH GRANT OPTION               |
| GRANT USAGE ON `file`.* TO 'ttt'@'%' WITH GRANT OPTION                 |
| GRANT ALL PRIVILEGES ON `redmoonoa9`.* TO 'ttt'@'%' WITH GRANT OPTION  |
| GRANT ALL PRIVILEGES ON `nacos`.* TO 'ttt'@'%' WITH GRANT OPTION       |
| GRANT ALL PRIVILEGES ON `data_center`.* TO 'ttt'@'%' WITH GRANT OPTION |
| GRANT ALL PRIVILEGES ON `xxl_job`.* TO 'ttt'@'%' WITH GRANT OPTION     |
+------------------------------------------------------------------------+
7 rows in set (0.01 sec)
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| austin             |
| data_center        |
| file               |
| nacos              |
| redmoonoa9         |
| xxl_job            |
+--------------------+
7 rows in set (0.00 sec)
`
在分析问题之前，先简单介绍一下 MySQL 权限相关的知识点。
# 权限介绍
众所周知，MySQL 的权限有很多钟，权限又可以分为全局权限（即整个数据库）和特定权限（即特定库表），并且同一用户可以具备多种权限，部分常用权限如下表：
| 权限 | 说明 |
| --- | --- |
| ALL | 代表 **所有** 权限（相反与 USAGE） |
| ALTER | 代表允许使用 **ALTER TABLE** 来改变表结构，ALTER TABLE 同时也需要有 CREATE 和 INSERT 权限 |
| CREATE | 代表允许创建新的数据库和表 |
| DROP | 代表允许删除数据库、表、视图 |
| SELECT | 代表允许从数据库中查询表数据 |
| INSERT | 代表允许向数据库中插入表数据 |
| UPDATE | 代表允许更新数据库中的表数据 |
| DELETE | 代表允许删除数据库中的表数据 |
| GRANT OPTION | 代表允许向其他用户授权或移除权限 |
| USAGE | 代表 **没有任何权限**（相反于 ALL） |
查看客户环境权限后，初步判断大概率是因为该用户对一个数据库同时具备 USAGE 和 GRANT OPTION 权限导致。
# 本地测试
当用户同时拥有 UASGE 和 GRANT OPTION 权限时会发生什么？
## 准备环境
创建一个用户对 `test` 库下所有表具有查询权限。
`mysql> show grants;
+---------------------------------------------------------+
| Grants for hjm@%                                        |
+---------------------------------------------------------+
| GRANT USAGE ON *.* TO 'hjm'@'%'                         |
| GRANT SELECT ON `test`.* TO 'hjm'@'%' WITH GRANT OPTION |
+---------------------------------------------------------+
2 rows in set (0.00 sec)
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| test               |
+--------------------+
2 rows in set (0.00 sec)
mysql> use test
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
| t3             |
| y1             |
+----------------+
4 rows in set (0.00 sec)
mysql> select * from y1;
+------+------+
| id   | name |
+------+------+
|    1 | a    |
|    2 | b    |
+------+------+
2 rows in set (0.00 sec)
`
如上测试可以证明：
- 当用户只对库拥有 UASGE 权限时，对该权限下数据库没有任何权限，也无法查看，符合预期。
- 当用户只对库拥有 GRANT OPTION 权限时，结果表明也是一切正常，符合预期。
## 修改权限
对该用户新增权限，对 `test` 库既有 UASGE 权限也有 GRANT OPTION 权限。
先撤回 SELECT 权限。
`mysql> revoke SELECT ON `test`.* from 'hjm'@'%' ;
Query OK, 0 rows affected (0.00 sec)
mysql> show grants for hjm;
+--------------------------------------------------------+
| Grants for hjm@%                                       |
+--------------------------------------------------------+
| GRANT USAGE ON *.* TO 'hjm'@'%'                        |
| GRANT USAGE ON `test`.* TO 'hjm'@'%' WITH GRANT OPTION |
+--------------------------------------------------------+
2 rows in set (0.00 sec)
`
登录 `hjm` 用户查看。
`mysql> show grants;
+--------------------------------------------------------+
| Grants for hjm@%                                       |
+--------------------------------------------------------+
| GRANT USAGE ON *.* TO 'hjm'@'%'                        |
| GRANT USAGE ON `test`.* TO 'hjm'@'%' WITH GRANT OPTION |
+--------------------------------------------------------+
2 rows in set (0.01 sec)
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| test               |
+--------------------+
2 rows in set (0.00 sec)
mysql> use test;
Database changed
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
mysql> show create table t1;
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                       |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
`id` int(11) DEFAULT NULL,
`name` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> select * from t1;
ERROR 1142 (42000): SELECT command denied to user 'hjm'@'10.186.62.91' for table 't1'
`
无法查看表数据。
# 总结
当用户对同一数据库同时具备 `USAGE` 和 `GRANT  OPTION` 两种权限时，就会出现冲突。此时便可以查看到该数据库以及库下所有表的信息，但无法查看表内具体数据。
> 注意：在通过 `REVOKE` 回收权限时，若该用户同时具备 `WITH GRANT OPTION` 权限，一定要记得通过 `REVOKE GRANT OPTION` 语句进行收回，这样权限才能回收的干净彻底。