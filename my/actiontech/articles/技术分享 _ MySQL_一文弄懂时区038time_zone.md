# 技术分享 | MySQL:一文弄懂时区&#038;time_zone

**原文链接**: https://opensource.actionsky.com/20211214-time_zone/
**分类**: 技术干货
**发布时间**: 2021-12-13T21:59:34-08:00

---

作者：胡呈清
爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：https://www.jianshu.com/u/a95ec11f67a8，欢迎讨论。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
你还在被以下问题困扰吗：
MySQL 的安装规范中应该设置什么时区？
JAVA 应用读取到的时间和北京时间差了14个小时，为什么？怎么解决？
已经运行一段时间的业务，修改 MySQL 的时区会影响已经存储的时间类型数据吗？
迁移数据时会有导致时间类型数据时区错误的可能吗？
&#8230;
看完这篇文章，你能解决上面所有的疑惑。首先出场的是和时区相关的启动参数和系统变量。
## 启动参数&系统变量
如果要在 MySQL 启动时就指定时区，则应该使用启动参数：`default-time-zone`，示例：
`--方法1：在启动命令中添加
mysqld --default-time-zone='+08:00' &
--方法2：在配置文件中添加
[mysqld]
default-time-zone='+08:00'
`
启动后我们可以看到控制时区的系统变量，其中 `time_zone` 变量控制时区，在MySQL运行时可以通过`set`命令修改（注意：不可以写在 my.cnf 中）：
`--查看
mysql> show global variables like '%time%zone%';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| system_time_zone | CST    |
| time_zone        | +08:00 |
+------------------+--------+
2 rows in set (0.00 sec)
--修改全局时区，所有已经创建的、新创建的session都会被修改
set global time_zone='+00:00';
--修改当前session的时区
set session time_zone='+00:00';
`
启动参数和系统变量的可用值遵循相同的格式：
- 
&#8216;SYSTEM&#8217; 表明使用系统时间
- 
相对于 UTC 时间的偏移，比如 &#8216;+08:00&#8217; 或者 &#8216;-6:00&#8217;
- 
某个时区的名字，比如 &#8216;Europe/Helsinki&#8217;，&#8221;Asia/Shanghai&#8221; 或 &#8216;UTC&#8217;，前提是已经把时区信息导入到了mysql库，否则会报错。导入方法：`mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -S /tmp/mysqld.sock mysql`
`system_time_zone` 变量只有全局值没有会话值，不能动态修改，MySQL 启动时，将尝试自动确定服务器的时区，并使用它来设置 system_time_zone 系统变量， 此后该值不变。当 time_zone=&#8217;system&#8217; 时，就是使用的这个时区，示例中 time_zone 就是 CST，而 CST 在 RedHat 上就是东八区：
`mysql> show global variables like '%time%zone%';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| system_time_zone | CST    |
| time_zone        | SYSTEM |
+------------------+--------+
2 rows in set (0.00 sec)
--可以看到在当前操作系统上 CST 就是 +08:00 时区
[root@localhost ~]# date -R
Thu, 02 Dec 2021 17:41:46 +0800
[root@localhost ~]# date
2021年 12月 02日 星期四 17:41:49 CST
`
## 时区影响了什么
概括一下就两点：
**1. NOW() 和 CURTIME() 系统函数的返回值受当前 session 的时区影响**
不仅是select now()，包括insert .. values(now())、以及字段的 DEFAULT CURRENT_TIMESTAMP 属性也受此影响：
`mysql> set time_zone='+00:00';
Query OK, 0 rows affected (0.00 sec)
mysql> select now(),CURTIME();
+---------------------+-----------+
| now()               | CURTIME() |
+---------------------+-----------+
| 2021-12-02 08:45:33 | 08:45:33  |
+---------------------+-----------+
1 row in set (0.00 sec)
mysql> set time_zone='+08:00';
Query OK, 0 rows affected (0.00 sec)
mysql> select now(),CURTIME();
+---------------------+-----------+
| now()               | CURTIME() |
+---------------------+-----------+
| 2021-12-02 16:45:39 | 16:45:39  |
+---------------------+-----------+
1 row in set (0.00 sec)
`
**2. timestamp 数据类型字段存储的数据受时区影响**
timestamp 数据类型会存储当时session的时区信息，读取时会根据当前 session 的时区进行转换；而 datetime 数据类型插入的是什么值，再读取就是什么值，不受时区影响。也可以理解为已经存储的数据是不会变的，只是 timestamp 类型数据在读取时会根据时区转换：
`mysql> set time_zone='+08:00';
Query OK, 0 rows affected (0.00 sec)
mysql> create table t(ts timestamp, dt datetime);
Query OK, 0 rows affected (0.02 sec)
mysql> insert into t values('2021-12-02 16:45:39','2021-12-02 16:45:39');
Query OK, 1 row affected (0.00 sec)
mysql> select * from t;
+---------------------+---------------------+
| ts                  | dt                  |
+---------------------+---------------------+
| 2021-12-02 16:45:39 | 2021-12-02 16:45:39 |
+---------------------+---------------------+
1 row in set (0.00 sec)
mysql> set time_zone='+00:00';
Query OK, 0 rows affected (0.00 sec)
mysql> select * from t;
+---------------------+---------------------+
| ts                  | dt                  |
+---------------------+---------------------+
| 2021-12-02 08:45:39 | 2021-12-02 16:45:39 |
+---------------------+---------------------+
1 row in set (0.00 sec)
`
## 结论
关于时区所有明面上的东西都在上面了，我们前面提到的困扰就是在暗处的经验。
**1. MySQL的安装规范中应该设置什么时区？**
对于国内的业务了，在 my.cnf 写入 `default-time-zone='+08:00'` `，其他地区和开发确认取对应时区即可。
为什么不设置为 `system` 呢？使用系统时间看起来也是个不错的选择，比较省事。不建议的原因有两点：
- 
操作系统的设置可能不归DBA管，万一别人没有设置正确的系统时区呢？把后背交给别人可能会有点发凉；
- 
多了一层系统调用，性能有损耗。
**2. JAVA应用读取到的时间和北京时间差了14个小时，为什么？怎么解决？**
这通常是 JDBC 参数中没有为连接设置时区属性（用`serverTimezone`参数指定），并且MySQL中没有设置全局时区，这样MySQL默认使用的是系统时区，即 CST。这样一来应用与MySQL 建立的连接的`session time_zone`为`CST`，前面我们提到 CST 在 RedHat 上是 +08:00 时区，但其实它一共能代表4个时区：
- 
Central Standard Time (USA) UT-6:00 美国标准时间
- 
Central Standard Time (Australia) UT+9:30 澳大利亚标准时间
- 
China Standard Time UT+8:00 中国标准时间
- 
Cuba Standard Time UT-4:00 古巴标准时间
JDBC在解析CST时使用了美国标准时间，这就会导致时区错误。要解决也简单：一是遵守上面刚说到的规范，对MySQL显示的设置&#8217;+08:00&#8217;时区；二是JDBC设置正确的 serverTimezone。
**3. 已经运行一段时间的业务，修改MySQL的时区会影响已经存储的时间类型数据吗？**
完全不会，只会影响对 timestamp 数据类型的读取。这里不得不提一句，为啥要用 timestamp？用 datetime 不香吗，范围更大，存储空间其实差别很小，赶紧加到开发规范中吧。
**4. 迁移数据时会有导致时间类型数据时区错误的可能吗？**
这个还真有，还是针对 timestamp 数据类型，比如使用 mysqldump 导出 csv 格式的数据，默认这种导出方式会使用 UTC 时区读取 timestamp 类型数据，这意味导入时必须手工设置 session.time_zone=&#8217;+00:00&#8217;才能保证时间准确：
`--将 test.t 导出成 csv
mysqldump -S /data/mysql/data/3306/mysqld.sock --single-transaction \
--master-data=2 -t -T /data/backup/test3 --fields-terminated-by=',' test t
--查看导出数据
cat /data/backup/test3/t.txt
2021-12-02 08:45:39,2021-12-02 16:45:39
`
如何避免？mysqldump 也提供了一个参数 `--skip-tz-utc`，意思就是导出数据的那个连接不设置 UTC 时区，使用 MySQL 的 gloobal time_zone 系统变量值。
其实 mysqldump 导出 sql 文件时默认也是使用 UTC 时区，并且会在导出的 sql 文件头部带有 session time_zone 信息，这样可以保证导 SQL 文件导入和导出时使用相同的时区，从而保证数据的时区正确（而导出的 csv 文件显然不可以携带此信息）。需要注意的是 `--compact` 参数会去掉 sql 文件的所有头信息，所以一定要记得：`--compact` 参数得和 `--skip-tz-utc` 一起使用。
`-- MySQL dump 10.13  Distrib 8.0.18, for linux-glibc2.12 (x86_64)
--
-- Host: 10.186.17.104    Database: sbtest
-- ------------------------------------------------------
...
/*!40103 SET TIME_ZONE='+00:00' */;
...
`