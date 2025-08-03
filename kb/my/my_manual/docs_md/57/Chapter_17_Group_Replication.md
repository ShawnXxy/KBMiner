Group Replication Background

accordingly. Sometimes servers can leave the group unexpectedly, in which case the failure detection
mechanism detects this and notifies the group that the view has changed. This is all automatic.

The chapter is structured as follows:

• Section 17.1, “Group Replication Background” provides an introduction to groups and how Group

Replication works.

• Section 17.2, “Getting Started” explains how to configure multiple MySQL Server instances to create a

group.

• Section 17.3, “Requirements and Limitations” explains architecture and setup requirements and

limitations for Group Replication.

• Section 17.4, “Monitoring Group Replication” explains how to monitor a group.

• Section 17.5, “Group Replication Operations” explains how to work with a group.

• Section 17.6, “Group Replication Security” explains how to secure a group.

• Upgrading Group Replication explains how to upgrade a group.

• Section 17.7, “Group Replication Variables” is a reference for the system variables specific to Group

Replication.

• Section 17.8, “Frequently Asked Questions” provides answers to some technical questions about

deploying and operating Group Replication.

• Section 17.9, “Group Replication Technical Details” provides in-depth information about how Group

Replication works.

17.1 Group Replication Background

This section provides background information on MySQL Group Replication.

The most common way to create a fault-tolerant system is to resort to making components redundant, in
other words the component can be removed and the system should continue to operate as expected. This
creates a set of challenges that raise complexity of such systems to a whole different level. Specifically,
replicated databases have to deal with the fact that they require maintenance and administration of several
servers instead of just one. Moreover, as servers are cooperating together to create the group several
other classic distributed systems problems have to be dealt with, such as network partitioning or split brain
scenarios.

Therefore, the ultimate challenge is to fuse the logic of the database and data replication with the logic of
having several servers coordinated in a consistent and simple way. In other words, to have multiple servers
agreeing on the state of the system and the data on each and every change that the system goes through.
This can be summarized as having servers reaching agreement on each database state transition, so that
they all progress as one single database or alternatively that they eventually converge to the same state.
Meaning that they need to operate as a (distributed) state machine.

MySQL Group Replication provides distributed state machine replication with strong coordination between
servers. Servers coordinate themselves automatically when they are part of the same group. The group
can operate in a single-primary mode with automatic primary election, where only one server accepts
updates at a time. Alternatively, for more advanced users the group can be deployed in multi-primary
mode, where all servers can accept updates, even if they are issued concurrently. This power comes at the
expense of applications having to work around the limitations imposed by such deployments.

3166

Replication Technologies

There is a built-in group membership service that keeps the view of the group consistent and available
for all servers at any given point in time. Servers can leave and join the group and the view is updated
accordingly. Sometimes servers can leave the group unexpectedly, in which case the failure detection
mechanism detects this and notifies the group that the view has changed. This is all automatic.

For a transaction to commit, the majority of the group have to agree on the order of a given transaction
in the global sequence of transactions. Deciding to commit or abort a transaction is done by each server
individually, but all servers make the same decision. If there is a network partition, resulting in a split where
members are unable to reach agreement, then the system does not progress until this issue is resolved.
Hence there is also a built-in, automatic, split-brain protection mechanism.

All of this is powered by the provided Group Communication System (GCS) protocols. These provide a
failure detection mechanism, a group membership service, and safe and completely ordered message
delivery. All these properties are key to creating a system which ensures that data is consistently replicated
across the group of servers. At the very core of this technology lies an implementation of the Paxos
algorithm. It acts as the group communication engine.

17.1.1 Replication Technologies

Before getting into the details of MySQL Group Replication, this section introduces some background
concepts and an overview of how things work. This provides some context to help understand what
is required for Group Replication and what the differences are between classic asynchronous MySQL
Replication and Group Replication.

17.1.1.1 Primary-Secondary Replication

Traditional MySQL Replication provides a simple Primary-Secondary approach to replication. There is a
primary (source) and there are one or more secondaries (replicas). The primary executes transactions,
commits them and then they are later (thus asynchronously) sent to the secondaries to be either re-
executed (in statement-based replication) or applied (in row-based replication). It is a shared-nothing
system, where all servers have a full copy of the data by default.

Figure 17.1 MySQL Asynchronous Replication

There is also semisynchronous replication, which adds one synchronization step to the protocol. This
means that the Primary waits, at commit time, for the secondary to acknowledge that it has received the
transaction. Only then does the Primary resume the commit operation.

3167

Replication Technologies

Figure 17.2 MySQL Semisynchronous Replication

In the two pictures above, you can see a diagram of the classic asynchronous MySQL Replication protocol
(and its semisynchronous variant as well). The arrows between the different instances represent messages
exchanged between servers or messages exchanged between servers and the client application.

17.1.1.2 Group Replication

Group Replication is a technique that can be used to implement fault-tolerant systems. The replication
group is a set of servers that each have their own entire copy of the data (a shared-nothing replication
scheme), and interact with each other through message passing. The communication layer provides a
set of guarantees such as atomic message and total order message delivery. These are very powerful
properties that translate into very useful abstractions that one can resort to build more advanced database
replication solutions.

MySQL Group Replication builds on top of such properties and abstractions and implements a multi-source
update everywhere replication protocol. A replication group is formed by multiple servers and each server
in the group may execute transactions independently at any time. However, all read-write transactions
commit only after they have been approved by the group. In other words, for any read-write transaction
the group needs to decide whether it commits or not, so the commit operation is not a unilateral decision
from the originating server. Read-only transactions need no coordination within the group and commit
immediately.

When a read-write transaction is ready to commit at the originating server, the server atomically broadcasts
the write values (the rows that were changed) and the corresponding write set (the unique identifiers of the
rows that were updated). Because the transaction is sent through an atomic broadcast, either all servers
in the group receive the transaction or none do. If they receive it, then they all receive it in the same order
with respect to other transactions that were sent before. All servers therefore receive the same set of
transactions in the same order, and a global total order is established for the transactions.

However, there may be conflicts between transactions that execute concurrently on different servers.
Such conflicts are detected by inspecting and comparing the write sets of two different and concurrent

3168

Group Replication Use Cases

transactions, in a process called certification. During certification, conflict detection is carried out at row
level: if two concurrent transactions, that executed on different servers, update the same row, then there is
a conflict. The conflict resolution procedure states that the transaction that was ordered first commits on all
servers, and the transaction ordered second aborts, and is therefore rolled back on the originating server
and dropped by the other servers in the group. For example, if t1 and t2 execute concurrently at different
sites, both changing the same row, and t2 is ordered before t1, then t2 wins the conflict and t1 is rolled
back. This is in fact a distributed first commit wins rule. Note that if two transactions are bound to conflict
more often than not, then it is a good practice to start them on the same server, where they have a chance
to synchronize on the local lock manager instead of being rolled back as a result of certification.

For applying and externalizing the certified transactions, Group Replication permits servers to deviate from
the agreed order of the transactions if this does not break consistency and validity. Group Replication is an
eventual consistency system, meaning that as soon as the incoming traffic slows down or stops, all group
members have the same data content. While traffic is flowing, transactions can be externalized in a slightly
different order, or externalized on some members before the others. For example, in multi-primary mode,
a local transaction might be externalized immediately following certification, although a remote transaction
that is earlier in the global order has not yet been applied. This is permitted when the certification process
has established that there is no conflict between the transactions. In single-primary mode, on the primary
server, there is a small chance that concurrent, non-conflicting local transactions might be committed and
externalized in a different order from the global order agreed by Group Replication. On the secondaries,
which do not accept writes from clients, transactions are always committed and externalized in the agreed
order.

The following figure depicts the MySQL Group Replication protocol and by comparing it to MySQL
Replication (or even MySQL semisynchronous replication) you can see some differences. Note that some
underlying consensus and Paxos related messages are missing from this picture for the sake of clarity.

Figure 17.3 MySQL Group Replication Protocol

17.1.2 Group Replication Use Cases

Group Replication enables you to create fault-tolerant systems with redundancy by replicating the system
state to a set of servers. Even if some of the servers subsequently fail, as long it is not all or a majority, the
system is still available. Depending on the number of servers which fail the group might have degraded
performance or scalability, but it is still available. Server failures are isolated and independent. They are

3169

Group Replication Details

tracked by a group membership service which relies on a distributed failure detector that is able to signal
when any servers leave the group, either voluntarily or due to an unexpected halt. There is a distributed
recovery procedure to ensure that when servers join the group they are brought up to date automatically.
There is no need for server fail-over, and the multi-source update everywhere nature ensures that even
updates are not blocked in the event of a single server failure. To summarize, MySQL Group Replication
guarantees that the database service is continuously available.

It is important to understand that although the database service is available, in the event of an unexpected
server exit, those clients connected to it must be redirected, or failed over, to a different server. This is
not something Group Replication attempts to resolve. A connector, load balancer, router, or some form of
middleware are more suitable to deal with this issue. For example see MySQL Router 8.0.

To summarize, MySQL Group Replication provides a highly available, highly elastic, dependable MySQL
service.

17.1.2.1 Examples of Use Case Scenarios

The following examples are typical use cases for Group Replication.

• Elastic Replication - Environments that require a very fluid replication infrastructure, where the number
of servers has to grow or shrink dynamically and with as few side-effects as possible. For instance,
database services for the cloud.

• Highly Available Shards - Sharding is a popular approach to achieve write scale-out. Use MySQL Group

Replication to implement highly available shards, where each shard maps to a replication group.

• Alternative to Source-Replica replication - In certain situations, using a single source server makes
it a single point of contention. Writing to an entire group may prove more scalable under certain
circumstances.

• Autonomic Systems - Additionally, you can deploy MySQL Group Replication purely for the automation

that is built into the replication protocol (described already in this and previous chapters).

17.1.3 Group Replication Details

This section presents details about some of the services that Group Replication builds on.

17.1.3.1 Group Membership

In MySQL Group Replication, a set of servers forms a replication group. A group has a name, which takes
the form of a UUID. The group is dynamic and servers can leave (either voluntarily or involuntarily) and join
it at any time. The group adjusts itself whenever servers join or leave.

If a server joins the group, it automatically brings itself up to date by fetching the missing state from an
existing server. If a server leaves the group, for instance it was taken down for maintenance, the remaining
servers notice that it has left and reconfigure the group automatically.

Group Replication has a group membership service that defines which servers are online and participating
in the group. The list of online servers is referred to as a view. Every server in the group has a consistent
view of which servers are the members participating actively in the group at a given moment in time.

Group members must agree not only on transaction commits, but also on which is the current view. If
existing members agree that a new server should become part of the group, the group is reconfigured to
integrate that server in it, which triggers a view change. If a server leaves the group, either voluntarily or
not, the group dynamically rearranges its configuration and a view change is triggered.

3170

Getting Started

other members agree on it. In that case, the suspect member is marked for expulsion from the group in a
coordinated decision, and is expelled after the expelling mechanism detects and implements the expulsion.

For information on the Group Replication system variables that you can configure to specify the responses
of working group members to failure situations, and the actions taken by group members that are
suspected of having failed, see Responses to Failure Detection and Network Partitioning.

17.1.3.3 Fault-tolerance

MySQL Group Replication builds on an implementation of the Paxos distributed algorithm to provide
distributed coordination between servers. As such, it requires a majority of servers to be active to reach
quorum and thus make a decision. This has direct impact on the number of failures the system can tolerate
without compromising itself and its overall functionality. The number of servers (n) needed to tolerate f
failures is then n = 2 x f + 1.

In practice this means that to tolerate one failure the group must have three servers in it. As such if one
server fails, there are still two servers to form a majority (two out of three) and allow the system to continue
to make decisions automatically and progress. However, if a second server fails involuntarily, then the
group (with one server left) blocks, because there is no majority to reach a decision.

The following is a small table illustrating the formula above.

Group Size

Majority

Instant Failures Tolerated

1

2

3

4

5

6

7

1

2

2

3

3

4

4

0

0

1

1

2

2

3

The next Chapter covers technical aspects of Group Replication.

17.2 Getting Started

MySQL Group Replication is provided as a plugin for the MySQL server; each server in a group requires
configuration and installation of the plugin. This section provides a detailed tutorial with the steps required
to create a replication group with at least three members.

Tip

An alternative way to deploy multiple instances of MySQL is by using InnoDB
Cluster, which uses Group Replication and wraps it in a programmatic environment
that enables you to easily work with groups of MySQL server instances in the
MySQL Shell 8.0. In addition, InnoDB Cluster interfaces seamlessly with MySQL
Router and simplifies deploying MySQL with high availability. See MySQL
AdminAPI.

17.2.1 Deploying Group Replication in Single-Primary Mode

Each of the MySQL server instances in a group can run on an independent physical host machine, which
is the recommended way to deploy Group Replication. This section explains how to create a replication
group with three MySQL Server instances, each running on a different host machine. See Section 17.2.2,

3172

Deploying Group Replication in Single-Primary Mode

transfer transactions from donor members to members that join the group. Therefore you need to set up
a replication user with the correct permissions so that Group Replication can establish direct member-to-
member recovery replication channels.

Start the MySQL server instance and then connect a client to it. Create a MySQL user with the
REPLICATION SLAVE privilege. This process can be captured in the binary log and then you can rely
on distributed recovery to replicate the statements used to create the user. Alternatively, you can disable
binary logging using SET SQL_LOG_BIN=0; and then create the user manually on each member, for
example if you want to avoid the changes being propagated to other server instances. If you do decide to
disable binary logging, ensure you renable it once you have configured the user.

In the following example the user rpl_user with the password password is shown. When configuring
your servers use a suitable user name and password.

mysql> CREATE USER rpl_user@'%' IDENTIFIED BY 'password';
mysql> GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';
mysql> FLUSH PRIVILEGES;

If binary logging was disabled, enable it again once the user has been created using SET
SQL_LOG_BIN=1;.

Once the user has been configured, use the CHANGE MASTER TO statement to configure the server to use
the given credentials for the group_replication_recovery replication channel the next time it needs
to recover its state from another member. Issue the following, replacing rpl_user and password with the
values used when creating the user.

mysql> CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password' \\
        FOR CHANNEL 'group_replication_recovery';

Distributed recovery is the first step taken by a server that joins the group and does not have the
same set of transactions as the group members. If these credentials are not set correctly for the
group_replication_recovery replication channel and the rpl_user as shown, the server cannot
connect to the donor members and run the distributed recovery process to gain synchrony with the other
group members, and hence ultimately cannot join the group. See Section 17.9.5, “Distributed Recovery”.

Similarly, if the server cannot correctly identify the other members via the server's hostname the recovery
process can fail. It is recommended that operating systems running MySQL have a properly configured
unique hostname, either using DNS or local settings. This hostname can be verified in the Member_host
column of the performance_schema.replication_group_members table. If multiple group members
externalize a default hostname set by the operating system, there is a chance of the member not resolving
to the correct member address and not being able to join the group. In such a situation use report_host
to configure a unique hostname to be externalized by each of the servers.

17.2.1.4 Launching Group Replication

It is first necessary to ensure that the Group Replication plugin is installed on server s1. If you used
plugin_load_add='group_replication.so' in the option file then the Group Replication plugin is
already installed, and you can proceed to the next step. Otherwise, you must install the plugin manually; to
do this, connect to the server using the mysql client, and issue the SQL statement shown here:

mysql> INSTALL PLUGIN group_replication SONAME 'group_replication.so';

Important

The mysql.session user must exist before you can load Group Replication.
mysql.session was added in MySQL version 5.7.19. If your data dictionary
was initialized using an earlier version you must perform the MySQL upgrade

3177

Deploying Group Replication in Single-Primary Mode

+----+------+
|  1 | Luis |
+----+------+

mysql> SHOW BINLOG EVENTS;
+---------------+-----+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name      | Pos | Event_type     | Server_id | End_log_pos | Info                                                               |
+---------------+-----+----------------+-----------+-------------+--------------------------------------------------------------------+
| binlog.000001 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.44-log, Binlog ver: 4                              |
| binlog.000001 | 123 | Previous_gtids |         1 |         150 |                                                                    |
| binlog.000001 | 150 | Gtid           |         1 |         211 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:1'  |
| binlog.000001 | 211 | Query          |         1 |         270 | BEGIN                                                              |
| binlog.000001 | 270 | View_change    |         1 |         369 | view_id=14724817264259180:1                                        |
| binlog.000001 | 369 | Query          |         1 |         434 | COMMIT                                                             |
| binlog.000001 | 434 | Gtid           |         1 |         495 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:2'  |
| binlog.000001 | 495 | Query          |         1 |         585 | CREATE DATABASE test                                               |
| binlog.000001 | 585 | Gtid           |         1 |         646 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:3'  |
| binlog.000001 | 646 | Query          |         1 |         770 | use `test`; CREATE TABLE t1 (c1 INT PRIMARY KEY, c2 TEXT NOT NULL) |
| binlog.000001 | 770 | Gtid           |         1 |         831 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:4'  |
| binlog.000001 | 831 | Query          |         1 |         899 | BEGIN                                                              |
| binlog.000001 | 899 | Table_map      |         1 |         942 | table_id: 108 (test.t1)                                            |
| binlog.000001 | 942 | Write_rows     |         1 |         984 | table_id: 108 flags: STMT_END_F                                    |
| binlog.000001 | 984 | Xid            |         1 |        1011 | COMMIT /* xid=38 */                                                |
+---------------+-----+----------------+-----------+-------------+--------------------------------------------------------------------+

As seen above, the database and the table objects were created and their corresponding DDL statements
were written to the binary log. Also, the data was inserted into the table and written to the binary log.
The importance of the binary log entries is illustrated in the following section when the group grows and
distributed recovery is executed as new members try to catch up and become online.

17.2.1.6 Adding Instances to the Group

At this point, the group has one member in it, server s1, which has some data in it. It is now time to expand
the group by adding the other two servers configured previously.

Adding a Second Instance

In order to add a second instance, server s2, first create the configuration file for it. The configuration is
similar to the one used for server s1, except for things such as the server_id.

[mysqld]

#
# Disable other storage engines
#
disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"

#
# Replication configuration parameters
#
server_id=2
gtid_mode=ON
enforce_gtid_consistency=ON
master_info_repository=TABLE
relay_log_info_repository=TABLE
binlog_checksum=NONE
log_slave_updates=ON
log_bin=binlog
binlog_format=ROW

#
# Group Replication configuration
#
transaction_write_set_extraction=XXHASH64

3179

Deploying Group Replication in Single-Primary Mode

group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
group_replication_start_on_boot=off
group_replication_local_address= "s2:33061"
group_replication_group_seeds= "s1:33061,s2:33061,s3:33061"
group_replication_bootstrap_group= off

Similar to the procedure for server s1, with the option file in place you launch the server. Then configure
the recovery credentials as follows. The commands are the same as used when setting up server s1 as
the user is shared within the group. This member needs to have the same replication user configured in
Section 17.2.1.3, “User Credentials”. If you are relying on distributed recovery to configure the user on all
members, when s2 connects to the seed s1 the replication user is relicated to s1. If you did not have binary
logging enabled when you configured the user credentials on s1, you must create the replication user on
s2. In this case, connect to s2 and issue:

SET SQL_LOG_BIN=0;
CREATE USER rpl_user@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';
SET SQL_LOG_BIN=1;
CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password' \\
 FOR CHANNEL 'group_replication_recovery';

If necessary, install the Group Replication plugin, see Section 17.2.1.4, “Launching Group Replication”.

Start Group Replication and s2 starts the process of joining the group.

mysql> START GROUP_REPLICATION;

Unlike the previous steps that were the same as those executed on s1, here there is a difference
in that you do not need to boostrap the group because the group already exiists. In other words on
s2 group_replication_bootstrap_group is set to off, and you do not issue SET GLOBAL
group_replication_bootstrap_group=ON; before starting Group Replication, because the group
has already been created and bootstrapped by server s1. At this point server s2 only needs to be added to
the already existing group.

Tip

When Group Replication starts successfully and the server joins the group it checks
the super_read_only variable. By setting super_read_only to ON in the
member's configuration file, you can ensure that servers which fail when starting
Group Replication for any reason do not accept transactions. If the server should
join the group as read-write instance, for example as the primary in a single-primary
group or as a member of a multi-primary group, when the super_read_only
variable is set to ON then it is set to OFF upon joining the group.

Checking the performance_schema.replication_group_members table again shows that there are
now two ONLINE servers in the group.

mysql> SELECT * FROM performance_schema.replication_group_members;
+---------------------------+--------------------------------------+-------------+-------------+---------------+
| CHANNEL_NAME              | MEMBER_ID                            | MEMBER_HOST | MEMBER_PORT | MEMBER_STATE  |
+---------------------------+--------------------------------------+-------------+-------------+---------------+
| group_replication_applier | 395409e1-6dfa-11e6-970b-00212844f856 |   s1        |        3306 | ONLINE        |
| group_replication_applier | ac39f1e6-6dfa-11e6-a69d-00212844f856 |   s2        |        3306 | ONLINE        |
+---------------------------+--------------------------------------+-------------+-------------+---------------+

When s2 attempted to join the group, Section 17.9.5, “Distributed Recovery” ensured that s2 applied
the same transactions which s1 had applied. Once this process completed, s2 could join the group as a
member, and at this point it is marked as ONLINE. In other words it must have already caught up with
server s1 automatically. Once s2 is ONLINE, it then begins to process transactions with the group. Verify
that s2 has indeed synchronized with server s1 as follows.

3180

Deploying Group Replication in Single-Primary Mode

mysql> SHOW DATABASES LIKE 'test';
+-----------------+
| Database (test) |
+-----------------+
| test            |
+-----------------+

mysql> SELECT * FROM test.t1;
+----+------+
| c1 | c2   |
+----+------+
|  1 | Luis |
+----+------+

mysql> SHOW BINLOG EVENTS;
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name      | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| binlog.000001 |    4 | Format_desc    |         2 |         123 | Server ver: 5.7.44-log, Binlog ver: 4                              |
| binlog.000001 |  123 | Previous_gtids |         2 |         150 |                                                                    |
| binlog.000001 |  150 | Gtid           |         1 |         211 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:1'  |
| binlog.000001 |  211 | Query          |         1 |         270 | BEGIN                                                              |
| binlog.000001 |  270 | View_change    |         1 |         369 | view_id=14724832985483517:1                                        |
| binlog.000001 |  369 | Query          |         1 |         434 | COMMIT                                                             |
| binlog.000001 |  434 | Gtid           |         1 |         495 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:2'  |
| binlog.000001 |  495 | Query          |         1 |         585 | CREATE DATABASE test                                               |
| binlog.000001 |  585 | Gtid           |         1 |         646 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:3'  |
| binlog.000001 |  646 | Query          |         1 |         770 | use `test`; CREATE TABLE t1 (c1 INT PRIMARY KEY, c2 TEXT NOT NULL) |
| binlog.000001 |  770 | Gtid           |         1 |         831 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:4'  |
| binlog.000001 |  831 | Query          |         1 |         890 | BEGIN                                                              |
| binlog.000001 |  890 | Table_map      |         1 |         933 | table_id: 108 (test.t1)                                            |
| binlog.000001 |  933 | Write_rows     |         1 |         975 | table_id: 108 flags: STMT_END_F                                    |
| binlog.000001 |  975 | Xid            |         1 |        1002 | COMMIT /* xid=30 */                                                |
| binlog.000001 | 1002 | Gtid           |         1 |        1063 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:5'  |
| binlog.000001 | 1063 | Query          |         1 |        1122 | BEGIN                                                              |
| binlog.000001 | 1122 | View_change    |         1 |        1261 | view_id=14724832985483517:2                                        |
| binlog.000001 | 1261 | Query          |         1 |        1326 | COMMIT                                                             |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+

As seen above, the second server has been added to the group and it has replicated the changes from
server s1 automatically using distributed recovery. In other words, the transactions applied on s1 up to the
point in time that s2 joined the group have been replicated to s2.

Adding Additional Instances

Adding additional instances to the group is essentially the same sequence of steps as adding the second
server, except that the configuration has to be changed as it had to be for server s2. To summarise the
required commands:

1. Create the configuration file

[mysqld]

#
# Disable other storage engines
#
disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"

#
# Replication configuration parameters
#
server_id=3
gtid_mode=ON
enforce_gtid_consistency=ON
master_info_repository=TABLE

3181

Deploying Group Replication in Single-Primary Mode

relay_log_info_repository=TABLE
binlog_checksum=NONE
log_slave_updates=ON
log_bin=binlog
binlog_format=ROW

#
# Group Replication configuration
#
group_replication_group_name="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
group_replication_start_on_boot=off
group_replication_local_address= "s3:33061"
group_replication_group_seeds= "s1:33061,s2:33061,s3:33061"
group_replication_bootstrap_group= off

2. Start the server and connect to it. Configure the recovery credentials for the group_replication_recovery
channel.

SET SQL_LOG_BIN=0;
CREATE USER rpl_user@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO rpl_user@'%';
FLUSH PRIVILEGES;
SET SQL_LOG_BIN=1;
CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password'  \\
FOR CHANNEL 'group_replication_recovery';

4. Install the Group Replication plugin and start it.

INSTALL PLUGIN group_replication SONAME 'group_replication.so';
START GROUP_REPLICATION;

At this point server s3 is booted and running, has joined the group and caught up with the other servers in
the group. Consulting the performance_schema.replication_group_members table again confirms
this is the case.

mysql> SELECT * FROM performance_schema.replication_group_members;
+---------------------------+--------------------------------------+-------------+-------------+---------------+
| CHANNEL_NAME              | MEMBER_ID                            | MEMBER_HOST | MEMBER_PORT | MEMBER_STATE  |
+---------------------------+--------------------------------------+-------------+-------------+---------------+
| group_replication_applier | 395409e1-6dfa-11e6-970b-00212844f856 |   s1        |       3306  | ONLINE        |
| group_replication_applier | 7eb217ff-6df3-11e6-966c-00212844f856 |   s3        |       3306  | ONLINE        |
| group_replication_applier | ac39f1e6-6dfa-11e6-a69d-00212844f856 |   s2        |       3306  | ONLINE        |
+---------------------------+--------------------------------------+-------------+-------------+---------------+

Issuing this same query on server s2 or server s1 yields the same result. Also, you can verify that server s3
has caught up:

mysql> SHOW DATABASES LIKE 'test';
+-----------------+
| Database (test) |
+-----------------+
| test            |
+-----------------+

mysql> SELECT * FROM test.t1;
+----+------+
| c1 | c2   |
+----+------+
|  1 | Luis |
+----+------+

mysql> SHOW BINLOG EVENTS;
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name      | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+

3182

Deploying Group Replication Locally

| binlog.000001 |    4 | Format_desc    |         3 |         123 | Server ver: 5.7.44-log, Binlog ver: 4                              |
| binlog.000001 |  123 | Previous_gtids |         3 |         150 |                                                                    |
| binlog.000001 |  150 | Gtid           |         1 |         211 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:1'  |
| binlog.000001 |  211 | Query          |         1 |         270 | BEGIN                                                              |
| binlog.000001 |  270 | View_change    |         1 |         369 | view_id=14724832985483517:1                                        |
| binlog.000001 |  369 | Query          |         1 |         434 | COMMIT                                                             |
| binlog.000001 |  434 | Gtid           |         1 |         495 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:2'  |
| binlog.000001 |  495 | Query          |         1 |         585 | CREATE DATABASE test                                               |
| binlog.000001 |  585 | Gtid           |         1 |         646 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:3'  |
| binlog.000001 |  646 | Query          |         1 |         770 | use `test`; CREATE TABLE t1 (c1 INT PRIMARY KEY, c2 TEXT NOT NULL) |
| binlog.000001 |  770 | Gtid           |         1 |         831 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:4'  |
| binlog.000001 |  831 | Query          |         1 |         890 | BEGIN                                                              |
| binlog.000001 |  890 | Table_map      |         1 |         933 | table_id: 108 (test.t1)                                            |
| binlog.000001 |  933 | Write_rows     |         1 |         975 | table_id: 108 flags: STMT_END_F                                    |
| binlog.000001 |  975 | Xid            |         1 |        1002 | COMMIT /* xid=29 */                                                |
| binlog.000001 | 1002 | Gtid           |         1 |        1063 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:5'  |
| binlog.000001 | 1063 | Query          |         1 |        1122 | BEGIN                                                              |
| binlog.000001 | 1122 | View_change    |         1 |        1261 | view_id=14724832985483517:2                                        |
| binlog.000001 | 1261 | Query          |         1 |        1326 | COMMIT                                                             |
| binlog.000001 | 1326 | Gtid           |         1 |        1387 | SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:6'  |
| binlog.000001 | 1387 | Query          |         1 |        1446 | BEGIN                                                              |
| binlog.000001 | 1446 | View_change    |         1 |        1585 | view_id=14724832985483517:3                                        |
| binlog.000001 | 1585 | Query          |         1 |        1650 | COMMIT                                                             |
+---------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+

17.2.2 Deploying Group Replication Locally

The most common way to deploy Group Replication is using multiple server instances, to provide high
availability. It is also possible to deploy Group Replication locally, for example for testing purposes. This
section explains how you can deploy Group Replication locally.

Important

Group Replication is usually deployed on multiple hosts because this ensures that
high-availability is provided. The instructions in this section are not suitable for
production deployments because all MySQL server instances are running on the
same single host. In the event of failure of this host, the whole group fails. Therefore
this information should be used for testing purposes and it should not be used in a
production environments.

This section explains how to create a replication group with three MySQL Server instances on one physical
machine. This means that three data directories are needed, one per server instance, and that you need
to configure each instance independently. This - procedure assumes that MySQL Server was downloaded
and unpacked - into the directory named mysql-5.7. Each MySQL server instance requires a specific
data directory. Create a directory named data, then in that directory create a subdirectory for each server
instance, for example s1, s2 and s3, and initialize each one.

mysql-5.7/bin/mysqld --initialize-insecure --basedir=$PWD/mysql-5.7 --datadir=$PWD/data/s1
mysql-5.7/bin/mysqld --initialize-insecure --basedir=$PWD/mysql-5.7 --datadir=$PWD/data/s2
mysql-5.7/bin/mysqld --initialize-insecure --basedir=$PWD/mysql-5.7 --datadir=$PWD/data/s3

Inside data/s1, data/s2, data/s3 is an initialized data directory, containing the mysql system database
and related tables and much more. To learn more about the initialization procedure, see Section 2.9.1,
“Initializing the Data Directory”.

Warning

Do not use -initialize-insecure in production environments, it is only
used here to simplify the tutorial. For more information on security settings, see
Section 17.6, “Group Replication Security”.

3183

Requirements and Limitations

Configuration of Local Group Replication Members

When you are following Section 17.2.1.2, “Configuring an Instance for Group Replication”, you need to add
configuration for the data directories added in the previous section. For example:

[mysqld]

# server configuration
datadir=<full_path_to_data>/data/s1
basedir=<full_path_to_bin>/mysql-8.0/

port=24801
socket=<full_path_to_sock_dir>/s1.sock

These settings configure MySQL server to use the data directory created earlier and which port the server
should open and start listening for incoming connections.

Note

The non-default port of 24801 is used because in this tutorial the three server
instances use the same hostname. In a setup with three different machines this
would not be required.

Group Replication requires a network connection between the members, which means that each member
must be able to resolve the network address of all of the other members. For example in this tutorial all
three instances run on one machine, so to ensure that the members can contact each other you could add
a line to the option file such as report_host=127.0.0.1.

Then each member needs to be able to connect to the other members on their
group_replication_local_address. For example in the option file of member s1 add:

group_replication_local_address= "127.0.0.1:24901"
group_replication_group_seeds= "127.0.0.1:24901,127.0.0.1:24902,127.0.0.1:24903"

This configures s1 to use port 24901 for internal group communication with seed members. For each
server instance you want to add to the group, make these changes in the option file of the member.
For each member you must ensure a unique address is specified, so use a unique port per instance for
group_replication_local_address. Usually you want all members to be able to serve as seeds for
members that are joining the group and have not got the transactions processed by the group. In this case,
add all of the ports to group_replication_group_seeds as shown above.

The remaining steps of Section 17.2.1, “Deploying Group Replication in Single-Primary Mode” apply
equally to a group which you have deployed locally in this way.

17.3 Requirements and Limitations

This section lists and explains the requirements and limitations of Group Replication.

17.3.1 Group Replication Requirements

Server instances that you want to use for Group Replication must satisfy the following requirements.

Infrastructure

• InnoDB Storage Engine.

 Data must be stored in the InnoDB transactional storage engine.

Transactions are executed optimistically and then, at commit time, are checked for conflicts. If there
are conflicts, in order to maintain consistency across the group, some transactions are rolled back. This

3184

Group Replication Limitations

Note

For a group in multi-primary mode, unless you rely on REPEATABLE READ
semantics in your applications, we recommend using the READ COMMITTED
isolation level with Group Replication. InnoDB does not use gap locks in READ
COMMITTED, which aligns the local conflict detection within InnoDB with the
distributed conflict detection performed by Group Replication. For a group in
single-primary mode, only the primary accepts writes, so the READ COMMITTED
isolation level is not important to Group Replication.

• Table Locks and Named Locks.

 The certification process does not take into account table locks

(see Section 13.3.5, “LOCK TABLES and UNLOCK TABLES Statements”) or named locks (see
GET_LOCK()).

• Replication Event Checksums.

 Due to a design limitation of replication event checksums, Group

Replication cannot currently make use of them. Therefore set --binlog-checksum=NONE.

• SERIALIZABLE Isolation Level.

 SERIALIZABLE isolation level is not supported in multi-primary

groups by default. Setting a transaction isolation level to SERIALIZABLE configures Group Replication
to refuse to commit the transaction.

• Concurrent DDL versus DML Operations.

 Concurrent data definition statements and data

manipulation statements executing against the same object but on different servers is not supported
when using multi-primary mode. During execution of Data Definition Language (DDL) statements on an
object, executing concurrent Data Manipulation Language (DML) on the same object but on a different
server instance has the risk of conflicting DDL executing on different instances not being detected.

• Foreign Keys with Cascading Constraints.

 Multi-primary mode groups (members all

configured with group_replication_single_primary_mode=OFF) do not support tables
with multi-level foreign key dependencies, specifically tables that have defined CASCADING
foreign key constraints. This is because foreign key constraints that result in cascading
operations executed by a multi-primary mode group can result in undetected conflicts and
lead to inconsistent data across the members of the group. Therefore we recommend setting
group_replication_enforce_update_everywhere_checks=ON on server instances used in
multi-primary mode groups to avoid undetected conflicts.

In single-primary mode this is not a problem as it does not allow concurrent writes to multiple members
of the group and thus there is no risk of undetected conflicts.

• MySQL Enterprise Audit and MySQL Enterprise Firewall.

 Prior to version 5.7.21 MySQL

Enterprise Audit and MySQL Enterprise Firewall use MyISAM tables in the mysql system database.
Group Replication does not support MyISAM tables.

• Multi-primary Mode Deadlock.

 When a group is operating in multi-primary mode, SELECT .. FOR
UPDATE statements can result in a deadlock. This is because the lock is not shared across the members
of the group, therefore the expectation for such a statement might not be reached.

• Replication Filters.

 Replication filters cannot be used on a MySQL server instance that is configured

for Group Replication, because filtering transactions on some servers would make the group unable to
reach agreement on a consistent state.

Limit on Group Size

The maximum number of MySQL servers that can be members of a single replication group is 9. If further
members attempt to join the group, their request is refused. This limit has been identified from testing and
benchmarking as a safe boundary where the group performs reliably on a stable local area network.

3187

Monitoring Group Replication

Limits on Transaction Size

If an individual transaction results in message contents which are large enough that the message cannot
be copied between group members over the network within a 5-second window, members can be
suspected of having failed, and then expelled, just because they are busy processing the transaction.
Large transactions can also cause the system to slow due to problems with memory allocation. To avoid
these issues use the following mitigations:

• Where possible, try and limit the size of your transactions. For example, split up files used with LOAD

DATA into smaller chunks.

• Use the system variable group_replication_transaction_size_limit to specify the maximum

transaction size that the group accepts. In releases up to and including MySQL 5.7.37, this system
variable defaults to zero, but from MySQL 5.7.38, and in MySQL 8.0, it defaults to a maximum
transaction size of 150000000 bytes (approximately 143 MB). Transactions above this limit are rolled
back and are not sent to Group Replication's Group Communication System (GCS) for distribution to
the group. Adjust the value of this variable depending on the maximum message size that you need the
group to tolerate, bearing in mind that the time taken to process a transaction is proportional to its size.

Note

When you upgrade from MySQL 5.7.37 or earlier to MySQL 5.7.38
or later, if your Group Replication servers previously accepted
transactions larger than the new default limit, and you were allowing
group_replication_transaction_size_limit to default to the old zero
limit, those transactions will start to fail after the upgrade to the new default. You
must either specify an appropriate size limit that allows the maximum message
size you need the group to tolerate (which is the recommended solution), or
specify a zero setting to restore the previous behavior.

• Use the system variable group_replication_compression_threshold to specify a

message size above which compression is applied. This system variable defaults to 1000000
bytes (1 MB), so large messages are automatically compressed. Compression is carried out by
Group Replication's Group Communication System (GCS) when it receives a message that was
permitted by the group_replication_transaction_size_limit setting but exceeds the
group_replication_compression_threshold setting. If you set the system variable value to
zero, compression is deactivated. For more information, see Section 17.9.7.2, “Message Compression”.

If you have deactivated message compression and do not specify a maximum transaction size, the upper
size limit for a message that can be handled by the applier thread on a member of a replication group
is the value of the member's slave_max_allowed_packet system variable, which has a default and
maximum value of 1073741824 bytes (1 GB). A message that exceeds this limit fails when the receiving
member attempts to handle it. The upper size limit for a message that a group member can originate and
attempt to transmit to the group is 4294967295 bytes (approximately 4 GB). This is a hard limit on the
packet size that is accepted by the group communication engine for Group Replication (XCom, a Paxos
variant), which receives messages after GCS has handled them. A message that exceeds this limit fails
when the originating member attempts to broadcast it.

17.4 Monitoring Group Replication

You can use the MySQL Performance Schema to monitor Group Replication. These Performance Schema
tables display information specific to Group Replication:

• replication_group_member_stats: See Section 17.4.3, “The replication_group_member_stats

Table”.

3188

Group Replication Server States

• replication_group_members: See Section 17.4.2, “The replication_group_members Table”.

These Performance Schema replication tables also show information relating to Group Replication:

• replication_connection_status shows information regarding Group Replication, such as

transactions received from the group and queued in the applier queue (relay log).

• replication_applier_status shows the states of channels and threads relating to Group

Replication. These can also be used to monitor what individual worker threads are doing.

Replication channels created by the Group Replication plugin are listed here:

• group_replication_recovery: Used for replication changes related to distributed recovery.

• group_replication_applier: Used for the incoming changes from the group, to apply transactions

coming directly from the group.

For information about system variables affecting Group Replication, see Section 17.7.1, “Group Replication
System Variables”. See Section 17.7.2, “Group Replication Status Variables”, for status variables providing
information about Group Replication.

Note

If you are monitoring one or more secondary instances using mysqladmin, you
should be aware that a FLUSH STATUS statement executed by this utility creates a
GTID event on the local instance which may impact future group operations.

17.4.1 Group Replication Server States

There are various states that a server instance can be in. If servers are communicating properly, all report
the same states for all servers. However, if there is a network partition, or a server leaves the group,
then different information could be reported, depending on which server is queried. If the server has left
the group then it cannot report updated information about the other servers' states. If there is a partition,
such that quorum is lost, servers are not able to coordinate between themselves. As a consequence, they
cannot guess what the status of different servers is. Therefore, instead of guessing their state they report
that some servers are unreachable.

Table 17.1 Server State

Field

ONLINE

RECOVERING

OFFLINE

Description

Group Synchronized

The member is ready to serve as
a fully functional group member,
meaning that the client can
connect and start executing
transactions.

The member is in the process of
becoming an active member of
the group and is currently going
through the recovery process,
receiving state information from a
donor.

The plugin is loaded but the
member does not belong to any
group.

Yes

No

No

3189

Field

ERROR

UNREACHABLE

The replication_group_members Table

Description

Group Synchronized

No

No

The state of the member.
Whenever there is an error on the
recovery phase or while applying
changes, the server enters this
state.

Whenever the local failure
detector suspects that a given
server is not reachable, because
for example it was disconnected
involuntarily, it shows that server's
state as UNREACHABLE.

Important

Once an instance enters ERROR state, the super_read_only option is set to
ON. To leave the ERROR state you must manually configure the instance with
super_read_only=OFF.

Note that Group Replication is not synchronous, but eventually synchronous. More precisely, transactions
are delivered to all group members in the same order, but their execution is not synchronized, meaning
that after a transaction is accepted to be committed, each member commits at its own pace.

17.4.2 The replication_group_members Table

The performance_schema.replication_group_members table is used for monitoring the status
of the different server instances that are members of the group. The information in the table is updated
whenever there is a view change, for example when the configuration of the group is dynamically changed
when a new member joins. At that point, servers exchange some of their metadata to synchronize
themselves and continue to cooperate together. The information is shared between all the server instances
that are members of the replication group, so information on all the group members can be queried from
any member. This table can be used to get a high level view of the state of a replication group, for example
by issuing:

SELECT * FROM performance_schema.replication_group_members;
+---------------------------+--------------------------------------+--------------+-------------+--------------+
| CHANNEL_NAME              | MEMBER_ID                            | MEMBER_HOST  | MEMBER_PORT | MEMBER_STATE |
+---------------------------+--------------------------------------+--------------+-------------+--------------+
| group_replication_applier | 041f26d8-f3f3-11e8-adff-080027337932 | example1     |      3306   | ONLINE       |
| group_replication_applier | f60a3e10-f3f2-11e8-8258-080027337932 | example2     |      3306   | ONLINE       |
| group_replication_applier | fc890014-f3f2-11e8-a9fd-080027337932 | example3     |      3306   | ONLINE       |
+---------------------------+--------------------------------------+--------------+-------------+--------------+

Based on this result we can see that the group consists of three members, each member's host and
port number which clients use to connect to the member, and the server_uuid of the member. The
MEMBER_STATE column shows one of the Section 17.4.1, “Group Replication Server States”, in this case
it shows that all three members in this group are ONLINE, and the MEMBER_ROLE column shows that
there are two secondaries, and a single primary. Therefore this group must be running in single-primary
mode. The MEMBER_VERSION column can be useful when you are upgrading a group and are combining
members running different MySQL versions. See Section 17.4.1, “Group Replication Server States” for
more information.

For more information about the Member_host value and its impact on the distributed recovery process,
see Section 17.2.1.3, “User Credentials”.

17.4.3 The replication_group_member_stats Table

3190

Group Replication Operations

Each member in a replication group certifies and applies transactions received by the group. Statistics
regarding the certifier and applier procedures are useful to understand how the applier queue is growing,
how many conflicts have been found, how many transactions were checked, which transactions are
committed everywhere, and so on.

The performance_schema.replication_group_member_stats table provides group-level
information related to the certification process, and also statistics for the transactions received and
originated by each individual member of the replication group. The information is shared between all the
server instances that are members of the replication group, so information on all the group members can
be queried from any member. Note that refreshing of statistics for remote members is controlled by the
message period specified in the group_replication_flow_control_period option, so these can
differ slightly from the locally collected statistics for the member where the query is made. To use this table
to monitor a Group Replication member, issue the following statement:

mysql> SELECT * FROM performance_schema.replication_group_member_stats\G

These columns are important for monitoring the performance of the members connected in the group.
Suppose that one of the group's members always reports a large number of transactions in its queue
compared to other members. This means that the member is delayed and is not able to keep up to date
with the other members of the group. Based on this information, you could decide to either remove the
member from the group, or delay the processing of transactions on the other members of the group in
order to reduce the number of queued transactions. This information can also help you to decide how to
adjust the flow control of the Group Replication plugin, see Section 17.9.7.3, “Flow Control”.

17.5 Group Replication Operations

This section describes the different modes of deploying Group Replication, explains common operations
for managing groups and provides information about how to tune your groups. .

17.5.1 Deploying in Multi-Primary or Single-Primary Mode

Group Replication operates in the following different modes:

• single-primary mode

• multi-primary mode

The default mode is single-primary. It is not possible to have members of the group deployed in different
modes, for example one configured in multi-primary mode while another one is in single-primary mode.
To switch between modes, the group and not the server, needs to be restarted with a different operating
configuration. Regardless of the deployed mode, Group Replication does not handle client-side fail-over,
that must be handled by the application itself, a connector or a middleware framework such as a proxy or
MySQL Router 8.0.

When deployed in multi-primary mode, statements are checked to ensure they are compatible with the
mode. The following checks are made when Group Replication is deployed in multi-primary mode:

• If a transaction is executed under the SERIALIZABLE isolation level, then its commit fails when

synchronizing itself with the group.

• If a transaction executes against a table that has foreign keys with cascading constraints, then the

transaction fails to commit when synchronizing itself with the group.

These checks can be deactivated by setting the option
group_replication_enforce_update_everywhere_checks to FALSE. When deploying in single-
primary mode, this option must be set to FALSE.

3191

Deploying in Multi-Primary or Single-Primary Mode

17.5.1.1 Single-Primary Mode

In this mode the group has a single-primary server that is set to read-write mode. All the other members
in the group are set to read-only mode (with super-read-only=ON ). This happens automatically. The
primary is typically the first server to bootstrap the group, all other servers that join automatically learn
about the primary server and are set to read only.

Figure 17.5 New Primary Election

When in single-primary mode, some of the checks deployed in multi-primary mode are disabled,
because the system enforces that only a single server writes to the group. For example, changes to
tables that have cascading foreign keys are allowed, whereas in multi-primary mode they are not.
Upon primary member failure, an automatic primary election mechanism chooses the new primary
member. The election process is performed by looking at the new view, and ordering the potential new
primaries based on the value of group_replication_member_weight. Assuming the group is
operating with all members running the same MySQL version, then the member with the highest value for
group_replication_member_weight is elected as the new primary. In the event that multiple servers
have the same group_replication_member_weight, the servers are then prioritized based on their
server_uuid in lexicographical order and by picking the first one. Once a new primary is elected, it is
automatically set to read-write and the other secondaries remain as secondaries, and as such, read-only.

When a new primary is elected, it is only writable once it has processed all of the transactions that came
from the old primary. This avoids possible concurrency issues between old transactions from the old
primary and the new ones being executed on this member. It is a good practice to wait for the new primary
to apply its replication related relay-log before re-routing client applications to it.

If the group is operating with members that are running different versions of MySQL then
the election process can be impacted. For example, if any member does not support
group_replication_member_weight, then the primary is chosen based on server_uuid order
from the members of the lower major version. Alternatively, if all members running different MySQL
versions do support group_replication_member_weight, the primary is chosen based on
group_replication_member_weight from the members of the lower major version.

17.5.1.2 Multi-Primary Mode

In multi-primary mode, there is no notion of a single primary. There is no need to engage an election
procedure because there is no server playing any special role.

3192

Tuning Recovery

Figure 17.6 Client Failover

All servers are set to read-write mode when joining the group.

17.5.1.3 Finding the Primary

The following example shows how to find out which server is currently the primary when deployed in
single-primary mode.

mysql> SHOW STATUS LIKE 'group_replication_primary_member';

17.5.2 Tuning Recovery

Whenever a new member joins a replication group, it connects to a suitable donor and fetches the data
that it has missed up until the point it is declared online. This critical component in Group Replication is
fault tolerant and configurable. The following section explains how recovery works and how to tune the
settings

Donor Selection

A random donor is selected from the existing online members in the group. This way there is a good
chance that the same server is not selected more than once when multiple members enter the group.

If the connection to the selected donor fails, a new connection is automatically attempted to a new
candidate donor. Once the connection retry limit is reached the recovery procedure terminates with an
error.

Note

A donor is picked randomly from the list of online members in the current view.

Enhanced Automatic Donor Switchover

The other main point of concern in recovery as a whole is to make sure that it copes with failures. Hence,
Group Replication provides robust error detection mechanisms. In earlier versions of Group Replication,
when reaching out to a donor, recovery could only detect connection errors due to authentication issues or
some other problem. The reaction to such problematic scenarios was to switch over to a new donor thus a
new connection attempt was made to a different member.

3193

Network Partitioning

This behavior was extended to also cover other failure scenarios:

• Purged data scenarios - If the selected donor contains some purged data that is needed for the recovery

process then an error occurs. Recovery detects this error and a new donor is selected.

• Duplicated data - If a server joining the group already contains some data that conflicts with the data
coming from the selected donor during recovery then an error occurs. This could be caused by some
errant transactions present in the server joining the group.

One could argue that recovery should fail instead of switching over to another donor, but in
heterogeneous groups there is chance that other members share the conflicting transactions and others
do not. For that reason, upon error, recovery selects another donor from the group.

• Other errors - If any of the recovery threads fail (receiver or applier threads fail) then an error occurs and

recovery switches over to a new donor.

Note

In case of some persistent failures or even transient failures recovery automatically
retries connecting to the same or a new donor.

Donor Connection Retries

The recovery data transfer relies on the binary log and existing MySQL replication framework, therefore it
is possible that some transient errors could cause errors in the receiver or applier threads. In such cases,
the donor switch over process has retry functionality, similar to that found in regular replication.

Number of Attempts

The number of attempts a server joining the group makes when trying to connect to a donor from the pool
of donors is 10. This is configured through the group_replication_recovery_retry_count plugin
variable . The following command sets the maximum number of attempts to connect to a donor to 10.

mysql> SET GLOBAL group_replication_recovery_retry_count= 10;

Note that this accounts for the global number of attempts that the server joining the group makes
connecting to each one of the suitable donors.

Sleep Routines

The group_replication_recovery_reconnect_interval plugin variable defines how much time
the recovery process should sleep between donor connection attempts. This variable has its default set to
60 seconds and you can change this value dynamically. The following command sets the recovery donor
connection retry interval to 120 seconds.

mysql> SET GLOBAL group_replication_recovery_reconnect_interval= 120;

Note, however, that recovery does not sleep after every donor connection attempt. As the server joining
the group is connecting to different servers and not to the same one over and over again, it can assume
that the problem that affects server A does not affect server B. As such, recovery suspends only when it
has gone through all the possible donors. Once the server joining the group has tried to connect to all the
suitable donors in the group and none remains, the recovery process sleeps for the number of seconds
configured by the group_replication_recovery_reconnect_interval variable.

17.5.3 Network Partitioning

3194

Network Partitioning

The group needs to achieve consensus whenever a change that needs to be replicated happens. This is
the case for regular transactions but is also required for group membership changes and some internal
messaging that keeps the group consistent. Consensus requires a majority of group members to agree on
a given decision. When a majority of group members is lost, the group is unable to progress and blocks
because it cannot secure majority or quorum.

Quorum may be lost when there are multiple involuntary failures, causing a majority of servers to be
removed abruptly from the group. For example, in a group of 5 servers, if 3 of them become silent at once,
the majority is compromised and thus no quorum can be achieved. In fact, the remaining two are not able
to tell if the other 3 servers have crashed or whether a network partition has isolated these 2 alone and
therefore the group cannot be reconfigured automatically.

On the other hand, if servers exit the group voluntarily, they instruct the group that it should reconfigure
itself. In practice, this means that a server that is leaving tells others that it is going away. This means that
other members can reconfigure the group properly, the consistency of the membership is maintained and
the majority is recalculated. For example, in the above scenario of 5 servers where 3 leave at once, if the
3 leaving servers warn the group that they are leaving, one by one, then the membership is able to adjust
itself from 5 to 2, and at the same time, securing quorum while that happens.

Note

Loss of quorum is by itself a side-effect of bad planning. Plan the group size for the
number of expected failures (regardless whether they are consecutive, happen all
at once or are sporadic).

The following sections explain what to do if the system partitions in such a way that no quorum is
automatically achieved by the servers in the group.

Tip

A primary that has been excluded from a group after a majority loss followed by
a reconfiguration can contain extra transactions that are not included in the new
group. If this happens, the attempt to add back the excluded member from the
group results in an error with the message This member has more executed
transactions than those present in the group.

Detecting Partitions

The replication_group_members performance schema table presents the status of each server in
the current view from the perspective of this server. The majority of the time the system does not run into
partitioning, and therefore the table shows information that is consistent across all servers in the group. In
other words, the status of each server on this table is agreed by all in the current view. However, if there is
network partitioning, and quorum is lost, then the table shows the status UNREACHABLE for those servers
that it cannot contact. This information is exported by the local failure detector built into Group Replication.

3195

Network Partitioning

Figure 17.7 Losing Quorum

To understand this type of network partition the following section describes a scenario where there are
initially 5 servers working together correctly, and the changes that then happen to the group once only 2
servers are online. The scenario is depicted in the figure.

As such, lets assume that there is a group with these 5 servers in it:

• Server s1 with member identifier 199b2df7-4aaf-11e6-bb16-28b2bd168d07

• Server s2 with member identifier 199bb88e-4aaf-11e6-babe-28b2bd168d07

• Server s3 with member identifier 1999b9fb-4aaf-11e6-bb54-28b2bd168d07

• Server s4 with member identifier 19ab72fc-4aaf-11e6-bb51-28b2bd168d07

3196

Network Partitioning

• Server s5 with member identifier 19b33846-4aaf-11e6-ba81-28b2bd168d07

Initially the group is running fine and the servers are happily communicating with each other. You can verify
this by logging into s1 and looking at its replication_group_members performance schema table. For
example:

mysql> SELECT MEMBER_ID,MEMBER_STATE, MEMBER_ROLE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+-------------+
| MEMBER_ID                            | MEMBER_STATE |-MEMBER_ROLE |
+--------------------------------------+--------------+-------------+
| 1999b9fb-4aaf-11e6-bb54-28b2bd168d07 | ONLINE       | SECONDARY   |
| 199b2df7-4aaf-11e6-bb16-28b2bd168d07 | ONLINE       | PRIMARY     |
| 199bb88e-4aaf-11e6-babe-28b2bd168d07 | ONLINE       | SECONDARY   |
| 19ab72fc-4aaf-11e6-bb51-28b2bd168d07 | ONLINE       | SECONDARY   |
| 19b33846-4aaf-11e6-ba81-28b2bd168d07 | ONLINE       | SECONDARY   |
+--------------------------------------+--------------+-------------+

However, moments later there is a catastrophic failure and servers s3, s4 and s5 stop unexpectedly. A few
seconds after this, looking again at the replication_group_members table on s1 shows that it is still
online, but several others members are not. In fact, as seen below they are marked as UNREACHABLE.
Moreover, the system could not reconfigure itself to change the membership, because the majority has
been lost.

mysql> SELECT MEMBER_ID,MEMBER_STATE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID                            | MEMBER_STATE |
+--------------------------------------+--------------+
| 1999b9fb-4aaf-11e6-bb54-28b2bd168d07 | UNREACHABLE  |
| 199b2df7-4aaf-11e6-bb16-28b2bd168d07 | ONLINE       |
| 199bb88e-4aaf-11e6-babe-28b2bd168d07 | ONLINE       |
| 19ab72fc-4aaf-11e6-bb51-28b2bd168d07 | UNREACHABLE  |
| 19b33846-4aaf-11e6-ba81-28b2bd168d07 | UNREACHABLE  |
+--------------------------------------+--------------+

The table shows that s1 is now in a group that has no means of progressing without external intervention,
because a majority of the servers are unreachable. In this particular case, the group membership list needs
to be reset to allow the system to proceed, which is explained in this section. Alternatively, you could also
choose to stop Group Replication on s1 and s2 (or stop completely s1 and s2), figure out what happened
with s3, s4 and s5 and then restart Group Replication (or the servers).

Unblocking a Partition

Group replication enables you to reset the group membership list by forcing a specific configuration.
For instance in the case above, where s1 and s2 are the only servers online, you could chose to force a
membership configuration consisting of only s1 and s2. This requires checking some information about s1
and s2 and then using the group_replication_force_members variable.

3197

Network Partitioning

Figure 17.8 Forcing a New Membership

Suppose that you are back in the situation where s1 and s2 are the only servers left in the group. Servers
s3, s4 and s5 have left the group unexpectedly. To make servers s1 and s2 continue, you want to force a
membership configuration that contains only s1 and s2.

Warning

This procedure uses group_replication_force_members and should be
considered a last resort remedy. It must be used with extreme care and only for
overriding loss of quorum. If misused, it could create an artificial split-brain scenario
or block the entire system altogether.

3198

Restarting a Group

Recall that the system is blocked and the current configuration is the following (as perceived by the local
failure detector on s1):

mysql> SELECT MEMBER_ID,MEMBER_STATE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID                            | MEMBER_STATE |
+--------------------------------------+--------------+
| 1999b9fb-4aaf-11e6-bb54-28b2bd168d07 | UNREACHABLE  |
| 199b2df7-4aaf-11e6-bb16-28b2bd168d07 | ONLINE       |
| 199bb88e-4aaf-11e6-babe-28b2bd168d07 | ONLINE       |
| 19ab72fc-4aaf-11e6-bb51-28b2bd168d07 | UNREACHABLE  |
| 19b33846-4aaf-11e6-ba81-28b2bd168d07 | UNREACHABLE  |
+--------------------------------------+--------------+

The first thing to do is to check what is the local address (group communication identifier) for s1 and s2.
Log in to s1 and s2 and get that information as follows.

mysql> SELECT @@group_replication_local_address;

Once you know the group communication addresses of s1 (127.0.0.1:10000) and s2
(127.0.0.1:10001), you can use that on one of the two servers to inject a new membership
configuration, thus overriding the existing one that has lost quorum. To do that on s1:

mysql> SET GLOBAL group_replication_force_members="127.0.0.1:10000,127.0.0.1:10001";

This unblocks the group by forcing a different configuration. Check replication_group_members on
both s1 and s2 to verify the group membership after this change. First on s1.

mysql> SELECT MEMBER_ID,MEMBER_STATE FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID                            | MEMBER_STATE |
+--------------------------------------+--------------+
| b5ffe505-4ab6-11e6-b04b-28b2bd168d07 | ONLINE       |
| b60907e7-4ab6-11e6-afb7-28b2bd168d07 | ONLINE       |
+--------------------------------------+--------------+

And then on s2.

mysql> SELECT * FROM performance_schema.replication_group_members;
+--------------------------------------+--------------+
| MEMBER_ID                            | MEMBER_STATE |
+--------------------------------------+--------------+
| b5ffe505-4ab6-11e6-b04b-28b2bd168d07 | ONLINE       |
| b60907e7-4ab6-11e6-afb7-28b2bd168d07 | ONLINE       |
+--------------------------------------+--------------+

When forcing a new membership configuration, make sure that any servers are going to be forced out of
the group are indeed stopped. In the scenario depicted above, if s3, s4 and s5 are not really unreachable
but instead are online, they may have formed their own functional partition (they are 3 out of 5, hence they
have the majority). In that case, forcing a group membership list with s1 and s2 could create an artificial
split-brain situation. Therefore it is important before forcing a new membership configuration to ensure that
the servers to be excluded are indeed shutdown and if they are not, shut them down before proceeding.

After you have used the group_replication_force_members system variable to successfully
force a new group membership and unblock the group, ensure that you clear the system
variable. group_replication_force_members must be empty in order to issue a START
GROUP_REPLICATION statement.

17.5.4 Restarting a Group

Group Replication is designed to ensure that the database service is continuously available, even if some
of the servers that form the group are currently unable to participate in it due to planned maintenance or

3199

Using MySQL Enterprise Backup with Group Replication

Using MySQL Enterprise Backup, create a backup of s2 by issuing on its host, for example, the following
command:

s2> mysqlbackup --defaults-file=/etc/my.cnf --backup-image=/backups/my.mbi_`date +%d%m_%H%M` \
        --backup-dir=/backups/backup_`date +%d%m_%H%M` --user=root -p \
        --host=127.0.0.1 backup-to-image

Note

• When backing up a secondary member, as MySQL Enterprise Backup cannot
write backup status and metadata to a read-only server instance, it might issue
warnings similar to the following one during the backup operation:

181113 21:31:08 MAIN WARNING: This backup operation cannot write to backup
progress. The MySQL server is running with the --super-read-only option.

You can avoid the warning by using the --no-history-logging option with
your backup command.

Restoring a Failed Member

Assume one of the members (s3 in the following example) is irreconcilably corrupted. The most recent
backup of group member s2 can be used to restore s3. Here are the steps for performing the restore:

1. Copy the backup of s2 onto the host for s3. The exact way to copy the backup depends on the

operating system and tools available to you. In this example, we assume the hosts are both Linux
servers and use SCP to copy the files between them:

s2/backups> scp my.mbi_2206_1429 s3:/backups

2. Restore the backup. Connect to the target host (the host for s3 in this case), and restore the backup

using MySQL Enterprise Backup. Here are the steps:

a. Stop the corrupted server, if it is still running. For example, on Linux distributions that use systemd:

s3> systemctl stop mysqld

b. Preserve the configuration file auto.cnf, located in the corrupted server's data directory, by

copying it to a safe location outside of the data directory. This is for preserving the server's UUID,
which is needed later.

c. Delete all contents in the data directory of s3. For example:

s3> rm -rf /var/lib/mysql/*

If the system variables innodb_data_home_dir, innodb_log_group_home_dir, and
innodb_undo_directory point to any directories other than the data directory, they should also
be made empty; otherwise, the restore operation fails.

d. Restore backup of s2 onto the host for s3:

s3> mysqlbackup --defaults-file=/etc/my.cnf \
  --datadir=/var/lib/mysql \
  --backup-image=/backups/my.mbi_2206_1429  \
  --backup-dir=/tmp/restore_`date +%d%m_%H%M` copy-back-and-apply-log

Note

The command above assumes that the binary logs and relay logs on s2
and s3 have the same base name and are at the same location on the two

3202

Using MySQL Enterprise Backup with Group Replication

servers. If these conditions are not met, for MySQL Enterprise Backup 4.1.2
and later, you should use the --log-bin and --relay-log options to
restore the binary log and relay log to their original file paths on s3. For
example, if you know that on s3 the binary log's base name is s3-bin and
the relay-log's base name is s3-relay-bin, your restore command should
look like:

mysqlbackup --defaults-file=/etc/my.cnf \
  --datadir=/var/lib/mysql \
  --backup-image=/backups/my.mbi_2206_1429  \
  --log-bin=s3-bin --relay-log=s3-relay-bin \
  --backup-dir=/tmp/restore_`date +%d%m_%H%M` copy-back-and-apply-log

Being able to restore the binary log and relay log to the right file paths
makes the restore process easier; if that is impossible for some reason, see
Rebuild the Failed Member to Rejoin as a New Member.

3. Restore the auto.cnf file for s3. To rejoin the replication group, the restored member must have

the same server_uuid it used to join the group before. Supply the old server UUID by copying the
auto.cnf file preserved in step 2 above into the data directory of the restored member.

Note

If you cannot supply the failed member's original server_uuid to the restored
member by restoring its old auto.cnf file, you must let the restored member
join the group as a new member; see instructions in Rebuild the Failed Member
to Rejoin as a New Member below on how to do that.

4. Start the restored server. For example, on Linux distributions that use systemd:

systemctl start mysqld

Note

If the server you are restoring is a primary member, perform the steps described
in Restoring a Primary Member before starting the restored server.

5. Restart Group Replication. Connect to the restarted s3 using, for example, a mysql client, and issue

the following command:

mysql> START GROUP_REPLICATION;

Before the restored instance can become an online member of the group, it needs to apply any
transactions that have happened to the group after the backup was taken; this is achieved using
Group Replication's distributed recovery mechanism, and the process starts after the START
GROUP_REPLICATION statement has been issued. To check the member status of the restored
instance, issue:

mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |
+-------------+-------------+--------------+
| s1          |        3306 | ONLINE       |
| s2          |        3306 | ONLINE       |
| s3          |        3306 | RECOVERING   |

3203

Using MySQL Enterprise Backup with Group Replication

+-------------+-------------+--------------+

This shows that s3 is applying transactions to catch up with the group. Once it has caught up with the
rest of the group, its member_state changes to ONLINE:

mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |
+-------------+-------------+--------------+
| s1          |        3306 | ONLINE       |
| s2          |        3306 | ONLINE       |
| s3          |        3306 | ONLINE       |
+-------------+-------------+--------------+

Note

If the server you are restoring is a primary member, once it has gained
synchrony with the group and become ONLINE, perform the steps described at
the end of Restoring a Primary Member to revert the configuration changes you
had made to the server before you started it.

The member has now been fully restored from the backup and functions as a regular member of the group.

Rebuild the Failed Member to Rejoin as a New Member

Sometimes, the steps outlined above in Restoring a Failed Member cannot be carried out because, for
example, the binary log or relay log is corrupted, or it is just missing from the backup. In such a situation,
use the backup to rebuild the member, and then add it to the group as a new member. In the steps below,
we assume the rebuilt member is named s3, like the failed member, and it is run on the same host as s3
was:

1. Copy the backup of s2 onto the host for s3 . The exact way to copy the backup depends on the

operating system and tools available to you. In this example we assume the hosts are both Linux
servers and use SCP to copy the files between them:

s2/backups> scp my.mbi_2206_1429 s3:/backups

2. Restore the backup. Connect to the target host (the host for s3 in this case), and restore the backup

using MySQL Enterprise Backup. Here are the steps:

a. Stop the corrupted server, if it is still running. For example, on Linux distributions that use systemd:

s3> systemctl stop mysqld

b. Delete all contents in the data directory of s3. For example:

s3> rm -rf /var/lib/mysql/*

If the system variables innodb_data_home_dir, innodb_log_group_home_dir, and
innodb_undo_directory point to any directories other than the data directory, they should also
be made empty; otherwise, the restore operation fails.

c. Restore the backup of s2 onto the host of s3. With this approach, we are rebuilding s3 as a

new member, for which we do not need or do not want to use the old binary and relay logs in the
backup; therefore, if these logs have been included in your backup, exclude them using the --
skip-binlog and --skip-relaylog options:

s3> mysqlbackup --defaults-file=/etc/my.cnf \
  --datadir=/var/lib/mysql \
  --backup-image=/backups/my.mbi_2206_1429  \

3204

Using MySQL Enterprise Backup with Group Replication

  --backup-dir=/tmp/restore_`date +%d%m_%H%M` \
  --skip-binlog --skip-relaylog \
  copy-back-and-apply-log

Notes

• If you have healthy binary log and relay logs in the backup that you can
transfer onto the target host with no issues, you are recommended to
follow the easier procedure as described in Restoring a Failed Member
above.

• Do NOT restore manually the corrupted server's auto.cnf file to the data
directory of the new member—when the rebuilt s3 joins the group as a
new member, it is going to be assigned a new server UUID.

3. Start the restored server. For example, on Linux distributions that use systemd:

systemctl start mysqld

Note

If the server you are restoring is a primary member, perform the steps described
in Restoring a Primary Member before starting the restored server.

4. Reconfigure the restored member to join Group Replication. Connect to the restored server with a

mysql client and reset the source and replica information with the following commands:

mysql> RESET MASTER;

mysql> RESET SLAVE ALL;

For the restored server to be able to recover automatically using Group Replication's built-in
mechanism for distributed recovery, configure the server's gtid_executed variable. To do this, use
the backup_gtid_executed.sql file included in the backup of s2, which is usually restored under
the restored member's data directory. Disable binary logging, use the backup_gtid_executed.sql
file to configure gtid_executed, and then re-enable binary logging by issuing the following
statements with your mysql client:

mysql> SET SQL_LOG_BIN=OFF;
mysql> SOURCE datadir/backup_gtid_executed.sql
mysql> SET SQL_LOG_BIN=ON;

Then, configure the Group Replication user credentials on the member:

mysql> CHANGE MASTER TO MASTER_USER='rpl_user', MASTER_PASSWORD='password' /
  FOR CHANNEL 'group_replication_recovery';

5. Restart Group Replication. Issue the following command to the restored server with your mysql client:

mysql> START GROUP_REPLICATION;

Before the restored instance can become an online member of the group, it needs to apply any
transactions that have happened to the group after the backup was taken; this is achieved using
Group Replication's distributed recovery mechanism, and the process starts after the START
GROUP_REPLICATION statement has been issued. To check the member status of the restored
instance, issue:

mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |

3205

Group Replication Security

+-------------+-------------+--------------+
| s3          |        3306 | RECOVERING   |
| s2          |        3306 | ONLINE       |
| s1          |        3306 | ONLINE       |
+-------------+-------------+--------------+

This shows that s3 is applying transactions to catch up with the group. Once it has caught up with the
rest of the group, its member_state changes to ONLINE:

mysql> SELECT member_host, member_port, member_state FROM performance_schema.replication_group_members;
+-------------+-------------+--------------+
| member_host | member_port | member_state |
+-------------+-------------+--------------+
| s3          |        3306 | ONLINE       |
| s2          |        3306 | ONLINE       |
| s1          |        3306 | ONLINE       |
+-------------+-------------+--------------+

Note

If the server you are restoring is a primary member, once it has gained
synchrony with the group and become ONLINE, perform the steps described at
the end of Restoring a Primary Member to revert the configuration changes you
had made to the server before you started it.

The member has now been restored to the group as a new member.

Restoring a Primary Member.
 If the restored member is a primary in the group, care must be taken to
prevent writes to the restored database during the Group Replication recovery phase: Depending on how
the group is accessed by clients, there is a possibility of DML statements being executed on the restored
member once it becomes accessible on the network, prior to the member finishing its catch-up on the
activities it has missed while off the group. To avoid this, before starting the restored server, configure the
following system variables in the server option file:

group_replication_start_on_boot=OFF
super_read_only=ON
event_scheduler=OFF

These settings ensure that the member becomes read-only at startup and that the event scheduler is
turned off while the member is catching up with the group during the recovery phase. Adequate error
handling must also be configured on the clients, as they are prevented temporarily from performing DML
operations during this period on the restored member. Once the restore process is fully completed and the
restored member is in-sync with the rest of the group, revert those changes; restart the event scheduler:

mysql> SET global event_scheduler=ON;

Edit the following system variables in the member's option file, so things are correctly configured for the
next startup:

group_replication_start_on_boot=ON
super_read_only=OFF
event_scheduler=ON

17.6 Group Replication Security

This section explains how to secure a group, securing the connections between members of a group, or by
establishing a security perimeter using IP address allowlisting.

17.6.1 Group Replication IP Address Allowlisting

3206

Group Replication IP Address Allowlisting

The Group Replication plugin has a configuration option to determine from which hosts an
incoming Group Communication System connection can be accepted. This option is called
group_replication_ip_whitelist. If you set this option on a server s1, then when server s2 is
establishing a connection to s1 for the purpose of engaging group communication, s1 first checks the
allowlist before accepting the connection from s2. If s2 is in the allowlist, then s1 accepts the connection,
otherwise s1 rejects the connection attempt by s2.

If you do not specify an allowlist explicitly, the group communication engine (XCom) automatically scans
active interfaces on the host, and identifies those with addresses on private subnetworks. These addresses
and the localhost IP address for IPv4 are used to create an automatic Group Replication allowlist. The
automatic allowlist therefore includes any IP addresses found for the host in the following ranges:

10/8 prefix       (10.0.0.0 - 10.255.255.255) - Class A
172.16/12 prefix  (172.16.0.0 - 172.31.255.255) - Class B
192.168/16 prefix (192.168.0.0 - 192.168.255.255) - Class C
127.0.0.1 - localhost for IPv4

An entry is added to the error log stating the addresses that have been allowlisted automatically for the
host.

The automatic allowlist of private addresses cannot be used for connections from servers outside the
private network, so a server, even if it has interfaces on public IPs, does not by default allow Group
Replication connections from external hosts. For Group Replication connections between server instances
that are on different machines, you must provide public IP addresses and specify these as an explicit
allowlist. If you specify any entries for the allowlist, the private and localhost addresses are not added
automatically, so if you use any of these, you must specify them explicitly.

To specify an allowlist manually, use the group_replication_ip_whitelist option. You cannot
change the allowlist on a server while it is an active member of a replication group. If the member is active,
you must issue a STOP GROUP_REPLICATION statement before changing the allowlist, and a START
GROUP_REPLICATION statement afterwards.

In the allowlist, you can specify any combination of the following:

• IPv4 addresses (for example, 198.51.100.44)

• IPv4 addresses with CIDR notation (for example, 192.0.2.21/24)

• Host names, from MySQL 5.7.21 (for example, example.org)

• Host names with CIDR notation, from MySQL 5.7.21 (for example, www.example.com/24)

IPv6 addresses, and host names that resolve to IPv6 addresses, are not supported in MySQL 5.7. You can
use CIDR notation in combination with host names or IP addresses to allowlist a block of IP addresses with
a particular network prefix, but do ensure that all the IP addresses in the specified subnet are under your
control.

You must stop and restart Group Replication on a member in order to change its allowlist. A comma must
separate each entry in the allowlist. For example:

mysql> STOP GROUP_REPLICATION;
mysql> SET GLOBAL group_replication_ip_whitelist="192.0.2.21/24,198.51.100.44,203.0.113.0/24,example.org,www.example.com/24";
mysql> START GROUP_REPLICATION;

The allowlist must contain the IP address or host name that is specified in each member's
group_replication_local_address system variable. This address is not the same as the MySQL

3207

Group Replication Secure Socket Layer (SSL) Support

server SQL protocol host and port, and is not specified in the bind_address system variable for the
server instance.

When a replication group is reconfigured (for example, when a new primary is elected or a member joins
or leaves), the group members re-establish connections between themselves. If a group member is only
allowlisted by servers that are no longer part of the replication group after the reconfiguration, it is unable
to reconnect to the remaining servers in the replication group that do not allowlist it. To avoid this scenario
entirely, specify the same allowlist for all servers that are members of the replication group.

Note

It is possible to configure different allowlists on different group members according
to your security requirements, for example, in order to keep different subnets
separate. If you need to configure different allowlists to meet your security
requirements, ensure that there is sufficient overlap between the allowlists in the
replication group to maximize the possibility of servers being able to reconnect in
the absence of their original seed member.

For host names, name resolution takes place only when a connection request is made by another server.
A host name that cannot be resolved is not considered for allowlist validation, and a warning message is
written to the error log. Forward-confirmed reverse DNS (FCrDNS) verification is carried out for resolved
host names.

Warning

Host names are inherently less secure than IP addresses in an allowlist. FCrDNS
verification provides a good level of protection, but can be compromised by certain
types of attack. Specify host names in your allowlist only when strictly necessary,
and ensure that all components used for name resolution, such as DNS servers,
are maintained under your control. You can also implement name resolution locally
using the hosts file, to avoid the use of external components.

17.6.2 Group Replication Secure Socket Layer (SSL) Support

Group communication connections as well as recovery connections, are secured using SSL. The following
sections explain how to configure connections.

Configuring SSL for Group Replication Recovery

Recovery is performed through a regular asynchronous replication connection. Once the donor is selected,
the server joining the group establishes an asynchronous replication connection. This is all automatic.

However, a user that requires an SSL connection must have been created before the server joining the
group connects to the donor. Typically, this is set up at the time one is provisioning a server to join the
group.

donor> SET SQL_LOG_BIN=0;
donor> CREATE USER 'rec_ssl_user'@'%' REQUIRE SSL;
donor> GRANT replication slave ON *.* TO 'rec_ssl_user'@'%';
donor> SET SQL_LOG_BIN=1;

Assuming that all servers already in the group have a replication user set up to use SSL, you configure the
server joining the group to use those credentials when connecting to the donor. That is done according to
the values of the SSL options provided for the Group Replication plugin.

new_member> SET GLOBAL group_replication_recovery_use_ssl=1;

3208

Group Replication Secure Socket Layer (SSL) Support

new_member> SET GLOBAL group_replication_recovery_ssl_ca= '.../cacert.pem';
new_member> SET GLOBAL group_replication_recovery_ssl_cert= '.../client-cert.pem';
new_member> SET GLOBAL group_replication_recovery_ssl_key= '.../client-key.pem';

And by configuring the recovery channel to use the credentials of the user that requires an SSL
connection.

new_member> CHANGE MASTER TO MASTER_USER="rec_ssl_user" FOR CHANNEL "group_replication_recovery";
new_member> START GROUP_REPLICATION;

Configuring SSL for Group Communication

Secure sockets can be used to establish communication between members in a group. The configuration
for this depends on the server's SSL configuration. As such, if the server has SSL configured, the Group
Replication plugin also has SSL configured. For more information on the options for configuring the server
SSL, see Command Options for Encrypted Connections. The options which configure Group Replication
are shown in the following table.

Table 17.2 SSL Options

Server Configuration

ssl_key

ssl_cert

ssl_ca

ssl_capath

ssl_crl

ssl_crlpath

ssl_cipher

tls_version

Plugin Configuration Description

Path of key file. To be used as client and server
certificate.

Path of certificate file. To be used as client and
server certificate.

Path of file with SSL Certificate Authorities that are
trusted.

Path of directory containing certificates for SSL
Certificate Authorities that are trusted.

Path of file containing the certificate revocation lists.

Path of directory containing revoked certificate lists.

Permitted ciphers to use while encrypting data over
the connection.

Secure communication uses this version and its
protocols.

These options are MySQL Server configuration options which Group Replication relies on for its
configuration. In addition there is the following Group Replication specific option to configure SSL on the
plugin itself.

• group_replication_ssl_mode - specifies the security state of the connection between Group

Replication members.

Table 17.3 group_replication_ssl_mode configuration values

Value

DISABLED

REQUIRED

VERIFY_CA

Description

Establish an unencrypted connection (default).

Establish a secure connection if the server supports
secure connections.

Like REQUIRED, but additionally verify the server
TLS certificate against the configured Certificate
Authority (CA) certificates.

3209

Group Replication and Virtual Private Networks (VPNs)

Value

VERIFY_IDENTITY

Description

Like VERIFY_CA, but additionally verify that the
server certificate matches the host to which the
connection is attempted.

The following example shows an example my.cnf file section used to configure SSL on a server and how
activate it for Group Replication.

[mysqld]
ssl_ca = "cacert.pem"
ssl_capath = "/.../ca_directory"
ssl_cert = "server-cert.pem"
ssl_cipher = "DHE-RSA-AEs256-SHA"
ssl_crl = "crl-server-revoked.crl"
ssl_crlpath = "/.../crl_directory"
ssl_key = "server-key.pem"
group_replication_ssl_mode= REQUIRED

The only plugin specific configuration option that is listed is group_replication_ssl_mode. This option
activates the SSL communication between members of the group, by configuring the SSL framework with
the ssl_* parameters that are provided to the server.

17.6.3 Group Replication and Virtual Private Networks (VPNs)

There is nothing preventing Group Replication from operating over a virtual private network. At its core,
it just relies on an IPv4 socket to establish connections between servers for the purpose of propagating
messages between them.

17.7 Group Replication Variables

The next two sections contain information about MySQL server system and server status variables which
are specific to the Group Replication plugin.

Table 17.4 Group Replication Variable and Option Summary

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Yes
group_replication_allow_local_disjoint_gtids_join

Yes

Yes

Yes
group_replication_allow_local_lower_version_join

Yes

Yes

group_replication_auto_increment_increment

Yes

Yes

Yes
group_replication_bootstrap_group
Yes

group_replication_components_stop_timeout

Yes

Yes

group_replication_compression_threshold

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_enforce_update_everywhere_checks

Yes

Yes

Yes

Yes
group_replication_exit_state_action
Yes

Yes

Yes
group_replication_flow_control_applier_threshold

Yes

Yes

Yes
group_replication_flow_control_certifier_threshold

Yes

Yes

group_replication_flow_control_mode

Yes

Yes

Yes
group_replication_force_members
Yes

group_replication_group_name

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

3210

Group Replication System Variables

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

group_replication_group_seeds

Yes

Yes

Yes

group_replication_gtid_assignment_block_size

Yes

Yes

Yes

group_replication_ip_whitelist

Yes

Yes

Yes
group_replication_local_address

Yes

Yes
group_replication_member_weight
Yes

Yes
group_replication_poll_spin_loops
Yes

group_replication_primary_member

group_replication_recovery_complete_at

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_recovery_reconnect_interval

Yes

Yes

Yes

group_replication_recovery_retry_count

Yes

Yes

Yes
group_replication_recovery_ssl_ca
Yes

group_replication_recovery_ssl_capath

Yes

Yes

Yes
group_replication_recovery_ssl_cert

Yes

group_replication_recovery_ssl_cipher

Yes

Yes

Yes
group_replication_recovery_ssl_crl
Yes

group_replication_recovery_ssl_crlpath

Yes

Yes

Yes
group_replication_recovery_ssl_key

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
group_replication_recovery_ssl_verify_server_cert

Yes

Yes

Yes
group_replication_recovery_use_ssl

Yes

group_replication_single_primary_mode

Yes

Yes

group_replication_ssl_mode

Yes

Yes

Yes
group_replication_start_on_boot

Yes

group_replication_transaction_size_limit

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
group_replication_unreachable_majority_timeout

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

17.7.1 Group Replication System Variables

This section lists the system variables that are specific to the Group Replication plugin.

The name of each Group Replication system variable is prefixed with group_replication_.

Most system variables for Group Replication are described as dynamic, and their values can be changed
while the server is running. However, in most cases, the change only takes effect after you stop and restart
Group Replication on the group member using a STOP GROUP_REPLICATION statement followed by a
START GROUP_REPLICATION statement. Changes to the following system variables take effect without
stopping and restarting Group Replication:

• group_replication_exit_state_action

• group_replication_flow_control_applier_threshold

• group_replication_flow_control_certifier_threshold

• group_replication_flow_control_hold_percent

3211

Group Replication System Variables

• group_replication_flow_control_max_quota

• group_replication_flow_control_member_quota_percent

• group_replication_flow_control_min_quota

• group_replication_flow_control_min_recovery_quota

• group_replication_flow_control_mode

• group_replication_force_members

• group_replication_member_weight

• group_replication_transaction_size_limit

• group_replication_unreachable_majority_timeout

Most system variables for Group Replication can have different values on different group members. For the
following system variables, it is advisable to set the same value on all members of a group in order to avoid
unnecessary rollback of transactions, failure of message delivery, or failure of message recovery:

• group_replication_auto_increment_increment

• group_replication_compression_threshold

• group_replication_transaction_size_limit

Some system variables on a Group Replication group member, including some Group Replication-
specific system variables and some general system variables, are group-wide configuration settings.
These system variables must have the same value on all group members, cannot be changed while
Group Replication is running, and require a full reboot of the group (a bootstrap by a server with
group_replication_bootstrap_group=ON) in order for the value change to take effect. These
conditions apply to the following system variables:

• group_replication_single_primary_mode

• group_replication_enforce_update_everywhere_checks

• group_replication_gtid_assignment_block_size

• default_table_encryption

• lower_case_table_names

• transaction_write_set_extraction

Important

• A number of system variables for Group Replication are not completely validated

during server startup if they are passed as command line arguments to the
server. These system variables include group_replication_group_name,
group_replication_single_primary_mode,
group_replication_force_members, the SSL variables, and the flow
control system variables. They are only fully validated after the server has
started.

• System variables for Group Replication that specify IP addresses or host names

for group members are not validated until a START GROUP_REPLICATION

3212

Group Replication System Variables

statement is issued. Group Replication's Group Communication System (GCS) is
not available to validate the values until that point.

The system variables that are specific to the Group Replication plugin are as follows:

• group_replication_allow_local_disjoint_gtids_join

Command-Line Format

--group-replication-allow-local-
disjoint-gtids-join[={OFF|ON}]

Introduced

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

5.7.17

5.7.21

group_replication_allow_local_disjoint_gtids_join

Global

Yes

Boolean

OFF

Deprecated in version 5.7.21 and scheduled for removal in a future version. Allows the server to join the
group even if it has local transactions that are not present in the group.

Warning

Use caution when enabling this option as incorrect usage can lead to conflicts in
the group and rollback of transactions. The option should only be enabled as a
last resort method to allow a server that has local transactions to join an existing
group, and then only if the local transactions do not affect the data that is handled
by the group (for example, an administrative action that was written to the binary
log). The option should not be left enabled on all group members.

• group_replication_allow_local_lower_version_join

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-allow-local-
lower-version-join[={OFF|ON}]

5.7.17

group_replication_allow_local_lower_version_join

Global

Yes

Boolean

OFF

Allows the current server to join the group even if it has a lower major version than the group.
With the default setting OFF, servers are not permitted to join a replication group if they
have a lower major version than the existing group members. For example, a MySQL 5.7
server cannot join a group that consists of MySQL 8.0 servers. This standard policy ensures
that all members of a group are able to exchange messages and apply transactions. Set
group_replication_allow_local_lower_version_join to ON only in the following scenarios:

• A server must be added to the group in an emergency in order to improve the group's fault tolerance,

and only older versions are available.

3213

Group Replication System Variables

• You want to carry out a downgrade of the replication group members without shutting down the whole

group and bootstrapping it again.

Warning

Setting this option to ON does not make the new member compatible with the
group, and allows it to join the group without any safeguards against incompatible
behaviors by the existing members. To ensure the new member's correct
operation, take both of the following precautions:

1. Before the server with the lower major version joins the group, stop all writes

on that server.

2. From the point where the server with the lower major version joins the group,

stop all writes on the other servers in the group.

Without these precautions, the server with the lower major version is likely to
experience difficulties and terminate with an error.

• group_replication_auto_increment_increment

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--group-replication-auto-increment-
increment=#

5.7.17

group_replication_auto_increment_increment

Global

Yes

Integer

7

1

65535

Determines the interval between successive column values for transactions that execute on
this server instance. This system variable should have the same value on all group members.
When Group Replication is started on a server, the value of the server system variable
auto_increment_increment is changed to this value, and the value of the server system variable
auto_increment_offset is changed to the server ID. These settings avoid the selection of duplicate
auto-increment values for writes on group members, which causes rollback of transactions. The
changes are reverted when Group Replication is stopped. These changes are only made and reverted if
auto_increment_increment and auto_increment_offset each have their default value of 1. If
their values have already been modified from the default, Group Replication does not alter them.

The default value of 7 represents a balance between the number of usable values and the permitted
maximum size of a replication group (9 members). If your group has more or fewer members, you can
set this system variable to match the expected number of group members before Group Replication is
started. You cannot change the setting while Group Replication is running.

Important

Setting group_replication_auto_increment_increment has no effect
when group_replication_single_primary_mode is ON.

3214

Group Replication System Variables

• group_replication_bootstrap_group

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-bootstrap-
group[={OFF|ON}]

5.7.17

group_replication_bootstrap_group

Global

Yes

Boolean

OFF

Configure this server to bootstrap the group. This option must only be set on one server and only when
starting the group for the first time or restarting the entire group. After the group has been bootstrapped,
set this option to OFF. It should be set to OFF both dynamically and in the configuration files. Starting two
servers or restarting one server with this option set while the group is running may lead to an artificial
split brain situation, where two independent groups with the same name are bootstrapped.

• group_replication_components_stop_timeout

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--group-replication-components-stop-
timeout=#

5.7.17

group_replication_components_stop_timeout

Global

Yes

Integer

31536000

2

31536000

seconds

Timeout, in seconds, that Group Replication waits for each of the components when shutting down.

• group_replication_compression_threshold

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--group-replication-compression-
threshold=#

5.7.17

group_replication_compression_threshold

Global

Yes

Integer

1000000

0

4294967295

3215

Group Replication System Variables

Unit

bytes

The threshold value in bytes above which compression is applied to messages sent between
group members. If this system variable is set to zero, compression is disabled. The value of
group_replication_compression_threshold should be the same on all group members.

Group Replication uses the LZ4 compression algorithm to compress messages sent
in the group. Note that the maximum supported input size for the LZ4 compression
algorithm is 2113929216 bytes. This limit is lower than the maximum possible value for the
group_replication_compression_threshold system variable, which is matched to the maximum
message size accepted by XCom. With the LZ4 compression algorithm, do not set a value greater than
2113929216 bytes for group_replication_compression_threshold, because transactions above
this size cannot be committed when message compression is enabled.

For more information, see Section 17.9.7.2, “Message Compression”.

• group_replication_enforce_update_everywhere_checks

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-enforce-update-
everywhere-checks[={OFF|ON}]

5.7.17

group_replication_enforce_update_everywhere_checks

Global

Yes

Boolean

OFF

Enable or disable strict consistency checks for multi-primary update everywhere. The default is that
checks are disabled. In single-primary mode, this option must be disabled on all group members. In
multi-primary mode, when this option is enabled, statements are checked as follows to ensure they are
compatible with multi-primary mode:

• If a transaction is executed under the SERIALIZABLE isolation level, then its commit fails when

synchronizing itself with the group.

• If a transaction executes against a table that has foreign keys with cascading constraints, then the

transaction fails to commit when synchronizing itself with the group.

This system variable is a group-wide configuration setting. It must have the same value on all group
members, cannot be changed while Group Replication is running, and requires a full reboot of the group
(a bootstrap by a server with group_replication_bootstrap_group=ON) in order for the value
change to take effect.

• group_replication_exit_state_action

Command-Line Format

Introduced

System Variable

Scope

Dynamic

--group-replication-exit-state-
action=value

5.7.24

group_replication_exit_state_action

Global

Yes

3216

Group Replication System Variables

Type

Default Value

Valid Values

Enumeration

READ_ONLY

ABORT_SERVER

READ_ONLY

Configures how Group Replication behaves when a server instance leaves the group
unintentionally, for example after encountering an applier error, or in the case of a loss of
majority, or when another member of the group expels it due to a suspicion timing out. The
timeout period for a member to leave the group in the case of a loss of majority is set by the
group_replication_unreachable_majority_timeout system variable. Note that an expelled
group member does not know that it was expelled until it reconnects to the group, so the specified action
is only taken if the member manages to reconnect, or if the member raises a suspicion on itself and
expels itself.

When group_replication_exit_state_action is set to ABORT_SERVER, if the member exits the
group unintentionally, the instance shuts down MySQL.

When group_replication_exit_state_action is set to READ_ONLY, if the member exits the
group unintentionally, the instance switches MySQL to super read only mode (by setting the system
variable super_read_only to ON). This setting is the default in MySQL 5.7.

Important

If a failure occurs before the member has successfully joined the group, the
specified exit action is not taken. This is the case if there is a failure during
the local configuration check, or a mismatch between the configuration of
the joining member and the configuration of the group. In these situations,
the super_read_only system variable is left with its original value, and the
server does not shut down MySQL. To ensure that the server cannot accept
updates when Group Replication did not start, we therefore recommend
that super_read_only=ON is set in the server's configuration file at
startup, which Group Replication changes to OFF on primary members after
it has been started successfully. This safeguard is particularly important
when the server is configured to start Group Replication on server boot
(group_replication_start_on_boot=ON), but it is also useful when Group
Replication is started manually using a START GROUP_REPLICATION command.

If a failure occurs after the member has successfully joined the group, the
specified exit action is taken. This is the case if there is an applier error, if the
member is expelled from the group, or if the member is set to time out in the
event of an unreachable majority. In these situations, if READ_ONLY is the exit
action, the super_read_only system variable is set to ON, or if ABORT_SERVER
is the exit action, the server shuts down MySQL.

Table 17.5 Exit actions in Group Replication failure situations

Failure situation

Member fails local configuration
check

OR

Group Replication started with
START GROUP_REPLICATION

Group Replication started with
group_replication_start_on_boot
=ON

super_read_only unchanged

super_read_only unchanged

MySQL continues running

MySQL continues running

3217

Group Replication System Variables

Failure situation

Group Replication started with
START GROUP_REPLICATION

Mismatch between joining
member and group configuration

Set super_read_only=ON at
startup to prevent updates

Group Replication started with
group_replication_start_on_boot
=ON
Set super_read_only=ON
at startup to prevent updates
(Important)

Applier error on member

super_read_only set to ON

super_read_only set to ON

OR

OR

OR

Member expelled from group

MySQL shuts down

MySQL shuts down

OR

Unreachable majority timeout

• group_replication_flow_control_applier_threshold

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--group-replication-flow-control-
applier-threshold=#

5.7.17

group_replication_flow_control_applier_threshold

Global

Yes

Integer

25000

0

2147483647

transactions

Specifies the number of waiting transactions in the applier queue that trigger flow control. This variable
can be changed without resetting Group Replication.

• group_replication_flow_control_certifier_threshold

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

3218

--group-replication-flow-control-
certifier-threshold=#

5.7.17

group_replication_flow_control_certifier_threshold

Global

Yes

Integer

25000

0

2147483647

Group Replication System Variables

Unit

transactions

Specifies the number of waiting transactions in the certifier queue that trigger flow control. This variable
can be changed without resetting Group Replication.

• group_replication_flow_control_hold_percent

Command-Line Format

--group-replication-flow-control-
hold-percent=#

System Variable

group_replication_flow_control_hold_percent

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Global

Yes

Integer

10

0

100

percentage

Defines what percentage of the group quota remains unused to allow a cluster under flow control to
catch up on backlog. A value of 0 implies that no part of the quota is reserved for catching up on the
work backlog.

• group_replication_flow_control_max_quota

Command-Line Format

--group-replication-flow-control-max-
quota=#

System Variable

group_replication_flow_control_max_quota

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

0

0

2147483647

Defines the maximum flow control quota of the group, or the maximum available quota for
any period while flow control is enabled. A value of 0 implies that there is no maximum quota
set. Cannot be smaller than group_replication_flow_control_min_quota and
group_replication_flow_control_min_recovery_quota.

• group_replication_flow_control_member_quota_percent

Command-Line Format

--group-replication-flow-control-
member-quota-percent=#

System Variable

group_replication_flow_control_member_quota_percent

Scope

Dynamic

Type

Global

Yes

Integer

3219

Group Replication System Variables

Default Value

Minimum Value

Maximum Value

Unit

0

0

100

percentage

Defines the percentage of the quota that a member should assume is available for itself when calculating
the quotas. A value of 0 implies that the quota should be split equally between members that were
writers in the last period.

• group_replication_flow_control_min_quota

Command-Line Format

--group-replication-flow-control-min-
quota=#

System Variable

group_replication_flow_control_min_quota

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

0

0

2147483647

Controls the lowest flow control quota that can be assigned to a member, independently of the calculated
minimum quota executed in the last period. A value of 0 implies that there is no minimum quota. Cannot
be larger than group_replication_flow_control_max_quota.

• group_replication_flow_control_min_recovery_quota

Command-Line Format

--group-replication-flow-control-min-
recovery-quota=#

System Variable

group_replication_flow_control_min_recovery_quota

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

0

0

2147483647

Controls the lowest quota that can be assigned to a member because of another recovering
member in the group, independently of the calculated minimum quota executed in the
last period. A value of 0 implies that there is no minimum quota. Cannot be larger than
group_replication_flow_control_max_quota.

• group_replication_flow_control_mode

Command-Line Format

3220

Introduced

--group-replication-flow-control-
mode=value

5.7.17

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

Group Replication System Variables

group_replication_flow_control_mode

Global

Yes

Enumeration

QUOTA

DISABLED

QUOTA

Specifies the mode used for flow control. This variable can be changed without resetting Group
Replication.

• group_replication_force_members

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-force-
members=value

5.7.17

group_replication_force_members

Global

Yes

String

A list of peer addresses as a comma separated list such as host1:port1,host2:port2. This option is
used to force a new group membership, in which the excluded members do not receive a new view and
are blocked. (You need to manually kill the excluded servers.) Any invalid host names in the list could
cause this action to fail because they could block group membership. For a description of the procedure
to follow, see Section 17.5.3, “Network Partitioning”.

You must specify the address or host name and port as they are given in the
group_replication_local_address option for each member. For example:

"198.51.100.44:33061,example.org:33061"

After you have used the group_replication_force_members system variable to successfully
force a new group membership and unblock the group, ensure that you clear the system
variable. group_replication_force_members must be empty in order to issue a START
GROUP_REPLICATION statement.

• group_replication_group_name

Command-Line Format

--group-replication-group-name=value

Introduced

System Variable

Scope

Dynamic

5.7.17

group_replication_group_name

Global

Yes

3221

Group Replication System Variables

Type

String

The name of the group which this server instance belongs to. Must be a valid UUID. This UUID is used
internally when setting GTIDs for Group Replication events in the binary log.

Important

A unique UUID must be used.

• group_replication_group_seeds

Command-Line Format

--group-replication-group-seeds=value

Introduced

System Variable

Scope

Dynamic

Type

5.7.17

group_replication_group_seeds

Global

Yes

String

A list of group members to which a joining member can connect to obtain details of all the current group
members. The joining member uses these details to select and connect to a group member to obtain the
data needed for synchrony with the group. The list consists of the seed member's network addresses
specified as a comma separated list, such as host1:port1,host2:port2.

Important

These addresses must not be the member's SQL hostname and port.

Note that the value you specify for this variable is not validated until a START GROUP_REPLICATION
statement is issued and the Group Communication System (GCS) is available.

Usually this list consists of all members of the group, but you can choose a subset of the group members
to be seeds. The list must contain at least one valid member address. Each address is validated
when starting Group Replication. If the list does not contain any valid host names, issuing START
GROUP_REPLICATION fails.

• group_replication_gtid_assignment_block_size

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--group-replication-gtid-assignment-
block-size=#

5.7.17

group_replication_gtid_assignment_block_size

Global

Yes

Integer

1000000

1

Maximum Value (64-bit platforms)

9223372036854775807

3222

Group Replication System Variables

Maximum Value (32-bit platforms)

4294967295

The number of consecutive GTIDs that are reserved for each member. Each member consumes its
blocks and reserves more when needed.

This system variable is a group-wide configuration setting. It must have the same value on all group
members, cannot be changed while Group Replication is running, and requires a full reboot of the group
(a bootstrap by a server with group_replication_bootstrap_group=ON) in order for the value
change to take effect.

• group_replication_ip_whitelist

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-ip-
whitelist=value

5.7.17

group_replication_ip_whitelist

Global

Yes

String

AUTOMATIC

Specifies the allowlist of hosts that are permitted to connect to the group. The address that you specify
for each group member in group_replication_local_address must be allowlisted on the other
servers in the replication group. Note that the value you specify for this variable is not validated until a
START GROUP_REPLICATION statement is issued and the Group Communication System (GCS) is
available.

By default, this system variable is set to AUTOMATIC, which permits connections from private
subnetworks active on the host. The group communication engine (XCom) automatically scans active
interfaces on the host, and identifies those with addresses on private subnetworks. These addresses
and the localhost IP address for IPv4 are used to create the Group Replication allowlist. For a list of
the ranges from which addresses are automatically allowlisted, see Section 17.6.1, “Group Replication
IP Address Allowlisting”.

The automatic allowlist of private addresses cannot be used for connections from servers outside the
private network. For Group Replication connections between server instances that are on different
machines, you must provide public IP addresses and specify these as an explicit allowlist. If you specify
any entries for the allowlist, the private addresses are not added automatically, so if you use any of
these, you must specify them explicitly. The localhost IP address is added automatically.

As the value of the group_replication_ip_whitelist option, you can specify any combination of
the following:

• IPv4 addresses (for example, 198.51.100.44)

• IPv4 addresses with CIDR notation (for example, 192.0.2.21/24)

• Host names, from MySQL 5.7.21 (for example, example.org)

• Host names with CIDR notation, from MySQL 5.7.21 (for example, www.example.com/24)

IPv6 addresses, and host names that resolve to IPv6 addresses, are not supported in MySQL 5.7.
You can use CIDR notation in combination with host names or IP addresses to allowlist a block of IP

3223

Group Replication System Variables

addresses with a particular network prefix, but do ensure that all the IP addresses in the specified subnet
are under your control.

A comma must separate each entry in the allowlist. For example:

192.0.2.22,198.51.100.0/24,example.org,www.example.com/24

It is possible to configure different allowlists on different group members according to your security
requirements, for example, in order to keep different subnets separate. However, this can cause issues
when a group is reconfigured. If you do not have a specific security requirement to do otherwise, use the
same allowlist on all members of a group. For more details, see Section 17.6.1, “Group Replication IP
Address Allowlisting”.

For host names, name resolution takes place only when a connection request is made by another
server. A host name that cannot be resolved is not considered for allowlist validation, and a warning
message is written to the error log. Forward-confirmed reverse DNS (FCrDNS) verification is carried out
for resolved host names.

Warning

Host names are inherently less secure than IP addresses in an allowlist. FCrDNS
verification provides a good level of protection, but can be compromised by
certain types of attack. Specify host names in your allowlist only when strictly
necessary, and ensure that all components used for name resolution, such as
DNS servers, are maintained under your control. You can also implement name
resolution locally using the hosts file, to avoid the use of external components.

• group_replication_local_address

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-local-
address=value

5.7.17

group_replication_local_address

Global

Yes

String

The network address which the member provides for connections from other members, specified as a
host:port formatted string. This address must be reachable by all members of the group because
it is used by the group communication engine for Group Replication (XCom, a Paxos variant) for TCP
communication between remote XCom instances. Communication with the local instance is over an input
channel using shared memory.

Warning

Do not use this address for communication with the member.

Other Group Replication members contact this member through this host:port for all internal group
communication. This is not the MySQL server SQL protocol host and port.

The address or host name that you specify in group_replication_local_address is used by
Group Replication as the unique identifier for a group member within the replication group. You can use
the same port for all members of a replication group as long as the host names or IP addresses are all

3224

Group Replication System Variables

different, and you can use the same host name or IP address for all members as long as the ports are all
different. The recommended port for group_replication_local_address is 33061. Note that the
value you specify for this variable is not validated until the START GROUP_REPLICATION statement is
issued and the Group Communication System (GCS) is available.

• group_replication_member_weight

Command-Line Format

--group-replication-member-weight=#

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

5.7.20

group_replication_member_weight

Global

Yes

Integer

50

0

100

percentage

A percentage weight that can be assigned to members to influence the chance of the member being
elected as primary in the event of failover, for example when the existing primary leaves a single-primary
group. Assign numeric weights to members to ensure that specific members are elected, for example
during scheduled maintenance of the primary or to ensure certain hardware is prioritized in the event of
failover.

For a group with members configured as follows:

• member-1: group_replication_member_weight=30, server_uuid=aaaa

• member-2: group_replication_member_weight=40, server_uuid=bbbb

• member-3: group_replication_member_weight=40, server_uuid=cccc

• member-4: group_replication_member_weight=40, server_uuid=dddd

during election of a new primary the members above would be sorted as member-2, member-3,
member-4, and member-1. This results in member-2 being chosen as the new primary in the event of
failover. For more information, see Section 17.5.1.1, “Single-Primary Mode”.

• group_replication_poll_spin_loops

Command-Line Format

--group-replication-poll-spin-loops=#

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

5.7.17

group_replication_poll_spin_loops

Global

Yes

Integer

0

0

Maximum Value (64-bit platforms)

18446744073709551615

3225

Group Replication System Variables

Maximum Value (32-bit platforms)

4294967295

The number of times the group communication thread waits for the communication engine mutex to be
released before the thread waits for more incoming network messages.

• group_replication_recovery_complete_at

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

--group-replication-recovery-
complete-at=value

5.7.17

group_replication_recovery_complete_at

Global

Yes

Enumeration

TRANSACTIONS_APPLIED

TRANSACTIONS_CERTIFIED

TRANSACTIONS_APPLIED

Recovery policies when handling cached transactions after state transfer. This option specifies whether
a member is marked online after it has received all transactions that it missed before it joined the group
(TRANSACTIONS_CERTIFIED) or after it has received and applied them (TRANSACTIONS_APPLIED).

• group_replication_recovery_retry_count

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--group-replication-recovery-retry-
count=#

5.7.17

group_replication_recovery_retry_count

Global

Yes

Integer

10

0

31536000

The number of times that the member that is joining tries to connect to the available donors before giving
up.

• group_replication_recovery_reconnect_interval

Command-Line Format

Introduced

System Variable

Scope

Dynamic

3226

--group-replication-recovery-
reconnect-interval=#

5.7.17

group_replication_recovery_reconnect_interval

Global

Yes

Group Replication System Variables

Type

Default Value

Minimum Value

Maximum Value

Unit

Integer

60

0

31536000

seconds

The sleep time, in seconds, between reconnection attempts when no donor was found in the group.

• group_replication_recovery_ssl_ca

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
ca=value

5.7.17

group_replication_recovery_ssl_ca

Global

Yes

String

The path to a file that contains a list of trusted SSL certificate authorities.

• group_replication_recovery_ssl_capath

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
capath=value

5.7.17

group_replication_recovery_ssl_capath

Global

Yes

String

The path to a directory that contains trusted SSL certificate authority certificates.

• group_replication_recovery_ssl_cert

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
cert=value

5.7.17

group_replication_recovery_ssl_cert

Global

Yes

String

The name of the SSL certificate file to use for establishing a secure connection.

3227

Group Replication System Variables

• group_replication_recovery_ssl_key

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
key=value

5.7.17

group_replication_recovery_ssl_key

Global

Yes

String

The name of the SSL key file to use for establishing a secure connection.

• group_replication_recovery_ssl_cipher

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
cipher=value

5.7.17

group_replication_recovery_ssl_cipher

Global

Yes

String

The list of permissible ciphers for SSL encryption.

• group_replication_recovery_ssl_crl

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
crl=value

5.7.17

group_replication_recovery_ssl_crl

Global

Yes

File name

The path to a directory that contains files containing certificate revocation lists.

• group_replication_recovery_ssl_crlpath

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

--group-replication-recovery-ssl-
crlpath=value

5.7.17

group_replication_recovery_ssl_crlpath

Global

Yes

Directory name

The path to a directory that contains files containing certificate revocation lists.

3228

Group Replication System Variables

• group_replication_recovery_ssl_verify_server_cert

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-recovery-ssl-
verify-server-cert[={OFF|ON}]

5.7.17

group_replication_recovery_ssl_verify_server_cert

Global

Yes

Boolean

OFF

Make the recovery process check the server's Common Name value in the donor sent certificate.

• group_replication_recovery_use_ssl

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-recovery-use-
ssl[={OFF|ON}]

5.7.17

group_replication_recovery_use_ssl

Global

Yes

Boolean

OFF

Whether Group Replication recovery connection should use SSL or not.

• group_replication_single_primary_mode

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Note

--group-replication-single-primary-
mode[={OFF|ON}]

5.7.17

group_replication_single_primary_mode

Global

Yes

Boolean

ON

This system variable is a group-wide configuration setting, and a full reboot of the
replication group is required for a change to take effect.

group_replication_single_primary_mode instructs the group to pick a single server
automatically to be the one that handles read/write workload. This server is the primary and all others
are secondaries.

This system variable is a group-wide configuration setting. It must have the same value on all group
members, cannot be changed while Group Replication is running, and requires a full reboot of the

3229

Group Replication System Variables

group (a bootstrap by a server with group_replication_bootstrap_group=ON) in order for the
value change to take effect. For instructions to safely bootstrap a group where transactions have been
executed and certified, see Section 17.5.4, “Restarting a Group”.

If the group has a value set for this system variable, and a joining member has a different value set for
the system variable, the joining member cannot join the group until the value is changed to match. If the
group members have a value set for this system variable, and the joining member does not support the
system variable, it cannot join the group.

Setting this variable ON causes any setting for group_replication_auto_increment_increment
to be ignored.

• group_replication_ssl_mode

Command-Line Format

--group-replication-ssl-mode=value

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

5.7.17

group_replication_ssl_mode

Global

Yes

Enumeration

DISABLED

DISABLED

REQUIRED

VERIFY_CA

VERIFY_IDENTITY

Specifies the security state of the connection between Group Replication members.

• group_replication_start_on_boot

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--group-replication-start-on-
boot[={OFF|ON}]

5.7.17

group_replication_start_on_boot

Global

Yes

Boolean

ON

Whether the server should start Group Replication or not during server start.

• group_replication_transaction_size_limit

Command-Line Format

3230

Introduced

--group-replication-transaction-size-
limit=#

5.7.19

Group Replication System Variables

System Variable

group_replication_transaction_size_limit

Scope

Dynamic

Type

Default Value (≥ 5.7.38)
Default Value (≥ 5.7.19, ≤ 5.7.37)
Minimum Value

Maximum Value

Unit

Global

Yes

Integer

150000000

0

0

2147483647

bytes

Configures the maximum transaction size in bytes which the replication group accepts. Transactions
larger than this size are rolled back by the receiving member and are not broadcast to the group. Large
transactions can cause problems for a replication group in terms of memory allocation, which can cause
the system to slow down, or in terms of network bandwidth consumption, which can cause a member to
be suspected of having failed because it is busy processing the large transaction.

When this system variable is set to 0, there is no limit to the size of transactions the group accepts.
In releases up to and including MySQL 5.7.37, the default setting for this system variable is 0. From
MySQL 5.7.38, and in MySQL 8.0, the default setting is 150000000 bytes (approximately 143 MB).
Adjust the value of this system variable depending on the maximum message size that you need the
group to tolerate, bearing in mind that the time taken to process a transaction is proportional to its size.
The value of group_replication_transaction_size_limit should be the same on all group
members. For further mitigation strategies for large transactions, see Section 17.3.2, “Group Replication
Limitations”.

• group_replication_unreachable_majority_timeout

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--group-replication-unreachable-
majority-timeout=#

5.7.19

group_replication_unreachable_majority_timeout

Global

Yes

Integer

0

0

31536000

seconds

Configures how long members that suffer a network partition and cannot connect to the majority wait
before leaving the group.

In a group of 5 servers (S1,S2,S3,S4,S5), if there is a disconnection between (S1,S2) and (S3,S4,S5)
there is a network partition. The first group (S1,S2) is now in a minority because it cannot contact more
than half of the group. While the majority group (S3,S4,S5) remains running, the minority group waits
for the specified time for a network reconnection. Any transactions processed by the minority group are
blocked until Group Replication is stopped using STOP GROUP REPLICATION on the members of the

3231

Group Replication Status Variables

minority. Note that group_replication_unreachable_majority_timeout has no effect if it is set
on the servers in the minority group after the loss of majority has been detected.

By default, this system variable is set to 0, which means that members that find themselves in a
minority due to a network partition wait forever to leave the group. If configured to a number of seconds,
members wait for this amount of time after losing contact with the majority of members before leaving the
group. When the specified time elapses, all pending transactions processed by the minority are rolled
back, and the servers in the minority partition move to the ERROR state. These servers then follow the
action specified by the system variable group_replication_exit_state_action, which can be to
set themselves to super read only mode or shut down MySQL.

Warning

When you have a symmetric group, with just two members for example (S0,S2),
if there is a network partition and there is no majority, after the configured timeout
all members enter ERROR state.

17.7.2 Group Replication Status Variables

MySQL 5.7 supports one status variable providing information about Group Replication. This variable is
described here:

• group_replication_primary_member

Shows the primary member's UUID when the group is operating in single-primary mode. If the group is
operating in multi-primary mode, shows an empty string. See Section 17.5.1.3, “Finding the Primary”.

17.8 Frequently Asked Questions

This section provides answers to frequently asked questions.

What is the maximum number of MySQL servers in a group?

A group can consist of maximum 9 servers. Attempting to add another server to a group with 9 members
causes the request to join to be refused. This limit has been identified from testing and benchmarking as a
safe boundary where the group performs reliably on a stable local area network.

How are servers in a group connected?

Servers in a group connect to the other servers in the group by opening a peer-to-peer TCP connection.
These connections are only used for internal communication and message passing between servers in the
group. This address is configured by the group_replication_local_address variable.

What is the group_replication_bootstrap_group option used for?

The bootstrap flag instructs a member to create a group and act as the initial seed server. The second
member joining the group needs to ask the member that bootstrapped the group to dynamically change the
configuration in order for it to be added to the group.

A member needs to bootstrap the group in two scenarios. When the group is originally created, or when
shutting down and restarting the entire group.

How do I set credentials for the recovery procedure?

You pre-configure the Group Replication recovery channel credentials using the CHANGE MASTER TO
statement.

3232

Can I scale-out my write-load using Group Replication?

Can I scale-out my write-load using Group Replication?

Not directly, but MySQL Group replication is a shared nothing full replication solution, where all servers
in the group replicate the same amount of data. Therefore if one member in the group writes N bytes to
storage as the result of a transaction commit operation, then roughly N bytes are written to storage on
other members as well, because the transaction is replicated everywhere.

However, given that other members do not have to do the same amount of processing that the original
member had to do when it originally executed the transaction, they apply the changes faster. Transactions
are replicated in a format that is used to apply row transformations only, without having to re-execute
transactions again (row-based format).

Furthermore, given that changes are propagated and applied in row-based format, this means that they
are received in an optimized and compact format, and likely reducing the number of IO operations required
when compared to the originating member.

To summarize, you can scale-out processing, by spreading conflict free transactions throughout different
members in the group. And you can likely scale-out a small fraction of your IO operations, since remote
servers receive only the necessary changes to read-modify-write changes to stable storage.

Does Group Replication require more network bandwidth and CPU, when
compared to simple replication and under the same workload?

Some additional load is expected because servers need to be constantly interacting with each other for
synchronization purposes. It is difficult to quantify how much more data. It also depends on the size of the
group (three servers puts less stress on the bandwidth requirements than nine servers in the group).

Also the memory and CPU footprint are larger, because more complex work is done for the server
synchronization part and for the group messaging.

Can I deploy Group Replication across wide-area networks?

Yes, but the network connection between each member must be reliable and have suitable perfomance.
Low latency, high bandwidth network connections are a requirement for optimal performance.

If network bandwidth alone is an issue, then Section 17.9.7.2, “Message Compression” can be used to
lower the bandwidth required. However, if the network drops packets, leading to re-transmissions and
higher end-to-end latency, throughput and latency are both negatively affected.

Warning

When the network round-trip time (RTT) between any group members is 5 seconds
or more you could encounter problems as the built-in failure detection mechanism
could be incorrectly triggered.

Do members automatically rejoin a group in case of temporary connectivity
problems?

This depends on the reason for the connectivity problem. If the connectivity problem is transient and
the reconnection is quick enough that the failure detector is not aware of it, then the server may not be
removed from the group. If it is a "long" connectivity problem, then the failure detector eventually suspects
a problem and the server is removed from the group.

Once a server is removed from the group, you need to join it back again. In other words, after a server is
removed explicitly from the group you need to rejoin it manually (or have a script doing it automatically).

3233

When is a member excluded from a group?

When is a member excluded from a group?

If the member becomes silent, the other members remove it from the group configuration. In practice this
may happen when the member has crashed or there is a network disconnection.

The failure is detected after a given timeout elapses for a given member and a new configuration without
the silent member in it is created.

What happens when one node is significantly lagging behind?

There is no method for defining policies for when to expel members automatically from the group. You
need to find out why a member is lagging behind and fix that or remove the member from the group.
Otherwise, if the server is so slow that it triggers the flow control, then the entire group slows down as well.
The flow control can be configured according to the your needs.

Upon suspicion of a problem in the group, is there a special member
responsible for triggering a reconfiguration?

No, there is no special member in the group in charge of triggering a reconfiguration.

Any member can suspect that there is a problem. All members need to (automatically) agree that a given
member has failed. One member is in charge of expelling it from the group, by triggering a reconfiguration.
Which member is responsible for expelling the member is not something you can control or set.

Can I use Group Replication for sharding?

Group Replication is designed to provide highly available replica sets; data and writes are duplicated
on each member in the group. For scaling beyond what a single system can provide, you need an
orchestration and sharding framework built around a number of Group Replication sets, where each replica
set maintains and manages a given shard or partition of your total dataset. This type of setup, often called
a “sharded cluster”, allows you to scale reads and writes linearly and without limit.

How do I use Group Replication with SELinux?

If SELinux is enabled, which you can verify using sestatus -v, then you need to enable the use of the
Group Replication communication port. See Setting the TCP Port Context for Group Replication.

How do I use Group Replication with iptables?

If iptables is enabled, then you need to open up the Group Replication port for communication between
the machines. To see the current rules in place on each machine, issue iptables -L. Assuming the port
configured is 33061, enable communication over the necessary port by issuing iptables -A INPUT -p
tcp --dport 33061 -j ACCEPT.

How do I recover the relay log for a replication channel used by a group
member?

The replication channels used by Group Replication behave in the same way as replication channels
used in source to replica replication, and as such rely on the relay log. In the event of a change of the
relay_log variable, or when the option is not set and the host name changes, there is a chance of errors.
See Section 16.2.4.1, “The Relay Log” for a recovery procedure in this situation. Alternatively, another way
of fixing the issue specifically in Group Replication is to issue a STOP GROUP_REPLICATION statement
and then a START GROUP_REPLICATION statement to restart the instance. The Group Replication plugin
creates the group_replication_applier channel again.

3234

Why does Group Replication use two bind addresses?

Why does Group Replication use two bind addresses?

Group Replication uses two bind addresses in order to split network traffic between the SQL address,
used by clients to communicate with the member, and the group_replication_local_address,
used internally by the group members to communicate. For example, assume a server with two
network interfaces assigned to the network addresses 203.0.113.1 and 198.51.100.179. In such
a situation you could use 203.0.113.1:33061 for the internal group network address by setting
group_replication_local_address=203.0.113.1:33061. Then you could use 198.51.100.179
for hostname and 3306 for the port. Client SQL applications would then connect to the member
at 198.51.100.179:3306. This enables you to configure different rules on the different networks.
Similarly, the internal group communication can be separated from the network connection used for client
applications, for increased security.

How does Group Replication use network addresses and hostnames?

Group Replication uses network connections between members and therefore its functionality is directly
impacted by how you configure hostnames and ports. For example, the Group Replication recovery
procedure is based on asynchronous replication which uses the server's hostname and port. When
a member joins a group it receives the group membership information, using the network address
information that is listed at performance_schema.replication_group_members. One of the
members listed in that table is selected as the donor of the missing data from the group to the new
member.

This means that any value you configure using a hostname, such as the SQL network address or the group
seeds address, must be a fully qualified name and resolvable by each member of the group. You can
ensure this for example through DNS, or correctly configured /etc/hosts files, or other local processes.
If a you want to configure the MEMBER_HOST value on a server, specify it using the --report-host
option on the server before joining it to the group.

Important

The assigned value is used directly and is not affected by the
skip_name_resolve system variable.

To configure MEMBER_PORT on a server, specify it using the report_port system variable.

Why did the auto increment setting on the server change?

When Group Replication is started on a server, the value of auto_increment_increment is changed
to the value of group_replication_auto_increment_increment, which defaults to 7, and the
value of auto_increment_offset is changed to the server ID. The changes are reverted when Group
Replication is stopped. These settings avoid the selection of duplicate auto-increment values for writes on
group members, which causes rollback of transactions. The default auto increment value of 7 for Group
Replication represents a balance between the number of usable values and the permitted maximum size of
a replication group (9 members).

The changes are only made and reverted if auto_increment_increment and
auto_increment_offset each have their default value of 1. If their values have already been modified
from the default, Group Replication does not alter them.

How do I find the primary?

If the group is operating in single-primary mode, it can be useful to find out which member is the primary.
See Section 17.5.1.3, “Finding the Primary”

3235

Group Replication Technical Details

17.9 Group Replication Technical Details

This section provides more technical details about MySQL Group Replication.

17.9.1 Group Replication Plugin Architecture

MySQL Group Replication is a MySQL plugin and it builds on the existing MySQL replication infrastructure,
taking advantage of features such as the binary log, row-based logging, and global transaction identifiers.
It integrates with current MySQL frameworks, such as the performance schema or plugin and service
infrastructures. The following figure presents a block diagram depicting the overall architecture of MySQL
Group Replication.

Figure 17.9 Group Replication Plugin Block Diagram

3236

The Group

The MySQL Group Replication plugin includes a set of APIs for capture, apply, and lifecycle, which control
how the plugin interacts with MySQL Server. There are interfaces to make information flow from the server
to the plugin and vice versa. These interfaces isolate the MySQL Server core from the Group Replication
plugin, and are mostly hooks placed in the transaction execution pipeline. In one direction, from server
to the plugin, there are notifications for events such as the server starting, the server recovering, the
server being ready to accept connections, and the server being about to commit a transaction. In the
other direction, the plugin instructs the server to perform actions such as committing or aborting ongoing
transactions, or queuing transactions in the relay log.

The next layer of the Group Replication plugin architecture is a set of components that react when a
notification is routed to them. The capture component is responsible for keeping track of context related to
transactions that are executing. The applier component is responsible for executing remote transactions
on the database. The recovery component manages distributed recovery, and is responsible for getting a
server that is joining the group up to date by selecting the donor, orchestrating the catch up procedure and
reacting to donor failures.

Continuing down the stack, the replication protocol module contains the specific logic of the replication
protocol. It handles conflict detection, and receives and propagates transactions to the group.

The final two layers of the Group Replication plugin architecture are the Group Communication System
(GCS) API, and an implementation of a Paxos-based group communication engine (XCom). The
GCS API is a high level API that abstracts the properties required to build a replicated state machine
(see Section 17.1, “Group Replication Background”). It therefore decouples the implementation of the
messaging layer from the remaining upper layers of the plugin. The group communication engine handles
communications with the members of the replication group.

17.9.2 The Group

In MySQL Group Replication, a set of servers forms a replication group. A group has a name, which takes
the form of a UUID. The group is dynamic and servers can leave (either voluntarily or involuntarily) and join
it at any time. The group adjusts itself whenever servers join or leave.

If a server joins the group, it automatically brings itself up to date by fetching the missing state from an
existing server. This state is transferred by means of Asynchronous MySQL replication. If a server leaves
the group, for instance it was taken down for maintenance, the remaining servers notice that it has left and
reconfigure the group automatically. The group membership service described at Section 17.1.3.1, “Group
Membership” powers all of this.

17.9.3 Data Manipulation Statements

As there are no primary servers (sources) for any particular data set, every server in the group is allowed
to execute transactions at any time, even transactions that change state (RW transactions).

Any server may execute a transaction without any a priori coordination. But, at commit time, it coordinates
with the rest of the servers in the group to reach a decision on the fate of that transaction. This coordination
serves two purposes: (i) check whether the transaction should commit or not; (ii) and propagate the
changes so that other servers can apply the transaction as well.

As a transaction is sent through an atomic broadcast, either all servers in the group receive the transaction
or none do. If they receive it, then they all receive it in the same order with respect to other transactions
that were sent before. Conflict detection is carried out by inspecting and comparing write sets of
transactions. Thus, they are detected at the row level. Conflict resolution follows the first committer wins
rule. If t1 and t2 execute concurrently at different sites, because t2 is ordered before t1, and both changed
the same row, then t2 wins the conflict and t1 aborts. In other words, t1 was trying to change data that had
been rendered stale by t2.

3237

Data Definition Statements

Note

If two transactions are bound to conflict more often than not, then it is a good
practice to start them on the same server. They then have a chance to synchronize
on the local lock manager instead of aborting later in the replication protocol.

17.9.4 Data Definition Statements

In a Group Replication topology, care needs to be taken when executing data definition statements
also commonly known as data definition language (DDL). Given that MySQL does not support atomic
or transactional DDL, one cannot optimistically execute DDL statements and later roll back if needs be.
Consequently, the lack of atomicity does not fit directly into the optimistic replication paradigm that Group
Replication is based on.

Therefore, more care needs to be taken when replicating data definition statements. Schema changes
and changes to the data that the object contains need to be handled through the same server while the
schema operation has not yet completed and replicated everywhere. Failure to do so can result in data
inconsistency.

Note

If the group is deployed in single-primary mode, then this is not a problem, because
all changes are performed through the same server, the primary.

Warning

MySQL DDL execution is not atomic or transactional. The server executes and
commits without securing group agreement first. As such, you must route DDL and
DML for the same object through the same server, while the DDL is executing and
has not replicated everywhere yet.

17.9.5 Distributed Recovery

This section describes the process through which a member joining a group catches up with the remaining
servers in the group, called distributed recovery. Distributed recovery can be summarized as the process
through which a server gets missing transactions from the group so that it can then join the group having
processed the same set of transactions as the other group members.

17.9.5.1 Distributed Recovery Basics

Whenever a member joins a replication group, it connects to an existing member to carry out state transfer.
The server joining the group transfers all the transactions that took place in the group before it joined,
which are provided by the existing member (called the donor). Next, the server joining the group applies
the transactions that took place in the group while this state transfer was in progress. When the server
joining the group has caught up with the remaining servers in the group, it begins to participate normally in
the group. This process is called distributed recovery.

In the first phase, the server joining the group selects one of the online servers on the group to be the
donor of the state that it is missing. The donor is responsible for providing the server joining the group all
the data it is missing up to the moment it has joined the group. This is achieved by relying on a standard
asynchronous replication channel, established between the donor and the server joining the group, see
Section 16.2.2, “Replication Channels”. Through this replication channel, the donor's binary logs are
replicated until the point that the view change happened when the server joining the group became part of
the group. The server joining the group applies the donor's binary logs as it receives them.

Phase 1

3238

Distributed Recovery

While the binary log is being replicated, the server joining the group also caches every transaction that is
exchanged within the group. In other words it is listening for transactions that are happening after it joined
the group and while it is applying the missing state from the donor. When the first phase ends and the
replication channel to the donor is closed, the server joining the group then starts phase two: the catch up.

Phase 2

In this phase, the server joining the group proceeds to the execution of the cached transactions. When the
number of transactions queued for execution finally reaches zero, the member is declared online.

Resilience

The recovery procedure withstands donor failures while the server joining the group is fetching binary
logs from it. In such cases, whenever a donor fails during phase 1, the server joining the group fails over
to a new donor and resumes from that one. When that happens the server joining the group closes the
connection to the failed server joining the group explicitly and opens a connection to a new donor. This
happens automatically.

17.9.5.2 Recovering From a Point-in-time

To synchronize the server joining the group with the donor up to a specific point in time, the server joining
the group and donor make use of the MySQL Global Transaction Identifiers (GTIDs) mechanism. See
Section 16.1.3, “Replication with Global Transaction Identifiers”. However, GTIDS only provide a means
to realize which transactions the server joining the group is missing, they do not help marking a specific
point in time to which the server joining the group must catch up, nor do they help conveying certification
information. This is the job of binary log view markers, which mark view changes in the binary log stream,
and also contain additional metadata information, provisioning the server joining the group with missing
certification related data.

View and View Changes

To explain the concept of view change markers, it is important to understand what a view and a view
change are.

A view corresponds to a group of members participating actively in the current configuration, in other words
at a specific point in time. They are correct and online in the system.

A view change occurs when a modification to the group configuration happens, such as a member joining
or leaving. Any group membership change results in an independent view change communicated to all
members at the same logical point in time.

A view identifier uniquely identifies a view. It is generated whenever a view change happens

At the group communication layer, view changes with their associated view ids are then boundaries
between the data exchanged before and after a member joins. This concept is implemented through a new
binary log event: the"view change log event". The view id thus becomes a marker as well for transactions
transmitted before and after changes happen in the group membership.

The view identifier itself is built from two parts: (i) one that is randomly generated and (ii) a monotonically
increasing integer. The first part is generated when the group is created, and remains unchanged while
there is at least one member in the group. The second part is incremented every time a view change
happens.

The reason for this heterogeneous pair that makes up the view id is the need to unambiguously mark
group changes whenever a member joins or leaves but also whenever all members leave the group and no
information remains of what view the group was in. In fact, the sole use of monotonic increasing identifiers

3239

Distributed Recovery

could lead to the reuse of the same id after full group shutdowns, destroying the uniqueness of the binary
log data markers that recovery depends on. To summarize, the first part identifies whenever the group was
started from the beginning and the incremental part when the group changed from that point on.

17.9.5.3 View Changes

This section explains the process which controls how the view change identifier is incorporated into a
binary log event and written to the log, The following steps are taken:

Begin: Stable Group

All servers are online and processing incoming transactions from the group. Some servers may be a little
behind in terms of transactions replicated, but eventually they converge. The group acts as one distributed
and replicated database.

Figure 17.10 Stable Group

View Change: a Member Joins

Whenever a new member joins the group and therefore a view change is performed, every online server
queues a view change log event for execution. This is queued because before the view change, several
transactions can be queued on the server to be applied and as such, these belong to the old view. Queuing
the view change event after them guarantees a correct marking of when this happened.

3240

Distributed Recovery

Meanwhile, the server joining the group selects the donor from the list of online servers as stated by the
membership service through the view abstraction. A member joins on view 4 and the online members write
a View change event to the binary log.

Figure 17.11 A Member Joins

State Transfer: Catching Up

Once the server joining the group has chosen which server in the group is to be the donor, a new
asynchronous replication connection is established between the two and the state transfer begins (phase
1). This interaction with the donor continues until the server joining the group's applier thread processes
the view change log event that corresponds to the view change triggered when the server joining the group
came into the group. In other words, the server joining the group replicates from the donor, until it gets to
the marker with the view identifier which matches the view marker it is already in.

3241

Distributed Recovery

Figure 17.12 State Transfer: Catching Up

As view identifiers are transmitted to all members in the group at the same logical time, the server
joining the group knows at which view identifier it should stop replicating. This avoids complex GTID set
calculations because the view id clearly marks which data belongs to each group view.

While the server joining the group is replicating from the donor, it is also caching incoming transactions
from the group. Eventually, it stops replicating from the donor and switches to applying those that are
cached.

3242

Distributed Recovery

Figure 17.13 Queued Transactions

Finish: Caught Up

When the server joining the group recognizes a view change log event with the expected view identifier,
the connection to the donor is terminated and it starts applying the cached transactions. An important point
to understand is the final recovery procedure. Although it acts as a marker in the binary log, delimiting
view changes, the view change log event also plays another role. It conveys the certification information
as perceived by all servers when the server joining the group entered the group, in other words the last
view change. Without it, the server joining the group would not have the necessary information to be able
to certify (detect conflicts) subsequent transactions.

3243

Distributed Recovery

The duration of the catch up (phase 2) is not deterministic, because it depends on the workload and
the rate of incoming transactions to the group. This process is completely online and the server joining
the group does not block any other server in the group while it is catching up. Therefore the number of
transactions the server joining the group is behind when it moves to phase 2 can, for this reason, vary and
thus increase or decrease according to the workload.

When the server joining the group reaches zero queued transactions and its stored data is equal to the
other members, its public state changes to online.

Figure 17.14 Instance Online

17.9.5.4 Usage Advice and Limitations of Distributed Recovery

Distributed recovery does have some limitations. It is based on classic asynchronous replication and as
such it may be slow if the server joining the group is not provisioned at all or is provisioned with a very
old backup image. This means that if the data to transfer is too big at phase 1, the server may take a very
long time to recover. As such, the recommendation is that before adding a server to the group, one should
provision it with a fairly recent snapshot of a server already in the group. This minimizes the length of
phase 1 and reduces the impact on the donor server, since it has to save and transfer less binary logs.

Warning

It is recommended that a server is provisioned before it is added to a group. That
way, one minimizes the time spent on the recovery step.

3244

17.9.6 Observability

Observability

There is a lot of automation built into the Group Replication plugin. Nonetheless, you might sometimes
need to understand what is happening behind the scenes. This is where the instrumentation of Group
Replication and Performance Schema becomes important. The entire state of the system (including the
view, conflict statistics and service states) can be queried through performance_schema tables. The
distributed nature of the replication protocol and the fact that server instances agree and thus synchronize
on transactions and metadata makes it simpler to inspect the state of the group. For example, you can
connect to a single server in the group and obtain both local and global information by issuing select
statements on the Group Replication related Performance Schema tables. For more information, see
Section 17.4, “Monitoring Group Replication”.

17.9.7 Group Replication Performance

This section explains how to use the available configuration options to gain the best performance from your
group.

17.9.7.1 Fine Tuning the Group Communication Thread

The group communication thread (GCT) runs in a loop while the Group Replication plugin is loaded. The
GCT receives messages from the group and from the plugin, handles quorum and failure detection related
tasks, sends out some keep alive messages and also handles the incoming and outgoing transactions
from/to the server/group. The GCT waits for incoming messages in a queue. When there are no messages,
the GCT waits. By configuring this wait to be a little longer (doing an active wait) before actually going to
sleep can prove to be beneficial in some cases. This is because the alternative is for the operating system
to switch out the GCT from the processor and do a context switch.

To force the GCT do an active wait, use the group_replication_poll_spin_loops option, which
makes the GCT loop, doing nothing relevant for the configured number of loops, before actually polling the
queue for the next message.

For example:

mysql> SET GLOBAL group_replication_poll_spin_loops= 10000;

17.9.7.2 Message Compression

For messages sent between online group members, Group Replication enables message compression
by default. Whether a specific message is compressed depends on the threshold that you configure using
the group_replication_compression_threshold system variable. Messages that have a payload
larger than the specified number of bytes are compressed.

The default compression threshold is 1000000 bytes. You could use the following statements to increase
the compression threshold to 2MB, for example:

STOP GROUP_REPLICATION;
SET GLOBAL group_replication_compression_threshold = 2097152;
START GROUP_REPLICATION;

If you set group_replication_compression_threshold to zero, message compression is disabled.

Group Replication uses the LZ4 compression algorithm to compress messages sent in the group. Note
that the maximum supported input size for the LZ4 compression algorithm is 2113929216 bytes. This limit
is lower than the maximum possible value for the group_replication_compression_threshold

3245

Group Replication Performance

system variable, which is matched to the maximum message size accepted by XCom. The LZ4 maximum
input size is therefore a practical limit for message compression, and transactions above this size cannot
be committed when message compression is enabled. With the LZ4 compression algorithm, do not set a
value greater than 2113929216 bytes for group_replication_compression_threshold.

The value of group_replication_compression_threshold is not required by Group Replication to
be the same on all group members. However, it is advisable to set the same value on all group members
in order to avoid unnecessary rollback of transactions, failure of message delivery, or failure of message
recovery.

Compression for messages sent in the group happens at the group communication engine level,
before the data is handed over to the group communication thread, so it takes place within the
context of the mysql user session thread. If the message payload size exceeds the threshold set by
group_replication_compression_threshold, the transaction payload is compressed before
being sent out to the group, and decompressed when it is received. Upon receiving a message, the
member checks the message envelope to verify whether it is compressed or not. If needed, then the
member decompresses the transaction, before delivering it to the upper layer. This process is shown in the
following figure.

3246

Group Replication Performance

Figure 17.15 Compression Support

When network bandwidth is a bottleneck, message compression can provide up to 30-40% throughput
improvement at the group communication level. This is especially important within the context of large
groups of servers under load. The TCP peer-to-peer nature of the interconnections between N participants
in the group makes the sender send the same amount of data N times. Furthermore, binary logs are likely
to exhibit a high compression ratio. This makes compression a compelling feature for Group Replication
workloads that contain large transactions.

17.9.7.3 Flow Control

Group Replication ensures that a transaction only commits after a majority of the members in a group have
received it and agreed on the relative order between all transactions that were sent concurrently.

3247

Group Replication Performance

This approach works well if the total number of writes to the group does not exceed the write capacity of
any member in the group. If it does and some of the members have less write throughput than others,
particularly less than the writer members, those members can start lagging behind of the writers.

Having some members lagging behind the group brings some problematic consequences, particularly, the
reads on such members may externalize very old data. Depending on why the member is lagging behind,
other members in the group may have to save more or less replication context to be able to fulfil potential
data transfer requests from the slow member.

There is however a mechanism in the replication protocol to avoid having too much distance, in terms of
transactions applied, between fast and slow members. This is known as the flow control mechanism. It
tries to address several goals:

1.

to keep the members close enough to make buffering and de-synchronization between members a
small problem;

2.

to adapt quickly to changing conditions like different workloads or more writers in the group;

3.

to give each member a fair share of the available write capacity;

4.

to not reduce throughput more than strictly necessary to avoid wasting resources.

Given the design of Group Replication, the decision whether to throttle or not may be decided taking into
account two work queues: (i) the certification queue; (ii) and on the binary log applier queue. Whenever
the size of one of these queues exceeds the user-defined threshold, the throttling mechanism is triggered.
Only configure: (i) whether to do flow control at the certifier or at the applier level, or both; and (ii) what is
the threshold for each queue.

The flow control depends on two basic mechanisms:

1.

the monitoring of members to collect some statistics on throughput and queue sizes of all group
members to make educated guesses on what is the maximum write pressure each member should be
subjected to;

2.

the throttling of members that are trying to write beyond their fair-share of the available capacity at each
moment in time.

Probes and Statistics

The monitoring mechanism works by having each member deploying a set of probes to collect information
about its work queues and throughput. It then propagates that information to the group periodically to share
that data with the other members.

Such probes are scattered throughout the plugin stack and allow one to establish metrics, such as:

• the certifier queue size;

• the replication applier queue size;

• the total number of transactions certified;

• the total number of remote transactions applied in the member;

• the total number of local transactions.

Once a member receives a message with statistics from another member, it calculates additional metrics
regarding how many transactions were certified, applied and locally executed in the last monitoring period.

3248

Group Replication Performance

Monitoring data is shared with others in the group periodically. The monitoring period must be high enough
to allow the other members to decide on the current write requests, but low enough that it has minimal
impact on group bandwidth. The information is shared every second, and this period is sufficient to address
both concerns.

Group Replication Throttling

Based on the metrics gathered across all servers in the group, a throttling mechanism kicks in and decides
whether to limit the rate a member is able to execute/commit new transactions.

Therefore, metrics acquired from all members are the basis for calculating the capacity of each member:
if a member has a large queue (for certification or the applier thread), then the capacity to execute new
transactions should be close to ones certified or applied in the last period.

The lowest capacity of all the members in the group determines the real capacity of the group, while the
number of local transactions determines how many members are writing to it, and, consequently, how
many members should that available capacity be shared with.

This means that every member has an established write quota based on the available capacity, in other
words a number of transactions it can safely issue for the next period. The writer quota is enforced by
the throttling mechanism if the queue size of the certifier or the binary log applier exceeds a user defined
threshold.

The quota is reduced by the number of transactions that were delayed in the last period, and then also
further reduced by 10% to allow the queue that triggered the problem to reduce its size. In order to avoid
large jumps in throughput once the queue size goes beyond the threshold, the throughput is only allowed
to grow by the same 10% per period after that.

The current throttling mechanism does not penalize transactions below quota, but delays finishing those
transactions that exceed it until the end of the monitoring period. As a consequence, if the quota is very
small for the write requests issued some transactions may have latencies close to the monitoring period.

3249

3250

