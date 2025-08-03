Upgrade Paths

• Review Section 3.5, “Changes in MySQL 8.4” for changes that you should be aware of before

upgrading. Some changes may require action.

• Review Section 1.4, “What Is New in MySQL 8.4 since MySQL 8.0” for deprecated and removed
features. An upgrade may require changes with respect to those features if you use any of them.

• Review Section 1.5, “Server and Status Variables and Options Added, Deprecated, or Removed
in MySQL 8.4 since 8.0”. If you use deprecated or removed variables, an upgrade may require
configuration changes.

• Review the Release Notes for information about fixes, changes, and new features.

• If you use replication, review Section 19.5.3, “Upgrading or Downgrading a Replication Topology”.

• Review Section 3.3, “Upgrade Best Practices” and plan accordingly.

• Upgrade procedures vary by platform and how the initial installation was performed. Use the

procedure that applies to your current MySQL installation:

• For binary and package-based installations on non-Windows platforms, refer to Section 3.7,

“Upgrading MySQL Binary or Package-based Installations on Unix/Linux”.

Note

For supported Linux distributions, the preferred method for upgrading
package-based installations is to use the MySQL software repositories
(MySQL Yum Repository, MySQL APT Repository, and MySQL SLES
Repository).

• For installations on an Enterprise Linux platform or Fedora using the MySQL Yum Repository,

refer to Section 3.8, “Upgrading MySQL with the MySQL Yum Repository”.

• For installations on Ubuntu using the MySQL APT repository, refer to Section 3.9, “Upgrading

MySQL with the MySQL APT Repository”.

• For installations on SLES using the MySQL SLES repository, refer to Section 3.10, “Upgrading

MySQL with the MySQL SLES Repository”.

• For installations performed using Docker, refer to Section 3.12, “Upgrading a Docker Installation of

MySQL”.

• For installations on Windows, refer to Section 3.11, “Upgrading MySQL on Windows”.

• If your MySQL installation contains a large amount of data that might take a long time to convert

after an in-place upgrade, it may be useful to create a test instance for assessing the conversions
that are required and the work involved to perform them. To create a test instance, make a copy of
your MySQL instance that contains the mysql database and other databases without the data. Run
the upgrade procedure on the test instance to assess the work involved to perform the actual data
conversion.

• Rebuilding and reinstalling MySQL language interfaces is recommended when you install or upgrade
to a new release of MySQL. This applies to MySQL interfaces such as PHP mysql extensions and
the Perl DBD::mysql module.

3.2 Upgrade Paths

Notes

• Make sure you understand the MySQL release model for MySQL for MySQL
long long-term support (LTS) and Innovation versions before proceeding with
a downgrade.

224

Run Applications in a Test Environment

You are ready to upgrade when the upgrade checking utility no longer reports any issues.

Run Applications in a Test Environment

After completing the upgrade checker's requirements, next test your applications on the new target
MySQL server. Check for errors and warnings in the MySQL error log and application logs.

Benchmark Applications and Workload Performance

We recommend benchmarking your own applications and workloads by comparing how they perform
using the previous and new versions of MySQL. Usually, newer MySQL versions add features and
improve performance but there are cases where an upgrade might run slower for specific queries.
Possible issues resulting in performance regressions:

• Prior server configuration is not optimal for newer version

• Changes to data types

• Additional storage required by Multi-byte character set support

• Storage engines changes

• Dropped or changed indexes

• Stronger encryption

• Stronger authentication

• SQL optimizer changes

• Newer version of MySQL require additional memory

• Physical or Virtual Hardware is slower - compute or storage

For related information and potential mitigation techniques, see Valid Performance Regressions.

Run Both MySQL Versions in Parallel

To minimize risk, it is best keep the current system running while running the upgraded system in
parallel.

Run Final Test Upgrade

Practice and do a run though prior to upgrading your production server. Thoroughly test the upgrade
procedures before upgrading a production system.

Check MySQL Backup

Check that the full backup exists and is viable before performing the upgrade.

Upgrade Production Server

You are ready to complete the upgrade.

Enterprise Support

If you're a MySQL Enterprise Edition customer, you can also contact the MySQL Support Team experts
with any questions you may have.

227

What the MySQL Upgrade Process Upgrades

3.4 What the MySQL Upgrade Process Upgrades

Installing a new version of MySQL may require upgrading these parts of the existing installation:

• The mysql system schema, which contains tables that store information required by the MySQL

server as it runs (see Section 7.3, “The mysql System Schema”). mysql schema tables fall into two
broad categories:

• Data dictionary tables, which store database object metadata.

• System tables (that is, the remaining non-data dictionary tables), which are used for other

operational purposes.

• Other schemas, some of which are built in and may be considered “owned” by the server, and others

which are not:

• The performance_schema, INFORMATION_SCHEMA, ndbinfo, and sys schemas.

• User schemas.

Two distinct version numbers are associated with parts of the installation that may require upgrading:

• The data dictionary version. This applies to the data dictionary tables.

• The server version, also known as the MySQL version. This applies to the system tables and objects

in other schemas.

In both cases, the actual version applicable to the existing MySQL installation is stored in the data
dictionary, and the current expected version is compiled into the new version of MySQL. When an
actual version is lower than the current expected version, those parts of the installation associated with
that version must be upgraded to the current version. If both versions indicate an upgrade is needed,
the data dictionary upgrade must occur first.

As a reflection of the two distinct versions just mentioned, the upgrade occurs in two steps:

• Step 1: Data dictionary upgrade.

This step upgrades:

• The data dictionary tables in the mysql schema. If the actual data dictionary version is lower than
the current expected version, the server creates data dictionary tables with updated definitions,
copies persisted metadata to the new tables, atomically replaces the old tables with the new ones,
and reinitializes the data dictionary.

• The Performance Schema, INFORMATION_SCHEMA, and ndbinfo.

• Step 2: Server upgrade.

This step comprises all other upgrade tasks. If the server version of the existing MySQL installation is
lower than that of the new installed MySQL version, everything else must be upgraded:

• The system tables in the mysql schema (the remaining non-data dictionary tables).

• The sys schema.

• User schemas.

The data dictionary upgrade (step 1) is the responsibility of the server, which performs this task as
necessary at startup unless invoked with an option that prevents it from doing so. The option is --
upgrade=NONE.

If the data dictionary is out of date but the server is prevented from upgrading it, the server does not
run, and exits with an error instead. For example:

228

Changes in MySQL 8.4

To prevent table checking, start the server with the --upgrade=NONE or --upgrade=MINIMAL
option.

To force table checking, start the server with the --upgrade=FORCE option.

• Step 2 marks all checked and repaired tables with the current MySQL version number. This ensures
that the next time upgrade checking occurs with the same version of the server, it can be determined
whether there is any need to check or repair a given table again.

3.5 Changes in MySQL 8.4

Before upgrading to MySQL 8.4, review the changes described in the following sections to identify
those that apply to your current MySQL installation and applications.

• Incompatible Changes in MySQL 8.4

• Changed Server Defaults

In addition, you can consult the resources listed here:

• Section 1.4, “What Is New in MySQL 8.4 since MySQL 8.0”

• MySQL 8.4 Release Notes

Incompatible Changes in MySQL 8.4

This section contains information about incompatible changes in MySQL 8.4.

• Spatial indexes.

 When upgrading to MySQL 8.4.4 or later, it is recommended that you drop any

spatial indexes beforehand, then re-create them after the upgrade is complete. Alternatively, you can
drop and re-create such indexes immediately following the upgrade, but before making use of any of
the tables in which they occur.

For more information, see Section 13.4.10, “Creating Spatial Indexes”.

• WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS() function removed.

 The

WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS() SQL function, deprecated in MySQL
8.0 has been removed; attempting to invoke it now causes a syntax error. Use
WAIT_FOR_EXECUTED_GTID_SET() instead.

• authentication_fido and authentication_fido_client no longer available
 Due to upgrading the libfido2 library bundled with the server to

on some platforms.
version 1.13.0, which requires OpenSSL 1.1.1 or higher, the authentication_fido and
authentication_fido_client authentication plugins are no longer available on Enterprise
Linux 6, Enterprise Linux 7, Solaris 11, or SUSE Enterprise Linux 12.

• NULL disallowed for command-line options.

 Setting server variables equal to SQL NULL

on the command line is not supported. In MySQL 8.4, setting any of these to NULL is specifically
disallowed, and attempting to do is rejected with an error.

The following variables are excepted from this restriction: admin_ssl_ca, admin_ssl_capath,
admin_ssl_cert, admin_ssl_cipher, admin_tls_ciphersuites, admin_ssl_key,
admin_ssl_crl, admin_ssl_crlpath, basedir, character_sets_dir,
ft_stopword_file, group_replication_recovery_tls_ciphersuites,
init_file, lc_messages_dir, plugin_dir, relay_log, relay_log_info_file,
replica_load_tmpdir, ssl_ca, ssl_capath, ssl_cert, ssl_cipher, ssl_crl,
ssl_crlpath, ssl_key, socket, tls_ciphersuites, and tmpdir.

See also Section 7.1.8, “Server System Variables”.

230

Changed Server Defaults

For additional information about changes in MySQL 8.4, see Section 1.4, “What Is New in MySQL 8.4
since MySQL 8.0”.

Changed Server Defaults

This section contains information about MySQL server system variables whose default values have
changed in MySQL 8.4 as compared to MySQL 8.0.

System Variable

InnoDB changes

Old Default

New Default

innodb_adaptive_hash_indexON

innodb_buffer_pool_in_core_file

ON

OFF

OFF

innodb_buffer_pool_instancesinnodb_buffer_pool_size <

1GB: 1; otherwise: 8

innodb_buffer_pool_size
<= 1GB: 1; otherwise:
MIN( 0.5 *
(innodb_buffer_pool_size
/
innodb_buffer_pool_chunk_size),
0.25 * number_of_cpus)

innodb_change_buffering

all

none

innodb_doublewrite_files innodb_buffer_pool_instances
* 2

2

innodb_doublewrite_pages Value of

128

innodb_write_io_threads

innodb_flush_method

fsync

O_DIRECT if supported,
otherwise fsync

innodb_io_capacity

200

10000

innodb_io_capacity_max

MIN(2 *
innodb_io_capacity,
2000)

2 * innodb_io_capacity

innodb_log_buffer_size

16777216

innodb_numa_interleave

OFF

innodb_page_cleaners

4

innodb_parallel_read_threads4

innodb_purge_threads

4

67108864

ON

Value of
innodb_buffer_pool_instances

MIN(number_of_cpus / 8,
4)

If number_of_cpus <= 16: 1;
otherwise: 4

innodb_use_fdatasync

OFF

ON

Group Replication changes

group_replication_consistencyEVENTUAL

BEFORE_ON_PRIMARY_FAILOVER

READ_ONLY
group_replication_exit_state_action

OFFLINE_MODE

Temporary table changes

temptable_max_mmap

temptable_max_ram

1073741824

1073741824

0

3% of total memory within a
range of 1-4 (GB)

temptable_use_mmap

ON

OFF

For more information about options or variables which have been added, see Option and Variable
Changes for MySQL 8.4, in the MySQL Server Version Reference.

231

In-Place Upgrade

• In-Place Upgrade

• Logical Upgrade

• MySQL Cluster Upgrade

In-Place Upgrade

An in-place upgrade involves shutting down the old MySQL server, replacing the old MySQL binaries
or packages with the new ones, restarting MySQL on the existing data directory, and upgrading any
remaining parts of the existing installation that require upgrading. For details about what may need
upgrading, see Section 3.4, “What the MySQL Upgrade Process Upgrades”.

Note

If you are upgrading an installation originally produced by installing multiple
RPM packages, upgrade all the packages, not just some. For example, if you
previously installed the server and client RPMs, do not upgrade just the server
RPM.

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown.
On these platforms, mysqld_safe is not installed. In such cases, use systemd
for server startup and shutdown instead of the methods used in the following
instructions. See Section 2.5.9, “Managing MySQL Server with systemd”.

For upgrades to MySQL Cluster installations, see also MySQL Cluster Upgrade.

To perform an in-place upgrade:

1. Review the information in Section 3.1, “Before You Begin”.

2. Ensure the upgrade readiness of your installation by completing the preliminary checks in

Section 3.6, “Preparing Your Installation for Upgrade”.

3.

If you use XA transactions with InnoDB, run XA RECOVER before upgrading to check for
uncommitted XA transactions. If results are returned, either commit or rollback the XA transactions
by issuing an XA COMMIT or XA ROLLBACK statement.

4.

If you normally run your MySQL server configured with innodb_fast_shutdown set to 2 (cold
shutdown), configure it to perform a fast or slow shutdown by executing either of these statements:

SET GLOBAL innodb_fast_shutdown = 1; -- fast shutdown
SET GLOBAL innodb_fast_shutdown = 0; -- slow shutdown

With a fast or slow shutdown, InnoDB leaves its undo logs and data files in a state that can be
dealt with in case of file format differences between releases.

5. Shut down the old MySQL server. For example:

mysqladmin -u root -p shutdown

6. Upgrade the MySQL binaries or packages. If upgrading a binary installation, unpack the new

MySQL binary distribution package. See Obtain and Unpack the Distribution. For package-based
installations, install the new packages.

7. Start the MySQL 8.4 server, using the existing data directory. For example:

mysqld_safe --user=mysql --datadir=/path/to/existing-datadir &

If there are encrypted InnoDB tablespaces, use the --early-plugin-load option to load the
keyring plugin.

235

Logical Upgrade

When you start the MySQL 8.4 server, it automatically detects whether data dictionary tables are
present. If not, the server creates them in the data directory, populates them with metadata, and
then proceeds with its normal startup sequence. During this process, the server upgrades metadata
for all database objects, including databases, tablespaces, system and user tables, views, and
stored programs (stored procedures and functions, triggers, and Event Scheduler events). The
server also removes files that previously were used for metadata storage. For example, after
upgrading from MySQL 8.3 to MySQL 8.4, you may notice that tables no longer have .frm files.

If this step fails, the server reverts all changes to the data directory. In this case, you should remove
all redo log files, start your MySQL 8.3 server on the same data directory, and fix the cause of any
errors. Then perform another slow shutdown of the 8.3 server and start the MySQL 8.4 server to try
again.

8.

In the previous step, the server upgrades the data dictionary as necessary, making any changes
required in the mysql system database between MySQL 8.3 and MySQL 8.4, so that you
can take advantage of new privileges or capabilities. It also brings the Performance Schema,
INFORMATION_SCHEMA, and sys databases up to date for MySQL 8.4, and examines all user
databases for incompatibilities with the current version of MySQL.

Note

The upgrade process does not upgrade the contents of the time zone tables.
For upgrade instructions, see Section 7.1.15, “MySQL Server Time Zone
Support”.

Logical Upgrade

A logical upgrade involves exporting SQL from the old MySQL instance using a backup or export utility
such as mysqldump, installing the new MySQL server, and applying the SQL to your new MySQL
instance. For details about what may need upgrading, see Section 3.4, “What the MySQL Upgrade
Process Upgrades”.

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown.
On these platforms, mysqld_safe is not installed. In such cases, use systemd
for server startup and shutdown instead of the methods used in the following
instructions. See Section 2.5.9, “Managing MySQL Server with systemd”.

Warning

Applying SQL extracted from a previous MySQL release to a new MySQL
release may result in errors due to incompatibilities introduced by new,
changed, deprecated, or removed features and capabilities. Consequently, SQL
extracted from a previous MySQL release may require modification to enable a
logical upgrade.

To identify incompatibilities before upgrading to the latest MySQL 8.4 release,
perform the steps described in Section 3.6, “Preparing Your Installation for
Upgrade”.

To perform a logical upgrade:

1. Review the information in Section 3.1, “Before You Begin”.

2. Export your existing data from the previous MySQL installation:

mysqldump -u root -p

236

MySQL Cluster Upgrade

mysqld_safe --user=mysql --datadir=/path/to/8.4-datadir --upgrade=FORCE &

Upon restart with --upgrade=FORCE, the server makes any changes required in the mysql
system schema between MySQL 8.3 and MySQL 8.4, so that you can take advantage of new
privileges or capabilities. It also brings the Performance Schema, INFORMATION_SCHEMA, and
sys schema up to date for MySQL 8.4, and examines all user schemas for incompatibilities with the
current version of MySQL.

Note

The upgrade process does not upgrade the contents of the time zone tables.
For upgrade instructions, see Section 7.1.15, “MySQL Server Time Zone
Support”.

MySQL Cluster Upgrade

The information in this section is an adjunct to the in-place upgrade procedure described in In-Place
Upgrade, for use if you are upgrading MySQL Cluster.

A MySQL Cluster upgrade can be performed as a regular rolling upgrade, following the usual three
ordered steps:

1. Upgrade MGM nodes.

2. Upgrade data nodes one at a time.

3. Upgrade API nodes one at a time (including MySQL servers).

There are two steps to upgrading each individual mysqld:

1.

Import the data dictionary.

Start the new server with the --upgrade=MINIMAL option to upgrade the data dictionary but not
the system tables.

The MySQL server must be connected to NDB for this phase to complete. If any NDB or NDBINFO
tables exist, and the server cannot connect to the cluster, it exits with an error message:

Failed to Populate DD tables.

2. Upgrade the system tables by restarting each individual mysqld without the --upgrade=MINIMAL

option.

3.8 Upgrading MySQL with the MySQL Yum Repository

For supported Yum-based platforms (see Section 2.5.1, “Installing MySQL on Linux Using the MySQL
Yum Repository”, for a list), you can perform an in-place upgrade for MySQL (that is, replacing the old
version and then running the new version using the old data files) with the MySQL Yum repository.

Notes

• An innovation series, such as MySQL 9.3, is in a separate track than an LTS

series, such as MySQL 8.4. The LTS series is active by default.

• Before performing any update to MySQL, follow carefully the instructions in

Chapter 3, Upgrading MySQL. Among other instructions discussed there, it is
especially important to back up your database before the update.

• The following instructions assume you have installed MySQL with the MySQL
Yum repository or with an RPM package directly downloaded from MySQL

238

Upgrading the Shared Client Libraries

For dnf-enabled platforms:

sudo dnf upgrade package-name

Upgrading the Shared Client Libraries

After updating MySQL using the Yum repository, applications compiled with older versions of the
shared client libraries should continue to work.

If you recompile applications and dynamically link them with the updated libraries:  As typical with new
versions of shared libraries where there are differences or additions in symbol versioning between
the newer and older libraries (for example, between the newer, standard 8.4 shared client libraries
and some older—prior or variant—versions of the shared libraries shipped natively by the Linux
distributions' software repositories, or from some other sources), any applications compiled using the
updated, newer shared libraries require those updated libraries on systems where the applications are
deployed. As expected, if those libraries are not in place, the applications requiring the shared libraries
fail. For this reason, be sure to deploy the packages for the shared libraries from MySQL on those
systems. To do this, add the MySQL Yum repository to the systems (see Adding the MySQL Yum
Repository) and install the latest shared libraries using the instructions given in Installing Additional
MySQL Products and Components with Yum.

3.9 Upgrading MySQL with the MySQL APT Repository

On Debian and Ubuntu platforms, to perform an in-place upgrade of MySQL and its components, use
the MySQL APT repository. See Upgrading MySQL with the MySQL APT Repository.

3.10 Upgrading MySQL with the MySQL SLES Repository

On the SUSE Linux Enterprise Server (SLES) platform, to perform an in-place upgrade of MySQL
and its components, use the MySQL SLES repository. See Upgrading MySQL with the MySQL SLES
Repository.

3.11 Upgrading MySQL on Windows

To upgrade MySQL on Windows, either download and execute the latest MySQL Server MSI or use
the Windows ZIP archive distribution.

Note

Unlike MySQL 8.4, MySQL 8.0 uses MySQL Installer to install and upgrade
MySQL Server along with most other MySQL products; but MySQL Installer
is not available with MySQL 8.1 and higher. However, the configuration
functionality used in MySQL Installer is available as of MySQL 8.1 using
Section 2.3.2, “Configuration: Using MySQL Configurator” that is bundled with
both the MSI and Zip archive.

The approach you select depends on how the existing installation was performed. Before proceeding,
review Chapter 3, Upgrading MySQL for additional information on upgrading MySQL that is not specific
to Windows.

Upgrading MySQL with MSI

Download and execute the latest MSI. Although upgrading between release series is not directly
supported, the "Custom Setup" option allows defining an installation location as otherwise the MSI
installs to the standard location, such as C:\Program Files\MySQL\MySQL Server 8.4\.

Execute MySQL Configurator to configure your installation.

240

Rebuilding or Repairing Tables or Indexes

• If you have created a loadable function with a given name and upgrade MySQL to a version
that implements a new built-in function with the same name, the loadable function becomes
inaccessible. To correct this, use DROP FUNCTION to drop the loadable function, and then use
CREATE FUNCTION to re-create the loadable function with a different nonconflicting name. The
same is true if the new version of MySQL implements a built-in function with the same name as an
existing stored function. See Section 11.2.5, “Function Name Parsing and Resolution”, for the rules
describing how the server interprets references to different kinds of functions.

• If upgrade to MySQL 8.4 fails due to any of the issues outlined in Section 3.6, “Preparing Your

Installation for Upgrade”, the server reverts all changes to the data directory. In this case, remove all
redo log files and restart the MySQL 8.3 server on the existing data directory to address the errors.
The redo log files (ib_logfile*) reside in the MySQL data directory by default. After the errors
are fixed, perform a slow shutdown (by setting innodb_fast_shutdown=0) before attempting the
upgrade again.

3.14 Rebuilding or Repairing Tables or Indexes

This section describes how to rebuild or repair tables or indexes, which may be necessitated by:

• Changes to how MySQL handles data types or character sets. For example, an error in a collation

might have been corrected, necessitating a table rebuild to update the indexes for character columns
that use the collation.

• Required table repairs or upgrades reported by CHECK TABLE or mysqlcheck.

Methods for rebuilding a table include:

• Dump and Reload Method

• ALTER TABLE Method

• REPAIR TABLE Method

Dump and Reload Method

If you are rebuilding tables because a different version of MySQL cannot handle them after a binary
(in-place) upgrade or downgrade, you must use the dump-and-reload method. Dump the tables
before upgrading or downgrading using your original version of MySQL. Then reload the tables after
upgrading or downgrading.

If you use the dump-and-reload method of rebuilding tables only for the purpose of rebuilding indexes,
you can perform the dump either before or after upgrading or downgrading. Reloading still must be
done afterward.

If you need to rebuild an InnoDB table because a CHECK TABLE operation indicates that a table
upgrade is required, use mysqldump to create a dump file and mysql to reload the file. If the CHECK
TABLE operation indicates that there is a corruption or causes InnoDB to fail, refer to Section 17.20.3,
“Forcing InnoDB Recovery” for information about using the innodb_force_recovery option to
restart InnoDB. To understand the type of problem that CHECK TABLE may be encountering, refer to
the InnoDB notes in Section 15.7.3.2, “CHECK TABLE Statement”.

To rebuild a table by dumping and reloading it, use mysqldump to create a dump file and mysql to
reload the file:

mysqldump db_name t1 > dump.sql
mysql db_name < dump.sql

To rebuild all the tables in a single database, specify the database name without any following table
name:

mysqldump db_name > dump.sql

242

