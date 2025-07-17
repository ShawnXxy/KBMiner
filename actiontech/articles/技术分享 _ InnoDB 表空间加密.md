# 技术分享 | InnoDB 表空间加密

**原文链接**: https://opensource.actionsky.com/20191009-innodb/
**分类**: 技术干货
**发布时间**: 2019-10-09T00:55:30-08:00

---

> **本文目录：**
一、表空间加密概述
1. 应⽤场景
2. 加密插件
3. 加密限制
4. 注意事项
二、加密表空间
1. 安装加密插件
2. 配置表空间加密
3. 查看表空间被加密的表
三、更新 master encryption key
四、导⼊导出
1. 案例
五、备份恢复
1. innobackupex
六、参考文档
**一、表空间加密概述**从 5.7.11 开始，InnoDB 支持对独立表空间进行静态数据加密。该加密是在引擎内部数据页级别的加密手段，在数据页写入文件系统时加密，从文件读到内存中时解密，目前广泛使用的是 YaSSL/OpenSSL 提供的 AES 加密算法，加密前后数据页大小不变，因此也称为透明加密。它使用两层加密密钥架构，包括 master encryption key 和 tablespace key：
- master encryption key 用于加密解密 tablespace key。当对一个表空间加密时，一个 tablespace key 会被加密并存储在该表表空间的头部
- tablespace key 用于加密表空间文件。当访问加密表空间时， 
∘ InnoDB 会先用 master encryption key 解密存储在表空间中的加密 tablespace key，得到明文的 tablespace key 后，再用 tablespace key 解密数据
- tablespace key 解密后的明文信息基本不变（除非进行 alter table test_1 encrytion=NO, alter table test_1 encrytion=YES）。而 master key 可以随时改变（比如使用 ALTER INSTANCE ROTATE INNODB MASTER KEY;），这个称为 master key rotation。因为 tablespace key 的明文不会变，所以更新 master encryption key 之后只需要把 tablespace key 重新加密写入第一个页中即可。
1. 应用场景未配置表空间加密时，当发生类似拖库操作时，数据极可能会泄漏。
配置表空间加密时，如果没有加密时使用的 keyring（该文件由 keyring_file_data 参数设定），是读取不到加密表空间数据的。所以当发生类似拖库操作时，没有相关的 keyring 文件时，数据基本不会泄漏的。这就要求存储的 keyring 一定要严加保管，可以采取以下措施来保存 keyring：
- 避免将 keyring 文件与表空间文件放在一块
- keyring 文件所在目录的权限需要严格控制
- 使用 keyring_file 插件进行表空间加密时，keyring 文件是放在本地的，这个相对不够安全。但可以将其放到非本地中，需要时复制到相关目录（比如重启数据库、更新 master encryption key，不需要时删除该文件即可
2. 加密插件InnoDB 表空间加密依赖插件进行加密。企业版提供以下四种插件：
keyring_file，keyring_encrypted_file，keyring_okv，keyring_aws。社区版目前只能使用 keyring_file 进行加密，本文仅介绍 keyring_file 插件：
- 企业版更加安全。因为对密钥也加密存储了，而社区版的密钥是放在本地存储的，相对不够安全
- 企业版支持多种后端存储密钥，对数据加密本身没区别
3. 加密限制- 1) AES 是唯一支持的加密算法。InnoDB 静态表空间加密使用 Electronic Codebook (ECB) 加密模式来加密 tablespace key，使用 Cipher Block Chaining (CBC) 加密模式加密数据文件
- 2) ENCRYPTION 使用该 COPY 命令而不是 INPLACE 命令进行表空间的加密
- 3) 仅支持对独立表空间加密。不支持加密其他表空间类型（如通用表空间和系统表空间）
- 4) 不能将表从加密的独立表空间移动或复制到不支持加密的表空间中
- 5) 表空间加密仅对表空间中的数据加密，不对 redo log，undo log，binary log 中的数据加密
- 6) 不允许修改已加密的表的存储引擎（修改为 innodb 存储引擎则没问题）
4. 注意事项- 1) ==在创建了第一个加密表空间、master encryption key 更新前后都必须立马备份密钥环文件。因为主加密密钥丢失后，加密表空间中的数据将无法恢复。所以加密表时，必须采取措施防止主加密密钥丢失，比如定时备份该文件#F44336 #F44336==
- 2) 从安全角度考虑，不建议将密钥环数据文件与表空间数据文件放在同一目录下
- 3) 如果数据库在正常操作期间退出或停止，一定要使用同样的加密配置来重启数据库，否则会导致以前加密的表空间无法访问
- 4) 当第一次对表空间加密时（无论是新表加密还是旧表加密），将生成第一个主加密密钥。但对于运行的数据库，移除 keyring 后，依旧可以创建、读写加密表空间（但在数据库重启或更新 master encryption key 后这些操作会失败）
- 5) 更新 master encryption key 前需确保 keyring 文件存在，如果不存在，则会更新失败，从而导致读写、创建加密表均失败
- 6) 仅当主从都配置了表空间加密，表空间加密操作才可能在主从中均执行成功
**二、加密表空间**
以下的测试案例是在如下环境进行的：
- linux 版本：7.5
- mysql 版本：MySQL 5.7.21
- 加密插件：keyring_file
1. 安装加密插件- 1) 必须先安装并配置加密插件。在启动数据库时使用 early-plugin-load 选项来指定使用的加密插件，并使用 keyring_file_data 定义加密插件存放密钥环文件的路径
∘ 需要提前创建好相关目录并调整权限，不然可能会报错
- 2) 只能使用一个加密插件，不能同时使用多个加密插件
- 3) 一旦在 MySQL 实例中创建了加密表，后续重启该实例时，必须给 early-plugin-load 指定创建加密表时使用的的加密插件。如果不这样做，则在启动服务器和InnoDB恢复期间会导致错误
- 4) 必须配置独立表空间：innodb_file_per_table=1
- `-- vim my.cnf，在 [mysqld] 下添加以下参数`
- `[mysqld]`
- `early-plugin-load="keyring_file.so"`
- `keyring_file_data=/opt/mysql/keyring/3306/keyring`
- `innodb_file_per_table=1`
- 
- `-- 创建相关目录及修改密钥环文件所在目录的权限`
- `mkdir -p /opt/mysql/keyring/3306/`
- `chown -R actiontech-universe:actiontech /opt/mysql/keyring/`
- `chown -R actiontech-mysql:actiontech-mysql /opt/mysql/keyring/3306/`
- 
- `-- 查看插件是否加载`
- `SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE 'keyring_file';`
2. 配置表空间加密
以下以 mydata.test_1 表来进行测试- `/*`
- `1. 为新表加密`
- `2. 插入数据至新表`
- `3. 取消表加密`
- `4. 开启表加密`
- `5. 查看加密表`
- `*/`
- 
- `mysql> CREATE TABLE mydata.test_1 (id INT primary key,age int) ENCRYPTION='Y';`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `mysql> insert into test_1 select 9,9;`
- `Query OK, 1 row affected (0.00 sec)`
- `Records: 1  Duplicates: 0  Warnings: 0`
- 
- `mysql> ALTER TABLE mydata.test_1 ENCRYPTION='N';`
- `Query OK, 0 rows affected (0.03 sec)`
- `Records: 0  Duplicates: 0  Warnings: 0`
- 
- `mysql> ALTER TABLE mydata.test_1 ENCRYPTION='Y';`
- `Query OK, 0 rows affected (0.02 sec)`
- `Records: 0  Duplicates: 0  Warnings: 0`
- 
- `mysql> show create table mydata.test_1;select * from mydata.test_1;`
- `+--------+------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| Table  | Create Table                                                                                                                                               |`
- `+--------+------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| test_1 | CREATE TABLE `test_1` (`
- `  `id` int(11) NOT NULL,`
- `  `age` int(11) DEFAULT NULL,`
- `  PRIMARY KEY (`id`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ENCRYPTION='Y' |`
- `+--------+------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `1 row in set (0.11 sec)`
- 
- `+----+------+`
- `| id | age  |`
- `+----+------+`
- `|  9 |    9 |`
- `+----+------+`
- `1 row in set (0.00 sec)`
- 
- `/*`
- `删除当前的 keyring，使用备份的 keyring 恢复到原路径并重启，此时再查看 mydata.test_1 会查看成功。因为 mydata.test_1 加密解密用的 keyring 一样`
- `*/`
- 
- `[root@localhost ~]# rm -rf /opt/mysql/keyring/3306/keyring`
- `[root@localhost ~]# mv /root/keyring /opt/mysql/keyring/3306/`
- `[root@localhost ~]# systemctl restart mysqld_3306`
- `[root@localhost ~]# mysql -h10.186.63.90 -uroot -p -P3306 -e"show create table mydata.test_1;select * from mydata.test_1;"`
- `Enter password:`
- `+--------+------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| Table  | Create Table                                                                                                                                               |`
- `+--------+------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `| test_1 | CREATE TABLE `test_1` (`
- `  `id` int(11) NOT NULL,`
- `  `age` int(11) DEFAULT NULL,`
- `  PRIMARY KEY (`id`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ENCRYPTION='Y' |`
- `+--------+------------------------------------------------------------------------------------------------------------------------------------------------------------+`
- `+----+------+`
- `| id | age  |`
- `+----+------+`
- `|  9 |    9 |`
- `+----+------+`
3. 查看表空间被加密的表
通过 ENCRYPTION 选项加密表空间时，表的加密信息会存放到 INFORMATION_SCHEMA.TABLES 的 CREATE_OPTIONS 字段中。所以可以查询该表来判断表是否加密。- `-- 查看加密的表：`
- `SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';`
- 
- `-- 查看未加密的表：`
- `select concat(TABLE_SCHEMA,".",TABLE_NAME) from INFORMATION_SCHEMA.TABLES where (TABLE_SCHEMA,TABLE_NAME) not in (SELECT TABLE_SCHEMA,TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%' and table_schema not in ('information_schema','performance_schema','sys','mysql','universe')) and TABLE_SCHEMA in ('mydata');`
**三、更新 master encryption key**应定期更换 master encryption key，或者怀疑 master encryption key 已经泄露时便需要更换了。
更新 master encryption key 只会改变 master encryption key 并重新加密 tablespace keys，不会解密或者重新加密表空间。
因为 tablespace_key 的明文不会变，更新 master_key 之后只需要把 tablespace_key 重新加密写入第一个页中即可。
master encryption key 的变更是一个原子的、实例级操作，每次变更 master encryption key 时，MySQL 实例中所有的 tablespace key 都会被重新加密并保存到各自的表空间头部。因为是原子操作，所以一旦开始更新，对所有 tablespace keys 的重新加密必须全部成功；
- `-- 手动更新 master encryption key，成功后不影响加密表的使用`
- 
- `[root@localhost ~]# ll /opt/mysql/keyring/3306/keyring`
- `-rw-r----- 1 mysql mysql 155 Apr 19 02:05 /opt/mysql/keyring/3306/keyring`
- `[root@localhost ~]# mysql -h10.186.63.90 -uroot -p -P3306 -e"ALTER INSTANCE ROTATE INNODB MASTER KEY;"`
- `Enter password:`
- `[root@localhost ~]# ll /opt/mysql/keyring/3306/keyring`
- `-rw-r----- 1 mysql mysql 283 Apr 19 02:24 /opt/mysql/keyring/3306/keyring`
- `[root@localhost ~]# mysql -h10.186.63.90 -uroot -p -P3306 -e"select * from mydata.test_1;"`
- `Enter password:`
- `+----+------+`
- `| id | age  |`
- `+----+------+`
- `|  9 |    9 |`
- `+----+------+`
**四、导入导出**
为了支持 Export/Import 加密表，引入了 transfer_key，在 export 的时候随机生成一个 transfer_key，把现有的 tablespace_key 用 transfer_key 加密，并将两者同时写入 table_name.cfp 的文件中，注意这里 transfer_key 保存的是明文。Import 会读取 transfer_key 用来解密，然后执行正常的 import 操作即可，一旦 import 完成，table_name.cfg 文件会被立刻删除：- 导出加密表空间时，innodb 除了会生成 .cfg 元数据文件之外，还会生成 .cfp 文件，用于加密 tablespace key 的 transfer key。加密的 tablespace key 和 transfer key 存储在 tablespace_name.cfp 文件
- 导入加密表时，需要同时导入 tablespace_name.cfp 和加密表空间才行，InnoDB 通过 transfer key 来解密 tablespace_name.cfp 文件中的 tablespace key
导入导出流程如下：- 1) 目标库：CREATE TABLE mydata.test_1 (id INT primary key,age int) ENCRYPTION=&#8217;Y&#8217;;，建立与源库同名、同结构的表。
- 2) 目标库：ALTER TABLE test_1 DISCARD TABLESPACE;，此时会删除 .ibd 文件
- 3) 源库：use test; FLUSH TABLES test_1 FOR EXPORT;，此时会产生 .cfg、.cfp 文件
- 4) 目标库：scp root@10.186.63.90:/opt/mysql/data/3306/mydata/test_1.{ibd,cfg.cfp} .
- 5) 目标库：chown actiontech-mysql:actiontech-mysql test_1*，复制文件后，需要修改用户组及权限。
- 6) 源库：unlock tables;，此时会删除 .cfg、.cfp 文件
- 7) 目标库：ALTER TABLE test_1 IMPORT TABLESPACE;，加载表 test_1
1. 案例
源库：10.186.63.90:3306目标库：10.186.63.91:3307
- `# 在目标库中建立与源库同名、同结构的表`
- `[root@localhost ~]# fg`
- `mysql -h10.186.63.91 -uroot -p -P3307    (wd: ~)`
- `Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.`
- 
- `mysql> create database mydata;`
- `Query OK, 1 row affected (0.01 sec)`
- 
- `mysql> CREATE TABLE mydata.test_1 (id INT primary key,age int) ENCRYPTION='Y';`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `# 目标库执行 DISCARD TABLESPACE`
- `mysql> use mydata;`
- `Reading table information for completion of table and column names`
- `You can turn off this feature to get a quicker startup with -A`
- 
- `Database changed`
- `mysql> ALTER TABLE test_1 DISCARD TABLESPACE;`
- `Query OK, 0 rows affected (0.02 sec)`
- 
- `# 源库执行 flush table ... fro export`
- `[root@localhost ~]# fg`
- `mysql -h10.186.63.90 -uroot -P3306 -p`
- `mysql> use mydata;`
- `Reading table information for completion of table and column names`
- `You can turn off this feature to get a quicker startup with -A`
- 
- `Database changed`
- `mysql> show tables;`
- `+------------------+`
- `| Tables_in_mydata |`
- `+------------------+`
- `| test_1           |`
- `+------------------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> FLUSH TABLES test_1 FOR EXPORT;`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql>`
- `[1]+  Stopped                 mysql -h10.186.63.90 -uroot -P3306 -p`
- 
- 
- `# 从源库拷贝文件至目标库`
- `[root@localhost mydata]# scp root@10.186.63.90:/opt/mysql/data/3306/mydata/test_1.{ibd,cfg,cfp} .`
- `root@10.186.63.90's password:`
- `test_1.ibd                                                                                         100%   96KB  41.0MB/s   00:00`
- `root@10.186.63.90's password:`
- `test_1.cfg                                                                                         100%  400   343.7KB/s   00:00`
- `root@10.186.63.90's password:`
- `test_1.cfp                                                                                         100%  100   132.7KB/s   00:00`
- `[root@localhost mydata]# ll`
- `total 120`
- `-rw-r----- 1 actiontech-mysql actiontech-mysql    67 Sep 28 05:49 db.opt`
- `-rw-r----- 1 root             root               400 Sep 28 05:57 test_1.cfg`
- `-rw-r----- 1 root             root               100 Sep 28 05:57 test_1.cfp`
- `-rw-r----- 1 actiontech-mysql actiontech-mysql  8584 Sep 28 05:50 test_1.frm`
- `-rw-r----- 1 root             root             98304 Sep 28 05:57 test_1.ibd`
- 
- `# 修改目标库上文件的权限`
- `[root@localhost mydata]# chown actiontech-mysql:actiontech-mysql *`
- 
- `# 源库上执行 unlock tables`
- `[root@localhost mydata]# fg`
- `mysql -h10.186.63.90 -uroot -P3306 -p    (wd: ~)`
- `mysql> use mydata;`
- `Database changed`
- `mysql> unlock tables;`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `# 目标库上执行 ALTER TABLE ... IMPORT TABLESPACE;`
- `[root@localhost mydata]# fg`
- `mysql -h10.186.63.91 -uroot -p -P3307    (wd: ~)`
- `mysql> select * from mydata.test_1;`
- `ERROR 1814 (HY000): Tablespace has been discarded for table 'test_1'`
- `mysql> ALTER TABLE test_1 IMPORT TABLESPACE;`
- `Query OK, 0 rows affected (0.05 sec)`
- 
- `mysql> select * from mydata.test_1;`
- `Empty set (0.00 sec)`
**五、备份恢复**
**1) mysqlbackup 备份恢复**https://dev.mysql.com/doc/mysql-enterprise-backup/4.1/en/meb-encrypted-innodb.html
**2) innobackupex 备份恢复**https://www.percona.com/doc/percona-xtrabackup/LATEST/advanced/encrypted_innodb_tablespace_backups.html#encrypted-innodb-tablespace-backups
mysqlbackup innobackupex 均可以对加密表空间进行加密，只不过需要注意版本：- mysqlbackup 4.1.0 及更新的版本支持 MySQL 5.7.20 及更早版本的加密表空间备份；mysqlbackup 4.1.1 及更新版本则支持 MySQL 5.7 的加密表空间备份
- innobackupex 支持加密表空间备份恢复的最小版本没查到相关说明
这里以 innobackupex 2.4.5 为例进行加密表空间的备份恢复。
1. innobackupex
- innobackupex 备份加密表空间的注意事项：innobackupex 仅支持使用 keyring_file、keyring_vault 插件加密表空间的备份
- innobackupex 不会复制密钥环文件到备份目录中，所以需要手动复制密钥环文件到配置文件指定的 keyring-file-data 路径
∘ 如果备份前后密钥环文件不同，则在还原时应该使用旧的密钥环文件
备份 10.186.63.90 中的数据至 10.186.63.91:3307- `# 全量备份：加密表空间的全备的流程与常规的备份恢复基本一样，只是需要额外指定一个参数：--keyring-file-data`
- 
- `mkdir /data2/all_backup`
- `/data/urman-agent/bin/innobackupex --defaults-file=/opt/mysql/etc/3306/my.cnf --user=root --password=test -P3306 --socket=/opt/mysql/data/3306/mysqld.sock --parallel=8 --keyring-file-data=/opt/mysql/keyring/3306/keyring --no-timestamp /data2/all_backup`
- 
- `# apply-log`
- `/data/urman-agent/bin/innobackupex --apply-log --keyring-file-data=/opt/mysql/keyring/3306/keyring /data2/all_backup/`
- 
- `# 复制全备文件、keyring 文件至目标库`
- `rm -rf /opt/mysql/data/3307/* && rm -rf /opt/mysql/keyring/3307/keyring  && rm -rf /opt/mysql/log/redolog/3307/ib_logfile*`
- `scp -r /data2/all_backup/ root@10.186.63.91:/data2/`
- `scp /opt/mysql/keyring/3306/keyring root@10.186.63.91:/opt/mysql/keyring/3307`
- 
- `# copy back`
- `/data/urman-agent//bin/innobackupex --defaults-file=/opt/mysql/etc/3307/my.cnf --copy-back --keyring-file-data=/opt/mysql/keyring/3307/keyring /data2/all_backup/`
- 
- `# 修改权限`
- `chown actiontech-mysql:actiontech-mysql /opt/mysql/keyring/3307/keyring`
- `chown -R actiontech-mysql:actiontech-mysql /opt/mysql/data/3307/*`
- `chown -R actiontech-mysql:actiontech-mysql /opt/mysql/log/redolog/*`
- 
- `# 启动`
- `systemctl start mysqld_3307`
**六、参考文档**
**1) 14.6.3.8 InnoDB Tablespace EncryptionInnoDB**
https://dev.mysql.com/doc/refman/5.7/en/innodb-tablespace-encryption.html#innodb-tablespace-encryption-about
**2) 表空间加密－原理篇**
http://mysql.taobao.org/monthly/2018/04/01/
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