# 技术分享 | MySQL Shell 收集 MySQL 诊断报告（上）

**原文链接**: https://opensource.actionsky.com/20230112-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-01-12T00:01:11-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
通常对于MySQL运行慢、异常运行等等现象，需要通过收集当时的诊断报告以便后期重点分析并且给出对应解决方案。对于MySQL来讲，目前收集诊断报告的方法大致有以下几类：
- 手动写脚本收集。
- Percona-toolkit工具集里自带的pt-stalk。
- MySQL的sys库自带存储过程diagnostics。
- MySQL Shell 工具的util 组件（需升级到MySQL 8.0.31 最新版才能体验全部诊断程序）
这些工具基本上都可以从不同程度收集OS 以及MySQL SERVER 的诊断数据，并且生成对应的诊断报告。 今天我们来介绍MySQL Shell 最新版本8.0.31 的util组件带来的全新诊断报告收集功能。
#### util.debug属性有三个诊断函数：
- collect_diagnostics 用来收集单实例、副本集、InnoDB Cluster 的诊断数据。**（*旧版本8.0.30 也可以用，不过功能不是很全面）*
- collect_high_load_diagnostics 用来循环多次收集，并找出负载异常的诊断数据。
- collect_slow_query_diagnostics 用来对函数collect_diagnostics收集到的慢日志做进一步分析。
##### 今天我们先来介绍第一个函数collect_diagnostics 如何使用：
函数collect_diagnostics 用来收集如下诊断数据并给出对应诊断报告：
- 无主键的表
- 死索引的表
- MySQL错误日志
- 二进制日志元数据
- 副本集状态（包含主库和从库）
- InnoDB Cluster 监控数据
- 表锁、行锁等数据
- 当前连接会话数据
- 当前内存数据
- 当前状态变量数据
- 当前MySQL 慢日志（需主动开启开关）
- OS 数据（CPU、内存、IO、网络、MySQL进程严重错误日志过滤等）
函数collect_diagnostics 有两个入参：一个是输出路径；另一个是可选字典配置选项，比如可以配置慢日志收集、定制执行SQL 语句、定制执行SHELL命令等等。
#### 以下是常用调用示例：
- 只传递参数1，给定诊断数据打包输出路径，诊断报告会整体打包为/tmp/cd1.zip。
util.debug.collect_diagnostics('/tmp/cd1')
- 激活慢日志抓取（必需条件：MySQL慢日志开关开启、日志输出格式为TABLE），诊断报告会整体打包为/tmp/cd2.zip，并且包含慢日志诊断报告。
util.debug.collect_diagnostics('/tmp/cd2',{"slowQueries":True})
- 定制执行SQL： 收集预置诊断报告同时也收集给定的SQL语句执行结果。
util.debug.collect_diagnostics('/tmp/cd3',{"customSql":["select * from ytt.t1 order by id desc limit 100"]})
- 定制执行SHELL命令： 收集预置诊断报告同时也收集给定的SHELL命令执行结果。
util.debug.collect_diagnostics('/tmp/cd4',{"customShell":["ps aux | grep mysqld"]})
- 收集所有成员诊断数据（副本集或者InnoDB Cluster）。
util.debug.collect_diagnostics('/tmp/cd5',{"allMembers":True})
分别执行以上5条命令，在/tmp目录下会生成如下文件： 以下5个打包文件即是我们运行的5条命令的结果。
root@ytt-pc:/tmp# ll cd*
-rw------- 1 root root  893042 1月   5 10:31 cd1.zip
-rw------- 1 root root  818895 1月   5 10:55 cd2.zip
-rw------- 1 root root  819183 1月   5 11:02 cd3.zip
-rw------- 1 root root  835387 1月   5 11:06 cd4.zip
-rw------- 1 root root 2040913 1月   5 11:31 cd5.zip
要查看具体诊断报告，得先解压这些文件。先来看下cd2.zip 解压后的内容：对于收集的诊断数据，有tsv和yaml两种格式的报告文件。报告文件以数字0开头，表示这个诊断报告来自一台单实例MySQL。
root@ytt-pc:/tmp/cd/cd2# ls|more
0.error_log
0.global_variables.tsv
0.global_variables.yaml
0.information_schema.innodb_metrics.tsv
0.information_schema.innodb_metrics.yaml
0.information_schema.innodb_trx.tsv
0.information_schema.innodb_trx.yaml
0.instance
0.metrics.tsv
0.performance_schema.events_waits_current.tsv
0.performance_schema.events_waits_current.yaml
0.performance_schema.host_cache.tsv
0.performance_schema.host_cache.yaml
0.performance_schema.metadata_locks.tsv
0.performance_schema.metadata_locks.yaml
...
比如查看此实例的连接字符串：
root@ytt-pc:/tmp/cd/cd2# cat 0.uri mysql://root@localhost:3306
以下为对应的慢日志报告：分别为慢日志数据、95分位慢日志数据以及根据扫描行数排序的慢日志数据。
root@ytt-pc:/tmp/cd/cd2# ls *slow*
0.slow_log.tsv   0.slow_queries_in_95_pctile.tsv   0.slow_queries_summary_by_rows_examined.tsv
0.slow_log.yaml  0.slow_queries_in_95_pctile.yaml  0.slow_queries_summary_by_rows_examined.yaml
cd1.zip、cd2.zip、cd3.zip、cd4.zip 都是基于单实例收集的诊断报告，解压后的文件都是以0开头；cd5.zip是基于副本集收集的诊断报告，解压后的文件是以1，2，3开头，分别代表实例3310，3311，3312。
比如查看副本集里3个成员的连接字符串：
root@ytt-pc:/tmp/cd/cd5# cat {1,2,3}.urimysql://root@127.0.0.1:3310?ssl-mode=requiredmysql://root@127.0.0.1:3311?ssl-mode=requiredmysql://root@127.0.0.1:3312?ssl-mode=required
目前副本集的拓扑： 3310 为主，3311，3312为从，可以在主库上执行show replicas 命令得到从库列表
MySQL  localhost:3310 ssl  SQL > show replicas;
+------------+-----------+------+------------+--------------------------------------+
| Server_Id  | Host      | Port | Source_Id  | Replica_UUID                         |
+------------+-----------+------+------------+--------------------------------------+
| 2736952196 | 127.0.0.1 | 3312 | 4023085694 | 0824a675-8ca9-11ed-a719-0800278da4ac |
| 3604736168 | 127.0.0.1 | 3311 | 4023085694 | 0526130e-8ca9-11ed-b797-0800278da4ac |
+------------+-----------+------+------------+--------------------------------------+
2 rows in set (0.0002 sec)
从诊断报告里查看实例3310 的从库列表：
root@ytt-pc:/tmp/cd/cd5# cat 1.SHOW_REPLICAS.yaml
...
#
Host: 127.0.0.1
Port: 3312
Replica_UUID: 0824a675-8ca9-11ed-a719-0800278da4ac
Server_Id: 2736952196
Source_Id: 4023085694
---
Host: 127.0.0.1
Port: 3311
Replica_UUID: 0526130e-8ca9-11ed-b797-0800278da4ac
Server_Id: 3604736168
Source_Id: 4023085694
#### 结语：
MySQL Shell 8.0.31 带来的增强版收集诊断报告功能，能更好的弥补MySQL在这一块的空缺，避免安装第三方工具，从而简化DBA的运维工作。