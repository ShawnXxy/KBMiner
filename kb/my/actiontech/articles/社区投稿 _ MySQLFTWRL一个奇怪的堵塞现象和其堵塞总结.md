# 社区投稿 | MySQL：FTWRL一个奇怪的堵塞现象和其堵塞总结

**原文链接**: https://opensource.actionsky.com/20190923-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-09-23T00:43:47-08:00

---

> **作者：高鹏**文章末尾有他著作的《深入理解MySQL主从原理 32讲》，深入透彻理解MySQL主从，GTID相关技术知识。**本案例由徐晨亮提供，并且一起探讨。**本文中，FTWRL = “flush table with read lock”
关于常用操作加 MDL LOCK 锁类型参考文章：http://blog.itpub.net/7728585/viewspace-2143093/测试版本 : MySQL 5.7.22
**一、两种不同的现象**首先建立一张有几条数据的表就可以了，我这里是 baguait1 表了。
案例1
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/表格1.png)											
步骤2“flush table with read lock;”操作等待状态为“Waiting for global read lock”，如下：- `mysql> select Id,State,Info   from information_schema.processlist  where command<>'sleep';`
- `+----+------------------------------+------------------------------------------------------------------------------------+`
- `| Id | State                        | Info                                                                               |`
- `+----+------------------------------+------------------------------------------------------------------------------------+`
- `|  1 | Waiting on empty queue       | NULL                                                                               |`
- `| 18 | Waiting for global read lock | flush table with read lock                                                         |`
- `|  3 | User sleep                   | select sleep(1000) from baguait1 for update                                        |`
- `|  6 | executing                    | select Id,State,Info   from information_schema.processlist  where command<>'sleep' |`
- `+----+------------------------------+------------------------------------------------------------------------------------+`
案例2这里比较奇怪了，实际上我很久以前就遇到过和测试过但是没有仔细研究过，这次刚好详细看看。
![](https://opensource.actionsky.com/wp-content/uploads/2019/09/表格2.png)											
步骤2“flush table with read lock;”操作等待状态为“Waiting for table flush”，状态如下：- `mysql> select Id,State,Info   from information_schema.processlist  where command<>'sleep';`
- `+----+-------------------------+------------------------------------------------------------------------------------+`
- `| Id | State                   | Info                                                                               |`
- `+----+-------------------------+------------------------------------------------------------------------------------+`
- `|  1 | Waiting on empty queue  | NULL                                                                               |`
- `| 26 | User sleep              | select sleep(1000) from baguait1                                                   |`
- `| 23 | Waiting for table flush | flush table with read lock                                                         |`
- `|  6 | executing               | select Id,State,Info   from information_schema.processlist  where command<>'sleep' |`
- `+----+-------------------------+------------------------------------------------------------------------------------+`
步骤4 “select * from testmts.baguait1 limit 1”操作等待状态为“Waiting for table flush”，这个现象看起来非常奇怪没有任何特殊的其他操作，select居然堵塞了。- `mysql> select Id,State,Info   from information_schema.processlist  where command<>'sleep';`
- `+----+-------------------------+------------------------------------------------------------------------------------+`
- `| Id | State                   | Info                                                                               |`
- `+----+-------------------------+------------------------------------------------------------------------------------+`
- `|  1 | Waiting on empty queue  | NULL                                                                               |`
- `| 26 | User sleep              | select sleep(1000) from baguait1                                                   |`
- `| 27 | executing               | select Id,State,Info   from information_schema.processlist  where command<>'sleep' |`
- `|  6 | Waiting for table flush | select * from testmts.baguait1 limit 1                                             |`
- `+----+-------------------------+------------------------------------------------------------------------------------+`
如果仔细对比两个案例实际上区别仅仅在于 步骤 1 中的 select 语句是否加了 for update，案例 2 中我们发现即便我们将 “flush table with read lock;” 会话 KILL 掉也会堵塞随后的关于本表上全部操作（包括 select ），这个等待实际上会持续到步骤 1 的 sleep 操作完成过后。对于线上数据库的话，如果在长时间的 select 大表期间执行 “flush table with read lock;” 就会出现这种情况，这种情况会造成全部关于本表的操作等待，即便你发现后杀掉了 FTWRL 会话也无济于事，等待会持续到 select 操作完成后，除非你 KILL 掉长时间的 select 操作。为什么会出现这种情况呢？我们接下来慢慢分析。
**二、sleep 函数生效点**关于本案例中我使用 sleep 函数来代替 select 大表操作做为测试，在这里这个代替是成立的。为什么成立呢我们来看一下 sleep 函数的生效点如下：- `T@3: | | | | | | | | >evaluate_join_record`
- `T@3: | | | | | | | | | enter: join: 0x7ffee0007350 join_tab index: 0 table: tii cond: 0x0`
- `T@3: | | | | | | | | | counts: evaluate_join_record join->examined_rows++: 1`
- `T@3: | | | | | | | | | >end_send`
- `T@3: | | | | | | | | | | >Query_result_send::send_data`
- `T@3: | | | | | | | | | | | >send_result_set_row`
- `T@3: | | | | | | | | | | | | >THD::enter_cond`
- `T@3: | | | | | | | | | | | | | THD::enter_stage: 'User sleep' /mysqldata/percona-server-locks-detail-5.7.22/sql/item_func.cc:6057`
- `T@3: | | | | | | | | | | | | | >PROFILING::status_change`
- `T@3: | | | | | | | | | | | | | <PROFILING::status_change 384`
- `T@3: | | | | | | | | | | | | <THD::enter_cond 3405`
这里看出 sleep 的生效点实际上每次 Innodb 层返回一行数据经过 where 条件判断后，再触发 sleep 函数，也就是每行经过 where 条件过滤的数据在发送给客户端之前都会进行一次 sleep 操作。这个时候实际上该打开表的和该上 MDL LOCK 的都已经完成了，因此使用 sleep 函数来模拟大表 select 操作导致的 FTWRL 堵塞是可以的。
**三、FTWRL 做了什么工作**实际上这部分我们可以在函数 mysql_execute_command 寻找 case SQLCOM_FLUSH 的部分，实际上主要调用函数为 reload_acl_and_cache，其中核心部分为：- `if (thd->global_read_lock.lock_global_read_lock(thd))//加 MDL GLOBAL 级别S锁`
- `    return 1;                               // Killed`
- `      if (close_cached_tables(thd, tables, //关闭表操作释放 share 和 cache`
- `                 ((options & REFRESH_FAST) ?  FALSE : TRUE),`
- `                 thd->variables.lock_wait_timeout)) //等待时间受lock_wait_timeout影响`
- `      {`
- `        /*`
- `          NOTE: my_error() has been already called by reopen_tables() within`
- `          close_cached_tables().`
- `        */`
- `        result= 1;`
- `      }`
- 
- `      if (thd->global_read_lock.make_global_read_lock_block_commit(thd)) // MDL COMMIT 锁`
- `      {`
- `        /* Don't leave things in a half-locked state */`
- `        thd->global_read_lock.unlock_global_read_lock(thd);`
- `        return 1;`
- `      }`
更具体的关闭表的操作和释放 table 缓存的部分包含在函数 close_cached_tables 中，我就不详细写了。
但是我们需要明白 table 缓存实际上包含两个部分：- table cache define：每一个表第一次打开的时候都会建立一个静态的表定义结构内存，当多个会话同时访问同一个表的时候，从这里拷贝成相应的 instance 供会话自己使用。由参数 table_definition_cache 定义大小，由状态值 Open_table_definitions查看当前使用的个数。对应函数 get_table_share。
- table cache instance：同上所述，这是会话实际使用的表定义结构是一个instance。由参数 table_open_cache 定义大小，由状态值 Open_tables 查看当前使用的个数。对应函数 open_table_from_share。
这里我统称为 table 缓存，好了下面是我总结的 FTWRL 的大概步骤：**第一步：**加 MDL LOCK 类型为 GLOBAL 级别为 S 。如果出现等待状态为 Waiting for global read lock 。注意 select 语句不会上 GLOBAL 级别上锁，但是 DML/DDL/FOR UPDATE 语句会上 GLOBAL 级别的 IX 锁，IX 锁和 S 锁不兼容会出现这种等待。下面是这个兼容矩阵：- `          | Type of active   |`
- `  Request |   scoped lock    |`
- `   type   | IS(*)  IX   S  X |`
- ` ---------+------------------+`
- ` IS       |  +      +   +  + |`
- ` IX       |  +      +   -  - |`
- ` S        |  +      -   +  - |`
- ` X        |  +      -   -  - |`
**第二步：**推进全局表缓存版本。源码中就是一个全局变量 refresh_version++。
**第三步：**释放没有使用的 table 缓存。可自行参考函数 close_cached_tables 函数。
**第四步：**判断是否有正在占用的 table 缓存，如果有则等待，等待占用者释放。等待状态为 Waiting for table flush 。这一步会去判断 table 缓存的版本和全局表缓存版本是否匹配，如果不匹配则等待如下：- `for (uint idx=0 ; idx < table_def_cache.records ; idx++)`
- `      {`
- `        share= (TABLE_SHARE*) my_hash_element(&table_def_cache, idx); //寻找整个 table cache shared hash结构`
- `        if (share->has_old_version()) //如果版本 和 当前 的 refresh_version 版本不一致`
- `        {`
- `          found= TRUE;`
- `          break; //跳出第一层查找 是否有老版本 存在`
- `        }`
- `      }`
- `...`
- `if (found)//如果找到老版本，需要等待`
- `    {`
- `      /*`
- `        The method below temporarily unlocks LOCK_open and frees`
- `        share's memory.`
- `      */`
- `      if (share->wait_for_old_version(thd, &abstime,`
- `                                    MDL_wait_for_subgraph::DEADLOCK_WEIGHT_DDL))`
- `      {`
- `        mysql_mutex_unlock(&LOCK_open);`
- `        result= TRUE;`
- `        goto err_with_reopen;`
- `      }`
- `    }`
而等待的结束就是占用的 table 缓存的占用者释放，这个释放操作存在于函数 close_thread_table 中，如下：- `if (table->s->has_old_version() || table->needs_reopen() ||`
- `      table_def_shutdown_in_progress)`
- `  {`
- `    tc->remove_table(table);//关闭 table cache instance`
- `    mysql_mutex_lock(&LOCK_open);`
- `    intern_close_table(table);//去掉 table cache define`
- `    mysql_mutex_unlock(&LOCK_open);`
- `  }`
最终会调用函数 MDL_wait::set_status 将 FTWRL 唤醒，也就是说对于正在占用的 table 缓存而言，释放者不是 FTWRL 会话线程而是占用者自己的会话线程 。不管怎么样最终整个 table 缓存将会被清空，如果经过 FTWRL 后去查看 Open_table_definitions 和 Open_tables 将会发现重新计数了。下面是唤醒函数的代码，也很明显：- `bool MDL_wait::set_status(enum_wait_status status_arg) open_table`
- `{`
- `  bool was_occupied= TRUE;`
- `  mysql_mutex_lock(&m_LOCK_wait_status);`
- `  if (m_wait_status == EMPTY)`
- `  {`
- `    was_occupied= FALSE;`
- `    m_wait_status= status_arg;`
- `    mysql_cond_signal(&m_COND_wait_status);//唤醒`
- `  }`
- `  mysql_mutex_unlock(&m_LOCK_wait_status);//解锁`
- `  return was_occupied;`
- `}`
**第五步：**加 MDL LOCK 类型 COMMIT 级别为 S 。如果出现等待状态为 Waiting for commit lock 。如果有大事务的提交很可能出现这种等待。
**四、案例 1 解析**步骤1：我们使用 select for update 语句，这个语句会加 GLOBAL 级别的 IX 锁，持续到语句结束（注意实际上还会加对象级别的 MDL_SHARED_WRITE(SW) 锁持续到事务结束，和 FTWRL 无关不做描述）步骤2：我们使用 FTWRL 语句，根据上面的分析需要获取 GLOBAL 级别的 S 锁，不兼容，因此出现了等待 Waiting for global read lock 。步骤3：我们 KILL 掉了 FTWRL 会话，这种情况下会话退出，FTWRL 就像没有执行过一样不会有任何影响，因为它在第一步就堵塞了。步骤4：我们的 select 操作不会受到任何影响，因为在 GLOBAL 级别 select 不会加 MDL LOCK ，对象级别 MDL LOCK select/select for update 是兼容的（即 MDL_SHARED_READ(SR) 和 MDL_SHARED_WRITE(SW) 兼容），且 FTWRL 还没有执行实际的操作。
**五、案例 2 解析**步骤1：我们使用 select 语句，这个语句不会在 GLOBAL 级别上任何的锁（注意实际上还会加对象级别的 MDL_SHARED_READ(SR) 锁持续到事务结束，和 FTWRL 无关不做描述）步骤2：我们使用 FTWRL 语句，根据上面的分析我们发现 FTWRL 语句可以获取了 GLOBAL 级别的S锁，因为单纯的 select 语句不会在 GLOBAL 级别上任何锁。同时会将全局表缓存版本推进然后释放掉没有使用的 table 缓存。但是在第三节的第四步中我们发现因为 baguait1 的表缓存正在被占用，因此出现了等待，等待状态为 Waiting for table flush 。步骤3：我们 KILL 掉了 FTWRL 会话，这种情况下虽然 GLOBAL 级别的 S 锁会释放，**但是全局表缓存版本已经推进了**，同时没有使用的 table 缓存已经释放掉了。步骤4：再次执行一个 baguait1 表上的 select 查询操作，**这个时候在打开表的时候会去判断是否 table 缓存的版本和全局表缓存版本匹配如果不匹配进入等待，等待为 Waiting for table flush ，**下面是这个判断：- `if (share->has_old_version())`
- `    {`
- `      /*`
- `        We already have an MDL lock. But we have encountered an old`
- `        version of table in the table definition cache which is possible`
- `        when someone changes the table version directly in the cache`
- `        without acquiring a metadata lock (e.g. this can happen during`
- `        "rolling" FLUSH TABLE(S)).`
- `        Release our reference to share, wait until old version of`
- `        share goes away and then try to get new version of table share.`
- `      */`
- `      release_table_share(share);`
- `     ...`
- `      wait_result= tdc_wait_for_old_version(thd, table_list->db,`
- `                                            table_list->table_name,`
- `                                            ot_ctx->get_timeout(),`
- `                                            deadlock_weight);`
整个等待操作和 FTWRL 一样，会等待占用者释放 table 缓存后才会醒来继续。因此后续本表的所有 select/DML/DDL 都会堵塞，代价极高，即便 KILL 掉 FTWRL 会话也无用。
**六、FTWRL 堵塞和被堵塞的简单总结**（1）被什么堵塞- 长时间的 DDL\DML\FOR UPDATE 堵塞 FTWRL ，因为 FTWRL 需要获取 GLOBAL 的 S 锁，而这些语句都会对 GLOBAL 持有 IX（MDL_INTENTION_EXCLUSIVE） 锁，根据兼容矩阵不兼容。等待为：Waiting for global read lock 。本文的案例 1 就是这种情况。
- 长时间的 select 堵塞 FTWRL ， 因为 FTWRL 会释放所有空闲的 table 缓存，如果有占用者占用某些 table 缓存，则会等待占用者自己释放这些 table 缓存。等待为：Waiting for table flush 。本文的案例 2 就是这种情况，会堵塞随后关于本表的任何语句，即便 KILL FTWRL 会话也不行，除非 KILL 掉长时间的 select 操作才行。实际上 flush table 也会存在这种堵塞情况。
- 长时间的 commit(如大事务提交)也会堵塞 FTWRL ，因为 FTWRL 需要获取 COMMIT 的 S 锁，而 commit 语句会对 commit 持有 IX（MDL_INTENTION_EXCLUSIVE）锁，根据兼容矩阵不兼容。等待为 Waiting for commit lock 。
（2）堵塞什么- FTWRL 会堵塞 DDL\DML\FOR UPDATE 操作，堵塞点为 GLOBAL 级别的 S 锁，等待为：Waiting for global read lock 。
- FTWRL 会堵塞 commit 操作，堵塞点为 COMMIT 的 S 锁，等待为 Waiting for commit lock 。
- FTWRL 不会堵塞 select 操作，因为 select 不会在 GLOBAL 级别上锁。
**最后提醒一下很多备份工具都要执行 FTWRL 操作，一定要注意它的堵塞/被堵塞场景和特殊场景。**
**备注栈帧和断点：**（1）使用的断点
- MDL_context::acquire_lock 获取 DML LOCK
- open_table_from_share 获取 table cache instance
- alloc_table_share 分配 table define（share）
- get_table_share 获取 table define（share）
- close_cached_tables flush table 关闭全部 table cache instance 和 table define
- reload_acl_and_cache flush with read lock 进行 MDL LOCK 加锁为 GLOBAL TYPE:S ,同时调用 close_cached_tables 同时获取 COMMIT 级别 TYPE S
- MDL_wait::set_status 唤醒操作
- close_thread_table 占用者判断释放
- my_hash_delete hash 删除操作，从 table cache instance 和 table define 中释放 table 缓存都是需要调用这个删除操作的。
（2）FTWRL 堵塞栈帧由于 select 堵塞栈帧：- `(gdb) bt`
- `#0  0x00007ffff7bd3a5e in pthread_cond_timedwait@@GLIBC_2.3.2 () from /lib64/libpthread.so.0`
- `#1  0x000000000192027b in native_cond_timedwait (cond=0x7ffedc007c78, mutex=0x7ffedc007c30, abstime=0x7fffec5bbb90)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/include/thr_cond.h:129`
- `#2  0x00000000019205ea in safe_cond_timedwait (cond=0x7ffedc007c78, mp=0x7ffedc007c08, abstime=0x7fffec5bbb90,`
- `    file=0x204cdd0 "/mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc", line=1899) at /mysqldata/percona-server-locks-detail-5.7.22/mysys/thr_cond.c:88`
- `#3  0x00000000014b9f21 in my_cond_timedwait (cond=0x7ffedc007c78, mp=0x7ffedc007c08, abstime=0x7fffec5bbb90,`
- `    file=0x204cdd0 "/mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc", line=1899) at /mysqldata/percona-server-locks-detail-5.7.22/include/thr_cond.h:180`
- `#4  0x00000000014ba484 in inline_mysql_cond_timedwait (that=0x7ffedc007c78, mutex=0x7ffedc007c08, abstime=0x7fffec5bbb90,`
- `    src_file=0x204cdd0 "/mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc", src_line=1899)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/include/mysql/psi/mysql_thread.h:1229`
- `#5  0x00000000014bb702 in MDL_wait::timed_wait (this=0x7ffedc007c08, owner=0x7ffedc007b70, abs_timeout=0x7fffec5bbb90, set_status_on_timeout=true,`
- `    wait_state_name=0x2d897b0) at /mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc:1899`
- `#6  0x00000000016cdb30 in TABLE_SHARE::wait_for_old_version (this=0x7ffee0a4fc30, thd=0x7ffedc007b70, abstime=0x7fffec5bbb90, deadlock_weight=100)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/table.cc:4717`
- `#7  0x000000000153829b in close_cached_tables (thd=0x7ffedc007b70, tables=0x0, wait_for_refresh=true, timeout=31536000)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:1291`
- `#8  0x00000000016123ec in reload_acl_and_cache (thd=0x7ffedc007b70, options=16388, tables=0x0, write_to_binlog=0x7fffec5bc9dc)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_reload.cc:224`
- `#9  0x00000000015cee9c in mysql_execute_command (thd=0x7ffedc007b70, first_level=true) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:4433`
- `#10 0x00000000015d2fde in mysql_parse (thd=0x7ffedc007b70, parser_state=0x7fffec5bd600) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:5901`
- `#11 0x00000000015c6b72 in dispatch_command (thd=0x7ffedc007b70, com_data=0x7fffec5bdd70, command=COM_QUERY)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:1490`
（3）杀点 FTWRL 会话后其他 select 操作等待栈帧：
- `#0  MDL_wait::timed_wait (this=0x7ffee8008298, owner=0x7ffee8008200, abs_timeout=0x7fffec58a600, set_status_on_timeout=true, wait_state_name=0x2d897b0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc:1888`
- `#1  0x00000000016cdb30 in TABLE_SHARE::wait_for_old_version (this=0x7ffee0011620, thd=0x7ffee8008200, abstime=0x7fffec58a600, deadlock_weight=0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/table.cc:4717`
- `#2  0x000000000153b6ba in tdc_wait_for_old_version (thd=0x7ffee8008200, db=0x7ffee80014a0 "testmts", table_name=0x7ffee80014a8 "tii", wait_timeout=31536000,`
- `    deadlock_weight=0) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:2957`
- `#3  0x000000000153ca97 in open_table (thd=0x7ffee8008200, table_list=0x7ffee8001708, ot_ctx=0x7fffec58aab0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:3548`
- `#4  0x000000000153f904 in open_and_process_table (thd=0x7ffee8008200, lex=0x7ffee800a830, tables=0x7ffee8001708, counter=0x7ffee800a8f0, flags=0,`
- `    prelocking_strategy=0x7fffec58abe0, has_prelocking_list=false, ot_ctx=0x7fffec58aab0) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:5213`
- `#5  0x0000000001540a58 in open_tables (thd=0x7ffee8008200, start=0x7fffec58aba0, counter=0x7ffee800a8f0, flags=0, prelocking_strategy=0x7fffec58abe0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:5831`
- `#6  0x0000000001541e93 in open_tables_for_query (thd=0x7ffee8008200, tables=0x7ffee8001708, flags=0)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:6606`
- `#7  0x00000000015d1dca in execute_sqlcom_select (thd=0x7ffee8008200, all_tables=0x7ffee8001708) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:5416`
- `#8  0x00000000015ca380 in mysql_execute_command (thd=0x7ffee8008200, first_level=true) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:2939`
- `#9  0x00000000015d2fde in mysql_parse (thd=0x7ffee8008200, parser_state=0x7fffec58c600) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:5901`
- `#10 0x00000000015c6b72 in dispatch_command (thd=0x7ffee8008200, com_data=0x7fffec58cd70, command=COM_QUERY)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:1490`
（4）占用者释放唤醒 FTWRL 栈帧：- `Breakpoint 3, MDL_wait::set_status (this=0x7ffedc000c78, status_arg=MDL_wait::GRANTED) at /mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc:1832`
- `1832      bool was_occupied= TRUE;`
- `(gdb) bt`
- `#0  MDL_wait::set_status (this=0x7ffedc000c78, status_arg=MDL_wait::GRANTED) at /mysqldata/percona-server-locks-detail-5.7.22/sql/mdl.cc:1832`
- `#1  0x00000000016c2483 in free_table_share (share=0x7ffee0011620) at /mysqldata/percona-server-locks-detail-5.7.22/sql/table.cc:607`
- `#2  0x0000000001536a22 in table_def_free_entry (share=0x7ffee0011620) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:524`
- `#3  0x00000000018fd7aa in my_hash_delete (hash=0x2e4cfe0, record=0x7ffee0011620 "\002") at /mysqldata/percona-server-locks-detail-5.7.22/mysys/hash.c:625`
- `#4  0x0000000001537673 in release_table_share (share=0x7ffee0011620) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:949`
- `#5  0x00000000016cad10 in closefrm (table=0x7ffee000f280, free_share=true) at /mysqldata/percona-server-locks-detail-5.7.22/sql/table.cc:3597`
- `#6  0x0000000001537d0e in intern_close_table (table=0x7ffee000f280) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:1109`
- `#7  0x0000000001539054 in close_thread_table (thd=0x7ffee0000c00, table_ptr=0x7ffee0000c68) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:1780`
- `#8  0x00000000015385fe in close_open_tables (thd=0x7ffee0000c00) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:1443`
- `#9  0x0000000001538d4a in close_thread_tables (thd=0x7ffee0000c00) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_base.cc:1722`
- `#10 0x00000000015d19bc in mysql_execute_command (thd=0x7ffee0000c00, first_level=true) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:5307`
- `#11 0x00000000015d2fde in mysql_parse (thd=0x7ffee0000c00, parser_state=0x7fffec5ee600) at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:5901`
- `#12 0x00000000015c6b72 in dispatch_command (thd=0x7ffee0000c00, com_data=0x7fffec5eed70, command=COM_QUERY)`
- `    at /mysqldata/percona-server-locks-detail-5.7.22/sql/sql_parse.cc:1490`
最后推荐高鹏的专栏《深入理解MySQL主从原理 32讲》，想要透彻了解学习MySQL 主从原理的朋友不容错过。
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