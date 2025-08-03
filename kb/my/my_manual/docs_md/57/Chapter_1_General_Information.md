About This Manual

• For a history of new features and bug fixes, see the Release Notes.

Important

To report problems or bugs, please use the instructions at Section 1.5,
“How to Report Bugs or Problems”. If you find a security bug in MySQL
Server, please let us know immediately by sending an email message to
<secalert_us@oracle.com>. Exception: Support customers should report all
problems, including security bugs, to Oracle Support.

1.1 About This Manual

This is the Reference Manual for the MySQL Database System, version 5.7, through release 5.7.44.
Differences between minor versions of MySQL 5.7 are noted in the present text with reference to release
numbers (5.7.x). For license information, see the Legal Notices.

This manual is not intended for use with older versions of the MySQL software due to the many functional
and other differences between MySQL 5.7 and previous versions. If you are using an earlier release of
the MySQL software, please refer to the appropriate manual. For example, MySQL 5.6 Reference Manual
covers the 5.6 series of MySQL software releases.

If you are using MySQL 8.0, please refer to the MySQL 8.0 Reference Manual.

Because this manual serves as a reference, it does not provide general instruction on SQL or relational
database concepts. It also does not teach you how to use your operating system or command-line
interpreter.

The MySQL Database Software is under constant development, and the Reference Manual is updated
frequently as well. The most recent version of the manual is available online in searchable form at https://
dev.mysql.com/doc/. Other formats also are available there, including downloadable HTML and PDF
versions.

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

• Text in this style is used for variable input for which you should substitute a value of your own

choosing.

• Text in this style is used for emphasis.

• Text in this style is used in table headings and to convey especially strong emphasis.

2

Typographical and Syntax Conventions

• Text in this style is used to indicate a program option that affects how the program is executed,

or that supplies information that is needed for the program to function in a certain way. Example: “The --
host option (short form -h) tells the mysql client program the hostname or IP address of the MySQL
server that it should connect to”.

• File names and directory names are written like this: “The global my.cnf file is located in the /etc

directory.”

• Character sequences are written like this: “To specify a wildcard, use the ‘%’ character.”

When commands or statements are prefixed by a prompt, we use these:

$> type a command here
#> type a command as root here
C:\> type a command here (Windows only)
mysql> type a mysql statement here

Commands are issued in your command interpreter. On Unix, this is typically a program such as sh, csh,
or bash. On Windows, the equivalent program is command.com or cmd.exe, typically run in a console
window. Statements prefixed by mysql are issued in the mysql command-line client.

Note

When you enter a command or statement shown in an example, do not type the
prompt shown in the example.

In some areas different systems may be distinguished from each other to show that commands should be
executed in two different environments. For example, while working with replication the commands might
be prefixed with source and replica:

source> type a mysql statement on the replication source here
replica> type a mysql statement on the replica here

Database, table, and column names must often be substituted into statements. To indicate that such
substitution is necessary, this manual uses db_name, tbl_name, and col_name. For example, you might
see a statement like this:

mysql> SELECT col_name FROM db_name.tbl_name;

This means that if you were to enter a similar statement, you would supply your own database, table, and
column names, perhaps like this:

mysql> SELECT author_name FROM biblio_db.author_list;

SQL keywords are not case-sensitive and may be written in any lettercase. This manual uses uppercase.

In syntax descriptions, square brackets (“[” and “]”) indicate optional words or clauses. For example, in the
following statement, IF EXISTS is optional:

DROP TABLE [IF EXISTS] tbl_name

When a syntax element consists of a number of alternatives, the alternatives are separated by vertical bars
(“|”). When one member from a set of choices may be chosen, the alternatives are listed within square
brackets (“[” and “]”):

TRIM([[BOTH | LEADING | TRAILING] [remstr] FROM] str)

When one member from a set of choices must be chosen, the alternatives are listed within braces (“{” and
“}”):

{DESCRIBE | DESC} tbl_name [col_name | wild]

3

Manual Authorship

An ellipsis (...) indicates the omission of a section of a statement, typically to provide a shorter version of
more complex syntax. For example, SELECT ... INTO OUTFILE is shorthand for the form of SELECT
statement that has an INTO OUTFILE clause following other parts of the statement.

An ellipsis can also indicate that the preceding syntax element of a statement may be repeated. In
the following example, multiple reset_option values may be given, with each of those after the first
preceded by commas:

RESET reset_option [,reset_option] ...

Commands for setting shell variables are shown using Bourne shell syntax. For example, the sequence to
set the CC environment variable and run the configure command looks like this in Bourne shell syntax:

$> CC=gcc ./configure

If you are using csh or tcsh, you must issue commands somewhat differently:

$> setenv CC gcc
$> ./configure

Manual Authorship

The Reference Manual source files are written in DocBook XML format. The HTML version and other
formats are produced automatically, primarily using the DocBook XSL stylesheets. For information about
DocBook, see http://docbook.org/

This manual was originally written by David Axmark and Michael “Monty” Widenius. It is maintained by the
MySQL Documentation Team, consisting of Edward Gilmore, Sudharsana Gomadam, Kim seong Loh,
Garima Sharma, Carlos Ortiz, Daniel So, and Jon Stephens.

1.2 Overview of the MySQL Database Management System

1.2.1 What is MySQL?

MySQL, the most popular Open Source SQL database management system, is developed, distributed, and
supported by Oracle Corporation.

The MySQL website (http://www.mysql.com/) provides the latest information about MySQL software.

• MySQL is a database management system.

A database is a structured collection of data. It may be anything from a simple shopping list to a picture
gallery or the vast amounts of information in a corporate network. To add, access, and process data
stored in a computer database, you need a database management system such as MySQL Server.
Since computers are very good at handling large amounts of data, database management systems play
a central role in computing, as standalone utilities, or as parts of other applications.

• MySQL databases are relational.

 A relational database stores data in separate tables rather than putting all the data in one big storeroom.
The database structures are organized into physical files optimized for speed. The logical model,
with objects such as databases, tables, views, rows, and columns, offers a flexible programming
environment. You set up rules governing the relationships between different data fields, such as one-to-
one, one-to-many, unique, required or optional, and “pointers” between different tables. The database
enforces these rules, so that with a well-designed database, your application never sees inconsistent,
duplicate, orphan, out-of-date, or missing data.

4

What is MySQL?

The SQL part of “MySQL” stands for “Structured Query Language”. SQL is the most common
standardized language used to access databases. Depending on your programming environment, you
might enter SQL directly (for example, to generate reports), embed SQL statements into code written in
another language, or use a language-specific API that hides the SQL syntax.

SQL is defined by the ANSI/ISO SQL Standard. The SQL standard has been evolving since 1986 and
several versions exist. In this manual, “SQL-92” refers to the standard released in 1992, “SQL:1999”
refers to the standard released in 1999, and “SQL:2003” refers to the current version of the standard. We
use the phrase “the SQL standard” to mean the current version of the SQL Standard at any time.

• MySQL software is Open Source.

    Open Source means that it is possible for anyone to use and modify the software. Anybody can
download the MySQL software from the Internet and use it without paying anything. If you wish, you
may study the source code and change it to suit your needs. The MySQL software uses the GPL (GNU
General Public License), http://www.fsf.org/licenses/, to define what you may and may not do with the
software in different situations. If you feel uncomfortable with the GPL or need to embed MySQL code
into a commercial application, you can buy a commercially licensed version from us. See the MySQL
Licensing Overview for more information (http://www.mysql.com/company/legal/licensing/).

• The MySQL Database Server is very fast, reliable, scalable, and easy to use.

If that is what you are looking for, you should give it a try. MySQL Server can run comfortably on a
desktop or laptop, alongside your other applications, web servers, and so on, requiring little or no
attention. If you dedicate an entire machine to MySQL, you can adjust the settings to take advantage
of all the memory, CPU power, and I/O capacity available. MySQL can also scale up to clusters of
machines, networked together.

MySQL Server was originally developed to handle large databases much faster than existing solutions
and has been successfully used in highly demanding production environments for several years.
Although under constant development, MySQL Server today offers a rich and useful set of functions.
Its connectivity, speed, and security make MySQL Server highly suited for accessing databases on the
Internet.

• MySQL Server works in client/server or embedded systems.

The MySQL Database Software is a client/server system that consists of a multithreaded SQL server
that supports different back ends, several different client programs and libraries, administrative tools, and
a wide range of application programming interfaces (APIs).

We also provide MySQL Server as an embedded multithreaded library that you can link into your
application to get a smaller, faster, easier-to-manage standalone product.

• A large amount of contributed MySQL software is available.

MySQL Server has a practical set of features developed in close cooperation with our users. It is very
likely that your favorite application or language supports the MySQL Database Server.

• HeatWave.

HeatWave is a fully managed database service, powered by the HeatWave in-memory query
accelerator. It is the only cloud service that combines transactions, real-time analytics across data
warehouses and data lakes, and machine learning in one MySQL Database; without the complexity,
latency, risks, and cost of ETL duplication. It is available on OCI, AWS, and Azure. Learn more at:
https://www.oracle.com/mysql/.

5

What Is New in MySQL 5.7

not fast enough or flexible enough for our needs. This resulted in a new SQL interface to our database but
with almost the same API interface as mSQL. This API was designed to enable third-party code that was
written for use with mSQL to be ported easily for use with MySQL.

MySQL is named after co-founder Monty Widenius's daughter, My.

The name of the MySQL Dolphin (our logo) is “Sakila,” which was chosen from a huge list of names
suggested by users in our “Name the Dolphin” contest. The winning name was submitted by Ambrose
Twebaze, an Open Source software developer from Eswatini (formerly Swaziland), Africa. According to
Ambrose, the feminine name Sakila has its roots in SiSwati, the local language of Eswatini. Sakila is also
the name of a town in Arusha, Tanzania, near Ambrose's country of origin, Uganda.

1.3 What Is New in MySQL 5.7

This section summarizes what has been added to, deprecated in, and removed from MySQL 5.7. A
companion section lists MySQL server options and variables that have been added, deprecated, or
removed in MySQL 5.7; see Section 1.4, “Server and Status Variables and Options Added, Deprecated, or
Removed in MySQL 5.7”.

• Features Added in MySQL 5.7

• Features Deprecated in MySQL 5.7

• Features Removed in MySQL 5.7

Features Added in MySQL 5.7

The following features have been added to MySQL 5.7:

• Security improvements.

 These security enhancements were added:

• In MySQL 8.0, caching_sha2_password is the default authentication plugin. To enable MySQL 5.7
clients to connect to 8.0 servers using accounts that authenticate using caching_sha2_password,
the MySQL 5.7 client library and client programs support the caching_sha2_password client-side
authentication plugin as of MySQL 5.7.23. This improves compatibility of MySQL 5.7 with MySQL 8.0
and higher servers. See Section 6.4.1.4, “Caching SHA-2 Pluggable Authentication”.

• The server now requires account rows in the mysql.user system table to have a nonempty plugin

column value and disables accounts with an empty value. For server upgrade instructions, see
Section 2.10.3, “Changes in MySQL 5.7”. DBAs are advised to also convert accounts that use the
mysql_old_password authentication plugin to use mysql_native_password instead, because
support for mysql_old_password has been removed. For account upgrade instructions, see
Section 6.4.1.3, “Migrating Away from Pre-4.1 Password Hashing and the mysql_old_password
Plugin”.

• MySQL now enables database administrators to establish a policy for automatic password

expiration: Any user who connects to the server using an account for which the password is past its
permitted lifetime must change the password. For more information, see Section 6.2.11, “Password
Management”.

• Administrators can lock and unlock accounts for better control over who can log in. For more

information, see Section 6.2.15, “Account Locking”.

• To make it easier to support secure connections, MySQL servers compiled using OpenSSL can

automatically generate missing SSL and RSA certificate and key files at startup. See Section 6.3.3.1,
“Creating SSL and RSA Certificates and Keys using MySQL”.

9

Features Added in MySQL 5.7

pages in each buffer pool to read out and dump. When there is other I/O activity being performed by
InnoDB background tasks, InnoDB attempts to limit the number of buffer pool load operations per
second using the innodb_io_capacity setting.

• Support is added to InnoDB for full-text parser plugins. For information about full-text parser plugins,

see Full-Text Parser Plugins and Writing Full-Text Parser Plugins.

• InnoDB supports multiple page cleaner threads for flushing dirty pages from buffer pool instances.
A new system variable, innodb_page_cleaners, is used to specify the number of page cleaner
threads. The default value of 1 maintains the previous configuration in which there is a single page
cleaner thread. This enhancement builds on work completed in MySQL 5.6, which introduced a single
page cleaner thread to offload buffer pool flushing work from the InnoDB master thread.

• Online DDL support is extended to the following operations for regular and partitioned InnoDB tables:

• OPTIMIZE TABLE

• ALTER TABLE ... FORCE

• ALTER TABLE ... ENGINE=INNODB (when run on an InnoDB table)

Online DDL support reduces table rebuild time and permits concurrent DML. See Section 14.13,
“InnoDB and Online DDL”.

• The Fusion-io Non-Volatile Memory (NVM) file system on Linux provides atomic write capability, which

makes the InnoDB doublewrite buffer redundant. The InnoDB doublewrite buffer is automatically
disabled for system tablespace files (ibdata files) located on Fusion-io devices that support atomic
writes.

• InnoDB supports the Transportable Tablespace feature for partitioned InnoDB tables and individual

InnoDB table partitions. This enhancement eases backup procedures for partitioned tables and
enables copying of partitioned tables and individual table partitions between MySQL instances. For
more information, see Section 14.6.1.3, “Importing InnoDB Tables”.

• The innodb_buffer_pool_size parameter is dynamic, allowing you to resize the buffer
pool without restarting the server. The resizing operation, which involves moving pages to a
new location in memory, is performed in chunks. Chunk size is configurable using the new
innodb_buffer_pool_chunk_size configuration option. You can monitor resizing progress
using the new Innodb_buffer_pool_resize_status status variable. For more information, see
Configuring InnoDB Buffer Pool Size Online.

• Multithreaded page cleaner support (innodb_page_cleaners) is extended to shutdown and

recovery phases.

• InnoDB supports indexing of spatial data types using SPATIAL indexes, including use of ALTER

TABLE ... ALGORITHM=INPLACE for online operations (ADD SPATIAL INDEX).

• InnoDB performs a bulk load when creating or rebuilding indexes. This method of index creation is
known as a “sorted index build”. This enhancement, which improves the efficiency of index creation,
also applies to full-text indexes. A new global configuration option, innodb_fill_factor, defines
the percentage of space on each page that is filled with data during a sorted index build, with the
remaining space reserved for future index growth. For more information, see Section 14.6.2.3, “Sorted
Index Builds”.

• A new log record type (MLOG_FILE_NAME) is used to identify tablespaces that have been modified
since the last checkpoint. This enhancement simplifies tablespace discovery during crash recovery

12

Features Deprecated in MySQL 5.7

following STOP SLAVE when statement-based replication is in use and Slave_open_temp_tables
remains greater than 0.

For more information, see Section 13.4.2.1, “CHANGE MASTER TO Statement”, and Section 16.3.7,
“Switching Sources During Failover”.

• Test suite.

 The MySQL test suite now uses InnoDB as the default storage engine.

• Multi-source replication is now possible.

 MySQL Multi-Source Replication adds the ability to

replicate from multiple sources to a replica. MySQL Multi-Source Replication topologies can be used to
back up multiple servers to a single server, to merge table shards, and consolidate data from multiple
servers to a single server. See Section 16.1.5, “MySQL Multi-Source Replication”.

As part of MySQL Multi-Source Replication, replication channels have been added. Replication channels
enable a replica to open multiple connections to replicate from, with each channel being a connection to
a source. See Section 16.2.2, “Replication Channels”.

• Group Replication Performance Schema tables.

 MySQL 5.7 adds a number of new tables to the
Performance Schema to provide information about replication groups and channels. These include the
following tables:

• replication_applier_configuration

• replication_applier_status

• replication_applier_status_by_coordinator

• replication_applier_status_by_worker

• replication_connection_configuration

• replication_connection_status

• replication_group_members

• replication_group_member_stats

All of these tables were added in MySQL 5.7.2, except for replication_group_members and
replication_group_member_stats, which were added in MySQL 5.7.6. For more information, see
Section 25.12.11, “Performance Schema Replication Tables”.

• Group Replication SQL.

 The following statements were added in MySQL 5.7.6 for controlling Group

Replication:

• START GROUP_REPLICATION

• STOP GROUP_REPLICATION

For more information, see Section 13.4.3, “SQL Statements for Controlling Group Replication”.

Features Deprecated in MySQL 5.7

The following features are deprecated in MySQL 5.7 and may be removed in a future series. Where
alternatives are shown, applications should be updated to use them.

For applications that use features deprecated in MySQL 5.7 that have been removed in a higher MySQL
series, statements may fail when replicated from a MySQL 5.7 source to a higher-series replica, or may

18

Features Deprecated in MySQL 5.7

have different effects on source and replica. To avoid such problems, applications that use features
deprecated in 5.7 should be revised to avoid them and use alternatives when possible.

• The ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE SQL modes are now
deprecated but enabled by default. The long term plan is to have them included in strict SQL mode and
to remove them as explicit modes in a future MySQL release.

The deprecated ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE SQL
modes are still recognized so that statements that name them do not produce an error, but are expected
to be removed in a future version of MySQL. To make advance preparation for versions of MySQL in
which these mode names do not exist, applications should be modified not to refer to them. See SQL
Mode Changes in MySQL 5.7.

• These SQL modes are now deprecated; expect them to be removed in a future version of MySQL:

DB2, MAXDB, MSSQL, MYSQL323, MYSQL40, ORACLE, POSTGRESQL, NO_FIELD_OPTIONS,
NO_KEY_OPTIONS, NO_TABLE_OPTIONS. These deprecations have two implications:

• Assigning a deprecated mode to the sql_mode system variable produces a warning.

• With the MAXDB SQL mode enabled, using CREATE TABLE or ALTER TABLE to add a TIMESTAMP

column to a table produces a warning.

• Changes to account-management statements make the following features obsolete. They are now

deprecated:

• Using GRANT to create users. Instead, use CREATE USER. Following this practice makes the

NO_AUTO_CREATE_USER SQL mode immaterial for GRANT statements, so it too is deprecated.

• Using GRANT to modify account properties other than privilege assignments. This includes

authentication, SSL, and resource-limit properties. Instead, establish such properties at account-
creation time with CREATE USER or modify them afterward with ALTER USER.

• IDENTIFIED BY PASSWORD 'auth_string' syntax for CREATE USER and GRANT. Instead, use
IDENTIFIED WITH auth_plugin AS 'auth_string' for CREATE USER and ALTER USER,
where the 'auth_string' value is in a format compatible with the named plugin.

• The PASSWORD() function is deprecated and should be avoided in any context. Thus, SET

PASSWORD ... = PASSWORD('auth_string') syntax is also deprecated. SET PASSWORD ...
= 'auth_string' syntax is not deprecated; nevertheless, ALTER USER is now the preferred
statement for assigning passwords.

• The old_passwords system variable. Account authentication plugins can no longer be left

unspecified in the mysql.user system table, so any statement that assigns a password from a
cleartext string can unambiguously determine the hashing method to use on the string before storing it
in the mysql.user table. This renders old_passwords superflous.

19

Features Deprecated in MySQL 5.7

• The query cache is deprecated. Deprecation includes these items:

• The FLUSH QUERY CACHE and RESET QUERY CACHE statements.

• The SQL_CACHE and SQL_NO_CACHE SELECT modifiers.

• These system variables: have_query_cache, ndb_cache_check_time, query_cache_limit,

query_cache_min_res_unit, query_cache_size, query_cache_type,
query_cache_wlock_invalidate.

• These status variables: Qcache_free_blocks, Qcache_free_memory,

Qcache_hits, Qcache_inserts, Qcache_lowmem_prunes, Qcache_not_cached,
Qcache_queries_in_cache, Qcache_total_blocks.

• Previously, the --transaction-isolation and --transaction-read-only server startup

options corresponded to the tx_isolation and tx_read_only system variables. For better name
correspondence between startup option and system variable names, transaction_isolation and
transaction_read_only have been created as aliases for tx_isolation and tx_read_only.
The tx_isolation and tx_read_only variables are now deprecated;expect them to be
removed in MySQL 8.0. Applications should be adjusted to use transaction_isolation and
transaction_read_only instead.

• The --skip-innodb option and its synonyms (--innodb=OFF, --disable-innodb, and so forth)
are deprecated. These options have no effect as of MySQL 5.7. because InnoDB cannot be disabled.

• The client-side --ssl and --ssl-verify-server-cert options are deprecated. Use --ssl-

mode=REQUIRED instead of --ssl=1 or --enable-ssl. Use --ssl-mode=DISABLED instead of --
ssl=0, --skip-ssl, or --disable-ssl. Use --ssl-mode=VERIFY_IDENTITY instead of --ssl-
verify-server-cert options. (The server-side --ssl option is not deprecated.)

For the C API, MYSQL_OPT_SSL_ENFORCE and MYSQL_OPT_SSL_VERIFY_SERVER_CERT options for
mysql_options() correspond to the client-side --ssl and --ssl-verify-server-cert options
and are deprecated. Use MYSQL_OPT_SSL_MODE with an option value of SSL_MODE_REQUIRED or
SSL_MODE_VERIFY_IDENTITY instead.

• The log_warnings system variable and --log-warnings server option are deprecated. Use the

log_error_verbosity system variable instead.

• The --temp-pool server option is deprecated.

• The binlog_max_flush_queue_time system variable does nothing in MySQL 5.7, and is deprecated

as of MySQL 5.7.9.

• The innodb_support_xa system variable, which enables InnoDB support for two-phase commit
in XA transactions, is deprecated as of MySQL 5.7.10. InnoDB support for two-phase commit in XA
transactions is always enabled as of MySQL 5.7.10.

• The metadata_locks_cache_size and metadata_locks_hash_instances system variables are

deprecated. These do nothing as of MySQL 5.7.4.

• The sync_frm system variable is deprecated.

• The global character_set_database and collation_database system variables are deprecated;

expect them to be removed in a future version of MySQL.

Assigning a value to the session character_set_database and collation_database system
variables is deprecated and assignments produce a warning. The session variables are expected to

20

Features Deprecated in MySQL 5.7

become read only in a future version of MySQL, and assignments to them to produce an error, while
remaining possible to read the session variables to determine the database character set and collation
for the default database.

• The global scope for the sql_log_bin system variable has been deprecated, and this variable can now
be set with session scope only. The statement SET GLOBAL SQL_LOG_BIN now produces an error.
It remains possible to read the global value of sql_log_bin, but doing so produces a warning. You
should act now to remove from your applications any dependencies on reading this value; the global
scope sql_log_bin is removed in MySQL 8.0.

• With the introduction of the data dictionary in MySQL 8.0, the --ignore-db-dir option and
ignore_db_dirs system variable became superfluous and were removed in that version.
Consequently, they are deprecated in MySQL 5.7.

• GROUP BY implicitly sorts by default (that is, in the absence of ASC or DESC designators), but relying

on implicit GROUP BY sorting in MySQL 5.7 is deprecated. To achieve a specific sort order of grouped
results, it is preferable to use To produce a given sort order, use explicit ASC or DESC designators for
GROUP BY columns or provide an ORDER BY clause. GROUP BY sorting is a MySQL extension that
may change in a future release; for example, to make it possible for the optimizer to order groupings in
whatever manner it deems most efficient and to avoid the sorting overhead.

• The EXTENDED and PARTITIONS keywords for the EXPLAIN statement are deprecated. These
keywords are still recognized but are now unnecessary because their effect is always enabled.

• The ENCRYPT(), ENCODE(), DECODE(), DES_ENCRYPT(), and DES_DECRYPT() encryption functions
are deprecated. For ENCRYPT(), consider using SHA2() instead for one-way hashing. For the others,
consider using AES_ENCRYPT() and AES_DECRYPT() instead. The --des-key-file option,
the have_crypt system variable, the DES_KEY_FILE option for the FLUSH statement, and the
HAVE_CRYPT CMake option also are deprecated.

• The MBREqual() spatial function is deprecated. Use MBREquals() instead.

• The functions described in Section 12.16.4, “Functions That Create Geometry Values from WKB

Values” previously accepted either WKB strings or geometry arguments. Use of geometry arguments is
deprecated. See that section for guidelines for migrating queries away from using geometry arguments.

• The INFORMATION_SCHEMA PROFILING table is deprecated. Use the Performance Schema instead;

see Chapter 25, MySQL Performance Schema.

• The INFORMATION_SCHEMA INNODB_LOCKS and INNODB_LOCK_WAITS tables are deprecated, to be

removed in MySQL 8.0, which provides replacement Performance Schema tables.

• The Performance Schema setup_timers table is deprecated and is removed in MySQL 8.0, as is the

TICK row in the performance_timers table.

• The sys schema sys.version view is deprecated; expect it be removed in a future version of MySQL.
Affected applications should be adjusted to use an alternative instead. For example, use the VERSION()
function to retrieve the MySQL server version.

• Treatment of \N as a synonym for NULL in SQL statements is deprecated and is removed in MySQL 8.0;

use NULL instead.

This change does not affect text file import or export operations performed with LOAD DATA or
SELECT ... INTO OUTFILE, for which NULL continues to be represented by \N. See Section 13.2.6,
“LOAD DATA Statement”.

• PROCEDURE ANALYSE() syntax is deprecated.

21

Features Deprecated in MySQL 5.7

• Comment stripping by the mysql client and the options to control it (--skip-comments, --comments)

are deprecated.

• mysqld_safe support for syslog output is deprecated. Use the native server syslog support used

instead. See Section 5.4.2, “The Error Log”.

• Conversion of pre-MySQL 5.1 database names containing special characters to 5.1 format with the
addition of a #mysql50# prefix is deprecated. Because of this, the --fix-db-names and --fix-
table-names options for mysqlcheck and the UPGRADE DATA DIRECTORY NAME clause for the
ALTER DATABASE statement are also deprecated.

Upgrades are supported only from one release series to another (for example, 5.0 to 5.1, or 5.1 to 5.5),
so there should be little remaining need for conversion of older 5.0 database names to current versions
of MySQL. As a workaround, upgrade a MySQL 5.0 installation to MySQL 5.1 before upgrading to a
more recent release.

• mysql_install_db functionality has been integrated into the MySQL server, mysqld. To use this
capability to initialize a MySQL installation, if you previously invoked mysql_install_db manually,
invoke mysqld with the --initialize or --initialize-insecure option, depending on whether
you want the server to generate a random password for the initial 'root'@'localhost' account.

mysql_install_db is now deprecated, as is the special --bootstrap option that
mysql_install_db passes to mysqld.

• The mysql_plugin utility is deprecated. Alternatives include loading plugins at server startup using
the --plugin-load or --plugin-load-add option, or at runtime using the INSTALL PLUGIN
statement.

• The resolveip utility is deprecated. nslookup, host, or dig can be used instead.

• The resolve_stack_dump utility is deprecated. Stack traces from official MySQL builds are always

symbolized, so there is no need to use resolve_stack_dump.

• The mysql_kill(), mysql_list_fields(), mysql_list_processes(), and

mysql_refresh() C API functions are deprecated. The same is true of the corresponding
COM_PROCESS_KILL, COM_FIELD_LIST, COM_PROCESS_INFO, and COM_REFRESH client/server
protocol commands. Instead, use mysql_query() to execute a KILL, SHOW COLUMNS, SHOW
PROCESSLIST, or FLUSH statement, respectively.

• The mysql_shutdown() C API function is deprecated. Instead, use mysql_query() to execute a

SHUTDOWN statement.

• The libmysqld embedded server library is deprecated as of MySQL 5.7.19. These are also

deprecated:

• The mysql_config --libmysqld-libs, --embedded-libs, and --embedded options

• The CMake WITH_EMBEDDED_SERVER, WITH_EMBEDDED_SHARED_LIBRARY, and

INSTALL_SECURE_FILE_PRIV_EMBEDDEDDIR options

• The (undocumented) mysql --server-arg option

• The mysqltest --embedded-server, --server-arg, and --server-file options

• The mysqltest_embedded and mysql_client_test_embedded test programs

Because libmysqld uses an API comparable to that of libmysqlclient, the migration path away
from libmysqld is straightforward:

22

Features Removed in MySQL 5.7

1. Bring up a standalone MySQL server (mysqld).

2. Modify application code to remove API calls that are specific to libmysqld.

3. Modify application code to connect to the standalone MySQL server.

4. Modify build scripts to use libmysqlclient rather than libmysqld. For example, if you use

mysql_config, invoke it with the --libs option rather than --libmysqld-libs.

• The replace utility is deprecated.

• Support for DTrace is deprecated.

• The JSON_MERGE() function is deprecated as of MySQL 5.7.22. Use JSON_MERGE_PRESERVE()

instead.

• Support for placing table partitions in shared InnoDB tablespaces is deprecated as of MySQL 5.7.24.
Shared tablespaces include the InnoDB system tablespace and general tablespaces. For information
about identifying partitions in shared tablespaces and moving them to file-per-table tablespaces, see
Preparing Your Installation for Upgrade.

• Support for TABLESPACE = innodb_file_per_table and TABLESPACE = innodb_temporary

clauses with CREATE TEMPORARY TABLE is deprecated as of MySQL 5.7.24.

• The --ndb perror option is deprecated. Use the ndb_perror utility instead.

• The myisam_repair_threads system variable myisam_repair_threads are deprecated as of

MySQL 5.7.38; expect support for both to be removed in a future release of MySQL.

From MySQL 5.7.38, values other than 1 (the default) for myisam_repair_threads produce a
warning.

Features Removed in MySQL 5.7

The following items are obsolete and have been removed in MySQL 5.7. Where alternatives are shown,
applications should be updated to use them.

For MySQL 5.6 applications that use features removed in MySQL 5.7, statements may fail when replicated
from a MySQL 5.6 source to a MySQL 5.7 replica, or may have different effects on source and replica. To
avoid such problems, applications that use features removed in MySQL 5.7 should be revised to avoid
them and use alternatives when possible.

• Support for passwords that use the older pre-4.1 password hashing format is removed, which involves

the following changes. Applications that use any feature no longer supported must be modified.

• The mysql_old_password authentication plugin is removed. Accounts that use this plugin

are disabled at startup and the server writes an “unknown plugin” message to the error log. For
instructions on upgrading accounts that use this plugin, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• The --secure-auth option to the server and client programs is the default, but is now a no-op. It is

deprecated; expect it to be removed in a future MySQL release.

• The --skip-secure-auth option to the server and client programs is no longer supported and

using it produces an error.

• The secure_auth system variable permits only a value of 1; a value of 0 is no longer permitted.

23

Features Removed in MySQL 5.7

• For the old_passwords system variable, a value of 1 (produce pre-4.1 hashes) is no longer

permitted.

• The OLD_PASSWORD() function is removed.

• In MySQL 5.6.6, the 2-digit YEAR(2) data type was deprecated. Support for YEAR(2) is now

removed. Once you upgrade to MySQL 5.7.5 or higher, any remaining 2-digit YEAR(2) columns
must be converted to 4-digit YEAR columns to become usable again. For conversion strategies,
see Section 11.2.5, “2-Digit YEAR(2) Limitations and Migrating to 4-Digit YEAR”. For example, run
mysql_upgrade after upgrading.

• The innodb_mirrored_log_groups system variable. The only supported value was 1, so it had no

purpose.

• The storage_engine system variable. Use default_storage_engine instead.

• The thread_concurrency system variable.

• The timed_mutexes system variable, which had no effect.

• The IGNORE clause for ALTER TABLE.

• INSERT DELAYED is no longer supported. The server recognizes but ignores the DELAYED keyword,

handles the insert as a nondelayed insert, and generates an ER_WARN_LEGACY_SYNTAX_CONVERTED
warning. (“INSERT DELAYED is no longer supported. The statement was converted to INSERT.”)
Similarly, REPLACE DELAYED is handled as a nondelayed replace. You should expect the DELAYED
keyword to be removed in a future release.

In addition, several DELAYED-related options or features were removed:

• The --delayed-insert option for mysqldump.

• The COUNT_WRITE_DELAYED, SUM_TIMER_WRITE_DELAYED, MIN_TIMER_WRITE_DELAYED,
AVG_TIMER_WRITE_DELAYED, and MAX_TIMER_WRITE_DELAYED columns of the Performance
Schema table_lock_waits_summary_by_table table.

• mysqlbinlog no longer writes comments mentioning INSERT DELAYED.

• Database symlinking on Windows using .sym files has been removed because it is redundant with

native symlink support available using mklink. Any .sym file symbolic links are now ignored and should
be replaced with symlinks created using mklink. See Section 8.12.3.3, “Using Symbolic Links for
Databases on Windows”.

• The unused --basedir, --datadir, and --tmpdir options for mysql_upgrade were removed.

• Previously, program options could be specified in full or as any unambiguous prefix. For example, the

--compress option could be given to mysqldump as --compr, but not as --comp because the latter
is ambiguous. Option prefixes are no longer supported; only full options are accepted. This is because
prefixes can cause problems when new options are implemented for programs and a prefix that is
currently unambiguous might become ambiguous in the future. Some implications of this change:

• The --key-buffer option must now be specified as --key-buffer-size.

• The --skip-grant option must now be specified as --skip-grant-tables.

• SHOW ENGINE INNODB MUTEX output is removed. Comparable information can be generated by

creating views on Performance Schema tables.

24

Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 5.7

• The InnoDB Tablespace Monitor and InnoDB Table Monitor are removed. For the Table Monitor,

equivalent information can be obtained from InnoDB INFORMATION_SCHEMA tables.

• The specially named tables used to enable and disable the standard InnoDB Monitor and InnoDB Lock
Monitor (innodb_monitor and innodb_lock_monitor) are removed and replaced by two dynamic
system variables: innodb_status_output and innodb_status_output_locks. For additional
information, see Section 14.18, “InnoDB Monitors”.

• The innodb_use_sys_malloc and innodb_additional_mem_pool_size system variables,

deprecated in MySQL 5.6.3, were removed.

• The msql2mysql, mysql_convert_table_format, mysql_find_rows,

mysql_fix_extensions, mysql_setpermission, mysql_waitpid, mysql_zap, mysqlaccess,
and mysqlbug utilities.

• The mysqlhotcopy utility. Alternatives include mysqldump and MySQL Enterprise Backup.

• The binary-configure.sh script.

• The INNODB_PAGE_ATOMIC_REF_COUNT CMake option is removed.

• The innodb_create_intrinsic option is removed.

• The innodb_optimize_point_storage option and related internal data types (DATA_POINT and

DATA_VAR_POINT) are removed.

• The innodb_log_checksum_algorithm option is removed.

• The myisam_repair_threads system variable as of MySQL 5.7.39.

1.4 Server and Status Variables and Options Added, Deprecated, or
Removed in MySQL 5.7

• Options and Variables Introduced in MySQL 5.7

• Options and Variables Deprecated in MySQL 5.7

• Options and Variables Removed in MySQL 5.7

This section lists server variables, status variables, and options that were added for the first time, have
been deprecated, or have been removed in MySQL 5.7.

Options and Variables Introduced in MySQL 5.7

The following system variables, status variables, and server options have been added in MySQL 5.7.

• Audit_log_current_size: Audit log file current size. Added in MySQL 5.7.9.

• Audit_log_event_max_drop_size: Size of largest dropped audited event. Added in MySQL 5.7.9.

• Audit_log_events: Number of handled audited events. Added in MySQL 5.7.9.

• Audit_log_events_filtered: Number of filtered audited events. Added in MySQL 5.7.9.

• Audit_log_events_lost: Number of dropped audited events. Added in MySQL 5.7.9.

• Audit_log_events_written: Number of written audited events. Added in MySQL 5.7.9.

• Audit_log_total_size: Combined size of written audited events. Added in MySQL 5.7.9.

25

Options and Variables Introduced in MySQL 5.7

• Audit_log_write_waits: Number of write-delayed audited events. Added in MySQL 5.7.9.

• Com_change_repl_filter: Count of CHANGE REPLICATION FILTER statements. Added in MySQL

5.7.3.

• Com_explain_other: Count of EXPLAIN FOR CONNECTION statements. Added in MySQL 5.7.2.

• Com_group_replication_start: Count of START GROUP_REPLICATION statements. Added in

MySQL 5.7.6.

• Com_group_replication_stop: Count of STOP GROUP_REPLICATION statements. Added in

MySQL 5.7.6.

• Com_show_create_user: Count of SHOW CREATE USER statements. Added in MySQL 5.7.6.

• Com_show_slave_status_nonblocking: Count of SHOW REPLICA | SLAVE STATUS

NONBLOCKING statements. Added in MySQL 5.7.0.

• Com_shutdown: Count of SHUTDOWN statements. Added in MySQL 5.7.9.

• Connection_control_delay_generated: How many times server delayed connection request.

Added in MySQL 5.7.17.

• Firewall_access_denied: Number of statements rejected by MySQL Enterprise Firewall plugin.

Added in MySQL 5.7.9.

• Firewall_access_granted: Number of statements accepted by MySQL Enterprise Firewall plugin.

Added in MySQL 5.7.9.

• Firewall_cached_entries: Number of statements recorded by MySQL Enterprise Firewall plugin.

Added in MySQL 5.7.9.

• Innodb_buffer_pool_resize_status: Status of dynamic buffer pool resizing operation. Added in

MySQL 5.7.5.

• Locked_connects: Number of attempts to connect to locked accounts. Added in MySQL 5.7.6.

• Max_execution_time_exceeded: Number of statements that exceeded execution timeout value.

Added in MySQL 5.7.8.

• Max_execution_time_set: Number of statements for which execution timeout was set. Added in

MySQL 5.7.8.

• Max_execution_time_set_failed: Number of statements for which execution timeout setting failed.

Added in MySQL 5.7.8.

• Max_statement_time_exceeded: Number of statements that exceeded execution timeout value.

Added in MySQL 5.7.4.

• Max_statement_time_set: Number of statements for which execution timeout was set. Added in

MySQL 5.7.4.

• Max_statement_time_set_failed: Number of statements for which execution timeout setting failed.

Added in MySQL 5.7.4.

• Max_used_connections_time: Time at which Max_used_connections reached its current value.

Added in MySQL 5.7.5.

• Performance_schema_index_stat_lost: Number of indexes for which statistics were lost. Added

in MySQL 5.7.6.

26

Options and Variables Introduced in MySQL 5.7

• Performance_schema_memory_classes_lost: How many memory instruments could not be

loaded. Added in MySQL 5.7.2.

• Performance_schema_metadata_lock_lost: Number of metadata locks that could not be

recorded. Added in MySQL 5.7.3.

• Performance_schema_nested_statement_lost: Number of stored program statements for which

statistics were lost. Added in MySQL 5.7.2.

• Performance_schema_prepared_statements_lost: Number of prepared statements that could

not be instrumented. Added in MySQL 5.7.4.

• Performance_schema_program_lost: Number of stored programs for which statistics were lost.

Added in MySQL 5.7.2.

• Performance_schema_table_lock_stat_lost: Number of tables for which lock statistics were

lost. Added in MySQL 5.7.6.

• Rewriter_number_loaded_rules: Number of rewrite rules successfully loaded into memory. Added

in MySQL 5.7.6.

• Rewriter_number_reloads: Number of reloads of rules table into memory. Added in MySQL 5.7.6.

• Rewriter_number_rewritten_queries: Number of queries rewritten since plugin was loaded.

Added in MySQL 5.7.6.

• Rewriter_reload_error: Whether error occurred when last loading rewriting rules into memory.

Added in MySQL 5.7.6.

• audit-log: Whether to activate audit log plugin. Added in MySQL 5.7.9.

• audit_log_buffer_size: Size of audit log buffer. Added in MySQL 5.7.9.

• audit_log_compression: Audit log file compression method. Added in MySQL 5.7.21.

• audit_log_connection_policy: Audit logging policy for connection-related events. Added in

MySQL 5.7.9.

• audit_log_current_session: Whether to audit current session. Added in MySQL 5.7.9.

• audit_log_disable: Whether to disable the audit log. Added in MySQL 5.7.37.

• audit_log_encryption: Audit log file encryption method. Added in MySQL 5.7.21.

• audit_log_exclude_accounts: Accounts not to audit. Added in MySQL 5.7.9.

• audit_log_file: Name of audit log file. Added in MySQL 5.7.9.

• audit_log_filter_id: ID of current audit log filter. Added in MySQL 5.7.13.

• audit_log_flush: Close and reopen audit log file. Added in MySQL 5.7.9.

• audit_log_format: Audit log file format. Added in MySQL 5.7.9.

• audit_log_format_unix_timestamp: Whether to include Unix timestamp in JSON-format audit log.

Added in MySQL 5.7.35.

• audit_log_include_accounts: Accounts to audit. Added in MySQL 5.7.9.

• audit_log_policy: Audit logging policy. Added in MySQL 5.7.9.

• audit_log_read_buffer_size: Audit log file read buffer size. Added in MySQL 5.7.21.

27

Options and Variables Introduced in MySQL 5.7

• audit_log_rotate_on_size: Close and reopen audit log file at this size. Added in MySQL 5.7.9.

• audit_log_statement_policy: Audit logging policy for statement-related events. Added in MySQL

5.7.9.

• audit_log_strategy: Audit logging strategy. Added in MySQL 5.7.9.

• authentication_ldap_sasl_auth_method_name: Authentication method name. Added in MySQL

5.7.19.

• authentication_ldap_sasl_bind_base_dn: LDAP server base distinguished name. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_bind_root_dn: LDAP server root distinguished name. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_bind_root_pwd: LDAP server root bind password. Added in MySQL

5.7.19.

• authentication_ldap_sasl_ca_path: LDAP server certificate authority file name. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_group_search_attr: LDAP server group search attribute. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_group_search_filter: LDAP custom group search filter. Added in

MySQL 5.7.21.

• authentication_ldap_sasl_init_pool_size: LDAP server initial connection pool size. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_log_status: LDAP server log level. Added in MySQL 5.7.19.

• authentication_ldap_sasl_max_pool_size: LDAP server maximum connection pool size.

Added in MySQL 5.7.19.

• authentication_ldap_sasl_server_host: LDAP server host name or IP address. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_server_port: LDAP server port number. Added in MySQL 5.7.19.

• authentication_ldap_sasl_tls: Whether to use encrypted connections to LDAP server. Added in

MySQL 5.7.19.

• authentication_ldap_sasl_user_search_attr: LDAP server user search attribute. Added in

MySQL 5.7.19.

• authentication_ldap_simple_auth_method_name: Authentication method name. Added in

MySQL 5.7.19.

• authentication_ldap_simple_bind_base_dn: LDAP server base distinguished name. Added in

MySQL 5.7.19.

• authentication_ldap_simple_bind_root_dn: LDAP server root distinguished name. Added in

MySQL 5.7.19.

• authentication_ldap_simple_bind_root_pwd: LDAP server root bind password. Added in

MySQL 5.7.19.

• authentication_ldap_simple_ca_path: LDAP server certificate authority file name. Added in

MySQL 5.7.19.

28

Options and Variables Introduced in MySQL 5.7

• authentication_ldap_simple_group_search_attr: LDAP server group search attribute. Added

in MySQL 5.7.19.

• authentication_ldap_simple_group_search_filter: LDAP custom group search filter. Added

in MySQL 5.7.21.

• authentication_ldap_simple_init_pool_size: LDAP server initial connection pool size. Added

in MySQL 5.7.19.

• authentication_ldap_simple_log_status: LDAP server log level. Added in MySQL 5.7.19.

• authentication_ldap_simple_max_pool_size: LDAP server maximum connection pool size.

Added in MySQL 5.7.19.

• authentication_ldap_simple_server_host: LDAP server host name or IP address. Added in

MySQL 5.7.19.

• authentication_ldap_simple_server_port: LDAP server port number. Added in MySQL 5.7.19.

• authentication_ldap_simple_tls: Whether to use encrypted connections to LDAP server. Added

in MySQL 5.7.19.

• authentication_ldap_simple_user_search_attr: LDAP server user search attribute. Added in

MySQL 5.7.19.

• authentication_windows_log_level: Windows authentication plugin logging level. Added in

MySQL 5.7.9.

• authentication_windows_use_principal_name: Whether to use Windows authentication plugin

principal name. Added in MySQL 5.7.9.

• auto_generate_certs: Whether to autogenerate SSL key and certificate files. Added in MySQL

5.7.5.

• avoid_temporal_upgrade: Whether ALTER TABLE should upgrade pre-5.6.4 temporal columns.

Added in MySQL 5.7.6.

• binlog_error_action: Controls what happens when server cannot write to binary log. Added in

MySQL 5.7.6.

• binlog_group_commit_sync_delay: Sets number of microseconds to wait before synchronizing

transactions to disk. Added in MySQL 5.7.5.

• binlog_group_commit_sync_no_delay_count: Sets maximum number of transactions to wait for
before aborting current delay specified by binlog_group_commit_sync_delay. Added in MySQL 5.7.5.

• binlog_gtid_simple_recovery: Controls how binary logs are iterated during GTID recovery. Added

in MySQL 5.7.6.

• binlog_transaction_dependency_history_size: Number of row hashes kept for looking up

transaction that last updated some row. Added in MySQL 5.7.22.

• binlog_transaction_dependency_tracking: Source of dependency information (commit

timestamps or transaction write sets) from which to assess which transactions can be executed in
parallel by replica's multithreaded applier. Added in MySQL 5.7.22.

• binlogging_impossible_mode: Deprecated and later removed. Use binlog_error_action instead.

Added in MySQL 5.7.5.

• block_encryption_mode: Mode for block-based encryption algorithms. Added in MySQL 5.7.4.

29

Options and Variables Introduced in MySQL 5.7

• check_proxy_users: Whether built-in authentication plugins do proxying. Added in MySQL 5.7.7.

• connection_control_failed_connections_threshold: Consecutive failed connection attempts

before delays occur. Added in MySQL 5.7.17.

• connection_control_max_connection_delay: Maximum delay (milliseconds) for server response

to failed connection attempts. Added in MySQL 5.7.17.

• connection_control_min_connection_delay: Minimum delay (milliseconds) for server response

to failed connection attempts. Added in MySQL 5.7.17.

• daemonize: Run as System V daemon. Added in MySQL 5.7.6.

• default_authentication_plugin: Default authentication plugin. Added in MySQL 5.7.2.

• default_password_lifetime: Age in days when passwords effectively expire. Added in MySQL

5.7.4.

• disable-partition-engine-check: Whether to disable startup check for tables without native

partitioning. Added in MySQL 5.7.17.

• disabled_storage_engines: Storage engines that cannot be used to create tables. Added in

MySQL 5.7.8.

• disconnect_on_expired_password: Whether server disconnects clients with expired passwords if

clients cannot handle such accounts. Added in MySQL 5.7.1.

• early-plugin-load: Specify plugins to load before loading mandatory built-in plugins and before

storage engine initialization. Added in MySQL 5.7.11.

• executed_gtids_compression_period: Renamed to gtid_executed_compression_period. Added in

MySQL 5.7.5.

• group_replication_allow_local_disjoint_gtids_join: Allow current server to join group

even if it has transactions not present in group. Added in MySQL 5.7.17.

• group_replication_allow_local_lower_version_join: Allow current server to join group

even if it has lower plugin version than group. Added in MySQL 5.7.17.

• group_replication_auto_increment_increment: Determines interval between successive

column values for transactions executing on this server. Added in MySQL 5.7.17.

• group_replication_bootstrap_group: Configure this server to bootstrap group. Added in MySQL

5.7.17.

• group_replication_components_stop_timeout: Timeout, in seconds, that plugin waits for each

component when shutting down. Added in MySQL 5.7.17.

• group_replication_compression_threshold: Value in bytes above which (LZ4) compression is

enforced; when set to zero, deactivates compression. Added in MySQL 5.7.17.

• group_replication_enforce_update_everywhere_checks: Enable or disable strict consistency

checks for multi-source update everywhere. Added in MySQL 5.7.17.

• group_replication_exit_state_action: How instance behaves when it leaves group

involuntarily. Added in MySQL 5.7.24.

• group_replication_flow_control_applier_threshold: Number of waiting transactions in

applier queue which trigger flow control. Added in MySQL 5.7.17.

30

Options and Variables Introduced in MySQL 5.7

• group_replication_flow_control_certifier_threshold: Number of waiting transactions in

certifier queue that trigger flow control. Added in MySQL 5.7.17.

• group_replication_flow_control_mode: Mode used for flow control. Added in MySQL 5.7.17.

• group_replication_force_members: Comma separated list of peer addresses, such as

host1:port1,host2:port2. Added in MySQL 5.7.17.

• group_replication_group_name: Name of group. Added in MySQL 5.7.17.

• group_replication_group_seeds: List of peer addresses, comma separated list such as

host1:port1,host2:port2. Added in MySQL 5.7.17.

• group_replication_gtid_assignment_block_size: Number of consecutive GTIDs that are

reserved for each member; each member consumes its blocks and reserves more when needed. Added
in MySQL 5.7.17.

• group_replication_ip_whitelist: List of hosts permitted to connect to group. Added in MySQL

5.7.17.

• group_replication_local_address: Local address in host:port format. Added in MySQL 5.7.17.

• group_replication_member_weight: Chance of this member being elected as primary. Added in

MySQL 5.7.20.

• group_replication_poll_spin_loops: Number of times group communication thread waits.

Added in MySQL 5.7.17.

• group_replication_recovery_complete_at: Recovery policies when handling cached

transactions after state transfer. Added in MySQL 5.7.17.

• group_replication_recovery_reconnect_interval: Sleep time, in seconds, between

reconnection attempts when no donor was found in group. Added in MySQL 5.7.17.

• group_replication_recovery_retry_count: Number of times that joining member tries to

connect to available donors before giving up. Added in MySQL 5.7.17.

• group_replication_recovery_ssl_ca: File that contains list of trusted SSL Certificate Authorities.

Added in MySQL 5.7.17.

• group_replication_recovery_ssl_capath: Directory that contains trusted SSL Certificate

Authority certificate files. Added in MySQL 5.7.17.

• group_replication_recovery_ssl_cert: Name of SSL certificate file to use for establishing

encrypted connection. Added in MySQL 5.7.17.

• group_replication_recovery_ssl_cipher: Permissible ciphers for SSL encryption. Added in

MySQL 5.7.17.

• group_replication_recovery_ssl_crl: File that contains certificate revocation lists. Added in

MySQL 5.7.17.

• group_replication_recovery_ssl_crlpath: Directory that contains certificate revocation-list

files. Added in MySQL 5.7.17.

• group_replication_recovery_ssl_key: Name of SSL key file to use for establishing encrypted

connection. Added in MySQL 5.7.17.

• group_replication_recovery_ssl_verify_server_cert: Make recovery process check server

Common Name value in certificate sent by donor. Added in MySQL 5.7.17.

31

Options and Variables Introduced in MySQL 5.7

• group_replication_recovery_use_ssl: Whether Group Replication recovery connection should

use SSL. Added in MySQL 5.7.17.

• group_replication_single_primary_mode: Instructs group to use single server for read/write

workload. Added in MySQL 5.7.17.

• group_replication_ssl_mode: Desired security state of connection between Group Replication

members. Added in MySQL 5.7.17.

• group_replication_start_on_boot: Whether server should start Group Replication during server

startup. Added in MySQL 5.7.17.

• group_replication_transaction_size_limit: Sets maximum size of transaction in bytes which

group accepts. Added in MySQL 5.7.19.

• group_replication_unreachable_majority_timeout: How long to wait for network partitions

that result in minority to leave group. Added in MySQL 5.7.19.

• gtid_executed_compression_period: Compress gtid_executed table each time this many

transactions have occurred. 0 means never compress this table. Applies only when binary logging is
disabled. Added in MySQL 5.7.6.

• have_statement_timeout: Whether statement execution timeout is available. Added in MySQL

5.7.4.

• initialize: Whether to run in initialization mode (secure). Added in MySQL 5.7.6.

• initialize-insecure: Whether to run in initialization mode (insecure). Added in MySQL 5.7.6.

• innodb_adaptive_hash_index_parts: Partitions adaptive hash index search system into n

partitions, with each partition protected by separate latch. Each index is bound to specific partition based
on space ID and index ID attributes. Added in MySQL 5.7.8.

• innodb_background_drop_list_empty: Delays table creation until background drop list is empty

(debug). Added in MySQL 5.7.10.

• innodb_buffer_pool_chunk_size: Chunk size used when resizing buffer pool. Added in MySQL

5.7.5.

• innodb_buffer_pool_dump_pct: Percentage of most recently used pages for each buffer pool to

read out and dump. Added in MySQL 5.7.2.

• innodb_compress_debug: Compresses all tables using specified compression algorithm. Added in

MySQL 5.7.8.

• innodb_deadlock_detect: Enables or disables deadlock detection. Added in MySQL 5.7.15.

• innodb_default_row_format: Default row format for InnoDB tables. Added in MySQL 5.7.9.

• innodb_disable_resize_buffer_pool_debug: Disables resizing of InnoDB buffer pool. Added in

MySQL 5.7.6.

• innodb_fill_factor: Percentage for B-tree leaf and non-leaf page space to be filled with data.

Remaining space is reserved for future growth. Added in MySQL 5.7.5.

• innodb_flush_sync: Enable innodb_flush_sync to ignore the innodb_io_capacity and

innodb_io_capacity_max settings for bursts of I/O activity that occur at checkpoints. Disable
innodb_flush_sync to adhere to limits on I/O activity as defined by innodb_io_capacity and
innodb_io_capacity_max. Added in MySQL 5.7.8.

32

Options and Variables Introduced in MySQL 5.7

• innodb_ft_result_cache_limit: InnoDB FULLTEXT search query result cache limit. Added in

MySQL 5.7.2.

• innodb_ft_total_cache_size: Total memory allocated for InnoDB FULLTEXT search index cache.

Added in MySQL 5.7.2.

• innodb_log_checkpoint_now: Debug option that forces InnoDB to write checkpoint. Added in

MySQL 5.7.2.

• innodb_log_checksum_algorithm: Specifies how to generate and verify checksum stored in each

redo log disk block. Added in MySQL 5.7.8.

• innodb_log_checksums: Enables or disables checksums for redo log pages. Added in MySQL 5.7.9.

• innodb_log_write_ahead_size: Redo log write-ahead block size. Added in MySQL 5.7.4.

• innodb_max_undo_log_size: Sets threshold for truncating InnoDB undo log. Added in MySQL 5.7.5.

• innodb_merge_threshold_set_all_debug: Overrides current MERGE_THRESHOLD setting with

specified value for all indexes that are currently in dictionary cache. Added in MySQL 5.7.6.

• innodb_numa_interleave: Enables NUMA MPOL_INTERLEAVE memory policy for allocation of

InnoDB buffer pool. Added in MySQL 5.7.9.

• innodb_optimize_point_storage: Enable this option to store POINT data as fixed-length data

rather than variable-length data. Added in MySQL 5.7.5.

• innodb_page_cleaners: Number of page cleaner threads. Added in MySQL 5.7.4.

• innodb_purge_rseg_truncate_frequency: Rate at which undo log purge should be invoked as

part of purge action. Value = n invokes undo log purge on every nth iteration of purge invocation. Added
in MySQL 5.7.5.

• innodb_stats_include_delete_marked: Include delete-marked records when calculating

persistent InnoDB statistics. Added in MySQL 5.7.17.

• innodb_status_output: Used to enable or disable periodic output for standard InnoDB Monitor. Also
used in combination with innodb_status_output_locks to enable and disable periodic output for InnoDB
Lock Monitor. Added in MySQL 5.7.4.

• innodb_status_output_locks: Used to enable or disable periodic output for standard InnoDB

Lock Monitor. innodb_status_output must also be enabled to produce periodic output for InnoDB Lock
Monitor. Added in MySQL 5.7.4.

• innodb_sync_debug: Enables InnoDB sync debug checking. Added in MySQL 5.7.8.

• innodb_temp_data_file_path: Path to temporary tablespace data files and their sizes. Added in

MySQL 5.7.1.

• innodb_tmpdir: Directory location for temporary table files created during online ALTER TABLE

operations. Added in MySQL 5.7.11.

• innodb_undo_log_truncate: Enable this option to mark InnoDB undo tablespace for truncation.

Added in MySQL 5.7.5.

• internal_tmp_disk_storage_engine: Storage engine for internal temporary tables. Added in

MySQL 5.7.5.

• keyring-migration-destination: Key migration destination keyring plugin. Added in MySQL

5.7.21.

33

Options and Variables Introduced in MySQL 5.7

• keyring-migration-host: Host name for connecting to running server for key migration. Added in

MySQL 5.7.21.

• keyring-migration-password: Password for connecting to running server for key migration. Added

in MySQL 5.7.21.

• keyring-migration-port: TCP/IP port number for connecting to running server for key migration.

Added in MySQL 5.7.21.

• keyring-migration-socket: Unix socket file or Windows named pipe for connecting to running

server for key migration. Added in MySQL 5.7.21.

• keyring-migration-source: Key migration source keyring plugin. Added in MySQL 5.7.21.

• keyring-migration-user: User name for connecting to running server for key migration. Added in

MySQL 5.7.21.

• keyring_aws_cmk_id: AWS keyring plugin customer master key ID value. Added in MySQL 5.7.19.

• keyring_aws_conf_file: AWS keyring plugin configuration file location. Added in MySQL 5.7.19.

• keyring_aws_data_file: AWS keyring plugin storage file location. Added in MySQL 5.7.19.

• keyring_aws_region: AWS keyring plugin region. Added in MySQL 5.7.19.

• keyring_encrypted_file_data: keyring_encrypted_file plugin data file. Added in MySQL 5.7.21.

• keyring_encrypted_file_password: keyring_encrypted_file plugin password. Added in MySQL

5.7.21.

• keyring_file_data: keyring_file plugin data file. Added in MySQL 5.7.11.

• keyring_okv_conf_dir: Oracle Key Vault keyring plugin configuration directory. Added in MySQL

5.7.12.

• keyring_operations: Whether keyring operations are enabled. Added in MySQL 5.7.21.

• log_backward_compatible_user_definitions: Whether to log CREATE/ALTER USER, GRANT

in backward-compatible fashion. Added in MySQL 5.7.6.

• log_builtin_as_identified_by_password: Whether to log CREATE/ALTER USER, GRANT in

backward-compatible fashion. Added in MySQL 5.7.9.

• log_error_verbosity: Error logging verbosity level. Added in MySQL 5.7.2.

• log_slow_admin_statements: Log slow OPTIMIZE, ANALYZE, ALTER and other administrative

statements to slow query log if it is open. Added in MySQL 5.7.1.

• log_slow_slave_statements: Cause slow statements as executed by replica to be written to slow

query log. Added in MySQL 5.7.1.

• log_statements_unsafe_for_binlog: Disables error 1592 warnings being written to error log.

Added in MySQL 5.7.11.

• log_syslog: Whether to write error log to syslog. Added in MySQL 5.7.5.

• log_syslog_facility: Facility for syslog messages. Added in MySQL 5.7.5.

• log_syslog_include_pid: Whether to include server PID in syslog messages. Added in MySQL

5.7.5.

34

Options and Variables Introduced in MySQL 5.7

• log_syslog_tag: Tag for server identifier in syslog messages. Added in MySQL 5.7.5.

• log_timestamps: Log timestamp format. Added in MySQL 5.7.2.

• max_digest_length: Maximum digest size in bytes. Added in MySQL 5.7.6.

• max_execution_time: Statement execution timeout value. Added in MySQL 5.7.8.

• max_points_in_geometry: Maximum number of points in geometry values for ST_Buffer_Strategy().

Added in MySQL 5.7.8.

• max_statement_time: Statement execution timeout value. Added in MySQL 5.7.4.

• mecab_charset: Character set currently used by MeCab full-text parser plugin. Added in MySQL 5.7.6.

• mecab_rc_file: Path to mecabrc configuration file for MeCab parser for full-text search. Added in

MySQL 5.7.6.

• mysql_firewall_mode: Whether MySQL Enterprise Firewall plugin is operational. Added in MySQL

5.7.9.

• mysql_firewall_trace: Whether to enable MySQL Enterprise Firewall plugin trace. Added in

MySQL 5.7.9.

• mysql_native_password_proxy_users: Whether mysql_native_password authentication plugin

does proxying. Added in MySQL 5.7.7.

• mysqlx: Whether X Plugin is initialized. Added in MySQL 5.7.12.

• mysqlx_bind_address: Network address X Plugin uses for connections. Added in MySQL 5.7.17.

• mysqlx_connect_timeout: Maximum permitted waiting time in seconds for a connection to set up a

session. Added in MySQL 5.7.12.

• mysqlx_idle_worker_thread_timeout: Time in seconds after which idle worker threads are

terminated. Added in MySQL 5.7.12.

• mysqlx_max_allowed_packet: Maximum size of network packets that can be received by X Plugin.

Added in MySQL 5.7.12.

• mysqlx_max_connections: Maximum number of concurrent client connections X Plugin can accept.

Added in MySQL 5.7.12.

• mysqlx_min_worker_threads: Minimum number of worker threads used for handling client requests.

Added in MySQL 5.7.12.

• mysqlx_port: Port number on which X Plugin accepts TCP/IP connections. Added in MySQL 5.7.12.

• mysqlx_port_open_timeout: Time which X Plugin waits when accepting connections. Added in

MySQL 5.7.17.

• mysqlx_socket: Path to socket where X Plugin listens for connections. Added in MySQL 5.7.15.

• mysqlx_ssl_ca: File that contains list of trusted SSL Certificate Authorities. Added in MySQL 5.7.12.

• mysqlx_ssl_capath: Directory that contains trusted SSL Certificate Authority certificate files. Added in

MySQL 5.7.12.

• mysqlx_ssl_cert: File that contains X.509 certificate. Added in MySQL 5.7.12.

• mysqlx_ssl_cipher: Permissible ciphers for connection encryption. Added in MySQL 5.7.12.

35

Options and Variables Introduced in MySQL 5.7

• mysqlx_ssl_crl: File that contains certificate revocation lists. Added in MySQL 5.7.12.

• mysqlx_ssl_crlpath: Directory that contains certificate revocation list files. Added in MySQL 5.7.12.

• mysqlx_ssl_key: File that contains X.509 key. Added in MySQL 5.7.12.

• named_pipe_full_access_group: Name of Windows group granted full access to named pipe.

Added in MySQL 5.7.25.

• ngram_token_size: Defines n-gram token size for full-text search ngram parser. Added in MySQL

5.7.6.

• offline_mode: Whether server is offline. Added in MySQL 5.7.5.

• parser_max_mem_size: Maximum amount of memory available to parser. Added in MySQL 5.7.12.

• performance-schema-consumer-events-transactions-current: Configure events-

transactions-current consumer. Added in MySQL 5.7.3.

• performance-schema-consumer-events-transactions-history: Configure events-

transactions-history consumer. Added in MySQL 5.7.3.

• performance-schema-consumer-events-transactions-history-long: Configure events-

transactions-history-long consumer. Added in MySQL 5.7.3.

• performance_schema_events_transactions_history_long_size: Number of rows in

events_transactions_history_long table. Added in MySQL 5.7.3.

• performance_schema_events_transactions_history_size: Number of rows per thread in

events_transactions_history table. Added in MySQL 5.7.3.

• performance_schema_max_digest_length: Maximum Performance Schema digest size in bytes.

Added in MySQL 5.7.8.

• performance_schema_max_index_stat: Maximum number of indexes to keep statistics for. Added

in MySQL 5.7.6.

• performance_schema_max_memory_classes: Maximum number of memory instruments. Added in

MySQL 5.7.2.

• performance_schema_max_metadata_locks: Maximum number of metadata locks to track. Added

in MySQL 5.7.3.

• performance_schema_max_prepared_statements_instances: Number of rows in

prepared_statements_instances table. Added in MySQL 5.7.4.

• performance_schema_max_program_instances: Maximum number of stored programs for

statistics. Added in MySQL 5.7.2.

• performance_schema_max_sql_text_length: Maximum number of bytes stored from SQL

statements. Added in MySQL 5.7.6.

• performance_schema_max_statement_stack: Maximum stored program nesting for statistics.

Added in MySQL 5.7.2.

• performance_schema_max_table_lock_stat: Maximum number of tables to keep lock statistics

for. Added in MySQL 5.7.6.

• performance_schema_show_processlist: Select SHOW PROCESSLIST implementation. Added

in MySQL 5.7.39.

36

Options and Variables Introduced in MySQL 5.7

• range_optimizer_max_mem_size: Limit on range optimizer memory consumption. Added in MySQL

5.7.9.

• rbr_exec_mode: Allows for switching server between IDEMPOTENT mode (key and some other errors

suppressed) and STRICT mode; STRICT mode is default. Added in MySQL 5.7.1.

• replication_optimize_for_static_plugin_config: Shared locks for semisynchronous

replication. Added in MySQL 5.7.33.

• replication_sender_observe_commit_only: Limited callbacks for semisynchronous replication.

Added in MySQL 5.7.33.

• require_secure_transport: Whether client connections must use secure transport. Added in

MySQL 5.7.8.

• rewriter_enabled: Whether query rewrite plugin is enabled. Added in MySQL 5.7.6.

• rewriter_verbose: For internal use. Added in MySQL 5.7.6.

• rpl_semi_sync_master_wait_for_slave_count: Number of replica acknowledgments source

must receive per transaction before proceeding. Added in MySQL 5.7.3.

• rpl_semi_sync_master_wait_point: Wait point for replica transaction receipt acknowledgment.

Added in MySQL 5.7.2.

• rpl_stop_slave_timeout: Number of seconds that STOP REPLICA or STOP SLAVE waits before

timing out. Added in MySQL 5.7.2.

• session_track_gtids: Enables tracker which can be set to track different GTIDs. Added in MySQL

5.7.6.

• session_track_schema: Whether to track schema changes. Added in MySQL 5.7.4.

• session_track_state_change: Whether to track session state changes. Added in MySQL 5.7.4.

• session_track_system_variables: Session variables to track changes for. Added in MySQL 5.7.4.

• session_track_transaction_info: How to perform transaction tracking. Added in MySQL 5.7.8.

• sha256_password_auto_generate_rsa_keys: Whether to generate RSA key-pair files

automatically. Added in MySQL 5.7.5.

• sha256_password_proxy_users: Whether sha256_password authentication plugin does proxying.

Added in MySQL 5.7.7.

• show_compatibility_56: Compatibility for SHOW STATUS/VARIABLES. Added in MySQL 5.7.6.

• show_create_table_verbosity: Whether to display ROW_FORMAT in SHOW CREATE TABLE

even if it has default value. Added in MySQL 5.7.22.

• show_old_temporals: Whether SHOW CREATE TABLE should indicate pre-5.6.4 temporal columns.

Added in MySQL 5.7.6.

• simplified_binlog_gtid_recovery: Renamed to binlog_gtid_simple_recovery. Added in MySQL

5.7.5.

• slave_parallel_type: Tells replica to use timestamp information (LOGICAL_CLOCK) or database

partioning (DATABASE) to parallelize transactions. Added in MySQL 5.7.2.

• slave_preserve_commit_order: Ensures that all commits by replica workers happen in same order

as on source to maintain consistency when using parallel applier threads. Added in MySQL 5.7.5.

37

Options and Variables Deprecated in MySQL 5.7

• super_read_only: Whether to ignore SUPER exceptions to read-only mode. Added in MySQL 5.7.8.

• thread_pool_algorithm: Thread pool algorithm. Added in MySQL 5.7.9.

• thread_pool_high_priority_connection: Whether current session is high priority. Added in

MySQL 5.7.9.

• thread_pool_max_unused_threads: Maximum permissible number of unused threads. Added in

MySQL 5.7.9.

• thread_pool_prio_kickup_timer: How long before statement is moved to high-priority execution.

Added in MySQL 5.7.9.

• thread_pool_size: Number of thread groups in thread pool. Added in MySQL 5.7.9.

• thread_pool_stall_limit: How long before statement is defined as stalled. Added in MySQL 5.7.9.

• tls_version: Permissible TLS protocols for encrypted connections. Added in MySQL 5.7.10.

• transaction_write_set_extraction: Defines algorithm used to hash writes extracted during

transaction. Added in MySQL 5.7.6.

• validate_password_check_user_name: Whether to check passwords against user name. Added in

MySQL 5.7.15.

• validate_password_dictionary_file_last_parsed: When dictionary file was last parsed.

Added in MySQL 5.7.8.

• validate_password_dictionary_file_words_count: Number of words in dictionary file. Added

in MySQL 5.7.8.

• version_tokens_session: Client token list for Version Tokens. Added in MySQL 5.7.8.

• version_tokens_session_number: For internal use. Added in MySQL 5.7.8.

Options and Variables Deprecated in MySQL 5.7

The following system variables, status variables, and options have been deprecated in MySQL 5.7.

• Innodb_available_undo_logs: Total number of InnoDB rollback segments; different from

innodb_rollback_segments, which displays number of active rollback segments. Deprecated in MySQL
5.7.19.

• Qcache_free_blocks: Number of free memory blocks in query cache. Deprecated in MySQL 5.7.20.

• Qcache_free_memory: Amount of free memory for query cache. Deprecated in MySQL 5.7.20.

• Qcache_hits: Number of query cache hits. Deprecated in MySQL 5.7.20.

• Qcache_inserts: Number of query cache inserts. Deprecated in MySQL 5.7.20.

• Qcache_lowmem_prunes: Number of queries which were deleted from query cache due to lack of free

memory in cache. Deprecated in MySQL 5.7.20.

• Qcache_not_cached: Number of noncached queries (not cacheable, or not cached due to

query_cache_type setting). Deprecated in MySQL 5.7.20.

• Qcache_queries_in_cache: Number of queries registered in query cache. Deprecated in MySQL

5.7.20.

• Qcache_total_blocks: Total number of blocks in query cache. Deprecated in MySQL 5.7.20.

38

Options and Variables Deprecated in MySQL 5.7

• Slave_heartbeat_period: Replica's replication heartbeat interval, in seconds. Deprecated in MySQL

5.7.6.

• Slave_last_heartbeat: Shows when latest heartbeat signal was received, in TIMESTAMP format.

Deprecated in MySQL 5.7.6.

• Slave_received_heartbeats: Number of heartbeats received by replica since previous reset.

Deprecated in MySQL 5.7.6.

• Slave_retried_transactions: Total number of times since startup that replication SQL thread has

retried transactions. Deprecated in MySQL 5.7.6.

• Slave_running: State of this server as replica (replication I/O thread status). Deprecated in MySQL

5.7.6.

• avoid_temporal_upgrade: Whether ALTER TABLE should upgrade pre-5.6.4 temporal columns.

Deprecated in MySQL 5.7.6.

• binlog_max_flush_queue_time: How long to read transactions before flushing to binary log.

Deprecated in MySQL 5.7.9.

• bootstrap: Used by mysql installation scripts. Deprecated in MySQL 5.7.6.

• des-key-file: Load keys for des_encrypt() and des_encrypt from given file. Deprecated in MySQL

5.7.6.

• disable-partition-engine-check: Whether to disable startup check for tables without native

partitioning. Deprecated in MySQL 5.7.17.

• group_replication_allow_local_disjoint_gtids_join: Allow current server to join group

even if it has transactions not present in group. Deprecated in MySQL 5.7.21.

• have_crypt: Availability of crypt() system call. Deprecated in MySQL 5.7.6.

• have_query_cache: Whether mysqld supports query cache. Deprecated in MySQL 5.7.20.

• ignore-db-dir: Treat directory as nondatabase directory. Deprecated in MySQL 5.7.16.

• ignore_db_dirs: Directories treated as nondatabase directories. Deprecated in MySQL 5.7.16.

• innodb: Enable InnoDB (if this version of MySQL supports it). Deprecated in MySQL 5.7.5.

• innodb_file_format: Format for new InnoDB tables. Deprecated in MySQL 5.7.7.

• innodb_file_format_check: Whether InnoDB performs file format compatibility checking.

Deprecated in MySQL 5.7.7.

• innodb_file_format_max: File format tag in shared tablespace. Deprecated in MySQL 5.7.7.

• innodb_large_prefix: Enables longer keys for column prefix indexes. Deprecated in MySQL 5.7.7.

• innodb_support_xa: Enable InnoDB support for XA two-phase commit. Deprecated in MySQL 5.7.10.

• innodb_undo_logs: Number of undo logs (rollback segments) used by InnoDB; alias for

innodb_rollback_segments. Deprecated in MySQL 5.7.19.

• innodb_undo_tablespaces: Number of tablespace files that rollback segments are divided between.

Deprecated in MySQL 5.7.21.

• log-warnings: Write some noncritical warnings to log file. Deprecated in MySQL 5.7.2.

• metadata_locks_cache_size: Size of metadata locks cache. Deprecated in MySQL 5.7.4.

39

Options and Variables Removed in MySQL 5.7

• metadata_locks_hash_instances: Number of metadata lock hashes. Deprecated in MySQL 5.7.4.

• myisam_repair_threads: Number of threads to use when repairing MyISAM tables. 1 disables

parallel repair. Deprecated in MySQL 5.7.38.

• old_passwords: Selects password hashing method for PASSWORD(). Deprecated in MySQL 5.7.6.

• partition: Enable (or disable) partitioning support. Deprecated in MySQL 5.7.16.

• query_cache_limit: Do not cache results that are bigger than this. Deprecated in MySQL 5.7.20.

• query_cache_min_res_unit: Minimal size of unit in which space for results is allocated (last unit is

trimmed after writing all result data). Deprecated in MySQL 5.7.20.

• query_cache_size: Memory allocated to store results from old queries. Deprecated in MySQL 5.7.20.

• query_cache_type: Query cache type. Deprecated in MySQL 5.7.20.

• query_cache_wlock_invalidate: Invalidate queries in query cache on LOCK for write. Deprecated

in MySQL 5.7.20.

• secure_auth: Disallow authentication for accounts that have old (pre-4.1) passwords. Deprecated in

MySQL 5.7.5.

• show_compatibility_56: Compatibility for SHOW STATUS/VARIABLES. Deprecated in MySQL

5.7.6.

• show_old_temporals: Whether SHOW CREATE TABLE should indicate pre-5.6.4 temporal columns.

Deprecated in MySQL 5.7.6.

• skip-partition: Do not enable user-defined partitioning. Deprecated in MySQL 5.7.16.

• sync_frm: Sync .frm to disk on create. Enabled by default. Deprecated in MySQL 5.7.6.

• temp-pool: Using this option causes most temporary files created to use small set of names, rather

than unique name for each new file. Deprecated in MySQL 5.7.18.

• tx_isolation: Default transaction isolation level. Deprecated in MySQL 5.7.20.

• tx_read_only: Default transaction access mode. Deprecated in MySQL 5.7.20.

Options and Variables Removed in MySQL 5.7

The following system variables, status variables, and options have been removed in MySQL 5.7.

• Com_show_slave_status_nonblocking: Count of SHOW REPLICA | SLAVE STATUS

NONBLOCKING statements. Removed in MySQL 5.7.6.

• Max_statement_time_exceeded: Number of statements that exceeded execution timeout value.

Removed in MySQL 5.7.8.

• Max_statement_time_set: Number of statements for which execution timeout was set. Removed in

MySQL 5.7.8.

• Max_statement_time_set_failed: Number of statements for which execution timeout setting failed.

Removed in MySQL 5.7.8.

• binlogging_impossible_mode: Deprecated and later removed. Use binlog_error_action instead.

Removed in MySQL 5.7.6.

• default-authentication-plugin: Default authentication plugin. Removed in MySQL 5.7.2.

40

How to Report Bugs or Problems

• executed_gtids_compression_period: Renamed to gtid_executed_compression_period.

Removed in MySQL 5.7.6.

• innodb_additional_mem_pool_size: Size of memory pool InnoDB uses to store data dictionary

information and other internal data structures. Removed in MySQL 5.7.4.

• innodb_log_checksum_algorithm: Specifies how to generate and verify checksum stored in each

redo log disk block. Removed in MySQL 5.7.9.

• innodb_optimize_point_storage: Enable this option to store POINT data as fixed-length data

rather than variable-length data. Removed in MySQL 5.7.6.

• innodb_use_sys_malloc: Whether InnoDB uses OS or own memory allocator. Removed in MySQL

5.7.4.

• log-slow-admin-statements: Log slow OPTIMIZE, ANALYZE, ALTER and other administrative

statements to slow query log if it is open. Removed in MySQL 5.7.1.

• log-slow-slave-statements: Cause slow statements as executed by replica to be written to slow

query log. Removed in MySQL 5.7.1.

• log_backward_compatible_user_definitions: Whether to log CREATE/ALTER USER, GRANT

in backward-compatible fashion. Removed in MySQL 5.7.9.

• max_statement_time: Statement execution timeout value. Removed in MySQL 5.7.8.

• myisam_repair_threads: Number of threads to use when repairing MyISAM tables. 1 disables

parallel repair. Removed in MySQL 5.7.39.

• simplified_binlog_gtid_recovery: Renamed to binlog_gtid_simple_recovery. Removed in

MySQL 5.7.6.

• storage_engine: Default storage engine. Removed in MySQL 5.7.5.

• thread_concurrency: Permits application to provide hint to threads system for desired number of

threads which should be run at one time. Removed in MySQL 5.7.2.

• timed_mutexes: Specify whether to time mutexes (only InnoDB mutexes are currently supported).

Removed in MySQL 5.7.5.

1.5 How to Report Bugs or Problems

Before posting a bug report about a problem, please try to verify that it is a bug and that it has not been
reported already:

• Start by searching the MySQL online manual at https://dev.mysql.com/doc/. We try to keep the manual
up to date by updating it frequently with solutions to newly found problems. In addition, the release
notes accompanying the manual can be particularly useful since it is quite possible that a newer version
contains a solution to your problem. The release notes are available at the location just given for the
manual.

• If you get a parse error for an SQL statement, please check your syntax closely. If you cannot find

something wrong with it, it is extremely likely that your current version of MySQL Server doesn't support
the syntax you are using. If you are using the current version and the manual doesn't cover the syntax
that you are using, MySQL Server doesn't support your statement.

If the manual covers the syntax you are using, but you have an older version of MySQL Server, you
should check the MySQL change history to see when the syntax was implemented. In this case, you
have the option of upgrading to a newer version of MySQL Server.

41

How to Report Bugs or Problems

• For solutions to some common problems, see Section B.3, “Problems and Common Errors”.

• Search the bugs database at http://bugs.mysql.com/ to see whether the bug has been reported and

fixed.

• You can also use http://www.mysql.com/search/ to search all the Web pages (including the manual) that

are located at the MySQL website.

If you cannot find an answer in the manual, the bugs database, or the mailing list archives, check with your
local MySQL expert. If you still cannot find an answer to your question, please use the following guidelines
for reporting the bug.

The normal way to report bugs is to visit http://bugs.mysql.com/, which is the address for our bugs
database. This database is public and can be browsed and searched by anyone. If you log in to the
system, you can enter new reports.

Bugs posted in the bugs database at http://bugs.mysql.com/ that are corrected for a given release are
noted in the release notes.

If you find a security bug in MySQL Server, please let us know immediately by sending an email message
to <secalert_us@oracle.com>. Exception: Support customers should report all problems, including
security bugs, to Oracle Support at http://support.oracle.com/.

To discuss problems with other users, you can use the MySQL Community Slack.

Writing a good bug report takes patience, but doing it right the first time saves time both for us and for
yourself. A good bug report, containing a full test case for the bug, makes it very likely that we will fix the
bug in the next release. This section helps you write your report correctly so that you do not waste your
time doing things that may not help us much or at all. Please read this section carefully and make sure that
all the information described here is included in your report.

Preferably, you should test the problem using the latest production or development version of MySQL
Server before posting. Anyone should be able to repeat the bug by just using mysql test <
script_file on your test case or by running the shell or Perl script that you include in the bug report.
Any bug that we are able to repeat has a high chance of being fixed in the next MySQL release.

It is most helpful when a good description of the problem is included in the bug report. That is, give a good
example of everything you did that led to the problem and describe, in exact detail, the problem itself.
The best reports are those that include a full example showing how to reproduce the bug or problem. See
Section 5.8, “Debugging MySQL”.

Remember that it is possible for us to respond to a report containing too much information, but not to one
containing too little. People often omit facts because they think they know the cause of a problem and
assume that some details do not matter. A good principle to follow is that if you are in doubt about stating
something, state it. It is faster and less troublesome to write a couple more lines in your report than to wait
longer for the answer if we must ask you to provide information that was missing from the initial report.

The most common errors made in bug reports are (a) not including the version number of the MySQL
distribution that you use, and (b) not fully describing the platform on which the MySQL server is installed
(including the platform type and version number). These are highly relevant pieces of information, and in
99 cases out of 100, the bug report is useless without them. Very often we get questions like, “Why doesn't
this work for me?” Then we find that the feature requested wasn't implemented in that MySQL version,
or that a bug described in a report has been fixed in newer MySQL versions. Errors often are platform-
dependent. In such cases, it is next to impossible for us to fix anything without knowing the operating
system and the version number of the platform.

If you compiled MySQL from source, remember also to provide information about your compiler if it is
related to the problem. Often people find bugs in compilers and think the problem is MySQL-related.

42

How to Report Bugs or Problems

Most compilers are under development all the time and become better version by version. To determine
whether your problem depends on your compiler, we need to know what compiler you used. Note that
every compiling problem should be regarded as a bug and reported accordingly.

If a program produces an error message, it is very important to include the message in your report. If we try
to search for something from the archives, it is better that the error message reported exactly matches the
one that the program produces. (Even the lettercase should be observed.) It is best to copy and paste the
entire error message into your report. You should never try to reproduce the message from memory.

If you have a problem with Connector/ODBC (MyODBC), please try to generate a trace file and send it with
your report. See How to Report Connector/ODBC Problems or Bugs.

If your report includes long query output lines from test cases that you run with the mysql command-
line tool, you can make the output more readable by using the --vertical option or the \G statement
terminator. The EXPLAIN SELECT example later in this section demonstrates the use of \G.

Please include the following information in your report:

• The version number of the MySQL distribution you are using (for example, MySQL 5.7.10). You can find
out which version you are running by executing mysqladmin version. The mysqladmin program can
be found in the bin directory under your MySQL installation directory.

• The manufacturer and model of the machine on which you experience the problem.

• The operating system name and version. If you work with Windows, you can usually get the name and
version number by double-clicking your My Computer icon and pulling down the “Help/About Windows”
menu. For most Unix-like operating systems, you can get this information by executing the command
uname -a.

• Sometimes the amount of memory (real and virtual) is relevant. If in doubt, include these values.

• The contents of the docs/INFO_BIN file from your MySQL installation. This file contains information

about how MySQL was configured and compiled.

• If you are using a source distribution of the MySQL software, include the name and version number of

the compiler that you used. If you have a binary distribution, include the distribution name.

• If the problem occurs during compilation, include the exact error messages and also a few lines of

context around the offending code in the file where the error occurs.

• If mysqld died, you should also report the statement that caused mysqld to unexpectedly exit. You can
usually get this information by running mysqld with query logging enabled, and then looking in the log
after mysqld exits. See Section 5.8, “Debugging MySQL”.

• If a database table is related to the problem, include the output from the SHOW CREATE TABLE
db_name.tbl_name statement in the bug report. This is a very easy way to get the definition of
any table in a database. The information helps us create a situation matching the one that you have
experienced.

• The SQL mode in effect when the problem occurred can be significant, so please report the value of

the sql_mode system variable. For stored procedure, stored function, and trigger objects, the relevant
sql_mode value is the one in effect when the object was created. For a stored procedure or function,
the SHOW CREATE PROCEDURE or SHOW CREATE FUNCTION statement shows the relevant SQL mode,
or you can query INFORMATION_SCHEMA for the information:

SELECT ROUTINE_SCHEMA, ROUTINE_NAME, SQL_MODE
FROM INFORMATION_SCHEMA.ROUTINES;

43

How to Report Bugs or Problems

For triggers, you can use this statement:

SELECT EVENT_OBJECT_SCHEMA, EVENT_OBJECT_TABLE, TRIGGER_NAME, SQL_MODE
FROM INFORMATION_SCHEMA.TRIGGERS;

• For performance-related bugs or problems with SELECT statements, you should always include the

output of EXPLAIN SELECT ..., and at least the number of rows that the SELECT statement produces.
You should also include the output from SHOW CREATE TABLE tbl_name for each table that is
involved. The more information you provide about your situation, the more likely it is that someone can
help you.

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
reproduce your situation, the better. If you can make a reproducible test case, you should upload it to be
attached to the bug report.

If you cannot provide a script, you should at least include the output from mysqladmin variables
extended-status processlist in your report to provide some information on how your system is
performing.

• If you cannot produce a test case with only a few rows, or if the test table is too big to be included in the
bug report (more than 10 rows), you should dump your tables using mysqldump and create a README
file that describes your problem. Create a compressed archive of your files using tar and gzip or zip.
After you initiate a bug report for our bugs database at http://bugs.mysql.com/, click the Files tab in the
bug report for instructions on uploading the archive to the bugs database.

• If you believe that the MySQL server produces a strange result from a statement, include not only the
result, but also your opinion of what the result should be, and an explanation describing the basis for
your opinion.

• When you provide an example of the problem, it is better to use the table names, variable names, and

so forth that exist in your actual situation than to come up with new names. The problem could be related
to the name of a table or variable. These cases are rare, perhaps, but it is better to be safe than sorry.
After all, it should be easier for you to provide an example that uses your actual situation, and it is by all
means better for us. If you have data that you do not want to be visible to others in the bug report, you
can upload it using the Files tab as previously described. If the information is really top secret and you do
not want to show it even to us, go ahead and provide an example using other names, but please regard
this as the last choice.

• Include all the options given to the relevant programs, if possible. For example, indicate the options that
you use when you start the mysqld server, as well as the options that you use to run any MySQL client
programs. The options to programs such as mysqld and mysql, and to the configure script, are often

44

How to Report Bugs or Problems

key to resolving problems and are very relevant. It is never a bad idea to include them. If your problem
involves a program written in a language such as Perl or PHP, please include the language processor's
version number, as well as the version for any modules that the program uses. For example, if you have
a Perl script that uses the DBI and DBD::mysql modules, include the version numbers for Perl, DBI,
and DBD::mysql.

• If your question is related to the privilege system, please include the output of mysqladmin reload,
and all the error messages you get when trying to connect. When you test your privileges, you should
execute mysqladmin reload version and try to connect with the program that gives you trouble.

• If you have a patch for a bug, do include it. But do not assume that the patch is all we need, or that we
can use it, if you do not provide some necessary information such as test cases showing the bug that
your patch fixes. We might find problems with your patch or we might not understand it at all. If so, we
cannot use it.

If we cannot verify the exact purpose of the patch, we will not use it. Test cases help us here. Show that
the patch handles all the situations that may occur. If we find a borderline case (even a rare one) where
the patch will not work, it may be useless.

• Guesses about what the bug is, why it occurs, or what it depends on are usually wrong. Even the

MySQL team cannot guess such things without first using a debugger to determine the real cause of a
bug.

• Indicate in your bug report that you have checked the reference manual and mail archive so that others

know you have tried to solve the problem yourself.

• If your data appears corrupt or you get errors when you access a particular table, first check your tables

with CHECK TABLE. If that statement reports any errors:

• The InnoDB crash recovery mechanism handles cleanup when the server is restarted after being
killed, so in typical operation there is no need to “repair” tables. If you encounter an error with
InnoDB tables, restart the server and see whether the problem persists, or whether the error
affected only cached data in memory. If data is corrupted on disk, consider restarting with the
innodb_force_recovery option enabled so that you can dump the affected tables.

• For non-transactional tables, try to repair them with REPAIR TABLE or with myisamchk. See

Chapter 5, MySQL Server Administration.

If you are running Windows, please verify the value of lower_case_table_names using the SHOW
VARIABLES LIKE 'lower_case_table_names' statement. This variable affects how the server
handles lettercase of database and table names. Its effect for a given value should be as described in
Section 9.2.3, “Identifier Case Sensitivity”.

• If you often get corrupted tables, you should try to find out when and why this happens. In this case,
the error log in the MySQL data directory may contain some information about what happened. (This
is the file with the .err suffix in the name.) See Section 5.4.2, “The Error Log”. Please include any
relevant information from this file in your bug report. Normally mysqld should never corrupt a table if
nothing killed it in the middle of an update. If you can find the cause of mysqld dying, it is much easier
for us to provide you with a fix for the problem. See Section B.3.1, “How to Determine What Is Causing a
Problem”.

• If possible, download and install the most recent version of MySQL Server and check whether it solves

your problem. All versions of the MySQL software are thoroughly tested and should work without
problems. We believe in making everything as backward-compatible as possible, and you should be able
to switch MySQL versions without difficulty. See Section 2.1.2, “Which MySQL Version and Distribution
to Install”.

45

MySQL Standards Compliance

1.6 MySQL Standards Compliance

This section describes how MySQL relates to the ANSI/ISO SQL standards. MySQL Server has many
extensions to the SQL standard, and here you can find out what they are and how to use them. You can
also find information about functionality missing from MySQL Server, and how to work around some of the
differences.

The SQL standard has been evolving since 1986 and several versions exist. In this manual, “SQL-92”
refers to the standard released in 1992. “SQL:1999”, “SQL:2003”, “SQL:2008”, and “SQL:2011” refer to the
versions of the standard released in the corresponding years, with the last being the most recent version.
We use the phrase “the SQL standard” or “standard SQL” to mean the current version of the SQL Standard
at any time.

One of our main goals with the product is to continue to work toward compliance with the SQL standard,
but without sacrificing speed or reliability. We are not afraid to add extensions to SQL or support for non-
SQL features if this greatly increases the usability of MySQL Server for a large segment of our user base.
The HANDLER interface is an example of this strategy. See Section 13.2.4, “HANDLER Statement”.

We continue to support transactional and nontransactional databases to satisfy both mission-critical 24/7
usage and heavy Web or logging usage.

MySQL Server was originally designed to work with medium-sized databases (10-100 million rows,
or about 100MB per table) on small computer systems. Today MySQL Server handles terabyte-sized
databases, but the code can also be compiled in a reduced version suitable for hand-held and embedded
devices. The compact design of the MySQL server makes development in both directions possible without
any conflicts in the source tree.

We are not targeting real-time support, although MySQL replication capabilities offer significant
functionality.

MySQL supports ODBC levels 0 to 3.51.

MySQL supports high-availability database clustering using the NDBCLUSTER storage engine. See
Chapter 21, MySQL NDB Cluster 7.5 and NDB Cluster 7.6.

We implement XML functionality which supports most of the W3C XPath standard. See Section 12.11,
“XML Functions”.

MySQL (5.7.8 and later) supports a native JSON data type as defined by RFC 7159, and based on the
ECMAScript standard (ECMA-262). See Section 11.5, “The JSON Data Type”. MySQL also implements
a subset of the SQL/JSON functions specified by a pre-publication draft of the SQL:2016 standard; see
Section 12.17, “JSON Functions”, for more information.

Selecting SQL Modes

The MySQL server can operate in different SQL modes, and can apply these modes differently for different
clients, depending on the value of the sql_mode system variable. DBAs can set the global SQL mode to
match site server operating requirements, and each application can set its session SQL mode to its own
requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it
easier to use MySQL in different environments and to use MySQL together with other database servers.

For more information on setting the SQL mode, see Section 5.1.10, “Server SQL Modes”.

46

Running MySQL in ANSI Mode

Running MySQL in ANSI Mode

To run MySQL Server in ANSI mode, start mysqld with the --ansi option. Running the server in ANSI
mode is the same as starting it with the following options:

--transaction-isolation=SERIALIZABLE --sql-mode=ANSI

To achieve the same effect at runtime, execute these two statements:

SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET GLOBAL sql_mode = 'ANSI';

You can see that setting the sql_mode system variable to 'ANSI' enables all SQL mode options that are
relevant for ANSI mode as follows:

mysql> SET GLOBAL sql_mode='ANSI';
mysql> SELECT @@GLOBAL.sql_mode;
        -> 'REAL_AS_FLOAT,PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ANSI'

Running the server in ANSI mode with --ansi is not quite the same as setting the SQL mode to 'ANSI'
because the --ansi option also sets the transaction isolation level.

See Section 5.1.6, “Server Command Options”.

1.6.1 MySQL Extensions to Standard SQL

MySQL Server supports some extensions that are likely not to be found in other SQL DBMSs. Be warned
that if you use them, your code is not portable to other SQL servers. In some cases, you can write code
that includes MySQL extensions, but is still portable, by using comments of the following form:

/*! MySQL-specific code */

In this case, MySQL Server parses and executes the code within the comment as it would any other SQL
statement, but other SQL servers ignore the extensions. For example, MySQL Server recognizes the
STRAIGHT_JOIN keyword in the following statement, but other servers do not:

SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...

If you add a version number after the ! character, the syntax within the comment is executed only if the
MySQL version is greater than or equal to the specified version number. The KEY_BLOCK_SIZE clause in
the following comment is executed only by servers from MySQL 5.1.10 or higher:

CREATE TABLE t1(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024 */;

The following descriptions list MySQL extensions, organized by category.

• Organization of data on disk

MySQL Server maps each database to a directory under the MySQL data directory, and maps tables
within a database to file names in the database directory. This has a few implications:

•     Database and table names are case-sensitive in MySQL Server on operating systems that

have case-sensitive file names (such as most Unix systems). See Section 9.2.3, “Identifier Case
Sensitivity”.

• You can use standard system commands to back up, rename, move, delete, and copy tables that

are managed by the MyISAM storage engine. For example, it is possible to rename a MyISAM table
by renaming the .MYD, .MYI, and .frm files to which the table corresponds. (Nevertheless, it is

47

MySQL Extensions to Standard SQL

preferable to use RENAME TABLE or ALTER TABLE ... RENAME and let the server rename the
files.)

• General language syntax

• By default, strings can be enclosed by " as well as '. If the ANSI_QUOTES SQL mode is enabled,
strings can be enclosed only by ' and the server interprets strings enclosed by " as identifiers.

• \ is the escape character in strings.

• In SQL statements, you can access tables from different databases with the db_name.tbl_name

syntax. Some SQL servers provide the same functionality but call this User space. MySQL
Server does not support tablespaces such as used in statements like this: CREATE TABLE
ralph.my_table ... IN my_tablespace.

• SQL statement syntax

• The ANALYZE TABLE, CHECK TABLE, OPTIMIZE TABLE, and REPAIR TABLE statements.

• The CREATE DATABASE, DROP DATABASE, and ALTER DATABASE statements. See Section 13.1.11,

“CREATE DATABASE Statement”, Section 13.1.22, “DROP DATABASE Statement”, and
Section 13.1.1, “ALTER DATABASE Statement”.

• The DO statement.

• EXPLAIN SELECT to obtain a description of how tables are processed by the query optimizer.

• The FLUSH and RESET statements.

• The SET statement. See Section 13.7.4.1, “SET Syntax for Variable Assignment”.

• The SHOW statement. See Section 13.7.5, “SHOW Statements”. The information produced by many of
the MySQL-specific SHOW statements can be obtained in more standard fashion by using SELECT to
query INFORMATION_SCHEMA. See Chapter 24, INFORMATION_SCHEMA Tables.

•   Use of LOAD DATA. In many cases, this syntax is compatible with Oracle LOAD DATA. See

Section 13.2.6, “LOAD DATA Statement”.

• Use of RENAME TABLE. See Section 13.1.33, “RENAME TABLE Statement”.

• Use of REPLACE instead of DELETE plus INSERT. See Section 13.2.8, “REPLACE Statement”.

• Use of CHANGE col_name, DROP col_name, or DROP INDEX, IGNORE or RENAME in ALTER TABLE
statements. Use of multiple ADD, ALTER, DROP, or CHANGE clauses in an ALTER TABLE statement.
See Section 13.1.8, “ALTER TABLE Statement”.

• Use of index names, indexes on a prefix of a column, and use of INDEX or KEY in CREATE TABLE

statements. See Section 13.1.18, “CREATE TABLE Statement”.

• Use of TEMPORARY or IF NOT EXISTS with CREATE TABLE.

• Use of IF EXISTS with DROP TABLE and DROP DATABASE.

• The capability of dropping multiple tables with a single DROP TABLE statement.

• The ORDER BY and LIMIT clauses of the UPDATE and DELETE statements.

• INSERT INTO tbl_name SET col_name = ... syntax.

48

MySQL Extensions to Standard SQL

• The DELAYED clause of the INSERT and REPLACE statements.

• The LOW_PRIORITY clause of the INSERT, REPLACE, DELETE, and UPDATE statements.

• Use of INTO OUTFILE or INTO DUMPFILE in SELECT statements. See Section 13.2.9, “SELECT

Statement”.

• Options such as STRAIGHT_JOIN or SQL_SMALL_RESULT in SELECT statements.

• You don't need to name all selected columns in the GROUP BY clause. This gives better performance

for some very specific, but quite normal queries. See Section 12.19, “Aggregate Functions”.

• You can specify ASC and DESC with GROUP BY, not just with ORDER BY.

• The ability to set variables in a statement with the := assignment operator. See Section 9.4, “User-

Defined Variables”.

• Data types

• The MEDIUMINT, SET, and ENUM data types, and the various BLOB and TEXT data types.

• The AUTO_INCREMENT, BINARY, NULL, UNSIGNED, and ZEROFILL data type attributes.

• Functions and operators

• To make it easier for users who migrate from other SQL environments, MySQL Server supports

aliases for many functions. For example, all string functions support both standard SQL syntax and
ODBC syntax.

• MySQL Server understands the || and && operators to mean logical OR and AND, as in the C

programming language. In MySQL Server, || and OR are synonyms, as are && and AND. Because
of this nice syntax, MySQL Server does not support the standard SQL || operator for string
concatenation; use CONCAT() instead. Because CONCAT() takes any number of arguments, it is easy
to convert use of the || operator to MySQL Server.

• Use of COUNT(DISTINCT value_list) where value_list has more than one element.

• String comparisons are case-insensitive by default, with sort ordering determined by the collation of
the current character set, which is latin1 (cp1252 West European) by default. To perform case-
sensitive comparisons instead, you should declare your columns with the BINARY attribute or use the
BINARY cast, which causes comparisons to be done using the underlying character code values rather
than a lexical ordering.

•   The % operator is a synonym for MOD(). That is, N % M is equivalent to MOD(N,M). % is supported

for C programmers and for compatibility with PostgreSQL.

• The =, <>, <=, <, >=, >, <<, >>, <=>, AND, OR, or LIKE operators may be used in expressions in the

output column list (to the left of the FROM) in SELECT statements. For example:

mysql> SELECT col1=1 AND col2=2 FROM my_table;

• The LAST_INSERT_ID() function returns the most recent AUTO_INCREMENT value. See

Section 12.15, “Information Functions”.

• LIKE is permitted on numeric values.

• The REGEXP and NOT REGEXP extended regular expression operators.

49

MySQL Differences from Standard SQL

• CONCAT() or CHAR() with one argument or more than two arguments. (In MySQL Server, these

functions can take a variable number of arguments.)

• The BIT_COUNT(), CASE, ELT(), FROM_DAYS(), FORMAT(), IF(), PASSWORD(), ENCRYPT(),
MD5(), ENCODE(), DECODE(), PERIOD_ADD(), PERIOD_DIFF(), TO_DAYS(), and WEEKDAY()
functions.

• Use of TRIM() to trim substrings. Standard SQL supports removal of single characters only.

• The GROUP BY functions STD(), BIT_OR(), BIT_AND(), BIT_XOR(), and GROUP_CONCAT(). See

Section 12.19, “Aggregate Functions”.

1.6.2 MySQL Differences from Standard SQL

We try to make MySQL Server follow the ANSI SQL standard and the ODBC SQL standard, but MySQL
Server performs operations differently in some cases:

• There are several differences between the MySQL and standard SQL privilege systems. For example, in
MySQL, privileges for a table are not automatically revoked when you delete a table. You must explicitly
issue a REVOKE statement to revoke privileges for a table. For more information, see Section 13.7.1.6,
“REVOKE Statement”.

• The CAST() function does not support cast to REAL or BIGINT. See Section 12.10, “Cast Functions and

Operators”.

1.6.2.1 SELECT INTO TABLE Differences

MySQL Server does not support the SELECT ... INTO TABLE Sybase SQL extension. Instead, MySQL
Server supports the INSERT INTO ... SELECT standard SQL syntax, which is basically the same thing.
See Section 13.2.5.1, “INSERT ... SELECT Statement”. For example:

INSERT INTO tbl_temp2 (fld_id)
    SELECT tbl_temp1.fld_order_id
    FROM tbl_temp1 WHERE tbl_temp1.fld_order_id > 100;

Alternatively, you can use SELECT ... INTO OUTFILE or CREATE TABLE ... SELECT.

You can use SELECT ... INTO with user-defined variables. The same syntax can also be used inside
stored routines using cursors and local variables. See Section 13.2.9.1, “SELECT ... INTO Statement”.

1.6.2.2 UPDATE Differences

If you access a column from the table to be updated in an expression, UPDATE uses the current value of
the column. The second assignment in the following statement sets col2 to the current (updated) col1
value, not the original col1 value. The result is that col1 and col2 have the same value. This behavior
differs from standard SQL.

UPDATE t1 SET col1 = col1 + 1, col2 = col1;

1.6.2.3 FOREIGN KEY Constraint Differences

The MySQL implementation of foreign key constraints differs from the SQL standard in the following key
respects:

• If there are several rows in the parent table with the same referenced key value, InnoDB performs a

foreign key check as if the other parent rows with the same key value do not exist. For example, if you

50

MySQL Differences from Standard SQL

define a RESTRICT type constraint, and there is a child row with several parent rows, InnoDB does not
permit the deletion of any of the parent rows.

• If ON UPDATE CASCADE or ON UPDATE SET NULL recurses to update the same table it has previously

updated during the same cascade, it acts like RESTRICT. This means that you cannot use self-
referential ON UPDATE CASCADE or ON UPDATE SET NULL operations. This is to prevent infinite
loops resulting from cascaded updates. A self-referential ON DELETE SET NULL, on the other hand, is
possible, as is a self-referential ON DELETE CASCADE. Cascading operations may not be nested more
than 15 levels deep.

• In an SQL statement that inserts, deletes, or updates many rows, foreign key constraints (like unique
constraints) are checked row-by-row. When performing foreign key checks, InnoDB sets shared row-
level locks on child or parent records that it must examine. MySQL checks foreign key constraints
immediately; the check is not deferred to transaction commit. According to the SQL standard, the
default behavior should be deferred checking. That is, constraints are only checked after the entire SQL
statement has been processed. This means that it is not possible to delete a row that refers to itself
using a foreign key.

• No storage engine, including InnoDB, recognizes or enforces the MATCH clause used in referential-

integrity constraint definitions. Use of an explicit MATCH clause does not have the specified effect, and it
causes ON DELETE and ON UPDATE clauses to be ignored. Specifying the MATCH should be avoided.

The MATCH clause in the SQL standard controls how NULL values in a composite (multiple-column)
foreign key are handled when comparing to a primary key in the referenced table. MySQL essentially
implements the semantics defined by MATCH SIMPLE, which permits a foreign key to be all or partially
NULL. In that case, a (child table) row containing such a foreign key can be inserted even though it does
not match any row in the referenced (parent) table. (It is possible to implement other semantics using
triggers.)

• MySQL requires that the referenced columns be indexed for performance reasons. However, MySQL
does not enforce a requirement that the referenced columns be UNIQUE or be declared NOT NULL.

A FOREIGN KEY constraint that references a non-UNIQUE key is not standard SQL but rather an
InnoDB extension. The NDB storage engine, on the other hand, requires an explicit unique key (or
primary key) on any column referenced as a foreign key.

The handling of foreign key references to nonunique keys or keys that contain NULL values is not well
defined for operations such as UPDATE or DELETE CASCADE. You are advised to use foreign keys that
reference only UNIQUE (including PRIMARY) and NOT NULL keys.

• For storage engines that do not support foreign keys (such as MyISAM), MySQL Server parses and

ignores foreign key specifications.

• MySQL parses but ignores “inline REFERENCES specifications” (as defined in the SQL standard) where
the references are defined as part of the column specification. MySQL accepts REFERENCES clauses
only when specified as part of a separate FOREIGN KEY specification.

Defining a column to use a REFERENCES tbl_name(col_name) clause has no actual effect and
serves only as a memo or comment to you that the column which you are currently defining is intended
to refer to a column in another table. It is important to realize when using this syntax that:

• MySQL does not perform any sort of check to make sure that col_name actually exists in tbl_name

(or even that tbl_name itself exists).

• MySQL does not perform any sort of action on tbl_name such as deleting rows in response to

actions taken on rows in the table which you are defining; in other words, this syntax induces no ON

51

MySQL Differences from Standard SQL

DELETE or ON UPDATE behavior whatsoever. (Although you can write an ON DELETE or ON UPDATE
clause as part of the REFERENCES clause, it is also ignored.)

• This syntax creates a column; it does not create any sort of index or key.

You can use a column so created as a join column, as shown here:

CREATE TABLE person (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name CHAR(60) NOT NULL,
    PRIMARY KEY (id)
);

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

52

How MySQL Deals with Constraints

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
`color` enum('red','blue','orange','white','black') NOT NULL,
`owner` smallint(5) unsigned NOT NULL,
PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1

For information about foreign key constraints, see Section 13.1.18.5, “FOREIGN KEY Constraints”.

1.6.2.4 '--' as the Start of a Comment

Standard SQL uses the C syntax /* this is a comment */ for comments, and MySQL Server
supports this syntax as well. MySQL also support extensions to this syntax that enable MySQL-specific
SQL to be embedded in the comment; see Section 9.6, “Comments”.

MySQL Server also uses # as the start comment character. This is nonstandard.

Standard SQL also uses “--” as a start-comment sequence. MySQL Server supports a variant of the --
comment style; the -- start-comment sequence is accepted as such, but must be followed by a whitespace
character such as a space or newline. The space is intended to prevent problems with generated SQL
queries that use constructs such as the following, which updates the balance to reflect a charge:

UPDATE account SET balance=balance-charge
WHERE account_id=user_id

Consider what happens when charge has a negative value such as -1, which might be the case when an
amount is credited to the account. In this case, the generated statement looks like this:

UPDATE account SET balance=balance--1
WHERE account_id=5752;

balance--1 is valid standard SQL, but -- is interpreted as the start of a comment, and part of the
expression is discarded. The result is a statement that has a completely different meaning than intended:

UPDATE account SET balance=balance
WHERE account_id=5752;

This statement produces no change in value at all. To keep this from happening, MySQL requires a
whitespace character following the -- for it to be recognized as a start-comment sequence in MySQL
Server, so that an expression such as balance--1 is always safe to use.

1.6.3 How MySQL Deals with Constraints

MySQL enables you to work both with transactional tables that permit rollback and with nontransactional
tables that do not. Because of this, constraint handling is a bit different in MySQL than in other DBMSs. We

53

How MySQL Deals with Constraints

must handle the case when you have inserted or updated a lot of rows in a nontransactional table for which
changes cannot be rolled back when an error occurs.

The basic philosophy is that MySQL Server tries to produce an error for anything that it can detect while
parsing a statement to be executed, and tries to recover from any errors that occur while executing the
statement. We do this in most cases, but not yet for all.

The options MySQL has when an error occurs are to stop the statement in the middle or to recover as well
as possible from the problem and continue. By default, the server follows the latter course. This means, for
example, that the server may coerce invalid values to the closest valid values.

Several SQL mode options are available to provide greater control over handling of bad data values
and whether to continue statement execution or abort when errors occur. Using these options, you can
configure MySQL Server to act in a more traditional fashion that is like other DBMSs that reject improper
input. The SQL mode can be set globally at server startup to affect all clients. Individual clients can
set the SQL mode at runtime, which enables each client to select the behavior most appropriate for its
requirements. See Section 5.1.10, “Server SQL Modes”.

The following sections describe how MySQL Server handles different types of constraints.

1.6.3.1 PRIMARY KEY and UNIQUE Index Constraints

Normally, errors occur for data-change statements (such as INSERT or UPDATE) that would violate
primary-key, unique-key, or foreign-key constraints. If you are using a transactional storage engine such
as InnoDB, MySQL automatically rolls back the statement. If you are using a nontransactional storage
engine, MySQL stops processing the statement at the row for which the error occurred and leaves any
remaining rows unprocessed.

MySQL supports an IGNORE keyword for INSERT, UPDATE, and so forth. If you use it, MySQL ignores
primary-key or unique-key violations and continues processing with the next row. See the section for the
statement that you are using (Section 13.2.5, “INSERT Statement”, Section 13.2.11, “UPDATE Statement”,
and so forth).

You can get information about the number of rows actually inserted or updated with the mysql_info() C
API function. You can also use the SHOW WARNINGS statement. See mysql_info(), and Section 13.7.5.40,
“SHOW WARNINGS Statement”.

InnoDB and NDB tables support foreign keys. See Section 1.6.3.2, “FOREIGN KEY Constraints”.

1.6.3.2 FOREIGN KEY Constraints

Foreign keys let you cross-reference related data across tables, and foreign key constraints help keep this
spread-out data consistent.

MySQL supports ON UPDATE and ON DELETE foreign key references in CREATE TABLE and ALTER
TABLE statements. The available referential actions are RESTRICT (the default), CASCADE, SET NULL,
and NO ACTION.

SET DEFAULT is also supported by the MySQL Server but is currently rejected as invalid by InnoDB.
Since MySQL does not support deferred constraint checking, NO ACTION is treated as RESTRICT. For the
exact syntax supported by MySQL for foreign keys, see Section 13.1.18.5, “FOREIGN KEY Constraints”.

MATCH FULL, MATCH PARTIAL, and MATCH SIMPLE are allowed, but their use should be avoided,
as they cause the MySQL Server to ignore any ON DELETE or ON UPDATE clause used in the same
statement. MATCH options do not have any other effect in MySQL, which in effect enforces MATCH SIMPLE
semantics full-time.

54

How MySQL Deals with Constraints

MySQL requires that foreign key columns be indexed; if you create a table with a foreign key constraint but
no index on a given column, an index is created.

You can obtain information about foreign keys from the Information Schema KEY_COLUMN_USAGE table.
An example of a query against this table is shown here:

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

Information about foreign keys on InnoDB tables can also be found in the INNODB_SYS_FOREIGN and
INNODB_SYS_FOREIGN_COLS tables, in the INFORMATION_SCHEMA database.

InnoDB and NDB tables support foreign keys.

1.6.3.3 Constraints on Invalid Data

MySQL 5.7.5 and later uses strict SQL mode by default, which treats invalid values such that the server
rejects them and aborts the statement in which they occur (see Section 5.1.10, “Server SQL Modes”).
Previously, MySQL was much more forgiving of incorrect values used in data entry; this now requires
disabling of strict mode, which is not recommended. The remainder of this section discusses the old
behavior followed by MySQL when strict mode has been disabled.

If you are not using strict mode, then whenever you insert an “incorrect” value into a column, such as
a NULL into a NOT NULL column or a too-large numeric value into a numeric column, MySQL sets the
column to the “best possible value” instead of producing an error: The following rules describe in more
detail how this works:

• If you try to store an out of range value into a numeric column, MySQL Server instead stores zero, the

smallest possible value, or the largest possible value, whichever is closest to the invalid value.

• For strings, MySQL stores either the empty string or as much of the string as can be stored in the

column.

• If you try to store a string that does not start with a number into a numeric column, MySQL Server stores

0.

• Invalid values for ENUM and SET columns are handled as described in Section 1.6.3.4, “ENUM and SET

Constraints”.

• MySQL permits you to store certain incorrect date values into DATE and DATETIME columns (such

as '2000-02-31' or '2000-02-00'). In this case, when an application has not enabled strict SQL
mode, it up to the application to validate the dates before storing them. If MySQL can store a date value
and retrieve exactly the same value, MySQL stores it as given. If the date is totally wrong (outside the
server's ability to store it), the special “zero” date value '0000-00-00' is stored in the column instead.

• If you try to store NULL into a column that does not take NULL values, an error occurs for single-

row INSERT statements. For multiple-row INSERT statements or for INSERT INTO ... SELECT
statements, MySQL Server stores the implicit default value for the column data type. In general, this is
0 for numeric types, the empty string ('') for string types, and the “zero” value for date and time types.
Implicit default values are discussed in Section 11.6, “Data Type Default Values”.

55

How MySQL Deals with Constraints

• If an INSERT statement specifies no value for a column, MySQL inserts its default value if the column
definition includes an explicit DEFAULT clause. If the definition has no such DEFAULT clause, MySQL
inserts the implicit default value for the column data type.

The reason for using the preceding rules when strict mode is not in effect is that we cannot check these
conditions until the statement has begun executing. We cannot just roll back if we encounter a problem
after updating a few rows, because the storage engine may not support rollback. The option of terminating
the statement is not that good; in this case, the update would be “half done,” which is probably the
worst possible scenario. In this case, it is better to “do the best you can” and then continue as if nothing
happened.

You can select stricter treatment of input values by using the STRICT_TRANS_TABLES or
STRICT_ALL_TABLES SQL modes:

SET sql_mode = 'STRICT_TRANS_TABLES';
SET sql_mode = 'STRICT_ALL_TABLES';

STRICT_TRANS_TABLES enables strict mode for transactional storage engines, and also to some extent
for nontransactional engines. It works like this:

• For transactional storage engines, bad data values occurring anywhere in a statement cause the

statement to abort and roll back.

• For nontransactional storage engines, a statement aborts if the error occurs in the first row to be inserted

or updated. (When the error occurs in the first row, the statement can be aborted to leave the table
unchanged, just as for a transactional table.) Errors in rows after the first do not abort the statement,
because the table has already been changed by the first row. Instead, bad data values are adjusted
and result in warnings rather than errors. In other words, with STRICT_TRANS_TABLES, a wrong value
causes MySQL to roll back all updates done so far, if that can be done without changing the table. But
once the table has been changed, further errors result in adjustments and warnings.

For even stricter checking, enable STRICT_ALL_TABLES. This is the same as STRICT_TRANS_TABLES
except that for nontransactional storage engines, errors abort the statement even for bad data in rows
following the first row. This means that if an error occurs partway through a multiple-row insert or update
for a nontransactional table, a partial update results. Earlier rows are inserted or updated, but those from
the point of the error on are not. To avoid this for nontransactional tables, either use single-row statements
or else use STRICT_TRANS_TABLES if conversion warnings rather than errors are acceptable. To avoid
problems in the first place, do not use MySQL to check column content. It is safest (and often faster) to let
the application ensure that it passes only valid values to the database.

With either of the strict mode options, you can cause errors to be treated as warnings by using INSERT
IGNORE or UPDATE IGNORE rather than INSERT or UPDATE without IGNORE.

1.6.3.4 ENUM and SET Constraints

ENUM and SET columns provide an efficient way to define columns that can contain only a given set of
values. See Section 11.3.5, “The ENUM Type”, and Section 11.3.6, “The SET Type”.

Unless strict mode is disabled (not recommended, but see Section 5.1.10, “Server SQL Modes”), the
definition of a ENUM or SET column acts as a constraint on values entered into the column. An error occurs
for values that do not satisfy these conditions:

• An ENUM value must be one of those listed in the column definition, or the internal numeric equivalent
thereof. The value cannot be the error value (that is, 0 or the empty string). For a column defined as
ENUM('a','b','c'), values such as '', 'd', or 'ax' are invalid and are rejected.

56

How MySQL Deals with Constraints

• A SET value must be the empty string or a value consisting only of the values listed in the column

definition separated by commas. For a column defined as SET('a','b','c'), values such as 'd' or
'a,b,c,d' are invalid and are rejected.

Errors for invalid values can be suppressed in strict mode if you use INSERT IGNORE or UPDATE
IGNORE. In this case, a warning is generated rather than an error. For ENUM, the value is inserted as the
error member (0). For SET, the value is inserted as given except that any invalid substrings are deleted.
For example, 'a,x,b,y' results in a value of 'a,b'.

57

58

