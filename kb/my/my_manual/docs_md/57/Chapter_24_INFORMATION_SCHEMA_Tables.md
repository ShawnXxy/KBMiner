Introduction

24.4.10 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table .............. 4169
24.4.11 The INFORMATION_SCHEMA INNODB_FT_DELETED Table ................................... 4170
24.4.12 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table ........................... 4171
24.4.13 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table ............................ 4173
24.4.14 The INFORMATION_SCHEMA INNODB_LOCKS Table ............................................. 4174
24.4.15 The INFORMATION_SCHEMA INNODB_LOCK_WAITS Table ................................... 4176
24.4.16 The INFORMATION_SCHEMA INNODB_METRICS Table ......................................... 4177
24.4.17 The INFORMATION_SCHEMA INNODB_SYS_COLUMNS Table ............................... 4179
24.4.18 The INFORMATION_SCHEMA INNODB_SYS_DATAFILES Table .............................. 4180
24.4.19 The INFORMATION_SCHEMA INNODB_SYS_FIELDS Table .................................... 4181
24.4.20 The INFORMATION_SCHEMA INNODB_SYS_FOREIGN Table ................................. 4182
24.4.21 The INFORMATION_SCHEMA INNODB_SYS_FOREIGN_COLS Table ...................... 4183
24.4.22 The INFORMATION_SCHEMA INNODB_SYS_INDEXES Table ................................. 4183
24.4.23 The INFORMATION_SCHEMA INNODB_SYS_TABLES Table ................................... 4185
24.4.24 The INFORMATION_SCHEMA INNODB_SYS_TABLESPACES Table ........................ 4186
24.4.25 The INFORMATION_SCHEMA INNODB_SYS_TABLESTATS View ............................ 4188
24.4.26 The INFORMATION_SCHEMA INNODB_SYS_VIRTUAL Table .................................. 4189
24.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table ......................... 4190
24.4.28 The INFORMATION_SCHEMA INNODB_TRX Table .................................................. 4192
24.5 INFORMATION_SCHEMA Thread Pool Tables ...................................................................... 4194
24.5.1 INFORMATION_SCHEMA Thread Pool Table Reference ............................................. 4195
24.5.2 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table ........................... 4195
24.5.3 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table ........................... 4197
24.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table ......................................... 4199
24.6 INFORMATION_SCHEMA Connection Control Tables ............................................................ 4199
24.6.1 INFORMATION_SCHEMA Connection Control Table Reference ................................... 4199
24.6.2 The INFORMATION_SCHEMA
CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table ............................................. 4200
24.7 INFORMATION_SCHEMA MySQL Enterprise Firewall Tables ................................................. 4200
24.7.1 INFORMATION_SCHEMA Firewall Table Reference .................................................... 4200
24.7.2 The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table .............................. 4201
24.7.3 The INFORMATION_SCHEMA MYSQL_FIREWALL_WHITELIST Table ....................... 4201
24.8 Extensions to SHOW Statements .......................................................................................... 4201

INFORMATION_SCHEMA provides access to database metadata, information about the MySQL server such
as the name of a database or table, the data type of a column, or access privileges. Other terms that are
sometimes used for this information are data dictionary and system catalog.

24.1 Introduction

INFORMATION_SCHEMA provides access to database metadata, information about the MySQL server such
as the name of a database or table, the data type of a column, or access privileges. Other terms that are
sometimes used for this information are data dictionary and system catalog.

• INFORMATION_SCHEMA Usage Notes

• Character Set Considerations

• INFORMATION_SCHEMA as Alternative to SHOW Statements

• INFORMATION_SCHEMA and Privileges

• Performance Considerations

• Standards Considerations

4098

Conventions in the INFORMATION_SCHEMA Reference Sections

Conventions in the INFORMATION_SCHEMA Reference Sections

The following sections describe each of the tables and columns in INFORMATION_SCHEMA. For each
column, there are three pieces of information:

• “INFORMATION_SCHEMA Name” indicates the name for the column in the INFORMATION_SCHEMA table.

This corresponds to the standard SQL name unless the “Remarks” field says “MySQL extension.”

• “SHOW Name” indicates the equivalent field name in the closest SHOW statement, if there is one.

• “Remarks” provides additional information where applicable. If this field is NULL, it means that the value
of the column is always NULL. If this field says “MySQL extension,” the column is a MySQL extension to
standard SQL.

Many sections indicate what SHOW statement is equivalent to a SELECT that retrieves information from
INFORMATION_SCHEMA. For SHOW statements that display information for the default database if you omit
a FROM db_name clause, you can often select information for the default database by adding an AND
TABLE_SCHEMA = SCHEMA() condition to the WHERE clause of a query that retrieves information from an
INFORMATION_SCHEMA table.

Related Information

These sections discuss additional INFORMATION_SCHEMA-related topics:

• information about INFORMATION_SCHEMA tables specific to the InnoDB storage engine: Section 24.4,

“INFORMATION_SCHEMA InnoDB Tables”

• information about INFORMATION_SCHEMA tables specific to the thread pool plugin: Section 24.5,

“INFORMATION_SCHEMA Thread Pool Tables”

• information about INFORMATION_SCHEMA tables specific to the CONNECTION_CONTROL plugin:

Section 24.6, “INFORMATION_SCHEMA Connection Control Tables”

• Answers to questions that are often asked concerning the INFORMATION_SCHEMA database:

Section A.7, “MySQL 5.7 FAQ: INFORMATION_SCHEMA”

• INFORMATION_SCHEMA queries and the optimizer: Section 8.2.3, “Optimizing

INFORMATION_SCHEMA Queries”

• The effect of collation on INFORMATION_SCHEMA comparisons: Section 10.8.7, “Using Collation in

INFORMATION_SCHEMA Searches”

24.2 INFORMATION_SCHEMA Table Reference

The following table summarizes all available INFORMATION_SCHEMA tables. For greater detail, see the
individual table descriptions.

Table 24.1 INFORMATION_SCHEMA Tables

Table Name

Description

Introduced

Deprecated

CHARACTER_SETS

Available character sets

COLLATION_CHARACTER_SET_APPLICABILITY
Character set applicable
to each collation

COLLATIONS

Collations for each
character set

4101

The INFORMATION_SCHEMA CHARACTER_SETS Table

Table Name

SCHEMA_PRIVILEGES

SCHEMATA

SESSION_STATUS

SESSION_VARIABLES

STATISTICS

TABLE_CONSTRAINTS

TABLE_PRIVILEGES

TABLES

TABLESPACES

TRIGGERS

USER_PRIVILEGES

VIEWS

Description

Privileges defined on schemas

Schema information

Status variables for current session

System variables for current session

Table index statistics

Which tables have constraints

Privileges defined on tables

Table information

Tablespace information

Trigger information

Privileges defined globally per user

View information

24.3.2 The INFORMATION_SCHEMA CHARACTER_SETS Table

The CHARACTER_SETS table provides information about available character sets.

The CHARACTER_SETS table has these columns:

• CHARACTER_SET_NAME

The character set name.

• DEFAULT_COLLATE_NAME

The default collation for the character set.

• DESCRIPTION

A description of the character set.

• MAXLEN

The maximum number of bytes required to store one character.

Notes

Character set information is also available from the SHOW CHARACTER SET statement. See
Section 13.7.5.3, “SHOW CHARACTER SET Statement”. The following statements are equivalent:

SELECT * FROM INFORMATION_SCHEMA.CHARACTER_SETS
  [WHERE CHARACTER_SET_NAME LIKE 'wild']

SHOW CHARACTER SET
  [LIKE 'wild']

24.3.3 The INFORMATION_SCHEMA COLLATIONS Table

The COLLATIONS table provides information about collations for each character set.

The COLLATIONS table has these columns:

4106

The INFORMATION_SCHEMA COLLATION_CHARACTER_SET_APPLICABILITY Table

• COLLATION_NAME

The collation name.

• CHARACTER_SET_NAME

The name of the character set with which the collation is associated.

• ID

The collation ID.

• IS_DEFAULT

Whether the collation is the default for its character set.

• IS_COMPILED

Whether the character set is compiled into the server.

• SORTLEN

This is related to the amount of memory required to sort strings expressed in the character set.

Notes

Collation information is also available from the SHOW COLLATION statement. See Section 13.7.5.4,
“SHOW COLLATION Statement”. The following statements are equivalent:

SELECT COLLATION_NAME FROM INFORMATION_SCHEMA.COLLATIONS
  [WHERE COLLATION_NAME LIKE 'wild']

SHOW COLLATION
  [LIKE 'wild']

24.3.4 The INFORMATION_SCHEMA
COLLATION_CHARACTER_SET_APPLICABILITY Table

The COLLATION_CHARACTER_SET_APPLICABILITY table indicates what character set is applicable for
what collation.

The COLLATION_CHARACTER_SET_APPLICABILITY table has these columns:

• COLLATION_NAME

The collation name.

• CHARACTER_SET_NAME

The name of the character set with which the collation is associated.

Notes

The COLLATION_CHARACTER_SET_APPLICABILITY columns are equivalent to the first two columns
displayed by the SHOW COLLATION statement.

24.3.5 The INFORMATION_SCHEMA COLUMNS Table

The COLUMNS table provides information about columns in tables.

4107

The INFORMATION_SCHEMA COLUMNS Table

The COLUMNS table has these columns:

• TABLE_CATALOG

The name of the catalog to which the table containing the column belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema (database) to which the table containing the column belongs.

• TABLE_NAME

The name of the table containing the column.

• COLUMN_NAME

The name of the column.

• ORDINAL_POSITION

The position of the column within the table. ORDINAL_POSITION is necessary because you might want
to say ORDER BY ORDINAL_POSITION. Unlike SHOW COLUMNS, SELECT from the COLUMNS table does
not have automatic ordering.

• COLUMN_DEFAULT

The default value for the column. This is NULL if the column has an explicit default of NULL, or if the
column definition includes no DEFAULT clause.

• IS_NULLABLE

The column nullability. The value is YES if NULL values can be stored in the column, NO if not.

• DATA_TYPE

The column data type.

The DATA_TYPE value is the type name only with no other information. The COLUMN_TYPE value
contains the type name and possibly other information such as the precision or length.

• CHARACTER_MAXIMUM_LENGTH

For string columns, the maximum length in characters.

• CHARACTER_OCTET_LENGTH

For string columns, the maximum length in bytes.

• NUMERIC_PRECISION

For numeric columns, the numeric precision.

• NUMERIC_SCALE

For numeric columns, the numeric scale.

• DATETIME_PRECISION

For temporal columns, the fractional seconds precision.

4108

The INFORMATION_SCHEMA COLUMNS Table

• CHARACTER_SET_NAME

For character string columns, the character set name.

• COLLATION_NAME

For character string columns, the collation name.

• COLUMN_TYPE

The column data type.

The DATA_TYPE value is the type name only with no other information. The COLUMN_TYPE value
contains the type name and possibly other information such as the precision or length.

• COLUMN_KEY

Whether the column is indexed:

• If COLUMN_KEY is empty, the column either is not indexed or is indexed only as a secondary column in

a multiple-column, nonunique index.

• If COLUMN_KEY is PRI, the column is a PRIMARY KEY or is one of the columns in a multiple-column

PRIMARY KEY.

• If COLUMN_KEY is UNI, the column is the first column of a UNIQUE index. (A UNIQUE index permits
multiple NULL values, but you can tell whether the column permits NULL by checking the Null
column.)

• If COLUMN_KEY is MUL, the column is the first column of a nonunique index in which multiple

occurrences of a given value are permitted within the column.

If more than one of the COLUMN_KEY values applies to a given column of a table, COLUMN_KEY displays
the one with the highest priority, in the order PRI, UNI, MUL.

A UNIQUE index may be displayed as PRI if it cannot contain NULL values and there is no PRIMARY
KEY in the table. A UNIQUE index may display as MUL if several columns form a composite UNIQUE
index; although the combination of the columns is unique, each column can still hold multiple
occurrences of a given value.

• EXTRA

Any additional information that is available about a given column. The value is nonempty in these cases:

• auto_increment for columns that have the AUTO_INCREMENT attribute.

• on update CURRENT_TIMESTAMP for TIMESTAMP or DATETIME columns that have the ON UPDATE

CURRENT_TIMESTAMP attribute.

• STORED GENERATED or VIRTUAL GENERATED for generated columns.

• PRIVILEGES

The privileges you have for the column.

• COLUMN_COMMENT

Any comment included in the column definition.

4109

The INFORMATION_SCHEMA COLUMN_PRIVILEGES Table

• GENERATION_EXPRESSION

For generated columns, displays the expression used to compute column values. Empty for
nongenerated columns. For information about generated columns, see Section 13.1.18.7, “CREATE
TABLE and Generated Columns”.

Notes

• In SHOW COLUMNS, the Type display includes values from several different COLUMNS columns.

• CHARACTER_OCTET_LENGTH should be the same as CHARACTER_MAXIMUM_LENGTH, except for

multibyte character sets.

• CHARACTER_SET_NAME can be derived from COLLATION_NAME. For example, if you say SHOW FULL

COLUMNS FROM t, and you see in the COLLATION_NAME column a value of latin1_swedish_ci, the
character set is what is before the first underscore: latin1.

Column information is also available from the SHOW COLUMNS statement. See Section 13.7.5.5, “SHOW
COLUMNS Statement”. The following statements are nearly equivalent:

SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE table_name = 'tbl_name'
  [AND table_schema = 'db_name']
  [AND column_name LIKE 'wild']

SHOW COLUMNS
  FROM tbl_name
  [FROM db_name]
  [LIKE 'wild']

24.3.6 The INFORMATION_SCHEMA COLUMN_PRIVILEGES Table

The COLUMN_PRIVILEGES table provides information about column privileges. It takes its values from the
mysql.columns_priv system table.

The COLUMN_PRIVILEGES table has these columns:

• GRANTEE

The name of the account to which the privilege is granted, in 'user_name'@'host_name' format.

• TABLE_CATALOG

The name of the catalog to which the table containing the column belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema (database) to which the table containing the column belongs.

• TABLE_NAME

The name of the table containing the column.

• COLUMN_NAME

The name of the column.

• PRIVILEGE_TYPE

4110

The INFORMATION_SCHEMA ENGINES Table

The privilege granted. The value can be any privilege that can be granted at the column level; see
Section 13.7.1.4, “GRANT Statement”. Each row lists a single privilege, so there is one row per column
privilege held by the grantee.

In the output from SHOW FULL COLUMNS, the privileges are all in one column and in lowercase, for
example, select,insert,update,references. In COLUMN_PRIVILEGES, there is one privilege per
row, in uppercase.

• IS_GRANTABLE

YES if the user has the GRANT OPTION privilege, NO otherwise. The output does not list GRANT OPTION
as a separate row with PRIVILEGE_TYPE='GRANT OPTION'.

Notes

• COLUMN_PRIVILEGES is a nonstandard INFORMATION_SCHEMA table.

The following statements are not equivalent:

SELECT ... FROM INFORMATION_SCHEMA.COLUMN_PRIVILEGES

SHOW GRANTS ...

24.3.7 The INFORMATION_SCHEMA ENGINES Table

The ENGINES table provides information about storage engines. This is particularly useful for checking
whether a storage engine is supported, or to see what the default engine is.

The ENGINES table has these columns:

• ENGINE

The name of the storage engine.

• SUPPORT

The server's level of support for the storage engine, as shown in the following table.

Value

YES

DEFAULT

NO

DISABLED

Meaning

The engine is supported and is active

Like YES, plus this is the default engine

The engine is not supported

The engine is supported but has been disabled

A value of NO means that the server was compiled without support for the engine, so it cannot be
enabled at runtime.

A value of DISABLED occurs either because the server was started with an option that disables the
engine, or because not all options required to enable it were given. In the latter case, the error log should
contain a reason indicating why the option is disabled. See Section 5.4.2, “The Error Log”.

You might also see DISABLED for a storage engine if the server was compiled to support it, but was
started with a --skip-engine_name option. For the NDB storage engine, DISABLED means the server
was compiled with support for NDB Cluster, but was not started with the --ndbcluster option.

All MySQL servers support MyISAM tables. It is not possible to disable MyISAM.

4111

The INFORMATION_SCHEMA EVENTS Table

• COMMENT

A brief description of the storage engine.

• TRANSACTIONS

Whether the storage engine supports transactions.

• XA

Whether the storage engine supports XA transactions.

• SAVEPOINTS

Whether the storage engine supports savepoints.

Notes

• ENGINES is a nonstandard INFORMATION_SCHEMA table.

Storage engine information is also available from the SHOW ENGINES statement. See Section 13.7.5.16,
“SHOW ENGINES Statement”. The following statements are equivalent:

SELECT * FROM INFORMATION_SCHEMA.ENGINES

SHOW ENGINES

24.3.8 The INFORMATION_SCHEMA EVENTS Table

The EVENTS table provides information about Event Manager events, which are discussed in Section 23.4,
“Using the Event Scheduler”.

The EVENTS table has these columns:

• EVENT_CATALOG

The name of the catalog to which the event belongs. This value is always def.

• EVENT_SCHEMA

The name of the schema (database) to which the event belongs.

• EVENT_NAME

The name of the event.

• DEFINER

The account named in the DEFINER clause (often the user who created the event), in
'user_name'@'host_name' format.

• TIME_ZONE

The event time zone, which is the time zone used for scheduling the event and that is in effect within the
event as it executes. The default value is SYSTEM.

• EVENT_BODY

The language used for the statements in the event's DO clause. The value is always SQL.

• EVENT_DEFINITION

4112

The INFORMATION_SCHEMA EVENTS Table

• CREATED

The date and time when the event was created. This is a TIMESTAMP value.

• LAST_ALTERED

The date and time when the event was last modified. This is a TIMESTAMP value. If the event has not
been modified since its creation, this value is the same as the CREATED value.

• LAST_EXECUTED

The date and time when the event last executed. This is a DATETIME value. If the event has never
executed, this column is NULL.

LAST_EXECUTED indicates when the event started. As a result, the ENDS column is never less than
LAST_EXECUTED.

• EVENT_COMMENT

The text of the comment, if the event has one. If not, this value is empty.

• ORIGINATOR

The server ID of the MySQL server on which the event was created; used in replication. This value may
be updated by ALTER EVENT to the server ID of the server on which that statement occurs, if executed
on a replication source. The default value is 0.

• CHARACTER_SET_CLIENT

The session value of the character_set_client system variable when the event was created.

• COLLATION_CONNECTION

The session value of the collation_connection system variable when the event was created.

• DATABASE_COLLATION

The collation of the database with which the event is associated.

Notes

• EVENTS is a nonstandard INFORMATION_SCHEMA table.

• Times in the EVENTS table are displayed using the event time zone, the current session time zone, or

UTC, as described in Section 23.4.4, “Event Metadata”.

• For more information about SLAVESIDE_DISABLED and the ORIGINATOR column, see

Section 16.4.1.16, “Replication of Invoked Features”.

Example

Suppose that the user 'jon'@'ghidora' creates an event named e_daily, and then modifies it a few
minutes later using an ALTER EVENT statement, as shown here:

DELIMITER |

CREATE EVENT e_daily
    ON SCHEDULE
      EVERY 1 DAY
    COMMENT 'Saves total number of sessions then clears the table each day'
    DO

4114

The INFORMATION_SCHEMA EVENTS Table

      BEGIN
        INSERT INTO site_activity.totals (time, total)
          SELECT CURRENT_TIMESTAMP, COUNT(*)
            FROM site_activity.sessions;
        DELETE FROM site_activity.sessions;
      END |

DELIMITER ;

ALTER EVENT e_daily
    ENABLE;

(Note that comments can span multiple lines.)

This user can then run the following SELECT statement, and obtain the output shown:

mysql> SELECT * FROM INFORMATION_SCHEMA.EVENTS
       WHERE EVENT_NAME = 'e_daily'
       AND EVENT_SCHEMA = 'myschema'\G
*************************** 1. row ***************************
       EVENT_CATALOG: def
        EVENT_SCHEMA: myschema
          EVENT_NAME: e_daily
             DEFINER: jon@ghidora
           TIME_ZONE: SYSTEM
          EVENT_BODY: SQL
    EVENT_DEFINITION: BEGIN
        INSERT INTO site_activity.totals (time, total)
          SELECT CURRENT_TIMESTAMP, COUNT(*)
            FROM site_activity.sessions;
        DELETE FROM site_activity.sessions;
      END
          EVENT_TYPE: RECURRING
          EXECUTE_AT: NULL
      INTERVAL_VALUE: 1
      INTERVAL_FIELD: DAY
            SQL_MODE: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,
                      NO_ZERO_IN_DATE,NO_ZERO_DATE,
                      ERROR_FOR_DIVISION_BY_ZERO,
                      NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
              STARTS: 2018-08-08 11:06:34
                ENDS: NULL
              STATUS: ENABLED
       ON_COMPLETION: NOT PRESERVE
             CREATED: 2018-08-08 11:06:34
        LAST_ALTERED: 2018-08-08 11:06:34
       LAST_EXECUTED: 2018-08-08 16:06:34
       EVENT_COMMENT: Saves total number of sessions then clears the
                      table each day
          ORIGINATOR: 1
CHARACTER_SET_CLIENT: utf8
COLLATION_CONNECTION: utf8_general_ci
  DATABASE_COLLATION: latin1_swedish_ci

Event information is also available from the SHOW EVENTS statement. See Section 13.7.5.18, “SHOW
EVENTS Statement”. The following statements are equivalent:

SELECT
    EVENT_SCHEMA, EVENT_NAME, DEFINER, TIME_ZONE, EVENT_TYPE, EXECUTE_AT,
    INTERVAL_VALUE, INTERVAL_FIELD, STARTS, ENDS, STATUS, ORIGINATOR,
    CHARACTER_SET_CLIENT, COLLATION_CONNECTION, DATABASE_COLLATION
  FROM INFORMATION_SCHEMA.EVENTS
  WHERE table_schema = 'db_name'
  [AND column_name LIKE 'wild']

SHOW EVENTS
  [FROM db_name]

4115

The INFORMATION_SCHEMA FILES Table

  [LIKE 'wild']

24.3.9 The INFORMATION_SCHEMA FILES Table

The FILES table provides information about the files in which MySQL tablespace data is stored.

The FILES table provides information about InnoDB data files. In NDB Cluster, this table also provides
information about the files in which NDB Cluster Disk Data tables are stored. For additional information
specific to InnoDB, see InnoDB Notes, later in this section; for additional information specific to NDB
Cluster, see NDB Notes.

The FILES table has these columns:

• FILE_ID

For InnoDB: The tablespace ID, also referred to as the space_id or fil_space_t::id.

For NDB: A file identifier. FILE_ID column values are auto-generated.

• FILE_NAME

For InnoDB: The name of the data file. File-per-table and general tablespaces have an .ibd file name
extension. Undo tablespaces are prefixed by undo. The system tablespace is prefixed by ibdata.
Temporary tablespaces are prefixed by ibtmp. The file name includes the file path, which may be
relative to the MySQL data directory (the value of the datadir system variable).

For NDB: The name of an UNDO log file created by CREATE LOGFILE GROUP or ALTER LOGFILE
GROUP, or of a data file created by CREATE TABLESPACE or ALTER TABLESPACE.

• FILE_TYPE

For InnoDB: The tablespace file type. There are three possible file types for InnoDB files. TABLESPACE
is the file type for any system, general, or file-per-table tablespace file that holds tables, indexes, or other
forms of user data. TEMPORARY is the file type for temporary tablespaces. UNDO LOG is the file type for
undo tablespaces, which hold undo records.

For NDB: One of the values UNDO LOG, DATAFILE, or TABLESPACE.

• TABLESPACE_NAME

The name of the tablespace with which the file is associated.

• TABLE_CATALOG

This value is always empty.

• TABLE_SCHEMA

This is always NULL.

• TABLE_NAME

This is always NULL.

• LOGFILE_GROUP_NAME

For InnoDB: This is always NULL.

For NDB: The name of the log file group to which the log file or data file belongs.

4116

The INFORMATION_SCHEMA FILES Table

For InnoDB: The maximum number of bytes permitted in the file. The value is NULL for all data
files except for predefined system tablespace data files. Maximum system tablespace file size is
defined by innodb_data_file_path. Maximum temporary tablespace file size is defined by
innodb_temp_data_file_path. A NULL value for a predefined system tablespace data file indicates
that a file size limit was not defined explicitly.

For NDB: This value is always the same as the INITIAL_SIZE value.

• AUTOEXTEND_SIZE

The auto-extend size of the tablespace. For NDB, AUTOEXTEND_SIZE is always NULL.

• CREATION_TIME

This is always NULL.

• LAST_UPDATE_TIME

This is always NULL.

• LAST_ACCESS_TIME

This is always NULL.

• RECOVER_TIME

This is always NULL.

• TRANSACTION_COUNTER

This is always NULL.

• VERSION

For InnoDB: This is always NULL.

For NDB: The version number of the file.

• ROW_FORMAT

For InnoDB: This is always NULL.

For NDB: One of FIXED or DYNAMIC.

• TABLE_ROWS

This is always NULL.

• AVG_ROW_LENGTH

This is always NULL.

• DATA_LENGTH

This is always NULL.

• MAX_DATA_LENGTH

This is always NULL.

4118

The INFORMATION_SCHEMA FILES Table

• INDEX_LENGTH

This is always NULL.

• DATA_FREE

For InnoDB: The total amount of free space (in bytes) for the entire tablespace. Predefined system
tablespaces, which include the system tablespace and temporary table tablespaces, may have one or
more data files.

For NDB: This is always NULL.

• CREATE_TIME

This is always NULL.

• UPDATE_TIME

This is always NULL.

• CHECK_TIME

This is always NULL.

• CHECKSUM

This is always NULL.

• STATUS

For InnoDB: This value is NORMAL by default. InnoDB file-per-table tablespaces may report
IMPORTING, which indicates that the tablespace is not yet available.

For NDB: This is always NORMAL.

• EXTRA

For InnoDB: This is always NULL.

For NDB: This column shows which data node the data file or undo log file belongs to (each data node
having its own copy of each file); for an undo log files, it also shows the size of the undo log buffer.
Suppose that you use this statement on an NDB Cluster with four data nodes:

CREATE LOGFILE GROUP mygroup
    ADD UNDOFILE 'new_undo.dat'
    INITIAL_SIZE 2G
    ENGINE NDB;

After running the CREATE LOGFILE GROUP statement successfully, you should see a result similar to
the one shown here for this query against the FILES table:

mysql> SELECT LOGFILE_GROUP_NAME, FILE_TYPE, EXTRA
         FROM INFORMATION_SCHEMA.FILES
         WHERE FILE_NAME = 'new_undo.dat';

+--------------------+-----------+-----------------------------------------+
| LOGFILE_GROUP_NAME | FILE_TYPE | EXTRA                                   |
+--------------------+-----------+-----------------------------------------+
| mygroup            | UNDO LOG  | CLUSTER_NODE=5;UNDO_BUFFER_SIZE=8388608 |
| mygroup            | UNDO LOG  | CLUSTER_NODE=6;UNDO_BUFFER_SIZE=8388608 |
| mygroup            | UNDO LOG  | CLUSTER_NODE=7;UNDO_BUFFER_SIZE=8388608 |

4119

The INFORMATION_SCHEMA FILES Table

| mygroup            | UNDO LOG  | CLUSTER_NODE=8;UNDO_BUFFER_SIZE=8388608 |
+--------------------+-----------+-----------------------------------------+

Notes

• FILES is a nonstandard INFORMATION_SCHEMA table.

InnoDB Notes

The following notes apply to InnoDB data files.

• Data reported by FILES is reported from the InnoDB in-memory cache for open files. By comparison,
INNODB_SYS_DATAFILES reports data from the InnoDB SYS_DATAFILES internal data dictionary
table.

• The data reported by FILES includes temporary tablespace data. This data is not available in
the InnoDB SYS_DATAFILES internal data dictionary table, and is therefore not reported by
INNODB_SYS_DATAFILES.

• Undo tablespace data is reported by FILES.

• The following query returns all data pertinent to InnoDB tablespaces.

SELECT
  FILE_ID, FILE_NAME, FILE_TYPE, TABLESPACE_NAME, FREE_EXTENTS,
  TOTAL_EXTENTS, EXTENT_SIZE, INITIAL_SIZE, MAXIMUM_SIZE,
  AUTOEXTEND_SIZE, DATA_FREE, STATUS
FROM INFORMATION_SCHEMA.FILES WHERE ENGINE='InnoDB'\G

NDB Notes

• The FILES table provides information about Disk Data files only; you cannot use it for determining disk
space allocation or availability for individual NDB tables. However, it is possible to see how much space
is allocated for each NDB table having data stored on disk—as well as how much remains available for
storage of data on disk for that table—using ndb_desc.

• The CREATION_TIME, LAST_UPDATE_TIME, and LAST_ACCESSED values are as reported by the

operating system, and are not supplied by the NDB storage engine. Where no value is provided by the
operating system, these columns display NULL.

• The difference between the TOTAL EXTENTS and FREE_EXTENTS columns is the number of extents

currently in use by the file:

SELECT TOTAL_EXTENTS - FREE_EXTENTS AS extents_used
    FROM INFORMATION_SCHEMA.FILES
    WHERE FILE_NAME = 'myfile.dat';

To approximate the amount of disk space in use by the file, multiply that difference by the value of the
EXTENT_SIZE column, which gives the size of an extent for the file in bytes:

SELECT (TOTAL_EXTENTS - FREE_EXTENTS) * EXTENT_SIZE AS bytes_used
    FROM INFORMATION_SCHEMA.FILES
    WHERE FILE_NAME = 'myfile.dat';

Similarly, you can estimate the amount of space that remains available in a given file by multiplying
FREE_EXTENTS by EXTENT_SIZE:

SELECT FREE_EXTENTS * EXTENT_SIZE AS bytes_free
    FROM INFORMATION_SCHEMA.FILES
    WHERE FILE_NAME = 'myfile.dat';

4120

The INFORMATION_SCHEMA FILES Table

Important

The byte values produced by the preceding queries are approximations only, and
their precision is inversely proportional to the value of EXTENT_SIZE. That is, the
larger EXTENT_SIZE becomes, the less accurate the approximations are.

It is also important to remember that once an extent is used, it cannot be freed again without dropping
the data file of which it is a part. This means that deletes from a Disk Data table do not release disk
space.

The extent size can be set in a CREATE TABLESPACE statement. For more information, see
Section 13.1.19, “CREATE TABLESPACE Statement”.

• An additional row is present in the FILES table following the creation of a logfile group. This row has

NULL for the value of the FILE_NAME column and 0 for the value of the FILE_ID column; the value of
the FILE_TYPE column is always UNDO LOG, and that of the STATUS column is always NORMAL. The
value of the ENGINE column for this row is always ndbcluster.

The FREE_EXTENTS column in this row shows the total number of free extents available to all undo files
belonging to a given log file group whose name and number are shown in the LOGFILE_GROUP_NAME
and LOGFILE_GROUP_NUMBER columns, respectively.

Suppose there are no existing log file groups on your NDB Cluster, and you create one using the
following statement:

mysql> CREATE LOGFILE GROUP lg1
         ADD UNDOFILE 'undofile.dat'
         INITIAL_SIZE = 16M
         UNDO_BUFFER_SIZE = 1M
         ENGINE = NDB;

You can now see this NULL row when you query the FILES table:

mysql> SELECT DISTINCT
         FILE_NAME AS File,
         FREE_EXTENTS AS Free,
         TOTAL_EXTENTS AS Total,
         EXTENT_SIZE AS Size,
         INITIAL_SIZE AS Initial
         FROM INFORMATION_SCHEMA.FILES;
+--------------+---------+---------+------+----------+
| File         | Free    | Total   | Size | Initial  |
+--------------+---------+---------+------+----------+
| undofile.dat |    NULL | 4194304 |    4 | 16777216 |
| NULL         | 4184068 |    NULL |    4 |     NULL |
+--------------+---------+---------+------+----------+

The total number of free extents available for undo logging is always somewhat less than the sum of
the TOTAL_EXTENTS column values for all undo files in the log file group due to overhead required for
maintaining the undo files. This can be seen by adding a second undo file to the log file group, then
repeating the previous query against the FILES table:

mysql> ALTER LOGFILE GROUP lg1
         ADD UNDOFILE 'undofile02.dat'
         INITIAL_SIZE = 4M
         ENGINE = NDB;

mysql> SELECT DISTINCT
         FILE_NAME AS File,
         FREE_EXTENTS AS Free,

4121

The INFORMATION_SCHEMA FILES Table

         TOTAL_EXTENTS AS Total,
         EXTENT_SIZE AS Size,
         INITIAL_SIZE AS Initial
         FROM INFORMATION_SCHEMA.FILES;
+----------------+---------+---------+------+----------+
| File           | Free    | Total   | Size | Initial  |
+----------------+---------+---------+------+----------+
| undofile.dat   |    NULL | 4194304 |    4 | 16777216 |
| undofile02.dat |    NULL | 1048576 |    4 |  4194304 |
| NULL           | 5223944 |    NULL |    4 |     NULL |
+----------------+---------+---------+------+----------+

The amount of free space in bytes which is available for undo logging by Disk Data tables using this log
file group can be approximated by multiplying the number of free extents by the initial size:

mysql> SELECT
         FREE_EXTENTS AS 'Free Extents',
         FREE_EXTENTS * EXTENT_SIZE AS 'Free Bytes'
         FROM INFORMATION_SCHEMA.FILES
         WHERE LOGFILE_GROUP_NAME = 'lg1'
         AND FILE_NAME IS NULL;
+--------------+------------+
| Free Extents | Free Bytes |
+--------------+------------+
|      5223944 |   20895776 |
+--------------+------------+

If you create an NDB Cluster Disk Data table and then insert some rows into it, you can see
approximately how much space remains for undo logging afterward, for example:

mysql> CREATE TABLESPACE ts1
         ADD DATAFILE 'data1.dat'
         USE LOGFILE GROUP lg1
         INITIAL_SIZE 512M
         ENGINE = NDB;

mysql> CREATE TABLE dd (
         c1 INT NOT NULL PRIMARY KEY,
         c2 INT,
         c3 DATE
         )
         TABLESPACE ts1 STORAGE DISK
         ENGINE = NDB;

mysql> INSERT INTO dd VALUES
         (NULL, 1234567890, '2007-02-02'),
         (NULL, 1126789005, '2007-02-03'),
         (NULL, 1357924680, '2007-02-04'),
         (NULL, 1642097531, '2007-02-05');

mysql> SELECT
         FREE_EXTENTS AS 'Free Extents',
         FREE_EXTENTS * EXTENT_SIZE AS 'Free Bytes'
         FROM INFORMATION_SCHEMA.FILES
         WHERE LOGFILE_GROUP_NAME = 'lg1'
         AND FILE_NAME IS NULL;
+--------------+------------+
| Free Extents | Free Bytes |
+--------------+------------+
|      5207565 |   20830260 |
+--------------+------------+

• An additional row is present in the FILES table for any NDB Cluster tablespace, whether or not any data
files are associated with the tablespace. This row has NULL for the value of the FILE_NAME column, and
the value of the FILE_ID column is always 0. The value shown in the FILE_TYPE column is always

4122

The INFORMATION_SCHEMA GLOBAL_STATUS and SESSION_STATUS Tables

TABLESPACE, and that of the STATUS column is always NORMAL. The value of the ENGINE column for
this row is always ndbcluster.

• For additional information, and examples of creating and dropping NDB Cluster Disk Data objects, see

Section 21.6.11, “NDB Cluster Disk Data Tables”.

• As of MySQL 5.7.31, you must have the PROCESS privilege to query this table.

24.3.10 The INFORMATION_SCHEMA GLOBAL_STATUS and
SESSION_STATUS Tables

Note

The value of the show_compatibility_56 system variable affects the
information available from the tables described here. For details, see the description
of that variable in Section 5.1.7, “Server System Variables”.

Note

Information available from the tables described here is also available from the
Performance Schema. The INFORMATION_SCHEMA tables are deprecated in
preference to the Performance Schema tables and are removed in MySQL 8.0.
For advice on migrating away from the INFORMATION_SCHEMA tables to the
Performance Schema tables, see Section 25.20, “Migrating to Performance
Schema System and Status Variable Tables”.

The GLOBAL_STATUS and SESSION_STATUS tables provide information about server status variables.
Their contents correspond to the information produced by the SHOW GLOBAL STATUS and SHOW
SESSION STATUS statements (see Section 13.7.5.35, “SHOW STATUS Statement”).

Notes

• The VARIABLE_VALUE column for each of these tables is defined as VARCHAR(1024).

24.3.11 The INFORMATION_SCHEMA GLOBAL_VARIABLES and
SESSION_VARIABLES Tables

Note

The value of the show_compatibility_56 system variable affects the
information available from the tables described here. For details, see the description
of that variable in Section 5.1.7, “Server System Variables”.

Note

Information available from the tables described here is also available from the
Performance Schema. The INFORMATION_SCHEMA tables are deprecated in
preference to the Performance Schema tables and are removed in MySQL 8.0.
For advice on migrating away from the INFORMATION_SCHEMA tables to the
Performance Schema tables, see Section 25.20, “Migrating to Performance
Schema System and Status Variable Tables”.

The GLOBAL_VARIABLES and SESSION_VARIABLES tables provide information about server status
variables. Their contents correspond to the information produced by the SHOW GLOBAL VARIABLES and
SHOW SESSION VARIABLES statements (see Section 13.7.5.39, “SHOW VARIABLES Statement”).

4123

The INFORMATION_SCHEMA KEY_COLUMN_USAGE Table

Notes

• The VARIABLE_VALUE column for each of these tables is defined as VARCHAR(1024). For variables
with very long values that are not completely displayed, use SELECT as a workaround. For example:

SELECT @@GLOBAL.innodb_data_file_path;

24.3.12 The INFORMATION_SCHEMA KEY_COLUMN_USAGE Table

The KEY_COLUMN_USAGE table describes which key columns have constraints.

The KEY_COLUMN_USAGE table has these columns:

• CONSTRAINT_CATALOG

The name of the catalog to which the constraint belongs. This value is always def.

• CONSTRAINT_SCHEMA

The name of the schema (database) to which the constraint belongs.

• CONSTRAINT_NAME

The name of the constraint.

• TABLE_CATALOG

The name of the catalog to which the table belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema (database) to which the table belongs.

• TABLE_NAME

The name of the table that has the constraint.

• COLUMN_NAME

The name of the column that has the constraint.

If the constraint is a foreign key, then this is the column of the foreign key, not the column that the foreign
key references.

• ORDINAL_POSITION

The column's position within the constraint, not the column's position within the table. Column positions
are numbered beginning with 1.

• POSITION_IN_UNIQUE_CONSTRAINT

NULL for unique and primary-key constraints. For foreign-key constraints, this column is the ordinal
position in key of the table that is being referenced.

• REFERENCED_TABLE_SCHEMA

The name of the schema (database) referenced by the constraint.

• REFERENCED_TABLE_NAME

4124

The INFORMATION_SCHEMA ndb_transid_mysql_connection_map Table

The name of the table referenced by the constraint.

• REFERENCED_COLUMN_NAME

The name of the column referenced by the constraint.

Suppose that there are two tables name t1 and t3 that have the following definitions:

CREATE TABLE t1
(
    s1 INT,
    s2 INT,
    s3 INT,
    PRIMARY KEY(s3)
) ENGINE=InnoDB;

CREATE TABLE t3
(
    s1 INT,
    s2 INT,
    s3 INT,
    KEY(s1),
    CONSTRAINT CO FOREIGN KEY (s2) REFERENCES t1(s3)
) ENGINE=InnoDB;

For those two tables, the KEY_COLUMN_USAGE table has two rows:

• One row with CONSTRAINT_NAME = 'PRIMARY', TABLE_NAME = 't1', COLUMN_NAME = 's3',

ORDINAL_POSITION = 1, POSITION_IN_UNIQUE_CONSTRAINT = NULL.

• One row with CONSTRAINT_NAME = 'CO', TABLE_NAME = 't3', COLUMN_NAME = 's2',

ORDINAL_POSITION = 1, POSITION_IN_UNIQUE_CONSTRAINT = 1.

24.3.13 The INFORMATION_SCHEMA ndb_transid_mysql_connection_map
Table

The ndb_transid_mysql_connection_map table provides a mapping between NDB transactions, NDB
transaction coordinators, and MySQL Servers attached to an NDB Cluster as API nodes. This information
is used when populating the server_operations and server_transactions tables of the ndbinfo
NDB Cluster information database.

The ndb_transid_mysql_connection_map table has these columns:

• mysql_connection_id

The MySQL server connection ID.

• node_id

The transaction coordinator node ID.

• ndb_transid

The NDB transaction ID.

Notes

The mysql_connection_id value is the same as the connection or session ID shown in the output of
SHOW PROCESSLIST.

4125

The INFORMATION_SCHEMA OPTIMIZER_TRACE Table

There are no SHOW statements associated with this table.

This is a nonstandard table, specific to NDB Cluster. It is implemented as an INFORMATION_SCHEMA
plugin; you can verify that it is supported by checking the output of SHOW PLUGINS. If
ndb_transid_mysql_connection_map support is enabled, the output from this statement includes
a plugin having this name, of type INFORMATION SCHEMA, and having status ACTIVE, as shown here
(using emphasized text):

mysql> SHOW PLUGINS;
+----------------------------------+--------+--------------------+---------+---------+
| Name                             | Status | Type               | Library | License |
+----------------------------------+--------+--------------------+---------+---------+
| binlog                           | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| mysql_native_password            | ACTIVE | AUTHENTICATION     | NULL    | GPL     |
| CSV                              | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| MEMORY                           | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| MRG_MYISAM                       | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| MyISAM                           | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| PERFORMANCE_SCHEMA               | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| BLACKHOLE                        | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| ARCHIVE                          | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| ndbcluster                       | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| ndbinfo                          | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| ndb_transid_mysql_connection_map | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| InnoDB                           | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
| INNODB_TRX                       | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_LOCKS                     | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_LOCK_WAITS                | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP                       | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMP_RESET                 | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMPMEM                    | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| INNODB_CMPMEM_RESET              | ACTIVE | INFORMATION SCHEMA | NULL    | GPL     |
| partition                        | ACTIVE | STORAGE ENGINE     | NULL    | GPL     |
+----------------------------------+--------+--------------------+---------+---------+
22 rows in set (0.00 sec)

The plugin is enabled by default. You can disable it (or force the server not to run unless the plugin
starts) by starting the server with the --ndb-transid-mysql-connection-map option. If the plugin is
disabled, the status is shown by SHOW PLUGINS as DISABLED. The plugin cannot be enabled or disabled
at runtime.

Although the names of this table and its columns are displayed using lowercase, you can use uppercase or
lowercase when referring to them in SQL statements.

For this table to be created, the MySQL Server must be a binary supplied with the NDB Cluster distribution,
or one built from the NDB Cluster sources with NDB storage engine support enabled. It is not available in
the standard MySQL 5.7 Server.

24.3.14 The INFORMATION_SCHEMA OPTIMIZER_TRACE Table

The OPTIMIZER_TRACE table provides information produced by the optimizer tracing capability for
traced statements. To enable tracking, use the optimizer_trace system variable. For details, see
Section 8.15, “Tracing the Optimizer”.

The OPTIMIZER_TRACE table has these columns:

• QUERY

The text of the traced statement.

• TRACE

4126

The INFORMATION_SCHEMA PARAMETERS Table

The trace, in JSON format.

• MISSING_BYTES_BEYOND_MAX_MEM_SIZE

Each remembered trace is a string that is extended as optimization progresses and appends data to it.
The optimizer_trace_max_mem_size variable sets a limit on the total amount of memory used by
all currently remembered traces. If this limit is reached, the current trace is not extended (and thus is
incomplete), and the MISSING_BYTES_BEYOND_MAX_MEM_SIZE column shows the number of bytes
missing from the trace.

• INSUFFICIENT_PRIVILEGES

If a traced query uses views or stored routines that have SQL SECURITY with a value of DEFINER, it
may be that a user other than the definer is denied from seeing the trace of the query. In that case, the
trace is shown as empty and INSUFFICIENT_PRIVILEGES has a value of 1. Otherwise, the value is 0.

24.3.15 The INFORMATION_SCHEMA PARAMETERS Table

The PARAMETERS table provides information about parameters for stored routines (stored procedures and
stored functions), and about return values for stored functions. The PARAMETERS table does not include
built-in (native) functions or loadable functions. Parameter information is similar to the contents of the
param_list column in the mysql.proc table.

The PARAMETERS table has these columns:

• SPECIFIC_CATALOG

The name of the catalog to which the routine containing the parameter belongs. This value is always
def.

• SPECIFIC_SCHEMA

The name of the schema (database) to which the routine containing the parameter belongs.

• SPECIFIC_NAME

The name of the routine containing the parameter.

• ORDINAL_POSITION

For successive parameters of a stored procedure or function, the ORDINAL_POSITION values are 1,
2, 3, and so forth. For a stored function, there is also a row that applies to the function return value (as
described by the RETURNS clause). The return value is not a true parameter, so the row that describes it
has these unique characteristics:

• The ORDINAL_POSITION value is 0.

• The PARAMETER_NAME and PARAMETER_MODE values are NULL because the return value has no

name and the mode does not apply.

• PARAMETER_MODE

The mode of the parameter. This value is one of IN, OUT, or INOUT. For a stored function return value,
this value is NULL.

• PARAMETER_NAME

4127

The INFORMATION_SCHEMA PARTITIONS Table

The name of the parameter. For a stored function return value, this value is NULL.

• DATA_TYPE

The parameter data type.

The DATA_TYPE value is the type name only with no other information. The DTD_IDENTIFIER value
contains the type name and possibly other information such as the precision or length.

• CHARACTER_MAXIMUM_LENGTH

For string parameters, the maximum length in characters.

• CHARACTER_OCTET_LENGTH

For string parameters, the maximum length in bytes.

• NUMERIC_PRECISION

For numeric parameters, the numeric precision.

• NUMERIC_SCALE

For numeric parameters, the numeric scale.

• DATETIME_PRECISION

For temporal parameters, the fractional seconds precision.

• CHARACTER_SET_NAME

For character string parameters, the character set name.

• COLLATION_NAME

For character string parameters, the collation name.

• DTD_IDENTIFIER

The parameter data type.

The DATA_TYPE value is the type name only with no other information. The DTD_IDENTIFIER value
contains the type name and possibly other information such as the precision or length.

• ROUTINE_TYPE

PROCEDURE for stored procedures, FUNCTION for stored functions.

24.3.16 The INFORMATION_SCHEMA PARTITIONS Table

The PARTITIONS table provides information about table partitions. Each row in this table corresponds to
an individual partition or subpartition of a partitioned table. For more information about partitioning tables,
see Chapter 22, Partitioning.

The PARTITIONS table has these columns:

• TABLE_CATALOG

The name of the catalog to which the table belongs. This value is always def.

4128

The INFORMATION_SCHEMA PARTITIONS Table

• TABLE_SCHEMA

The name of the schema (database) to which the table belongs.

• TABLE_NAME

The name of the table containing the partition.

• PARTITION_NAME

The name of the partition.

• SUBPARTITION_NAME

If the PARTITIONS table row represents a subpartition, the name of subpartition; otherwise NULL.

• PARTITION_ORDINAL_POSITION

All partitions are indexed in the same order as they are defined, with 1 being the number assigned to the
first partition. The indexing can change as partitions are added, dropped, and reorganized; the number
shown is this column reflects the current order, taking into account any indexing changes.

• SUBPARTITION_ORDINAL_POSITION

Subpartitions within a given partition are also indexed and reindexed in the same manner as partitions
are indexed within a table.

• PARTITION_METHOD

One of the values RANGE, LIST, HASH, LINEAR HASH, KEY, or LINEAR KEY; that is, one of the
available partitioning types as discussed in Section 22.2, “Partitioning Types”.

• SUBPARTITION_METHOD

One of the values HASH, LINEAR HASH, KEY, or LINEAR KEY; that is, one of the available
subpartitioning types as discussed in Section 22.2.6, “Subpartitioning”.

• PARTITION_EXPRESSION

The expression for the partitioning function used in the CREATE TABLE or ALTER TABLE statement that
created the table's current partitioning scheme.

For example, consider a partitioned table created in the test database using this statement:

CREATE TABLE tp (
    c1 INT,
    c2 INT,
    c3 VARCHAR(25)
)
PARTITION BY HASH(c1 + c2)
PARTITIONS 4;

The PARTITION_EXPRESSION column in a PARTITIONS table row for a partition from this table
displays c1 + c2, as shown here:

mysql> SELECT DISTINCT PARTITION_EXPRESSION
       FROM INFORMATION_SCHEMA.PARTITIONS
       WHERE TABLE_NAME='tp' AND TABLE_SCHEMA='test';
+----------------------+
| PARTITION_EXPRESSION |

4129

The INFORMATION_SCHEMA PARTITIONS Table

+----------------------+
| c1 + c2              |
+----------------------+

For an NDB table that is not explicitly partitioned, this column is empty. For tables using other storage
engines and which are not partitioned, this column is NULL.

• SUBPARTITION_EXPRESSION

This works in the same fashion for the subpartitioning expression that defines the subpartitioning for
a table as PARTITION_EXPRESSION does for the partitioning expression used to define a table's
partitioning.

If the table has no subpartitions, this column is NULL.

• PARTITION_DESCRIPTION

This column is used for RANGE and LIST partitions. For a RANGE partition, it contains the value set in
the partition's VALUES LESS THAN clause, which can be either an integer or MAXVALUE. For a LIST
partition, this column contains the values defined in the partition's VALUES IN clause, which is a list of
comma-separated integer values.

For partitions whose PARTITION_METHOD is other than RANGE or LIST, this column is always NULL.

• TABLE_ROWS

The number of table rows in the partition.

For partitioned InnoDB tables, the row count given in the TABLE_ROWS column is only an estimated
value used in SQL optimization, and may not always be exact.

For NDB tables, you can also obtain this information using the ndb_desc utility.

• AVG_ROW_LENGTH

The average length of the rows stored in this partition or subpartition, in bytes. This is the same as
DATA_LENGTH divided by TABLE_ROWS.

For NDB tables, you can also obtain this information using the ndb_desc utility.

• DATA_LENGTH

The total length of all rows stored in this partition or subpartition, in bytes; that is, the total number of
bytes stored in the partition or subpartition.

For NDB tables, you can also obtain this information using the ndb_desc utility.

• MAX_DATA_LENGTH

The maximum number of bytes that can be stored in this partition or subpartition.

For NDB tables, you can also obtain this information using the ndb_desc utility.

• INDEX_LENGTH

The length of the index file for this partition or subpartition, in bytes.

For partitions of NDB tables, whether the tables use implicit or explicit partitioning, the INDEX_LENGTH
column value is always 0. However, you can obtain equivalent information using the ndb_desc utility.

4130

The INFORMATION_SCHEMA PARTITIONS Table

• DATA_FREE

The number of bytes allocated to the partition or subpartition but not used.

For NDB tables, you can also obtain this information using the ndb_desc utility.

• CREATE_TIME

The time that the partition or subpartition was created.

• UPDATE_TIME

The time that the partition or subpartition was last modified.

• CHECK_TIME

The last time that the table to which this partition or subpartition belongs was checked.

For partitioned InnoDB tables, the value is always NULL.

• CHECKSUM

The checksum value, if any; otherwise NULL.

• PARTITION_COMMENT

Notes

The text of the comment, if the partition has one. If not, this value is empty.

The maximum length for a partition comment is defined as 1024 characters, and the display width of the
PARTITION_COMMENT column is also 1024, characters to match this limit.

• NODEGROUP

This is the nodegroup to which the partition belongs. For NDB Cluster tables, this is always default.
For partitioned tables using storage engines other than NDB, the value is also default. Otherwise, this
column is empty.

• TABLESPACE_NAME

The name of the tablespace to which the partition belongs. The value is always DEFAULT, unless the
table uses the NDB storage engine (see the Notes at the end of this section).

• PARTITIONS is a nonstandard INFORMATION_SCHEMA table.

• A table using any storage engine other than NDB and which is not partitioned has one row in

the PARTITIONS table. However, the values of the PARTITION_NAME, SUBPARTITION_NAME,
PARTITION_ORDINAL_POSITION, SUBPARTITION_ORDINAL_POSITION, PARTITION_METHOD,
SUBPARTITION_METHOD, PARTITION_EXPRESSION, SUBPARTITION_EXPRESSION, and
PARTITION_DESCRIPTION columns are all NULL. Also, the PARTITION_COMMENT column in this case
is blank.

• An NDB table which is not explicitly partitioned has one row in the PARTITIONS table for each data node

in the NDB cluster. For each such row:

• The SUBPARTITION_NAME, SUBPARTITION_ORDINAL_POSITION, SUBPARTITION_METHOD,
SUBPARTITION_EXPRESSION, CREATE_TIME, UPDATE_TIME, CHECK_TIME, CHECKSUM, and
TABLESPACE_NAME columns are all NULL.

4131

The INFORMATION_SCHEMA PLUGINS Table

• The PARTITION_METHOD is always KEY.

• The NODEGROUP column is default.

• The PARTITION_EXPRESSION and PARTITION_COMMENT columns are empty.

24.3.17 The INFORMATION_SCHEMA PLUGINS Table

The PLUGINS table provides information about server plugins.

The PLUGINS table has these columns:

• PLUGIN_NAME

The name used to refer to the plugin in statements such as INSTALL PLUGIN and UNINSTALL
PLUGIN.

• PLUGIN_VERSION

The version from the plugin's general type descriptor.

• PLUGIN_STATUS

The plugin status, one of ACTIVE, INACTIVE, DISABLED, or DELETED.

• PLUGIN_TYPE

The type of plugin, such as STORAGE ENGINE, INFORMATION_SCHEMA, or AUTHENTICATION.

• PLUGIN_TYPE_VERSION

The version from the plugin's type-specific descriptor.

• PLUGIN_LIBRARY

The name of the plugin shared library file. This is the name used to refer to the plugin file in statements
such as INSTALL PLUGIN and UNINSTALL PLUGIN. This file is located in the directory named by
the plugin_dir system variable. If the library name is NULL, the plugin is compiled in and cannot be
uninstalled with UNINSTALL PLUGIN.

• PLUGIN_LIBRARY_VERSION

The plugin API interface version.

• PLUGIN_AUTHOR

The plugin author.

• PLUGIN_DESCRIPTION

A short description of the plugin.

• PLUGIN_LICENSE

How the plugin is licensed (for example, GPL).

• LOAD_OPTION

4132

The INFORMATION_SCHEMA PROCESSLIST Table

How the plugin was loaded. The value is OFF, ON, FORCE, or FORCE_PLUS_PERMANENT. See
Section 5.5.1, “Installing and Uninstalling Plugins”.

Notes

• PLUGINS is a nonstandard INFORMATION_SCHEMA table.

• For plugins installed with INSTALL PLUGIN, the PLUGIN_NAME and PLUGIN_LIBRARY values are also

registered in the mysql.plugin table.

• For information about plugin data structures that form the basis of the information in the PLUGINS table,

see The MySQL Plugin API.

Plugin information is also available from the SHOW PLUGINS statement. See Section 13.7.5.25, “SHOW
PLUGINS Statement”. These statements are equivalent:

SELECT
  PLUGIN_NAME, PLUGIN_STATUS, PLUGIN_TYPE,
  PLUGIN_LIBRARY, PLUGIN_LICENSE
FROM INFORMATION_SCHEMA.PLUGINS;

SHOW PLUGINS;

24.3.18 The INFORMATION_SCHEMA PROCESSLIST Table

The MySQL process list indicates the operations currently being performed by the set of threads executing
within the server. The PROCESSLIST table is one source of process information. For a comparison of this
table with other sources, see Sources of Process Information.

The PROCESSLIST table has these columns:

• ID

The connection identifier. This is the same value displayed in the Id column of the SHOW PROCESSLIST
statement, displayed in the PROCESSLIST_ID column of the Performance Schema threads table, and
returned by the CONNECTION_ID() function within the thread.

• USER

The MySQL user who issued the statement. A value of system user refers to a nonclient thread
spawned by the server to handle tasks internally, for example, a delayed-row handler thread or an I/O
or SQL thread used on replica hosts. For system user, there is no host specified in the Host column.
unauthenticated user refers to a thread that has become associated with a client connection but for
which authentication of the client user has not yet occurred. event_scheduler refers to the thread that
monitors scheduled events (see Section 23.4, “Using the Event Scheduler”).

• HOST

The host name of the client issuing the statement (except for system user, for which there is no host).
The host name for TCP/IP connections is reported in host_name:client_port format to make it
easier to determine which client is doing what.

• DB

The default database for the thread, or NULL if none has been selected.

• COMMAND

4133

The INFORMATION_SCHEMA PROFILING Table

The type of command the thread is executing on behalf of the client, or Sleep if the session is idle. For
descriptions of thread commands, see Section 8.14, “Examining Server Thread (Process) Information”.
The value of this column corresponds to the COM_xxx commands of the client/server protocol and
Com_xxx status variables. See Section 5.1.9, “Server Status Variables”.

• TIME

The time in seconds that the thread has been in its current state. For a replica SQL thread, the value
is the number of seconds between the timestamp of the last replicated event and the real time of the
replica host. See Section 16.2.3, “Replication Threads”.

• STATE

An action, event, or state that indicates what the thread is doing. For descriptions of STATE values, see
Section 8.14, “Examining Server Thread (Process) Information”.

Most states correspond to very quick operations. If a thread stays in a given state for many seconds,
there might be a problem that needs to be investigated.

• INFO

The statement the thread is executing, or NULL if it is executing no statement. The statement might be
the one sent to the server, or an innermost statement if the statement executes other statements. For
example, if a CALL statement executes a stored procedure that is executing a SELECT statement, the
INFO value shows the SELECT statement.

• PROCESSLIST is a nonstandard INFORMATION_SCHEMA table.

• Like the output from the SHOW PROCESSLIST statement, the PROCESSLIST table provides information
about all threads, even those belonging to other users, if you have the PROCESS privilege. Otherwise
(without the PROCESS privilege), nonanonymous users have access to information about their own
threads but not threads for other users, and anonymous users have no access to thread information.

• If an SQL statement refers to the PROCESSLIST table, MySQL populates the entire table once, when

statement execution begins, so there is read consistency during the statement. There is no read
consistency for a multi-statement transaction.

The following statements are equivalent:

SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST

SHOW FULL PROCESSLIST

Notes

24.3.19 The INFORMATION_SCHEMA PROFILING Table

The PROFILING table provides statement profiling information. Its contents correspond to the information
produced by the SHOW PROFILE and SHOW PROFILES statements (see Section 13.7.5.30, “SHOW
PROFILE Statement”). The table is empty unless the profiling session variable is set to 1.

Note

This table is deprecated; expect it to be removed in a future release of MySQL.
Use the Performance Schema instead; see Section 25.19.1, “Query Profiling Using
Performance Schema”.

4134

The INFORMATION_SCHEMA REFERENTIAL_CONSTRAINTS Table

The PROFILING table has these columns:

• QUERY_ID

A numeric statement identifier.

• SEQ

A sequence number indicating the display order for rows with the same QUERY_ID value.

• STATE

The profiling state to which the row measurements apply.

• DURATION

How long statement execution remained in the given state, in seconds.

• CPU_USER, CPU_SYSTEM

User and system CPU use, in seconds.

• CONTEXT_VOLUNTARY, CONTEXT_INVOLUNTARY

How many voluntary and involuntary context switches occurred.

• BLOCK_OPS_IN, BLOCK_OPS_OUT

The number of block input and output operations.

• MESSAGES_SENT, MESSAGES_RECEIVED

The number of communication messages sent and received.

• PAGE_FAULTS_MAJOR, PAGE_FAULTS_MINOR

The number of major and minor page faults.

• SWAPS

How many swaps occurred.

• SOURCE_FUNCTION, SOURCE_FILE, and SOURCE_LINE

Information indicating where in the source code the profiled state executes.

Notes

• PROFILING is a nonstandard INFORMATION_SCHEMA table.

Profiling information is also available from the SHOW PROFILE and SHOW PROFILES statements. See
Section 13.7.5.30, “SHOW PROFILE Statement”. For example, the following queries are equivalent:

SHOW PROFILE FOR QUERY 2;

SELECT STATE, FORMAT(DURATION, 6) AS DURATION
FROM INFORMATION_SCHEMA.PROFILING
WHERE QUERY_ID = 2 ORDER BY SEQ;

24.3.20 The INFORMATION_SCHEMA REFERENTIAL_CONSTRAINTS Table

4135

The INFORMATION_SCHEMA ROUTINES Table

The REFERENTIAL_CONSTRAINTS table provides information about foreign keys.

The REFERENTIAL_CONSTRAINTS table has these columns:

• CONSTRAINT_CATALOG

The name of the catalog to which the constraint belongs. This value is always def.

• CONSTRAINT_SCHEMA

The name of the schema (database) to which the constraint belongs.

• CONSTRAINT_NAME

The name of the constraint.

• UNIQUE_CONSTRAINT_CATALOG

The name of the catalog containing the unique constraint that the constraint references. This value is
always def.

• UNIQUE_CONSTRAINT_SCHEMA

The name of the schema (database) containing the unique constraint that the constraint references.

• UNIQUE_CONSTRAINT_NAME

The name of the unique constraint that the constraint references.

• MATCH_OPTION

The value of the constraint MATCH attribute. The only valid value at this time is NONE.

• UPDATE_RULE

The value of the constraint ON UPDATE attribute. The possible values are CASCADE, SET NULL, SET
DEFAULT, RESTRICT, NO ACTION.

• DELETE_RULE

The value of the constraint ON DELETE attribute. The possible values are CASCADE, SET NULL, SET
DEFAULT, RESTRICT, NO ACTION.

• TABLE_NAME

The name of the table. This value is the same as in the TABLE_CONSTRAINTS table.

• REFERENCED_TABLE_NAME

The name of the table referenced by the constraint.

24.3.21 The INFORMATION_SCHEMA ROUTINES Table

The ROUTINES table provides information about stored routines (stored procedures and stored functions).
The ROUTINES table does not include built-in (native) functions or loadable functions.

The column named “mysql.proc Name” indicates the mysql.proc table column that corresponds to the
INFORMATION_SCHEMA ROUTINES table column, if any.

The ROUTINES table has these columns:

4136

The INFORMATION_SCHEMA ROUTINES Table

• SPECIFIC_NAME

The name of the routine.

• ROUTINE_CATALOG

The name of the catalog to which the routine belongs. This value is always def.

• ROUTINE_SCHEMA

The name of the schema (database) to which the routine belongs.

• ROUTINE_NAME

The name of the routine.

• ROUTINE_TYPE

PROCEDURE for stored procedures, FUNCTION for stored functions.

• DATA_TYPE

If the routine is a stored function, the return value data type. If the routine is a stored procedure, this
value is empty.

The DATA_TYPE value is the type name only with no other information. The DTD_IDENTIFIER value
contains the type name and possibly other information such as the precision or length.

• CHARACTER_MAXIMUM_LENGTH

For stored function string return values, the maximum length in characters. If the routine is a stored
procedure, this value is NULL.

• CHARACTER_OCTET_LENGTH

For stored function string return values, the maximum length in bytes. If the routine is a stored
procedure, this value is NULL.

• NUMERIC_PRECISION

For stored function numeric return values, the numeric precision. If the routine is a stored procedure, this
value is NULL.

• NUMERIC_SCALE

For stored function numeric return values, the numeric scale. If the routine is a stored procedure, this
value is NULL.

• DATETIME_PRECISION

For stored function temporal return values, the fractional seconds precision. If the routine is a stored
procedure, this value is NULL.

• CHARACTER_SET_NAME

For stored function character string return values, the character set name. If the routine is a stored
procedure, this value is NULL.

• COLLATION_NAME

4137

The INFORMATION_SCHEMA ROUTINES Table

For stored function character string return values, the collation name. If the routine is a stored procedure,
this value is NULL.

• DTD_IDENTIFIER

If the routine is a stored function, the return value data type. If the routine is a stored procedure, this
value is empty.

The DATA_TYPE value is the type name only with no other information. The DTD_IDENTIFIER value
contains the type name and possibly other information such as the precision or length.

• ROUTINE_BODY

The language used for the routine definition. This value is always SQL.

• ROUTINE_DEFINITION

The text of the SQL statement executed by the routine.

• EXTERNAL_NAME

This value is always NULL.

• EXTERNAL_LANGUAGE

The language of the stored routine. MySQL calculates EXTERNAL_LANGUAGE thus:

• If mysql.proc.language='SQL', EXTERNAL_LANGUAGE is NULL

• Otherwise, EXTERNAL_LANGUAGE is what is in mysql.proc.language. However, we do not have

external languages yet, so it is always NULL.

• PARAMETER_STYLE

This value is always SQL.

• IS_DETERMINISTIC

YES or NO, depending on whether the routine is defined with the DETERMINISTIC characteristic.

• SQL_DATA_ACCESS

The data access characteristic for the routine. The value is one of CONTAINS SQL, NO SQL, READS
SQL DATA, or MODIFIES SQL DATA.

• SQL_PATH

This value is always NULL.

• SECURITY_TYPE

The routine SQL SECURITY characteristic. The value is one of DEFINER or INVOKER.

• CREATED

The date and time when the routine was created. This is a TIMESTAMP value.

• LAST_ALTERED

4138

The INFORMATION_SCHEMA SCHEMATA Table

The date and time when the routine was last modified. This is a TIMESTAMP value. If the routine has not
been modified since its creation, this value is the same as the CREATED value.

• SQL_MODE

The SQL mode in effect when the routine was created or altered, and under which the routine executes.
For the permitted values, see Section 5.1.10, “Server SQL Modes”.

• ROUTINE_COMMENT

The text of the comment, if the routine has one. If not, this value is empty.

• DEFINER

The account named in the DEFINER clause (often the user who created the routine), in
'user_name'@'host_name' format.

• CHARACTER_SET_CLIENT

The session value of the character_set_client system variable when the routine was created.

• COLLATION_CONNECTION

The session value of the collation_connection system variable when the routine was created.

• DATABASE_COLLATION

The collation of the database with which the routine is associated.

Notes

• To see information about a routine, you must be the user named in the routine DEFINER clause or have
SELECT access to the mysql.proc table. If you do not have privileges for the routine itself, the value
displayed for the ROUTINE_DEFINITION column is NULL.

• Information about stored function return values is also available in the PARAMETERS table. The return

value row for a stored function can be identified as the row that has an ORDINAL_POSITION value of 0.

24.3.22 The INFORMATION_SCHEMA SCHEMATA Table

A schema is a database, so the SCHEMATA table provides information about databases.

The SCHEMATA table has these columns:

• CATALOG_NAME

The name of the catalog to which the schema belongs. This value is always def.

• SCHEMA_NAME

The name of the schema.

• DEFAULT_CHARACTER_SET_NAME

The schema default character set.

• DEFAULT_COLLATION_NAME

4139

The INFORMATION_SCHEMA SCHEMA_PRIVILEGES Table

The schema default collation.

• SQL_PATH

This value is always NULL.

Schema names are also available from the SHOW DATABASES statement. See Section 13.7.5.14, “SHOW
DATABASES Statement”. The following statements are equivalent:

SELECT SCHEMA_NAME AS `Database`
  FROM INFORMATION_SCHEMA.SCHEMATA
  [WHERE SCHEMA_NAME LIKE 'wild']

SHOW DATABASES
  [LIKE 'wild']

You see only those databases for which you have some kind of privilege, unless you have the global SHOW
DATABASES privilege.

Caution

Because a global privilege is considered a privilege for all databases, any global
privilege enables a user to see all database names with SHOW DATABASES or by
examining the INFORMATION_SCHEMA SCHEMATA table.

24.3.23 The INFORMATION_SCHEMA SCHEMA_PRIVILEGES Table

The SCHEMA_PRIVILEGES table provides information about schema (database) privileges. It takes its
values from the mysql.db system table.

The SCHEMA_PRIVILEGES table has these columns:

• GRANTEE

The name of the account to which the privilege is granted, in 'user_name'@'host_name' format.

• TABLE_CATALOG

The name of the catalog to which the schema belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema.

• PRIVILEGE_TYPE

The privilege granted. The value can be any privilege that can be granted at the schema level; see
Section 13.7.1.4, “GRANT Statement”. Each row lists a single privilege, so there is one row per schema
privilege held by the grantee.

• IS_GRANTABLE

YES if the user has the GRANT OPTION privilege, NO otherwise. The output does not list GRANT OPTION
as a separate row with PRIVILEGE_TYPE='GRANT OPTION'.

• SCHEMA_PRIVILEGES is a nonstandard INFORMATION_SCHEMA table.

Notes

4140

The INFORMATION_SCHEMA STATISTICS Table

The following statements are not equivalent:

SELECT ... FROM INFORMATION_SCHEMA.SCHEMA_PRIVILEGES

SHOW GRANTS ...

24.3.24 The INFORMATION_SCHEMA STATISTICS Table

The STATISTICS table provides information about table indexes.

The STATISTICS table has these columns:

• TABLE_CATALOG

The name of the catalog to which the table containing the index belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema (database) to which the table containing the index belongs.

• TABLE_NAME

The name of the table containing the index.

• NON_UNIQUE

0 if the index cannot contain duplicates, 1 if it can.

• INDEX_SCHEMA

The name of the schema (database) to which the index belongs.

• INDEX_NAME

The name of the index. If the index is the primary key, the name is always PRIMARY.

• SEQ_IN_INDEX

The column sequence number in the index, starting with 1.

• COLUMN_NAME

The column name. See also the description for the EXPRESSION column.

• COLLATION

How the column is sorted in the index. This can have values A (ascending), D (descending), or NULL (not
sorted).

• CARDINALITY

An estimate of the number of unique values in the index. To update this number, run ANALYZE TABLE
or (for MyISAM tables) myisamchk -a.

CARDINALITY is counted based on statistics stored as integers, so the value is not necessarily exact
even for small tables. The higher the cardinality, the greater the chance that MySQL uses the index
when doing joins.

• SUB_PART

4141

The INFORMATION_SCHEMA TABLES Table

The index prefix. That is, the number of indexed characters if the column is only partly indexed, NULL if
the entire column is indexed.

Note

Prefix limits are measured in bytes. However, prefix lengths for index
specifications in CREATE TABLE, ALTER TABLE, and CREATE INDEX
statements are interpreted as number of characters for nonbinary string types
(CHAR, VARCHAR, TEXT) and number of bytes for binary string types (BINARY,
VARBINARY, BLOB). Take this into account when specifying a prefix length for a
nonbinary string column that uses a multibyte character set.

For additional information about index prefixes, see Section 8.3.4, “Column Indexes”, and
Section 13.1.14, “CREATE INDEX Statement”.

• PACKED

Indicates how the key is packed. NULL if it is not.

• NULLABLE

Contains YES if the column may contain NULL values and '' if not.

• INDEX_TYPE

The index method used (BTREE, FULLTEXT, HASH, RTREE).

• COMMENT

Information about the index not described in its own column, such as disabled if the index is disabled.

• INDEX_COMMENT

Any comment provided for the index with a COMMENT attribute when the index was created.

Notes

• There is no standard INFORMATION_SCHEMA table for indexes. The MySQL column list is similar to

what SQL Server 2000 returns for sp_statistics, except that QUALIFIER and OWNER are replaced
with CATALOG and SCHEMA, respectively.

Information about table indexes is also available from the SHOW INDEX statement. See Section 13.7.5.22,
“SHOW INDEX Statement”. The following statements are equivalent:

SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name

24.3.25 The INFORMATION_SCHEMA TABLES Table

The TABLES table provides information about tables in databases.

The TABLES table has these columns:

4142

The INFORMATION_SCHEMA TABLES Table

Refer to the notes at the end of this section for information regarding other storage engines.

• MAX_DATA_LENGTH

For MyISAM, MAX_DATA_LENGTH is maximum length of the data file. This is the total number of bytes of
data that can be stored in the table, given the data pointer size used.

Unused for InnoDB.

Refer to the notes at the end of this section for information regarding other storage engines.

• INDEX_LENGTH

For MyISAM, INDEX_LENGTH is the length of the index file, in bytes.

For InnoDB, INDEX_LENGTH is the approximate amount of space allocated for non-clustered indexes,
in bytes. Specifically, it is the sum of non-clustered index sizes, in pages, multiplied by the InnoDB page
size.

Refer to the notes at the end of this section for information regarding other storage engines.

• DATA_FREE

The number of allocated but unused bytes.

InnoDB tables report the free space of the tablespace to which the table belongs. For a table located
in the shared tablespace, this is the free space of the shared tablespace. If you are using multiple
tablespaces and the table has its own tablespace, the free space is for only that table. Free space
means the number of bytes in completely free extents minus a safety margin. Even if free space displays
as 0, it may be possible to insert rows as long as new extents need not be allocated.

For NDB Cluster, DATA_FREE shows the space allocated on disk for, but not used by, a Disk Data table
or fragment on disk. (In-memory data resource usage is reported by the DATA_LENGTH column.)

For partitioned tables, this value is only an estimate and may not be absolutely correct. A more accurate
method of obtaining this information in such cases is to query the INFORMATION_SCHEMA PARTITIONS
table, as shown in this example:

SELECT SUM(DATA_FREE)
    FROM  INFORMATION_SCHEMA.PARTITIONS
    WHERE TABLE_SCHEMA = 'mydb'
    AND   TABLE_NAME   = 'mytable';

For more information, see Section 24.3.16, “The INFORMATION_SCHEMA PARTITIONS Table”.

• AUTO_INCREMENT

The next AUTO_INCREMENT value.

• CREATE_TIME

When the table was created.

• UPDATE_TIME

When the data file was last updated. For some storage engines, this value is NULL. For example,
InnoDB stores multiple tables in its system tablespace and the data file timestamp does not apply. Even
with file-per-table mode with each InnoDB table in a separate .ibd file, change buffering can delay the

4144

The INFORMATION_SCHEMA TABLES Table

write to the data file, so the file modification time is different from the time of the last insert, update, or
delete. For MyISAM, the data file timestamp is used; however, on Windows the timestamp is not updated
by updates, so the value is inaccurate.

UPDATE_TIME displays a timestamp value for the last UPDATE, INSERT, or DELETE performed on
InnoDB tables that are not partitioned. For MVCC, the timestamp value reflects the COMMIT time, which
is considered the last update time. Timestamps are not persisted when the server is restarted or when
the table is evicted from the InnoDB data dictionary cache.

The UPDATE_TIME column also shows this information for partitioned InnoDB tables.

• CHECK_TIME

When the table was last checked. Not all storage engines update this time, in which case, the value is
always NULL.

For partitioned InnoDB tables, CHECK_TIME is always NULL.

• TABLE_COLLATION

The table default collation. The output does not explicitly list the table default character set, but the
collation name begins with the character set name.

• CHECKSUM

The live checksum value, if any.

• CREATE_OPTIONS

Extra options used with CREATE TABLE.

CREATE_OPTIONS shows partitioned if the table is partitioned.

CREATE_OPTIONS shows the ENCRYPTION clause specified for tables created in file-per-table
tablespaces.

When creating a table with strict mode disabled, the storage engine's default row format is used if the
specified row format is not supported. The actual row format of the table is reported in the ROW_FORMAT
column. CREATE_OPTIONS shows the row format that was specified in the CREATE TABLE statement.

When altering the storage engine of a table, table options that are not applicable to the new storage
engine are retained in the table definition to enable reverting the table with its previously defined options
to the original storage engine, if necessary. The CREATE_OPTIONS column may show retained options.

• TABLE_COMMENT

The comment used when creating the table (or information as to why MySQL could not access the table
information).

Notes

• For NDB tables, the output of this statement shows appropriate values for the AVG_ROW_LENGTH and

DATA_LENGTH columns, with the exception that BLOB columns are not taken into account.

• For NDB tables, DATA_LENGTH includes data stored in main memory only; the MAX_DATA_LENGTH and

DATA_FREE columns apply to Disk Data.

4145

The INFORMATION_SCHEMA TABLESPACES Table

• For NDB Cluster Disk Data tables, MAX_DATA_LENGTH shows the space allocated for the disk part of a

Disk Data table or fragment. (In-memory data resource usage is reported by the DATA_LENGTH column.)

• For MEMORY tables, the DATA_LENGTH, MAX_DATA_LENGTH, and INDEX_LENGTH values approximate
the actual amount of allocated memory. The allocation algorithm reserves memory in large amounts to
reduce the number of allocation operations.

• For views, all TABLES columns are NULL except that TABLE_NAME indicates the view name and

TABLE_COMMENT says VIEW.

Table information is also available from the SHOW TABLE STATUS and SHOW TABLES statements.
See Section 13.7.5.36, “SHOW TABLE STATUS Statement”, and Section 13.7.5.37, “SHOW TABLES
Statement”. The following statements are equivalent:

SELECT
    TABLE_NAME, ENGINE, VERSION, ROW_FORMAT, TABLE_ROWS, AVG_ROW_LENGTH,
    DATA_LENGTH, MAX_DATA_LENGTH, INDEX_LENGTH, DATA_FREE, AUTO_INCREMENT,
    CREATE_TIME, UPDATE_TIME, CHECK_TIME, TABLE_COLLATION, CHECKSUM,
    CREATE_OPTIONS, TABLE_COMMENT
  FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLE STATUS
  FROM db_name
  [LIKE 'wild']

The following statements are equivalent:

SELECT
  TABLE_NAME, TABLE_TYPE
  FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW FULL TABLES
  FROM db_name
  [LIKE 'wild']

24.3.26 The INFORMATION_SCHEMA TABLESPACES Table

This table is unused. Other INFORMATION_SCHEMA tables may provide related information:

• For NDB, the INFORMATION_SCHEMA FILES table provides tablespace-related information.

• For InnoDB, the INFORMATION_SCHEMA INNODB_SYS_TABLESPACES and INNODB_SYS_DATAFILES

tables provide tablespace metadata.

24.3.27 The INFORMATION_SCHEMA TABLE_CONSTRAINTS Table

The TABLE_CONSTRAINTS table describes which tables have constraints.

The TABLE_CONSTRAINTS table has these columns:

• CONSTRAINT_CATALOG

The name of the catalog to which the constraint belongs. This value is always def.

• CONSTRAINT_SCHEMA

The name of the schema (database) to which the constraint belongs.

4146

The INFORMATION_SCHEMA TABLE_PRIVILEGES Table

• CONSTRAINT_NAME

The name of the constraint.

• TABLE_SCHEMA

The name of the schema (database) to which the table belongs.

• TABLE_NAME

The name of the table.

• CONSTRAINT_TYPE

The type of constraint. The value can be UNIQUE, PRIMARY KEY, FOREIGN KEY, or CHECK. This is a
CHAR (not ENUM) column. The CHECK value is not available until MySQL supports CHECK.

The UNIQUE and PRIMARY KEY information is about the same as what you get from the Key_name
column in the output from SHOW INDEX when the Non_unique column is 0.

24.3.28 The INFORMATION_SCHEMA TABLE_PRIVILEGES Table

The TABLE_PRIVILEGES table provides information about table privileges. It takes its values from the
mysql.tables_priv system table.

The TABLE_PRIVILEGES table has these columns:

• GRANTEE

The name of the account to which the privilege is granted, in 'user_name'@'host_name' format.

• TABLE_CATALOG

The name of the catalog to which the table belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema (database) to which the table belongs.

• TABLE_NAME

The name of the table.

• PRIVILEGE_TYPE

The privilege granted. The value can be any privilege that can be granted at the table level; see
Section 13.7.1.4, “GRANT Statement”. Each row lists a single privilege, so there is one row per table
privilege held by the grantee.

• IS_GRANTABLE

YES if the user has the GRANT OPTION privilege, NO otherwise. The output does not list GRANT OPTION
as a separate row with PRIVILEGE_TYPE='GRANT OPTION'.

Notes

• TABLE_PRIVILEGES is a nonstandard INFORMATION_SCHEMA table.

The following statements are not equivalent:

4147

The INFORMATION_SCHEMA TRIGGERS Table

SELECT ... FROM INFORMATION_SCHEMA.TABLE_PRIVILEGES

SHOW GRANTS ...

24.3.29 The INFORMATION_SCHEMA TRIGGERS Table

The TRIGGERS table provides information about triggers. To see information about a table's triggers, you
must have the TRIGGER privilege for the table.

The TRIGGERS table has these columns:

• TRIGGER_CATALOG

The name of the catalog to which the trigger belongs. This value is always def.

• TRIGGER_SCHEMA

The name of the schema (database) to which the trigger belongs.

• TRIGGER_NAME

The name of the trigger.

• EVENT_MANIPULATION

The trigger event. This is the type of operation on the associated table for which the trigger activates.
The value is INSERT (a row was inserted), DELETE (a row was deleted), or UPDATE (a row was
modified).

• EVENT_OBJECT_CATALOG, EVENT_OBJECT_SCHEMA, and EVENT_OBJECT_TABLE

As noted in Section 23.3, “Using Triggers”, every trigger is associated with exactly one table. These
columns indicate the catalog and schema (database) in which this table occurs, and the table name,
respectively. The EVENT_OBJECT_CATALOG value is always def.

• ACTION_ORDER

The ordinal position of the trigger's action within the list of triggers on the same table with the same
EVENT_MANIPULATION and ACTION_TIMING values.

• ACTION_CONDITION

This value is always NULL.

• ACTION_STATEMENT

The trigger body; that is, the statement executed when the trigger activates. This text uses UTF-8
encoding.

• ACTION_ORIENTATION

This value is always ROW.

• ACTION_TIMING

Whether the trigger activates before or after the triggering event. The value is BEFORE or AFTER.

• ACTION_REFERENCE_OLD_TABLE

This value is always NULL.

4148

The INFORMATION_SCHEMA TRIGGERS Table

• ACTION_REFERENCE_NEW_TABLE

This value is always NULL.

• ACTION_REFERENCE_OLD_ROW and ACTION_REFERENCE_NEW_ROW

The old and new column identifiers, respectively. The ACTION_REFERENCE_OLD_ROW value is always
OLD and the ACTION_REFERENCE_NEW_ROW value is always NEW.

• CREATED

The date and time when the trigger was created. This is a TIMESTAMP(2) value (with a fractional part
in hundredths of seconds) for triggers created in MySQL 5.7.2 or later, NULL for triggers created prior to
5.7.2.

• SQL_MODE

The SQL mode in effect when the trigger was created, and under which the trigger executes. For the
permitted values, see Section 5.1.10, “Server SQL Modes”.

• DEFINER

The account named in the DEFINER clause (often the user who created the trigger), in
'user_name'@'host_name' format.

• CHARACTER_SET_CLIENT

The session value of the character_set_client system variable when the trigger was created.

• COLLATION_CONNECTION

The session value of the collation_connection system variable when the trigger was created.

• DATABASE_COLLATION

The collation of the database with which the trigger is associated.

Example

The following example uses the ins_sum trigger defined in Section 23.3, “Using Triggers”:

mysql> SELECT * FROM INFORMATION_SCHEMA.TRIGGERS
       WHERE TRIGGER_SCHEMA='test' AND TRIGGER_NAME='ins_sum'\G
*************************** 1. row ***************************
           TRIGGER_CATALOG: def
            TRIGGER_SCHEMA: test
              TRIGGER_NAME: ins_sum
        EVENT_MANIPULATION: INSERT
      EVENT_OBJECT_CATALOG: def
       EVENT_OBJECT_SCHEMA: test
        EVENT_OBJECT_TABLE: account
              ACTION_ORDER: 1
          ACTION_CONDITION: NULL
          ACTION_STATEMENT: SET @sum = @sum + NEW.amount
        ACTION_ORIENTATION: ROW
             ACTION_TIMING: BEFORE
ACTION_REFERENCE_OLD_TABLE: NULL
ACTION_REFERENCE_NEW_TABLE: NULL
  ACTION_REFERENCE_OLD_ROW: OLD
  ACTION_REFERENCE_NEW_ROW: NEW
                   CREATED: 2018-08-08 10:10:12.61
                  SQL_MODE: ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,

4149

The INFORMATION_SCHEMA USER_PRIVILEGES Table

                            NO_ZERO_IN_DATE,NO_ZERO_DATE,
                            ERROR_FOR_DIVISION_BY_ZERO,
                            NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
                   DEFINER: me@localhost
      CHARACTER_SET_CLIENT: utf8
      COLLATION_CONNECTION: utf8_general_ci
        DATABASE_COLLATION: latin1_swedish_ci

Trigger information is also available from the SHOW TRIGGERS statement. See Section 13.7.5.38, “SHOW
TRIGGERS Statement”.

24.3.30 The INFORMATION_SCHEMA USER_PRIVILEGES Table

The USER_PRIVILEGES table provides information about global privileges. It takes its values from the
mysql.user system table.

The USER_PRIVILEGES table has these columns:

• GRANTEE

The name of the account to which the privilege is granted, in 'user_name'@'host_name' format.

• TABLE_CATALOG

The name of the catalog. This value is always def.

• PRIVILEGE_TYPE

The privilege granted. The value can be any privilege that can be granted at the global level; see
Section 13.7.1.4, “GRANT Statement”. Each row lists a single privilege, so there is one row per global
privilege held by the grantee.

• IS_GRANTABLE

YES if the user has the GRANT OPTION privilege, NO otherwise. The output does not list GRANT OPTION
as a separate row with PRIVILEGE_TYPE='GRANT OPTION'.

Notes

• USER_PRIVILEGES is a nonstandard INFORMATION_SCHEMA table.

The following statements are not equivalent:

SELECT ... FROM INFORMATION_SCHEMA.USER_PRIVILEGES

SHOW GRANTS ...

24.3.31 The INFORMATION_SCHEMA VIEWS Table

The VIEWS table provides information about views in databases. You must have the SHOW VIEW privilege
to access this table.

The VIEWS table has these columns:

• TABLE_CATALOG

The name of the catalog to which the view belongs. This value is always def.

• TABLE_SCHEMA

The name of the schema (database) to which the view belongs.

4150

The INFORMATION_SCHEMA VIEWS Table

• TABLE_NAME

The name of the view.

• VIEW_DEFINITION

The SELECT statement that provides the definition of the view. This column has most of what you see
in the Create Table column that SHOW CREATE VIEW produces. Skip the words before SELECT and
skip the words WITH CHECK OPTION. Suppose that the original statement was:

CREATE VIEW v AS
  SELECT s2,s1 FROM t
  WHERE s1 > 5
  ORDER BY s1
  WITH CHECK OPTION;

Then the view definition looks like this:

SELECT s2,s1 FROM t WHERE s1 > 5 ORDER BY s1

• CHECK_OPTION

The value of the CHECK_OPTION attribute. The value is one of NONE, CASCADE, or LOCAL.

• IS_UPDATABLE

MySQL sets a flag, called the view updatability flag, at CREATE VIEW time. The flag is set to YES (true)
if UPDATE and DELETE (and similar operations) are legal for the view. Otherwise, the flag is set to NO
(false). The IS_UPDATABLE column in the VIEWS table displays the status of this flag.

If a view is not updatable, statements such UPDATE, DELETE, and INSERT are illegal and are rejected.
(Even if a view is updatable, it might not be possible to insert into it; for details, refer to Section 23.5.3,
“Updatable and Insertable Views”.)

The IS_UPDATABLE flag may be unreliable if a view depends on one or more other views, and one of
these underlying views is updated. Regardless of the IS_UPDATABLE value, the server keeps track of
the updatability of a view and correctly rejects data change operations to views that are not updatable. If
the IS_UPDATABLE value for a view has become inaccurate to due to changes to underlying views, the
value can be updated by deleting and re-creating the view.

• DEFINER

The account of the user who created the view, in 'user_name'@'host_name' format.

• SECURITY_TYPE

The view SQL SECURITY characteristic. The value is one of DEFINER or INVOKER.

• CHARACTER_SET_CLIENT

The session value of the character_set_client system variable when the view was created.

• COLLATION_CONNECTION

The session value of the collation_connection system variable when the view was created.

Notes

MySQL permits different sql_mode settings to tell the server the type of SQL syntax to support. For
example, you might use the ANSI SQL mode to ensure MySQL correctly interprets the standard SQL

4151

INFORMATION_SCHEMA InnoDB Table Reference

Table Name

INNODB_CMP_RESET

INNODB_CMPMEM

INNODB_CMPMEM_RESET

INNODB_FT_BEING_DELETED

INNODB_FT_CONFIG

Description

Deprecated

Status for operations related to
compressed InnoDB tables

Status for compressed pages
within InnoDB buffer pool

Status for compressed pages
within InnoDB buffer pool

Snapshot of
INNODB_FT_DELETED table

Metadata for InnoDB table
FULLTEXT index and associated
processing

INNODB_FT_DEFAULT_STOPWORD Default list of stopwords for
InnoDB FULLTEXT indexes

INNODB_FT_DELETED

INNODB_FT_INDEX_CACHE

INNODB_FT_INDEX_TABLE

INNODB_LOCK_WAITS

INNODB_LOCKS

Rows deleted from InnoDB table
FULLTEXT index

Token information for newly
inserted rows in InnoDB
FULLTEXT index

Inverted index information for
processing text searches against
InnoDB table FULLTEXT index

InnoDB transaction lock-wait
information

InnoDB transaction lock
information

5.7.14

5.7.14

INNODB_METRICS

InnoDB performance information

INNODB_SYS_COLUMNS

Columns in each InnoDB table

INNODB_SYS_DATAFILES

Data file path information for
InnoDB file-per-table and general
tablespaces

INNODB_SYS_FIELDS

Key columns of InnoDB indexes

INNODB_SYS_FOREIGN

InnoDB foreign-key metadata

INNODB_SYS_FOREIGN_COLS

InnoDB foreign-key column status
information

INNODB_SYS_INDEXES

InnoDB index metadata

INNODB_SYS_TABLES

InnoDB table metadata

INNODB_SYS_TABLESPACES

INNODB_SYS_TABLESTATS

INNODB_SYS_VIRTUAL

INNODB_TEMP_TABLE_INFO

InnoDB file-per-table, general, and
undo tablespace metadata

InnoDB table low-level status
information

InnoDB virtual generated column
metadata

Information about active user-
created InnoDB temporary tables

4153

The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table

Table Name

INNODB_TRX

Description

Deprecated

Active InnoDB transaction
information

24.4.2 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table

The INNODB_BUFFER_PAGE table provides information about each page in the InnoDB buffer pool.

For related usage information and examples, see Section 14.16.5, “InnoDB INFORMATION_SCHEMA
Buffer Pool Tables”.

Warning

Querying the INNODB_BUFFER_PAGE table can affect performance. Do not query
this table on a production system unless you are aware of the performance impact
and have determined it to be acceptable. To avoid impacting performance on a
production system, reproduce the issue you want to investigate and query buffer
pool statistics on a test instance.

The INNODB_BUFFER_PAGE table has these columns:

• POOL_ID

The buffer pool ID. This is an identifier to distinguish between multiple buffer pool instances.

• BLOCK_ID

The buffer pool block ID.

• SPACE

The tablespace ID; the same value as INNODB_SYS_TABLES.SPACE.

• PAGE_NUMBER

The page number.

• PAGE_TYPE

The page type. The following table shows the permitted values.

Table 24.4 INNODB_BUFFER_PAGE.PAGE_TYPE Values

Page Type

ALLOCATED

BLOB

COMPRESSED_BLOB2

COMPRESSED_BLOB

EXTENT_DESCRIPTOR

FILE_SPACE_HEADER

IBUF_BITMAP

IBUF_FREE_LIST

4154

Description

Freshly allocated page

Uncompressed BLOB page

Subsequent comp BLOB page

First compressed BLOB page

Extent descriptor page

File space header

Insert buffer bitmap

Insert buffer free list

The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table

Page Type

IBUF_INDEX

INDEX

INODE

RTREE_INDEX

SYSTEM

TRX_SYSTEM

UNDO_LOG

UNKNOWN

• FLUSH_TYPE

The flush type.

• FIX_COUNT

Description

Insert buffer index

B-tree node

Index node

R-tree index

System page

Transaction system data

Undo log page

Unknown

The number of threads using this block within the buffer pool. When zero, the block is eligible to be
evicted.

• IS_HASHED

Whether a hash index has been built on this page.

• NEWEST_MODIFICATION

The Log Sequence Number of the youngest modification.

• OLDEST_MODIFICATION

The Log Sequence Number of the oldest modification.

• ACCESS_TIME

An abstract number used to judge the first access time of the page.

• TABLE_NAME

The name of the table the page belongs to. This column is applicable only to pages with a PAGE_TYPE
value of INDEX.

• INDEX_NAME

The name of the index the page belongs to. This can be the name of a clustered index or a secondary
index. This column is applicable only to pages with a PAGE_TYPE value of INDEX.

• NUMBER_RECORDS

The number of records within the page.

• DATA_SIZE

The sum of the sizes of the records. This column is applicable only to pages with a PAGE_TYPE value of
INDEX.

• COMPRESSED_SIZE

4155

The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table

The compressed page size. NULL for pages that are not compressed.

• PAGE_STATE

The page state. The following table shows the permitted values.

Table 24.5 INNODB_BUFFER_PAGE.PAGE_STATE Values

Page State

FILE_PAGE

MEMORY

NOT_USED

NULL

READY_FOR_USE

REMOVE_HASH

• IO_FIX

Description

A buffered file page

Contains a main memory object

In the free list

Clean compressed pages, compressed pages
in the flush list, pages used as buffer pool watch
sentinels

A free page

Hash index should be removed before placing in
the free list

Whether any I/O is pending for this page: IO_NONE = no pending I/O, IO_READ = read pending,
IO_WRITE = write pending.

• IS_OLD

Whether the block is in the sublist of old blocks in the LRU list.

• FREE_PAGE_CLOCK

The value of the freed_page_clock counter when the block was the last placed at the head of the
LRU list. The freed_page_clock counter tracks the number of blocks removed from the end of the
LRU list.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE LIMIT 1\G
*************************** 1. row ***************************
            POOL_ID: 0
           BLOCK_ID: 0
              SPACE: 97
        PAGE_NUMBER: 2473
          PAGE_TYPE: INDEX
         FLUSH_TYPE: 1
          FIX_COUNT: 0
          IS_HASHED: YES
NEWEST_MODIFICATION: 733855581
OLDEST_MODIFICATION: 0
        ACCESS_TIME: 3378385672
         TABLE_NAME: `employees`.`salaries`
         INDEX_NAME: PRIMARY
     NUMBER_RECORDS: 468
          DATA_SIZE: 14976
    COMPRESSED_SIZE: 0
         PAGE_STATE: FILE_PAGE
             IO_FIX: IO_NONE
             IS_OLD: YES

4156

The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table

    FREE_PAGE_CLOCK: 66

Notes

• This table is useful primarily for expert-level performance monitoring, or when developing performance-

related extensions for MySQL.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• When tables, table rows, partitions, or indexes are deleted, associated pages remain in the buffer pool

until space is required for other data. The INNODB_BUFFER_PAGE table reports information about these
pages until they are evicted from the buffer pool. For more information about how the InnoDB manages
buffer pool data, see Section 14.5.1, “Buffer Pool”.

24.4.3 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table

The INNODB_BUFFER_PAGE_LRU table provides information about the pages in the InnoDB buffer pool;
in particular, how they are ordered in the LRU list that determines which pages to evict from the buffer pool
when it becomes full.

The INNODB_BUFFER_PAGE_LRU table has the same columns as the INNODB_BUFFER_PAGE table,
except that the INNODB_BUFFER_PAGE_LRU table has LRU_POSITION and COMPRESSED columns
instead of BLOCK_ID and PAGE_STATE columns.

For related usage information and examples, see Section 14.16.5, “InnoDB INFORMATION_SCHEMA
Buffer Pool Tables”.

Warning

Querying the INNODB_BUFFER_PAGE_LRU table can affect performance. Do not
query this table on a production system unless you are aware of the performance
impact and have determined it to be acceptable. To avoid impacting performance
on a production system, reproduce the issue you want to investigate and query
buffer pool statistics on a test instance.

The INNODB_BUFFER_PAGE_LRU table has these columns:

• POOL_ID

The buffer pool ID. This is an identifier to distinguish between multiple buffer pool instances.

• LRU_POSITION

The position of the page in the LRU list.

• SPACE

The tablespace ID; the same value as INNODB_SYS_TABLES.SPACE.

• PAGE_NUMBER

The page number.

• PAGE_TYPE

The page type. The following table shows the permitted values.

4157

The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table

Table 24.6 INNODB_BUFFER_PAGE_LRU.PAGE_TYPE Values

Page Type

ALLOCATED

BLOB

COMPRESSED_BLOB2

COMPRESSED_BLOB

EXTENT_DESCRIPTOR

FILE_SPACE_HEADER

IBUF_BITMAP

IBUF_FREE_LIST

IBUF_INDEX

INDEX

INODE

RTREE_INDEX

SYSTEM

TRX_SYSTEM

UNDO_LOG

UNKNOWN

• FLUSH_TYPE

The flush type.

• FIX_COUNT

Description

Freshly allocated page

Uncompressed BLOB page

Subsequent comp BLOB page

First compressed BLOB page

Extent descriptor page

File space header

Insert buffer bitmap

Insert buffer free list

Insert buffer index

B-tree node

Index node

R-tree index

System page

Transaction system data

Undo log page

Unknown

The number of threads using this block within the buffer pool. When zero, the block is eligible to be
evicted.

• IS_HASHED

Whether a hash index has been built on this page.

• NEWEST_MODIFICATION

The Log Sequence Number of the youngest modification.

• OLDEST_MODIFICATION

The Log Sequence Number of the oldest modification.

• ACCESS_TIME

An abstract number used to judge the first access time of the page.

• TABLE_NAME

The name of the table the page belongs to. This column is applicable only to pages with a PAGE_TYPE
value of INDEX.

• INDEX_NAME

4158

The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table

The name of the index the page belongs to. This can be the name of a clustered index or a secondary
index. This column is applicable only to pages with a PAGE_TYPE value of INDEX.

• NUMBER_RECORDS

The number of records within the page.

• DATA_SIZE

The sum of the sizes of the records. This column is applicable only to pages with a PAGE_TYPE value of
INDEX.

• COMPRESSED_SIZE

The compressed page size. NULL for pages that are not compressed.

• COMPRESSED

Whether the page is compressed.

• IO_FIX

Whether any I/O is pending for this page: IO_NONE = no pending I/O, IO_READ = read pending,
IO_WRITE = write pending.

• IS_OLD

Whether the block is in the sublist of old blocks in the LRU list.

• FREE_PAGE_CLOCK

The value of the freed_page_clock counter when the block was the last placed at the head of the
LRU list. The freed_page_clock counter tracks the number of blocks removed from the end of the
LRU list.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU LIMIT 1\G
*************************** 1. row ***************************
            POOL_ID: 0
       LRU_POSITION: 0
              SPACE: 97
        PAGE_NUMBER: 1984
          PAGE_TYPE: INDEX
         FLUSH_TYPE: 1
          FIX_COUNT: 0
          IS_HASHED: YES
NEWEST_MODIFICATION: 719490396
OLDEST_MODIFICATION: 0
        ACCESS_TIME: 3378383796
         TABLE_NAME: `employees`.`salaries`
         INDEX_NAME: PRIMARY
     NUMBER_RECORDS: 468
          DATA_SIZE: 14976
    COMPRESSED_SIZE: 0
         COMPRESSED: NO
             IO_FIX: IO_NONE
             IS_OLD: YES
    FREE_PAGE_CLOCK: 0

4159

The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table

Notes

• This table is useful primarily for expert-level performance monitoring, or when developing performance-

related extensions for MySQL.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• Querying this table can require MySQL to allocate a large block of contiguous memory, more than 64

bytes times the number of active pages in the buffer pool. This allocation could potentially cause an out-
of-memory error, especially for systems with multi-gigabyte buffer pools.

• Querying this table requires MySQL to lock the data structure representing the buffer pool while

traversing the LRU list, which can reduce concurrency, especially for systems with multi-gigabyte buffer
pools.

• When tables, table rows, partitions, or indexes are deleted, associated pages remain in the buffer pool
until space is required for other data. The INNODB_BUFFER_PAGE_LRU table reports information about
these pages until they are evicted from the buffer pool. For more information about how the InnoDB
manages buffer pool data, see Section 14.5.1, “Buffer Pool”.

24.4.4 The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table

The INNODB_BUFFER_POOL_STATS table provides much of the same buffer pool information provided
in SHOW ENGINE INNODB STATUS output. Much of the same information may also be obtained using
InnoDB buffer pool server status variables.

The idea of making pages in the buffer pool “young” or “not young” refers to transferring them between the
sublists at the head and tail of the buffer pool data structure. Pages made “young” take longer to age out of
the buffer pool, while pages made “not young” are moved much closer to the point of eviction.

For related usage information and examples, see Section 14.16.5, “InnoDB INFORMATION_SCHEMA
Buffer Pool Tables”.

The INNODB_BUFFER_POOL_STATS table has these columns:

• POOL_ID

The buffer pool ID. This is an identifier to distinguish between multiple buffer pool instances.

• POOL_SIZE

The InnoDB buffer pool size in pages.

• FREE_BUFFERS

The number of free pages in the InnoDB buffer pool.

• DATABASE_PAGES

The number of pages in the InnoDB buffer pool containing data. This number includes both dirty and
clean pages.

• OLD_DATABASE_PAGES

The number of pages in the old buffer pool sublist.

4160

The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table

• MODIFIED_DATABASE_PAGES

The number of modified (dirty) database pages.

• PENDING_DECOMPRESS

The number of pages pending decompression.

• PENDING_READS

The number of pending reads.

• PENDING_FLUSH_LRU

The number of pages pending flush in the LRU.

• PENDING_FLUSH_LIST

The number of pages pending flush in the flush list.

• PAGES_MADE_YOUNG

The number of pages made young.

• PAGES_NOT_MADE_YOUNG

The number of pages not made young.

• PAGES_MADE_YOUNG_RATE

The number of pages made young per second (pages made young since the last printout / time
elapsed).

• PAGES_MADE_NOT_YOUNG_RATE

The number of pages not made per second (pages not made young since the last printout / time
elapsed).

• NUMBER_PAGES_READ

The number of pages read.

• NUMBER_PAGES_CREATED

The number of pages created.

• NUMBER_PAGES_WRITTEN

The number of pages written.

• PAGES_READ_RATE

The number of pages read per second (pages read since the last printout / time elapsed).

• PAGES_CREATE_RATE

The number of pages created per second (pages created since the last printout / time elapsed).

• PAGES_WRITTEN_RATE

The number of pages written per second (pages written since the last printout / time elapsed).

4161

The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table

• NUMBER_PAGES_GET

The number of logical read requests.

• HIT_RATE

The buffer pool hit rate.

• YOUNG_MAKE_PER_THOUSAND_GETS

The number of pages made young per thousand gets.

• NOT_YOUNG_MAKE_PER_THOUSAND_GETS

The number of pages not made young per thousand gets.

• NUMBER_PAGES_READ_AHEAD

The number of pages read ahead.

• NUMBER_READ_AHEAD_EVICTED

The number of pages read into the InnoDB buffer pool by the read-ahead background thread that were
subsequently evicted without having been accessed by queries.

• READ_AHEAD_RATE

The read-ahead rate per second (pages read ahead since the last printout / time elapsed).

• READ_AHEAD_EVICTED_RATE

The number of read-ahead pages evicted without access per second (read-ahead pages not accessed
since the last printout / time elapsed).

• LRU_IO_TOTAL

Total LRU I/O.

• LRU_IO_CURRENT

LRU I/O for the current interval.

• UNCOMPRESS_TOTAL

The total number of pages decompressed.

• UNCOMPRESS_CURRENT

The number of pages decompressed in the current interval.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_POOL_STATS\G
*************************** 1. row ***************************
                         POOL_ID: 0
                       POOL_SIZE: 8192
                    FREE_BUFFERS: 1
                  DATABASE_PAGES: 8085
              OLD_DATABASE_PAGES: 2964
         MODIFIED_DATABASE_PAGES: 0
              PENDING_DECOMPRESS: 0
                   PENDING_READS: 0

4162

The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables

               PENDING_FLUSH_LRU: 0
              PENDING_FLUSH_LIST: 0
                PAGES_MADE_YOUNG: 22821
            PAGES_NOT_MADE_YOUNG: 3544303
           PAGES_MADE_YOUNG_RATE: 357.62602199870594
       PAGES_MADE_NOT_YOUNG_RATE: 0
               NUMBER_PAGES_READ: 2389
            NUMBER_PAGES_CREATED: 12385
            NUMBER_PAGES_WRITTEN: 13111
                 PAGES_READ_RATE: 0
               PAGES_CREATE_RATE: 0
              PAGES_WRITTEN_RATE: 0
                NUMBER_PAGES_GET: 33322210
                        HIT_RATE: 1000
    YOUNG_MAKE_PER_THOUSAND_GETS: 18
NOT_YOUNG_MAKE_PER_THOUSAND_GETS: 0
         NUMBER_PAGES_READ_AHEAD: 2024
       NUMBER_READ_AHEAD_EVICTED: 0
                 READ_AHEAD_RATE: 0
         READ_AHEAD_EVICTED_RATE: 0
                    LRU_IO_TOTAL: 0
                  LRU_IO_CURRENT: 0
                UNCOMPRESS_TOTAL: 0
              UNCOMPRESS_CURRENT: 0

Notes

• This table is useful primarily for expert-level performance monitoring, or when developing performance-

related extensions for MySQL.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.5 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET
Tables

The INNODB_CMP and INNODB_CMP_RESET tables provide status information on operations related to
compressed InnoDB tables.

The INNODB_CMP and INNODB_CMP_RESET tables have these columns:

• PAGE_SIZE

The compressed page size in bytes.

• COMPRESS_OPS

The number of times a B-tree page of size PAGE_SIZE has been compressed. Pages are compressed
whenever an empty page is created or the space for the uncompressed modification log runs out.

• COMPRESS_OPS_OK

The number of times a B-tree page of size PAGE_SIZE has been successfully compressed. This count
should never exceed COMPRESS_OPS.

• COMPRESS_TIME

The total time in seconds used for attempts to compress B-tree pages of size PAGE_SIZE.

• UNCOMPRESS_OPS

4163

The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables

The number of times a B-tree page of size PAGE_SIZE has been uncompressed. B-tree pages are
uncompressed whenever compression fails or at first access when the uncompressed page does not
exist in the buffer pool.

• UNCOMPRESS_TIME

The total time in seconds used for uncompressing B-tree pages of the size PAGE_SIZE.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_CMP\G
*************************** 1. row ***************************
      page_size: 1024
   compress_ops: 0
compress_ops_ok: 0
  compress_time: 0
 uncompress_ops: 0
uncompress_time: 0
*************************** 2. row ***************************
      page_size: 2048
   compress_ops: 0
compress_ops_ok: 0
  compress_time: 0
 uncompress_ops: 0
uncompress_time: 0
*************************** 3. row ***************************
      page_size: 4096
   compress_ops: 0
compress_ops_ok: 0
  compress_time: 0
 uncompress_ops: 0
uncompress_time: 0
*************************** 4. row ***************************
      page_size: 8192
   compress_ops: 86955
compress_ops_ok: 81182
  compress_time: 27
 uncompress_ops: 26828
uncompress_time: 5
*************************** 5. row ***************************
      page_size: 16384
   compress_ops: 0
compress_ops_ok: 0
  compress_time: 0
 uncompress_ops: 0
uncompress_time: 0

Notes

• Use these tables to measure the effectiveness of InnoDB table compression in your database.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For usage information, see Section 14.9.1.4, “Monitoring InnoDB Table Compression at Runtime” and

Section 14.16.1.3, “Using the Compression Information Schema Tables”. For general information about
InnoDB table compression, see Section 14.9, “InnoDB Table and Page Compression”.

24.4.6 The INFORMATION_SCHEMA INNODB_CMPMEM and
INNODB_CMPMEM_RESET Tables

4164

The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables

The INNODB_CMPMEM and INNODB_CMPMEM_RESET tables provide status information on compressed
pages within the InnoDB buffer pool.

The INNODB_CMPMEM and INNODB_CMPMEM_RESET tables have these columns:

• PAGE_SIZE

The block size in bytes. Each record of this table describes blocks of this size.

• BUFFER_POOL_INSTANCE

A unique identifier for the buffer pool instance.

• PAGES_USED

The number of blocks of size PAGE_SIZE that are currently in use.

• PAGES_FREE

The number of blocks of size PAGE_SIZE that are currently available for allocation. This column shows
the external fragmentation in the memory pool. Ideally, these numbers should be at most 1.

• RELOCATION_OPS

The number of times a block of size PAGE_SIZE has been relocated. The buddy system can relocate the
allocated “buddy neighbor” of a freed block when it tries to form a bigger freed block. Reading from the
INNODB_CMPMEM_RESET table resets this count.

• RELOCATION_TIME

The total time in microseconds used for relocating blocks of size PAGE_SIZE. Reading from the table
INNODB_CMPMEM_RESET resets this count.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_CMPMEM\G
*************************** 1. row ***************************
           page_size: 1024
buffer_pool_instance: 0
          pages_used: 0
          pages_free: 0
      relocation_ops: 0
     relocation_time: 0
*************************** 2. row ***************************
           page_size: 2048
buffer_pool_instance: 0
          pages_used: 0
          pages_free: 0
      relocation_ops: 0
     relocation_time: 0
*************************** 3. row ***************************
           page_size: 4096
buffer_pool_instance: 0
          pages_used: 0
          pages_free: 0
      relocation_ops: 0
     relocation_time: 0
*************************** 4. row ***************************
           page_size: 8192
buffer_pool_instance: 0
          pages_used: 7673
          pages_free: 15

4165

The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET Tables

      relocation_ops: 4638
     relocation_time: 0
*************************** 5. row ***************************
           page_size: 16384
buffer_pool_instance: 0
          pages_used: 0
          pages_free: 0
      relocation_ops: 0
     relocation_time: 0

Notes

• Use these tables to measure the effectiveness of InnoDB table compression in your database.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For usage information, see Section 14.9.1.4, “Monitoring InnoDB Table Compression at Runtime” and

Section 14.16.1.3, “Using the Compression Information Schema Tables”. For general information about
InnoDB table compression, see Section 14.9, “InnoDB Table and Page Compression”.

24.4.7 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and
INNODB_CMP_PER_INDEX_RESET Tables

The INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET tables provide status information
on operations related to compressed InnoDB tables and indexes, with separate statistics for each
combination of database, table, and index, to help you evaluate the performance and usefulness of
compression for specific tables.

For a compressed InnoDB table, both the table data and all the secondary indexes are compressed. In
this context, the table data is treated as just another index, one that happens to contain all the columns: the
clustered index.

The INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET tables have these columns:

• DATABASE_NAME

The schema (database) containing the applicable table.

• TABLE_NAME

The table to monitor for compression statistics.

• INDEX_NAME

The index to monitor for compression statistics.

• COMPRESS_OPS

The number of compression operations attempted. Pages are compressed whenever an empty page is
created or the space for the uncompressed modification log runs out.

• COMPRESS_OPS_OK

The number of successful compression operations. Subtract from the COMPRESS_OPS value to get
the number of compression failures. Divide by the COMPRESS_OPS value to get the percentage of
compression failures.

4166

The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table

• COMPRESS_TIME

The total time in seconds used for compressing data in this index.

• UNCOMPRESS_OPS

The number of uncompression operations performed. Compressed InnoDB pages are uncompressed
whenever compression fails, or the first time a compressed page is accessed in the buffer pool and the
uncompressed page does not exist.

• UNCOMPRESS_TIME

The total time in seconds used for uncompressing data in this index.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_CMP_PER_INDEX\G
*************************** 1. row ***************************
  database_name: employees
     table_name: salaries
     index_name: PRIMARY
   compress_ops: 0
compress_ops_ok: 0
  compress_time: 0
 uncompress_ops: 23451
uncompress_time: 4
*************************** 2. row ***************************
  database_name: employees
     table_name: salaries
     index_name: emp_no
   compress_ops: 0
compress_ops_ok: 0
  compress_time: 0
 uncompress_ops: 1597
uncompress_time: 0

Notes

• Use these tables to measure the effectiveness of InnoDB table compression for specific tables, indexes,

or both.

• You must have the PROCESS privilege to query these tables.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of these tables, including data types and default values.

• Because collecting separate measurements for every index imposes substantial performance overhead,

INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET statistics are not gathered by
default. You must enable the innodb_cmp_per_index_enabled system variable before performing
the operations on compressed tables that you want to monitor.

• For usage information, see Section 14.9.1.4, “Monitoring InnoDB Table Compression at Runtime” and

Section 14.16.1.3, “Using the Compression Information Schema Tables”. For general information about
InnoDB table compression, see Section 14.9, “InnoDB Table and Page Compression”.

24.4.8 The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table

The INNODB_FT_BEING_DELETED table provides a snapshot of the INNODB_FT_DELETED table;
it is used only during an OPTIMIZE TABLE maintenance operation. When OPTIMIZE TABLE is
run, the INNODB_FT_BEING_DELETED table is emptied, and DOC_ID values are removed from the

4167

The INFORMATION_SCHEMA INNODB_FT_CONFIG Table

INNODB_FT_DELETED table. Because the contents of INNODB_FT_BEING_DELETED typically have
a short lifetime, this table has limited utility for monitoring or debugging. For information about running
OPTIMIZE TABLE on tables with FULLTEXT indexes, see Section 12.9.6, “Fine-Tuning MySQL Full-Text
Search”.

This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system
variable to the name (including the database name) of the table that contains the FULLTEXT
index; for example test/articles. The output appears similar to the example provided for the
INNODB_FT_DELETED table.

For related usage information and examples, see Section 14.16.4, “InnoDB INFORMATION_SCHEMA
FULLTEXT Index Tables”.

The INNODB_FT_BEING_DELETED table has these columns:

• DOC_ID

The document ID of the row that is in the process of being deleted. This value might reflect the value
of an ID column that you defined for the underlying table, or it can be a sequence value generated by
InnoDB when the table contains no suitable column. This value is used when you do text searches, to
skip rows in the INNODB_FT_INDEX_TABLE table before data for deleted rows is physically removed
from the FULLTEXT index by an OPTIMIZE TABLE statement. For more information, see Optimizing
InnoDB Full-Text Indexes.

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For more information about InnoDB FULLTEXT search, see Section 14.6.2.4, “InnoDB Full-Text

Indexes”, and Section 12.9, “Full-Text Search Functions”.

24.4.9 The INFORMATION_SCHEMA INNODB_FT_CONFIG Table

The INNODB_FT_CONFIG table provides metadata about the FULLTEXT index and associated processing
for an InnoDB table.

This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system
variable to the name (including the database name) of the table that contains the FULLTEXT index; for
example test/articles.

For related usage information and examples, see Section 14.16.4, “InnoDB INFORMATION_SCHEMA
FULLTEXT Index Tables”.

The INNODB_FT_CONFIG table has these columns:

• KEY

The name designating an item of metadata for an InnoDB table containing a FULLTEXT index.

The values for this column might change, depending on the needs for performance tuning and
debugging for InnoDB full-text processing. The key names and their meanings include:

• optimize_checkpoint_limit: The number of seconds after which an OPTIMIZE TABLE run

stops.

4168

The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table

• synced_doc_id: The next DOC_ID to be issued.

• stopword_table_name: The database/table name for a user-defined stopword table. The

VALUE column is empty if there is no user-defined stopword table.

• use_stopword: Indicates whether a stopword table is used, which is defined when the FULLTEXT

index is created.

• VALUE

The value associated with the corresponding KEY column, reflecting some limit or current value for an
aspect of a FULLTEXT index for an InnoDB table.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_CONFIG;
+---------------------------+-------------------+
| KEY                       | VALUE             |
+---------------------------+-------------------+
| optimize_checkpoint_limit | 180               |
| synced_doc_id             | 0                 |
| stopword_table_name       | test/my_stopwords |
| use_stopword              | 1                 |
+---------------------------+-------------------+

Notes

• This table is intended only for internal configuration. It is not intended for statistical information purposes.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For more information about InnoDB FULLTEXT search, see Section 14.6.2.4, “InnoDB Full-Text

Indexes”, and Section 12.9, “Full-Text Search Functions”.

24.4.10 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD
Table

The INNODB_FT_DEFAULT_STOPWORD table holds a list of stopwords that are used by default when
creating a FULLTEXT index on InnoDB tables. For information about the default InnoDB stopword list and
how to define your own stopword lists, see Section 12.9.4, “Full-Text Stopwords”.

For related usage information and examples, see Section 14.16.4, “InnoDB INFORMATION_SCHEMA
FULLTEXT Index Tables”.

The INNODB_FT_DEFAULT_STOPWORD table has these columns:

• value

A word that is used by default as a stopword for FULLTEXT indexes on InnoDB tables. This is not used
if you override the default stopword processing with either the innodb_ft_server_stopword_table
or the innodb_ft_user_stopword_table system variable.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_DEFAULT_STOPWORD;

4169

The INFORMATION_SCHEMA INNODB_FT_DELETED Table

+-------+
| value |
+-------+
| a     |
| about |
| an    |
| are   |
| as    |
| at    |
| be    |
| by    |
| com   |
| de    |
| en    |
| for   |
| from  |
| how   |
| i     |
| in    |
| is    |
| it    |
| la    |
| of    |
| on    |
| or    |
| that  |
| the   |
| this  |
| to    |
| was   |
| what  |
| when  |
| where |
| who   |
| will  |
| with  |
| und   |
| the   |
| www   |
+-------+
36 rows in set (0.00 sec)

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For more information about InnoDB FULLTEXT search, see Section 14.6.2.4, “InnoDB Full-Text

Indexes”, and Section 12.9, “Full-Text Search Functions”.

24.4.11 The INFORMATION_SCHEMA INNODB_FT_DELETED Table

The INNODB_FT_DELETED table stores rows that are deleted from the FULLTEXT index for an InnoDB
table. To avoid expensive index reorganization during DML operations for an InnoDB FULLTEXT index,
the information about newly deleted words is stored separately, filtered out of search results when you
do a text search, and removed from the main search index only when you issue an OPTIMIZE TABLE
statement for the InnoDB table. For more information, see Optimizing InnoDB Full-Text Indexes.

This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system
variable to the name (including the database name) of the table that contains the FULLTEXT index; for
example test/articles.

4170

The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table

For related usage information and examples, see Section 14.16.4, “InnoDB INFORMATION_SCHEMA
FULLTEXT Index Tables”.

The INNODB_FT_DELETED table has these columns:

• DOC_ID

The document ID of the newly deleted row. This value might reflect the value of an ID column that
you defined for the underlying table, or it can be a sequence value generated by InnoDB when the
table contains no suitable column. This value is used when you do text searches, to skip rows in
the INNODB_FT_INDEX_TABLE table before data for deleted rows is physically removed from the
FULLTEXT index by an OPTIMIZE TABLE statement. For more information, see Optimizing InnoDB Full-
Text Indexes.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_DELETED;
+--------+
| DOC_ID |
+--------+
|      6 |
|      7 |
|      8 |
+--------+

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For more information about InnoDB FULLTEXT search, see Section 14.6.2.4, “InnoDB Full-Text

Indexes”, and Section 12.9, “Full-Text Search Functions”.

24.4.12 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table

The INNODB_FT_INDEX_CACHE table provides token information about newly inserted rows in a
FULLTEXT index. To avoid expensive index reorganization during DML operations, the information about
newly indexed words is stored separately, and combined with the main search index only when OPTIMIZE
TABLE is run, when the server is shut down, or when the cache size exceeds a limit defined by the
innodb_ft_cache_size or innodb_ft_total_cache_size system variable.

This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system
variable to the name (including the database name) of the table that contains the FULLTEXT index; for
example test/articles.

For related usage information and examples, see Section 14.16.4, “InnoDB INFORMATION_SCHEMA
FULLTEXT Index Tables”.

The INNODB_FT_INDEX_CACHE table has these columns:

• WORD

A word extracted from the text of a newly inserted row.

• FIRST_DOC_ID

4171

The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table

The first document ID in which this word appears in the FULLTEXT index.

• LAST_DOC_ID

The last document ID in which this word appears in the FULLTEXT index.

• DOC_COUNT

The number of rows in which this word appears in the FULLTEXT index. The same word can occur
several times within the cache table, once for each combination of DOC_ID and POSITION values.

• DOC_ID

The document ID of the newly inserted row. This value might reflect the value of an ID column that you
defined for the underlying table, or it can be a sequence value generated by InnoDB when the table
contains no suitable column.

• POSITION

The position of this particular instance of the word within the relevant document identified by the DOC_ID
value. The value does not represent an absolute position; it is an offset added to the POSITION of the
previous instance of that word.

• This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system

variable to the name (including the database name) of the table that contains the FULLTEXT
index; for example test/articles. The following example demonstrates how to use the
innodb_ft_aux_table system variable to show information about a FULLTEXT index for a specified
table.

mysql> USE test;

mysql> CREATE TABLE articles (
         id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
         title VARCHAR(200),
         body TEXT,
         FULLTEXT (title,body)
       ) ENGINE=InnoDB;

mysql> INSERT INTO articles (title,body) VALUES
       ('MySQL Tutorial','DBMS stands for DataBase ...'),
       ('How To Use MySQL Well','After you went through a ...'),
       ('Optimizing MySQL','In this tutorial we show ...'),
       ('1001 MySQL Tricks','1. Never run mysqld as root. 2. ...'),
       ('MySQL vs. YourSQL','In the following database comparison ...'),
       ('MySQL Security','When configured properly, MySQL ...');

mysql> SET GLOBAL innodb_ft_aux_table = 'test/articles';

mysql> SELECT WORD, DOC_COUNT, DOC_ID, POSITION
       FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_CACHE LIMIT 5;
+------------+-----------+--------+----------+
| WORD       | DOC_COUNT | DOC_ID | POSITION |
+------------+-----------+--------+----------+
| 1001       |         1 |      4 |        0 |
| after      |         1 |      2 |       22 |
| comparison |         1 |      5 |       44 |
| configured |         1 |      6 |       20 |
| database   |         2 |      1 |       31 |
+------------+-----------+--------+----------+

Notes

4172

The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For more information about InnoDB FULLTEXT search, see Section 14.6.2.4, “InnoDB Full-Text

Indexes”, and Section 12.9, “Full-Text Search Functions”.

24.4.13 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table

The INNODB_FT_INDEX_TABLE table provides information about the inverted index used to process text
searches against the FULLTEXT index of an InnoDB table.

This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system
variable to the name (including the database name) of the table that contains the FULLTEXT index; for
example test/articles.

For related usage information and examples, see Section 14.16.4, “InnoDB INFORMATION_SCHEMA
FULLTEXT Index Tables”.

The INNODB_FT_INDEX_TABLE table has these columns:

• WORD

A word extracted from the text of the columns that are part of a FULLTEXT.

• FIRST_DOC_ID

The first document ID in which this word appears in the FULLTEXT index.

• LAST_DOC_ID

The last document ID in which this word appears in the FULLTEXT index.

• DOC_COUNT

The number of rows in which this word appears in the FULLTEXT index. The same word can occur
several times within the cache table, once for each combination of DOC_ID and POSITION values.

• DOC_ID

The document ID of the row containing the word. This value might reflect the value of an ID column that
you defined for the underlying table, or it can be a sequence value generated by InnoDB when the table
contains no suitable column.

• POSITION

The position of this particular instance of the word within the relevant document identified by the DOC_ID
value.

Notes

• This table is empty initially. Before querying it, set the value of the innodb_ft_aux_table system

variable to the name (including the database name) of the table that contains the FULLTEXT
index; for example test/articles. The following example demonstrates how to use the
innodb_ft_aux_table system variable to show information about a FULLTEXT index for a specified
table. Before information for newly inserted rows appears in INNODB_FT_INDEX_TABLE, the FULLTEXT
index cache must be flushed to disk. This is accomplished by running an OPTIMIZE TABLE operation

4173

The INFORMATION_SCHEMA INNODB_LOCKS Table

on the indexed table with the innodb_optimize_fulltext_only system variable enabled. (The
example disables that variable again at the end because it is intended to be enabled only temporarily.)

mysql> USE test;

mysql> CREATE TABLE articles (
         id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
         title VARCHAR(200),
         body TEXT,
         FULLTEXT (title,body)
       ) ENGINE=InnoDB;

mysql> INSERT INTO articles (title,body) VALUES
       ('MySQL Tutorial','DBMS stands for DataBase ...'),
       ('How To Use MySQL Well','After you went through a ...'),
       ('Optimizing MySQL','In this tutorial we show ...'),
       ('1001 MySQL Tricks','1. Never run mysqld as root. 2. ...'),
       ('MySQL vs. YourSQL','In the following database comparison ...'),
       ('MySQL Security','When configured properly, MySQL ...');

mysql> SET GLOBAL innodb_optimize_fulltext_only=ON;

mysql> OPTIMIZE TABLE articles;
+---------------+----------+----------+----------+
| Table         | Op       | Msg_type | Msg_text |
+---------------+----------+----------+----------+
| test.articles | optimize | status   | OK       |
+---------------+----------+----------+----------+

mysql> SET GLOBAL innodb_ft_aux_table = 'test/articles';

mysql> SELECT WORD, DOC_COUNT, DOC_ID, POSITION
       FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_TABLE LIMIT 5;
+------------+-----------+--------+----------+
| WORD       | DOC_COUNT | DOC_ID | POSITION |
+------------+-----------+--------+----------+
| 1001       |         1 |      4 |        0 |
| after      |         1 |      2 |       22 |
| comparison |         1 |      5 |       44 |
| configured |         1 |      6 |       20 |
| database   |         2 |      1 |       31 |
+------------+-----------+--------+----------+

mysql> SET GLOBAL innodb_optimize_fulltext_only=OFF;

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For more information about InnoDB FULLTEXT search, see Section 14.6.2.4, “InnoDB Full-Text

Indexes”, and Section 12.9, “Full-Text Search Functions”.

24.4.14 The INFORMATION_SCHEMA INNODB_LOCKS Table

The INNODB_LOCKS table provides information about each lock that an InnoDB transaction has requested
but not yet acquired, and each lock that a transaction holds that is blocking another transaction.

Note

This table is deprecated as of MySQL 5.7.14 and is removed in MySQL 8.0.

The INNODB_LOCKS table has these columns:

4174

The INFORMATION_SCHEMA INNODB_LOCKS Table

• LOCK_ID

A unique lock ID number, internal to InnoDB. Treat it as an opaque string. Although LOCK_ID currently
contains TRX_ID, the format of the data in LOCK_ID is subject to change at any time. Do not write
applications that parse the LOCK_ID value.

• LOCK_TRX_ID

The ID of the transaction holding the lock. To obtain details about the transaction, join this column with
the TRX_ID column of the INNODB_TRX table.

• LOCK_MODE

How the lock is requested. Permitted lock mode descriptors are S, X, IS, IX, GAP, AUTO_INC, and
UNKNOWN. Lock mode descriptors may be used in combination to identify particular lock modes. For
information about InnoDB lock modes, see Section 14.7.1, “InnoDB Locking”.

• LOCK_TYPE

The type of lock. Permitted values are RECORD for a row-level lock, TABLE for a table-level lock.

• LOCK_TABLE

The name of the table that has been locked or contains locked records.

• LOCK_INDEX

The name of the index, if LOCK_TYPE is RECORD; otherwise NULL.

• LOCK_SPACE

The tablespace ID of the locked record, if LOCK_TYPE is RECORD; otherwise NULL.

• LOCK_PAGE

The page number of the locked record, if LOCK_TYPE is RECORD; otherwise NULL.

• LOCK_REC

The heap number of the locked record within the page, if LOCK_TYPE is RECORD; otherwise NULL.

• LOCK_DATA

The data associated with the lock, if any. A value is shown if the LOCK_TYPE is RECORD, otherwise the
value is NULL. Primary key values of the locked record are shown for a lock placed on the primary key
index. Secondary index values of the locked record are shown for a lock placed on a unique secondary
index. Secondary index values are shown with primary key values appended if the secondary index is
not unique. If there is no primary key, LOCK_DATA shows either the key values of a selected unique
index or the unique InnoDB internal row ID number, according to the rules governing InnoDB clustered
index use (see Section 14.6.2.1, “Clustered and Secondary Indexes”). LOCK_DATA reports “supremum
pseudo-record” for a lock taken on a supremum pseudo-record. If the page containing the locked record
is not in the buffer pool because it was written to disk while the lock was held, InnoDB does not fetch the
page from disk. Instead, LOCK_DATA reports NULL.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS\G
*************************** 1. row ***************************

4175

The INFORMATION_SCHEMA INNODB_LOCK_WAITS Table

    lock_id: 3723:72:3:2
lock_trx_id: 3723
  lock_mode: X
  lock_type: RECORD
 lock_table: `mysql`.`t`
 lock_index: PRIMARY
 lock_space: 72
  lock_page: 3
   lock_rec: 2
  lock_data: 1, 9
*************************** 2. row ***************************
    lock_id: 3722:72:3:2
lock_trx_id: 3722
  lock_mode: S
  lock_type: RECORD
 lock_table: `mysql`.`t`
 lock_index: PRIMARY
 lock_space: 72
  lock_page: 3
   lock_rec: 2
  lock_data: 1, 9

Notes

• Use this table to help diagnose performance problems that occur during times of heavy concurrent load.
Its contents are updated as described in Section 14.16.2.3, “Persistence and Consistency of InnoDB
Transaction and Locking Information”.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For usage information, see Section 14.16.2.1, “Using InnoDB Transaction and Locking Information”.

24.4.15 The INFORMATION_SCHEMA INNODB_LOCK_WAITS Table

The INNODB_LOCK_WAITS table contains one or more rows for each blocked InnoDB transaction,
indicating the lock it has requested and any locks that are blocking that request.

Note

This table is deprecated as of MySQL 5.7.14 and is removed in MySQL 8.0.

The INNODB_LOCK_WAITS table has these columns:

• REQUESTING_TRX_ID

The ID of the requesting (blocked) transaction.

• REQUESTED_LOCK_ID

The ID of the lock for which a transaction is waiting. To obtain details about the lock, join this column
with the LOCK_ID column of the INNODB_LOCKS table.

• BLOCKING_TRX_ID

The ID of the blocking transaction.

• BLOCKING_LOCK_ID

4176

The INFORMATION_SCHEMA INNODB_METRICS Table

The ID of a lock held by a transaction blocking another transaction from proceeding. To obtain details
about the lock, join this column with the LOCK_ID column of the INNODB_LOCKS table.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS\G
*************************** 1. row ***************************
requesting_trx_id: 3396
requested_lock_id: 3396:91:3:2
  blocking_trx_id: 3395
 blocking_lock_id: 3395:91:3:2

Notes

• Use this table to help diagnose performance problems that occur during times of heavy concurrent load.
Its contents are updated as described in Section 14.16.2.3, “Persistence and Consistency of InnoDB
Transaction and Locking Information”.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• For usage information, see Section 14.16.2.1, “Using InnoDB Transaction and Locking Information”.

24.4.16 The INFORMATION_SCHEMA INNODB_METRICS Table

The INNODB_METRICS table provides a wide variety of InnoDB performance information, complementing
the specific focus areas of the Performance Schema tables for InnoDB. With simple queries, you can
check the overall health of the system. With more detailed queries, you can diagnose issues such as
performance bottlenecks, resource shortages, and application issues.

Each monitor represents a point within the InnoDB source code that is instrumented to gather counter
information. Each counter can be started, stopped, and reset. You can also perform these actions for a
group of counters using their common module name.

By default, relatively little data is collected. To start, stop, and reset counters, set one of the system
variables innodb_monitor_enable, innodb_monitor_disable, innodb_monitor_reset, or
innodb_monitor_reset_all, using the name of the counter, the name of the module, a wildcard match
for such a name using the “%” character, or the special keyword all.

For usage information, see Section 14.16.6, “InnoDB INFORMATION_SCHEMA Metrics Table”.

The INNODB_METRICS table has these columns:

• NAME

A unique name for the counter.

• SUBSYSTEM

The aspect of InnoDB that the metric applies to.

• COUNT

The value since the counter was enabled.

• MAX_COUNT

4177

The INFORMATION_SCHEMA INNODB_METRICS Table

The maximum value since the counter was enabled.

• MIN_COUNT

The minimum value since the counter was enabled.

• AVG_COUNT

The average value since the counter was enabled.

• COUNT_RESET

The counter value since it was last reset. (The _RESET columns act like the lap counter on a stopwatch:
you can measure the activity during some time interval, while the cumulative figures are still available in
COUNT, MAX_COUNT, and so on.)

• MAX_COUNT_RESET

The maximum counter value since it was last reset.

• MIN_COUNT_RESET

The minimum counter value since it was last reset.

• AVG_COUNT_RESET

The average counter value since it was last reset.

• TIME_ENABLED

The timestamp of the last start.

• TIME_DISABLED

The timestamp of the last stop.

• TIME_ELAPSED

The elapsed time in seconds since the counter started.

• TIME_RESET

The timestamp of the last reset.

• STATUS

Whether the counter is still running (enabled) or stopped (disabled).

• TYPE

Whether the item is a cumulative counter, or measures the current value of some resource.

• COMMENT

The counter description.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME='dml_inserts'\G

4178

The INFORMATION_SCHEMA INNODB_SYS_COLUMNS Table

*************************** 1. row ***************************
           NAME: dml_inserts
      SUBSYSTEM: dml
          COUNT: 3
      MAX_COUNT: 3
      MIN_COUNT: NULL
      AVG_COUNT: 0.046153846153846156
    COUNT_RESET: 3
MAX_COUNT_RESET: 3
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: NULL
   TIME_ENABLED: 2014-12-04 14:18:28
  TIME_DISABLED: NULL
   TIME_ELAPSED: 65
     TIME_RESET: NULL
         STATUS: enabled
           TYPE: status_counter
        COMMENT: Number of rows inserted

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• Transaction counter COUNT values may differ from the number of transaction events reported in
Performance Schema EVENTS_TRANSACTIONS_SUMMARY tables. InnoDB counts only those
transactions that it executes, whereas Performance Schema collects events for all non-aborted
transactions initiated by the server, including empty transactions.

24.4.17 The INFORMATION_SCHEMA INNODB_SYS_COLUMNS Table

The INNODB_SYS_COLUMNS table provides metadata about InnoDB table columns, equivalent to the
information from the SYS_COLUMNS table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_COLUMNS table has these columns:

• TABLE_ID

An identifier representing the table associated with the column; the same value as
INNODB_SYS_TABLES.TABLE_ID.

• NAME

The name of the column. These names can be uppercase or lowercase depending on the
lower_case_table_names setting. There are no special system-reserved names for columns.

• POS

The ordinal position of the column within the table, starting from 0 and incrementing sequentially.
When a column is dropped, the remaining columns are reordered so that the sequence has no gaps.
The POS value for a virtual generated column encodes the column sequence number and ordinal
position of the column. For more information, see the POS column description in Section 24.4.26, “The
INFORMATION_SCHEMA INNODB_SYS_VIRTUAL Table”.

• MTYPE

4179

The INFORMATION_SCHEMA INNODB_SYS_DATAFILES Table

Stands for “main type”. A numeric identifier for the column type. 1 = VARCHAR, 2 = CHAR, 3 =
FIXBINARY, 4 = BINARY, 5 = BLOB, 6 = INT, 7 = SYS_CHILD, 8 = SYS, 9 = FLOAT, 10 = DOUBLE, 11 =
DECIMAL, 12 = VARMYSQL, 13 = MYSQL, 14 = GEOMETRY.

• PRTYPE

The InnoDB “precise type”, a binary value with bits representing MySQL data type, character set code,
and nullability.

• LEN

The column length, for example 4 for INT and 8 for BIGINT. For character columns in multibyte
character sets, this length value is the maximum length in bytes needed to represent a definition such as
VARCHAR(N); that is, it might be 2*N, 3*N, and so on depending on the character encoding.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_COLUMNS where TABLE_ID = 71\G
*************************** 1. row ***************************
TABLE_ID: 71
    NAME: col1
     POS: 0
   MTYPE: 6
  PRTYPE: 1027
     LEN: 4
*************************** 2. row ***************************
TABLE_ID: 71
    NAME: col2
     POS: 1
   MTYPE: 2
  PRTYPE: 524542
     LEN: 10
*************************** 3. row ***************************
TABLE_ID: 71
    NAME: col3
     POS: 2
   MTYPE: 1
  PRTYPE: 524303
     LEN: 10

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.18 The INFORMATION_SCHEMA INNODB_SYS_DATAFILES Table

The INNODB_SYS_DATAFILES table provides data file path information for InnoDB file-per-table and
general tablespaces, equivalent to the information in the SYS_DATAFILES table in the InnoDB data
dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

4180

The INFORMATION_SCHEMA INNODB_SYS_FIELDS Table

Note

The INFORMATION_SCHEMA FILES table reports metadata for all InnoDB
tablespace types including file-per-table tablespaces, general tablespaces, the
system tablespace, the temporary tablespace, and undo tablespaces, if present.

The INNODB_SYS_DATAFILES table has these columns:

• SPACE

The tablespace ID.

• PATH

The tablespace data file path. If a file-per-table tablespace is created in a location outside the MySQL
data directory, the path value is a fully qualified directory path. Otherwise, the path is relative to the data
directory.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_DATAFILES WHERE SPACE = 57\G
*************************** 1. row ***************************
SPACE: 57
 PATH: ./test/t1.ibd

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.19 The INFORMATION_SCHEMA INNODB_SYS_FIELDS Table

The INNODB_SYS_FIELDS table provides metadata about the key columns (fields) of InnoDB indexes,
equivalent to the information from the SYS_FIELDS table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_FIELDS table has these columns:

• INDEX_ID

An identifier for the index associated with this key field; the same value as
INNODB_SYS_INDEXES.INDEX_ID.

• NAME

The name of the original column from the table; the same value as INNODB_SYS_COLUMNS.NAME.

• POS

The ordinal position of the key field within the index, starting from 0 and incrementing sequentially. When
a column is dropped, the remaining columns are reordered so that the sequence has no gaps.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_FIELDS WHERE INDEX_ID = 117\G

4181

The INFORMATION_SCHEMA INNODB_SYS_FOREIGN Table

*************************** 1. row ***************************
INDEX_ID: 117
    NAME: col1
     POS: 0

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.20 The INFORMATION_SCHEMA INNODB_SYS_FOREIGN Table

The INNODB_SYS_FOREIGN table provides metadata about InnoDB foreign keys, equivalent to the
information from the SYS_FOREIGN table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_FOREIGN table has these columns:

• ID

The name (not a numeric value) of the foreign key index, preceded by the schema (database) name (for
example, test/products_fk).

• FOR_NAME

The name of the child table in this foreign key relationship.

• REF_NAME

The name of the parent table in this foreign key relationship.

• N_COLS

The number of columns in the foreign key index.

• TYPE

A collection of bit flags with information about the foreign key column, ORed together. 0 = ON DELETE/
UPDATE RESTRICT, 1 = ON DELETE CASCADE, 2 = ON DELETE SET NULL, 4 = ON UPDATE
CASCADE, 8 = ON UPDATE SET NULL, 16 = ON DELETE NO ACTION, 32 = ON UPDATE NO ACTION.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_FOREIGN\G
*************************** 1. row ***************************
      ID: test/fk1
FOR_NAME: test/child
REF_NAME: test/parent
  N_COLS: 1
    TYPE: 1

Notes

4182

• You must have the PROCESS privilege to query this table.

The INFORMATION_SCHEMA INNODB_SYS_FOREIGN_COLS Table

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.21 The INFORMATION_SCHEMA INNODB_SYS_FOREIGN_COLS Table

The INNODB_SYS_FOREIGN_COLS table provides status information about the columns of InnoDB foreign
keys, equivalent to the information from the SYS_FOREIGN_COLS table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_FOREIGN_COLS table has these columns:

• ID

The foreign key index associated with this index key field, using the same value as
INNODB_SYS_FOREIGN.ID.

• FOR_COL_NAME

The name of the associated column in the child table.

• REF_COL_NAME

The name of the associated column in the parent table.

• POS

The ordinal position of this key field within the foreign key index, starting from 0.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_FOREIGN_COLS WHERE ID = 'test/fk1'\G
*************************** 1. row ***************************
          ID: test/fk1
FOR_COL_NAME: parent_id
REF_COL_NAME: id
         POS: 0

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.22 The INFORMATION_SCHEMA INNODB_SYS_INDEXES Table

The INNODB_SYS_INDEXES table provides metadata about InnoDB indexes, equivalent to the information
in the internal SYS_INDEXES table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_INDEXES table has these columns:

• INDEX_ID

4183

The INFORMATION_SCHEMA INNODB_SYS_INDEXES Table

An identifier for the index. Index identifiers are unique across all the databases in an instance.

• NAME

The name of the index. Most indexes created implicitly by InnoDB have consistent names but the index
names are not necessarily unique. Examples: PRIMARY for a primary key index, GEN_CLUST_INDEX for
the index representing a primary key when one is not specified, and ID_IND, FOR_IND, and REF_IND
for foreign key constraints.

• TABLE_ID

An identifier representing the table associated with the index; the same value as
INNODB_SYS_TABLES.TABLE_ID.

• TYPE

A numeric value derived from bit-level information that identifies the index type. 0 = nonunique
secondary index; 1 = automatically generated clustered index (GEN_CLUST_INDEX); 2 = unique
nonclustered index; 3 = clustered index; 32 = full-text index; 64 = spatial index; 128 = secondary index
on a virtual generated column.

• N_FIELDS

The number of columns in the index key. For GEN_CLUST_INDEX indexes, this value is 0 because the
index is created using an artificial value rather than a real table column.

• PAGE_NO

The root page number of the index B-tree. For full-text indexes, the PAGE_NO column is unused and set
to -1 (FIL_NULL) because the full-text index is laid out in several B-trees (auxiliary tables).

• SPACE

An identifier for the tablespace where the index resides. 0 means the InnoDB system tablespace. Any
other number represents a table created with a separate .ibd file in file-per-table mode. This identifier
stays the same after a TRUNCATE TABLE statement. Because all indexes for a table reside in the same
tablespace as the table, this value is not necessarily unique.

• MERGE_THRESHOLD

The merge threshold value for index pages. If the amount of data in an index page falls below the
MERGE_THRESHOLD value when a row is deleted or when a row is shortened by an update operation,
InnoDB attempts to merge the index page with the neighboring index page. The default threshold value
is 50%. For more information, see Section 14.8.12, “Configuring the Merge Threshold for Index Pages”.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_INDEXES WHERE TABLE_ID = 34\G
*************************** 1. row ***************************
       INDEX_ID: 39
           NAME: GEN_CLUST_INDEX
       TABLE_ID: 34
           TYPE: 1
       N_FIELDS: 0
        PAGE_NO: 3
          SPACE: 23
MERGE_THRESHOLD: 50
*************************** 2. row ***************************
       INDEX_ID: 40

4184

The INFORMATION_SCHEMA INNODB_SYS_TABLES Table

           NAME: i1
       TABLE_ID: 34
           TYPE: 0
       N_FIELDS: 1
        PAGE_NO: 4
          SPACE: 23
MERGE_THRESHOLD: 50

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.23 The INFORMATION_SCHEMA INNODB_SYS_TABLES Table

The INNODB_SYS_TABLES table provides metadata about InnoDB tables, equivalent to the information
from the SYS_TABLES table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_TABLES table has these columns:

• TABLE_ID

An identifier for the InnoDB table. This value is unique across all databases in the instance.

• NAME

The name of the table, preceded by the schema (database) name where appropriate (for example,
test/t1). Names of databases and user tables are in the same case as they were originally defined,
possibly influenced by the lower_case_table_names setting.

• FLAG

A numeric value that represents bit-level information about table format and storage characteristics.

• N_COLS

The number of columns in the table. The number reported includes three hidden columns that are
created by InnoDB (DB_ROW_ID, DB_TRX_ID, and DB_ROLL_PTR). The number reported also includes
virtual generated columns, if present.

• SPACE

An identifier for the tablespace where the table resides. 0 means the InnoDB system tablespace. Any
other number represents either a file-per-table tablespace or a general tablespace. This identifier stays
the same after a TRUNCATE TABLE statement. For file-per-table tablespaces, this identifier is unique for
tables across all databases in the instance.

• FILE_FORMAT

The table's file format (Antelope or Barracuda).

• ROW_FORMAT

The table's row format (Compact, Redundant, Dynamic, or Compressed).

4185

The INFORMATION_SCHEMA INNODB_SYS_TABLESPACES Table

• ZIP_PAGE_SIZE

The zip page size. Applies only to tables with a row format of Compressed.

• SPACE_TYPE

The type of tablespace to which the table belongs. Possible values include System for
the system tablespace, General for general tablespaces, and Single for file-per-table
tablespaces. Tables assigned to the system tablespace using CREATE TABLE or ALTER TABLE
TABLESPACE=innodb_system have a SPACE_TYPE of General. For more information, see CREATE
TABLESPACE.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES WHERE TABLE_ID = 214\G
*************************** 1. row ***************************
     TABLE_ID: 214
         NAME: test/t1
         FLAG: 129
       N_COLS: 4
        SPACE: 233
  FILE_FORMAT: Antelope
   ROW_FORMAT: Compact
ZIP_PAGE_SIZE: 0
   SPACE_TYPE: General

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.24 The INFORMATION_SCHEMA INNODB_SYS_TABLESPACES Table

The INNODB_SYS_TABLESPACES table provides metadata about InnoDB file-per-table and general
tablespaces, equivalent to the information in the SYS_TABLESPACES table in the InnoDB data dictionary.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

Note

The INFORMATION_SCHEMA FILES table reports metadata for all InnoDB
tablespace types including file-per-table tablespaces, general tablespaces, the
system tablespace, the temporary tablespace, and undo tablespaces, if present.

The INNODB_SYS_TABLESPACES table has these columns:

• SPACE

The tablespace ID.

• NAME

The schema (database) and table name.

• FLAG

4186

The INFORMATION_SCHEMA INNODB_SYS_TABLESPACES Table

A numeric value that represents bit-level information about tablespace format and storage
characteristics.

• FILE_FORMAT

The tablespace file format. For example, Antelope, Barracuda, or Any (general tablespaces support
any row format). The data in this field is interpreted from the tablespace flags information that resides in
the .ibd file. For more information about InnoDB file formats, see Section 14.10, “InnoDB File-Format
Management”.

• ROW_FORMAT

The tablespace row format (Compact or Redundant, Dynamic, or Compressed). The data in this
column is interpreted from the tablespace flags information that resides in the .ibd file.

• PAGE_SIZE

The tablespace page size. The data in this column is interpreted from the tablespace flags information
that resides in the .ibd file.

• ZIP_PAGE_SIZE

The tablespace zip page size. The data in this column is interpreted from the tablespace flags
information that resides in the .ibd file.

• SPACE_TYPE

The type of tablespace. Possible values include General for general tablespaces and Single for file-
per-table tablespaces.

• FS_BLOCK_SIZE

The file system block size, which is the unit size used for hole punching. This column pertains to the
InnoDB transparent page compression feature.

• FILE_SIZE

The apparent size of the file, which represents the maximum size of the file, uncompressed. This column
pertains to the InnoDB transparent page compression feature.

• ALLOCATED_SIZE

The actual size of the file, which is the amount of space allocated on disk. This column pertains to the
InnoDB transparent page compression feature.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES WHERE SPACE = 26\G
*************************** 1. row ***************************
         SPACE: 26
          NAME: test/t1
          FLAG: 0
   FILE_FORMAT: Antelope
    ROW_FORMAT: Compact or Redundant
     PAGE_SIZE: 16384
 ZIP_PAGE_SIZE: 0
    SPACE_TYPE: Single
 FS_BLOCK_SIZE: 4096
     FILE_SIZE: 98304

4187

The INFORMATION_SCHEMA INNODB_SYS_TABLESTATS View

ALLOCATED_SIZE: 65536

Notes

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

• Because tablespace flags are always zero for all Antelope file formats (unlike table flags), there is no
way to determine from this flag integer if the tablespace row format is Redundant or Compact. As a
result, the possible values for the ROW_FORMAT field are “Compact or Redundant”, “Compressed”, or
“Dynamic.”

• With the introduction of general tablespaces, InnoDB system tablespace data (for SPACE 0) is exposed

in INNODB_SYS_TABLESPACES.

24.4.25 The INFORMATION_SCHEMA INNODB_SYS_TABLESTATS View

The INNODB_SYS_TABLESTATS table provides a view of low-level status information about InnoDB
tables. This data is used by the MySQL optimizer to calculate which index to use when querying an
InnoDB table. This information is derived from in-memory data structures rather than data stored on disk.
There is no corresponding internal InnoDB system table.

InnoDB tables are represented in this view if they have been opened since the last server restart and have
not aged out of the table cache. Tables for which persistent stats are available are always represented in
this view.

Table statistics are updated only for DELETE or UPDATE operations that modify indexed columns. Statistics
are not updated by operations that modify only nonindexed columns.

ANALYZE TABLE clears table statistics and sets the STATS_INITIALIZED column to Uninitialized.
Statistics are collected again the next time the table is accessed.

For related usage information and examples, see Section 14.16.3, “InnoDB INFORMATION_SCHEMA
System Tables”.

The INNODB_SYS_TABLESTATS table has these columns:

• TABLE_ID

An identifier representing the table for which statistics are available; the same value as
INNODB_SYS_TABLES.TABLE_ID.

• NAME

The name of the table; the same value as INNODB_SYS_TABLES.NAME.

• STATS_INITIALIZED

The value is Initialized if the statistics are already collected, Uninitialized if not.

• NUM_ROWS

The current estimated number of rows in the table. Updated after each DML operation. The value could
be imprecise if uncommitted transactions are inserting into or deleting from the table.

• CLUST_INDEX_SIZE

4188

The INFORMATION_SCHEMA INNODB_SYS_VIRTUAL Table

The number of pages on disk that store the clustered index, which holds the InnoDB table data in
primary key order. This value might be null if no statistics are collected yet for the table.

• OTHER_INDEX_SIZE

The number of pages on disk that store all secondary indexes for the table. This value might be null if no
statistics are collected yet for the table.

• MODIFIED_COUNTER

The number of rows modified by DML operations, such as INSERT, UPDATE, DELETE, and also cascade
operations from foreign keys. This column is reset each time table statistics are recalculated

• AUTOINC

The next number to be issued for any auto-increment-based operation. The rate at which the AUTOINC
value changes depends on how many times auto-increment numbers have been requested and how
many numbers are granted per request.

• REF_COUNT

When this counter reaches zero, the table metadata can be evicted from the table cache.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLESTATS where TABLE_ID = 71\G
*************************** 1. row ***************************
         TABLE_ID: 71
             NAME: test/t1
STATS_INITIALIZED: Initialized
         NUM_ROWS: 1
 CLUST_INDEX_SIZE: 1
 OTHER_INDEX_SIZE: 0
 MODIFIED_COUNTER: 1
          AUTOINC: 0
        REF_COUNT: 1

Notes

• This table is useful primarily for expert-level performance monitoring, or when developing performance-

related extensions for MySQL.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.26 The INFORMATION_SCHEMA INNODB_SYS_VIRTUAL Table

The INNODB_SYS_VIRTUAL table provides metadata about InnoDB virtual generated columns and
columns upon which virtual generated columns are based, equivalent to information in the SYS_VIRTUAL
table in the InnoDB data dictionary.

A row appears in the INNODB_SYS_VIRTUAL table for each column upon which a virtual generated
column is based.

The INNODB_SYS_VIRTUAL table has these columns:

• TABLE_ID

4189

The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table

An identifier representing the table associated with the virtual column; the same value as
INNODB_SYS_TABLES.TABLE_ID.

• POS

The position value of the virtual generated column. The value is large because it encodes the column
sequence number and ordinal position. The formula used to calculate the value uses a bitwise operation:

((nth virtual generated column for the InnoDB instance + 1) << 16)
+ the ordinal position of the virtual generated column

For example, if the first virtual generated column in the InnoDB instance is the third column of the table,
the formula is (0 + 1) << 16) + 2. The first virtual generated column in the InnoDB instance is
always number 0. As the third column in the table, the ordinal position of the virtual generated column is
2. Ordinal positions are counted from 0.

• BASE_POS

The ordinal position of the columns upon which a virtual generated column is based.

Example

mysql> CREATE TABLE `t1` (
         `a` int(11) DEFAULT NULL,
         `b` int(11) DEFAULT NULL,
         `c` int(11) GENERATED ALWAYS AS (a+b) VIRTUAL,
         `h` varchar(10) DEFAULT NULL
       ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_VIRTUAL
       WHERE TABLE_ID IN
         (SELECT TABLE_ID FROM INFORMATION_SCHEMA.INNODB_TABLES
          WHERE NAME LIKE "test/t1");
+----------+-------+----------+
| TABLE_ID | POS   | BASE_POS |
+----------+-------+----------+
|       95 | 65538 |        0 |
|       95 | 65538 |        1 |
+----------+-------+----------+

Notes

• If a constant value is assigned to a virtual generated column, as in the following table, an entry for the

column does not appear in the INNODB_SYS_VIRTUAL table. For an entry to appear, a virtual generated
column must have a base column.

CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) GENERATED ALWAYS AS (5) VIRTUAL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

However, metadata for such a column does appear in the INNODB_SYS_COLUMNS table.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table

4190

The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table

The INNODB_TEMP_TABLE_INFO table provides information about user-created InnoDB temporary tables
that are active in an InnoDB instance. It does not provide information about internal InnoDB temporary
tables used by the optimizer. The INNODB_TEMP_TABLE_INFO table is created when first queried, exists
only in memory, and is not persisted to disk.

For usage information and examples, see Section 14.16.7, “InnoDB INFORMATION_SCHEMA Temporary
Table Info Table”.

The INNODB_TEMP_TABLE_INFO table has these columns:

• TABLE_ID

The table ID of the temporary table.

• NAME

The name of the temporary table.

• N_COLS

The number of columns in the temporary table. The number includes three hidden columns created by
InnoDB (DB_ROW_ID, DB_TRX_ID, and DB_ROLL_PTR).

• SPACE

The ID of the temporary tablespace where the temporary table resides. In 5.7, non-compressed InnoDB
temporary tables reside in a shared temporary tablespace. The data file for the shared temporary
tablespace is defined by the innodb_temp_data_file_path system variable. By default, there is
a single data file for the shared temporary tablespace named ibtmp1, which is located in the data
directory. Compressed temporary tables reside in separate file-per-table tablespaces located in the
temporary file directory defined by tmpdir. The temporary tablespace ID is a nonzero value that is
dynamically generated on server restart.

• PER_TABLE_TABLESPACE

A value of TRUE indicates that the temporary table resides in a separate file-per-table tablespace. A
value of FALSE indicates that the temporary table resides in the shared temporary tablespace.

• IS_COMPRESSED

A value of TRUE indicates that the temporary table is compressed.

Example

mysql> CREATE TEMPORARY TABLE t1 (c1 INT PRIMARY KEY) ENGINE=INNODB;

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TEMP_TABLE_INFO\G
*************************** 1. row ***************************
            TABLE_ID: 38
                NAME: #sql26cf_6_0
              N_COLS: 4
               SPACE: 52
PER_TABLE_TABLESPACE: FALSE
       IS_COMPRESSED: FALSE

Notes

• This table is useful primarily for expert-level monitoring.

• You must have the PROCESS privilege to query this table.

4191

The INFORMATION_SCHEMA INNODB_TRX Table

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.4.28 The INFORMATION_SCHEMA INNODB_TRX Table

The INNODB_TRX table provides information about every transaction currently executing inside InnoDB,
including whether the transaction is waiting for a lock, when the transaction started, and the SQL statement
the transaction is executing, if any.

For usage information, see Section 14.16.2.1, “Using InnoDB Transaction and Locking Information”.

The INNODB_TRX table has these columns:

• TRX_ID

A unique transaction ID number, internal to InnoDB. These IDs are not created for transactions that are
read only and nonlocking. For details, see Section 8.5.3, “Optimizing InnoDB Read-Only Transactions”.

• TRX_WEIGHT

The weight of a transaction, reflecting (but not necessarily the exact count of) the number of rows
altered and the number of rows locked by the transaction. To resolve a deadlock, InnoDB selects
the transaction with the smallest weight as the “victim” to roll back. Transactions that have changed
nontransactional tables are considered heavier than others, regardless of the number of altered and
locked rows.

• TRX_STATE

The transaction execution state. Permitted values are RUNNING, LOCK WAIT, ROLLING BACK, and
COMMITTING.

• TRX_STARTED

The transaction start time.

• TRX_REQUESTED_LOCK_ID

The ID of the lock the transaction is currently waiting for, if TRX_STATE is LOCK WAIT; otherwise NULL.
To obtain details about the lock, join this column with the LOCK_ID column of the INNODB_LOCKS table.

• TRX_WAIT_STARTED

The time when the transaction started waiting on the lock, if TRX_STATE is LOCK WAIT; otherwise
NULL.

• TRX_MYSQL_THREAD_ID

The MySQL thread ID. To obtain details about the thread, join this column with the ID column of the
INFORMATION_SCHEMA PROCESSLIST table, but see Section 14.16.2.3, “Persistence and Consistency
of InnoDB Transaction and Locking Information”.

• TRX_QUERY

The SQL statement that is being executed by the transaction.

• TRX_OPERATION_STATE

The transaction's current operation, if any; otherwise NULL.

4192

The INFORMATION_SCHEMA INNODB_TRX Table

• TRX_TABLES_IN_USE

The number of InnoDB tables used while processing the current SQL statement of this transaction.

• TRX_TABLES_LOCKED

The number of InnoDB tables that the current SQL statement has row locks on. (Because these are row
locks, not table locks, the tables can usually still be read from and written to by multiple transactions,
despite some rows being locked.)

• TRX_LOCK_STRUCTS

The number of locks reserved by the transaction.

• TRX_LOCK_MEMORY_BYTES

The total size taken up by the lock structures of this transaction in memory.

• TRX_ROWS_LOCKED

The approximate number or rows locked by this transaction. The value might include delete-marked
rows that are physically present but not visible to the transaction.

• TRX_ROWS_MODIFIED

The number of modified and inserted rows in this transaction.

• TRX_CONCURRENCY_TICKETS

A value indicating how much work the current transaction can do before being swapped out, as specified
by the innodb_concurrency_tickets system variable.

• TRX_ISOLATION_LEVEL

The isolation level of the current transaction.

• TRX_UNIQUE_CHECKS

Whether unique checks are turned on or off for the current transaction. For example, they might be
turned off during a bulk data load.

• TRX_FOREIGN_KEY_CHECKS

Whether foreign key checks are turned on or off for the current transaction. For example, they might be
turned off during a bulk data load.

• TRX_LAST_FOREIGN_KEY_ERROR

The detailed error message for the last foreign key error, if any; otherwise NULL.

• TRX_ADAPTIVE_HASH_LATCHED

Whether the adaptive hash index is locked by the current transaction. When the adaptive hash index
search system is partitioned, a single transaction does not lock the entire adaptive hash index. Adaptive
hash index partitioning is controlled by innodb_adaptive_hash_index_parts, which is set to 8 by
default.

• TRX_ADAPTIVE_HASH_TIMEOUT

4193

INFORMATION_SCHEMA Thread Pool Tables

Deprecated in MySQL 5.7.8. Always returns 0.

Whether to relinquish the search latch immediately for the adaptive hash index, or reserve it across calls
from MySQL. When there is no adaptive hash index contention, this value remains zero and statements
reserve the latch until they finish. During times of contention, it counts down to zero, and statements
release the latch immediately after each row lookup. When the adaptive hash index search system is
partitioned (controlled by innodb_adaptive_hash_index_parts), the value remains 0.

• TRX_IS_READ_ONLY

A value of 1 indicates the transaction is read only.

• TRX_AUTOCOMMIT_NON_LOCKING

A value of 1 indicates the transaction is a SELECT statement that does not use the FOR UPDATE or
LOCK IN SHARED MODE clauses, and is executing with autocommit enabled so that the transaction
contains only this one statement. When this column and TRX_IS_READ_ONLY are both 1, InnoDB
optimizes the transaction to reduce the overhead associated with transactions that change table data.

Example

mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX\G
*************************** 1. row ***************************
                    trx_id: 1510
                 trx_state: RUNNING
               trx_started: 2014-11-19 13:24:40
     trx_requested_lock_id: NULL
          trx_wait_started: NULL
                trx_weight: 586739
       trx_mysql_thread_id: 2
                 trx_query: DELETE FROM employees.salaries WHERE salary > 65000
       trx_operation_state: updating or deleting
         trx_tables_in_use: 1
         trx_tables_locked: 1
          trx_lock_structs: 3003
     trx_lock_memory_bytes: 450768
           trx_rows_locked: 1407513
         trx_rows_modified: 583736
   trx_concurrency_tickets: 0
       trx_isolation_level: REPEATABLE READ
         trx_unique_checks: 1
    trx_foreign_key_checks: 1
trx_last_foreign_key_error: NULL
 trx_adaptive_hash_latched: 0
 trx_adaptive_hash_timeout: 10000
          trx_is_read_only: 0
trx_autocommit_non_locking: 0

Notes

• Use this table to help diagnose performance problems that occur during times of heavy concurrent load.
Its contents are updated as described in Section 14.16.2.3, “Persistence and Consistency of InnoDB
Transaction and Locking Information”.

• You must have the PROCESS privilege to query this table.

• Use the INFORMATION_SCHEMA COLUMNS table or the SHOW COLUMNS statement to view additional

information about the columns of this table, including data types and default values.

24.5 INFORMATION_SCHEMA Thread Pool Tables

4194

INFORMATION_SCHEMA Thread Pool Table Reference

The following sections describe the INFORMATION_SCHEMA tables associated with the thread pool
plugin (see Section 5.5.3, “MySQL Enterprise Thread Pool”). They provide information about thread pool
operation:

• TP_THREAD_GROUP_STATE: Information about thread pool thread group states

• TP_THREAD_GROUP_STATS: Thread group statistics

• TP_THREAD_STATE: Information about thread pool thread states

Rows in these tables represent snapshots in time. In the case of TP_THREAD_STATE, all rows for a thread
group comprise a snapshot in time. Thus, the MySQL server holds the mutex of the thread group while
producing the snapshot. But it does not hold mutexes on all thread groups at the same time, to prevent a
statement against TP_THREAD_STATE from blocking the entire MySQL server.

The thread pool INFORMATION_SCHEMA tables are implemented by individual plugins and the decision
whether to load one can be made independently of the others (see Section 5.5.3.2, “Thread Pool
Installation”). However, the content of all the tables depends on the thread pool plugin being enabled. If a
table plugin is enabled but the thread pool plugin is not, the table becomes visible and can be accessed,
but is empty.

24.5.1 INFORMATION_SCHEMA Thread Pool Table Reference

The following table summarizes INFORMATION_SCHEMA thread pool tables. For greater detail, see the
individual table descriptions.

Table 24.7 INFORMATION_SCHEMA Thread Pool Tables

Table Name

TP_THREAD_GROUP_STATE

TP_THREAD_GROUP_STATS

TP_THREAD_STATE

Description

Thread pool thread group states

Thread pool thread group statistics

Thread pool thread information

24.5.2 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table

The TP_THREAD_GROUP_STATE table has one row per thread group in the thread pool. Each row provides
information about the current state of a group.

The TP_THREAD_GROUP_STATE table has these columns:

• TP_GROUP_ID

The thread group ID. This is a unique key within the table.

• CONSUMER THREADS

The number of consumer threads. There is at most one thread ready to start executing if the active
threads become stalled or blocked.

• RESERVE_THREADS

The number of threads in the reserved state. This means that they are not started until there is a need
to wake a new thread and there is no consumer thread. This is where most threads end up when the
thread group has created more threads than needed for normal operation. Often a thread group needs
additional threads for a short while and then does not need them again for a while. In this case, they go

4195

The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table

into the reserved state and remain until needed again. They take up some extra memory resources, but
no extra computing resources.

• CONNECT_THREAD_COUNT

The number of threads that are processing or waiting to process connection initialization and
authentication. There can be a maximum of four connection threads per thread group; these threads
expire after a period of inactivity.

This column was added in MySQL 5.7.18.

• CONNECTION_COUNT

The number of connections using this thread group.

• QUEUED_QUERIES

The number of statements waiting in the high-priority queue.

• QUEUED_TRANSACTIONS

The number of statements waiting in the low-priority queue. These are the initial statements for
transactions that have not started, so they also represent queued transactions.

• STALL_LIMIT

The value of the thread_pool_stall_limit system variable for the thread group. This is the same
value for all thread groups.

• PRIO_KICKUP_TIMER

The value of the thread_pool_prio_kickup_timer system variable for the thread group. This is the
same value for all thread groups.

• ALGORITHM

The value of the thread_pool_algorithm system variable for the thread group. This is the same
value for all thread groups.

• THREAD_COUNT

The number of threads started in the thread pool as part of this thread group.

• ACTIVE_THREAD_COUNT

The number of threads active in executing statements.

• STALLED_THREAD_COUNT

The number of stalled statements in the thread group. A stalled statement could be executing, but from a
thread pool perspective it is stalled and making no progress. A long-running statement quickly ends up in
this category.

• WAITING_THREAD_NUMBER

If there is a thread handling the polling of statements in the thread group, this specifies the thread
number within this thread group. It is possible that this thread could be executing a statement.

• OLDEST_QUEUED

4196

The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table

How long in milliseconds the oldest queued statement has been waiting for execution.

• MAX_THREAD_IDS_IN_GROUP

The maximum thread ID of the threads in the group. This is the same as MAX(TP_THREAD_NUMBER) for
the threads when selected from the TP_THREAD_STATE table. That is, these two queries are equivalent:

SELECT TP_GROUP_ID, MAX_THREAD_IDS_IN_GROUP
FROM TP_THREAD_GROUP_STATE;

SELECT TP_GROUP_ID, MAX(TP_THREAD_NUMBER)
FROM TP_THREAD_STATE GROUP BY TP_GROUP_ID;

24.5.3 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table

The TP_THREAD_GROUP_STATS table reports statistics per thread group. There is one row per group.

The TP_THREAD_GROUP_STATS table has these columns:

• TP_GROUP_ID

The thread group ID. This is a unique key within the table.

• CONNECTIONS_STARTED

The number of connections started.

• CONNECTIONS_CLOSED

The number of connections closed.

• QUERIES_EXECUTED

The number of statements executed. This number is incremented when a statement starts executing, not
when it finishes.

• QUERIES_QUEUED

The number of statements received that were queued for execution. This does not count statements that
the thread group was able to begin executing immediately without queuing, which can happen under the
conditions described in Section 5.5.3.3, “Thread Pool Operation”.

• THREADS_STARTED

The number of threads started.

• PRIO_KICKUPS

The number of statements that have been moved from low-priority queue to high-priority queue based
on the value of the thread_pool_prio_kickup_timer system variable. If this number increases
quickly, consider increasing the value of that variable. A quickly increasing counter means that the
priority system is not keeping transactions from starting too early. For InnoDB, this most likely means
deteriorating performance due to too many concurrent transactions..

• STALLED_QUERIES_EXECUTED

The number of statements that have become defined as stalled due to executing for longer than the
value of the thread_pool_stall_limit system variable.

4197

The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table

• BECOME_CONSUMER_THREAD

The number of times thread have been assigned the consumer thread role.

• BECOME_RESERVE_THREAD

The number of times threads have been assigned the reserve thread role.

• BECOME_WAITING_THREAD

The number of times threads have been assigned the waiter thread role. When statements are queued,
this happens very often, even in normal operation, so rapid increases in this value are normal in the case
of a highly loaded system where statements are queued up.

• WAKE_THREAD_STALL_CHECKER

The number of times the stall check thread decided to wake or create a thread to possibly handle some
statements or take care of the waiter thread role.

• SLEEP_WAITS

The number of THD_WAIT_SLEEP waits. These occur when threads go to sleep; for example, by calling
the SLEEP() function.

• DISK_IO_WAITS

The number of THD_WAIT_DISKIO waits. These occur when threads perform disk I/O that is likely to
not hit the file system cache. Such waits occur when the buffer pool reads and writes data to disk, not for
normal reads from and writes to files.

• ROW_LOCK_WAITS

The number of THD_WAIT_ROW_LOCK waits for release of a row lock by another transaction.

• GLOBAL_LOCK_WAITS

The number of THD_WAIT_GLOBAL_LOCK waits for a global lock to be released.

• META_DATA_LOCK_WAITS

The number of THD_WAIT_META_DATA_LOCK waits for a metadata lock to be released.

• TABLE_LOCK_WAITS

The number of THD_WAIT_TABLE_LOCK waits for a table to be unlocked that the statement needs to
access.

• USER_LOCK_WAITS

The number of THD_WAIT_USER_LOCK waits for a special lock constructed by the user thread.

• BINLOG_WAITS

The number of THD_WAIT_BINLOG_WAITS waits for the binary log to become free.

• GROUP_COMMIT_WAITS

The number of THD_WAIT_GROUP_COMMIT waits. These occur when a group commit must wait for the
other parties to complete their part of a transaction.

4198

The INFORMATION_SCHEMA TP_THREAD_STATE Table

• FSYNC_WAITS

The number of THD_WAIT_SYNC waits for a file sync operation.

24.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table

The TP_THREAD_STATE table has one row per thread created by the thread pool to handle connections.

The TP_THREAD_STATE table has these columns:

• TP_GROUP_ID

The thread group ID.

• TP_THREAD_NUMBER

The ID of the thread within its thread group. TP_GROUP_ID and TP_THREAD_NUMBER together provide a
unique key within the table.

• PROCESS_COUNT

The 10ms interval in which the statement that uses this thread is currently executing. 0 means no
statement is executing, 1 means it is in the first 10ms, and so forth.

• WAIT_TYPE

The type of wait for the thread. NULL means the thread is not blocked. Otherwise, the thread is blocked
by a call to thd_wait_begin() and the value specifies the type of wait. The xxx_WAIT columns of the
TP_THREAD_GROUP_STATS table accumulate counts for each wait type.

The WAIT_TYPE value is a string that describes the type of wait, as shown in the following table.

Table 24.8 TP_THREAD_STATE Table WAIT_TYPE Values

Wait Type

THD_WAIT_SLEEP

THD_WAIT_DISKIO

THD_WAIT_ROW_LOCK

THD_WAIT_GLOBAL_LOCK

THD_WAIT_META_DATA_LOCK

THD_WAIT_TABLE_LOCK

THD_WAIT_USER_LOCK

THD_WAIT_BINLOG

THD_WAIT_GROUP_COMMIT

THD_WAIT_SYNC

Meaning

Waiting for sleep

Waiting for Disk IO

Waiting for row lock

Waiting for global lock

Waiting for metadata lock

Waiting for table lock

Waiting for user lock

Waiting for binlog

Waiting for group commit

Waiting for fsync

24.6 INFORMATION_SCHEMA Connection Control Tables

The following sections describe the INFORMATION_SCHEMA tables associated with the
connection_control plugin.

24.6.1 INFORMATION_SCHEMA Connection Control Table Reference

4199

The INFORMATION_SCHEMA CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table

The following table summarizes INFORMATION_SCHEMA connection control tables. For greater detail, see
the individual table descriptions.

Table 24.9 INFORMATION_SCHEMA Connection Control Tables

Table Name

Description

CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS

Current number of consecutive
failed connection attempts per
account

Introduced

5.7.17

24.6.2 The INFORMATION_SCHEMA
CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table

This table provides information about the current number of consecutive failed connection attempts per
account (user/host combination). The table was added in MySQL 5.7.17.

CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS has these columns:

• USERHOST

The user/host combination indicating an account that has failed connection attempts, in
'user_name'@'host_name' format.

• FAILED_ATTEMPTS

The current number of consecutive failed connection attempts for the USERHOST value. This counts
all failed attempts, regardless of whether they were delayed. The number of attempts for which the
server added a delay to its response is the difference between the FAILED_ATTEMPTS value and the
connection_control_failed_connections_threshold system variable value.

Notes

• The CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS plugin must be activated for this table to be
available, and the CONNECTION_CONTROL plugin must be activated or the table contents are always
empty. See Section 6.4.2, “Connection Control Plugins”.

• The table contains rows only for accounts that have had one or more consecutive failed connection

attempts without a subsequent successful attempt. When an account connects successfully, its failed-
connection count is reset to zero and the server removes any row corresponding to the account.

• Assigning a value to the connection_control_failed_connections_threshold system variable
at runtime resets all accumulated failed-connection counters to zero, which causes the table to become
empty.

24.7 INFORMATION_SCHEMA MySQL Enterprise Firewall Tables

The following sections describe the INFORMATION_SCHEMA tables associated with MySQL Enterprise
Firewall (see Section 6.4.6, “MySQL Enterprise Firewall”). They provide views into the firewall in-memory
data cache. These tables are available only if the appropriate firewall plugins are enabled.

24.7.1 INFORMATION_SCHEMA Firewall Table Reference

The following table summarizes INFORMATION_SCHEMA firewall tables. For greater detail, see the
individual table descriptions.

4200

The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table

Table 24.10 INFORMATION_SCHEMA Firewall Tables

Table Name

Description

MYSQL_FIREWALL_USERS

Firewall in-memory data for account profiles

MYSQL_FIREWALL_WHITELIST

Firewall in-memory data for account profile allowlists

24.7.2 The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table

The MYSQL_FIREWALL_USERS table provides a view into the in-memory data cache for MySQL Enterprise
Firewall. It lists names and operational modes of registered firewall account profiles. It is used in
conjunction with the mysql.firewall_users system table that provides persistent storage of firewall
data; see MySQL Enterprise Firewall Tables.

The MYSQL_FIREWALL_USERS table has these columns:

• USERHOST

The account profile name. Each account name has the format user_name@host_name.

• MODE

The current operational mode for the profile. Permitted mode values are OFF, DETECTING,
PROTECTING, RECORDING, and RESET. For details about their meanings, see Firewall Concepts.

24.7.3 The INFORMATION_SCHEMA MYSQL_FIREWALL_WHITELIST Table

The MYSQL_FIREWALL_WHITELIST table provides a view into the in-memory data cache for MySQL
Enterprise Firewall. It lists allowlist rules of registered firewall account profiles. It is used in conjunction with
the mysql.firewall_whitelist system table that provides persistent storage of firewall data; see
MySQL Enterprise Firewall Tables.

The MYSQL_FIREWALL_WHITELIST table has these columns:

• USERHOST

The account profile name. Each account name has the format user_name@host_name.

• RULE

A normalized statement indicating an acceptable statement pattern for the profile. A profile allowlist is the
union of its rules.

24.8 Extensions to SHOW Statements

Some extensions to SHOW statements accompany the implementation of INFORMATION_SCHEMA:

• SHOW can be used to get information about the structure of INFORMATION_SCHEMA itself.

• Several SHOW statements accept a WHERE clause that provides more flexibility in specifying which rows

to display.

The IS_UPDATABLE flag may be unreliable if a view depends on one or more other views, and one of
these underlying views is updated. Regardless of the IS_UPDATABLE value, the server keeps track of
the updatability of a view and correctly rejects data change operations to views that are not updatable. If
the IS_UPDATABLE value for a view has become inaccurate to due to changes to underlying views, the
value can be updated by deleting and recreating the view.

4201

Extensions to SHOW Statements

INFORMATION_SCHEMA is an information database, so its name is included in the output from SHOW
DATABASES. Similarly, SHOW TABLES can be used with INFORMATION_SCHEMA to obtain a list of its
tables:

mysql> SHOW TABLES FROM INFORMATION_SCHEMA;
+---------------------------------------+
| Tables_in_INFORMATION_SCHEMA          |
+---------------------------------------+
| CHARACTER_SETS                        |
| COLLATIONS                            |
| COLLATION_CHARACTER_SET_APPLICABILITY |
| COLUMNS                               |
| COLUMN_PRIVILEGES                     |
| ENGINES                               |
| EVENTS                                |
| FILES                                 |
| GLOBAL_STATUS                         |
| GLOBAL_VARIABLES                      |
| KEY_COLUMN_USAGE                      |
| PARTITIONS                            |
| PLUGINS                               |
| PROCESSLIST                           |
| REFERENTIAL_CONSTRAINTS               |
| ROUTINES                              |
| SCHEMATA                              |
| SCHEMA_PRIVILEGES                     |
| SESSION_STATUS                        |
| SESSION_VARIABLES                     |
| STATISTICS                            |
| TABLES                                |
| TABLE_CONSTRAINTS                     |
| TABLE_PRIVILEGES                      |
| TRIGGERS                              |
| USER_PRIVILEGES                       |
| VIEWS                                 |
+---------------------------------------+

SHOW COLUMNS and DESCRIBE can display information about the columns in individual
INFORMATION_SCHEMA tables.

SHOW statements that accept a LIKE clause to limit the rows displayed also permit a WHERE clause that
specifies more general conditions that selected rows must satisfy:

SHOW CHARACTER SET
SHOW COLLATION
SHOW COLUMNS
SHOW DATABASES
SHOW FUNCTION STATUS
SHOW INDEX
SHOW OPEN TABLES
SHOW PROCEDURE STATUS
SHOW STATUS
SHOW TABLE STATUS
SHOW TABLES
SHOW TRIGGERS
SHOW VARIABLES

The WHERE clause, if present, is evaluated against the column names displayed by the SHOW statement.
For example, the SHOW CHARACTER SET statement produces these output columns:

mysql> SHOW CHARACTER SET;
+----------+-----------------------------+---------------------+--------+
| Charset  | Description                 | Default collation   | Maxlen |
+----------+-----------------------------+---------------------+--------+
| big5     | Big5 Traditional Chinese    | big5_chinese_ci     |      2 |

4202

Extensions to SHOW Statements

| dec8     | DEC West European           | dec8_swedish_ci     |      1 |
| cp850    | DOS West European           | cp850_general_ci    |      1 |
| hp8      | HP West European            | hp8_english_ci      |      1 |
| koi8r    | KOI8-R Relcom Russian       | koi8r_general_ci    |      1 |
| latin1   | cp1252 West European        | latin1_swedish_ci   |      1 |
| latin2   | ISO 8859-2 Central European | latin2_general_ci   |      1 |
...

To use a WHERE clause with SHOW CHARACTER SET, you would refer to those column names. As an
example, the following statement displays information about character sets for which the default collation
contains the string 'japanese':

mysql> SHOW CHARACTER SET WHERE `Default collation` LIKE '%japanese%';
+---------+---------------------------+---------------------+--------+
| Charset | Description               | Default collation   | Maxlen |
+---------+---------------------------+---------------------+--------+
| ujis    | EUC-JP Japanese           | ujis_japanese_ci    |      3 |
| sjis    | Shift-JIS Japanese        | sjis_japanese_ci    |      2 |
| cp932   | SJIS for Windows Japanese | cp932_japanese_ci   |      2 |
| eucjpms | UJIS for Windows Japanese | eucjpms_japanese_ci |      3 |
+---------+---------------------------+---------------------+--------+

This statement displays the multibyte character sets:

mysql> SHOW CHARACTER SET WHERE Maxlen > 1;
+---------+---------------------------+---------------------+--------+
| Charset | Description               | Default collation   | Maxlen |
+---------+---------------------------+---------------------+--------+
| big5    | Big5 Traditional Chinese  | big5_chinese_ci     |      2 |
| ujis    | EUC-JP Japanese           | ujis_japanese_ci    |      3 |
| sjis    | Shift-JIS Japanese        | sjis_japanese_ci    |      2 |
| euckr   | EUC-KR Korean             | euckr_korean_ci     |      2 |
| gb2312  | GB2312 Simplified Chinese | gb2312_chinese_ci   |      2 |
| gbk     | GBK Simplified Chinese    | gbk_chinese_ci      |      2 |
| utf8    | UTF-8 Unicode             | utf8_general_ci     |      3 |
| ucs2    | UCS-2 Unicode             | ucs2_general_ci     |      2 |
| cp932   | SJIS for Windows Japanese | cp932_japanese_ci   |      2 |
| eucjpms | UJIS for Windows Japanese | eucjpms_japanese_ci |      3 |
+---------+---------------------------+---------------------+--------+

4203

4204

