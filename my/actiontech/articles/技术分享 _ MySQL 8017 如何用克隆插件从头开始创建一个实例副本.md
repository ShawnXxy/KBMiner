# 技术分享 | MySQL 8.0.17 如何用克隆插件从头开始创建一个实例副本

**原文链接**: https://opensource.actionsky.com/20190805-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-08-05T00:28:44-08:00

---

> 作者：Vinicius Grippa
**序**
在这篇文章中，我们将讨论一个新功能 —— MySQL 8.0.17 clone 插件。在文章中，我将演示如何轻松地创建“经典”复制（一主一从），从头开始构建备用副本。
克隆插件允许在本地或从远程 MySQL 服务器实例克隆数据。在 InnoDB 中，克隆的数据是存储在物理快照的数据，这意味着，例如，数据可用于创建备用副本。让我们亲自动手，看看它是如何工作的。
**MySQL 8.0.17 clone 插件的安装和验证过程**
安装非常简单，与安装其他插件的工作方式相同。下面是安装克隆插件的命令行：
`    master [localhost:45008] ((none)) > INSTALL PLUGIN clone SONAME 'mysql_clone.so';`
- `Query OK, 0 rows affected (0.00 sec)`
以及如何检查克隆插件是否处于活动状态：- `master [localhost:45008] ((none)) > SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS`
- `WHERE PLUGIN_NAME LIKE 'clone';`
- `+-------------+---------------+`
- `| PLUGIN_NAME | PLUGIN_STATUS |`
- `+-------------+---------------+`
- `| clone | ACTIVE |`
- `+-------------+---------------+`
- `1 row in set (0.00 sec)`
请注意，这些步骤需要在 Donor（供体）和 Recipient（受体，也成为 Slave）上都执行。执行安装后，插件将在重新启动后自动加载，因此您不必再担心这一点。接下来，我们将在 Donor 上创建具有必要权限的用户，这样我们就可以远程连接到实例来克隆它。- `master [localhost:45008] ((none)) > create user clone_user@'%' identified by 'sekret';`
- `Query OK, 0 rows affected (0.01 sec)`
- `master [localhost:45008] ((none)) > GRANT BACKUP_ADMIN ON *.* TO 'clone_user'@'%';`
- `Query OK, 0 rows affected (0.00 sec)`
作为安全措施，我建议将百分号 ％ 替换为从机的 IP、主机名或网络掩码，以便只有未来的从服务器才能接受连接。现在，从服务器上，克隆用户需要CLONE_ADMIN 权限来替换从机数据，在克隆操作期间阻止 DDL 并自动重新启动服务器。- `slave1 [localhost:45009] ((none)) > create user clone_user@'localhost' identified by 'sekret';`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `slave1 [localhost:45009] ((none)) > GRANT CLONE_ADMIN ON *.* TO 'clone_user'@'localhost';`
- `Query OK, 0 rows affected (0.00 sec)`
接下来，安装并验证插件，并在主和从服务器上创建用户。
**克隆过程**
如上所述，克隆过程可以在本地或远程执行。此外，它支持复制，这意味着克隆操作从捐赠者提取和传输复制坐标并将其应用于收件人。它可用于 GTID 或非 GTID 复制。因此，要开始克隆过程，首先，让我们确保有一个有效的供体（Master）。这由 clone_valid_donor_list 参数控制。由于它是动态参数，您可以在服务器运行时进行更改。使用 show variables 命令将显示参数是否具有有效的供体（Master）：- `slave1 [localhost:45009] ((none)) > SHOW VARIABLES LIKE 'clone_valid_donor_list';`
- `+------------------------+-------+`
- `| Variable_name | Value |`
- `+------------------------+-------+`
- `| clone_valid_donor_list | |`
- `+------------------------+-------+`
- `1 row in set (0.01 sec)`
例子中，我们需要对它进行设置：- `slave1 [localhost:45009] ((none)) > set global clone_valid_donor_list = '127.0.0.1:45008';`
- `Query OK, 0 rows affected (0.00 sec)`
下一步不是强制性的，但使用默认的 log_error_verbosity，错误日志不会显示有关克隆进度的大量信息。所以，对于这个例子，我会将详细程度调整到更高的级别（在供体和受体机上）：- `mysql > set global log_error_verbosity=3;`
- `Query OK, 0 rows affected (0.00 sec)`
现在，让我们在受体（Slave）上开始克隆过程：- `slave1 [localhost:45009] ((none)) > CLONE INSTANCE FROM clone_user@127.0.0.1:45008 identified by 'sekret';`
- `Query OK, 0 rows affected (38.58 sec)`
可以在两个服务器的错误日志中观察克隆进度。以下是供体（Master）的输出：- `2019-07-31T12:48:48.558231Z 47 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: Acquired backup lock.'`
- `2019-07-31T12:48:48.558307Z 47 [Note] [MY-013457] [InnoDB] Clone Begin Master Task by clone_user@localhost`
- `2019-07-31T12:48:48.876138Z 47 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: COM_INIT: Storage Initialize.'`
- `2019-07-31T12:48:48.876184Z 47 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: COM_RES_COMPLETE.'`
- `2019-07-31T12:48:53.996976Z 48 [Note] [MY-013458] [InnoDB] Clone set state change ACK: 1`
- `2019-07-31T12:48:53.997046Z 48 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: COM_ACK: Storage Ack.'`
`2019-07-31T12:48:53.997148Z 48 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: COM_RES_COMPLETE.'`
- `2019-07-31T12:48:54.096766Z 47 [Note] [MY-013458] [InnoDB] Clone Master received state change ACK`
- `2019-07-31T12:48:54.096847Z 47 [Note] [MY-013458] [InnoDB] Clone State Change : Number of tasks = 1`
- `2019-07-31T12:48:54.096873Z 47 [Note] [MY-013458] [InnoDB] Clone State BEGIN FILE COPY`
- `...`
- `2019-07-31T12:49:33.939968Z 47 [Note] [MY-013457] [InnoDB] Clone End Master Task ID: 0 Passed, code: 0:`
- `2019-07-31T12:49:33.940016Z 47 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: COM_EXIT: Storage End.'`
- `2019-07-31T12:49:33.940115Z 47 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: COM_RES_COMPLETE.'`
- `2019-07-31T12:49:33.940150Z 47 [Note] [MY-013273] [Clone] Plugin Clone reported: 'Server: Exiting clone protocol.'`
和受体（Slave）：- `2019-07-31T12:48:48.521515Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Task Connect.'`
- `2019-07-31T12:48:48.557855Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Master ACK Connect.'`
- `2019-07-31T12:48:48.557923Z 8 [Note] [MY-013457] [InnoDB] Clone Apply Begin Master Version Check`
- `2019-07-31T12:48:48.558474Z 8 [Note] [MY-013457] [InnoDB] Clone Apply Version End Master Task ID: 0 Passed, code: 0:`
- `2019-07-31T12:48:48.558507Z 8 [Note] [MY-013457] [InnoDB] Clone Apply Begin Master Task`
- `2019-07-31T12:48:48.558749Z 8 [Warning] [MY-013460] [InnoDB] Clone removing all user data for provisioning: Started`
- `2019-07-31T12:48:48.558769Z 8 [Note] [MY-011977] [InnoDB] Clone Drop all user data`
- `2019-07-31T12:48:48.863134Z 8 [Note] [MY-011977] [InnoDB] Clone: Fix Object count: 371 task: 0`
- `2019-07-31T12:48:53.829493Z 8 [Note] [MY-011977] [InnoDB] Clone Drop User schemas`
- `2019-07-31T12:48:53.829948Z 8 [Note] [MY-011977] [InnoDB] Clone: Fix Object count: 5 task: 0`
- `2019-07-31T12:48:53.838939Z 8 [Note] [MY-011977] [InnoDB] Clone Drop User tablespaces`
- `2019-07-31T12:48:53.839800Z 8 [Note] [MY-011977] [InnoDB] Clone: Fix Object count: 6 task: 0`
- `2019-07-31T12:48:53.910728Z 8 [Note] [MY-011977] [InnoDB] Clone Drop: finished successfully`
- `...`
- `2019-07-31T12:49:33.836509Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Command COM_EXECUTE.'`
- `2019-07-31T12:49:33.836998Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Master ACK COM_EXIT.'`
- `2019-07-31T12:49:33.839498Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Master ACK Disconnect : abort: false.'`
- `2019-07-31T12:49:33.851403Z 0 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Command COM_EXECUTE.'`
- `2019-07-31T12:49:33.851796Z 0 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Task COM_EXIT.'`
- `2019-07-31T12:49:33.852398Z 0 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Task Disconnect : abort: false.'`
- `2019-07-31T12:49:33.852472Z 0 [Note] [MY-013457] [InnoDB] Clone Apply End Task ID: 1 Passed, code: 0:`
- `2019-07-31T12:49:33.940156Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Task COM_EXIT.'`
- `2019-07-31T12:49:33.940810Z 8 [Note] [MY-013272] [Clone] Plugin Clone reported: 'Client: Task Disconnect : abort: false.'`
- `2019-07-31T12:49:33.944244Z 8 [Note] [MY-013457] [InnoDB] Clone Apply End Master Task ID: 0 Passed, code: 0:`
请注意，克隆过程完成后，将重新启动受体（Slave）上的 MySQL 服务。在此之后，数据库已准备好被访问，最后一步是设置副本。
**复制过程**
二进制日志位置（文件名，偏移量）和 GTID 坐标都从供体（Master） MySQL 服务器实例中提取和传输。可以在克隆的 MySQL 服务器实例上执行以下查询，以查看二进制日志位置或应用的最后一个事务的 GTID：- `# Binary log position`
- `slave1 [localhost:45009] ((none)) > SELECT BINLOG_FILE, BINLOG_POSITION FROM performance_schema.clone_status;`
- `+------------------+-----------------+`
- `| BINLOG_FILE | BINLOG_POSITION |`
- `+------------------+-----------------+`
- `| mysql-bin.000001 | 437242601 |`
- `+------------------+-----------------+`
- `1 row in set (0.01 sec)`
- `# GTID`
- `slave1 [localhost:45009] ((none)) > SELECT @@GLOBAL.GTID_EXECUTED;`
- `+----------------------------------------------+`
- `| @@GLOBAL.GTID_EXECUTED |`
- `+----------------------------------------------+`
- `| 00045008-1111-1111-1111-111111111111:1-32968 |`
- `+----------------------------------------------+`
- `1 row in set (0.00 sec)`
有了这些信息，我们需要相应地执行 CHANGE MASTER 命令：- `slave1 [localhost:45009] ((none)) > CHANGE MASTER TO`
- `    MASTER_HOST = '127.0.0.1',`
- `    MASTER_PORT = 45008,`
- `    MASTER_USER='root',`
- `    MASTER_PASSWORD='msandbox',`
- `    MASTER_AUTO_POSITION = 1;`
- `Query OK, 0 rows affected, 2 warnings (0.02 sec)`
- 
- `slave1 [localhost:45009] ((none)) > start slave;`
- `Query OK, 0 rows affected (0.00 sec)`
**限制**
克隆插件有一些限制，这里将对它们进行描述。在我看来，社区将面临两个主要限制。首先，它只能克隆 InnoDB 引擎的表。这意味着 MyISAM 和 CSV 引擎存储的任何表，都将被克隆为空表。另一个限制是关于 DDL，包括 TRUNCATE TABLE，这在克隆操作期间是不允许的。但是，允许并发 DML。如果 DDL 正在运行，则克隆操作将等待锁定：- `+----+------------+-----------------+------+----------+-------+----------------------------+------+`
- `| Id | User       | Host            | db   | Command  | Time  | State                      | Info |`
- `+----+------------+-----------------+------+----------+-------+----------------------------+------+`
- `| 63 | clone_user | localhost:34402 | NULL | clone    |     3 | Waiting for backup lock    | NULL |`
- `+----+------------+-----------------+------+----------+-------+----------------------------+------+`
否则，如果克隆操作正在运行，则 DDL 将等待锁定：- `+----+-----------------+-----------------+------+------------------+-------+---------------------------------------------------------------+----------------------------------+`
- `| Id | User            | Host            | db   | Command          | Time  | State                                                         | Info                             |`
- `+----+-----------------+-----------------+------+------------------+-------+---------------------------------------------------------------+----------------------------------+`
- `| 52 | msandbox        | localhost       | test | Query            |     5 | Waiting for backup lock                                       | alter table joinit engine=innodb |`
- `| 60 | clone_user      | localhost:34280 | NULL | clone            |    15 | Receiving from client                                         | NULL                             |`
- `| 61 | clone_user      | localhost:34282 | NULL | clone            |    15 | Receiving from client                                         | NULL                             |`
- `| 62 | clone_user      | localhost:34284 | NULL | clone            |     6 | Receiving from client                                         | NULL                             |`
- `+----+-----------------+-----------------+------+------------------+-------+---------------------------------------------------------------+----------------------------------+`
**结论**借助 MySQL 8.0.17 clone 插件，创建副本变得更加容易。此功能也可以使用 SSL 连接和加密数据使用。在发布此博客文章时，克隆插件不仅可用于设置异步副本，还可用于设置组复制成员。阅读原文https://www.percona.com/blog/2019/08/01/mysql-8-0-17-clone-plugin-how-to-create-a-slave-from-scratch/
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)