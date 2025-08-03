Setting the Storage Engine

Feature

MyISAM

Memory

InnoDB

Archive

Yes (note 6)

No

No

No

No

Yes

N/A

Table

No

Yes

Yes (note 7)

No (note 8)

Yes

Row

Yes

Limited (note 9) Yes

RAM

No

No

Yes

64TB

No

Yes

Yes

Yes

No

No

No

Row

No

Yes

None

No

No

Yes

NDB

No

Yes

No

Yes

Yes

Row

No

Yes

384EB

Yes

Yes

Yes

Full-text search
indexes

Geospatial data
type support

Geospatial
indexing support

Hash indexes

Index caches

Yes

Yes

Yes

No

Yes

Locking
granularity

MVCC

Replication
support (note 1)

Table

No

Yes

Storage limits

256TB

T-tree indexes

Transactions

Update statistics
for data
dictionary

No

No

Yes

Notes:

1. Implemented in the server, rather than in the storage engine.

2. Compressed MyISAM tables are supported only when using the compressed row format. Tables using
the compressed row format with MyISAM are read only.

3. Implemented in the server via encryption functions.

4. Implemented in the server via encryption functions; In MySQL 5.7 and later, data-at-rest encryption is
supported.

5. Implemented in the server via encryption functions; encrypted NDB backups as of NDB 8.0.22;
transparent NDB file system encryption supported in NDB 8.0.29 and later.

6. Support for FULLTEXT indexes is available in MySQL 5.6 and later.

7. Support for geospatial indexing is available in MySQL 5.7 and later.

8. InnoDB utilizes hash indexes internally for its Adaptive Hash Index feature.

9. See the discussion later in this section.

15.1 Setting the Storage Engine

When you create a new table, you can specify which storage engine to use by adding an ENGINE table
option to the CREATE TABLE statement:

-- ENGINE=INNODB not needed unless you have set a different
-- default storage engine.
CREATE TABLE t1 (i INT) ENGINE = INNODB;
-- Simple table definitions can be switched from one to another.

2918

The MyISAM Storage Engine

CREATE TABLE t2 (i INT) ENGINE = CSV;
CREATE TABLE t3 (i INT) ENGINE = MEMORY;

When you omit the ENGINE option, the default storage engine is used. The default engine is InnoDB
in MySQL 5.7. You can specify the default engine by using the --default-storage-engine server
startup option, or by setting the default-storage-engine option in the my.cnf configuration file.

You can set the default storage engine for the current session by setting the default_storage_engine
variable:

SET default_storage_engine=NDBCLUSTER;

The storage engine for TEMPORARY tables created with CREATE TEMPORARY TABLE can be set
separately from the engine for permanent tables by setting the default_tmp_storage_engine, either
at startup or at runtime.

To convert a table from one storage engine to another, use an ALTER TABLE statement that indicates the
new engine:

ALTER TABLE t ENGINE = InnoDB;

See Section 13.1.18, “CREATE TABLE Statement”, and Section 13.1.8, “ALTER TABLE Statement”.

If you try to use a storage engine that is not compiled in or that is compiled in but deactivated, MySQL
instead creates a table using the default storage engine. For example, in a replication setup, perhaps your
source server uses InnoDB tables for maximum safety, but the replica servers use other storage engines
for speed at the expense of durability or concurrency.

By default, a warning is generated whenever CREATE TABLE or ALTER TABLE cannot use the default
storage engine. To prevent confusing, unintended behavior if the desired engine is unavailable, enable
the NO_ENGINE_SUBSTITUTION SQL mode. If the desired engine is unavailable, this setting produces
an error instead of a warning, and the table is not created or altered. See Section 5.1.10, “Server SQL
Modes”.

For new tables, MySQL always creates an .frm file to hold the table and column definitions. The table's
index and data may be stored in one or more other files, depending on the storage engine. The server
creates the .frm file above the storage engine level. Individual storage engines create any additional
files required for the tables that they manage. If a table name contains special characters, the names for
the table files contain encoded versions of those characters as described in Section 9.2.4, “Mapping of
Identifiers to File Names”.

15.2 The MyISAM Storage Engine

MyISAM is based on the older (and no longer available) ISAM storage engine but has many useful
extensions.

Table 15.2 MyISAM Storage Engine Features

Feature

B-tree indexes

Backup/point-in-time recovery (Implemented in
the server, rather than in the storage engine.)

Cluster database support

Clustered indexes

Compressed data

Support

Yes

Yes

No

No

Yes (Compressed MyISAM tables are supported
only when using the compressed row format. Tables

2919

MyISAM Table Storage Formats

String indexes are space compressed. If the first index part is a string, it is also prefix compressed. Space
compression makes the index file smaller than the worst-case figure if a string column has a lot of trailing
space or is a VARCHAR column that is not always used to the full length. Prefix compression is used on
keys that start with a string. Prefix compression helps if there are many strings with an identical prefix.

In MyISAM tables, you can also prefix compress numbers by specifying the PACK_KEYS=1 table option
when you create the table. Numbers are stored with the high byte first, so this helps when you have many
integer keys that have an identical prefix.

15.2.3 MyISAM Table Storage Formats

MyISAM supports three different storage formats. Two of them, fixed and dynamic format, are chosen
automatically depending on the type of columns you are using. The third, compressed format, can be
created only with the myisampack utility (see Section 4.6.5, “myisampack — Generate Compressed,
Read-Only MyISAM Tables”).

When you use CREATE TABLE or ALTER TABLE for a table that has no BLOB or TEXT columns, you can
force the table format to FIXED or DYNAMIC with the ROW_FORMAT table option.

See Section 13.1.18, “CREATE TABLE Statement”, for information about ROW_FORMAT.

You can decompress (unpack) compressed MyISAM tables using myisamchk --unpack; see
Section 4.6.3, “myisamchk — MyISAM Table-Maintenance Utility”, for more information.

15.2.3.1 Static (Fixed-Length) Table Characteristics

Static format is the default for MyISAM tables. It is used when the table contains no variable-length columns
(VARCHAR, VARBINARY, BLOB, or TEXT). Each row is stored using a fixed number of bytes.

Of the three MyISAM storage formats, static format is the simplest and most secure (least subject to
corruption). It is also the fastest of the on-disk formats due to the ease with which rows in the data file can
be found on disk: To look up a row based on a row number in the index, multiply the row number by the
row length to calculate the row position. Also, when scanning a table, it is very easy to read a constant
number of rows with each disk read operation.

The security is evidenced if your computer crashes while the MySQL server is writing to a fixed-format
MyISAM file. In this case, myisamchk can easily determine where each row starts and ends, so it can
usually reclaim all rows except the partially written one. MyISAM table indexes can always be reconstructed
based on the data rows.

Note

Fixed-length row format is only available for tables without BLOB or TEXT columns.
Creating a table with these columns with an explicit ROW_FORMAT clause does not
raise an error or warning; the format specification is ignored.

Static-format tables have these characteristics:

• CHAR and VARCHAR columns are space-padded to the specified column width, although the column type

is not altered. BINARY and VARBINARY columns are padded with 0x00 bytes to the column width.

• NULL columns require additional space in the row to record whether their values are NULL. Each NULL

column takes one bit extra, rounded up to the nearest byte.

• Very quick.

• Easy to cache.

2924

MyISAM Table Storage Formats

• Easy to reconstruct after a crash, because rows are located in fixed positions.

• Reorganization is unnecessary unless you delete a huge number of rows and want to return free disk

space to the operating system. To do this, use OPTIMIZE TABLE or myisamchk -r.

• Usually require more disk space than dynamic-format tables.

• The expected row length in bytes for static-sized rows is calculated using the following expression:

row length = 1
             + (sum of column lengths)
             + (number of NULL columns + delete_flag + 7)/8
             + (number of variable-length columns)

delete_flag is 1 for tables with static row format. Static tables use a bit in the row record for a flag that
indicates whether the row has been deleted. delete_flag is 0 for dynamic tables because the flag is
stored in the dynamic row header.

15.2.3.2 Dynamic Table Characteristics

Dynamic storage format is used if a MyISAM table contains any variable-length columns (VARCHAR,
VARBINARY, BLOB, or TEXT), or if the table was created with the ROW_FORMAT=DYNAMIC table option.

Dynamic format is a little more complex than static format because each row has a header that indicates
how long it is. A row can become fragmented (stored in noncontiguous pieces) when it is made longer as a
result of an update.

You can use OPTIMIZE TABLE or myisamchk -r to defragment a table. If you have fixed-length
columns that you access or change frequently in a table that also contains some variable-length columns, it
might be a good idea to move the variable-length columns to other tables just to avoid fragmentation.

Dynamic-format tables have these characteristics:

• All string columns are dynamic except those with a length less than four.

• Each row is preceded by a bitmap that indicates which columns contain the empty string (for string

columns) or zero (for numeric columns). This does not include columns that contain NULL values. If a
string column has a length of zero after trailing space removal, or a numeric column has a value of zero,
it is marked in the bitmap and not saved to disk. Nonempty strings are saved as a length byte plus the
string contents.

• NULL columns require additional space in the row to record whether their values are NULL. Each NULL

column takes one bit extra, rounded up to the nearest byte.

• Much less disk space usually is required than for fixed-length tables.

• Each row uses only as much space as is required. However, if a row becomes larger, it is split into as
many pieces as are required, resulting in row fragmentation. For example, if you update a row with
information that extends the row length, the row becomes fragmented. In this case, you may have to run
OPTIMIZE TABLE or myisamchk -r from time to time to improve performance. Use myisamchk -ei
to obtain table statistics.

• More difficult than static-format tables to reconstruct after a crash, because rows may be fragmented into

many pieces and links (fragments) may be missing.

• The expected row length for dynamic-sized rows is calculated using the following expression:

3
+ (number of columns + 7) / 8

2925

MyISAM Table Problems

+ (number of char columns)
+ (packed size of numeric columns)
+ (length of strings)
+ (number of NULL columns + 7) / 8

There is a penalty of 6 bytes for each link. A dynamic row is linked whenever an update causes an
enlargement of the row. Each new link is at least 20 bytes, so the next enlargement probably goes in the
same link. If not, another link is created. You can find the number of links using myisamchk -ed. All
links may be removed with OPTIMIZE TABLE or myisamchk -r.

15.2.3.3 Compressed Table Characteristics

Compressed storage format is a read-only format that is generated with the myisampack tool.
Compressed tables can be uncompressed with myisamchk.

Compressed tables have the following characteristics:

• Compressed tables take very little disk space. This minimizes disk usage, which is helpful when using

slow disks (such as CD-ROMs).

• Each row is compressed separately, so there is very little access overhead. The header for a row takes
up one to three bytes depending on the biggest row in the table. Each column is compressed differently.
There is usually a different Huffman tree for each column. Some of the compression types are:

• Suffix space compression.

• Prefix space compression.

• Numbers with a value of zero are stored using one bit.

• If values in an integer column have a small range, the column is stored using the smallest possible

type. For example, a BIGINT column (eight bytes) can be stored as a TINYINT column (one byte) if
all its values are in the range from -128 to 127.

• If a column has only a small set of possible values, the data type is converted to ENUM.

• A column may use any combination of the preceding compression types.

• Can be used for fixed-length or dynamic-length rows.

Note

While a compressed table is read only, and you cannot therefore update or add
rows in the table, DDL (Data Definition Language) operations are still valid. For
example, you may still use DROP to drop the table, and TRUNCATE TABLE to empty
the table.

15.2.4 MyISAM Table Problems

The file format that MySQL uses to store data has been extensively tested, but there are always
circumstances that may cause database tables to become corrupted. The following discussion describes
how this can happen and how to handle it.

15.2.4.1 Corrupted MyISAM Tables

Even though the MyISAM table format is very reliable (all changes to a table made by an SQL statement
are written before the statement returns), you can still get corrupted tables if any of the following events
occur:

2926

Characteristics of MEMORY Tables

Despite the in-memory processing for MEMORY tables, they are not necessarily faster than InnoDB tables
on a busy server, for general-purpose queries, or under a read/write workload. In particular, the table
locking involved with performing updates can slow down concurrent usage of MEMORY tables from multiple
sessions.

Depending on the kinds of queries performed on a MEMORY table, you might create indexes as either the
default hash data structure (for looking up single values based on a unique key), or a general-purpose B-
tree data structure (for all kinds of queries involving equality, inequality, or range operators such as less
than or greater than). The following sections illustrate the syntax for creating both kinds of indexes. A
common performance issue is using the default hash indexes in workloads where B-tree indexes are more
efficient.

Characteristics of MEMORY Tables

The MEMORY storage engine associates each table with one disk file, which stores the table definition (not
the data). The file name begins with the table name and has an extension of .frm.

MEMORY tables have the following characteristics:

• Space for MEMORY tables is allocated in small blocks. Tables use 100% dynamic hashing for inserts. No
overflow area or extra key space is needed. No extra space is needed for free lists. Deleted rows are put
in a linked list and are reused when you insert new data into the table. MEMORY tables also have none of
the problems commonly associated with deletes plus inserts in hashed tables.

• MEMORY tables use a fixed-length row-storage format. Variable-length types such as VARCHAR are stored

using a fixed length.

• MEMORY tables cannot contain BLOB or TEXT columns.

• MEMORY includes support for AUTO_INCREMENT columns.

• Non-TEMPORARY MEMORY tables are shared among all clients, just like any other non-TEMPORARY table.

DDL Operations for MEMORY Tables

To create a MEMORY table, specify the clause ENGINE=MEMORY on the CREATE TABLE statement.

CREATE TABLE t (i INT) ENGINE = MEMORY;

As indicated by the engine name, MEMORY tables are stored in memory. They use hash indexes by default,
which makes them very fast for single-value lookups, and very useful for creating temporary tables.
However, when the server shuts down, all rows stored in MEMORY tables are lost. The tables themselves
continue to exist because their definitions are stored in .frm files on disk, but they are empty when the
server restarts.

This example shows how you might create, use, and remove a MEMORY table:

mysql> CREATE TABLE test ENGINE=MEMORY
           SELECT ip,SUM(downloads) AS down
           FROM log_table GROUP BY ip;
mysql> SELECT COUNT(ip),AVG(down) FROM test;
mysql> DROP TABLE test;

The maximum size of MEMORY tables is limited by the max_heap_table_size system variable, which
has a default value of 16MB. To enforce different size limits for MEMORY tables, change the value of this
variable. The value in effect for CREATE TABLE, or a subsequent ALTER TABLE or TRUNCATE TABLE,

2930

Indexes

is the value used for the life of the table. A server restart also sets the maximum size of existing MEMORY
tables to the global max_heap_table_size value. You can set the size for individual tables as described
later in this section.

Indexes

The MEMORY storage engine supports both HASH and BTREE indexes. You can specify one or the other for
a given index by adding a USING clause as shown here:

CREATE TABLE lookup
    (id INT, INDEX USING HASH (id))
    ENGINE = MEMORY;
CREATE TABLE lookup
    (id INT, INDEX USING BTREE (id))
    ENGINE = MEMORY;

For general characteristics of B-tree and hash indexes, see Section 8.3.1, “How MySQL Uses Indexes”.

MEMORY tables can have up to 64 indexes per table, 16 columns per index and a maximum key length of
3072 bytes.

If a MEMORY table hash index has a high degree of key duplication (many index entries containing the
same value), updates to the table that affect key values and all deletes are significantly slower. The
degree of this slowdown is proportional to the degree of duplication (or, inversely proportional to the index
cardinality). You can use a BTREE index to avoid this problem.

MEMORY tables can have nonunique keys. (This is an uncommon feature for implementations of hash
indexes.)

Columns that are indexed can contain NULL values.

User-Created and Temporary Tables

MEMORY table contents are stored in memory, which is a property that MEMORY tables share with internal
temporary tables that the server creates on the fly while processing queries. However, the two types of
tables differ in that MEMORY tables are not subject to storage conversion, whereas internal temporary tables
are:

• If an internal temporary table becomes too large, the server automatically converts it to on-disk storage,

as described in Section 8.4.4, “Internal Temporary Table Use in MySQL”.

• User-created MEMORY tables are never converted to disk tables.

Loading Data

To populate a MEMORY table when the MySQL server starts, you can use the init_file system variable.
For example, you can put statements such as INSERT INTO ... SELECT or LOAD DATA into a file to
load the table from a persistent data source, and use init_file to name the file. See Section 5.1.7,
“Server System Variables”, and Section 13.2.6, “LOAD DATA Statement”.

MEMORY Tables and Replication

When a replication source server shuts down and restarts, its MEMORY tables become empty. To replicate
this effect to replicas, the first time that the source uses a given MEMORY table after startup, it logs an
event that notifies replicas that the table must be emptied by writing a DELETE or (from MySQL 5.7.32)

2931

Managing Memory Use

TRUNCATE TABLE statement for that table to the binary log. When a replica server shuts down and
restarts, its MEMORY tables also become empty, and it writes a DELETE or (from MySQL 5.7.32) TRUNCATE
TABLE statement to its own binary log, which is passed on to any downstream replicas.

When you use MEMORY tables in a replication topology, in some situations, the table on the source and the
table on the replica may differ. For information on handling each of these situations to prevent stale reads
or errors, see Section 16.4.1.20, “Replication and MEMORY Tables”.

Managing Memory Use

The server needs sufficient memory to maintain all MEMORY tables that are in use at the same time.

Memory is not reclaimed if you delete individual rows from a MEMORY table. Memory is reclaimed only
when the entire table is deleted. Memory that was previously used for deleted rows is re-used for new
rows within the same table. To free all the memory used by a MEMORY table when you no longer require
its contents, execute DELETE or TRUNCATE TABLE to remove all rows, or remove the table altogether
using DROP TABLE. To free up the memory used by deleted rows, use ALTER TABLE ENGINE=MEMORY
to force a table rebuild.

The memory needed for one row in a MEMORY table is calculated using the following expression:

SUM_OVER_ALL_BTREE_KEYS(max_length_of_key + sizeof(char*) * 4)
+ SUM_OVER_ALL_HASH_KEYS(sizeof(char*) * 2)
+ ALIGN(length_of_row+1, sizeof(char*))

ALIGN() represents a round-up factor to cause the row length to be an exact multiple of the char pointer
size. sizeof(char*) is 4 on 32-bit machines and 8 on 64-bit machines.

As mentioned earlier, the max_heap_table_size system variable sets the limit on the maximum size
of MEMORY tables. To control the maximum size for individual tables, set the session value of this variable
before creating each table. (Do not change the global max_heap_table_size value unless you intend
the value to be used for MEMORY tables created by all clients.) The following example creates two MEMORY
tables, with a maximum size of 1MB and 2MB, respectively:

mysql> SET max_heap_table_size = 1024*1024;
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1 (id INT, UNIQUE(id)) ENGINE = MEMORY;
Query OK, 0 rows affected (0.01 sec)

mysql> SET max_heap_table_size = 1024*1024*2;
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t2 (id INT, UNIQUE(id)) ENGINE = MEMORY;
Query OK, 0 rows affected (0.00 sec)

Both tables revert to the server's global max_heap_table_size value if the server restarts.

You can also specify a MAX_ROWS table option in CREATE TABLE statements for MEMORY tables to provide
a hint about the number of rows you plan to store in them. This does not enable the table to grow beyond
the max_heap_table_size value, which still acts as a constraint on maximum table size. For maximum
flexibility in being able to use MAX_ROWS, set max_heap_table_size at least as high as the value to
which you want each MEMORY table to be able to grow.

Additional Resources

A forum dedicated to the MEMORY storage engine is available at https://forums.mysql.com/list.php?92.

2932

The CSV Storage Engine

15.4 The CSV Storage Engine

The CSV storage engine stores data in text files using comma-separated values format.

The CSV storage engine is always compiled into the MySQL server.

To examine the source for the CSV engine, look in the storage/csv directory of a MySQL source
distribution.

When you create a CSV table, the server creates a table format file in the database directory. The file
begins with the table name and has an .frm extension. The storage engine also creates plain text data file
having a name that begins with the table name and has a .CSV extension. When you store data into the
table, the storage engine saves it into the data file in comma-separated values format.

mysql> CREATE TABLE test (i INT NOT NULL, c CHAR(10) NOT NULL)
       ENGINE = CSV;
Query OK, 0 rows affected (0.06 sec)

mysql> INSERT INTO test VALUES(1,'record one'),(2,'record two');
Query OK, 2 rows affected (0.05 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM test;
+---+------------+
| i | c          |
+---+------------+
| 1 | record one |
| 2 | record two |
+---+------------+
2 rows in set (0.00 sec)

Creating a CSV table also creates a corresponding metafile that stores the state of the table and the
number of rows that exist in the table. The name of this file is the same as the name of the table with the
extension CSM.

If you examine the test.CSV file in the database directory created by executing the preceding statements,
its contents should look like this:

"1","record one"
"2","record two"

This format can be read, and even written, by spreadsheet applications such as Microsoft Excel.

15.4.1 Repairing and Checking CSV Tables

The CSV storage engine supports the CHECK TABLE and REPAIR TABLE statements to verify and, if
possible, repair a damaged CSV table.

When running the CHECK TABLE statement, the CSV file is checked for validity by looking for the correct
field separators, escaped fields (matching or missing quotation marks), the correct number of fields
compared to the table definition and the existence of a corresponding CSV metafile. The first invalid row
discovered reports an error. Checking a valid table produces output like that shown below:

mysql> CHECK TABLE csvtest;
+--------------+-------+----------+----------+
| Table        | Op    | Msg_type | Msg_text |
+--------------+-------+----------+----------+
| test.csvtest | check | status   | OK       |
+--------------+-------+----------+----------+

2933

CSV Limitations

A check on a corrupted table returns a fault such as

mysql> CHECK TABLE csvtest;
+--------------+-------+----------+----------+
| Table        | Op    | Msg_type | Msg_text |
+--------------+-------+----------+----------+
| test.csvtest | check | error    | Corrupt  |
+--------------+-------+----------+----------+

To repair a table, use REPAIR TABLE, which copies as many valid rows from the existing CSV data as
possible, and then replaces the existing CSV file with the recovered rows. Any rows beyond the corrupted
data are lost.

mysql> REPAIR TABLE csvtest;
+--------------+--------+----------+----------+
| Table        | Op     | Msg_type | Msg_text |
+--------------+--------+----------+----------+
| test.csvtest | repair | status   | OK       |
+--------------+--------+----------+----------+

Warning

During repair, only the rows from the CSV file up to the first damaged row are copied
to the new table. All other rows from the first damaged row to the end of the table
are removed, even valid rows.

15.4.2 CSV Limitations

The CSV storage engine does not support indexing.

Partitioning is not supported for tables using the CSV storage engine.

All tables that you create using the CSV storage engine must have the NOT NULL attribute on all columns.

15.5 The ARCHIVE Storage Engine

The ARCHIVE storage engine produces special-purpose tables that store large amounts of unindexed data
in a very small footprint.

Table 15.5 ARCHIVE Storage Engine Features

Feature

B-tree indexes

Backup/point-in-time recovery (Implemented in
the server, rather than in the storage engine.)

Cluster database support

Clustered indexes

Compressed data

Data caches

Encrypted data

Support

No

Yes

No

No

Yes

No

Yes (Implemented in the server via encryption
functions.)

Foreign key support

Full-text search indexes

No

No

2934

The ARCHIVE Storage Engine

Feature

Geospatial data type support

Geospatial indexing support

Hash indexes

Index caches

Locking granularity

MVCC

Replication support (Implemented in the server,
rather than in the storage engine.)

Storage limits

T-tree indexes

Transactions

Update statistics for data dictionary

Support

Yes

No

No

No

Row

No

Yes

None

No

No

Yes

The ARCHIVE storage engine is included in MySQL binary distributions. To enable this storage engine if
you build MySQL from source, invoke CMake with the -DWITH_ARCHIVE_STORAGE_ENGINE option.

To examine the source for the ARCHIVE engine, look in the storage/archive directory of a MySQL
source distribution.

You can check whether the ARCHIVE storage engine is available with the SHOW ENGINES statement.

When you create an ARCHIVE table, the server creates a table format file in the database directory. The
file begins with the table name and has an .frm extension. The storage engine creates other files, all
having names beginning with the table name. The data file has an extension of .ARZ. An .ARN file may
appear during optimization operations.

The ARCHIVE engine supports INSERT, REPLACE, and SELECT, but not DELETE or UPDATE. It does
support ORDER BY operations, BLOB columns, and basically all data types including spatial data types
(see Section 11.4.1, “Spatial Data Types”). Geographic spatial reference systems are not supported. The
ARCHIVE engine uses row-level locking.

The ARCHIVE engine supports the AUTO_INCREMENT column attribute. The AUTO_INCREMENT column
can have either a unique or nonunique index. Attempting to create an index on any other column results
in an error. The ARCHIVE engine also supports the AUTO_INCREMENT table option in CREATE TABLE
statements to specify the initial sequence value for a new table or reset the sequence value for an existing
table, respectively.

ARCHIVE does not support inserting a value into an AUTO_INCREMENT column less than the current
maximum column value. Attempts to do so result in an ER_DUP_KEY error.

The ARCHIVE engine ignores BLOB columns if they are not requested and scans past them while reading.

Storage: Rows are compressed as they are inserted. The ARCHIVE engine uses zlib lossless data
compression (see http://www.zlib.net/). You can use OPTIMIZE TABLE to analyze the table and pack it
into a smaller format (for a reason to use OPTIMIZE TABLE, see later in this section). The engine also
supports CHECK TABLE. There are several types of insertions that are used:

• An INSERT statement just pushes rows into a compression buffer, and that buffer flushes as necessary.

The insertion into the buffer is protected by a lock. A SELECT forces a flush to occur.

2935

Additional Resources

• A bulk insert is visible only after it completes, unless other inserts occur at the same time, in which case
it can be seen partially. A SELECT never causes a flush of a bulk insert unless a normal insert occurs
while it is loading.

Retrieval: On retrieval, rows are uncompressed on demand; there is no row cache. A SELECT operation
performs a complete table scan: When a SELECT occurs, it finds out how many rows are currently
available and reads that number of rows. SELECT is performed as a consistent read. Note that lots of
SELECT statements during insertion can deteriorate the compression, unless only bulk or delayed inserts
are used. To achieve better compression, you can use OPTIMIZE TABLE or REPAIR TABLE. The number
of rows in ARCHIVE tables reported by SHOW TABLE STATUS is always accurate. See Section 13.7.2.4,
“OPTIMIZE TABLE Statement”, Section 13.7.2.5, “REPAIR TABLE Statement”, and Section 13.7.5.36,
“SHOW TABLE STATUS Statement”.

Additional Resources

• A forum dedicated to the ARCHIVE storage engine is available at https://forums.mysql.com/list.php?112.

15.6 The BLACKHOLE Storage Engine

The BLACKHOLE storage engine acts as a “black hole” that accepts data but throws it away and does not
store it. Retrievals always return an empty result:

mysql> CREATE TABLE test(i INT, c CHAR(10)) ENGINE = BLACKHOLE;
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO test VALUES(1,'record one'),(2,'record two');
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM test;
Empty set (0.00 sec)

To enable the BLACKHOLE storage engine if you build MySQL from source, invoke CMake with the -
DWITH_BLACKHOLE_STORAGE_ENGINE option.

To examine the source for the BLACKHOLE engine, look in the sql directory of a MySQL source
distribution.

When you create a BLACKHOLE table, the server creates a table format file in the database directory. The
file begins with the table name and has an .frm extension. There are no other files associated with the
table.

The BLACKHOLE storage engine supports all kinds of indexes. That is, you can include index declarations
in the table definition.

The maximum key length is 1000 bytes.

You can check whether the BLACKHOLE storage engine is available with the SHOW ENGINES statement.

Inserts into a BLACKHOLE table do not store any data, but if statement based binary logging is enabled,
the SQL statements are logged and replicated to replica servers. This can be useful as a repeater or filter
mechanism.

Suppose that your application requires replica-side filtering rules, but transferring all binary log data to the
replica first results in too much traffic. In such a case, it is possible to set up on the source host a “dummy”
replica process whose default storage engine is BLACKHOLE, depicted as follows:

2936

The BLACKHOLE Storage Engine

Figure 15.1 Replication using BLACKHOLE for Filtering

The source writes to its binary log. The “dummy” mysqld process acts as a replica, applying the desired
combination of replicate-do-* and replicate-ignore-* rules, and writes a new, filtered binary log
of its own. (See Section 16.1.6, “Replication and Binary Logging Options and Variables”.) This filtered log
is provided to the replica.

The dummy process does not actually store any data, so there is little processing overhead incurred by
running the additional mysqld process on the replication source host. This type of setup can be repeated
with additional replication replicas.

INSERT triggers for BLACKHOLE tables work as expected. However, because the BLACKHOLE table does
not actually store any data, UPDATE and DELETE triggers are not activated: The FOR EACH ROW clause in
the trigger definition does not apply because there are no rows.

Other possible uses for the BLACKHOLE storage engine include:

• Verification of dump file syntax.

• Measurement of the overhead from binary logging, by comparing performance using BLACKHOLE with

and without binary logging enabled.

• BLACKHOLE is essentially a “no-op” storage engine, so it could be used for finding performance

bottlenecks not related to the storage engine itself.

The BLACKHOLE engine is transaction-aware, in the sense that committed transactions are written to the
binary log and rolled-back transactions are not.

Blackhole Engine and Auto Increment Columns

The Blackhole engine is a no-op engine. Any operations performed on a table using BLACKHOLE have
no effect. This should be borne in mind when considering the behavior of primary key columns that auto
increment. The engine does not automatically increment field values, and does not retain auto increment
column state. This has important implications in replication.

2937

The MERGE Storage Engine

Consider the following replication scenario where all three of the following conditions apply:

1. On a source server there is a blackhole table with an auto increment field that is a primary key.

2. On a replica the same table exists but using the MyISAM engine.

3.

Inserts are performed into the source's table without explicitly setting the auto increment value in the
INSERT statement itself or through using a SET INSERT_ID statement.

In this scenario, replication fails with a duplicate entry error on the primary key column.

In statement based replication, the value of INSERT_ID in the context event is always the same.
Replication therefore fails due to trying insert a row with a duplicate value for a primary key column.

In row based replication, the value that the engine returns for the row always be the same for each insert.
This results in the replica attempting to replay two insert log entries using the same value for the primary
key column, and so replication fails.

Column Filtering

When using row-based replication, (binlog_format=ROW), a replica where the last columns are missing
from a table is supported, as described in the section Section 16.4.1.10, “Replication with Differing Table
Definitions on Source and Replica”.

This filtering works on the replica side, that is, the columns are copied to the replica before they are filtered
out. There are at least two cases where it is not desirable to copy the columns to the replica:

1.

If the data is confidential, so the replica server should not have access to it.

2.

If the source has many replicas, filtering before sending to the replicas may reduce network traffic.

Source column filtering can be achieved using the BLACKHOLE engine. This is carried out in a way similar
to how source table filtering is achieved - by using the BLACKHOLE engine and the --replicate-do-
table or --replicate-ignore-table option.

The setup for the source is:

CREATE TABLE t1 (public_col_1, ..., public_col_N,
                 secret_col_1, ..., secret_col_M) ENGINE=MyISAM;

The setup for the trusted replica is:

CREATE TABLE t1 (public_col_1, ..., public_col_N) ENGINE=BLACKHOLE;

The setup for the untrusted replica is:

CREATE TABLE t1 (public_col_1, ..., public_col_N) ENGINE=MyISAM;

15.7 The MERGE Storage Engine

The MERGE storage engine, also known as the MRG_MyISAM engine, is a collection of identical MyISAM
tables that can be used as one. “Identical” means that all tables have identical column data types and
index information. You cannot merge MyISAM tables in which the columns are listed in a different order,
do not have exactly the same data types in corresponding columns, or have the indexes in different order.
However, any or all of the MyISAM tables can be compressed with myisampack. See Section 4.6.5,
“myisampack — Generate Compressed, Read-Only MyISAM Tables”. Differences between tables such as
these do not matter:

2938

The MERGE Storage Engine

• Names of corresponding columns and indexes can differ.

• Comments for tables, columns, and indexes can differ.

• Table options such as AVG_ROW_LENGTH, MAX_ROWS, or PACK_KEYS can differ.

An alternative to a MERGE table is a partitioned table, which stores partitions of a single table in separate
files. Partitioning enables some operations to be performed more efficiently and is not limited to the
MyISAM storage engine. For more information, see Chapter 22, Partitioning.

When you create a MERGE table, MySQL creates two files on disk. The files have names that begin with
the table name and have an extension to indicate the file type. An .frm file stores the table format, and an
.MRG file contains the names of the underlying MyISAM tables that should be used as one. The tables do
not have to be in the same database as the MERGE table.

You can use SELECT, DELETE, UPDATE, and INSERT on MERGE tables. You must have SELECT, DELETE,
and UPDATE privileges on the MyISAM tables that you map to a MERGE table.

Note

The use of MERGE tables entails the following security issue: If a user has access to
MyISAM table t, that user can create a MERGE table m that accesses t. However,
if the user's privileges on t are subsequently revoked, the user can continue to
access t by doing so through m.

Use of DROP TABLE with a MERGE table drops only the MERGE specification. The underlying tables are not
affected.

To create a MERGE table, you must specify a UNION=(list-of-tables) option that indicates which
MyISAM tables to use. You can optionally specify an INSERT_METHOD option to control how inserts into
the MERGE table take place. Use a value of FIRST or LAST to cause inserts to be made in the first or last
underlying table, respectively. If you specify no INSERT_METHOD option or if you specify it with a value of
NO, inserts into the MERGE table are not permitted and attempts to do so result in an error.

The following example shows how to create a MERGE table:

mysql> CREATE TABLE t1 (
    ->    a INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ->    message CHAR(20)) ENGINE=MyISAM;
mysql> CREATE TABLE t2 (
    ->    a INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ->    message CHAR(20)) ENGINE=MyISAM;
mysql> INSERT INTO t1 (message) VALUES ('Testing'),('table'),('t1');
mysql> INSERT INTO t2 (message) VALUES ('Testing'),('table'),('t2');
mysql> CREATE TABLE total (
    ->    a INT NOT NULL AUTO_INCREMENT,
    ->    message CHAR(20), INDEX(a))
    ->    ENGINE=MERGE UNION=(t1,t2) INSERT_METHOD=LAST;

Column a is indexed as a PRIMARY KEY in the underlying MyISAM tables, but not in the MERGE table.
There it is indexed but not as a PRIMARY KEY because a MERGE table cannot enforce uniqueness over
the set of underlying tables. (Similarly, a column with a UNIQUE index in the underlying tables should be
indexed in the MERGE table but not as a UNIQUE index.)

After creating the MERGE table, you can use it to issue queries that operate on the group of tables as a
whole:

mysql> SELECT * FROM total;

2939

The MERGE Storage Engine

+---+---------+
| a | message |
+---+---------+
| 1 | Testing |
| 2 | table   |
| 3 | t1      |
| 1 | Testing |
| 2 | table   |
| 3 | t2      |
+---+---------+

To remap a MERGE table to a different collection of MyISAM tables, you can use one of the following
methods:

• DROP the MERGE table and re-create it.

• Use ALTER TABLE tbl_name UNION=(...) to change the list of underlying tables.

It is also possible to use ALTER TABLE ... UNION=() (that is, with an empty UNION clause) to
remove all of the underlying tables. However, in this case, the table is effectively empty and inserts fail
because there is no underlying table to take new rows. Such a table might be useful as a template for
creating new MERGE tables with CREATE TABLE ... LIKE.

The underlying table definitions and indexes must conform closely to the definition of the MERGE table.
Conformance is checked when a table that is part of a MERGE table is opened, not when the MERGE table
is created. If any table fails the conformance checks, the operation that triggered the opening of the table
fails. This means that changes to the definitions of tables within a MERGE may cause a failure when the
MERGE table is accessed. The conformance checks applied to each table are:

• The underlying table and the MERGE table must have the same number of columns.

• The column order in the underlying table and the MERGE table must match.

• Additionally, the specification for each corresponding column in the parent MERGE table and the

underlying tables are compared and must satisfy these checks:

• The column type in the underlying table and the MERGE table must be equal.

• The column length in the underlying table and the MERGE table must be equal.

• The column of the underlying table and the MERGE table can be NULL.

• The underlying table must have at least as many indexes as the MERGE table. The underlying table may

have more indexes than the MERGE table, but cannot have fewer.

Note

A known issue exists where indexes on the same columns must be in identical
order, in both the MERGE table and the underlying MyISAM table. See Bug
#33653.

Each index must satisfy these checks:

• The index type of the underlying table and the MERGE table must be the same.

• The number of index parts (that is, multiple columns within a compound index) in the index definition

for the underlying table and the MERGE table must be the same.

• For each index part:

2940

Additional Resources

• Index part lengths must be equal.

• Index part types must be equal.

• Index part languages must be equal.

• Check whether index parts can be NULL.

If a MERGE table cannot be opened or used because of a problem with an underlying table, CHECK TABLE
displays information about which table caused the problem.

Additional Resources

• A forum dedicated to the MERGE storage engine is available at https://forums.mysql.com/list.php?93.

15.7.1 MERGE Table Advantages and Disadvantages

MERGE tables can help you solve the following problems:

• Easily manage a set of log tables. For example, you can put data from different months into separate

tables, compress some of them with myisampack, and then create a MERGE table to use them as one.

• Obtain more speed. You can split a large read-only table based on some criteria, and then put individual
tables on different disks. A MERGE table structured this way could be much faster than using a single
large table.

• Perform more efficient searches. If you know exactly what you are looking for, you can search in just one
of the underlying tables for some queries and use a MERGE table for others. You can even have many
different MERGE tables that use overlapping sets of tables.

• Perform more efficient repairs. It is easier to repair individual smaller tables that are mapped to a MERGE

table than to repair a single large table.

• Instantly map many tables as one. A MERGE table need not maintain an index of its own because it uses
the indexes of the individual tables. As a result, MERGE table collections are very fast to create or remap.
(You must still specify the index definitions when you create a MERGE table, even though no indexes are
created.)

• If you have a set of tables from which you create a large table on demand, you can instead create a

MERGE table from them on demand. This is much faster and saves a lot of disk space.

• Exceed the file size limit for the operating system. Each MyISAM table is bound by this limit, but a

collection of MyISAM tables is not.

• You can create an alias or synonym for a MyISAM table by defining a MERGE table that maps to that
single table. There should be no really notable performance impact from doing this (only a couple of
indirect calls and memcpy() calls for each read).

The disadvantages of MERGE tables are:

• You can use only identical MyISAM tables for a MERGE table.

• Some MyISAM features are unavailable in MERGE tables. For example, you cannot create FULLTEXT

indexes on MERGE tables. (You can create FULLTEXT indexes on the underlying MyISAM tables, but you
cannot search the MERGE table with a full-text search.)

2941

MERGE Table Problems

• If the MERGE table is nontemporary, all underlying MyISAM tables must be nontemporary. If the MERGE

table is temporary, the MyISAM tables can be any mix of temporary and nontemporary.

•  MERGE tables use more file descriptors than MyISAM tables. If 10 clients are using a MERGE table that

maps to 10 tables, the server uses (10 × 10) + 10 file descriptors. (10 data file descriptors for each of the
10 clients, and 10 index file descriptors shared among the clients.)

• Index reads are slower. When you read an index, the MERGE storage engine needs to issue a read on all
underlying tables to check which one most closely matches a given index value. To read the next index
value, the MERGE storage engine needs to search the read buffers to find the next value. Only when one
index buffer is used up does the storage engine need to read the next index block. This makes MERGE
indexes much slower on eq_ref searches, but not much slower on ref searches. For more information
about eq_ref and ref, see Section 13.8.2, “EXPLAIN Statement”.

15.7.2 MERGE Table Problems

The following are known problems with MERGE tables:

• MERGE child tables are locked through the parent table. If the parent is a temporary table, it is not locked,

and thus the child tables are also not locked; this means that parallel use of the underlying MyISAM
tables corrupts them.

• If you use ALTER TABLE to change a MERGE table to another storage engine, the mapping to the

underlying tables is lost. Instead, the rows from the underlying MyISAM tables are copied into the altered
table, which then uses the specified storage engine.

• The INSERT_METHOD table option for a MERGE table indicates which underlying MyISAM table to use for
inserts into the MERGE table. However, use of the AUTO_INCREMENT table option for that MyISAM table
has no effect for inserts into the MERGE table until at least one row has been inserted directly into the
MyISAM table.

• A MERGE table cannot maintain uniqueness constraints over the entire table. When you perform an
INSERT, the data goes into the first or last MyISAM table (as determined by the INSERT_METHOD
option). MySQL ensures that unique key values remain unique within that MyISAM table, but not over all
the underlying tables in the collection.

• Because the MERGE engine cannot enforce uniqueness over the set of underlying tables, REPLACE does

not work as expected. The two key facts are:

• REPLACE can detect unique key violations only in the underlying table to which it is going to write

(which is determined by the INSERT_METHOD option). This differs from violations in the MERGE table
itself.

• If REPLACE detects a unique key violation, it changes only the corresponding row in the underlying
table it is writing to; that is, the first or last table, as determined by the INSERT_METHOD option.

Similar considerations apply for INSERT ... ON DUPLICATE KEY UPDATE.

• MERGE tables do not support partitioning. That is, you cannot partition a MERGE table, nor can any of a

MERGE table's underlying MyISAM tables be partitioned.

• You should not use ANALYZE TABLE, REPAIR TABLE, OPTIMIZE TABLE, ALTER TABLE, DROP

TABLE, DELETE without a WHERE clause, or TRUNCATE TABLE on any of the tables that are mapped
into an open MERGE table. If you do so, the MERGE table may still refer to the original table and yield
unexpected results. To work around this problem, ensure that no MERGE tables remain open by issuing a
FLUSH TABLES statement prior to performing any of the named operations.

2942

The FEDERATED Storage Engine

The unexpected results include the possibility that the operation on the MERGE table reports table
corruption. If this occurs after one of the named operations on the underlying MyISAM tables, the
corruption message is spurious. To deal with this, issue a FLUSH TABLES statement after modifying the
MyISAM tables.

• DROP TABLE on a table that is in use by a MERGE table does not work on Windows because the MERGE

storage engine's table mapping is hidden from the upper layer of MySQL. Windows does not permit open
files to be deleted, so you first must flush all MERGE tables (with FLUSH TABLES) or drop the MERGE
table before dropping the table.

• The definition of the MyISAM tables and the MERGE table are checked when the tables are accessed (for
example, as part of a SELECT or INSERT statement). The checks ensure that the definitions of the tables
and the parent MERGE table definition match by comparing column order, types, sizes and associated
indexes. If there is a difference between the tables, an error is returned and the statement fails. Because
these checks take place when the tables are opened, any changes to the definition of a single table,
including column changes, column ordering, and engine alterations causes the statement to fail.

• The order of indexes in the MERGE table and its underlying tables should be the same. If you use ALTER
TABLE to add a UNIQUE index to a table used in a MERGE table, and then use ALTER TABLE to add a
nonunique index on the MERGE table, the index ordering is different for the tables if there was already a
nonunique index in the underlying table. (This happens because ALTER TABLE puts UNIQUE indexes
before nonunique indexes to facilitate rapid detection of duplicate keys.) Consequently, queries on tables
with such indexes may return unexpected results.

• If you encounter an error message similar to ERROR 1017 (HY000): Can't find file:

'tbl_name.MRG' (errno: 2), it generally indicates that some of the underlying tables do not use
the MyISAM storage engine. Confirm that all of these tables are MyISAM.

• The maximum number of rows in a MERGE table is 264 (~1.844E+19; the same as for a MyISAM table). It
is not possible to merge multiple MyISAM tables into a single MERGE table that would have more than this
number of rows.

• Use of underlying MyISAM tables of differing row formats with a parent MERGE table is currently known to

fail. See Bug #32364.

• You cannot change the union list of a nontemporary MERGE table when LOCK TABLES is in effect. The

following does not work:

CREATE TABLE m1 ... ENGINE=MRG_MYISAM ...;
LOCK TABLES t1 WRITE, t2 WRITE, m1 WRITE;
ALTER TABLE m1 ... UNION=(t1,t2) ...;

However, you can do this with a temporary MERGE table.

• You cannot create a MERGE table with CREATE ... SELECT, neither as a temporary MERGE table, nor

as a nontemporary MERGE table. For example:

CREATE TABLE m1 ... ENGINE=MRG_MYISAM ... SELECT ...;

Attempts to do this result in an error: tbl_name is not BASE TABLE.

• In some cases, differing PACK_KEYS table option values among the MERGE and underlying tables cause
unexpected results if the underlying tables contain CHAR or BINARY columns. As a workaround, use
ALTER TABLE to ensure that all involved tables have the same PACK_KEYS value. (Bug #50646)

15.8 The FEDERATED Storage Engine

2943

FEDERATED Storage Engine Overview

The FEDERATED storage engine lets you access data from a remote MySQL database without using
replication or cluster technology. Querying a local FEDERATED table automatically pulls the data from the
remote (federated) tables. No data is stored on the local tables.

To include the FEDERATED storage engine if you build MySQL from source, invoke CMake with the -
DWITH_FEDERATED_STORAGE_ENGINE option.

The FEDERATED storage engine is not enabled by default in the running server; to enable FEDERATED, you
must start the MySQL server binary using the --federated option.

To examine the source for the FEDERATED engine, look in the storage/federated directory of a
MySQL source distribution.

15.8.1 FEDERATED Storage Engine Overview

When you create a table using one of the standard storage engines (such as MyISAM, CSV or InnoDB),
the table consists of the table definition and the associated data. When you create a FEDERATED table, the
table definition is the same, but the physical storage of the data is handled on a remote server.

A FEDERATED table consists of two elements:

• A remote server with a database table, which in turn consists of the table definition (stored in the .frm
file) and the associated table. The table type of the remote table may be any type supported by the
remote mysqld server, including MyISAM or InnoDB.

• A local server with a database table, where the table definition matches that of the corresponding table

on the remote server. The table definition is stored within the .frm file. However, there is no data file on
the local server. Instead, the table definition includes a connection string that points to the remote table.

When executing queries and statements on a FEDERATED table on the local server, the operations that
would normally insert, update or delete information from a local data file are instead sent to the remote
server for execution, where they update the data file on the remote server or return matching rows from the
remote server.

The basic structure of a FEDERATED table setup is shown in Figure 15.2, “FEDERATED Table Structure”.

Figure 15.2 FEDERATED Table Structure

2944

How to Create FEDERATED Tables

When a client issues an SQL statement that refers to a FEDERATED table, the flow of information between
the local server (where the SQL statement is executed) and the remote server (where the data is physically
stored) is as follows:

1. The storage engine looks through each column that the FEDERATED table has and constructs an

appropriate SQL statement that refers to the remote table.

2. The statement is sent to the remote server using the MySQL client API.

3. The remote server processes the statement and the local server retrieves any result that the statement

produces (an affected-rows count or a result set).

4.

If the statement produces a result set, each column is converted to internal storage engine format that
the FEDERATED engine expects and can use to display the result to the client that issued the original
statement.

The local server communicates with the remote server using MySQL client C API functions. It invokes
mysql_real_query() to send the statement. To read a result set, it uses mysql_store_result()
and fetches rows one at a time using mysql_fetch_row().

15.8.2 How to Create FEDERATED Tables

To create a FEDERATED table you should follow these steps:

1. Create the table on the remote server. Alternatively, make a note of the table definition of an existing

table, perhaps using the SHOW CREATE TABLE statement.

2. Create the table on the local server with an identical table definition, but adding the connection

information that links the local table to the remote table.

For example, you could create the following table on the remote server:

CREATE TABLE test_table (
    id     INT(20) NOT NULL AUTO_INCREMENT,
    name   VARCHAR(32) NOT NULL DEFAULT '',
    other  INT(20) NOT NULL DEFAULT '0',
    PRIMARY KEY  (id),
    INDEX name (name),
    INDEX other_key (other)
)
ENGINE=MyISAM
DEFAULT CHARSET=latin1;

For creating the local table to be federated to the remote table, there are two options available. You can
either create the local table and specify the connection string (containing the server name, login, password)
to be used to connect to the remote table using the CONNECTION, or you can use an existing connection
that you have previously created using the CREATE SERVER statement.

Important

When you create the local table it must have an identical field definition to the
remote table.

Note

You can improve the performance of a FEDERATED table by adding indexes to the
table on the host. The optimization occurs because the query sent to the remote
server includes the contents of the WHERE clause, and is sent to the remote server

2945

How to Create FEDERATED Tables

and subsequently executed locally. This reduces the network traffic that would
otherwise request the entire table from the server for local processing.

15.8.2.1 Creating a FEDERATED Table Using CONNECTION

To use the first method, you must specify the CONNECTION string after the engine type in a CREATE
TABLE statement. For example:

CREATE TABLE federated_table (
    id     INT(20) NOT NULL AUTO_INCREMENT,
    name   VARCHAR(32) NOT NULL DEFAULT '',
    other  INT(20) NOT NULL DEFAULT '0',
    PRIMARY KEY  (id),
    INDEX name (name),
    INDEX other_key (other)
)
ENGINE=FEDERATED
DEFAULT CHARSET=latin1
CONNECTION='mysql://fed_user@remote_host:9306/federated/test_table';

Note

CONNECTION replaces the COMMENT used in some previous versions of MySQL.

The CONNECTION string contains the information required to connect to the remote server containing
the table used for physical storage of the data. The connection string specifies the server name, login
credentials, port number and database/table information. In the example, the remote table is on the server
remote_host, using port 9306. The name and port number should match the host name (or IP address)
and port number of the remote MySQL server instance you want to use as your remote table.

The format of the connection string is as follows:

scheme://user_name[:password]@host_name[:port_num]/db_name/tbl_name

Where:

• scheme: A recognized connection protocol. Only mysql is supported as the scheme value at this point.

• user_name: The user name for the connection. This user must have been created on the remote server,
and must have suitable privileges to perform the required actions (SELECT, INSERT, UPDATE, and so
forth) on the remote table.

• password: (Optional) The corresponding password for user_name.

• host_name: The host name or IP address of the remote server.

• port_num: (Optional) The port number for the remote server. The default is 3306.

• db_name: The name of the database holding the remote table.

• tbl_name: The name of the remote table. The name of the local and the remote table do not have to

match.

Sample connection strings:

CONNECTION='mysql://username:password@hostname:port/database/tablename'
CONNECTION='mysql://username@hostname/database/tablename'
CONNECTION='mysql://username:password@hostname/database/tablename'

2946

How to Create FEDERATED Tables

15.8.2.2 Creating a FEDERATED Table Using CREATE SERVER

If you are creating a number of FEDERATED tables on the same server, or if you want to simplify the
process of creating FEDERATED tables, you can use the CREATE SERVER statement to define the server
connection parameters, just as you would with the CONNECTION string.

The format of the CREATE SERVER statement is:

CREATE SERVER
server_name
FOREIGN DATA WRAPPER wrapper_name
OPTIONS (option [, option] ...)

The server_name is used in the connection string when creating a new FEDERATED table.

For example, to create a server connection identical to the CONNECTION string:

CONNECTION='mysql://fed_user@remote_host:9306/federated/test_table';

You would use the following statement:

CREATE SERVER fedlink
FOREIGN DATA WRAPPER mysql
OPTIONS (USER 'fed_user', HOST 'remote_host', PORT 9306, DATABASE 'federated');

To create a FEDERATED table that uses this connection, you still use the CONNECTION keyword, but
specify the name you used in the CREATE SERVER statement.

CREATE TABLE test_table (
    id     INT(20) NOT NULL AUTO_INCREMENT,
    name   VARCHAR(32) NOT NULL DEFAULT '',
    other  INT(20) NOT NULL DEFAULT '0',
    PRIMARY KEY  (id),
    INDEX name (name),
    INDEX other_key (other)
)
ENGINE=FEDERATED
DEFAULT CHARSET=latin1
CONNECTION='fedlink/test_table';

The connection name in this example contains the name of the connection (fedlink) and the name of
the table (test_table) to link to, separated by a slash. If you specify only the connection name without a
table name, the table name of the local table is used instead.

For more information on CREATE SERVER, see Section 13.1.17, “CREATE SERVER Statement”.

The CREATE SERVER statement accepts the same arguments as the CONNECTION string. The CREATE
SERVER statement updates the rows in the mysql.servers table. See the following table for information
on the correspondence between parameters in a connection string, options in the CREATE SERVER
statement, and the columns in the mysql.servers table. For reference, the format of the CONNECTION
string is as follows:

scheme://user_name[:password]@host_name[:port_num]/db_name/tbl_name

Description

CONNECTION string

CREATE SERVER option mysql.servers

Connection scheme

scheme

wrapper_name

Remote user

user_name

USER

column

Wrapper

Username

2947

FEDERATED Storage Engine Notes and Tips

Description

CONNECTION string

CREATE SERVER option mysql.servers

Remote password

password

PASSWORD

Remote host

Remote port

Remote database

host_name

port_num

db_name

HOST

PORT

DATABASE

15.8.3 FEDERATED Storage Engine Notes and Tips

column

Password

Host

Port

Db

You should be aware of the following points when using the FEDERATED storage engine:

• FEDERATED tables may be replicated to other replicas, but you must ensure that the replica servers are
able to use the user/password combination that is defined in the CONNECTION string (or the row in the
mysql.servers table) to connect to the remote server.

The following items indicate features that the FEDERATED storage engine does and does not support:

• The remote server must be a MySQL server.

• The remote table that a FEDERATED table points to must exist before you try to access the table through

the FEDERATED table.

• It is possible for one FEDERATED table to point to another, but you must be careful not to create a loop.

• A FEDERATED table does not support indexes in the usual sense; because access to the table data is

handled remotely, it is actually the remote table that makes use of indexes. This means that, for a query
that cannot use any indexes and so requires a full table scan, the server fetches all rows from the remote
table and filters them locally. This occurs regardless of any WHERE or LIMIT used with this SELECT
statement; these clauses are applied locally to the returned rows.

Queries that fail to use indexes can thus cause poor performance and network overload. In addition,
since returned rows must be stored in memory, such a query can also lead to the local server swapping,
or even hanging.

• Care should be taken when creating a FEDERATED table since the index definition from an equivalent
MyISAM or other table may not be supported. For example, creating a FEDERATED table with an index
prefix fails for VARCHAR, TEXT or BLOB columns. The following definition in MyISAM is valid:

CREATE TABLE `T1`(`A` VARCHAR(100),UNIQUE KEY(`A`(30))) ENGINE=MYISAM;

The key prefix in this example is incompatible with the FEDERATED engine, and the equivalent statement
fails:

CREATE TABLE `T1`(`A` VARCHAR(100),UNIQUE KEY(`A`(30))) ENGINE=FEDERATED
  CONNECTION='MYSQL://127.0.0.1:3306/TEST/T1';

If possible, you should try to separate the column and index definition when creating tables on both the
remote server and the local server to avoid these index issues.

• Internally, the implementation uses SELECT, INSERT, UPDATE, and DELETE, but not HANDLER.

• The FEDERATED storage engine supports SELECT, INSERT, UPDATE, DELETE, TRUNCATE TABLE, and
indexes. It does not support ALTER TABLE, or any Data Definition Language statements that directly
affect the structure of the table, other than DROP TABLE. The current implementation does not use
prepared statements.

2948

FEDERATED Storage Engine Resources

• FEDERATED accepts INSERT ... ON DUPLICATE KEY UPDATE statements, but if a duplicate-key

violation occurs, the statement fails with an error.

• Transactions are not supported.

• FEDERATED performs bulk-insert handling such that multiple rows are sent to the remote table in a
batch, which improves performance. Also, if the remote table is transactional, it enables the remote
storage engine to perform statement rollback properly should an error occur. This capability has the
following limitations:

• The size of the insert cannot exceed the maximum packet size between servers. If the insert exceeds

this size, it is broken into multiple packets and the rollback problem can occur.

• Bulk-insert handling does not occur for INSERT ... ON DUPLICATE KEY UPDATE.

• There is no way for the FEDERATED engine to know if the remote table has changed. The reason for

this is that this table must work like a data file that would never be written to by anything other than the
database system. The integrity of the data in the local table could be breached if there was any change
to the remote database.

• When using a CONNECTION string, you cannot use an '@' character in the password. You can get round

this limitation by using the CREATE SERVER statement to create a server connection.

• The insert_id and timestamp options are not propagated to the data provider.

• Any DROP TABLE statement issued against a FEDERATED table drops only the local table, not the

remote table.

• FEDERATED tables do not work with the query cache.

• User-defined partitioning is not supported for FEDERATED tables.

15.8.4 FEDERATED Storage Engine Resources

The following additional resources are available for the FEDERATED storage engine:

• A forum dedicated to the FEDERATED storage engine is available at https://forums.mysql.com/list.php?

105.

15.9 The EXAMPLE Storage Engine

The EXAMPLE storage engine is a stub engine that does nothing. Its purpose is to serve as an example in
the MySQL source code that illustrates how to begin writing new storage engines. As such, it is primarily of
interest to developers.

To enable the EXAMPLE storage engine if you build MySQL from source, invoke CMake with the -
DWITH_EXAMPLE_STORAGE_ENGINE option.

To examine the source for the EXAMPLE engine, look in the storage/example directory of a MySQL
source distribution.

When you create an EXAMPLE table, the server creates a table format file in the database directory. The
file begins with the table name and has an .frm extension. No other files are created. No data can be
stored into the table. Retrievals return an empty result.

mysql> CREATE TABLE test (i INT) ENGINE = EXAMPLE;
Query OK, 0 rows affected (0.78 sec)

2949

Other Storage Engines

mysql> INSERT INTO test VALUES(1),(2),(3);
ERROR 1031 (HY000): Table storage engine for 'test' doesn't »
                    have this option

mysql> SELECT * FROM test;
Empty set (0.31 sec)

The EXAMPLE storage engine does not support indexing.

15.10 Other Storage Engines

Other storage engines may be available from third parties and community members that have used the
Custom Storage Engine interface.

Third party engines are not supported by MySQL. For further information, documentation, installation
guides, bug reporting or for any help or assistance with these engines, please contact the developer of the
engine directly.

For more information on developing a customer storage engine that can be used with the Pluggable
Storage Engine Architecture, see MySQL Internals: Writing a Custom Storage Engine.

15.11 Overview of MySQL Storage Engine Architecture

The MySQL pluggable storage engine architecture enables a database professional to select a specialized
storage engine for a particular application need while being completely shielded from the need to manage
any specific application coding requirements. The MySQL server architecture isolates the application
programmer and DBA from all of the low-level implementation details at the storage level, providing a
consistent and easy application model and API. Thus, although there are different capabilities across
different storage engines, the application is shielded from these differences.

The pluggable storage engine architecture provides a standard set of management and support services
that are common among all underlying storage engines. The storage engines themselves are the
components of the database server that actually perform actions on the underlying data that is maintained
at the physical server level.

This efficient and modular architecture provides huge benefits for those wishing to specifically target
a particular application need—such as data warehousing, transaction processing, or high availability
situations—while enjoying the advantage of utilizing a set of interfaces and services that are independent
of any one storage engine.

The application programmer and DBA interact with the MySQL database through Connector APIs and
service layers that are above the storage engines. If application changes bring about requirements that
demand the underlying storage engine change, or that one or more storage engines be added to support
new needs, no significant coding or process changes are required to make things work. The MySQL server
architecture shields the application from the underlying complexity of the storage engine by presenting a
consistent and easy-to-use API that applies across storage engines.

15.11.1 Pluggable Storage Engine Architecture

MySQL Server uses a pluggable storage engine architecture that enables storage engines to be loaded
into and unloaded from a running MySQL server.

Plugging in a Storage Engine

Before a storage engine can be used, the storage engine plugin shared library must be loaded into MySQL
using the INSTALL PLUGIN statement. For example, if the EXAMPLE engine plugin is named example
and the shared library is named ha_example.so, you load it with the following statement:

2950

The Common Database Server Layer

INSTALL PLUGIN example SONAME 'ha_example.so';

To install a pluggable storage engine, the plugin file must be located in the MySQL plugin directory, and
the user issuing the INSTALL PLUGIN statement must have INSERT privilege for the mysql.plugin
table.

The shared library must be located in the MySQL server plugin directory, the location of which is given by
the plugin_dir system variable.

Unplugging a Storage Engine

To unplug a storage engine, use the UNINSTALL PLUGIN statement:

UNINSTALL PLUGIN example;

If you unplug a storage engine that is needed by existing tables, those tables become inaccessible, but are
still present on disk (where applicable). Ensure that there are no tables using a storage engine before you
unplug the storage engine.

15.11.2 The Common Database Server Layer

A MySQL pluggable storage engine is the component in the MySQL database server that is responsible for
performing the actual data I/O operations for a database as well as enabling and enforcing certain feature
sets that target a specific application need. A major benefit of using specific storage engines is that you
are only delivered the features needed for a particular application, and therefore you have less system
overhead in the database, with the end result being more efficient and higher database performance. This
is one of the reasons that MySQL has always been known to have such high performance, matching or
beating proprietary monolithic databases in industry standard benchmarks.

From a technical perspective, what are some of the unique supporting infrastructure components that are
in a storage engine? Some of the key feature differentiations include:

• Concurrency: Some applications have more granular lock requirements (such as row-level locks)

than others. Choosing the right locking strategy can reduce overhead and therefore improve overall
performance. This area also includes support for capabilities such as multi-version concurrency control
or “snapshot” read.

• Transaction Support: Not every application needs transactions, but for those that do, there are very well

defined requirements such as ACID compliance and more.

• Referential Integrity: The need to have the server enforce relational database referential integrity through

DDL defined foreign keys.

• Physical Storage: This involves everything from the overall page size for tables and indexes as well as

the format used for storing data to physical disk.

• Index Support: Different application scenarios tend to benefit from different index strategies. Each

storage engine generally has its own indexing methods, although some (such as B-tree indexes) are
common to nearly all engines.

• Memory Caches: Different applications respond better to some memory caching strategies than others,
so although some memory caches are common to all storage engines (such as those used for user
connections or MySQL's high-speed Query Cache), others are uniquely defined only when a particular
storage engine is put in play.

• Performance Aids: This includes multiple I/O threads for parallel operations, thread concurrency,

database checkpointing, bulk insert handling, and more.

2951

The Common Database Server Layer

• Miscellaneous Target Features: This may include support for geospatial operations, security restrictions

for certain data manipulation operations, and other similar features.

Each set of the pluggable storage engine infrastructure components are designed to offer a selective set
of benefits for a particular application. Conversely, avoiding a set of component features helps reduce
unnecessary overhead. It stands to reason that understanding a particular application's set of requirements
and selecting the proper MySQL storage engine can have a dramatic impact on overall system efficiency
and performance.

2952

