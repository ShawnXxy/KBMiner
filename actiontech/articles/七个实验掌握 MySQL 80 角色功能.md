# 七个实验掌握 MySQL 8.0 角色功能

**原文链接**: https://opensource.actionsky.com/20200318-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-03-18T02:06:11-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
角色一直存在各个数据库中，比如 SQL Server、Oracle 等，MySQL 自从版本 8.0 release，引入了角色这个概念。
**角色的概念**
角色就是一组针对各种数据库权限的集合。
比如，把一个角色分配给一个用户，那这个用户就拥有了这个角色包含的所有权限。一个角色可以分配给多个用户，另外一个用户也可以拥有多个角色，**两者是多对多的关系**。不过 MySQL 角色目前还没有提供类似于其他数据库的系统预分配的角色。比如某些数据库的 db_owner、 db_datareader 、 db_datawriter 等等。那接下来我分几个方面，来示例说明角色的使用以及相关注意事项。
示例 1：一个完整角色的授予步骤
用管理员创建三个角色：db_owner, db_datareader, db_datawriter- `mysql> create role db_owner,db_datareader,db_datawriter;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `mysql> grant all on ytt_new.* to db_owner;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> grant select on ytt_new.* to db_datareader;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> grant insert,delete,update on ytt_new.* to db_datawriter;`
- `Query OK, 0 rows affected (0.01 sec)`
创建三个普通用户，分别为 ytt1、ytt2、ytt3。- `mysql> create user ytt1 identified by 'ytt',ytt2 identified by 'ytt',ytt3 identified by 'ytt';`
- `Query OK, 0 rows affected (0.01 sec)`
分别授予这三个用户对应的角色。- `-- 授权角色`
- `mysql> grant db_owner to ytt1;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `-- 激活角色`
- `mysql> set default role db_owner to ytt1;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> grant db_datareader to ytt2;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> set default role db_datareader to ytt2;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> grant db_datawriter to ytt3;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> set default role db_datawriter to ytt3;`
- `Query OK, 0 rows affected (0.01 sec)`
以上是角色授予的一套完整步骤。那上面有点非常规的地方是激活角色这个步骤。MySQL 角色在创建之初默认是没有激活的，也就是说创建角色，并且给一个用户特定的角色，这个用户其实并不能直接使用这个角色，除非激活了才可以。
示例 2：一个用户可以拥有多个角色
- `-- 用管理员登录并且创建用户`
- `mysql> create user ytt4 identified by 'ytt';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `-- 把之前的三个角色都分配给用户ytt4.`
- `mysql> grant db_owner,db_datareader,db_datawriter to ytt4;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 激活用户ytt4的所有角色.`
- `mysql> set default role all to ytt4;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `-- ytt4 用户登录`
- `root@ytt-pc:/var/lib/mysql# mysql -uytt4 -pytt -P3304 -hytt-pc`
- `...`
- 
- `-- 查看当前角色列表`
- `mysql> select current_role();`
- `+--------------------------------------------------------+`
- `| current_role()                                         |`
- `+--------------------------------------------------------+`
- `| `db_datareader`@`%`,`db_datawriter`@`%`,`db_owner`@`%` |`
- `+--------------------------------------------------------+`
- `1 row in set (0.00 sec)`
- 
- `-- 简单创建一张表并且插入记录， 检索记录，完了删掉这张表`
- 
- `mysql> use ytt_new`
- `Database changed`
- `mysql> create table t11(id int);`
- `Query OK, 0 rows affected (0.05 sec)`
- 
- `mysql> insert into t11 values (1);`
- `Query OK, 1 row affected (0.02 sec)`
- 
- `mysql> select * from t11;`
- `+------+`
- `| id   |`
- `+------+`
- `|    1 |`
- `+------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> drop table t11;`
- `Query OK, 0 rows affected (0.04 sec)`
示例 3：用户在当前 session 里角色互换其实意思是说，用户连接到 MySQL 服务器后，可以切换当前的角色列表，比如由 db_owner 切换到 db_datareader。
- `-- 还是之前的用户ytt4, 切换到db_datareader`
- `mysql> set role db_datareader;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> select current_role();`
- `+---------------------+`
- `| current_role()      |`
- `+---------------------+`
- `| `db_datareader`@`%` |`
- `+---------------------+`
- `1 row in set (0.00 sec)`
- 
- `-- 切换后，没有权限创建表`
- `mysql> create table t11(id int);`
- `ERROR 1142 (42000): CREATE command denied to user 'ytt4'@'ytt-pc' for table 't11'`
- 
- 
- `-- 切换到 db_owner，恢复所有权限。`
- `mysql> set role db_owner;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> create table t11(id int);`
- `Query OK, 0 rows affected (0.04 sec)`
示例 4：关于角色的两个参数
activate_all_roles_on_login：是否在连接 MySQL 服务时自动激活角色mandatory_roles：强制所有用户默认角色- `-- 用管理员连接MySQL,`
- `-- 设置默认激活角色`
- `mysql> set global activate_all_roles_on_login=on;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `-- 设置强制给所有用户赋予角色db_datareader`
- `mysql> set global mandatory_roles='db_datareader';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `-- 创建用户ytt7.`
- `mysql> create user ytt7;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 用 ytt7登录数据库`
- `root@ytt-pc:/var/lib/mysql# mysql -uytt7 -P3304 -hytt-pc`
- `...`
- 
- `mysql> show grants;`
- `+-------------------------------------------+`
- `| Grants for ytt7@%                         |`
- `+-------------------------------------------+`
- `| GRANT USAGE ON *.* TO `ytt7`@`%`          |`
- `| GRANT SELECT ON `ytt_new`.* TO `ytt7`@`%` |`
- `| GRANT `db_datareader`@`%` TO `ytt7`@`%`   |`
- `+-------------------------------------------+`
- `3 rows in set (0.00 sec)`
示例 5 ：create role 和 create user 都有创建角色权限，两者有啥区别？
以下分别创建两个用户 ytt8、ytt9，一个给 create role，一个给 create user 权限。- `-- 管理员登录，创建用户ytt8,ytt9.`
- `mysql> create user ytt8,ytt9;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> grant create role on *.* to ytt8;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `mysql> grant create user on *.* to ytt9;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 用ytt8 登录，`
- `root@ytt-pc:/var/lib/mysql# mysql -uytt8 -P3304 -hytt-pc`
- `...`
- 
- `mysql> create role db_test;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `-- 可以创建角色，但是不能创建用户`
- `mysql> create user ytt10;`
- `ERROR 1227 (42000): Access denied; you need (at least one of) the CREATE USER privilege(s) for this operation`
- `mysql> \q`
- `Bye`
- 
- `-- 用ytt9 登录`
- `root@ytt-pc:/var/lib/mysql# mysql -uytt9 -P3304 -hytt-pc`
- `...`
- 
- `-- 角色和用户都能创建`
- `mysql> create role db_test2;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `mysql> create user ytt10;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> \q`
- `Bye`
那这里其实看到 create user 包含了 create role，create user 即可以创建用户，也可以创建角色。
示例 6：MySQL 用户也可以当角色来用
- `-- 用管理员登录，创建用户ytt11,ytt12.`
- `mysql> create user ytt11,ytt12;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> grant select on ytt_new.* to ytt11;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 把ytt11普通用户的权限授予给ytt12`
- `mysql> grant ytt11 to ytt12;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 来查看 ytt12的权限，可以看到拥有了ytt11的权限`
- `mysql> show grants for ytt12;`
- `+-----------------------------------+`
- `| Grants for ytt12@%                |`
- `+-----------------------------------+`
- `| GRANT USAGE ON *.* TO `ytt12`@`%` |`
- `| GRANT `ytt11`@`%` TO `ytt12`@`%`  |`
- `+-----------------------------------+`
- `2 rows in set (0.00 sec)`
- 
- `-- 在细化点，看看ytt12拥有哪些具体的权限`
- `mysql> show grants for ytt12 using ytt11;`
- `+--------------------------------------------+`
- `| Grants for ytt12@%                         |`
- `+--------------------------------------------+`
- `| GRANT USAGE ON *.* TO `ytt12`@`%`          |`
- `| GRANT SELECT ON `ytt_new`.* TO `ytt12`@`%` |`
- `| GRANT `ytt11`@`%` TO `ytt12`@`%`           |`
- `+--------------------------------------------+`
- `3 rows in set (0.00 sec)`
示例 7：角色的撤销
角色撤销和之前权限撤销类似。要么 revoke，要么删除角色，那这个角色会从所有拥有它的用户上移除。- `-- 用管理员登录，移除ytt2的角色`
- `mysql> revoke db_datareader from ytt2;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 删除所有角色`
- `mysql> drop role db_owner,db_datareader,db_datawriter;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `-- 对应的角色也从ytt1上移除掉了`
- `mysql> show grants for ytt1;`
- `+----------------------------------+`
- `| Grants for ytt1@%                |`
- `+----------------------------------+`
- `| GRANT USAGE ON *.* TO `ytt1`@`%` |`
- `+----------------------------------+`
- `1 row in set (0.00 sec)`
至此，我分了 7 个目录说明了角色在各个方面的使用以及注意事项，希望对大家有帮助。