# 新特性解读 | MySQL 8.0错误日志深入过滤（上）

**原文链接**: https://opensource.actionsky.com/20220406-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-04-05T23:38:41-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
&#8212;
MySQL 8.0 有一个组件叫 component_log_filter_dragnet ， 它主要功能就是对 MySQL 的错误日志内容进行定制化过滤与改造，之前有简单提过，这次来详细说下如何使用。
使用前，先安装组件：
`INSTALL COMPONENT 'file://component_log_filter_dragnet'; 
`
安装后，设置系统参数*log_error_services* 来启用它。
`SET global log_error_services = 'log_filter_dragnet; log_sink_internal';
`
通过系统参数*dragnet.log_error_filter_rules* 来调整过滤规则，比如对指定错误代码限流、改造输出等等。类似对MySQL监控，必须有过滤条件、触发动作、最终结果等关键因素。 过滤条件则类似SQL语句中单个字段或者多个字段组合过滤。比如字段 值、NOT EXISTS 字段、过滤条件组合等。存在三种字段：分别为核心字段，可选字段，用户自定义字段。
##### 本篇我们来介绍核心字段。
###### 核心字段列表如下：
- 
**time**:  时间，比如可以设置在2022年12月1日之前都不允许写错误日志。
- 
**msg**： 错误信息， 由于err_code直接能定位到msg，一般很少用它来判断，msg可以参与定制内容。
- 
**prio**：优先级，对应的值为*ERROR、WARNING、INFORMATION、NOTE*几个值或者任意组合，与设置系统参数*log_error_verbosity* 效果类似。
- 
**err_code**/**SQL_state**： 具体错误代码，也即错误信息的KEY。
- 
**err_symbol**： 具体错误符号，MySQL每个错误代码都对应一个错误符号。具体的err_symbol 数据可以用perror 打印或者从官网错误参考页面查找：https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
- 
**subsystem**:  指定过滤的子系统项目，比如：Server、InnoDB等。
###### 触发动作有以下四个：
- 
**drop**: 删除错误数据。
- 
**throttle**:  对内容限流。
- 
**set**：定制字段数据。
- 
**unset**:  重置字段数据。
本篇要改造的错误日志基于如下命令产生：全篇用***命令A***代替。
`[root@ytt-pc ytt]# mysql -utest33333 
ERROR 1045 (28000): Access denied for user 'test33333'@'localhost' (using password: NO)
`
**对应的错误日志代码：从结果截取两个err_code 分别为MY-013360和MY-010926。**
`2022-03-24T06:03:59.511173Z 50 [Warning] [MY-013360] [Server] Plugin sha256_password reported: ''sha256_password' is deprecated and will be removed in a future release. Please use caching_sha2_password instead'
2022-03-24T06:03:59.511322Z 50 [Note] [MY-010926] [Server] Access denied for user 'test33333'@'localhost' (using password: NO)
`
##### 接下来我举例说明一些常见用法：
- 
###### 字段time
类似对表时间字段进行过滤，可以定义一个等值条件或者取值范围。例如让2023-01-01之前的错误数据不记入日志，配合字段time以及动作drop来实现：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if time 
退出执行命令A，只要时间还没到2023年，错误日志里就不会记录任何数据。
- 
###### 字段prio.
比如可以用字段prio来屏蔽warning数据，让其不计入错误日志，实现如下：
`   ytt-pc:(none):8.0.28>set global dragnet.log_error_filter_rules='if prio==warning then drop .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，完了查看错误日志：日志里只保留Note数据，warning数据没有记入。
`   2022-03-24T06:05:41.037512Z 52 [Note] [MY-010926] [Server] Access denied for user 'test33333'@'localhost' (using password: NO)
`
- 
###### 字段err_code/SQL_state.
err_code 最直接，只要查到错误代码，根据err_code来过滤即可。比如禁止错误代码为MY-010926的数据记入日志，可以直接用err_code=MY-010926来过滤，实现如下：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 then drop .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，完了查看错误日志：不存在错误代码为MY-010926的数据。
`   2022-03-24T06:08:47.771611Z 53 [Warning] [MY-013360] [Server] Plugin sha256_password reported: ''sha256_password' is deprecated and will be removed in a future release. Please use caching_sha2_password instead'
`
假设想定制错误代码，把它们改造成MySQL官网错误参考页面查不到的值，可以配合动作set来实现：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 or err_code==MY-013360  then set err_code=1234567890 .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，完了查看错误日志：相关错误代码全部替换为**MY-1234567890**。
`   2022-03-24T06:12:37.456522Z 55 [Warning] [MY-1234567890] [Server] Plugin sha256_password reported: ''sha256_password' is deprecated and will be removed in a future release. Please use caching_sha2_password instead'
2022-03-24T06:12:37.456676Z 55 [Note] [MY-1234567890] [Server] Access denied for user 'test33333'@'localhost' (using password: NO)
`
假设想定制错误数据，可以在set动作时，更新字段msg的值，实现如下：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 or err_code==MY-013360  then set msg=''你来看哦，没有了哦！！！'' .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，完了查看错误日志：错误数据已经被重新定制。
`   2022-03-24T06:16:05.617758Z 56 [Warning] [MY-013360] [Server] 你来看哦，没有了哦！！！
2022-03-24T06:16:05.617898Z 56 [Note] [MY-010926] [Server] 你来看哦，没有了哦！！！
`
以上err_code也可以直接替换为对应的SQL_state，效果一样。比如：sql_state='HY000'（这里是字符串）。
- 
###### 字段err_symbol
之前说过，err_symbol和err_code类似，通过perror打印这两个错误代码对应的err_symbol如下：括号里大写的两串字符。
`   [root@ytt-pc ytt]# perror MY-013360 MY-010926
MySQL error code MY-013360 (ER_SERVER_WARN_DEPRECATED): '%s' is deprecated and will be removed in a future release. Please use %s instead
MySQL error code MY-010926 (ER_ACCESS_DENIED_ERROR_WITH_PASSWORD): Access denied for user '%-.48s'@'%-.64s' (using password: %s)
`
现在来由err_symbol实现刚才err_code定制的msg数据：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_symbol==''ER_SERVER_WARN_DEPRECATED''  or err_symbol==''ER_ACCESS_DENIED_ERROR_WITH_PASSWORD'' then set msg=''你来看哦，没有了哦！！''.';
Query OK, 0 rows affected (0.00 sec)
`
- 
###### 字段subsystem
假设要屏蔽Server级别的错误（本篇这两个错误代码对应的数据也是Server级别的），实现如下：
`   ytt-pc:(none):8.0.28>set global dragnet.log_error_filter_rules='if subsystem==''Server'' then drop .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，再次查看错误日志：Server级别的错误数据都没记入日志。
- 
###### 动作复原命令：unset
unset 可以初始化具体的字段，比如初始化这两个错误代码对应的msg，实现如下：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 or err_code==MY-013360  then unset msg .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，完了查看错误日志：数据变为*“No error message, or error message of non-string type. This is almost certainly a bug!”*
`   2022-03-24T06:24:14.846763Z 59 [ERROR] [MY-013360] [Server] No error message, or error message of non-string type. This is almost certainly a bug!
2022-03-24T06:24:14.846925Z 59 [ERROR] [MY-010926] [Server] No error message, or error message of non-string type. This is almost certainly a bug!
`
- 
###### 动作限流命令：throttle
假设这两个错误数据在日志里只能记录两条，实现如下：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 or err_code==MY-013360 then throttle 2 .';
Query OK, 0 rows affected (0.00 sec)
`
无论执行多少次命令A，同样的错误数据在日志里只记录两条。
假设限制这两个错误数据在日志里每分钟记录2条，实现如下：
`ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 or err_code==MY-013360 then throttle 2/60 .';
Query OK, 0 rows affected (0.00 sec)
`
效果为错误日志以分钟级别记录这两条数据。
- 
###### 在条件里加上稍微复杂的判断条件
假设错误代码MY-010926 对应的msg被定制为“**好的，就这样**！”，错误代码MY-013360对应的msg被定制为“**不错哦，就这样吧**！”，实现如下：
`   ytt-pc:ytt:8.0.28>set global dragnet.log_error_filter_rules='if err_code==MY-010926 then set msg=''好的，就这样！'' elseif err_code==MY-013360 then set msg=''不错哦，就这样吧！'' .';
Query OK, 0 rows affected (0.00 sec)
`
退出执行命令A，完了查看错误日志：msg 被对应的定制数据分别覆盖。
`   2022-03-24T06:32:06.505039Z 60 [Warning] [MY-013360] [Server] 不错哦，就这样吧！
2022-03-24T06:32:06.505296Z 60 [Note] [MY-010926] [Server] 好的，就这样！
`
由于内容较多，我分成了两部分，第一部分就到此为止。