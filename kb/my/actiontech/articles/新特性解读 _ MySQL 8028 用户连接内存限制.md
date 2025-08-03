# 新特性解读 | MySQL 8.0.28 用户连接内存限制

**原文链接**: https://opensource.actionsky.com/20200303-mysql-2/
**分类**: MySQL 新特性
**发布时间**: 2022-03-02T22:09:32-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
以往 MySQL 想要限制单个连接的内存，只能小心翼翼的设置各种 SESSION 变量，防止执行某些 SQL 导致单个连接的内存溢出！ 能不能直接在 MySQL 服务端包含这样一个功能，简化数据库的运维呢？
MySQL 最新版本 8.0.28 在前几天发布，其中有一项新功能就是在数据库侧来限制单个连接内存，着实有点小兴奋。
##### MySQL 8.0.28 与此功能有关的几个新参数如下：
- 
**connection_memory_limit**：核心参数！用来限制单用户连接的内存上限值，默认为 BIGINT UNSIGNED 的最大值：18446744073709551615 字节，最小为2MB。
- 
**global_connection_memory_tracking**：设置是否开启对连接内存功能的追踪，并且把连接内存数据存入状态变量 **Global_connection_memory** 。为了性能考虑，默认关闭。
- 
**connection_memory_chunk_size**: 在参数 global_connection_memory_tracking 开启的场景下，设置状态变量 Global_connection_memory 的更新频率。
##### 接下来我们体验下这个新特性。
管理员端设置内存限制参数上限：为了尽快看到效果，设置为最小值。
`localhost:(none)>set global connection_memory_limit=2097152;
Query OK, 0 rows affected (0.00 sec)
`
创建一个新用户 tt1 ，并赋予基于库 ytt 的只读权限。
`localhost:(none)>create user tt1 identified by 'tt';
Query OK, 0 rows affected (0.03 sec)
localhost:(none)>grant select on ytt.* to tt1;
Query OK, 0 rows affected (0.02 sec)
`
创建一张表，插入一行记录： 这里使用 longtext 数据类型能让查询结果更快内存溢出。
`localhost:ytt>create table t(id int primary key, r1 longtext);
Query OK, 0 rows affected (2.39 sec)
localhost:ytt>insert t values (1,lpad('mysql',6000000,'database'));
Query OK, 1 row affected (0.63 sec)
`
用户 tt1 登录验证：对字段 r1 进行简单 GROUP BY 检索 ，**报连接内存超出设定限制错误，连接关闭。**
`debian-ytt1:ytt>select count(r1) from t group by r1;
ERROR 4082 (HY000): Connection closed. Connection memory limit 2097152 bytes exceeded. Consumed 7094928 bytes.
`
不过这个新功能对管理员和内置用户不生效。 用 ROOT 用户重新登录 MySQL 执行刚才那条 SQL ：
`root@debian-ytt1:~# mysql -S /tmp/mysqld_3306.sock
...
localhost:(none)>use ytt
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
localhost:ytt>select count(r1) from t group by r1;
+-----------+
| count(r1) |
+-----------+
|         1 |
+-----------+
1 row in set (0.03 sec)
`
##### 可以看到，管理员可以正常执行这条SQL。所以我们 DBA 给开发用户赋予权限时，为了避免不必要的运维工作，禁止赋 SUPER 权限。