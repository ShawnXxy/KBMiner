# 社区投稿 | MySQL 跨实例 copy 大表解决方案

**原文链接**: https://opensource.actionsky.com/20190927-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-09-27T00:55:21-08:00

---

**作者简介**
任坤，现居珠海，先后担任专职 Oracle 和 MySQL DBA，现在主要负责 MySQL、mongoDB 和 Redis 维护工作。
**一、背景**某天晚上 20:00 左右开发人员找到我，要求把 pre-prod 环境上的某张表导入到 prod ，第二天早上 07:00 上线要用。
该表有数亿条数据，压缩后 ibd 文件大约 25G 左右，表结构比较简单：- `CREATE TABLE `t` (`
- ``UNIQUE_KEY` varchar(32) NOT NULL,`
- ``DESC` varchar(64) DEFAULT NULL ,`
- ``NUM_ID` int(10) DEFAULT '0' ,`
- `PRIMARY KEY (`UNIQUE_KEY`),`
- `KEY `index_NumID` (`NUM_ID`) USING BTREE`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED`
MySQL 版本：pre-prod 和 prod 都采用 5.7.25 ，单向主从结构。
**二、解决方案**最简单的方法是采用 mysqldump + source ，但是该表数量比较多，之前测试的时候至少耗时 4h+ ，这次任务时间窗口比较短，如果中间执行失败再重试，可能会影响业务正式上线。采用 select into outfile + load infile 会快一点，但是该方案有个致命问题：该命令在主库会把所有数据当成单个事务执行，只有把数据全部成功插入后，才会将 binlog 复制到从库，这样会造成从库严重延迟，而且生成的单个 binlog 大小严重超标，在磁盘空间不足时可能会把磁盘占满。经过比较，最终采用了可传输表空间方案，MySQL 5.6 借鉴 Oracle 引入该技术，允许在 2 个不同实例间快速的 copy innodb 大表。该方案规避了昂贵的 sql 解析和 B+tree 叶节点分裂，目标库可直接重用其他实例已有的 ibd 文件，只需同步一下数据字典，并对 ibd 文件页进行一下校验，即可完成数据同步操作。
具体操作步骤如下：
- 1. 目标库，创建表结构，然后执行 ALTER TABLE t DISCARD TABLESPACE ，此时表t只剩下 frm 文件
- 2. 源库，开启 2 个会话
session1：执行 FLUSH TABLES t FOR EXPORT ，该命令会对 t 加锁，将t的脏数据从 buffer pool 同步到表文件，同时新生成 1 个文件 t.cfg ，该文件存储了表的数据字典信息
session2：保持 session1 打开状态，此时将 t.cfg 和 t.ibd 远程传输到目标库的数据目录，如果目标库是主从结构，需要分别传输到主从两个实例，传输完毕后修改属主为 mysql:mysql
- 3. 源库，session1 执行 unlock tables ，解锁表 t ，此时 t 恢复正常读写
- 4. 目标库，执行 ALTER TABLE t IMPORT TABLESPACE ，如果是主从结构，只需要在主库执行即可
**三、实测**
针对该表，执行 ALTER TABLE &#8230; IMPORT TABLESPACE 命令只需要 6 分钟完成，且 IO 消耗和主从延迟都被控制到合理范围。原本需要数个小时的操作，只需 10 多分钟完成（算上数据传输耗时）。如果线上有空表需要一次性加载大量数据，可以考虑先将数据导入到测试环境，然后通过可传输表空间技术同步到线上，可节约大量执行时间和服务器资源。
**四、总结**
可传输表空间，有如下使用限制：
- 源库和目标库版本一致
- 只适用于 innodb 引擎表
- 源库执行 flush tables t for export 时，该表会不可写
**社区近期动态**
**No.1**
**10.26 DBLE 用户见面会 北京站**
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/默认标题_横版海报_2019.09.16.jpg)											
爱可生开源社区将在 2019 年 10 月 26 日迎来在北京的首场 DBLE 用户见面会，以线下**互动分享**的会议形式跟大家见面。
时间：10月26日 9:00 &#8211; 12:00 AM
地点：HomeCafe 上地店（北京市海淀区上地二街一号龙泉湖酒店对面）
重要提醒：
1. 同日下午还有 dbaplus 社群举办的沙龙：聚焦数据中台、数据架构与优化。
2. 爱可生开源社区会在每年10.24日开源一款高质量产品。本次在 dbaplus 沙龙会议上，爱可生的资深研发工程师闫阿龙，将为大家带来《金融分布式事务实践及txle概述》，并在现场开源。
**No.2**
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
**No.3**
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