# 技术分享 | MySQL：max_allowed_packet 影响了什么？

**原文链接**: https://opensource.actionsky.com/20220712-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-07-11T23:29:11-08:00

---

作者：胡呈清
爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：https://www.jianshu.com/u/a95ec11f67a8，欢迎讨论。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
max_allowed_packet 表示 MySQL Server 或者客户端接收的 packet 的最大大小，packet 即数据包，MySQL Server 和客户端上都有这个限制。
## 数据包
每个数据包，都由包头、包体两部分组成，包头由 3 字节的包体长度、1 字节的包编号组成。3 字节最多能够表示 2 ^ 24 = 16777216 字节（16 M），也就是说，一个数据包的包体长度必须小于等于 16M 。
如果要发送超过 16M 的数据怎么办？
当要发送大于 16M 的数据时，会把数据拆分成多个 16M 的数据包，除最后一个数据包之外，其它数据包大小都是 16M。而 MySQL Server 收到这样的包后，如果发现包体长度等于 16M ，它就知道本次接收的数据由多个数据包组成，会先把当前数据包的内容写入缓冲区，然后接着读取下一个数据包，并把下一个数据包的内容追加到缓冲区，直到读到结束数据包，就接收到客户端发送的完整数据了。
那怎样算一个数据包？
- 一个 SQL 是一个数据包
- 返回查询结果时，一行数据算一个数据包
- 解析的 binlog ，如果用 mysql 客户端导入，一个 SQL 算一个数据包
- 在复制中，一个 event 算一个数据包
下面我们通过测试来讨论 max_allowed_packet 的实际影响。
#### 导入 SQL 文件受 max_allowed_packet 限制吗？
如果 SQL 文件中有单个 SQL 大小超过 max_allowed_packet ，会报错：
##导出时设置 mysqldump --net-buffer-length=16M，这样保证导出的sql文件中单个 multiple-row INSERT 大小为 16M
mysqldump -h127.0.0.1 -P13306 -uroot -proot --net-buffer-length=16M \
--set-gtid-purged=off sbtest sbtest1 > /data/backup/sbtest1.sql
##设置max_allowed_packet=1M
##导入报错
[root@localhost data]
# mysql -h127.0.0.1 -P13306 -uroot -proot db3 < /data/backup/sbtest1.sql mysql: [Warning] Using a password on the command line interface can be insecure. ERROR 1153 (08S01) at line 41: Got a packet bigger than 'max_allowed_packet' bytes 
##### 导入解析后的 binlog 受 max_allowed_packet 限制吗？
row 格式的 binlog，单个SQL修改的数据产生的 binlog 如果超过 max_allowed_packet，也会报错。
在恢复数据到指定时间点的场景，解析后的binlog单个事务大小超过1G，并且这个事务只包含一个SQL，此时一定会触发 max_allowed_packet 的报错。但是恢复数据的任务又很重要，怎么办呢？可以将 binlog 改名成 relay log，用 sql 线程回放来绕过这个限制。
##### 查询结果受 max_allowed_packet 限制吗？
查询结果中，只要单行数据不超过客户端设置的 max_allowed_packet 即可：
##插入2行20M大小的数据
[root@localhost tmp]
# dd if=/dev/zero of=20m.img bs=1 count=0 seek=20M 记录了0+0 的读入 记录了0+0 的写出 0字节(0 B)已复制，0.000219914 秒，0.0 kB/秒 
[root@localhost tmp]
# ll -h 20m.img 
-rw-r--r-- 1 root root 20M 6月   6 15:15 20m.img 
mysql> create table t1(id int auto_increment primary key,a longblob); Query OK, 0 rows affected (0.03 sec) 
mysql> insert into t1 values(NULL,load_file('/tmp/20m.img')); Query OK, 1 row affected (0.65 sec) 
mysql> insert into t1 values(NULL,load_file('/tmp/20m.img')); Query OK, 1 row affected (0.65 sec) 
##mysql客户端默认 --max-allowed-packet=16M,读取失败 
mysql> select * from t1; 
ERROR 2020 (HY000): Got packet bigger than 'max_allowed_packet' bytes 
##设置 mysql 客户端 --max-allowed-packet=22M，读取成功 
[root@localhost ~]# mysql -h127.0.0.1 -P13306 -uroot -proot --max-allowed-packet=23068672 sbtest -e "select * from t1;" > /tmp/t1.txt 
[root@localhost ~]# ll  -h /tmp/t1.txt 
-rw-r--r-- 1 root root 81M 6月   6 15:30 /tmp/t1.txt 
##### load data 文件大小受 max_allowed_packet 限制吗？
load data 文件大小、单行大小都不受 max_allowed_packet 影响：
##将上一个测试中的数据导出，2行数据一共81M
mysql> select * into outfile '/tmp/t1.csv' from t1;
Query OK, 2 rows affected (0.57 sec)
[root@localhost ~]# ll -h /tmp/t1.csv
-rw-r----- 1 mysql mysql 81M 6月   6 15:32 /tmp/t1.csv 
##MySQL Server max_allowed_packet=16M 
mysql> select @@max_allowed_packet; 
+----------------------+
| @@max_allowed_packet |
+----------------------+
|             16777216 |
+----------------------+ 
1 row in set (0.00 sec) ##load data 成功,不受 max_allowed_packet 限制 
mysql> load data infile '/tmp/t1.csv' into table t1;
Query OK, 2 rows affected (1.10 sec) 
Records: 2  Deleted: 0  Skipped: 0  Warnings: 0 
##### binlog 中超过 1G 的 SQL ，是如何突破 max_allowed_packet 复制到从库的？
从库 slave io 线程、slave sql 线程可以处理的最大数据包大小由参数 slave_max_allowed_packet 控制。这是限制 binlog event 大小，而不是单个 SQL 修改数据的大小。
主库 dump 线程会自动设置 max_allowed_packet为1G，不会依赖全局变量 max_allowed_packet。用来控制主库 DUMP 线程每次读取 event 的最大大小。
具体可以参考：
https://mp.weixin.qq.com/s/EfNY_UwEthiu-DEBO7TrsA
另外超过 4G 的大事务，从库心跳会报错：
https://opensource.actionsky.com/20201218-mysql/