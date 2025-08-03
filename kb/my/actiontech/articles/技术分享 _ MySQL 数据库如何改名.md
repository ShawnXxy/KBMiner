# 技术分享 | MySQL 数据库如何改名？

**原文链接**: https://opensource.actionsky.com/20200617-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-06-17T23:34:24-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
最近客户咨询了我一个关于如何更改 MySQL 库名的问题。其实如何安全的更改数据库名，是个非常棘手的问题，特别是针对 MySQL 来数据库来说。今天梳理出来，供大家参考。
被取消的命令
MySQL 之前提供了一个 `rename database db_old to db_new` 的命令来直接对数据库改名，可能由于实现的功能不完备（比如，这条命令可能是一个超大的事务，或者是由于之前的表很多还是 MyISAM 等），后来的版本直接取消了这条命令。
更改数据库名大致上有以下几种方案：
**一、mysqldump 导入导出**
要说最简单的方法，就是直接用 mysqldump 工具，在旧库导出再往新库导入（最原始、最慢、最容易想到）的方法：
旧库 yttdb_old 导出（包含的对象：表、视图、触发器、事件、存储过程、存储函数）- `root@debian-ytt1:/home/ytt# time mysqldump --login-path=root_ytt --set-gtid-purged=off   --single-transaction --routines --events yttdb_old > /tmp/yttdb_old.sql`
- 
- `real    2m24.388s`
- `user    0m5.422s`
- `sys     0m1.120s`
新库 yttdb_new 导入
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -D yttdb_new < /tmp/yttdb_old.sql`
- 
- `real    12m27.324s`
- `user    0m3.778s`
- `sys     0m0.947s`
以上结果是在我个人笔记本的虚拟机上测试，**时间上花费了 12 分 27 秒**，这里源库 yttdb_old 上的表个数为 2002，总共也就 826M，不到 1G，并且包含了视图，触发器，存储过程，存储函数，事件等都有。- `root@debian-ytt1:/home/ytt/mysql-sandboxes/3500/sandboxdata/yttdb_old# ls -l |wc -l`
- `2002`
- 
- `root@debian-ytt1:/home/ytt/mysql-sandboxes/3500/sandboxdata/yttdb_old# du -sh`
- `826M    .`
接下来，记得删除旧库 yttdb_old， 那数据库改名就完成了。看起来这个方法非常简单，可是最大的缺点是太慢了！那有没有其他的比较快的方法呢？答案是有的，不过步骤比这个要复杂很多。接下来来看第二种方法。
**二、改整库的表名**
利用 MySQL 更改表名的方法来批量把旧库的所有表依次遍历，改名为新库的表。
这种方法比第一种要快很多倍，但是没有第一步操作起来那么顺滑，不能一步到位。比如，要把数据库 yttdb_old 改名为 yttdb_new，如果数据库 yttdb_old 里只有磁盘表，那很简单，直接改名即可。- `alter table yttdb_old.t1 to yttdb_new.t1;`
或者写个脚本来批量改，非常简单。
但是一般旧库里不只有磁盘表，还包含其他各种对象。这时候可以先考虑把旧库的各种对象导出来，完了在逐一改完表名后导进去。
**导出旧库 yttdb_old 下除了磁盘表外的其他所有对象（存储函数、存储过程、触发器、事件）**
- `root@debian-ytt1:/home/ytt# time  mysqldump --login-path=root_ytt -t -d -n  --set-gtid-purged=off --triggers --routines --events yttdb_old  > /tmp/yttdb_old_other_object.sql`
- 
- `real    1m41.901s`
- `user    0m1.166s`
- `sys     0m0.606s`
**视图在 MySQL 里被看作是表，因此得先查找出视图名字，再单独导出：**- `root@debian-ytt1:~# view_list=`mysql --login-path=root_ytt -e  "SELECT table_name FROM information_schema.views WHERE table_schema = 'yttdb_old';" -s | tr '\n' ' '``
- 
- `root@debian-ytt1:~# time  mysqldump --login-path=root_ytt --set-gtid-purged=off  --triggers=false yttdb_old $view_list  > /tmp/yttdb_old_view_lists.sql`
- 
- `real    0m0.123s`
- `user    0m0.007s`
- `sys     0m0.007s`
那这些额外的对象成功导出来后，就可以在旧库里删除他们了。当然了，做这些操作之前，建议把旧库的所有对象，包括表，都备份出来，备份方式很多，这里就不细讲了。
现在我们来依次删除这些对象：（其实除了触发器和视图外，其他的对象也可以不用删除，不过为了让改名完后旧库清空，就必须得先删掉它们）。
**为了清晰期间，我这里每种对象单独删除，也可以直接一次性全部删除。**
批量删除存储函数：
- `root@debian-ytt1:/home/ytt# func_lists=`mysql --login-path=root_ytt -e  "SELECT concat('drop function if exists ',routine_name,';') FROM  information_schema.routines  WHERE routine_schema = 'yttdb_old' AND routine_type = 1 " -ss``
- 
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -e "use yttdb_old;$func_lists"`
- 
- `real    0m0.048s`
- `user    0m0.005s`
- `sys     0m0.005s`
批量删除存储过程：- `root@debian-ytt1:/home/ytt# procedure_lists=`mysql --login-path=root_ytt -e  "SELECT concat('drop procedure if exists ',routine_name,';') FROM  information_schema.routines  WHERE routine_schema = 'yttdb_old' AND routine_type = 2 " -ss``
- 
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -e "use yttdb_old;$procedure_lists"`
- `real    0m0.046s`
- `user    0m0.006s`
- `sys     0m0.005s`
批量删除触发器：- `root@debian-ytt1:/home/ytt# trigger_lists=`mysql --login-path=root_ytt -e  "SELECT concat('drop trigger if exists yttdb_old.',trigger_name,';') FROM  information_schema.TRIGGERS WHERE trigger_schema='yttdb_old'" -ss``
- 
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -e "use yttdb_old;$trigger_lists"`
- 
- `real    0m0.050s`
- `user    0m0.008s`
- `sys     0m0.003s`
批量删除视图：- `root@debian-ytt1:/home/ytt# view_lists=`mysql --login-path=root_ytt -e  "SELECT concat('drop view if exists ',table_name,';') FROM  information_schema.VIEWS WHERE table_schema='yttdb_old'" -ss``
- 
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -e "use yttdb_old;$view_lists"`
- 
- `real    0m0.070s`
- `user    0m0.006s`
- `sys     0m0.005s`
批量删除事件：- `root@debian-ytt1:/home/ytt# event_lists=`mysql --login-path=root_ytt -e  "SELECT concat('drop event if exists ',event_name,';') FROM  information_schema.EVENTS WHERE event_schema='yttdb_old'" -ss``
- 
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -e  "use yttdb_old;$event_lists"`
- 
- `real    0m0.054s`
- `user    0m0.011s`
- `sys     0m0.000s`
**完了后利用 `rename table old_table to new_table` 语句来批量更改表名到新库：**
- `(debian-ytt1:3500)|(yttdb_new)>set group_concat_max_len = 18446744073709551615;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `(debian-ytt1:3500)|(yttdb_new)>SELECT CONCAT('rename table ',`
- `                GROUP_CONCAT(CONCAT(' yttdb_old.',table_name,' to yttdb_new.',table_name)) )`
- `                FROM information_schema.TABLES`
- `                WHERE table_schema = 'yttdb_old' AND table_type = 1 INTO @rename_lists;`
- `Query OK, 1 row affected (0.01 sec)`
- 
- `(debian-ytt1:3500)|(yttdb_new)>prepare s1 from @rename_lists;`
- `Query OK, 0 rows affected (0.00 sec)`
- `Statement prepared`
- 
- `(debian-ytt1:3500)|(yttdb_new)>execute s1;`
- `Query OK, 0 rows affected (55.41 sec)`
- 
- `(debian-ytt1:3500)|(yttdb_new)>drop prepare s1;`
- `Query OK, 0 rows affected (00.01 sec)`
**批量更改表名总共才花费 55.41 秒。接下来再把之前导出来的其他对象导入新库 yttdb_new：**
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -D  yttdb_new < /tmp/yttdb_old_other_object.sql`
- 
- `real    0m0.222s`
- `user    0m0.081s`
- `sys     0m0.000s`
- `root@debian-ytt1:/home/ytt# time mysql --login-path=root_ytt -D  yttdb_new < /tmp/yttdb_old_view_lists.sql`
- 
- `real    0m0.158s`
- `user    0m0.013s`
- `sys     0m0.000s`
接下来进行功能验证，验证表数量、触发器、存储过程、存储函数、事件等数目是不是对的上。
**三、历史方案**
其实在 MySQL 早期还有一种方法。
假设 MySQL 部署好了后，所有的 binlog 都有备份，并且二进制日志格式还是 statement 的话，那就可以简单搭建一台从机，让它慢慢追主机到新的库名，等确切要更改旧库的时候，再直接晋升从机为主机即可。
这里只需要从机配置一个参数来把旧库指向为新库：replicate-rewrite-db=yttdb_old->yttdb_new不过这种局限性很大，不具备标准化，不推荐。
**总结**
其实针对 MySQL 本身改库名，大致就这么几种方法：- 如果数据量小，推荐第一种；
- 数据量大，则推荐第二种；
- 数据量巨大，那就非 MySQL 本身能解决的了。
可通过部署第三方 ETL 工具，通过解析 MySQL 二进制日志或其他的方式来把旧库数据直接读取到新库达到改名的目的等等。