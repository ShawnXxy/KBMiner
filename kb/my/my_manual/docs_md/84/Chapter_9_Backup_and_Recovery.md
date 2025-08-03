Backup and Recovery Types

• For additional information about InnoDB backup procedures, see Section 17.18.1, “InnoDB Backup”.

• Replication enables you to maintain identical data on multiple servers. This has several benefits,

such as enabling client query load to be distributed over servers, availability of data even if a given
server is taken offline or fails, and the ability to make backups with no impact on the source by using
a replica. See Chapter 19, Replication.

• MySQL InnoDB Cluster is a collection of products that work together to provide a high availability

solution. A group of MySQL servers can be configured to create a cluster using MySQL Shell. The
cluster of servers has a single source, called the primary, which acts as the read-write source.
Multiple secondary servers are replicas of the source. A minimum of three servers are required to
create a high availability cluster. A client application is connected to the primary via MySQL Router.
If the primary fails, a secondary is automatically promoted to the role of primary, and MySQL Router
routes requests to the new primary.

• NDB Cluster provides a high-availability, high-redundancy version of MySQL adapted for the

distributed computing environment. See Chapter 25, MySQL NDB Cluster 8.4, which provides
information about MySQL NDB Cluster 8.4.5.

9.1 Backup and Recovery Types

This section describes the characteristics of different types of backups.

Physical (Raw) Versus Logical Backups

Physical backups consist of raw copies of the directories and files that store database contents. This
type of backup is suitable for large, important databases that need to be recovered quickly when
problems occur.

Logical backups save information represented as logical database structure (CREATE DATABASE,
CREATE TABLE statements) and content (INSERT statements or delimited-text files). This type of
backup is suitable for smaller amounts of data where you might edit the data values or table structure,
or recreate the data on a different machine architecture.

Physical backup methods have these characteristics:

• The backup consists of exact copies of database directories and files. Typically this is a copy of all or

part of the MySQL data directory.

• Physical backup methods are faster than logical because they involve only file copying without

conversion.

• Output is more compact than for logical backup.

• Because backup speed and compactness are important for busy, important databases, the MySQL
Enterprise Backup product performs physical backups. For an overview of the MySQL Enterprise
Backup product, see Section 32.1, “MySQL Enterprise Backup Overview”.

• Backup and restore granularity ranges from the level of the entire data directory down to the level of
individual files. This may or may not provide for table-level granularity, depending on storage engine.
For example, InnoDB tables can each be in a separate file, or share file storage with other InnoDB
tables; each MyISAM table corresponds uniquely to a set of files.

• In addition to databases, the backup can include any related files such as log or configuration files.

• Data from MEMORY tables is tricky to back up this way because their contents are not stored on disk.
(The MySQL Enterprise Backup product has a feature where you can retrieve data from MEMORY
tables during a backup.)

• Backups are portable only to other machines that have identical or similar hardware characteristics.

1614

Reloading SQL-Format Backups

were not included in the partial dump. If you only replay one partial dump file on the target server,
the extra GTIDs do not cause any problems with the future operation of that server. However, if you
replay a second dump file on the target server that contains the same GTIDs (for example, another
partial dump from the same source server), any SET @@GLOBAL.gtid_purged statement in the
second dump file fails. To avoid this issue, either set the mysqldump option --set-gtid-purged to
OFF or COMMENTED to output the second dump file without an active SET @@GLOBAL.gtid_purged
statement, or remove the statement manually before replaying the dump file.

9.4.2 Reloading SQL-Format Backups

To reload a dump file written by mysqldump that consists of SQL statements, use it as input to
the mysql client. If the dump file was created by mysqldump with the --all-databases or --
databases option, it contains CREATE DATABASE and USE statements and it is not necessary to
specify a default database into which to load the data:

$> mysql < dump.sql

Alternatively, from within mysql, use a source command:

mysql> source dump.sql

If the file is a single-database dump not containing CREATE DATABASE and USE statements, create the
database first (if necessary):

$> mysqladmin create db1

Then specify the database name when you load the dump file:

$> mysql db1 < dump.sql

Alternatively, from within mysql, create the database, select it as the default database, and load the
dump file:

mysql> CREATE DATABASE IF NOT EXISTS db1;
mysql> USE db1;
mysql> source dump.sql

Note

For Windows PowerShell users: Because the "<" character is reserved for future
use in PowerShell, an alternative approach is required, such as using quotes
cmd.exe /c "mysql < dump.sql".

9.4.3 Dumping Data in Delimited-Text Format with mysqldump

This section describes how to use mysqldump to create delimited-text dump files. For information
about reloading such dump files, see Section 9.4.4, “Reloading Delimited-Text Format Backups”.

If you invoke mysqldump with the --tab=dir_name option, it uses dir_name as the output directory
and dumps tables individually in that directory using two files for each table. The table name is the base
name for these files. For a table named t1, the files are named t1.sql and t1.txt. The .sql file
contains a CREATE TABLE statement for the table. The .txt file contains the table data, one line per
table row.

The following command dumps the contents of the db1 database to files in the /tmp database:

$> mysqldump --tab=/tmp db1

The .txt files containing table data are written by the server, so they are owned by the system
account used for running the server. The server uses SELECT ... INTO OUTFILE to write the files,
so you must have the FILE privilege to perform this operation, and an error occurs if a given .txt file
already exists.

1624

mysqldump Tips

$> mysql db1 < t1.sql
$> mysqlimport db1 t1.txt

An alternative to using mysqlimport to load the data file is to use the LOAD DATA statement from
within the mysql client:

mysql> USE db1;
mysql> LOAD DATA INFILE 't1.txt' INTO TABLE t1;

If you used any data-formatting options with mysqldump when you initially dumped the table, you must
use the same options with mysqlimport or LOAD DATA to ensure proper interpretation of the data file
contents:

$> mysqlimport --fields-terminated-by=,
         --fields-enclosed-by='"' --lines-terminated-by=0x0d0a db1 t1.txt

Or:

mysql> USE db1;
mysql> LOAD DATA INFILE 't1.txt' INTO TABLE t1
       FIELDS TERMINATED BY ',' FIELDS ENCLOSED BY '"'
       LINES TERMINATED BY '\r\n';

9.4.5 mysqldump Tips

This section surveys techniques that enable you to use mysqldump to solve specific problems:

• How to make a copy a database

• How to copy a database from one server to another

• How to dump stored programs (stored procedures and functions, triggers, and events)

• How to dump definitions and data separately

9.4.5.1 Making a Copy of a Database

$> mysqldump db1 > dump.sql
$> mysqladmin create db2
$> mysql db2 < dump.sql

Do not use --databases on the mysqldump command line because that causes USE db1 to be
included in the dump file, which overrides the effect of naming db2 on the mysql command line.

9.4.5.2 Copy a Database from one Server to Another

On Server 1:

$> mysqldump --databases db1 > dump.sql

Copy the dump file from Server 1 to Server 2.

On Server 2:

$> mysql < dump.sql

Use of --databases with the mysqldump command line causes the dump file to include CREATE
DATABASE and USE statements that create the database if it does exist and make it the default
database for the reloaded data.

Alternatively, you can omit --databases from the mysqldump command. Then you need to create
the database on Server 2 (if necessary) and specify it as the default database when you reload the
dump file.

On Server 1:

1626

mysqldump Tips

$> mysqldump db1 > dump.sql

On Server 2:

$> mysqladmin create db1
$> mysql db1 < dump.sql

You can specify a different database name in this case, so omitting --databases from the
mysqldump command enables you to dump data from one database and load it into another.

9.4.5.3 Dumping Stored Programs

Several options control how mysqldump handles stored programs (stored procedures and functions,
triggers, and events):

• --events: Dump Event Scheduler events

• --routines: Dump stored procedures and functions

• --triggers: Dump triggers for tables

The --triggers option is enabled by default so that when tables are dumped, they are accompanied
by any triggers they have. The other options are disabled by default and must be specified explicitly to
dump the corresponding objects. To disable any of these options explicitly, use its skip form: --skip-
events, --skip-routines, or --skip-triggers.

9.4.5.4 Dumping Table Definitions and Content Separately

The --no-data option tells mysqldump not to dump table data, resulting in the dump file containing
only statements to create the tables. Conversely, the --no-create-info option tells mysqldump to
suppress CREATE statements from the output, so that the dump file contains only table data.

For example, to dump table definitions and data separately for the test database, use these
commands:

$> mysqldump --no-data test > dump-defs.sql
$> mysqldump --no-create-info test > dump-data.sql

For a definition-only dump, add the --routines and --events options to also include stored routine
and event definitions:

$> mysqldump --no-data --routines --events test > dump-defs.sql

9.4.5.5 Using mysqldump to Test for Upgrade Incompatibilities

When contemplating a MySQL upgrade, it is prudent to install the newer version separately from your
current production version. Then you can dump the database and database object definitions from the
production server and load them into the new server to verify that they are handled properly. (This is
also useful for testing downgrades.)

On the production server:

$> mysqldump --all-databases --no-data --routines --events > dump-defs.sql

On the upgraded server:

$> mysql < dump-defs.sql

Because the dump file does not contain table data, it can be processed quickly. This enables you to
spot potential incompatibilities without waiting for lengthy data-loading operations. Look for warnings or
errors while the dump file is being processed.

After you have verified that the definitions are handled properly, dump the data and try to load it into the
upgraded server.

1627

Point-in-Time (Incremental) Recovery

On the production server:

$> mysqldump --all-databases --no-create-info > dump-data.sql

On the upgraded server:

$> mysql < dump-data.sql

Now check the table contents and run some test queries.

9.5 Point-in-Time (Incremental) Recovery

Point-in-time recovery refers to recovery of data changes up to a given point in time. Typically, this type
of recovery is performed after restoring a full backup that brings the server to its state as of the time the
backup was made. (The full backup can be made in several ways, such as those listed in Section 9.2,
“Database Backup Methods”.) Point-in-time recovery then brings the server up to date incrementally
from the time of the full backup to a more recent time.

9.5.1 Point-in-Time Recovery Using Binary Log

This section explains the general idea of using the binary log to perform a point-in-time-recovery. The
next section, Section 9.5.2, “Point-in-Time Recovery Using Event Positions”, explains the operation in
details with an example.

Note

Many of the examples in this and the next section use the mysql client to
process binary log output produced by mysqlbinlog. If your binary log
contains \0 (null) characters, that output cannot be parsed by mysql unless
you invoke it with the --binary-mode option.

The source of information for point-in-time recovery is the set of binary log files generated subsequent
to the full backup operation. Therefore, to allow a server to be restored to a point-in-time, binary logging
must be enabled on it, which is the default setting for MySQL 8.4 (see Section 7.4.4, “The Binary Log”).

To restore data from the binary log, you must know the name and location of the current binary log
files. By default, the server creates binary log files in the data directory, but a path name can be
specified with the --log-bin option to place the files in a different location. To see a listing of all
binary log files, use this statement:

mysql> SHOW BINARY LOGS;

To determine the name of the current binary log file, issue the following statement:

mysql> SHOW BINARY LOG STATUS;

The mysqlbinlog utility converts the events in the binary log files from binary format to text so that
they can be viewed or applied. mysqlbinlog has options for selecting sections of the binary log
based on event times or position of events within the log. See Section 6.6.9, “mysqlbinlog — Utility for
Processing Binary Log Files”.

Applying events from the binary log causes the data modifications they represent to be reexecuted.
This enables recovery of data changes for a given span of time. To apply events from the binary log,
process mysqlbinlog output using the mysql client:

$> mysqlbinlog binlog_files | mysql -u root -p

If binary log files have been encrypted, mysqlbinlog cannot read them directly as in the previous
example, but can read them from the server using the --read-from-remote-server (-R) option.
For example:

1628

Point-in-Time Recovery Using Event Positions

$> mysqlbinlog --read-from-remote-server --host=host_name --port=3306  --user=root --password --ssl-mode=required  binlog_files | mysql -u root -p

Here, the option --ssl-mode=required has been used to ensure that the data from the binary log
files is protected in transit, because it is sent to mysqlbinlog in an unencrypted format.

Important

VERIFY_CA and VERIFY_IDENTITY are better choices than REQUIRED for the
SSL mode, because they help prevent man-in-the-middle attacks. To implement
one of these settings, you must first ensure that the CA certificate for the server
is reliably available to all the clients that use it in your environment, otherwise
availability issues will result. See Command Options for Encrypted Connections.

Viewing log contents can be useful when you need to determine event times or positions to select
partial log contents prior to executing events. To view events from the log, send mysqlbinlog output
into a paging program:

$> mysqlbinlog binlog_files | more

Alternatively, save the output in a file and view the file in a text editor:

$> mysqlbinlog binlog_files > tmpfile
$> ... edit tmpfile ...

After editing the file, apply the contents as follows:

$> mysql -u root -p < tmpfile

If you have more than one binary log to apply on the MySQL server, use a single connection to apply
the contents of all binary log files that you want to process. Here is one way to do so:

$> mysqlbinlog binlog.000001 binlog.000002 | mysql -u root -p

Another approach is to write the whole log to a single file and then process the file:

$> mysqlbinlog binlog.000001 >  /tmp/statements.sql
$> mysqlbinlog binlog.000002 >> /tmp/statements.sql
$> mysql -u root -p -e "source /tmp/statements.sql"

9.5.2 Point-in-Time Recovery Using Event Positions

The last section, Section 9.5.1, “Point-in-Time Recovery Using Binary Log”, explains the general idea
of using the binary log to perform a point-in-time-recovery. The section explains the operation in details
with an example.

As an example, suppose that around 20:06:00 on March 11, 2020, an SQL statement was executed
that deleted a table. You can perform a point-in-time recovery to restore the server up to its state right
before the table deletion. These are some sample steps to achieve that:

1. Restore the last full backup created before the point-in-time of interest (call it tp, which is 20:06:00
on March 11, 2020 in our example). When finished, note the binary log position up to which you
have restored the server for later use, and restart the server.

Note

While the last binary log position recovered is also displayed by InnoDB
after the restore and server restart, that is not a reliable means for obtaining
the ending log position of your restore, as there could be DDL events and
non-InnoDB changes that have taken place after the time reflected by the
displayed position. Your backup and restore tool should provide you with
the last binary log position for your recovery: for example, if you are using
mysqlbinlog for the task, check the stop position of the binary log replay;

1629

Point-in-Time Recovery Using Event Positions

if you are using MySQL Enterprise Backup, the last binary log position has
been saved in your backup. See Point-in-Time Recovery.

2. Find the precise binary log event position corresponding to the point in time up to which you want to
restore your database. In our example, given that we know the rough time where the table deletion
took place (tp), we can find the log position by checking the log contents around that time using the
mysqlbinlog utility. Use the --start-datetime and --stop-datetime options to specify a
short time period around tp, and then look for the event in the output. For example:

$> mysqlbinlog --start-datetime="2020-03-11 20:05:00" \
                   --stop-datetime="2020-03-11 20:08:00" --verbose \
         /var/lib/mysql/bin.123456 | grep -C 15 "DROP TABLE"

/*!80014 SET @@session.original_server_version=80019*//*!*/;
/*!80014 SET @@session.immediate_server_version=80019*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 232
#200311 20:06:20 server id 1  end_log_pos 355 CRC32 0x2fc1e5ea  Query thread_id=16 exec_time=0 error_code=0
SET TIMESTAMP=1583971580/*!*/;
SET @@session.pseudo_thread_id=16/*!*/;
SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
SET @@session.sql_mode=1168113696/*!*/;
SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
/*!\C utf8mb4 *//*!*/;
SET @@session.character_set_client=255,@@session.collation_connection=255,@@session.collation_server=255/*!*/;
SET @@session.lc_time_names=0/*!*/;
SET @@session.collation_database=DEFAULT/*!*/;
/*!80011 SET @@session.default_collation_for_utf8mb4=255*//*!*/;
DROP TABLE `pets`.`cats` /* generated by server */
/*!*/;
# at 355
#200311 20:07:48 server id 1  end_log_pos 434 CRC32 0x123d65df  Anonymous_GTID last_committed=1 sequence_number=2 rbr_only=no original_committed_timestamp=1583971668462467 immediate_commit_timestamp=1583971668462467 transaction_length=473
# original_commit_timestamp=1583971668462467 (2020-03-11 20:07:48.462467 EDT)
# immediate_commit_timestamp=1583971668462467 (2020-03-11 20:07:48.462467 EDT)
/*!80001 SET @@session.original_commit_timestamp=1583971668462467*//*!*/;
/*!80014 SET @@session.original_server_version=80019*//*!*/;
/*!80014 SET @@session.immediate_server_version=80019*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 434
#200311 20:07:48 server id 1  end_log_pos 828 CRC32 0x57fac9ac  Query thread_id=16 exec_time=0 error_code=0 Xid = 217
use `pets`/*!*/;
SET TIMESTAMP=1583971668/*!*/;
/*!80013 SET @@session.sql_require_primary_key=0*//*!*/;
CREATE TABLE dogs

From the output of mysqlbinlog, the DROP TABLE `pets`.`cats` statement can be found
in the segment of the binary log between the line # at 232 and # at 355, which means the
statement takes place after the log position 232, and the log is at position 355 after the DROP
TABLE statement.

Note

Only use the --start-datetime and --stop-datetime options to
help you find the actual event positions of interest. Using the two options to
specify the range of binary log segment to apply is not recommended: there
is a higher risk of missing binary log events when using the options. Use --
start-position and --stop-position instead.

3. Apply the events in binary log file to the server, starting with the log position your found in step 1

(assume it is 155) and ending at the position you have found in step 2 that is before your point-in-
time of interest (which is 232):

$> mysqlbinlog --start-position=155 --stop-position=232 /var/lib/mysql/bin.123456 \
         | mysql -u root -p

The command recovers all the transactions from the starting position until just before the stop
position. Because the output of mysqlbinlog includes SET TIMESTAMP statements before each

1630

MyISAM Table Maintenance and Crash Recovery

SQL statement recorded, the recovered data and related MySQL logs reflect the original times at
which the transactions were executed.

Your database has now been restored to the point-in-time of interest, tp, right before the table
pets.cats was dropped.

4. Beyond the point-in-time recovery that has been finished, if you also want to reexecute all the

statements after your point-in-time of interest, use mysqlbinlog again to apply all the events after
tp to the server. We noted in step 2 that after the statement we wanted to skip, the log is at position
355; we can use it for the --start-position option, so that any statements after the position are
included:

$> mysqlbinlog --start-position=355 /var/lib/mysql/bin.123456 \
         | mysql -u root -p

Your database has been restored the latest statement recorded in the binary log file, but with the
selected event skipped.

9.6 MyISAM Table Maintenance and Crash Recovery

This section discusses how to use myisamchk to check or repair MyISAM tables (tables that have
.MYD and .MYI files for storing data and indexes). For general myisamchk background, see
Section 6.6.4, “myisamchk — MyISAM Table-Maintenance Utility”. Other table-repair information can
be found at Section 3.14, “Rebuilding or Repairing Tables or Indexes”.

You can use myisamchk to check, repair, or optimize database tables. The following sections describe
how to perform these operations and how to set up a table maintenance schedule. For information
about using myisamchk to get information about your tables, see Section 6.6.4.5, “Obtaining Table
Information with myisamchk”.

Even though table repair with myisamchk is quite secure, it is always a good idea to make a backup
before doing a repair or any maintenance operation that could make a lot of changes to a table.

myisamchk operations that affect indexes can cause MyISAM FULLTEXT indexes to be rebuilt with
full-text parameters that are incompatible with the values used by the MySQL server. To avoid this
problem, follow the guidelines in Section 6.6.4.1, “myisamchk General Options”.

MyISAM table maintenance can also be done using the SQL statements that perform operations similar
to what myisamchk can do:

• To check MyISAM tables, use CHECK TABLE.

• To repair MyISAM tables, use REPAIR TABLE.

• To optimize MyISAM tables, use OPTIMIZE TABLE.

• To analyze MyISAM tables, use ANALYZE TABLE.

For additional information about these statements, see Section 15.7.3, “Table Maintenance
Statements”.

These statements can be used directly or by means of the mysqlcheck client program. One
advantage of these statements over myisamchk is that the server does all the work. With myisamchk,
you must make sure that the server does not use the tables at the same time so that there is no
unwanted interaction between myisamchk and the server.

9.6.1 Using myisamchk for Crash Recovery

This section describes how to check for and deal with data corruption in MySQL databases. If your
tables become corrupted frequently, you should try to find the reason why. See Section B.3.3.3, “What
to Do If MySQL Keeps Crashing”.

1631

How to Check MyISAM Tables for Errors

For an explanation of how MyISAM tables can become corrupted, see Section 18.2.4, “MyISAM Table
Problems”.

If you run mysqld with external locking disabled (which is the default), you cannot reliably use
myisamchk to check a table when mysqld is using the same table. If you can be certain that no
one can access the tables using mysqld while you run myisamchk, you only have to execute
mysqladmin flush-tables before you start checking the tables. If you cannot guarantee this, you
must stop mysqld while you check the tables. If you run myisamchk to check tables that mysqld is
updating at the same time, you may get a warning that a table is corrupt even when it is not.

If the server is run with external locking enabled, you can use myisamchk to check tables at any
time. In this case, if the server tries to update a table that myisamchk is using, the server waits for
myisamchk to finish before it continues.

If you use myisamchk to repair or optimize tables, you must always ensure that the mysqld server
is not using the table (this also applies if external locking is disabled). If you do not stop mysqld, you
should at least do a mysqladmin flush-tables before you run myisamchk. Your tables may
become corrupted if the server and myisamchk access the tables simultaneously.

When performing crash recovery, it is important to understand that each MyISAM table tbl_name in a
database corresponds to the three files in the database directory shown in the following table.

File

tbl_name.MYD

tbl_name.MYI

Purpose

Data file

Index file

Each of these three file types is subject to corruption in various ways, but problems occur most often in
data files and index files.

myisamchk works by creating a copy of the .MYD data file row by row. It ends the repair stage by
removing the old .MYD file and renaming the new file to the original file name. If you use --quick,
myisamchk does not create a temporary .MYD file, but instead assumes that the .MYD file is correct
and generates only a new index file without touching the .MYD file. This is safe, because myisamchk
automatically detects whether the .MYD file is corrupt and aborts the repair if it is. You can also specify
the --quick option twice to myisamchk. In this case, myisamchk does not abort on some errors
(such as duplicate-key errors) but instead tries to resolve them by modifying the .MYD file. Normally
the use of two --quick options is useful only if you have too little free disk space to perform a normal
repair. In this case, you should at least make a backup of the table before running myisamchk.

9.6.2 How to Check MyISAM Tables for Errors

To check a MyISAM table, use the following commands:

• myisamchk tbl_name

This finds 99.99% of all errors. What it cannot find is corruption that involves only the data file (which
is very unusual). If you want to check a table, you should normally run myisamchk without options or
with the -s (silent) option.

• myisamchk -m tbl_name

This finds 99.999% of all errors. It first checks all index entries for errors and then reads through all
rows. It calculates a checksum for all key values in the rows and verifies that the checksum matches
the checksum for the keys in the index tree.

• myisamchk -e tbl_name

This does a complete and thorough check of all data (-e means “extended check”). It does a check-
read of every key for each row to verify that they indeed point to the correct row. This may take a

1632

How to Repair MyISAM Tables

long time for a large table that has many indexes. Normally, myisamchk stops after the first error
it finds. If you want to obtain more information, you can add the -v (verbose) option. This causes
myisamchk to keep going, up through a maximum of 20 errors.

• myisamchk -e -i tbl_name

This is like the previous command, but the -i option tells myisamchk to print additional statistical
information.

In most cases, a simple myisamchk command with no arguments other than the table name is
sufficient to check a table.

9.6.3 How to Repair MyISAM Tables

The discussion in this section describes how to use myisamchk on MyISAM tables (extensions .MYI
and .MYD).

You can also use the CHECK TABLE and REPAIR TABLE statements to check and repair MyISAM
tables. See Section 15.7.3.2, “CHECK TABLE Statement”, and Section 15.7.3.5, “REPAIR TABLE
Statement”.

Symptoms of corrupted tables include queries that abort unexpectedly and observable errors such as
these:

• Can't find file tbl_name.MYI (Errcode: nnn)

• Unexpected end of file

• Record file is crashed

• Got error nnn from table handler

To get more information about the error, run perror nnn, where nnn is the error number. The
following example shows how to use perror to find the meanings for the most common error numbers
that indicate a problem with a table:

$> perror 126 127 132 134 135 136 141 144 145
MySQL error code 126 = Index file is crashed
MySQL error code 127 = Record-file is crashed
MySQL error code 132 = Old database file
MySQL error code 134 = Record was already deleted (or record file crashed)
MySQL error code 135 = No more room in record file
MySQL error code 136 = No more room in index file
MySQL error code 141 = Duplicate unique key or constraint on write or update
MySQL error code 144 = Table is crashed and last repair failed
MySQL error code 145 = Table was marked as crashed and should be repaired

Note that error 135 (no more room in record file) and error 136 (no more room in index file) are not
errors that can be fixed by a simple repair. In this case, you must use ALTER TABLE to increase the
MAX_ROWS and AVG_ROW_LENGTH table option values:

ALTER TABLE tbl_name MAX_ROWS=xxx AVG_ROW_LENGTH=yyy;

If you do not know the current table option values, use SHOW CREATE TABLE.

For the other errors, you must repair your tables. myisamchk can usually detect and fix most problems
that occur.

The repair process involves up to three stages, described here. Before you begin, you should change
location to the database directory and check the permissions of the table files. On Unix, make sure that
they are readable by the user that mysqld runs as (and to you, because you need to access the files
you are checking). If it turns out you need to modify files, they must also be writable by you.

1633

How to Repair MyISAM Tables

This section is for the cases where a table check fails (such as those described in Section 9.6.2, “How
to Check MyISAM Tables for Errors”), or you want to use the extended features that myisamchk
provides.

The myisamchk options used for table maintenance with are described in Section 6.6.4, “myisamchk
— MyISAM Table-Maintenance Utility”. myisamchk also has variables that you can set to control
memory allocation that may improve performance. See Section 6.6.4.6, “myisamchk Memory Usage”.

If you are going to repair a table from the command line, you must first stop the mysqld server. Note
that when you do mysqladmin shutdown on a remote server, the mysqld server is still available for
a while after mysqladmin returns, until all statement-processing has stopped and all index changes
have been flushed to disk.

Stage 1: Checking your tables

Run myisamchk *.MYI or myisamchk -e *.MYI if you have more time. Use the -s (silent) option
to suppress unnecessary information.

If the mysqld server is stopped, you should use the --update-state option to tell myisamchk to
mark the table as “checked.”

You have to repair only those tables for which myisamchk announces an error. For such tables,
proceed to Stage 2.

If you get unexpected errors when checking (such as out of memory errors), or if myisamchk
crashes, go to Stage 3.

Stage 2: Easy safe repair

First, try myisamchk -r -q tbl_name (-r -q means “quick recovery mode”). This attempts to
repair the index file without touching the data file. If the data file contains everything that it should and
the delete links point at the correct locations within the data file, this should work, and the table is fixed.
Start repairing the next table. Otherwise, use the following procedure:

1. Make a backup of the data file before continuing.

2. Use myisamchk -r tbl_name (-r means “recovery mode”). This removes incorrect rows and

deleted rows from the data file and reconstructs the index file.

3.

If the preceding step fails, use myisamchk --safe-recover tbl_name. Safe recovery mode
uses an old recovery method that handles a few cases that regular recovery mode does not (but is
slower).

Note

If you want a repair operation to go much faster, you should set the values of
the sort_buffer_size and key_buffer_size variables each to about 25%
of your available memory when running myisamchk.

If you get unexpected errors when repairing (such as out of memory errors), or if myisamchk
crashes, go to Stage 3.

Stage 3: Difficult repair

You should reach this stage only if the first 16KB block in the index file is destroyed or contains
incorrect information, or if the index file is missing. In this case, it is necessary to create a new index
file. Do so as follows:

1. Move the data file to a safe place.

2. Use the table description file to create new (empty) data and index files:

$> mysql db_name

1634

MyISAM Table Optimization

mysql> SET autocommit=1;
mysql> TRUNCATE TABLE tbl_name;
mysql> quit

3. Copy the old data file back onto the newly created data file. (Do not just move the old file back onto

the new file. You want to retain a copy in case something goes wrong.)

Important

If you are using replication, you should stop it prior to performing the above
procedure, since it involves file system operations, and these are not logged by
MySQL.

Go back to Stage 2. myisamchk -r -q should work. (This should not be an endless loop.)

You can also use the REPAIR TABLE tbl_name USE_FRM SQL statement, which performs
the whole procedure automatically. There is also no possibility of unwanted interaction between
a utility and the server, because the server does all the work when you use REPAIR TABLE. See
Section 15.7.3.5, “REPAIR TABLE Statement”.

9.6.4 MyISAM Table Optimization

To coalesce fragmented rows and eliminate wasted space that results from deleting or updating rows,
run myisamchk in recovery mode:

$> myisamchk -r tbl_name

You can optimize a table in the same way by using the OPTIMIZE TABLE SQL statement. OPTIMIZE
TABLE does a table repair and a key analysis, and also sorts the index tree so that key lookups are
faster. There is also no possibility of unwanted interaction between a utility and the server, because the
server does all the work when you use OPTIMIZE TABLE. See Section 15.7.3.4, “OPTIMIZE TABLE
Statement”.

myisamchk has a number of other options that you can use to improve the performance of a table:

• --analyze or -a: Perform key distribution analysis. This improves join performance by enabling the
join optimizer to better choose the order in which to join the tables and which indexes it should use.

• --sort-index or -S: Sort the index blocks. This optimizes seeks and makes table scans that use

indexes faster.

• --sort-records=index_num or -R index_num: Sort data rows according to a given index.

This makes your data much more localized and may speed up range-based SELECT and ORDER BY
operations that use this index.

For a full description of all available options, see Section 6.6.4, “myisamchk — MyISAM Table-
Maintenance Utility”.

9.6.5 Setting Up a MyISAM Table Maintenance Schedule

It is a good idea to perform table checks on a regular basis rather than waiting for problems to
occur. One way to check and repair MyISAM tables is with the CHECK TABLE and REPAIR TABLE
statements. See Section 15.7.3, “Table Maintenance Statements”.

Another way to check tables is to use myisamchk. For maintenance purposes, you can use
myisamchk -s. The -s option (short for --silent) causes myisamchk to run in silent mode,
printing messages only when errors occur.

It is also a good idea to enable automatic MyISAM table checking. For example, whenever the machine
has done a restart in the middle of an update, you usually need to check each table that could have

1635

Setting Up a MyISAM Table Maintenance Schedule

been affected before it is used further. (These are “expected crashed tables.”) To cause the server to
check MyISAM tables automatically, start it with the myisam_recover_options system variable set.
See Section 7.1.8, “Server System Variables”.

You should also check your tables regularly during normal system operation. For example, you can run
a cron job to check important tables once a week, using a line like this in a crontab file:

35 0 * * 0 /path/to/myisamchk --fast --silent /path/to/datadir/*/*.MYI

This prints out information about crashed tables so that you can examine and repair them as
necessary.

To start with, execute myisamchk -s each night on all tables that have been updated during the last
24 hours. As you see that problems occur infrequently, you can back off the checking frequency to
once a week or so.

Normally, MySQL tables need little maintenance. If you are performing many updates to MyISAM tables
with dynamic-sized rows (tables with VARCHAR, BLOB, or TEXT columns) or have tables with many
deleted rows you may want to defragment/reclaim space from the tables from time to time. You can do
this by using OPTIMIZE TABLE on the tables in question. Alternatively, if you can stop the mysqld
server for a while, change location into the data directory and use this command while the server is
stopped:

$> myisamchk -r -s --sort-index --myisam_sort_buffer_size=16M */*.MYI

1636

