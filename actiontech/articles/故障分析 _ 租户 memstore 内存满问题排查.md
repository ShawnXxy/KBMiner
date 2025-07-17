# 故障分析 | 租户 memstore 内存满问题排查

**原文链接**: https://opensource.actionsky.com/20230428-oceanbase/
**分类**: 技术干货
**发布时间**: 2023-04-27T18:37:49-08:00

---

作者：操盛春
技术专家，任职于爱可生，专注研究 MySQL、OceanBase 源码。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文是对官方同名文档部分内容的解释，官方文档链接：
https://www.oceanbase.com/docs/enterprise-oceanbase-database-cn-10000000000362143
#### 一、检查冻结情况
##### 1.1 冻结功能是否正常？
以 tenant_id = 1001 租户为例，查询 __all_virtual_tenant_memstore_info 表：
-- 注意：where 条件中 tenant_id 需要修改成实际场景对应的值
select * from __all_virtual_tenant_memstore_info where tenant_id = 1001\G
*************************** 1. row ***************************
tenant_id: 1001
svr_ip: 10.186.17.106
svr_port: 22882
active_memstore_used: 1295451600
total_memstore_used: 1298137088
major_freeze_trigger: 8589934550
memstore_limit: 17179869150
freeze_cnt: 0
active_memstore_used 表示活跃状态的 MemTable 占用的内存，major_freeze_trigger 表示 memstore 占用内存达到 major_freeze_trigger 之后会触发转储（或合并）。
如果冻结功能正常，租户 memstore 占用内存到达 major_freeze_trigger 之后，就会先冻结、然后转储该租户下的 MemTable，转储完成的 MemTable 占用的内存会从 active_memstore_used 中减去。
冻结是转储或合并的前置操作，所以，先根据 active_memstore_used 和 major_freeze_trigger 的大小关系，判断冻结功能是否正常：
- active_memstore_used <= major_freeze_trigger，说明冻结功能正常，需要检查转储情况，参照 `2. 检查转储情况`小节。
- active_memstore_used > major_freeze_trigger，说明冻结功能不正常，需要查看冻结线程的情况，参照 `1.2 冻结线程是否正常工作？`小节。
##### 1.2 冻结线程是否正常工作？
可以执行以下命令判断负责冻结功能的线程是否在正常运行：
[admin@hostname log]$ grep "tenant manager timer task" observer.log
## 如果线程正常运行，会每 2s 输出一次：====== tenant manager timer task ======
[2023-02-16 08:13:47.952516] INFO  [COMMON] ob_tenant_mgr.cpp:207 [21537][2][Y0-0000000000000000] [lt=10] [dc=0] ====== tenant manager timer task ======
[2023-02-16 08:13:49.953761] INFO  [COMMON] ob_tenant_mgr.cpp:207 [21537][2][Y0-0000000000000000] [lt=9] [dc=0] ====== tenant manager timer task ======
[2023-02-16 08:13:51.955373] INFO  [COMMON] ob_tenant_mgr.cpp:207 [21537][2][Y0-0000000000000000] [lt=52] [dc=0] ====== tenant manager timer task ======
[2023-02-16 08:13:54.022403] INFO  [COMMON] ob_tenant_mgr.cpp:207 [21537][2][Y0-0000000000000000] [lt=21] [dc=0] ====== tenant manager timer task ======
[2023-02-16 08:13:56.023441] INFO  [COMMON] ob_tenant_mgr.cpp:207 [21537][2][Y0-0000000000000000] [lt=8] [dc=0] ====== tenant manager timer task ======
[2023-02-16 08:13:58.024985] INFO  [COMMON] ob_tenant_mgr.cpp:207 [21537][2][Y0-0000000000000000] [lt=9] [dc=0] ====== tenant manager timer task ======
...
如果日志中能够每 2s 正常输出信息：====== tenant manager timer task ======，说明负责冻结功能的线程正常运行，那就意味着是某些 MemTable 无法冻结，导致 memstore 占用内存超过 major_freeze_trigger。
这种情况下，需要查看有哪些没有冻结的 MemTable：
-- 注意：where 条件中 svr_ip、tenant_id 需要修改成实际场景对应的值
select a.table_name, b.table_id, b.partition_id, b.mt_base_version, b.mt_is_frozen, b.mt_protection_clock, b.mt_snapshot_version
from gv$table as a inner join __all_virtual_tenant_memstore_allocator_info as b
on a.table_id = b.table_id
where b.mt_is_frozen = 0 and b.svr_ip='10.186.17.106' and b.tenant_id = 1001
order by mt_protection_clock;
+------------+------------------+--------------+------------------+--------------+---------------------+---------------------+
| table_name | table_id         | partition_id | mt_base_version  | mt_is_frozen | mt_protection_clock | mt_snapshot_version |
+------------+------------------+--------------+------------------+--------------+---------------------+---------------------+
| t1         | 1100611139453777 |            0 | 1678500259180548 |            0 |                   0 | 9223372036854775807 |
| t4         | 1100611139453785 |            0 | 1678500010823930 |            0 |                   0 | 9223372036854775807 |
| t3         | 1100611139453781 |            0 | 1678945615601759 |            0 |           165599800 | 9223372036854775807 |
| t5         | 1100611139453787 |            0 | 1678500010823930 |            0 |           276698400 | 9223372036854775807 |
| t2         | 1100611139453778 |            0 | 1678500258966417 |            0 |           404566600 | 9223372036854775807 |
| t6         | 1100611139453789 |            0 | 1678945429338788 |            0 | 9223372036854775807 | 9223372036854775807 |
+------------+------------------+--------------+------------------+--------------+---------------------+---------------------+
mt_protection_clock 表示某个 MemTable 创建、转储、合并之后，进行增、删、改等操作第一次分配内存时，该 MemTable 所属租户 memstore 已占用内存。
> 按 mt_protection_clock 排序似乎没有什么特殊意义，可能只是为了方便查看而已。
mt_protection_clock = 9223372036854775807，是个特殊值。
某个 MemTable 转储或合并之后，它的 mt_protection_clock 会修改为 9223372036854775807，然后一直保持不变，直到转储或合并之后第一次分配内存，mt_protection_clock 才会发生变化。
如果转储或合并之后，MemTable 没有再分配过内存，mt_protection_clock 会一直保持为 9223372036854775807，重启 OB 之后也还是 9223372036854775807，直到接下来第一次分配内存，mt_protection_clock 的值才会发生变化。
因为租户 memstore 占用内存达到 freeze_trigger_percentage 对应的内存上限之后，会触发租户级别的转储，也就是该租户下的所有 MemTable 都会进行转储。基于这个前提，上面 SQL 语句查询出来的 mt_is_frozen 等于 0，并且 mt_protection_clock 不等于 9223372036854775807 的 MemTable 就有可能是冻结异常的表，需要逐个排查确认是否冻结异常。
**为什么是有可能冻结异常的表？**
因为有可能转储或合并之后，某些 MemTable 表又发生了 DML 操作，插入了新的数据，这种情况下，mt_is_frozen = 0、mt_protection_clock != 9223372036854775807 就是正常的了。
排除这种情况之后，剩下的 MemTable 就是冻结异常的表。
经过上面的一系列操作之后，如果找到了冻结异常的表，可以通过 table_id 查找对应的错误日志，以 table_id = 1100611139453778 为例：
## 进入 observer.log.wf 日志文件所在的目录
## 如果 OB 的 enable_syslog_wf = false，需要把 observer.log.wf 替换为 observer.log
grep 1100611139453778 observer.log.wf | grep -E "WARN|ERROR"
## 如果上面的命令没有找到错误日志，也可试试以下命令
grep "fail to do minor freeze" observer.log.wf | grep 1100611139453778
#### 二、检查转储情况
##### 2.1 转储功能是否正常？
以 tenant_id = 1001 租户为例，查询 __all_virtual_tenant_memstore_info 表：
> 检查转储情况作为检查冻结情况的下一个步骤，只有当冻结情况正常时，才要检查转储情况。这里所举例子和 1. 检查冻结情况中的例子是同一个，为了方便查看，就复制过来了。
-- 注意：where 条件中 tenant_id 需要修改成实际场景对应的值
select * from __all_virtual_tenant_memstore_info where tenant_id = 1001\G
*************************** 1. row ***************************
tenant_id: 1001
svr_ip: 10.186.17.106
svr_port: 22882
active_memstore_used: 1295451600
total_memstore_used: 1298137088
major_freeze_trigger: 8589934550
memstore_limit: 17179869150
freeze_cnt: 0
1.检查冻结情况小节介绍过，active_memstore_used <= major_freeze_trigger，说明冻结功能正常。
在此基础上，再判断 total_memstore_used 和 major_freeze_trigger 的关系：
- 如果 total_memstore_used <= major_freeze_trigger，说明转储功能正常，那就说明一切正常，不需要排查了。
- 如果 total_memstore_used > major_freeze_trigger，说明转储功能不正常，参照 2.2 及以后小节的内容。
##### 2.2 是否存在活跃事务？
如果是 OB 2.2.x 版本，可以通过以下 SQL 查询已冻结但未释放内存的 MemTable，是否因为存在活跃事务，导致转储调度异常，内存无法释放。
-- 注意：where 条件中 svr_ip、tenant_id 需要修改成实际场景对应的值
-- table_type = 0 表示 MEMTABLE
-- is_active = 0 表示 MEMTABLE 处于冻结状态，还未转储结束
-- 关于 is_active，参照官方文档：https://www.oceanbase.com/docs/enterprise-oceanbase-database-cn-10000000000364739
select * from __all_virtual_table_mgr as a
where a.table_type = 0 and a.is_active = 0 and a.trx_count > 0 and (a.table_id, a.partition_id) in (
select table_id, partition_id from __all_virtual_tenant_memstore_allocator_info
where svr_ip='10.186.17.106' and tenant_id=1001 and mt_is_frozen=1
)
如果上面 SQL 查询到了 MemTable，说明这些查出来的表上因为存在活跃事务，导致转储调度异常。
可以通过 __all_virtual_trans_stat 表，查看 MemTable 表的事务信息，以确定事务长时间处于活跃状态的原因。比如：大事务。
如果从 __all_virtual_trans_stat 表中没有得到有效信息，可以再从日志文件中查看上面 MemTable 相关的事务日志，需要根据哪些关键词过滤事务日志，官方文档没有写，后续再补充吧（已列入遗留问题列表）。
##### 2.3 从副本 clog 回放进度慢？
查看已冻结的 MemTable，是否因为 MemTable 的弱一致性读时间戳小于快照点（snapshot_version），导致 MemTable 转储调度异常，内存无法释放。
> 关于弱一致性读时间戳，参照官方文档：弱一致性读。(https://www.oceanbase.com/docs/enterprise-oceanbase-database-cn-10000000000944818)
> 为什么 MemTable 的弱一致性读时间戳小于快照点（snapshot_version）会导致该 MemTable 转储调度异常，我还没有弄清楚，咨询了官方还没有答复，后面搞清楚了再补充（已列入遗留问题列表）。
-- 注意：where 条件中 svr_ip、tenant_id 需要修改成实际场景对应的值
-- table_type = 0 表示 MEMTABLE
-- is_active = 0 表示 MEMTABLE 处于冻结状态，还未转储结束
-- 关于 is_active，参照官方文档：https://www.oceanbase.com/docs/enterprise-oceanbase-database-cn-10000000000364739
select 
a.svr_ip, a.table_id, a.partition_id, a.is_active, a.table_type, a.snapshot_version,
b.min_trans_service_ts, b.min_replay_engine_ts, b.min_log_service_ts
from __all_virtual_table_mgr as a inner join __all_virtual_partition_info as b
on a.table_id = b.table_id and a.partition_id = b.partition_idx and a.svr_ip = b.svr_ip
where a.table_type = 0 
and a.is_active = 0 
and a.snapshot_version > least(least(b.min_trans_service_ts, b.min_replay_engine_ts), b.min_log_service_ts)
and (a.table_id, a.partition_id) in (
select table_id, partition_id from __all_virtual_tenant_memstore_allocator_info
where svr_ip='10.186.17.106' and tenant_id=1001 and mt_is_frozen=1
);
> least(least(min_trans_service_ts, min_replay_engine_ts), min_log_service_ts) 表示取 min_trans_service_ts, min_replay_engine_ts, min_log_service_ts 3 个字段中的最小值。
如果上面 SQL 查询到了 MemTable，说明这些表的弱一致性读时间戳小于快照点（snapshot_version），接下来查看是否因为是否因为 clog 日志回放速度慢导致弱一致性读时间戳落后比较多。
-- 用上面的 SQL（select 子句中只保留了 table_id、partition_id 字段）作为 in 条件的子查询
select * from __all_virtual_partition_replay_status
where (table_id, partition_idx) in (
select a.table_id, a.partition_id
from __all_virtual_table_mgr as a inner join __all_virtual_partition_info as b
on a.table_id = b.table_id and a.partition_id = b.partition_idx and a.svr_ip = b.svr_ip
where a.table_type = 0 
and a.is_active = 0 
and a.snapshot_version > least(least(b.min_trans_service_ts, b.min_replay_engine_ts), b.min_log_service_ts)
and (a.table_id, a.partition_id) in (
select table_id, partition_id from __all_virtual_tenant_memstore_allocator_info
where svr_ip='10.186.17.106' and tenant_id=1001 and mt_is_frozen=1
)
);
##### 2.4 确认转储是否成功？
如果 2.2、2.3 小节都没有查询到转储调度异常的 MemTable，接下来根据已冻结但未释放内存的 MemTable 的 pkey(table_id + partition_id) 到 observer.log 日志文件中查看转储过程的日志，以确认转储是否成功。
- 先查出来已冻结但未释放内存的 MemTable 的 pkey：
select table_id, partition_id from __all_virtual_tenant_memstore_allocator_info
where svr_ip='10.186.17.106' and tenant_id=1001 and mt_is_frozen=1
- 根据 pkey（这里实际上只用了 table_id） 到 observer.log 日志文件中查看转储过程的日志：
## 1100611139453778 是 table_id，需要替换成实际使用是的 table_id
grep "add dag success.*1100611139453778" observer.log
grep "task start process.*1100611139453778" observer.log
grep "task finish process.*1100611139453778" observer.log
grep "dag finish.*1100611139453778" observer.log
说明：官方文档中这个步骤是根据 pkey 到 observer.log 中查找是否有相应的转储日志，但是实际上根本是查到不的，因为租户 memstore 占用内存达到 freeze_trigger_percentage 对应的内存上限时，是以租户为维度进行转储的，关于转储过程的日志，记录的是租户 ID，如下：
[403269][938][Y0-0000000000000000] [lt=28] [dc=0] add dag success(dag=0x7fffd6d0b5d0, start_time=1679040139626760, id=Y0-0000000000000000, *dag={this:0x7fffd6d0b5d0, type:7, name:"DAG_MAJOR_FINISH", id:Y0-0000000000000000, dag_ret:0, dag_status:1, start_time:1679040139626760, tenant_id:1}, dag->hash()=0, dag_cnt=1, dag_type_cnts=1)
[242340][416][Y59620ABA116A-0005F70FC566F959] [lt=40] [dc=0] task finish process(ret=0, start_time=1679023923679973, end_time=1679023923680479, runtime=506, *this={type:30, status:2, dag_:{this:0x7fffd6e7e800, type:7, name:"DAG_MAJOR_FINISH", id:Y59620ABA116A-0005F70FC566F959, dag_ret:0, dag_status:2, start_time:1679023923678832, tenant_id:1}})
[403017][456][Y59620ABA116A-0005F7134FC908DD] [lt=21] [dc=0] dag finished(*dag={this:0x7fffd6d0c020, type:7, name:"DAG_MAJOR_FINISH", id:Y59620ABA116A-0005F7134FC908DD, dag_ret:0, dag_status:3, start_time:1679040379627887, tenant_id:1}, runtime=1995, dag_cnt=0, dag_cnts_[dag->get_type()]=0)
所以，这一步实际上可以先跳过，暂且认为转储调度没有异常，就说明会转储成功。
##### 2.5 MemTable 引用计数是否正常？
如果确认了转储调度正常，转储过程也正常，但是已冻结的 MemTable 内存却没有释放，那再确认下是否因为 MemTable 的引用计数异常，导致内存无法释放。
-- 注意：where 条件中 svr_ip、tenant_id 需要修改成实际场景对应的值
-- table_type = 0 表示 MEMTABLE
-- is_active = 0 表示 MEMTABLE 处于冻结状态，还未转储结束
-- 关于 is_active，参照官方文档：https://www.oceanbase.com/docs/enterprise-oceanbase-database-cn-10000000000364739
select * from __all_virtual_table_mgr as a
where a.table_type = 0 and a.is_active = 0 and a.write_ref > 0 and (a.table_id, a.partition_id) in (
select table_id, partition_id from __all_virtual_tenant_memstore_allocator_info
where svr_ip='10.186.17.106' and tenant_id=1001 and mt_is_frozen=1
);
正常情况下，转储过程完成之后，MemTable 的引用计数（write_ref）应该变为 0。
如果上面 SQL 查询到了 MemTable，说明已完成冻结、转储过程的 MemTable 中，还存在引用计数大于 0 的 MemTable，那就说明这些 MemTable 的引用计数异常，导致内存无法释放。
#### 三、遗留问题
- 通过哪些关键字到 observer.log 文件中查看某个表的事务日志？
- 为什么 MemTable 的弱一致性读时间戳小于快照点（snapshot_version）会导致该 MemTable 转储调度异常？
- OB 自动触发转储是按租户维度进行的，observer.log 中怎么查询单个表的转储过程日志？