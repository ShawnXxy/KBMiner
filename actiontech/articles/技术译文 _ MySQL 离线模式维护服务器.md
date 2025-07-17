# 技术译文 | MySQL 离线模式维护服务器

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e8%af%91%e6%96%87-mysql-%e7%a6%bb%e7%ba%bf%e6%a8%a1%e5%bc%8f%e7%bb%b4%e6%8a%a4%e6%9c%8d%e5%8a%a1%e5%99%a8/
**分类**: MySQL 新特性
**发布时间**: 2023-10-09T00:48:11-08:00

---

# 离线模式
作为 DBA，最常见的任务之一就是批量处理 MySQL 服务的启停或其他一些活动。在停止 MySQL 服务前，我们可能需要检查是否有活动连接；如果有，我们可能需要把它们全部杀死。通常，我们使用 [pt-kill](https://docs.percona.com/percona-toolkit/pt-kill.html?_gl=1*11ns0v*_gcl_au*NTg1NzA0MDMyLjE2OTAxMDY1MzY.*_ga*MTM2Mjk4NTIwNC4xNjkwMTA2NTM2*_ga_DXWV0B7PSN*MTY5NjY0Mzc3Ny4yNS4xLjE2OTY2NDQ3MTEuNjAuMC4w) 杀死应用连接或使用 `SELECT` 语句查询准备杀死语句。例如：
`pt-kill --host=192.168.11.11 --user=percona -p --sentinel /tmp/pt-kill.sentinel2 --pid /tmp/pt-kill.pid --victims all --match-command 'Query' --ignore-user 'pmm|rdsadmin|system_user|percona' --busy-time 10 --verbose --print --kill
select concat('kill ',id,';') from information_schema.processlist where user='app_user';
`
MySQL 有一个名为 `offline_mode` 的变量来将服务器设置为维护模式。设置此选项后，它会立即断开所有不具有 **SYSTEM_VARIABLES_ADMIN** 和 **CONNECTION_ADMIN** 权限的客户端连接，并且不允许新连接，除非用户拥有这些权限。如果您手动终止连接或使用 `pt-kill`，则无法避免新连接的创建。但通过使用这种模式，我们可以避免新的连接。这是一个全局动态变量，我们可以在服务器运行时设置此模式。
要启用 `offline_mode`，用户帐户必须具有 **SYSTEM_VARIABLES_ADMIN*** 权限和 **CONNECTION_ADMIN** 权限（或已弃用的 **SUPER** 权限，它涵盖了这两个权限）。**CONNECTION_ADMIN** 从 MySQL 8.0.31 开始是必需的，并建议在所有版本中使用，以防止意外锁定。让我们测试一下。
要对此进行测试，请创建一个新用户 *app_user*，该用户仅具有 **DDL/DML** 权限。
`mysql> create user app_user identified by 'App@!234TEst';
Query OK, 0 rows affected (0.20 sec)
mysql> GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP , REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE,CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, CREATE TABLESPACE on *.* to app_user;
Query OK, 0 rows affected (0.00 sec)
`
使用 *aap_user* 用户启动 sysbench 工具。
`[root@centos12 vagrant]# sysbench /usr/share/sysbench/oltp_read_write.lua --threads=10 --time=100  --mysql-db=sysbench --mysql-user=app_user --mysql-password='App@!234TEst' run
sysbench 1.0.20 (using bundled LuaJIT 2.1.0-beta2)
Running the test with following options:
Number of threads: 10
Initializing random number generator from current time
Initializing worker threads...
`
```
mysql> show processlist;
+----+-----------------+---------------------+----------+-------------+------+-----------------------------------------------------------------+------------------------------------------------------------------------------------------------------+---------+-----------+---------------+
| Id | User | Host | db | Command | Time | State | Info | Time_ms | Rows_sent | Rows_examined |
+----+-----------------+---------------------+----------+-------------+------+-----------------------------------------------------------------+------------------------------------------------------------------------------------------------------+---------+-----------+---------------+
| 5 | event_scheduler | localhost | NULL | Daemon | 2151 | Waiting for next activation | NULL | 2151034 | 0 | 0 |
| 9 | bhuvan | 192.168.33.11:50642 | NULL | Binlog Dump | 2102 | Source has sent all binlog to replica; waiting for more updates | NULL | 2102317 | 0 | 0 |
| 14 | bhuvan | localhost | NULL | Query | 0 | init | show processlist | 0 | 0 | 0 |
| 20 | app_user | localhost | sysbench | Execute | 0 | waiting for handler commit | COMMIT | 11 | 0 | 0 |
| 21 | app_user | localhost | sysbench | Execute | 0 | updating | DELETE FROM sbtest1 WHERE id=5000 | 6 | 0 | 0 |
| 23 | app_user | localhost | sysbench | Execute | 0 | waiting for handler commit | COMMIT | 8 | 0 | 0 |
| 24 | app_user | localhost | sysbench | Execute | 0 | waiting for handler commit | COMMIT | 18 | 0 | 0 |
| 25 | app_user | localhost | sysbench | Execute | 0 | updating | UPDATE sbtest1 SET c='99153469917-25523144931-18125321038-96151238215-88445737418-14906501975-136014 | 13 | 0 | 0 |
| 27 | app_user | localhost | sysbench | Execute | 0 | waiting for handler commit | COMMIT | 7 | 0 | 0 |
| 28 | app_user | localhost | sysbench | Execute | 0 | statistics | SELECT c FROM sbtest1 WHERE id=5003 | 0 | 0 | 0 |
| 29 | app_user | localhost | sysbench | Execute | 0 | updating | UPDATE sbtest1 SET c='84180675456-88426921120-90373546373-84823361786-77912396694-08592771856-912331 | 13 | 0 | 0 |
+----+-----------------+---------------------+----------+-------------+------+-----------------------------------------------------------------+------------------------------------------------------------------------------------------------------+---------+-----------+---------------+
13 rows in set (0.00 sec)
```
当 sysbench 运行时，设置 `offline_mode=ON`，来自 [sysbech](https://www.howtoforge.com/how-to-benchmark-your-system-cpu-file-io-mysql-with-sysbench#:~:text=1%20Installing%20sysbench,-On%20Debian%2FUbuntu&text=On%20CentOS%20and%20Fedora%2C%20it%20can%20be%20installed%20from%20EPEL%20repository.&text=to%20learn%20more%20about%20its,IO%20performance%2C%20and%20MySQL%20performance.) 的所有连接都将被终止。您将在 sysbench 中看到错误。
`mysql> select @@offline_mode;
+----------------+
| @@offline_mode |
+----------------+
| 0 |
+----------------+
1 row in set (0.15 sec)
mysql> set global offline_mode=1;
Query OK, 0 rows affected (0.15 sec)
mysql> show processlist;
+----+-----------------+---------------------+------+-------------+------+-----------------------------------------------------------------+------------------+---------+-----------+---------------+
| Id | User | Host | db | Command | Time | State | Info | Time_ms | Rows_sent | Rows_examined |
+----+-----------------+---------------------+------+-------------+------+-----------------------------------------------------------------+------------------+---------+-----------+---------------+
| 5 | event_scheduler | localhost | NULL | Daemon | 2178 | Waiting for next activation | NULL | 2178008 | 0 | 0 |
| 9 | bhuvan | 192.168.33.11:50642 | NULL | Binlog Dump | 2129 | Source has sent all binlog to replica; waiting for more updates | NULL | 2129291 | 0 | 0 |
| 14 | bhuvan | localhost | NULL | Query | 0 | init | show processlist | 0 | 0 | 0 |
+----+-----------------+---------------------+------+-------------+------+-----------------------------------------------------------------+------------------+---------+-----------+---------------+
3 rows in set (0.01 sec)
`
如果您在 `offline_mode=1` 时尝试使用 *app_user* 连接数据库，它将不允许连接并收到一条错误消息，表明服务器当前处于离线模式。这个 `offline_mode` 不会影响复制。可以看到上面的 processlist 日志，当我们设置 `offline_mode=1` 时，复制线程并没有断开。要禁用 `offline_mode`，请将值设置为 0。
`mysql> set global offline_mode=0;
Query OK, 0 rows affected (0.00 sec)
`
# 结论
`offline_mode` 是将服务器置于维护模式的一个不错的选择。只需确保应用程序用户没有管理员权限，只有管理员有。我们可以在以下情况下使用 `offline_mode`：
- 在将数据库服务器取出进行维护或其相关活动之前，请在配置文件中进行更改并保持此模式，直到所有活动完成。
- 在从服务器进行备份时，我们可以设置这个 `offline_mode`，以避免服务器的负载，使备份速度更快。
- 如果由于大量查询而导致副本上出现大量复制，我们可以设置此模式，直到复制与主服务器同步。
- 当您想立即终止所有应用程序连接时。
本文原文：[https://www.percona.com/blog/mysql-offline-mode-to-disconnect-client-connections/](https://www.percona.com/blog/mysql-offline-mode-to-disconnect-client-connections/)