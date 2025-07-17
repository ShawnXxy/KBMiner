# 新特性解读 | MySQL 8.0 REDO 归档目录权限问题

**原文链接**: https://opensource.actionsky.com/20230418-mysql8/
**分类**: MySQL 新特性
**发布时间**: 2023-04-17T22:06:37-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
特分享出来最近在整理 MySQL 热备工具的实验题目时遇到的 REDO 日志归档问题！
MySQL 的 REDO 日志归档功能在 8.0.17 版本后发布，目的是为了解决使用 MySQL 热备工具比如 mysqlbackup 、xtrabackup 等备份 REDO 日志的速度慢于业务生成 REDO 日志的速度而导致的备份数据不一致问题（未及时备份的 RRDO 日志被提前覆盖写入！）。
MySQL的 REDO 日志归档功能开启非常简单，只需对参数innodb_redo_log_archive_dirs简单设置即可。
set persist innodb_redo_log_archive_dirs='redo_archive1:/redo_mysql/3306'
其中 redo_archive1 是一个标签，可以随便起名字；/redo_mysql/3306 用来指定REDO 日志归档存放的位置。
##### 我在使用的过程中，遇到几个细节问题：
##### 1. REDO 日志归档的目录权限、属主等一定要设置正确，要不然可能会有以下几种错误输出 (MySQL 客户端提示错误，热备工具可能提示警告！)：
###### 错误1：ERROR 3844 (HY000): Redo log archive directory &#8216;/redo_mysql/3306&#8217; does not exist or is not a directory
前期需要创建的目录与相关权限设定如下：
# 归档目录得提前建！
[root@ytt-pc ~]# mkdir -p /redo_mysql/3306
# 设置归档目录访问权限，只允许属主完全访问。
[root@ytt-pc ~]# chmod -R 700 /redo_mysql/3306/
接下来使用MySQL管理员用户或者具有system_variables_admin权限的用户来在线设置此变量：
# 设置变量
<mysql:8.0.32:(none)>set persist innodb_redo_log_archive_dirs='redo_archive1:/redo_mysql/3306';
Query OK, 0 rows affected (0.01 sec)
# 查看变量
<mysql:8.0.32:(none)>show variables like 'innodb_redo_log_archive_dirs';
+------------------------------+--------------------------------+
| Variable_name                | Value                       |
+------------------------------+--------------------------------+
| innodb_redo_log_archive_dirs | redo_archive1:/redo_mysql/3306 |
+------------------------------+--------------------------------+
1 row in set (0.00 sec)
使用mysqlbackup来发起一个备份：
[root@ytt-pc /]# mysqlbackup --defaults-file=/etc/my.cnf --defaults-group-suffix=@3306 --login-path=backup_pass2 --backup-dir=/tmp/full --show-progress backup
#备份完成后，有一个警告：
mysqlbackup completed OK! with 1 warnings
#往前翻此警告： 这里是详细内容！
230329 13:43:48 MAIN  WARNING: MySQL query 'DO innodb_redo_log_archive_start('redo_archive1','16800686281315958');': 3844, Redo log archive directory '/redo_mysql/3306/16800686281315958' does not exist or is not a directory
错误1是由于访问归档目录的属主不具备写权限，修复错误1：确认运行MySQL实例的OS用户为 ytt。
[root@ytt-pc 3306]# ps aux | grep mysqld
ytt       4625  1.0  4.5 1800264 373112 ?      Ssl  12:47   0:00 /usr/sbin/mysqld --defaults-group-suffix=@3306
给/redo_mysql/3306 设置属于OS用户ytt的权限：错误1被修复。
[root@ytt-pc /]# chown -R ytt.ytt /redo_mysql
此时使用mysqlbackup 重新发起一个热备，会产生一个新的错误代码， 我们把它命名为错误2。
###### 错误2：其实是一个警告！根据错误代码内容，提示为无权限操作此目录(OS errno: 13 &#8211; Permission denied)。
230329 13:48:10 MAIN  WARNING: MySQL query 'DO innodb_redo_log_archive_start('redo_archive1','16800688906187002');': 3847, Cannot create redo log archive file '/redo_mysql/3306/16800688906187002/archive.01132dcf-cde1-11ed-971f-0800272d8a05.000001.log' (OS errno: 13 - Permission denied)
问题产生的原因是调用mysqlbackup的OS用户不具备归档日志目录的写权限，必须使用对应的OS用户来调用mysqlbackup。
以下是解决方法和主动验证步骤。
# 解决方法：需要切换到此目录OS属主用户：
[root@ytt-pc tmp]# su ytt
[ytt@ytt-pc tmp]$ mysqlbackup --defaults-file=/etc/my.cnf --defaults-group-suffix=@3306 --login-path=backup_pass2 --backup-dir=/tmp/full  backup
# 备份完成，无报错：
mysqlbackup completed OK!
# 摘取其中归档日志的信息如下：
230329 14:46:00 MAIN     INFO: Creating monitor for redo archive.
230329 14:46:00 MAIN     INFO: Started redo log archiving.
# 对应的MySQL 日志内容为：mysqlbackup 备份过程中调用系统函数innodb_redo_log_archive_start来激活 REDO 日志归档，调用系统函数innodb_redo_log_archive_stop来关闭 REDO 日志归档。 这里do是MySQL一个特有的语法，只执行不输出，有点类似其他数据库的perform语句。
2023-03-29T06:46:00.553205Z        47 Query     SELECT @@GLOBAL.innodb_redo_log_archive_dirs
2023-03-29T06:46:00.553389Z        47 Query     DO innodb_redo_log_archive_start('redo_archive1','16800723605224011')
..
2023-03-29T06:46:03.895591Z        47 Query     DO innodb_redo_log_archive_stop()
###### 2. 用于 REDO 日志归档的 MySQL 用户必须有 innodb_redo_log_archive 权限。
<mysql:8.0.32:(none)>show grants for backup_user2\G
...
*************************** 2. row ***************************
Grants for backup_user2@%: GRANT BACKUP_ADMIN,ENCRYPTION_KEY_ADMIN,INNODB_REDO_LOG_ARCHIVE,SYSTEM_VARIABLES_ADMIN ON *.* TO `backup_user2`@`%`
...
5 rows in set (0.00 sec)
###### 3. REDO 日志归档功能除了使用热备工具来调用外，也可以直接在 MySQL 客户端来调用。
[ytt@ytt-pc ~]$ mysql --login-path=backup_pass2
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 41
Server version: 8.0.32 MySQL Community Server - GPL
...
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
<mysql:8.0.32:(none)>DO innodb_redo_log_archive_start('redo_archive1','20230329');
Query OK, 0 rows affected (0.02 sec)
对应的归档日志：
[ytt@ytt-pc 20230329]$ pwd
/redo_mysql/3306/20230329
[ytt@ytt-pc 20230329]$ du -sh archive.01132dcf-cde1-11ed-971f-0800272d8a05.000001.log 
4.0K archive.01132dcf-cde1-11ed-971f-0800272d8a05.000001.log
期间造点数据，可以看到归档日志的大小变化：由4K增长到128M
[ytt@ytt-pc 20230329]$ du -sh archive.01132dcf-cde1-11ed-971f-0800272d8a05.000001.log 
128M archive.01132dcf-cde1-11ed-971f-0800272d8a05.000001.log
###### 4. 激活 REDO 日志归档的会话要保持打开，关闭会话则REDO 日志不再归档！
###### 5. REDO 日志归档的目录不能属于 MySQL 实例已经确认的目录，比如 datadir，innodb_directories 等等。