About This Manual

Important

To report problems or bugs, please use the instructions at Section 1.5,
“How to Report Bugs or Problems”. If you find a security bug in MySQL
Server, please let us know immediately by sending an email message to
<secalert_us@oracle.com>. Exception: Support customers should report
all problems, including security bugs, to Oracle Support.

1.1 About This Manual

This is the Reference Manual for the MySQL Database System, version 8.0, through release 8.0.42.
Differences between minor versions of MySQL 8.0 are noted in the present text with reference to
release numbers (8.0.x). For license information, see the Legal Notices.

This manual is not intended for use with older versions of the MySQL software due to the many
functional and other differences between MySQL 8.0 and previous versions. If you are using an earlier
release of the MySQL software, please refer to the appropriate manual. For example, MySQL 5.7
Reference Manual covers the 5.7 series of MySQL software releases.

If you are using MySQL 8.4, please refer to the MySQL 8.4 Reference Manual.

Because this manual serves as a reference, it does not provide general instruction on SQL or relational
database concepts. It also does not teach you how to use your operating system or command-line
interpreter.

The MySQL Database Software is under constant development, and the Reference Manual is updated
frequently as well. The most recent version of the manual is available online in searchable form at
https://dev.mysql.com/doc/. Other formats also are available there, including downloadable HTML and
PDF versions.

The source code for MySQL itself contains internal documentation written using Doxygen. The
generated Doxygen content is available from https://dev.mysql.com/doc/index-other.html. It is also
possible to generate this content locally from a MySQL source distribution using the instructions at
Section 2.8.10, “Generating MySQL Doxygen Documentation Content”.

If you have questions about using MySQL, join the MySQL Community Slack. If you have suggestions
concerning additions or corrections to the manual itself, please send them to the http://www.mysql.com/
company/contact/.

Typographical and Syntax Conventions

This manual uses certain typographical conventions:

• Text in this style is used for SQL statements; database, table, and column names; program
listings and source code; and environment variables. Example: “To reload the grant tables, use the
FLUSH PRIVILEGES statement.”

• Text in this style indicates input that you type in examples.

• Text in this style indicates the names of executable programs and scripts, examples being
mysql (the MySQL command-line client program) and mysqld (the MySQL server executable).

• Text in this style is used for variable input for which you should substitute a value of your

own choosing.

• Text in this style is used for emphasis.

• Text in this style is used in table headings and to convey especially strong emphasis.

• Text in this style is used to indicate a program option that affects how the program is

executed, or that supplies information that is needed for the program to function in a certain way.

2

Typographical and Syntax Conventions

Example: “The --host option (short form -h) tells the mysql client program the hostname or IP
address of the MySQL server that it should connect to”.

• File names and directory names are written like this: “The global my.cnf file is located in the /etc

directory.”

• Character sequences are written like this: “To specify a wildcard, use the ‘%’ character.”

When commands or statements are prefixed by a prompt, we use these:

$> type a command here
#> type a command as root here
C:\> type a command here (Windows only)
mysql> type a mysql statement here

Commands are issued in your command interpreter. On Unix, this is typically a program such as sh,
csh, or bash. On Windows, the equivalent program is command.com or cmd.exe, typically run in a
console window. Statements prefixed by mysql are issued in the mysql command-line client.

Note

When you enter a command or statement shown in an example, do not type the
prompt shown in the example.

In some areas different systems may be distinguished from each other to show that commands should
be executed in two different environments. For example, while working with replication the commands
might be prefixed with source and replica:

source> type a mysql statement on the replication source here
replica> type a mysql statement on the replica here

Database, table, and column names must often be substituted into statements. To indicate that such
substitution is necessary, this manual uses db_name, tbl_name, and col_name. For example, you
might see a statement like this:

mysql> SELECT col_name FROM db_name.tbl_name;

This means that if you were to enter a similar statement, you would supply your own database, table,
and column names, perhaps like this:

mysql> SELECT author_name FROM biblio_db.author_list;

SQL keywords are not case-sensitive and may be written in any lettercase. This manual uses
uppercase.

In syntax descriptions, square brackets (“[” and “]”) indicate optional words or clauses. For example, in
the following statement, IF EXISTS is optional:

DROP TABLE [IF EXISTS] tbl_name

When a syntax element consists of a number of alternatives, the alternatives are separated by vertical
bars (“|”). When one member from a set of choices may be chosen, the alternatives are listed within
square brackets (“[” and “]”):

TRIM([[BOTH | LEADING | TRAILING] [remstr] FROM] str)

When one member from a set of choices must be chosen, the alternatives are listed within braces (“{”
and “}”):

{DESCRIBE | DESC} tbl_name [col_name | wild]

An ellipsis (...) indicates the omission of a section of a statement, typically to provide a shorter
version of more complex syntax. For example, SELECT ... INTO OUTFILE is shorthand for the form
of SELECT statement that has an INTO OUTFILE clause following other parts of the statement.

3

Manual Authorship

An ellipsis can also indicate that the preceding syntax element of a statement may be repeated. In
the following example, multiple reset_option values may be given, with each of those after the first
preceded by commas:

RESET reset_option [,reset_option] ...

Commands for setting shell variables are shown using Bourne shell syntax. For example, the sequence
to set the CC environment variable and run the configure command looks like this in Bourne shell
syntax:

$> CC=gcc ./configure

If you are using csh or tcsh, you must issue commands somewhat differently:

$> setenv CC gcc
$> ./configure

Manual Authorship

The Reference Manual source files are written in DocBook XML format. The HTML version and other
formats are produced automatically, primarily using the DocBook XSL stylesheets. For information
about DocBook, see http://docbook.org/

This manual was originally written by David Axmark and Michael “Monty” Widenius. It is maintained by
the MySQL Documentation Team, consisting of Edward Gilmore, Sudharsana Gomadam, Kim seong
Loh, Garima Sharma, Carlos Ortiz, Daniel So, and Jon Stephens.

1.2 Overview of the MySQL Database Management System

1.2.1 What is MySQL?

MySQL, the most popular Open Source SQL database management system, is developed, distributed,
and supported by Oracle Corporation.

The MySQL website (http://www.mysql.com/) provides the latest information about MySQL software.

• MySQL is a database management system.

A database is a structured collection of data. It may be anything from a simple shopping list to
a picture gallery or the vast amounts of information in a corporate network. To add, access, and
process data stored in a computer database, you need a database management system such
as MySQL Server. Since computers are very good at handling large amounts of data, database
management systems play a central role in computing, as standalone utilities, or as parts of other
applications.

• MySQL databases are relational.

 A relational database stores data in separate tables rather than putting all the data in one big
storeroom. The database structures are organized into physical files optimized for speed. The
logical model, with objects such as databases, tables, views, rows, and columns, offers a flexible
programming environment. You set up rules governing the relationships between different data
fields, such as one-to-one, one-to-many, unique, required or optional, and “pointers” between
different tables. The database enforces these rules, so that with a well-designed database, your
application never sees inconsistent, duplicate, orphan, out-of-date, or missing data.

The SQL part of “MySQL” stands for “Structured Query Language”. SQL is the most common
standardized language used to access databases. Depending on your programming environment,
you might enter SQL directly (for example, to generate reports), embed SQL statements into code
written in another language, or use a language-specific API that hides the SQL syntax.

SQL is defined by the ANSI/ISO SQL Standard. The SQL standard has been evolving since 1986
and several versions exist. In this manual, “SQL-92” refers to the standard released in 1992,

4

The Main Features of MySQL

“SQL:1999” refers to the standard released in 1999, and “SQL:2003” refers to the current version
of the standard. We use the phrase “the SQL standard” to mean the current version of the SQL
Standard at any time.

• MySQL software is Open Source.

    Open Source means that it is possible for anyone to use and modify the software. Anybody can
download the MySQL software from the Internet and use it without paying anything. If you wish, you
may study the source code and change it to suit your needs. The MySQL software uses the GPL
(GNU General Public License), http://www.fsf.org/licenses/, to define what you may and may not do
with the software in different situations. If you feel uncomfortable with the GPL or need to embed
MySQL code into a commercial application, you can buy a commercially licensed version from us.
See the MySQL Licensing Overview for more information (http://www.mysql.com/company/legal/
licensing/).

• The MySQL Database Server is very fast, reliable, scalable, and easy to use.

If that is what you are looking for, you should give it a try. MySQL Server can run comfortably on a
desktop or laptop, alongside your other applications, web servers, and so on, requiring little or no
attention. If you dedicate an entire machine to MySQL, you can adjust the settings to take advantage
of all the memory, CPU power, and I/O capacity available. MySQL can also scale up to clusters of
machines, networked together.

MySQL Server was originally developed to handle large databases much faster than existing
solutions and has been successfully used in highly demanding production environments for several
years. Although under constant development, MySQL Server today offers a rich and useful set of
functions. Its connectivity, speed, and security make MySQL Server highly suited for accessing
databases on the Internet.

• MySQL Server works in client/server or embedded systems.

The MySQL Database Software is a client/server system that consists of a multithreaded SQL server
that supports different back ends, several different client programs and libraries, administrative tools,
and a wide range of application programming interfaces (APIs).

We also provide MySQL Server as an embedded multithreaded library that you can link into your
application to get a smaller, faster, easier-to-manage standalone product.

• A large amount of contributed MySQL software is available.

MySQL Server has a practical set of features developed in close cooperation with our users. It is
very likely that your favorite application or language supports the MySQL Database Server.

• HeatWave.

HeatWave is a fully managed database service, powered by the HeatWave in-memory query
accelerator. It is the only cloud service that combines transactions, real-time analytics across data
warehouses and data lakes, and machine learning in one MySQL Database; without the complexity,
latency, risks, and cost of ETL duplication. It is available on OCI, AWS, and Azure. Learn more at:
https://www.oracle.com/mysql/.

The official way to pronounce “MySQL” is “My Ess Que Ell” (not “my sequel”), but we do not mind if you
pronounce it as “my sequel” or in some other localized way.

1.2.2 The Main Features of MySQL

This section describes some of the important characteristics of the MySQL Database Software. In most
respects, the roadmap applies to all versions of MySQL. For information about features as they are
introduced into MySQL on a series-specific basis, see the “In a Nutshell” section of the appropriate
Manual:

5

History of MySQL

• MySQL Connector/NET enables developers to easily create .NET applications that require secure,

high-performance data connectivity with MySQL. It implements the required ADO.NET interfaces and
integrates into ADO.NET aware tools. Developers can build applications using their choice of .NET
languages. MySQL Connector/NET is a fully managed ADO.NET driver written in 100% pure C#.
See MySQL Connector/NET Developer Guide.

Localization

• The server can provide error messages to clients in many languages. See Section 12.12, “Setting

the Error Message Language”.

• Full support for several different character sets, including latin1 (cp1252), german, big5, ujis,

several Unicode character sets, and more. For example, the Scandinavian characters “å”, “ä” and “ö”
are permitted in table and column names.

• All data is saved in the chosen character set.

• Sorting and comparisons are done according to the default character set and collation. It is possible
to change this when the MySQL server is started (see Section 12.3.2, “Server Character Set and
Collation”). To see an example of very advanced sorting, look at the Czech sorting code. MySQL
Server supports many different character sets that can be specified at compile time and runtime.

• The server time zone can be changed dynamically, and individual clients can specify their own time

zone. See Section 7.1.15, “MySQL Server Time Zone Support”.

Clients and Tools

• MySQL includes several client and utility programs. These include both command-line programs
such as mysqldump and mysqladmin, and graphical programs such as MySQL Workbench.

• MySQL Server has built-in support for SQL statements to check, optimize, and repair tables. These

statements are available from the command line through the mysqlcheck client. MySQL also
includes myisamchk, a very fast command-line utility for performing these operations on MyISAM
tables. See Chapter 6, MySQL Programs.

• MySQL programs can be invoked with the --help or -? option to obtain online assistance.

1.2.3 History of MySQL

We started out with the intention of using the mSQL database system to connect to our tables using
our own fast low-level (ISAM) routines. However, after some testing, we came to the conclusion that
mSQL was not fast enough or flexible enough for our needs. This resulted in a new SQL interface to our
database but with almost the same API interface as mSQL. This API was designed to enable third-party
code that was written for use with mSQL to be ported easily for use with MySQL.

MySQL is named after co-founder Monty Widenius's daughter, My.

The name of the MySQL Dolphin (our logo) is “Sakila,” which was chosen from a huge list of names
suggested by users in our “Name the Dolphin” contest. The winning name was submitted by Ambrose
Twebaze, an Open Source software developer from Eswatini (formerly Swaziland), Africa. According
to Ambrose, the feminine name Sakila has its roots in SiSwati, the local language of Eswatini. Sakila is
also the name of a town in Arusha, Tanzania, near Ambrose's country of origin, Uganda.

1.3 What Is New in MySQL 8.0

This section summarizes what has been added to, deprecated in, and removed from MySQL 8.0.
A companion section lists MySQL server options and variables that have been added, deprecated,
or removed in MySQL 8.0; see Section 1.4, “Server and Status Variables and Options Added,
Deprecated, or Removed in MySQL 8.0”.

• Features Added in MySQL 8.0

8

Features Added in MySQL 8.0

instruction duration on different processor architectures. For more information, see Section 17.8.8,
“Configuring Spin Lock Polling”.

• InnoDB parallel read thread performance for large data sets was improved in MySQL 8.0.17

through better utilization of read threads, through a reduction in read thread I/O for prefetch activity
that occurs during parallel scans, and through support for parallel scanning of partitions.

The parallel read thread feature is controlled by the innodb_parallel_read_threads
variable. The maximum setting is now 256, which is the total number of threads for all client
connections. If the thread limit is reached, connections fall back to using a single thread.

• The innodb_idle_flush_pct variable, introduced in MySQL 8.0.18, permits placing a limit on

page flushing during idle periods, which can help extend the life of solid state storage devices. See
Limiting Buffer Flushing During Idle Periods.

• Efficient sampling of InnoDB data for the purpose of generating histogram statistics is supported

as of MySQL 8.0.19. See Histogram Statistics Analysis.

• As of MySQL 8.0.20, the doublewrite buffer storage area resides in doublewrite files. In previous
releases, the storage area resided in the system tablespace. Moving the storage area out of
the system tablespace reduces write latency, increases throughput, and provides flexibility with
respect to placement of doublewrite buffer pages. The following system variables were introduced
for advanced doublewrite buffer configuration:

• innodb_doublewrite_dir

Defines the doublewrite buffer file directory.

• innodb_doublewrite_files

Defines the number of doublewrite files.

• innodb_doublewrite_pages

Defines the maximum number of doublewrite pages per thread for a batch write.

• innodb_doublewrite_batch_size

Defines the number of doublewrite pages to write in a batch.

For more information, see Section 17.6.4, “Doublewrite Buffer”.

• The Contention-Aware Transaction Scheduling (CATS) algorithm, which prioritizes transactions

that are waiting for locks, was improved in MySQL 8.0.20. Transaction scheduling weight
computation is now performed a separate thread entirely, which improves computation
performance and accuracy.

The First In First Out (FIFO) algorithm, which had also been used for transaction scheduling,
was removed. The FIFO algorithm was rendered redundant by CATS algorithm enhancements.

19

Features Added in MySQL 8.0

Transaction scheduling previously performed by the FIFO algorithm is now performed by the
CATS algorithm.

A TRX_SCHEDULE_WEIGHT column was added to the INFORMATION_SCHEMA.INNODB_TRX
table, which permits querying transaction scheduling weights assigned by the CATS algorithm.

The following INNODB_METRICS counters were added for monitoring code-level transaction
scheduling events:

• lock_rec_release_attempts

The number of attempts to release record locks.

• lock_rec_grant_attempts

The number of attempts to grant record locks.

• lock_schedule_refreshes

The number of times the wait-for graph was analyzed to update transaction schedule weights.

For more information, see Section 17.7.6, “Transaction Scheduling”.

• As of MySQL 8.0.21, to improve concurrency for operations that require access to lock queues
for table and row resources, the lock system mutex (lock_sys->mutex) was replaced in by
sharded latches, and lock queues were grouped into table and page lock queue shards, with each
shard protected by a dedicated mutex. Previously, the single lock system mutex protected all
lock queues, which was a point of contention on high-concurrency systems. The new sharded
implementation permits more granular access to lock queues.

The lock system mutex (lock_sys->mutex) was replaced by the following sharded latches:

• A global latch (lock_sys->latches.global_latch) consisting of 64 read-write lock objects
(rw_lock_t). Access to an individual lock queue requires a shared global latch and a latch on
the lock queue shard. Operations that require access to all lock queues take an exclusive global
latch, which latches all table and page lock queue shards.

• Table shard latches (lock_sys->latches.table_shards.mutexes), implemented as an

array of 512 mutexes, with each mutex dedicated to one of 512 table lock queue shards.

• Page shard latches (lock_sys->latches.page_shards.mutexes), implemented as an
array of 512 mutexes, with each mutex dedicated to one of 512 page lock queue shards.

The Performance Schema wait/synch/mutex/innodb/lock_mutex instrument for monitoring
the single lock system mutex was replaced by instruments for monitoring the new global, table
shard, and page shard latches:

• wait/synch/sxlock/innodb/lock_sys_global_rw_lock

• wait/synch/mutex/innodb/lock_sys_table_mutex

• wait/synch/mutex/innodb/lock_sys_page_mutex

• As of MySQL 8.0.21, table and table partition data files created outside of the data directory using
the DATA DIRECTORY clause are restricted to directories known to InnoDB. This change permits

20

Features Added in MySQL 8.0

database administrators to control where tablespace data files are created and ensures that the
data files can be found during recovery.

General and file-per-table tablespaces data files (.ibd files) can no longer be created in the undo
tablespace directory (innodb_undo_directory) unless that directly is known to InnoDB.

Known directories are those defined by the datadir, innodb_data_home_dir, and
innodb_directories variables.

Truncating an InnoDB table that resides in a file-per-table tablespace drops the existing
tablespace and creates a new one. As of MySQL 8.0.21, InnoDB creates the new tablespace
in the default location and writes a warning to the error log if the current tablespace directory
is unknown. To have TRUNCATE TABLE create the tablespace in its current location, add the
directory to the innodb_directories setting before running TRUNCATE TABLE.

• As of MySQL 8.0.21, redo logging can be enabled and disabled using ALTER INSTANCE

{ENABLE|DISABLE} INNODB REDO_LOG syntax. This functionality is intended for loading data
into a new MySQL instance. Disabling redo logging helps speed up data loading by avoiding redo
log writes.

The new INNODB_REDO_LOG_ENABLE privilege permits enabling and disabling redo logging.

The new Innodb_redo_log_enabled status variable permits monitoring redo logging status.

See Disabling Redo Logging.

• At startup, InnoDB validates the paths of known tablespace files against tablespace file paths

stored in the data dictionary in case tablespace files have been moved to a different location. The
new innodb_validate_tablespace_paths variable, introduced in MySQL 8.0.21, permits
disabling tablespace path validation. This feature is intended for environments where tablespaces
files are not moved. Disabling tablespace path validation improves startup time on systems with a
large number of tablespace files.

For more information, see Section 17.6.3.7, “Disabling Tablespace Path Validation”.

• As of MySQL 8.0.21, on storage engines that support atomic DDL, the CREATE TABLE ...

SELECT statement is logged as one transaction in the binary log when row-based replication is
in use. Previously, it was logged as two transactions, one to create the table, and the other to
insert data. With this change, CREATE TABLE ... SELECT statements are now safe for row-
based replication and permitted for use with GTID-based replication. For more information, see
Section 15.1.1, “Atomic Data Definition Statement Support”.

• Truncating an undo tablespace on a busy system could affect performance due to associated
flushing operations that remove old undo tablespace pages from the buffer pool and flush the
initial pages of the new undo tablespace to disk. To address this issue, the flushing operations are
removed as of MySQL 8.0.21.

Old undo tablespace pages are released passively as they become least recently used, or are
removed at the next full checkpoint. The initial pages of the new undo tablespace are now redo
logged instead of flushed to disk during the truncate operation, which also improves durability of
the undo tablespace truncate operation.

To prevent potential issues caused by an excessive number of undo tablespace truncate
operations, truncate operations on the same undo tablespace between checkpoints are now
limited to 64. If the limit is exceeded, an undo tablespace can still be made inactive, but it is not
truncated until after the next checkpoint.

INNODB_METRICS counters associated with defunct undo truncate flushing operations
were removed. Removed counters include: undo_truncate_sweep_count,

21

Features Added in MySQL 8.0

undo_truncate_sweep_usec, undo_truncate_flush_count, and
undo_truncate_flush_usec.

See Section 17.6.3.4, “Undo Tablespaces”.

• As of MySQL 8.0.22, the new innodb_extend_and_initialize variable permits configuring

how InnoDB allocates space to file-per-table and general tablespaces on Linux. By default,
when an operation requires additional space in a tablespace, InnoDB allocates pages to the
tablespace and physically writes NULLs to those pages. This behavior affects performance if
new pages are allocated frequently. You can disable innodb_extend_and_initialize on
Linux systems to avoid physically writing NULLs to newly allocated tablespace pages. When
innodb_extend_and_initialize is disabled, space is allocated using posix_fallocate()
calls, which reserve space without physically writing NULLs.

A posix_fallocate() operation is not atomic, which makes it possible for a failure to occur
between allocating space to a tablespace file and updating the file metadata. Such a failure can
leave newly allocated pages in an uninitialized state, resulting in a failure when InnoDB attempts
to access those pages. To prevent this scenario, InnoDB writes a redo log record before allocating
a new tablespace page. If a page allocation operation is interrupted, the operation is replayed from
the redo log record during recovery.

• As of MySQL 8.0.23, InnoDB supports encryption of doublewrite file pages belonging to encrypted
tablespaces. The pages are encrypted using the encryption key of the associated tablespace. For
more information, see Section 17.13, “InnoDB Data-at-Rest Encryption”.

• The temptable_max_mmap variable, introduced in MySQL 8.0.23, defines the maximum amount
of memory the TempTable storage engine is permitted to allocate from memory-mapped (MMAP)
files before it starts storing internal temporary table data on disk. A setting of 0 disables allocation
from MMAP files. For more information, see Section 10.4.4, “Internal Temporary Table Use in
MySQL”.

• The AUTOEXTEND_SIZE option, introduced in MySQL 8.0.23, defines the amount by which
InnoDB extends the size of a tablespace when it becomes full, making it possible to extend
tablespace size in larger increments. The AUTOEXTEND_SIZE option is supported with the
CREATE TABLE, ALTER TABLE, CREATE TABLESPACE, and ALTER TABLESPACE statements.
For more information, see Section 17.6.3.9, “Tablespace AUTOEXTEND_SIZE Configuration”.

An AUTOEXTEND_SIZE size column was added to the Information Schema
INNODB_TABLESPACES table.

• The innodb_segment_reserve_factor system variable, introduced in MySQL 8.0.26, permits
configuring the percentage of tablespace file segment pages that are reserved as empty pages.
For more information, see Configuring the Percentage of Reserved File Segment Pages.

• On platforms that support fdatasync() system calls, the innodb_use_fdatasync variable,
introduced in MySQL 8.0.26, permits using fdatasync() instead of fsync() for operating
system flushes. An fdatasync() system call does not flush changes to file metadata unless
required for subsequent data retrieval, providing a potential performance benefit.

• As of MySQL 8.0.28, the tmp_table_size variable defines the maximum size of any individual
in-memory internal temporary table created by the TempTable storage engine. An appropriate
size limit prevents individual queries from consuming an inordinate amount global TempTable
resources. See Internal Temporary Table Storage Engine.

• From MySQL 8.0.28, the innodb_open_files variable, which defines the number
of files InnoDB can have open at one time, can be set at runtime using a SELECT

22

Features Added in MySQL 8.0

innodb_set_open_files_limit(N) statement. The statement executes a stored procedure
that sets the new limit.

To prevent non-LRU manged files from consuming the entire innodb_open_files limit, non-
LRU managed files are limited to 90 percent of the innodb_open_files limit, which reserves 10
percent of the innodb_open_files limit for LRU managed files.

The innodb_open_files limit includes temporary tablespace files, which were not counted
toward the limit previously.

• From MySQL 8.0.28, InnoDB supports ALTER TABLE ... RENAME COLUMN operations using

ALGORITHM=INSTANT.

For more information about this and other DDL operations that support ALGORITHM=INSTANT,
see Section 17.12.1, “Online DDL Operations”.

• From MySQL 8.0.29, InnoDB supports ALTER TABLE ... DROP COLUMN operations using

ALGORITHM=INSTANT.

Prior to MySQL 8.0.29, an instantly added column could only be added as the last column of the
table. From MySQL 8.0.29, an instantly added column can be added to any position in the table.

Instantly added or dropped columns create a new version of the affected row. Up to 64 row
versions are permitted. A new TOTAL_ROW_VERSIONS column was added to the Information
Schema INNODB_TABLES table to track the number of row versions.

For more information about DDL operations that support ALGORITHM=INSTANT, see
Section 17.12.1, “Online DDL Operations”.

• From MySQL 8.0.30, the innodb_doublewrite system variable supports DETECT_ONLY and
DETECT_AND_RECOVER settings. With the DETECT_ONLY setting, database page content is not
written to the doublewrite buffer, and recovery does not use the doublewrite buffer to fix incomplete
page writes. This lightweight setting is intended for detecting incomplete page writes only. The
DETECT_AND_RECOVER setting is equivalent to the existing ON setting. For more information, see
Section 17.6.4, “Doublewrite Buffer”.

• From MySQL 8.0.30, InnoDB supports dynamic configuration of redo log capacity. The

innodb_redo_log_capacity system variable can be set at runtime to increase or decrease the
total amount of disk space occupied by redo log files.

With this change, the number of redo log files and their default location has also changed. From
MySQL 8.0.30, InnoDB maintains 32 redo log files in the #innodb_redo directory in the data
directory. Previously, InnoDB created two redo log files in the data directory by default, and the
number and size of redo log files were controlled by the innodb_log_files_in_group and
innodb_log_file_size variables. These two variables are now deprecated.

When the innodb_redo_log_capacity setting is defined, innodb_log_files_in_group
and innodb_log_file_size settings are ignored; otherwise, those settings are used to
compute the innodb_redo_log_capacity setting (innodb_log_files_in_group *
innodb_log_file_size = innodb_redo_log_capacity). If none of those variables are set,
redo log capacity is set to the innodb_redo_log_capacity default value, which is 104857600
bytes (100MB).

Several status variables are provided for monitoring the redo log and redo log resizing operations.

For more information, see Section 17.6.5, “Redo Log”.

• With MySQL 8.0.31, there are two new status variables for monitoring online buffer pool

resizing operations. The Innodb_buffer_pool_resize_status_code status variable
reports a status code indicating the stage of an online buffer pool resizing operation. The

23

Features Added in MySQL 8.0

Innodb_buffer_pool_resize_status_progress status variable reports a percentage value
indicating the progress of each stage.

For more information, see Section 17.8.3.1, “Configuring InnoDB Buffer Pool Size”.

• Character set support.

 The default character set has changed from latin1 to utf8mb4. The
utf8mb4 character set has several new collations, including utf8mb4_ja_0900_as_cs, the first
Japanese language-specific collation available for Unicode in MySQL. For more information, see
Section 12.10.1, “Unicode Character Sets”.

• JSON enhancements.

 The following enhancements or additions were made to MySQL's JSON

functionality:

• Added the ->> (inline path) operator, which is equivalent to calling JSON_UNQUOTE() on the

result of JSON_EXTRACT().

This is a refinement of the column path operator -> introduced in MySQL 5.7; col->>"$.path"
is equivalent to JSON_UNQUOTE(col->"$.path"). The inline path operator can be used
wherever you can use JSON_UNQUOTE(JSON_EXTRACT()), such SELECT column lists, WHERE
and HAVING clauses, and ORDER BY and GROUP BY clauses. For more information, see the
description of the operator, as well as JSON Path Syntax.

• Added two JSON aggregation functions JSON_ARRAYAGG() and JSON_OBJECTAGG().

JSON_ARRAYAGG() takes a column or expression as its argument, and aggregates the result as a
single JSON array. The expression can evaluate to any MySQL data type; this does not have to be
a JSON value. JSON_OBJECTAGG() takes two columns or expressions which it interprets as a key
and a value; it returns the result as a single JSON object. For more information and examples, see
Section 14.19, “Aggregate Functions”.

• Added the JSON utility function JSON_PRETTY(), which outputs an existing JSON value in an

easy-to-read format; each JSON object member or array value is printed on a separate line, and a
child object or array is intended 2 spaces with respect to its parent.

This function also works with a string that can be parsed as a JSON value.

For more detailed information and examples, see Section 14.17.8, “JSON Utility Functions”.

• When sorting JSON values in a query using ORDER BY, each value is now represented by a

variable-length part of the sort key, rather than a part of a fixed 1K in size. In many cases this can
reduce excessive usage. For example, a scalar INT or even BIGINT value actually requires very
few bytes, so that the remainder of this space (up to 90% or more) was taken up by padding. This
change has the following benefits for performance:

• Sort buffer space is now used more effectively, so that filesorts need not flush to disk as early
or often as with fixed-length sort keys. This means that more data can be sorted in memory,
avoiding unnecessary disk access.

• Shorter keys can be compared more quickly than longer ones, providing a noticeable

improvement in performance. This is true for sorts performed entirely in memory as well as for
sorts that require writing to and reading from disk.

• Added support in MySQL 8.0.2 for partial, in-place updates of JSON column values, which is more

efficient than completely removing an existing JSON value and writing a new one in its place,
as was done previously when updating any JSON column. For this optimization to be applied,
the update must be applied using JSON_SET(), JSON_REPLACE(), or JSON_REMOVE(). New
elements cannot be added to the JSON document being updated; values within the document

24

Features Added in MySQL 8.0

cannot take more space than they did before the update. See Partial Updates of JSON Values, for
a detailed discussion of the requirements.

Partial updates of JSON documents can be written to the binary log, taking up less space
than logging complete JSON documents. Partial updates are always logged as such when
statement-based replication is in use. For this to work with row-based replication, you must first
set binlog_row_value_options=PARTIAL_JSON; see this variable's description for more
information.

• Added the JSON utility functions JSON_STORAGE_SIZE() and JSON_STORAGE_FREE().

JSON_STORAGE_SIZE() returns the storage space in bytes used for the binary representation of
a JSON document prior to any partial update (see previous item). JSON_STORAGE_FREE() shows
the amount of space remaining in a table column of type JSON after it has been partially updated
using JSON_SET() or JSON_REPLACE(); this is greater than zero if the binary representation of
the new value is less than that of the previous value.

Each of these functions also accepts a valid string representation of a JSON document. For such
a value, JSON_STORAGE_SIZE() returns the space used by its binary representation following
its conversion to a JSON document. For a variable containing the string representation of a JSON
document, JSON_STORAGE_FREE() returns zero. Either function produces an error if its (non-null)
argument cannot be parsed as a valid JSON document, and NULL if the argument is NULL.

For more information and examples, see Section 14.17.8, “JSON Utility Functions”.

JSON_STORAGE_SIZE() and JSON_STORAGE_FREE() were implemented in MySQL 8.0.2.

• Added support in MySQL 8.0.2 for ranges such as $[1 to 5] in XPath expressions. Also added
support in this version for the last keyword and relative addressing, such that $[last] always
selects the last (highest-numbered) element in the array and $[last-1] the next to last element.
last and expressions using it can also be included in range definitions. For example, $[last-2
to last-1] returns the last two elements but one from an array. See Searching and Modifying
JSON Values, for additional information and examples.

• Added a JSON merge function intended to conform to RFC 7396. JSON_MERGE_PATCH(), when
used on 2 JSON objects, merges them into a single JSON object that has as members a union of
the following sets:

• Each member of the first object for which there is no member with the same key in the second

object.

• Each member of the second object for which there is no member having the same key in the first

object, and whose value is not the JSON null literal.

• Each member having a key that exists in both objects, and whose value in the second object is

not the JSON null literal.

As part of this work, the JSON_MERGE() function has been renamed JSON_MERGE_PRESERVE().
JSON_MERGE() continues to be recognized as an alias for JSON_MERGE_PRESERVE() in MySQL
8.0, but is now deprecated and is subject to removal in a future version of MySQL.

For more information and examples, see Section 14.17.4, “Functions That Modify JSON Values”.

• Implemented “last duplicate key wins” normalization of duplicate keys, consistent with RFC 7159

and most JavaScript parsers. An example of this behavior is shown here, where only the rightmost
member having the key x is preserved:

mysql> SELECT JSON_OBJECT('x', '32', 'y', '[true, false]',
     >                     'x', '"abc"', 'x', '100') AS Result;
+------------------------------------+
| Result                             |
+------------------------------------+

25

Features Added in MySQL 8.0

| {"x": "100", "y": "[true, false]"} |
+------------------------------------+
1 row in set (0.00 sec)

Values inserted into MySQL JSON columns are also normalized in this way, as shown in this
example:

mysql> CREATE TABLE t1 (c1 JSON);

mysql> INSERT INTO t1 VALUES ('{"x": 17, "x": "red", "x": [3, 5, 7]}');

mysql> SELECT c1 FROM t1;
+------------------+
| c1               |
+------------------+
| {"x": [3, 5, 7]} |
+------------------+

This is an incompatible change from previous versions of MySQL, where a “first duplicate key
wins” algorithm was used in such cases.

See Normalization, Merging, and Autowrapping of JSON Values, for more information and
examples.

• Added the JSON_TABLE() function in MySQL 8.0.4. This function accepts JSON data and returns

it as a relational table having the specified columns.

This function has the syntax JSON_TABLE(expr, path COLUMNS column_list) [AS]
alias), where expr is an expression that returns JSON data, path is a JSON path applied to
the source, and column_list is a list of column definitions. An example is shown here:

mysql> SELECT *
    -> FROM
    ->   JSON_TABLE(
    ->     '[{"a":3,"b":"0"},{"a":"3","b":"1"},{"a":2,"b":1},{"a":0},{"b":[1,2]}]',
    ->     "$[*]" COLUMNS(
    ->       rowid FOR ORDINALITY,
    ->
    ->       xa INT EXISTS PATH "$.a",
    ->       xb INT EXISTS PATH "$.b",
    ->
    ->       sa VARCHAR(100) PATH "$.a",
    ->       sb VARCHAR(100) PATH "$.b",
    ->
    ->       ja JSON PATH "$.a",
    ->       jb JSON PATH "$.b"
    ->     )
    ->   ) AS  jt1;
+-------+------+------+------+------+------+--------+
| rowid | xa   | xb   | sa   | sb   | ja   | jb     |
+-------+------+------+------+------+------+--------+
|     1 |    1 |    1 | 3    | 0    | 3    | "0"    |
|     2 |    1 |    1 | 3    | 1    | "3"  | "1"    |
|     3 |    1 |    1 | 2    | 1    | 2    | 1      |
|     4 |    1 |    0 | 0    | NULL | 0    | NULL   |
|     5 |    0 |    1 | NULL | NULL | NULL | [1, 2] |
+-------+------+------+------+------+------+--------+

The JSON source expression can be any expression that yields a valid JSON document, including
a JSON literal, a table column, or a function call that returns JSON such as JSON_EXTRACT(t1,
data, '$.post.comments'). For more information, see Section 14.17.6, “JSON Table
Functions”.

• Data type support.

 MySQL now supports use of expressions as default values in data

type specifications. This includes the use of expressions as default values for the BLOB, TEXT,
GEOMETRY, and JSON data types, which previously could not be assigned default values at all. For
details, see Section 13.6, “Data Type Default Values”.

26

Features Added in MySQL 8.0

• Optimizer.

 These optimizer enhancements were added:

• MySQL now supports invisible indexes. An invisible index is not used by the optimizer at all, but is
otherwise maintained normally. Indexes are visible by default. Invisible indexes make it possible to
test the effect of removing an index on query performance, without making a destructive change
that must be undone should the index turn out to be required. See Section 10.3.12, “Invisible
Indexes”.

• MySQL now supports descending indexes: DESC in an index definition is no longer ignored but
causes storage of key values in descending order. Previously, indexes could be scanned in
reverse order but at a performance penalty. A descending index can be scanned in forward order,
which is more efficient. Descending indexes also make it possible for the optimizer to use multiple-
column indexes when the most efficient scan order mixes ascending order for some columns and
descending order for others. See Section 10.3.13, “Descending Indexes”.

• MySQL now supports creation of functional index key parts that index expression values rather
than column values. Functional key parts enable indexing of values that cannot be indexed
otherwise, such as JSON values. For details, see Section 15.1.15, “CREATE INDEX Statement”.

• In MySQL 8.0.14 and later, trivial WHERE conditions arising from constant literal expressions are
removed during preparation, rather than later on during optimization. Removal of the condition
earlier in the process makes it possible to simplify joins for queries with outer joins having trivial
conditions, such as this one:

SELECT * FROM t1 LEFT JOIN t2 ON condition_1 WHERE condition_2 OR 0 = 1

The optimizer now sees during preparation that 0 = 1 is always false, making OR 0 = 1
redundant, and removes it, leaving this:

SELECT * FROM t1 LEFT JOIN t2 ON condition_1 where condition_2

Now the optimizer can rewrite the query as an inner join, like this:

SELECT * FROM t1 LEFT JOIN t2 WHERE condition_1 AND condition_2

For more information, see Section 10.2.1.9, “Outer Join Optimization”.

• In MySQL 8.0.16 and later, MySQL can use constant folding at optimization time to handle

comparisons between a column and a constant value where the constant is out of range or on
a range boundary with respect to the type of the column, rather than doing so for each row at
execution time. For example, given a table t with a TINYINT UNSIGNED column c, the optimizer
can rewrite a condition such as WHERE c < 256 to WHERE 1 (and optimize the condition away
altogether), or WHERE c >= 255 to WHERE c = 255.

See Section 10.2.1.14, “Constant-Folding Optimization”, for more information.

• Beginning with MySQL 8.0.16, the semijoin optimizations used with IN subqueries can now

be applied to EXISTS subqueries as well. In addition, the optimizer now decorrelates trivially-
correlated equality predicates in the WHERE condition attached to the subquery, so that they can be
treated similarly to expressions in IN subqueries; this applies to both EXISTS and IN subqueries.

For more information, see Section 10.2.2.1, “Optimizing IN and EXISTS Subquery Predicates with
Semijoin Transformations”.

• As of MySQL 8.0.17, the server rewrites any incomplete SQL predicates (that is, predicates

having the form WHERE value, in which value is a column name or constant expression and
no comparison operator is used) internally as WHERE value <> 0 during the contextualization

27

Features Added in MySQL 8.0

phase, so that the query resolver, query optimizer, and query executor need work only with
complete predicates.

One visible effect of this change is that, for Boolean values, EXPLAIN output now shows true and
false, rather than 1 and 0.

Another effect of this change is that evaluation of a JSON value in an SQL boolean context
performs an implicit comparison against JSON integer 0. Consider the table created and populated
as shown here:

mysql> CREATE TABLE test (id INT, col JSON);

mysql> INSERT INTO test VALUES (1, '{"val":true}'), (2, '{"val":false}');

Previously, the server attempted to convert an extracted true or false value to an SQL boolean
when comparing it in an SQL boolean context, as shown by the following query using IS TRUE:

mysql> SELECT id, col, col->"$.val" FROM test WHERE col->"$.val" IS TRUE;
+------+---------------+--------------+
| id   | col           | col->"$.val" |
+------+---------------+--------------+
|    1 | {"val": true} | true         |
+------+---------------+--------------+

In MySQL 8.0.17 and later, the implicit comparison of the extracted value with JSON integer 0
leads to a different result:

mysql> SELECT id, col, col->"$.val" FROM test WHERE col->"$.val" IS TRUE;
+------+----------------+--------------+
| id   | col            | col->"$.val" |
+------+----------------+--------------+
|    1 | {"val": true}  | true         |
|    2 | {"val": false} | false        |
+------+----------------+--------------+

Beginning with MySQL 8.0.21, you can use JSON_VALUE() on the extracted value to perform type
conversion prior to performing the test, as shown here:

mysql> SELECT id, col, col->"$.val" FROM test
    ->     WHERE JSON_VALUE(col, "$.val" RETURNING UNSIGNED) IS TRUE;
+------+---------------+--------------+
| id   | col           | col->"$.val" |
+------+---------------+--------------+
|    1 | {"val": true} | true         |
+------+---------------+--------------+

Also beginning with MySQL 8.0.21, the server provides the warning Evaluating a JSON
value in SQL boolean context does an implicit comparison against JSON
integer 0; if this is not what you want, consider converting JSON to an
SQL numeric type with JSON_VALUE RETURNING when comparing extracted values in an
SQL boolean context in this manner.

• In MySQL 8.0.17 and later a WHERE condition having NOT IN (subquery) or NOT EXISTS

(subquery) is transformed internally into an antijoin. (An antijoin returns all rows from the table
for which there is no row in the table to which it is joined matching the join condition.) This removes
the subquery which can result in faster query execution since the subquery's tables are now
handled on the top level.

This is similar to, and reuses, the existing IS NULL (Not exists) optimization for outer joins;
see EXPLAIN Extra Information.

28

Features Added in MySQL 8.0

• Beginning with MySQL 8.0.21, a single-table UPDATE or DELETE statement can now in many
cases make use of a semijoin transformation or subquery materialization. This applies to
statements of the forms shown here:

• UPDATE t1 SET t1.a=value WHERE t1.a IN (SELECT t2.a FROM t2)

• DELETE FROM t1 WHERE t1.a IN (SELECT t2.a FROM t2)

This can be done for a single-table UPDATE or DELETE meeting the following conditions:

• The UPDATE or DELETE statement uses a subquery having a [NOT] IN or [NOT] EXISTS

predicate.

• The statement has no ORDER BY clause, and has no LIMIT clause.

(The multi-table versions of UPDATE and DELETE do not support ORDER BY or LIMIT.)

• The target table does not support read-before-write removal (relevant only for NDB tables).

• Semijoin or subquery materialization is allowed, based on any hints contained in the subquery

and the value of optimizer_switch.

When the semijoin optimization is used for an eligible single-table DELETE or UPDATE, this is
visible in the optimizer trace: for a multi-table statement there is a join_optimization object
in the trace, while there is none for a single-table statement. The conversion is also visible in the
output of EXPLAIN FORMAT=TREE or EXPLAIN ANALYZE; a single-table statement shows <not
executable by iterator executor>, while a multi-table statement reports a full plan.

Also beginning with MySQL 8.0.21, semi-consistent reads are supported by multi-table UPDATE
statements using InnoDB tables, for transaction isolation levels weaker than REPEATABLE READ.

• Improved hash join performance.

 MySQL 8.0.23 reimplements the hash table used for hash
joins, resulting in several improvements in hash join performance. This work includes a fix for an
issue (Bug #31516149, Bug #99933) whereby only roughly 2/3 of the memory allocated for the join
buffer (join_buffer_size) could actually be used by a hash join.

The new hash table is generally faster than the old one, and uses less memory for alignment,
keys/values, and in scenarios where there are many equal keys. In addition, the server can now
free old memory when the size of the hash table increases.

• Common table expressions.

 MySQL now supports common table expressions, both

nonrecursive and recursive. Common table expressions enable use of named temporary result
sets, implemented by permitting a WITH clause preceding SELECT statements and certain other
statements. For more information, see Section 15.2.20, “WITH (Common Table Expressions)”.

As of MySQL 8.0.19, the recursive SELECT part of a recursive common table expression (CTE)
supports a LIMIT clause. LIMIT with OFFSET is also supported. See Recursive Common Table
Expressions, for more information.

• Window functions.

 MySQL now supports window functions that, for each row from a query,

perform a calculation using rows related to that row. These include functions such as RANK(),
LAG(), and NTILE(). In addition, several existing aggregate functions now can be used as window
functions (for example, SUM() and AVG()). For more information, see Section 14.20, “Window
Functions”.

• Lateral derived tables.

 A derived table now may be preceded by the LATERAL keyword to

specify that it is permitted to refer to (depend on) columns of preceding tables in the same FROM
clause. Lateral derived tables make possible certain SQL operations that cannot be done with
nonlateral derived tables or that require less-efficient workarounds. See Section 15.2.15.9, “Lateral
Derived Tables”.

29

Features Added in MySQL 8.0

• Aliases in single-table DELETE statements.
statements support the use of table aliases.

 In MySQL 8.0.16 and later, single-table DELETE

• Regular expression support.

 Previously, MySQL used the Henry Spencer regular expression
library to support regular expression operators (REGEXP, RLIKE). Regular expression support has
been reimplemented using International Components for Unicode (ICU), which provides full Unicode
support and is multibyte safe. The REGEXP_LIKE() function performs regular expression matching
in the manner of the REGEXP and RLIKE operators, which now are synonyms for that function. In
addition, the REGEXP_INSTR(), REGEXP_REPLACE(), and REGEXP_SUBSTR() functions are
available to find match positions and perform substring substitution and extraction, respectively. The
regexp_stack_limit and regexp_time_limit system variables provide control over resource
consumption by the match engine. For more information, see Section 14.8.2, “Regular Expressions”.
For information about ways in which applications that use regular expressions may be affected by
the implementation change, see Regular Expression Compatibility Considerations.

One effect of this change is that [a-zA-Z] and [0-9] perform much better in MySQL 8.0 than
[[:alpha:]] and [[:digit:]], respectively. Existing applications that use the character classes
in pattern matching should be upgraded to use the ranges instead.

• Internal temporary tables.

 The TempTable storage engine replaces the MEMORY storage

engine as the default engine for in-memory internal temporary tables. The TempTable
storage engine provides efficient storage for VARCHAR and VARBINARY columns. The
internal_tmp_mem_storage_engine session variable defines the storage engine for in-
memory internal temporary tables. Permitted values are TempTable (the default) and MEMORY.
The temptable_max_ram variable defines the maximum amount of memory that the TempTable
storage engine can use before data is stored to disk.

• Logging.

 These enhancements were added to improve logging:

• Error logging was rewritten to use the MySQL component architecture. Traditional error logging

is implemented using built-in components, and logging using the system log is implemented as a
loadable component. In addition, a loadable JSON log writer is available. For more information,
see Section 7.4.2, “The Error Log”.

• From MySQL 8.0.30, error log components can be loaded implicitly at startup before the InnoDB
storage engine is available. This new method of loading error log components loads and enables
the components defined by the log_error_services variable.

Previously, error log components had to be installed first using INSTALL COMPONENT and could
only be loaded after InnoDB was fully available, as the list of components to load was read from
the mysql.components table, which is an InnoDB table.

Implicit loading of error log components has these advantages:

• Log components are loaded earlier in the startup sequence, making logged information available

sooner.

• It helps avoid loss of buffered log information should a failure occur during startup.

• Loading log components using INSTALL COMPONENT is not required, simplifying error log

configuration.

The explicit method of loading log components using INSTALL COMPONENT remains supported
for backward compatibility.

For more information, see Section 7.4.2.1, “Error Log Configuration”.

• Backup lock.

 A new type of backup lock permits DML during an online backup while preventing
operations that could result in an inconsistent snapshot. The new backup lock is supported by LOCK
INSTANCE FOR BACKUP and UNLOCK INSTANCE syntax. The BACKUP_ADMIN privilege is required
to use these statements.

30

Features Added in MySQL 8.0

• Replication.

 The following enhancements have been made to MySQL Replication:

• MySQL Replication now supports binary logging of partial updates to JSON documents using a
compact binary format, saving space in the log over logging complete JSON documents. Such
compact logging is done automatically when statement-based logging is in use, and can be
enabled by setting the new binlog_row_value_options system variable to PARTIAL_JSON.
For more information, see Partial Updates of JSON Values, as well as the description of
binlog_row_value_options.

• Connection management.

 MySQL Server now permits a TCP/IP port to be configured

specifically for administrative connections. This provides an alternative to the single administrative
connection that is permitted on the network interfaces used for ordinary connections even when
max_connections connections are already established. See Section 7.1.12.1, “Connection
Interfaces”.

MySQL now provides more control over the use of compression to minimize the number of bytes
sent over connections to the server. Previously, a given connection was either uncompressed or
used the zlib compression algorithm. Now, it is also possible to use the zstd algorithm, and to
select a compression level for zstd connections. The permitted compression algorithms can be
configured on the server side, as well as on the connection-origination side for connections by client
programs and by servers participating in source/replica replication or Group Replication. For more
information, see Section 6.2.8, “Connection Compression Control”.

• Configuration.

 The maximum permitted length of host names throughout MySQL has been
raised to 255 ASCII characters, up from the previous limit of 60 characters. This applies to, for
example, host name-related columns in the data dictionary, mysql system schema, Performance
Schema, INFORMATION_SCHEMA, and sys schema; the MASTER_HOST value for the CHANGE
MASTER TO statement; the Host column in SHOW PROCESSLIST statement output; host names in
account names (such as used in account-management statements and in DEFINER attributes); and
host name-related command options and system variables.

Caveats:

• The increase in permitted host name length can affect tables with indexes on host name columns.
For example, tables in the mysql system schema that index host names now have an explicit
ROW_FORMAT attribute of DYNAMIC to accommodate longer index values.

• Some file name-valued configuration settings might be constructed based on the server host
name. The permitted values are constrained by the underlying operating system, which may
not permit file names long enough to include 255-character host names. This affects the
general_log_file, log_error, pid_file, relay_log, and slow_query_log_file
system variables and corresponding options. If host name-based values are too long for the OS,
explicit shorter values must be provided.

• Although the server now supports 255-character host names, connections to the server

established using the --ssl-mode=VERIFY_IDENTITY option are constrained by maximum host
name length supported by OpenSSL. Host name matches pertain to two fields of SSL certificates,
which have maximum lengths as follows: Common Name: maximum length 64; Subject Alternative
Name: maximum length as per RFC#1034.

• Plugins.

 Previously, MySQL plugins could be written in C or C++. MySQL header files used by

plugins now contain C++ code, which means that plugins must be written in C++, not C.

• C API.

 The MySQL C API now supports asynchronous functions for nonblocking communication
with the MySQL server. Each function is the asynchronous counterpart to an existing synchronous
function. The synchronous functions block if reads from or writes to the server connection must wait.
The asynchronous functions enable an application to check whether work on the server connection
is ready to proceed. If not, the application can perform other work before checking again later. See C
API Asynchronous Interface.

31

Features Added in MySQL 8.0

• Additional target types for casts.

 The functions CAST() and CONVERT() now support

conversions to types DOUBLE, FLOAT, and REAL. Added in MySQL 8.0.17. See Section 14.10, “Cast
Functions and Operators”.

• JSON schema validation.

 MySQL 8.0.17 adds two functions JSON_SCHEMA_VALID() and

JSON_SCHEMA_VALIDATION_REPORT() for validating JSON documents again JSON schemas.
JSON_SCHEMA_VALID() returns TRUE (1) if the document validates against the schema and
FALSE (0) if it does not. JSON_SCHEMA_VALIDATION_REPORT() returns a JSON document
containing detailed information about the results of the validation. The following statements apply to
both of these functions:

• The schema must conform to Draft 4 of the JSON Schema specification.

• required attributes are supported.

• External resources and the $ref keyword are not supported.

• Regular expression patterns are supported; invalid patterns are silently ignored.

See Section 14.17.7, “JSON Schema Validation Functions”, for more information and examples.

• Multi-valued indexes.

 Beginning with MySQL 8.0.17, InnoDB supports the creation of a multi-
valued index, which is a secondary index defined on a JSON column that stores an array of values
and which can have multiple index records for a single data record. Such an index uses a key part
definition such as CAST(data->'$.zipcode' AS UNSIGNED ARRAY). A multi-valued index is
used automatically by the MySQL optimizer for suitable queries, as can be viewed in the output of
EXPLAIN.

As part of this work, MySQL adds a new function JSON_OVERLAPS() and a new MEMBER OF()
operator for working with JSON documents, additionally extending the CAST() function with a new
ARRAY keyword, as described in the following list:

• JSON_OVERLAPS() compares two JSON documents. If they contain any key-value pairs or array

elements in common, the function returns TRUE (1); otherwise it returns FALSE (0). If both values
are scalars, the function performs a simple test for equality. If one argument is a JSON array and
the other is a scalar, the scalar is treated as an array element. Thus, JSON_OVERLAPS() acts as
a complement to JSON_CONTAINS().

• MEMBER OF() tests whether the first operand (a scalar or JSON document) is a member of the
JSON array passed as the second operand, returning TRUE (1) if it is, and FALSE (0) if it is not.
No type conversion of the operand is performed.

• CAST(expression AS type ARRAY) permits creation of a functional index by casting the
JSON array found in a JSON document at json_path to an SQL array. Type specifiers are
limited to those already supported by CAST(), with the exception of BINARY (not supported). This
usage of CAST() (and the ARRAY keyword) is supported only by InnoDB, and only for the creation
of a multi-valued index.

For detailed information about multi-valued indexes, including examples, see Multi-Valued
Indexes. Section 14.17.3, “Functions That Search JSON Values”, provides information about
JSON_OVERLAPS() and MEMBER OF(), along with examples of use.

• Hintable time_zone.

 As of MySQL 8.0.17, the time_zone session variable is hintable using

SET_VAR.

• Redo Log Archiving.

 As of MySQL 8.0.17, InnoDB supports redo log archiving. Backup utilities
that copy redo log records may sometimes fail to keep pace with redo log generation while a backup
operation is in progress, resulting in lost redo log records due to those records being overwritten. The
redo log archiving feature addresses this issue by sequentially writing redo log records to an archive
file. Backup utilities can copy redo log records from the archive file as necessary, thereby avoiding
the potential loss of data. For more information, see Redo Log Archiving.

32

Features Added in MySQL 8.0

• The Clone Plugin.

 As of MySQL 8.0.17, MySQL provides a clone plugin that permits cloning

InnoDB data locally or from a remote MySQL server instance. A local cloning operation stores
cloned data on the same server or node where the MySQL instance runs. A remote cloning operation
transfers cloned data over the network from a donor MySQL server instance to the recipient server or
node where the cloning operation was initiated.

The clone plugin supports replication. In addition to cloning data, a cloning operation extracts and
transfers replication coordinates from the donor and applies them on the recipient, which enables
using the clone plugin for provisioning Group Replication members and replicas. Using the clone
plugin for provisioning is considerably faster and more efficient than replicating a large number of
transactions. Group Replication members can also be configured to use the clone plugin as an
alternative method of recovery, so that members automatically choose the most efficient way to
retrieve group data from seed members.

For more information, see Section 7.6.7, “The Clone Plugin”, and Section 20.5.4.2, “Cloning for
Distributed Recovery”.

As of MySQL 8.0.27, concurrent DDL operations on the donor MySQL Server instance are permitted
while a cloning operation is in progress. Previously, a backup lock was held during the cloning
operation, preventing concurrent DDL on the donor. To revert to the previous behavior of blocking
concurrent DDL on the donor during a clone operation, enable the clone_block_ddl variable. See
Section 7.6.7.4, “Cloning and Concurrent DDL”.

As of MySQL 8.0.29, the clone_delay_after_data_drop variable permits specifying a delay
period immediately after removing existing data on the recipient MySQL Server instance at the start
of a remote cloning operation. The delay is intended to provide enough time for the file system on the
recipient host to free space before data is cloned from the donor MySQL Server instance. Certain file
systems free space asynchronously in a background process. On these file systems, cloning data
too soon after dropping existing data can result in clone operation failures due to insufficient space.
The maximum delay period is 3600 seconds (1 hour). The default setting is 0 (no delay).

As of MySQL 8.0.37, cloning is allowed between different point releases. In other words, only the
major and minor version numbers must match when previously the point release number also had to
match.

For example, clone functionality now permits cloning 8.0.37 to 8.0.41 or 8.0.51 to 8.0.39. Previous
restrictions still apply to versions older than 8.0.37, so cloning the likes of 8.0.36 to 8.0.42 or vice-
versa is not permitted.

• Hash Join Optimization.

 Beginning with MySQL 8.0.18, a hash join is used whenever each pair

of tables in a join includes at least one equi-join condition, and no indexes apply to any join condition.
A hash join does not require indexes, although it can be used with indexes applying to single-table
predicates only. A hash join is more efficient in most cases than the block-nested loop algorithm.
Joins such as those shown here can be optimized in this manner:

SELECT *
    FROM t1
    JOIN t2
        ON t1.c1=t2.c1;

SELECT *
    FROM t1
    JOIN t2
        ON (t1.c1 = t2.c1 AND t1.c2 < t2.c2)
    JOIN t3

33

Features Added in MySQL 8.0

        ON (t2.c1 = t3.c1)

Hash joins can also be used for Cartesian products—that is, when no join condition is specified.

You can see when the hash join optimization is being used for a particular query using EXPLAIN
FORMAT=TREE or EXPLAIN ANALYZE. (In MySQL 8.0.20 and later, you can also use EXPLAIN,
omitting FORMAT=TREE.)

The amount of memory available to a hash join is limited by the value of join_buffer_size. A
hash join that requires more than this much memory is executed on disk; the number of disk files that
can be used by an on-disk hash join is limited by open_files_limit.

As of MySQL 8.0.19, the hash_join optimizer switch which was introduced in MySQL 8.0.18 no
longer supported (hash_join=on still appears as part of the value of optimizer_switch, but setting it
no longer has any effect). The HASH_JOIN and NO_HASH_JOIN optimizer hints are also no longer
supported. The switch and the hint are both now deprecated; expect them to be removed in a future
MySQL release. In MySQL 8.0.18 and later, hash joins can be disabled using the NO_BNL optimizer
switch.

In MySQL 8.0.20 and later, block nested loop is no longer used in the MySQL server, and a hash join
is employed any time a block nested loop would have been used previously, even when the query
contains no equi-join conditions. This applies to inner non-equijoins, semijoins, antijoins, left outer
joins, and right outer joins. The block_nested_loop flag for the optimizer_switch system
variable as well as the BNL and NO_BNL optimizer hints are still supported, but henceforth control
use of hash joins only. In addition, both inner and outer joins (including semijoins and antijoins) can
now employ batched key access (BKA), which allocates join buffer memory incrementally so that
individual queries need not use up large amounts of resources that they do not actually require for
resolution. BKA for inner joins only is supported starting with MySQL 8.0.18.

MySQL 8.0.20 also replaces the executor used in previous versions of MySQL with the iterator
executor. This work includes replacement of the old index subquery engines that governed queries of
the form WHERE value IN (SELECT column FROM table WHERE ...) for those IN queries
which have not been optimized as semijoins, as well as queries materialized in the same form, which
formerly depended on the old executor.

For more information and examples, see Section 10.2.1.4, “Hash Join Optimization”. See also
Batched Key Access Joins.

• EXPLAIN ANALYZE Statement.

 A new form of the EXPLAIN statement, EXPLAIN ANALYZE,
is implemented in MySQL 8.0.18, providing expanded information about the execution of SELECT
statements in TREE format for each iterator used in processing the query, and making it possible to
compare estimated cost with the actual cost of the query. This information includes startup cost, total
cost, number of rows returned by this iterator, and the number of loops executed.

In MySQL 8.0.21 and later, this statement also supports a FORMAT=TREE specifier. TREE is the only
supported format.

See Obtaining Information with EXPLAIN ANALYZE, for more information.

• Query cast injection.

 In version 8.0.18 and later, MySQL injects cast operations into the query

item tree inside expressions and conditions in which the data type of the argument and the expected
data type do not match. This has no effect on query results or speed of execution, but makes the
query as executed equivalent to one which is compliant with the SQL standard while maintaining
backwards compatibility with previous releases of MySQL.

Such implicit casts are now performed between temporal types (DATE, DATETIME, TIMESTAMP,
TIME) and numeric types (SMALLINT, TINYINT, MEDIUMINT, INT/INTEGER, BIGINT;
DECIMAL/NUMERIC; FLOAT, DOUBLE, REAL; BIT) whenever they are compared using any of the
standard numeric comparison operators (=, >=, >, <, <=, <>/!=, or <=>). In this case, any value
that is not already a DOUBLE is cast as one. Cast injection is also now performed for comparisons

34

Features Added in MySQL 8.0

between DATE or TIME values and DATETIME values, where the arguments are cast whenever
necessary as DATETIME.

Beginning with MySQL 8.0.21, such casts are also performed when comparing string types with
other types. String types that are cast include CHAR, VARCHAR, BINARY, VARBINARY, BLOB, TEXT,
ENUM, and SET. When comparing a value of a string type with a numeric type or YEAR, the string
cast is to DOUBLE; if the type of the other argument is not FLOAT, DOUBLE, or REAL, it is also cast to
DOUBLE. When comparing a string type to a DATETIME or TIMESTAMP value, the string is cast is to
DATETIME; when comparing a string type with DATE, the string is cast to DATE.

It is possible to see when casts are injected into a given query by viewing the output of EXPLAIN
ANALYZE, EXPLAIN FORMAT=JSON, or, as shown here, EXPLAIN FORMAT=TREE:

mysql> CREATE TABLE d (dt DATETIME, d DATE, t TIME);
Query OK, 0 rows affected (0.62 sec)

mysql> CREATE TABLE n (i INT, d DECIMAL, f FLOAT, dc DECIMAL);
Query OK, 0 rows affected (0.51 sec)

mysql> CREATE TABLE s (c CHAR(25), vc VARCHAR(25),
    ->     bn BINARY(50), vb VARBINARY(50), b BLOB, t TEXT,
    ->     e ENUM('a', 'b', 'c'), se SET('x' ,'y', 'z'));
Query OK, 0 rows affected (0.50 sec)

mysql> EXPLAIN FORMAT=TREE SELECT * from d JOIN n ON d.dt = n.i\G
*************************** 1. row ***************************
EXPLAIN: -> Inner hash join (cast(d.dt as double) = cast(n.i as double))
(cost=0.70 rows=1)
    -> Table scan on n  (cost=0.35 rows=1)
    -> Hash
        -> Table scan on d  (cost=0.35 rows=1)

mysql> EXPLAIN FORMAT=TREE SELECT * from s JOIN d ON d.dt = s.c\G
*************************** 1. row ***************************
EXPLAIN: -> Inner hash join (d.dt = cast(s.c as datetime(6)))  (cost=0.72 rows=1)
    -> Table scan on d  (cost=0.37 rows=1)
    -> Hash
        -> Table scan on s  (cost=0.35 rows=1)

1 row in set (0.01 sec)

mysql> EXPLAIN FORMAT=TREE SELECT * from n JOIN s ON n.d = s.c\G
*************************** 1. row ***************************
EXPLAIN: -> Inner hash join (cast(n.d as double) = cast(s.c as double))  (cost=0.70 rows=1)
    -> Table scan on s  (cost=0.35 rows=1)
    -> Hash
        -> Table scan on n  (cost=0.35 rows=1)

1 row in set (0.00 sec)

Such casts can also be seen by executing EXPLAIN [FORMAT=TRADITIONAL], in which case it is
also necessary to issue SHOW WARNINGS after executing the EXPLAIN statement.

• Time zone support for TIMESTAMP and DATETIME.

 As of MySQL 8.0.19, the server accepts
a time zone offset with inserted datetime (TIMESTAMP and DATETIME) values. This offset uses the
same format as that employed when setting the time_zone system variable, except that a leading
zero is required when the hours portion of the offset is less than 10, and '-00:00' is not allowed.

35

Features Added in MySQL 8.0

Examples of datetime literals that include time zone offsets are '2019-12-11 10:40:30-05:00',
'2003-04-14 03:30:00+10:00', and '2020-01-01 15:35:45+05:30'.

Time zone offsets are not displayed when selecting datetime values.

Datetime literals incorporating time zone offsets can be used as prepared statement parameter
values.

As part of this work, the value used to set the time_zone system variable is now also restricted to
the range -13:59 to +14:00, inclusive. (It remains possible to assign name values to time_zone
such as 'EST', 'Posix/Australia/Brisbane', and 'Europe/Stockholm' to this variable,
provided that the MySQL time zone tables are loaded; see Populating the Time Zone Tables).

For more information and examples, see Section 7.1.15, “MySQL Server Time Zone Support”, as
well as Section 13.2.2, “The DATE, DATETIME, and TIMESTAMP Types”.

• Precise information for JSON schema CHECK constraint failures.

 When using

JSON_SCHEMA_VALID() to specify a CHECK constraint, MySQL 8.0.19 and later provides precise
information about the reasons for failures of such constraints.

For examples and more information, see JSON_SCHEMA_VALID() and CHECK constraints. See
also Section 15.1.20.6, “CHECK Constraints”.

• Row and column aliases with ON DUPLICATE KEY UPDATE.

 Beginning with MySQL 8.0.19,

it is possible to reference the row to be inserted, and, optionally, its columns, using aliases. Consider
the following INSERT statement on a table t having columns a and b:

INSERT INTO t SET a=9,b=5
    ON DUPLICATE KEY UPDATE a=VALUES(a)+VALUES(b);

Using the alias new for the new row, and, in some cases, the aliases m and n for this row's columns,
the INSERT statement can be rewritten in many different ways, some examples of which are shown
here:

INSERT INTO t SET a=9,b=5 AS new
    ON DUPLICATE KEY UPDATE a=new.a+new.b;

INSERT INTO t VALUES(9,5) AS new
    ON DUPLICATE KEY UPDATE a=new.a+new.b;

INSERT INTO t SET a=9,b=5 AS new(m,n)
    ON DUPLICATE KEY UPDATE a=m+n;

INSERT INTO t VALUES(9,5) AS new(m,n)
    ON DUPLICATE KEY UPDATE a=m+n;

For more information and examples, see Section 15.2.7.2, “INSERT ... ON DUPLICATE KEY
UPDATE Statement”.

• SQL standard explicit table clause and table value constructor.

 Added table value

constructors and explicit table clauses according to the SQL standard. These are implemented in
MySQL 8.0.19, respectively, as the TABLE statement and the VALUES statement.

The TABLE statement has the format TABLE table_name, and is equivalent to SELECT * FROM
table_name. It supports ORDER BY and LIMIT clauses ( the latter with optional OFFSET), but
does not allow for the selection of individual table columns. TABLE can be used anywhere that you

36

Features Added in MySQL 8.0

would employ the equivalent SELECT statement; this includes joins, unions, INSERT ... SELECT,
REPLACE, CREATE TABLE ... SELECT statements, and subqueries. For example:

• TABLE t1 UNION TABLE t2 is equivalent to SELECT * FROM t1 UNION SELECT * FROM

t2

• CREATE TABLE t2 TABLE t1 is equivalent to CREATE TABLE t2 SELECT * FROM t1

• SELECT a FROM t1 WHERE b > ANY (TABLE t2) is equivalent to SELECT a FROM t1

WHERE b > ANY (SELECT * FROM t2).

VALUES can be used to supply a table value to an INSERT, REPLACE, or SELECT statement, and
consists of the VALUES keyword followed by a series of row constructors (ROW()) separated by
commas. For example, the statement INSERT INTO t1 VALUES ROW(1,2,3), ROW(4,5,6),
ROW(7,8,9) provides an SQL-compliant equivalent to the MySQL-specific INSERT INTO t1
VALUES (1,2,3), (4,5,6), (7,8,9). You can also select from a VALUES table value
constructor just as you would a table, bearing in mind that you must supply a table alias when doing
so, and use this SELECT just as you would any other; this includes joins, unions, and subqueries.

For more information about TABLE and VALUES, and for examples of their use, see the following
sections of this documentation:

• Section 15.2.16, “TABLE Statement”

• Section 15.2.19, “VALUES Statement”

• Section 15.1.20.4, “CREATE TABLE ... SELECT Statement”

• Section 15.2.7.1, “INSERT ... SELECT Statement”

• Section 15.2.13.2, “JOIN Clause”

• Section 15.2.15, “Subqueries”

• Section 15.2.18, “UNION Clause”

• Optimizer hints for FORCE INDEX, IGNORE INDEX.

 MySQL 8.0 introduces index-level

optimizer hints which serve as analogs to the traditional index hints as described in Section 10.9.4,
“Index Hints”. The new hints are listed here, along with their FORCE INDEX or IGNORE INDEX
equivalents:

• GROUP_INDEX: Equivalent to FORCE INDEX FOR GROUP BY

NO_GROUP_INDEX: Equivalent to IGNORE INDEX FOR GROUP BY

• JOIN_INDEX: Equivalent to FORCE INDEX FOR JOIN

NO_JOIN_INDEX: Equivalent to IGNORE INDEX FOR JOIN

• ORDER_INDEX: Equivalent to FORCE INDEX FOR ORDER BY

NO_ORDER_INDEX: Equivalent to IGNORE INDEX FOR ORDER BY

• INDEX: Same as GROUP_INDEX plus JOIN_INDEX plus ORDER_INDEX; equivalent to FORCE

INDEX with no modifier

NO_INDEX: Same as NO_GROUP_INDEX plus NO_JOIN_INDEX plus NO_ORDER_INDEX;
equivalent to IGNORE INDEX with no modifier

For example, the following two queries are equivalent:

SELECT a FROM t1 FORCE INDEX (i_a) FOR JOIN WHERE a=1 AND b=2;

37

Features Added in MySQL 8.0

SELECT /*+ JOIN_INDEX(t1 i_a) */ a FROM t1 WHERE a=1 AND b=2;

The optimizer hints listed previously follow the same basic rules for syntax and usage as existing
index-level optimizer hints.

These optimizer hints are intended to replace FORCE INDEX and IGNORE INDEX, which we plan
to deprecate in a future MySQL release, and subsequently to remove from MySQL. They do not
implement a single exact equivalent for USE INDEX; instead, you can employ one or more of
NO_INDEX, NO_JOIN_INDEX, NO_GROUP_INDEX, or NO_ORDER_INDEX to achieve the same effect.

For further information and examples of use, see Index-Level Optimizer Hints.

• JSON_VALUE() function.

 MySQL 8.0.21 implements a new function JSON_VALUE() intended to

simplify indexing of JSON columns. In its most basic form, it takes as arguments a JSON document
and a JSON path pointing to a single value in that document, as well as (optionally) allowing you to
specify a return type with the RETURNING keyword. JSON_VALUE(json_doc, path RETURNING
type) is equivalent to this:

CAST(
    JSON_UNQUOTE( JSON_EXTRACT(json_doc, path) )
    AS type
);

You can also specify ON EMPTY, ON ERROR, or both clauses, similar to those employed with
JSON_TABLE().

You can use JSON_VALUE() to create an index on an expression on a JSON column like this:

CREATE TABLE t1(
    j JSON,
    INDEX i1 ( (JSON_VALUE(j, '$.id' RETURNING UNSIGNED)) )
);

INSERT INTO t1 VALUES ROW('{"id": "123", "name": "shoes", "price": "49.95"}');

A query using this expression, such as that shown here, can make use of the index:

SELECT j->"$.name" as name, j->"$.price" as price
    FROM t1
    WHERE JSON_VALUE(j, '$.id' RETURNING UNSIGNED) = 123;

In many cases, this is simpler than creating a generated column from the JSON column and then
creating an index on the generated column.

For more information and examples, see the description of JSON_VALUE().

• User comments and user attributes.

 MySQL 8.0.21 introduces the ability to set user comments

and user attributes when creating or updating user accounts. A user comment consists of arbitrary
text passed as the argument to a COMMENT clause used with a CREATE USER or ALTER USER
statement. A user attribute consists of data in the form of a JSON object passed as the argument
to an ATTRIBUTE clause used with either of these two statements. The attribute can contain any
valid key-value pairs in JSON object notation. Only one of COMMENT or ATTRIBUTE can be used in a
single CREATE USER or ALTER USER statement.

User comments and user attributes are stored together internally as a JSON object, the comment
text as the value of an element having comment as its key. This information can be retrieved from
the ATTRIBUTE column of the Information Schema USER_ATTRIBUTES table; since it is in JSON
format, you can use MySQL's JSON function and operators to parse its contents (see Section 14.17,

38

Features Added in MySQL 8.0

“JSON Functions”). Successive changes to the user attribute are merged with its current value as
when using the JSON_MERGE_PATCH() function.

Example:

mysql> CREATE USER 'mary'@'localhost' COMMENT 'This is Mary Smith\'s account';
Query OK, 0 rows affected (0.33 sec)

mysql> ALTER USER 'mary'@'localhost'
    -≫     ATTRIBUTE '{"fname":"Mary", "lname":"Smith"}';
Query OK, 0 rows affected (0.14 sec)

mysql> ALTER USER 'mary'@'localhost'
    -≫     ATTRIBUTE '{"email":"mary.smith@example.com"}';
Query OK, 0 rows affected (0.12 sec)

mysql> SELECT
    ->    USER,
    ->    HOST,
    ->    ATTRIBUTE->>"$.fname" AS 'First Name',
    ->    ATTRIBUTE->>"$.lname" AS 'Last Name',
    ->    ATTRIBUTE->>"$.email" AS 'Email',
    ->    ATTRIBUTE->>"$.comment" AS 'Comment'
    -> FROM INFORMATION_SCHEMA.USER_ATTRIBUTES
    -> WHERE USER='mary' AND HOST='localhost'\G
*************************** 1. row ***************************
      USER: mary
      HOST: localhost
First Name: Mary
 Last Name: Smith
     Email: mary.smith@example.com
   Comment: This is Mary Smith's account
1 row in set (0.00 sec)

For more information and examples, see Section 15.7.1.3, “CREATE USER Statement”,
Section 15.7.1.1, “ALTER USER Statement”, and Section 28.3.46, “The INFORMATION_SCHEMA
USER_ATTRIBUTES Table”.

• New optimizer_switch flags.

 MySQL 8.0.21 adds two new flags for the optimizer_switch

system variable, as described in the following list:

• prefer_ordering_index flag

By default, MySQL attempts to use an ordered index for any ORDER BY or GROUP BY query
that has a LIMIT clause, whenever the optimizer determines that this would result in faster
execution. Because it is possible in some cases that choosing a different optimization for such
queries actually performs better, it is now possible to disable this optimization by setting the
prefer_ordering_index flag to off.

The default value for this flag is on.

• subquery_to_derived flag

When this flag is set to on, the optimizer transforms eligible scalar subqueries into joins on derived
tables. For example, the query SELECT * FROM t1 WHERE t1.a > (SELECT COUNT(a)
FROM t2) is rewritten as SELECT t1.a FROM t1 JOIN ( SELECT COUNT(t2.a) AS c
FROM t2 ) AS d WHERE t1.a > d.c.

This optimization can be applied to a subquery which is part of a SELECT, WHERE, JOIN, or
HAVING clause; contains one or more aggregate functions but no GROUP BY clause; is not
correlated; and does not use any nondeterministic functions.

The optimization can also be applied to a table subquery which is the argument to IN, NOT IN,
EXISTS, or NOT EXISTS, and which does not contain a GROUP BY. For example, the query
SELECT * FROM t1 WHERE t1.b < 0 OR t1.a IN (SELECT t2.a + 1 FROM t2) is

39

Features Added in MySQL 8.0

rewritten as SELECT a, b FROM t1 LEFT JOIN (SELECT DISTINCT 1 AS e1, t2.a AS
e2 FROM t2) d ON t1.a + 1 = d.e2 WHERE t1.b < 0 OR d.e1 IS NOT NULL.

Starting with MySQL 8.0.24, this optimization can also be applied to a correlated scalar subquery
by applying an extra grouping to it, and then an outer join on the lifted predicate. For example, a
query such as SELECT * FROM t1 WHERE (SELECT a FROM t2 WHERE t2.a=t1.a) > 0
can be rewritten as SELECT t1.* FROM t1 LEFT OUTER JOIN (SELECT a, COUNT(*) AS
ct FROM t2 GROUP BY a) AS derived ON t1.a = derived.a WHERE derived.a >
0. MySQL performs a cardinality check to make sure that the subquery does not return more than
one row (ER_SUBQUERY_NO_1_ROW). See Section 15.2.15.7, “Correlated Subqueries”, for more
information.

This optimization is normally disabled, since it does not yield a noticeable performance benefit in
most cases; the flag is set to off by default.

For more information, see Section 10.9.2, “Switchable Optimizations”. See also Section 10.2.1.19,
“LIMIT Query Optimization”, Section 10.2.2.1, “Optimizing IN and EXISTS Subquery Predicates with
Semijoin Transformations”, and Section 10.2.2.4, “Optimizing Derived Tables, View References, and
Common Table Expressions with Merging or Materialization”.

• XML enhancements.

 As of MySQL 8.0.21, the LOAD XML statement now supports CDATA

sections in the XML to be imported.

• Casting to the YEAR type now supported.

 Beginning with MySQL 8.0.22, the server allows

casting to YEAR. Both the CAST() and CONVERT() functions support single-digit, two-digit, and four-
digit YEAR values. For one-digit and two-digit values, the allowed range is 0-99. Four-digit values
must be in the range 1901-2155. YEAR can also be used as the return type for the JSON_VALUE()
function; this function supports four-digit years only.

String, time-and-date, and floating-point values can all be cast to YEAR. Casting of GEOMETRY values
to YEAR is not supported.

For more information, including conversion rules, see the description of the CONVERT() function.

• Retrieval of TIMESTAMP values as UTC.

 MySQL 8.0.22 and later supports conversion of
a TIMESTAMP column value from the system time zone to a UTC DATETIME on retrieval, using
CAST(value AT TIME ZONE specifier AS DATETIME), where the specifier is one of
[INTERVAL] '+00:00' or 'UTC'. The precision of the DATETIME value returned by the cast
can be specified up to 6 decimal places, if desired. The ARRAY keyword is not supported with this
construct.

TIMESTAMP values inserted into a table using a timezone offset are also supported. Use of AT TIME
ZONE is not supported for CONVERT() or any other MySQL function or construct.

For further information and examples, see the description of the CAST() function.

• Dump file output synchronization.

 MySQL 8.0.22 and later supports periodic synchronization
when writing to files by SELECT INTO DUMPFILE and SELECT INTO OUTFILE statements. This
can be enabled by setting the select_into_disk_sync system variable to ON; the size of the
write buffer is determined by the value set for select_into_buffer_size; the default is 131072
(217) bytes.

In addition, an optional delay following synchronization to disk can be set using
select_into_disk_sync_delay; the default is no delay (0 milliseconds).

For more information, see the descriptions of the variables referenced previously in this item.

• Single preparation of statements.

 As of MySQL 8.0.22, a prepared statement is prepared a

single time, rather than once each time it is executed. This is done when executing PREPARE. This
is also true for any statement inside a stored procedure; the statement is prepared once, when the
stored procedure is first executed.

40

Features Added in MySQL 8.0

One result of this change is that the fashion in which dynamic parameters used in prepared
statements are resolved is also changed in the ways listed here:

• A prepared statement parameter is assigned a data type when the statement is prepared; the type
persists for each subsequent execution of the statement (unless the statement is reprepared; see
following).

Using a different data type for a given parameter or user variable within a prepared statement
for executions of the statement subsequent to the first execution may cause the statement to be
reprepared; for this reason, it is advisable to use the same data type for a given parameter when
re-executing a prepared statement.

• The following constructs employing window functions are no longer accepted, in order to align with

the SQL standard:

• NTILE(NULL)

• NTH_VALUE(expr, NULL)

• LEAD(expr, nn) and LAG(expr, nn), where nn is a negative number

This facilitates greater compliance with the SQL standard. See the individual function descriptions
for further details.

• A user variable referenced within a prepared statement now has its data type determined when the

statement is prepared; the type persists for each subsequent execution of the statement.

• A user variable referenced by a statement occurring within a stored procedure now has its data
type determined the first time the statement is executed; the type persists for any subsequent
invocation of the containing stored procedure.

• When executing a prepared statement of the form SELECT expr1, expr2, ... FROM table

ORDER BY ?, passing an integer value N for the parameter no longer causes ordering of the
results by the Nth expression in the select list; the results are no longer ordered, as is expected
with ORDER BY constant.

Preparing a statement used as a prepared statement or within a stored procedure only once
enhances the performance of the statement, since it negates the added cost of repeated preparation.
Doing so also avoids possible multiple rollbacks of preparation structures, which has been the source
of numerous issues in MySQL.

For more information, see Section 15.5.1, “PREPARE Statement”.

• RIGHT JOIN as LEFT JOIN handling.

 As of MySQL 8.0.22, the server handles all instances of
RIGHT JOIN internally as LEFT JOIN, eliminating a number of special cases in which a complete
conversion was not performed at parse time.

• Derived condition pushdown optimization.

 MySQL 8.0.22 (and later) implements derived

condition pushdown for queries having materialized derived tables. For a query such as SELECT
* FROM (SELECT i, j FROM t1) AS dt WHERE i > constant, it is now possible in many
cases to push the outer WHERE condition down to the derived table, in this case resulting in SELECT
* FROM (SELECT i, j FROM t1 WHERE i > constant) AS dt.

Previously, if the derived table was materialized and not merged, MySQL materialized the entire
table, then qualified the rows with the WHERE condition. Moving the WHERE condition into the
subquery using the derived condition pushdown optimization can often reduce the number of rows
must be processed, which can decrease the time needed to execute the query.

An outer WHERE condition can be pushed down directly to a materialized derived table when the
derived table does not use any aggregate or window functions. When the derived table has a GROUP

41

Features Added in MySQL 8.0

BY and does not use any window functions, the outer WHERE condition can be pushed down to the
derived table as a HAVING condition. The WHERE condition can also be pushed down when the
derived table uses a window function and the outer WHERE references columns used in the window
function's PARTITION clause.

Derived condition pushdown is enabled by default, as indicated by the optimizer_switch
system variable's derived_condition_pushdown flag. The flag, added in MySQL 8.0.22,
is set to on by default; to disable the optimization for a specific query, you can use the
NO_DERIVED_CONDITION_PUSHDOWN optimizer hint (also added in MySQL 8.0.22). If the
optimization is disabled due to derived_condition_pushdown being set to off, you can enable
it for a given query using DERIVED_CONDITION_PUSHDOWN.

The derived condition pushdown optimization cannot be employed for a derived table that contains
a LIMIT clause. Prior to MySQL 8.0.29, the optimization also cannot be used when the query
contains UNION. In MySQL 8.0.29 and later, conditions can be pushed down to both query blocks of
a union in most cases; see Section 10.2.2.5, “Derived Condition Pushdown Optimization”, for more
information.

In addition, a condition that itself uses a subquery cannot be pushed down, and a WHERE condition
cannot be pushed down to a derived table that is also an inner table of an outer join. For additional
information and examples, see Section 10.2.2.5, “Derived Condition Pushdown Optimization”.

• Non-locking reads on MySQL grant tables.

 As of MySQL 8.0.22, to permit concurrent DML

and DDL operations on MySQL grant tables, read operations that previously acquired row locks on
MySQL grant tables are executed as non-locking reads.

The operations that are now performed as non-locking reads on MySQL grant tables include:

• SELECT statements and other read-only statements that read data from grant tables through join
lists and subqueries, including SELECT ... FOR SHARE statements, using any transaction
isolation level.

• DML operations that read data from grant tables (through join lists or subqueries) but do not

modify them, using any transaction isolation level.

For additional information, see Grant Table Concurrency.

• 64-bit support for FROM_UNIXTIME(), UNIX_TIMESTAMP(), CONVERT_TZ().

 As of MySQL

8.0.28, the functions FROM_UNIXTIME(), UNIX_TIMESTAMP(), and CONVERT_TZ() handle 64-bit
values on platforms that support them. This includes 64-bit versions of Linux, MacOS, and Windows.

On compatible platforms, UNIX_TIMESTAMP() now handles values up to '3001-01-18
23:59:59.999999' UTC, and FROM_UNIXTIME() can convert values up to 32536771199.999999
seconds since the Unix Epoch; CONVERT_TZ() now accepts values that do not exceed
'3001-01-18 23:59:59.999999' UTC following conversion.

The behavior of these functions on 32-bit platforms is unaffected by these changes. The behavior
of the TIMESTAMP type is also not affected (on any platform); for working with datetimes after
'2038-01-19 03:14:07.999999', UTC, use the DATETIME type instead.

For more information, see the descriptions of the individual functions just discussed, in Section 14.7,
“Date and Time Functions”.

• Resource allocation control.

 Beginning with MySQL 8.0.28, you can see the amount of memory
used for queries issued by all regular users by checking the Global_connection_memory status

42

Features Added in MySQL 8.0

variable. (This total does not include resources used by system users such as MySQL root. It is also
exclusive of any memory taken by the InnoDB buffer pool.)

To enable updates of Global_connection_memory, it is necessary to set
global_connection_memory_tracking = 1; this is 0 (off) by default. You can control how
often Global_connection_memory is updated by setting connection_memory_chunk_size.

It is also possible to set memory usage limits for normal users on the session or global level, or both,
by setting either or both of the system variables listed here:

• connection_memory_limit: Amount of memory allocated for each connection. Whenever this

limit is exceeded for any user, new queries from this user are rejected.

• global_connection_memory_limit: Amount of memory allocated for all connections.

Whenever this limit is exceeded, new queries from any regular user are rejected.

These limits do not apply to system processes or administrative accounts.

See the descriptions of the referenced variables for more information.

• Detached XA transactions.

 MySQL 8.0.29 adds support for XA transactions which, once
prepared, are no longer connected to the originating connection. This means that they can be
committed or rolled back by another connection, and that the current session can immediately begin
another transaction.

A system variable xa_detach_on_prepare controls whether XA transaction are detached; the
default is ON, which causes all XA transactions to be detached. Use of temporary tables is disallowed
for XA transactions when this is in effect.

For more information, see Section 15.3.8.2, “XA Transaction States”.

• Automatic binary log purge control.

 MySQL 8.0.29 adds the

binlog_expire_logs_auto_purge system variable, which provides a single interface for
enabling and disabling automatic purging of the binary logs. This is enabled (ON) by default; to
disable automatic purging of the binary log files, set this variable to OFF.

binlog_expire_logs_auto_purge must be ON in order for automatic purging of the binary log
files to proceed; the value of this variable takes precedence over that of any other server option or
variable, including (but not exclusive to) binlog_expire_logs_seconds.

The setting for binlog_expire_logs_auto_purge has no effect on PURGE BINARY LOGS.

• Conditional routine and trigger creation statements.
following statements support an IF NOT EXISTS option:

 Beginning with MySQL 8.0.29, the

• CREATE FUNCTION

• CREATE PROCEDURE

• CREATE TRIGGER

For CREATE FUNCTION when creating a stored function and CREATE PROCEDURE, this option
prevents an error from occurring if there is already a routine having the same name. For CREATE
FUNCTION when used to create a loadable function, the option prevents an error if there already
exists a loadable function having that name. For CREATE TRIGGER, the option prevents an error
from occurring if there already exists in the same schema and on the same table a trigger having the
same name.

This enhancement aligns the syntax of these statements more closely with that of CREATE
DATABASE, CREATE TABLE, CREATE USER, and CREATE EVENT (all of which already support IF

43

Features Added in MySQL 8.0

NOT EXISTS), and acts to complement the IF EXISTS option supported by DROP PROCEDURE,
DROP FUNCTION, and DROP TRIGGER statements.

For more information, see the descriptions of the indicated SQL statements, as well as Function
Name Resolution. See also Section 19.5.1.7, “Replication of CREATE TABLE ... SELECT
Statements”.

• Included FIDO library upgrade.

 MySQL 8.0.30 upgrades the included fido2 library (used with

the authentication_fido plugin) from version 1.5.0 to version 1.8.0.

See Section 8.4.1.11, “FIDO Pluggable Authentication”, for more information.

• Character sets: Language-specific collations.

 Previously, when more than one language had

the exact same collation definition, MySQL implemented collations for only one of the languages,
which meant that some languages were covered only by utf8mb4 Unicode 9.0 collations specific
to other languages. MySQL 8.0.30 (and later) fixes such issues by providing language-specific
collations for those languages that were previously covered only by language-specific collations for
other languages. Languages covered by the new collations are listed here:

• Norwegian (Nynorsk)

and

Norwegian (Bokmål)

• Serbian (Latin characters)

• Bosnian (Latin characters)

• Bulgarian

• Galician

• Mongolian (Cyrillic characters)

MySQL provides *_as_cs and *_ai_ci collations for each of the languages just listed.

For more information, see Language-Specific Collations.

• IF EXISTS and IGNORE UNKNOWN USER options for REVOKE.

 MySQL 8.0.30 implements

two new options for REVOKE which can be used to determine whether a statement yields an error or
a warning when a user, role, or privilege specified in the statement cannot be found, or cannot be
assigned. Very basic syntax showing the placement of these new options is provided here:

REVOKE [IF EXISTS] privilege_or_role
    ON object
    FROM user_or_role [IGNORE UNKNOWN USER]

IF EXISTS causes an unsuccessful REVOKE statement to raise a warning instead of an error, as
long as the named target user or role actually exists, despite any references in the statement to any
roles or privileges which cannot be found.

IGNORE UNKNOWN USER causes an unsuccessful REVOKE to raise a warning rather than an error
when the target user or role named in the statement cannot be found.

For further information and examples, see Section 15.7.1.8, “REVOKE Statement”.

• Generated invisible primary keys.

 Beginning with MySQL 8.0.30, it is possible to run a

replication source server such that a generated invisible primary key (GIPK) is added to any InnoDB
table that is created without an explicit primary key. The generated key column definition added to
such a table is equivalent to what is shown here:

my_row_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT INVISIBLE PRIMARY KEY

44

Features Added in MySQL 8.0

GIPK mode is not enabled by default. To enable it, set the
sql_generate_invisible_primary_key server system variable to ON.

Generated invisible primary keys are normally visible in the output of statements such as SHOW
CREATE TABLE and SHOW INDEX, as well as in MySQL Information Schema tables such as the
COLUMNS and STATISTICS tables. You can cause them to be hidden in such cases instead, by
setting show_gipk_in_create_table_and_information_schema to OFF.

As part of this work, a new --skip-generated-invisible-primary-key option is added to
mysqldump and mysqlpump to exclude generated invisible primary keys, columns, and column
values from their output.

GIPKs and replication between tables with or without primary keys.
a replica effectively ignores any setting for sql_generate_invisible_primary_key on the
source, such that it has no effect on replicated tables. MySQL 8.0.32 and later makes it possible
for the replica to add a generated invisible primary key to any InnoDB table that otherwise, as
replicated, has no primary key. You can do this by invoking CHANGE REPLICATION SOURCE
TO ... REQUIRE_TABLE_PRIMARY_KEY_CHECK = GENERATE on the replica.

 In MySQL Replication,

REQUIRE_TABLE_PRIMARY_KEY_CHECK = GENERATE is not compatible with MySQL Group
Replication.

For further information, see Section 15.1.20.11, “Generated Invisible Primary Keys”.

• Crash-safe XA transactions.

 Previously, XA transactions were not fully resilient to an

unexpected halt with respect to the binary log, and if this occurred while the server was executing XA
PREPARE, XA COMMIT, or XA ROLLBACK, the server was not guaranteed to be recoverable to the
correct state, possibly leaving the binary log with extra XA transactions that had not been applied, or
missing one or more XA transactions that had been applied. Beginning with MySQL 8.0.30, this is no
longer an issue, and a server that drops out of a replication topology for whatever reason can always
be brought back to a consistent XA transaction state when rejoining.

Known issue: When the same transaction XID is used to execute XA transactions sequentially
and a break occurs during the execution of XA COMMIT ... ONE PHASE, using this same XID,
after this transaction has been prepared in the storage engine, it may not be possible any longer to
synchronize the state between the binary log and the storage engine.

For more information, see Section 15.3.8.3, “Restrictions on XA Transactions”.

• Nesting with UNION.

 Beginning with MySQL 8.0.31, bodies of parenthesized query expressions

can be nested up to 63 levels deep in combination with UNION. Such queries were previously
rejected with error ER_NOT_SUPPORTED_YET, but are now allowed. EXPLAIN output for such a
query is shown here:

mysql> EXPLAIN FORMAT=TREE (
    ->   (SELECT a, b, c FROM t ORDER BY a LIMIT 3) ORDER BY b LIMIT 2
    -> ) ORDER BY c LIMIT 1\G
*************************** 1. row ***************************
EXPLAIN: -> Limit: 1 row(s)  (cost=5.55..5.55 rows=1)
    -> Sort: c, limit input to 1 row(s) per chunk  (cost=2.50 rows=0)
        -> Table scan on <result temporary>  (cost=2.50 rows=0)
            -> Temporary table  (cost=5.55..5.55 rows=1)
                -> Limit: 2 row(s)  (cost=2.95..2.95 rows=1)
                    -> Sort: b, limit input to 2 row(s) per chunk  (cost=2.50 rows=0)
                        -> Table scan on <result temporary>  (cost=2.50 rows=0)
                            -> Temporary table  (cost=2.95..2.95 rows=1)
                                -> Limit: 3 row(s)  (cost=0.35 rows=1)
                                    -> Sort: t.a, limit input to 3 row(s) per chunk  (cost=0.35 rows=1)
                                        -> Table scan on t  (cost=0.35 rows=1)

45

Features Added in MySQL 8.0

1 row in set (0.00 sec)

MySQL follows SQL standard semantics when collapsing bodies of parenthesized query
expressions, so that a higher outer limit cannot override an inner lower one. For example,
(SELECT ... LIMIT 5) LIMIT 10 can return no more than five rows.

The 63-level limit is imposed only after the MySQL Optimizer's parser has performed any
simplifications or merges which it can.

For more information, see Section 15.2.11, “Parenthesized Query Expressions”.

• Disabling query rewrites.

 Previously, when using the Rewriter plugin, all queries were subject

to being rewritten, regardless of user. This could be problematic in certain cases, such as when
administering the system, or when applying statements originating from a replication source or a
dump file created by mysqldump or another MySQL program. MySQL 8.0.31 provides a solution to
such issues by implementing a new user privilege SKIP_QUERY_REWRITE; statements issued by a
user having this privilege are ignored by Rewriter and not rewritten.

MySQL 8.0.31 also adds a new server system variable
rewriter_enabled_for_threads_without_privilege_checks. When set to OFF, rewritable
statements issued by threads for which PRIVILEGE_CHECKS_USER is NULL (such as replication
applier threads) are not rewritten by the Rewriter plugin. The default is ON, which means such
statements are rewritten.

For more information, see Section 7.6.4, “The Rewriter Query Rewrite Plugin”.

• Replication filtering of XA statements.

 Previously, the statements XA START, XA END, XA

COMMIT, and XA ROLLBACK were filtered by the default database whenever using --replicate-
do-db or --replicate-ignore-db, which could lead to missed transactions. As of MySQL
8.0.31, these statements are not filtered in such cases, regardless of the value of binlog_format.

• Replication filtering and privilege checks.

 Beginning with MySQL 8.0.31, when replication

filtering is in use, a replica no longer raises replication errors related to privilege checks or
require_row_format validation for events which are filtered out, making it possible to filter out
any transactions that fail validation.

Because privilege checks on filtered rows can no longer cause replication to stop, a replica can now
accept only the portion of a database to which a given user has been granted access; this is true as
long as updates to this part of the database are replicated only in row-based format.

This capability may also be of use when migrating to HeatWave Service from an on-premise or cloud
service which uses tables for administration or other purposes to which the inbound replication user
does not have access.

For more information, see Section 19.2.5, “How Servers Evaluate Replication Filtering Rules”, as
well as Section 19.5.1.29, “Replica Errors During Replication”.

• INTERSECT and EXCEPT table operators.

 MySQL 8.0.31 adds support for the SQL

INTERSECT and EXCEPT table operators. Where a and b represent result sets of queries, these
operators behave as follows:

• a INTERSECT b includes only rows appearing in both result sets a and b.

• a EXCEPT b returns only those rows from result set a which do not also appear in b.

INTERSECT DISTINCT, INTERSECT ALL, EXCEPT DISTINCT, and EXCEPT ALL are all
supported; DISTINCT is the default for both INTERSECT and EXCEPT (this is the same as for
UNION).

For more information and examples, see Section 15.2.8, “INTERSECT Clause”, and Section 15.2.4,
“EXCEPT Clause”.

46

Features Added in MySQL 8.0

• User-defined histograms.

 Beginning with MySQL 8.0.31, it is possible to set the histogram of a

column to a user-specified JSON value. This can be done using the following SQL syntax:

ANALYZE TABLE tbl_name
  UPDATE HISTOGRAM ON col_name
  USING DATA 'json_data'

This statement creates or overwrites a histogram for column col_name of table tbl_name using the
histogram's JSON representation json_data. After executing this statement, you can verify that the
histogram was created or updated by querying the Information Schema COLUMN_STATISTICS table,
like this:

SELECT HISTOGRAM FROM INFORMATION_SCHEMA.COLUMN_STATISTICS
  WHERE TABLE_NAME='tbl_name'
  AND COLUMN_NAME='col_name';

The column value returned should be the same json_data used in the previous ANALYZE TABLE
statement.

This can be of use in cases where values deemed important are missed by the histogram sampling
process. When this happens, you may want to modify the histogram or set your own histogram
based on the complete data set. In addition, sampling a large user data set and building a histogram
from it are resource-heavy operations which can impact user queries. With this enhancement,
histogram generation can be moved off the (primary) server and performed on a replica instead; the
generated histograms can then be assigned to the proper table columns on the source server.

For more information and examples, see Histogram Statistics Analysis.

• Server build ID (Linux).

 MySQL 8.0.31 adds the read-only build_id system variable for Linux

systems, where a 160-bit SHA1 signature is generated at compile time; the value of build_id is that
of the generated value converted to a hexadecimal string, providing a unique identifier for the build.

build_id is written to the server log each time MySQL starts.

If you build MySQL from source, you can observe that this value changes each time you recompile
the server. See Section 2.8, “Installing MySQL from Source”, for more information.

This variable is not supported on platforms other than Linux.

• Default EXPLAIN output format.

 MySQL 8.0.32 adds a system variable explain_format

which determines the format of the output from an EXPLAIN statement used to obtain a query
execution plan in the absence of any FORMAT option. For example, if the value of explain_format
is TREE, then the output from any such EXPLAIN uses the tree-like format, just as if the statement
had specified FORMAT=TREE.

This behavior is overridden by the value set in a FORMAT option. Suppose that explain_format
is set to TREE; even so, EXPLAIN FORMAT=JSON stmt displays the result using the JSON output
format.

For more information and examples, see the description of the explain_format system variable,
as well as Obtaining Execution Plan Information. There are also implications for the behavior of
EXPLAIN ANALYZE; see Obtaining Information with EXPLAIN ANALYZE.

• ST_TRANSFORM() Cartesian SRS support.

 Prior to MySQL 8.0.30, the ST_TRANSFORM()

function did not support Cartesian Spatial Reference Systems. In MySQL 8.0.30 and later, this
function provides support for the Popular Visualisation Pseudo Mercator (EPSG 1024) projection
method, used for WGS 84 Pseudo-Mercator (SRID 3857). MySQL 8.0.32 and later supports all
Cartesian SRSs, except for EPSG 1042, EPSG 1043, EPSG 9816, and EPSG 9826.

47

Features Deprecated in MySQL 8.0

• mysql client --system-command option.

 The --system-command option for the mysql client,

available in MySQL 8.0.40 and later, enables or disables the system command.

This option is enabled by default. To disable it, use --system-command=OFF or --skip-system-
command, which causes the system command to be rejected with an error.

• mysql client --commands option.

 The mysql client --commands option, introduced in MySQL

8.0.43, enables or disables most mysql client commands.

This option is enabled by default. To disable it, start the mysql client with --commands=OFF or --
skip-commands.

For more information, see Section 6.5.1.1, “mysql Client Options”.

Features Deprecated in MySQL 8.0

The following features are deprecated in MySQL 8.0 and may be removed in a future series. Where
alternatives are shown, applications should be updated to use them.

For applications that use features deprecated in MySQL 8.0 that have been removed in a higher
MySQL series, statements may fail when replicated from a MySQL 8.0 source to a higher-series
replica, or may have different effects on source and replica. To avoid such problems, applications that
use features deprecated in 8.0 should be revised to avoid them and use alternatives when possible.

• Wildcard characters in database grants.

 The use of the characters % and _ as wildcards in

database grants is deprecated as of MySQL 8.0.35. You should expect for the wildcard functionality
to removed in a future MySQL release and for these characters always to be treated as literals, as
they are already whenever the value of the partial_revokes server system variable is ON.

In addition, the treatment of % by the server as a synonym for localhost when checking privileges
is now also deprecated as of MySQL 8.0.35, and thus subject to removal in a future version of
MySQL.

• Pluggable FIDO authentication is deprecated in MySQL 8.0.35 and later.

• The --character-set-client-handshake option, originally intended for use with upgrades

from very old versions of MySQL, is now deprecated in MySQL 8.0.35 and later MySQL 8.0 releases,
where a warning is issued whenever it is used. You should expect this option to be removed in a
future version of MySQL; applications depending on this option should begin migration away from it
as soon as possible.

• The old and new server system variables and related server options are deprecated in MySQL 8.0,
beginning with MySQL 8.0.35. A warning is now issued whenever either of these variables is set or
read. Because these variables are destined for removal in a future version of MySQL, applications
which depend on them should begin migration away from them as soon as possible.

• Legacy audit log filtering mode is deprecated as of MySQL 8.0.34. New deprecation warnings are
emitted for legacy audit log filtering system variables. These deprecated variables are either read-
only or dynamic.

(Read-only) audit_log_policy now writes a warning message to the MySQL server error log
during server startup when the value is not ALL (default value).

(Dynamic) audit_log_include_accounts, audit_log_exclude_accounts,
audit_log_statement_policy, and audit_log_connection_policy. Dynamic variables
print a warning message based on usage:

• Passing in a non-NULL value to audit_log_include_accounts or

audit_log_exclude_accounts during MySQL server startup now writes a warning message to
the server error log.

48

Features Deprecated in MySQL 8.0

• Passing in a non-default value to audit_log_statement_policy or

audit_log_connection_policy during MySQL server startup now writes a warning message
to the server error log. ALL is the default value for both variables.

• Changing an existing value using SET syntax during a MySQL client session now writes a warning

message to the client log.

• Persisting a variable using SET PERSIST syntax during a MySQL client session now writes a

warning message to the client log.

• In MySQL 8.0.34 and later, the mysql_native_password authentication plugin is deprecated and
it now produces a deprecation warning in the server error log if an account attempts to authenticate
using mysql_native_password as an authentication method.

• The ssl_fips_mode server system variable, --ssl-fips-mode client option, and the

MYSQL_OPT_SSL_FIPS_MODE option are deprecated and subject to removal in a future version of
MySQL.

• The keyring_file and keyring_encrypted_file plugins are deprecated as of MySQL

8.0.34. These keyring plugins are superseded by the component_keyring_file and
component_keyring_encrypted_file components. For a concise comparison of keyring
components and plugins, see Section 8.4.4.1, “Keyring Components Versus Keyring Plugins”.

• As of MySQL 8.0.31, the keyring_oci plugin is deprecated and subject to removal in a future
release of MySQL. Instead, consider using the component_keyring_oci component for
storing keyring data (see Section 8.4.4.11, “Using the Oracle Cloud Infrastructure Vault Keyring
Component”).

• The utf8mb3 character set is deprecated. Please use utf8mb4 instead.

• The following character sets are deprecated:

• ucs2 (see Section 12.9.4, “The ucs2 Character Set (UCS-2 Unicode Encoding)”)

• macroman and macce (see Section 12.10.2, “West European Character Sets”, and

Section 12.10.3, “Central European Character Sets”)

• dec (see Section 12.10.2, “West European Character Sets”)

• hp8 (see Section 12.10.2, “West European Character Sets”)

In MySQL 8.0.28 and later, any of these character sets or their collations produces a deprecation
warning when used in either of the following ways:

• When starting the MySQL server with --character-set-server or --collation-server

• When specified in any SQL statement, including but not limited to CREATE TABLE, CREATE

DATABASE, SET NAMES, and ALTER TABLE

You should use utf8mb4 instead any of the character sets listed previously.

User-defined collations are deprecated. Beginning with MySQL 8.0.33, either of the following causes
a warning to be written to the log:

• Use of COLLATE in any SQL statement together with the name of a user-defined collation

• Using the name of a user-defined collation for the value of collation_server,

collation_database, or collation_connection.

You should expect support for user-defined collations to be removed in a future version of MySQL.

49

Features Deprecated in MySQL 8.0

• Because caching_sha2_password is the default authentication plugin in MySQL 8.0 and provides
a superset of the capabilities of the sha256_password authentication plugin, sha256_password
is deprecated; expect it to be removed in a future version of MySQL. MySQL accounts that
authenticate using sha256_password should be migrated to use caching_sha2_password
instead.

• The validate_password plugin has been reimplemented to use the component infrastructure. The
plugin form of validate_password is still available but is now deprecated; expect it to be removed
in a future version of MySQL. MySQL installations that use the plugin should make the transition
to using the component instead. See Section 8.4.3.3, “Transitioning to the Password Validation
Component”.

• The ENGINE clause for the ALTER TABLESPACE and DROP TABLESPACE statements is deprecated.

• The PAD_CHAR_TO_FULL_LENGTH SQL mode is deprecated.

• AUTO_INCREMENT support is deprecated for columns of type FLOAT and DOUBLE (and any

synonyms). Consider removing the AUTO_INCREMENT attribute from such columns, or convert them
to an integer type.

• The UNSIGNED attribute is deprecated for columns of type FLOAT, DOUBLE, and DECIMAL (and any

synonyms). Consider using a simple CHECK constraint instead for such columns.

• FLOAT(M,D) and DOUBLE(M,D) syntax to specify the number of digits for columns of type FLOAT
and DOUBLE (and any synonyms) is a nonstandard MySQL extension. This syntax is deprecated.

• The ZEROFILL attribute is deprecated for numeric data types, as is the display width attribute for

integer data types. Consider using an alternative means of producing the effect of these attributes.
For example, applications could use the LPAD() function to zero-pad numbers up to the desired
width, or they could store the formatted numbers in CHAR columns.

• For string data types, the BINARY attribute is a nonstandard MySQL extension that is shorthand

for specifying the binary (_bin) collation of the column character set (or of the table default
character set if no column character set is specified). In MySQL 8.0, this nonstandard use of
BINARY is ambiguous because the utf8mb4 character set has multiple _bin collations, so the
BINARY attribute is deprecated; expect support for it to be removed in a future version of MySQL.
Applications should be adjusted to use an explicit _bin collation instead.

The use of BINARY to specify a data type or character set remains unchanged.

• Previous versions of MySQL supported the nonstandard shorthand expressions ASCII and

UNICODE, respectively, for CHARACTER SET latin1 and CHARACTER SET ucs2. ASCII and
UNICODE are deprecated (MySQL 8.0.28 and later) and now produce a warning. Use CHARACTER
SET instead, in both cases.

• The nonstandard C-style &&, ||, and ! operators that are synonyms for the standard SQL AND, OR,
and NOT operators, respectively, are deprecated. Applications that use the nonstandard operators
should be adjusted to use the standard operators.

Note

Use of || is deprecated unless the PIPES_AS_CONCAT SQL mode is
enabled. In that case, || signifies the SQL-standard string concatenation
operator).

• The JSON_MERGE() function is deprecated. Use JSON_MERGE_PRESERVE() instead.

• The SQL_CALC_FOUND_ROWS query modifier and accompanying FOUND_ROWS() function are
deprecated. See the FOUND_ROWS() description for information about an alternative strategy.

• Support for TABLESPACE = innodb_file_per_table and TABLESPACE =

innodb_temporary clauses with CREATE TEMPORARY TABLE is deprecated as of MySQL 8.0.13.

50

Features Deprecated in MySQL 8.0

• For SELECT statements, use of an INTO clause after FROM but not at the end of the SELECT is
deprecated as of MySQL 8.0.20. It is preferred to place the INTO at the end of the statement.

For UNION statements, these two variants containing INTO are deprecated as of MySQL 8.0.20:

• In the trailing query block of a query expression, use of INTO before FROM.

• In a parenthesized trailing block of a query expression, use of INTO, regardless of its position

relative to FROM.

See Section 15.2.13.1, “SELECT ... INTO Statement”, and Section 15.2.18, “UNION Clause”.

• FLUSH HOSTS is deprecated as of MySQL 8.0.23. Instead, truncate the Performance Schema

host_cache table:

TRUNCATE TABLE performance_schema.host_cache;

The TRUNCATE TABLE operation requires the DROP privilege for the table.

• The mysql_upgrade client is deprecated because its capabilities for upgrading the system tables in
the mysql system schema and objects in other schemas have been moved into the MySQL server.
See Section 3.4, “What the MySQL Upgrade Process Upgrades”.

• The --no-dd-upgrade server option is deprecated. It is superseded by the --upgrade option,

which provides finer control over data dictionary and server upgrade behavior.

• The mysql_upgrade_info file, which is created data directory and used to store the MySQL

version number, is deprecated; expect it to be removed in a future version of MySQL.

• The relay_log_info_file system variable and --master-info-file option are deprecated.
Previously, these were used to specify the name of the relay log info log and source info log when
relay_log_info_repository=FILE and master_info_repository=FILE were set, but
those settings have been deprecated. The use of files for the relay log info log and source info log
has been superseded by crash-safe replica tables, which are the default in MySQL 8.0.

• The max_length_for_sort_data system variable is now deprecated due to optimizer changes

that make it obsolete and of no effect.

• These legacy parameters for compression of connections to the server are deprecated:

The --compress client command-line option; the MYSQL_OPT_COMPRESS option for the
mysql_options() C API function; the slave_compressed_protocol system variable. For
information about parameters to use instead, see Section 6.2.8, “Connection Compression Control”.

• Use of the MYSQL_PWD environment variable to specify a MySQL password is deprecated.

• Use of VALUES() to access new row values in INSERT ... ON DUPLICATE KEY UPDATE is

deprecated as of MySQL 8.0.20. Use aliases for the new row and columns, instead.

• Because specifying ON ERROR before ON EMPTY when invoking JSON_TABLE() is counter to the
SQL standard, this syntax is now deprecated in MySQL. Beginning with MySQL 8.0.20, the server
prints a warning whenever you attempt to do so. When specifying both of these clauses in a single
JSON_TABLE() invocation, make sure that ON EMPTY is used first.

• Columns with index prefixes have never been supported as part of a table's partitioning key;

previously, these were allowed when creating, altering, or upgrading partitioned tables but were
excluded by the table's partitioning function, and no warning that this had occurred was issued by
the server. This permissive behavior is now deprecated, and subject to removal in a future version
of MySQL in which using any such columns in the partitioning key causes the CREATE TABLE or
ALTER TABLE statement in they occur to be rejected.

As of MySQL 8.0.21, whenever columns using index prefixes are specified as part of the partitioning
key, a warning is generated for each such column. Whenever a CREATE TABLE or ALTER TABLE

51

Features Deprecated in MySQL 8.0

statement is rejected because all columns in the proposed partitioning key would have index
prefixes, the resulting error now provides the exact reason for the rejection. In either instance, this
includes cases in which the columns used in the partitioning function are defined implicitly as those in
the table's primary key by employing an empty PARTITION BY KEY() clause.

For more information and examples, see Column index prefixes not supported for key partitioning.

• The InnoDB memcached plugin is deprecated as of MySQL 8.0.22; expect support for it to be

removed in a future version of MySQL.

• The temptable_use_mmap variable is deprecated as of MySQL 8.0.26; expect support for it to be

removed in a future version of MySQL.

• The BINARY operator is deprecated as of MySQL 8.0.27, and you should expect its removal in a
future version of MySQL. Use of BINARY now causes a warning. Use CAST(... AS BINARY)
instead.

• The default_authentication_plugin variable is deprecated as of MySQL 8.0.27; expect

support for it to be removed in a future version of MySQL.

The default_authentication_plugin variable is still used in MySQL 8.0.27, but in conjunction
with and at a lower precedence than the new authentication_policy system variable, which is
introduced in MySQL 8.0.27 with the multifactor authentication feature. For details, see The Default
Authentication Plugin.

• The --abort-slave-event-count and --disconnect-slave-event-count server options,
used by the MySQL test suite and not normally used in production, are deprecated as of MySQL
8.0.29; expect both options to be removed in a future version of MySQL.

• The myisam_repair_threads system variable and myisamchk --parallel-recover option
are deprecated as of MySQL 8.0.29; expect support for both to be removed in a future release of
MySQL.

From MySQL 8.0.29, values other than 1 (the default) for myisam_repair_threads produce a
warning.

• Previously, MySQL accepted DATE, TIME, DATETIME, and TIMESTAMP literals containing an

arbitrary number of (arbitrary) delimiter characters, as well as DATETIME and TIMESTAMP literals
with an arbitrary number of whitespace characters before, after, and between the date and time
parts. As of MySQL 8.0.29, the server raises a deprecation warning whenever the literal value
contains any of the following:

• One or more nonstandard delimiter characters

• Excess delimiter characters

• Whitespace other than the space character (' ', 0x20)

• Excess space characters

One deprecation warning is issued per temporal value, even if there are multiple issues with it. This
warning is not promoted to an error in strict mode, so that performing an INSERT of such a value still
succeeds when strict mode is in effect.

You should expect the nonstandard behavior to be removed in a future version of MySQL, and take
steps now to insure that your applications do not depend on it.

See String and Numeric Literals in Date and Time Context, for more information and examples.

• The replica_parallel_type system variable and its associated server option --replica-

parallel-type are deprecated as of MySQL 8.0.29. Beginning with this release, reading or setting
this value raises a deprecation warning; expect it to be removed in a future version of MySQL.

52

Features Deprecated in MySQL 8.0

• Beginning with MySQL 8.0.30, setting the replica_parallel_workers system variable (or the
equivalent server option) to 0 is deprecated, and elicits a warning. When you want a replica to use
single threading, use replica_parallel_workers=1 instead, which produces the same result,
but with no warning.

• The --skip-host-cache server option is deprecated beginning with MySQL 8.0.30; expect its

removal in a future MySQL release. Use the host_cache_size system variable instead.

• The --old-style-user-limits option, intended for backwards compatibility with very old

(pre-5.0.3) releases, is deprecated as of MySQL 8.0.30; using it now raises a warning. You should
expect this option to be removed in a future release of MySQL.

• The innodb_log_files_in_group and innodb_log_file_size variables are deprecated as
of MySQL 8.0.30. These variables are superseded by the innodb_redo_log_capacity variable.
For more information, see Section 17.6.5, “Redo Log”.

• As of MySQL 8.0.32, the use of “FULL” as an unquoted identifier is deprecated, due to the fact that
it is a reserved keyword in the SQL standard. This means that a statement such as CREATE TABLE
full (c1 INT, c2 INT) now raises a warning (ER_WARN_DEPRECATED_IDENT). To prevent
this from happening, change the name or, as shown here, encase it in backticks (`):

CREATE TABLE `full` (c1 INT, c2 INT);

For more information, see Section 11.3, “Keywords and Reserved Words”.

• Beginning with MySQL 8.0.32, the use of the dollar sign ($) as the leading character of an unquoted
identifier is deprecated and produces a warning. Such usage is subject to removal in a future release
of MySQL. This includes identifiers used as names of databases, tables, views, columns, or stored
programs, as well as aliases for any of these. The dollar sign may still be used as the first character
of a quoted identifier. See Section 11.2, “Schema Object Names”, for more information.

• The binlog_format server system variable is deprecated as of MySQL 8.0.34, and is subject

to being removed in a future release. Changing the binary logging format, is also deprecated, with
the expectation that the removal of binlog_format will leave row-based binary logging, already
the default in MySQL 8.0, as the only binary logging format used or supported by MySQL. For this
reason, new MySQL installations should use only row-based binary logging; existing replication
setups using binlog_format=STATEMENT or binlog_format=MIXED logging format should be
migrated to the row-based format.

The system variables log_bin_trust_function_creators and
log_statements_unsafe_for_binlog, are used exclusively for statement-based logging and
replication. For this reason, they are now also deprecated, and subject to removal in a future version
of MySQL.

Setting or selecting the value of binlog_format, log_bin_trust_function_creators, or
log_statements_unsafe_for_binlog raises a warning in MySQL 8.0.34 and later.

• The mysqlpump client utility program is deprecated beginning with MySQL 8.0.34, and produces a

deprecation warning when invoked. This program is subject to removal in a future version of MySQL.
Since MySQL provides other means of performing database dumps and backups with the same or
additional functionality, including mysqldump and MySQL Shell, this program is now considered
redundant.

The associated lz4_decompress and zlib_decompress utilities are also deprecated as of
MySQL 8.0.34.

• The use of a version number without a whitespace character following (or end of comment) is

deprecated as of MySQL 8.0.34, and raises a warning. This statement raises a warning in MySQL
8.0.34 or later, as shown here:

mysql> CREATE TABLE t1(a INT, KEY (a)) /*!50110KEY_BLOCK_SIZE=1024*/ ENGINE=MYISAM;
Query OK, 0 rows affected, 1 warning (0.01 sec)

53

Features Removed in MySQL 8.0

mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
  Level: Warning
   Code: 4164
Message: Immediately starting the version comment after the version number is
deprecated and may change behavior in a future release. Please insert a
white-space character after the version number.
1 row in set (0.00 sec)

To avoid such warnings, insert one or more whitespace characters after the version number, like this:

mysql> CREATE TABLE t2(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024*/ ENGINE=MYISAM;
Query OK, 0 rows affected (0.00 sec)

See also Section 11.7, “Comments”.

• As of MySQL 8.0.34, the sync_relay_log_info system variable is deprecated, along with its
equivalent server startup option --sync-relay-log-info. You should expect support for this
variable, and for storing replication applier metadata in a file, to be removed in a future version of
MySQL. You are advised to update any of your MySQL applications which may depend on it before
this occurs.

• The binlog_transaction_dependency_tracking server system variable is deprecated as

of MySQL 8.0.35, and subject to removal in a future version of MySQL. Referencing this variable or
the equivalent mysqld startup option --binlog-transaction-dependency-tracking now
triggers a warning. There are no plans to replace this variable or its functionality, which is expected
later to be made internal to the server.

Features Removed in MySQL 8.0

The following items are obsolete and have been removed in MySQL 8.0. Where alternatives are
shown, applications should be updated to use them.

For MySQL 5.7 applications that use features removed in MySQL 8.0, statements may fail when
replicated from a MySQL 5.7 source to a MySQL 8.0 replica, or may have different effects on source
and replica. To avoid such problems, applications that use features removed in MySQL 8.0 should be
revised to avoid them and use alternatives when possible.

• The innodb_locks_unsafe_for_binlog system variable was removed. The READ COMMITTED

isolation level provides similar functionality.

• The information_schema_stats variable, introduced in MySQL 8.0.0, was removed and

replaced by information_schema_stats_expiry in MySQL 8.0.3.

information_schema_stats_expiry defines an expiration setting for cached
INFORMATION_SCHEMA table statistics. For more information, see Section 10.2.3, “Optimizing
INFORMATION_SCHEMA Queries”.

• Code related to obsolete InnoDB system tables was removed in MySQL 8.0.3.

INFORMATION_SCHEMA views based on InnoDB system tables were replaced by internal system
views on data dictionary tables. Affected InnoDB INFORMATION_SCHEMA views were renamed:

Table 1.1 Renamed InnoDB Information Schema Views

Old Name

INNODB_SYS_COLUMNS

INNODB_SYS_DATAFILES

INNODB_SYS_FIELDS

INNODB_SYS_FOREIGN

New Name

INNODB_COLUMNS

INNODB_DATAFILES

INNODB_FIELDS

INNODB_FOREIGN

INNODB_SYS_FOREIGN_COLS

INNODB_FOREIGN_COLS

54

Features Removed in MySQL 8.0

Old Name

INNODB_SYS_INDEXES

INNODB_SYS_TABLES

INNODB_SYS_TABLESPACES

INNODB_SYS_TABLESTATS

INNODB_SYS_VIRTUAL

New Name

INNODB_INDEXES

INNODB_TABLES

INNODB_TABLESPACES

INNODB_TABLESTATS

INNODB_VIRTUAL

After upgrading to MySQL 8.0.3 or later, update any scripts that reference previous InnoDB
INFORMATION_SCHEMA view names.

• The following features related to account management are removed:

• Using GRANT to create users. Instead, use CREATE USER. Following this practice makes the

NO_AUTO_CREATE_USER SQL mode immaterial for GRANT statements, so it too is removed, and
an error now is written to the server log when the presence of this value for the sql_mode option
in the options file prevents mysqld from starting.

• Using GRANT to modify account properties other than privilege assignments. This includes

authentication, SSL, and resource-limit properties. Instead, establish such properties at account-
creation time with CREATE USER or modify them afterward with ALTER USER.

• IDENTIFIED BY PASSWORD 'auth_string' syntax for CREATE USER and GRANT. Instead,
use IDENTIFIED WITH auth_plugin AS 'auth_string' for CREATE USER and ALTER
USER, where the 'auth_string' value is in a format compatible with the named plugin.

Additionally, because IDENTIFIED BY PASSWORD syntax was removed, the
log_builtin_as_identified_by_password system variable is superfluous and was
removed.

• The PASSWORD() function. Additionally, PASSWORD() removal means that SET PASSWORD ...

= PASSWORD('auth_string') syntax is no longer available.

• The old_passwords system variable.

55

Features Removed in MySQL 8.0

• The query cache was removed. Removal includes these items:

• The FLUSH QUERY CACHE and RESET QUERY CACHE statements.

• These system variables: query_cache_limit, query_cache_min_res_unit,

query_cache_size, query_cache_type, query_cache_wlock_invalidate.

• These status variables: Qcache_free_blocks, Qcache_free_memory,

Qcache_hits, Qcache_inserts, Qcache_lowmem_prunes, Qcache_not_cached,
Qcache_queries_in_cache, Qcache_total_blocks.

• These thread states: checking privileges on cached query, checking query cache

for query, invalidating query cache entries, sending cached result to
client, storing result in query cache, Waiting for query cache lock.

• The SQL_CACHE SELECT modifier.

These deprecated query cache items remain deprecated, but have no effect; expect them to be
removed in a future MySQL release:

• The SQL_NO_CACHE SELECT modifier.

• The ndb_cache_check_time system variable.

The have_query_cache system variable remains deprecated, and always has a value of NO;
expect it to be removed in a future MySQL release.

• The data dictionary provides information about database objects, so the server no longer checks
directory names in the data directory to find databases. Consequently, the --ignore-db-dir
option and ignore_db_dirs system variables are extraneous and are removed.

• The DDL log, also known as the metadata log, has been removed. Beginning with MySQL 8.0.3, this

functionality is handled by the data dictionary innodb_ddl_log table. See Viewing DDL Logs.

• The tx_isolation and tx_read_only system variables have been removed. Use

transaction_isolation and transaction_read_only instead.

• The sync_frm system variable has been removed because .frm files have become obsolete.

• The secure_auth system variable and --secure-auth client option have been removed. The

MYSQL_SECURE_AUTH option for the mysql_options() C API function was removed.

• The multi_range_count system variable is removed.

• The log_warnings system variable and --log-warnings server option have been removed. Use

the log_error_verbosity system variable instead.

• The global scope for the sql_log_bin system variable was removed. sql_log_bin has session
scope only, and applications that rely on accessing @@GLOBAL.sql_log_bin should be adjusted.

• The metadata_locks_cache_size and metadata_locks_hash_instances system variables

are removed.

• The unused date_format, datetime_format, time_format, and max_tmp_tables system

variables are removed.

• These deprecated compatibility SQL modes are removed: DB2, MAXDB, MSSQL, MYSQL323,

MYSQL40, ORACLE, POSTGRESQL, NO_FIELD_OPTIONS, NO_KEY_OPTIONS, NO_TABLE_OPTIONS.
They can no longer be assigned to the sql_mode system variable or used as permitted values for
the mysqldump --compatible option.

Removal of MAXDB means that the TIMESTAMP data type for CREATE TABLE or ALTER TABLE is
treated as TIMESTAMP, and is no longer treated as DATETIME.

56

Features Removed in MySQL 8.0

• The deprecated ASC or DESC qualifiers for GROUP BY clauses are removed. Queries that previously

relied on GROUP BY sorting may produce results that differ from previous MySQL versions. To
produce a given sort order, provide an ORDER BY clause.

• The EXTENDED and PARTITIONS keywords for the EXPLAIN statement have been removed. These

keywords are unnecessary because their effect is always enabled.

• These encryption-related items are removed:

• The ENCODE() and DECODE() functions.

• The ENCRYPT() function.

• The DES_ENCRYPT(), and DES_DECRYPT() functions, the --des-key-file option, the

have_crypt system variable, the DES_KEY_FILE option for the FLUSH statement, and the
HAVE_CRYPT CMake option.

In place of the removed encryption functions: For ENCRYPT(), consider using SHA2() instead for
one-way hashing. For the others, consider using AES_ENCRYPT() and AES_DECRYPT() instead.

• In MySQL 5.7, several spatial functions available under multiple names were deprecated to move

in the direction of making the spatial function namespace more consistent, the goal being that each
spatial function name begin with ST_ if it performs an exact operation, or with MBR if it performs an
operation based on minimum bounding rectangles. In MySQL 8.0, the deprecated functions are
removed to leave only the corresponding ST_ and MBR functions:

• These functions are removed in favor of the MBR names: Contains(), Disjoint(), Equals(),

Intersects(), Overlaps(), Within().

• These functions are removed in favor of the ST_ names: Area(), AsBinary(),

AsText(), AsWKB(), AsWKT(), Buffer(), Centroid(), ConvexHull(), Crosses(),
Dimension(), Distance(), EndPoint(), Envelope(), ExteriorRing(),
GeomCollFromText(), GeomCollFromWKB(), GeomFromText(), GeomFromWKB(),
GeometryCollectionFromText(), GeometryCollectionFromWKB(),
GeometryFromText(), GeometryFromWKB(), GeometryN(), GeometryType(),
InteriorRingN(), IsClosed(), IsEmpty(), IsSimple(), LineFromText(),
LineFromWKB(), LineStringFromText(), LineStringFromWKB(), MLineFromText(),
MLineFromWKB(), MPointFromText(), MPointFromWKB(), MPolyFromText(),
MPolyFromWKB(), MultiLineStringFromText(), MultiLineStringFromWKB(),
MultiPointFromText(), MultiPointFromWKB(), MultiPolygonFromText(),
MultiPolygonFromWKB(), NumGeometries(), NumInteriorRings(), NumPoints(),
PointFromText(), PointFromWKB(), PointN(), PolyFromText(), PolyFromWKB(),
PolygonFromText(), PolygonFromWKB(), SRID(), StartPoint(), Touches(), X(), Y().

• GLength() is removed in favor of ST_Length().

• The functions described in Section 14.16.4, “Functions That Create Geometry Values from WKB

Values” previously accepted either WKB strings or geometry arguments. Geometry arguments are
no longer permitted and produce an error. See that section for guidelines for migrating queries away
from using geometry arguments.

• The parser no longer treats \N as a synonym for NULL in SQL statements. Use NULL instead.

This change does not affect text file import or export operations performed with LOAD DATA
or SELECT ... INTO OUTFILE, for which NULL continues to be represented by \N. See
Section 15.2.9, “LOAD DATA Statement”.

• PROCEDURE ANALYSE() syntax is removed.

• The client-side --ssl and --ssl-verify-server-cert options have been removed. Use --
ssl-mode=REQUIRED instead of --ssl=1 or --enable-ssl. Use --ssl-mode=DISABLED

57

Features Removed in MySQL 8.0

instead of --ssl=0, --skip-ssl, or --disable-ssl. Use --ssl-mode=VERIFY_IDENTITY
instead of --ssl-verify-server-cert options. (The server-side --ssl option is still available,
but is deprecated as of MySQL 8.0.26 and subject to removal in a future MySQL version.)

For the C API, MYSQL_OPT_SSL_ENFORCE and MYSQL_OPT_SSL_VERIFY_SERVER_CERT
options for mysql_options() correspond to the client-side --ssl and --ssl-verify-
server-cert options and are removed. Use MYSQL_OPT_SSL_MODE with an option value of
SSL_MODE_REQUIRED or SSL_MODE_VERIFY_IDENTITY instead.

• The --temp-pool server option was removed.

• The ignore_builtin_innodb system variable is removed.

• The server no longer performs conversion of pre-MySQL 5.1 database names containing special
characters to 5.1 format with the addition of a #mysql50# prefix. Because these conversions are
no longer performed, the --fix-db-names and --fix-table-names options for mysqlcheck,
the UPGRADE DATA DIRECTORY NAME clause for the ALTER DATABASE statement, and the
Com_alter_db_upgrade status variable are removed.

Upgrades are supported only from one major version to another (for example, 5.0 to 5.1, or 5.1 to
5.5), so there should be little remaining need for conversion of older 5.0 database names to current
versions of MySQL. As a workaround, upgrade a MySQL 5.0 installation to MySQL 5.1 before
upgrading to a more recent release.

• The mysql_install_db program has been removed from MySQL distributions. Data directory

initialization should be performed by invoking mysqld with the --initialize or --initialize-
insecure option instead. In addition, the --bootstrap option for mysqld that was used by
mysql_install_db was removed, and the INSTALL_SCRIPTDIR CMake option that controlled the
installation location for mysql_install_db was removed.

• The generic partitioning handler was removed from the MySQL server. In order to support

partitioning of a given table, the storage engine used for the table must now provide its own (“native”)
partitioning handler. The --partition and --skip-partition options are removed from the
MySQL Server, and partitioning-related entries are no longer shown in the output of SHOW PLUGINS
or in the Information Schema PLUGINS table.

Two MySQL storage engines currently provide native partitioning support: InnoDB and NDB. Of
these, only InnoDB is supported in MySQL 8.0. Any attempt to create partitioned tables in MySQL
8.0 using any other storage engine fails.

Ramifications for upgrades.
 The direct upgrade of a partitioned table using a storage engine
other than InnoDB (such as MyISAM) from MySQL 5.7 (or earlier) to MySQL 8.0 is not supported.
There are two options for handling such a table:

• Remove the table's partitioning, using ALTER TABLE ... REMOVE PARTITIONING.

• Change the storage engine used for the table to InnoDB, with ALTER TABLE ...

ENGINE=INNODB.

At least one of the two operations just listed must be performed for each partitioned non-InnoDB
table prior to upgrading the server to MySQL 8.0. Otherwise, such a table cannot be used following
the upgrade.

Due to the fact that table creation statements that would result in a partitioned table using a storage
engine without partitioning support now fail with an error (ER_CHECK_NOT_IMPLEMENTED), you must
make sure that any statements in a dump file (such as that written by mysqldump) from an older
version of MySQL that you wish to import into a MySQL 8.0 server that create partitioned tables do

58

Features Removed in MySQL 8.0

not also specify a storage engine such as MyISAM that has no native partitioning handler. You can
do this by performing either of the following:

• Remove any references to partitioning from CREATE TABLE statements that use a value for the

STORAGE ENGINE option other than InnoDB.

• Specifying the storage engine as InnoDB, or allow InnoDB to be used as the table's storage

engine by default.

For more information, see Section 26.6.2, “Partitioning Limitations Relating to Storage Engines”.

• System and status variable information is no longer maintained in the INFORMATION_SCHEMA.
These tables are removed: GLOBAL_VARIABLES, SESSION_VARIABLES, GLOBAL_STATUS,
SESSION_STATUS. Use the corresponding Performance Schema tables instead. See
Section 29.12.14, “Performance Schema System Variable Tables”, and Section 29.12.15,
“Performance Schema Status Variable Tables”. In addition, the show_compatibility_56
system variable was removed. It was used in the transition period during which system and status
variable information in INFORMATION_SCHEMA tables was moved to Performance Schema tables,
and is no longer needed. These status variables are removed: Slave_heartbeat_period,
Slave_last_heartbeat, Slave_received_heartbeats, Slave_retried_transactions,
Slave_running. The information they provided is available in Performance Schema tables; see
Migrating to Performance Schema System and Status Variable Tables.

• The Performance Schema setup_timers table was removed, as was the TICK row in the

performance_timers table.

• The libmysqld embedded server library is removed, along with:

• The mysql_options() MYSQL_OPT_GUESS_CONNECTION,

MYSQL_OPT_USE_EMBEDDED_CONNECTION, MYSQL_OPT_USE_REMOTE_CONNECTION, and
MYSQL_SET_CLIENT_IP options

• The mysql_config --libmysqld-libs, --embedded-libs, and --embedded options

• The CMake WITH_EMBEDDED_SERVER, WITH_EMBEDDED_SHARED_LIBRARY, and

INSTALL_SECURE_FILE_PRIV_EMBEDDEDDIR options

• The (undocumented) mysql --server-arg option

• The mysqltest --embedded-server, --server-arg, and --server-file options

• The mysqltest_embedded and mysql_client_test_embedded test programs

• The mysql_plugin utility was removed. Alternatives include loading plugins at server startup using
the --plugin-load or --plugin-load-add option, or at runtime using the INSTALL PLUGIN
statement.

• The resolveip utility is removed. nslookup, host, or dig can be used instead.

• The resolve_stack_dump utility is removed. Stack traces from official MySQL builds are always

symbolized, so there is no need to use resolve_stack_dump.

• The following server error codes are not used and have been removed. Applications that test

specifically for any of these errors should be updated.

ER_BINLOG_READ_EVENT_CHECKSUM_FAILURE
ER_BINLOG_ROW_RBR_TO_SBR
ER_BINLOG_ROW_WRONG_TABLE_DEF
ER_CANT_ACTIVATE_LOG
ER_CANT_CHANGE_GTID_NEXT_IN_TRANSACTION
ER_CANT_CREATE_FEDERATED_TABLE
ER_CANT_CREATE_SROUTINE
ER_CANT_DELETE_FILE
ER_CANT_GET_WD

59

Features Removed in MySQL 8.0

ER_CANT_SET_GTID_PURGED_WHEN_GTID_MODE_IS_OFF
ER_CANT_SET_WD
ER_CANT_WRITE_LOCK_LOG_TABLE
ER_CREATE_DB_WITH_READ_LOCK
ER_CYCLIC_REFERENCE
ER_DB_DROP_DELETE
ER_DELAYED_NOT_SUPPORTED
ER_DIFF_GROUPS_PROC
ER_DISK_FULL
ER_DROP_DB_WITH_READ_LOCK
ER_DROP_USER
ER_DUMP_NOT_IMPLEMENTED
ER_ERROR_DURING_CHECKPOINT
ER_ERROR_ON_CLOSE
ER_EVENTS_DB_ERROR
ER_EVENT_CANNOT_DELETE
ER_EVENT_CANT_ALTER
ER_EVENT_COMPILE_ERROR
ER_EVENT_DATA_TOO_LONG
ER_EVENT_DROP_FAILED
ER_EVENT_MODIFY_QUEUE_ERROR
ER_EVENT_NEITHER_M_EXPR_NOR_M_AT
ER_EVENT_OPEN_TABLE_FAILED
ER_EVENT_STORE_FAILED
ER_EXEC_STMT_WITH_OPEN_CURSOR
ER_FAILED_ROUTINE_BREAK_BINLOG
ER_FLUSH_MASTER_BINLOG_CLOSED
ER_FORM_NOT_FOUND
ER_FOUND_GTID_EVENT_WHEN_GTID_MODE_IS_OFF__UNUSED
ER_FRM_UNKNOWN_TYPE
ER_GOT_SIGNAL
ER_GRANT_PLUGIN_USER_EXISTS
ER_GTID_MODE_REQUIRES_BINLOG
ER_GTID_NEXT_IS_NOT_IN_GTID_NEXT_LIST
ER_HASHCHK
ER_INDEX_REBUILD
ER_INNODB_NO_FT_USES_PARSER
ER_LIST_OF_FIELDS_ONLY_IN_HASH_ERROR
ER_LOAD_DATA_INVALID_COLUMN_UNUSED
ER_LOGGING_PROHIBIT_CHANGING_OF
ER_MALFORMED_DEFINER
ER_MASTER_KEY_ROTATION_ERROR_BY_SE
ER_NDB_CANT_SWITCH_BINLOG_FORMAT
ER_NEVER_USED
ER_NISAMCHK
ER_NO_CONST_EXPR_IN_RANGE_OR_LIST_ERROR
ER_NO_FILE_MAPPING
ER_NO_GROUP_FOR_PROC
ER_NO_RAID_COMPILED
ER_NO_SUCH_KEY_VALUE
ER_NO_SUCH_PARTITION__UNUSED
ER_OBSOLETE_CANNOT_LOAD_FROM_TABLE
ER_OBSOLETE_COL_COUNT_DOESNT_MATCH_CORRUPTED
ER_ORDER_WITH_PROC
ER_PARTITION_SUBPARTITION_ERROR
ER_PARTITION_SUBPART_MIX_ERROR
ER_PART_STATE_ERROR
ER_PASSWD_LENGTH
ER_QUERY_ON_MASTER
ER_RBR_NOT_AVAILABLE
ER_SKIPPING_LOGGED_TRANSACTION
ER_SLAVE_CHANNEL_DELETE
ER_SLAVE_MULTIPLE_CHANNELS_HOST_PORT
ER_SLAVE_MUST_STOP
ER_SLAVE_WAS_NOT_RUNNING
ER_SLAVE_WAS_RUNNING
ER_SP_GOTO_IN_HNDLR
ER_SP_PROC_TABLE_CORRUPT
ER_SQL_MODE_NO_EFFECT
ER_SR_INVALID_CREATION_CTX
ER_TABLE_NEEDS_UPG_PART
ER_TOO_MUCH_AUTO_TIMESTAMP_COLS

60

Features Removed in MySQL 8.0

ER_UNEXPECTED_EOF
ER_UNION_TABLES_IN_DIFFERENT_DIR
ER_UNSUPPORTED_BY_REPLICATION_THREAD
ER_UNUSED1
ER_UNUSED2
ER_UNUSED3
ER_UNUSED4
ER_UNUSED5
ER_UNUSED6
ER_VIEW_SELECT_DERIVED_UNUSED
ER_WRONG_MAGIC
ER_WSAS_FAILED

• The deprecated INFORMATION_SCHEMA INNODB_LOCKS and INNODB_LOCK_WAITS tables are
removed. Use the Performance Schema data_locks and data_lock_waits tables instead.

Note

In MySQL 5.7, the LOCK_TABLE column in the INNODB_LOCKS table and the
locked_table column in the sys schema innodb_lock_waits and x
$innodb_lock_waits views contain combined schema/table name values.
In MySQL 8.0, the data_locks table and the sys schema views contain
separate schema name and table name columns. See Section 30.4.3.9, “The
innodb_lock_waits and x$innodb_lock_waits Views”.

• InnoDB no longer supports compressed temporary tables. When innodb_strict_mode is enabled

(the default), CREATE TEMPORARY TABLE returns an error if ROW_FORMAT=COMPRESSED or
KEY_BLOCK_SIZE is specified. If innodb_strict_mode is disabled, warnings are issued and the
temporary table is created using a non-compressed row format.

• InnoDB no longer creates .isl files (InnoDB Symbolic Link files) when creating tablespace data

files outside of the MySQL data directory. The innodb_directories option now supports locating
tablespace files created outside of the data directory.

With this change, moving a remote tablespace while the server is offline by manually modifying
an .isl file is no longer supported. Moving remote tablespace files is now supported by the
innodb_directories option. See Section 17.6.3.6, “Moving Tablespace Files While the Server is
Offline”.

• The following InnoDB file format variables were removed:

• innodb_file_format

• innodb_file_format_check

• innodb_file_format_max

• innodb_large_prefix

File format variables were necessary for creating tables compatible with earlier versions of InnoDB
in MySQL 5.1. Now that MySQL 5.1 has reached the end of its product lifecycle, these options are no
longer required.

The FILE_FORMAT column was removed from the INNODB_TABLES and INNODB_TABLESPACES
Information Schema tables.

• The innodb_support_xa system variable, which enables support for two-phase commit in XA
transactions, was removed. InnoDB support for two-phase commit in XA transactions is always
enabled.

• Support for DTrace was removed.

• The JSON_APPEND() function was removed. Use JSON_ARRAY_APPEND() instead.

61

Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 8.0

• Support for placing table partitions in shared InnoDB tablespaces was removed in MySQL

8.0.13. Shared tablespaces include the InnoDB system tablespace and general tablespaces. For
information about identifying partitions in shared tablespaces and moving them to file-per-table
tablespaces, see Section 3.6, “Preparing Your Installation for Upgrade”.

• Support for setting user variables in statements other than SET was deprecated in MySQL 8.0.13.

This functionality is subject to removal in MySQL 8.4.

• The --ndb perror option was removed. Use the ndb_perror utility instead.

• The innodb_undo_logs variable was removed. The innodb_rollback_segments variables

performs the same function and should be used instead.

• The Innodb_available_undo_logs status variable was removed. The number of

available rollback segments per tablespace may be retrieved using SHOW VARIABLES LIKE
'innodb_rollback_segments';

• As of MySQL 8.0.14, the previously deprecated innodb_undo_tablespaces variable is no longer

configurable. For more information, see Section 17.6.3.4, “Undo Tablespaces”.

• Support for the ALTER TABLE ... UPGRADE PARTITIONING statement has been removed.

• As of MySQL 8.0.16, support for the internal_tmp_disk_storage_engine system variable has
been removed; internal temporary tables on disk now always use the InnoDB storage engine. See
Storage Engine for On-Disk Internal Temporary Tables,for more information.

• The DISABLE_SHARED CMake option was unused and has been removed.

• The myisam_repair_threads system variable is removed as of MySQL 8.0.30.

1.4 Server and Status Variables and Options Added, Deprecated,
or Removed in MySQL 8.0

• Options and Variables Introduced in MySQL 8.0

• Options and Variables Deprecated in MySQL 8.0

• Options and Variables Removed in MySQL 8.0

This section lists server variables, status variables, and options that were added for the first time, have
been deprecated, or have been removed in MySQL 8.0.

Options and Variables Introduced in MySQL 8.0

The following system variables, status variables, and server options have been added in MySQL 8.0.

• Acl_cache_items_count: Number of cached privilege objects. Added in MySQL 8.0.0.

• Audit_log_current_size: Audit log file current size. Added in MySQL 8.0.11.

• Audit_log_event_max_drop_size: Size of largest dropped audited event. Added in MySQL

8.0.11.

• Audit_log_events: Number of handled audited events. Added in MySQL 8.0.11.

• Audit_log_events_filtered: Number of filtered audited events. Added in MySQL 8.0.11.

• Audit_log_events_lost: Number of dropped audited events. Added in MySQL 8.0.11.

• Audit_log_events_written: Number of written audited events. Added in MySQL 8.0.11.

• Audit_log_total_size: Combined size of written audited events. Added in MySQL 8.0.11.

• Audit_log_write_waits: Number of write-delayed audited events. Added in MySQL 8.0.11.

62

Options and Variables Introduced in MySQL 8.0

• Authentication_ldap_sasl_supported_methods: Supported authentication methods for

SASL LDAP authentication. Added in MySQL 8.0.21.

• Caching_sha2_password_rsa_public_key: caching_sha2_password authentication plugin

RSA public key value. Added in MySQL 8.0.4.

• Com_alter_resource_group: Count of ALTER RESOURCE GROUP statements. Added in

MySQL 8.0.3.

• Com_alter_user_default_role: Count of ALTER USER ... DEFAULT ROLE statements. Added

in MySQL 8.0.0.

• Com_change_replication_source: Count of CHANGE REPLICATION SOURCE TO and

CHANGE MASTER TO statements. Added in MySQL 8.0.23.

• Com_clone: Count of CLONE statements. Added in MySQL 8.0.2.

• Com_create_resource_group: Count of CREATE RESOURCE GROUP statements. Added in

MySQL 8.0.3.

• Com_create_role: Count of CREATE ROLE statements. Added in MySQL 8.0.0.

• Com_drop_resource_group: Count of DROP RESOURCE GROUP statements. Added in MySQL

8.0.3.

• Com_drop_role: Count of DROP ROLE statements. Added in MySQL 8.0.0.

• Com_grant_roles: Count of GRANT ROLE statements. Added in MySQL 8.0.0.

• Com_install_component: Count of INSTALL COMPONENT statements. Added in MySQL 8.0.0.

• Com_replica_start: Count of START REPLICA and START SLAVE statements. Added in

MySQL 8.0.22.

• Com_replica_stop: Count of STOP REPLICA and STOP SLAVE statements. Added in MySQL

8.0.22.

• Com_restart: Count of RESTART statements. Added in MySQL 8.0.4.

• Com_revoke_roles: Count of REVOKE ROLES statements. Added in MySQL 8.0.0.

• Com_set_resource_group: Count of SET RESOURCE GROUP statements. Added in MySQL

8.0.3.

• Com_set_role: Count of SET ROLE statements. Added in MySQL 8.0.0.

• Com_show_replica_status: Count of SHOW REPLICA STATUS and SHOW SLAVE STATUS

statements. Added in MySQL 8.0.22.

• Com_show_replicas: Count of SHOW REPLICAS and SHOW SLAVE HOSTS statements. Added

in MySQL 8.0.22.

• Com_uninstall_component: Count of UINSTALL COMPONENT statements. Added in MySQL

8.0.0.

• Compression_algorithm: Compression algorithm for current connection. Added in MySQL

8.0.18.

• Compression_level: Compression level for current connection. Added in MySQL 8.0.18.

• Connection_control_delay_generated: How many times server delayed connection request.

Added in MySQL 8.0.1.

• Current_tls_ca: Current value of ssl_ca system variable. Added in MySQL 8.0.16.

63

Options and Variables Introduced in MySQL 8.0

• Current_tls_capath: Current value of ssl_capath system variable. Added in MySQL 8.0.16.

• Current_tls_cert: Current value of ssl_cert system variable. Added in MySQL 8.0.16.

• Current_tls_cipher: Current value of ssl_cipher system variable. Added in MySQL 8.0.16.

• Current_tls_ciphersuites: Current value of tsl_ciphersuites system variable. Added in MySQL

8.0.16.

• Current_tls_crl: Current value of ssl_crl system variable. Added in MySQL 8.0.16.

• Current_tls_crlpath: Current value of ssl_crlpath system variable. Added in MySQL 8.0.16.

• Current_tls_key: Current value of ssl_key system variable. Added in MySQL 8.0.16.

• Current_tls_version: Current value of tls_version system variable. Added in MySQL 8.0.16.

• Error_log_buffered_bytes: Number of bytes used in error_log table. Added in MySQL 8.0.22.

• Error_log_buffered_events: Number of events in error_log table. Added in MySQL 8.0.22.

• Error_log_expired_events: Number of events discarded from error_log table. Added in MySQL

8.0.22.

• Error_log_latest_write: Time of last write to error_log table. Added in MySQL 8.0.22.

• Firewall_access_denied: Number of statements rejected by MySQL Enterprise Firewall plugin.

Added in MySQL 8.0.11.

• Firewall_access_granted: Number of statements accepted by MySQL Enterprise Firewall

plugin. Added in MySQL 8.0.11.

• Firewall_cached_entries: Number of statements recorded by MySQL Enterprise Firewall

plugin. Added in MySQL 8.0.11.

• Global_connection_memory: Amount of memory currently used by all user threads. Added in

MySQL 8.0.28.

• Innodb_buffer_pool_resize_status_code: InnoDB buffer pool resize status code. Added in

MySQL 8.0.31.

• Innodb_buffer_pool_resize_status_progress: InnoDB buffer pool resize status progress.

Added in MySQL 8.0.31.

• Innodb_redo_log_capacity_resized: Redo log capacity after the last completed capacity

resize operation. Added in MySQL 8.0.30.

• Innodb_redo_log_checkpoint_lsn: The redo log checkpoint LSN. Added in MySQL 8.0.30.

• Innodb_redo_log_current_lsn: The redo log current LSN. Added in MySQL 8.0.30.

• Innodb_redo_log_enabled: InnoDB redo log status. Added in MySQL 8.0.21.

• Innodb_redo_log_flushed_to_disk_lsn: The red log flushed-to-disk LSN. Added in MySQL

8.0.30.

• Innodb_redo_log_logical_size: The redo log logical size. Added in MySQL 8.0.30.

• Innodb_redo_log_physical_size: The redo log physical size. Added in MySQL 8.0.30.

• Innodb_redo_log_read_only: Whether the redo log is read-only. Added in MySQL 8.0.30.

• Innodb_redo_log_resize_status: The redo log resize status. Added in MySQL 8.0.30.

• Innodb_redo_log_uuid: The redo log UUID. Added in MySQL 8.0.30.

64

Options and Variables Introduced in MySQL 8.0

• Innodb_system_rows_deleted: Number of rows deleted from system schema tables. Added in

MySQL 8.0.19.

• Innodb_system_rows_inserted: Number of rows inserted into system schema tables. Added in

MySQL 8.0.19.

• Innodb_system_rows_read: Number of rows read from system schema tables. Added in MySQL

8.0.19.

• Innodb_system_rows_updated: Number of rows updated in system schema tables. Added in

MySQL 8.0.19.

• Innodb_undo_tablespaces_active: Number of active undo tablespaces. Added in MySQL

8.0.14.

• Innodb_undo_tablespaces_explicit: Number of user-created undo tablespaces. Added in

MySQL 8.0.14.

• Innodb_undo_tablespaces_implicit: Number of undo tablespaces created by InnoDB. Added

in MySQL 8.0.14.

• Innodb_undo_tablespaces_total: Total number of undo tablespaces. Added in MySQL 8.0.14.

• Mysqlx_bytes_received_compressed_payload: Number of bytes received as compressed

message payloads, measured before decompression. Added in MySQL 8.0.19.

• Mysqlx_bytes_received_uncompressed_frame: Number of bytes received as compressed

message payloads, measured after decompression. Added in MySQL 8.0.19.

• Mysqlx_bytes_sent_compressed_payload: Number of bytes sent as compressed message

payloads, measured after compression. Added in MySQL 8.0.19.

• Mysqlx_bytes_sent_uncompressed_frame: Number of bytes sent as compressed message

payloads, measured before compression. Added in MySQL 8.0.19.

• Mysqlx_compression_algorithm: Compression algorithm in use for X Protocol connection for

this session. Added in MySQL 8.0.20.

• Mysqlx_compression_level: Compression level in use for X Protocol connection for this

session. Added in MySQL 8.0.20.

• Replica_open_temp_tables: Number of temporary tables that replication SQL thread currently

has open. Added in MySQL 8.0.26.

• Replica_rows_last_search_algorithm_used: Search algorithm most recently used by this

replica to locate rows for row-based replication (index, table, or hash scan). Added in MySQL 8.0.26.

• Resource_group_supported: Whether server supports the resource group feature. Added in

MySQL 8.0.31.

• Rpl_semi_sync_replica_status: Whether semisynchronous replication is operational on

replica. Added in MySQL 8.0.26.

• Rpl_semi_sync_source_clients: Number of semisynchronous replicas. Added in MySQL

8.0.26.

• Rpl_semi_sync_source_net_avg_wait_time: Average time source has waited for replies from

replica. Added in MySQL 8.0.26.

• Rpl_semi_sync_source_net_wait_time: Total time source has waited for replies from replica.

Added in MySQL 8.0.26.

• Rpl_semi_sync_source_net_waits: Total number of times source waited for replies from

replica. Added in MySQL 8.0.26.

65

Options and Variables Introduced in MySQL 8.0

• Rpl_semi_sync_source_no_times: Number of times source turned off semisynchronous

replication. Added in MySQL 8.0.26.

• Rpl_semi_sync_source_no_tx: Number of commits not acknowledged successfully. Added in

MySQL 8.0.26.

• Rpl_semi_sync_source_status: Whether semisynchronous replication is operational on source.

Added in MySQL 8.0.26.

• Rpl_semi_sync_source_timefunc_failures: Number of times source failed when calling time

functions. Added in MySQL 8.0.26.

• Rpl_semi_sync_source_tx_avg_wait_time: Average time source waited for each transaction.

Added in MySQL 8.0.26.

• Rpl_semi_sync_source_tx_wait_time: Total time source waited for transactions. Added in

MySQL 8.0.26.

• Rpl_semi_sync_source_tx_waits: Total number of times source waited for transactions. Added

in MySQL 8.0.26.

• Rpl_semi_sync_source_wait_pos_backtraverse: Total number of times source has waited
for event with binary coordinates lower than events waited for previously. Added in MySQL 8.0.26.

• Rpl_semi_sync_source_wait_sessions: Number of sessions currently waiting for replica

replies. Added in MySQL 8.0.26.

• Rpl_semi_sync_source_yes_tx: Number of commits acknowledged successfully. Added in

MySQL 8.0.26.

• Secondary_engine_execution_count: Number of queries offloaded to a secondary engine.

Added in MySQL 8.0.13.

• Ssl_session_cache_timeout: Current SSL session timeout value in cache. Added in MySQL

8.0.29.

• Telemetry_traces_supported: Whether server telemetry traces is supported. Added in MySQL

8.0.33.

• Tls_library_version: Runtime version of OpenSSL library in use. Added in MySQL 8.0.30.

• activate_all_roles_on_login: Whether to activate all user roles at connect time. Added in

MySQL 8.0.2.

• admin-ssl: Enable connection encryption. Added in MySQL 8.0.21.

• admin_address: IP address to bind to for connections on administrative interface. Added in MySQL

8.0.14.

• admin_port: TCP/IP number to use for connections on administrative interface. Added in MySQL

8.0.14.

• admin_ssl_ca: File that contains list of trusted SSL Certificate Authorities. Added in MySQL 8.0.21.

• admin_ssl_capath: Directory that contains trusted SSL Certificate Authority certificate files. Added

in MySQL 8.0.21.

• admin_ssl_cert: File that contains X.509 certificate. Added in MySQL 8.0.21.

• admin_ssl_cipher: Permissible ciphers for connection encryption. Added in MySQL 8.0.21.

• admin_ssl_crl: File that contains certificate revocation lists. Added in MySQL 8.0.21.

• admin_ssl_crlpath: Directory that contains certificate revocation list files. Added in MySQL

8.0.21.

66

Options and Variables Introduced in MySQL 8.0

• admin_ssl_key: File that contains X.509 key. Added in MySQL 8.0.21.

• admin_tls_ciphersuites: Permissible TLSv1.3 ciphersuites for encrypted connections. Added

in MySQL 8.0.21.

• admin_tls_version: Permissible TLS protocols for encrypted connections. Added in MySQL

8.0.21.

• audit-log: Whether to activate audit log plugin. Added in MySQL 8.0.11.

• audit_log_buffer_size: Size of audit log buffer. Added in MySQL 8.0.11.

• audit_log_compression: Audit log file compression method. Added in MySQL 8.0.11.

• audit_log_connection_policy: Audit logging policy for connection-related events. Added in

MySQL 8.0.11.

• audit_log_current_session: Whether to audit current session. Added in MySQL 8.0.11.

• audit_log_database: Schema where audit tables are stored. Added in MySQL 8.0.33.

• audit_log_disable: Whether to disable the audit log. Added in MySQL 8.0.28.

• audit_log_encryption: Audit log file encryption method. Added in MySQL 8.0.11.

• audit_log_exclude_accounts: Accounts not to audit. Added in MySQL 8.0.11.

• audit_log_file: Name of audit log file. Added in MySQL 8.0.11.

• audit_log_filter_id: ID of current audit log filter. Added in MySQL 8.0.11.

• audit_log_flush: Close and reopen audit log file. Added in MySQL 8.0.11.

• audit_log_flush_interval_seconds: Whether to perform a recurring flush of the memory

cache. Added in MySQL 8.0.34.

• audit_log_format: Audit log file format. Added in MySQL 8.0.11.

• audit_log_format_unix_timestamp: Whether to include Unix timestamp in JSON-format audit

log. Added in MySQL 8.0.26.

• audit_log_include_accounts: Accounts to audit. Added in MySQL 8.0.11.

• audit_log_max_size: Limit on combined size of JSON audit log files. Added in MySQL 8.0.26.

• audit_log_password_history_keep_days: Number of days to retain archived audit log

encryption passwords. Added in MySQL 8.0.17.

• audit_log_policy: Audit logging policy. Added in MySQL 8.0.11.

• audit_log_prune_seconds: The number of seconds after which audit log files become subject to

pruning. Added in MySQL 8.0.24.

• audit_log_read_buffer_size: Audit log file read buffer size. Added in MySQL 8.0.11.

• audit_log_rotate_on_size: Close and reopen audit log file at this size. Added in MySQL

8.0.11.

• audit_log_statement_policy: Audit logging policy for statement-related events. Added in

MySQL 8.0.11.

• audit_log_strategy: Audit logging strategy. Added in MySQL 8.0.11.

• authentication_fido_rp_id: Relying party ID for FIDO multifactor authentication. Added in

MySQL 8.0.27.

67

Options and Variables Introduced in MySQL 8.0

• authentication_kerberos_service_key_tab: File containing Kerberos service keys to

authenticate TGS ticket. Added in MySQL 8.0.26.

• authentication_kerberos_service_principal: Kerberos service principal name. Added in

MySQL 8.0.26.

• authentication_ldap_sasl_auth_method_name: Authentication method name. Added in

MySQL 8.0.11.

• authentication_ldap_sasl_bind_base_dn: LDAP server base distinguished name. Added in

MySQL 8.0.11.

• authentication_ldap_sasl_bind_root_dn: LDAP server root distinguished name. Added in

MySQL 8.0.11.

• authentication_ldap_sasl_bind_root_pwd: LDAP server root bind password. Added in

MySQL 8.0.11.

• authentication_ldap_sasl_ca_path: LDAP server certificate authority file name. Added in

MySQL 8.0.11.

• authentication_ldap_sasl_group_search_attr: LDAP server group search attribute.

Added in MySQL 8.0.11.

• authentication_ldap_sasl_group_search_filter: LDAP custom group search filter.

Added in MySQL 8.0.11.

• authentication_ldap_sasl_init_pool_size: LDAP server initial connection pool size.

Added in MySQL 8.0.11.

• authentication_ldap_sasl_log_status: LDAP server log level. Added in MySQL 8.0.11.

• authentication_ldap_sasl_max_pool_size: LDAP server maximum connection pool size.

Added in MySQL 8.0.11.

• authentication_ldap_sasl_referral: Whether to enable LDAP search referral. Added in

MySQL 8.0.20.

• authentication_ldap_sasl_server_host: LDAP server host name or IP address. Added in

MySQL 8.0.11.

• authentication_ldap_sasl_server_port: LDAP server port number. Added in MySQL

8.0.11.

• authentication_ldap_sasl_tls: Whether to use encrypted connections to LDAP server.

Added in MySQL 8.0.11.

• authentication_ldap_sasl_user_search_attr: LDAP server user search attribute. Added in

MySQL 8.0.11.

• authentication_ldap_simple_auth_method_name: Authentication method name. Added in

MySQL 8.0.11.

• authentication_ldap_simple_bind_base_dn: LDAP server base distinguished name. Added

in MySQL 8.0.11.

• authentication_ldap_simple_bind_root_dn: LDAP server root distinguished name. Added

in MySQL 8.0.11.

• authentication_ldap_simple_bind_root_pwd: LDAP server root bind password. Added in

MySQL 8.0.11.

• authentication_ldap_simple_ca_path: LDAP server certificate authority file name. Added in

MySQL 8.0.11.

68

Options and Variables Introduced in MySQL 8.0

• authentication_ldap_simple_group_search_attr: LDAP server group search attribute.

Added in MySQL 8.0.11.

• authentication_ldap_simple_group_search_filter: LDAP custom group search filter.

Added in MySQL 8.0.11.

• authentication_ldap_simple_init_pool_size: LDAP server initial connection pool size.

Added in MySQL 8.0.11.

• authentication_ldap_simple_log_status: LDAP server log level. Added in MySQL 8.0.11.

• authentication_ldap_simple_max_pool_size: LDAP server maximum connection pool size.

Added in MySQL 8.0.11.

• authentication_ldap_simple_referral: Whether to enable LDAP search referral. Added in

MySQL 8.0.20.

• authentication_ldap_simple_server_host: LDAP server host name or IP address. Added in

MySQL 8.0.11.

• authentication_ldap_simple_server_port: LDAP server port number. Added in MySQL

8.0.11.

• authentication_ldap_simple_tls: Whether to use encrypted connections to LDAP server.

Added in MySQL 8.0.11.

• authentication_ldap_simple_user_search_attr: LDAP server user search attribute.

Added in MySQL 8.0.11.

• authentication_policy: Plugins for multifactor authentication; see documentation for syntax.

Added in MySQL 8.0.27.

• authentication_windows_log_level: Windows authentication plugin logging level. Added in

MySQL 8.0.11.

• authentication_windows_use_principal_name: Whether to use Windows authentication

plugin principal name. Added in MySQL 8.0.11.

• binlog_encryption: Enable encryption for binary log files and relay log files on this server. Added

in MySQL 8.0.14.

• binlog_expire_logs_auto_purge: Controls automatic purging of binary log files; can be

overridden when enabled, by setting both binlog_expire_logs_seconds and expire_logs_days to 0.
Added in MySQL 8.0.29.

• binlog_expire_logs_seconds: Purge binary logs after this many seconds. Added in MySQL

8.0.1.

• binlog_rotate_encryption_master_key_at_startup: Rotate binary log master key at

server startup. Added in MySQL 8.0.14.

• binlog_row_metadata: Whether to record all or only minimal table related metadata to binary log

when using row-based logging. Added in MySQL 8.0.1.

• binlog_row_value_options: Enables binary logging of partial JSON updates for row-based

replication. Added in MySQL 8.0.3.

• binlog_transaction_compression: Enable compression for transaction payloads in binary log

files. Added in MySQL 8.0.20.

• binlog_transaction_compression_level_zstd: Compression level for transaction payloads

in binary log files. Added in MySQL 8.0.20.

69

Options and Variables Introduced in MySQL 8.0

• binlog_transaction_dependency_history_size: Number of row hashes kept for looking up

transaction that last updated some row. Added in MySQL 8.0.1.

• binlog_transaction_dependency_tracking: Source of dependency information (commit

timestamps or transaction write sets) from which to assess which transactions can be executed in
parallel by replica's multithreaded applier. Added in MySQL 8.0.1.

• build_id: A unique build ID generated at compile time (Linux only). Added in MySQL 8.0.31.

• caching_sha2_password_auto_generate_rsa_keys: Whether to autogenerate RSA key-pair

files. Added in MySQL 8.0.4.

• caching_sha2_password_digest_rounds: Number of hash rounds for
caching_sha2_password authentication plugin. Added in MySQL 8.0.24.

• caching_sha2_password_private_key_path: SHA2 authentication plugin private key path

name. Added in MySQL 8.0.3.

• caching_sha2_password_public_key_path: SHA2 authentication plugin public key path

name. Added in MySQL 8.0.3.

• check-table-functions: How to proceed when scanning data dictionary for functions used in
table constraints and other expressions, and such a function causes an error. Use WARN to log
warnings; ABORT (default) also logs warnings, and halts any upgrade in progress. Added in MySQL
8.0.42.

• clone_autotune_concurrency: Enables dynamic spawning of threads for remote cloning

operations. Added in MySQL 8.0.17.

• clone_block_ddl: Enables an exclusive backup lock during clone operations. Added in MySQL

8.0.27.

• clone_buffer_size: Defines size of intermediate buffer on donor MySQL server instance. Added

in MySQL 8.0.17.

• clone_ddl_timeout: Number of seconds cloning operation waits for backup lock. Added in

MySQL 8.0.17.

• clone_delay_after_data_drop: The time delay in seconds before the clone process starts.

Added in MySQL 8.0.29.

• clone_donor_timeout_after_network_failure: The time allowed to restart a cloning

operation after a network failure. Added in MySQL 8.0.24.

• clone_enable_compression: Enables compression of data at network layer during cloning.

Added in MySQL 8.0.17.

• clone_max_concurrency: Maximum number of concurrent threads used to perform cloning

operation. Added in MySQL 8.0.17.

• clone_max_data_bandwidth: Maximum data transfer rate in MiB per second for remote cloning

operation. Added in MySQL 8.0.17.

• clone_max_network_bandwidth: Maximum network transfer rate in MiB per second for remote

cloning operation. Added in MySQL 8.0.17.

• clone_ssl_ca: Specifies path to certificate authority (CA) file. Added in MySQL 8.0.14.

• clone_ssl_cert: Specifies path to public key certificate file. Added in MySQL 8.0.14.

• clone_ssl_key: Specifies path to private key file. Added in MySQL 8.0.14.

• clone_valid_donor_list: Defines donor host addresses for remote cloning operations. Added

in MySQL 8.0.17.

70

Options and Variables Introduced in MySQL 8.0

• component_scheduler.enabled: Whether the scheduler is actively executing tasks. Added in

MySQL 8.0.34.

• connection_control_failed_connections_threshold: Consecutive failed connection

attempts before delays occur. Added in MySQL 8.0.1.

• connection_control_max_connection_delay: Maximum delay (milliseconds) for server

response to failed connection attempts. Added in MySQL 8.0.1.

• connection_control_min_connection_delay: Minimum delay (milliseconds) for server

response to failed connection attempts. Added in MySQL 8.0.1.

• connection_memory_chunk_size: Update Global_connection_memory only when user memory

usage changes by this amount or more; 0 disables updating. Added in MySQL 8.0.28.

• connection_memory_limit: Maximum amount of memory that can be consumed by any one

user connection before all queries by this user are rejected. Does not apply to system users such as
MySQL root. Added in MySQL 8.0.28.

• create_admin_listener_thread: Whether to use dedicated listening thread for connections on

administrative interface. Added in MySQL 8.0.14.

• cte_max_recursion_depth: Common table expression maximum recursion depth. Added in

MySQL 8.0.3.

• ddl-rewriter: Whether to activate ddl_rewriter plugin. Added in MySQL 8.0.16.

• default_collation_for_utf8mb4: Default collation for utf8mb4 character set; for internal use

by MySQL Replication only. Added in MySQL 8.0.11.

• default_table_encryption: Default schema and tablespace encryption setting. Added in

MySQL 8.0.16.

• dragnet.Status: Result of most recent assignment to dragnet.log_error_filter_rules. Added in

MySQL 8.0.12.

• dragnet.log_error_filter_rules: Filter rules for error logging. Added in MySQL 8.0.4.

• early-plugin-load: Specify plugins to load before loading mandatory built-in plugins and before

storage engine initialization. Added in MySQL 8.0.0.

• enterprise_encryption.maximum_rsa_key_size: Maximum size of RSA keys generated by

MySQL Enterprise Encryption. Added in MySQL 8.0.30.

• enterprise_encryption.rsa_support_legacy_padding: Decrypt and verify legacy MySQL

Enterprise Encryption content. Added in MySQL 8.0.30.

• explain_format: Determines default output format used by EXPLAIN statements. Added in

MySQL 8.0.32.

• generated_random_password_length: Maximum length of generated passwords. Added in

MySQL 8.0.18.

• global_connection_memory_limit: Maximum total amount of memory that can be consumed
by all user connections. When exceeded by Global_connection_memory, all queries from regular
users are rejected. Does not apply to system users such as MySQL root. Added in MySQL 8.0.28.

• global_connection_memory_tracking: Whether or not to calculate global connection memory

usage (as shown by Global_connection_memory); default is disabled. Added in MySQL 8.0.28.

• group_replication_advertise_recovery_endpoints: Connections offered for distributed

recovery. Added in MySQL 8.0.21.

71

Options and Variables Introduced in MySQL 8.0

• group_replication_autorejoin_tries: Number of tries that member makes to rejoin group

automatically. Added in MySQL 8.0.16.

• group_replication_clone_threshold: Transaction number gap between donor and recipient

above which remote cloning operation is used for state transfer. Added in MySQL 8.0.17.

• group_replication_communication_debug_options: Level of debugging messages for

Group Replication components. Added in MySQL 8.0.3.

• group_replication_communication_max_message_size: Maximum message size for Group

Replication communications, larger messages are fragmented. Added in MySQL 8.0.16.

• group_replication_communication_stack: Specifies which communication stack (XCom or

MySQL) should be used to establish group communication connections between members. Added in
MySQL 8.0.27.

• group_replication_consistency: Type of transaction consistency guarantee which group

provides. Added in MySQL 8.0.14.

• group_replication_exit_state_action: How instance behaves when it leaves group

involuntarily. Added in MySQL 8.0.12.

• group_replication_flow_control_hold_percent: Percentage of group quota to remain

unused. Added in MySQL 8.0.2.

• group_replication_flow_control_max_quota: Maximum flow control quota for group.

Added in MySQL 8.0.2.

• group_replication_flow_control_member_quota_percent: Percentage of quota which
member should assume is available for itself when calculating quotas. Added in MySQL 8.0.2.

• group_replication_flow_control_min_quota: Lowest flow control quota which can be

assigned per member. Added in MySQL 8.0.2.

• group_replication_flow_control_min_recovery_quota: Lowest quota which can be
assigned per member because another group member is recovering. Added in MySQL 8.0.2.

• group_replication_flow_control_period: Defines how many seconds to wait between flow

control iterations. Added in MySQL 8.0.2.

• group_replication_flow_control_release_percent: How group quota should be released

when flow control no longer needs to throttle writer members. Added in MySQL 8.0.2.

• group_replication_ip_allowlist: List of hosts permitted to connect to group (MySQL 8.0.22

and later). Added in MySQL 8.0.22.

• group_replication_member_expel_timeout: Time between suspected failure of group

member and expelling it from group, causing group membership reconfiguration. Added in MySQL
8.0.13.

• group_replication_member_weight: Chance of this member being elected as primary. Added

in MySQL 8.0.2.

• group_replication_message_cache_size: Maximum memory for group communication

engine message cache (XCom). Added in MySQL 8.0.16.

• group_replication_paxos_single_leader: Use a single consensus leader in single-primary

mode. Added in MySQL 8.0.27.

• group_replication_recovery_compression_algorithms: Permitted compression

algorithms for outgoing recovery connections. Added in MySQL 8.0.18.

• group_replication_recovery_get_public_key: Whether to accept preference about

fetching public key from donor. Added in MySQL 8.0.4.

72

Options and Variables Introduced in MySQL 8.0

• group_replication_recovery_public_key_path: To accept public key information. Added in

MySQL 8.0.4.

• group_replication_recovery_tls_ciphersuites: Permitted cipher suites when TLSv1.3 is
used for connection encryption with this instance as client (joining member). Added in MySQL 8.0.19.

• group_replication_recovery_tls_version: Permitted TLS protocols for connection

encryption as client (joining member). Added in MySQL 8.0.19.

• group_replication_recovery_zstd_compression_level: Compression level for recovery

connections that use zstd compression. Added in MySQL 8.0.18.

• group_replication_tls_source: Source of TLS material for Group Replication. Added in

MySQL 8.0.21.

• group_replication_unreachable_majority_timeout: How long to wait for network

partitions that result in minority to leave group. Added in MySQL 8.0.2.

• group_replication_view_change_uuid: UUID for view change event GTIDs. Added in MySQL

8.0.26.

• histogram_generation_max_mem_size: Maximum memory for creating histogram statistics.

Added in MySQL 8.0.2.

• immediate_server_version: MySQL Server release number of server which is immediate

replication source. Added in MySQL 8.0.14.

• information_schema_stats_expiry: Expiration setting for cached table statistics. Added in

MySQL 8.0.3.

• init_replica: Statements that are executed when replica connects to source. Added in MySQL

8.0.26.

• innodb-dedicated-server: Enables automatic configuration of buffer pool size, log file size, and

flush method. Added in MySQL 8.0.3.

• innodb_buffer_pool_debug: Permits multiple buffer pool instances when buffer pool is less than

1GB in size. Added in MySQL 8.0.0.

• innodb_buffer_pool_in_core_file: Controls writing of buffer pool pages to core files, defaults

to OFF (as of 8.4) on systems that support MADV_DONTDUMP. Added in MySQL 8.0.14.

• innodb_checkpoint_disabled: Disables checkpoints so that deliberate server exit always

initiates recovery. Added in MySQL 8.0.2.

• innodb_ddl_buffer_size: The maximum buffer size for DDL operations. Added in MySQL

8.0.27.

• innodb_ddl_log_crash_reset_debug: Debug option that resets DDL log crash injection

counters. Added in MySQL 8.0.3.

• innodb_ddl_threads: The maximum number of parallel threads for index creation. Added in

MySQL 8.0.27.

• innodb_deadlock_detect: Enables or disables deadlock detection. Added in MySQL 8.0.0.

• innodb_directories: Defines directories to scan at startup for tablespace data files. Added in

MySQL 8.0.4.

• innodb_doublewrite_batch_size: This functionality was replaced by

innodb_doublewrite_pages. Added in MySQL 8.0.20.

• innodb_doublewrite_dir: Doublewrite buffer file directory. Added in MySQL 8.0.20.

73

Options and Variables Introduced in MySQL 8.0

• innodb_doublewrite_files: Number of doublewrite files. Added in MySQL 8.0.20.

• innodb_doublewrite_pages: Number of doublewrite pages per thread. Added in MySQL 8.0.20.

• innodb_extend_and_initialize: Controls how new tablespace pages are allocated on Linux.

Added in MySQL 8.0.22.

• innodb_fsync_threshold: Controls how often InnoDB calls fsync when creating new file. Added

in MySQL 8.0.13.

• innodb_idle_flush_pct: Limits I/0 operations when InnoDB is idle. Added in MySQL 8.0.18.

• innodb_log_checkpoint_fuzzy_now: Debug option that forces InnoDB to write fuzzy

checkpoint. Added in MySQL 8.0.13.

• innodb_log_spin_cpu_abs_lwm: Minimum amount of CPU usage below which user threads no

longer spin while waiting for flushed redo. Added in MySQL 8.0.11.

• innodb_log_spin_cpu_pct_hwm: Maximum amount of CPU usage above which user threads no

longer spin while waiting for flushed redo. Added in MySQL 8.0.11.

• innodb_log_wait_for_flush_spin_hwm: Maximum average log flush time beyond which user

threads no longer spin while waiting for flushed redo. Added in MySQL 8.0.11.

• innodb_log_writer_threads: Enables dedicated log writer threads for writing and flushing redo

logs. Added in MySQL 8.0.22.

• innodb_parallel_read_threads: Number of threads for parallel index reads. Added in MySQL

8.0.14.

• innodb_print_ddl_logs: Whether or not to print DDL logs to error log. Added in MySQL 8.0.3.

• innodb_redo_log_archive_dirs: Labeled redo log archive directories. Added in MySQL 8.0.17.

• innodb_redo_log_capacity: The size limit for redo log files. Added in MySQL 8.0.30.

• innodb_redo_log_encrypt: Controls encryption of redo log data for encrypted tablespaces.

Added in MySQL 8.0.1.

• innodb_scan_directories: Defines directories to scan for tablespace files during InnoDB

recovery. Added in MySQL 8.0.2.

• innodb_segment_reserve_factor: The percentage of tablespace file segment pages reserved

as empty pages. Added in MySQL 8.0.26.

• innodb_spin_wait_pause_multiplier: Multiplier value used to determine number of PAUSE

instructions in spin-wait loops. Added in MySQL 8.0.16.

• innodb_stats_include_delete_marked: Include delete-marked records when calculating

persistent InnoDB statistics. Added in MySQL 8.0.1.

• innodb_temp_tablespaces_dir: Session temporary tablespaces path. Added in MySQL 8.0.13.

• innodb_tmpdir: Directory location for temporary table files created during online ALTER TABLE

operations. Added in MySQL 8.0.0.

• innodb_undo_log_encrypt: Controls encryption of undo log data for encrypted tablespaces.

Added in MySQL 8.0.1.

• innodb_use_fdatasync: Whether InnoDB uses fdatasync() instead of fsync() when flushing data

to the operating system. Added in MySQL 8.0.26.

• innodb_validate_tablespace_paths: Enables tablespace path validation at startup. Added in

MySQL 8.0.21.

74

Options and Variables Introduced in MySQL 8.0

• internal_tmp_mem_storage_engine: Storage engine to use for internal in-memory temporary

tables. Added in MySQL 8.0.2.

• keyring-migration-destination: Key migration destination keyring plugin. Added in MySQL

8.0.4.

• keyring-migration-host: Host name for connecting to running server for key migration. Added

in MySQL 8.0.4.

• keyring-migration-password: Password for connecting to running server for key migration.

Added in MySQL 8.0.4.

• keyring-migration-port: TCP/IP port number for connecting to running server for key

migration. Added in MySQL 8.0.4.

• keyring-migration-socket: Unix socket file or Windows named pipe for connecting to running

server for key migration. Added in MySQL 8.0.4.

• keyring-migration-source: Key migration source keyring plugin. Added in MySQL 8.0.4.

• keyring-migration-to-component: Keyring migration is from plugin to component. Added in

MySQL 8.0.24.

• keyring-migration-user: User name for connecting to running server for key migration. Added

in MySQL 8.0.4.

• keyring_aws_cmk_id: AWS keyring plugin customer master key ID value. Added in MySQL

8.0.11.

• keyring_aws_conf_file: AWS keyring plugin configuration file location. Added in MySQL 8.0.11.

• keyring_aws_data_file: AWS keyring plugin storage file location. Added in MySQL 8.0.11.

• keyring_aws_region: AWS keyring plugin region. Added in MySQL 8.0.11.

• keyring_encrypted_file_data: keyring_encrypted_file plugin data file. Added in MySQL

8.0.11.

• keyring_encrypted_file_password: keyring_encrypted_file plugin password. Added in

MySQL 8.0.11.

• keyring_hashicorp_auth_path: HashiCorp Vault AppRole authentication path. Added in

MySQL 8.0.18.

• keyring_hashicorp_ca_path: Path to keyring_hashicorp CA file. Added in MySQL 8.0.18.

• keyring_hashicorp_caching: Whether to enable keyring_hashicorp caching. Added in MySQL

8.0.18.

• keyring_hashicorp_commit_auth_path: keyring_hashicorp_auth_path value in use. Added in

MySQL 8.0.18.

• keyring_hashicorp_commit_ca_path: keyring_hashicorp_ca_path value in use. Added in

MySQL 8.0.18.

• keyring_hashicorp_commit_caching: keyring_hashicorp_caching value in use. Added in

MySQL 8.0.18.

• keyring_hashicorp_commit_role_id: keyring_hashicorp_role_id value in use. Added in

MySQL 8.0.18.

• keyring_hashicorp_commit_server_url: keyring_hashicorp_server_url value in use. Added

in MySQL 8.0.18.

75

Options and Variables Introduced in MySQL 8.0

• keyring_hashicorp_commit_store_path: keyring_hashicorp_store_path value in use. Added

in MySQL 8.0.18.

• keyring_hashicorp_role_id: HashiCorp Vault AppRole authentication role ID. Added in

MySQL 8.0.18.

• keyring_hashicorp_secret_id: HashiCorp Vault AppRole authentication secret ID. Added in

MySQL 8.0.18.

• keyring_hashicorp_server_url: HashiCorp Vault server URL. Added in MySQL 8.0.18.

• keyring_hashicorp_store_path: HashiCorp Vault store path. Added in MySQL 8.0.18.

• keyring_oci_ca_certificate: CA certificate file for peer authentication. Added in MySQL

8.0.22.

• keyring_oci_compartment: OCI compartment OCID. Added in MySQL 8.0.22.

• keyring_oci_encryption_endpoint: OCI encryption server endpoint. Added in MySQL 8.0.22.

• keyring_oci_key_file: OCI RSA private key file. Added in MySQL 8.0.22.

• keyring_oci_key_fingerprint: OCI RSA private key file fingerprint. Added in MySQL 8.0.22.

• keyring_oci_management_endpoint: OCI management server endpoint. Added in MySQL

8.0.22.

• keyring_oci_master_key: OCI master key OCID. Added in MySQL 8.0.22.

• keyring_oci_secrets_endpoint: OCI secrets server endpoint. Added in MySQL 8.0.22.

• keyring_oci_tenancy: OCI tenancy OCID. Added in MySQL 8.0.22.

• keyring_oci_user: OCI user OCID. Added in MySQL 8.0.22.

• keyring_oci_vaults_endpoint: OCI vaults server endpoint. Added in MySQL 8.0.22.

• keyring_oci_virtual_vault: OCI vault OCID. Added in MySQL 8.0.22.

• keyring_okv_conf_dir: Oracle Key Vault keyring plugin configuration directory. Added in

MySQL 8.0.11.

• keyring_operations: Whether keyring operations are enabled. Added in MySQL 8.0.4.

• lock_order: Whether to enable LOCK_ORDER tool at runtime. Added in MySQL 8.0.17.

• lock_order_debug_loop: Whether to cause debug assert when LOCK_ORDER tool encounters

dependency flagged as loop. Added in MySQL 8.0.17.

• lock_order_debug_missing_arc: Whether to cause debug assert when LOCK_ORDER tool

encounters undeclared dependency. Added in MySQL 8.0.17.

• lock_order_debug_missing_key: Whether to cause debug assert when LOCK_ORDER tool
encounters object not properly instrumented with Performance Schema. Added in MySQL 8.0.17.

• lock_order_debug_missing_unlock: Whether to cause debug assert when LOCK_ORDER

tool encounters lock that is destroyed while still held. Added in MySQL 8.0.17.

• lock_order_dependencies: Path to lock_order_dependencies.txt file. Added in MySQL 8.0.17.

• lock_order_extra_dependencies: Path to second dependency file. Added in MySQL 8.0.17.

• lock_order_output_directory: Directory where LOCK_ORDER tool writes logs. Added in

MySQL 8.0.17.

76

Options and Variables Introduced in MySQL 8.0

• lock_order_print_txt: Whether to perform lock-order graph analysis and print textual report.

Added in MySQL 8.0.17.

• lock_order_trace_loop: Whether to print log file trace when LOCK_ORDER tool encounters

dependency flagged as loop. Added in MySQL 8.0.17.

• lock_order_trace_missing_arc: Whether to print log file trace when LOCK_ORDER tool

encounters undeclared dependency. Added in MySQL 8.0.17.

• lock_order_trace_missing_key: Whether to print log file trace when LOCK_ORDER tool

encounters object not properly instrumented with Performance Schema. Added in MySQL 8.0.17.

• lock_order_trace_missing_unlock: Whether to print log file trace when LOCK_ORDER tool

encounters lock that is destroyed while still held. Added in MySQL 8.0.17.

• log_error_filter_rules: Filter rules for error logging. Added in MySQL 8.0.2.

• log_error_services: Components to use for error logging. Added in MySQL 8.0.2.

• log_error_suppression_list: Warning/information error log messages to suppress. Added in

MySQL 8.0.13.

• log_replica_updates: Whether replica should log updates performed by its replication SQL

thread to its own binary log. Added in MySQL 8.0.26.

• log_slow_extra: Whether to write extra information to slow query log file. Added in MySQL

8.0.14.

• log_slow_replica_statements: Cause slow statements as executed by replica to be written to

slow query log. Added in MySQL 8.0.26.

• mandatory_roles: Automatically granted roles for all users. Added in MySQL 8.0.2.

• mysql_firewall_mode: Whether MySQL Enterprise Firewall plugin is operational. Added in

MySQL 8.0.11.

• mysql_firewall_trace: Whether to enable MySQL Enterprise Firewall plugin trace. Added in

MySQL 8.0.11.

• mysqlx: Whether X Plugin is initialized. Added in MySQL 8.0.11.

• mysqlx_compression_algorithms: Compression algorithms permitted for X Protocol

connections. Added in MySQL 8.0.19.

• mysqlx_deflate_default_compression_level: Default compression level for Deflate

algorithm on X Protocol connections. Added in MySQL 8.0.20.

• mysqlx_deflate_max_client_compression_level: Maximum permitted compression level

for Deflate algorithm on X Protocol connections. Added in MySQL 8.0.20.

• mysqlx_interactive_timeout: Number of seconds to wait for interactive clients to time out.

Added in MySQL 8.0.4.

• mysqlx_lz4_default_compression_level: Default compression level for LZ4 algorithm on X

Protocol connections. Added in MySQL 8.0.20.

• mysqlx_lz4_max_client_compression_level: Maximum permitted compression level for LZ4

algorithm on X Protocol connections. Added in MySQL 8.0.20.

• mysqlx_read_timeout: Number of seconds to wait for blocking read operations to complete.

Added in MySQL 8.0.4.

• mysqlx_wait_timeout: Number of seconds to wait for activity from connection. Added in MySQL

8.0.4.

77

Options and Variables Introduced in MySQL 8.0

• mysqlx_write_timeout: Number of seconds to wait for blocking write operations to complete.

Added in MySQL 8.0.4.

• mysqlx_zstd_default_compression_level: Default compression level for zstd algorithm on X

Protocol connections. Added in MySQL 8.0.20.

• mysqlx_zstd_max_client_compression_level: Maximum permitted compression level for

zstd algorithm on X Protocol connections. Added in MySQL 8.0.20.

• named_pipe_full_access_group: Name of Windows group granted full access to named pipe.

Added in MySQL 8.0.14.

• no-dd-upgrade: Prevent automatic upgrade of data dictionary tables at startup. Added in MySQL

8.0.4.

• no-monitor: Do not fork monitor process required for RESTART. Added in MySQL 8.0.12.

• original_commit_timestamp: Time when transaction was committed on original source. Added

in MySQL 8.0.1.

• original_server_version: MySQL Server release number of server on which transaction was

originally committed. Added in MySQL 8.0.14.

• partial_revokes: Whether partial revocation is enabled. Added in MySQL 8.0.16.

• password_history: Number of password changes required before password reuse. Added in

MySQL 8.0.3.

• password_require_current: Whether password changes require current password verification.

Added in MySQL 8.0.13.

• password_reuse_interval: Number of days elapsed required before password reuse. Added in

MySQL 8.0.3.

• performance-schema-consumer-events-statements-cpu: Configure statement CPU-usage

consumer. Added in MySQL 8.0.28.

• performance_schema_max_digest_sample_age: Query resample age in seconds. Added in

MySQL 8.0.3.

• performance_schema_show_processlist: Select SHOW PROCESSLIST implementation.

Added in MySQL 8.0.22.

• persist_only_admin_x509_subject: SSL certificate X.509 Subject that enables persisting

persist-restricted system variables. Added in MySQL 8.0.14.

• persist_sensitive_variables_in_plaintext: Whether the server is permitted to store the

values of sensitive system variables in an unencrypted format. Added in MySQL 8.0.29.

• persisted_globals_load: Whether to load persisted configuration settings. Added in MySQL

8.0.0.

• print_identified_with_as_hex: For SHOW CREATE USER, print hash values containing

unprintable characters in hex. Added in MySQL 8.0.17.

• protocol_compression_algorithms: Permitted compression algorithms for incoming

connections. Added in MySQL 8.0.18.

• pseudo_replica_mode: For internal server use. Added in MySQL 8.0.26.

• regexp_stack_limit: Regular expression match stack size limit. Added in MySQL 8.0.4.

• regexp_time_limit: Regular expression match timeout. Added in MySQL 8.0.4.

78

Options and Variables Introduced in MySQL 8.0

• replica_checkpoint_group: Maximum number of transactions processed by multithreaded
replica before checkpoint operation is called to update progress status. Not supported by NDB
Cluster. Added in MySQL 8.0.26.

• replica_checkpoint_period: Update progress status of multithreaded replica and flush relay
log info to disk after this number of milliseconds. Not supported by NDB Cluster. Added in MySQL
8.0.26.

• replica_compressed_protocol: Use compression of source/replica protocol. Added in MySQL

8.0.26.

• replica_exec_mode: Allows for switching replication thread between IDEMPOTENT mode (key
and some other errors suppressed) and STRICT mode; STRICT mode is default, except for NDB
Cluster, where IDEMPOTENT is always used. Added in MySQL 8.0.26.

• replica_load_tmpdir: Location where replica should put its temporary files when replicating

LOAD DATA statements. Added in MySQL 8.0.26.

• replica_max_allowed_packet: Maximum size, in bytes, of packet that can be sent from
replication source server to replica; overrides max_allowed_packet. Added in MySQL 8.0.26.

• replica_net_timeout: Number of seconds to wait for more data from source/replica connection

before aborting read. Added in MySQL 8.0.26.

• replica_parallel_type: Tells replica to use timestamp information (LOGICAL_CLOCK) or

database partitioning (DATABASE) to parallelize transactions. Added in MySQL 8.0.26.

• replica_parallel_workers: Number of applier threads for executing replication transactions.

NDB Cluster: see documentation. Added in MySQL 8.0.26.

• replica_pending_jobs_size_max: Maximum size of replica worker queues holding events not

yet applied. Added in MySQL 8.0.26.

• replica_preserve_commit_order: Ensures that all commits by replica workers happen in same
order as on source to maintain consistency when using parallel applier threads. Added in MySQL
8.0.26.

• replica_skip_errors: Tells replication thread to continue replication when query returns error

from provided list. Added in MySQL 8.0.26.

• replica_sql_verify_checksum: Cause replica to examine checksums when reading from relay

log. Added in MySQL 8.0.26.

• replica_transaction_retries: Number of times replication SQL thread retries transaction in
case it failed with deadlock or elapsed lock wait timeout, before giving up and stopping. Added in
MySQL 8.0.26.

• replica_type_conversions: Controls type conversion mode on replica. Value is list of zero or
more elements from this list: ALL_LOSSY, ALL_NON_LOSSY. Set to empty string to disallow type
conversions between source and replica. Added in MySQL 8.0.26.

• replication_optimize_for_static_plugin_config: Shared locks for semisynchronous

replication. Added in MySQL 8.0.23.

• replication_sender_observe_commit_only: Limited callbacks for semisynchronous

replication. Added in MySQL 8.0.23.

• require_row_format: For internal server use. Added in MySQL 8.0.19.

• resultset_metadata: Whether server returns result set metadata. Added in MySQL 8.0.3.

• rewriter_enabled_for_threads_without_privilege_checks: If this is set to OFF,

rewrites are skipped for replication threads which execute with privilege checks disabled
(PRIVILEGE_CHECKS_USER is NULL). Added in MySQL 8.0.31.

79

Options and Variables Introduced in MySQL 8.0

• rpl_read_size: Set minimum amount of data in bytes which is read from binary log files and relay

log files. Added in MySQL 8.0.11.

• rpl_semi_sync_replica_enabled: Whether semisynchronous replication is enabled on replica.

Added in MySQL 8.0.26.

• rpl_semi_sync_replica_trace_level: Semisynchronous replication debug trace level on

replica. Added in MySQL 8.0.26.

• rpl_semi_sync_source_enabled: Whether semisynchronous replication is enabled on source.

Added in MySQL 8.0.26.

• rpl_semi_sync_source_timeout: Number of milliseconds to wait for replica acknowledgment.

Added in MySQL 8.0.26.

• rpl_semi_sync_source_trace_level: Semisynchronous replication debug trace level on

source. Added in MySQL 8.0.26.

• rpl_semi_sync_source_wait_for_replica_count: Number of replica acknowledgments

source must receive per transaction before proceeding. Added in MySQL 8.0.26.

• rpl_semi_sync_source_wait_no_replica: Whether source waits for timeout even with no

replicas. Added in MySQL 8.0.26.

• rpl_semi_sync_source_wait_point: Wait point for replica transaction receipt

acknowledgment. Added in MySQL 8.0.26.

• rpl_stop_replica_timeout: Number of seconds that STOP REPLICA waits before timing out.

Added in MySQL 8.0.26.

• schema_definition_cache: Number of schema definition objects that can be kept in dictionary

object cache. Added in MySQL 8.0.0.

• secondary_engine_cost_threshold: Optimizer cost threshold for query offload to a secondary

engine. Added in MySQL 8.0.16.

• select_into_buffer_size: Size of buffer used for OUTFILE or DUMPFILE export file; overrides

read_buffer_size. Added in MySQL 8.0.22.

• select_into_disk_sync: Synchronize data with storage device after flushing buffer for OUTFILE

or DUMPFILE export file; OFF disables synchronization and is default value. Added in MySQL
8.0.22.

• select_into_disk_sync_delay: When select_into_sync_disk = ON, sets delay in milliseconds

after each synchronization of OUTFILE or DUMPFILE export file buffer, no effect otherwise. Added in
MySQL 8.0.22.

• show-replica-auth-info: Show user name and password in SHOW REPLICAS on this source.

Added in MySQL 8.0.26.

• show_create_table_skip_secondary_engine: Whether to exclude the SECONDARY

ENGINE clause from SHOW CREATE TABLE output. Added in MySQL 8.0.18.

• show_create_table_verbosity: Whether to display ROW_FORMAT in SHOW CREATE

TABLE even if it has default value. Added in MySQL 8.0.11.

• show_gipk_in_create_table_and_information_schema: Whether generated invisible

primary keys are displayed in SHOW statements and INFORMATION_SCHEMA tables. Added in
MySQL 8.0.30.

• skip-replica-start: If set, replication is not autostarted when replica server starts. Added in

MySQL 8.0.26.

80

Options and Variables Introduced in MySQL 8.0

• source_verify_checksum: Cause source to examine checksums when reading from binary log.

Added in MySQL 8.0.26.

• sql_generate_invisible_primary_key: Whether to generate invisible primary keys for any
InnoDB tables which were created on this server and which have no explicit PKs. Added in MySQL
8.0.30.

• sql_replica_skip_counter: Number of events from source that replica should skip. Not

compatible with GTID replication. Added in MySQL 8.0.26.

• sql_require_primary_key: Whether tables must have primary key. Added in MySQL 8.0.13.

• ssl_fips_mode: Whether to enable FIPS mode on server side. Added in MySQL 8.0.11.

• ssl_session_cache_mode: Whether to enable session ticket generation by server. Added in

MySQL 8.0.29.

• ssl_session_cache_timeout: SSL Session timeout value in seconds. Added in MySQL 8.0.29.

• sync_source_info: Synchronize source information after every #th event. Added in MySQL

8.0.26.

• syseventlog.facility: Facility for syslog messages. Added in MySQL 8.0.13.

• syseventlog.include_pid: Whether to include server PID in syslog messages. Added in

MySQL 8.0.13.

• syseventlog.tag: Tag for server identifier in syslog messages. Added in MySQL 8.0.13.

• table_encryption_privilege_check: Enables TABLE_ENCRYPTION_ADMIN privilege

check. Added in MySQL 8.0.16.

• tablespace_definition_cache: Number of tablespace definition objects that can be kept in

dictionary object cache. Added in MySQL 8.0.0.

• temptable_max_mmap: The maximum amount of memory the TempTable storage engine can

allocate from memory-mapped temporary files. Added in MySQL 8.0.23.

• temptable_max_ram: Defines maximum amount of memory that can occupied by TempTable

storage engine before data is stored on disk. Added in MySQL 8.0.2.

• temptable_use_mmap: Defines whether TempTable storage engine allocates memory-mapped

files when the temptable_max_ram threshold is reached. Added in MySQL 8.0.16.

• terminology_use_previous: Use terminology from before specified version where changes are

incompatible. Added in MySQL 8.0.26.

• thread_pool_algorithm: Thread pool algorithm. Added in MySQL 8.0.11.

• thread_pool_dedicated_listeners: Dedicates a listener thread in each thread group to listen

for network events. Added in MySQL 8.0.23.

• thread_pool_high_priority_connection: Whether current session is high priority. Added in

MySQL 8.0.11.

• thread_pool_max_active_query_threads: Maximum permissible number of active query

threads per group. Added in MySQL 8.0.19.

• thread_pool_max_transactions_limit: Maximum number of transactions permitted during

thread pool operation. Added in MySQL 8.0.23.

• thread_pool_max_unused_threads: Maximum permissible number of unused threads. Added in

MySQL 8.0.11.

81

Options and Variables Deprecated in MySQL 8.0

• thread_pool_prio_kickup_timer: How long before statement is moved to high-priority

execution. Added in MySQL 8.0.11.

• thread_pool_query_threads_per_group: Maximum number of query threads for a thread

group. Added in MySQL 8.0.31.

• thread_pool_size: Number of thread groups in thread pool. Added in MySQL 8.0.11.

• thread_pool_stall_limit: How long before statement is defined as stalled. Added in MySQL

8.0.11.

• thread_pool_transaction_delay: Delay period before thread pool executes a new transaction.

Added in MySQL 8.0.31.

• tls_ciphersuites: Permissible TLSv1.3 ciphersuites for encrypted connections. Added in

MySQL 8.0.16.

• upgrade: Control automatic upgrade at startup. Added in MySQL 8.0.16.

• use_secondary_engine: Whether to execute queries using a secondary engine. Added in MySQL

8.0.13.

• validate-config: Validate server configuration. Added in MySQL 8.0.16.

• validate_password.changed_characters_percentage: Minimum percentage of changed

characters required for new passwords. Added in MySQL 8.0.34.

• validate_password.check_user_name: Whether to check passwords against user name.

Added in MySQL 8.0.4.

• validate_password.dictionary_file: validate_password dictionary file. Added in MySQL

8.0.4.

• validate_password.dictionary_file_last_parsed: When dictionary file was last parsed.

Added in MySQL 8.0.4.

• validate_password.dictionary_file_words_count: Number of words in dictionary file.

Added in MySQL 8.0.4.

• validate_password.length: validate_password required password length. Added in MySQL

8.0.4.

• validate_password.mixed_case_count: validate_password required number of uppercase/

lowercase characters. Added in MySQL 8.0.4.

• validate_password.number_count: validate_password required number of digit characters.

Added in MySQL 8.0.4.

• validate_password.policy: validate_password password policy. Added in MySQL 8.0.4.

• validate_password.special_char_count: validate_password required number of special

characters. Added in MySQL 8.0.4.

• version_compile_zlib: Version of compiled-in zlib library. Added in MySQL 8.0.11.

• windowing_use_high_precision: Whether to compute window functions to high precision.

Added in MySQL 8.0.2.

Options and Variables Deprecated in MySQL 8.0

The following system variables, status variables, and options have been deprecated in MySQL 8.0.

• Compression: Whether client connection uses compression in client/server protocol. Deprecated in

MySQL 8.0.18.

82

Options and Variables Deprecated in MySQL 8.0

• Rsa_public_key: sha256_password authentication plugin RSA public key value. Deprecated in

MySQL 8.0.16.

• Slave_open_temp_tables: Number of temporary tables that replication SQL thread currently has

open. Deprecated in MySQL 8.0.26.

• Slave_rows_last_search_algorithm_used: Search algorithm most recently used by this

replica to locate rows for row-based replication (index, table, or hash scan). Deprecated in MySQL
8.0.26.

• abort-slave-event-count: Option used by mysql-test for debugging and testing of replication.

Deprecated in MySQL 8.0.29.

• admin-ssl: Enable connection encryption. Deprecated in MySQL 8.0.26.

• audit_log_connection_policy: Audit logging policy for connection-related events. Deprecated

in MySQL 8.0.34.

• audit_log_exclude_accounts: Accounts not to audit. Deprecated in MySQL 8.0.34.

• audit_log_include_accounts: Accounts to audit. Deprecated in MySQL 8.0.34.

• audit_log_policy: Audit logging policy. Deprecated in MySQL 8.0.34.

• audit_log_statement_policy: Audit logging policy for statement-related events. Deprecated in

MySQL 8.0.34.

• authentication_fido_rp_id: Relying party ID for FIDO multifactor authentication. Deprecated

in MySQL 8.0.35.

• binlog_format: Specifies format of binary log. Deprecated in MySQL 8.0.34.

• binlog_transaction_dependency_tracking: Source of dependency information (commit

timestamps or transaction write sets) from which to assess which transactions can be executed in
parallel by replica's multithreaded applier. Deprecated in MySQL 8.0.35.

• character-set-client-handshake: Do not ignore client side character set value sent during

handshake. Deprecated in MySQL 8.0.35.

• daemon_memcached_enable_binlog: . Deprecated in MySQL 8.0.22.

• daemon_memcached_engine_lib_name: Shared library implementing InnoDB memcached

plugin. Deprecated in MySQL 8.0.22.

• daemon_memcached_engine_lib_path: Directory which contains shared library implementing

InnoDB memcached plugin. Deprecated in MySQL 8.0.22.

• daemon_memcached_option: Space-separated options which are passed to underlying

memcached daemon on startup. Deprecated in MySQL 8.0.22.

• daemon_memcached_r_batch_size: Specifies how many memcached read operations to perform

before doing COMMIT to start new transaction. Deprecated in MySQL 8.0.22.

• daemon_memcached_w_batch_size: Specifies how many memcached write operations to

perform before doing COMMIT to start new transaction. Deprecated in MySQL 8.0.22.

• default_authentication_plugin: Default authentication plugin. Deprecated in MySQL 8.0.27.

• disconnect-slave-event-count: Option used by mysql-test for debugging and testing of

replication. Deprecated in MySQL 8.0.29.

• expire_logs_days: Purge binary logs after this many days. Deprecated in MySQL 8.0.3.

• group_replication_ip_whitelist: List of hosts permitted to connect to group. Deprecated in

MySQL 8.0.22.

83

Options and Variables Deprecated in MySQL 8.0

• group_replication_primary_member: Primary member UUID when group operates in single-

primary mode. Empty string if group is operating in multi-primary mode. Deprecated in MySQL 8.0.4.

• group_replication_recovery_complete_at: Recovery policies when handling cached

transactions after state transfer. Deprecated in MySQL 8.0.34.

• have_openssl: Whether mysqld supports SSL connections. Deprecated in MySQL 8.0.26.

• have_ssl: Whether mysqld supports SSL connections. Deprecated in MySQL 8.0.26.

• init_slave: Statements that are executed when replica connects to source. Deprecated in MySQL

8.0.26.

• innodb_api_bk_commit_interval: How often to auto-commit idle connections which use

InnoDB memcached interface, in seconds. Deprecated in MySQL 8.0.22.

• innodb_api_disable_rowlock: . Deprecated in MySQL 8.0.22.

• innodb_api_enable_binlog: Allows use of InnoDB memcached plugin with MySQL binary log.

Deprecated in MySQL 8.0.22.

• innodb_api_enable_mdl: Locks table used by InnoDB memcached plugin, so that it cannot be

dropped or altered by DDL through SQL interface. Deprecated in MySQL 8.0.22.

• innodb_api_trx_level: Allows control of transaction isolation level on queries processed by

memcached interface. Deprecated in MySQL 8.0.22.

• innodb_log_file_size: Size of each log file in log group. Deprecated in MySQL 8.0.30.

• innodb_log_files_in_group: Number of InnoDB log files in log group. Deprecated in MySQL

8.0.30.

• innodb_undo_tablespaces: Number of tablespace files that rollback segments are divided

between. Deprecated in MySQL 8.0.4.

• keyring_encrypted_file_data: keyring_encrypted_file plugin data file. Deprecated in MySQL

8.0.34.

• keyring_encrypted_file_password: keyring_encrypted_file plugin password. Deprecated in

MySQL 8.0.34.

• keyring_file_data: keyring_file plugin data file. Deprecated in MySQL 8.0.34.

• keyring_oci_ca_certificate: CA certificate file for peer authentication. Deprecated in MySQL

8.0.31.

• keyring_oci_compartment: OCI compartment OCID. Deprecated in MySQL 8.0.31.

• keyring_oci_encryption_endpoint: OCI encryption server endpoint. Deprecated in MySQL

8.0.31.

• keyring_oci_key_file: OCI RSA private key file. Deprecated in MySQL 8.0.31.

• keyring_oci_key_fingerprint: OCI RSA private key file fingerprint. Deprecated in MySQL

8.0.31.

• keyring_oci_management_endpoint: OCI management server endpoint. Deprecated in MySQL

8.0.31.

• keyring_oci_master_key: OCI master key OCID. Deprecated in MySQL 8.0.31.

• keyring_oci_secrets_endpoint: OCI secrets server endpoint. Deprecated in MySQL 8.0.31.

• keyring_oci_tenancy: OCI tenancy OCID. Deprecated in MySQL 8.0.31.

84

Options and Variables Deprecated in MySQL 8.0

• keyring_oci_user: OCI user OCID. Deprecated in MySQL 8.0.31.

• keyring_oci_vaults_endpoint: OCI vaults server endpoint. Deprecated in MySQL 8.0.31.

• keyring_oci_virtual_vault: OCI vault OCID. Deprecated in MySQL 8.0.31.

• log_bin_trust_function_creators: If equal to 0 (default), then when --log-bin is used, stored
function creation is allowed only to users having SUPER privilege and only if function created does
not break binary logging. Deprecated in MySQL 8.0.34.

• log_bin_use_v1_row_events: Whether server is using version 1 binary log row events.

Deprecated in MySQL 8.0.18.

• log_slave_updates: Whether replica should log updates performed by its replication SQL thread

to its own binary log. Deprecated in MySQL 8.0.26.

• log_slow_slave_statements: Cause slow statements as executed by replica to be written to

slow query log. Deprecated in MySQL 8.0.26.

• log_statements_unsafe_for_binlog: Disables error 1592 warnings being written to error log.

Deprecated in MySQL 8.0.34.

• log_syslog: Whether to write error log to syslog. Deprecated in MySQL 8.0.2.

• master-info-file: Location and name of file that remembers source and where I/O replication

thread is in source's binary log. Deprecated in MySQL 8.0.18.

• master_info_repository: Whether to write connection metadata repository, containing source
information and replication I/O thread location in source's binary log, to file or table. Deprecated in
MySQL 8.0.23.

• master_verify_checksum: Cause source to examine checksums when reading from binary log.

Deprecated in MySQL 8.0.26.

• max_length_for_sort_data: Max number of bytes in sorted records. Deprecated in MySQL

8.0.20.

• myisam_repair_threads: Number of threads to use when repairing MyISAM tables. 1 disables

parallel repair. Deprecated in MySQL 8.0.29.

• mysql_native_password_proxy_users: Whether mysql_native_password authentication plugin

does proxying. Deprecated in MySQL 8.0.16.

• new: Use very new, possibly 'unsafe' functions. Deprecated in MySQL 8.0.35.

• no-dd-upgrade: Prevent automatic upgrade of data dictionary tables at startup. Deprecated in

MySQL 8.0.16.

• old: Cause server to revert to certain behaviors present in older versions. Deprecated in MySQL

8.0.35.

• old-style-user-limits: Enable old-style user limits (before 5.0.3, user resources were counted

per each user+host vs. per account). Deprecated in MySQL 8.0.30.

• performance_schema_show_processlist: Select SHOW PROCESSLIST implementation.

Deprecated in MySQL 8.0.35.

• pseudo_slave_mode: For internal server use. Deprecated in MySQL 8.0.26.

• query_prealloc_size: Persistent buffer for query parsing and execution. Deprecated in MySQL

8.0.29.

• relay_log_info_file: File name for applier metadata repository in which replica records

information about relay logs. Deprecated in MySQL 8.0.18.

85

Options and Variables Deprecated in MySQL 8.0

• relay_log_info_repository: Whether to write location of replication SQL thread in relay logs to

file or table. Deprecated in MySQL 8.0.23.

• replica_parallel_type: Tells replica to use timestamp information (LOGICAL_CLOCK) or
database partitioning (DATABASE) to parallelize transactions. Deprecated in MySQL 8.0.29.

• rpl_stop_slave_timeout: Number of seconds that STOP REPLICA or STOP SLAVE waits

before timing out. Deprecated in MySQL 8.0.26.

• safe-user-create: Do not allow new user creation by user who has no write privileges to

mysql.user table; this option is deprecated and ignored. Deprecated in MySQL 8.0.11.

• sha256_password_auto_generate_rsa_keys: Whether to generate RSA key-pair files

automatically. Deprecated in MySQL 8.0.16.

• sha256_password_private_key_path: SHA256 authentication plugin private key path name.

Deprecated in MySQL 8.0.16.

• sha256_password_proxy_users: Whether sha256_password authentication plugin does

proxying. Deprecated in MySQL 8.0.16.

• sha256_password_public_key_path: SHA256 authentication plugin public key path name.

Deprecated in MySQL 8.0.16.

• show-slave-auth-info: Show user name and password in SHOW REPLICAS and SHOW

SLAVE HOSTS on this source. Deprecated in MySQL 8.0.26.

• skip-character-set-client-handshake: Ignore client side character set value sent during

handshake. Deprecated in MySQL 8.0.35.

• skip-host-cache: Do not cache host names. Deprecated in MySQL 8.0.30.

• skip-new: Do not use new, possibly wrong routines. Deprecated in MySQL 8.0.35.

• skip-slave-start: If set, replication is not autostarted when replica server starts. Deprecated in

MySQL 8.0.26.

• skip-ssl: Disable connection encryption. Deprecated in MySQL 8.0.26.

• slave-skip-errors: Tells replication thread to continue replication when query returns error from

provided list. Deprecated in MySQL 8.0.26.

• slave_checkpoint_group: Maximum number of transactions processed by multithreaded replica

before checkpoint operation is called to update progress status. Not supported by NDB Cluster.
Deprecated in MySQL 8.0.26.

• slave_checkpoint_period: Update progress status of multithreaded replica and flush relay log
info to disk after this number of milliseconds. Not supported by NDB Cluster. Deprecated in MySQL
8.0.26.

• slave_compressed_protocol: Use compression of source/replica protocol. Deprecated in

MySQL 8.0.18.

• slave_load_tmpdir: Location where replica should put its temporary files when replicating LOAD

DATA statements. Deprecated in MySQL 8.0.26.

• slave_max_allowed_packet: Maximum size, in bytes, of packet that can be sent from replication

source server to replica; overrides max_allowed_packet. Deprecated in MySQL 8.0.26.

• slave_net_timeout: Number of seconds to wait for more data from source/replica connection

before aborting read. Deprecated in MySQL 8.0.26.

• slave_parallel_type: Tells replica to use timestamp information (LOGICAL_CLOCK) or
database partioning (DATABASE) to parallelize transactions. Deprecated in MySQL 8.0.26.

86

Options and Variables Removed in MySQL 8.0

• slave_parallel_workers: Number of applier threads for executing replication transactions in
parallel; 0 or 1 disables replica multithreading. NDB Cluster: see documentation. Deprecated in
MySQL 8.0.26.

• slave_pending_jobs_size_max: Maximum size of replica worker queues holding events not yet

applied. Deprecated in MySQL 8.0.26.

• slave_preserve_commit_order: Ensures that all commits by replica workers happen in same
order as on source to maintain consistency when using parallel applier threads. Deprecated in
MySQL 8.0.26.

• slave_rows_search_algorithms: Determines search algorithms used for replica update

batching. Any 2 or 3 from this list: INDEX_SEARCH, TABLE_SCAN, HASH_SCAN. Deprecated in
MySQL 8.0.18.

• slave_sql_verify_checksum: Cause replica to examine checksums when reading from relay

log. Deprecated in MySQL 8.0.26.

• slave_transaction_retries: Number of times replication SQL thread retries transaction in

case it failed with deadlock or elapsed lock wait timeout, before giving up and stopping. Deprecated
in MySQL 8.0.26.

• slave_type_conversions: Controls type conversion mode on replica. Value is list of zero or

more elements from this list: ALL_LOSSY, ALL_NON_LOSSY. Set to empty string to disallow type
conversions between source and replica. Deprecated in MySQL 8.0.26.

• sql_slave_skip_counter: Number of events from source that replica should skip. Not

compatible with GTID replication. Deprecated in MySQL 8.0.26.

• ssl: Enable connection encryption. Deprecated in MySQL 8.0.26.

• ssl_fips_mode: Whether to enable FIPS mode on server side. Deprecated in MySQL 8.0.34.

• symbolic-links: Permit symbolic links for MyISAM tables. Deprecated in MySQL 8.0.2.

• sync_master_info: Synchronize source information after every #th event. Deprecated in MySQL

8.0.26.

• sync_relay_log_info: Synchronize relay.info file to disk after every #th event. Deprecated in

MySQL 8.0.34.

• temptable_use_mmap: Defines whether TempTable storage engine allocates memory-mapped

files when the temptable_max_ram threshold is reached. Deprecated in MySQL 8.0.26.

• transaction_prealloc_size: Persistent buffer for transactions to be stored in binary log.

Deprecated in MySQL 8.0.29.

• transaction_write_set_extraction: Defines algorithm used to hash writes extracted during

transaction. Deprecated in MySQL 8.0.26.

Options and Variables Removed in MySQL 8.0

The following system variables, status variables, and options have been removed in MySQL 8.0.

• Com_alter_db_upgrade: Count of ALTER DATABASE ... UPGRADE DATA DIRECTORY NAME

statements. Removed in MySQL 8.0.0.

• Innodb_available_undo_logs: Total number of InnoDB rollback segments; different from

innodb_rollback_segments, which displays number of active rollback segments. Removed in MySQL
8.0.2.

• Qcache_free_blocks: Number of free memory blocks in query cache. Removed in MySQL 8.0.3.

87

Options and Variables Removed in MySQL 8.0

• Qcache_free_memory: Amount of free memory for query cache. Removed in MySQL 8.0.3.

• Qcache_hits: Number of query cache hits. Removed in MySQL 8.0.3.

• Qcache_inserts: Number of query cache inserts. Removed in MySQL 8.0.3.

• Qcache_lowmem_prunes: Number of queries which were deleted from query cache due to lack of

free memory in cache. Removed in MySQL 8.0.3.

• Qcache_not_cached: Number of noncached queries (not cacheable, or not cached due to

query_cache_type setting). Removed in MySQL 8.0.3.

• Qcache_queries_in_cache: Number of queries registered in query cache. Removed in MySQL

8.0.3.

• Qcache_total_blocks: Total number of blocks in query cache. Removed in MySQL 8.0.3.

• Slave_heartbeat_period: Replica's replication heartbeat interval, in seconds. Removed in

MySQL 8.0.1.

• Slave_last_heartbeat: Shows when latest heartbeat signal was received, in TIMESTAMP

format. Removed in MySQL 8.0.1.

• Slave_received_heartbeats: Number of heartbeats received by replica since previous reset.

Removed in MySQL 8.0.1.

• Slave_retried_transactions: Total number of times since startup that replication SQL thread

has retried transactions. Removed in MySQL 8.0.1.

• Slave_running: State of this server as replica (replication I/O thread status). Removed in MySQL

8.0.1.

• bootstrap: Used by mysql installation scripts. Removed in MySQL 8.0.0.

• date_format: DATE format (unused). Removed in MySQL 8.0.3.

• datetime_format: DATETIME/TIMESTAMP format (unused). Removed in MySQL 8.0.3.

• des-key-file: Load keys for des_encrypt() and des_encrypt from given file. Removed in MySQL

8.0.3.

• group_replication_allow_local_disjoint_gtids_join: Allow current server to join group

even if it has transactions not present in group. Removed in MySQL 8.0.4.

• have_crypt: Availability of crypt() system call. Removed in MySQL 8.0.3.

• ignore-db-dir: Treat directory as nondatabase directory. Removed in MySQL 8.0.0.

• ignore_builtin_innodb: Ignore built-in InnoDB. Removed in MySQL 8.0.3.

• ignore_db_dirs: Directories treated as nondatabase directories. Removed in MySQL 8.0.0.

• innodb_checksums: Enable InnoDB checksums validation. Removed in MySQL 8.0.0.

• innodb_disable_resize_buffer_pool_debug: Disables resizing of InnoDB buffer pool.

Removed in MySQL 8.0.0.

• innodb_file_format: Format for new InnoDB tables. Removed in MySQL 8.0.0.

• innodb_file_format_check: Whether InnoDB performs file format compatibility checking.

Removed in MySQL 8.0.0.

• innodb_file_format_max: File format tag in shared tablespace. Removed in MySQL 8.0.0.

• innodb_large_prefix: Enables longer keys for column prefix indexes. Removed in MySQL 8.0.0.

88

Options and Variables Removed in MySQL 8.0

• innodb_locks_unsafe_for_binlog: Force InnoDB not to use next-key locking. Instead use only

row-level locking. Removed in MySQL 8.0.0.

• innodb_scan_directories: Defines directories to scan for tablespace files during InnoDB

recovery. Removed in MySQL 8.0.4.

• innodb_stats_sample_pages: Number of index pages to sample for index distribution statistics.

Removed in MySQL 8.0.0.

• innodb_support_xa: Enable InnoDB support for XA two-phase commit. Removed in MySQL

8.0.0.

• innodb_undo_logs: Number of undo logs (rollback segments) used by InnoDB; alias for

innodb_rollback_segments. Removed in MySQL 8.0.2.

• internal_tmp_disk_storage_engine: Storage engine for internal temporary tables. Removed

in MySQL 8.0.16.

• log-warnings: Write some noncritical warnings to log file. Removed in MySQL 8.0.3.

• log_builtin_as_identified_by_password: Whether to log CREATE/ALTER USER, GRANT

in backward-compatible fashion. Removed in MySQL 8.0.11.

• log_error_filter_rules: Filter rules for error logging. Removed in MySQL 8.0.4.

• log_syslog: Whether to write error log to syslog. Removed in MySQL 8.0.13.

• log_syslog_facility: Facility for syslog messages. Removed in MySQL 8.0.13.

• log_syslog_include_pid: Whether to include server PID in syslog messages. Removed in

MySQL 8.0.13.

• log_syslog_tag: Tag for server identifier in syslog messages. Removed in MySQL 8.0.13.

• max_tmp_tables: Unused. Removed in MySQL 8.0.3.

• metadata_locks_cache_size: Size of metadata locks cache. Removed in MySQL 8.0.13.

• metadata_locks_hash_instances: Number of metadata lock hashes. Removed in MySQL

8.0.13.

• multi_range_count: Maximum number of ranges to send to table handler at once during range

selects. Removed in MySQL 8.0.3.

• myisam_repair_threads: Number of threads to use when repairing MyISAM tables. 1 disables

parallel repair. Removed in MySQL 8.0.30.

• old_passwords: Selects password hashing method for PASSWORD(). Removed in MySQL 8.0.11.

• partition: Enable (or disable) partitioning support. Removed in MySQL 8.0.0.

• query_cache_limit: Do not cache results that are bigger than this. Removed in MySQL 8.0.3.

• query_cache_min_res_unit: Minimal size of unit in which space for results is allocated (last unit

is trimmed after writing all result data). Removed in MySQL 8.0.3.

• query_cache_size: Memory allocated to store results from old queries. Removed in MySQL 8.0.3.

• query_cache_type: Query cache type. Removed in MySQL 8.0.3.

• query_cache_wlock_invalidate: Invalidate queries in query cache on LOCK for write.

Removed in MySQL 8.0.3.

• secure_auth: Disallow authentication for accounts that have old (pre-4.1) passwords. Removed in

MySQL 8.0.3.

89

How to Report Bugs or Problems

• show_compatibility_56: Compatibility for SHOW STATUS/VARIABLES. Removed in MySQL

8.0.1.

• skip-partition: Do not enable user-defined partitioning. Removed in MySQL 8.0.0.

• sync_frm: Sync .frm to disk on create. Enabled by default. Removed in MySQL 8.0.0.

• temp-pool: Using this option causes most temporary files created to use small set of names, rather

than unique name for each new file. Removed in MySQL 8.0.1.

• time_format: TIME format (unused). Removed in MySQL 8.0.3.

• tx_isolation: Default transaction isolation level. Removed in MySQL 8.0.3.

• tx_read_only: Default transaction access mode. Removed in MySQL 8.0.3.

1.5 How to Report Bugs or Problems

Before posting a bug report about a problem, please try to verify that it is a bug and that it has not been
reported already:

• Start by searching the MySQL online manual at https://dev.mysql.com/doc/. We try to keep the

manual up to date by updating it frequently with solutions to newly found problems. In addition, the
release notes accompanying the manual can be particularly useful since it is quite possible that a
newer version contains a solution to your problem. The release notes are available at the location
just given for the manual.

• If you get a parse error for an SQL statement, please check your syntax closely. If you cannot find
something wrong with it, it is extremely likely that your current version of MySQL Server doesn't
support the syntax you are using. If you are using the current version and the manual doesn't cover
the syntax that you are using, MySQL Server doesn't support your statement.

If the manual covers the syntax you are using, but you have an older version of MySQL Server, you
should check the MySQL change history to see when the syntax was implemented. In this case, you
have the option of upgrading to a newer version of MySQL Server.

• For solutions to some common problems, see Section B.3, “Problems and Common Errors”.

• Search the bugs database at http://bugs.mysql.com/ to see whether the bug has been reported and

fixed.

• You can also use http://www.mysql.com/search/ to search all the Web pages (including the manual)

that are located at the MySQL website.

If you cannot find an answer in the manual, the bugs database, or the mailing list archives, check with
your local MySQL expert. If you still cannot find an answer to your question, please use the following
guidelines for reporting the bug.

The normal way to report bugs is to visit http://bugs.mysql.com/, which is the address for our bugs
database. This database is public and can be browsed and searched by anyone. If you log in to the
system, you can enter new reports.

Bugs posted in the bugs database at http://bugs.mysql.com/ that are corrected for a given release are
noted in the release notes.

If you find a security bug in MySQL Server, please let us know immediately by sending an email
message to <secalert_us@oracle.com>. Exception: Support customers should report all
problems, including security bugs, to Oracle Support at http://support.oracle.com/.

To discuss problems with other users, you can use the MySQL Community Slack.

Writing a good bug report takes patience, but doing it right the first time saves time both for us and for
yourself. A good bug report, containing a full test case for the bug, makes it very likely that we will fix

90

How to Report Bugs or Problems

the bug in the next release. This section helps you write your report correctly so that you do not waste
your time doing things that may not help us much or at all. Please read this section carefully and make
sure that all the information described here is included in your report.

Preferably, you should test the problem using the latest production or development version of MySQL
Server before posting. Anyone should be able to repeat the bug by just using mysql test <
script_file on your test case or by running the shell or Perl script that you include in the bug report.
Any bug that we are able to repeat has a high chance of being fixed in the next MySQL release.

It is most helpful when a good description of the problem is included in the bug report. That is, give a
good example of everything you did that led to the problem and describe, in exact detail, the problem
itself. The best reports are those that include a full example showing how to reproduce the bug or
problem. See Section 7.9, “Debugging MySQL”.

Remember that it is possible for us to respond to a report containing too much information, but not to
one containing too little. People often omit facts because they think they know the cause of a problem
and assume that some details do not matter. A good principle to follow is that if you are in doubt about
stating something, state it. It is faster and less troublesome to write a couple more lines in your report
than to wait longer for the answer if we must ask you to provide information that was missing from the
initial report.

The most common errors made in bug reports are (a) not including the version number of the MySQL
distribution that you use, and (b) not fully describing the platform on which the MySQL server is
installed (including the platform type and version number). These are highly relevant pieces of
information, and in 99 cases out of 100, the bug report is useless without them. Very often we get
questions like, “Why doesn't this work for me?” Then we find that the feature requested wasn't
implemented in that MySQL version, or that a bug described in a report has been fixed in newer
MySQL versions. Errors often are platform-dependent. In such cases, it is next to impossible for us to
fix anything without knowing the operating system and the version number of the platform.

If you compiled MySQL from source, remember also to provide information about your compiler if
it is related to the problem. Often people find bugs in compilers and think the problem is MySQL-
related. Most compilers are under development all the time and become better version by version. To
determine whether your problem depends on your compiler, we need to know what compiler you used.
Note that every compiling problem should be regarded as a bug and reported accordingly.

If a program produces an error message, it is very important to include the message in your report. If
we try to search for something from the archives, it is better that the error message reported exactly
matches the one that the program produces. (Even the lettercase should be observed.) It is best
to copy and paste the entire error message into your report. You should never try to reproduce the
message from memory.

If you have a problem with Connector/ODBC (MyODBC), please try to generate a trace file and send it
with your report. See How to Report Connector/ODBC Problems or Bugs.

If your report includes long query output lines from test cases that you run with the mysql command-
line tool, you can make the output more readable by using the --vertical option or the \G statement
terminator. The EXPLAIN SELECT example later in this section demonstrates the use of \G.

Please include the following information in your report:

• The version number of the MySQL distribution you are using (for example, MySQL 5.7.10). You can
find out which version you are running by executing mysqladmin version. The mysqladmin
program can be found in the bin directory under your MySQL installation directory.

• The manufacturer and model of the machine on which you experience the problem.

• The operating system name and version. If you work with Windows, you can usually get the name
and version number by double-clicking your My Computer icon and pulling down the “Help/About
Windows” menu. For most Unix-like operating systems, you can get this information by executing the
command uname -a.

91

How to Report Bugs or Problems

• Sometimes the amount of memory (real and virtual) is relevant. If in doubt, include these values.

• The contents of the docs/INFO_BIN file from your MySQL installation. This file contains information

about how MySQL was configured and compiled.

• If you are using a source distribution of the MySQL software, include the name and version number

of the compiler that you used. If you have a binary distribution, include the distribution name.

• If the problem occurs during compilation, include the exact error messages and also a few lines of

context around the offending code in the file where the error occurs.

• If mysqld died, you should also report the statement that caused mysqld to unexpectedly exit. You
can usually get this information by running mysqld with query logging enabled, and then looking in
the log after mysqld exits. See Section 7.9, “Debugging MySQL”.

• If a database table is related to the problem, include the output from the SHOW CREATE TABLE
db_name.tbl_name statement in the bug report. This is a very easy way to get the definition of
any table in a database. The information helps us create a situation matching the one that you have
experienced.

• The SQL mode in effect when the problem occurred can be significant, so please report the value
of the sql_mode system variable. For stored procedure, stored function, and trigger objects, the
relevant sql_mode value is the one in effect when the object was created. For a stored procedure
or function, the SHOW CREATE PROCEDURE or SHOW CREATE FUNCTION statement shows the
relevant SQL mode, or you can query INFORMATION_SCHEMA for the information:

SELECT ROUTINE_SCHEMA, ROUTINE_NAME, SQL_MODE
FROM INFORMATION_SCHEMA.ROUTINES;

For triggers, you can use this statement:

SELECT EVENT_OBJECT_SCHEMA, EVENT_OBJECT_TABLE, TRIGGER_NAME, SQL_MODE
FROM INFORMATION_SCHEMA.TRIGGERS;

• For performance-related bugs or problems with SELECT statements, you should always include

the output of EXPLAIN SELECT ..., and at least the number of rows that the SELECT statement
produces. You should also include the output from SHOW CREATE TABLE tbl_name for each
table that is involved. The more information you provide about your situation, the more likely it is that
someone can help you.

The following is an example of a very good bug report. The statements are run using the mysql
command-line tool. Note the use of the \G statement terminator for statements that would otherwise
provide very long output lines that are difficult to read.

mysql> SHOW VARIABLES;
mysql> SHOW COLUMNS FROM ...\G
       <output from SHOW COLUMNS>
mysql> EXPLAIN SELECT ...\G
       <output from EXPLAIN>
mysql> FLUSH STATUS;
mysql> SELECT ...;
       <A short version of the output from SELECT,
       including the time taken to run the query>
mysql> SHOW STATUS;
       <output from SHOW STATUS>

• If a bug or problem occurs while running mysqld, try to provide an input script that reproduces the
anomaly. This script should include any necessary source files. The more closely the script can
reproduce your situation, the better. If you can make a reproducible test case, you should upload it to
be attached to the bug report.

If you cannot provide a script, you should at least include the output from mysqladmin variables
extended-status processlist in your report to provide some information on how your system
is performing.

92

How to Report Bugs or Problems

• If you cannot produce a test case with only a few rows, or if the test table is too big to be included in
the bug report (more than 10 rows), you should dump your tables using mysqldump and create a
README file that describes your problem. Create a compressed archive of your files using tar and
gzip or zip. After you initiate a bug report for our bugs database at http://bugs.mysql.com/, click the
Files tab in the bug report for instructions on uploading the archive to the bugs database.

• If you believe that the MySQL server produces a strange result from a statement, include not only the
result, but also your opinion of what the result should be, and an explanation describing the basis for
your opinion.

• When you provide an example of the problem, it is better to use the table names, variable names,
and so forth that exist in your actual situation than to come up with new names. The problem could
be related to the name of a table or variable. These cases are rare, perhaps, but it is better to be
safe than sorry. After all, it should be easier for you to provide an example that uses your actual
situation, and it is by all means better for us. If you have data that you do not want to be visible
to others in the bug report, you can upload it using the Files tab as previously described. If the
information is really top secret and you do not want to show it even to us, go ahead and provide an
example using other names, but please regard this as the last choice.

• Include all the options given to the relevant programs, if possible. For example, indicate the

options that you use when you start the mysqld server, as well as the options that you use to run
any MySQL client programs. The options to programs such as mysqld and mysql, and to the
configure script, are often key to resolving problems and are very relevant. It is never a bad idea
to include them. If your problem involves a program written in a language such as Perl or PHP,
please include the language processor's version number, as well as the version for any modules
that the program uses. For example, if you have a Perl script that uses the DBI and DBD::mysql
modules, include the version numbers for Perl, DBI, and DBD::mysql.

• If your question is related to the privilege system, please include the output of mysqladmin

reload, and all the error messages you get when trying to connect. When you test your privileges,
you should execute mysqladmin reload version and try to connect with the program that gives
you trouble.

• If you have a patch for a bug, do include it. But do not assume that the patch is all we need, or that

we can use it, if you do not provide some necessary information such as test cases showing the bug
that your patch fixes. We might find problems with your patch or we might not understand it at all. If
so, we cannot use it.

If we cannot verify the exact purpose of the patch, we will not use it. Test cases help us here. Show
that the patch handles all the situations that may occur. If we find a borderline case (even a rare one)
where the patch will not work, it may be useless.

• Guesses about what the bug is, why it occurs, or what it depends on are usually wrong. Even the

MySQL team cannot guess such things without first using a debugger to determine the real cause of
a bug.

• Indicate in your bug report that you have checked the reference manual and mail archive so that

others know you have tried to solve the problem yourself.

• If your data appears corrupt or you get errors when you access a particular table, first check your

tables with CHECK TABLE. If that statement reports any errors:

• The InnoDB crash recovery mechanism handles cleanup when the server is restarted after being
killed, so in typical operation there is no need to “repair” tables. If you encounter an error with
InnoDB tables, restart the server and see whether the problem persists, or whether the error
affected only cached data in memory. If data is corrupted on disk, consider restarting with the
innodb_force_recovery option enabled so that you can dump the affected tables.

• For non-transactional tables, try to repair them with REPAIR TABLE or with myisamchk. See

Chapter 7, MySQL Server Administration.

93

MySQL Standards Compliance

If you are running Windows, please verify the value of lower_case_table_names using the SHOW
VARIABLES LIKE 'lower_case_table_names' statement. This variable affects how the server
handles lettercase of database and table names. Its effect for a given value should be as described
in Section 11.2.3, “Identifier Case Sensitivity”.

• If you often get corrupted tables, you should try to find out when and why this happens. In this case,
the error log in the MySQL data directory may contain some information about what happened. (This
is the file with the .err suffix in the name.) See Section 7.4.2, “The Error Log”. Please include any
relevant information from this file in your bug report. Normally mysqld should never corrupt a table
if nothing killed it in the middle of an update. If you can find the cause of mysqld dying, it is much
easier for us to provide you with a fix for the problem. See Section B.3.1, “How to Determine What Is
Causing a Problem”.

• If possible, download and install the most recent version of MySQL Server and check whether it
solves your problem. All versions of the MySQL software are thoroughly tested and should work
without problems. We believe in making everything as backward-compatible as possible, and you
should be able to switch MySQL versions without difficulty. See Section 2.1.2, “Which MySQL
Version and Distribution to Install”.

1.6 MySQL Standards Compliance

This section describes how MySQL relates to the ANSI/ISO SQL standards. MySQL Server has many
extensions to the SQL standard, and here you can find out what they are and how to use them. You
can also find information about functionality missing from MySQL Server, and how to work around
some of the differences.

The SQL standard has been evolving since 1986 and several versions exist. In this manual, “SQL-92”
refers to the standard released in 1992. “SQL:1999”, “SQL:2003”, “SQL:2008”, and “SQL:2011” refer
to the versions of the standard released in the corresponding years, with the last being the most recent
version. We use the phrase “the SQL standard” or “standard SQL” to mean the current version of the
SQL Standard at any time.

One of our main goals with the product is to continue to work toward compliance with the SQL
standard, but without sacrificing speed or reliability. We are not afraid to add extensions to SQL
or support for non-SQL features if this greatly increases the usability of MySQL Server for a large
segment of our user base. The HANDLER interface is an example of this strategy. See Section 15.2.5,
“HANDLER Statement”.

We continue to support transactional and nontransactional databases to satisfy both mission-critical
24/7 usage and heavy Web or logging usage.

MySQL Server was originally designed to work with medium-sized databases (10-100 million rows,
or about 100MB per table) on small computer systems. Today MySQL Server handles terabyte-sized
databases.

We are not targeting real-time support, although MySQL replication capabilities offer significant
functionality.

MySQL supports ODBC levels 0 to 3.51.

MySQL supports high-availability database clustering using the NDBCLUSTER storage engine. See
Chapter 25, MySQL NDB Cluster 8.0.

We implement XML functionality which supports most of the W3C XPath standard. See Section 14.11,
“XML Functions”.

MySQL supports a native JSON data type as defined by RFC 7159, and based on the ECMAScript
standard (ECMA-262). See Section 13.5, “The JSON Data Type”. MySQL also implements a subset

94

Selecting SQL Modes

of the SQL/JSON functions specified by a pre-publication draft of the SQL:2016 standard; see
Section 14.17, “JSON Functions”, for more information.

Selecting SQL Modes

The MySQL server can operate in different SQL modes, and can apply these modes differently for
different clients, depending on the value of the sql_mode system variable. DBAs can set the global
SQL mode to match site server operating requirements, and each application can set its session SQL
mode to its own requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes
it easier to use MySQL in different environments and to use MySQL together with other database
servers.

For more information on setting the SQL mode, see Section 7.1.11, “Server SQL Modes”.

Running MySQL in ANSI Mode

To run MySQL Server in ANSI mode, start mysqld with the --ansi option. Running the server in
ANSI mode is the same as starting it with the following options:

--transaction-isolation=SERIALIZABLE --sql-mode=ANSI

To achieve the same effect at runtime, execute these two statements:

SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET GLOBAL sql_mode = 'ANSI';

You can see that setting the sql_mode system variable to 'ANSI' enables all SQL mode options that
are relevant for ANSI mode as follows:

mysql> SET GLOBAL sql_mode='ANSI';
mysql> SELECT @@GLOBAL.sql_mode;
        -> 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ANSI'

Running the server in ANSI mode with --ansi is not quite the same as setting the SQL mode to
'ANSI' because the --ansi option also sets the transaction isolation level.

See Section 7.1.7, “Server Command Options”.

1.6.1 MySQL Extensions to Standard SQL

MySQL Server supports some extensions that you are not likely to find in other SQL DBMSs. Be
warned that if you use them, your code is most likely not portable to other SQL servers. In some cases,
you can write code that includes MySQL extensions, but is still portable, by using comments of the
following form:

/*! MySQL-specific code */

In this case, MySQL Server parses and executes the code within the comment as it would any other
SQL statement, but other SQL servers should ignore the extensions. For example, MySQL Server
recognizes the STRAIGHT_JOIN keyword in the following statement, but other servers should not:

SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...

If you add a version number after the ! character, the syntax within the comment is executed only if the
MySQL version is greater than or equal to the specified version number. The KEY_BLOCK_SIZE clause
in the following comment is executed only by servers from MySQL 5.1.10 or higher:

CREATE TABLE t1(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024 */;

The following descriptions list MySQL extensions, organized by category.

95

MySQL Extensions to Standard SQL

• Organization of data on disk

MySQL Server maps each database to a directory under the MySQL data directory, and maps tables
within a database to file names in the database directory. Consequently, database and table names
are case-sensitive in MySQL Server on operating systems that have case-sensitive file names (such
as most Unix systems). See Section 11.2.3, “Identifier Case Sensitivity”.

• General language syntax

• By default, strings can be enclosed by " as well as '. If the ANSI_QUOTES SQL mode is enabled,
strings can be enclosed only by ' and the server interprets strings enclosed by " as identifiers.

• \ is the escape character in strings.

• In SQL statements, you can access tables from different databases with the db_name.tbl_name

syntax. Some SQL servers provide the same functionality but call this User space. MySQL
Server doesn't support tablespaces such as used in statements like this: CREATE TABLE
ralph.my_table ... IN my_tablespace.

• SQL statement syntax

• The ANALYZE TABLE, CHECK TABLE, OPTIMIZE TABLE, and REPAIR TABLE statements.

• The CREATE DATABASE, DROP DATABASE, and ALTER DATABASE statements. See

Section 15.1.12, “CREATE DATABASE Statement”, Section 15.1.24, “DROP DATABASE
Statement”, and Section 15.1.2, “ALTER DATABASE Statement”.

• The DO statement.

• EXPLAIN SELECT to obtain a description of how tables are processed by the query optimizer.

• The FLUSH and RESET statements.

• The SET statement. See Section 15.7.6.1, “SET Syntax for Variable Assignment”.

• The SHOW statement. See Section 15.7.7, “SHOW Statements”. The information produced by

many of the MySQL-specific SHOW statements can be obtained in more standard fashion by using
SELECT to query INFORMATION_SCHEMA. See Chapter 28, INFORMATION_SCHEMA Tables.

•   Use of LOAD DATA. In many cases, this syntax is compatible with Oracle LOAD DATA. See

Section 15.2.9, “LOAD DATA Statement”.

• Use of RENAME TABLE. See Section 15.1.36, “RENAME TABLE Statement”.

• Use of REPLACE instead of DELETE plus INSERT. See Section 15.2.12, “REPLACE Statement”.

• Use of CHANGE col_name, DROP col_name, or DROP INDEX, IGNORE or RENAME in ALTER
TABLE statements. Use of multiple ADD, ALTER, DROP, or CHANGE clauses in an ALTER TABLE
statement. See Section 15.1.9, “ALTER TABLE Statement”.

• Use of index names, indexes on a prefix of a column, and use of INDEX or KEY in CREATE TABLE

statements. See Section 15.1.20, “CREATE TABLE Statement”.

• Use of TEMPORARY or IF NOT EXISTS with CREATE TABLE.

• Use of IF EXISTS with DROP TABLE and DROP DATABASE.

• The capability of dropping multiple tables with a single DROP TABLE statement.

• The ORDER BY and LIMIT clauses of the UPDATE and DELETE statements.

• INSERT INTO tbl_name SET col_name = ... syntax.

96

MySQL Extensions to Standard SQL

• The DELAYED clause of the INSERT and REPLACE statements.

• The LOW_PRIORITY clause of the INSERT, REPLACE, DELETE, and UPDATE statements.

• Use of INTO OUTFILE or INTO DUMPFILE in SELECT statements. See Section 15.2.13,

“SELECT Statement”.

• Options such as STRAIGHT_JOIN or SQL_SMALL_RESULT in SELECT statements.

• You don't need to name all selected columns in the GROUP BY clause. This gives better

performance for some very specific, but quite normal queries. See Section 14.19, “Aggregate
Functions”.

• You can specify ASC and DESC with GROUP BY, not just with ORDER BY.

• The ability to set variables in a statement with the := assignment operator. See Section 11.4,

“User-Defined Variables”.

• Data types

• The MEDIUMINT, SET, and ENUM data types, and the various BLOB and TEXT data types.

• The AUTO_INCREMENT, BINARY, NULL, UNSIGNED, and ZEROFILL data type attributes.

• Functions and operators

• To make it easier for users who migrate from other SQL environments, MySQL Server supports

aliases for many functions. For example, all string functions support both standard SQL syntax and
ODBC syntax.

• MySQL Server understands the || and && operators to mean logical OR and AND, as in the C

programming language. In MySQL Server, || and OR are synonyms, as are && and AND. Because
of this nice syntax, MySQL Server doesn't support the standard SQL || operator for string
concatenation; use CONCAT() instead. Because CONCAT() takes any number of arguments, it is
easy to convert use of the || operator to MySQL Server.

• Use of COUNT(DISTINCT value_list) where value_list has more than one element.

• String comparisons are case-insensitive by default, with sort ordering determined by the collation
of the current character set, which is utf8mb4 by default. To perform case-sensitive comparisons
instead, you should declare your columns with the BINARY attribute or use the BINARY cast, which
causes comparisons to be done using the underlying character code values rather than a lexical
ordering.

•   The % operator is a synonym for MOD(). That is, N % M is equivalent to MOD(N,M). % is

supported for C programmers and for compatibility with PostgreSQL.

• The =, <>, <=, <, >=, >, <<, >>, <=>, AND, OR, or LIKE operators may be used in expressions in

the output column list (to the left of the FROM) in SELECT statements. For example:

mysql> SELECT col1=1 AND col2=2 FROM my_table;

• The LAST_INSERT_ID() function returns the most recent AUTO_INCREMENT value. See

Section 14.15, “Information Functions”.

• LIKE is permitted on numeric values.

• The REGEXP and NOT REGEXP extended regular expression operators.

• CONCAT() or CHAR() with one argument or more than two arguments. (In MySQL Server, these

functions can take a variable number of arguments.)

97

MySQL Differences from Standard SQL

• The BIT_COUNT(), CASE, ELT(), FROM_DAYS(), FORMAT(), IF(), MD5(), PERIOD_ADD(),

PERIOD_DIFF(), TO_DAYS(), and WEEKDAY() functions.

• Use of TRIM() to trim substrings. Standard SQL supports removal of single characters only.

• The GROUP BY functions STD(), BIT_OR(), BIT_AND(), BIT_XOR(), and GROUP_CONCAT().

See Section 14.19, “Aggregate Functions”.

1.6.2 MySQL Differences from Standard SQL

We try to make MySQL Server follow the ANSI SQL standard and the ODBC SQL standard, but
MySQL Server performs operations differently in some cases:

• There are several differences between the MySQL and standard SQL privilege systems. For

example, in MySQL, privileges for a table are not automatically revoked when you delete a table.
You must explicitly issue a REVOKE statement to revoke privileges for a table. For more information,
see Section 15.7.1.8, “REVOKE Statement”.

• The CAST() function does not support cast to REAL or BIGINT. See Section 14.10, “Cast Functions

and Operators”.

1.6.2.1 SELECT INTO TABLE Differences

MySQL Server doesn't support the SELECT ... INTO TABLE Sybase SQL extension. Instead,
MySQL Server supports the INSERT INTO ... SELECT standard SQL syntax, which is basically the
same thing. See Section 15.2.7.1, “INSERT ... SELECT Statement”. For example:

INSERT INTO tbl_temp2 (fld_id)
    SELECT tbl_temp1.fld_order_id
    FROM tbl_temp1 WHERE tbl_temp1.fld_order_id > 100;

Alternatively, you can use SELECT ... INTO OUTFILE or CREATE TABLE ... SELECT.

You can use SELECT ... INTO with user-defined variables. The same syntax can also be used
inside stored routines using cursors and local variables. See Section 15.2.13.1, “SELECT ... INTO
Statement”.

1.6.2.2 UPDATE Differences

If you access a column from the table to be updated in an expression, UPDATE uses the current value
of the column. The second assignment in the following statement sets col2 to the current (updated)
col1 value, not the original col1 value. The result is that col1 and col2 have the same value. This
behavior differs from standard SQL.

UPDATE t1 SET col1 = col1 + 1, col2 = col1;

1.6.2.3 FOREIGN KEY Constraint Differences

The MySQL implementation of foreign key constraints differs from the SQL standard in the following
key respects:

• If there are several rows in the parent table with the same referenced key value, InnoDB performs

a foreign key check as if the other parent rows with the same key value do not exist. For example, if
you define a RESTRICT type constraint, and there is a child row with several parent rows, InnoDB
does not permit the deletion of any of the parent rows.

• If ON UPDATE CASCADE or ON UPDATE SET NULL recurses to update the same table it has

previously updated during the same cascade, it acts like RESTRICT. This means that you cannot
use self-referential ON UPDATE CASCADE or ON UPDATE SET NULL operations. This is to prevent
infinite loops resulting from cascaded updates. A self-referential ON DELETE SET NULL, on the

98

MySQL Differences from Standard SQL

other hand, is possible, as is a self-referential ON DELETE CASCADE. Cascading operations may not
be nested more than 15 levels deep.

• In an SQL statement that inserts, deletes, or updates many rows, foreign key constraints (like unique
constraints) are checked row-by-row. When performing foreign key checks, InnoDB sets shared row-
level locks on child or parent records that it must examine. MySQL checks foreign key constraints
immediately; the check is not deferred to transaction commit. According to the SQL standard, the
default behavior should be deferred checking. That is, constraints are only checked after the entire
SQL statement has been processed. This means that it is not possible to delete a row that refers to
itself using a foreign key.

• No storage engine, including InnoDB, recognizes or enforces the MATCH clause used in referential-
integrity constraint definitions. Use of an explicit MATCH clause does not have the specified effect,
and it causes ON DELETE and ON UPDATE clauses to be ignored. Specifying the MATCH should be
avoided.

The MATCH clause in the SQL standard controls how NULL values in a composite (multiple-column)
foreign key are handled when comparing to a primary key in the referenced table. MySQL essentially
implements the semantics defined by MATCH SIMPLE, which permits a foreign key to be all or
partially NULL. In that case, a (child table) row containing such a foreign key can be inserted even
though it does not match any row in the referenced (parent) table. (It is possible to implement other
semantics using triggers.)

• MySQL requires that the referenced columns be indexed for performance reasons. However, MySQL
does not enforce a requirement that the referenced columns be UNIQUE or be declared NOT NULL.

A FOREIGN KEY constraint that references a non-UNIQUE key is not standard SQL but rather an
InnoDB extension. The NDB storage engine, on the other hand, requires an explicit unique key (or
primary key) on any column referenced as a foreign key.

The handling of foreign key references to nonunique keys or keys that contain NULL values is not
well defined for operations such as UPDATE or DELETE CASCADE. You are advised to use foreign
keys that reference only UNIQUE (including PRIMARY) and NOT NULL keys.

• For storage engines that do not support foreign keys (such as MyISAM), MySQL Server parses and

ignores foreign key specifications.

• MySQL parses but ignores “inline REFERENCES specifications” (as defined in the SQL standard)

where the references are defined as part of the column specification. MySQL accepts REFERENCES
clauses only when specified as part of a separate FOREIGN KEY specification.

Defining a column to use a REFERENCES tbl_name(col_name) clause has no actual effect
and serves only as a memo or comment to you that the column which you are currently defining is
intended to refer to a column in another table. It is important to realize when using this syntax that:

• MySQL does not perform any sort of check to make sure that col_name actually exists in

tbl_name (or even that tbl_name itself exists).

• MySQL does not perform any sort of action on tbl_name such as deleting rows in response to
actions taken on rows in the table which you are defining; in other words, this syntax induces no
ON DELETE or ON UPDATE behavior whatsoever. (Although you can write an ON DELETE or ON
UPDATE clause as part of the REFERENCES clause, it is also ignored.)

• This syntax creates a column; it does not create any sort of index or key.

You can use a column so created as a join column, as shown here:

CREATE TABLE person (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name CHAR(60) NOT NULL,
    PRIMARY KEY (id)
);

99

MySQL Differences from Standard SQL

CREATE TABLE shirt (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    style ENUM('t-shirt', 'polo', 'dress') NOT NULL,
    color ENUM('red', 'blue', 'orange', 'white', 'black') NOT NULL,
    owner SMALLINT UNSIGNED NOT NULL REFERENCES person(id),
    PRIMARY KEY (id)
);

INSERT INTO person VALUES (NULL, 'Antonio Paz');

SELECT @last := LAST_INSERT_ID();

INSERT INTO shirt VALUES
(NULL, 'polo', 'blue', @last),
(NULL, 'dress', 'white', @last),
(NULL, 't-shirt', 'blue', @last);

INSERT INTO person VALUES (NULL, 'Lilliana Angelovska');

SELECT @last := LAST_INSERT_ID();

INSERT INTO shirt VALUES
(NULL, 'dress', 'orange', @last),
(NULL, 'polo', 'red', @last),
(NULL, 'dress', 'blue', @last),
(NULL, 't-shirt', 'white', @last);

SELECT * FROM person;
+----+---------------------+
| id | name                |
+----+---------------------+
|  1 | Antonio Paz         |
|  2 | Lilliana Angelovska |
+----+---------------------+

SELECT * FROM shirt;
+----+---------+--------+-------+
| id | style   | color  | owner |
+----+---------+--------+-------+
|  1 | polo    | blue   |     1 |
|  2 | dress   | white  |     1 |
|  3 | t-shirt | blue   |     1 |
|  4 | dress   | orange |     2 |
|  5 | polo    | red    |     2 |
|  6 | dress   | blue   |     2 |
|  7 | t-shirt | white  |     2 |
+----+---------+--------+-------+

SELECT s.* FROM person p INNER JOIN shirt s
   ON s.owner = p.id
 WHERE p.name LIKE 'Lilliana%'
   AND s.color <> 'white';

+----+-------+--------+-------+
| id | style | color  | owner |
+----+-------+--------+-------+
|  4 | dress | orange |     2 |
|  5 | polo  | red    |     2 |
|  6 | dress | blue   |     2 |
+----+-------+--------+-------+

When used in this fashion, the REFERENCES clause is not displayed in the output of SHOW CREATE
TABLE or DESCRIBE:

SHOW CREATE TABLE shirt\G
*************************** 1. row ***************************
Table: shirt
Create Table: CREATE TABLE `shirt` (
`id` smallint(5) unsigned NOT NULL auto_increment,
`style` enum('t-shirt','polo','dress') NOT NULL,

100

How MySQL Deals with Constraints

`color` enum('red','blue','orange','white','black') NOT NULL,
`owner` smallint(5) unsigned NOT NULL,
PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

For information about foreign key constraints, see Section 15.1.20.5, “FOREIGN KEY Constraints”.

1.6.2.4 '--' as the Start of a Comment

Standard SQL uses the C syntax /* this is a comment */ for comments, and MySQL Server
supports this syntax as well. MySQL also support extensions to this syntax that enable MySQL-specific
SQL to be embedded in the comment; see Section 11.7, “Comments”.

MySQL Server also uses # as the start comment character. This is nonstandard.

Standard SQL also uses “--” as a start-comment sequence. MySQL Server supports a variant of the
-- comment style; the -- start-comment sequence is accepted as such, but must be followed by a
whitespace character such as a space or newline. The space is intended to prevent problems with
generated SQL queries that use constructs such as the following, which updates the balance to reflect
a charge:

UPDATE account SET balance=balance-charge
WHERE account_id=user_id

Consider what happens when charge has a negative value such as -1, which might be the case when
an amount is credited to the account. In this case, the generated statement looks like this:

UPDATE account SET balance=balance--1
WHERE account_id=5752;

balance--1 is valid standard SQL, but -- is interpreted as the start of a comment, and part of
the expression is discarded. The result is a statement that has a completely different meaning than
intended:

UPDATE account SET balance=balance
WHERE account_id=5752;

This statement produces no change in value at all. To keep this from happening, MySQL requires a
whitespace character following the -- for it to be recognized as a start-comment sequence in MySQL
Server, so that an expression such as balance--1 is always safe to use.

1.6.3 How MySQL Deals with Constraints

MySQL enables you to work both with transactional tables that permit rollback and with
nontransactional tables that do not. Because of this, constraint handling is a bit different in MySQL
than in other DBMSs. We must handle the case when you have inserted or updated a lot of rows in a
nontransactional table for which changes cannot be rolled back when an error occurs.

The basic philosophy is that MySQL Server tries to produce an error for anything that it can detect
while parsing a statement to be executed, and tries to recover from any errors that occur while
executing the statement. We do this in most cases, but not yet for all.

The options MySQL has when an error occurs are to stop the statement in the middle or to recover as
well as possible from the problem and continue. By default, the server follows the latter course. This
means, for example, that the server may coerce invalid values to the closest valid values.

Several SQL mode options are available to provide greater control over handling of bad data values
and whether to continue statement execution or abort when errors occur. Using these options, you
can configure MySQL Server to act in a more traditional fashion that is like other DBMSs that reject
improper input. The SQL mode can be set globally at server startup to affect all clients. Individual
clients can set the SQL mode at runtime, which enables each client to select the behavior most
appropriate for its requirements. See Section 7.1.11, “Server SQL Modes”.

101

How MySQL Deals with Constraints

The following sections describe how MySQL Server handles different types of constraints.

1.6.3.1 PRIMARY KEY and UNIQUE Index Constraints

Normally, errors occur for data-change statements (such as INSERT or UPDATE) that would violate
primary-key, unique-key, or foreign-key constraints. If you are using a transactional storage engine
such as InnoDB, MySQL automatically rolls back the statement. If you are using a nontransactional
storage engine, MySQL stops processing the statement at the row for which the error occurred and
leaves any remaining rows unprocessed.

MySQL supports an IGNORE keyword for INSERT, UPDATE, and so forth. If you use it, MySQL ignores
primary-key or unique-key violations and continues processing with the next row. See the section for
the statement that you are using (Section 15.2.7, “INSERT Statement”, Section 15.2.17, “UPDATE
Statement”, and so forth).

You can get information about the number of rows actually inserted or updated with the
mysql_info() C API function. You can also use the SHOW WARNINGS statement. See mysql_info(),
and Section 15.7.7.42, “SHOW WARNINGS Statement”.

InnoDB and NDB tables support foreign keys. See Section 1.6.3.2, “FOREIGN KEY Constraints”.

1.6.3.2 FOREIGN KEY Constraints

Foreign keys let you cross-reference related data across tables, and foreign key constraints help keep
this spread-out data consistent.

MySQL supports ON UPDATE and ON DELETE foreign key references in CREATE TABLE and ALTER
TABLE statements. The available referential actions are RESTRICT, CASCADE, SET NULL, and NO
ACTION (the default).

SET DEFAULT is also supported by the MySQL Server but is currently rejected as invalid by InnoDB.
Since MySQL does not support deferred constraint checking, NO ACTION is treated as RESTRICT.
For the exact syntax supported by MySQL for foreign keys, see Section 15.1.20.5, “FOREIGN KEY
Constraints”.

MATCH FULL, MATCH PARTIAL, and MATCH SIMPLE are allowed, but their use should be avoided,
as they cause the MySQL Server to ignore any ON DELETE or ON UPDATE clause used in the same
statement. MATCH options do not have any other effect in MySQL, which in effect enforces MATCH
SIMPLE semantics full-time.

MySQL requires that foreign key columns be indexed; if you create a table with a foreign key constraint
but no index on a given column, an index is created.

You can obtain information about foreign keys from the Information Schema KEY_COLUMN_USAGE
table. An example of a query against this table is shown here:

mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME
     > FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
     > WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
+--------------+---------------+-------------+-----------------+
| TABLE_SCHEMA | TABLE_NAME    | COLUMN_NAME | CONSTRAINT_NAME |
+--------------+---------------+-------------+-----------------+
| fk1          | myuser        | myuser_id   | f               |
| fk1          | product_order | customer_id | f2              |
| fk1          | product_order | product_id  | f1              |
+--------------+---------------+-------------+-----------------+
3 rows in set (0.01 sec)

Information about foreign keys on InnoDB tables can also be found in the INNODB_FOREIGN and
INNODB_FOREIGN_COLS tables, in the INFORMATION_SCHEMA database.

InnoDB and NDB tables support foreign keys.

102

How MySQL Deals with Constraints

1.6.3.3 Enforced Constraints on Invalid Data

By default, MySQL 8.0 rejects invalid or improper data values and aborts the statement in which they
occur. It is possible to alter this behavior to be more forgiving of invalid values, such that the server
coerces them to valid ones for data entry, by disabling strict SQL mode (see Section 7.1.11, “Server
SQL Modes”), but this is not recommended.

Older versions of MySQL employed the forgiving behavior by default; for a description of this behavior,
see Constraints on Invalid Data.

1.6.3.4 ENUM and SET Constraints

ENUM and SET columns provide an efficient way to define columns that can contain only a given set of
values. See Section 13.3.5, “The ENUM Type”, and Section 13.3.6, “The SET Type”.

Unless strict mode is disabled (not recommended, but see Section 7.1.11, “Server SQL Modes”), the
definition of a ENUM or SET column acts as a constraint on values entered into the column. An error
occurs for values that do not satisfy these conditions:

• An ENUM value must be one of those listed in the column definition, or the internal numeric equivalent
thereof. The value cannot be the error value (that is, 0 or the empty string). For a column defined as
ENUM('a','b','c'), values such as '', 'd', or 'ax' are invalid and are rejected.

• A SET value must be the empty string or a value consisting only of the values listed in the column

definition separated by commas. For a column defined as SET('a','b','c'), values such as 'd'
or 'a,b,c,d' are invalid and are rejected.

Errors for invalid values can be suppressed in strict mode if you use INSERT IGNORE or UPDATE
IGNORE. In this case, a warning is generated rather than an error. For ENUM, the value is inserted as
the error member (0). For SET, the value is inserted as given except that any invalid substrings are
deleted. For example, 'a,x,b,y' results in a value of 'a,b'.

103

104

