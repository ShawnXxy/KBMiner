# 技术分享 | 巧用 binlog Event 发现问题

**原文链接**: https://opensource.actionsky.com/20191212-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-12-11T18:56:37-08:00

---

> **作者：****高鹏（八怪）**文章末尾有他著作的《深入理解 MySQL 主从原理 32 讲》，深入透彻理解 MySQL 主从，GTID 相关技术知识。
**本文建议横屏观看，效果更佳**
有了前面对 Event 的了解，我们就可以利用这些 Event 来完成一些工作了。我曾经在学习了这些常用的 Event 后，使用 C 语言写过一个解析 Event 的工具，我叫它‘infobin’，意思就是从 binary log 提取信息的意思。据我所知虽然这个工具在少数情况下会出现 BUG 但是还是有些朋友在用。我这里并不是要推广我的工具，而是要告诉大家这种思路。我是结合工作中遇到的一些问题来完成了这个工具的，主要功能包含如下：- 分析 binary log 中是否有长期未提交的事务 ，长期不提交的事务将会引发更多的锁争用。
- 分析 binary log 中是否有大事务 ，大事务的提交可能会堵塞其它事务的提交。
- 分析 binary log 中每个表生成了多少 DML Event，这样就能知道哪个表的修改量最大。
- 分析 binary log 中 Event 的生成速度，这样就能知道哪个时间段生成的 Event 更多。
> 下面是这个工具的地址，供大家参考：https://github.com/gaopengcarl/infobin
这个工具的帮助信息如下：
- `[root@gp1 infobin]# ./infobin`
- `USAGE ERROR!`
- `[Author]: gaopeng [QQ]:22389860[blog]:http://blog.itpub.net/7728585/`
- `--USAGE:./infobin binlogfile pieces bigtrxsize bigtrxtime [-t] [-force]`
- `[binlogfile]:binlog file!`
- `[piece]:how many piece will split,is a Highly balanced histogram,`
- `find which time generate biggest binlog.(must:piece<2000000)`
- `[bigtrxsize](bytes):larger than this size trx will view.(must:trx>256(bytes))`
- `[bigtrxtime](sec):larger than this sec trx will view.(must:>0(sec))`
- `[[-t]]:if[-t] no detail isprintout,the result will small`
- `[[-force]]:force analyze if unkown error check!!`
接下来我们具体来看看这几个功能大概是怎么实现的。
**一、分析长期未提交的事务**前面我已经多次提到过对于一个手动提交的事务而言有如下特点，我们以‘Insert’语句为列：1. GTID_LOG_EVENT 和 XID_EVENT 是命令‘COMMIT’发起的时间。2. QUERY_EVENT 是第一个‘Insert’命令发起的时间。3. MAP_EVENT/WRITE_ROWS_EVENT 是每个‘Insert’命令发起的时间。
那实际上我们就可以用（1）减去（2）就能得到第一个‘DML’命令发起到‘COMMIT’命令发起之间所消耗的时间，再使用一个用户输入参数来自定义多久没有提交的事务叫做长期未提交的事务就可以了，我的工具中使用 bigtrxtime 作为这个输入。我们来用一个例子说明，我们做如下语句：
![](https://opensource.actionsky.com/wp-content/uploads/2019/12/表格1.png)											
**我们来看看 Event 的顺序和时间如下：**
![](https://opensource.actionsky.com/wp-content/uploads/2019/12/表格2.png)											
如果我们使用最后一个 XID_EVENT 的时间减去 QUERY_EVENT 的时间，那么这个事务从第一条语句开始到‘COMMIT’的时间就计算出来了。注意一点，实际上‘BEGIN’命令并没有记录到 Event 中，它只是做了一个标记让事务不会自动进入提交流程。> 关于‘BEGIN’命令做了什么可以参考我的简书文章如下：https://www.jianshu.com/p/6de1e8071279
**二、分析大事务**这部分实现比较简单，我们只需要扫描每一个事务 GTID_LOG_EVENT 和 XID_EVENT 之间的所有 Event 将它们的总和计算下来，就可以得到每一个事务生成 Event 的大小（但是为了兼容最好计算 QUERY_EVENT 和 XID_EVENT 之间的 Event 总量）。再使用一个用户输入参数自定义多大的事务叫做大事务就可以了，我的工具中使用 bigtrxsize 作为这个输入参数。
如果参数 binlog_row_image 参数设置为‘FULL’，我们可以大概计算一下特定表的每行数据修改生成的日志占用的大小：
- ‘Insert’和‘Delete’：因为只有 before_image 或者 after_image，因此 100 字节一行数据加上一些额外的开销大约加上 10 字节也就是 110 字节一行。如果定位大事务为 100M 那么大约修改量为 100W 行数据。
- ‘Update’：因为包含 before_image 和 after_image，因此上面的计算的 110 字节还需要乘以 2。因此如果定位大事务为 100M 那么大约修改量为 50W 行数据。
我认为 20M 作为大事务的定义比较合适，当然这个根据自己的需求进行计算。
**三、分析 binary log 中 Event 的生成速度**这个实现就很简单了，我们只需要把 binary log 按照输入参数进行分片，统计结束 Event 和开始 Event 的时间差值就能大概算出每个分片生成花费了多久时间，我们工具使用 piece 作为分片的传入参数。通过这个分析，我们可以大概知道哪一段时间 Event 生成量更大，也侧面反映了数据库的繁忙程度。
**四、分析每个表生成了多少 DML Event**这个功能也非常实用，通过这个分析我们可以知道数据库中哪一个表的修改量最大。实现方式主要是通过扫描 binary log 中的 MAP_EVENT 和接下来的 DML Event，通过 table id 获取表名，然后将 DML Event 的大小归入这个表中，做一个链表，最后排序输出就好了。但是前面我们说过 table id 即便在一个事务中也可能改变，这是我开始没有考虑到的，因此这个工具有一定的问题，但是大部分情况是可以正常运行的。
**五、工具展示**下面我就来展示一下我说的这些功能，我做了如下操作：- `mysql> flush binary logs;`
- `Query OK, 0 rows affected (0.51 sec)`
- 
- `mysql> select count(*) from tti;`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `| 98304|`
- `+----------+`
- `1 row inset(0.06 sec)`
- 
- `mysql> deletefrom tti;`
- `Query OK, 98304 rows affected (2.47 sec)`
- 
- `mysql> begin;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> insert into tti values(1,'gaopeng');`
- `Query OK, 1 row affected (0.00 sec)`
- 
- `mysql> select sleep(20);`
- `+-----------+`
- `| sleep(20) |`
- `+-----------+`
- `| 0|`
- `+-----------+`
- `1 row inset(20.03 sec)`
- 
- `mysql> commit;`
- `Query OK, 0 rows affected (0.22 sec)`
- 
- `mysql> insert into tpp values(10);`
- `Query OK, 1 row affected (0.14 sec)`
在示例中我切换了一个 binary log，同时做了 3 个事务：
- 删除了 tti 表数据一共 98304 行数据。
- 向 tti 表插入了一条数据，等待了 20 多秒提交。
- 向 tpp 表插入了一条数据。
我们使用工具来分析一下，下面是统计输出：
- `./infobin mysql-bin.0000053100000015-t > log.log`
- `more log.log`
- 
- `...`
- `-------------Total now--------------`
- `Trx total[counts]:3`
- `Event total[counts]:125`
- `Max trx event size:8207(bytes) Pos:420[0X1A4]`
- `Avg binlog size(/sec):9265.844(bytes)[9.049(kb)]`
- `Avg binlog size(/min):555950.625(bytes)[542.921(kb)]`
- `--Piece view:`
- `(1)Time:1561442359-1561442383(24(s)) piece:296507(bytes)[289.558(kb)]`
- `(2)Time:1561442383-1561442383(0(s)) piece:296507(bytes)[289.558(kb)]`
- `(3)Time:1561442383-1561442455(72(s)) piece:296507(bytes)[289.558(kb)]`
- `--Large than 500000(bytes) trx:`
- `(1)Trx_size:888703(bytes)[867.874(kb)] trx_begin_p:299[0X12B]`
- `trx_end_p:889002[0XD90AA]`
- `Total large trx count size(kb):#867.874(kb)`
- `--Large than 15(secs) trx:`
- `(1)Trx_sec:31(sec) trx_begin_time:[2019062514:00:08(CST)]`
- `trx_end_time:[2019062514:00:39(CST)] trx_begin_pos:889067`
- `trx_end_pos:889267 query_exe_time:0`
- `--EveryTable binlog size(bytes) and times:`
- `Note:size unit is bytes`
- `---(1)CurrentTable:test.tpp::`
- `Insert:binlog size(40(Bytes)) times(1)`
- `Update:binlog size(0(Bytes)) times(0)`
- `Delete:binlog size(0(Bytes)) times(0)`
- `Total:binlog size(40(Bytes)) times(1)`
- `---(2)CurrentTable:test.tti::`
- `Insert:binlog size(48(Bytes)) times(1)`
- `Update:binlog size(0(Bytes)) times(0)`
- `Delete:binlog size(888551(Bytes)) times(109)`
- `Total:binlog size(888599(Bytes)) times(110)`
- `---Total binlog dml event size:888639(Bytes) times(111)`
我们发现我们做的操作都统计出来了：- 包含一个大事务日志总量大于 500K，大小为 800K 左右，这是我的删除 tti 表中 98304 行数据造成的。
- `--Large than 500000(bytes) trx:`
- `(1)Trx_size:888703(bytes)[867.874(kb)] trx_begin_p:299[0X12B]`
- `trx_end_p:889002[0XD90AA]`
- 包含一个长期未提交的事务，时间为 31 秒，这是我特意等待 20 多秒提交引起的。
- `--Large than 15(secs) trx:`
- `(1)Trx_sec:31(sec) trx_begin_time:[2019062514:00:08(CST)]`
- `trx_end_time:[2019062514:00:39(CST)] trx_begin_pos:889067`
- `trx_end_pos:889267 query_exe_time:0`
- 本 binary log 有两个表的修改记录 tti 和 tpp，其中 tti 表有‘Delete’操作和‘Insert’操作，tpp 表只有‘Insert’操作，并且包含了日志量的大小。
- `--EveryTable binlog size(bytes) and times:`
- `Note:size unit is bytes`
- `---(1)CurrentTable:test.tpp::`
- `Insert:binlog size(40(Bytes)) times(1)`
- `Update:binlog size(0(Bytes)) times(0)`
- `Delete:binlog size(0(Bytes)) times(0)`
- `Total:binlog size(40(Bytes)) times(1)`
- `---(2)CurrentTable:test.tti::`
- `Insert:binlog size(48(Bytes)) times(1)`
- `Update:binlog size(0(Bytes)) times(0)`
- `Delete:binlog size(888551(Bytes)) times(109)`
- `Total:binlog size(888599(Bytes)) times(110)`
- `---Total binlog dml event size:888639(Bytes) times(111)`
好了到这里我想告诉你的就是，学习了 Event 过后就可以自己通过各种语言去试着解析binary log，也许你还能写出更好的工具实现更多的功能。
当然也可以通过 mysqlbinlog 进行解析后，然后通过 shell/python 去统计，但是这个工具的速度要远远快于这种方式。
最后推荐高鹏的专栏《深入理解 MySQL 主从原理 32 讲》，想要透彻了解学习 MySQL 主从原理的朋友不容错过。
作者微信：gp_22389860
![](.img/0aff2ace.jpg)											
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