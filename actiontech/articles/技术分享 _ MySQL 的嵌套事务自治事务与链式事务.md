# 技术分享 | MySQL 的嵌套事务、自治事务与链式事务

**原文链接**: https://opensource.actionsky.com/20191218-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-12-18T00:27:58-08:00

---

这篇文章有感于最近支持某客户从 Oracle 迁移到 MySQL 过程中的启示。接下来我们**详细说明 MySQL 中的事务种类。**
**分类**
1. 普通事务以 begin / start transaction 开始，commit / rollback 结束的事务。或者是带有保存点 savepoint 的事务。
2. 链式事务
一个事务在提交的时候自动将上下文传给下一个事务，也就是说一个事务的提交和下一个事务的开始是原子性的，下一个事务可以看到上一个事务的处理结果。MySQL 的链式事务靠参数 completion_type 控制，并且回滚和提交的语句后面加上 work 关键词。
3. 嵌套事务
有多个 begin / commit / rollback 这样的事务块的事务，并且有父子关系。子事务的提交完成后不会真的提交，而是等到父事务提交才真正的提交。
4. 自治事务
内部事务的提交不随外部事务的影响，一般用作记录内部事务的异常情况。MySQL 不支持自治事务，但是某些场景可以用 MySQL 的插件式引擎来变相实现。
接下来，我们每种事务用详细例子来说明。
**实例**
**1. 普通事务**下表 c1，开始一个事务块，有两个保存点 s1 & s2。我们回滚了 s2 之后的所有操作，并且提交了 s2 之前的所有操作，此时 s1 & s2 已经失效。那记录数刚好两条。- `{"db":"ytt"},"port":"3320"}-mysql>truncate c1;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>`
- `{"db":"ytt"},"port":"3320"}-mysql>`
- `{"db":"ytt"},"port":"3320"}-mysql>use ytt`
- `Database changed`
- `{"db":"ytt"},"port":"3320"}-mysql>begin;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (1,20,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>savepoint s1;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (2,30,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>savepoint s2;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (3,40,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>rollback to savepoint s2;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>commit;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>select * from c1;`
- `+----+------+---------------------+`
- `| id | c1   | c2                  |`
- `+----+------+---------------------+`
- `|  1 |   20 | 2019-12-02 10:07:02 |`
- `|  2 |   30 | 2019-12-02 10:07:12 |`
- `+----+------+---------------------+`
- `2 rows in set (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>`
**2. 链式事务**
设置 completion_type=1，也就是开启了链式事务特征。下面例子，commit work 后的语句是一个隐式事务语句。也就是说语句 rollback 语句执行后，默认的话，sql 2 肯定已经提交了。但是由于继承了上下文，也就是语句 sql 2变为 `begin;SQL2;`　那此时 sql 2 和 rollback 语句其实是一个事务块儿了。最终结果就是只有两条记录。- `{"db":"ytt"},"port":"3320"}-mysql>truncate table c1;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>set completion_type=1;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (4,50,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (5,60,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `-- sql 1`
- `{"db":"ytt"},"port":"3320"}-mysql>commit work;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `-- sql 2`
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (6,70,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `-- sql 3`
- `{"db":"ytt"},"port":"3320"}-mysql>rollback;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>select * from c1;`
- `+----+------+---------------------+`
- `| id | c1   | c2                  |`
- `+----+------+---------------------+`
- `|  4 |   50 | 2019-12-02 10:14:16 |`
- `|  5 |   60 | 2019-12-02 10:14:31 |`
- `+----+------+---------------------+`
- `2 rows in set (0.00 sec)`
**3. 嵌套事务**
其实严格意义上来说，MySQL 是不支持嵌套事务的。MySQL 的每个事务块的开始默认的会提交掉之前的事务。比如下面的例子，第二个 begin 语句默认会变为 `commit;begin;` 那之后的 rollback 其实只回滚了一条记录。最终记录数为 ID=7 这条。- `{"db":"ytt"},"port":"3320"}-mysql>truncate table c1;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>begin;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (7,80,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>begin;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>insert into c1 values (8,90,now());`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>rollback;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3320"}-mysql>select * from c1;`
- `+----+------+---------------------+`
- `| id | c1   | c2                  |`
- `+----+------+---------------------+`
- `|  7 |   80 | 2019-12-02 10:24:44 |`
- `+----+------+---------------------+`
- `1 row in set (0.00 sec)`
**4. 自治事务**
其实 MySQL 本来不支持自治事务，但是基于 MySQL 先天的可插拔架构来说，也可以变相的实现自治事务。比如可以把记录日志的表变为非事务引擎表，比如 MyISAM。- `{"db":"(none)"},"port":"3326"}-mysql>use ytt`
- `Database changed`
- `{"db":"ytt"},"port":"3326"}-mysql>create table log(err_msg varchar(200))engine myisam;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3326"}-mysql>begin;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3326"}-mysql>insert into t1 values (100);`
- `Query OK, 1 row affected (0.01 sec)`
- 
- `{"db":"ytt"},"port":"3326"}-mysql>insert into log values ('这个记录不应该插入进来');`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3326"}-mysql>select * from t1;`
- `+------+`
- `| id   |`
- `+------+`
- `|  100 |`
- `+------+`
- `1 row in set (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3326"}-mysql>rollback;`
- `Query OK, 0 rows affected, 1 warning (0.00 sec)`
- 
- `{"db":"ytt"},"port":"3326"}-mysql>select * from log;`
- `+-----------------------------------+`
- `| err_msg                           |`
- `+-----------------------------------+`
- `| 这个记录不应该插入进来            |`
- `+-----------------------------------+`
- `1 row in set (0.00 sec)`
**总结**
本篇内容主要把 MySQL 的事务类别简单介绍了下，针对了日常使用的几种场景做了简单的 SQL 演示，希望对大家有帮助。
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
技术交流群，进群后可提问
QQ群（669663113）
社区通道，邮件&电话
osc@actionsky.com
现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
格式：.md/.doc/.txt
主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
要求：原创且未发布过
奖励：作者署名；200元京东E卡+社区周边
投稿方式：
邮箱：osc@actionsky.com
格式：[投稿]姓名+文章标题
以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系