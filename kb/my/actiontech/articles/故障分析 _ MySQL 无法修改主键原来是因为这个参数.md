# 故障分析 | MySQL 无法修改主键？原来是因为这个参数

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-mysql-%e6%97%a0%e6%b3%95%e4%bf%ae%e6%94%b9%e4%b8%bb%e9%94%ae%ef%bc%9f%e5%8e%9f%e6%9d%a5%e6%98%af%e5%9b%a0%e4%b8%ba%e8%bf%99%e4%b8%aa%e5%8f%82%e6%95%b0/
**分类**: MySQL 新特性
**发布时间**: 2024-01-23T21:17:44-08:00

---

同事咨询了一个问题，TDSQL（for MySQL）中的某张表主键需要改为联合主键，是否必须先删除现有的主键？因为删除主键时，提示这个错误。
> 
作者：刘晨，网名 bisal ，具有十年以上的应用运维工作经验，目前主要从事数据库应用研发能力提升和技术管理相关的工作，Oracle ACE（Alumni），腾讯云TVP，拥有 Oracle OCM & OCP 、EXIN DevOps Master 、SCJP 等国际认证，国内首批 Oracle YEP 成员，OCMU 成员，《DevOps 最佳实践》中文译者之一，CSDN & ITPub 专家博主，公众号”bisal的个人杂货铺”，长期坚持分享技术文章，多次在线上和线下分享技术主题。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 800 字，预计阅读需要 2 分钟。
# 问题背景
同事咨询了一个问题，TDSQL（for MySQL）中的某张表主键需要改为联合主键，是否必须先删除现有的主键？因为删除主键时，提示这个错误。
`[test]> alter table test drop primary key;
ERROR 3750 (HY000): Unable to create or change a table without a primary key, 
when the system variable 'sql_require_primary_key' is set. 
Add a primary key to the table or unset this variable to avoid this message. 
Note that tables without a primary key can cause performance problems in row-based replication, 
so please consult your DBA before changing this setting.
`
# 问题分析
从提示上可以看到具体的原因，当设置了 *sql_require_primary_key* 参数，不能创建或改变一张没有主键的表。解决方案是增加主键或者删除此参数避免错误，同时提醒了，如果表无主键，可能会导致基于行的复制产生性能问题。
*sql_require_primary_key* 参数控制的是强制检查主键，可以动态修改。
`参数名称：sql_require_primary_key
作用范围：Global & Session
动态修改：Yes
默认值：OFF
该参数设置为ON时，SQL语句create table创建新表或者alter语句对已存在的表进行修改，将会强制检查表中是否包含主键，如果没有主键，则会报错。
`
**针对这个场景，是否还可以将主键改为联合主键？**
创建一张测试表，主键初始是 `id`。
`bisal@mysqldb:  [test]> create table t_primary_key (id int, c1 varchar(1), c2 varchar(1), constraint pk_t_id primary key(id));
Query OK, 0 rows affected (0.07 sec)
`
# 解决方案
## 方案一
既然 *sql_require_primary_key* 参数控制了强制检验主键，而且又是可动态修改的，临时关闭，再打开即可。
`bisal@mysqldb:  [test]> alter table t_primary_key drop primary key;
ERROR 3750 (HY000): Unable to create or change a table without a primary key, when the system variable 'sql_require_primary_key' is set. Add a primary key to the table or unset this variable to avo
bisal@mysqldb:  [(none)]> show variables like '%sql_require%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| sql_require_primary_key | OFF   |
+-------------------------+-------+
1 row in set (0.00 sec)
bisal@mysqldb:  [(none)]> set sql_require_primary_key = ON;
Query OK, 0 rows affected (0.02 sec)
bisal@mysqldb:  [(none)]> show variables like '%sql_require%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| sql_require_primary_key | ON    |
+-------------------------+-------+
1 row in set (0.00 sec)
bisal@mysqldb:  [test]> alter table t_primary_key drop primary key;
Query OK, 0 rows affected (0.10 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
但可能的风险，就是删除主键，再创建主键的这段时间内，如果有主键字段的重复数据插入，就可能导致创建新的主键不成功。另外，鉴于该参数设置成为非默认值，创建完主键，需要记得改过来。
## 方案二
如果 *sql_require_primary_key* 设置为 **ON**，意思就是表任何的时刻都需要有主键，不能出现真空。变更主键的操作，实际包含了删除原主键和创建新的主键两个步骤，因此只需要将两个步骤合并成一个即可。
MySQL 支持多个语句一次执行，因此只需要将 `alter table ... drop primary key` 和 `add constraint ... primary key ...` 合成一条语句。
`bisal@mysqldb:  [test]> alter table t_primary_key drop primary key, add constraint pk_t_01 primary key (id, c1);
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0
`
# 总结
从这个问题可以看出来，MySQL 的参数控制粒度很细，但通过各种应对方法，可以针对性解决特定的场景问题，但前提还是对参数的意义，以及场景的需求能充分了解，才能找到合适的解决方案。