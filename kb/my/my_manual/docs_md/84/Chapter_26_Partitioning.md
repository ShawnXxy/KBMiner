Overview of Partitioning in MySQL

Section 26.3, “Partition Management”, covers methods of adding, removing, and altering partitions in
existing partitioned tables.

Section 26.3.4, “Maintenance of Partitions”, discusses table maintenance commands for use with
partitioned tables.

The PARTITIONS table in the INFORMATION_SCHEMA database provides information about partitions
and partitioned tables. See Section 28.3.21, “The INFORMATION_SCHEMA PARTITIONS Table”, for
more information; for some examples of queries against this table, see Section 26.2.7, “How MySQL
Partitioning Handles NULL”.

For known issues with partitioning in MySQL 8.4, see Section 26.6, “Restrictions and Limitations on
Partitioning”.

You may also find the following resources to be useful when working with partitioned tables.

Additional Resources.
include the following:

 Other sources of information about user-defined partitioning in MySQL

• MySQL Partitioning Forum

This is the official discussion forum for those interested in or experimenting with MySQL Partitioning
technology. It features announcements and updates from MySQL developers and others. It is
monitored by members of the Partitioning Development and Documentation Teams.

• PlanetMySQL

A MySQL news site featuring MySQL-related blogs, which should be of interest to anyone using
my MySQL. We encourage you to check here for links to blogs kept by those working with MySQL
Partitioning, or to have your own blog added to those covered.

26.1 Overview of Partitioning in MySQL

This section provides a conceptual overview of partitioning in MySQL 8.4.

For information on partitioning restrictions and feature limitations, see Section 26.6, “Restrictions and
Limitations on Partitioning”.

The SQL standard does not provide much in the way of guidance regarding the physical aspects
of data storage. The SQL language itself is intended to work independently of any data structures
or media underlying the schemas, tables, rows, or columns with which it works. Nonetheless, most
advanced database management systems have evolved some means of determining the physical
location to be used for storing specific pieces of data in terms of the file system, hardware or even
both. In MySQL, the InnoDB storage engine has long supported the notion of a tablespace (see
Section 17.6.3, “Tablespaces”), and the MySQL Server, even prior to the introduction of partitioning,
could be configured to employ different physical directories for storing different databases (see
Section 10.12.2, “Using Symbolic Links”, for an explanation of how this is done).

Partitioning takes this notion a step further, by enabling you to distribute portions of individual tables
across a file system according to rules which you can set largely as needed. In effect, different portions
of a table are stored as separate tables in different locations. The user-selected rule by which the
division of data is accomplished is known as a partitioning function, which in MySQL can be the
modulus, simple matching against a set of ranges or value lists, an internal hashing function, or a linear
hashing function. The function is selected according to the partitioning type specified by the user, and
takes as its parameter the value of a user-supplied expression. This expression can be a column value,
a function acting on one or more column values, or a set of one or more column values, depending on
the type of partitioning that is used.

In the case of RANGE, LIST, and [LINEAR] HASH partitioning, the value of the partitioning column
is passed to the partitioning function, which returns an integer value representing the number of the

4518

Partitioning Types

examine. Partition selection is also supported for the data modification statements DELETE, INSERT,
REPLACE, UPDATE, and LOAD DATA, LOAD XML. See the descriptions of these statements for more
information and examples.

26.2 Partitioning Types

This section discusses the types of partitioning which are available in MySQL 8.4. These include the
types listed here:

• RANGE partitioning.

 This type of partitioning assigns rows to partitions based on column values

falling within a given range. See Section 26.2.1, “RANGE Partitioning”. For information about an
extension to this type, RANGE COLUMNS, see Section 26.2.3.1, “RANGE COLUMNS partitioning”.

• LIST partitioning.

 Similar to partitioning by RANGE, except that the partition is selected based
on columns matching one of a set of discrete values. See Section 26.2.2, “LIST Partitioning”. For
information about an extension to this type, LIST COLUMNS, see Section 26.2.3.2, “LIST COLUMNS
partitioning”.

• HASH partitioning.

 With this type of partitioning, a partition is selected based on the value

returned by a user-defined expression that operates on column values in rows to be inserted into the
table. The function may consist of any expression valid in MySQL that yields an integer value. See
Section 26.2.4, “HASH Partitioning”.

An extension to this type, LINEAR HASH, is also available, see Section 26.2.4.1, “LINEAR HASH
Partitioning”.

• KEY partitioning.

 This type of partitioning is similar to partitioning by HASH, except that only one

or more columns to be evaluated are supplied, and the MySQL server provides its own hashing
function. These columns can contain other than integer values, since the hashing function supplied
by MySQL guarantees an integer result regardless of the column data type. An extension to this
type, LINEAR KEY, is also available. See Section 26.2.5, “KEY Partitioning”.

A very common use of database partitioning is to segregate data by date. Some database systems
support explicit date partitioning, which MySQL does not implement in 8.4. However, it is not difficult
in MySQL to create partitioning schemes based on DATE, TIME, or DATETIME columns, or based on
expressions making use of such columns.

When partitioning by KEY or LINEAR KEY, you can use a DATE, TIME, or DATETIME column as the
partitioning column without performing any modification of the column value. For example, this table
creation statement is perfectly valid in MySQL:

CREATE TABLE members (
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    username VARCHAR(16) NOT NULL,
    email VARCHAR(35),
    joined DATE NOT NULL
)
PARTITION BY KEY(joined)
PARTITIONS 6;

In MySQL 8.4, it is also possible to use a DATE or DATETIME column as the partitioning column using
RANGE COLUMNS and LIST COLUMNS partitioning.

Other partitioning types require a partitioning expression that yields an integer value or NULL. If you
wish to use date-based partitioning by RANGE, LIST, HASH, or LINEAR HASH, you can simply employ
a function that operates on a DATE, TIME, or DATETIME column and returns such a value, as shown
here:

CREATE TABLE members (
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,

4521

RANGE Partitioning

not overlapping, and are defined using the VALUES LESS THAN operator. For the next few examples,
suppose that you are creating a table such as the following to hold personnel records for a chain of 20
video stores, numbered 1 through 20:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
);

Note

The employees table used here has no primary or unique keys. While the
examples work as shown for purposes of the present discussion, you should
keep in mind that tables are extremely likely in practice to have primary keys,
unique keys, or both, and that allowable choices for partitioning columns
depend on the columns used for these keys, if any are present. For a discussion
of these issues, see Section 26.6.1, “Partitioning Keys, Primary Keys, and
Unique Keys”.

This table can be partitioned by range in a number of ways, depending on your needs. One way would
be to use the store_id column. For instance, you might decide to partition the table 4 ways by adding
a PARTITION BY RANGE clause as shown here:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)
PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN (21)
);

In this partitioning scheme, all rows corresponding to employees working at stores 1 through 5 are
stored in partition p0, to those employed at stores 6 through 10 are stored in partition p1, and so on.
Each partition is defined in order, from lowest to highest. This is a requirement of the PARTITION BY
RANGE syntax; you can think of it as being analogous to a series of if ... elseif ... statements
in C or Java in this regard.

It is easy to determine that a new row containing the data (72, 'Mitchell', 'Wilson',
'1998-06-25', DEFAULT, 7, 13) is inserted into partition p2, but what happens when your chain
adds a 21st store? Under this scheme, there is no rule that covers a row whose store_id is greater
than 20, so an error results because the server does not know where to place it. You can keep this
from occurring by using a “catchall” VALUES LESS THAN clause in the CREATE TABLE statement that
provides for all values greater than the highest value explicitly named:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)

4523

LIST Partitioning

    PARTITION p0 VALUES LESS THAN (1960),
    PARTITION p1 VALUES LESS THAN (1970),
    PARTITION p2 VALUES LESS THAN (1980),
    PARTITION p3 VALUES LESS THAN (1990),
    PARTITION p4 VALUES LESS THAN MAXVALUE
);

In MySQL 8.4, it is also possible to partition a table by RANGE based on the value of a TIMESTAMP
column, using the UNIX_TIMESTAMP() function, as shown in this example:

CREATE TABLE quarterly_report_status (
    report_id INT NOT NULL,
    report_status VARCHAR(20) NOT NULL,
    report_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
PARTITION BY RANGE ( UNIX_TIMESTAMP(report_updated) ) (
    PARTITION p0 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-01-01 00:00:00') ),
    PARTITION p1 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-04-01 00:00:00') ),
    PARTITION p2 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-07-01 00:00:00') ),
    PARTITION p3 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-10-01 00:00:00') ),
    PARTITION p4 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-01-01 00:00:00') ),
    PARTITION p5 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-04-01 00:00:00') ),
    PARTITION p6 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-07-01 00:00:00') ),
    PARTITION p7 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-10-01 00:00:00') ),
    PARTITION p8 VALUES LESS THAN ( UNIX_TIMESTAMP('2010-01-01 00:00:00') ),
    PARTITION p9 VALUES LESS THAN (MAXVALUE)
);

In MySQL 8.4, any other expressions involving TIMESTAMP values are not permitted. (See Bug
#42849.)

Note

It is also possible in MySQL 8.4 to use
UNIX_TIMESTAMP(timestamp_column) as a partitioning expression for
tables that are partitioned by LIST. However, it is usually not practical to do
so.

2. Partition the table by RANGE COLUMNS, using a DATE or DATETIME column as the partitioning

column. For example, the members table could be defined using the joined column directly, as
shown here:

CREATE TABLE members (
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    username VARCHAR(16) NOT NULL,
    email VARCHAR(35),
    joined DATE NOT NULL
)
PARTITION BY RANGE COLUMNS(joined) (
    PARTITION p0 VALUES LESS THAN ('1960-01-01'),
    PARTITION p1 VALUES LESS THAN ('1970-01-01'),
    PARTITION p2 VALUES LESS THAN ('1980-01-01'),
    PARTITION p3 VALUES LESS THAN ('1990-01-01'),
    PARTITION p4 VALUES LESS THAN MAXVALUE
);

Note

The use of partitioning columns employing date or time types other than DATE
or DATETIME is not supported with RANGE COLUMNS.

26.2.2 LIST Partitioning

List partitioning in MySQL is similar to range partitioning in many ways. As in partitioning by RANGE,
each partition must be explicitly defined. The chief difference between the two types of partitioning is
that, in list partitioning, each partition is defined and selected based on the membership of a column

4526

LIST Partitioning

value in one of a set of value lists, rather than in one of a set of contiguous ranges of values. This is
done by using PARTITION BY LIST(expr) where expr is a column value or an expression based
on a column value and returning an integer value, and then defining each partition by means of a
VALUES IN (value_list), where value_list is a comma-separated list of integers.

Note

In MySQL 8.4, it is possible to match against only a list of integers (and possibly
NULL—see Section 26.2.7, “How MySQL Partitioning Handles NULL”) when
partitioning by LIST.

However, other column types may be used in value lists when employing LIST
COLUMN partitioning, which is described later in this section.

Unlike the case with partitions defined by range, list partitions do not need to be declared in any
particular order. For more detailed syntactical information, see Section 15.1.20, “CREATE TABLE
Statement”.

For the examples that follow, we assume that the basic definition of the table to be partitioned is
provided by the CREATE TABLE statement shown here:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
);

(This is the same table used as a basis for the examples in Section 26.2.1, “RANGE Partitioning”. As
with the other partitioning examples, we assume that the default_storage_engine is InnoDB.)

Suppose that there are 20 video stores distributed among 4 franchises as shown in the following table.

Region

North

East

West

Central

Store ID Numbers

3, 5, 6, 9, 17

1, 2, 10, 11, 19, 20

4, 12, 13, 14, 18

7, 8, 15, 16

To partition this table in such a way that rows for stores belonging to the same region are stored in the
same partition, you could use the CREATE TABLE statement shown here:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY LIST(store_id) (
    PARTITION pNorth VALUES IN (3,5,6,9,17),
    PARTITION pEast VALUES IN (1,2,10,11,19,20),
    PARTITION pWest VALUES IN (4,12,13,14,18),
    PARTITION pCentral VALUES IN (7,8,15,16)
);

This makes it easy to add or drop employee records relating to specific regions to or from the table.
For instance, suppose that all stores in the West region are sold to another company. In MySQL
8.4, all rows relating to employees working at stores in that region can be deleted with the query

4527

COLUMNS Partitioning

MySQL also provides support for LIST COLUMNS partitioning, a variant of LIST partitioning
that enables you to use columns of types other than integer for partitioning columns, and to use
multiple columns as partitioning keys. For more information, see Section 26.2.3.2, “LIST COLUMNS
partitioning”.

26.2.3 COLUMNS Partitioning

The next two sections discuss COLUMNS partitioning, which are variants on RANGE and LIST
partitioning. COLUMNS partitioning enables the use of multiple columns in partitioning keys. All of
these columns are taken into account both for the purpose of placing rows in partitions and for the
determination of which partitions are to be checked for matching rows in partition pruning.

In addition, both RANGE COLUMNS partitioning and LIST COLUMNS partitioning support the use of non-
integer columns for defining value ranges or list members. The permitted data types are shown in the
following list:

• All integer types: TINYINT, SMALLINT, MEDIUMINT, INT (INTEGER), and BIGINT. (This is the

same as with partitioning by RANGE and LIST.)

Other numeric data types (such as DECIMAL or FLOAT) are not supported as partitioning columns.

• DATE and DATETIME.

Columns using other data types relating to dates or times are not supported as partitioning columns.

• The following string types: CHAR, VARCHAR, BINARY, and VARBINARY.

TEXT and BLOB columns are not supported as partitioning columns.

The discussions of RANGE COLUMNS and LIST COLUMNS partitioning in the next two sections assume
that you are already familiar with partitioning based on ranges and lists as supported in MySQL 5.1 and
later; for more information about these, see Section 26.2.1, “RANGE Partitioning”, and Section 26.2.2,
“LIST Partitioning”, respectively.

26.2.3.1 RANGE COLUMNS partitioning

Range columns partitioning is similar to range partitioning, but enables you to define partitions using
ranges based on multiple column values. In addition, you can define the ranges using columns of types
other than integer types.

RANGE COLUMNS partitioning differs significantly from RANGE partitioning in the following ways:

• RANGE COLUMNS does not accept expressions, only names of columns.

• RANGE COLUMNS accepts a list of one or more columns.

RANGE COLUMNS partitions are based on comparisons between tuples (lists of column values) rather
than comparisons between scalar values. Placement of rows in RANGE COLUMNS partitions is also
based on comparisons between tuples; this is discussed further later in this section.

• RANGE COLUMNS partitioning columns are not restricted to integer columns; string, DATE and

DATETIME columns can also be used as partitioning columns. (See Section 26.2.3, “COLUMNS
Partitioning”, for details.)

The basic syntax for creating a table partitioned by RANGE COLUMNS is shown here:

CREATE TABLE table_name
PARTITION BY RANGE COLUMNS(column_list) (
    PARTITION partition_name VALUES LESS THAN (value_list)[,
    PARTITION partition_name VALUES LESS THAN (value_list)][,
    ...]
)

column_list:

4529

COLUMNS Partitioning

    column_name[, column_name][, ...]

value_list:
    value[, value][, ...]

Note

Not all CREATE TABLE options that can be used when creating partitioned
tables are shown here. For complete information, see Section 15.1.20,
“CREATE TABLE Statement”.

In the syntax just shown, column_list is a list of one or more columns (sometimes called a
partitioning column list), and value_list is a list of values (that is, it is a partition definition value list).
A value_list must be supplied for each partition definition, and each value_list must have the
same number of values as the column_list has columns. Generally speaking, if you use N columns
in the COLUMNS clause, then each VALUES LESS THAN clause must also be supplied with a list of N
values.

The elements in the partitioning column list and in the value list defining each partition must occur
in the same order. In addition, each element in the value list must be of the same data type as the
corresponding element in the column list. However, the order of the column names in the partitioning
column list and the value lists does not have to be the same as the order of the table column definitions
in the main part of the CREATE TABLE statement. As with table partitioned by RANGE, you can use
MAXVALUE to represent a value such that any legal value inserted into a given column is always less
than this value. Here is an example of a CREATE TABLE statement that helps to illustrate all of these
points:

mysql> CREATE TABLE rcx (
    ->     a INT,
    ->     b INT,
    ->     c CHAR(3),
    ->     d INT
    -> )
    -> PARTITION BY RANGE COLUMNS(a,d,c) (
    ->     PARTITION p0 VALUES LESS THAN (5,10,'ggg'),
    ->     PARTITION p1 VALUES LESS THAN (10,20,'mmm'),
    ->     PARTITION p2 VALUES LESS THAN (15,30,'sss'),
    ->     PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE,MAXVALUE)
    -> );
Query OK, 0 rows affected (0.15 sec)

Table rcx contains the columns a, b, c, d. The partitioning column list supplied to the COLUMNS
clause uses 3 of these columns, in the order a, d, c. Each value list used to define a partition contains
3 values in the same order; that is, each value list tuple has the form (INT, INT, CHAR(3)), which
corresponds to the data types used by columns a, d, and c (in that order).

Placement of rows into partitions is determined by comparing the tuple from a row to be inserted that
matches the column list in the COLUMNS clause with the tuples used in the VALUES LESS THAN
clauses to define partitions of the table. Because we are comparing tuples (that is, lists or sets
of values) rather than scalar values, the semantics of VALUES LESS THAN as used with RANGE
COLUMNS partitions differs somewhat from the case with simple RANGE partitions. In RANGE partitioning,
a row generating an expression value that is equal to a limiting value in a VALUES LESS THAN is
never placed in the corresponding partition; however, when using RANGE COLUMNS partitioning, it is
sometimes possible for a row whose partitioning column list's first element is equal in value to the that
of the first element in a VALUES LESS THAN value list to be placed in the corresponding partition.

Consider the RANGE partitioned table created by this statement:

CREATE TABLE r1 (
    a INT,
    b INT
)
PARTITION BY RANGE (a)  (
    PARTITION p0 VALUES LESS THAN (5),
    PARTITION p1 VALUES LESS THAN (MAXVALUE)

4530

COLUMNS Partitioning

);

If we insert 3 rows into this table such that the column value for a is 5 for each row, all 3 rows are
stored in partition p1 because the a column value is in each case not less than 5, as we can see by
executing the proper query against the Information Schema PARTITIONS table:

mysql> INSERT INTO r1 VALUES (5,10), (5,11), (5,12);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT PARTITION_NAME, TABLE_ROWS
    ->     FROM INFORMATION_SCHEMA.PARTITIONS
    ->     WHERE TABLE_NAME = 'r1';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          0 |
| p1             |          3 |
+----------------+------------+
2 rows in set (0.00 sec)

Now consider a similar table rc1 that uses RANGE COLUMNS partitioning with both columns a and b
referenced in the COLUMNS clause, created as shown here:

CREATE TABLE rc1 (
    a INT,
    b INT
)
PARTITION BY RANGE COLUMNS(a, b) (
    PARTITION p0 VALUES LESS THAN (5, 12),
    PARTITION p3 VALUES LESS THAN (MAXVALUE, MAXVALUE)
);

If we insert exactly the same rows into rc1 as we just inserted into r1, the distribution of the rows is
quite different:

mysql> INSERT INTO rc1 VALUES (5,10), (5,11), (5,12);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT PARTITION_NAME, TABLE_ROWS
    ->     FROM INFORMATION_SCHEMA.PARTITIONS
    ->     WHERE TABLE_NAME = 'rc1';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          2 |
| p3             |          1 |
+----------------+------------+
2 rows in set (0.00 sec)

This is because we are comparing rows rather than scalar values. We can compare the row values
inserted with the limiting row value from the VALUES THAN LESS THAN clause used to define partition
p0 in table rc1, like this:

mysql> SELECT (5,10) < (5,12), (5,11) < (5,12), (5,12) < (5,12);
+-----------------+-----------------+-----------------+
| (5,10) < (5,12) | (5,11) < (5,12) | (5,12) < (5,12) |
+-----------------+-----------------+-----------------+
|               1 |               1 |               0 |
+-----------------+-----------------+-----------------+
1 row in set (0.00 sec)

The 2 tuples (5,10) and (5,11) evaluate as less than (5,12), so they are stored in partition p0.
Since 5 is not less than 5 and 12 is not less than 12, (5,12) is considered not less than (5,12), and
is stored in partition p1.

The SELECT statement in the preceding example could also have been written using explicit row
constructors, like this:

4531

COLUMNS Partitioning

SELECT ROW(5,10) < ROW(5,12), ROW(5,11) < ROW(5,12), ROW(5,12) < ROW(5,12);

For more information about the use of row constructors in MySQL, see Section 15.2.15.5, “Row
Subqueries”.

For a table partitioned by RANGE COLUMNS using only a single partitioning column, the storing of
rows in partitions is the same as that of an equivalent table that is partitioned by RANGE. The following
CREATE TABLE statement creates a table partitioned by RANGE COLUMNS using 1 partitioning column:

CREATE TABLE rx (
    a INT,
    b INT
)
PARTITION BY RANGE COLUMNS (a)  (
    PARTITION p0 VALUES LESS THAN (5),
    PARTITION p1 VALUES LESS THAN (MAXVALUE)
);

If we insert the rows (5,10), (5,11), and (5,12) into this table, we can see that their placement is
the same as it is for the table r we created and populated earlier:

mysql> INSERT INTO rx VALUES (5,10), (5,11), (5,12);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT PARTITION_NAME,TABLE_ROWS
    ->     FROM INFORMATION_SCHEMA.PARTITIONS
    ->     WHERE TABLE_NAME = 'rx';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          0 |
| p1             |          3 |
+----------------+------------+
2 rows in set (0.00 sec)

It is also possible to create tables partitioned by RANGE COLUMNS where limiting values for one or
more columns are repeated in successive partition definitions. You can do this as long as the tuples of
column values used to define the partitions are strictly increasing. For example, each of the following
CREATE TABLE statements is valid:

CREATE TABLE rc2 (
    a INT,
    b INT
)
PARTITION BY RANGE COLUMNS(a,b) (
    PARTITION p0 VALUES LESS THAN (0,10),
    PARTITION p1 VALUES LESS THAN (10,20),
    PARTITION p2 VALUES LESS THAN (10,30),
    PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE)
 );

CREATE TABLE rc3 (
    a INT,
    b INT
)
PARTITION BY RANGE COLUMNS(a,b) (
    PARTITION p0 VALUES LESS THAN (0,10),
    PARTITION p1 VALUES LESS THAN (10,20),
    PARTITION p2 VALUES LESS THAN (10,30),
    PARTITION p3 VALUES LESS THAN (10,35),
    PARTITION p4 VALUES LESS THAN (20,40),
    PARTITION p5 VALUES LESS THAN (MAXVALUE,MAXVALUE)
 );

The following statement also succeeds, even though it might appear at first glance that it would not,
since the limiting value of column b is 25 for partition p0 and 20 for partition p1, and the limiting value
of column c is 100 for partition p1 and 50 for partition p2:

4532

COLUMNS Partitioning

CREATE TABLE rc4 (
    a INT,
    b INT,
    c INT
)
PARTITION BY RANGE COLUMNS(a,b,c) (
    PARTITION p0 VALUES LESS THAN (0,25,50),
    PARTITION p1 VALUES LESS THAN (10,20,100),
    PARTITION p2 VALUES LESS THAN (10,30,50),
    PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE,MAXVALUE)
 );

When designing tables partitioned by RANGE COLUMNS, you can always test successive partition
definitions by comparing the desired tuples using the mysql client, like this:

mysql> SELECT (0,25,50) < (10,20,100), (10,20,100) < (10,30,50);
+-------------------------+--------------------------+
| (0,25,50) < (10,20,100) | (10,20,100) < (10,30,50) |
+-------------------------+--------------------------+
|                       1 |                        1 |
+-------------------------+--------------------------+
1 row in set (0.00 sec)

If a CREATE TABLE statement contains partition definitions that are not in strictly increasing order, it
fails with an error, as shown in this example:

mysql> CREATE TABLE rcf (
    ->     a INT,
    ->     b INT,
    ->     c INT
    -> )
    -> PARTITION BY RANGE COLUMNS(a,b,c) (
    ->     PARTITION p0 VALUES LESS THAN (0,25,50),
    ->     PARTITION p1 VALUES LESS THAN (20,20,100),
    ->     PARTITION p2 VALUES LESS THAN (10,30,50),
    ->     PARTITION p3 VALUES LESS THAN (MAXVALUE,MAXVALUE,MAXVALUE)
    ->  );
ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

When you get such an error, you can deduce which partition definitions are invalid by making “less
than” comparisons between their column lists. In this case, the problem is with the definition of partition
p2 because the tuple used to define it is not less than the tuple used to define partition p3, as shown
here:

mysql> SELECT (0,25,50) < (20,20,100), (20,20,100) < (10,30,50);
+-------------------------+--------------------------+
| (0,25,50) < (20,20,100) | (20,20,100) < (10,30,50) |
+-------------------------+--------------------------+
|                       1 |                        0 |
+-------------------------+--------------------------+
1 row in set (0.00 sec)

It is also possible for MAXVALUE to appear for the same column in more than one VALUES LESS THAN
clause when using RANGE COLUMNS. However, the limiting values for individual columns in successive
partition definitions should otherwise be increasing, there should be no more than one partition defined
where MAXVALUE is used as the upper limit for all column values, and this partition definition should
appear last in the list of PARTITION ... VALUES LESS THAN clauses. In addition, you cannot use
MAXVALUE as the limiting value for the first column in more than one partition definition.

As stated previously, it is also possible with RANGE COLUMNS partitioning to use non-integer columns
as partitioning columns. (See Section 26.2.3, “COLUMNS Partitioning”, for a complete listing of these.)
Consider a table named employees (which is not partitioned), created using the following statement:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',

4533

COLUMNS Partitioning

    job_code INT NOT NULL,
    store_id INT NOT NULL
);

Using RANGE COLUMNS partitioning, you can create a version of this table that stores each row in one
of four partitions based on the employee's last name, like this:

CREATE TABLE employees_by_lname (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)
PARTITION BY RANGE COLUMNS (lname)  (
    PARTITION p0 VALUES LESS THAN ('g'),
    PARTITION p1 VALUES LESS THAN ('m'),
    PARTITION p2 VALUES LESS THAN ('t'),
    PARTITION p3 VALUES LESS THAN (MAXVALUE)
);

Alternatively, you could cause the employees table as created previously to be partitioned using this
scheme by executing the following ALTER TABLE statement:

ALTER TABLE employees PARTITION BY RANGE COLUMNS (lname)  (
    PARTITION p0 VALUES LESS THAN ('g'),
    PARTITION p1 VALUES LESS THAN ('m'),
    PARTITION p2 VALUES LESS THAN ('t'),
    PARTITION p3 VALUES LESS THAN (MAXVALUE)
);

Note

Because different character sets and collations have different sort orders,
the character sets and collations in use may effect which partition of a table
partitioned by RANGE COLUMNS a given row is stored in when using string
columns as partitioning columns. In addition, changing the character set or
collation for a given database, table, or column after such a table is created may
cause changes in how rows are distributed. For example, when using a case-
sensitive collation, 'and' sorts before 'Andersen', but when using a collation
that is case-insensitive, the reverse is true.

For information about how MySQL handles character sets and collations, see
Chapter 12, Character Sets, Collations, Unicode.

Similarly, you can cause the employees table to be partitioned in such a way that each row is stored
in one of several partitions based on the decade in which the corresponding employee was hired using
the ALTER TABLE statement shown here:

ALTER TABLE employees PARTITION BY RANGE COLUMNS (hired)  (
    PARTITION p0 VALUES LESS THAN ('1970-01-01'),
    PARTITION p1 VALUES LESS THAN ('1980-01-01'),
    PARTITION p2 VALUES LESS THAN ('1990-01-01'),
    PARTITION p3 VALUES LESS THAN ('2000-01-01'),
    PARTITION p4 VALUES LESS THAN ('2010-01-01'),
    PARTITION p5 VALUES LESS THAN (MAXVALUE)
);

See Section 15.1.20, “CREATE TABLE Statement”, for additional information about PARTITION BY
RANGE COLUMNS syntax.

26.2.3.2 LIST COLUMNS partitioning

MySQL 8.4 provides support for LIST COLUMNS partitioning. This is a variant of LIST partitioning
that enables the use of multiple columns as partition keys, and for columns of data types other than

4534

COLUMNS Partitioning

integer types to be used as partitioning columns; you can use string types, DATE, and DATETIME
columns. (For more information about permitted data types for COLUMNS partitioning columns, see
Section 26.2.3, “COLUMNS Partitioning”.)

Suppose that you have a business that has customers in 12 cities which, for sales and marketing
purposes, you organize into 4 regions of 3 cities each as shown in the following table:

Region

1

2

3

4

Cities

Oskarshamn, Högsby, Mönsterås

Vimmerby, Hultsfred, Västervik

Nässjö, Eksjö, Vetlanda

Uppvidinge, Alvesta, Växjo

With LIST COLUMNS partitioning, you can create a table for customer data that assigns a row to any of
4 partitions corresponding to these regions based on the name of the city where a customer resides, as
shown here:

CREATE TABLE customers_1 (
    first_name VARCHAR(25),
    last_name VARCHAR(25),
    street_1 VARCHAR(30),
    street_2 VARCHAR(30),
    city VARCHAR(15),
    renewal DATE
)
PARTITION BY LIST COLUMNS(city) (
    PARTITION pRegion_1 VALUES IN('Oskarshamn', 'Högsby', 'Mönsterås'),
    PARTITION pRegion_2 VALUES IN('Vimmerby', 'Hultsfred', 'Västervik'),
    PARTITION pRegion_3 VALUES IN('Nässjö', 'Eksjö', 'Vetlanda'),
    PARTITION pRegion_4 VALUES IN('Uppvidinge', 'Alvesta', 'Växjo')
);

As with partitioning by RANGE COLUMNS, you do not need to use expressions in the COLUMNS() clause
to convert column values into integers. (In fact, the use of expressions other than column names is not
permitted with COLUMNS().)

It is also possible to use DATE and DATETIME columns, as shown in the following example that
uses the same name and columns as the customers_1 table shown previously, but employs LIST
COLUMNS partitioning based on the renewal column to store rows in one of 4 partitions depending on
the week in February 2010 the customer's account is scheduled to renew:

CREATE TABLE customers_2 (
    first_name VARCHAR(25),
    last_name VARCHAR(25),
    street_1 VARCHAR(30),
    street_2 VARCHAR(30),
    city VARCHAR(15),
    renewal DATE
)
PARTITION BY LIST COLUMNS(renewal) (
    PARTITION pWeek_1 VALUES IN('2010-02-01', '2010-02-02', '2010-02-03',
        '2010-02-04', '2010-02-05', '2010-02-06', '2010-02-07'),
    PARTITION pWeek_2 VALUES IN('2010-02-08', '2010-02-09', '2010-02-10',
        '2010-02-11', '2010-02-12', '2010-02-13', '2010-02-14'),
    PARTITION pWeek_3 VALUES IN('2010-02-15', '2010-02-16', '2010-02-17',
        '2010-02-18', '2010-02-19', '2010-02-20', '2010-02-21'),
    PARTITION pWeek_4 VALUES IN('2010-02-22', '2010-02-23', '2010-02-24',
        '2010-02-25', '2010-02-26', '2010-02-27', '2010-02-28')
);

This works, but becomes cumbersome to define and maintain if the number of dates involved grows
very large; in such cases, it is usually more practical to employ RANGE or RANGE COLUMNS partitioning
instead. In this case, since the column we wish to use as the partitioning key is a DATE column, we use
RANGE COLUMNS partitioning, as shown here:

4535

HASH Partitioning

CREATE TABLE customers_3 (
    first_name VARCHAR(25),
    last_name VARCHAR(25),
    street_1 VARCHAR(30),
    street_2 VARCHAR(30),
    city VARCHAR(15),
    renewal DATE
)
PARTITION BY RANGE COLUMNS(renewal) (
    PARTITION pWeek_1 VALUES LESS THAN('2010-02-09'),
    PARTITION pWeek_2 VALUES LESS THAN('2010-02-15'),
    PARTITION pWeek_3 VALUES LESS THAN('2010-02-22'),
    PARTITION pWeek_4 VALUES LESS THAN('2010-03-01')
);

See Section 26.2.3.1, “RANGE COLUMNS partitioning”, for more information.

In addition (as with RANGE COLUMNS partitioning), you can use multiple columns in the COLUMNS()
clause.

See Section 15.1.20, “CREATE TABLE Statement”, for additional information about PARTITION BY
LIST COLUMNS() syntax.

26.2.4 HASH Partitioning

Partitioning by HASH is used primarily to ensure an even distribution of data among a predetermined
number of partitions. With range or list partitioning, you must specify explicitly which partition a given
column value or set of column values should be stored in; with hash partitioning, this decision is taken
care of for you, and you need only specify a column value or expression based on a column value to be
hashed and the number of partitions into which the partitioned table is to be divided.

To partition a table using HASH partitioning, it is necessary to append to the CREATE TABLE statement
a PARTITION BY HASH (expr) clause, where expr is an expression that returns an integer. This
can simply be the name of a column whose type is one of MySQL's integer types. In addition, you
most likely want to follow this with PARTITIONS num, where num is a positive integer representing the
number of partitions into which the table is to be divided.

Note

For simplicity, the tables in the examples that follow do not use any keys. You
should be aware that, if a table has any unique keys, every column used in the
partitioning expression for this table must be part of every unique key, including
the primary key. See Section 26.6.1, “Partitioning Keys, Primary Keys, and
Unique Keys”, for more information.

The following statement creates a table that uses hashing on the store_id column and is divided into
4 partitions:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY HASH(store_id)
PARTITIONS 4;

If you do not include a PARTITIONS clause, the number of partitions defaults to 1; using the
PARTITIONS keyword without a number following it results in a syntax error.

You can also use an SQL expression that returns an integer for expr. For instance, you might want to
partition based on the year in which an employee was hired. This can be done as shown here:

4536

HASH Partitioning

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;

expr must return a nonconstant, nonrandom integer value (in other words, it should be varying
but deterministic), and must not contain any prohibited constructs as described in Section 26.6,
“Restrictions and Limitations on Partitioning”. You should also keep in mind that this expression is
evaluated each time a row is inserted or updated (or possibly deleted); this means that very complex
expressions may give rise to performance issues, particularly when performing operations (such as
batch inserts) that affect a great many rows at one time.

The most efficient hashing function is one which operates upon a single table column and whose value
increases or decreases consistently with the column value, as this allows for “pruning” on ranges of
partitions. That is, the more closely that the expression varies with the value of the column on which it
is based, the more efficiently MySQL can use the expression for hash partitioning.

For example, where date_col is a column of type DATE, then the expression TO_DAYS(date_col)
is said to vary directly with the value of date_col, because for every change in the value
of date_col, the value of the expression changes in a consistent manner. The variance of
the expression YEAR(date_col) with respect to date_col is not quite as direct as that of
TO_DAYS(date_col), because not every possible change in date_col produces an equivalent
change in YEAR(date_col). Even so, YEAR(date_col) is a good candidate for a hashing function,
because it varies directly with a portion of date_col and there is no possible change in date_col
that produces a disproportionate change in YEAR(date_col).

By way of contrast, suppose that you have a column named int_col whose type is INT. Now
consider the expression POW(5-int_col,3) + 6. This would be a poor choice for a hashing
function because a change in the value of int_col is not guaranteed to produce a proportional
change in the value of the expression. Changing the value of int_col by a given amount can produce
widely differing changes in the value of the expression. For example, changing int_col from 5 to 6
produces a change of -1 in the value of the expression, but changing the value of int_col from 6 to
7 produces a change of -7 in the expression value.

In other words, the more closely the graph of the column value versus the value of the expression
follows a straight line as traced by the equation y=cx where c is some nonzero constant, the better the
expression is suited to hashing. This has to do with the fact that the more nonlinear an expression is,
the more uneven the distribution of data among the partitions it tends to produce.

In theory, pruning is also possible for expressions involving more than one column value, but
determining which of such expressions are suitable can be quite difficult and time-consuming. For this
reason, the use of hashing expressions involving multiple columns is not particularly recommended.

When PARTITION BY HASH is used, the storage engine determines which partition of num partitions
to use based on the modulus of the result of the expression. In other words, for a given expression
expr, the partition in which the record is stored is partition number N, where N = MOD(expr, num).
Suppose that table t1 is defined as follows, so that it has 4 partitions:

CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;

If you insert a record into t1 whose col3 value is '2005-09-15', then the partition in which it is
stored is determined as follows:

MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)

4537

HASH Partitioning

=  1

MySQL 8.4 also supports a variant of HASH partitioning known as linear hashing which employs a more
complex algorithm for determining the placement of new rows inserted into the partitioned table. See
Section 26.2.4.1, “LINEAR HASH Partitioning”, for a description of this algorithm.

The user-supplied expression is evaluated each time a record is inserted or updated. It may also—
depending on the circumstances—be evaluated when records are deleted.

26.2.4.1 LINEAR HASH Partitioning

MySQL also supports linear hashing, which differs from regular hashing in that linear hashing utilizes a
linear powers-of-two algorithm whereas regular hashing employs the modulus of the hashing function's
value.

Syntactically, the only difference between linear-hash partitioning and regular hashing is the addition of
the LINEAR keyword in the PARTITION BY clause, as shown here:

CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY LINEAR HASH( YEAR(hired) )
PARTITIONS 4;

Given an expression expr, the partition in which the record is stored when linear hashing is used is
partition number N from among num partitions, where N is derived according to the following algorithm:

1. Find the next power of 2 greater than num. We call this value V; it can be calculated as:

V = POWER(2, CEILING(LOG(2, num)))

(Suppose that num is 13. Then LOG(2,13) is 3.7004397181411. CEILING(3.7004397181411)
is 4, and V = POWER(2,4), which is 16.)

2. Set N = F(column_list) & (V - 1).

3. While N >= num:

• Set V = V / 2

• Set N = N & (V - 1)

Suppose that the table t1, using linear hash partitioning and having 6 partitions, is created using this
statement:

CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY LINEAR HASH( YEAR(col3) )
    PARTITIONS 6;

Now assume that you want to insert two records into t1 having the col3 column values
'2003-04-14' and '1998-10-19'. The partition number for the first of these is determined as
follows:

V = POWER(2, CEILING( LOG(2,6) )) = 8
N = YEAR('2003-04-14') & (8 - 1)
   = 2003 & 7
   = 3

(3 >= 6 is FALSE: record stored in partition #3)

The number of the partition where the second record is stored is calculated as shown here:

4538

Subpartitioning

PARTITION BY KEY(s1)
PARTITIONS 10;

The preceding statement would not be valid, were a different partitioning type to be specified. (In
this case, simply using PARTITION BY KEY() would also be valid and have the same effect as
PARTITION BY KEY(s1), since s1 is the table's primary key.)

For additional information about this issue, see Section 26.6, “Restrictions and Limitations on
Partitioning”.

Columns with index prefixes are not supported in partitioning keys. This means that CHAR, VARCHAR,
BINARY, and VARBINARY columns can be used in a partitioning key, as long as they do not employ
prefixes; because a prefix must be specified for BLOB and TEXT columns in index definitions, it is
not possible to use columns of these two types in partitioning keys. In older versions of MySQL,
columns using prefixes were permitted when creating, altering, or upgrading a partitioned table, even
though they were not included in the table's partitioning key; in MySQL 8.4, this is no longer allowed
deprecated, and the server rejects any CREATE TABLE or ALTER TABLE statement affecting a
partitioned table in which one or more columns using prefixes occur with an error. See Column index
prefixes not supported for key partitioning.

Note

Tables using the NDB storage engine are implicitly partitioned by KEY, using
the table's primary key as the partitioning key (as with other MySQL storage
engines). In the event that the NDB Cluster table has no explicit primary key,
the “hidden” primary key generated by the NDB storage engine for each NDB
Cluster table is used as the partitioning key.

If you define an explicit partitioning scheme for an NDB table, the table
must have an explicit primary key, and any columns used in the partitioning
expression must be part of this key. However, if the table uses an “empty”
partitioning expression—that is, PARTITION BY KEY() with no column
references—then no explicit primary key is required.

You can observe this partitioning using the ndb_desc utility (with the -p
option).

Important

For a key-partitioned table, you cannot execute an ALTER TABLE DROP
PRIMARY KEY, as doing so generates the error ERROR 1466 (HY000):
Field in list of fields for partition function not found
in table. This is not an issue for NDB Cluster tables which are partitioned
by KEY; in such cases, the table is reorganized using the “hidden” primary key
as the table's new partitioning key. See Chapter 25, MySQL NDB Cluster 8.4.

It is also possible to partition a table by linear key. Here is a simple example:

CREATE TABLE tk (
    col1 INT NOT NULL,
    col2 CHAR(5),
    col3 DATE
)
PARTITION BY LINEAR KEY (col1)
PARTITIONS 3;

The LINEAR keyword has the same effect on KEY partitioning as it does on HASH partitioning, with the
partition number being derived using a powers-of-two algorithm rather than modulo arithmetic. See
Section 26.2.4.1, “LINEAR HASH Partitioning”, for a description of this algorithm and its implications.

26.2.6 Subpartitioning

4540

Subpartitioning

Subpartitioning—also known as composite partitioning—is the further division of each partition in a
partitioned table. Consider the following CREATE TABLE statement:

CREATE TABLE ts (id INT, purchased DATE)
    PARTITION BY RANGE( YEAR(purchased) )
    SUBPARTITION BY HASH( TO_DAYS(purchased) )
    SUBPARTITIONS 2 (
        PARTITION p0 VALUES LESS THAN (1990),
        PARTITION p1 VALUES LESS THAN (2000),
        PARTITION p2 VALUES LESS THAN MAXVALUE
    );

Table ts has 3 RANGE partitions. Each of these partitions—p0, p1, and p2—is further divided into
2 subpartitions. In effect, the entire table is divided into 3 * 2 = 6 partitions. However, due to the
action of the PARTITION BY RANGE clause, the first 2 of these store only those records with a value
less than 1990 in the purchased column.

It is possible to subpartition tables that are partitioned by RANGE or LIST. Subpartitions may use either
HASH or KEY partitioning. This is also known as composite partitioning.

Note

SUBPARTITION BY HASH and SUBPARTITION BY KEY generally follow
the same syntax rules as PARTITION BY HASH and PARTITION BY KEY,
respectively. An exception to this is that SUBPARTITION BY KEY (unlike
PARTITION BY KEY) does not currently support a default column, so the
column used for this purpose must be specified, even if the table has an explicit
primary key. This is a known issue which we are working to address; see Issues
with subpartitions, for more information and an example.

It is also possible to define subpartitions explicitly using SUBPARTITION clauses to specify options for
individual subpartitions. For example, a more verbose fashion of creating the same table ts as shown
in the previous example would be:

CREATE TABLE ts (id INT, purchased DATE)
    PARTITION BY RANGE( YEAR(purchased) )
    SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
        PARTITION p0 VALUES LESS THAN (1990) (
            SUBPARTITION s0,
            SUBPARTITION s1
        ),
        PARTITION p1 VALUES LESS THAN (2000) (
            SUBPARTITION s2,
            SUBPARTITION s3
        ),
        PARTITION p2 VALUES LESS THAN MAXVALUE (
            SUBPARTITION s4,
            SUBPARTITION s5
        )
    );

Some syntactical items of note are listed here:

• Each partition must have the same number of subpartitions.

• If you explicitly define any subpartitions using SUBPARTITION on any partition of a partitioned table,

you must define them all. In other words, the following statement fails:

CREATE TABLE ts (id INT, purchased DATE)
    PARTITION BY RANGE( YEAR(purchased) )
    SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
        PARTITION p0 VALUES LESS THAN (1990) (
            SUBPARTITION s0,
            SUBPARTITION s1
        ),

4541

How MySQL Partitioning Handles NULL

        PARTITION p1 VALUES LESS THAN (2000),
        PARTITION p2 VALUES LESS THAN MAXVALUE (
            SUBPARTITION s2,
            SUBPARTITION s3
        )
    );

This statement would still fail even if it used SUBPARTITIONS 2.

• Each SUBPARTITION clause must include (at a minimum) a name for the subpartition. Otherwise,
you may set any desired option for the subpartition or allow it to assume its default setting for that
option.

• Subpartition names must be unique across the entire table. For example, the following CREATE

TABLE statement is valid:

CREATE TABLE ts (id INT, purchased DATE)
    PARTITION BY RANGE( YEAR(purchased) )
    SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
        PARTITION p0 VALUES LESS THAN (1990) (
            SUBPARTITION s0,
            SUBPARTITION s1
        ),
        PARTITION p1 VALUES LESS THAN (2000) (
            SUBPARTITION s2,
            SUBPARTITION s3
        ),
        PARTITION p2 VALUES LESS THAN MAXVALUE (
            SUBPARTITION s4,
            SUBPARTITION s5
        )
    );

26.2.7 How MySQL Partitioning Handles NULL

Partitioning in MySQL does nothing to disallow NULL as the value of a partitioning expression, whether
it is a column value or the value of a user-supplied expression. Even though it is permitted to use
NULL as the value of an expression that must otherwise yield an integer, it is important to keep in mind
that NULL is not a number. MySQL's partitioning implementation treats NULL as being less than any
non-NULL value, just as ORDER BY does.

This means that treatment of NULL varies between partitioning of different types, and may produce
behavior which you do not expect if you are not prepared for it. This being the case, we discuss in
this section how each MySQL partitioning type handles NULL values when determining the partition in
which a row should be stored, and provide examples for each.

 If you insert a row into a table partitioned by RANGE
Handling of NULL with RANGE partitioning.
such that the column value used to determine the partition is NULL, the row is inserted into the lowest
partition. Consider these two tables in a database named p, created as follows:

mysql> CREATE TABLE t1 (
    ->     c1 INT,
    ->     c2 VARCHAR(20)
    -> )
    -> PARTITION BY RANGE(c1) (
    ->     PARTITION p0 VALUES LESS THAN (0),
    ->     PARTITION p1 VALUES LESS THAN (10),
    ->     PARTITION p2 VALUES LESS THAN MAXVALUE
    -> );
Query OK, 0 rows affected (0.09 sec)

mysql> CREATE TABLE t2 (
    ->     c1 INT,
    ->     c2 VARCHAR(20)
    -> )
    -> PARTITION BY RANGE(c1) (
    ->     PARTITION p0 VALUES LESS THAN (-5),

4542

How MySQL Partitioning Handles NULL

    ->     PARTITION p1 VALUES LESS THAN (0),
    ->     PARTITION p2 VALUES LESS THAN (10),
    ->     PARTITION p3 VALUES LESS THAN MAXVALUE
    -> );
Query OK, 0 rows affected (0.09 sec)

You can see the partitions created by these two CREATE TABLE statements using the following query
against the PARTITIONS table in the INFORMATION_SCHEMA database:

mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
     >   FROM INFORMATION_SCHEMA.PARTITIONS
     >   WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME LIKE 't_';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| t1         | p0             |          0 |              0 |           0 |
| t1         | p1             |          0 |              0 |           0 |
| t1         | p2             |          0 |              0 |           0 |
| t2         | p0             |          0 |              0 |           0 |
| t2         | p1             |          0 |              0 |           0 |
| t2         | p2             |          0 |              0 |           0 |
| t2         | p3             |          0 |              0 |           0 |
+------------+----------------+------------+----------------+-------------+
7 rows in set (0.00 sec)

(For more information about this table, see Section 28.3.21, “The INFORMATION_SCHEMA
PARTITIONS Table”.) Now let us populate each of these tables with a single row containing a NULL in
the column used as the partitioning key, and verify that the rows were inserted using a pair of SELECT
statements:

mysql> INSERT INTO t1 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t2 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM t1;
+------+--------+
| id   | name   |
+------+--------+
| NULL | mothra |
+------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM t2;
+------+--------+
| id   | name   |
+------+--------+
| NULL | mothra |
+------+--------+
1 row in set (0.00 sec)

You can see which partitions are used to store the inserted rows by rerunning the previous query
against INFORMATION_SCHEMA.PARTITIONS and inspecting the output:

mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
     >   FROM INFORMATION_SCHEMA.PARTITIONS
     >   WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME LIKE 't_';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| t1         | p0             |          1 |             20 |          20 |
| t1         | p1             |          0 |              0 |           0 |
| t1         | p2             |          0 |              0 |           0 |
| t2         | p0             |          1 |             20 |          20 |
| t2         | p1             |          0 |              0 |           0 |
| t2         | p2             |          0 |              0 |           0 |
| t2         | p3             |          0 |              0 |           0 |
+------------+----------------+------------+----------------+-------------+
7 rows in set (0.01 sec)

4543

How MySQL Partitioning Handles NULL

You can also demonstrate that these rows were stored in the lowest-numbered partition of each table
by dropping these partitions, and then re-running the SELECT statements:

mysql> ALTER TABLE t1 DROP PARTITION p0;
Query OK, 0 rows affected (0.16 sec)

mysql> ALTER TABLE t2 DROP PARTITION p0;
Query OK, 0 rows affected (0.16 sec)

mysql> SELECT * FROM t1;
Empty set (0.00 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)

(For more information on ALTER TABLE ... DROP PARTITION, see Section 15.1.9, “ALTER TABLE
Statement”.)

NULL is also treated in this way for partitioning expressions that use SQL functions. Suppose that we
define a table using a CREATE TABLE statement such as this one:

CREATE TABLE tndate (
    id INT,
    dt DATE
)
PARTITION BY RANGE( YEAR(dt) ) (
    PARTITION p0 VALUES LESS THAN (1990),
    PARTITION p1 VALUES LESS THAN (2000),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);

As with other MySQL functions, YEAR(NULL) returns NULL. A row with a dt column value of NULL is
treated as though the partitioning expression evaluated to a value less than any other value, and so is
inserted into partition p0.

Handling of NULL with LIST partitioning.
if and only if one of its partitions is defined using that value-list that contains NULL. The converse of
this is that a table partitioned by LIST which does not explicitly use NULL in a value list rejects rows
resulting in a NULL value for the partitioning expression, as shown in this example:

 A table that is partitioned by LIST admits NULL values

mysql> CREATE TABLE ts1 (
    ->     c1 INT,
    ->     c2 VARCHAR(20)
    -> )
    -> PARTITION BY LIST(c1) (
    ->     PARTITION p0 VALUES IN (0, 3, 6),
    ->     PARTITION p1 VALUES IN (1, 4, 7),
    ->     PARTITION p2 VALUES IN (2, 5, 8)
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO ts1 VALUES (9, 'mothra');
ERROR 1504 (HY000): Table has no partition for value 9

mysql> INSERT INTO ts1 VALUES (NULL, 'mothra');
ERROR 1504 (HY000): Table has no partition for value NULL

Only rows having a c1 value between 0 and 8 inclusive can be inserted into ts1. NULL falls outside
this range, just like the number 9. We can create tables ts2 and ts3 having value lists containing
NULL, as shown here:

mysql> CREATE TABLE ts2 (
    ->     c1 INT,
    ->     c2 VARCHAR(20)
    -> )
    -> PARTITION BY LIST(c1) (
    ->     PARTITION p0 VALUES IN (0, 3, 6),
    ->     PARTITION p1 VALUES IN (1, 4, 7),
    ->     PARTITION p2 VALUES IN (2, 5, 8),

4544

How MySQL Partitioning Handles NULL

    ->     PARTITION p3 VALUES IN (NULL)
    -> );
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE TABLE ts3 (
    ->     c1 INT,
    ->     c2 VARCHAR(20)
    -> )
    -> PARTITION BY LIST(c1) (
    ->     PARTITION p0 VALUES IN (0, 3, 6),
    ->     PARTITION p1 VALUES IN (1, 4, 7, NULL),
    ->     PARTITION p2 VALUES IN (2, 5, 8)
    -> );
Query OK, 0 rows affected (0.01 sec)

When defining value lists for partitioning, you can (and should) treat NULL just as you would any other
value. For example, both VALUES IN (NULL) and VALUES IN (1, 4, 7, NULL) are valid, as are
VALUES IN (1, NULL, 4, 7), VALUES IN (NULL, 1, 4, 7), and so on. You can insert a row
having NULL for column c1 into each of the tables ts2 and ts3:

mysql> INSERT INTO ts2 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO ts3 VALUES (NULL, 'mothra');
Query OK, 1 row affected (0.00 sec)

By issuing the appropriate query against INFORMATION_SCHEMA.PARTITIONS, you can determine
which partitions were used to store the rows just inserted (we assume, as in the previous examples,
that the partitioned tables were created in the p database):

mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
     >   FROM INFORMATION_SCHEMA.PARTITIONS
     >   WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME LIKE 'ts_';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| ts2        | p0             |          0 |              0 |           0 |
| ts2        | p1             |          0 |              0 |           0 |
| ts2        | p2             |          0 |              0 |           0 |
| ts2        | p3             |          1 |             20 |          20 |
| ts3        | p0             |          0 |              0 |           0 |
| ts3        | p1             |          1 |             20 |          20 |
| ts3        | p2             |          0 |              0 |           0 |
+------------+----------------+------------+----------------+-------------+
7 rows in set (0.01 sec)

As shown earlier in this section, you can also verify which partitions were used for storing the rows by
deleting these partitions and then performing a SELECT.

 NULL is handled somewhat differently for
Handling of NULL with HASH and KEY partitioning.
tables partitioned by HASH or KEY. In these cases, any partition expression that yields a NULL value
is treated as though its return value were zero. We can verify this behavior by examining the effects
on the file system of creating a table partitioned by HASH and populating it with a record containing
appropriate values. Suppose that you have a table th (also in the p database) created using the
following statement:

mysql> CREATE TABLE th (
    ->     c1 INT,
    ->     c2 VARCHAR(20)
    -> )
    -> PARTITION BY HASH(c1)
    -> PARTITIONS 2;
Query OK, 0 rows affected (0.00 sec)

The partitions belonging to this table can be viewed using the query shown here:

mysql> SELECT TABLE_NAME,PARTITION_NAME,TABLE_ROWS,AVG_ROW_LENGTH,DATA_LENGTH
     >   FROM INFORMATION_SCHEMA.PARTITIONS
     >   WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME ='th';

4545

Partition Management

+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| th         | p0             |          0 |              0 |           0 |
| th         | p1             |          0 |              0 |           0 |
+------------+----------------+------------+----------------+-------------+
2 rows in set (0.00 sec)

TABLE_ROWS for each partition is 0. Now insert two rows into th whose c1 column values are NULL
and 0, and verify that these rows were inserted, as shown here:

mysql> INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM th;
+------+---------+
| c1   | c2      |
+------+---------+
| NULL | mothra  |
+------+---------+
|    0 | gigan   |
+------+---------+
2 rows in set (0.01 sec)

Recall that for any integer N, the value of NULL MOD N is always NULL. For tables that are partitioned
by HASH or KEY, this result is treated for determining the correct partition as 0. Checking the
Information Schema PARTITIONS table once again, we can see that both rows were inserted into
partition p0:

mysql> SELECT TABLE_NAME, PARTITION_NAME, TABLE_ROWS, AVG_ROW_LENGTH, DATA_LENGTH
     >   FROM INFORMATION_SCHEMA.PARTITIONS
     >   WHERE TABLE_SCHEMA = 'p' AND TABLE_NAME ='th';
+------------+----------------+------------+----------------+-------------+
| TABLE_NAME | PARTITION_NAME | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH |
+------------+----------------+------------+----------------+-------------+
| th         | p0             |          2 |             20 |          20 |
| th         | p1             |          0 |              0 |           0 |
+------------+----------------+------------+----------------+-------------+
2 rows in set (0.00 sec)

By repeating the last example using PARTITION BY KEY in place of PARTITION BY HASH in the
definition of the table, you can verify that NULL is also treated like 0 for this type of partitioning.

26.3 Partition Management

There are a number of ways using SQL statements to modify partitioned tables; it is possible to add,
drop, redefine, merge, or split existing partitions using the partitioning extensions to the ALTER TABLE
statement. There are also ways to obtain information about partitioned tables and partitions. We
discuss these topics in the sections that follow.

• For information about partition management in tables partitioned by RANGE or LIST, see

Section 26.3.1, “Management of RANGE and LIST Partitions”.

• For a discussion of managing HASH and KEY partitions, see Section 26.3.2, “Management of HASH

and KEY Partitions”.

• See Section 26.3.5, “Obtaining Information About Partitions”, for a discussion of mechanisms

provided in MySQL 8.4 for obtaining information about partitioned tables and partitions.

• For a discussion of performing maintenance operations on partitions, see Section 26.3.4,

“Maintenance of Partitions”.

Note

All partitions of a partitioned table must have the same number of subpartitions;
it is not possible to change the subpartitioning once the table has been created.

4546

Management of RANGE and LIST Partitions

To change a table's partitioning scheme, it is necessary only to use the ALTER TABLE statement with
a partition_options option, which has the same syntax as that as used with CREATE TABLE
for creating a partitioned table; this option (also) always begins with the keywords PARTITION BY.
Suppose that the following CREATE TABLE statement was used to create a table that is partitioned by
range:

CREATE TABLE trb3 (id INT, name VARCHAR(50), purchased DATE)
    PARTITION BY RANGE( YEAR(purchased) ) (
        PARTITION p0 VALUES LESS THAN (1990),
        PARTITION p1 VALUES LESS THAN (1995),
        PARTITION p2 VALUES LESS THAN (2000),
        PARTITION p3 VALUES LESS THAN (2005)
    );

To repartition this table so that it is partitioned by key into two partitions using the id column value as
the basis for the key, you can use this statement:

ALTER TABLE trb3 PARTITION BY KEY(id) PARTITIONS 2;

This has the same effect on the structure of the table as dropping the table and re-creating it using
CREATE TABLE trb3 PARTITION BY KEY(id) PARTITIONS 2;.

ALTER TABLE ... ENGINE [=] ... changes only the storage engine used by the table, and
leaves the table's partitioning scheme intact. The statement succeeds only if the target storage engine
provides partitioning support. You can use ALTER TABLE ... REMOVE PARTITIONING to remove a
table's partitioning; see Section 15.1.9, “ALTER TABLE Statement”.

Important

Only a single PARTITION BY, ADD PARTITION, DROP PARTITION,
REORGANIZE PARTITION, or COALESCE PARTITION clause can be used in a
given ALTER TABLE statement. If you (for example) wish to drop a partition and
reorganize a table's remaining partitions, you must do so in two separate ALTER
TABLE statements (one using DROP PARTITION and then a second one using
REORGANIZE PARTITION).

You can delete all rows from one or more selected partitions using ALTER TABLE ... TRUNCATE
PARTITION.

26.3.1 Management of RANGE and LIST Partitions

Adding and dropping of range and list partitions are handled in a similar fashion, so we discuss the
management of both sorts of partitioning in this section. For information about working with tables that
are partitioned by hash or key, see Section 26.3.2, “Management of HASH and KEY Partitions”.

Dropping a partition from a table that is partitioned by either RANGE or by LIST can be accomplished
using the ALTER TABLE statement with the DROP PARTITION option. Suppose that you have created
a table that is partitioned by range and then populated with 10 records using the following CREATE
TABLE and INSERT statements:

mysql> CREATE TABLE tr (id INT, name VARCHAR(50), purchased DATE)
    ->     PARTITION BY RANGE( YEAR(purchased) ) (
    ->         PARTITION p0 VALUES LESS THAN (1990),
    ->         PARTITION p1 VALUES LESS THAN (1995),
    ->         PARTITION p2 VALUES LESS THAN (2000),
    ->         PARTITION p3 VALUES LESS THAN (2005),
    ->         PARTITION p4 VALUES LESS THAN (2010),
    ->         PARTITION p5 VALUES LESS THAN (2015)
    ->     );
Query OK, 0 rows affected (0.28 sec)

mysql> INSERT INTO tr VALUES
    ->     (1, 'desk organiser', '2003-10-15'),
    ->     (2, 'alarm clock', '1997-11-05'),

4547

Management of RANGE and LIST Partitions

If you wish to drop all data from all partitions while preserving the table definition and its partitioning
scheme, use the TRUNCATE TABLE statement. (See Section 15.1.37, “TRUNCATE TABLE
Statement”.)

If you intend to change the partitioning of a table without losing data, use ALTER TABLE ...
REORGANIZE PARTITION instead. See below or in Section 15.1.9, “ALTER TABLE Statement”, for
information about REORGANIZE PARTITION.

If you now execute a SHOW CREATE TABLE statement, you can see how the partitioning makeup of
the table has been changed:

mysql> SHOW CREATE TABLE tr\G
*************************** 1. row ***************************
       Table: tr
Create Table: CREATE TABLE `tr` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `purchased` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE ( YEAR(purchased))
(PARTITION p0 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1995) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2005) ENGINE = InnoDB,
 PARTITION p4 VALUES LESS THAN (2010) ENGINE = InnoDB,
 PARTITION p5 VALUES LESS THAN (2015) ENGINE = InnoDB) */
1 row in set (0.00 sec)

When you insert new rows into the changed table with purchased column values between
'1995-01-01' and '2004-12-31' inclusive, those rows are stored in partition p3. You can verify
this as follows:

mysql> INSERT INTO tr VALUES (11, 'pencil holder', '1995-07-12');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM tr WHERE purchased
    -> BETWEEN '1995-01-01' AND '2004-12-31';
+------+----------------+------------+
| id   | name           | purchased  |
+------+----------------+------------+
|    1 | desk organiser | 2003-10-15 |
|   11 | pencil holder  | 1995-07-12 |
+------+----------------+------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE tr DROP PARTITION p3;
Query OK, 0 rows affected (0.03 sec)

mysql> SELECT * FROM tr WHERE purchased
    -> BETWEEN '1995-01-01' AND '2004-12-31';
Empty set (0.00 sec)

The number of rows dropped from the table as a result of ALTER TABLE ... DROP PARTITION is
not reported by the server as it would be by the equivalent DELETE query.

Dropping LIST partitions uses exactly the same ALTER TABLE ... DROP PARTITION syntax as
used for dropping RANGE partitions. However, there is one important difference in the effect this has
on your use of the table afterward: You can no longer insert into the table any rows having any of the
values that were included in the value list defining the deleted partition. (See Section 26.2.2, “LIST
Partitioning”, for an example.)

To add a new range or list partition to a previously partitioned table, use the ALTER TABLE ... ADD
PARTITION statement. For tables which are partitioned by RANGE, this can be used to add a new
range to the end of the list of existing partitions. Suppose that you have a partitioned table containing
membership data for your organization, which is defined as follows:

CREATE TABLE members (
    id INT,

4549

Management of RANGE and LIST Partitions

    fname VARCHAR(25),
    lname VARCHAR(25),
    dob DATE
)
PARTITION BY RANGE( YEAR(dob) ) (
    PARTITION p0 VALUES LESS THAN (1980),
    PARTITION p1 VALUES LESS THAN (1990),
    PARTITION p2 VALUES LESS THAN (2000)
);

Suppose further that the minimum age for members is 16. As the calendar approaches the end of
2015, you realize that you must soon be prepared to admit members who were born in 2000 (and
later). You can modify the members table to accommodate new members born in the years 2000 to
2010 as shown here:

ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));

With tables that are partitioned by range, you can use ADD PARTITION to add new partitions to the
high end of the partitions list only. Trying to add a new partition in this manner between or before
existing partitions results in an error as shown here:

mysql> ALTER TABLE members
     >     ADD PARTITION (
     >     PARTITION n VALUES LESS THAN (1970));
ERROR 1463 (HY000): VALUES LESS THAN value must be strictly »
   increasing for each partition

You can work around this problem by reorganizing the first partition into two new ones that split the
range between them, like this:

ALTER TABLE members
    REORGANIZE PARTITION p0 INTO (
        PARTITION n0 VALUES LESS THAN (1970),
        PARTITION n1 VALUES LESS THAN (1980)
);

Using SHOW CREATE TABLE you can see that the ALTER TABLE statement has had the desired
effect:

mysql> SHOW CREATE TABLE members\G
*************************** 1. row ***************************
       Table: members
Create Table: CREATE TABLE `members` (
  `id` int(11) DEFAULT NULL,
  `fname` varchar(25) DEFAULT NULL,
  `lname` varchar(25) DEFAULT NULL,
  `dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE ( YEAR(dob))
(PARTITION n0 VALUES LESS THAN (1970) ENGINE = InnoDB,
 PARTITION n1 VALUES LESS THAN (1980) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (2000) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2010) ENGINE = InnoDB) */
1 row in set (0.00 sec)

See also Section 15.1.9.1, “ALTER TABLE Partition Operations”.

You can also use ALTER TABLE ... ADD PARTITION to add new partitions to a table that is
partitioned by LIST. Suppose a table tt is defined using the following CREATE TABLE statement:

CREATE TABLE tt (
    id INT,
    data INT
)
PARTITION BY LIST(data) (
    PARTITION p0 VALUES IN (5, 10, 15),
    PARTITION p1 VALUES IN (6, 12, 18)
);

4550

Management of RANGE and LIST Partitions

You can add a new partition in which to store rows having the data column values 7, 14, and 21 as
shown:

ALTER TABLE tt ADD PARTITION (PARTITION p2 VALUES IN (7, 14, 21));

Keep in mind that you cannot add a new LIST partition encompassing any values that are already
included in the value list of an existing partition. If you attempt to do so, an error results:

mysql> ALTER TABLE tt ADD PARTITION
     >     (PARTITION np VALUES IN (4, 8, 12));
ERROR 1465 (HY000): Multiple definition of same constant »
                    in list partitioning

Because any rows with the data column value 12 have already been assigned to partition p1, you
cannot create a new partition on table tt that includes 12 in its value list. To accomplish this, you could
drop p1, and add np and then a new p1 with a modified definition. However, as discussed earlier, this
would result in the loss of all data stored in p1—and it is often the case that this is not what you really
want to do. Another solution might appear to be to make a copy of the table with the new partitioning
and to copy the data into it using CREATE TABLE ... SELECT ..., then drop the old table and
rename the new one, but this could be very time-consuming when dealing with a large amounts of
data. This also might not be feasible in situations where high availability is a requirement.

You can add multiple partitions in a single ALTER TABLE ... ADD PARTITION statement as shown
here:

CREATE TABLE employees (
  id INT NOT NULL,
  fname VARCHAR(50) NOT NULL,
  lname VARCHAR(50) NOT NULL,
  hired DATE NOT NULL
)
PARTITION BY RANGE( YEAR(hired) ) (
  PARTITION p1 VALUES LESS THAN (1991),
  PARTITION p2 VALUES LESS THAN (1996),
  PARTITION p3 VALUES LESS THAN (2001),
  PARTITION p4 VALUES LESS THAN (2005)
);

ALTER TABLE employees ADD PARTITION (
    PARTITION p5 VALUES LESS THAN (2010),
    PARTITION p6 VALUES LESS THAN MAXVALUE
);

Fortunately, MySQL's partitioning implementation provides ways to redefine partitions without losing
data. Let us look first at a couple of simple examples involving RANGE partitioning. Recall the members
table which is now defined as shown here:

mysql> SHOW CREATE TABLE members\G
*************************** 1. row ***************************
       Table: members
Create Table: CREATE TABLE `members` (
  `id` int(11) DEFAULT NULL,
  `fname` varchar(25) DEFAULT NULL,
  `lname` varchar(25) DEFAULT NULL,
  `dob` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE ( YEAR(dob))
(PARTITION n0 VALUES LESS THAN (1970) ENGINE = InnoDB,
 PARTITION n1 VALUES LESS THAN (1980) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (2000) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2010) ENGINE = InnoDB) */
1 row in set (0.00 sec)

Suppose that you would like to move all rows representing members born before 1960 into a separate
partition. As we have already seen, this cannot be done using ALTER TABLE ... ADD PARTITION.
However, you can use another partition-related extension to ALTER TABLE to accomplish this:

4551

Management of RANGE and LIST Partitions

ALTER TABLE members REORGANIZE PARTITION n0 INTO (
    PARTITION s0 VALUES LESS THAN (1960),
    PARTITION s1 VALUES LESS THAN (1970)
);

In effect, this command splits partition n0 into two new partitions s0 and s1. It also moves the data that
was stored in n0 into the new partitions according to the rules embodied in the two PARTITION ...
VALUES ... clauses, so that s0 contains only those records for which YEAR(dob) is less than 1960
and s1 contains those rows in which YEAR(dob) is greater than or equal to 1960 but less than 1970.

A REORGANIZE PARTITION clause may also be used for merging adjacent partitions. You can
reverse the effect of the previous statement on the members table as shown here:

ALTER TABLE members REORGANIZE PARTITION s0,s1 INTO (
    PARTITION p0 VALUES LESS THAN (1970)
);

No data is lost in splitting or merging partitions using REORGANIZE PARTITION. In executing the
above statement, MySQL moves all of the records that were stored in partitions s0 and s1 into partition
p0.

The general syntax for REORGANIZE PARTITION is shown here:

ALTER TABLE tbl_name
    REORGANIZE PARTITION partition_list
    INTO (partition_definitions);

Here, tbl_name is the name of the partitioned table, and partition_list is a comma-separated
list of names of one or more existing partitions to be changed. partition_definitions
is a comma-separated list of new partition definitions, which follow the same rules as for the
partition_definitions list used in CREATE TABLE. You are not limited to merging several
partitions into one, or to splitting one partition into many, when using REORGANIZE PARTITION. For
example, you can reorganize all four partitions of the members table into two, like this:

ALTER TABLE members REORGANIZE PARTITION p0,p1,p2,p3 INTO (
    PARTITION m0 VALUES LESS THAN (1980),
    PARTITION m1 VALUES LESS THAN (2000)
);

You can also use REORGANIZE PARTITION with tables that are partitioned by LIST. Let us return
to the problem of adding a new partition to the list-partitioned tt table and failing because the new
partition had a value that was already present in the value-list of one of the existing partitions. We can
handle this by adding a partition that contains only nonconflicting values, and then reorganizing the
new partition and the existing one so that the value which was stored in the existing one is now moved
to the new one:

ALTER TABLE tt ADD PARTITION (PARTITION np VALUES IN (4, 8));
ALTER TABLE tt REORGANIZE PARTITION p1,np INTO (
    PARTITION p1 VALUES IN (6, 18),
    PARTITION np VALUES in (4, 8, 12)
);

Here are some key points to keep in mind when using ALTER TABLE ... REORGANIZE PARTITION
to repartition tables that are partitioned by RANGE or LIST:

• The PARTITION options used to determine the new partitioning scheme are subject to the same

rules as those used with a CREATE TABLE statement.

A new RANGE partitioning scheme cannot have any overlapping ranges; a new LIST partitioning
scheme cannot have any overlapping sets of values.

• The combination of partitions in the partition_definitions list should account for the same

range or set of values overall as the combined partitions named in the partition_list.

4552

Management of HASH and KEY Partitions

For example, partitions p1 and p2 together cover the years 1980 through 1999 in the members table
used as an example in this section. Any reorganization of these two partitions should cover the same
range of years overall.

• For tables partitioned by RANGE, you can reorganize only adjacent partitions; you cannot skip range

partitions.

For instance, you could not reorganize the example members table using a statement beginning with
ALTER TABLE members REORGANIZE PARTITION p0,p2 INTO ... because p0 covers the
years prior to 1970 and p2 the years from 1990 through 1999 inclusive, so these are not adjacent
partitions. (You cannot skip partition p1 in this case.)

• You cannot use REORGANIZE PARTITION to change the type of partitioning used by the table (for
example, you cannot change RANGE partitions to HASH partitions or the reverse). You also cannot
use this statement to change the partitioning expression or column. To accomplish either of these
tasks without dropping and re-creating the table, you can use ALTER TABLE ... PARTITION
BY ..., as shown here:

ALTER TABLE members
    PARTITION BY HASH( YEAR(dob) )
    PARTITIONS 8;

26.3.2 Management of HASH and KEY Partitions

Tables which are partitioned by hash or by key are very similar to one another with regard to making
changes in a partitioning setup, and both differ in a number of ways from tables which have been
partitioned by range or list. For that reason, this section addresses the modification of tables partitioned
by hash or by key only. For a discussion of adding and dropping of partitions of tables that are
partitioned by range or list, see Section 26.3.1, “Management of RANGE and LIST Partitions”.

You cannot drop partitions from tables that are partitioned by HASH or KEY in the same way that
you can from tables that are partitioned by RANGE or LIST. However, you can merge HASH or KEY
partitions using ALTER TABLE ... COALESCE PARTITION. Suppose that a clients table
containing data about clients is divided into 12 partitions, created as shown here:

CREATE TABLE clients (
    id INT,
    fname VARCHAR(30),
    lname VARCHAR(30),
    signed DATE
)
PARTITION BY HASH( MONTH(signed) )
PARTITIONS 12;

To reduce the number of partitions from 12 to 8, execute the following ALTER TABLE statement:

mysql> ALTER TABLE clients COALESCE PARTITION 4;
Query OK, 0 rows affected (0.02 sec)

COALESCE works equally well with tables that are partitioned by HASH, KEY, LINEAR HASH, or LINEAR
KEY. Here is an example similar to the previous one, differing only in that the table is partitioned by
LINEAR KEY:

mysql> CREATE TABLE clients_lk (
    ->     id INT,
    ->     fname VARCHAR(30),
    ->     lname VARCHAR(30),
    ->     signed DATE
    -> )
    -> PARTITION BY LINEAR KEY(signed)
    -> PARTITIONS 12;
Query OK, 0 rows affected (0.03 sec)

mysql> ALTER TABLE clients_lk COALESCE PARTITION 4;

4553

Exchanging Partitions and Subpartitions with Tables

The syntax for ALTER TABLE ... EXCHANGE PARTITION is shown here, where pt is the
partitioned table, p is the partition (or subpartition) to be exchanged, and nt is the nonpartitioned table
to be exchanged with p:

ALTER TABLE pt
    EXCHANGE PARTITION p
    WITH TABLE nt;

Optionally, you can append WITH VALIDATION or WITHOUT VALIDATION. When WITHOUT
VALIDATION is specified, the ALTER TABLE ... EXCHANGE PARTITION operation does not
perform any row-by-row validation when exchanging a partition a nonpartitioned table, allowing
database administrators to assume responsibility for ensuring that rows are within the boundaries of
the partition definition. WITH VALIDATION is the default.

One and only one partition or subpartition may be exchanged with one and only one nonpartitioned
table in a single ALTER TABLE EXCHANGE PARTITION statement. To exchange multiple partitions
or subpartitions, use multiple ALTER TABLE EXCHANGE PARTITION statements. EXCHANGE
PARTITION may not be combined with other ALTER TABLE options. The partitioning and (if
applicable) subpartitioning used by the partitioned table may be of any type or types supported in
MySQL 8.4.

Exchanging a Partition with a Nonpartitioned Table

Suppose that a partitioned table e has been created and populated using the following SQL
statements:

CREATE TABLE e (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30)
)
    PARTITION BY RANGE (id) (
        PARTITION p0 VALUES LESS THAN (50),
        PARTITION p1 VALUES LESS THAN (100),
        PARTITION p2 VALUES LESS THAN (150),
        PARTITION p3 VALUES LESS THAN (MAXVALUE)
);

INSERT INTO e VALUES
    (1669, "Jim", "Smith"),
    (337, "Mary", "Jones"),
    (16, "Frank", "White"),
    (2005, "Linda", "Black");

Now we create a nonpartitioned copy of e named e2. This can be done using the mysql client as
shown here:

mysql> CREATE TABLE e2 LIKE e;
Query OK, 0 rows affected (0.04 sec)

mysql> ALTER TABLE e2 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.07 sec)
Records: 0  Duplicates: 0  Warnings: 0

You can see which partitions in table e contain rows by querying the Information Schema PARTITIONS
table, like this:

mysql> SELECT PARTITION_NAME, TABLE_ROWS
           FROM INFORMATION_SCHEMA.PARTITIONS
           WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          1 |
| p1             |          0 |
| p2             |          0 |
| p3             |          3 |

4555

Exchanging Partitions and Subpartitions with Tables

+----------------+------------+
2 rows in set (0.00 sec)

Note

For partitioned InnoDB tables, the row count given in the TABLE_ROWS column
of the Information Schema PARTITIONS table is only an estimated value used
in SQL optimization, and is not always exact.

To exchange partition p0 in table e with table e2, you can use ALTER TABLE, as shown here:

mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
Query OK, 0 rows affected (0.04 sec)

More precisely, the statement just issued causes any rows found in the partition to be swapped with
those found in the table. You can observe how this has happened by querying the Information Schema
PARTITIONS table, as before. The table row that was previously found in partition p0 is no longer
present:

mysql> SELECT PARTITION_NAME, TABLE_ROWS
           FROM INFORMATION_SCHEMA.PARTITIONS
           WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          0 |
| p1             |          0 |
| p2             |          0 |
| p3             |          3 |
+----------------+------------+
4 rows in set (0.00 sec)

If you query table e2, you can see that the “missing” row can now be found there:

mysql> SELECT * FROM e2;
+----+-------+-------+
| id | fname | lname |
+----+-------+-------+
| 16 | Frank | White |
+----+-------+-------+
1 row in set (0.00 sec)

The table to be exchanged with the partition does not necessarily have to be empty. To demonstrate
this, we first insert a new row into table e, making sure that this row is stored in partition p0 by
choosing an id column value that is less than 50, and verifying this afterward by querying the
PARTITIONS table:

mysql> INSERT INTO e VALUES (41, "Michael", "Green");
Query OK, 1 row affected (0.05 sec)

mysql> SELECT PARTITION_NAME, TABLE_ROWS
           FROM INFORMATION_SCHEMA.PARTITIONS
           WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          1 |
| p1             |          0 |
| p2             |          0 |
| p3             |          3 |
+----------------+------------+
4 rows in set (0.00 sec)

Now we once again exchange partition p0 with table e2 using the same ALTER TABLE statement as
previously:

mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
Query OK, 0 rows affected (0.28 sec)

4556

Exchanging Partitions and Subpartitions with Tables

The output of the following queries shows that the table row that was stored in partition p0 and the
table row that was stored in table e2, prior to issuing the ALTER TABLE statement, have now switched
places:

mysql> SELECT * FROM e;
+------+-------+-------+
| id   | fname | lname |
+------+-------+-------+
|   16 | Frank | White |
| 1669 | Jim   | Smith |
|  337 | Mary  | Jones |
| 2005 | Linda | Black |
+------+-------+-------+
4 rows in set (0.00 sec)

mysql> SELECT PARTITION_NAME, TABLE_ROWS
           FROM INFORMATION_SCHEMA.PARTITIONS
           WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          1 |
| p1             |          0 |
| p2             |          0 |
| p3             |          3 |
+----------------+------------+
4 rows in set (0.00 sec)

mysql> SELECT * FROM e2;
+----+---------+-------+
| id | fname   | lname |
+----+---------+-------+
| 41 | Michael | Green |
+----+---------+-------+
1 row in set (0.00 sec)

Nonmatching Rows

You should keep in mind that any rows found in the nonpartitioned table prior to issuing the ALTER
TABLE ... EXCHANGE PARTITION statement must meet the conditions required for them to be
stored in the target partition; otherwise, the statement fails. To see how this occurs, first insert a row
into e2 that is outside the boundaries of the partition definition for partition p0 of table e. For example,
insert a row with an id column value that is too large; then, try to exchange the table with the partition
again:

mysql> INSERT INTO e2 VALUES (51, "Ellen", "McDonald");
Query OK, 1 row affected (0.08 sec)

mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2;
ERROR 1707 (HY000): Found row that does not match the partition

Only the WITHOUT VALIDATION option would permit this operation to succeed:

mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2 WITHOUT VALIDATION;
Query OK, 0 rows affected (0.02 sec)

When a partition is exchanged with a table that contains rows that do not match the partition definition,
it is the responsibility of the database administrator to fix the non-matching rows, which can be
performed using REPAIR TABLE or ALTER TABLE ... REPAIR PARTITION.

Exchanging Partitions Without Row-By-Row Validation

To avoid time consuming validation when exchanging a partition with a table that has many rows, it is
possible to skip the row-by-row validation step by appending WITHOUT VALIDATION to the ALTER
TABLE ... EXCHANGE PARTITION statement.

The following example compares the difference between execution times when exchanging a partition
with a nonpartitioned table, with and without validation. The partitioned table (table e) contains two

4557

Exchanging Partitions and Subpartitions with Tables

partitions of 1 million rows each. The rows in p0 of table e are removed and p0 is exchanged with
a nonpartitioned table of 1 million rows. The WITH VALIDATION operation takes 0.74 seconds. By
comparison, the WITHOUT VALIDATION operation takes 0.01 seconds.

# Create a partitioned table with 1 million rows in each partition

CREATE TABLE e (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30)
)
    PARTITION BY RANGE (id) (
        PARTITION p0 VALUES LESS THAN (1000001),
        PARTITION p1 VALUES LESS THAN (2000001),
);

mysql> SELECT COUNT(*) FROM e;
| COUNT(*) |
+----------+
|  2000000 |
+----------+
1 row in set (0.27 sec)

# View the rows in each partition

SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+-------------+
| PARTITION_NAME | TABLE_ROWS  |
+----------------+-------------+
| p0             |     1000000 |
| p1             |     1000000 |
+----------------+-------------+
2 rows in set (0.00 sec)

# Create a nonpartitioned table of the same structure and populate it with 1 million rows

CREATE TABLE e2 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30)
);

mysql> SELECT COUNT(*) FROM e2;
+----------+
| COUNT(*) |
+----------+
|  1000000 |
+----------+
1 row in set (0.24 sec)

# Create another nonpartitioned table of the same structure and populate it with 1 million rows

CREATE TABLE e3 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30)
);

mysql> SELECT COUNT(*) FROM e3;
+----------+
| COUNT(*) |
+----------+
|  1000000 |
+----------+
1 row in set (0.25 sec)

# Drop the rows from p0 of table e

mysql> DELETE FROM e WHERE id < 1000001;
Query OK, 1000000 rows affected (5.55 sec)

# Confirm that there are no rows in partition p0

4558

Exchanging Partitions and Subpartitions with Tables

mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          0 |
| p1             |    1000000 |
+----------------+------------+
2 rows in set (0.00 sec)

# Exchange partition p0 of table e with the table e2 'WITH VALIDATION'

mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e2 WITH VALIDATION;
Query OK, 0 rows affected (0.74 sec)

# Confirm that the partition was exchanged with table e2

mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |    1000000 |
| p1             |    1000000 |
+----------------+------------+
2 rows in set (0.00 sec)

# Once again, drop the rows from p0 of table e

mysql> DELETE FROM e WHERE id < 1000001;
Query OK, 1000000 rows affected (5.55 sec)

# Confirm that there are no rows in partition p0

mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |          0 |
| p1             |    1000000 |
+----------------+------------+
2 rows in set (0.00 sec)

# Exchange partition p0 of table e with the table e3 'WITHOUT VALIDATION'

mysql> ALTER TABLE e EXCHANGE PARTITION p0 WITH TABLE e3 WITHOUT VALIDATION;
Query OK, 0 rows affected (0.01 sec)

# Confirm that the partition was exchanged with table e3

mysql> SELECT PARTITION_NAME, TABLE_ROWS FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME = 'e';
+----------------+------------+
| PARTITION_NAME | TABLE_ROWS |
+----------------+------------+
| p0             |    1000000 |
| p1             |    1000000 |
+----------------+------------+
2 rows in set (0.00 sec)

If a partition is exchanged with a table that contains rows that do not match the partition definition, it is
the responsibility of the database administrator to fix the non-matching rows, which can be performed
using REPAIR TABLE or ALTER TABLE ... REPAIR PARTITION.

Exchanging a Subpartition with a Nonpartitioned Table

You can also exchange a subpartition of a subpartitioned table (see Section 26.2.6, “Subpartitioning”)
with a nonpartitioned table using an ALTER TABLE ... EXCHANGE PARTITION statement. In the
following example, we first create a table es that is partitioned by RANGE and subpartitioned by KEY,
populate this table as we did table e, and then create an empty, nonpartitioned copy es2 of the table,
as shown here:

4559

Exchanging Partitions and Subpartitions with Tables

mysql> CREATE TABLE es (
    ->     id INT NOT NULL,
    ->     fname VARCHAR(30),
    ->     lname VARCHAR(30)
    -> )
    ->     PARTITION BY RANGE (id)
    ->     SUBPARTITION BY KEY (lname)
    ->     SUBPARTITIONS 2 (
    ->         PARTITION p0 VALUES LESS THAN (50),
    ->         PARTITION p1 VALUES LESS THAN (100),
    ->         PARTITION p2 VALUES LESS THAN (150),
    ->         PARTITION p3 VALUES LESS THAN (MAXVALUE)
    ->     );
Query OK, 0 rows affected (2.76 sec)

mysql> INSERT INTO es VALUES
    ->     (1669, "Jim", "Smith"),
    ->     (337, "Mary", "Jones"),
    ->     (16, "Frank", "White"),
    ->     (2005, "Linda", "Black");
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> CREATE TABLE es2 LIKE es;
Query OK, 0 rows affected (1.27 sec)

mysql> ALTER TABLE es2 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.70 sec)
Records: 0  Duplicates: 0  Warnings: 0

Although we did not explicitly name any of the subpartitions when creating table es, we can obtain
generated names for these by including the SUBPARTITION_NAME column of the PARTITIONS table
from INFORMATION_SCHEMA when selecting from that table, as shown here:

mysql> SELECT PARTITION_NAME, SUBPARTITION_NAME, TABLE_ROWS
    ->     FROM INFORMATION_SCHEMA.PARTITIONS
    ->     WHERE TABLE_NAME = 'es';
+----------------+-------------------+------------+
| PARTITION_NAME | SUBPARTITION_NAME | TABLE_ROWS |
+----------------+-------------------+------------+
| p0             | p0sp0             |          1 |
| p0             | p0sp1             |          0 |
| p1             | p1sp0             |          0 |
| p1             | p1sp1             |          0 |
| p2             | p2sp0             |          0 |
| p2             | p2sp1             |          0 |
| p3             | p3sp0             |          3 |
| p3             | p3sp1             |          0 |
+----------------+-------------------+------------+
8 rows in set (0.00 sec)

The following ALTER TABLE statement exchanges subpartition p3sp0 in table es with the
nonpartitioned table es2:

mysql> ALTER TABLE es EXCHANGE PARTITION p3sp0 WITH TABLE es2;
Query OK, 0 rows affected (0.29 sec)

You can verify that the rows were exchanged by issuing the following queries:

mysql> SELECT PARTITION_NAME, SUBPARTITION_NAME, TABLE_ROWS
    ->     FROM INFORMATION_SCHEMA.PARTITIONS
    ->     WHERE TABLE_NAME = 'es';
+----------------+-------------------+------------+
| PARTITION_NAME | SUBPARTITION_NAME | TABLE_ROWS |
+----------------+-------------------+------------+
| p0             | p0sp0             |          1 |
| p0             | p0sp1             |          0 |
| p1             | p1sp0             |          0 |
| p1             | p1sp1             |          0 |
| p2             | p2sp0             |          0 |
| p2             | p2sp1             |          0 |

4560

Maintenance of Partitions

| p3             | p3sp0             |          0 |
| p3             | p3sp1             |          0 |
+----------------+-------------------+------------+
8 rows in set (0.00 sec)

mysql> SELECT * FROM es2;
+------+-------+-------+
| id   | fname | lname |
+------+-------+-------+
| 1669 | Jim   | Smith |
|  337 | Mary  | Jones |
| 2005 | Linda | Black |
+------+-------+-------+
3 rows in set (0.00 sec)

If a table is subpartitioned, you can exchange only a subpartition of the table—not an entire partition—
with an unpartitioned table, as shown here:

mysql> ALTER TABLE es EXCHANGE PARTITION p3 WITH TABLE es2;
ERROR 1704 (HY000): Subpartitioned table, use subpartition instead of partition

Table structures are compared in a strict fashion; the number, order, names, and types of columns
and indexes of the partitioned table and the nonpartitioned table must match exactly. In addition, both
tables must use the same storage engine:

mysql> CREATE TABLE es3 LIKE e;
Query OK, 0 rows affected (1.31 sec)

mysql> ALTER TABLE es3 REMOVE PARTITIONING;
Query OK, 0 rows affected (0.53 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> SHOW CREATE TABLE es3\G
*************************** 1. row ***************************
       Table: es3
Create Table: CREATE TABLE `es3` (
  `id` int(11) NOT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `lname` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)

mysql> ALTER TABLE es3 ENGINE = MyISAM;
Query OK, 0 rows affected (0.15 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> ALTER TABLE es EXCHANGE PARTITION p3sp0 WITH TABLE es3;
ERROR 1497 (HY000): The mix of handlers in the partitions is not allowed in this version of MySQL

The ALTER TABLE ... ENGINE ... statement in this example works because the previous ALTER
TABLE removed the partitioning from table es3.

26.3.4 Maintenance of Partitions

A number of table and partition maintenance tasks can be carried out on partitioned tables using SQL
statements intended for such purposes.

Table maintenance of partitioned tables can be accomplished using the statements CHECK TABLE,
OPTIMIZE TABLE, ANALYZE TABLE, and REPAIR TABLE, which are supported for partitioned tables.

You can use a number of extensions to ALTER TABLE for performing operations of this type on one or
more partitions directly, as described in the following list:

• Rebuilding partitions.

 Rebuilds the partition; this has the same effect as dropping all records
stored in the partition, then reinserting them. This can be useful for purposes of defragmentation.

Example:

4561

Obtaining Information About Partitions

ALTER TABLE t1 REBUILD PARTITION p0, p1;

• Optimizing partitions.

 If you have deleted a large number of rows from a partition or if you have
made many changes to a partitioned table with variable-length rows (that is, having VARCHAR, BLOB,
or TEXT columns), you can use ALTER TABLE ... OPTIMIZE PARTITION to reclaim any unused
space and to defragment the partition data file.

Example:

ALTER TABLE t1 OPTIMIZE PARTITION p0, p1;

Using OPTIMIZE PARTITION on a given partition is equivalent to running CHECK PARTITION,
ANALYZE PARTITION, and REPAIR PARTITION on that partition.

Some MySQL storage engines, including InnoDB, do not support per-partition optimization; in
these cases, ALTER TABLE ... OPTIMIZE PARTITION analyzes and rebuilds the entire table,
and causes an appropriate warning to be issued. (Bug #11751825, Bug #42822) Use ALTER
TABLE ... REBUILD PARTITION and ALTER TABLE ... ANALYZE PARTITION instead, to
avoid this issue.

• Analyzing partitions.

 This reads and stores the key distributions for partitions.

Example:

ALTER TABLE t1 ANALYZE PARTITION p3;

• Repairing partitions.

 This repairs corrupted partitions.

Example:

ALTER TABLE t1 REPAIR PARTITION p0,p1;

Normally, REPAIR PARTITION fails when the partition contains duplicate key errors. You can use
ALTER IGNORE TABLE with this option, in which case all rows that cannot be moved due to the
presence of duplicate keys are removed from the partition (Bug #16900947).

• Checking partitions.

 You can check partitions for errors in much the same way that you can use

CHECK TABLE with nonpartitioned tables.

Example:

ALTER TABLE trb3 CHECK PARTITION p1;

This statement tells you whether the data or indexes in partition p1 of table t1 are corrupted. If this is
the case, use ALTER TABLE ... REPAIR PARTITION to repair the partition.

Normally, CHECK PARTITION fails when the partition contains duplicate key errors. You can use
ALTER IGNORE TABLE with this option, in which case the statement returns the contents of each
row in the partition where a duplicate key violation is found. Only the values for the columns in the
partitioning expression for the table are reported. (Bug #16900947)

Each of the statements in the list just shown also supports the keyword ALL in place of the list of
partition names. Using ALL causes the statement to act on all partitions in the table.

You can also truncate partitions using ALTER TABLE ... TRUNCATE PARTITION. This statement
can be used to delete all rows from one or more partitions in much the same way that TRUNCATE
TABLE deletes all rows from a table.

ALTER TABLE ... TRUNCATE PARTITION ALL truncates all partitions in the table.

26.3.5 Obtaining Information About Partitions

4562

Obtaining Information About Partitions

This section discusses obtaining information about existing partitions, which can be done in a number
of ways. Methods of obtaining such information include the following:

• Using the SHOW CREATE TABLE statement to view the partitioning clauses used in creating a

partitioned table.

• Using the SHOW TABLE STATUS statement to determine whether a table is partitioned.

• Querying the Information Schema PARTITIONS table.

• Using the statement EXPLAIN SELECT to see which partitions are used by a given SELECT.

When insertions, deletions, or updates are made to partitioned tables, the binary log records
information about the partition and (if any) the subpartition in which the row event took place. A new
row event is created for a modification that takes place in a different partition or subpartition, even if
the table involved is the same. So if a transaction involves three partitions or subpartitions, three row
events are generated. For an update event, the partition information is recorded for both the “before”
image and the “after” image. The partition information is displayed if you specify the -v or --verbose
option when viewing the binary log using mysqlbinlog. Partition information is only recorded when
row-based logging is in use (binlog_format=ROW).

As discussed elsewhere in this chapter, SHOW CREATE TABLE includes in its output the PARTITION
BY clause used to create a partitioned table. For example:

mysql> SHOW CREATE TABLE trb3\G
*************************** 1. row ***************************
       Table: trb3
Create Table: CREATE TABLE `trb3` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `purchased` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE (YEAR(purchased))
(PARTITION p0 VALUES LESS THAN (1990) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (1995) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (2000) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (2005) ENGINE = InnoDB) */
0 row in set (0.00 sec)

The output from SHOW TABLE STATUS for partitioned tables is the same as that for nonpartitioned
tables, except that the Create_options column contains the string partitioned. The
Engine column contains the name of the storage engine used by all partitions of the table. (See
Section 15.7.7.38, “SHOW TABLE STATUS Statement”, for more information about this statement.)

You can also obtain information about partitions from INFORMATION_SCHEMA, which contains a
PARTITIONS table. See Section 28.3.21, “The INFORMATION_SCHEMA PARTITIONS Table”.

It is possible to determine which partitions of a partitioned table are involved in a given SELECT query
using EXPLAIN. The partitions column in the EXPLAIN output lists the partitions from which
records would be matched by the query.

Suppose that a table trb1 is created and populated as follows:

CREATE TABLE trb1 (id INT, name VARCHAR(50), purchased DATE)
    PARTITION BY RANGE(id)
    (
        PARTITION p0 VALUES LESS THAN (3),
        PARTITION p1 VALUES LESS THAN (7),
        PARTITION p2 VALUES LESS THAN (9),
        PARTITION p3 VALUES LESS THAN (11)
    );

INSERT INTO trb1 VALUES
    (1, 'desk organiser', '2003-10-15'),

4563

Obtaining Information About Partitions

    (2, 'CD player', '1993-11-05'),
    (3, 'TV set', '1996-03-10'),
    (4, 'bookcase', '1982-01-10'),
    (5, 'exercise bike', '2004-05-09'),
    (6, 'sofa', '1987-06-05'),
    (7, 'popcorn maker', '2001-11-22'),
    (8, 'aquarium', '1992-08-04'),
    (9, 'study desk', '1984-09-16'),
    (10, 'lava lamp', '1998-12-25');

You can see which partitions are used in a query such as SELECT * FROM trb1;, as shown here:

mysql> EXPLAIN SELECT * FROM trb1\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: trb1
   partitions: p0,p1,p2,p3
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 10
        Extra: Using filesort

In this case, all four partitions are searched. However, when a limiting condition making use of the
partitioning key is added to the query, you can see that only those partitions containing matching
values are scanned, as shown here:

mysql> EXPLAIN SELECT * FROM trb1 WHERE id < 5\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: trb1
   partitions: p0,p1
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 10
        Extra: Using where

EXPLAIN  also provides information about keys used and possible keys:

mysql> ALTER TABLE trb1 ADD PRIMARY KEY (id);
Query OK, 10 rows affected (0.03 sec)
Records: 10  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM trb1 WHERE id < 5\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: trb1
   partitions: p0,p1
         type: range
possible_keys: PRIMARY
          key: PRIMARY
      key_len: 4
          ref: NULL
         rows: 7
        Extra: Using where

If EXPLAIN is used to examine a query against a nonpartitioned table, no error is produced, but the
value of the partitions column is always NULL.

The rows column of EXPLAIN output displays the total number of rows in the table.

See also Section 15.8.2, “EXPLAIN Statement”.

4564

Partition Pruning

26.4 Partition Pruning

The optimization known as partition pruning is based on a relatively simple concept which can be
described as “Do not scan partitions where there can be no matching values”. Suppose a partitioned
table t1 is created by this statement:

CREATE TABLE t1 (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    region_code TINYINT UNSIGNED NOT NULL,
    dob DATE NOT NULL
)
PARTITION BY RANGE( region_code ) (
    PARTITION p0 VALUES LESS THAN (64),
    PARTITION p1 VALUES LESS THAN (128),
    PARTITION p2 VALUES LESS THAN (192),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);

Suppose that you wish to obtain results from a SELECT statement such as this one:

SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;

It is easy to see that none of the rows which ought to be returned are in either of the partitions p0 or
p3; that is, we need search only in partitions p1 and p2 to find matching rows. By limiting the search, it
is possible to expend much less time and effort in finding matching rows than by scanning all partitions
in the table. This “cutting away” of unneeded partitions is known as pruning. When the optimizer can
make use of partition pruning in performing this query, execution of the query can be an order of
magnitude faster than the same query against a nonpartitioned table containing the same column
definitions and data.

The optimizer can perform pruning whenever a WHERE condition can be reduced to either one of the
following two cases:

• partition_column = constant

• partition_column IN (constant1, constant2, ..., constantN)

In the first case, the optimizer simply evaluates the partitioning expression for the value given,
determines which partition contains that value, and scans only this partition. In many cases, the equal
sign can be replaced with another arithmetic comparison, including <, >, <=, >=, and <>. Some queries
using BETWEEN in the WHERE clause can also take advantage of partition pruning. See the examples
later in this section.

In the second case, the optimizer evaluates the partitioning expression for each value in the list,
creates a list of matching partitions, and then scans only the partitions in this partition list.

SELECT, DELETE, and UPDATE statements support partition pruning. An INSERT statement also
accesses only one partition per inserted row; this is true even for a table that is partitioned by HASH or
KEY although this is not currently shown in the output of EXPLAIN.

Pruning can also be applied to short ranges, which the optimizer can convert into equivalent lists
of values. For instance, in the previous example, the WHERE clause can be converted to WHERE
region_code IN (126, 127, 128, 129). Then the optimizer can determine that the first two
values in the list are found in partition p1, the remaining two values in partition p2, and that the other
partitions contain no relevant values and so do not need to be searched for matching rows.

The optimizer can also perform pruning for WHERE conditions that involve comparisons of the preceding
types on multiple columns for tables that use RANGE COLUMNS or LIST COLUMNS partitioning.

This type of optimization can be applied whenever the partitioning expression consists of an equality or
a range which can be reduced to a set of equalities, or when the partitioning expression represents an

4565

Partition Selection

PARTITION BY LIST(region_code) (
    PARTITION r0 VALUES IN (1, 3),
    PARTITION r1 VALUES IN (2, 5, 8),
    PARTITION r2 VALUES IN (4, 9),
    PARTITION r3 VALUES IN (6, 7, 10)
);

For a statement such as SELECT * FROM t3 WHERE region_code BETWEEN 1 AND 3, the
optimizer determines in which partitions the values 1, 2, and 3 are found (r0 and r1) and skips the
remaining ones (r2 and r3).

For tables that are partitioned by HASH or [LINEAR] KEY, partition pruning is also possible in cases in
which the WHERE clause uses a simple = relation against a column used in the partitioning expression.
Consider a table created like this:

CREATE TABLE t4 (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    region_code TINYINT UNSIGNED NOT NULL,
    dob DATE NOT NULL
)
PARTITION BY KEY(region_code)
PARTITIONS 8;

A statement that compares a column value with a constant can be pruned:

UPDATE t4 WHERE region_code = 7;

Pruning can also be employed for short ranges, because the optimizer can turn such conditions into IN
relations. For example, using the same table t4 as defined previously, queries such as these can be
pruned:

SELECT * FROM t4 WHERE region_code > 2 AND region_code < 6;

SELECT * FROM t4 WHERE region_code BETWEEN 3 AND 5;

In both these cases, the WHERE clause is transformed by the optimizer into WHERE region_code IN
(3, 4, 5).

Important

This optimization is used only if the range size is smaller than the number of
partitions. Consider this statement:

DELETE FROM t4 WHERE region_code BETWEEN 4 AND 12;

The range in the WHERE clause covers 9 values (4, 5, 6, 7, 8, 9, 10, 11, 12), but
t4 has only 8 partitions. This means that the DELETE cannot be pruned.

When a table is partitioned by HASH or [LINEAR] KEY, pruning can be used only on integer columns.
For example, this statement cannot use pruning because dob is a DATE column:

SELECT * FROM t4 WHERE dob >= '2001-04-14' AND dob <= '2005-10-15';

However, if the table stores year values in an INT column, then a query having WHERE year_col >=
2001 AND year_col <= 2005 can be pruned.

Tables using a storage engine that provides automatic partitioning, such as the NDB storage engine
used by MySQL Cluster can be pruned if they are explicitly partitioned.

26.5 Partition Selection

Explicit selection of partitions and subpartitions for rows matching a given WHERE condition is
supported. Partition selection is similar to partition pruning, in that only specific partitions are checked
for matches, but differs in two key respects:

4567

Partition Selection

1. The partitions to be checked are specified by the issuer of the statement, unlike partition pruning,

which is automatic.

2. Whereas partition pruning applies only to queries, explicit selection of partitions is supported for

both queries and a number of DML statements.

SQL statements supporting explicit partition selection are listed here:

• SELECT

• DELETE

• INSERT

• REPLACE

• UPDATE

• LOAD DATA.

• LOAD XML.

The remainder of this section discusses explicit partition selection as it applies generally to the
statements just listed, and provides some examples.

Explicit partition selection is implemented using a PARTITION option. For all supported statements,
this option uses the syntax shown here:

      PARTITION (partition_names)

      partition_names:
          partition_name, ...

This option always follows the name of the table to which the partition or partitions belong.
partition_names is a comma-separated list of partitions or subpartitions to be used. Each
name in this list must be the name of an existing partition or subpartition of the specified table; if
any of the partitions or subpartitions are not found, the statement fails with an error (partition
'partition_name' doesn't exist). Partitions and subpartitions named in partition_names
may be listed in any order, and may overlap.

When the PARTITION option is used, only the partitions and subpartitions listed are checked for
matching rows. This option can be used in a SELECT statement to determine which rows belong to
a given partition. Consider a partitioned table named employees, created and populated using the
statements shown here:

SET @@SQL_MODE = '';

CREATE TABLE employees  (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(25) NOT NULL,
    lname VARCHAR(25) NOT NULL,
    store_id INT NOT NULL,
    department_id INT NOT NULL
)
    PARTITION BY RANGE(id)  (
        PARTITION p0 VALUES LESS THAN (5),
        PARTITION p1 VALUES LESS THAN (10),
        PARTITION p2 VALUES LESS THAN (15),
        PARTITION p3 VALUES LESS THAN MAXVALUE
);

INSERT INTO employees VALUES
    ('', 'Bob', 'Taylor', 3, 2), ('', 'Frank', 'Williams', 1, 2),
    ('', 'Ellen', 'Johnson', 3, 4), ('', 'Jim', 'Smith', 2, 4),
    ('', 'Mary', 'Jones', 1, 1), ('', 'Linda', 'Black', 2, 3),
    ('', 'Ed', 'Jones', 2, 1), ('', 'June', 'Wilson', 3, 1),
    ('', 'Andy', 'Smith', 1, 3), ('', 'Lou', 'Waters', 2, 4),
    ('', 'Jill', 'Stone', 1, 4), ('', 'Roger', 'White', 3, 2),

4568

Partition Selection

    ('', 'Howard', 'Andrews', 1, 2), ('', 'Fred', 'Goldberg', 3, 3),
    ('', 'Barbara', 'Brown', 2, 3), ('', 'Alice', 'Rogers', 2, 2),
    ('', 'Mark', 'Morgan', 3, 3), ('', 'Karen', 'Cole', 3, 2);

You can see which rows are stored in partition p1 like this:

mysql> SELECT * FROM employees PARTITION (p1);
+----+-------+--------+----------+---------------+
| id | fname | lname  | store_id | department_id |
+----+-------+--------+----------+---------------+
|  5 | Mary  | Jones  |        1 |             1 |
|  6 | Linda | Black  |        2 |             3 |
|  7 | Ed    | Jones  |        2 |             1 |
|  8 | June  | Wilson |        3 |             1 |
|  9 | Andy  | Smith  |        1 |             3 |
+----+-------+--------+----------+---------------+
5 rows in set (0.00 sec)

The result is the same as obtained by the query SELECT * FROM employees WHERE id BETWEEN
5 AND 9.

To obtain rows from multiple partitions, supply their names as a comma-delimited list. For example,
SELECT * FROM employees PARTITION (p1, p2) returns all rows from partitions p1 and p2
while excluding rows from the remaining partitions.

Any valid query against a partitioned table can be rewritten with a PARTITION option to restrict the
result to one or more desired partitions. You can use WHERE conditions, ORDER BY and LIMIT options,
and so on. You can also use aggregate functions with HAVING and GROUP BY options. Each of the
following queries produces a valid result when run on the employees table as previously defined:

mysql> SELECT * FROM employees PARTITION (p0, p2)
    ->     WHERE lname LIKE 'S%';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
|  4 | Jim   | Smith |        2 |             4 |
| 11 | Jill  | Stone |        1 |             4 |
+----+-------+-------+----------+---------------+
2 rows in set (0.00 sec)

mysql> SELECT id, CONCAT(fname, ' ', lname) AS name
    ->     FROM employees PARTITION (p0) ORDER BY lname;
+----+----------------+
| id | name           |
+----+----------------+
|  3 | Ellen Johnson  |
|  4 | Jim Smith      |
|  1 | Bob Taylor     |
|  2 | Frank Williams |
+----+----------------+
4 rows in set (0.06 sec)

mysql> SELECT store_id, COUNT(department_id) AS c
    ->     FROM employees PARTITION (p1,p2,p3)
    ->     GROUP BY store_id HAVING c > 4;
+---+----------+
| c | store_id |
+---+----------+
| 5 |        2 |
| 5 |        3 |
+---+----------+
2 rows in set (0.00 sec)

Statements using partition selection can be employed with tables using any of the supported
partitioning types. When a table is created using [LINEAR] HASH or [LINEAR] KEY partitioning and
the names of the partitions are not specified, MySQL automatically names the partitions p0, p1, p2, ...,
pN-1, where N is the number of partitions. For subpartitions not explicitly named, MySQL assigns
automatically to the subpartitions in each partition pX the names pXsp0, pXsp1, pXsp2, ..., pXspM-1,
where M is the number of subpartitions. When executing against this table a SELECT (or other SQL

4569

Partition Selection

statement for which explicit partition selection is allowed), you can use these generated names in a
PARTITION option, as shown here:

mysql> CREATE TABLE employees_sub  (
    ->     id INT NOT NULL AUTO_INCREMENT,
    ->     fname VARCHAR(25) NOT NULL,
    ->     lname VARCHAR(25) NOT NULL,
    ->     store_id INT NOT NULL,
    ->     department_id INT NOT NULL,
    ->     PRIMARY KEY pk (id, lname)
    -> )
    ->     PARTITION BY RANGE(id)
    ->     SUBPARTITION BY KEY (lname)
    ->     SUBPARTITIONS 2 (
    ->         PARTITION p0 VALUES LESS THAN (5),
    ->         PARTITION p1 VALUES LESS THAN (10),
    ->         PARTITION p2 VALUES LESS THAN (15),
    ->         PARTITION p3 VALUES LESS THAN MAXVALUE
    -> );
Query OK, 0 rows affected (1.14 sec)

mysql> INSERT INTO employees_sub   # reuse data in employees table
    ->     SELECT * FROM employees;
Query OK, 18 rows affected (0.09 sec)
Records: 18  Duplicates: 0  Warnings: 0

mysql> SELECT id, CONCAT(fname, ' ', lname) AS name
    ->     FROM employees_sub PARTITION (p2sp1);
+----+---------------+
| id | name          |
+----+---------------+
| 10 | Lou Waters    |
| 14 | Fred Goldberg |
+----+---------------+
2 rows in set (0.00 sec)

You may also use a PARTITION option in the SELECT portion of an INSERT ... SELECT statement,
as shown here:

mysql> CREATE TABLE employees_copy LIKE employees;
Query OK, 0 rows affected (0.28 sec)

mysql> INSERT INTO employees_copy
    ->     SELECT * FROM employees PARTITION (p2);
Query OK, 5 rows affected (0.04 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM employees_copy;
+----+--------+----------+----------+---------------+
| id | fname  | lname    | store_id | department_id |
+----+--------+----------+----------+---------------+
| 10 | Lou    | Waters   |        2 |             4 |
| 11 | Jill   | Stone    |        1 |             4 |
| 12 | Roger  | White    |        3 |             2 |
| 13 | Howard | Andrews  |        1 |             2 |
| 14 | Fred   | Goldberg |        3 |             3 |
+----+--------+----------+----------+---------------+
5 rows in set (0.00 sec)

Partition selection can also be used with joins. Suppose we create and populate two tables using the
statements shown here:

CREATE TABLE stores (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(30) NOT NULL
)
    PARTITION BY HASH(id)
    PARTITIONS 2;

INSERT INTO stores VALUES
    ('', 'Nambucca'), ('', 'Uranga'),

4570

Partition Selection

    ('', 'Bellingen'), ('', 'Grafton');

CREATE TABLE departments  (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL
)
    PARTITION BY KEY(id)
    PARTITIONS 2;

INSERT INTO departments VALUES
    ('', 'Sales'), ('', 'Customer Service'),
    ('', 'Delivery'), ('', 'Accounting');

You can explicitly select partitions (or subpartitions, or both) from any or all of the tables in a join.
(The PARTITION option used to select partitions from a given table immediately follows the name of
the table, before all other options, including any table alias.) For example, the following query gets
the name, employee ID, department, and city of all employees who work in the Sales or Delivery
department (partition p1 of the departments table) at the stores in either of the cities of Nambucca
and Bellingen (partition p0 of the stores table):

mysql> SELECT
    ->     e.id AS 'Employee ID', CONCAT(e.fname, ' ', e.lname) AS Name,
    ->     s.city AS City, d.name AS department
    -> FROM employees AS e
    ->     JOIN stores PARTITION (p1) AS s ON e.store_id=s.id
    ->     JOIN departments PARTITION (p0) AS d ON e.department_id=d.id
    -> ORDER BY e.lname;
+-------------+---------------+-----------+------------+
| Employee ID | Name          | City      | department |
+-------------+---------------+-----------+------------+
|          14 | Fred Goldberg | Bellingen | Delivery   |
|           5 | Mary Jones    | Nambucca  | Sales      |
|          17 | Mark Morgan   | Bellingen | Delivery   |
|           9 | Andy Smith    | Nambucca  | Delivery   |
|           8 | June Wilson   | Bellingen | Sales      |
+-------------+---------------+-----------+------------+
5 rows in set (0.00 sec)

For general information about joins in MySQL, see Section 15.2.13.2, “JOIN Clause”.

When the PARTITION option is used with DELETE statements, only those partitions (and subpartitions,
if any) listed with the option are checked for rows to be deleted. Any other partitions are ignored, as
shown here:

mysql> SELECT * FROM employees WHERE fname LIKE 'j%';
+----+-------+--------+----------+---------------+
| id | fname | lname  | store_id | department_id |
+----+-------+--------+----------+---------------+
|  4 | Jim   | Smith  |        2 |             4 |
|  8 | June  | Wilson |        3 |             1 |
| 11 | Jill  | Stone  |        1 |             4 |
+----+-------+--------+----------+---------------+
3 rows in set (0.00 sec)

mysql> DELETE FROM employees PARTITION (p0, p1)
    ->     WHERE fname LIKE 'j%';
Query OK, 2 rows affected (0.09 sec)

mysql> SELECT * FROM employees WHERE fname LIKE 'j%';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill  | Stone |        1 |             4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)

Only the two rows in partitions p0 and p1 matching the WHERE condition were deleted. As you can see
from the result when the SELECT is run a second time, there remains a row in the table matching the
WHERE condition, but residing in a different partition (p2).

4571

Partition Selection

UPDATE statements using explicit partition selection behave in the same way; only rows in the
partitions referenced by the PARTITION option are considered when determining the rows to be
updated, as can be seen by executing the following statements:

mysql> UPDATE employees PARTITION (p0)
    ->     SET store_id = 2 WHERE fname = 'Jill';
Query OK, 0 rows affected (0.00 sec)
Rows matched: 0  Changed: 0  Warnings: 0

mysql> SELECT * FROM employees WHERE fname = 'Jill';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill  | Stone |        1 |             4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)

mysql> UPDATE employees PARTITION (p2)
    ->     SET store_id = 2 WHERE fname = 'Jill';
Query OK, 1 row affected (0.09 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM employees WHERE fname = 'Jill';
+----+-------+-------+----------+---------------+
| id | fname | lname | store_id | department_id |
+----+-------+-------+----------+---------------+
| 11 | Jill  | Stone |        2 |             4 |
+----+-------+-------+----------+---------------+
1 row in set (0.00 sec)

In the same way, when PARTITION is used with DELETE, only rows in the partition or partitions named
in the partition list are checked for deletion.

For statements that insert rows, the behavior differs in that failure to find a suitable partition causes the
statement to fail. This is true for both INSERT and REPLACE statements, as shown here:

mysql> INSERT INTO employees PARTITION (p2) VALUES (20, 'Jan', 'Jones', 1, 3);
ERROR 1729 (HY000): Found a row not matching the given partition set
mysql> INSERT INTO employees PARTITION (p3) VALUES (20, 'Jan', 'Jones', 1, 3);
Query OK, 1 row affected (0.07 sec)

mysql> REPLACE INTO employees PARTITION (p0) VALUES (20, 'Jan', 'Jones', 3, 2);
ERROR 1729 (HY000): Found a row not matching the given partition set

mysql> REPLACE INTO employees PARTITION (p3) VALUES (20, 'Jan', 'Jones', 3, 2);
Query OK, 2 rows affected (0.09 sec)

For statements that write multiple rows to a partitioned table that using the InnoDB storage engine:
If any row in the list following VALUES cannot be written to one of the partitions specified in the
partition_names list, the entire statement fails and no rows are written. This is shown for INSERT
statements in the following example, reusing the employees table created previously:

mysql> ALTER TABLE employees
    ->     REORGANIZE PARTITION p3 INTO (
    ->         PARTITION p3 VALUES LESS THAN (20),
    ->         PARTITION p4 VALUES LESS THAN (25),
    ->         PARTITION p5 VALUES LESS THAN MAXVALUE
    ->     );
Query OK, 6 rows affected (2.09 sec)
Records: 6  Duplicates: 0  Warnings: 0

mysql> SHOW CREATE TABLE employees\G
*************************** 1. row ***************************
       Table: employees
Create Table: CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(25) NOT NULL,
  `lname` varchar(25) NOT NULL,
  `store_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL,

4572

Restrictions and Limitations on Partitioning

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE (id)
(PARTITION p0 VALUES LESS THAN (5) ENGINE = InnoDB,
 PARTITION p1 VALUES LESS THAN (10) ENGINE = InnoDB,
 PARTITION p2 VALUES LESS THAN (15) ENGINE = InnoDB,
 PARTITION p3 VALUES LESS THAN (20) ENGINE = InnoDB,
 PARTITION p4 VALUES LESS THAN (25) ENGINE = InnoDB,
 PARTITION p5 VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */
1 row in set (0.00 sec)

mysql> INSERT INTO employees PARTITION (p3, p4) VALUES
    ->     (24, 'Tim', 'Greene', 3, 1),  (26, 'Linda', 'Mills', 2, 1);
ERROR 1729 (HY000): Found a row not matching the given partition set

mysql> INSERT INTO employees PARTITION (p3, p4, p5) VALUES
    ->     (24, 'Tim', 'Greene', 3, 1),  (26, 'Linda', 'Mills', 2, 1);
Query OK, 2 rows affected (0.06 sec)
Records: 2  Duplicates: 0  Warnings: 0

The preceding is true for both INSERT statements and REPLACE statements that write multiple rows.

Partition selection is disabled for tables employing a storage engine that supplies automatic
partitioning, such as NDB.

26.6 Restrictions and Limitations on Partitioning

This section discusses current restrictions and limitations on MySQL partitioning support.

Prohibited constructs.

 The following constructs are not permitted in partitioning expressions:

• Stored procedures, stored functions, loadable functions, or plugins.

• Declared variables or user variables.

For a list of SQL functions which are permitted in partitioning expressions, see Section 26.6.3,
“Partitioning Limitations Relating to Functions”.

Arithmetic and logical operators.
partitioning expressions. However, the result must be an integer value or NULL (except in the case of
[LINEAR] KEY partitioning, as discussed elsewhere in this chapter; see Section 26.2, “Partitioning
Types”, for more information).

   Use of the arithmetic operators +, -, and * is permitted in

The DIV operator is also supported; the / operator is not permitted.

The bit operators |, &, ^, <<, >>, and ~ are not permitted in partitioning expressions.

Server SQL mode.
   Tables employing user-defined partitioning do not preserve the SQL mode in
effect at the time that they were created. As discussed elsewhere in this Manual (see Section 7.1.11,
“Server SQL Modes”), the results of many MySQL functions and operators may change according
to the server SQL mode. Therefore, a change in the SQL mode at any time after the creation of
partitioned tables may lead to major changes in the behavior of such tables, and could easily lead to
corruption or loss of data. For these reasons, it is strongly recommended that you never change the
server SQL mode after creating partitioned tables.

For one such change in the server SQL mode making a partitioned tables unusable, consider
the following CREATE TABLE statement, which can be executed successfully only if the
NO_UNSIGNED_SUBTRACTION mode is in effect:

mysql> SELECT @@sql_mode;
+------------+
| @@sql_mode |
+------------+
|            |
+------------+
1 row in set (0.00 sec)

4573

Restrictions and Limitations on Partitioning

operations are performed as soon as the partitioning operation has completed. For InnoDB-specific
exceptions to this limitation, see Partitioning Operations.

• Indexes; partition pruning.

 As with nonpartitioned tables, proper use of indexes can speed

up queries on partitioned tables significantly. In addition, designing partitioned tables and queries
on these tables to take advantage of partition pruning can improve performance dramatically. See
Section 26.4, “Partition Pruning”, for more information.

Index condition pushdown is supported for partitioned tables. See Section 10.2.1.6, “Index Condition
Pushdown Optimization”.

• Performance with LOAD DATA.

 In MySQL 8.4, LOAD DATA uses buffering to improve

performance. You should be aware that the buffer uses 130 KB memory per partition to achieve this.

Maximum number of partitions.
The maximum possible number of partitions for a given table not using the NDB storage engine is 8192.
This number includes subpartitions.

The maximum possible number of user-defined partitions for a table using the NDB storage engine
is determined according to the version of the NDB Cluster software being used, the number of data
nodes, and other factors. See NDB and user-defined partitioning, for more information.

If, when creating tables with a large number of partitions (but less than the maximum), you encounter
an error message such as Got error ... from storage engine: Out of resources
when opening file, you may be able to address the issue by increasing the value of the
open_files_limit system variable. However, this is dependent on the operating system, and may
not be possible or advisable on all platforms; see Section B.3.2.16, “File Not Found and Similar Errors”,
for more information. In some cases, using large numbers (hundreds) of partitions may also not be
advisable due to other concerns, so using more partitions does not automatically lead to better results.

See also File system operations.

Foreign keys not supported for partitioned InnoDB tables.
Partitioned tables using the InnoDB storage engine do not support foreign keys. More specifically, this
means that the following two statements are true:

1. No definition of an InnoDB table employing user-defined partitioning may contain foreign key

references; no InnoDB table whose definition contains foreign key references may be partitioned.

2. No InnoDB table definition may contain a foreign key reference to a user-partitioned table; no
InnoDB table with user-defined partitioning may contain columns referenced by foreign keys.

The scope of the restrictions just listed includes all tables that use the InnoDB storage engine. CREATE
TABLE and ALTER TABLE statements that would result in tables violating these restrictions are not
allowed.

ALTER TABLE ... ORDER BY.
a partitioned table causes ordering of rows only within each partition.

 An ALTER TABLE ... ORDER BY column statement run against

ADD COLUMN ... ALGORITHM=INSTANT.
COLUMN ... ALGORITHM=INSTANT on a partitioned table, it is no longer possible to exchange
partitions with this table.

 Once you perform ALTER TABLE ... ADD

Effects on REPLACE statements by modification of primary keys.
cases (see Section 26.6.1, “Partitioning Keys, Primary Keys, and Unique Keys”) to modify a table's
primary key. Be aware that, if your application uses REPLACE statements and you do this, the results
of these statements can be drastically altered. See Section 15.2.12, “REPLACE Statement”, for more
information and an example.

 It can be desirable in some

FULLTEXT indexes.
Partitioned tables do not support FULLTEXT indexes or searches.

4575

Restrictions and Limitations on Partitioning

Spatial columns.
partitioned tables.

 Columns with spatial data types such as POINT or GEOMETRY cannot be used in

Temporary tables.
Temporary tables cannot be partitioned.

Log tables.
BY ... statement on such a table fails with an error.

 It is not possible to partition the log tables; an ALTER TABLE ... PARTITION

Data type of partitioning key.
A partitioning key must be either an integer column or an expression that resolves to an integer.
Expressions employing ENUM columns cannot be used. The column or expression value may also be
NULL; see Section 26.2.7, “How MySQL Partitioning Handles NULL”.

There are two exceptions to this restriction:

1. When partitioning by [LINEAR] KEY, it is possible to use columns of any valid MySQL data type

other than TEXT or BLOB as partitioning keys, because the internal key-hashing functions produce
the correct data type from these types. For example, the following two CREATE TABLE statements
are valid:

CREATE TABLE tkc (c1 CHAR)
PARTITION BY KEY(c1)
PARTITIONS 4;

CREATE TABLE tke
    ( c1 ENUM('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet') )
PARTITION BY LINEAR KEY(c1)
PARTITIONS 6;

2. When partitioning by RANGE COLUMNS or LIST COLUMNS, it is possible to use string, DATE, and
DATETIME columns. For example, each of the following CREATE TABLE statements is valid:

CREATE TABLE rc (c1 INT, c2 DATE)
PARTITION BY RANGE COLUMNS(c2) (
    PARTITION p0 VALUES LESS THAN('1990-01-01'),
    PARTITION p1 VALUES LESS THAN('1995-01-01'),
    PARTITION p2 VALUES LESS THAN('2000-01-01'),
    PARTITION p3 VALUES LESS THAN('2005-01-01'),
    PARTITION p4 VALUES LESS THAN(MAXVALUE)
);

CREATE TABLE lc (c1 INT, c2 CHAR(1))
PARTITION BY LIST COLUMNS(c2) (
    PARTITION p0 VALUES IN('a', 'd', 'g', 'j', 'm', 'p', 's', 'v', 'y'),
    PARTITION p1 VALUES IN('b', 'e', 'h', 'k', 'n', 'q', 't', 'w', 'z'),
    PARTITION p2 VALUES IN('c', 'f', 'i', 'l', 'o', 'r', 'u', 'x', NULL)
);

Neither of the preceding exceptions applies to BLOB or TEXT column types.

Subqueries.
A partitioning key may not be a subquery, even if that subquery resolves to an integer value or NULL.

Column index prefixes not supported for key partitioning.
partitioned by key, any columns in the partitioning key which use column prefixes are not allowed in
the table's partitioning function. Consider the following CREATE TABLE statement, which has three
VARCHAR columns, and whose primary key uses all three columns and specifies a prefix for one of
them. This statement is rejected with an error, as shown here:

 When creating a table that is

mysql> USE d;
Database changed
mysql> CREATE TABLE t1 (
    ->     a VARCHAR(10000),
    ->     b VARCHAR(25),
    ->     c VARCHAR(10),

4576

Restrictions and Limitations on Partitioning

    ->     PRIMARY KEY (a(10), b, c)
    -> ) PARTITION BY KEY() PARTITIONS 2;
ERROR 6123 (HY000): Column 'd.t1.a' having prefix key part 'a(10)' in the
PARTITION BY KEY() clause is not supported.

For general information about partitioning tables by key, see Section 26.2.5, “KEY Partitioning”.

Issues with subpartitions.
Subpartitions must use HASH or KEY partitioning. Only RANGE and LIST partitions may be
subpartitioned; HASH and KEY partitions cannot be subpartitioned.

 SUBPARTITION BY KEY requires that the subpartitioning column or columns be specified explicitly,
unlike the case with PARTITION BY KEY, where it can be omitted (in which case the table's primary
key column is used by default). Consider the table created by this statement:

CREATE TABLE ts (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30)
);

You can create a table having the same columns, partitioned by KEY, using a statement such as this
one:

CREATE TABLE ts (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30)
)
PARTITION BY KEY()
PARTITIONS 4;

The previous statement is treated as though it had been written like this, with the table's primary key
column used as the partitioning column:

CREATE TABLE ts (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30)
)
PARTITION BY KEY(id)
PARTITIONS 4;

However, the following statement that attempts to create a subpartitioned table using the default
column as the subpartitioning column fails, and the column must be specified for the statement to
succeed, as shown here:

mysql> CREATE TABLE ts (
    ->     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ->     name VARCHAR(30)
    -> )
    -> PARTITION BY RANGE(id)
    -> SUBPARTITION BY KEY()
    -> SUBPARTITIONS 4
    -> (
    ->     PARTITION p0 VALUES LESS THAN (100),
    ->     PARTITION p1 VALUES LESS THAN (MAXVALUE)
    -> );
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that
corresponds to your MySQL server version for the right syntax to use near ')

mysql> CREATE TABLE ts (
    ->     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ->     name VARCHAR(30)
    -> )
    -> PARTITION BY RANGE(id)
    -> SUBPARTITION BY KEY(id)
    -> SUBPARTITIONS 4
    -> (
    ->     PARTITION p0 VALUES LESS THAN (100),
    ->     PARTITION p1 VALUES LESS THAN (MAXVALUE)

4577

Partitioning Keys, Primary Keys, and Unique Keys

    -> );
Query OK, 0 rows affected (0.07 sec)

This is a known issue (see Bug #51470).

DATA DIRECTORY and INDEX DIRECTORY options.
DIRECTORY options are ignored (see Bug #32091). You can employ these options for individual
partitions or subpartitions of InnoDB tables. The directory specified in a DATA DIRECTORY clause
must be known to InnoDB. For more information, see Using the DATA DIRECTORY Clause.

 Table-level DATA DIRECTORY and INDEX

Repairing and rebuilding partitioned tables.
ANALYZE TABLE, and REPAIR TABLE are supported for partitioned tables.

 The statements CHECK TABLE, OPTIMIZE TABLE,

In addition, you can use ALTER TABLE ... REBUILD PARTITION to rebuild one or more partitions
of a partitioned table; ALTER TABLE ... REORGANIZE PARTITION also causes partitions to
be rebuilt. See Section 15.1.9, “ALTER TABLE Statement”, for more information about these two
statements.

ANALYZE, CHECK, OPTIMIZE, REPAIR, and TRUNCATE operations are supported with subpartitions.
See Section 15.1.9.1, “ALTER TABLE Partition Operations”.

File name delimiters for partitions and subpartitions.
include generated delimiters such as #P# and #SP#. The lettercase of such delimiters can vary and
should not be depended upon.

 Table partition and subpartition file names

26.6.1 Partitioning Keys, Primary Keys, and Unique Keys

This section discusses the relationship of partitioning keys with primary keys and unique keys. The rule
governing this relationship can be expressed as follows: All columns used in the partitioning expression
for a partitioned table must be part of every unique key that the table may have.

In other words, every unique key on the table must use every column in the table's partitioning
expression. (This also includes the table's primary key, since it is by definition a unique key. This
particular case is discussed later in this section.) For example, each of the following table creation
statements is invalid:

CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2)
)
PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1),
    UNIQUE KEY (col3)
)
PARTITION BY HASH(col1 + col3)
PARTITIONS 4;

In each case, the proposed table would have at least one unique key that does not include all columns
used in the partitioning expression.

Each of the following statements is valid, and represents one way in which the corresponding invalid
table creation statement could be made to work:

CREATE TABLE t1 (

4578

Partitioning Keys, Primary Keys, and Unique Keys

    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3)
)
PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3)
)
PARTITION BY HASH(col1 + col3)
PARTITIONS 4;

This example shows the error produced in such cases:

mysql> CREATE TABLE t3 (
    ->     col1 INT NOT NULL,
    ->     col2 DATE NOT NULL,
    ->     col3 INT NOT NULL,
    ->     col4 INT NOT NULL,
    ->     UNIQUE KEY (col1, col2),
    ->     UNIQUE KEY (col3)
    -> )
    -> PARTITION BY HASH(col1 + col3)
    -> PARTITIONS 4;
ERROR 1491 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function

The CREATE TABLE statement fails because both col1 and col3 are included in the proposed
partitioning key, but neither of these columns is part of both of unique keys on the table. This shows
one possible fix for the invalid table definition:

mysql> CREATE TABLE t3 (
    ->     col1 INT NOT NULL,
    ->     col2 DATE NOT NULL,
    ->     col3 INT NOT NULL,
    ->     col4 INT NOT NULL,
    ->     UNIQUE KEY (col1, col2, col3),
    ->     UNIQUE KEY (col3)
    -> )
    -> PARTITION BY HASH(col3)
    -> PARTITIONS 4;
Query OK, 0 rows affected (0.05 sec)

In this case, the proposed partitioning key col3 is part of both unique keys, and the table creation
statement succeeds.

The following table cannot be partitioned at all, because there is no way to include in a partitioning key
any columns that belong to both unique keys:

CREATE TABLE t4 (
    col1 INT NOT NULL,
    col2 INT NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3),
    UNIQUE KEY (col2, col4)
);

Since every primary key is by definition a unique key, this restriction also includes the table's primary
key, if it has one. For example, the next two statements are invalid:

CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,

4579

Partitioning Keys, Primary Keys, and Unique Keys

    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2)
)
PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col3),
    UNIQUE KEY(col2)
)
PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;

In both cases, the primary key does not include all columns referenced in the partitioning expression.
However, both of the next two statements are valid:

CREATE TABLE t7 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2)
)
PARTITION BY HASH(col1 + YEAR(col2))
PARTITIONS 4;

CREATE TABLE t8 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col4),
    UNIQUE KEY(col2, col1)
)
PARTITION BY HASH(col1 + YEAR(col2))
PARTITIONS 4;

If a table has no unique keys—this includes having no primary key—then this restriction does not
apply, and you may use any column or columns in the partitioning expression as long as the column
type is compatible with the partitioning type.

For the same reason, you cannot later add a unique key to a partitioned table unless the key includes
all columns used by the table's partitioning expression. Consider the partitioned table created as shown
here:

mysql> CREATE TABLE t_no_pk (c1 INT, c2 INT)
    ->     PARTITION BY RANGE(c1) (
    ->         PARTITION p0 VALUES LESS THAN (10),
    ->         PARTITION p1 VALUES LESS THAN (20),
    ->         PARTITION p2 VALUES LESS THAN (30),
    ->         PARTITION p3 VALUES LESS THAN (40)
    ->     );
Query OK, 0 rows affected (0.12 sec)

It is possible to add a primary key to t_no_pk using either of these ALTER TABLE statements:

#  possible PK
mysql> ALTER TABLE t_no_pk ADD PRIMARY KEY(c1);
Query OK, 0 rows affected (0.13 sec)
Records: 0  Duplicates: 0  Warnings: 0

# drop this PK
mysql> ALTER TABLE t_no_pk DROP PRIMARY KEY;
Query OK, 0 rows affected (0.10 sec)
Records: 0  Duplicates: 0  Warnings: 0

4580

Partitioning Limitations Relating to Storage Engines

#  use another possible PK
mysql> ALTER TABLE t_no_pk ADD PRIMARY KEY(c1, c2);
Query OK, 0 rows affected (0.12 sec)
Records: 0  Duplicates: 0  Warnings: 0

# drop this PK
mysql> ALTER TABLE t_no_pk DROP PRIMARY KEY;
Query OK, 0 rows affected (0.09 sec)
Records: 0  Duplicates: 0  Warnings: 0

However, the next statement fails, because c1 is part of the partitioning key, but is not part of the
proposed primary key:

#  fails with error 1503
mysql> ALTER TABLE t_no_pk ADD PRIMARY KEY(c2);
ERROR 1503 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function

Since t_no_pk has only c1 in its partitioning expression, attempting to adding a unique key on c2
alone fails. However, you can add a unique key that uses both c1 and c2.

These rules also apply to existing nonpartitioned tables that you wish to partition using ALTER
TABLE ... PARTITION BY. Consider a table np_pk created as shown here:

mysql> CREATE TABLE np_pk (
    ->     id INT NOT NULL AUTO_INCREMENT,
    ->     name VARCHAR(50),
    ->     added DATE,
    ->     PRIMARY KEY (id)
    -> );
Query OK, 0 rows affected (0.08 sec)

The following ALTER TABLE statement fails with an error, because the added column is not part of
any unique key in the table:

mysql> ALTER TABLE np_pk
    ->     PARTITION BY HASH( TO_DAYS(added) )
    ->     PARTITIONS 4;
ERROR 1503 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function

However, this statement using the id column for the partitioning column is valid, as shown here:

mysql> ALTER TABLE np_pk
    ->     PARTITION BY HASH(id)
    ->     PARTITIONS 4;
Query OK, 0 rows affected (0.11 sec)
Records: 0  Duplicates: 0  Warnings: 0

In the case of np_pk, the only column that may be used as part of a partitioning expression is id; if
you wish to partition this table using any other column or columns in the partitioning expression, you
must first modify the table, either by adding the desired column or columns to the primary key, or by
dropping the primary key altogether.

26.6.2 Partitioning Limitations Relating to Storage Engines

In MySQL 8.4, partitioning support is not actually provided by the MySQL Server, but rather by a table
storage engine's own or native partitioning handler. In MySQL 8.4, only the InnoDB and NDB storage
engines provide native partitioning handlers. This means that partitioned tables cannot be created
using any other storage engine than these. (You must be using MySQL NDB Cluster with the NDB
storage engine to create NDB tables.)

InnoDB storage engine.
Partitioned InnoDB tables cannot have foreign key references, nor can they have columns referenced
by foreign keys. InnoDB tables which have or which are referenced by foreign keys cannot be
partitioned.

 InnoDB foreign keys and MySQL partitioning are not compatible.

4581

Partitioning Limitations Relating to Functions

ALTER TABLE ... OPTIMIZE PARTITION does not work correctly with partitioned tables that
use InnoDB. Use ALTER TABLE ... REBUILD PARTITION and ALTER TABLE ... ANALYZE
PARTITION, instead, for such tables. For more information, see Section 15.1.9.1, “ALTER TABLE
Partition Operations”.

 Partitioning by KEY
User-defined partitioning and the NDB storage engine (NDB Cluster).
(including LINEAR KEY) is the only type of partitioning supported for the NDB storage engine. It is
not possible under normal circumstances in NDB Cluster to create an NDB Cluster table using any
partitioning type other than [LINEAR] KEY, and attempting to do so fails with an error.

The maximum number of partitions that can be defined for an NDB table depends on the number of
data nodes and node groups in the cluster, the version of the NDB Cluster software in use, and other
factors. See NDB and user-defined partitioning, for more information.

The maximum amount of fixed-size data that can be stored per partition in an NDB table is 128 TB.
Previously, this was 16 GB.

CREATE TABLE and ALTER TABLE statements that would cause a user-partitioned NDB table not to
meet either or both of the following two requirements are not permitted, and fail with an error:

1. The table must have an explicit primary key.

2. All columns listed in the table's partitioning expression must be part of the primary key.

Exception.
PARTITION BY KEY() or PARTITION BY LINEAR KEY()), then no explicit primary key is required.

 If a user-partitioned NDB table is created using an empty column-list (that is, using

Partition selection.
Selection”, for more information.

 Partition selection is not supported for NDB tables. See Section 26.5, “Partition

Upgrading partitioned tables.
must be dumped and reloaded.

 When performing an upgrade, tables which are partitioned by KEY

For information about converting MyISAM tables to InnoDB, see Section 17.6.1.5, “Converting Tables
from MyISAM to InnoDB”.

26.6.3 Partitioning Limitations Relating to Functions

This section discusses limitations in MySQL Partitioning relating specifically to functions used in
partitioning expressions.

Only the MySQL functions shown in the following list are allowed in partitioning expressions:

• ABS()

• CEILING() (see CEILING() and FLOOR())

• DATEDIFF()

• DAY()

• DAYOFMONTH()

• DAYOFWEEK()

• DAYOFYEAR()

• EXTRACT() (see EXTRACT() function with WEEK specifier)

• FLOOR() (see CEILING() and FLOOR())

• HOUR()

4582

Partitioning Limitations Relating to Functions

• MICROSECOND()

• MINUTE()

• MOD()

• MONTH()

• QUARTER()

• SECOND()

• TIME_TO_SEC()

• TO_DAYS()

• TO_SECONDS()

• UNIX_TIMESTAMP() (with TIMESTAMP columns)

• WEEKDAY()

• YEAR()

• YEARWEEK()

In MySQL 8.4, partition pruning is supported for the TO_DAYS(), TO_SECONDS(), YEAR(), and
UNIX_TIMESTAMP() functions. See Section 26.4, “Partition Pruning”, for more information.

CEILING() and FLOOR().
 Each of these functions returns an integer only if it is passed an argument
of an exact numeric type, such as one of the INT types or DECIMAL. This means, for example, that the
following CREATE TABLE statement fails with an error, as shown here:

mysql> CREATE TABLE t (c FLOAT) PARTITION BY LIST( FLOOR(c) )(
    ->     PARTITION p0 VALUES IN (1,3,5),
    ->     PARTITION p1 VALUES IN (2,4,6)
    -> );
ERROR 1490 (HY000): The PARTITION function returns the wrong type

 The value returned by the EXTRACT() function, when
EXTRACT() function with WEEK specifier.
used as EXTRACT(WEEK FROM col), depends on the value of the default_week_format system
variable. For this reason, EXTRACT() is not permitted as a partitioning function when it specifies the
unit as WEEK. (Bug #54483)

See Section 14.6.2, “Mathematical Functions”, for more information about the return types of these
functions, as well as Section 13.1, “Numeric Data Types”.

4583

4584

