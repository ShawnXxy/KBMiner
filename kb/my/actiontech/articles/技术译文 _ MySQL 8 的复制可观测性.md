# 技术译文 | MySQL 8 的复制可观测性

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e8%af%91%e6%96%87-mysql-8-%e7%9a%84%e5%a4%8d%e5%88%b6%e5%8f%af%e8%a7%82%e6%b5%8b%e6%80%a7/
**分类**: MySQL 新特性
**发布时间**: 2023-09-03T16:08:44-08:00

---

本文讲解了 MySQL 8 在复制观测性上带来更丰富的观测信息。
> 作者：Frederic Descamps MySQL 社区经理
本文来源：Oracle MySQL 官网博客
- 爱可生开源社区出品。
许多经验丰富的 MySQL DBA 都使用过 `SHOW REPLICA STATUS` 输出中的 `Seconds_Behind_Source` 来判断（异步）复制的运行状态。
> 注意：这里使用新的术语 REPLICA。我相信所有人都使用过旧的术语。
然而，MySQL 复制机制已经有很大进步，复制功能团队也做了很多工作，能够为 MySQL 中所有可用的复制模式提供的更丰富观测信息。
例如，我们增加了并行复制，组复制等，但是这些信息都无法从原来的 `SHOW REPLICA STATUS` 输出中看到。
系统库 `Performance_Schema` 提供了比 `SHOW REPLICA STATUS` 更好的监控和观察复制进程的方式。
当前，`Performance_Schema` 中有 15 张表用于记录复制信息量化：
`+------------------------------------------------------+
| Tables_in_performance_schema (replication%)          |
+------------------------------------------------------+
| replication_applier_configuration                    |
| replication_applier_filters                          |
| replication_applier_global_filters                   |
| replication_applier_status                           |
| replication_applier_status_by_coordinator            |
| replication_applier_status_by_worker                 |
| replication_asynchronous_connection_failover         |
| replication_asynchronous_connection_failover_managed |
| replication_connection_configuration                 |
| replication_connection_status                        |
| replication_group_communication_information          |
| replication_group_configuration_version              |
| replication_group_member_actions                     |
| replication_group_member_stats                       |
| replication_group_members                            |
+------------------------------------------------------+
15 rows in set (0.0038 sec)
`
但不容置疑，理解这些指标的含义并找出对我们 MySQL DBA 真正有意义的信息也不总是那么容易：例如，副本与数据源是否有延迟?
我准备了一些[视图](https://gist.github.com/lefred/1bad64403923664a14e0f20f572d7526)，可以安装在 `sys schema` 中，利用这些指标为我们 DBA 提供相关信息。
我们来更仔细地看一下这些视图。
# 复制延迟
`select * from sys.replication_lag;
+---------------------------+-----------------------+------------------------+
| channel_name              | max_lag_from_original | max_lag_from_immediate |
+---------------------------+-----------------------+------------------------+
| clusterset_replication    | 00:00:04.963223       | 00:00:04.940782        |
| group_replication_applier | 0                     | 0                      |
+---------------------------+-----------------------+------------------------+
`
从上面的输出中，我们可以看到此实例是一个异步复制的副本，但它也是组复制集群的一部分。
事实上，这是 [InnoDB ClusterSet](https://dev.mysql.com/doc/mysql-shell/8.0/en/innodb-clusterset.html) 中 DR 集群的主要成员。
我们还可以看到这个副本的迟到差不多有 5 秒。
然后，我们会看到复制通道的名称，以及与原始提交者和直接源（在级联复制的情况下）的最大延迟（因为在并行复制的情况下可能有多个工作线程）。
在组复制集群（InnoDB Cluster）的 Secondary 节点上，我们可以看到以下输出：
`select * from sys.replication_lag;
+----------------------------+-----------------------+------------------------+
| channel_name               | max_lag_from_original | max_lag_from_immediate |
+----------------------------+-----------------------+------------------------+
| group_replication_recovery | null                  | null                   |
| group_replication_applier  | 00:00:02.733008       | 00:00:02.733008        |
+----------------------------+-----------------------+------------------------+
`
我们可以看到，用于恢复的通道（当节点加入组时读取丢失的二进制日志事件、事务）没有被使用，而组复制的应用程序相对源节点稍有滞后。
# 复制状态
这个视图更完整，每个工作线程都有一行。
以我们 DR 站点 InnoDB ClusterSet 中的 Primary 节点为例：
`select * from replication_status;
+-------------------------------+----------+----------+---------+-------------------+--------------------+
| channel                       | io_state | co_state | w_state | lag_from_original | lag_from_immediate |
+-------------------------------+----------+----------+---------+-------------------+--------------------+
| group_replication_applier (1) | ON       | ON       | ON      | none              | none               |
| group_replication_applier (2) | ON       | ON       | ON      | none              | none               |
| group_replication_applier (3) | ON       | ON       | ON      | none              | none               |
| group_replication_applier (4) | ON       | ON       | ON      | none              | none               |
| clusterset_replication (1)    | ON       | ON       | ON      | 00:00:15.395870   | 00:00:15.380884    |
| clusterset_replication (2)    | ON       | ON       | ON      | 00:00:15.395686   | 00:00:15.380874    |
| clusterset_replication (3)    | ON       | ON       | ON      | 00:00:15.411204   | 00:00:15.388451    |
| clusterset_replication (4)    | ON       | ON       | ON      | 00:00:15.406154   | 00:00:15.388434    |
+-------------------------------+----------+----------+---------+-------------------+--------------------+
`
可以看到，集群并行（异步）复制使用 4 个并行工作线程。
你可能注意到有 3 种状态（所有都为 ON）。但使用 `SHOW REPLICA STATUS` 我们只能看到：
`       Replica_IO_Running: Yes
Replica_SQL_Running: Yes
`
通过并行复制，我们在应用 binlog 事件期间有另一个线程参与复制：coordinator 线程。
# 完整复制状态信息
当然，我们也可以获取更多关于复制的详细信息。
来看一个结果例子：
`select * from sys.replication_status_full\G
*************************** 1. row ***************************
channel: group_replication_applier (1)
host: <NULL>
port: 0
user:
source_uuid: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
group_name: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
last_heartbeat_timestamp: 0000-00-00 00:00:00.000000
heartbeat_interval: 30
io_state: ON
io_thread_state: NULL
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Replica has read all relay log; waiting for more updates
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: Waiting for an event from Coordinator
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 03:36:40.474223
applier_busy_state: IDLE
lag_from_original: none
lag_from_immediate: none
transport_time: 1.80 us
time_to_relay_log: 12.00 us
apply_time: 784.00 us
last_applied_transaction: 7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e:3
last_queued_transaction: 7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e:3
queued_gtid_set_to_apply:
*************************** 2. row ***************************
channel: group_replication_applier (2)
host: <NULL>
port: 0
user:
source_uuid: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
group_name: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
last_heartbeat_timestamp: 0000-00-00 00:00:00.000000
heartbeat_interval: 30
io_state: ON
io_thread_state: NULL
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Replica has read all relay log; waiting for more updates
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: Waiting for an event from Coordinator
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 03:36:40.474223
applier_busy_state: IDLE
lag_from_original: none
lag_from_immediate: none
transport_time: 1.80 us
time_to_relay_log: 12.00 us
apply_time:   0 ps
last_applied_transaction:
last_queued_transaction: 7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e:3
queued_gtid_set_to_apply:
*************************** 3. row ***************************
channel: group_replication_applier (3)
host: <NULL>
port: 0
user:
source_uuid: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
group_name: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
last_heartbeat_timestamp: 0000-00-00 00:00:00.000000
heartbeat_interval: 30
io_state: ON
io_thread_state: NULL
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Replica has read all relay log; waiting for more updates
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: Waiting for an event from Coordinator
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 03:36:40.474223
applier_busy_state: IDLE
lag_from_original: none
lag_from_immediate: none
transport_time: 1.80 us
time_to_relay_log: 12.00 us
apply_time:   0 ps
last_applied_transaction:
last_queued_transaction: 7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e:3
queued_gtid_set_to_apply:
*************************** 4. row ***************************
channel: group_replication_applier (4)
host: <NULL>
port: 0
user:
source_uuid: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
group_name: 7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e
last_heartbeat_timestamp: 0000-00-00 00:00:00.000000
heartbeat_interval: 30
io_state: ON
io_thread_state: NULL
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Replica has read all relay log; waiting for more updates
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: Waiting for an event from Coordinator
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 03:36:40.474223
applier_busy_state: IDLE
lag_from_original: none
lag_from_immediate: none
transport_time: 1.80 us
time_to_relay_log: 12.00 us
apply_time:   0 ps
last_applied_transaction:
last_queued_transaction: 7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e:3
queued_gtid_set_to_apply:
*************************** 5. row ***************************
channel: clusterset_replication (1)
host: 127.0.0.1
port: 3310
user: mysql_innodb_cs_b0adbc6c
source_uuid: 2cb77a02-40eb-11ee-83f4-c8cb9e32df8e
group_name:
last_heartbeat_timestamp: 2023-08-22 18:48:41.037817
heartbeat_interval: 30
io_state: ON
io_thread_state: Waiting for source to send event
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Waiting for replica workers to process their queues
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: waiting for handler commit
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 00:00:00.001134
applier_busy_state: APPLYING
lag_from_original: 00:00:01.799071
lag_from_immediate: 00:00:01.783404
transport_time: 2.26 ms
time_to_relay_log: 19.00 us
apply_time: 14.63 ms
last_applied_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105180
last_queued_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105547
queued_gtid_set_to_apply: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105184-105547
*************************** 6. row ***************************
channel: clusterset_replication (2)
host: 127.0.0.1
port: 3310
user: mysql_innodb_cs_b0adbc6c
source_uuid: 2cb77a02-40eb-11ee-83f4-c8cb9e32df8e
group_name:
last_heartbeat_timestamp: 2023-08-22 18:48:41.037817
heartbeat_interval: 30
io_state: ON
io_thread_state: Waiting for source to send event
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Waiting for replica workers to process their queues
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: waiting for handler commit
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 00:00:00.001134
applier_busy_state: APPLYING
lag_from_original: 00:00:01.797743
lag_from_immediate: 00:00:01.783390
transport_time: 2.26 ms
time_to_relay_log: 19.00 us
apply_time: 21.47 ms
last_applied_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105181
last_queued_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105547
queued_gtid_set_to_apply: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105184-105547
*************************** 7. row ***************************
channel: clusterset_replication (3)
host: 127.0.0.1
port: 3310
user: mysql_innodb_cs_b0adbc6c
source_uuid: 2cb77a02-40eb-11ee-83f4-c8cb9e32df8e
group_name:
last_heartbeat_timestamp: 2023-08-22 18:48:41.037817
heartbeat_interval: 30
io_state: ON
io_thread_state: Waiting for source to send event
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Waiting for replica workers to process their queues
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: waiting for handler commit
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 00:00:00.001134
applier_busy_state: APPLYING
lag_from_original: 00:00:01.786087
lag_from_immediate: 00:00:01.767563
transport_time: 2.26 ms
time_to_relay_log: 19.00 us
apply_time: 21.58 ms
last_applied_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105182
last_queued_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105547
queued_gtid_set_to_apply: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105184-105547
*************************** 8. row ***************************
channel: clusterset_replication (4)
host: 127.0.0.1
port: 3310
user: mysql_innodb_cs_b0adbc6c
source_uuid: 2cb77a02-40eb-11ee-83f4-c8cb9e32df8e
group_name:
last_heartbeat_timestamp: 2023-08-22 18:48:41.037817
heartbeat_interval: 30
io_state: ON
io_thread_state: Waiting for source to send event
io_errno: 0
io_errmsg:
io_errtime: 0000-00-00 00:00:00.000000
co_state: ON
co_thread_state: Waiting for replica workers to process their queues
co_errno: 0
co_errmsg:
co_errtime: 0000-00-00 00:00:00.000000
w_state: ON
w_thread_state: waiting for handler commit
w_errno: 0
w_errmsg:
w_errtime: 0000-00-00 00:00:00.000000
time_since_last_message: 00:00:00.001134
applier_busy_state: APPLYING
lag_from_original: 00:00:01.785881
lag_from_immediate: 00:00:01.767550
transport_time: 2.26 ms
time_to_relay_log: 19.00 us
apply_time: 29.59 ms
last_applied_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105183
last_queued_transaction: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105547
queued_gtid_set_to_apply: 54d83026-40eb-11ee-a5d3-c8cb9e32df8e:105184-105547
`
通过这个视图，我们可以获得更多详细信息，例如复制心跳。我们还对 GTID（排队、应用等）进行了概述。
我们也可以看到传输时间（网络）、写入中继日志的时间以及最终应用的时间等信息。
当然，您可以根据需要来选择视图的显示内容，例如：
# InnoDB 集群，ClusterSet，只读副本
如果使用由 Admin API 和 MySQL Shell 管理的集成解决方案，那么所有这些信息已经通过 `status()` 方法可以获知。
`status()` 方法可以扩展 3 个值：
- 返回集群元数据版本、组协议版本、组名称、集群成员 UUID、成员角色和状态（由组复制报告），及被隔离的系统变量列表。
- 返回每个连接和应用程序处理的事务信息。
- 返回每个集群成员复制机制更详细的统计信息。
下面来看一下扩展选项 3 的 ClusterSet 示例：
`JS> cs.status({extended:3})
{
"clusters": {
"cluster2": {
"clusterRole": "REPLICA",
"clusterSetReplication": {
"applierQueuedTransactionSet": "54d83026-40eb-11ee-a5d3-c8cb9e32df8e:137385-138500",
"applierQueuedTransactionSetSize": 1116,
"applierState": "ON",
"applierStatus": "APPLYING",
"applierThreadState": "waiting for handler commit",
"applierWorkerThreads": 4,
"coordinatorState": "ON",
"coordinatorThreadState": "Waiting for replica workers to process their queues",
"options": {
"connectRetry": 3,
"delay": 0,
"heartbeatPeriod": 30,
"retryCount": 10
},
"receiver": "127.0.0.1:4420",
"receiverStatus": "ON",
"receiverThreadState": "Waiting for source to send event",
"receiverTimeSinceLastMessage": "00:00:00.002737",
"replicationSsl": null,
"source": "127.0.0.1:3310"
},
"clusterSetReplicationStatus": "OK",
"communicationStack": "MYSQL",
"globalStatus": "OK",
"groupName": "7b6bf13d-40ed-11ee-bfdd-c8cb9e32df8e",
"groupViewChangeUuid": "7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e",
"paxosSingleLeader": "OFF",
"receivedTransactionSet": "54d83026-40eb-11ee-a5d3-c8cb9e32df8e:129-138500",
"ssl": "REQUIRED",
"status": "OK_NO_TOLERANCE",
"statusText": "Cluster is NOT tolerant to any failures.",
"topology": {
"127.0.0.1:4420": {
"address": "127.0.0.1:4420",
"applierWorkerThreads": 4,
"fenceSysVars": [
"read_only",
"super_read_only"
],
"memberId": "c3d726ac-40ec-11ee-ab38-c8cb9e32df8e",
"memberRole": "PRIMARY",
"memberState": "ONLINE",
"mode": "R/O",
"readReplicas": {},
"replicationLagFromImmediateSource": "00:00:05.420247",
"replicationLagFromOriginalSource": "00:00:05.433548",
"role": "HA",
"status": "ONLINE",
"version": "8.1.0"
},
"127.0.0.1:4430": {
"address": "127.0.0.1:4430",
"applierWorkerThreads": 4,
"fenceSysVars": [
"read_only",
"super_read_only"
],
"memberId": "709b15ea-40ed-11ee-a9b3-c8cb9e32df8e",
"memberRole": "SECONDARY",
"memberState": "ONLINE",
"mode": "R/O",
"readReplicas": {},
"replicationLagFromImmediateSource": "00:00:00.038075",
"replicationLagFromOriginalSource": "00:00:05.432536",
"role": "HA",
"status": "ONLINE",
"version": "8.1.0"
}
},
"transactionSet": "2cb77a02-40eb-11ee-83f4-c8cb9e32df8e:1-4,54d83026-40eb-11ee-a5d3-c8cb9e32df8e:1-137384,54d8329c-40eb-11ee-a5d3-c8cb9e32df8e:1-5,7b6bf4f0-40ed-11ee-bfdd-c8cb9e32df8e:1-3",
"transactionSetConsistencyStatus": "OK",
"transactionSetErrantGtidSet": "",
"transactionSetMissingGtidSet": "54d83026-40eb-11ee-a5d3-c8cb9e32df8e:137385-138552"
},
"myCluster": {
"clusterRole": "PRIMARY",
"communicationStack": "MYSQL",
"globalStatus": "OK",
"groupName": "54d83026-40eb-11ee-a5d3-c8cb9e32df8e",
"groupViewChangeUuid": "54d8329c-40eb-11ee-a5d3-c8cb9e32df8e",
"paxosSingleLeader": "OFF",
"primary": "127.0.0.1:3310",
"ssl": "REQUIRED",
"status": "OK",
"statusText": "Cluster is ONLINE and can tolerate up to ONE failure.",
"topology": {
"127.0.0.1:3310": {
"address": "127.0.0.1:3310",
"applierWorkerThreads": 4,
"fenceSysVars": [],
"memberId": "2cb77a02-40eb-11ee-83f4-c8cb9e32df8e",
"memberRole": "PRIMARY",
"memberState": "ONLINE",
"mode": "R/W",
"readReplicas": {
"127.0.0.1:4410": {
"address": "127.0.0.1:4410",
"applierStatus": "APPLYING",
"applierThreadState": "waiting for handler commit",
"applierWorkerThreads": 4,
"receiverStatus": "ON",
"receiverThreadState": "Waiting for source to send event",
"replicationSources": [
"PRIMARY"
],
"replicationSsl": "TLS_AES_256_GCM_SHA384 TLSv1.3",
"role": "READ_REPLICA",
"status": "ONLINE",
"version": "8.1.0"
}
},
"role": "HA",
"status": "ONLINE",
"version": "8.1.0"
},
"127.0.0.1:3320": {
"address": "127.0.0.1:3320",
"applierWorkerThreads": 4,
"fenceSysVars": [
"read_only",
"super_read_only"
],
"memberId": "327cb102-40eb-11ee-9904-c8cb9e32df8e",
"memberRole": "SECONDARY",
"memberState": "ONLINE",
"mode": "R/O",
"readReplicas": {},
"replicationLagFromImmediateSource": "00:00:04.536190",
"replicationLagFromOriginalSource": "00:00:04.536190",
"role": "HA",
"status": "ONLINE",
"version": "8.1.0"
},
"127.0.0.1:3330": {
"address": "127.0.0.1:3330",
"applierWorkerThreads": 4,
"fenceSysVars": [
"read_only",
"super_read_only"
],
"memberId": "3d141d7e-40eb-11ee-933b-c8cb9e32df8e",
"memberRole": "SECONDARY",
"memberState": "ONLINE",
"mode": "R/O",
"readReplicas": {},
"replicationLagFromImmediateSource": "00:00:04.652745",
"replicationLagFromOriginalSource": "00:00:04.652745",
"role": "HA",
"status": "ONLINE",
"version": "8.1.0"
}
},
"transactionSet": "2cb77a02-40eb-11ee-83f4-c8cb9e32df8e:1-4,54d83026-40eb-11ee-a5d3-c8cb9e32df8e:1-138552,54d8329c-40eb-11ee-a5d3-c8cb9e32df8e:1-5"
}
},
"domainName": "myClusterSet",
"globalPrimaryInstance": "127.0.0.1:3310",
"metadataServer": "127.0.0.1:3310",
"primaryCluster": "myCluster",
"status": "HEALTHY",
"statusText": "All Clusters available."
}
`
# 结论
复制部分的可观察性非常详细，并通过 MySQL 8 提供了大量信息。也许现在是改变查看或监视复制方式的好时机。