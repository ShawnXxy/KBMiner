# 技术分享 | 两个单机 MySQL 该如何校验数据一致性

**原文链接**: https://opensource.actionsky.com/20220125-mysql-2/
**分类**: MySQL 新特性
**发布时间**: 2022-01-25T00:25:13-08:00

---

作者：莫善
某互联网公司高级 DBA。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
### 需求介绍
业务有两个 MySQL 集群是通过 MQ 进行同步的，昨晚 MQ 出现异常，报了很多主键冲突，想请 dba 帮忙校验一下两个集群的数据是否一致。
### 一、前言
当接到这个需求的时候并没当回事，隐约有点印象 pt-table-checksum 能通过 dsn 实现 MySQL 的数据校验，所以当时就应承下来了。不曾想，啪啪打脸，回想起来真是草率了。
本文参考的是 pt-table-checksum 的校验逻辑，基于数据块去遍历每个表，然后比对 checksum 的值判断该块是否一致，本文主要是想聊聊我在实现数据校验脚本过程中遇到的问题以及解决思路，希望对大家有帮助。
### 二、测试 dsn
利用线上的配置文件搭建一套主从环境。
> 
- 
搭建步骤略
- 
本例使用 mysql 5.7.26 进行测试
- 
本例使用 percona-toolkit-3.2.1 进行测试
#### 1、校验主从数据一致性
这个用例将通过 dsn 方式连接从库。
> 
配置 dsn 过程略
`$ ./bin/pt-table-checksum h='192.168.1.1',u='mydba',p='test123456',P=6666 --nocheck-replication-filters --replicate=test.checksums --no-check-binlog-format -d dbatest1  --recursion-method dsn=t=percona_schema.dsns
Checking if all tables can be checksummed ...
Starting checksum ...
TS ERRORS  DIFFS     ROWS  DIFF_ROWS  CHUNKS SKIPPED    TIME TABLE
01-13T17:48:20      0      0        0          0       1       0   0.377 dbatest1.dbatest
`
> 
可以看到测试通过，能正常做校验。
#### 2、校验非主从数据一致性
这个用例将通过 dsn 方式连接从库，但是会将从库的复制链路 stop 掉，并清空复制信息。
`mysql> stop slave;
Query OK, 0 rows affected (0.01 sec)
mysql> reset slave all;
Query OK, 0 rows affected (0.01 sec)
mysql> 
`
`$ ./bin/pt-table-checksum h='192.168.1.1',u='mydba',p='test123456',P=6666 --nocheck-replication-filters --replicate=test.checksums --no-check-binlog-format -d dbatest1  --recursion-method dsn=t=percona_schema.dsns
Checking if all tables can be checksummed ...
Starting checksum ...
Replica mysql2 is stopped.  Waiting.
Replica mysql2 is stopped.  Waiting.
Replica mysql2 is stopped.  Waiting.
Replica mysql2 is stopped.  Waiting.
`
> 
直接翻车，可以看到校验会提示从库【is stopped.  Waiting】，这就尴尬了，pt-table-checksum 居然不支持非主从环境的数据校验，既然如此那只能另想他法了。
### 三、开发工具遇到的问题
#### 1、解决复杂的联合主键问题
###### （1）查询索引失效，或者查询报错问题
熟悉 pt-table-checksum 的朋友应该都知道，该工具是基于主键(非空唯一键)进行扫描数据行，其实这个逻辑针对整型单列主键实现起来很简单，但是如果是联合主键且是字符型，好像就没那么简单了，有兴趣的可以思考一下。下面我先说一下大致的逻辑：
第一步：判断 _min_rowid 是否为空，为空就取该表的第一行，并记作 _min_rowid 。
`if [ -z "${_min_rowid}" ]
then #拿出当前表的最小行id, 每次拿数据的起始行
_min_rowid="$(${mysql_comm} -NBe "select min(pk) from table")"
fi
`
第二步：根据 _min_rowid 作为条件进行扫描该表，取下一个数据块的数据，记录数据块的最后一行数据的主键值，记录 checksum 的值，并记下 _min_rowid 。
`select * from table where pk > ${_min_rowid} limit checksize #计算这个块的checksum值
_min_rowid="$(${mysql_comm} -NBe "select max(pk) from (select pk from table where pk > ${_min_rowid} order by pk limit checksize)a")" #记录下一个最小行pk值
`
第三步：判断_min_rowid是否为空，非空重复第二步，为空退出检查。
`if [ -z "${_min_rowid}" ]
then
break
else
continue
fi
`
通过上述三个步骤可以看到，如果是单列整型的主键，实现起来很简单，但是问题来了，业务的表的主键五花八门，有的是联合主键，有的是字符型的联合主键，还有整型+字符型的联合主键，那么上述的实现方式显然是有问题的。所以实现起来需要多考虑几个问题：
- 
需要考虑主键是否是联合主键。
> 
如果是联合主键，在取数据块的时候查询条件就是 where pk1 > xxx and pk2 > yyy
- 
需要考虑主键字段的数据类型是否是整型或字符型。
> 
如果主键字段是字符型，在取数据块的时候查询条件就是 where pk > &#8216;xxx&#8217; ，否则查询将不会使用到索引。
鉴于存在上述两个问题，可以参考如下实现逻辑：
- 
获取主键字段列表，放在数组里
`pri_name=($(${mysql_comm} -NBe "select COLUMN_NAME from information_schema.columns where table_name = 'table' and table_schema = 'db' and COLUMN_KEY = 'PRI';"))
`
- 
根据主键字段名获取字段的数据类型，放在关联数组里
` for tmp in ${pri_name[@]}
do #将各个主键字段的数据类型记录到字典, 后文会判断主键字段的类型是否是字符型, 如果是字符型就需要特殊处理(带引号)
__="select DATA_TYPE from information_schema.columns where table_schema = 'db' and table_name = 'table' and COLUMN_KEY = 'PRI' and COLUMN_NAME = '${tmp}'"
pri_type["${tmp}"]="$(${mysql_comm} -NBe "${__}" 2>/dev/null)"
done
`
- 
根据字段的数据类型，如果是字符型就需要做特殊处理
`for tmp in ${pri_name[@]}
do #这步主要是解决将主键弄清楚, 到底是单列主键还是多列, 到底是整型还是其他, 然后根据不同的类型拼接成一个字符串, 主要是用来作为后面取数是否要加单引号
#因为整型取出来不用做特殊处理, 但是非整型需要加上单引号, 要不然作为where条件对比的时候肯定有问题
if [ "$(grep -ic "int" 
> 
这步的作用是说在取每个块的数据，需要记录 _min_rowid 的时候会根据主键的类型记录不一样的值，比如 :
- 
整型就记录成_min_rowid=1
- 
字符型就记录成_min_rowid='1'
- 
整型 + 字符型的联合主键就记录成_min_rowid=1,'1'
- 
字符型的联合主键就记录成_min_rowid='1','2'
> 
这样在每次取数据块的时候where后面的条件既能正确的使用索引，也不至于因为是非整型而没有带上引号而报错。
##### （2）如何界定每个数据块的左区间的边界
假如有这么一个联合主键字段 primary key(a,b,c) 都是整型，该如何编写遍历 sql 呢？起初我的想法很简单，具体如下：
`_min_rowid=(xxx,yyy,zzz)
select * from where 1 = 1 and a >= xxx and b >= yyy and c > zzz order by a,b,c limit checksize
`
> 
乍一看好像逻辑没问题，但是实际跑脚本的时候发现这个逻辑不能完全扫完全表，后来经过多次测试校验，得出下面的逻辑sql
`_min_rowid=(xxx,yyy,zzz)
select * from where 1 = 1 and ((a > xxx) or (a = xxx and b > yyy) or (a = xxx and b = yyy and c > zzz)) order by a,b,c limit checksize
`
至此在编写校验脚本过程遇到的两个问题就算告一段落了，剩下的就是各种逻辑处理了，不过多赘述，有兴趣的可以自行阅读脚本文件。
### 四、数据校验工具做了哪些改动
#### 1、取消 for update
本着最低程度影响业务，所以取消加锁逻辑。但是又要保证该数据块的数据一致性，如果这个数据块是个热数据，当前正在变更，那么校验的时候难免会不一致。所以只能通过多次校验实现，默认是校验20次，其中有一次校验结果是一致，就认为是一致的，如果前5次校验过程中，这个数据块的数据没有变化，也视为不一致（可能是因为延迟，也可能是真的不一致）。
> 
另外 checksum 状态是写到临时文件而非写到业务数据库。
#### 2、支持表结构校验
pt-table-checksum 不校验表结构，改写时添加表结构的校验。
#### 3、支持基于表的并行校验
可以基于表的并行校验，可由用户指定并行数，但是脚本有个安全机制，如果用户指定的并行数大于当前 cpu 空闲核心数，就会按当前（空闲核心数-1）作为并行数。
#### 4、支持网络监控
添加网络监控，由用户指定网络上限百分比，当网卡流量超过这个百分比就暂停任务，等待网卡流量低于阈值才会继续任务。这个主要是出于对于中间件（mycat）的场景或者分布式数据库（tidb）的场景。
#### 5、支持定时任务功能
支持定时任务功能，用户可以使用这个功能规避业务高峰，仅在业务低峰进行数据校验。
> 
指定了时间段执行校验任务，如果当天没校验完成，等到次日会继续校验。
#### 6、支持任意两个节点的校验
不仅限于主从节点的校验，只要目标对象支持 MySQL 的标准 SQL 语法就能做数据校验。
#### 7、添加超时机制及自杀机制
校验逻辑是通过 SQL 采集目标节点的数据库，如果目标数据库系统当前存在异常，无疑是雪上加霜，将会触发未知问题，所以添加超时机制，单次取数据块的阈值是5s，超过5秒就放弃等待重试。测试发现，有时候即便触发超时了，但是 SQL 任务还是会在目标数据库的 processlist 中能看到，所以又添加了一个 kill 机制，超时后会触发一个 kill processlist id 的动作。另外为了避免 kill 错，在每个 SQL 对象添加了一个32位的 md5 值，每次 kill 的时候会校验这个 md5 值。
> 
保留 threads_running 的监控，如果 threads_running 过大就会暂停校验，这部分监控逻辑是跟网络监控一起
### 五、数据校验工具使用介绍
本工具借鉴 pt-table-checksum 工具思路改写，可以检查随意两个 mysql（支持 mysql sql 语法的数据库）节点的数据一致性。
> 
本工具仅供学习使用，如需检查线上的数据，请充分测试
#### 1、校验逻辑
基于主键以一个块遍历数据表，比对checksum的值，块的大小可通过参数指定。
（1）获取该表的第一个数据块的查询SQL。
（2）将两个目标节点的数据块的checksum的值，记录到临时文件，file1 file2。
（3）比对file1 file2是否一致。
> 
- 
不一致 : 重复（2）的操作，至多连续20次，还不一致会将该SQL记录到table目录
- 
一致 : 跳到（4）
- 
file1为空 : 表示该表遍历完成，直接跳到（5）
（4）获取该表的下一个数据块的查询SQL。
（5）检查通过就跳到（7），检查不通过调到（6）。
（6）读取table目录校验不通过的SQL进行再次校验。
- 
本次校验通过也视为数据一致
- 
如果校验不通过，会将不一致的部分记录到diff目录
（7）该表校验任务结束。
#### 2、功能介绍
- 
检查随意两个几点的数据一致性
- 
支持表结构的校验
- 
支持并发检查，基于表的并发
- 
支持指定时间，可以规避业务高峰期
- 
支持网络监控，如果网络超过阈值可以暂停校验
- 
不支持无主键(非空唯一键)的表
- 
不支持联合主键达到四个字段及以上的表
#### 3、安装教程
##### （1）下载
`git clone https://gitee.com/mo-shan/check_data_for_mysql.git
cd check_data_for_mysql
`
##### （2）配置
- 
编辑配置文件
`cd /path/check_data_for_mysql
vim conf/check.conf
`
> 
请结合实际情况根据注释提示进行相关配置
- 
修改工作路径
`sed -i 's#^work_dir=.*#work_dir=\"/check_data_for_mysql_path\"#g' start.sh #将这里的check_data_for_mysql_path改成check_data_for_mysql的家目录的绝对路径
`
#### 4、使用说明
##### （1）目录介绍
`moshan /data/git/check_data_for_mysql > tree -L 2
.
├── conf
│   └── check.conf
├── func
│   ├── f_check_diff_for_mysql.sh
│   ├── f_check_diff_for_row.sh
│   ├── f_logging.sh
│   └── f_switch_time.sh
├── log
├── manager.sh
├── README.en.md
├── README.md
└── start.sh
3 directories, 9 files
moshan /data/git/check_data_for_mysql >
`
- 
conf 配置文件的目录，check.conf 是配置文件
- 
log 日志目录
- 
start.sh 主程序
- 
manager.sh 网络监控脚本，任务状态的管理脚本
- 
func 目录是存放脚本的目录
> 
- 
f_check_diff_for_mysql.sh 校验数据块的脚本
- 
f_check_diff_for_row.sh 校验数据行，这个脚本是将f_check_diff_for_mysql.sh校验不通过的结果做进一步校验
##### （2）帮助手册
- 
主程序
`moshan /data/git/check_data_for_mysql > bash start.sh
Usage: start.sh
[ -t check_table ]             需要检查的表列表, 默认整库
[ -T skip_check_table ]        不需要检查的表, 默认不过滤
[ -d check_db ]                需要检查的库, 默认是除了系统库以外的所有库
[ -D skip_check_db ]           不需要检查的库, 默认不过滤
[ -w threads ]                 最大并发数
[ -l limit_time ]              哪些时间段允许跑校验, 默认是所有时间, 如需限制可以使用该参数进行限制, 多个时间用英文逗号隔开
1-5,10-15   表示1点到5点(包含1点和5点), 或者10点到15点可以跑, 需要注意都是闭区间的
1,5,10,15   表示1点, 5点, 10点, 15点可以跑
[ -f true ]                    是否执行check操作, 默认是false, 只有为true的时候才会check
[ -h ]                         帮助信息
moshan /data/git/check_data_for_mysql >
`
> 
可以根据需求进行参数使用，如需规避业务高峰期在低峰执行校验任务，请使用-l参数指定执行时间 ，如'-l 1-5'表示凌晨1点到5点执行校验任务，如果当天六点前没校验完成，会等到次日凌晨1点继续校验
- 
任务管理脚本
`moshan /data/git/check_data_for_mysql > bash manager.sh -h
Usage: manager.sh
[ -a start|stop|continue|pause ]     监控任务的管理动作, 数据校验任务的管理动作
start : 启动网络监控
stop|pause|continue : 连同校验脚本一起停掉|暂停|继续
[ -t eth0 ]                          网卡设备名, 默认是eth0
[ -n 50 ]                            网卡流量超过这个百分比就暂停, 等网卡流量小于这个就继续, 默认是50
[ -h ]                               帮助信息
moshan /data/git/check_data_for_mysql > 
`
> 
可以根据实际网卡信息针对该网卡进行监控，当流量达到指定的阈值就会暂时暂停数据校验。这个脚本主要是针对使用了中间件，比如mycat（mysql到mycat）。或者是tidb（tikv到tidb），这种情况下回占用较多网络带宽。
- 
该脚本必须要求在整个工具的家目录下执行
##### （3）常用命令参考
- 
管理脚本相关
> 
- 
bash manager.sh -a start -t eth0 -n 30 启动eth0网卡的流量监控，流量达到30%就暂停数据校验
- 
bash manager.sh -a pause 暂停监控及暂停数据校验任务
- 
bash manager.sh -a continue 继续监控及继续数据校验
- 
bash manager.sh -a stop 停止监控及停止数据校验
- 
主程序相关
> 
- 
bash start.sh -f true -d dbatest -t test1 -l 0-5 仅校验dbatest库下的test表，且在0点到5点执行校验任务
##### （4）测试用例-校验通过场景
- 
每次执行校验任务的时候强制要清空log目录，所以请做好校验结果的备份
- 
执行校验任务的时候强烈建议开启screen
- 
有网卡监控需求，执行监控脚本时也强烈建议单独开启 screen 进行监控 
第一步：先开启一个 screen 监控网络
`moshan /data/git/check_data_for_mysql > screen -S check_net_3306
moshan /data/git/check_data_for_mysql > bash manager.sh -a start
[ 2022-01-18 11:55:34 ] [ 1000 Mb/s ] [ RX : 2    MB/S ]  [ TX : 2    MB/S ]
[ 2022-01-18 11:55:35 ] [ 1000 Mb/s ] [ RX : 2    MB/S ]  [ TX : 4    MB/S ]
[ 2022-01-18 11:55:36 ] [ 1000 Mb/s ] [ RX : 2    MB/S ]  [ TX : 2    MB/S ]
[ 2022-01-18 11:55:37 ] [ 1000 Mb/s ] [ RX : 2    MB/S ]  [ TX : 3    MB/S ]
[ 2022-01-18 11:55:38 ] [ 1000 Mb/s ] [ RX : 1    MB/S ]  [ TX : 2    MB/S ]
[ 2022-01-18 11:55:39 ] [ 1000 Mb/s ] [ RX : 1    MB/S ]  [ TX : 2    MB/S ]
[ 2022-01-18 11:55:41 ] [ 1000 Mb/s ] [ RX : 1    MB/S ]  [ TX : 2    MB/S ]
[ 2022-01-18 11:55:42 ] [ 1000 Mb/s ] [ RX : 2    MB/S ]  [ TX : 8    MB/S ]
`
第二步：新开启一个screen执行校验任务
`moshan /data/git/check_data_for_mysql > screen -S check_data_3306
moshan /data/git/check_data_for_mysql > bash start.sh -d dba -t dbatest1 -f true 
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_prepare:130 ] [ 本次数据一致性检查开始 ]
[ 2022-01-17 20:32:19 ] [ 警告 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:185 ] [ 本次数据一致性检查将检查如下库 : [dba] ]
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:203 ] [ 正在检查dba库 ]
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ func/f_check_diff_for_mysql.sh ] [ f_check_diff_for_mysql:249 ] [ dba.dbatest1 ] [ 表结构一致 ]
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ func/f_check_diff_for_mysql.sh ] [ f_check_diff_for_mysql:491 ] [ dba.dbatest1 ] [ 1,1 ] [ 00 d 00 h 00 m 00 s ] [ 9.09%, (0:0)/1 ] [ 数据一致 ]
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ func/f_check_diff_for_mysql.sh ] [ f_check_diff_for_mysql:491 ] [ dba.dbatest1 ] [ 2,11 ] [ 00 d 00 h 00 m 00 s ] [ 100.00%, (0:0)/1 ] [ 数据一致 ]
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ func/f_check_diff_for_mysql.sh ] [ f_check_diff_for_mysql:504 ] [ dba.dbatest1 ] [ 检查完毕 ]
[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:242 ] [ 本次数据一致性检查完成 ] [ 通过 ]
moshan /data/git/check_data_for_mysql > 
`
> 
检查结束后会提示检查通过，否则就是检查不通过，如下面的用例。
##### （5）测试用例-校验不通过场景
- 
执行校验任务的时候强烈建议开启 screen
`moshan /data/git/check_data_for_mysql > screen -S check_data_3306
moshan /data/git/check_data_for_mysql > bash start.sh -d dbatest1 -f true 
[ 2022-01-17 20:32:09 ] [ 成功 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_prepare:130 ] [ 本次数据一致性检查开始 ]
[ 2022-01-17 20:32:09 ] [ 警告 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:185 ] [ 本次数据一致性检查将检查如下库 : [dbatest1] ]
[ 2022-01-17 20:32:09 ] [ 成功 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:203 ] [ 正在检查dbatest1库 ]
[ 2022-01-17 20:32:09 ] [ 警告 ] [ 192.168.1.1 ] [ func/f_check_diff_for_mysql.sh ] [ f_check_diff_for_mysql:242 ] [ dbatest1.dbatest ] [ 表结构不一致 ] [ a_time name ] [ 跳过该表的检查 ]
[ 2022-01-17 20:32:09 ] [ 错误 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:232 ] [ 本次数据一致性检查完成 ] [ 不通过 ]
[ 2022-01-17 20:32:09 ] [ 错误 ] [ 192.168.1.1 ] [ start.sh/start.sh ] [ f_main:237 ] [ dbatest1.dbatest:table structure err ]
moshan /data/git/check_data_for_mysql >
`
#### 5、测试结果解读
`moshan /data/git/check_data_for_mysql > ls -l
total 444
-rw-r--r-- 1 root root 450389 Jan 18 11:56 info.log
drwxr-xr-x 2 root root    194 Jan 18 11:56 list
drwxr-xr-x 2 root root      6 Jan 18 11:56 md5
drwxr-xr-x 6 root root     72 Jan 18 11:56 pri
drwxr-xr-x 5 root root     42 Jan 18 11:52 res
-rw-r--r-- 1 root root     65 Jan 18 11:56 skip.log
moshan /data/git/check_data_for_mysql > 
`
（1）info.log 文件
> 
校验的日志，会将数据库的数据是否一致一一记录，如下是一行日志记录。
`[ 2022-01-17 20:32:19 ] [ 成功 ] [ 192.168.1.1 ] [ func/f_check_diff_for_mysql.sh ] [ f_check_diff_for_mysql:491 ] [ dba.dbatest1 ] [ 2,11 ] [ 00 d 00 h 00 m 00 s ] [ 100.00%, (0:0)/1 ] [ 数据一致 ]
`
> 
- 
[ 2022-01-17 20:32:19 ] 第一段是记录日志的时间
- 
[ 成功 ] 第二段是日志状态
- 
[ 192.168.1.1 ] 第三段是产生日志的机器 ip
- 
[ func/f_check_diff_for_mysql.sh ] 第四段是哪个文件产生的日志
- 
[ f_check_diff_for_mysql:491 ] 第五段是哪个函数:行号产生的日志
- 
[ dba.dbatest1 ] 第六段是针对哪个 db 哪个表产生的日志
- 
[ 2,11 ] 第七段是数据块的左右闭区间
- 
[ 00 d 00 h 00 m 00 s ] 第八段是针对该表的数据校验总执行的时间
- 
[ 100.00%, (0:0)/1 ] 第九段是执行进度，其中小括号部分表示：(校验通过的表个数:校验不通过的表个数)/总共需要校验的表的个数
- 
[ 数据一致 ] 第十段是数据一致状态。
（2）list目录
`-rw-r--r-- 1 root root  77 Jan 18 11:52 dba_ing.list
-rw-r--r-- 1 root root  77 Jan 18 11:56 dba.list
`
> 
这个目录会针对每个 db 记录两个文件，一个是已经校验通过的表，另一个是正在校验的表。
（3）md5 目录
> 
保存数据块的 checksum 临时目录，可以忽略
（4）pri 目录
> 
这个目录会针对每个 db 都创建一个目录，然后记录每个表当前校验的数据块的最后一行数据的 pk(pk list)值
（5）res 目录
> 
这个目录是记录校验结果的目录，会有三个子目录
`drwxr-xr-x 2 root root 6 Jan 18 11:52 diff
drwxr-xr-x 2 root root 6 Jan 18 11:52 row
drwxr-xr-x 2 root root 6 Jan 18 11:56 table
`
> 
- 
table : f_check_diff_for_mysql.sh 脚本会将校验不通过的数据块的SQL记录在这里。这个目录会按db创建目录，将记录校验不通过的数据块的SQL语句格式如下："table/db/table.log"
- 
row : f_check_diff_for_row.sh 脚本会读取table目录的SQL语句进行再次校验，然后产生的的临时文件存在row目录，可以忽略
- 
diff : f_check_diff_for_row.sh 脚本会读取table目录的SQL语句进行再次校验，然后产生的再次校验不通过的部分存记录到这个目录，格式如下："diff/db.table.num.diff"
这是 table 目录下记录某个数据块不一致的一个例子
`set tx_isolation='REPEATABLE-READ';set innodb_lock_wait_timeout=1;SELECT '127d04065afd91d587bbb19bc16037a6:mobile_bind', COUNT(*) AS cnt, COALESCE(LOWER(CONV(BIT_XOR(CAST(CRC32(CONCAT_WS('#',`id`,`uid`,`count`,`score`,`timestamp`,`info`,`mobile_info`,`del`,CONCAT(ISNULL(`id`),ISNULL(`uid`),ISNULL(`count`),ISNULL(`score`),ISNULL(`timestamp`),ISNULL(`info`),ISNULL(`mobile_info`),ISNULL(`del`)))) AS UNSIGNED)), 10, 16)), 0) AS crc FROM (select * from tdb_spam_oltp.`mobile_bind` where 1 = 1 and id > 667930554 order by id limit 10000 )a
`
> 
如果校验某个数据块发现两个节点数据不一致会记录这个 SQL
- 
一来是方便f_check_diff_for_row.sh脚本再次校验
- 
二来是方便用户再次确认是真的不一致还是因为这是热数据，在校验的时候正在频繁被修改
这是 diff 目录下记录某个数据行不一致的一个例子
`7974c7974
667930554 1   1642491495866595584 100 948895134572797275  2022-01-10 16:01:30 2022-01-10 16:32:01 {"dlvBoid":7877725947093058957} -667930554
`
> 
同一个主键，如果数据不一致会以这样的格式记录到 diff 目录
（6）skip.log 文件
> 
检查不通过在log目录都会生成一个 skip.log 文件, 里面记录了哪些表被跳过检查及跳过原因，如果检查通过就不会有这个文件。
`moshan /data/git/check_data_for_mysql > ls -l log/skip.log 
-rw-r--r-- 1 root root 37 Jan 17 20:35 log/skip.log
moshan /data/git/check_data_for_mysql > cat log/skip.log 
dbatest1.dbatest:table structure err
moshan /data/git/check_data_for_mysql >
`
### 六、写在最后
本工具是参考了 pt-table-checksum 工具的一些思路并结合自身经验进行改写，尚有很多不足之处，仅做学习交流之用，如有线上环境使用需求，请在测试环境充分测试。