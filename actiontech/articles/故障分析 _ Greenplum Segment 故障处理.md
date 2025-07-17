# 故障分析 | Greenplum Segment 故障处理

**原文链接**: https://opensource.actionsky.com/20230130-greenplum/
**分类**: 技术干货
**发布时间**: 2023-01-29T22:01:33-08:00

---

作者：杨文
DBA，负责客户项目的需求与维护，会点数据库，不限于MySQL、Redis、Cassandra、GreenPlum、ClickHouse、Elastic、TDSQL等等。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一、前情提要：
我们知道Greenplum集群由Master Severs和Segment Severs组成。其中故障存在三种类别：Master故障、Segment故障、数据异常。之前我们已经聊过“Master故障”和“数据异常”的处理方式，今天将介绍Segment故障的处理方式。
#### 二、本地模拟故障环境：
###### 2.1、第一种情况：段故障。
[gpadmin@master ~]$ gpstate
20221127:22:39:00:022659 gpstate:master:gpadmin-[INFO]:-Starting gpstate with args: 
20221127:22:39:00:022659 gpstate:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:22:39:00:022659 gpstate:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:22:39:00:022659 gpstate:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:22:39:00:022659 gpstate:master:gpadmin-[INFO]:-Gathering data from segments...
...
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-Greenplum instance status summary
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Master instance                                           = Active
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Master standby                                            = standby
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Standby master state                                      = Standby host passive
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total segment instance count from metadata                = 40
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Primary Segment Status
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total primary segments                                    = 20
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total primary segment valid (at master)                   = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total primary segment failures (at master)                = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number of postmaster.pid files missing              = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number of postmaster.pid files found                = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number of postmaster.pid PIDs missing               = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number of postmaster.pid PIDs found                 = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number of /tmp lock files missing                   = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number of /tmp lock files found                     = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number postmaster processes missing                 = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number postmaster processes found                   = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Mirror Segment Status
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total mirror segments                                     = 20
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total mirror segment valid (at master)                    = 20
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total mirror segment failures (at master)                 = 0
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number of postmaster.pid files missing              = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number of postmaster.pid files found                = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number of postmaster.pid PIDs missing               = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number of postmaster.pid PIDs found                 = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number of /tmp lock files missing                   = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number of /tmp lock files found                     = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number postmaster processes missing                 = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number postmaster processes found                   = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[WARNING]:-Total number mirror segments acting as primary segments   = 4                      <<<<<<<<
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-   Total number mirror segments acting as mirror segments    = 16
20221127:22:39:03:022659 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
[gpadmin@master ~]$ gpstate -m
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-Starting gpstate with args: -m
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:--------------------------------------------------------------
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:--Current GPDB mirror list and status
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:--Type = Group
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:--------------------------------------------------------------
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   Mirror       Datadir                            Port    Status              Data Status    
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data02       /greenplum/gpdata/mirror/gpseg0    56000   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data02       /greenplum/gpdata/mirror/gpseg1    56001   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data02       /greenplum/gpdata/mirror/gpseg2    56002   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data03       /greenplum/gpdata/mirror/gpseg3    56000   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data03       /greenplum/gpdata/mirror/gpseg4    56001   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data03       /greenplum/gpdata/mirror/gpseg5    56002   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data01       /greenplum/gpdata/mirror/gpseg6    56000   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data01       /greenplum/gpdata/mirror/gpseg7    56001   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data01       /greenplum/gpdata/mirror/gpseg8    56002   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-data05       /greenplum/gpdata/mirror/gpseg9    56000   Failed                             <<<<<<<<
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-data05       /greenplum/gpdata/mirror/gpseg10   56001   Failed                             <<<<<<<<
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-data05       /greenplum/gpdata/mirror/gpseg11   56002   Failed                             <<<<<<<<
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data04       /greenplum/gpdata/mirror/gpseg12   56000   Acting as Primary   Not In Sync
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data04       /greenplum/gpdata/mirror/gpseg13   56001   Acting as Primary   Not In Sync
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data04       /greenplum/gpdata/mirror/gpseg14   56002   Acting as Primary   Not In Sync
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data02       /greenplum/gpdata/mirror/gpseg15   56003   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data03       /greenplum/gpdata/mirror/gpseg16   56003   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data04       /greenplum/gpdata/mirror/gpseg17   56003   Passive             Synchronized
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-data05       /greenplum/gpdata/mirror/gpseg18   56003   Failed                             <<<<<<<<
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:-   data01       /greenplum/gpdata/mirror/gpseg19   56003   Acting as Primary   Not In Sync
20221127:22:44:55:023196 gpstate:master:gpadmin-[INFO]:--------------------------------------------------------------
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-4 segment(s) configured as mirror(s) are acting as primaries
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-4 segment(s) configured as mirror(s) have failed
20221127:22:44:55:023196 gpstate:master:gpadmin-[WARNING]:-4 mirror segment(s) acting as primaries are not synchronized
2.2、第二种情况：表空间故障。
[gpadmin@data05 ~]$ cd /greenplum/gpdata/mirror/gpseg10
[gpadmin@data05 gpseg10]$ ls
backup_label.old    gpmetrics               pg_clog            pg_logical    pg_stat                PG_VERSION            postmaster.pid
base                gpperfmon               pg_distributedlog  pg_multixact  pg_stat_tmp            pg_xlog               recovery.conf
fts_probe_file.bak  gpsegconfig_dump        pg_dynshmem        pg_notify     pg_subtrans            postgresql.auto.conf  recovery.done
global              gpssh.conf              pg_hba.conf        pg_replslot   pg_tblspc              postgresql.conf
gpexpand.pid        internal.auto.conf      pg_ident.conf      pg_serial     pg_twophase            postgresql.conf.bak
gpexpand.status     internal.auto.conf.bak  pg_log             pg_snapshots  pg_utilitymodedtmredo  postmaster.opts
[gpadmin@data05 gpseg10]$ rm -rf pg_tblspc/
[gpadmin@master ~]$ gpstate -e
20221127:23:13:29:026114 gpstate:master:gpadmin-[INFO]:-Starting gpstate with args: -e
20221127:23:13:29:026114 gpstate:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:23:13:29:026114 gpstate:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:23:13:29:026114 gpstate:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:23:13:29:026114 gpstate:master:gpadmin-[INFO]:-Gathering data from segments...
20221127:23:13:30:026114 gpstate:master:gpadmin-[WARNING]:-pg_stat_replication shows no standby connections
20221127:23:13:30:026114 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:23:13:30:026114 gpstate:master:gpadmin-[INFO]:-Segment Mirroring Status Report
20221127:23:13:30:026114 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:23:13:30:026114 gpstate:master:gpadmin-[INFO]:-Downed Segments (may include segments where status could not be retrieved)
20221127:23:13:30:026114 gpstate:master:gpadmin-[INFO]:-   Segment      Port    Config status   Status
20221127:23:13:30:026114 gpstate:master:gpadmin-[INFO]:-   data05       56001   Up              Process error -- database process may be down
#### 三、故障分析及解决：
##### 3.1、针对“2.1”情况的处理：
在线生成一个配置文件：
[gpadmin@master ~]$ gprecoverseg -o ./recover1
20221127:22:48:41:023405 gprecoverseg:master:gpadmin-[INFO]:-Starting gprecoverseg with args: -o ./recover1
20221127:22:48:41:023405 gprecoverseg:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:22:48:41:023405 gprecoverseg:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:22:48:41:023405 gprecoverseg:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:22:48:41:023405 gprecoverseg:master:gpadmin-[INFO]:-Configuration file output to ./recover1 successfully.
[gpadmin@master ~]$ more recover1
data05|55000|/greenplum/gpdata/primary/gpseg12
data05|55001|/greenplum/gpdata/primary/gpseg13
data05|55002|/greenplum/gpdata/primary/gpseg14
data05|55003|/greenplum/gpdata/primary/gpseg19
通过生成的配置文件进行修复集群：
[gpadmin@master ~]$ gprecoverseg -i ./recover1 -a
检查状态：
[gpadmin@master ~]$ gpstate -e
20221127:22:56:57:024771 gpstate:master:gpadmin-[INFO]:-Starting gpstate with args: -e
20221127:22:56:57:024771 gpstate:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:22:56:57:024771 gpstate:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:22:56:57:024771 gpstate:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:22:56:57:024771 gpstate:master:gpadmin-[INFO]:-Gathering data from segments...
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-Segment Mirroring Status Report
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-Segments with Primary and Mirror Roles Switched
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-   Current Primary   Port    Mirror       Port
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-   data04            56000   data05       55000
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-   data04            56001   data05       55001
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-   data04            56002   data05       55002
20221127:22:56:58:024771 gpstate:master:gpadmin-[INFO]:-   data01            56003   data05       55003
[gpadmin@master ~]$ psql -c "select * from gp_segment_configuration order by content asc,dbid;"
dbid | content | role | preferred_role | mode | status | port  | hostname | address |             datadir              
------+---------+------+----------------+------+--------+-------+----------+---------+-----------------------------------
44 |      -1 | p    | p              | s    | u      |  5432 | master   | master  | /greenplum/gpdata/master/gpseg-1
45 |      -1 | m    | m              | s    | u      |  5432 | standby  | standby | /greenplum/gpdata/master/gpseg-1
2 |       0 | p    | p              | s    | u      | 55000 | data01   | data01  | /greenplum/gpdata/primary/gpseg0
11 |       0 | m    | m              | s    | u      | 56000 | data02   | data02  | /greenplum/gpdata/mirror/gpseg0
3 |       1 | p    | p              | s    | u      | 55001 | data01   | data01  | /greenplum/gpdata/primary/gpseg1
12 |       1 | m    | m              | s    | u      | 56001 | data02   | data02  | /greenplum/gpdata/mirror/gpseg1
4 |       2 | p    | p              | s    | u      | 55002 | data01   | data01  | /greenplum/gpdata/primary/gpseg2
13 |       2 | m    | m              | s    | u      | 56002 | data02   | data02  | /greenplum/gpdata/mirror/gpseg2
5 |       3 | p    | p              | s    | u      | 55000 | data02   | data02  | /greenplum/gpdata/primary/gpseg3
14 |       3 | m    | m              | s    | u      | 56000 | data03   | data03  | /greenplum/gpdata/mirror/gpseg3
6 |       4 | p    | p              | s    | u      | 55001 | data02   | data02  | /greenplum/gpdata/primary/gpseg4
15 |       4 | m    | m              | s    | u      | 56001 | data03   | data03  | /greenplum/gpdata/mirror/gpseg4
7 |       5 | p    | p              | s    | u      | 55002 | data02   | data02  | /greenplum/gpdata/primary/gpseg5
16 |       5 | m    | m              | s    | u      | 56002 | data03   | data03  | /greenplum/gpdata/mirror/gpseg5
8 |       6 | p    | p              | s    | u      | 55000 | data03   | data03  | /greenplum/gpdata/primary/gpseg6
17 |       6 | m    | m              | s    | u      | 56000 | data01   | data01  | /greenplum/gpdata/mirror/gpseg6
9 |       7 | p    | p              | s    | u      | 55001 | data03   | data03  | /greenplum/gpdata/primary/gpseg7
18 |       7 | m    | m              | s    | u      | 56001 | data01   | data01  | /greenplum/gpdata/mirror/gpseg7
10 |       8 | p    | p              | s    | u      | 55002 | data03   | data03  | /greenplum/gpdata/primary/gpseg8
19 |       8 | m    | m              | s    | u      | 56002 | data01   | data01  | /greenplum/gpdata/mirror/gpseg8
21 |       9 | p    | p              | s    | u      | 55000 | data04   | data04  | /greenplum/gpdata/primary/gpseg9
30 |       9 | m    | m              | s    | u      | 56000 | data05   | data05  | /greenplum/gpdata/mirror/gpseg9
22 |      10 | p    | p              | s    | u      | 55001 | data04   | data04  | /greenplum/gpdata/primary/gpseg10
31 |      10 | m    | m              | s    | u      | 56001 | data05   | data05  | /greenplum/gpdata/mirror/gpseg10
23 |      11 | p    | p              | s    | u      | 55002 | data04   | data04  | /greenplum/gpdata/primary/gpseg11
32 |      11 | m    | m              | s    | u      | 56002 | data05   | data05  | /greenplum/gpdata/mirror/gpseg11
24 |      12 | m    | p              | s    | u      | 55000 | data05   | data05  | /greenplum/gpdata/primary/gpseg12
27 |      12 | p    | m              | s    | u      | 56000 | data04   | data04  | /greenplum/gpdata/mirror/gpseg12
25 |      13 | m    | p              | s    | u      | 55001 | data05   | data05  | /greenplum/gpdata/primary/gpseg13
28 |      13 | p    | m              | s    | u      | 56001 | data04   | data04  | /greenplum/gpdata/mirror/gpseg13
26 |      14 | m    | p              | s    | u      | 55002 | data05   | data05  | /greenplum/gpdata/primary/gpseg14
29 |      14 | p    | m              | s    | u      | 56002 | data04   | data04  | /greenplum/gpdata/mirror/gpseg14
33 |      15 | p    | p              | s    | u      | 55003 | data01   | data01  | /greenplum/gpdata/primary/gpseg15
39 |      15 | m    | m              | s    | u      | 56003 | data02   | data02  | /greenplum/gpdata/mirror/gpseg15
34 |      16 | p    | p              | s    | u      | 55003 | data02   | data02  | /greenplum/gpdata/primary/gpseg16
40 |      16 | m    | m              | s    | u      | 56003 | data03   | data03  | /greenplum/gpdata/mirror/gpseg16
35 |      17 | p    | p              | s    | u      | 55003 | data03   | data03  | /greenplum/gpdata/primary/gpseg17
41 |      17 | m    | m              | s    | u      | 56003 | data04   | data04  | /greenplum/gpdata/mirror/gpseg17
36 |      18 | p    | p              | s    | u      | 55003 | data04   | data04  | /greenplum/gpdata/primary/gpseg18
42 |      18 | m    | m              | s    | u      | 56003 | data05   | data05  | /greenplum/gpdata/mirror/gpseg18
37 |      19 | m    | p              | s    | u      | 55003 | data05   | data05  | /greenplum/gpdata/primary/gpseg19
38 |      19 | p    | m              | s    | u      | 56003 | data01   | data01  | /greenplum/gpdata/mirror/gpseg19
(42 rows)
可以看到所有段都是up状态了，但存在部分段角色异常。
修复角色状态：
[gpadmin@master ~]$ gprecoverseg -r
再次检查确认状态，此处省略。
##### 3.2、针对“2.2”情况的处理：
如果可以自动生成配置文件，就使用自动生成的。如果无法自动生成，则手工创建：
[gpadmin@master ~]$ vi recover2
data05|56001|/greenplum/gpdata/mirror/gpseg10
通过生成的配置文件进行修复集群：
[gpadmin@master ~]$ gprecoverseg -i ./recover2 -a
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-Starting gprecoverseg with args: -i ./recover2 -F
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-Heap checksum setting is consistent between master and the segments that are candidates for recoverseg
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-Greenplum instance recovery parameters
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:----------------------------------------------------------
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-Recovery from configuration -i option supplied
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:----------------------------------------------------------
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-Recovery 1 of 1
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:----------------------------------------------------------
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Synchronization mode                 = Full
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Failed instance host                 = data05
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Failed instance address              = data05
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Failed instance directory            = /greenplum/gpdata/mirror/gpseg10
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Failed instance port                 = 56001
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Recovery Source instance host        = data04
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Recovery Source instance address     = data04
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Recovery Source instance directory   = /greenplum/gpdata/primary/gpseg10
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Recovery Source instance port        = 55001
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:-   Recovery Target                      = in-place
20221127:23:15:43:026332 gprecoverseg:master:gpadmin-[INFO]:----------------------------------------------------------
20221127:23:15:47:026332 gprecoverseg:master:gpadmin-[INFO]:-1 segment(s) to recover
20221127:23:15:47:026332 gprecoverseg:master:gpadmin-[INFO]:-Ensuring 1 failed segment(s) are stopped
20221127:23:15:47:026332 gprecoverseg:master:gpadmin-[INFO]:-Ensuring that shared memory is cleaned up for stopped segments
20221127:23:15:47:026332 gprecoverseg:master:gpadmin-[INFO]:-Validating remote directories
20221127:23:15:48:026332 gprecoverseg:master:gpadmin-[INFO]:-Configuring new segments data05 (dbid 31): pg_basebackup: base backup completed
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-Updating configuration with new mirrors
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-Updating mirrors
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-Starting mirrors
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-era is c6f862530103c913_221127213422
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-Commencing parallel segment instance startup, please wait...
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-Process results...
20221127:23:15:51:026332 gprecoverseg:master:gpadmin-[INFO]:-Triggering FTS probe
20221127:23:15:52:026332 gprecoverseg:master:gpadmin-[INFO]:-******************************************************************
20221127:23:15:52:026332 gprecoverseg:master:gpadmin-[INFO]:-Updating segments for streaming is completed.
20221127:23:15:52:026332 gprecoverseg:master:gpadmin-[INFO]:-For segments updated successfully, streaming will continue in the background.
20221127:23:15:52:026332 gprecoverseg:master:gpadmin-[INFO]:-Use  gpstate -s  to check the streaming progress.
20221127:23:15:52:026332 gprecoverseg:master:gpadmin-[INFO]:-******************************************************************
进程检查：
[gpadmin@data05 gpseg10]$ ps -ef |grep postgres
gpadmin   45364      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/primary/gpseg13 -p 55001
gpadmin   45367      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/primary/gpseg12 -p 55000
gpadmin   45369      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/primary/gpseg14 -p 55002
gpadmin   45373      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/primary/gpseg19 -p 55003
gpadmin   45378      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/mirror/gpseg9 -p 56000
gpadmin   45380      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/mirror/gpseg18 -p 56003
gpadmin   45382      1  0 22:53 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/mirror/gpseg11 -p 56002
gpadmin   47899      1  0 23:15 ?        00:00:00 /usr/local/greenplum-db-6.7.0/bin/postgres -D /greenplum/gpdata/mirror/gpseg10 -p 56001
......
表空间检查：
[gpadmin@data05 gpseg10]$ ls
backup_label.old    gpmetrics               pg_clog            pg_logical    pg_stat                PG_VERSION            postmaster.pid
base                gpperfmon               pg_distributedlog  pg_multixact  pg_stat_tmp            pg_xlog               recovery.conf
fts_probe_file.bak  gpsegconfig_dump        pg_dynshmem        pg_notify     pg_subtrans            postgresql.auto.conf  recovery.done
global              gpssh.conf              pg_hba.conf        pg_replslot   pg_tblspc              postgresql.conf
gpexpand.pid        internal.auto.conf      pg_ident.conf      pg_serial     pg_twophase            postgresql.conf.bak
gpexpand.status     internal.auto.conf.bak  pg_log             pg_snapshots  pg_utilitymodedtmredo  postmaster.opts
状态检查：
[gpadmin@master ~]$ gpstate -e
20221127:23:23:01:026934 gpstate:master:gpadmin-[INFO]:-Starting gpstate with args: -e
20221127:23:23:01:026934 gpstate:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:23:23:01:026934 gpstate:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:23:23:01:026934 gpstate:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:23:23:01:026934 gpstate:master:gpadmin-[INFO]:-Gathering data from segments...
20221127:23:23:02:026934 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:23:23:02:026934 gpstate:master:gpadmin-[INFO]:-Segment Mirroring Status Report
20221127:23:23:02:026934 gpstate:master:gpadmin-[INFO]:-----------------------------------------------------
20221127:23:23:02:026934 gpstate:master:gpadmin-[INFO]:-All segments are running normally
对于这种情况，一般不会存在数据节点状态异常的情况：
[gpadmin@master ~]$ psql -c "select * from gp_segment_configuration order by content asc,dbid;"
dbid | content | role | preferred_role | mode | status | port  | hostname | address |             datadir              
------+---------+------+----------------+------+--------+-------+----------+---------+-----------------------------------
44 |      -1 | p    | p              | s    | u      |  5432 | master   | master  | /greenplum/gpdata/master/gpseg-1
45 |      -1 | m    | m              | s    | u      |  5432 | standby  | standby | /greenplum/gpdata/master/gpseg-1
2 |       0 | p    | p              | s    | u      | 55000 | data01   | data01  | /greenplum/gpdata/primary/gpseg0
11 |       0 | m    | m              | s    | u      | 56000 | data02   | data02  | /greenplum/gpdata/mirror/gpseg0
3 |       1 | p    | p              | s    | u      | 55001 | data01   | data01  | /greenplum/gpdata/primary/gpseg1
12 |       1 | m    | m              | s    | u      | 56001 | data02   | data02  | /greenplum/gpdata/mirror/gpseg1
4 |       2 | p    | p              | s    | u      | 55002 | data01   | data01  | /greenplum/gpdata/primary/gpseg2
13 |       2 | m    | m              | s    | u      | 56002 | data02   | data02  | /greenplum/gpdata/mirror/gpseg2
5 |       3 | p    | p              | s    | u      | 55000 | data02   | data02  | /greenplum/gpdata/primary/gpseg3
14 |       3 | m    | m              | s    | u      | 56000 | data03   | data03  | /greenplum/gpdata/mirror/gpseg3
6 |       4 | p    | p              | s    | u      | 55001 | data02   | data02  | /greenplum/gpdata/primary/gpseg4
15 |       4 | m    | m              | s    | u      | 56001 | data03   | data03  | /greenplum/gpdata/mirror/gpseg4
7 |       5 | p    | p              | s    | u      | 55002 | data02   | data02  | /greenplum/gpdata/primary/gpseg5
16 |       5 | m    | m              | s    | u      | 56002 | data03   | data03  | /greenplum/gpdata/mirror/gpseg5
8 |       6 | p    | p              | s    | u      | 55000 | data03   | data03  | /greenplum/gpdata/primary/gpseg6
17 |       6 | m    | m              | s    | u      | 56000 | data01   | data01  | /greenplum/gpdata/mirror/gpseg6
9 |       7 | p    | p              | s    | u      | 55001 | data03   | data03  | /greenplum/gpdata/primary/gpseg7
18 |       7 | m    | m              | s    | u      | 56001 | data01   | data01  | /greenplum/gpdata/mirror/gpseg7
10 |       8 | p    | p              | s    | u      | 55002 | data03   | data03  | /greenplum/gpdata/primary/gpseg8
19 |       8 | m    | m              | s    | u      | 56002 | data01   | data01  | /greenplum/gpdata/mirror/gpseg8
21 |       9 | p    | p              | s    | u      | 55000 | data04   | data04  | /greenplum/gpdata/primary/gpseg9
30 |       9 | m    | m              | s    | u      | 56000 | data05   | data05  | /greenplum/gpdata/mirror/gpseg9
22 |      10 | p    | p              | s    | u      | 55001 | data04   | data04  | /greenplum/gpdata/primary/gpseg10
31 |      10 | m    | m              | s    | u      | 56001 | data05   | data05  | /greenplum/gpdata/mirror/gpseg10
23 |      11 | p    | p              | s    | u      | 55002 | data04   | data04  | /greenplum/gpdata/primary/gpseg11
32 |      11 | m    | m              | s    | u      | 56002 | data05   | data05  | /greenplum/gpdata/mirror/gpseg11
24 |      12 | p    | p              | s    | u      | 55000 | data05   | data05  | /greenplum/gpdata/primary/gpseg12
27 |      12 | m    | m              | s    | u      | 56000 | data04   | data04  | /greenplum/gpdata/mirror/gpseg12
25 |      13 | p    | p              | s    | u      | 55001 | data05   | data05  | /greenplum/gpdata/primary/gpseg13
28 |      13 | m    | m              | s    | u      | 56001 | data04   | data04  | /greenplum/gpdata/mirror/gpseg13
26 |      14 | p    | p              | s    | u      | 55002 | data05   | data05  | /greenplum/gpdata/primary/gpseg14
29 |      14 | m    | m              | s    | u      | 56002 | data04   | data04  | /greenplum/gpdata/mirror/gpseg14
33 |      15 | p    | p              | s    | u      | 55003 | data01   | data01  | /greenplum/gpdata/primary/gpseg15
39 |      15 | m    | m              | s    | u      | 56003 | data02   | data02  | /greenplum/gpdata/mirror/gpseg15
34 |      16 | p    | p              | s    | u      | 55003 | data02   | data02  | /greenplum/gpdata/primary/gpseg16
40 |      16 | m    | m              | s    | u      | 56003 | data03   | data03  | /greenplum/gpdata/mirror/gpseg16
35 |      17 | p    | p              | s    | u      | 55003 | data03   | data03  | /greenplum/gpdata/primary/gpseg17
41 |      17 | m    | m              | s    | u      | 56003 | data04   | data04  | /greenplum/gpdata/mirror/gpseg17
36 |      18 | p    | p              | s    | u      | 55003 | data04   | data04  | /greenplum/gpdata/primary/gpseg18
42 |      18 | m    | m              | s    | u      | 56003 | data05   | data05  | /greenplum/gpdata/mirror/gpseg18
37 |      19 | p    | p              | s    | u      | 55003 | data05   | data05  | /greenplum/gpdata/primary/gpseg19
38 |      19 | m    | m              | s    | u      | 56003 | data01   | data01  | /greenplum/gpdata/mirror/gpseg19
查看数据：
[gpadmin@master ~]$ psql -c "select gp_segment_id,count(*) from test_yw;"
同样可以看到所有数据节点上的数据都是正常的。