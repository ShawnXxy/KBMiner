# 技术分享 | 控制mysqldump导出的SQL文件的事务大小

**原文链接**: https://opensource.actionsky.com/20190826-mysqldump/
**分类**: MySQL 新特性
**发布时间**: 2019-08-26T00:31:43-08:00

---

**背景******有人问mysqldump出来的insert语句，是否可以按每 10 row 一条insert语句的形式组织。
**思考1：****参数&#8211;extended-insert**********回忆过去所学：我只知道有一对参数
**&#8211;extended-insert(默认值)**表示使用长 INSERT ，多 row 在合并一起批量 INSERT，提高导入效率
**&#8211;skip-extended-insert**一行一个的短INSERT均不满足群友需求，无法控制按每 10 row 一条 insert 语句的形式组织。
**思考2：****“避免大事务”******之前一直没有考虑过这个问题。这个问题的提出，相信主要是为了“避免大事务”。所以满足 insert 均为小事务即可。下面，我们来探讨一下以下问题：1. 什么是大事务？2. 那么 mysqldump 出来的 insert 语句可能是大事务吗？
**什么是大事务？**- 定义：运行时间比较长，操作的数据比较多的事务我们称之为大事务。
- 大事务风险：
∘ 锁定太多的数据，造成大量的阻塞和锁超时，回滚所需要的时间比较长。
∘ 执行时间长，容易造成主从延迟。
∘ undo log膨胀
- 避免大事务：我这里按公司实际场景，规定了，每次操作/获取数据量应该少于5000条，结果集应该小于2M
**mysqldump出来的SQL文件有大事务吗？**> 前提，MySQL 默认是自提交的，所以如果没有明确地开启事务，一条 SQL 语句就是一条事务。在 mysqldump 里，就是一条 SQL 语句为一条事务。
按照我的“避免大事务”自定义规定，答案是**没有**的。原来，mysqldump 会按照参数&#8211;net-buffer-length，来自动切分 SQL 语句。默认值是 1M。按照我们前面定义的标准，没有达到我们的 2M 的大事务标准。&#8211;net-buffer-length 最大可设置为 16777216，人手设置大于这个值，会自动调整为 16777216，即 16M。设置 16M，可以提升导出导入性能。如果为了避免大事务，那就不建议调整这个参数，使用默认值即可。- `[root@192-168-199-198 ~]# mysqldump --net-buffer-length=104652800 -uroot -proot -P3306 -h192.168.199.198 test t >16M.sql`
- `mysqldump: [Warning] option 'net_buffer_length': unsigned value 104652800 adjusted to 16777216`
- `#设置大于16M，参数被自动调整为16M`
> 注意，指的是 mysqldump 的参数，而不是 mysqld 的参数。官方文档提到: If you increase this variable, ensure that the MySQL server net_buffer_length system variable has a value at least this large.
意思是 mysqldump 增大这个值，mysqld 也得增大这个值，测试结论是不需要的。怀疑官方文档有误。
不过，在导入的时候，受到服务器参数 max_allowed_packet 影响，它控制了服务器能接受的数据包的最大大小，默认值是 4194304，即 4M。所以导入数据库时需要调整参数 max_allowed_packet 的值。- `set global max_allowed_packet=16*1024*1024*1024;`
不调整的话，会出现以下报错：- `[root@192-168-199-198 ~]# mysql -uroot -proot -P3306 -h192.168.199.198 test <16M.sql`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `ERROR 2006 (HY000) at line 46: MySQL server has gone away`
**相关测试**最后，我放出我的相关测试步骤- `mysql> select version();`
- `+------------+`
- `| version()  |`
- `+------------+`
- `| 5.7.26-log |`
- `+------------+`
- `1 row in set (0.00 sec)`
**造100万行数据**- `create database test;`
- `use test;`
- `CREATE TABLE `t` (`
- `  `a` int(11) DEFAULT NULL,`
- `  `b` int(11) DEFAULT NULL,`
- `  `c` varchar(255) DEFAULT NULL`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8;`
- 
- `insert into t values (1,1,'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyztuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz');`
- 
- `insert into t select * from t; #重复执行20次`
- `# 直到出现Records: 524288  Duplicates: 0  Warnings: 0`
- `# 说明数据量达到100多万条了。`
- 
- `mysql> select count(*) from t;`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|  1048576 |`
- `+----------+`
- `1 row in set (1.04 sec)`
数据大小如下，有 284MB- `[root@192-168-199-198 test]# pwd`
- `/data/mysql/mysql3306/data/test`
- `[root@192-168-199-198 test]# du -sh t.ibd`
- `284M    t.ibd`
**&#8211;net-buffer-length=1M**- `[root@192-168-199-198 ~]# mysqldump -uroot -proot -S /tmp/mysql3306.sock test t >1M.sql`
- `[root@192-168-199-198 ~]# du -sh 1M.sql`
- `225M    1M.sql`
- `[root@192-168-199-198 ~]# cat 1M.sql |grep -i insert |wc -l`
- `226`
默认 &#8211;net-buffer-length=1M 的情况下，225M 的SQL文件里有 226 条 insert ，平均下来确实就是每条 insert 的 SQL 大小为 1M。**&#8211;net-buffer-length=16M**
- `[root@192-168-199-198 ~]# mysqldump --net-buffer-length=16M -uroot -proot -S /tmp/mysql3306.sock test t >16M.sql`
- `[root@192-168-199-198 ~]# du -sh 16M.sql`
- `225M    16M.sql`
- `[root@192-168-199-198 ~]# cat 16M.sql |grep -i insert |wc -l`
- `15`
默认&#8211;net-buffer-length=16M 的情况下，225M 的 SQL 文件里有 15 条 insert，平均下来确实就是每条 insert 的 SQL 大小为 16M。所以，这里证明了 &#8211;net-buffer-length 确实可用于拆分 mysqldump 备份文件的SQL大小的。
**性能测试**insert 次数越多，交互次数就越多，性能越低。 但鉴于上面例子的 insert 数量差距不大，只有 16 倍，性能差距不会很大(实际测试也是如此)。我们直接对比 &#8211;net-buffer-length=16K 和 &#8211;net-buffer-length=16M 的情况，他们insert次数相差了 1024 倍。- `[root@192-168-199-198 ~]# time mysql -uroot -proot -S /tmp/mysql3306.sock test <16K.sql`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- 
- `real    0m10.911s  #11秒`
- `user    0m1.273s`
- `sys    0m0.677s`
- `[root@192-168-199-198 ~]# mysql -uroot -proot -S /tmp/mysql3306.sock -e "reset master";`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `[root@192-168-199-198 ~]# time mysql -uroot -proot -S /tmp/mysql3306.sock test <16M.sql`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- 
- `real    0m8.083s  #8秒`
- `user    0m1.669s`
- `sys    0m0.066s`
结果明显。&#8211;net-buffer-length 设置越大，客户端与数据库交互次数越少，导入越快。
**结论**mysqldump 默认设置下导出的备份文件，符合导入需求，不会造成大事务。性能方面也符合要求，不需要调整参数。
**参考链接：**https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html#option_mysqldump_net-buffer-length
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
- 技术交流群，进群后可提问
QQ群（669663113）
- 社区通道，邮件&电话
osc@actionsky.com
- 现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
- 格式：.md/.doc/.txt
- 主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
- 要求：原创且未发布过
- 奖励：作者署名；200元京东E卡+社区周边
投稿方式：
- 邮箱：osc@actionsky.com
- 格式：[投稿]姓名+文章标题
- 以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系