# 技术分享 | MySQL 闪回工具 MyFlash

**原文链接**: https://opensource.actionsky.com/20201214-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-12-14T00:39:22-08:00

---

作者：陈怡
爱可生南分团队 DBA，负责公司自动化运维平台维护和处理客户问题。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**前言**
MyFlash 是美团点评开源的一个 MySQL 闪回工具，可以用来回滚 MySQL 中的 DML 操作，恢复到某时刻的数据。本文将简单地介绍 MySQL 闪回工具 MyFlash 的使用。
### 限制
MyFlash 工具存在如下限制：
- binlog 格式必须为 row，且 binlog_row_image = full
- 仅支持 5.6 与 5.7 版本的 MySQL
- 只能回滚 DML（ 增、删、改 ）操作
### 下载安装
下载 MyFlash 安装包，将安装包安装于 /data 目录下，编译之前，先安装依赖包。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
[root@10-186-62-22 ~ ]# cd /data`[root@10-186-62-22 data]# wget https://github.com/Meituan-Dianping/MyFlash/archive/master.zip``[root@10-186-62-22 data]# unzip master.zip``Archive:  master.zip``b128c0faaf1a657d09238b7cda1c2a80ad599909``   creating: MyFlash-master/`` extracting: MyFlash-master/.gitignore  ``  inflating: MyFlash-master/License.md  ``  inflating: MyFlash-master/README.md  ``   creating: MyFlash-master/binary/``  inflating: MyFlash-master/binary/flashback  ``  inflating: MyFlash-master/binary/mysqlbinlog20160408  ``  inflating: MyFlash-master/binlog_output_base.flashback  ``  inflating: MyFlash-master/build.sh  ``   creating: MyFlash-master/doc/`` extracting: MyFlash-master/doc/FAQ.md  `` extracting: MyFlash-master/doc/Function.md  ``  inflating: MyFlash-master/doc/INSTALL.md  ``  inflating: MyFlash-master/doc/TestCase.md  ``  inflating: MyFlash-master/doc/how_to_use.md  ``   creating: MyFlash-master/source/``  inflating: MyFlash-master/source/binlogParseGlib.c  ``   creating: MyFlash-master/source/mysqlHelper/`` extracting: MyFlash-master/source/mysqlHelper/mysqlHelper.c  ``   creating: MyFlash-master/source/network/``  inflating: MyFlash-master/source/network/network.c  ``   creating: MyFlash-master/testbinlog/``  inflating: MyFlash-master/testbinlog/haha.000005  ``  inflating: MyFlash-master/testbinlog/haha.000007  ``  inflating: MyFlash-master/testbinlog/haha.000008  ``  inflating: MyFlash-master/testbinlog/haha.000009  ``  inflating: MyFlash-master/testbinlog/haha.000041``[root@10-186-62-22 data]# mv MyFlash-master MyFlash``[root@10-186-62-22 data]# cd MyFlash/``[root@10-186-62-22 MyFlash]# yum install gcc glib2-devel -y``[root@10-186-62-22 MyFlash]# gcc -w  `pkg-config --cflags --libs glib-2.0` source/binlogParseGlib.c  -o binary/flashback
```
### 用法
- 
```
flashback [OPTION...]
```
常用参数说明：
&#8211;databaseNames指定需要回滚的数据库名。多个数据库可以用 “,” 隔开。如果不指定该参数，相当于指定了所有数据库。&#8211;tableNames指定需要回滚的表名。多个表可以用 “,” 隔开。如果不指定该参数，相当于指定了所有表。&#8211;start-position指定回滚开始的位置。如不指定，从文件的开始处回滚。请指定正确的有效的位置，否则无法回滚。&#8211;stop-position指定回滚结束的位置。如不指定，回滚到文件结尾。请指定正确的有效的位置，否则无法回滚。&#8211;start-datetime 指定回滚的开始时间。注意格式必须是 %Y-%m-%d %H:%M:%S。如不指定，则不限定时间。&#8211;stop-datetime指定回滚的结束时间。注意格式必须是 %Y-%m-%d %H:%M:%S。如不指定，则不限定时间。&#8211;sqlTypes指定需要回滚的 sql 类型。目前支持的过滤类型是 INSERT, UPDATE, DELETE。多个类型可以用 “,” 隔开。&#8211;maxSplitSize指定解析分割后文件最大大小，单位为 M。&#8211;binlogFileNames指定需要回滚的 binlog 文件，如有多个，用 “,” 隔开。&#8211;outBinlogFileNameBase指定输出的 binlog 文件前缀，如不指定，则默认为 binlog_output_base.flashback。&#8211;logLevel指定输出的日志级别，可选级别有 debug, warning, error，默认级别为 error 级别。&#8211;include-gtids指定需要回滚的 gtid，支持 gtid 的单个和范围两种形式，如有多种形式，用 “,” 隔开。&#8211;exclude-gtids指定不需要回滚的 gtid，支持 gtid 的单个和范围两种形式，如有多种形式，用 “,” 隔开。
### 测试用例
模拟在一个实例中，对 d1.t1 进行了 update 操作和 delete 操作，需要回滚 update 和 delete 操作场景。
原 d1.t1 表中数据如下：
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
mysql> select * from d1.t1;``+------+``| id   |``+------+``|    1 |``|    2 |``|    3 |``|    4 |``|    5 |``|    6 |``|    7 |``|    8 |``|    9 |``|   10 |``+------+``10 rows in set (0.00 sec)``mysql> checksum table d1.t1;``+-------+------------+``| Table | Checksum   |``+-------+------------+``| d1.t1 | 1635096377 |``+-------+------------+``1 row in set (0.00 sec)
```
进行了 update 和 delete 操作：
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
mysql> update d1.t1 set id=id+10 where id<6;``Query OK, 5 rows affected (0.01 sec)``Rows matched: 5  Changed: 5  Warnings: 0``
``mysql> select * from d1.t1;``+------+``| id   |``+------+``|   11 |``|   12 |``|   13 |``|   14 |``|   15 |``|    6 |``|    7 |``|    8 |``|    9 |``|   10 |``+------+``10 rows in set (0.00 sec)``
``mysql> checksum table d1.t1;``+-------+------------+``| Table | Checksum   |``+-------+------------+``| d1.t1 | 1061066609 |``+-------+------------+``1 row in set (0.00 sec)``
``mysql> delete from d1.t1 where id<10;``Query OK, 4 rows affected (0.00 sec)``
``mysql> select * from d1.t1;``+------+``| id   |``+------+``|   11 |``|   12 |``|   13 |``|   14 |``|   15 |``|   10 |``+------+``6 rows in set (0.00 sec)``
``mysql> checksum table d1.t1;``+-------+------------+``| Table | Checksum   |``+-------+------------+``| d1.t1 | 1094682723 |``+-------+------------+``1 row in set (0.00 sec)
```
此时，期望回滚 update 和 delete 操作。先 flush binlog，切换 binlog 文件：
- 
- 
```
mysql> flush logs;``Query OK, 0 rows affected (0.07 sec)
```
解析 binlog，查看对应 update 和 delete 操作，在 17:22:30 时进行 update 操作，在 17:23:35 时已经完成了delete 操作。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
[root@10-186-62-22 3308]# mysqlbinlog -vv mysql-bin.000001 |less``#201129  17:22:30 server id 313253419  end_log_pos 450327 CRC32 0x23bf37dd       Query   thread_id=108971        exec_time=0     error_code=0``SET TIMESTAMP=1606670550/*!*/;``BEGIN``/*!*/;``# at 450327``#201129  17:22:30 server id 313253419  end_log_pos 450387 CRC32 0xe368ad04       Rows_query``# update d1.t1 set id=id+10 where id<6``# at 450387``#201129  17:22:30 server id 313253419  end_log_pos 450430 CRC32 0x3b1221e2       Table_map: `d1`.`t1` mapped to number 223``# at 450430``#201129  17:22:30 server id 313253419  end_log_pos 450516 CRC32 0x484dc736       Update_rows: table id 223 flags: STMT_END_F``
``BINLOG '``1tjDXx0r3qsSPAAAAFPfBgCAACR1cGRhdGUgZDEudDEgc2V0IGlkPWlkKzEwIHdoZXJlIGlkPDYE``rWjj``1tjDXxMr3qsSKwAAAH7fBgAAAN8AAAAAAAEAAmQxAAJ0MQABAwAB4iESOw==``1tjDXx8r3qsSVgAAANTfBgAAAN8AAAAAAAEAAgAB///+AQAAAP4LAAAA/gIAAAD+DAAAAP4DAAAA``/g0AAAD+BAAAAP4OAAAA/gUAAAD+DwAAADbHTUg=``'/*!*/;``### UPDATE `d1`.`t1```### WHERE``###   @1=1 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=11 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=2 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=12 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=3 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=13 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=4 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=14 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=5 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=15 /* INT meta=0 nullable=1 is_null=0 */``# at 450516``#201129  17:22:30 server id 313253419  end_log_pos 450547 CRC32 0x4905fbcf       Xid = 33117376``COMMIT/*!*/;``# at 450547``#201129  17:23:09 server id 313253419  end_log_pos 450682 CRC32 0xb993ef68       Query   thread_id=108971        exec_time=0     error_code=0``SET TIMESTAMP=1606670589/*!*/;``BEGIN``/*!*/;``# at 450682``#201129  17:23:09 server id 313253419  end_log_pos 450735 CRC32 0x767343ad       Rows_query``# delete from d1.t1 where id<10``# at 450735``#201129  17:23:09 server id 313253419  end_log_pos 450778 CRC32 0x6bd9dc7b       Table_map: `d1`.`t1` mapped to number 223``# at 450778``#201129  17:23:09 server id 313253419  end_log_pos 450833 CRC32 0x1ba9f05c       Delete_rows: table id 223 flags: STMT_END_F``
``BINLOG '``/djDXx0r3qsSNQAAAK/gBgCAAB1kZWxldGUgZnJvbSBkMS50MSB3aGVyZSBpZDwxMK1Dc3Y=``/djDXxMr3qsSKwAAANrgBgAAAN8AAAAAAAEAAmQxAAJ0MQABAwABe9zZaw==``/djDXyAr3qsSNwAAABHhBgAAAN8AAAAAAAEAAgAB//4GAAAA/gcAAAD+CAAAAP4JAAAAXPCpGw==``'/*!*/;``### DELETE FROM `d1`.`t1```### WHERE``###   @1=6 /* INT meta=0 nullable=1 is_null=0 */``### DELETE FROM `d1`.`t1```### WHERE``###   @1=7 /* INT meta=0 nullable=1 is_null=0 */``### DELETE FROM `d1`.`t1```### WHERE``###   @1=8 /* INT meta=0 nullable=1 is_null=0 */``### DELETE FROM `d1`.`t1```### WHERE``###   @1=9 /* INT meta=0 nullable=1 is_null=0 */``# at 450833``#201129  17:23:09 server id 313253419  end_log_pos 450864 CRC32 0x8c6244ec       Xid = 33117815``COMMIT/*!*/;``# at 450864``#201129  17:23:35 server id 313253419  end_log_pos 450929 CRC32 0x6191c83b       GTID [commit=no]``SET @@SESSION.GTID_NEXT= '36edb64b-17fa-11eb-a621-02000aba3e16:1028'/*!*/;
```
使用 MyFlash 工具进行回滚，进入到工具的安装目录，执行命令反向解析 binlog，指定要回滚的库、表、开始时间和结束时间，并指定反向解析的 SQL 语句类型：
- 
```
[root@10-186-62-22 MyFlash]# ./binary/flashback --databaseNames="d1" --tableNames="t1" --start-datetime="2020-11-29 17:22:30" --stop-datetime="2020-11-29 17:24:30"  --sqlTypes="UPDATE,DELETE" --binlogFileNames=/opt/mysql/log/binlog/3308/mysql-bin.000001 --outBinlogFileNameBase=test.sql
```
查看到反向解析后的 binlog 文件，执行顺序为先回滚 delete 操作，将被删除的数据添加，再逆向 update 语句。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
[root@10-186-62-22 MyFlash]# mysqlbinlog -vv test.sql.flashback ``/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=1*/;``/*!40019 SET @@session.max_insert_delayed_threads=0*/;``/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;``DELIMITER /*!*/;``# at 4``#201027 10:15:00 server id 313253419  end_log_pos 123 CRC32 0x500482f7   Start: binlog v 4, server v 5.7.25-log created 201027 10:15:00 at startup``# Warning: this binlog is either in use or was not closed properly.``ROLLBACK/*!*/;``BINLOG '``pIKXXw8r3qsSdwAAAHsAAAABAAQANS43LjI1LWxvZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA``AAAAAAAAAAAAAAAAAACkgpdfEzgNAAgAEgAEBAQEEgAAXwAEGggAAAAICAgCAAAACgoKKioAEjQA``AfeCBFA=``'/*!*/;``# at 123``#201129  17:23:09 server id 313253419  end_log_pos 166 CRC32 0x6bd9dc7b   Table_map: `d1`.`t1` mapped to number 223``# at 166``#201129  17:23:09 server id 313253419  end_log_pos 221 CRC32 0x1ba9f05c   Write_rows: table id 223 flags: STMT_END_F``
``BINLOG '``/djDXxMr3qsSKwAAAKYAAAAAAN8AAAAAAAEAAmQxAAJ0MQABAwABe9zZaw==``/djDXx4r3qsSNwAAAN0AAAAAAN8AAAAAAAEAAgAB//4GAAAA/gcAAAD+CAAAAP4JAAAAXPCpGw==``'/*!*/;``### INSERT INTO `d1`.`t1```### SET``###   @1=6 /* INT meta=0 nullable=1 is_null=0 */``### INSERT INTO `d1`.`t1```### SET``###   @1=7 /* INT meta=0 nullable=1 is_null=0 */``### INSERT INTO `d1`.`t1```### SET``###   @1=8 /* INT meta=0 nullable=1 is_null=0 */``### INSERT INTO `d1`.`t1```### SET``###   @1=9 /* INT meta=0 nullable=1 is_null=0 */``# at 221``#201129  17:38:00 server id 313253419  end_log_pos 252 CRC32 0xf267b63c   Xid = 33082944``COMMIT/*!*/;``# at 252``#201129  17:22:30 server id 313253419  end_log_pos 295 CRC32 0x3b1221e2   Table_map: `d1`.`t1` mapped to number 223``# at 295``#201129  17:22:30 server id 313253419  end_log_pos 381 CRC32 0x484dc736   Update_rows: table id 223 flags: STMT_END_F``
``BINLOG '``1tjDXxMr3qsSKwAAACcBAAAAAN8AAAAAAAEAAmQxAAJ0MQABAwAB4iESOw==``1tjDXx8r3qsSVgAAAH0BAAAAAN8AAAAAAAEAAgAB///+CwAAAP4BAAAA/gwAAAD+AgAAAP4NAAAA``/gMAAAD+DgAAAP4EAAAA/g8AAAD+BQAAADbHTUg=``'/*!*/;``### UPDATE `d1`.`t1```### WHERE``###   @1=11 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=1 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=12 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=2 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=13 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=3 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=14 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=4 /* INT meta=0 nullable=1 is_null=0 */``### UPDATE `d1`.`t1```### WHERE``###   @1=15 /* INT meta=0 nullable=1 is_null=0 */``### SET``###   @1=5 /* INT meta=0 nullable=1 is_null=0 */``# at 381``#201129  17:38:00 server id 313253419  end_log_pos 412 CRC32 0xf267b63c   Xid = 33082944``COMMIT/*!*/;``DELIMITER ;``# End of log file``ROLLBACK /* added by mysqlbinlog */;``/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;``/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```
将反向解析的 binlog 文件语句回放到数据库中。由于所测试的实例中已经开启 gtid 模式，而反向解析出来的 binlog 文件中没有定义 @@SESSION.GTID_NEXT，直接执行会出现报错 “ERROR 1782 (HY000) at line 19: @@SESSION.GTID_NEXT cannot be set to ANONYMOUS when @@GLOBAL.GTID_MODE = ON.” ，所以需要添加 &#8211;skip-gtids 选项来执行回滚语句，加上 &#8211;skip-gtids 选项后解析出来的文件，会指定 SET @@SESSION.GTID_NEXT=&#8217;AUTOMATIC&#8217; ，这样就可以回放成功了。
- 
- 
- 
- 
- 
- 
```
[root@10-186-62-22 MyFlash]# mysqlbinlog test.sql.flashback | mysql -S /tmp/mysqld.sock -uroot -proot``mysql: [Warning] Using a password on the command line interface can be insecure.``ERROR 1782 (HY000) at line 19: @@SESSION.GTID_NEXT cannot be set to ANONYMOUS when @@GLOBAL.GTID_MODE = ON.``[root@10-186-62-22 MyFlash]#``[root@10-186-62-22 MyFlash]# mysqlbinlog --skip-gtids test.sql.flashback | mysql -S /tmp/mysqld.sock -uroot -proot``mysql: [Warning] Using a password on the command line interface can be insecure.
```
验证数据，数据已经恢复到 update 操作之前，完成回滚操作。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
mysql> select * from d1.t1;``+------+``| id   |``+------+``|    1 |``|    2 |``|    3 |``|    4 |``|    5 |``|   10 |``|    6 |``|    7 |``|    8 |``|    9 |``+------+``10 rows in set (0.00 sec)``
``mysql> checksum table d1.t1;``+-------+------------+``| Table | Checksum   |``+-------+------------+``| d1.t1 | 1635096377 |``+-------+------------+`1 row in set (0.00 sec)
```
> **参考链接：**
https://github.com/Meituan-Dianping/MyFlash/blob/master/README.md
相关推荐：
[技术分享 | 关于 MySQL Online DDL 有趣的验证](https://opensource.actionsky.com/20201208-mysql/)
[技术分享 | MySQL 8.0.21 Disable Redo Log 性能测试](https://opensource.actionsky.com/20200727-mysql/)
[技术分享 | MySQL binlog 压缩功能对性能的影响](https://opensource.actionsky.com/202011119-mysql/)