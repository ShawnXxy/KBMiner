Upgrade Paths

• Review Section 3.2, “Upgrade Paths” to ensure that your intended upgrade path is supported.

• Review Section 3.5, “Changes in MySQL 8.0” for changes that you should be aware of before

upgrading. Some changes may require action.

• Review Section 1.3, “What Is New in MySQL 8.0” for deprecated and removed features. An upgrade

may require changes with respect to those features if you use any of them.

• Review Section 1.4, “Server and Status Variables and Options Added, Deprecated, or Removed

in MySQL 8.0”. If you use deprecated or removed variables, an upgrade may require configuration
changes.

• Review the Release Notes for information about fixes, changes, and new features.

• If you use replication, review Section 19.5.3, “Upgrading a Replication Topology”.

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

• Upgrade from MySQL 5.7 to 8.0 is supported. However, upgrade is only supported between General
Availability (GA) releases. For MySQL 8.0, it is required that you upgrade from a MySQL 5.7 GA
release (5.7.9 or higher). Upgrades from non-GA releases of MySQL 5.7 are not supported.

286

Review Supported Platforms

• A logical upgrade: exporting SQL from the old MySQL instance to the new.

• A replication topology upgrade: account for each server's topology role.

Review Supported Platforms

If your current operating system is not supported by the new version of MySQL, then plan to upgrade
the operating system as otherwise an in-place upgrade is not supported.

For a current list of supported platforms, see: https://www.mysql.com/support/supportedplatforms/
database.html

Understand MySQL Server Changes

Each major version comes with new features, changes in behavior, deprecations, and removals. It is
important to understand the impact of each of these to existing applications.

See: Section 3.5, “Changes in MySQL 8.0”.

Run Upgrade Checker and Fix Incompatibilities

MySQL Shell's Upgrade Checker Utility detects incompatibilities between database versions that must
be addressed before performing the upgrade. The util.checkForServerUpgrade() function
verifies that MySQL server instances are ready to upgrade. Connect to the existing MySQL server and
select the MySQL Server version you plan to upgrade to for the utility to report issues to address prior
to an upgrade. These include incompatibilities in data types, storage engines, and so on.

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

288

Changes in MySQL 8.0

3.5 Changes in MySQL 8.0

Before upgrading to MySQL 8.0, review the changes described in this section to identify those that
apply to your current MySQL installation and applications. Perform any recommended actions.

Changes marked as Incompatible change are incompatibilities with earlier versions of MySQL, and
may require your attention before upgrading. Our aim is to avoid these changes, but occasionally they
are necessary to correct problems that would be worse than an incompatibility between releases. If an
upgrade issue applicable to your installation involves an incompatibility, follow the instructions given in
the description.

• Data Dictionary Changes

• caching_sha2_password as the Preferred Authentication Plugin

• Configuration Changes

• Server Changes

• InnoDB Changes

• SQL Changes

• Changed Server Defaults

• Valid Performance Regressions

Data Dictionary Changes

MySQL Server 8.0 incorporates a global data dictionary containing information about database objects
in transactional tables. In previous MySQL series, dictionary data was stored in metadata files and
nontransactional system tables. As a result, the upgrade procedure requires that you verify the upgrade
readiness of your installation by checking specific prerequisites. For more information, see Section 3.6,
“Preparing Your Installation for Upgrade”. A data dictionary-enabled server entails some general
operational differences; see Section 16.7, “Data Dictionary Usage Differences”.

caching_sha2_password as the Preferred Authentication Plugin

The caching_sha2_password and sha256_password authentication plugins provide more secure
password encryption than the mysql_native_password plugin, and caching_sha2_password
provides better performance than sha256_password. Due to these superior security and performance
characteristics of caching_sha2_password, it is as of MySQL 8.0 the preferred authentication
plugin, and is also the default authentication plugin rather than mysql_native_password. This
change affects both the server and the libmysqlclient client library:

• For the server, the default value of the default_authentication_plugin system variable

changes from mysql_native_password to caching_sha2_password.

This change applies only to new accounts created after installing or upgrading to MySQL 8.0 or
higher. For accounts already existing in an upgraded installation, their authentication plugin remains
unchanged. Existing users who wish to switch to caching_sha2_password can do so using the
ALTER USER statement:

ALTER USER user
  IDENTIFIED WITH caching_sha2_password
  BY 'password';

• The libmysqlclient library treats caching_sha2_password as the default authentication

plugin rather than mysql_native_password.

The following sections discuss the implications of the more prominent role of
caching_sha2_password:

293

caching_sha2_password as the Preferred Authentication Plugin

• MySQL Connector/Python scripts that use the native Python implementation of the client/server

protocol can specify the auth_plugin connection option. (Alternatively, use the Connector/Python
C Extension, which is able to connect to MySQL 8.0 servers without the need for auth_plugin.)

caching_sha2_password-Compatible Clients and Connectors

If a client or connector is available that has been updated to know about caching_sha2_password,
using it is the best way to ensure compatibility when connecting to a MySQL 8.0 server configured with
caching_sha2_password as the default authentication plugin.

These clients and connectors have been upgraded to support caching_sha2_password:

• The libmysqlclient client library in MySQL 8.0 (8.0.4 or higher). Standard MySQL clients such

as mysql and mysqladmin are libmysqlclient-based, so they are compatible as well.

• The libmysqlclient client library in MySQL 5.7 (5.7.23 or higher). Standard MySQL clients such

as mysql and mysqladmin are libmysqlclient-based, so they are compatible as well.

• MySQL Connector/C++ 1.1.11 or higher or 8.0.7 or higher.

• MySQL Connector/J 8.0.9 or higher.

• MySQL Connector/NET 8.0.10 or higher (through the classic MySQL protocol).

• MySQL Connector/Node.js 8.0.9 or higher.

• PHP: the X DevAPI PHP extension (mysql_xdevapi) supports caching_sha2_password.

PHP: the PDO_MySQL and ext/mysqli extensions do not support caching_sha2_password.
In addition, when used with PHP versions before 7.1.16 and PHP 7.2 before 7.2.4, they fail
to connect with default_authentication_plugin=caching_sha2_password even if
caching_sha2_password is not used.

caching_sha2_password and the root Administrative Account

For upgrades to MySQL 8.0, the authentication plugin existing accounts remains unchanged, including
the plugin for the 'root'@'localhost' administrative account.

For new MySQL 8.0 installations, when you initialize the data directory (using the instructions at
Section 2.9.1, “Initializing the Data Directory”), the 'root'@'localhost' account is created, and that
account uses caching_sha2_password by default. To connect to the server following data directory
initialization, you must therefore use a client or connector that supports caching_sha2_password.
If you can do this but prefer that the root account use mysql_native_password after installation,
install MySQL and initialize the data directory as you normally would. Then connect to the server as
root and use ALTER USER as follows to change the account authentication plugin and password:

ALTER USER 'root'@'localhost'
  IDENTIFIED WITH mysql_native_password
  BY 'password';

If the client or connector that you use does not yet support caching_sha2_password, you
can use a modified data directory-initialization procedure that associates the root account with
mysql_native_password as soon as the account is created. To do so, use either of these
techniques:

• Supply a --default-authentication-plugin=mysql_native_password option along with

--initialize or --initialize-insecure.

• Set default_authentication_plugin to mysql_native_password in an option file,

and name that option file using a --defaults-file option along with --initialize or --
initialize-insecure. (In this case, if you continue to use that option file for subsequent
server startups, new accounts are created with mysql_native_password rather than
caching_sha2_password unless you remove the default_authentication_plugin setting
from the option file.)

296

Configuration Changes

caching_sha2_password and Replication

In replication scenarios for which all servers have been upgraded to MySQL 8.0.4 or higher, replica
connections to source servers can use accounts that authenticate with caching_sha2_password.
For such connections, the same requirement applies as for other clients that use accounts that
authenticate with caching_sha2_password: Use a secure connection or RSA-based password
exchange.

To connect to a caching_sha2_password account for source/replica replication:

• Use any of the following CHANGE MASTER TO options:

MASTER_SSL = 1
GET_MASTER_PUBLIC_KEY = 1
MASTER_PUBLIC_KEY_PATH='path to RSA public key file'

• Alternatively, you can use the RSA public key-related options if the required keys are supplied at

server startup.

To connect to a caching_sha2_password account for Group Replication:

• For MySQL built using OpenSSL, set any of the following system variables:

SET GLOBAL group_replication_recovery_use_ssl = ON;
SET GLOBAL group_replication_recovery_get_public_key = 1;
SET GLOBAL group_replication_recovery_public_key_path = 'path to RSA public key file';

• Alternatively, you can use the RSA public key-related options if the required keys are supplied at

server startup.

Configuration Changes

• Incompatible change: A MySQL storage engine is now responsible for providing its own partitioning
handler, and the MySQL server no longer provides generic partitioning support. InnoDB and NDB are
the only storage engines that provide a native partitioning handler that is supported in MySQL 8.0. A
partitioned table using any other storage engine must be altered—either to convert it to InnoDB or
NDB, or to remove its partitioning—before upgrading the server, else it cannot be used afterwards.

For information about converting MyISAM tables to InnoDB, see Section 17.6.1.5, “Converting
Tables from MyISAM to InnoDB”.

A table creation statement that would result in a partitioned table using a storage engine without such
support fails with an error (ER_CHECK_NOT_IMPLEMENTED) in MySQL 8.0. If you import databases
from a dump file created in MySQL 5.7 (or earlier) using mysqldump into a MySQL 8.0 server, you
must make sure that any statements creating partitioned tables do not also specify an unsupported
storage engine, either by removing any references to partitioning, or by specifying the storage engine
as InnoDB or allowing it to be set as InnoDB by default.

Note

The procedure given at Section 3.6, “Preparing Your Installation for Upgrade”,
describes how to identify partitioned tables that must be altered before
upgrading to MySQL 8.0.

See Section 26.6.2, “Partitioning Limitations Relating to Storage Engines”, for further information.

• Incompatible change: Several server error codes are not used and have been removed (for a list,
see Features Removed in MySQL 8.0). Applications that test specifically for any of them should be
updated.

• Important change: The default character set has changed from latin1 to utf8mb4. These system

variables are affected:

297

InnoDB Changes

• With the introduction of the --innodb-directories feature, the location of file-per-table and

general tablespace files created with an absolute path or in a location outside of the data directory
should be added to the innodb_directories argument value. Otherwise, InnoDB is not able to
locate these files during recovery. To view tablespace file locations, query the Information Schema
FILES table:

SELECT TABLESPACE_NAME, FILE_NAME FROM INFORMATION_SCHEMA.FILES \G

• Undo logs can no longer reside in the system tablespace. In MySQL 8.0, undo logs reside in two
undo tablespaces by default. For more information, see Section 17.6.3.4, “Undo Tablespaces”.

When upgrading from MySQL 5.7 to MySQL 8.0, any undo tablespaces that exist in the MySQL
5.7 instance are removed and replaced by two new default undo tablespaces. Default undo
tablespaces are created in the location defined by the innodb_undo_directory variable. If
the innodb_undo_directory variable is undefined, undo tablespaces are created in the data
directory. Upgrade from MySQL 5.7 to MySQL 8.0 requires a slow shutdown which ensures that
undo tablespaces in the MySQL 5.7 instance are empty, permitting them to be removed safely.

When upgrading to MySQL 8.0.14 or later from an earlier MySQL 8.0 release, undo tablespaces that
exist in the pre-upgrade instance as a result of an innodb_undo_tablespaces setting greater
than 2 are treated as user-defined undo tablespaces, which can be deactivated and dropped using
ALTER UNDO TABLESPACE and DROP UNDO TABLESPACE syntax, respectively, after upgrading.
Upgrade within the MySQL 8.0 release series may not always require a slow shutdown which means
that existing undo tablespaces could contain undo logs. Therefore, existing undo tablespaces are not
removed by the upgrade process.

• Incompatible change: As of MySQL 8.0.17, the CREATE TABLESPACE ... ADD DATAFILE

clause does not permit circular directory references. For example, the circular directory reference
(/../) in the following statement is not permitted:

CREATE TABLESPACE ts1 ADD DATAFILE ts1.ibd 'any_directory/../ts1.ibd';

An exception to the restriction exists on Linux, where a circular directory reference is permitted if
the preceding directory is a symbolic link. For example, the data file path in the example above is
permitted if any_directory is a symbolic link. (It is still permitted for data file paths to begin with
'../'.)

To avoid upgrade issues, remove any circular directory references from tablespace data file paths
before upgrading to MySQL 8.0.17 or higher. To inspect tablespace paths, query the Information
Schema INNODB_DATAFILES table.

• Due to a regression introduced in MySQL 8.0.14, in-place upgrade on a case-sensitive file system

from MySQL 5.7 or a MySQL 8.0 release prior to MySQL 8.0.14 to MySQL 8.0.16 failed for instances
with partitioned tables and lower_case_table_names=1. The failure was caused by a case
mismatch issue related to partitioned table file names. The fix that introduced the regression was
reverted, which permits upgrades to MySQL 8.0.17 from MySQL 5.7 or MySQL 8.0 releases prior to
MySQL 8.0.14 to function as normal. However, the regression is still present in the MySQL 8.0.14,
8.0.15, and 8.0.16 releases.

In-place upgrade on a case-sensitive file system from MySQL 8.0.14, 8.0.15, or 8.0.16 to MySQL
8.0.17 fails with the following error when starting the server after upgrading binaries or packages to
MySQL 8.0.17 if partitioned tables are present and lower_case_table_names=1:

Upgrading from server version version_number with
partitioned tables and lower_case_table_names == 1 on a case sensitive file
system may cause issues, and is therefore prohibited. To upgrade anyway, restart
the new server version with the command line option 'upgrade=FORCE'. When
upgrade is completed, please execute 'RENAME TABLE part_table_name
TO new_table_name; RENAME TABLE new_table_name
TO part_table_name;' for each of the partitioned tables.

301

InnoDB Changes

Please see the documentation for further information.

If you encounter this error when upgrading to MySQL 8.0.17, perform the following workaround:

1. Restart the server with --upgrade=force to force the upgrade operation to proceed.

2.

Identify partitioned table file names with lowercase partition name delimiters (#p# or #sp#):

mysql> SELECT FILE_NAME FROM INFORMATION_SCHEMA.FILES WHERE FILE_NAME LIKE '%#p#%' OR FILE_NAME LIKE '%#sp#%';

3. For each file identified, rename the associated table using a temporary name, then rename the

table back to its original name.

mysql> RENAME TABLE table_name TO temporary_table_name;
mysql> RENAME TABLE temporary_table_name TO table_name;

4. Verify that there are no partitioned table file names lowercase partition name delimiters (an empty

result set should be returned).

mysql> SELECT FILE_NAME FROM INFORMATION_SCHEMA.FILES WHERE FILE_NAME LIKE '%#p#%' OR FILE_NAME LIKE '%#sp#%';
Empty set (0.00 sec)

5. Run ANALYZE TABLE on each renamed table to update the optimizer statistics in the

mysql.innodb_index_stats and mysql.innodb_table_stats tables.

Because of the regression still present in the MySQL 8.0.14, 8.0.15, and 8.0.16 releases, importing
partitioned tables from MySQL 8.0.14, 8.0.15, or 8.0.16 to MySQL 8.0.17 is not supported on case-
sensitive file systems where lower_case_table_names=1. Attempting to do so results in a
“Tablespace is missing for table” error.

• MySQL uses delimiter strings when constructing tablespace names and file names for table

partitions. A “ #p# ” delimiter string precedes partition names, and an “ #sp# ” delimiter string
precedes subpartition names, as shown:

      schema_name.table_name#p#partition_name#sp#subpartition_name
      table_name#p#partition_name#sp#subpartition_name.ibd

Historically, delimiter strings have been uppercase (#P# and #SP#) on case-sensitive file systems
such as Linux, and lowercase (#p# and #sp#) on case-insensitive file systems such as Windows.
As of MySQL 8.0.19, delimiter strings are lowercase on all file systems. This change prevents
issues when migrating data directories between case-sensitive and case-insensitive file systems.
Uppercase delimiter strings are no longer used.

Additionally, partition tablespace names and file names generated based on user-specified partition
or subpartition names, which can be specified in uppercase or lowercase, are now generated (and
stored internally) in lowercase regardless of the lower_case_table_names setting to ensure
case-insensitivity. For example, if a table partition is created with the name PART_1, the tablespace
name and file name are generated in lowercase:

      schema_name.table_name#p#part_1
      table_name#p#part_1.ibd

During upgrade, MySQL checks and modifies if necessary:

• Partition file names on disk and in the data dictionary to ensure lowercase delimiters and partition

names.

• Partition metadata in the data dictionary for related issues introduced by previous bug fixes.

• InnoDB statistics data for related issues introduced by previous bug fixes.

During tablespace import operations, partition tablespace file names on disk are checked and
modified if necessary to ensure lowercase delimiters and partition names.

302

Changed Server Defaults

behavior has been reverted in MySQL 8.0.16, and InnoDB once again uses a generated constraint
name.

For consistency with InnoDB, NDB releases based on MySQL 8.0.16 or higher use a generated
constraint name if the CONSTRAINT symbol  clause is not specified, or the CONSTRAINT keyword
is specified without a symbol. NDB releases based on MySQL 5.7 and earlier MySQL 8.0 releases
used the FOREIGN KEY index_name  value.

The changes described above may introduce incompatibilities for applications that depend on the
previous foreign key constraint naming behavior.

• The handling of system variable values by MySQL flow control functions such as IFNULL() and
CASE() changed in MySQL 8.0.22; system variable values are now handled as column values of
the same character and collation, rather than as constants. Some queries using these functions with
system variables that were previously successful may subsequently be rejected with Illegal mix
of collations. In such cases, cast the system variable to the correct character set and collation.

• Incompatible change: MySQL 8.0.28 fixes an issue in previous MySQL 8.0 releases whereby the

CONVERT() function sometimes allowed invalid casts of BINARY values to nonbinary character sets.
Applications which may have relied on this behavior should be checked and if necessary modified
prior to upgrade.

In particular, where CONVERT() was used as part of an expression for an indexed generated
column, the change in the function's behavior may result in index corruption following an upgrade to
MySQL 8.0.28. You can prevent this from happening by following these steps:

1. Prior to performing the upgrade, correct any invalid input data.

2. Drop and then re-create the index.

You can also force a table rebuild using ALTER TABLE table FORCE, instead.

3. Upgrade the MySQL software.

If you cannot validate the input data beforehand, you should not re-create the index or rebuild the
table until after you perform the upgrade to MySQL 8.0.28.

Changed Server Defaults

MySQL 8.0 comes with improved defaults, aiming at the best out of the box experience possible. These
changes are driven by the fact that technology is advancing (machines have more CPUS, use SSDs
and so on), more data is being stored, MySQL is evolving (InnoDB, Group Replication, AdminAPI),
and so on. The following table summarizes the defaults which have been changed to provide the best
MySQL experience for the majority of users.

Option/Parameter

Server changes

Old Default

New Default

character_set_server

latin1

utf8mb4

collation_server

latin1_swedish_ci

utf8mb4_0900_ai_ci

explicit_defaults_for_timestamp

OFF

optimizer_trace_max_mem_size16KB

validate_password_check_user_name

OFF

ON

1MB

ON

back_log

-1 (autosize) changed
from : back_log = 50 +
(max_connections / 5)

-1 (autosize) changed to :
back_log = max_connections

max_allowed_packet

4194304 (4MB)

67108864 (64MB)

max_error_count

64

1024

304

Changed Server Defaults

• The default value of the event_scheduler system variable changed from OFF to ON. In other
words, the event scheduler is enabled by default. This is an enabler for new features in SYS, for
example “kill idle transactions”.

• The default value of the table_open_cache system variable changed from 2000 to 4000. This is a

minor change which increases session concurrency on table access.

• The default value of the log_error_verbosity system variable changed from 3 (Notes) to 2

(Warning). The purpose is to make the MySQL 8.0 error log less verbose by default.

InnoDB Defaults

• Incompatible change The default value of the innodb_undo_tablespaces system variable

changed from 0 to 2. The configures the number of undo tablespaces used by InnoDB. In MySQL
8.0 the minimum value for innodb_undo_tablespaces is 2 and rollback segments cannot be
created in the system tablespace anymore. Thus, this is a case where you cannot revert back to
5.7 behavior. The purpose of this change is to be able to auto-truncate Undo logs (see next item),
reclaiming disk space used by (occasional) long transactions such as a mysqldump.

• The default value of the innodb_undo_log_truncate system variable  changed from
OFF to ON. When enabled, undo tablespaces that exceed the threshold value defined by
innodb_max_undo_log_size are marked for truncation. Only undo tablespaces can be truncated.
Truncating undo logs that reside in the system tablespace is not supported. An upgrade from 5.7 to
8.0 automatically converts your system to use  undo tablespaces, using the system tablespace is not
an option in 8.0.

• The default value of the innodb_flush_method system variable changed from NULL to
fsync on Unix-like systems and from NULL to unbuffered on Windows systems. This is
more of a terminology and option cleanup without any tangible impact. For Unix this is just a
documentation change as the default was fsync also in 5.7 (the default NULL meant fsync).
Similarly on Windows, innodb_flush_method default NULL meant async_unbuffered in
5.7, and is replaced by default unbuffered in 8.0, which in combination with the existing default
innodb_use_native_aio=ON has the same effect.

• Incompatible change The default value of the innodb_autoinc_lock_mode system variable
changed from 1 (consecutive) to 2 (interleaved). The change to interleaved lock mode as the
default setting reflects the change from statement-based to row-based replication as the default
replication type, which occurred in MySQL 5.7. Statement-based replication requires the consecutive
auto-increment lock mode to ensure that auto-increment values are assigned in a predictable
and repeatable order for a given sequence of SQL statements, whereas row-based replication
is not sensitive to the execution order of SQL statements. Thus, this change is known to be
incompatible with statement based replication, and may break some applications or user-generated
test suites that depend on sequential auto increment. The previous default can be restored by setting
innodb_autoinc_lock_mode=1;

• The default value of the innodb_flush_neighbors system variable changes from 1 (enable) to
0 (disable). This is done because fast IO (SSDs) is now the default for deployment. We expect that
for the majority of users, this results in a small performance gain. Users who are using slower hard
drives may see a performance loss, and are encouraged to revert to the previous defaults by setting
innodb_flush_neighbors=1.

• The default value of the innodb_max_dirty_pages_pct_lwm system variable changed from

0 (%) to 10 (%). With innodb_max_dirty_pages_pct_lwm=10, InnoDB increases its flushing
activity when >10% of the buffer pool contains modified (‘dirty’) pages. The purpose of this change is
to trade off peak throughput slightly, in exchange for more consistent performance.

• The default value of the innodb_max_dirty_pages_pct system variable changed from 75

(%) to 90 (%). This change combines with the change to innodb_max_dirty_pages_pct_lwm
and together they ensure a smooth InnoDB flushing behavior, avoiding flushing bursts.
To revert to the previous behavior, set innodb_max_dirty_pages_pct=75 and
innodb_max_dirty_pages_pct_lwm=0.

307

Changed Server Defaults

Performance Schema Defaults

• Performance Schema Meta Data Locking  (MDL) instrumentation is turned on by default. The

compiled default  for performance-schema-instrument='wait/lock/metadata/sql/%=ON'
changed from OFF to ON.  This is an enabler for adding MDL oriented views in SYS.

• Performance Schema Memory instrumentation is turned on by default. The compiled default  for

performance-schema-instrument='memory/%=COUNTED' changed from OFF to COUNTED.
This is important because the accounting is incorrect if instrumentation is enabled after server start,
and you could get a negative balance from missing an allocation, but catching a free.

• Performance Schema Transaction instrumentation is turned on by default. The compiled default  for
  performance-schema-consumer-events-transactions-current=ON, performance-
schema-consumer-events-transactions-history=ON, and performance-schema-
instrument='transaction%=ON' changed from OFF to ON.

Replication Defaults

• The default value of the log_bin system variable changed from OFF to ON. In other words, binary
logging is enabled by default. Nearly all production installations have the binary log enabled as it is
used for replication and point-in-time recovery. Thus, by enabling binary log by default we eliminate
one configuration step, enabling it later requires a mysqld restart. Enabling it by default also
provides better test coverage and it becomes easier to spot performance regressions. Remember to
also set server_id (see following change). The 8.0 default behavior is as if you issued ./mysqld
--log-bin --server-id=1. If you are on 8.0 and want 5.7 behavior you can issue ./mysqld
--skip-log-bin --server-id=0.

• The default value of the server_id system variable changed from 0 to 1 (combines with the

change to log_bin=ON). The server can be started with this default ID, but in practice you must set
the server-id according to the replication infrastructure being deployed, to avoid having duplicate
server ids.

• The default value of the log-slave-updates system variable changed from OFF to ON.  This

causes a replica to log replicated events into its own binary log. This option is required for Group
Replication, and also ensures correct behavior in various replication chain setups, which have
become the norm today.

• The default value of the expire_logs_days system variable changed from 0 to 30. The new

default 30 causes mysqld to periodically purge unused binary logs that are older than 30 days. This
change helps prevent excessive amounts of disk space being wasted on binary logs that are no
longer needed for replication or recovery purposes. The old value of 0 disables any automatic binary
log purges.

• The default value of the master_info_repository and relay_log_info_repository system

variables change from FILE to TABLE. Thus in 8.0, replication metadata is stored in InnoDB by
default. This increases reliability to try and achieve crash safe replication by default.

• The default value of the transaction-write-set-extraction system variable changed from

OFF to XXHASH64. This change enables transaction write sets by default. By using Transaction Write
Sets, the source has to do slightly more work to generate the write sets, but the result is helpful in
conflict detection. This is a requirement for Group Replication and the new default makes it easy to
enable binary log writeset parallelization on the source to speed up replication.

• The default value of the slave_rows_search_algorithms system variable changed from

INDEX_SCAN,TABLE_SCAN to INDEX_SCAN,HASH_SCAN. This change speeds up row-based
replication by reducing the number of table scans the replica applier has to do to apply the changes
to a table without a primary key.

• The default value of the slave_pending_jobs_size_max system variable changed from 16M to

128M. This change increases the amount of memory available to multithreaded replicas.

308

Valid Performance Regressions

• The default value of the gtid_executed_compression_period system variable changed from

1000 to 0. This change ensures that compression of the mysql.gtid_executed table only occurs
implicitly as required.

Group Replication Defaults

• The default value of group_replication_autorejoin_tries changed from 0 to 3, which

means that automatic rejoin is enabled by default. This system variable specifies the number of tries
that a member makes to automatically rejoin the group if it is expelled, or if it is unable to contact
a majority of the group before the group_replication_unreachable_majority_timeout
setting is reached.

• The default value of group_replication_exit_state_action changed from ABORT_SERVER
to READ_ONLY. This means that when a member exits the group, for example after a network failure,
the instance becomes read-only, rather than being shut down.

• The default value of group_replication_member_expel_timeout changed from 0 to 5,

meaning that a member suspected of having lost contact with the group is liable for expulsion 5
seconds after the 5-second detection period.

Most of these defaults are reasonably good for both development and production environments. An
exception to this is the --innodb-dedicated-server option, whose default value remains OFF,
although we recommend ON for production environments. The reason for defaulting to OFF is that it
causes shared environments such as developer laptops to become unusable, because it takes all the
memory it can find.

For production environments we recommend using --innodb-dedicated-server, which
determines values for the following InnoDB variables (if not specified explicitly), based on available
memory: innodb_buffer_pool_size, innodb_log_file_size, and innodb_flush_method.
See Section 17.8.12, “Enabling Automatic InnoDB Configuration for a Dedicated MySQL Server”.

Although the new defaults are the best configuration choices for most use cases, there are special
cases, as well as legacy reasons for using existing 5.7 configuration choices. For example, some
people prefer to upgrade to 8.0 with as few changes to their applications or operational environment
as possible. We recommend to evaluate all the new defaults and use as many as you can. Most new
defaults can be tested in 5.7, so you can validate the new defaults in 5.7 production before upgrading
to 8.0. For the few defaults where you need your old 5.7 value, set the corresponding configuration
variable or startup option in your operational environment.

MySQL 8.0 has the Performance Schema variables_info table, which shows for each system
variable the source from which it was most recently set, as well as its range of values. This provides
SQL access to all there is to know about a configuration variable and its values.

Valid Performance Regressions

Performance regressions are expected between MySQL versions 5.7 and 8.0. MySQL 8.0 has more
features, changes default values, is more robust, and adds security functionality and additional
diagnostic information. Listed here are valid reasons for regressions between these versions which
includes potential mediation options. This is not an exhaustive list.

Changes related to default values changing between MySQL versions 5.7 and 8.0:

• Binary logs are disabled by default in 5.7, and enabled by default in 8.0.

Mediation: Disable binary logging by specifying the --skip-log-bin or --disable-log-bin
option at startup.

• The default character set changed from latin1 to utf8mb4 in 8.0. While utf8mb4 performs

significantly better in 8.0 than it did in 5.7, latin1 is faster than utf8mb4.

Mediation: Use latin1 in 8.0 if utf8mb4 is not needed.

309

Preparing Your Installation for Upgrade

Transactional Data Dictionary (atomic DDL) was introduced in 8.0.

• This increases robustness/reliability at the expense of DDL performance (CREATE / DROP intensive

loads), but it should not impact the DML load (SELECT / INSERT / UPDATE / DELETE).

Mediation: None

The more modern TLS ciphers/algorithms used as of 5.7.28 has an effect when TLS (SSL) is enabled
(the default):

• Before MySQL 5.7.28, MySQL uses the yaSSL library for the community edition and OpenSSL for

the enterprise edition.

As of MySQL 5.7.28, MySQL only uses OpenSSL with its stronger TLS ciphers, which are more
costly in terms of performance.

Upgrading to MySQL 8.0 from MySQL 5.7.28 or earlier can cause a TLS performance regression.

Mediation: None (if TLS is required for security reasons)

Performance Schema (PFS) instrumentation is much wider in 8.0 than in 5.7:

• PFS cannot be compiled out in MySQL 8.0 but it can be turned off. Some performance schema

instrumentation will still exist even when turned off, but overhead will be smaller.

Mediation: Set performance_schema = OFF in 8.0, or turn off performance schema instrumentation
at finer granularity if some but not all PFS functionality is needed.

Truncating undo tablespaces is enabled by default in 8.0 which can significantly impact performance:

• Historically InnoDB stored undo logs in the system tablespace but there was no way to reclaim space
used by undo log. The system tablespace would only grow and not shrink, and this inspired feature
requests to remedy this.

MySQL 8.0 moved the undo log to separate tablespaces which allows both manual and automatic
undo log truncation.

However, auto-truncation has a permanent performance overhead and it can potentially cause stalls.

Mediation: Set innodb_undo_log_truncate = OFF in 8.0, and manually truncate undo logs as needed.
For related information, see Truncating Undo Tablespaces.

The character classes [[:alpha:]] or [[:digit:]] do not perform as well with regular expression
functions such as REGEXP() and RLIKE() in MySQL 8.0 as they did in MySQL 5.7. This is due to the
replacement in MySQL 8.0 of the Spencer regular expression library with the ICU library, which uses
UTF-16 internally.

Mediation: In place of [[:alpha:]], use [a-zA-Z]; in place of [[:digit:]], use [0-9].

3.6 Preparing Your Installation for Upgrade

Before upgrading to the latest MySQL 8.0 release, ensure the upgrade readiness of your current
MySQL 5.7 or MySQL 8.0 server instance by performing the preliminary checks described below. The
upgrade process may fail otherwise.

Tip

Consider using the MySQL Shell upgrade checker utility that enables you to
verify whether MySQL server instances are ready for upgrade. You can select
a target MySQL Server release to which you plan to upgrade, ranging from the
MySQL Server 8.0.11 up to the MySQL Server release number that matches

310

Preparing Your Installation for Upgrade

the current MySQL Shell release number. The upgrade checker utility carries
out the automated checks that are relevant for the specified target release, and
advises you of further relevant checks that you should make manually. The
upgrade checker works for all Bugfix, Innovation, and LTS releases of MySQL.
Installation instructions for MySQL Shell can be found here.

Preliminary checks:

1. The following issues must not be present:

• There must be no tables that use obsolete data types or functions.

In-place upgrade to MySQL 8.0 is not supported if tables contain old temporal columns in
pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional
seconds precision). If your tables still use the old temporal column format, upgrade them using
REPAIR TABLE before attempting an in-place upgrade to MySQL 8.0. For more information, see
Server Changes, in MySQL 5.7 Reference Manual.

• There must be no orphan .frm files.

• Triggers must not have a missing or empty definer or an invalid creation context (indicated by

the character_set_client, collation_connection, Database Collation attributes
displayed by SHOW TRIGGERS or the INFORMATION_SCHEMA TRIGGERS table). Any such
triggers must be dumped and restored to fix the issue.

To check for these issues, execute this command:

mysqlcheck -u root -p --all-databases --check-upgrade

If mysqlcheck reports any errors, correct the issues.

2. There must be no partitioned tables that use a storage engine that does not have native partitioning

support. To identify such tables, execute this query:

SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE ENGINE NOT IN ('innodb', 'ndbcluster')
AND CREATE_OPTIONS LIKE '%partitioned%';

Any table reported by the query must be altered to use InnoDB or be made nonpartitioned. To
change a table storage engine to InnoDB, execute this statement:

ALTER TABLE table_name ENGINE = INNODB;

For information about converting MyISAM tables to InnoDB, see Section 17.6.1.5, “Converting
Tables from MyISAM to InnoDB”.

To make a partitioned table nonpartitioned, execute this statement:

ALTER TABLE table_name REMOVE PARTITIONING;

3. Some keywords may be reserved in MySQL 8.0 that were not reserved previously. See

Section 11.3, “Keywords and Reserved Words”. This can cause words previously used as
identifiers to become illegal. To fix affected statements, use identifier quoting. See Section 11.2,
“Schema Object Names”.

4. There must be no tables in the MySQL 5.7 mysql system database that have the same name as
a table used by the MySQL 8.0 data dictionary. To identify tables with those names, execute this
query:

SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE LOWER(TABLE_SCHEMA) = 'mysql'
and LOWER(TABLE_NAME) IN

311

Preparing Your Installation for Upgrade

(
'catalogs',
'character_sets',
'check_constraints',
'collations',
'column_statistics',
'column_type_elements',
'columns',
'dd_properties',
'events',
'foreign_key_column_usage',
'foreign_keys',
'index_column_usage',
'index_partitions',
'index_stats',
'indexes',
'parameter_type_elements',
'parameters',
'resource_groups',
'routines',
'schemata',
'st_spatial_reference_systems',
'table_partition_values',
'table_partitions',
'table_stats',
'tables',
'tablespace_files',
'tablespaces',
'triggers',
'view_routine_usage',
'view_table_usage'
);

Any tables reported by the query must be dropped or renamed (use RENAME TABLE). This may
also entail changes to applications that use the affected tables.

5. There must be no tables that have foreign key constraint names longer than 64 characters. Use this

query to identify tables with constraint names that are too long:

SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME IN
  (SELECT LEFT(SUBSTR(ID,INSTR(ID,'/')+1),
               INSTR(SUBSTR(ID,INSTR(ID,'/')+1),'_ibfk_')-1)
   FROM INFORMATION_SCHEMA.INNODB_SYS_FOREIGN
   WHERE CHAR_LENGTH(SUBSTR(ID,INSTR(ID,'/')+1))>64);

For a table with a constraint name that exceeds 64 characters, drop the constraint and add it back
with constraint name that does not exceed 64 characters (use ALTER TABLE).

6. There must be no obsolete SQL modes defined by sql_mode system variable. Attempting to use
an obsolete SQL mode prevents MySQL 8.0 from starting. Applications that use obsolete SQL
modes should be revised to avoid them. For information about SQL modes removed in MySQL 8.0,
see Server Changes.

7. Only upgrade a MySQL server instance that was properly shut down. If the instance unexpectedly
shutdown, then restart the instance and shut it down with innodb_fast_shutdown=0 before
upgrade.

8. There must be no views with explicitly defined columns names that exceed 64 characters (views

with column names up to 255 characters were permitted in MySQL 5.7). To avoid upgrade errors,
such views should be altered before upgrading. Currently, the only method of identify views with
column names that exceed 64 characters is to inspect the view definition using SHOW CREATE
VIEW. You can also inspect view definitions by querying the Information Schema VIEWS table.

9. There must be no tables or stored procedures with individual ENUM or SET column elements that

exceed 255 characters or 1020 bytes in length. Prior to MySQL 8.0, the maximum combined length
of ENUM or SET column elements was 64K. In MySQL 8.0, the maximum character length of an

312

Preparing Your Installation for Upgrade

individual ENUM or SET column element is 255 characters, and the maximum byte length is 1020
bytes. (The 1020 byte limit supports multibyte character sets). Before upgrading to MySQL 8.0,
modify any ENUM or SET column elements that exceed the new limits. Failing to do so causes the
upgrade to fail with an error.

10. Before upgrading to MySQL 8.0.13 or higher, there must be no table partitions that reside in shared
InnoDB tablespaces, which include the system tablespace and general tablespaces. Identify table
partitions in shared tablespaces by querying INFORMATION_SCHEMA:

If upgrading from MySQL 5.7, run this query:

SELECT DISTINCT NAME, SPACE, SPACE_TYPE FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES
  WHERE NAME LIKE '%#P#%' AND SPACE_TYPE NOT LIKE 'Single';

If upgrading from an earlier MySQL 8.0 release, run this query:

SELECT DISTINCT NAME, SPACE, SPACE_TYPE FROM INFORMATION_SCHEMA.INNODB_TABLES
  WHERE NAME LIKE '%#P#%' AND SPACE_TYPE NOT LIKE 'Single';

Move table partitions from shared tablespaces to file-per-table tablespaces using ALTER
TABLE ... REORGANIZE PARTITION:

ALTER TABLE table_name REORGANIZE PARTITION partition_name
  INTO (partition_definition TABLESPACE=innodb_file_per_table);

11. There must be no queries and stored program definitions from MySQL 8.0.12 or lower that use ASC
or DESC qualifiers for GROUP BY clauses. Otherwise, upgrading to MySQL 8.0.13 or higher may
fail, as may replicating to MySQL 8.0.13 or higher replica servers. For additional details, see SQL
Changes.

12. Your MySQL 5.7 installation must not use features that are not supported by MySQL 8.0. Any

changes here are necessarily installation specific, but the following example illustrates the kind of
thing to look for:

Some server startup options and system variables have been removed in MySQL 8.0. See
Features Removed in MySQL 8.0, and Section 1.4, “Server and Status Variables and Options
Added, Deprecated, or Removed in MySQL 8.0”. If you use any of these, an upgrade requires
configuration changes.

Example: Because the data dictionary provides information about database objects, the server
no longer checks directory names in the data directory to find databases. Consequently, the
--ignore-db-dir option is extraneous and has been removed. To handle this, remove any
instances of --ignore-db-dir from your startup configuration. In addition, remove or move
the named data directory subdirectories before upgrading to MySQL 8.0. (Alternatively, let the
8.0 server add those directories to the data dictionary as databases, then remove each of those
databases using DROP DATABASE.)

13. If you intend to change the lower_case_table_names setting to 1 at upgrade time, ensure that

schema and table names are lowercase before upgrading. Otherwise, a failure could occur due to a
schema or table name lettercase mismatch. You can use the following queries to check for schema
and table names containing uppercase characters:

mysql> select TABLE_NAME, if(sha(TABLE_NAME) !=sha(lower(TABLE_NAME)),'Yes','No') as UpperCase from information_schema.tables;

As of MySQL 8.0.19, if lower_case_table_names=1, table and schema names are checked
by the upgrade process to ensure that all characters are lowercase. If table or schema names are
found to contain uppercase characters, the upgrade process fails with an error.

Note

Changing the lower_case_table_names setting at upgrade time is not
recommended.

313

Upgrading MySQL Binary or Package-based Installations on Unix/Linux

If upgrade to MySQL 8.0 fails due to any of the issues outlined above, the server reverts all changes
to the data directory. In this case, remove all redo log files and restart the MySQL 5.7 server on
the existing data directory to address the errors. The redo log files (ib_logfile*) reside in the
MySQL data directory by default. After the errors are fixed, perform a slow shutdown (by setting
innodb_fast_shutdown=0) before attempting the upgrade again.

3.7 Upgrading MySQL Binary or Package-based Installations on
Unix/Linux

This section describes how to upgrade MySQL binary and package-based installations on Unix/Linux.
In-place and logical upgrade methods are described.

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

If you are upgrading from MySQL 5.7.11 or earlier to MySQL 8.0, and there are encrypted InnoDB
tablespaces, rotate the keyring master key by executing this statement:

ALTER INSTANCE ROTATE INNODB MASTER KEY;

5.

If you normally run your MySQL server configured with innodb_fast_shutdown set to 2 (cold
shutdown), configure it to perform a fast or slow shutdown by executing either of these statements:

SET GLOBAL innodb_fast_shutdown = 1; -- fast shutdown

314

In-Place Upgrade

SET GLOBAL innodb_fast_shutdown = 0; -- slow shutdown

With a fast or slow shutdown, InnoDB leaves its undo logs and data files in a state that can be
dealt with in case of file format differences between releases.

6. Shut down the old MySQL server. For example:

mysqladmin -u root -p shutdown

7. Upgrade the MySQL binaries or packages. If upgrading a binary installation, unpack the new

MySQL binary distribution package. See Obtain and Unpack the Distribution. For package-based
installations, install the new packages.

8. Start the MySQL 8.0 server, using the existing data directory. For example:

mysqld_safe --user=mysql --datadir=/path/to/existing-datadir &

If there are encrypted InnoDB tablespaces, use the --early-plugin-load option to load the
keyring plugin.

When you start the MySQL 8.0 server, it automatically detects whether data dictionary tables are
present. If not, the server creates them in the data directory, populates them with metadata, and
then proceeds with its normal startup sequence. During this process, the server upgrades metadata
for all database objects, including databases, tablespaces, system and user tables, views, and
stored programs (stored procedures and functions, triggers, and Event Scheduler events). The
server also removes files that previously were used for metadata storage. For example, after
upgrading from MySQL 5.7 to MySQL 8.0, you may notice that tables no longer have .frm files.

If this step fails, the server reverts all changes to the data directory. In this case, you should remove
all redo log files, start your MySQL 5.7 server on the same data directory, and fix the cause of any
errors. Then perform another slow shutdown of the 5.7 server and start the MySQL 8.0 server to try
again.

9.

In the previous step, the server upgrades the data dictionary as necessary. Now it is necessary to
perform any remaining upgrade operations:

• As of MySQL 8.0.16, the server does so as part of the previous step, making any changes
required in the mysql system database between MySQL 5.7 and MySQL 8.0, so that you
can take advantage of new privileges or capabilities. It also brings the Performance Schema,
INFORMATION_SCHEMA, and sys databases up to date for MySQL 8.0, and examines all user
databases for incompatibilities with the current version of MySQL.

• Prior to MySQL 8.0.16, the server upgrades only the data dictionary in the previous step. After
the MySQL 8.0 server starts successfully, execute mysql_upgrade to perform the remaining
upgrade tasks:

mysql_upgrade -u root -p

Then shut down and restart the MySQL server to ensure that any changes made to the system
tables take effect. For example:

mysqladmin -u root -p shutdown
mysqld_safe --user=mysql --datadir=/path/to/existing-datadir &

The first time you start the MySQL 8.0 server (in an earlier step), you may notice messages in
the error log regarding nonupgraded tables. If mysql_upgrade has been run successfully, there
should be no such messages the second time you start the server.

Note

The upgrade process does not upgrade the contents of the time zone tables.
For upgrade instructions, see Section 7.1.15, “MySQL Server Time Zone
Support”.

315

Logical Upgrade

If the upgrade process uses mysql_upgrade (that is, prior to MySQL 8.0.16),
the process does not upgrade the contents of the help tables, either. For
upgrade instructions in that case, see Section 7.1.17, “Server-Side Help
Support”.

Logical Upgrade

A logical upgrade involves exporting SQL from the old MySQL instance using a backup or export utility
such as mysqldump or mysqlpump, installing the new MySQL server, and applying the SQL to your
new MySQL instance. For details about what may need upgrading, see Section 3.4, “What the MySQL
Upgrade Process Upgrades”.

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

To identify incompatibilities before upgrading to the latest MySQL 8.0 release,
perform the steps described in Section 3.6, “Preparing Your Installation for
Upgrade”.

To perform a logical upgrade:

1. Review the information in Section 3.1, “Before You Begin”.

2. Export your existing data from the previous MySQL installation:

mysqldump -u root -p
  --add-drop-table --routines --events
  --all-databases --force > data-for-upgrade.sql

Note

Use the --routines and --events options with mysqldump (as shown
above) if your databases include stored programs. The --all-databases
option includes all databases in the dump, including the mysql database
that holds the system tables.

Important

If you have tables that contain generated columns, use the mysqldump
utility provided with MySQL 5.7.9 or higher to create your dump files. The
mysqldump utility provided in earlier releases uses incorrect syntax for
generated column definitions (Bug #20769542). You can use the Information
Schema COLUMNS table to identify tables with generated columns.

3. Shut down the old MySQL server. For example:

mysqladmin -u root -p shutdown

4.

Install MySQL 8.0. For installation instructions, see Chapter 2, Installing MySQL.

316

Logical Upgrade

5.

Initialize a new data directory, as described in Section 2.9.1, “Initializing the Data Directory”. For
example:

mysqld --initialize --datadir=/path/to/8.0-datadir

Copy the temporary 'root'@'localhost' password displayed to your screen or written to your
error log for later use.

6. Start the MySQL 8.0 server, using the new data directory. For example:

mysqld_safe --user=mysql --datadir=/path/to/8.0-datadir &

7. Reset the root password:

$> mysql -u root -p
Enter password: ****  <- enter temporary root password

mysql> ALTER USER USER() IDENTIFIED BY 'your new password';

8. Load the previously created dump file into the new MySQL server. For example:

mysql -u root -p --force < data-for-upgrade.sql

Note

It is not recommended to load a dump file when GTIDs are enabled on
the server (gtid_mode=ON), if your dump file includes system tables.
mysqldump issues DML instructions for the system tables which use the
non-transactional MyISAM storage engine, and this combination is not
permitted when GTIDs are enabled. Also be aware that loading a dump file
from a server with GTIDs enabled, into another server with GTIDs enabled,
causes different transaction identifiers to be generated.

9. Perform any remaining upgrade operations:

• In MySQL 8.0.16 and higher, shut down the server, then restart it with the --upgrade=FORCE

option to perform the remaining upgrade tasks:

mysqladmin -u root -p shutdown
mysqld_safe --user=mysql --datadir=/path/to/8.0-datadir --upgrade=FORCE &

Upon restart with --upgrade=FORCE, the server makes any changes required in the mysql
system schema between MySQL 5.7 and MySQL 8.0, so that you can take advantage of new
privileges or capabilities. It also brings the Performance Schema, INFORMATION_SCHEMA, and
sys schema up to date for MySQL 8.0, and examines all user schemas for incompatibilities with
the current version of MySQL.

• Prior to MySQL 8.0.16, execute mysql_upgrade to perform the remaining upgrade tasks:

mysql_upgrade -u root -p

Then shut down and restart the MySQL server to ensure that any changes made to the system
tables take effect. For example:

mysqladmin -u root -p shutdown
mysqld_safe --user=mysql --datadir=/path/to/8.0-datadir &

Note

The upgrade process does not upgrade the contents of the time zone tables.
For upgrade instructions, see Section 7.1.15, “MySQL Server Time Zone
Support”.

317

MySQL Cluster Upgrade

If the upgrade process uses mysql_upgrade (that is, prior to MySQL 8.0.16),
the process does not upgrade the contents of the help tables, either. For
upgrade instructions in that case, see Section 7.1.17, “Server-Side Help
Support”.

Note

Loading a dump file that contains a MySQL 5.7 mysql schema re-creates two
tables that are no longer used: event and proc. (The corresponding MySQL
8.0 tables are events and routines, both of which are data dictionary tables
and are protected.) After you are satisfied that the upgrade was successful, you
can remove the event and proc tables by executing these SQL statements:

DROP TABLE mysql.event;
DROP TABLE mysql.proc;

MySQL Cluster Upgrade

The information in this section is an adjunct to the in-place upgrade procedure described in In-Place
Upgrade, for use if you are upgrading MySQL Cluster.

As of MySQL 8.0.16, a MySQL Cluster upgrade can be performed as a regular rolling upgrade,
following the usual three ordered steps:

1. Upgrade MGM nodes.

2. Upgrade data nodes one at a time.

3. Upgrade API nodes one at a time (including MySQL servers).

The way to upgrade each of the nodes remains almost the same as prior to MySQL 8.0.16 because
there is a separation between upgrading the data dictionary and upgrading the system tables. There
are two steps to upgrading each individual mysqld:

1.

Import the data dictionary.

Start the new server with the --upgrade=MINIMAL option to upgrade the data dictionary but
not the system tables. This is essentially the same as the pre-MySQL 8.0.16 action of starting the
server and not invoking mysql_upgrade.

The MySQL server must be connected to NDB for this phase to complete. If any NDB or NDBINFO
tables exist, and the server cannot connect to the cluster, it exits with an error message:

Failed to Populate DD tables.

2. Upgrade the system tables.

Prior to MySQL 8.0.16, the DBA invokes the mysql_upgrade client to upgrade the system tables.
As of MySQL 8.0.16, the server performs this action: To upgrade the system tables, restart each
individual mysqld without the --upgrade=MINIMAL option.

3.8 Upgrading MySQL with the MySQL Yum Repository

For supported Yum-based platforms (see Section 2.5.1, “Installing MySQL on Linux Using the MySQL
Yum Repository”, for a list), you can perform an in-place upgrade for MySQL (that is, replacing the old
version and then running the new version using the old data files) with the MySQL Yum repository.

Notes

• Before performing any update to MySQL, follow carefully the instructions in

Chapter 3, Upgrading MySQL. Among other instructions discussed there, it is
especially important to back up your database before the update.

318

Selecting a Target Series

• The following instructions assume you have installed MySQL with the MySQL
Yum repository or with an RPM package directly downloaded from MySQL
Developer Zone's MySQL Download page; if that is not the case, following
the instructions in Replacing a Third-Party Distribution of MySQL Using the
MySQL Yum Repository.

Selecting a Target Series

1.

By default, the MySQL Yum repository updates MySQL to the latest version in the release series
you have chosen during installation (see Selecting a Release Series for details), which means, for
example, a 5.7.x installation is not updated to a 8.0.x release automatically. To update to another
release series, you must first disable the subrepository for the series that has been selected
(by default, or by yourself) and enable the subrepository for your target series. To do that, see
the general instructions given in Selecting a Release Series. For upgrading from MySQL 5.7
to 8.0, perform the reverse of the steps illustrated in Selecting a Release Series, disabling the
subrepository for the MySQL 5.7 series and enabling that for the MySQL 8.0 series.

As a general rule, to upgrade from one release series to another, go to the next series rather than
skipping a series. For example, if you are currently running MySQL 5.6 and wish to upgrade to 8.0,
upgrade to MySQL 5.7 first before upgrading to 8.0.

Important

For important information about upgrading from MySQL 5.7 to 8.0, see
Upgrading from MySQL 5.7 to 8.0.

Upgrading MySQL

2.

Upgrade MySQL and its components by the following command, for platforms that are not dnf-
enabled:

sudo yum update mysql-server

For platforms that are dnf-enabled:

sudo dnf upgrade mysql-server

Alternatively, you can update MySQL by telling Yum to update everything on your system, which
might take considerably more time. For platforms that are not dnf-enabled:

sudo yum update

For platforms that are dnf-enabled:

sudo dnf upgrade

Restarting MySQL

3.

The MySQL server always restarts after an update by Yum. Prior to MySQL 8.0.16, run
mysql_upgrade after the server restarts to check and possibly resolve any incompatibilities
between the old data and the upgraded software. mysql_upgrade also performs other functions;
for details, see Section 6.4.5, “mysql_upgrade — Check and Upgrade MySQL Tables”. As of
MySQL 8.0.16, this step is not required, as the server performs all tasks previously handled by
mysql_upgrade.

You can also update only a specific component. Use the following command to list all the installed
packages for the MySQL components (for dnf-enabled systems, replace yum in the command with
dnf):

sudo yum list installed | grep "^mysql"

319

Upgrading the Shared Client Libraries

After identifying the package name of the component of your choice, update the package with the
following command, replacing package-name with the name of the package. For platforms that are
not dnf-enabled:

sudo yum update package-name

For dnf-enabled platforms:

sudo dnf upgrade package-name

Upgrading the Shared Client Libraries

After updating MySQL using the Yum repository, applications compiled with older versions of the
shared client libraries should continue to work.

If you recompile applications and dynamically link them with the updated libraries:  As typical with new
versions of shared libraries where there are differences or additions in symbol versioning between
the newer and older libraries (for example, between the newer, standard 8.0 shared client libraries
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
the MySQL APT repository. See Upgrading MySQL with the MySQL APT Repository in A Quick Guide
to Using the MySQL APT Repository.

3.10 Upgrading MySQL with the MySQL SLES Repository

On the SUSE Linux Enterprise Server (SLES) platform, to perform an in-place upgrade of MySQL
and its components, use the MySQL SLES repository. See Upgrading MySQL with the MySQL SLES
Repository in A Quick Guide to Using the MySQL SLES Repository.

3.11 Upgrading MySQL on Windows

There are two approaches for upgrading MySQL on Windows:

• Using MySQL Installer

• Using the Windows ZIP archive distribution

The approach you select depends on how the existing installation was performed. Before proceeding,
review Chapter 3, Upgrading MySQL for additional information on upgrading MySQL that is not specific
to Windows.

Note

Whichever approach you choose, always back up your current MySQL
installation before performing an upgrade. See Section 9.2, “Database Backup
Methods”.

Upgrades between non-GA releases (or from a non-GA release to a GA release) are not supported.
Significant development changes take place in non-GA releases and you may encounter compatibility
issues or problems starting the server.

320

Upgrading MySQL with MySQL Installer

Note

MySQL Installer does not support upgrades between Community releases and
Commercial releases. If you require this type of upgrade, perform it using the
ZIP archive approach.

Upgrading MySQL with MySQL Installer

Performing an upgrade with MySQL Installer is the best approach when the current server installation
was performed with it and the upgrade is within the current release series. MySQL Installer does
not support upgrades between release series, such as from 5.7 to 8.0, and it does not provide an
upgrade indicator to prompt you to upgrade. For instructions on upgrading between release series, see
Upgrading MySQL Using the Windows ZIP Distribution.

To perform an upgrade using MySQL Installer:

1. Start MySQL Installer.

2. From the dashboard, click Catalog to download the latest changes to the catalog. The installed

server can be upgraded only if the dashboard displays an arrow next to the version number of the
server.

3. Click Upgrade. All products that have a newer version now appear in a list.

Note

MySQL Installer deselects the server upgrade option for milestone
releases (Pre-Release) in the same release series. In addition, it displays
a warning to indicate that the upgrade is not supported, identifies the risks
of continuing, and provides a summary of the steps to perform an upgrade
manually. You can reselect server upgrade and proceed at your own risk.

4. Deselect all but the MySQL server product, unless you intend to upgrade other products at this

time, and click Next.

5. Click Execute to start the download. When the download finishes, click Next to begin the upgrade

operation.

Upgrades to MySQL 8.0.16 and higher may show an option to skip the upgrade check and process
for system tables. For more information about this option, see Important server upgrade conditions.

6. Configure the server.

Upgrading MySQL Using the Windows ZIP Distribution

To perform an upgrade using the Windows ZIP archive distribution:

1. Download the latest Windows ZIP Archive distribution of MySQL from https://dev.mysql.com/

downloads/.

2.

If the server is running, stop it. If the server is installed as a service, stop the service with the
following command from the command prompt:

C:\> SC STOP mysqld_service_name

Alternatively, use NET STOP mysqld_service_name .

If you are not running the MySQL server as a service, use mysqladmin to stop it. For example,
before upgrading from MySQL 5.7 to 8.0, use mysqladmin from MySQL 5.7 as follows:

321

Upgrading a Docker Installation of MySQL

C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqladmin" -u root shutdown

Note

If the MySQL root user account has a password, invoke mysqladmin with
the -p option and enter the password when prompted.

3. Extract the ZIP archive. You may either overwrite your existing MySQL installation (usually located
at C:\mysql), or install it into a different directory, such as C:\mysql8. Overwriting the existing
installation is recommended.

4. Restart the server. For example, use the SC START mysqld_service_name  or NET START
mysqld_service_name  command if you run MySQL as a service, or invoke mysqld directly
otherwise.

5. Prior to MySQL 8.0.16, run mysql_upgrade as Administrator to check your tables, attempt to

repair them if necessary, and update your grant tables if they have changed so that you can take
advantage of any new capabilities. See Section 6.4.5, “mysql_upgrade — Check and Upgrade
MySQL Tables”. As of MySQL 8.0.16, this step is not required, as the server performs all tasks
previously handled by mysql_upgrade.

6.

If you encounter errors, see Section 2.3.5, “Troubleshooting a Microsoft Windows MySQL Server
Installation”.

3.12 Upgrading a Docker Installation of MySQL

To upgrade a Docker installation of MySQL, refer to Upgrading a MySQL Server Container.

3.13 Upgrade Troubleshooting

• A schema mismatch in a MySQL 5.7 instance between the .frm file of a table and the InnoDB data
dictionary can cause an upgrade to MySQL 8.0 to fail. Such mismatches may be due to .frm file
corruption. To address this issue, dump and restore affected tables before attempting the upgrade
again.

• If problems occur, such as that the new mysqld server does not start, verify that you do not have

an old my.cnf file from your previous installation. You can check this with the --print-defaults
option (for example, mysqld --print-defaults). If this command displays anything other than
the program name, you have an active my.cnf file that affects server or client operation.

• If, after an upgrade, you experience problems with compiled client programs, such as Commands

out of sync or unexpected core dumps, you probably have used old header or library
files when compiling your programs. In this case, check the date for your mysql.h file and
libmysqlclient.a library to verify that they are from the new MySQL distribution. If not, recompile
your programs with the new headers and libraries. Recompilation might also be necessary for
programs compiled against the shared client library if the library major version number has changed
(for example, from libmysqlclient.so.20 to libmysqlclient.so.21).

• If you have created a loadable function with a given name and upgrade MySQL to a version
that implements a new built-in function with the same name, the loadable function becomes
inaccessible. To correct this, use DROP FUNCTION to drop the loadable function, and then use
CREATE FUNCTION to re-create the loadable function with a different nonconflicting name. The
same is true if the new version of MySQL implements a built-in function with the same name as an
existing stored function. See Section 11.2.5, “Function Name Parsing and Resolution”, for the rules
describing how the server interprets references to different kinds of functions.

• If upgrade to MySQL 8.0 fails due to any of the issues outlined in Section 3.6, “Preparing Your

Installation for Upgrade”, the server reverts all changes to the data directory. In this case, remove all

322

Rebuilding or Repairing Tables or Indexes

redo log files and restart the MySQL 5.7 server on the existing data directory to address the errors.
The redo log files (ib_logfile*) reside in the MySQL data directory by default. After the errors
are fixed, perform a slow shutdown (by setting innodb_fast_shutdown=0) before attempting the
upgrade again.

3.14 Rebuilding or Repairing Tables or Indexes

This section describes how to rebuild or repair tables or indexes, which may be necessitated by:

• Changes to how MySQL handles data types or character sets. For example, an error in a collation

might have been corrected, necessitating a table rebuild to update the indexes for character columns
that use the collation.

• Required table repairs or upgrades reported by CHECK TABLE, mysqlcheck, or mysql_upgrade.

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
TABLE operation indicates that there is a corruption or causes InnoDB to fail, refer to Section 17.21.3,
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
mysql db_name < dump.sql

To rebuild all tables in all databases, use the --all-databases option:

mysqldump --all-databases > dump.sql
mysql < dump.sql

ALTER TABLE Method

To rebuild a table with ALTER TABLE, use a “null” alteration; that is, an ALTER TABLE statement that
“changes” the table to use the storage engine that it already has. For example, if t1 is an InnoDB
table, use this statement:

323

REPAIR TABLE Method

ALTER TABLE t1 ENGINE = InnoDB;

If you are not sure which storage engine to specify in the ALTER TABLE statement, use SHOW CREATE
TABLE to display the table definition.

REPAIR TABLE Method

The REPAIR TABLE method is only applicable to MyISAM, ARCHIVE, and CSV tables.

You can use REPAIR TABLE if the table checking operation indicates that there is a corruption or that
an upgrade is required. For example, to repair a MyISAM table, use this statement:

REPAIR TABLE t1;

mysqlcheck --repair provides command-line access to the REPAIR TABLE statement. This can
be a more convenient means of repairing tables because you can use the --databases or --all-
databases option to repair all tables in specific databases or all databases, respectively:

mysqlcheck --repair --databases db_name ...
mysqlcheck --repair --all-databases

3.15 Copying MySQL Databases to Another Machine

In cases where you need to transfer databases between different architectures, you can use
mysqldump to create a file containing SQL statements. You can then transfer the file to the other
machine and feed it as input to the mysql client.

Use mysqldump --help to see what options are available.

Note

If GTIDs are in use on the server where you create the dump (gtid_mode=ON),
by default, mysqldump includes the contents of the gtid_executed set in
the dump to transfer these to the new machine. The results of this can vary
depending on the MySQL Server versions involved. Check the description for
mysqldump's --set-gtid-purged option to find what happens with the
versions you are using, and how to change the behavior if the outcome of the
default behavior is not suitable for your situation.

The easiest (although not the fastest) way to move a database between two machines is to run the
following commands on the machine on which the database is located:

mysqladmin -h 'other_hostname' create db_name
mysqldump db_name | mysql -h 'other_hostname' db_name

If you want to copy a database from a remote machine over a slow network, you can use these
commands:

mysqladmin create db_name
mysqldump -h 'other_hostname' --compress db_name | mysql db_name

You can also store the dump in a file, transfer the file to the target machine, and then load the file
into the database there. For example, you can dump a database to a compressed file on the source
machine like this:

mysqldump --quick db_name | gzip > db_name.gz

Transfer the file containing the database contents to the target machine and run these commands
there:

mysqladmin create db_name

324

Copying MySQL Databases to Another Machine

gunzip < db_name.gz | mysql db_name

You can also use mysqldump and mysqlimport to transfer the database. For large tables, this is
much faster than simply using mysqldump. In the following commands, DUMPDIR represents the full
path name of the directory you use to store the output from mysqldump.

First, create the directory for the output files and dump the database:

mkdir DUMPDIR
mysqldump --tab=DUMPDIR
   db_name

Then transfer the files in the DUMPDIR directory to some corresponding directory on the target machine
and load the files into MySQL there:

mysqladmin create db_name           # create database
cat DUMPDIR/*.sql | mysql db_name   # create tables in database
mysqlimport db_name
   DUMPDIR/*.txt   # load data into tables

Do not forget to copy the mysql database because that is where the grant tables are stored. You
might have to run commands as the MySQL root user on the new machine until you have the mysql
database in place.

After you import the mysql database on the new machine, execute mysqladmin flush-
privileges so that the server reloads the grant table information.

325

326

