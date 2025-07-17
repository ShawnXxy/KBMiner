# 故障分析 | Binlog 太大导致无法解析怎么办？

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-binlog-%e5%a4%aa%e5%a4%a7%e5%af%bc%e8%87%b4%e6%97%a0%e6%b3%95%e8%a7%a3%e6%9e%90%e6%80%8e%e4%b9%88%e5%8a%9e%ef%bc%9f/
**分类**: 技术干货
**发布时间**: 2023-11-20T22:58:36-08:00

---

由于业务写入了一条大事务，导致 MySQL 的 binlog 膨胀。在解析大的 binlog 时，经常会遇到这个问题，导致无法解析，没有其他工具的情况下，很难分析问题。
> 作者：孙绪宗，新浪微博 DBA 团队工程师，主要负责 MySQL、PostgreSQL 等关系型数据库运维。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文共 3200 字，预计阅读需要 10 分钟。
# 故障现象
由于业务写入了一条大事务，导致 MySQL 的 binlog 膨胀。在解析大的 binlog 时，经常会遇到这个问题，导致无法解析，没有其他工具的情况下，很难分析问题。
# 故障复现
`[root@xuzong mysql]# ls -lh mysql-bin.003300
-rw-r----- 1 my3696 mysql 6.7G Oct 30 16:24 mysql-bin.003300
[root@xuzong mysql]# /usr/local/mysql-5.7.35/bin/mysqlbinlog -vv mysql-bin.003300 > 1.sql
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.334z3P' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
mysqlbinlog: Error writing file '/tmp/tmp.0Uirch' (Errcode: 28 - No space left on device)
`
# 猜测
- 可能是配置文件中 tmpdir 的问题，但是修改这个得重启 MySQL。
- 能不能在不重启 MySQL 的情况下，修改这个临时空间。
# 验证猜测
## 猜测一
看一下 my.cnf 设置的 tmpdir，发现并不是使用的这个参数，看来猜测一不对。
`[root@mysql mysql]# cat my.cnf | grep tmpdir
tmpdir                          = /data1/dbatemp
`
## 猜测二
网上搜了一下，大部分是讲临时表满怎么解决的，也就是猜测一的方案，并没有很明确的方法来修改 mybinlog 解析时，所使用的的临时句柄占用空间。
# 问题分析
只能看看源码，看一下 mysqlbinlog 到底是怎么获取 tmpdir 的。
`mysqbinlog.cc
int main(int argc, char** argv)
{
........
MY_TMPDIR tmpdir;
tmpdir.list= 0;
if (!dirname_for_local_load)
{
if (init_tmpdir(&tmpdir, 0))
exit(1);
dirname_for_local_load= my_strdup(PSI_NOT_INSTRUMENTED,
my_tmpdir(&tmpdir), MY_WME);
}
........
}
mf_tempdir.cc
my_bool init_tmpdir(MY_TMPDIR *tmpdir, const char *pathlist)
{
char *end, *copy;
char buff[FN_REFLEN];
DBUG_ENTER("init_tmpdir");
DBUG_PRINT("enter", ("pathlist: %s", pathlist ? pathlist : "NULL"));
Prealloced_array<char*, 10, true> full_list(key_memory_MY_TMPDIR_full_list);
memset(tmpdir, 0, sizeof(*tmpdir));
if (!pathlist || !pathlist[0])
{
/* Get default temporary directory */
pathlist=getenv("TMPDIR");    /* Use this if possible */ //这里能看到是获取的机器环境变量
#if defined(_WIN32)
if (!pathlist)
pathlist=getenv("TEMP"); //windows是temp
if (!pathlist)
pathlist=getenv("TMP");  //linux是tmp
#endif
if (!pathlist || !pathlist[0])
pathlist= DEFAULT_TMPDIR;
}
........
}
`
好家伙，竟然是获取的机器环境变量，那么这个问题就解决了。
# 问题处理
临时修改一下机器的 tmpdir 变量即可。
`[root@mysql mysql]# export TMPDIR="/data1"
[root@mysql mysql]# echo ${TMPDIR:-/tmp}
[root@xuzong mysql]# /usr/local/mysql-5.7.35/bin/mysqlbinlog -vv mysql-bin.003300 > 1.sql
`
# 总结
- 有问题还是要看看源码。
- 可以考虑使用 binlog 解析工具，比如 bin2sql 解决问题。
- 可以看看慢日志里是否有记录。
# 补充
原来这个问题在 [MySQL 官方手册](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) 中有所描述，在此做一个补充。
![](.img/58312bed.jpg)
> When running mysqlbinlog against a large binary log, be careful that the filesystem has enough space for the resulting files. To configure the directory that mysqlbinlog uses for temporary files, use the TMPDIR environment variable.