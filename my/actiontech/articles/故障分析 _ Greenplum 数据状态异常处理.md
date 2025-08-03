# 故障分析 | Greenplum 数据状态异常处理

**原文链接**: https://opensource.actionsky.com/20221208-greenplum/
**分类**: 技术干货
**发布时间**: 2022-12-06T17:50:25-08:00

---

作者：杨文
DBA，负责客户项目的需求与维护，会点数据库，不限于MySQL、Redis、Cassandra、GreenPlum、ClickHouse、Elastic、TDSQL等等。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一、背景：
客户在巡检时，发现 Greenplum 虽然正常运行，但有些数据的状态异常。我们知道 Greenplum 的数据是存在主段和镜像段上的，当 primary 数据异常，会自动的启用 mirror 数据。当然为了保证数据的高可用，还是要及时修复异常数据。
#### 二、本地模拟客户故障环境：
[gpadmin@master ~]$ psql -c "select * from gp_segment_configuration order by content asc,dbid;"
dbid | content | role | preferred_role | mode | status | port  |   hostname   |   address    |              datadir              
------+---------+------+----------------+------+--------+-------+--------------+--------------+-----------------------------------
44 |      -1 | p    | p              | s    | u      |  5432 |   master     |   master     | /greenplum/gpdata/master/gpseg-1
45 |      -1 | m    | m              | s    | u      |  5432 |   standby    |   standby    | /greenplum/gpdata/master/gpseg-1
2 |       0 | p    | p              | s    | u      | 55000 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg0
11 |       0 | m    | m              | s    | u      | 56000 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg0
3 |       1 | p    | p              | s    | u      | 55001 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg1
12 |       1 | m    | m              | s    | u      | 56001 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg1
4 |       2 | p    | p              | s    | u      | 55002 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg2
13 |       2 | m    | m              | s    | u      | 56002 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg2
5 |       3 | p    | p              | s    | u      | 55000 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg3
14 |       3 | m    | m              | s    | u      | 56000 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg3
6 |       4 | p    | p              | s    | u      | 55001 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg4
15 |       4 | m    | m              | s    | u      | 56001 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg4
7 |       5 | p    | p              | s    | u      | 55002 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg5
16 |       5 | m    | m              | s    | u      | 56002 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg5
8 |       6 | p    | p              | s    | u      | 55000 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg6
17 |       6 | m    | m              | s    | u      | 56000 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg6
9 |       7 | p    | p              | s    | u      | 55001 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg7
18 |       7 | m    | m              | s    | u      | 56001 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg7
10 |       8 | p    | p              | s    | u      | 55002 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg8
19 |       8 | m    | m              | s    | u      | 56002 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg8
21 |       9 | m    | p              | s    | d      | 55000 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg9
30 |       9 | p    | m              | s    | u      | 56000 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg9
22 |      10 | m    | p              | s    | d      | 55001 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg10
31 |      10 | p    | m              | s    | u      | 56001 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg10
23 |      11 | m    | p              | s    | d      | 55002 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg11
32 |      11 | p    | m              | s    | u      | 56002 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg11
24 |      12 | m    | p              | s    | d      | 55000 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg12
27 |      12 | p    | m              | s    | u      | 56000 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg12
25 |      13 | m    | p              | s    | d      | 55001 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg13
28 |      13 | p    | m              | s    | u      | 56001 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg13
26 |      14 | m    | p              | s    | d      | 55002 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg14
29 |      14 | p    | m              | s    | u      | 56002 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg14
33 |      15 | m    | p              | s    | d      | 55003 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg15
39 |      15 | p    | m              | s    | u      | 56003 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg15
34 |      16 | m    | p              | s    | d      | 55003 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg16
40 |      16 | p    | m              | s    | u      | 56003 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg16
35 |      17 | m    | p              | s    | d      | 55003 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg17
41 |      17 | p    | m              | s    | u      | 56003 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg17
36 |      18 | m    | p              | s    | d      | 55003 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg18
42 |      18 | p    | m              | s    | u      | 56003 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg18
37 |      19 | m    | p              | s    | d      | 55003 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg19
38 |      19 | p    | m              | s    | u      | 56003 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg19
(42 rows)
可以看到42个数据节点中有11个数据节点处于 down 状态；
#### 三、故障分析及解决：
###### 3.1、数据检查：
分别去down掉的节点中去查看数据文件（此处我们只取一个节点进行展示对比）：
[gpadmin@data02 gpseg16]$ pwd
/greenplum/gpdata/primary/gpseg16
[gpadmin@data02 gpseg16]$ ls
base                pg_hba.conf    pg_serial     pg_utilitymodedtmredo
fts_probe_file.bak  pg_ident.conf  pg_snapshots  PG_VERSION
global              pg_log         pg_stat       pg_xlog
internal.auto.conf  pg_logical     pg_stat_tmp   postgresql.auto.conf
pg_clog             pg_multixact   pg_subtrans   postgresql.conf
pg_distributedlog   pg_notify      pg_tblspc     postmaster.opts
pg_dynshmem         pg_replslot    pg_twophase
可以发现都缺少了 postmaster.pid 文件。
为了看的更清楚，我们找一个状态正常的节点查看对比：
[gpadmin@data01 gpseg1]$ pwd
/greenplum/gpdata/primary/gpseg1
[gpadmin@data01 gpseg1]$ ls
base                pg_hba.conf    pg_serial     pg_utilitymodedtmredo
fts_probe_file.bak  pg_ident.conf  pg_snapshots  PG_VERSION
global              pg_log         pg_stat       pg_xlog
internal.auto.conf  pg_logical     pg_stat_tmp   postgresql.auto.conf
pg_clog             pg_multixact   pg_subtrans   postgresql.conf
pg_distributedlog   pg_notify      pg_tblspc     postmaster.opts
pg_dynshmem         pg_replslot    pg_twophase   postmaster.pid
[gpadmin@data01 gpseg1]$ cat postmaster.pid
20517
/greenplum/gpdata/primary/gpseg1
1652022705
55001
/tmp
*
55001001     393219
说明：很多人说此时重启集群可以轻易的解决这个问题，但实际上重启集群并不能保证一定会解决问题，并且重启集群会导致业务中断。
###### 3.2、在线生成一个配置文件：
[gpadmin@master ~]$ gprecoverseg -o ./recover
20221127:22:10:22:020909 gprecoverseg:master:gpadmin-[INFO]:-Starting gprecoverseg with args: -o ./recover
20221127:22:10:22:020909 gprecoverseg:master:gpadmin-[INFO]:-local Greenplum Version: 'postgres (Greenplum Database) 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b'
20221127:22:10:22:020909 gprecoverseg:master:gpadmin-[INFO]:-master Greenplum Version: 'PostgreSQL 9.4.24 (Greenplum Database 6.7.0 build commit:2fbc274bc15a19b5de3c6e44ad5073464cd4f47b) on x86_64-unknown-linux-gnu, compiled by gcc (GCC) 6.4.0, 64-bit compiled on Apr 16 2020 02:24:06'
20221127:22:10:22:020909 gprecoverseg:master:gpadmin-[INFO]:-Obtaining Segment details from master...
20221127:22:10:22:020909 gprecoverseg:master:gpadmin-[INFO]:-Configuration file output to ./recover successfully.
[gpadmin@master ~]$ ls
gpAdminLogs  recover
[gpadmin@master ~]$ more recover
data04|55000|/greenplum/gpdata/primary/gpseg9
data04|55001|/greenplum/gpdata/primary/gpseg10
data04|55002|/greenplum/gpdata/primary/gpseg11
data05|55000|/greenplum/gpdata/primary/gpseg12
data05|55001|/greenplum/gpdata/primary/gpseg13
data05|55002|/greenplum/gpdata/primary/gpseg14
data01|55003|/greenplum/gpdata/primary/gpseg15
data02|55003|/greenplum/gpdata/primary/gpseg16
data03|55003|/greenplum/gpdata/primary/gpseg17
data04|55003|/greenplum/gpdata/primary/gpseg18
data05|55003|/greenplum/gpdata/primary/gpseg19
###### 3.3、通过生成的配置文件进行修复集群：
[gpadmin@master ~]$ gprecoverseg -i ./recover -F 
执行过程省略，但有个选项需要确认：
Continue with segment recovery procedure Yy|Nn (default=N):
> y
###### 3.4、检查数据：
[gpadmin@master ~]$ psql -c "select * from gp_segment_configuration order by content asc,dbid;"
dbid | content | role | preferred_role | mode | status | port  |   hostname   |   address    |              datadir              
------+---------+------+----------------+------+--------+-------+--------------+--------------+-----------------------------------
44 |      -1 | p    | p              | s    | u      |  5432 |   master     |   master     | /greenplum/gpdata/master/gpseg-1
45 |      -1 | m    | m              | s    | u      |  5432 |   standby    |   standby    | /greenplum/gpdata/master/gpseg-1
2 |       0 | p    | p              | s    | u      | 55000 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg0
11 |       0 | m    | m              | s    | u      | 56000 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg0
3 |       1 | p    | p              | s    | u      | 55001 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg1
12 |       1 | m    | m              | s    | u      | 56001 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg1
4 |       2 | p    | p              | s    | u      | 55002 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg2
13 |       2 | m    | m              | s    | u      | 56002 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg2
5 |       3 | p    | p              | s    | u      | 55000 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg3
14 |       3 | m    | m              | s    | u      | 56000 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg3
6 |       4 | p    | p              | s    | u      | 55001 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg4
15 |       4 | m    | m              | s    | u      | 56001 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg4
7 |       5 | p    | p              | s    | u      | 55002 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg5
16 |       5 | m    | m              | s    | u      | 56002 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg5
8 |       6 | p    | p              | s    | u      | 55000 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg6
17 |       6 | m    | m              | s    | u      | 56000 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg6
9 |       7 | p    | p              | s    | u      | 55001 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg7
18 |       7 | m    | m              | s    | u      | 56001 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg7
10 |       8 | p    | p              | s    | u      | 55002 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg8
19 |       8 | m    | m              | s    | u      | 56002 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg8
21 |       9 | m    | p              | s    | u      | 55000 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg9
30 |       9 | p    | m              | s    | u      | 56000 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg9
22 |      10 | m    | p              | s    | u      | 55001 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg10
31 |      10 | p    | m              | s    | u      | 56001 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg10
23 |      11 | m    | p              | s    | u      | 55002 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg11
32 |      11 | p    | m              | s    | u      | 56002 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg11
24 |      12 | m    | p              | s    | u      | 55000 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg12
27 |      12 | p    | m              | s    | u      | 56000 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg12
25 |      13 | m    | p              | s    | u      | 55001 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg13
28 |      13 | p    | m              | s    | u      | 56001 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg13
26 |      14 | m    | p              | s    | u      | 55002 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg14
29 |      14 | p    | m              | s    | u      | 56002 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg14
33 |      15 | m    | p              | s    | u      | 55003 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg15
39 |      15 | p    | m              | s    | u      | 56003 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg15
34 |      16 | m    | p              | s    | u      | 55003 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg16
40 |      16 | p    | m              | s    | u      | 56003 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg16
35 |      17 | m    | p              | s    | u      | 55003 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg17
41 |      17 | p    | m              | s    | u      | 56003 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg17
36 |      18 | m    | p              | s    | u      | 55003 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg18
42 |      18 | p    | m              | s    | u      | 56003 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg18
37 |      19 | m    | p              | s    | u      | 55003 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg19
38 |      19 | p    | m              | s    | u      | 56003 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg19
(42 rows)
此时可以看到所有数据节点的状态都是正常的up状态。
[gpadmin@master ~]$ psql
psql (9.4.24)
Type "help" for help.
postgres=# \c test
You are now connected to database "test" as user "gpadmin".
test=# select gp_segment_id,count(*) from test_yw group by gp_segment_id;
gp_segment_id | count 
---------------+-------
1 |   384
13 |   396
14 |   403
9 |   429
10 |   376
16 |   364
12 |   389
6 |   414
0 |   426
15 |   426
3 |   404
19 |   411
4 |   409
2 |   393
8 |   410
18 |   407
7 |   407
11 |   420
5 |   346
17 |   386
(20 rows)
test=# \q
可以看到所有数据节点上都是有数据的，且都正常。
其实仔细看可以发现，上面的数据节点看起来都很正常，但还有个小小的问题：部分数据节点的角色存在异常，即有的&#8221;主段&#8221;角色变成了“镜像段”角色，有的&#8221;镜像段&#8221;角色变成了“主段”角色。
###### 3.5、修复数据角色状态：
[gpadmin@master ~]$ gprecoverseg -r
执行过程省略，但有个选项需要确认：
Continue with segment rebalance procedure Yy|Nn (default=N):
> y
###### 3.6、再次检查：
[gpadmin@master ~]$ psql -c "select * from gp_segment_configuration order by content asc,dbid;"
dbid | content | role | preferred_role | mode | status | port  |   hostname   |   address    |              datadir              
------+---------+------+----------------+------+--------+-------+--------------+--------------+-----------------------------------
44 |      -1 | p    | p              | s    | u      |  5432 |   master     |   master     | /greenplum/gpdata/master/gpseg-1
45 |      -1 | m    | m              | s    | u      |  5432 |   standby    |   standby    | /greenplum/gpdata/master/gpseg-1
2 |       0 | p    | p              | s    | u      | 55000 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg0
11 |       0 | m    | m              | s    | u      | 56000 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg0
3 |       1 | p    | p              | s    | u      | 55001 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg1
12 |       1 | m    | m              | s    | u      | 56001 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg1
4 |       2 | p    | p              | s    | u      | 55002 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg2
13 |       2 | m    | m              | s    | u      | 56002 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg2
5 |       3 | p    | p              | s    | u      | 55000 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg3
14 |       3 | m    | m              | s    | u      | 56000 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg3
6 |       4 | p    | p              | s    | u      | 55001 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg4
15 |       4 | m    | m              | s    | u      | 56001 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg4
7 |       5 | p    | p              | s    | u      | 55002 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg5
16 |       5 | m    | m              | s    | u      | 56002 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg5
8 |       6 | p    | p              | s    | u      | 55000 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg6
17 |       6 | m    | m              | s    | u      | 56000 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg6
9 |       7 | p    | p              | s    | u      | 55001 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg7
18 |       7 | m    | m              | s    | u      | 56001 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg7
10 |       8 | p    | p              | s    | u      | 55002 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg8
19 |       8 | m    | m              | s    | u      | 56002 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg8
21 |       9 | p    | p              | s    | u      | 55000 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg9
30 |       9 | m    | m              | s    | u      | 56000 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg9
22 |      10 | p    | p              | s    | u      | 55001 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg10
31 |      10 | m    | m              | s    | u      | 56001 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg10
23 |      11 | p    | p              | s    | u      | 55002 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg11
32 |      11 | m    | m              | s    | u      | 56002 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg11
24 |      12 | p    | p              | s    | u      | 55000 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg12
27 |      12 | m    | m              | s    | u      | 56000 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg12
25 |      13 | p    | p              | s    | u      | 55001 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg13
28 |      13 | m    | m              | s    | u      | 56001 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg13
26 |      14 | p    | p              | s    | u      | 55002 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg14
29 |      14 | m    | m              | s    | u      | 56002 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg14
33 |      15 | p    | p              | s    | u      | 55003 |   data01     |   data01     | /greenplum/gpdata/primary/gpseg15
39 |      15 | m    | m              | s    | u      | 56003 |   data02     |   data02     | /greenplum/gpdata/mirror/gpseg15
34 |      16 | p    | p              | s    | u      | 55003 |   data02     |   data02     | /greenplum/gpdata/primary/gpseg16
40 |      16 | m    | m              | s    | u      | 56003 |   data03     |   data03     | /greenplum/gpdata/mirror/gpseg16
35 |      17 | p    | p              | s    | u      | 55003 |   data03     |   data03     | /greenplum/gpdata/primary/gpseg17
41 |      17 | m    | m              | s    | u      | 56003 |   data04     |   data04     | /greenplum/gpdata/mirror/gpseg17
36 |      18 | p    | p              | s    | u      | 55003 |   data04     |   data04     | /greenplum/gpdata/primary/gpseg18
42 |      18 | m    | m              | s    | u      | 56003 |   data05     |   data05     | /greenplum/gpdata/mirror/gpseg18
37 |      19 | p    | p              | s    | u      | 55003 |   data05     |   data05     | /greenplum/gpdata/primary/gpseg19
38 |      19 | m    | m              | s    | u      | 56003 |   data01     |   data01     | /greenplum/gpdata/mirror/gpseg19
(42 rows)
此时可以看到数据节点的所有状态都是正确的。
此时去之前异常数据节点中去查看数据文件，可以发现之前缺少的 postmaster.pid 文件都存在了，并且还多了 recovery.done 文件：
[gpadmin@data02 gpseg16]$ pwd
/greenplum/gpdata/primary/gpseg16
[gpadmin@data02 gpseg16]$ ls
backup_label.old        pg_clog            pg_stat_tmp
base                    pg_distributedlog  pg_subtrans
fts_probe_file.bak      pg_dynshmem        pg_tblspc
global                  pg_hba.conf        pg_twophase
gpexpand.pid            pg_ident.conf      pg_utilitymodedtmredo
gpexpand.status         pg_log             PG_VERSION
gpexpand.status_detail  pg_logical         pg_xlog
gpmetrics               pg_multixact       postgresql.auto.conf
gpperfmon               pg_notify          postgresql.conf
gpsegconfig_dump        pg_replslot        postgresql.conf.bak
gpssh.conf              pg_serial          postmaster.opts
internal.auto.conf      pg_snapshots       postmaster.pid
internal.auto.conf.bak  pg_stat            recovery.done
[gpadmin@data02 gpseg16]$ more postmaster.pid
19572
/greenplum/gpdata/primary/gpseg16
1669556066
55003
/tmp
*
55003001    327680
[gpadmin@data02 gpseg16]$ more recovery.done  
standby_mode = 'on'
primary_conninfo = 'user=gpadmin host=data03 port=56003 sslmode=prefer sslcompression=1 krbsrvname=postgres application_name=gp_walreceiver'
primary_slot_name = 'internal_wal_replication_slot'
查看数据：
[gpadmin@master ~]$ psql -c "select gp_segment_id,count(*) from test_yw;" 
同样可以看到所有数据节点上的数据都是正常的。