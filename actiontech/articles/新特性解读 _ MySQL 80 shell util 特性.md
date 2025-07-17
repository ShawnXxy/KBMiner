# 新特性解读 | MySQL 8.0 shell util 特性

**原文链接**: https://opensource.actionsky.com/20190924-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-09-23T22:47:33-08:00

---

**背景**
本文介绍 MySQL 8.0 shell 子模块 Util 的两个导入特性 importTable/import_table(JS和python 版本的命名差异)、importJson/import_json的使用方法。其中import_table 是通过传统 MySQL 协议来通信，Import_json 是通过 X 插件协议来通信。MySQL 一直以来提供导入文件 SQL 命令 load data infile（单线程）以及对应的可执行文件 mysqlimport（多线程）。比如我导入 100W 行示例数据到表 ytt.tl1, 花了 24 秒。这个已经是 MySQL 默认导入来的最快的。- `[root@mysql-dev ytt]# time mysqlimport  --login-path=ytt_master --fields-terminated-by=, --use-threads=4 ytt  /var/lib/mysql-files/tl1.csv`
- `ytt.tl1: Records: 1048576  Deleted: 0  Skipped: 0  Warnings: 0`
- 
- `real    0m24.815s`
- `user    0m0.013s`
- `sys     0m0.031s`
**分析**
那我们现在看下 mysqlimport 工具的升级版，mysqlshell 的 util 工具集。使用这两个工具之前，必须得临时开启 local_infile 选项。
**1. import_table**
- `[root@mysql-dev ytt]# mysqlsh`
- `MySQL Shell 8.0.17`
- 
- `Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.`
- `Oracle is a registered trademark of Oracle Corporation and/or its affiliates.`
- `Other names may be trademarks of their respective owners.`
- 
- `Type '\help' or '\?' for help; '\quit' to exit.`
建立 3306 端口的新连接- `MySQL  JS > \c admin@127.0.0.1:3306`
- `Creating a session to 'admin@127.0.0.1:3306'`
- `Fetching schema names for autocompletion... Press ^C to stop.`
- `Your MySQL connection id is 56`
- `Server version: 8.0.17 MySQL Community Server - GPL`
- `No default schema selected; type \use <schema>to set one.`
我这里切换为 python 模式- `MySQL  127.0.0.1:3306 ssl  JS > \py`
- `Switching to Python mode...`
- `MySQL  127.0.0.1:3306 ssl  Py > \use ytt`
- `Default schema set to `ytt`.`
清空掉示例表 Ytt.tl1- `MySQL  127.0.0.1:3306 ssl  ytt  Py > \sql truncate tl1;`
- `Fetching table and column names from `ytt` for auto-completion... Press ^C to stop.`
- `Query OK, 0 rows affected (0.2354 sec)`
示例表表结构- `MySQL  127.0.0.1:3306 ssl  ytt  Py > \sql show create table tl1\G`
- `*************************** 1. row ***************************`
- `       Table: tl1`
- `Create Table: CREATE TABLE `tl1` (`
- `  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,`
- `  `r1` int(11) DEFAULT NULL,`
- `  `r2` int(11) DEFAULT NULL,`
- `  `r3` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,`
- `  `r4` datetime DEFAULT NULL,`
- `  PRIMARY KEY (`id`),`
- `  UNIQUE KEY `id` (`id`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci`
- `1 row in set (0.0011 sec)`
import_table 有两个参数，第一个参数定义导入文件的路径，第二个定义相关选项，比如导入的格式，并发的数量等。定义文件路径（参数1）- `MySQL  127.0.0.1:3306 ssl  ytt  Py > y_file1='/var/lib/mysql-files/tl1.csv'`
定义选项（参数2）- `MySQL  127.0.0.1:3306 ssl  ytt  Py > y_options1={"schema":"ytt","table":"tl1","fieldsTerminatedBy":",","showProgress":True,"threads":4}`
执行导入：- `MySQL  127.0.0.1:3306 ssl  ytt  Py > util.import_table(y_file1,y_options1);`
- `Importing from file '/var/lib/mysql-files/tl1.csv' to table `ytt`.`tl1` in MySQL Server at 127.0.0.1:3306 using 1 thread`
- `[Worker000] ytt.tl1: Records: 1048576  Deleted: 0  Skipped: 0  Warnings: 0`
- `100% (40.87 MB / 40.87 MB), 2.14 MB/s`
- `File '/var/lib/mysql-files/tl1.csv' (40.87 MB) was imported in 16.7394 sec at 2.44 MB/s`
- `Total rows affected in ytt.tl1: Records: 1048576  Deleted: 0  Skipped: 0  Warnings: 0`
**只花了不到 17 秒，比传统 mysqlimport 快了不少。**
我们上面指定了显式指定了字段分隔符，那有没有已经定义好的组合格式呢？ 答案是有的，选项 dialect 可以指定以下格式：csv，tsv，json，csv-unix
那么上面的导入，我们可以更简单，改下变量 y_options1 的定义- `MySQL  127.0.0.1:3306 ssl  ytt  Py > \sql truncate tl1;`
- `Query OK, 0 rows affected (0.0776 sec)`
- `MySQL  127.0.0.1:3306 ssl  ytt  Py > y_options1={"schema":"ytt","table":"tl1","dialect":"csv-unix","showProgress":True,"threads":4}`
- `MySQL  127.0.0.1:3306 ssl  ytt  Py > util.import_table(y_file1,y_options1);`
- `Importing from file '/var/lib/mysql-files/tl1.csv' to table `ytt`.`tl1` in MySQL Server at 127.0.0.1:3306 using 1 thread`
- `[Worker000] ytt.tl1: Records: 1048576  Deleted: 0  Skipped: 0  Warnings: 0`
- `100% (40.87 MB / 40.87 MB), 2.67 MB/s`
- `File '/var/lib/mysql-files/tl1.csv' (40.87 MB) was imported in 14.1000 sec at 2.90 MB/s`
- `Total rows affected in ytt.tl1: Records: 1048576  Deleted: 0  Skipped: 0  Warnings: 0`
导入时间差不多。这里要说明下，dialect 选项的优先级比较低，比如添加了&#8217;linesTerminatedBy&#8217;:&#8217;\r\n&#8217;， 则覆盖他自己的&#8217;\n&#8217;。选项 diaelect 还有一个可选值为 json，可以直接把 json 结果导入到文档表里。比如我新建一张表 tl1_json- `MySQL  127.0.0.1:3306 ssl  ytt  Py > \sql create table tl1_json(`
- `     id bigint primary key,`
- `     content json);`
- `Query OK, 0 rows affected (0.3093 sec)`
重新定义文件以及导入选项。- `MySQL  127.0.0.1:3306 ssl  ytt  Py > y_file2='/var/lib/mysql-files/tl1.json'`
- `MySQL  127.0.0.1:3306 ssl  ytt  Py > rows=['content']`
- `MySQL  127.0.0.1:3306 ssl  ytt  Py > y_options2={"schema":"ytt","table":"tl1_json","dialect":"json","showProgress":True,"threads":4,'columns':rows}`
导入 JSON 数据- `MySQL  127.0.0.1:3306 ssl  ytt  Py > util.import_table(y_file2,y_options2)`
- `Importing from file '/var/lib/mysql-files/tl1.json' to table `ytt`.`tl1_json` in MySQL Server at 127.0.0.1:3306 using 2 threads`
- `[Worker000] ytt.tl1_json: Records: 464633  Deleted: 0  Skipped: 0  Warnings: 0`
- `[Worker001] ytt.tl1_json: Records: 583943  Deleted: 0  Skipped: 0  Warnings: 0`
- `100% (90.15 MB / 90.15 MB), 2.71 MB/s`
- `File '/var/lib/mysql-files/tl1.json' (90.15 MB) was imported in 23.3530 sec at 3.86 MB/s`
- `Total rows affected in ytt.tl1_json: Records: 1048576  Deleted: 0  Skipped: 0  Warnings: 0`
速度也还可以，不到 24 秒。那导入 json 数据，就必须得提到以 X 插件协议通信的工具 import_json了。
**2. imort_json**我们切换到 mysqlx 端口- `MySQL  127.0.0.1:3306 ssl  ytt  Py > \c admin@127.0.0.1:33060`
- `Creating a session to 'admin@127.0.0.1:33060'`
- `Fetching schema names for autocompletion... Press ^C to stop.`
- `Closing old connection...`
- `Your MySQL connection id is 16 (X protocol)`
- `Server version: 8.0.17 MySQL Community Server - GPL`
- `No default schema selected; type \use <schema> to set one.`
- ` MySQL  127.0.0.1:33060+ ssl  Py > \use ytt`
- `Default schema `ytt` accessible through db.`
- `-- 清空表tl1_json`
- ` MySQL  127.0.0.1:33060+ ssl  ytt  Py > \sql truncate tl1_json;`
- `Query OK, 0 rows affected (0.1098 sec)`
import_json 参数和 Import_table 参数类似，这里我改下选项- `MySQL  127.0.0.1:33060+ ssl  ytt  Py > y_file3=y_file2`
- 
- `MySQL  127.0.0.1:33060+ ssl  ytt  Py > y_options3={"schema":"ytt","table":"tl1_json",'tableColumn':'content'}`
- 
- `MySQL  127.0.0.1:33060+ ssl  ytt  Py > util.import_json(y_file3,y_options3)`
- `Importing from file "/var/lib/mysql-files/tl1.json" to table `ytt`.`tl1_json` in MySQL Server at 127.0.0.1:33060`
- 
- `.. 517776.. 1032724.. 1048576.. 1048576`
- `Processed 90.15 MB in 1048576 documents in 35.2400 sec (29.76K documents/s)`
- `Total successfully imported documents 1048576 (29.76K documents/s)`
我在手册上没有看到多线程的选项，所以单线程跑 35 秒慢了些。查看刚刚导入的数据- `MySQL  127.0.0.1:33060+ ssl  ytt  Py > \sql select  id,json_pretty(content) from tl1_json limit 1\G`
- `*************************** 1. row ***************************`
- `                  id: 1`
- `json_pretty(content): {`
- `  "id": 1,`
- `  "r1": 10,`
- `  "r2": 10,`
- `  "r3": "mysql",`
- `  "r4": "2019-09-16 16:49:50.000000"`
- `}`
- `1 row in set (0.0007 sec)`
import_json 不仅仅可以导入 Json 数据，更重要的是可以在 BSON 和 JSON 之间平滑的转换，有兴趣的同学可以去 TRY 下。
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