# 技术分享 | MySQL 组复制数据一致性管理解析

**原文链接**: https://opensource.actionsky.com/20200518-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-05-18T00:49:09-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
来源于客户的一个问题。客户对组复制的数据一致性保障机制非常困惑，一直不太明白，其实就是对组复制参数 `group_replication_consistency` 几个值的含义不太清楚。这里我举了几个简单的例子，来说明这个参数包含的几个选项的真实含义。
**一、概念**
组复制的概念：组复制是 MySQL 基于传统的主从复制开发的一个插件。这个插件改善了原生主从复制的一些重大功能缺陷，诸如数据一致性监测管理、自动冲突监测、自动故障监测、自动收缩扩容节点、自动数据回补等等。
组复制功能自 MySQL 5.7 发布到现在最新版 MySQL 8.0.20，经历了各种缺陷修复、功能升级，目前已经比较完善。
参数 `group_replication_consistency` 共 5 个值可选：
1. EVENTUAL：确保最终一致性，并不能保证数据实时同步。（MySQL 8.0.14 之前只有这一个选项）
2. BEFORE：确保本地强一致性，并不保证其他节点数据实时同步。
3. AFTER：确保全局强一致性，可以保证所有节点数据实时同步。
4. BEFORE_AND_AFTER：最高级别，确保本地强一致性，全局强一致性。结合 BEOFRE 和 AFTER 的特性。
5. BEFORE_ON_PRIMARY_FAILOVER：确保从节点晋升为主节点后的本地一致性。
**接下来，在组复制的默认模式下讨论 EVENTUAL，BEFORE，AFTER 这三类值的含义以及使用场景。**
**二、环境准备**
- debian-ytt1:3306（写节点，简称节点 1）
- debian-ytt2:3306（读节点，简称节点 2）
- debian-ytt3:3306（读节点，简称节点 3）
以下为集群 ytt_mgr 的状态，节点 1 为主，节点 2 和节点 3 为从。
- `MySQL  debian-ytt1:3306 ssl  ytt  Py > c1 = dba.get_cluster('ytt_mgr');`
- `MySQL  debian-ytt1:3306 ssl  ytt  Py > c1.status();`
- `{`
- `    "clusterName": "ytt_mgr",`
- `    "defaultReplicaSet": {`
- `        "name": "default",`
- `        "primary": "debian-ytt1:3306",`
- `        "ssl": "REQUIRED",`
- `        "status": "OK",`
- `        "statusText": "Cluster is ONLINE and can tolerate up to ONE failure.",`
- `        "topology": {`
- `            "debian-ytt1:3306": {`
- `                "address": "debian-ytt1:3306",`
- `                "mode": "R/W",`
- `                "readReplicas": {},`
- `                "replicationLag": null,`
- `                "role": "HA",`
- `                "status": "ONLINE",`
- `                "version": "8.0.20"`
- `            },`
- `            "debian-ytt2:3306": {`
- `                "address": "debian-ytt2:3306",`
- `                "mode": "R/O",`
- `                "readReplicas": {},`
- `                "replicationLag": null,`
- `                "role": "HA",`
- `                "status": "ONLINE",`
- `                "version": "8.0.20"`
- `            },`
- `            "debian-ytt3:3306": {`
- `                "address": "debian-ytt3:3306",`
- `                "mode": "R/O",`
- `                "readReplicas": {},`
- `                "replicationLag": null,`
- `                "role": "HA",`
- `                "status": "ONLINE",`
- `                "version": "8.0.20"`
- `            }`
- `        },`
- `        "topologyMode": "Single-Primary"`
- `    },`
- `    "groupInformationSourceMember": "debian-ytt1:3306"`
- `}`
**三、三种选项值的含义和适用场景**
3.1 EVENTUAL
这类选项代表**最终一致性**，组复制默认值。意思是说，设置了 EVENTUAL 的节点，其读或者写请求可以立即返回结果，不用等到新请求之前的中继日志处理完。
创建一张测试表 t1。- `<debian-ytt1|mysql>create table t1 (id serial primary key, r1 int,r2 int,r3 char(36));`
- `Query OK, 0 rows affected (0.07 sec)`
节点 1 正常插入一条记录。- `<debian-ytt1|mysql>insert into t1 (r1,r2,r3) select 10,20,uuid();`
- `Query OK, 1 row affected (0.02 sec)`
- `Records: 1  Duplicates: 0  Warnings: 0`
节点 2 及时应用这条记录到表 t1。- `<debian-ytt2|mysql>select * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |   10 |   20 | e878289e-89c4-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
- `1 row in set (0.00 sec)`
此时给节点 2 加一个 server 层的共享读锁，人为制造拥堵延迟。- `<debian-ytt2|mysql>lock table t1 read;`
- `Query OK, 0 rows affected (0.00 sec)`
节点 1 再次插入一条 ID 为 2 的新记录。- `<debian-ytt1|mysql>insert into t1 (r1,r2,r3) select 20,20,uuid();`
- `Query OK, 1 row affected (0.02 sec)`
- `Records: 1  Duplicates: 0  Warnings: 0`
- 
- `<debian-ytt1|mysql>select  * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |   10 |   20 | e878289e-89c4-11ea-861d-08002753f58d |`
- `|  2 |   20 |   20 | 2982d33f-89c5-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
- `2 rows in set (0.00 sec)`
此时再次查询节点 2 可立即返回结果，但是数据并非最新，不包含最新 ID 为 2 的记录，还是之前的旧数据。- `<debian-ytt2|mysql>select * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |   10 |   20 | e878289e-89c4-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
- `1 row in set (0.00 sec)`
节点 2 上，ID 为 2 的这条记录，目前状态为：已拉到自己的中继日志，但尚未应用到表 t1。表 t1 的共享读锁释放掉后，才能继续应用。现在释放表 t1 的共享读锁，再次查询已经包含最新的记录。- `<debian-ytt2|mysql>unlock tables;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `<debian-ytt2|mysql>select * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |   10 |   20 | e878289e-89c4-11ea-861d-08002753f58d |`
- `|  3 |   20 |   20 | 759cc5c0-89c7-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
从以上例子可以看出，最终一致性模式优缺点。- 优点：可以快速返回本节点已经成功应用的数据，不用等待所有的数据应用完成。
- 缺点：可能返回的数据比较旧。
3.2 BEFORE
这类选项代表**保证本地节点强一致性**。也就是说设置为此选项的本地节点必须要等待中继日志数据全部应用完成后，才会执行新的请求，否则会一直等待。等待的时间和中继日志里未应用的事务量成一定比率。
为了清晰起见，清空表 t1 数据。- `<debian-ytt1|mysql>truncate t1;`
- `Query OK, 0 rows affected (0.17 sec)`
新启一个连接到节点 2，给表 t1 上共享读锁，对应的 SESSION ID =1。- `<debian-ytt2|mysql>lock table t1 read;`
- `Query OK, 0 rows affected (0.01 sec)`
在节点 1 上插入一条新记录。- `<debian-ytt1|mysql>insert into t1 select 1,1,1,uuid();`
- `Query OK, 1 row affected (0.02 sec)`
- `Records: 1  Duplicates: 0  Warnings: 0`
另外开启一个新连接到节点 2，对应的 SESSION ID = 2。设置参数 group_replication_consistency=before，完了立刻查询表 t1 数据，处于等待状态。- `<debian-ytt2|mysql>set @@group_replication_consistency='before';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `<debian-ytt2|mysql>select * from t1;`
- 
- `# 此处 HANG 住！`
在节点 3 上查询表 t1 数据，立刻返回刚才插入的记录，也就是说对节点 3 没有影响。- `<debian-ytt3|mysql>select * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |    1 |    1 | ee83837e-89ce-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
- `1 row in set (0.00 sec)`
此时切换到节点 2 的 SESSION ID = 1 的会话，解锁表 t1。- `<debian-ytt2|mysql>unlock tables;`
- `Query OK, 0 rows affected (0.00 sec)`
再次查看节点 2 的 SESSION ID = 2 的会话，结果已经返回，时间为 3 分 17 秒。相比 EVENTUAL，并不是立即返回结果。- `<debian-ytt2|mysql>select * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |    1 |    1 | ee83837e-89ce-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
- `1 row in set (3 min 17.51 sec)`
可以看出，BEFORE 模式优先保证了本地节点永远读取到最新的数据。最大的缺点是必须煎熬等待本地节点中继日志里未应用的数据正常应用。如果日志里有很多写的不好的事务块或者大事务，则会造成本节点很大的延迟。
3.3 AFTER
这类选项代表**全局强一致性**。设置为此模式的节点，必须等待集群内其他所有其他节点应用完自己中继日志里的事务，才能返回结果。
把节点 1 参数 `group_replication_consistency` 设置为 AFTER，清空表 t1。- `<debian-ytt1|mysql>truncate t1;`
- `Query OK, 0 rows affected (0.22 sec)`
- 
- `<debian-ytt1|mysql>set @@group_replication_consistency='after';`
- `Query OK, 0 rows affected (0.00 sec)`
在节点 2 上，给表 t1 加共享读锁。- `<debian-ytt2|mysql>lock table t1 read;`
- `Query OK, 0 rows affected (0.01 sec)`
之后在节点 1 插入一条记录，并没有立即返回，处于等待状态，因为节点 2 上的表 t1 被锁了，节点 2 的日志要成功应用必须要等表 t1 解锁才可以。
- `<debian-ytt1|mysql>insert into t1 select 1,1,1,uuid();`
- 
- `# 处于等待状态`
此时回到节点 2，由于模式默认，立即返回结果，不过数据很旧。
- `<debian-ytt2|mysql>select * from t1;`
- `Empty set (0.00 sec)`
此时在节点 3 上对表 t1 进行查询，发现这个请求也处于等待状态。也就是说虽然节点 3 也是默认模式，但是由于主节点设置为 AFTER，节点 3 也必须等待其他的从节点日志应用完毕后才能返回结果。
- `<debian-ytt3|mysql>select * from t1;`
现在在节点 2 上解锁表 t1，再次回到节点 1 上的 ID 为 121 的连接，结果已经返回，不过花费了 6 分 47 秒。
- `<debian-ytt1|mysql>insert into t1 select 1,1,1,uuid();`
- `Query OK, 1 row affected (6 min 47.14 sec)`
- `Records: 1  Duplicates: 0  Warnings: 0`
此时在节点 3 上检查之前的查询，结果也已经返回。
- `<debian-ytt3|mysql>select * from t1;`
- `+----+------+------+--------------------------------------+`
- `| id | r1   | r2   | r3                                   |`
- `+----+------+------+--------------------------------------+`
- `|  1 |    1 |    1 | 49430687-89e9-11ea-861d-08002753f58d |`
- `+----+------+------+--------------------------------------+`
- `1 row in set (18.25 sec)`
从以上过程可以看到，AFTER 是一个强同步的选项。优先保证了集群内所有节点的数据一致性，但是也带来一个很大的性能问题：集群对外总的事务提交时间依赖于组内最慢的那个节点。如果最慢的节点遇到故障，那其他节点就必须等待超时回滚了。
**总结**
本文对组复制的数据一致性级别参数值的设置做了详细的演示。可以看到我只说明了前三个选项，后面两个由于基于前三个选项的组合，这里没有单独说明，感兴趣可以自己实验下。