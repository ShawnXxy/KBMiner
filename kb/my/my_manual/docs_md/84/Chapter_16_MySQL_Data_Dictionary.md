How the Data Dictionary is Upgraded

queries, whereas system tables contain auxiliary data such as time zone and help information. MySQL
system tables and data dictionary tables also differ in how they are upgraded. The MySQL server
manages data dictionary upgrades. See How the Data Dictionary is Upgraded. Upgrading MySQL
system tables requires running the full MySQL upgrade procedure. See Section 3.4, “What the MySQL
Upgrade Process Upgrades”.

How the Data Dictionary is Upgraded

New versions of MySQL may include changes to data dictionary table definitions. Such changes are
present in newly installed versions of MySQL, but when performing an in-place upgrade of MySQL
binaries, changes are applied when the MySQL server is restarted using the new binaries. At startup,
the data dictionary version of the server is compared to the version information stored in the data
dictionary to determine if data dictionary tables should be upgraded. If an upgrade is necessary and
supported, the server creates data dictionary tables with updated definitions, copies persisted metadata
to the new tables, atomically replaces the old tables with the new ones, and reinitializes the data
dictionary. If an upgrade is not necessary, startup continues without updating the data dictionary tables.

Upgrade of data dictionary tables is an atomic operation, which means that all of the data dictionary
tables are upgraded as necessary or the operation fails. If the upgrade operation fails, server startup
fails with an error. In this case, the old server binaries can be used with the old data directory to
start the server. When the new server binaries are used again to start the server, the data dictionary
upgrade is reattempted.

Generally, after data dictionary tables are successfully upgraded, it is not possible to restart the server
using the old server binaries. As a result, downgrading MySQL server binaries to a previous MySQL
version is not supported after data dictionary tables are upgraded.

Viewing Data Dictionary Tables Using a Debug Build of MySQL

Data dictionary tables are protected by default but can be accessed by compiling MySQL
with debugging support (using the -DWITH_DEBUG=1 CMake option) and specifying the
+d,skip_dd_table_access_check debug option and modifier. For information about compiling
debug builds, see Section 7.9.1.1, “Compiling MySQL for Debugging”.

Warning

Modifying or writing to data dictionary tables directly is not recommended and
may render your MySQL instance inoperable.

After compiling MySQL with debugging support, use this SET statement to make data dictionary tables
visible to the mysql client session:

mysql> SET SESSION debug='+d,skip_dd_table_access_check';

Use this query to retrieve a list of data dictionary tables:

mysql> SELECT name, schema_id, hidden, type FROM mysql.tables where schema_id=1 AND hidden='System';

Use SHOW CREATE TABLE to view data dictionary table definitions. For example:

mysql> SHOW CREATE TABLE mysql.catalogs\G

16.2 Removal of File-based Metadata Storage

In previous MySQL releases, dictionary data was partially stored in metadata files. Issues with file-
based metadata storage included expensive file scans, susceptibility to file system-related bugs,
complex code for handling of replication and crash recovery failure states, and a lack of extensibility
that made it difficult to add metadata for new features and relational objects.

The metadata files listed below are removed from MySQL. Unless otherwise noted, data previously
stored in metadata files is now stored in data dictionary tables.

• .frm files: Table metadata files. With the removal of .frm files:

2946

Data Dictionary Limitations

• Previously, it was possible to dump stored routine and event definitions together with their creation
and modification timestamps, by dumping the proc and event tables. As of MySQL 8.4, those
tables are not used, so it is not possible to dump timestamps.

• Previously, creating a stored routine that contains illegal characters produced a warning. As of

MySQL 8.4, this is an error.

16.8 Data Dictionary Limitations

This section describes temporary limitations introduced with the MySQL data dictionary.

• Manual creation of database directories under the data directory (for example, with mkdir) is

unsupported. Manually created database directories are not recognized by the MySQL Server.

• DDL operations take longer due to writing to storage, undo logs, and redo logs instead of .frm files.

2952

