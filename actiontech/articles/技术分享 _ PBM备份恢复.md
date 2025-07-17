# 技术分享 | PBM备份恢复

**原文链接**: https://opensource.actionsky.com/20230321-pbm/
**分类**: 技术干货
**发布时间**: 2023-03-20T21:59:17-08:00

---

作者：张洪
爱可生南区 DBA 团队成员，主要负责mysql故障处理及相关技术支持。爱好旅游，摄影。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 概述
Percona Backup for MongoDB(PBM)是一个针对MongoDB副本集和分片的一致性备份开源工具，它支持逻辑备份、物理备份、增量备份以及选择性备份和恢复等特性，并且支持Point-in-Time恢复到指定时间点。
但非常可惜的是物理备份相关功能目前仅适用于Percona Server for MongoDB的分支，因此下面主要围绕逻辑备份与Point-in-Time来展开，MongoDB Community版本要求4.0及以上。
#### 架构
![](.img/3d719108.png)
**pbm-agent**
pbm-agent用于执行备份、恢复，删除和其它操作的进程，它必须运行在集群的每个mongod实例上。包括副本集中的secondary节点以及分片集群中的config副本集。
所有pbm-agent都会监视PBM Control集合的更新，当PBM CLI对PBM Control集合产生更新时，将会在每个副本集上选择一个secondary上的pbm-agent执行操作，如果没有响应则会选择Primary上的pbm-agent执行操作。
被选中的pbm-agent将会加锁，避免同时触发备份和恢复等互斥操作。操作完成后将会释放锁，并更新PBM Control集合
**PBM CLI**
PBM CLI是一个操作PBM的命令行工具，它使用PBM Control集合与pbm-agent进程通信。通过更新和读取操作、日志等相应的PBM Control集合来启动和监视备份和恢复操作。同时，它也将PBM配置信息保存在PBM Control集合中。
**PBM Control collections**
PBM Control collections是存储配置数据和备份状态的特殊集合，分片环境存放在config副本集的admin数据库中，副本集则保存在自身的admin数据库中。
主要包含以下集合：
- admin.pbmBackups：备份的日志和状态
- admin.pbmAgents：pbm-agent的运行状态
- admin.pbmConfig：PBM的配置信息
- admin.pbmCmd：用于定义和触发操作
- admin.pbmLock：pbm-agent同步锁
- admin.pbmLockOp：用于协调不互斥的操作，如执行备份、删除备份等
- admin.pbmLog：存储pbm-agent的日志信息
- admin.pbmOpLog：存储操作ID
- admin.pbmPITRChunks：存储point-in-time恢复的oplog块
- admin.pbmPITRState：存储point-in-time恢复增量备份的状态
- admin.pbmRestores：存储还原历史记录和状态
- admin.pbmStatus：记录PBM备份状态
**remote backup storge**
远程备份存储是保存备份文件的位置，可以是S3存储，也可以是Filesystem。通过pbm list命令可以查看备份集。备份文件名称都是以UTC备份开始时间作为前缀，每个备份都有一个元数据文件。对于备份中的每个副本集：
- 有一个mongodump格式的压缩归档文件，它是集合的转储
- 覆盖备份时间的oplog的BSON文件转储
#### 安装配置
下载PBM
# wget https://downloads.percona.com/downloads/percona-backup-mongodb/percona-backup-mongodb-2.0.3/binary/tarball/percona-backup-mongodb-2.0.3-x86_64.tar.gz
解压PBM
# tar -xvf percona-backup-mongodb-2.0.3-x86_64.tar.gz
配置环境变量
# echo "export PATH=$PATH:/usr/local/percona-backup-mongodb-2.0.3-x86_64" >> /etc/profile
# source /etc/profile
在副本集上创建PBM用户，如果是分片环境，则每个shard以及config都需要创建
# create pbm role
shard1:PRIMARY> db.getSiblingDB("admin").createRole({ "role": "pbmAnyAction",
"privileges": [
{ "resource": { "anyResource": true },
"actions": [ "anyAction" ]
}
],
"roles": []
});
# create pbm user
shard1:PRIMARY> db.getSiblingDB("admin").createUser({user: "pbmuser",
"pwd": "secretpwd",
"roles" : [
{ "db" : "admin", "role" : "readWrite", "collection": "" },
{ "db" : "admin", "role" : "backup" },
{ "db" : "admin", "role" : "clusterMonitor" },
{ "db" : "admin", "role" : "restore" },
{ "db" : "admin", "role" : "pbmAnyAction" }
]
});
配置remote backup storge，除mongos外，每个节点都需要存在对应的备份目录
cat > /etc/pbm_config.yaml <<EOF
storage:
type: filesystem
filesystem:
path: /data/backup
EOF
将配置写入到数据库中，分片集群需要填写config的地址
pbm config --file /etc/pbm_config.yaml --mongodb-uri "mongodb://pbmuser:secretpwd@10.186.65.37:27018,10.186.65.66:27018,10.186.65.68:27018/?replicaSet=config"
启动每个节点对应的pbm-agent
nohup pbm-agent --mongodb-uri "mongodb://pbmuser:secretpwd@10.186.65.37:27017" > /var/log/pbm-agent-27017.log 2>&1 &
为了后续方便，不用每次输入`--mongodb-uri`，可以把PBM_MONGODB_URI设置到环境变量中
# echo 'export PBM_MONGODB_URI="mongodb://pbmuser:secretpwd@10.186.65.37:27018,10.186.65.66:27018,10.186.65.68:27018/?replicaSet=config"' >> /etc/profile
# source /etc/profile
#### 全量备份
![](.img/95f8ebee.png)
全备支持物理备份和逻辑备份，通过&#8211;type指定，可选项有physical和logical两种。因MongoDB社区版不支持物理备份，就只围绕逻辑备份来展开。
全量备份即对整个集群除mongos以外进行完整的备份，只需要执行一次，就能完成整个集群的备份。备份命令如下：
pbm backup --type=logical --mongodb-uri "mongodb://pbmuser:secretpwd@10.186.65.37:27018,10.186.65.66:27018,10.186.65.68:27018/?replicaSet=config"
**备份压缩**
pbm支持备份压缩，目前的算法有gzip、zstd、snappy、lz4，通过`--compression`选项指定。同时能指定对应的压缩级别，通过&#8211;compression-level选项指定。不同算法的压缩级别如下所示：
| 压缩算法 | 压缩级别 | 默认 |
| --- | --- | --- |
| ztsd | 1-4 | 2 |
| snappy | NULL | NULL |
| lz4 | 1-16 | 1 |
| gzip or pgzip | -1,0,1,9 | -1 |
**优先级**
负责备份的pbm-agent默认会在从节点中随机选出，规定时间内从节点没有响应，则在主节点进行备份。现在可以通过指定每个节点的备份优先级来控制备份节点选择，避免在一个机器承载多个实例的情况下备份集中在同一台服务器导致IO性能不足。在配置文件中加入下列配置
backup:
priority:
"10.186.65.37:27017": 2
"10.186.65.37:27018": 1
"10.186.65.68:27017": 2
不在配置文件中的节点优先级默认为1，如果没有设置任何优先级，下列类型的节点则优先被选中
- 隐藏节点：优先级为2
- secondary节点：优先级为1
- Primary节点：优先级为0.5
**备份管理**
查看pbm状态
pbm status --mongodb-uri
Cluster:
========
shard3:
- shard3/10.186.65.68:27017 [P]: pbm-agent v2.0.3 OK
shard1:
- shard1/10.186.65.37:27017 [P]: pbm-agent v2.0.3 OK
shard2:
- shard2/10.186.65.66:27017 [P]: pbm-agent v2.0.3 OK
config:
- config/10.186.65.37:27018 [P]: pbm-agent v2.0.3 OK
- config/10.186.65.66:27018 [S]: pbm-agent v2.0.3 OK
- config/10.186.65.68:27018 [S]: pbm-agent v2.0.3 OK
PITR incremental backup:
========================
Status [OFF]
Currently running:
==================
(none)
Backups:
========
FS  /data/backup
Snapshots:
2023-02-22T07:18:40Z 4.66MB <logical> [restore_to_time: 2023-02-22T07:18:45Z]
备份完成后，可以通过`pbm list`查看所有备份集，也可以通过pbm describe-backup查看备份的具体信息
# pbm list
Backup snapshots:
2023-02-22T07:18:40Z <logical> [restore_to_time: 2023-02-22T07:18:45Z]
# pbm describe-backup 2023-02-22T07:18:40Z
name: "2023-02-22T07:18:40Z"
opid: 63f5c1d0a6375c868415cac4
type: logical
last_write_time: "2023-02-22T07:18:45Z"
last_transition_time: "2023-02-22T07:18:59Z"
mongodb_version: 4.0.28
pbm_version: 2.0.3
status: done
size_h: 4.7 MiB
replsets:
- name: shard2
status: done
last_write_time: "2023-02-22T07:18:44Z"
last_transition_time: "2023-02-22T07:18:55Z"
- name: shard3
status: done
last_write_time: "2023-02-22T07:18:44Z"
last_transition_time: "2023-02-22T07:18:59Z"
- name: shard1
status: done
last_write_time: "2023-02-22T07:18:44Z"
last_transition_time: "2023-02-22T07:18:57Z"
- name: config
status: done
last_write_time: "2023-02-22T07:18:45Z"
last_transition_time: "2023-02-22T07:18:48Z"
configsvr: true
查看备份日志可以使用`pbm logs`进行查看，有下列选项可选：
- -t：查看最后N行记录
- -e：查看所有备份或指定备份
- -n：指定节点或副本集
- -s：按日志级别进行过滤，从低到高依次是D(debug)、I(Info)、W(Warning)、E(Error)、F(Fatal)
- -o：以文本或JSON格式显示日志信息
- -i：指定操作ID
# 查看特定备份的日志
pbm logs --tail=200 --event=backup/2023-02-22T07:18:40Z
# 查看副本集shard1的日志
pbm logs -n shard1 -s E
如果正在运行任务想要终止，可以使用`pbm canal-backup`取消
pbm cancel-backup
删除快照备份可以使用`pbm delete-backup`，默认删除前会进行二次确认，指定`--force`选项可以直接删除。删除oplog chunk可以执行`pbm delete-pitr`
pbm delete-backup --force 2023-02-22T07:18:40Z 
如果想要删除指定时间之前的备份，可以设置`--older-than`参数，传递下列格式的时间戳
- %Y-%M-%DT%H:%M:%S (e.g. 2020-04-20T13:13:20)
- %Y-%M-%D (e.g. 2020-04-20)
#### 增量备份
Point-in-Time Recovery可以将数据还原到指定时间点，期间会从备份快照中恢复数据库，并重放oplog到指定时间点。Point-in-Time Recovery是v1.3.0加入的，需要手动启用pitr.enabled参数
pbm config --set pitr.enabled=true 
在启用Point-in-Time Recovery之后，pbm-agent会定期保存oplog chunk，一个chunk包含10分钟跨度的oplog事件，如果禁用时间点恢复或因备份快照操作的开始而中断，则时间可能会更短。oplog保存在远程存储的pbmPitr子目录中，chunk的名称反映了开始时间和结束时间
如果想要调整时间跨度，可以配置`pitr.oplogSpanMin`
pbm config --set pitr.oplogSpanMin=5
oplog备份也支持压缩，可以配置`pitr.compression`
pbm config --set pitr.compression=gzip
#### 数据恢复
![](.img/810eb5da.png)
**恢复注意事项**
通过pbm store命令并指定还原时间戳，在还原之前还需要注意以下几点：
- 从1.x版本开始，Percona Backup For MongoDB复制了Mongodump的行为，还原时只清理备份中包含的集合，对于备份之后，还原之前创建的集合不进行清理，需要在还原前手动执行db.dropDatabase()清理
- 在恢复运行过程中，阻止客户端访问数据库
- 分片备份只能还原到分片集群中，还原期间将写入分片primary节点
- 为避免恢复期间pbm-agent内存消耗，V1.3.2可以针对恢复在配置文件设置下列参数
restore:  batchSize: 500  numInsertionWorkers: 10
**分片集群恢复**
分片集群在做恢复前，需要先完成以下步骤
1.停止balancer
mongos> sh.stopBalancer()
2.关闭所有mongos，阻止客户端访问
3.如果启用了PITR，则禁用该功能
pbm config --set pitr.enabled=false
查看备份快照和PITR有效时间点
pbm list
Backup snapshots:
2023-02-22T07:18:40Z <logical> [restore_to_time: 2023-02-22T07:18:45Z]
PITR <on>:
2023-02-22T07:18:46Z - 2023-02-22T08:36:45Z
执行PITR恢复
pbm restore --time="2023-02-22T08:30:00"
恢复完成后重新启用PITR和balance进程，并开启mongos对外提供服务
mongos> sh.startBalancer()pbm config --set pitr.enabled=true
**异机恢复**
从v1.8版本开始，可以将逻辑备份恢复到具有相同或更多shard的新环境中，并且这些shard的副本集名称可以与原环境不同。但我们需要配置以下映射关系
pbm restore --time="2023-02-22T08:30:00" --replset-remapping="shard1=shard4,shard2=shard5"
##### 性能
pbm提供了性能测试工具pbm-speed-test，默认采用半随机数据进行测试，如果要基于现有集合进行测试，请设置&#8211;sample-collection选项
pbm-speed-test storage --compression=gzip --size-gb 100
Test started
100.00GB sent in 37m17s.
Avg upload rate = 45.78MB/s
pbm整体的性能相对于mongodump并没有较大的提升，主要还是体现在下列几个特点：
- 在分片集群中进行一致性备份和恢复
- 支持完全备份/恢复、选择性备份恢复等多种粒度
- 支持基于时间点的恢复
##### 选择性备份和恢复
选择性备份和恢复功能可以针对指定的数据库或集合，但目前还只是一个实验性功能，谨慎使用。它具有以下场景选项：
- 备份单个数据库或特定集合，并从中恢复所有数据
- 从单个数据库备份恢复特定的集合
- 从全备中恢复某些数据库或集合
- 从全备中Point-in-recovery某些数据库或集合
备份指定集合时，需要指定`--ns`选项，格式为`<database.collection>`。分片环境的URI需要填写config的地址
pbm backup --ns=test.col1
如果要备份整个test数据库，可以改为下列格式
pbm backup --ns=test.*
恢复指定数据库或集合，恢复过程中不会影响现有集群的可用性
pbm restore 2023-02-22T07:18:40Z --ns test.col1
基于时间点恢复数据库或集合
pbm restore --base-snapshot 2023-02-22T07:18:40Z --time 2023-02-22T09:06:00 --ns test.col1
**已知限制**
- 只支持逻辑备份恢复
- 不支持分片集合
- 不支持批量指定namespace
- 不支持Multi-collection事务
- 不能备份恢复本地数据库中的系统集合
- 时间点恢复需要通过完全备份来作为基础
参考链接：https://docs.percona.com/percona-backup-mongodb/intro.html