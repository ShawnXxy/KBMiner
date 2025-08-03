# 技术分享 | MySQL 慢查询记录原理和内容解析

**原文链接**: https://opensource.actionsky.com/20191022-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-10-22T00:15:34-08:00

---

> **作者：****高鹏**文章末尾有他著作的《深入理解 MySQL 主从原理 32 讲》，深入透彻理解 MySQL 主从，GTID 相关技术知识。源码版本：percona 5.7.14
本文为学习记录，可能有误请谅解，也提供了一些源码接口供有兴趣的朋友调试。
**本文建议PC端观看，效果更佳。**
**背景**
本文并不准备说明如何开启记录慢查询，只是将一些重要的部分进行解析。如何记录慢查询可以自行参考官方文档：- 5.4.5 The Slow Query Log
本文使用 Percona 版本来开启参数 log_slow_verbosity，得到了更详细的慢查询信息。通常情况下信息没有这么多，但是一定是包含关系，本文也会使用 Percona 的参数解释说明一下这个参数的含义。
### 一、慢查询中的时间
实际上慢查询中的时间就是时钟时间，是通过操作系统的命令获得的时间，如下是 Linux 中获取时间的方式：- `while (gettimeofday(&t, NULL) != 0)`
- `  {}`
- `  newtime= (ulonglong)t.tv_sec * 1000000 + t.tv_usec;`
- `return newtime;`
实际上就是通过 OS 的 API gettimeofday 函数获得的时间。
### 二、慢查询记录的依据
1. long_query_time：如果执行时间超过本参数设置记录慢查询。
2. log_queries_not_using_indexes：如果语句未使用索引记录慢查询。
3. log_slow_admin_statements：是否记录管理语句。(如 ALTER TABLE,ANALYZE TABLE, CHECK TABLE, CREATE INDEX, DROP INDEX, OPTIMIZE TABLE, and REPAIR TABLE.)
本文主要讨论 long_query_time 参数的含义。
### 三、long_query_time 参数的具体含义
如果我们将语句的执行时间定义为如下：
- `实际消耗时间 = 实际执行时间+锁等待消耗时间`
**那么 long_query_time 实际上界定的是实际执行时间，所以有些情况下虽然语句实际消耗的时间很长但是是因为锁等待时间较长而引起的，那么实际上这种语句也不会记录到慢查询。**
我们看一下 **log_slow_applicable **函数的代码片段：
- `res= cur_utime - thd->utime_after_lock;`
- 
- `if(res > thd->variables.long_query_time)`
- `    thd->server_status|= SERVER_QUERY_WAS_SLOW;`
- `else`
- `    thd->server_status&= ~SERVER_QUERY_WAS_SLOW;`
这里实际上清楚的说明了上面的观点，是不是慢查询就是通过这个函数进行的判断的，**非常重要**。我可以清晰的看到如下公式：- res（实际执行时间）= cur_utime（实际消耗时间）- thd->utime_after_lock( 锁等待消耗时间) 实际上在慢查询中记录的正是
- Query_time：实际消耗时间
- Lock_time：锁等待消耗时间
**但是是否是慢查询其评判标准却是实际执行时间及 Query_time &#8211; Lock_time**其中锁等待消耗时间（Lock_time）我现在已经知道的包括：1. MySQL 层 MDL LOCK 等待消耗的时间。(Waiting for table metadata lock)
2. MySQL 层 MyISAM 表锁消耗的时间。(Waiting for table level lock)
3. InnoDB 层 行锁消耗的时间。
### 四、MySQL 是如何记录锁时间
我们可以看到在公式中 utime_after_lock（锁等待消耗时间 Lock_time）的记录也就成了整个公式的关键，那么我们试着进行 debug。
##### 1. MySQL 层 utime_after_lock 的记录方式
不管是 MDL LOCK 等待消耗的时间还是 MyISAM 表锁消耗的时间都是在 MySQL 层记录的，实际上它只是记录在函数 mysql_lock_tables 的末尾会调用的 THD::set_time_after_lock 进行的记录时间而已如下：- `void set_time_after_lock()`
- `{`
- `    utime_after_lock= my_micro_time();`
- `    MYSQL_SET_STATEMENT_LOCK_TIME(m_statement_psi, (utime_after_lock - start_utime));`
- `}`
那么这里可以解析为代码运行到 mysql_lock_tables 函数的末尾之前的所有的时间都记录到 utime_after_lock 时间中，实际上并不精确。但是 MDL LOCK 的获取和 MyISAM 表锁的获取都包含在里面。**所以即便是 select 语句也可能会看到 Lock_time 并不为 0。**下面是部分栈帧：
- `#0  THD::set_time_after_lock (this=0x7fff28012820) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_class.h:3414`
- `#1  0x0000000001760d6d in mysql_lock_tables (thd=0x7fff28012820, tables=0x7fff28c16b58, count=1, flags=0) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/lock.cc:366`
- `#2  0x000000000151dc1a in lock_tables (thd=0x7fff28012820, tables=0x7fff28c165b0, count=1, flags=0) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_base.cc:6700`
- `#3  0x00000000017c4234 in Sql_cmd_delete::mysql_delete (this=0x7fff28c16b50, thd=0x7fff28012820, limit=18446744073709551615)`
- `    at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_delete.cc:136`
##### 2. InnoDB 层的行锁的 utime_after_lock 记录方式
InnoDB 引擎层调用通过 thd_set_lock_wait_time 调用 thd_storage_lock_wait 函数完成的，部分栈帧如下：
- `#0  thd_storage_lock_wait (thd=0x7fff2c000bc0, value=9503561) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_class.cc:798`
- `#1  0x00000000019a4b2a in thd_set_lock_wait_time (thd=0x7fff2c000bc0, value=9503561)`
- `    at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:1784`
- `#2  0x0000000001a4b50f in lock_wait_suspend_thread (thr=0x7fff2c088200) at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/lock/lock0wait.cc:363`
- `#3  0x0000000001b0ec9b in row_mysql_handle_errors (new_err=0x7ffff0317d54, trx=0x7ffff2f2e5d0, thr=0x7fff2c088200, savept=0x0)`
- `    at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/row/row0mysql.cc:772`
- `#4  0x0000000001b4fe61 in row_search_mvcc (buf=0x7fff2c087640 "\377", mode=PAGE_CUR_G, prebuilt=0x7fff2c087ac0, match_mode=0, direction=0)`
- `    at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/row/row0sel.cc:5940`
函数本身还是很简单，自己看看就知道了，就是相加而已如下：### 
### 
### 
- `void thd_storage_lock_wait(THD *thd, longlong value)`
- `{`
- `  thd->utime_after_lock+= value;`
- `}`
### 五、Percona 中的 log_slow_verbosity 参数
这是 Percona 的解释：Specifies how much information to include in your slow log. The value is a comma-delimited string, and can contain any combination of the following values:- microtime：Log queries with microsecond precision (mandatory).
- query_plan：Log information about the query&#8217;s execution plan (optional).
- innodb：Log InnoDB statistics (optional).
- minimal：Equivalent to enabling just microtime.
- standard：Equivalent to enabling microtime,innodb.
- full：Equivalent to all other values OR&#8217;ed together.
总之在 Percona 中可以修改这个参数获得更加详细的信息大概的格式如下：- `# Time: 2018-05-30T09:30:12.039775Z`
- `# User@Host: root[root] @ localhost []  Id:    10`
- `# Schema: test  Last_errno: 1317  Killed: 0`
- `# Query_time: 19.254508  Lock_time: 0.001043  Rows_sent: 0  Rows_examined: 0  Rows_affected: 0`
- `# Bytes_sent: 44  Tmp_tables: 0  Tmp_disk_tables: 0  Tmp_table_sizes: 0`
- `# InnoDB_trx_id: 0`
- `# QC_Hit: No  Full_scan: No  Full_join: No  Tmp_table: No  Tmp_table_on_disk: No`
- `# Filesort: No  Filesort_on_disk: No  Merge_passes: 0`
- `#   InnoDB_IO_r_ops: 0  InnoDB_IO_r_bytes: 0  InnoDB_IO_r_wait: 0.000000`
- `#   InnoDB_rec_lock_wait: 0.000000  InnoDB_queue_wait: 0.000000`
- `#   InnoDB_pages_distinct: 0`
- `SET timestamp=1527672612;`
- `select count(*) from z1 limit 1;`
### 六、输出的详细解释
本节将会进行详细的解释，全部的慢查询的输出都来自于函数 File_query_log::write_slow ，有兴趣的同学可以自己看看，我这里也会给出输出的位置和含义，其中含义部分可能给出的是源码中的注释。
##### 1. 第一部分时间
- `# Time: 2018-05-30T09:30:12.039775Z`
对应的代码：
- `my_snprintf(buff, sizeof buff,"# Time: %s\n", my_timestamp);`
其中 my_timestamp 取值来自于- `thd->current_utime();`
实际上就是：- `while(gettimeofday(&t, NULL) != 0)`
- `{}`
- `  newtime= (ulonglong)t.tv_sec * 1000000+ t.tv_usec;`
- `return newtime;`
可以看到实际就是调用 gettimeofday 系统调用得到的系统当前时间。注意：对于 5.6 来讲还有一句判断- `if(current_time != last_time)`
如果两次打印的时间秒钟一致则不会输出时间，只有通过后面介绍的- `SET timestamp=1527753496;`
来判断时间，5.7.14 没有看到这样的代码。
##### 2. 第二部分用户信息
- `# User@Host: root[root] @ localhost []  Id:    10`
对应的代码：- `  buff_len= my_snprintf(buff, 32, "%5u", thd->thread_id());`
- `if(my_b_printf(&log_file, "# User@Host: %s  Id: %s\n", user_host, buff)`
- `== (uint) -1)`
- `goto err;`
- `}`
user_host 是一串字符串，参考代码：- `size_t user_host_len= (strxnmov(user_host_buff, MAX_USER_HOST_SIZE,`
- `                                  sctx->priv_user().str`
- `? sctx->priv_user().str : "",`
- `"[", sctx_user.length ? sctx_user.str :`
- `(thd->slave_thread ? "SQL_SLAVE": ""),`
- `"] @ ",`
- `                                  sctx_host.length ? sctx_host.str : "", " [",`
- `                                  sctx_ip.length ? sctx_ip.str : "", "]",`
- `NullS) - user_host_buff);`
解释如下：- root：m_priv_user &#8211; The user privilege we are using. May be &#8220;&#8221; for anonymous user。
- [root]：m_user &#8211; user of the client, set to NULL until the user has been read from the connection。
- localhost：m_host &#8211; host of the client。
- []:client IP m_ip &#8211; client IP。
- Id：10 thd->thread_id() 实际上就是 show processlist 出来的 id。
##### 3. 第三部分 schema 等信息
- `# Schema: test  Last_errno: 1317  Killed: 0`
对应的代码：- `"# Schema: %s  Last_errno: %u  Killed: %u\n"`
- `(thd->db().str ? thd->db().str : ""),`
- `  thd->last_errno, (uint) thd->killed,`
- Schema：m_db Name of the current (default) database.If there is the current (default) database, &#8220;db&#8221; contains its name. If there is no current (default) database, &#8220;db&#8221; is NULL and &#8220;db_length&#8221; is 0. In other words, &#8220;db&#8221;, &#8220;db_length&#8221; must either be NULL, or contain a valid database name.
- Last_errno：
Variable last_errno contains the last error/warning acquired during query execution.
- Killed：这里代表的是终止的错误码。源码中如下：
enum killedstate
{
NOTKILLED=0,
KILLBADDATA=1,
KILLCONNECTION=ERSERVERSHUTDOWN,
KILLQUERY=ERQUERYINTERRUPTED,
KILLTIMEOUT=ERQUERYTIMEOUT,
KILLEDNOVALUE /* means neither of the states */
};
在错误码中代表如下：
{ &#8220;ERSERVERSHUTDOWN&#8221;, 1053, &#8220;Server shutdown in progress&#8221; },
{ &#8220;ERQUERYINTERRUPTED&#8221;, 1317, &#8220;Query execution was interrupted&#8221; },
{ &#8220;ERQUERYTIMEOUT&#8221;, 1886, &#8220;Query execution was interrupted,
maxstatement_time exceeded&#8221; },
##### 4. 第四部分执行信息
这部分可能是大家最关心的部分，很多信息也是默认输出都会输出的。- `# Query_time: 19.254508  Lock_time: 0.001043  Rows_sent: 0  Rows_examined: 0  Rows_affected: 0`
- `# Bytes_sent: 44  Tmp_tables: 0  Tmp_disk_tables: 0  Tmp_table_sizes: 0`
- `# InnoDB_trx_id: 0`
对应代码：- `my_b_printf(&log_file,`
- `"# Schema: %s  Last_errno: %u  Killed: %u\n"`
- `"# Query_time: %s  Lock_time: %s  Rows_sent: %llu"`
- `"  Rows_examined: %llu  Rows_affected: %llu\n"`
- `"# Bytes_sent: %lu",`
- `(thd->db().str ? thd->db().str : ""),`
- `                  thd->last_errno, (uint) thd->killed,`
- `                  query_time_buff, lock_time_buff,`
- `(ulonglong) thd->get_sent_row_count(),`
- `(ulonglong) thd->get_examined_row_count(),`
- `(thd->get_row_count_func() > 0)`
- `? (ulonglong) thd->get_row_count_func() : 0,`
- `(ulong) (thd->status_var.bytes_sent - thd->bytes_sent_old)`
- `my_b_printf(&log_file,`
- `"  Tmp_tables: %lu  Tmp_disk_tables: %lu  "`
- `"Tmp_table_sizes: %llu",`
- `                    thd->tmp_tables_used, thd->tmp_tables_disk_used,`
- `                    thd->tmp_tables_size)`
- `snprintf(buf, 20, "%llX", thd->innodb_trx_id);及thd->innodb_trx_id`
- Query_time：语句执行的时间及实际消耗时间 。
- Lock_time：包含 MDL lock 和 InnoDB row lock 和 MyISAM 表锁消耗时间的总和及锁等待消耗时间。前面已经进行了描述（实际上也并不全是锁等待的时间只是锁等待包含在其中）。
- `我们来看看Query_time和Lock_time的源码来源，它们来自于Query_logger::slow_log_write函数如下：`
- 
- `    query_utime= (current_utime > thd->start_utime) ?`
- `(current_utime - thd->start_utime) : 0;`
- `    lock_utime=  (thd->utime_after_lock > thd->start_utime) ?`
- `(thd->utime_after_lock - thd->start_utime) : 0;`
- 
- `下面是数据current_utime 的来源，`
- 
- `current_utime= thd->current_utime();`
- `实际上就是：`
- `while(gettimeofday(&t, NULL) != 0)`
- `{}`
- `  newtime= (ulonglong)t.tv_sec * 1000000+ t.tv_usec;`
- `return newtime;`
- `获取当前时间而已`
- 
- `对于thd->utime_after_lock的获取我已经在前文进行了描述，不再解释。`
- Rows_sent：发送给 mysql 客户端的行数，下面是源码中的解释 Number of rows we actually sent to the client
- Rows_examined：InnoDB 引擎层扫描的行数,下面是源码中的解释。(备注栈帧1)
Number of rows read and/or evaluated for a statement. Used for slow log reporting. An examined row is defined as a row that is read and/or evaluated according to a statement condition, including increate_sort_index(). Rows may be counted more than once, e.g., a statement including ORDER BY could possibly evaluate the row in filesort() before reading it for e.g. update.
- Rows_affected：涉及到修改的话（比如DML语句）这是受影响的行数。
for DML statements: to the number of affected rows;
for DDL statements: to 0.
- Bytes_sent：发送给客户端的实际数据的字节数，它来自于(ulong) (thd->status_var.bytes_sent &#8211; thd->bytes_sent_old)
- Tmp_tables：临时表的个数。
- Tmp_disk_tables：磁盘临时表的个数。
- Tmp_table_sizes：临时表的大小。
以上三个指标来自于：- `thd->tmp_tables_used`
- `thd->tmp_tables_disk_used`
- `thd->tmp_tables_size`
这三个指标增加的位置对应在 free_tmp_table 函数中如下：
- `  thd->tmp_tables_used++;`
- `if(entry->file)`
- `{`
- `      thd->tmp_tables_size += entry->file->stats.data_file_length;`
- `if(entry->file->ht->db_type != DB_TYPE_HEAP)`
- `          thd->tmp_tables_disk_used++;`
- `}`
- InnoDB_trx_id：事物 ID，也就是 trx->id，/*!< transaction id */
##### 5. 第五部分优化器相关信息
- `# QC_Hit: No  Full_scan: No  Full_join: No  Tmp_table: No  Tmp_table_on_disk: No`
- `# Filesort: No  Filesort_on_disk: No  Merge_passes: 0`
这一行来自于如下代码：- ` my_b_printf(&log_file,`
- `"# QC_Hit: %s  Full_scan: %s  Full_join: %s  Tmp_table: %s  "`
- `"Tmp_table_on_disk: %s\n"                             \`
- `"# Filesort: %s  Filesort_on_disk: %s  Merge_passes: %lu\n",`
- `((thd->query_plan_flags & QPLAN_QC) ? "Yes": "No"),`
- `((thd->query_plan_flags & QPLAN_FULL_SCAN) ? "Yes": "No"),`
- `((thd->query_plan_flags & QPLAN_FULL_JOIN) ? "Yes": "No"),`
- `((thd->query_plan_flags & QPLAN_TMP_TABLE) ? "Yes": "No"),`
- `((thd->query_plan_flags & QPLAN_TMP_DISK) ? "Yes": "No"),`
- `((thd->query_plan_flags & QPLAN_FILESORT) ? "Yes": "No"),`
- `((thd->query_plan_flags & QPLAN_FILESORT_DISK) ? "Yes": "No"),`
这里注意一个处理的技巧，这里 query_plan_flags 中每一位都代表一个含义，这样存储既能存储足够多的信息同时存储空间也很小，是 C/C++ 中常用的方式。- QC_Hit: No：是否 query cache 命中。
- Full_scan：此处相当于 Select_scan 的含义，是否进行了全扫描包括 using index。
- Full_join：此处相当于 Select_full_join 的含义，是否被驱动表使用到了索引，如果没有使用到索引则为 YES。
**考虑如下的执行计划：******- `mysql> desc select*,sleep(1) from testuin a,testuin1 b where a.id1=b.id1;`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+----------------------------------------------------+`
- `| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref| rows | filtered | Extra|`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+----------------------------------------------------+`
- `|  1| SIMPLE      | a     | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    5|   100.00| NULL                                               |`
- `|  1| SIMPLE      | b     | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    5|    20.00| Usingwhere; Using join buffer (BlockNestedLoop) |`
- `+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+----------------------------------------------------+`
- `2 rows inset, 1 warning (0.00 sec)`
如此输出如下：- `# QC_Hit: No  Full_scan: Yes  Full_join: Yes`
- Tmp_table：是否使用了临时表，在函数 create_tmp_table 中设置。
- Tmp_table_on_disk：是否使用了磁盘临时表，如果时候 innodb 引擎则在 create_innodb_tmp_table 函数中设置。
- Filesort：是否进行了排序，在函数 filesort 中设置。
- Filesort_on_disk：是否使用了磁盘排序，同样在函数 filesort 中设置，但是设置之前会进行是否需要磁盘排序文件的判断。
- Merge_passes：进行多路归并排序，归并的次数。Variable query_plan_fsort_passes collects information about file sort passes acquired during query execution.
##### 6. 第六部分 InnoDB 相关信息
- `#   InnoDB_IO_r_ops: 0  InnoDB_IO_r_bytes: 0  InnoDB_IO_r_wait: 0.000000`
- `#   InnoDB_rec_lock_wait: 0.000000  InnoDB_queue_wait: 0.000000`
- `#   InnoDB_pages_distinct: 0`
这一行来自于如下代码：- `char buf[3][20];`
- `    snprintf(buf[0], 20, "%.6f", thd->innodb_io_reads_wait_timer / 1000000.0);`
- `    snprintf(buf[1], 20, "%.6f", thd->innodb_lock_que_wait_timer / 1000000.0);`
- `    snprintf(buf[2], 20, "%.6f", thd->innodb_innodb_que_wait_timer / 1000000.0);`
- `if(my_b_printf(&log_file,`
- `"#   InnoDB_IO_r_ops: %lu  InnoDB_IO_r_bytes: %llu  "`
- `"InnoDB_IO_r_wait: %s\n"`
- `"#   InnoDB_rec_lock_wait: %s  InnoDB_queue_wait: %s\n"`
- `"#   InnoDB_pages_distinct: %lu\n",`
- `                    thd->innodb_io_reads, thd->innodb_io_read,`
- `                    buf[0], buf[1], buf[2], thd->innodb_page_access)`
- `== (uint) -1)`
- InnoDB_IO_r_ops：物理 IO 读取次数。
- InnoDB_IO_r_bytes：物理 IO 读取的总字节数。
- InnoDB_IO_r_wait：物理 IO 读取等待的时间。innodb 使用 BUF_IO_READ 标记为物理 io 读取繁忙，参考函数 buf_wait_for_read。
- InnoDB_rec_lock_wait：等待行锁消耗的时间。在函数 que_thr_end_lock_wait 中设置。
- InnoDB_queue_wait：等待进入 innodb 引擎消耗的时间，在函数 srv_conc_enter_innodb_with_atomics 中设置。
（参考http://blog.itpub.net/7728585/viewspace-2140446/）
- InnoDB_pages_distinct：innodb 访问的页数，包含物理和逻辑 IO，在函数 buf_page_get_gen 的末尾通过 increment_page_get_statistics 函数设置。
##### 7. 第七部分 set timestamp
- `SET timestamp=1527753496;`
这一句来自源码，注意源码注释解释就是获取的服务器的当前的时间（current_utime）。- `/*`
- `    This info used to show up randomly, depending on whether the query`
- `    checked the query start time or not. now we always write current`
- `    timestamp to the slow log`
- `  */`
- `end= my_stpcpy(end, ",timestamp=");`
- `end= int10_to_str((long) (current_utime / 1000000), end, 10);`
- 
- `if(end!= buff)`
- `{`
- `*end++=';';`
- `*end='\n';`
- `if(my_b_write(&log_file, (uchar*) "SET ", 4) ||`
- `        my_b_write(&log_file, (uchar*) buff + 1, (uint) (end-buff)))`
- `goto err;`
- `}`
**七、总结**本文通过查询源码解释了一些关于 MySQL 慢查询的相关的知识，主要解释了慢查询是基于什么标准进行记录的，同时输出中各个指标的含义，当然这仅仅是我自己得出的结果，如果有不同意见可以一起讨论。备注栈帧 1 ：本栈帧主要跟踪 Rows_examined 的变化及 join->examined_rows++；的变化- `(gdb) info b`
- `NumTypeDispEnbAddressWhat`
- `1       breakpoint     keep y   0x0000000000ebd5f3in main(int, char**) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/main.cc:25`
- `        breakpoint already hit 1 time`
- `4       breakpoint     keep y   0x000000000155b94fin do_select(JOIN*) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:872`
- `        breakpoint already hit 5 times`
- `5       breakpoint     keep y   0x000000000155ca39in evaluate_join_record(JOIN*, QEP_TAB*) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:1473`
- `        breakpoint already hit 20 times`
- `6       breakpoint     keep y   0x00000000019b4313in ha_innobase::index_first(uchar*)`
- `                                               at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9547`
- `        breakpoint already hit 4 times`
- `7       breakpoint     keep y   0x00000000019b45cdin ha_innobase::rnd_next(uchar*)`
- `                                               at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9651`
- `8       breakpoint     keep y   0x00000000019b2ba6in ha_innobase::index_read(uchar*, uchar const*, uint, ha_rkey_function)`
- `                                               at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9004`
- `        breakpoint already hit 3 times`
- `9       breakpoint     keep y   0x00000000019b4233in ha_innobase::index_next(uchar*)`
- `                                               at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9501`
- `        breakpoint already hit 5 times`
- 
- `#0  ha_innobase::index_next (this=0x7fff2cbc6b40, buf=0x7fff2cbc7080 "\375\n") at /root/mysql5.7.14/percona-server-5.7.14-7/storage/innobase/handler/ha_innodb.cc:9501`
- `#1  0x0000000000f680d8 in handler::ha_index_next (this=0x7fff2cbc6b40, buf=0x7fff2cbc7080 "\375\n") at /root/mysql5.7.14/percona-server-5.7.14-7/sql/handler.cc:3269`
- `#2  0x000000000155fa02 in join_read_next (info=0x7fff2c007750) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:2660`
- `#3  0x000000000155c397 in sub_select (join=0x7fff2c007020, qep_tab=0x7fff2c007700, end_of_records=false)`
- `    at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:1274`
- `#4  0x000000000155bd06 in do_select (join=0x7fff2c007020) at /root/mysql5.7.14/percona-server-5.7.14-7/sql/sql_executor.cc:944`
最后推荐高鹏的专栏《深入理解 MySQL 主从原理 32 讲》，想要透彻了解学习 MySQL 主从原理的朋友不容错过。
作者微信：gp_22389860
![](.img/0aff2ace.jpg)											
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
**「3306π」成都站 Meetup**
知数堂将在 2019 年 10 月 26 日在成都举办线下会议，本次会议中邀请了五位数据库领域的资深研发/DBA进行主题分享。
时间：2019年10月26日 13:00-18:00
地点：成都市高新区天府三街198号腾讯成都大厦A座多功能厅
**No.3**
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
**No.4**
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