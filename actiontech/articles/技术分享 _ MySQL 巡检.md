# 技术分享 | MySQL 巡检

**原文链接**: https://opensource.actionsky.com/20210527-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-05-27T21:42:10-08:00

---

作者：王向
爱可生 DBA 团队成员，负责公司 DMP 产品的运维和客户 MySQL 问题的处理。擅长数据库故障处理。对数据库技术和 python 有着浓厚的兴趣。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# MySQL巡检
- 操作系统层面
cpu
- 内存
- I/O
- 磁盘
- **系统基础信息**
- 操作系统日志
- MySQL
重点参数
- MySQL的状态
- 库表情况
- MySQL主从检测
- 高可用层面
- 中间件的巡检
## 操作系统层面
巡检嘛没啥特别的，就直奔主题把。
### cpu
`sar -u 10 3 
`
### 内存
` sar -r 10 3
`
### I/O
`sar -b 10 3
`
### 磁盘
`df -h
`
### 系统基础信息
当然，查看是否使用numa和swap，或是否频繁交互信息等。还有其他的监控项目，这里就不一一赘述了。
### 操作系统日志
除此之外，还需要关注日志类信息，例如：
`tail 200 /var/log/messages
dmesg | tail 200
`
## MySQL
MySQL重点参数的检查，及主从健康状态的巡检。
### 重点参数
| 参数 | 参考值 |
| --- | --- |
| innodb_buffer_pool_size | 系统的50%-75% |
| binlog_format | ROW |
| sync_binlog | 1 |
| innodb_flush_log_at_trx_commit | 1 |
| read_only | 从库ON，主库OFF |
| super_read_only | 从库ON，主库OFF |
| log_slave_updates | 1 |
| innodb_io_capacity | sata/sas硬盘这个值在200sas raid10: 2000ssd硬盘：8000fusion-io（闪存卡）：25,000-50,000 |
| max_connections |  |
### MySQL的状态
`\s
show full processlist;
show engine innodb status\G
show slave hosts;
`
#### wait事件
`show global status like 'Innodb_buffer_pool_wait_free';
show global status like 'Innodb_log_waits';
`
#### 锁
`#表锁
show global status like 'Table_locks_waited';
show global status like 'Table_locks_immediate';
#行锁
show global status like 'Innodb_row_lock_current_waits';当前等待锁的行锁数量
show global status like 'Innodb_row_lock_time';请求行锁总耗时
show global status like 'Innodb_row_lock_time_avg';请求行锁平均耗时
show global status like 'Innodb_row_lock_time_max';请求行锁最久耗时
show global status like 'Innodb_row_lock_waits';行锁发生次数
#还可以定时收集INFORMATION_SCHEMA里面的信息：
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS; 
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS; // MySQL 8.0 中已经不再使用，建议观测 sys 库
#临时表/临时文件
show global status like 'Created_tmp_disk_tables';
show global status like 'Created_tmp_files';
#打开表/文件数
show global status like 'Open_files';
show global status like 'Open_table_definitions';
show global status like 'Open_tables';
#并发连接数
show global status like 'Threads_running';
show global status like 'Threads_created';
show global status like 'Threads_cached';
show global status like 'Aborted_clients';
#客户端没有正确关闭连接导致客户端终止而中断的连接数
show global status like 'Aborted_connects';
`
#### Binlog
`# 使用临时二进制日志缓存但超过 binlog_cache_size 值，需要使用临时文件存储事务中的语句的事务数
binlog_cache_disk_use;
# 使用二进制日志缓存的事务数
binlog_cache_use;
# 使用二进制日志语句缓存但超过 binlog_stmt_cache_size 的值，需要使用临时文件存储这些语句的非事务语句的数量
binlog_stmt_cache_disk_use;
# 使用二进制日志语句缓存的非事务性语句的数量
binglog_cache_disk_use;
`
#### 链接数
`# 试图连接到（不管成不成功）mysql服务器的链接数
show global status like 'Connection'; 
`
#### 临时表
`# 服务器执行语句时,在硬盘上自动创建的临时表的数量,是指在排序时,内存不够用(tmp_table_size小于需要排序的结果集)，所以需要创建基于磁盘的临时表进行排序
show global status like 'Created_tmp_disk_tables'; 
# 服务器执行语句时自动创建的内存中的临时表的数量
show global status like 'Created_tmp_files';
`
#### 索引
`# 内部提交语句
show global status like 'Handler_commit'; 
# 内部 rollback语句数量
show global status like 'Handler_rollback'; 
# 索引第一条记录被读的次数,如果高,则它表明服务器正执行大量全索引扫描
show global status like 'Handler_read_first';  
# 根据索引读一行的请求数，如果较高，说明查询和表的索引正确
show global status like 'Handler_read_key'; 
# 查询读索引最后一个索引键请求数
show global status like 'Handler_read_last';
# 按照索引顺序读下一行的请求数
show global status like 'Handler_read_next'; 
# 按照索引顺序读前一行的请求数
show global status like 'Handler_read_prev';
# 根据固定位置读一行的请求数，如果值较高，说明可能使用了大量需要mysql扫整个表的查询或没有正确使用索引
show global status like 'Handler_read_rnd'; 
# 在数据文件中读下一行的请求数，如果你正进行大量的表扫，该值会较高
show global status like 'Handler_read_rnd_next'; 
# 被缓存的.frm文件数量
show global status like 'Open_table_definitions'; 
# 已经打开的表的数量,如果较大,table_open_cache值可能太小
show global status like 'Opened_tables';
# 当前打开的表的数量
show global status like 'Open_tables';
# 已经发送给服务器的查询个数
show global status like 'Queries';
# 没有使用索引的联接的数量,如果该值不为0,你应该仔细检查表的所有
show global status like 'Select_full_join';
# 对第一个表进行完全扫的联接的数量
show global status like 'Select_scan';
# 查询时间超过long_query_time秒的查询个数
show global status like 'Slow_queries';
# 排序算法已经执行的合并的数量,如果值较大,增加sort_buffer_size大小
show global status like 'Sort_merge_passes';
`
#### 线程
`# 线程缓存内的线程数量
show global status like 'Threads_cached';
# 当前打开的连接数量
show global status like 'Threads_connected';
# 创建用来处理连接的线程数
show global status like 'Threads_created';
# 激活的（非睡眠状态）线程数
show global status like 'Threads_running';
`
### 库表情况
#### 自增id使用情况
`SELECT
table_schema,
table_name,
ENGINE,
Auto_increment 
FROM
information_schema.TABLES 
WHERE
TABLE_SCHEMA NOT IN (
"INFORMATION_SCHEMA",
"PERFORMANCE_SCHEMA",
"MYSQL",
"SYS") limit 30;
`
#### 表行数数据大小统计
`SELECT
table_schema "Database name",
sum( table_rows ) "No. of rows",
sum( data_length ) / 1024 / 1024 "Size data (MB)",
sum( index_length )/ 1024 / 1024 "Size index (MB)" 
FROM
information_schema.TABLES 
GROUP BY
table_schema;
`
#### 表行数 TOP 30
`SELECT 
TABLE_SCHEMA,
TABLE_NAME,
TABLE_ROWS
FROM 
`information_schema`.`tables` 
WHERE
TABLE_SCHEMA not in('information_schema','sys','mysql','performance_schema')
ORDER BY table_rows DESC LIMIT 30;
`
#### 存储引擎不是innodb的表
`SELECT
TABLE_SCHEMA,
TABLE_NAME,
ENGINE 
FROM
INFORMATION_SCHEMA.TABLES 
WHERE
ENGINE != 'innodb' 
AND TABLE_SCHEMA NOT IN ( "INFORMATION_SCHEMA", "PERFORMANCE_SCHEMA", "MYSQL", "SYS" );
`
#### 表数据和碎片 TOP 30
`select 
TABLE_SCHEMA,
TABLE_NAME,
TABLE_ROWS,
DATA_LENGTH,
INDEX_LENGTH,
DATA_FREE
from 
information_schema.tables 
where 
DATA_FREE is not null 
ORDER BY DATA_FREE DESC LIMIT 30;
`
#### 无主键的表
`SELECT
t1.table_schema,
t1.table_name,
t1.table_type 
FROM
information_schema.TABLES t1
LEFT OUTER JOIN information_schema.TABLE_CONSTRAINTS t2 ON t1.table_schema = t2.TABLE_SCHEMA 
AND t1.table_name = t2.TABLE_NAME 
AND t2.CONSTRAINT_NAME IN ( 'PRIMARY' ) 
WHERE
t2.table_name IS NULL 
AND t1.TABLE_SCHEMA NOT IN ( 'information_schema', 'performance_schema', 'test', 'mysql', 'sys' ) 
AND t1.table_type = "BASE TABLE";
`
### MySQL主从检测
`#主从状态
show slave status\G
#主从是否延迟
Master_Log_File == Relay_Master_Log_File 
&& Read_Master_Log_Pos == Exec_Master_Log_Pos
`
### 高可用层面
**MHA &#038;&#038; keepalived**
观察日志看是否有频繁主从切换，如果有的话就分析一下是什么原因导致频繁切换？
### 中间件的巡检
mycat &#038;&#038; proxysql
这些中间件的巡检，首先参考系统巡检，再看一下中间件本身的日志类和状态类信息，网络延迟或丢包的检查，也是必须要做工作。