# 技术分享 | MySQL Shell 定制化部署 MySQL 实例

**原文链接**: https://opensource.actionsky.com/20220727-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-07-26T21:41:26-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
之前写过使用 MySQL Shell 的 DBA 组件来搭建、运维 MySQL InnoDB Cluster 。今天我们来继续对 DBA 组件进行延伸介绍，探讨如何用它定制化部署 MySQL 实例。
#### 一、如何部署多个不同版本的 MySQL 实例：
默认使用 DBA 组件部署多个实例时，使用系统内置的 MySQL 版本，也就是在环境变量$PATH包含的路径里搜寻 mysqld 来确认具体的实例版本。比如我机器上，默认 MySQL 版本为 8.0 ，所以直接部署后的实例版本也是8.0。
root@ytt-normal:~# mysqlsh --py 
MySQL Shell 8.0.29
...
MySQL  Py > dba.deploy_sandbox_instance(3350);
A new MySQL sandbox instance will be created on this host in 
/root/mysql-sandboxes/3350
...
Instance localhost:3350 successfully deployed and started.
Use shell.connect('root@localhost:3350') to connect to the instance.
例如以上端口为3350的实例在部署完成后，新建一个连接，成功后客户端就会收到具体版本：Server version: 8.0.29 MySQL Community Server &#8211; GPL。
MySQL  Py > \c root@localhost:3350
...
Your MySQL connection id is 12
Server version: 8.0.29 MySQL Community Server - GPL
如果想同时部署多个不同版本MySQL实例，只需要把对应版本的 mysqld 路径放入$PATH即可。需要注意的是，新路径与老$PATH拼接顺序：新路径在前，老$PATH在后！部署完成后，记得再把$PATH内容还原。
比如我机器上 MySQL 5.7 版本安装包目录为：/root/opt/mysql/5.7.34 ，那么添加这个目录的子目录 bin 到环境变量 $PATH 即可：
root@ytt-normal:~# export PATH=/root/opt/mysql/5.7.34/bin:$PATH
重新进入 MySQL Shell 环境，和上面 MySQL 8.0 相同的部署方式：可以看到，新部署的实例版本为 5.7.34-log MySQL Community Server (GPL)。
MySQL  Py > dba.deploy_sandbox_instance(3351)
A new MySQL sandbox instance will be created on this host in 
/root/mysql-sandboxes/3351
...
Instance localhost:3351 successfully deployed and started.
Use shell.connect('root@localhost:3351') to connect to the instance.
MySQL  Py > \c root@localhost:3351
...
Your MySQL connection id is 7
Server version: 5.7.34-log MySQL Community Server (GPL)
#### 二、如何更改部署实例的基本目录：
默认部署实例文件在~/mysql-sandboxes下，按照实例端口划分，每个端口一个子目录。比如之前部署的两个 MySQL 实例，分别对应目录 /root/mysql-sandboxes/3350、/root/mysql-sandboxes/3351 。
##### 有两种方法可以更改部署实例的基本目录：
##### 1. 调用 dba.deploy_sandbox_instance 时，显式指定部署目录：
- sandboxDir: path where the new instance will be deployed.
例如部署一个新实例3352，指定基本目录为：/tmp/mysql-sandbox。
MySQL  Py > dba.deploy_sandbox_instance(3352,{"sandboxDir":"/tmp/mysql-sandbox"})
A new MySQL sandbox instance will be created on this host in 
/tmp/mysql-sandbox/3352
...
Instance localhost:3352 successfully deployed and started.
Use shell.connect('root@localhost:3352') to connect to the instance.
这种方法最大的缺点就是对于后续新实例的部署不具备通用性，需要针对每个新实例分别指定 sandboxDir 选项才可以。如果不显式指定，则继续使用默认目录：~/mysql-sandboxes。例如下面部署实例3353，依然使用默认目录。
MySQL  Py > dba.deploy_sandbox_instance(3353)
A new MySQL sandbox instance will be created on this host in 
/root/mysql-sandboxes/3353
接下来的方式直接在 MySQL Shell 的Shell 组件里指定基本部署目录，对全局有效。
##### 2. 显式设置shell 组件的 options 字典属性，修改 KEY 名为 sandboxDir 的值为指定目录：
- sandboxDir: default path where the new sandbox instances for InnoDB cluster will be deployed
设置 sandboxDir 为 /tmp/mysql-sandbox ： &#8211;persist 为永久生效，类似 MySQL 里的 set persist 语法效果。
MySQL  Py > \option --persist sandboxDir /tmp/mysql-sandbox
重新进入 MySQL Shell 环境，部署两个新实例，对应端口分别为3353和3354：这两个实例都被部署在目录/tmp/mysql-sandbox下。
MySQL  Py > for i in range(3353,3355):
->     dba.deploy_sandbox_instance(i)
-> 
A new MySQL sandbox instance will be created on this host in 
/tmp/mysql-sandbox/3353
...
A new MySQL sandbox instance will be created on this host in 
/tmp/mysql-sandbox/3354
...
#### 三、如何更改新部署的实例参数：
上面部署的几个实例都没有设定具体参数，只使用了默认值。不管部署的实例用于什么场景，有些参数还是要随场景更改的。 更改参数有以下两种方式：
##### 1. 部署实例的同时对参数进行配置：适合更改少量参数。
比如新部署一个实例3355，分别指定以下参数：
server-id=1000
tmp_table_size=64M
read_buffer_size=1M
添加这几个参数到 mysqldOptions 数组即可。
MySQL  Py > dba.deploy_sandbox_instance(3355,{"mysqldOptions":["server_id=1000","tmp_table_size=64M","read_buffer_size=1M"]})
A new MySQL sandbox instance will be created on this host in 
/tmp/mysql-sandbox/3355
...
Instance localhost:3355 successfully deployed and started.
Use shell.connect('root@localhost:3355') to connect to the instance.
确认 my.cnf 已经更改成功：
root@ytt-normal:/tmp/mysql-sandbox/3355# grep "server_id\|tmp_table_size\|read_buffer_size" my.cnf      server_id = 1000      tmp_table_size = 64M      read_buffer_size = 1M
##### 2. 部署实例后对参数进行配置：适合更改大量参数。
直接更改对应的 my.cnf ，完了重启即可。
#### 总结：
使用MySQL Shell 的 DBA 组件可以很方便的部署MySQL实例，但是不建议上生产，因为进入 MySQL Shell 环境后，可以对这些实例随意维护，风险加大。