# 技术分享 | MySQL 存储过程中的只读语句超时怎么办？

**原文链接**: https://opensource.actionsky.com/20220824-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-08-24T00:13:07-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 有一个参数叫 max_execution_time ，用来设置只读语句执行的超时时间，但是仅对单独执行的 select 语句有效；对于非单独执行的 select 语句，比如包含在存储过程、触发器等内置事务块里则不生效。官方手册上对这个参数解释如下：
[`max_execution_time`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_execution_time) applies as follows:
- The global [`max_execution_time`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_execution_time) value provides the default for the session value for new connections. The session value applies to `SELECT` executions executed within the session that include no [`MAX_EXECUTION_TIME(*`N`*)`](https://dev.mysql.com/doc/refman/8.0/en/optimizer-hints.html#optimizer-hints-execution-time) optimizer hint or for which *`N`* is 0.
- [`max_execution_time`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_execution_time) applies to read-only [`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html) statements. Statements that are not read only are those that invoke a stored function that modifies data as a side effect.
- [`max_execution_time`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_execution_time) is ignored for [`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html) statements in stored programs.
那对这种非单独出现的 select 语句，该如何控制超时时间呢？
先来看下参数 max_execution_time 设置后的效果。此参数设置后，select 语句如果执行时间过长，会直接被 cancel 掉，并且报错，如下所示：
mysql> set @@max_execution_time=1000;
Query OK, 0 rows affected (0.00 sec)
mysql> select sleep(2) from t1 limit 1;
ERROR 3024 (HY000): Query execution was interrupted, maximum statement execution time exceeded
或者是采用直接加 Hint 的方式，也能限制 select 语句的执行时间： 下面两种方式都能起到限制 select 语句执行时间的作用。
mysql> select /*+ max_execution_time(1000) */ sleep(2) from t1 limit 2;
ERROR 3024 (HY000): Query execution was interrupted, maximum statement execution time exceeded
mysql> select /*+ set_var(max_execution_time=1000) */ sleep(2) from t1 limit 2;
ERROR 3024 (HY000): Query execution was interrupted, maximum statement execution time exceeded
那如果把这条 select 语句封装在存储过程内部，按照手册上对参数 max_execution_time 的解释，则不生效。比如新建一个存储过程 sp_test ：
DELIMITER $$
USE `ytt`$$
DROP PROCEDURE IF EXISTS `sp_test`$$
CREATE DEFINER=`admin`@`%` PROCEDURE `sp_test`()
BEGIN
select sleep(2) from t1 limit 1;
END$$
DELIMITER ;
重新设置 max_execution_time 值为1秒：调用存储过程 sp_test ，  可以正常执行，select 语句并没有被 cancel 掉！
mysql> call sp_test;
+----------+
| sleep(2) |
+----------+
|        0 |
+----------+
1 rows in set (2.01 sec)
Query OK, 0 rows affected (2.01 sec)
那如何解决这个问题呢？
为了更方便大家测试，把语句 select sleep(2) from t1 limit 1 改为 select sleep(2000) from t1 limit 1 。既然 MySQL 层面有这样的限制，那只能从非 MySQL 层面来想办法。最直接有效的就是写个脚本来主动 cancel 掉 select 语句。脚本如下：
root@ytt-normal:/home/ytt/script# cat kill_query 
#!/bin/sh
QUERY_ID=`mysql -ss -e "select id from information_schema.processlist where user='admin' and db='ytt' and time>10 and regexp_like(info,'^select','i')"`
if [ $QUERY_ID ];then
echo "kill query $QUERY_ID"
mysql -e "kill query $QUERY_ID"
fi
完后把脚本放到 crontab 或者 MySQL 自己的 event 里来定时执行即可。单独执行脚本效果如下：
root@ytt-normal:/home/ytt/script# ./kill_query 
kill query 50
除了自己编写脚本，还有一个工具可以实现类似的效果，它包含在我们熟知的 Percona-toolkit 工具箱里，叫 pt-kill 。
pt-kill 工具可以根据各种触发条件来执行指定动作：比如 cancel 掉指定 SQL 语句、kill 掉指定 session 等。所以完全可以使用 pt-kill 工具来实现  select 语句超时被自动 cancel 掉。如下所示：pt-kill 工具会在后台一直运行，监听 MySQL 进程，一旦触发条件被激活，即可执行相应动作。
root@ytt-normal:/home/ytt/script# pt-kill --match-db=ytt --match-user=admin --match-host=%  \--match-info='^select' --victims=all --busy-time='10s' --print --kill-query
# 2022-08-15T17:29:03 KILL QUERY 50 (Query 11 sec) select sleep(2000) from t1 limit 1
有一点需要注意：select 语句超时自动 cancel 掉这样的功能不适宜用在生产环境！因为你无法预知其执行结果的时效性、上下文是否相关等特点。