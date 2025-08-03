# 故障分析 | MySQL 执行 Online DDL 操作报错空间不足？

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-mysql-%e6%89%a7%e8%a1%8c-online-ddl-%e6%93%8d%e4%bd%9c%e6%8a%a5%e9%94%99%e7%a9%ba%e9%97%b4%e4%b8%8d%e8%b6%b3%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2024-02-19T23:44:52-08:00

---

在 MySQL 中执行 Online DDL 之前，需要保证在三个方面的空间充足。
> 作者：徐文梁，爱可生 DBA 成员，一个执着于技术的数据库工程师，主要负责数据库日常运维工作。擅长 MySQL，Redis 及其他常见数据库也有涉猎；喜欢垂钓，看书，看风景，结交新朋友。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 1400 字，预计阅读需要 4 分钟。
# 问题背景
客户反馈对某张表执行 `alter table table_name engine=innodb;` 时报错空间不足。
通过登录数据库查看客户的 *tmpdir* 设置的路径，发现是 `/tmp`。该目录磁盘空间本身较小，调整 *tmpdir* 的路径与数据目录相同，重新执行 `ALTER` 操作执行成功。
问题到此结束了，但是故事并没有结束。通过查看[官网信息](https://dev.mysql.com/doc/refman/5.7/en/innodb-online-ddl-space-requirements.html)，我们可以从这个小小的报错中深挖更多信息。
# 信息解读
从官网的论述中，我们可以了解到，在进行 Online DDL 操作时，需要保证以下三个方面的空间充足，否则可能会导致空间不足报错。
## 临时日志文件
当进行 Online DDL 操作创建索引或者更改表时，临时日志文件会记录期间的并发 DML 操作，临时日志文件最大值由 _innodb_online_alter_log_max*size* 参数控制，如果 Online DDL 操作耗时较长（如果表数据量较大这是很有可能的），并且期间并发 DML 对表中的记录修改较多，则可能导致临时日志文件大小超过 _innodb_online_alter_log_max*size* 值，从而引发 **DB_ONLINE_LOG_TOO_BIG** 错误，并回滚未提交的并发 DML 操作。
## 临时排序文件
对于会重建表的 Online DDL 操作，在创建索引期间，会将临时排序文件写入到 MySQL 的临时目录。仅考虑 UNIX 系统，对应的参数为 *tmpdir*，如果 `/tmp` 目录比较小，请设置该参数为其他目录，否则可能会因为无法容纳排序文件而导致 Online DDL 失败。
## 中间表文件
对于会重建表的 Online DDL 操作，会在与原始表相同的目录中创建一个临时中间表文件，中间表文件可能需要与原始表大小相等的空间。中间表文件名以 *#sql-ib* 前缀开头，仅在 Online DDL 操作期间短暂出现。
# 前置准备
针对官网的论述，我们可以进行实际测试，这里对临时排序文件和中间表文件场景进行测试，为了故事更好的发展，先做一些准备工作：
**1. 创建一个测试库**
数据目录对应为 `/opt/mysql/data/3310/my_test`。
`create database my_test;
`
**2. 限制数据目录大小**
`#创建一个指定大小的磁盘镜像文件，这里为 600M
dd if=/dev/zero of=/root/test.img bs=60M count=10
#挂载设备
losetup /dev/loop0 /root/test.img
#格式化设备
mkfs.ext3 /dev/loop0
#挂载为文件夹，则限制其文件夹空间大小为 600M
mount -t ext3 /dev/loop0 /opt/mysql/data/3310/my_test
#修改属组为 MySQL 服务对应用户
chown -R mysql.mysql /opt/mysql/data/3310/my_test
`
**3. 创建一张测试表**
`CREATE TABLE `student` (
`id` int(11) NOT NULL,
`name` varchar(50) NOT NULL,
`score` int(11) DEFAULT NULL,
`age` int(11) DEFAULT NULL,
`sex` varchar(10) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
`
**4. 插入一些数据**
注意：数据量不要太小，小于 `/opt/mysql/data/3310/my_test` 目录的一半，建议 **30%** 左右。
`./mysql_random_data_load -h127.0.0.1 -P3310 -uuniverse_op -p'xxx' --max-threads=8 my_test student 1500000
`
**5. 修改 /tmp 大小**
这里 *tmpdir* 目录为 `/tmp`，修改 `/tmp` 大小为一个较小值。
`mount -o remount,size=1M tmpfs /tmp
`
**6. 修改其他参数**
修改 `tmp_table_size` 和 `max_heap_table_size` 值为较小值，这里仅仅为了便于生成磁盘临时文件，生产环境不建议，会严重影响性能。
`set sort_buffer_size=128*1024;
set tmp_table_size=128*1024;
`
# 场景测试
登录数据库执行如下操作，可以观察到添加索引失败，报错信息如下：
`mysql> alter table student add  idx_name index(name);
ERROR 1878 (HY000): Temporary file write failure.
`
执行如下操作修改 `/tmp` 目录大小，再次执行 `ALTER` 操作成功。
`[root@localhost ~]# mount -o remount,size=500M tmpfs /tmp
mysql> alter table student add index(name);
Query OK, 0 rows affected (4.92 sec)
Records: 0 Duplicates: 0 Warnings: 0
`
观察 `/opt/mysql/data/3310/my_test` 目录已使用空间，如果使用率较低，**建议继续插入数据到磁盘空间使用率超过 50%**
执行如下操作，会报如下错误：
`mysql> alter table student engine=innodb;
ERROR 1114 (HY000): The table 'student' is full
`
# 问题总结
好了，最后总结一下。为了我们的 Online DDL 操作顺利进行，需要注意以下几点：
- 在进行操作前，记得先检查 `innodb_online_alter_log_max_size` 值，预估下是否需要修改。
可以直接修改为一个较大值，但是没有百分百的好事，坏处就是如果业务在 DDL 操作期间并发 DML 修改记录较多，Online DDL 结束时锁定表以应用记录的 DML 时间会增加。所以，选择好时机很重要，在对的时间做对的事，当然是在业务低峰期，或者考虑工具吧（*pt-osc* 或 *ghost*）。
- 在安装实例时即设置 *tmpdir* 为合理的值。
温馨提示，该值不支持动态修改，真出现问题就晚了，毕竟生产上不允许随便重启服务的。
- 及时关注磁盘空间。
不要等到磁盘空间快满了才想着通过 Online DDL 操作进行碎片空间清理。例如 `optimize table table_name;`，`alter table  table_name engine=innodb;` 等操作。这些操作本身也是需要额外的空间的，等待你的可能是 FAILURE。