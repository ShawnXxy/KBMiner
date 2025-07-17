# 技术分享 | Slow Query Log 使用详解

**原文链接**: https://opensource.actionsky.com/20210114-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-01-14T00:31:31-08:00

---

作者：宓祥康爱可生交付服务部团队 DBA 擅长日志分析、问题排查等；主要负责处理 MySQL 与我司自研数据库自动化管理平台 DMP 的日常运维问题，对数据库及周边技术有浓厚的学习兴趣。本文来源：原创投稿* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 引言
- 什么是 Slow Query Log？
- 该如何使用它？
- 它的存在对运维数据库有什么帮助呢？
## 一、 简介
慢查询日志，开启它我们可以通过参数来控制其记录执行或查询时间长的 SQL、全表扫描的 SQL、没有使用索引的 SQL。没错，它的作用就是记录哪些糟糕的、让数据库变慢的 SQL，把它们揪出来。
我们一般通过如下参数来控制 slow 的开启与记录：slow_query_log、slow_query_log_file、long_query_time、min_examined_row_limit、log_output、log_queries_not_using_indexes、log_throttle_queries_not_using_indexes。
- slow_query_log：控制 slow_query_log 是否开启，参数 ON|OFF
- slow_query_log_file：控制文件的写入位置，参数为文件的具体位置，如：/data/slow.log
- long_query_time：设置 SQL 执行时间大于等于多少秒（可精确到微秒）时记录到日志中
- min_examined_row_limit：设置检查的行数大于等于多少行时记录到日志中
- log_output：设置慢查询记录到哪里，参数 FILE|TABLE
- log_queries_not_using_indexes：控制查询过程中未使用索引或全表扫描的 SQL 是否记录到日志中
- log_throttle_queries_not_using_indexes：开启 log_queries_not_using_indexes 后，此参数会限制每分钟可以写入慢速查询日志的此类查询的数量，参数设置 0 为不限制
# 二、查看方式与内容分析
慢日志分析的方式有两种，因为慢日志文件一般较小，所以一种方式为在慢日志文件中直接使用 less 或 more 命令来查看。第二种方式则是利用 MySQL 官方提供给我们的程序：mysqldumpslow 来快速查看 slowlog 日志中记录的慢 SQL。
对于我们详细来分析 SQL 的话，一般采用第一种方式，查找到对应时间点的对应 SQL 来进行分析。
`show master status;
# Time: 2020-11-16T08:27:16.777259+08:00
# User@Host: root[root] @ [127.0.0.1] Id: 248
# Query_time: 15.293745 Lock_time: 0.000000 Rows_sent: 0 Rows_examined: 0
SET timestamp=1605486436;
`那么如何读懂慢日志里面对这些信息呢？
`show master status 	#慢 SQL
Time 		        #出现该慢 SQL 的时间
query_time		# SQL 语句的查询时间(在 MySQL 中所有类型的 SQL 语句执行的时间都叫做 query_time,而在 Oracle 中则仅指 select)
lock_time: 	        #锁的时间
rows_sent: 		#返回了多少行,如果做了聚合就不准确了
rows_examined:		#执行这条 SQL 处理了多少行数据
SET timestamp 		#时间戳
`通过这些我们就可以来明确的知道一条 SQL 究竟执行了多长时间的查询，有没有发生锁等待，此查询实际在数据库中读取了多少行数据了。
# 三、如何在线安全清空 slow.log 文件
在开启 log_queries_not_using_indexes 后，slow log 文件不仅仅会记录慢查询日志，还会把查询过程中未使用索引或全表扫描的 SQL 记录到日志中，久而久之日志的空间便会变得越来越大，那么如何在线且安全的清空这些 slow log 日志，为磁盘释放空间呢？
MySQL 对于慢日志的输出方式支持两种，TABLE 和 FILE，查看方法如下：
`mysql> show variables like '%log_output%'; 
+---------------+------------+
| Variable_name | Value      |
+---------------+------------+
| log_output    | FILE,TABLE |
+---------------+------------+
`确认清楚输出方式后，可以分别对不同的输出方式选择不同的清空方法，本次将对两种清空方法共同介绍。
## 3.1 FILE 类型清空方法
- 查询 slow query log 开启状态
`mysql> show variables like '%slow_query_log%';
+---------------------+-------------------------------------+
| Variable_name       | Value                               |
+---------------------+-------------------------------------+
| slow_query_log      | ON                                  |
| slow_query_log_file | /opt/mysql/data/3306/mysql-slow.log |
+---------------------+-------------------------------------+
`- 关闭 slow query log
`mysql> set global slow_query_log=0;
`- 确认关闭成功
`mysql> show variables like '%slow_query_log%';
+---------------------+-------------------------------------+
| Variable_name       | Value                               |
+---------------------+-------------------------------------+
| slow_query_log      | OFF                                 |
| slow_query_log_file | /opt/mysql/data/3306/mysql-slow.log |
+---------------------+-------------------------------------+
`- 对日志进行重命名或移除
`mv /opt/mysql/data/3306/mysql-slow.log /opt/mysql/data/3306/mysql-old-slow.log
`- 重新开启 slow query log
`mysql> set global slow_query_log=1;
`- 执行 SQL 进行验证
`mysql> select sleep(5);
+----------+
| sleep(5) |
+----------+
|        0 |
+----------+
`- 验证新生成文件记录成功
`cat /opt/mysql/data/3306/mysql-slow.log 
[root@DMP1 3306]# cat mysql-slow.log
/opt/mysql/base/5.7.31/bin/mysqld, Version: 5.7.31-log (MySQL Community Server (GPL)). started with:
Tcp port: 3306  Unix socket: /opt/mysql/data/3306/mysqld.sock
Time                 Id Command    Argument
# Time: 2021-01-05T13:26:44.001647+08:00
# User@Host: root[root] @ localhost []  Id: 81786
# Query_time: 5.000397  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 0
SET timestamp=1609824404;
select sleep(5);
`- 清理旧的 slowlog 文件
`mv /opt/mysql/data/3306/mysql-old-slow.log /mysqlback`
## 3.2 TABLE 类型清空方法
- 
先关闭 slow query log
`mysql> set global slow_query_log=0;
`
- 
确认关闭成功
`mysql> show variables like 'slow_query_log';
+---------------------+-------------------------------------+
| Variable_name       | Value                               |
+---------------------+-------------------------------------+
| slow_query_log      | OFF                                 |
+---------------------+-------------------------------------+
`
- 
TABLE 类型的 slowlog 存放在 mysql.slow_log 表中,对 slow_log 进行重命名为 old_slow_log
`mysql> use mysql
mysql> ALTER TABLE slow_log RENAME old_slow_log;
`
- 
创建全新的 slow_log 文件拷贝原来 slow_log 文件的表结构
`mysql> CREATE TABLE slow_log LIKE old_slow_log;
`
- 
启动 slow query log
`mysql> SET GLOBAL slow_query_log = 1;
`
- 
测试验证
`mysql> select sleep(5);
+----------+
| sleep(5) |
+----------+
|        0 |
+----------+
mysql> select * from slow_log \G
*************************** 1. row ***************************
start_time: 2021-01-05 13:49:13.864002
user_host: root[root] @ localhost []
query_time: 00:00:05.000322
lock_time: 00:00:00.000000
rows_sent: 1
rows_examined: 0
db: mysql
last_insert_id: 0
insert_id: 0
server_id: 874143039
sql_text: select sleep(5)
thread_id: 339487
`
- 
删除旧的 slow_log 表
`mysql> drop table old_slow_log;`
# 
# 总结
该文章主要讲述了 slow log 的开启方式、分析方法与清空操作，熟练使用分析 slow log 文件可以实时观察数据库 SQL 的执行情况，并为 SQL 优化奠定基础。
**文章推荐：**
[技术分享 | SELinux 与 MySQL](https://opensource.actionsky.com/20210108-mysql/)
[技术分享 | 愈发膨胀的慢日志](https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e6%84%88%e5%8f%91%e8%86%a8%e8%83%80%e7%9a%84%e6%85%a2%e6%97%a5%e5%bf%97/)
[技术分享 | binlog 实用解析工具 my2sql](https://opensource.actionsky.com/20210105-my2sql/)