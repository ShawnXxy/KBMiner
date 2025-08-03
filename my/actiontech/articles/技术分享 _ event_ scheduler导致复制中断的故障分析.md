# 技术分享 | event_ scheduler导致复制中断的故障分析

**原文链接**: https://opensource.actionsky.com/20190704-event_-scheduler/
**分类**: 技术干货
**发布时间**: 2019-07-04T18:16:44-08:00

---

## 问题背景
在5.6.29和5.7.11版本之前，当binlog格式设置成mixed时，创建event事件中包含sysdate函数时，会导致复制中断。[【与此bug相关】](https://bugs.mysql.com/bug.php?id=71859)
## 场景重现
测试版本：mysql 5.6.23
重现方法：分别设置statement、mixed、row格式执行以下语句，mixed格式时会导致复制中断，其他两种格式不会造成复制中断。
`DELIMITER $$
DROP EVENT IF EXISTS `MIS_CUMULATIVE_REV_EVENT`
$$
CREATE EVENT IF NOT EXISTS `MIS_CUMULATIVE_REV_EVENT`
ON SCHEDULE EVERY 3 second STARTS sysdate() 
ON COMPLETION PRESERVE
DO BEGIN
DECLARE EXIT HANDLER FOR SQLEXCEPTION
SELECT CONCAT('SQL EXCEPTION - TERMINATING EVENT FOR STORED PROCEDURE CALL');
END
$$`
- statement 模式
set global binlog_format=statement;
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片1.png)											
设置5s延迟观察下starts字段时间，复制正常，主从有差异
slave2 [localhost] {msandbox} (test) > change master to MASTER_DELAY=5;
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片2.png)											
- Row模式
set global binlog_format=row;
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片3.png)											
复制正常，主从有差异
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片4.png)											
start字段同样有差异，因为sysdate函数是sql实际执行时间；如果是now函数，start字段时间会是一样的。
- mixed模式
set global binlog_format=mixed;
关闭延迟
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片5-1024x440.png)											
mixed模式下产生的binlog日志
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片6-1024x640.png)											
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片7-1-1024x640.png)											
正常的statement 和row 模式
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/图片8.png)											
## 
从这些截图可知，在mixed模式下创建event时，在同一个事务内即产生了DDL statement，也产生了额外写入mysql.event表的row事件。
对于DDL语句在任何binlog格式下，都会以statement格式记录。
1.mixed模式下遇到非复制安全函数会转换成row模式。例如：sysdate()返回实际执行时间而非调用时间与now函数有差异。
`mysql> SELECT NOW(), SLEEP(2), NOW();
+---------------------+----------+---------------------+
| NOW()               | SLEEP(2) | NOW()               |
+---------------------+----------+---------------------+
| 2006-04-12 13:47:36 |        0 | 2006-04-12 13:47:36 |
+---------------------+----------+---------------------+
mysql> SELECT SYSDATE(), SLEEP(2), SYSDATE();
+---------------------+----------+---------------------+
| SYSDATE()           | SLEEP(2) | SYSDATE()           |
+---------------------+----------+---------------------+
| 2006-04-12 13:47:44 |        0 | 2006-04-12 13:47:46 |
+---------------------+----------+---------------------+
`
## 问题分析
利用systemtap观察下，create event时函数调用，定位为何产生了row事件。
查看源码中有哪些create_event函数
`[root@10-186-21-66 ~]# stap -L 'process("/usr/local/mysql/bin/mysqld").function("create_event")'
process("/usr/local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld").function("create_event@/export/home/pb2/build/sb_0-14249461-1422537824.58/mysqlcom-pro-5.6.23/sql/event_db_repository.cc:660") $this:class Event_db_repository* const $thd:struct THD* $parse_data:struct Event_parse_data* $create_if_not:bool $event_already_exists:bool* $table:struct TABLE* $sp:struct sp_head* $saved_mode:sql_mode_t $mdl_savepoint:class MDL_savepoint
process("/usr/local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld").function("create_event@/export/home/pb2/build/sb_0-14249461-1422537824.58/mysqlcom-pro-5.6.23/sql/event_queue.cc:200") $this:class Event_queue* const $thd:struct THD* $new_element:struct Event_queue_element* $created:bool* $__FUNCTION__:char[] const
process("/usr/local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld").function("create_event@/export/home/pb2/build/sb_0-14249461-1422537824.58/mysqlcom-pro-5.6.23/sql/events.cc:307") $thd:struct THD* $parse_data:struct Event_parse_data* $if_not_exists:bool
`
共有以下3处
第1处：
`/**
Create a new event.
@param[in,out]  thd            THD
@param[in]      parse_data     Event's data from parsing stage
@param[in]      if_not_exists  Whether IF NOT EXISTS was
specified
In case there is an event with the same name (db) and
IF NOT EXISTS is specified, an warning is put into the stack.
@sa Events::drop_event for the notes about locking, pre-locking
and Events DDL.
@retval  FALSE  OK
@retval  TRUE   Error (reported)
*/
bool
Events::create_event(THD *thd, Event_parse_data *parse_data,
bool if_not_exists)
`
第2处：
`/**
Creates an event record in mysql.event table.
Creates an event. Relies on mysql_event_fill_row which is shared with
::update_event.
@pre All semantic checks must be performed outside. This function
only creates a record on disk.
@pre The thread handle has no open tables.
@param[in,out] thd                   THD
@param[in]     parse_data            Parsed event definition
@param[in]     create_if_not         TRUE if IF NOT EXISTS clause was provided
to CREATE EVENT statement
@param[out]    event_already_exists  When method is completed successfully
set to true if event already exists else
set to false
@retval FALSE  success
@retval TRUE   error
*/
bool
Event_db_repository::create_event(THD *thd, Event_parse_data *parse_data,
bool create_if_not,
bool *event_already_exists)
`
第3处：
`/**
Adds an event to the queue.
Compute the next execution time for an event, and if it is still
active, add it to the queue. Otherwise delete it.
The object is left intact in case of an error. Otherwise
the queue container assumes ownership of it.
@param[in]  thd      thread handle
@param[in]  new_element a new element to add to the queue
@param[out] created  set to TRUE if no error and the element is
added to the queue, FALSE otherwise
@retval TRUE  an error occured. The value of created is undefined,
the element was not deleted.
@retval FALSE success
*/
bool
Event_queue::create_event(THD *thd, Event_queue_element *new_element,
bool *created)
`
利用systemtap观察以下两个函数调用情况
`probe process("/usr/local/mysql/bin/mysqld").function("create_event") {
printf(">>>>>>create_event\n");
print_ubacktrace();
}
probe process("/usr/local/mysql/bin/mysqld").function("set_current_stmt_binlog_format_row") {
printf("+++++set_current_stmt_binlog_format_row\n");
print_ubacktrace();
}
`
运行stap -v event.stp，在另一个mysql终端执行创建event语句
`>>>>>>create_event
0x7d36b1 : _ZN6Events12create_eventEP3THDP16Event_parse_datab+0x21/0x340 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x727984 : _Z21mysql_execute_commandP3THD+0x5804/0x6ce0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x729178 : _Z11mysql_parseP3THDPcjP12Parser_state+0x318/0x420 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72a4cb : _Z16dispatch_command19enum_server_commandP3THDPcj+0xbcb/0x28f0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72c2c7 : _Z10do_commandP3THD+0xd7/0x1c0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3ee6 : _Z24do_handle_one_connectionP3THD+0x116/0x1b0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3fc5 : handle_one_connection+0x45/0x60 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x9b22f6 : pfs_spawn_thread+0x126/0x140 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x7ff7b42859d1 [/lib64/libpthread-2.12.so+0x79d1/0x219000]
>>>>>>create_event
0x8bae27 : _ZN19Event_db_repository12create_eventEP3THDP16Event_parse_databPb+0x17/0x2b0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x7d377f : _ZN6Events12create_eventEP3THDP16Event_parse_datab+0xef/0x340 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x727984 : _Z21mysql_execute_commandP3THD+0x5804/0x6ce0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x729178 : _Z11mysql_parseP3THDPcjP12Parser_state+0x318/0x420 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72a4cb : _Z16dispatch_command19enum_server_commandP3THDPcj+0xbcb/0x28f0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72c2c7 : _Z10do_commandP3THD+0xd7/0x1c0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3ee6 : _Z24do_handle_one_connectionP3THD+0x116/0x1b0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3fc5 : handle_one_connection+0x45/0x60 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x9b22f6 : pfs_spawn_thread+0x126/0x140 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x7ff7b42859d1 [/lib64/libpthread-2.12.so+0x79d1/0x219000]
+++++set_current_stmt_binlog_format_row
0x8e6556 : _ZN3THD21decide_logging_formatEP10TABLE_LIST+0x606/0xa60 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6d4e68 : _Z11lock_tablesP3THDP10TABLE_LISTjj+0xe8/0x860 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6de9d2 : _Z20open_and_lock_tablesP3THDP10TABLE_LISTbjP19Prelocking_strategy+0xa2/0xe0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x8ba6a1 : _ZN19Event_db_repository16open_event_tableEP3THD13thr_lock_typePP5TABLE+0x101/0x1d0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x8bae94 : _ZN19Event_db_repository12create_eventEP3THDP16Event_parse_databPb+0x84/0x2b0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x7d377f : _ZN6Events12create_eventEP3THDP16Event_parse_datab+0xef/0x340 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x727984 : _Z21mysql_execute_commandP3THD+0x5804/0x6ce0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x729178 : _Z11mysql_parseP3THDPcjP12Parser_state+0x318/0x420 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72a4cb : _Z16dispatch_command19enum_server_commandP3THDPcj+0xbcb/0x28f0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72c2c7 : _Z10do_commandP3THD+0xd7/0x1c0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3ee6 : _Z24do_handle_one_connectionP3THD+0x116/0x1b0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3fc5 : handle_one_connection+0x45/0x60 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x9b22f6 : pfs_spawn_thread+0x126/0x140 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x7ff7b42859d1 [/lib64/libpthread-2.12.so+0x79d1/0x219000]
>>>>>>create_event
0x8bc64e : _ZN11Event_queue12create_eventEP3THDP19Event_queue_elementPb+0x1e/0xe0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x7d3916 : _ZN6Events12create_eventEP3THDP16Event_parse_datab+0x286/0x340 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x727984 : _Z21mysql_execute_commandP3THD+0x5804/0x6ce0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x729178 : _Z11mysql_parseP3THDPcjP12Parser_state+0x318/0x420 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72a4cb : _Z16dispatch_command19enum_server_commandP3THDPcj+0xbcb/0x28f0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x72c2c7 : _Z10do_commandP3THD+0xd7/0x1c0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3ee6 : _Z24do_handle_one_connectionP3THD+0x116/0x1b0 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x6f3fc5 : handle_one_connection+0x45/0x60 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
0x9b22f6 : pfs_spawn_thread+0x126/0x140 [...local/mysql-advanced-5.6.23-linux-glibc2.5-x86_64/bin/mysqld]
`
基本可知函数调用顺序 Event::create_event -> Event_db_repository::create_event -> decide_logging_format -> set_current_stmt_binlog_format_row_if_mixed -> Event_queue::create_event
binlog.cc decide_logging_format()
`  if (lex->is_stmt_unsafe() || lex->is_stmt_row_injection()
|| (flags_write_all_set & HA_BINLOG_STMT_CAPABLE) == 0)
{
/* log in row format! */
set_current_stmt_binlog_format_row_if_mixed();
}
`
因为sysdate()是非安全函数，所以调用了set_current_stmt_binlog_format_row_if_mixed()。
问题应该出在set_current_stmt_binlog_format_row_if_mixed
`[root@10-186-21-66 ~]# addr2line -e /usr/local/mysql/bin/mysqld 0x8e6556
/export/home/pb2/build/sb_0-14249461-1422537824.58/mysqlcom-pro-5.6.23/sql/sql_class.h:3669
`
sql_class.h
`   inline void set_current_stmt_binlog_format_row_if_mixed()
{
DBUG_ENTER("set_current_stmt_binlog_format_row_if_mixed");
/*
This should only be called from decide_logging_format.
@todo Once we have ensured this, uncomment the following
statement, remove the big comment below that, and remove the
in_sub_stmt==0 condition from the following 'if'.
*/
/* DBUG_ASSERT(in_sub_stmt == 0); */
/*
If in a stored/function trigger, the caller should already have done the
change. We test in_sub_stmt to prevent introducing bugs where people
wouldn't ensure that, and would switch to row-based mode in the middle
of executing a stored function/trigger (which is too late, see also
reset_current_stmt_binlog_format_row()); this condition will make their
tests fail and so force them to propagate the
lex->binlog_row_based_if_mixed upwards to the caller.
*/
if ((variables.binlog_format == BINLOG_FORMAT_MIXED) &&
(in_sub_stmt == 0))
set_current_stmt_binlog_format_row();
DBUG_VOID_RETURN;
}
省略部分代码
inline void set_current_stmt_binlog_format_row()
{
DBUG_ENTER("set_current_stmt_binlog_format_row");
current_stmt_binlog_format= BINLOG_FORMAT_ROW;
DBUG_VOID_RETURN;
}
`
从上述代码可以看出，此函数判断binlog格式是mixed时则调用set_current_stmt_binlog_format_row，
修复补丁中，在create_event 和update_event 函数中，在调用Event_db_repository::create_event前设置binlog格式为statement，再执行Event_db_repository::create_event时就不会产生row事件了。
`@@ -308,6 +308,7 @@ Events::create_event(THD *thd, Event_parse_data *parse_data,
{
bool ret;
bool save_binlog_row_based, event_already_exists;
+  ulong save_binlog_format= thd->variables.binlog_format;
DBUG_ENTER("Events::create_event");
if (check_if_system_tables_error())
@@ -341,10 +342,15 @@ Events::create_event(THD *thd, Event_parse_data *parse_data,
*/
if ((save_binlog_row_based= thd->is_current_stmt_binlog_format_row()))
thd->clear_current_stmt_binlog_format_row();
+  thd->variables.binlog_format= BINLOG_FORMAT_STMT;
+
if (lock_object_name(thd, MDL_key::EVENT,
parse_data->dbname.str, parse_data->name.str))
-    DBUG_RETURN(TRUE);
+  {
+    ret= true;
+    goto err;
+  }
/* On error conditions my_error() is called so no need to handle here */
if (!(ret= db_repository->create_event(thd, parse_data, if_not_exists,
@@ -399,10 +405,12 @@ Events::create_event(THD *thd, Event_parse_data *parse_data,
}
}
}
+err:
/* Restore the state of binlog format */
DBUG_ASSERT(!thd->is_current_stmt_binlog_format_row());
if (save_binlog_row_based)
thd->set_current_stmt_binlog_format_row();
+  thd->variables.binlog_format= save_binlog_format;
`
完整补丁见：git log -p 112899f406d2f1f838a180669781a8973ef3e343
## 结论
1.升级到5.6.29版本或改用row模式
2.如果event 的dml语句中出现类似sysdate()，在mixed模式下并不会造成数据不一致，会自动转成row模式
3.在主从环境下创建event_scheduler，slave默认是禁用状态SLAVESIDE_DISABLED。应考虑主从切换后，原主从的event_scheduler状态，避免产生意外行为，比如 new slave 写入数据。
**近期社区动态**
![](.img/44cd00ec.jpg)