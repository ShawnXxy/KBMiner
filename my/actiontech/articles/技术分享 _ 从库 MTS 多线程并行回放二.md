# 技术分享 | 从库 MTS 多线程并行回放（二）

**原文链接**: https://opensource.actionsky.com/20200220-mts/
**分类**: 技术干货
**发布时间**: 2020-02-20T02:20:10-08:00

---

> **作者：****高鹏**
文章末尾有他著作的《深入理解 MySQL 主从原理 32 讲》，深入透彻理解 MySQL 主从，GTID 相关技术知识。
**本节包含一个笔记，链接如下：****https://www.jianshu.com/p/e920a6d33005**
这一节会先描述 MTS 的工作线程执行 Event 的大概流程。然后重点描述一下 MTS 中检查点的概念。在后面的第 25 节我们可以看到，MTS 的异常恢复很多情况下需要依赖这个检查点，从检查点位置开始扫描 relay log 做恢复操作，但是在 GTID AUTO_POSITION MODE 模式且设置了 recovery_relay_log=1 的情况下这种依赖将会弱化。
**一、工作线程执行 Event**
前面我们已经讨论了协调线程分发 Event 的规则，实际上协调线程只是将 Event 分发到了工作线程的执行队列中。那么工作线程执行 Event 就需要从执行队列中拿出这些 Event，然后进行执行。整个过程可以参考函数 slave_worker_exec_job_group。因为这个流程比较简单，因此就不需要画图了，但是我们需要关注一些点如下：
（1）从执行队列中读取 Event。注意这里如果执行队列中没有 Event 那么就进入空闲等待，也就是工作线程处于无事可做的状态，等待状态为 ‘Waiting for an event from Coordinator’。
（2）如果执行到 XID_EVENT 那么说明事务已经结束了那么需要完成内存信息更新操作。可参考 Slave_worker::slave_worker_exec_event 和 Xid_apply_log_event::do_apply_event_worker 函数。更新内存相关信息可参考函数 commit_positions 函数。下面是一些更新的信息，我们可以看到和 slave_worker_info 表中的信息基本一致，如下：
- `1、更新当前信息`
- `strmake(group_relay_log_name, ptr_g->group_relay_log_name,`
- `sizeof(group_relay_log_name) - 1);`
- `group_relay_log_pos= ev->future_event_relay_log_pos;`
- `set_group_master_log_pos(ev->common_header->log_pos);`
- `set_group_master_log_name(c_rli->get_group_master_log_name());`
- 
- `2、将检查点信息进行写入：`
- `strmake(checkpoint_relay_log_name, ptr_g-`
- `>checkpoint_relay_log_name,sizeof(checkpoint_relay_log_name) - 1);`
- `checkpoint_relay_log_pos= ptr_g->checkpoint_relay_log_pos;`
- `strmake(checkpoint_master_log_name, ptr_g-`
- `>checkpoint_log_name,sizeof(checkpoint_master_log_name) - 1);`
- `checkpoint_master_log_pos= ptr_g->checkpoint_log_pos;`
- 
- `3、设置GAQ序号：`
- ` checkpoint_seqno= ptr_g->checkpoint_seqno;`
- `更新整个BITMAP，可能已经由检查点进行GAQ出队：`
- `for (uint pos= ptr_g->shifted; pos < c_rli->checkpoint_group; pos++)`
- `//重新设置位图 因为checkpoint已经`
- `{`
- `//ptr_g->shifted是GAQ中出队的事务个数`
- `if (bitmap_is_set(&group_shifted, pos))`
- `//这里就需要偏移掉出队的事务，恢复已经不需要了`
- `bitmap_set_bit(&group_executed, pos - ptr_g->shifted);`
- `}`
- `4、设置位图：`
- `bitmap_set_bit(&group_executed, ptr_g->checkpoint_seqno);`
- `//在本次事务相应的位置设置为1`
（3）如果执行到 XID_EVENT 那么说明事务已经结束了那么需要完成内存信息的持久化，即强制刷内存信息持久化到 slave_worker_info 表中（relay_log_info_repository 设置为TABLE）。可参考函数 commit_positions 函数，如下：
- `if ((error= w->commit_positions(this, ptr_group,`
- `w->is_transactional())))`
（4）如果执行到 XID_EVENT 还需要进行事务的提交操作，也就是进行 Innodb 层事务的提交。
从上面我们可以看到 MTS 中每次事务的提交并不会更新 slave_relay_log_info 表，而是进行 slave_worker_info 表的更新，将最新的信息写入到 slave_worker_info 表中。
我们前面也说过 SQL 线程已经蜕变为协调线程，那么 slave_relay_log_info 表什么时候更新呢？下面我们就能看到 slave_relay_log_info 表的更新实际上由协调线程在做完检查点之后更新。
**二、MTS 中检查点中的重要概念**
总的说来 MTS 中的检查点是 MTS 进行异常恢复的起点。实际上就是代表到这个位置之前（包含自身）事务都是已经在从库执行过了，但之后的事务可能执行完成了也可能没有执行完成。检查点由协调线程进行。
**（1）协调线程的 GAQ 队列**前面我们已经知道 MTS 中为每个工作线程维护了一个 Event 的分发队列。除此之外协调线程还维护了一个非常的重要的队列 GAQ，它是一个环形队列。下面是源码中的定义：
- `/*`
- `  master-binlog ordered queue of Slave_job_group descriptors of groups`
- `  that are under processing. The queue size is @c checkpoint_group. Group assigned`
- `*/`
- `Slave_committed_queue *gaq;`
每次协调线程分发事务的时候都会将事务记录到 GAQ 队列中，因此 GAQ 中事务的顺序总是和 relay log 文件中事务的顺序一致的。检查点正是作用在 GAQ 队列上的，每次检查点的位置称为 LWM，还记得上一节我叫大家先忽略的 LWM 吗？就是这个。源码中定义也正是如此，它在 GAQ 队列中进行维护。如下：
- `/*`
- `   The last checkpoint time Low-Water-Mark`
- `*/`
- `Slave_job_group lwm;`
在 GAQ 队列中还维护有一个叫做 checkpoint_seqno 的序号，它是最后一次检查点以来每个分配事务的序号，下面是源码中的定义：
- `uint checkpoint_seqno;  // counter of groups executed after the most recent CP`
在协调线程读取到 GTIDLOGEVENT 后为其分配序号，记作 checkpoint_seqno，如下：
- `rli->checkpoint_seqno++;//增加seqno`
当协调线程进行检查点的时候 checkpoint_seqno 序号会减去出队的事务数量，如下：
- `checkpoint_seqno= checkpoint_seqno - shift; //这里减去出队的事务`
在 MTS 异常恢复的时候也会用到这个序号，每个工作线程会通过这个序号来确认本工作线程执行事务的上限，如下：
- `      for (uint i= (w->checkpoint_seqno + 1) - recovery_group_cnt,`
- `                 j= 0; i <= w->checkpoint_seqno; i++, j++)`
- `            {`
- `              if (bitmap_is_set(&w->group_executed, i))`
- `//如果这一位 已经设置`
- `              {`
- `                DBUG_PRINT("mts", ("Setting bit %u.", j));`
- `                bitmap_fast_test_and_set(groups, j);`
- `//那么GTOUPS 这个 bitmap中应该设置，最终GTOUPS会包含全的需要恢复的事务`
- `              }`
- `            }`
关于详细的异常恢复流程将在第 25 节描述。
**（2）工作线程的 Bitmap**有了 GAQ 队列和检查点就知道异常恢复开始的位置了。但是我们并不知道每一个工作线程都完成了哪些事务，哪些又没有执行完成，因此就不能确认哪些事务需要恢复。在 MTS 中并行回放事务的提交并不是按分发顺序的进行的，某些大事务（或者其他原因比锁堵塞）可能迟迟不能提交，而一些小事务却会很快提交完成。这些迟迟不能提交的事务就成为了所谓的 &#8216;gap&#8217;，如果使用了 GTID 那么在查看已经执行 GTID SET 的时候可能出现一些‘空洞’，为了防止 &#8216;gap&#8217; 的发生通常需要设置参数 slave_preserve_commit_order。下一节我们将会看到这种‘空洞’以及 slave_preserve_commit_order 的作用。但是如果要设置了 slave_preserve_commit_order 参数就需要开启从库记录 binary log 的功能，因此必须开启 log_slave_updates 参数。下面是源码的判断：
- `  if (opt_slave_preserve_commit_order && rli->opt_slave_parallel_workers > 0 &&`
- `      opt_bin_log && opt_log_slave_updates)`
- `    commit_order_mngr= new Commit_order_manager(rli->opt_slave_parallel_workers);`
- `//order commit 管理器`
这里先提前说一下 MTS 恢复的会有两个关键阶段：
- 扫描阶段通过扫描检查点以后的 relay log。通过每个工作线程的 Bitmap 区分出哪些事务已经执行完成，哪些事务没有执行完成，并且汇总形成恢复 Bitmap，同时得到需要恢复的事务总量。
- 执行阶段
通过这个汇总的恢复 Bitmap，将这些没有执行完成事务读取 relay log 再次执行。
这个 Bitmap 位图和 GAQ 中的事务一一对应。当执行 XID_EVENT 完成提交后这一位将会被设置为 ‘1’。
**（3）协调线程信息的持久化**
这个已经在前面提到过，实际上每次进行检查点的时候都需要将检查点的位置固化到 slave_relay_log_info 表中（relay_log_info_repository 设置为 TABLE）。因此 slave_relay_log_info 中存储的实际上不是实时的信息而是检查点的信息。下面就是 slave_relay_log_info 表的表结构：
- `mysql> desc slave_relay_log_info;`
- `+-------------------+---------------------+------+-----+---------+-------+`
- `| Field             | Type                | Null | Key | Default | Extra |`
- `+-------------------+---------------------+------+-----+---------+-------+`
- `| Number_of_lines   | int(10) unsigned    | NO   |     | NULL    |       |`
- `| Relay_log_name    | text                | NO   |     | NULL    |       |`
- `| Relay_log_pos     | bigint(20) unsigned | NO   |     | NULL    |       |`
- `| Master_log_name   | text                | NO   |     | NULL    |       |`
- `| Master_log_pos    | bigint(20) unsigned | NO   |     | NULL    |       |`
- `| Sql_delay         | int(11)             | NO   |     | NULL    |       |`
- `| Number_of_workers | int(10) unsigned    | NO   |     | NULL    |       |`
- `| Id                | int(10) unsigned    | NO   |     | NULL    |       |`
- `| Channel_name      | char(64)            | NO   | PRI | NULL    |       |`
- `+-------------------+---------------------+------+-----+---------+-------+`
与此同时 show slave status 中的某些信息也是检查点的内存信息。下面的信息将是来自检查点：- Relay_Log_File：最新一次检查点的 relay log 文件名。
- Relay_Log_Pos：最新一次检查点的 relay log 位点。
- Relay_Master_Log_File：最新一次检查点的主库 binary log 文件名。
- Exec_Master_Log_Pos：最新一次检查点的主库 binary log 位点。
- Seconds_Behind_Master：根据检查点指向事务的提交时间计算的延迟。
需要注意的是我们的 GTID 模块独立在这一套理论之外，在第 3 节我们讲 GTID 模块的初始化的时候我们就说过 GTID 模块的初始化是在从库信息初始化之前就完成了。因此在做 MTS 异常恢复的时候使用 GTID AUTO_POSITION MODE 模式将会变得更加简单和安全，细节将在第 25 节描述。
**（4）工作线程信息的持久化**工作线程的信息就持久化在 slave_worker_info 表中，前面我们描述工作线程执行 Event 注意点的时候已经做了相应的描述。执行 XID_EVENT 完成事务提交之后会将信息写入到 slave_worker_info 表中（relay_log_info_repository 设置为 TABLE）。其中包括信息：
- Relay_log_name：工作线程最后一个提交事务的 relay log 文件名。
- Relay_log_pos：工作线程最后一个提交事务的 relay log 位点。
- Master_log_name：工作线程最后一个提交事务的主库 binary log 文件名。
- Master_log_pos：工作线程最后一个提交事务的主库 binary log 文件位点。
- Checkpoint_relay_log_name：工作线程最后一个提交事务对应检查点的 relay log 文件名。
- Checkpoint_relay_log_pos：工作线程最后一个提交事务对应检查点的 relay log 位点。
- Checkpoint_master_log_name：工作线程最后一个提交事务对应检查点的主库 binary log 文件名。
- Checkpoint_master_log_pos：工作线程最后一个提交事务对应检查点的主库 binary log 位点。
- Checkpoint_seqno：工作线程最后一个提交事务对应 checkpoint_seqno 序号。
- Checkpoint_group_size：工作线程的 Bitmap 字节数，约等于 GAQ 队列大小 /8，因为 1 个字节为 8 位。
- Checkpoint_group_bitmap：工作线程对应的 Bitmap 位图信息。
关于 Checkpoint_group_size 的换算参考函数 Slave_worker::write_info。
**（5）两个参数**- slave_checkpoint_group：GAQ 队列大小。
- slave_checkpoint_period：多久执行一次检查点，默认 300 毫秒。
**（6）检查点执行的时机**- 超过 slave_checkpoint_period 配置。可参考 next_event 函数如下：
- `if (rli->is_parallel_exec() && (opt_mts_checkpoint_period != 0 || force))`
- `{`
- `ulonglong period= static_cast<ulonglong>(opt_mts_checkpoint_period * 1000000ULL);`
- `...`
- `(void) mts_checkpoint_routine(rli, period, force, true/*need_data_lock=true*/);`
- `...`
- `      }`
- 达到 GAQ 队列已满，如下：
- ` //如果达到了 GAQ的大小 设置为force 强制checkpoint`
- `bool force= (rli->checkpoint_seqno > (rli->checkpoint_group - 1));`
- 正常stop slave。
**（7）一个列子**通常有压力的情况下的 slave_worker_info 中的所有工作线程最大的 Checkpoint_master_log_pos 应该和 slave_relay_log_info 中的 Master_log_pos 相等，因为这是最后一个检查点的位点信息，如下：
![](https://opensource.actionsky.com/wp-content/uploads/2020/02/图1-1024x274.png)											
**三、MTS 中的检查点的流程**
这一部分将详细描述一下检查点的步骤，关于检查点可以参考函数 mts_checkpoint_routine。
假设现在有 7 个事务是可以并行执行的，工作线程数量为 4 个。当前协调线程已经分发了 5 个，前面 4 个事务都已经执行完成，其中第 5 的一个事务是大事务。那么可能当前的状态图如下：
![](https://opensource.actionsky.com/wp-content/uploads/2020/02/图2-1024x996.png)											
前面 4 个事务每个工作线程都分到一个，最后一个大事务这里假设由工作线程 2 进行执行，图中用红色部分表示。
**（1）判断是超过了 slave_checkpoint_period 设置的大小，如果超过需要进行检查点。**- `  if (!force && diff < period)`
- `//是否需要进行检查点是否超过了slave_checkpoint_period的设置`
- `  {`
- `    /*`
- `      We do not need to execute the checkpoint now because`
- `      the time elapsed is not enough.`
- `    */`
- `    DBUG_RETURN(FALSE);`
- `  }`
**（2）扫描 GAQ 队列进行出队操作，直到第一个没有提交的事务为止。图中红色部分就是一个大事务，检查点只能停留在它之前。**- `cnt= rli->gaq->move_queue_head(&rli->workers);`
- `//work数组 返回出队的个数`
move_queue_head 部分代码如下：
- `    if (ptr_g->worker_id == MTS_WORKER_UNDEF ||`
- `        my_atomic_load32(&ptr_g->done) == 0)`
- `//当前GROUP是否已经执行完成 如果没有执行完成就需要 停止本次检查点`
- `      break; /* 'gap' at i'th */`
**（3）更新内存和 relay_log_info_repository 表的信息为本次检查点指向的位置。**先更新内存信息，也就是我们 show slave status 中看到的信息：
- `rli->set_group_master_log_pos(rli->gaq->lwm.group_master_log_pos);`
- `rli->set_group_relay_log_pos(rli->gaq->lwm.group_relay_log_pos);`
- `rli->set_group_relay_log_name(rli->gaq->lwm.group_relay_log_name);`
然后强制写入表 slave_relay_log_info 中：
- `error= rli->flush_info(TRUE);`
- `//将本次检查点信息 写入到relay_log_info_repository表中`
**（4）更新 last_master_timestamp 信息为检查点位置事务的 XID_EVENT 的 timstamp 值。**
这个值在第 27 节中会详细描述，它是计算 Seconds_behind_master 的一个因素：
- `/*`
- `    Update the rli->last_master_timestamp for reporting correct Seconds_behind_master.`
- `    If GAQ is empty, set it to zero.`
- `    Else, update it with the timestamp of the first job of the Slave_job_queue`
- `    which was assigned in the Log_event::get_slave_worker() function.`
- `  */`
- `ts= rli->gaq->empty()? 0 : reinterpret_cast<Slave_job_group*>(rli->gaq->head_queue())->ts;`
- `//rli->gaq->head_queue 检查点位置的GROUP的时间`
- `rli->reset_notified_checkpoint(cnt, ts, need_data_lock, true);`
- `reset_notified_checkpoint函数中有：`
- `last_master_timestamp= new_ts;`
因此 MTS 中 Seconds_behind_master 的计算和检查点息息相关。
**（5）最后还会将前面 GAQ 出队的事务数量进行统计，因为每个工作线程需要根据这个值来进行 Bitmap 位图的偏移。并且还会维护我们前面说的 GAQ 的 checkpoint_seqno 值。**这个操作也是在函数 Relay_log_info::reset_notified_checkpoint 中完成的，实际上很简单部分代码如下：
- `for (Slave_worker **it= workers.begin(); it != workers.end(); ++it)`
- `//循环每个woker`
- `w->bitmap_shifted= w->bitmap_shifted + shift;`
- `//每个worker线程都会增加 这个偏移量`
- `checkpoint_seqno= checkpoint_seqno - shift;`
- `//这里减去 移动的个数`
到这里整个检查点的基本操作就完成了。我们看到实际上步骤并不多，拿到 Bitmap 偏移量后每个工作线程就会在随后的第一个事务提交的时候进行位图的偏移，checkpoint_seqno 计数也会更新。
我们前面的假设环境中，如果触发了一次检查点，并且协调线程将后两个可以并行的事务发给了工作线程 1 和 3 进行处理并且处理完成。那么我们的图会变成如下：
![](https://opensource.actionsky.com/wp-content/uploads/2020/02/图3-1024x935.png)											
这张图中我用不同样色表示了不同线条，因为它们交叉比较多。GAQ 中的红色事务就是我们假设的大事务它仍然没有执行完成，它也是我们所谓的 ‘gap’。如果这个时候 MySQL 实例异常重启，那么这个红色 ‘gap’ 就是我们启动后需要找到的事务，方式就是通过 Bitmap 位图进行比对，后面说异常恢复的时候再详细讨论。如果是开启了 GTID，这种 ‘gap’ 很容易就能观察到，下一节将进行测试。
同时我们需要注意这个时候工作线程 2 并没有分发新的事务执行，因为工作线程 2 没有执行完大事务， 因此在 slave_woker_info 表中它的信息仍然显示为上一次提交事务的信息。而工作线程 4 因为没有分配到新的事务，因此 slave_woker_info 表中它的信息也显示为上一次提交事务的信息。因此在 slave_woker_info 中工作线程 2 和工作线程 4 的检查点信息、Bitmap 信息、checkpoint_seqno 都是老的信息。
**总结**
好了，到这里我已经说明了 MTS 中三个关键点。
- 协调线程是根据什么规则进行事务分发的。
- 工作线程如何拿到分发的事务。
- MTS 中的检查点是如何进行的。
但是还有一个关键点没有说，就是前面多次提到的异常恢复，第 25 节将重点解释。
第 20 节结束。
最后推荐高鹏的专栏《深入理解 MySQL 主从原理 32 讲》，想要透彻了解学习 MySQL 主从原理的朋友不容错过。
作者微信：gp_22389860
![](.img/0aff2ace.jpg)