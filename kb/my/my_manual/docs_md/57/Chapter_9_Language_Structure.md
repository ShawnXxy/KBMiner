Numeric Literals

To insert binary data into a string column (such as a BLOB column), you should represent certain
characters by escape sequences. Backslash (\) and the quote character used to quote the string must be
escaped. In certain client environments, it may also be necessary to escape NUL or Control+Z. The mysql
client truncates quoted strings containing NUL characters if they are not escaped, and Control+Z may be
taken for END-OF-FILE on Windows if not escaped. For the escape sequences that represent each of
these characters, see Table 9.1, “Special Character Escape Sequences”.

When writing application programs, any string that might contain any of these special characters must be
properly escaped before the string is used as a data value in an SQL statement that is sent to the MySQL
server. You can do this in two ways:

• Process the string with a function that escapes the special characters. In a C program, you can
use the mysql_real_escape_string_quote() C API function to escape characters. See
mysql_real_escape_string_quote(). Within SQL statements that construct other SQL statements, you
can use the QUOTE() function. The Perl DBI interface provides a quote method to convert special
characters to the proper escape sequences. See Section 27.9, “MySQL Perl API”. Other language
interfaces may provide a similar capability.

• As an alternative to explicitly escaping special characters, many MySQL APIs provide a placeholder

capability that enables you to insert special markers into a statement string, and then bind data values
to them when you issue the statement. In this case, the API takes care of escaping special characters in
the values for you.

9.1.2 Numeric Literals

Number literals include exact-value (integer and DECIMAL) literals and approximate-value (floating-point)
literals.

Integers are represented as a sequence of digits. Numbers may include . as a decimal separator.
Numbers may be preceded by - or + to indicate a negative or positive value, respectively. Numbers
represented in scientific notation with a mantissa and exponent are approximate-value numbers.

Exact-value numeric literals have an integer part or fractional part, or both. They may be signed. Examples:
1, .2, 3.4, -5, -6.78, +9.10.

Approximate-value numeric literals are represented in scientific notation with a mantissa and exponent.
Either or both parts may be signed. Examples: 1.2E3, 1.2E-3, -1.2E3, -1.2E-3.

Two numbers that look similar may be treated differently. For example, 2.34 is an exact-value (fixed-point)
number, whereas 2.34E0 is an approximate-value (floating-point) number.

The DECIMAL data type is a fixed-point type and calculations are exact. In MySQL, the DECIMAL type
has several synonyms: NUMERIC, DEC, FIXED. The integer types also are exact-value types. For more
information about exact-value calculations, see Section 12.21, “Precision Math”.

The FLOAT and DOUBLE data types are floating-point types and calculations are approximate. In MySQL,
types that are synonymous with FLOAT or DOUBLE are DOUBLE PRECISION and REAL.

An integer may be used in floating-point context; it is interpreted as the equivalent floating-point number.

9.1.3 Date and Time Literals

• Standard SQL and ODBC Date and Time Literals

• String and Numeric Literals in Date and Time Context

1654

Hexadecimal Literals

• As a number in hhmmss format, provided that it makes sense as a time. For example, 101112 is
understood as '10:11:12'. The following alternative formats are also understood: ss, mmss, or
hhmmss.

A trailing fractional seconds part is recognized in the 'D hh:mm:ss.fraction',
'hh:mm:ss.fraction', 'hhmmss.fraction', and hhmmss.fraction time formats, where
fraction is the fractional part in up to microseconds (6 digits) precision. The fractional part should
always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter is
recognized. For information about fractional seconds support in MySQL, see Section 11.2.7, “Fractional
Seconds in Time Values”.

For TIME values specified as strings that include a time part delimiter, it is unnecessary to specify two
digits for hours, minutes, or seconds values that are less than 10. '8:3:2' is the same as '08:03:02'.

9.1.4 Hexadecimal Literals

Hexadecimal literal values are written using X'val' or 0xval notation, where val contains hexadecimal
digits (0..9, A..F). Lettercase of the digits and of any leading X does not matter. A leading 0x is case-
sensitive and cannot be written as 0X.

Legal hexadecimal literals:

X'01AF'
X'01af'
x'01AF'
x'01af'
0x01AF
0x01af

Illegal hexadecimal literals:

X'0G'   (G is not a hexadecimal digit)
0X01AF  (0X must be written as 0x)

Values written using X'val' notation must contain an even number of digits or a syntax error occurs. To
correct the problem, pad the value with a leading zero:

mysql> SET @s = X'FFF';
ERROR 1064 (42000): You have an error in your SQL syntax;
check the manual that corresponds to your MySQL server
version for the right syntax to use near 'X'FFF''

mysql> SET @s = X'0FFF';
Query OK, 0 rows affected (0.00 sec)

Values written using 0xval notation that contain an odd number of digits are treated as having an extra
leading 0. For example, 0xaaa is interpreted as 0x0aaa.

By default, a hexadecimal literal is a binary string, where each pair of hexadecimal digits represents a
character:

mysql> SELECT X'4D7953514C', CHARSET(X'4D7953514C');
+---------------+------------------------+
| X'4D7953514C' | CHARSET(X'4D7953514C') |
+---------------+------------------------+
| MySQL         | binary                 |
+---------------+------------------------+
mysql> SELECT 0x5461626c65, CHARSET(0x5461626c65);
+--------------+-----------------------+
| 0x5461626c65 | CHARSET(0x5461626c65) |
+--------------+-----------------------+

1657

Bit-Value Literals

| cat       |
+-----------+

9.1.5 Bit-Value Literals

Bit-value literals are written using b'val' or 0bval notation. val is a binary value written using zeros and
ones. Lettercase of any leading b does not matter. A leading 0b is case-sensitive and cannot be written as
0B.

Legal bit-value literals:

b'01'
B'01'
0b01

Illegal bit-value literals:

b'2'    (2 is not a binary digit)
0B01    (0B must be written as 0b)

By default, a bit-value literal is a binary string:

mysql> SELECT b'1000001', CHARSET(b'1000001');
+------------+---------------------+
| b'1000001' | CHARSET(b'1000001') |
+------------+---------------------+
| A          | binary              |
+------------+---------------------+
mysql> SELECT 0b1100001, CHARSET(0b1100001);
+-----------+--------------------+
| 0b1100001 | CHARSET(0b1100001) |
+-----------+--------------------+
| a         | binary             |
+-----------+--------------------+

A bit-value literal may have an optional character set introducer and COLLATE clause, to designate it as a
string that uses a particular character set and collation:

[_charset_name] b'val' [COLLATE collation_name]

Examples:

SELECT _latin1 b'1000001';
SELECT _utf8 0b1000001 COLLATE utf8_danish_ci;

The examples use b'val' notation, but 0bval notation permits introducers as well. For information about
introducers, see Section 10.3.8, “Character Set Introducers”.

In numeric contexts, MySQL treats a bit literal like an integer. To ensure numeric treatment of a bit literal,
use it in numeric context. Ways to do this include adding 0 or using CAST(... AS UNSIGNED). For
example, a bit literal assigned to a user-defined variable is a binary string by default. To assign the value
as a number, use it in numeric context:

mysql> SET @v1 = b'1100001';
mysql> SET @v2 = b'1100001'+0;
mysql> SET @v3 = CAST(b'1100001' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| a    |   97 |   97 |
+------+------+------+

1659

Identifier Length Limits

In the select list of a query, a quoted column alias can be specified using identifier or string quoting
characters:

mysql> SELECT 1 AS `one`, 2 AS 'two';
+-----+-----+
| one | two |
+-----+-----+
|   1 |   2 |
+-----+-----+

Elsewhere in the statement, quoted references to the alias must use identifier quoting or the reference is
treated as a string literal.

It is recommended that you do not use names that begin with Me or MeN, where M and N are integers. For
example, avoid using 1e as an identifier, because an expression such as 1e+3 is ambiguous. Depending
on context, it might be interpreted as the expression 1e + 3 or as the number 1e+3.

Be careful when using MD5() to produce table names because it can produce names in illegal or
ambiguous formats such as those just described.

A user variable cannot be used directly in an SQL statement as an identifier or as part of an identifier. See
Section 9.4, “User-Defined Variables”, for more information and examples of workarounds.

Special characters in database and table names are encoded in the corresponding file system names as
described in Section 9.2.4, “Mapping of Identifiers to File Names”. If you have databases or tables from an
older version of MySQL that contain special characters and for which the underlying directory names or file
names have not been updated to use the new encoding, the server displays their names with a prefix of
#mysql50#. For information about referring to such names or converting them to the newer encoding, see
that section.

9.2.1 Identifier Length Limits

The following table describes the maximum length for each type of identifier.

Identifier Type

Database

Table

Column

Index

Constraint

Stored Program

View

Tablespace

Server

Log File Group

Alias

Maximum Length (characters)

64 (NDB storage engine: 63)

64 (NDB storage engine: 63)

64

64

64

64

64

64

64

64

256 (see exception following table)

Compound Statement Label

User-Defined Variable

16

64

Aliases for column names in CREATE VIEW statements are checked against the maximum column length
of 64 characters (not the maximum alias length of 256 characters).

1662

Identifier Qualifiers

Note

This syntax is deprecated as of MySQL 5.7.20; expect it to be removed in a future
version of MySQL.

The permitted qualifiers for object names depend on the object type:

• A database name is fully qualified and takes no qualifier:

CREATE DATABASE db1;

• A table, view, or stored program name may be given a database-name qualifier. Examples of unqualified

and qualified names in CREATE statements:

CREATE TABLE mytable ...;
CREATE VIEW myview ...;
CREATE PROCEDURE myproc ...;
CREATE FUNCTION myfunc ...;
CREATE EVENT myevent ...;

CREATE TABLE mydb.mytable ...;
CREATE VIEW mydb.myview ...;
CREATE PROCEDURE mydb.myproc ...;
CREATE FUNCTION mydb.myfunc ...;
CREATE EVENT mydb.myevent ...;

• A trigger is associated with a table, so any qualifier applies to the table name:

CREATE TRIGGER mytrigger ... ON mytable ...;

CREATE TRIGGER mytrigger ... ON mydb.mytable ...;

• A column name may be given multiple qualifiers to indicate context in statements that reference it, as

shown in the following table.

Column Reference

col_name

tbl_name.col_name

db_name.tbl_name.col_name

Meaning

Column col_name from whichever table used in
the statement contains a column of that name

Column col_name from table tbl_name of the
default database

Column col_name from table tbl_name of the
database db_name

In other words, a column name may be given a table-name qualifier, which itself may be given
a database-name qualifier. Examples of unqualified and qualified column references in SELECT
statements:

SELECT c1 FROM mytable
WHERE c2 > 100;

SELECT mytable.c1 FROM mytable
WHERE mytable.c2 > 100;

SELECT mydb.mytable.c1 FROM mydb.mytable
WHERE mydb.mytable.c2 > 100;

You need not specify a qualifier for an object reference in a statement unless the unqualified reference is
ambiguous. Suppose that column c1 occurs only in table t1, c2 only in t2, and c in both t1 and t2. Any

1664

Identifier Case Sensitivity

unqualified reference to c is ambiguous in a statement that refers to both tables and must be qualified as
t1.c or t2.c to indicate which table you mean:

SELECT c1, c2, t1.c FROM t1 INNER JOIN t2
WHERE t2.c > 100;

Similarly, to retrieve from a table t in database db1 and from a table t in database db2 in the same
statement, you must qualify the table references: For references to columns in those tables, qualifiers are
required only for column names that appear in both tables. Suppose that column c1 occurs only in table
db1.t, c2 only in db2.t, and c in both db1.t and db2.t. In this case, c is ambiguous and must be
qualified but c1 and c2 need not be:

SELECT c1, c2, db1.t.c FROM db1.t INNER JOIN db2.t
WHERE db2.t.c > 100;

Table aliases enable qualified column references to be written more simply:

SELECT c1, c2, t1.c FROM db1.t AS t1 INNER JOIN db2.t AS t2
WHERE t2.c > 100;

9.2.3 Identifier Case Sensitivity

In MySQL, databases correspond to directories within the data directory. Each table within a database
corresponds to at least one file within the database directory (and possibly more, depending on the
storage engine). Triggers also correspond to files. Consequently, the case sensitivity of the underlying
operating system plays a part in the case sensitivity of database, table, and trigger names. This means
such names are not case-sensitive in Windows, but are case-sensitive in most varieties of Unix. One
notable exception is macOS, which is Unix-based but uses a default file system type (HFS+) that is not
case-sensitive. However, macOS also supports UFS volumes, which are case-sensitive just as on any
Unix. See Section 1.6.1, “MySQL Extensions to Standard SQL”. The lower_case_table_names system
variable also affects how the server handles identifier case sensitivity, as described later in this section.

Note

Although database, table, and trigger names are not case-sensitive on some
platforms, you should not refer to one of these using different cases within the same
statement. The following statement would not work because it refers to a table both
as my_table and as MY_TABLE:

mysql> SELECT * FROM my_table WHERE MY_TABLE.col=1;

Column, index, stored routine, and event names are not case-sensitive on any platform, nor are column
aliases.

However, names of logfile groups are case-sensitive. This differs from standard SQL.

By default, table aliases are case-sensitive on Unix, but not so on Windows or macOS. The following
statement would not work on Unix, because it refers to the alias both as a and as A:

mysql> SELECT col_name FROM tbl_name AS a
       WHERE a.col_name = 1 OR A.col_name = 2;

However, this same statement is permitted on Windows. To avoid problems caused by such differences,
it is best to adopt a consistent convention, such as always creating and referring to databases and tables
using lowercase names. This convention is recommended for maximum portability and ease of use.

How table and database names are stored on disk and used in MySQL is affected by the
lower_case_table_names system variable, which you can set when starting mysqld.

1665

Mapping of Identifiers to File Names

RENAME TABLE T1 TO t1;

To convert one or more entire databases, dump them before setting lower_case_table_names, then
drop the databases, and reload them after setting lower_case_table_names:

1. Use mysqldump to dump each database:

mysqldump --databases db1 > db1.sql
mysqldump --databases db2 > db2.sql
...

Do this for each database that must be recreated.

2. Use DROP DATABASE to drop each database.

3. Stop the server, set lower_case_table_names, and restart the server.

4. Reload the dump file for each database. Because lower_case_table_names is set, each database

and table name is converted to lowercase as it is re-created:

mysql < db1.sql
mysql < db2.sql
...

Object names may be considered duplicates if their uppercase forms are equal according to a binary
collation. That is true for names of cursors, conditions, procedures, functions, savepoints, stored routine
parameters, stored program local variables, and plugins. It is not true for names of columns, constraints,
databases, partitions, statements prepared with PREPARE, tables, triggers, users, and user-defined
variables.

File system case sensitivity can affect searches in string columns of INFORMATION_SCHEMA tables. For
more information, see Section 10.8.7, “Using Collation in INFORMATION_SCHEMA Searches”.

9.2.4 Mapping of Identifiers to File Names

There is a correspondence between database and table identifiers and names in the file system. For the
basic structure, MySQL represents each database as a directory in the data directory, and each table by
one or more files in the appropriate database directory. For the table format files (.FRM), the data is always
stored in this structure and location.

For the data and index files, the exact representation on disk is storage engine specific. These files
may be stored in the same location as the FRM files, or the information may be stored in a separate file.
InnoDB data is stored in the InnoDB data files. If you are using tablespaces with InnoDB, then the specific
tablespace files you create are used instead.

Any character is legal in database or table identifiers except ASCII NUL (X'00'). MySQL encodes
any characters that are problematic in the corresponding file system objects when it creates database
directories or table files:

• Basic Latin letters (a..zA..Z), digits (0..9) and underscore (_) are encoded as is. Consequently, their

case sensitivity directly depends on file system features.

• All other national letters from alphabets that have uppercase/lowercase mapping are encoded as shown

in the following table. Values in the Code Range column are UCS-2 values.

Code Range

Pattern

Number

00C0..017F

[@][0..4][g..z]

5*20= 100

Used

97

Unused

Blocks

3

Latin-1
Supplement +

1667

Mapping of Identifiers to File Names

Code Range

Pattern

Number

Used

Unused

0370..03FF

[@][5..9][g..z]

5*20= 100

88

0400..052F

[@][g..z][0..6]

20*7= 140

0530..058F

[@][g..z][7..8]

20*2= 40

2160..217F

[@][g..z][9]

20*1= 20

0180..02AF

[@][g..z][a..k]

20*11=220

1E00..1EFF

[@][g..z][l..r]

20*7= 140

1F00..1FFF

[@][g..z][s..z]

20*8= 160

.... ....

[@][a..f][g..z]

6*20= 120

24B6..24E9

[@][@][a..z]

FF21..FF5A

[@][a..z][@]

26

26

137

38

16

203

136

144

0

26

26

12

3

2

4

17

4

16

120

0

0

Blocks
Latin Extended-
A

Greek and
Coptic

Cyrillic + Cyrillic
Supplement

Armenian

Number Forms

Latin Extended-
B + IPA
Extensions

Latin Extended
Additional

Greek Extended

RESERVED

Enclosed
Alphanumerics

Halfwidth and
Fullwidth forms

One of the bytes in the sequence encodes lettercase. For example: LATIN CAPITAL LETTER A WITH
GRAVE is encoded as @0G, whereas LATIN SMALL LETTER A WITH GRAVE is encoded as @0g. Here
the third byte (G or g) indicates lettercase. (On a case-insensitive file system, both letters are treated as
the same.)

For some blocks, such as Cyrillic, the second byte determines lettercase. For other blocks, such as
Latin1 Supplement, the third byte determines lettercase. If two bytes in the sequence are letters (as
in Greek Extended), the leftmost letter character stands for lettercase. All other letter bytes must be in
lowercase.

• All nonletter characters except underscore (_), as well as letters from alphabets that do not have

uppercase/lowercase mapping (such as Hebrew) are encoded using hexadecimal representation using
lowercase letters for hexadecimal digits a..f:

0x003F -> @003f
0xFFFF -> @ffff

The hexadecimal values correspond to character values in the ucs2 double-byte character set.

On Windows, some names such as nul, prn, and aux are encoded by appending @@@ to the name when
the server creates the corresponding file or directory. This occurs on all platforms for portability of the
corresponding database object between platforms.

If you have databases or tables from a version of MySQL older than 5.1.6 that contain special
characters and for which the underlying directory names or file names have not been updated to use
the new encoding, the server displays their names with a prefix of #mysql50# in the output from
INFORMATION_SCHEMA tables or SHOW statements. For example, if you have a table named a@b and its
name encoding has not been updated, SHOW TABLES displays it like this:

mysql> SHOW TABLES;
+----------------+

1668

Function Name Parsing and Resolution

| Tables_in_test |
+----------------+
| #mysql50#a@b   |
+----------------+

To refer to such a name for which the encoding has not been updated, you must supply the #mysql50#
prefix:

mysql> SHOW COLUMNS FROM `a@b`;
ERROR 1146 (42S02): Table 'test.a@b' doesn't exist

mysql> SHOW COLUMNS FROM `#mysql50#a@b`;
+-------+---------+------+-----+---------+-------+
| Field | Type    | Null | Key | Default | Extra |
+-------+---------+------+-----+---------+-------+
| i     | int(11) | YES  |     | NULL    |       |
+-------+---------+------+-----+---------+-------+

To update old names to eliminate the need to use the special prefix to refer to them, re-encode them with
mysqlcheck. The following commands update all names to the new encoding:

mysqlcheck --check-upgrade --all-databases
mysqlcheck --fix-db-names --fix-table-names --all-databases

To check only specific databases or tables, omit --all-databases and provide the appropriate
database or table arguments. For information about mysqlcheck invocation syntax, see Section 4.5.3,
“mysqlcheck — A Table Maintenance Program”.

Note

The #mysql50# prefix is intended only to be used internally by the server. You
should not create databases or tables with names that use this prefix.

Also, mysqlcheck cannot fix names that contain literal instances of the @ character
that is used for encoding special characters. If you have databases or tables that
contain this character, use mysqldump to dump them before upgrading to MySQL
5.1.6 or later, and then reload the dump file after upgrading.

Note

Conversion of pre-MySQL 5.1 database names containing special characters to
5.1 format with the addition of a #mysql50# prefix is deprecated; expect it to be
removed in a future version of MySQL. Because such conversions are deprecated,
the --fix-db-names and --fix-table-names options for mysqlcheck
and the UPGRADE DATA DIRECTORY NAME clause for the ALTER DATABASE
statement are also deprecated.

Upgrades are supported only from one release series to another (for example, 5.0
to 5.1, or 5.1 to 5.5), so there should be little remaining need for conversion of older
5.0 database names to current versions of MySQL. As a workaround, upgrade a
MySQL 5.0 installation to MySQL 5.1 before upgrading to a more recent release.

9.2.5 Function Name Parsing and Resolution

MySQL supports built-in (native) functions, loadable functions, and stored functions. This section describes
how the server recognizes whether the name of a built-in function is used as a function call or as an
identifier, and how the server determines which function to use in cases when functions of different types
exist with a given name.

1669

Function Name Parsing and Resolution

• EXTRACT

• GROUP_CONCAT

• MAX

• MID

• MIN

• NOW

• POSITION

• SESSION_USER

• STD

• STDDEV

• STDDEV_POP

• STDDEV_SAMP

• SUBDATE

• SUBSTR

• SUBSTRING

• SUM

• SYSDATE

• SYSTEM_USER

• TRIM

• VARIANCE

• VAR_POP

• VAR_SAMP

For functions not listed as special in sql/lex.h, whitespace does not matter. They are interpreted as
function calls only when used in expression context and may be used freely as identifiers otherwise. ASCII
is one such name. However, for these nonaffected function names, interpretation may vary in expression
context: func_name () is interpreted as a built-in function if there is one with the given name; if not,
func_name () is interpreted as a loadable function or stored function if one exists with that name.

The IGNORE_SPACE SQL mode can be used to modify how the parser treats function names that are
whitespace-sensitive:

• With IGNORE_SPACE disabled, the parser interprets the name as a function call when there is no

whitespace between the name and the following parenthesis. This occurs even when the function name
is used in nonexpression context:

mysql> CREATE TABLE count(i INT);
ERROR 1064 (42000): You have an error in your SQL syntax ...
near 'count(i INT)'

1671

Function Name Parsing and Resolution

To eliminate the error and cause the name to be treated as an identifier, either use whitespace following
the name or write it as a quoted identifier (or both):

CREATE TABLE count (i INT);
CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);

• With IGNORE_SPACE enabled, the parser loosens the requirement that there be no whitespace between
the function name and the following parenthesis. This provides more flexibility in writing function calls.
For example, either of the following function calls are legal:

SELECT COUNT(*) FROM mytable;
SELECT COUNT (*) FROM mytable;

However, enabling IGNORE_SPACE also has the side effect that the parser treats the affected function
names as reserved words (see Section 9.3, “Keywords and Reserved Words”). This means that a space
following the name no longer signifies its use as an identifier. The name can be used in function calls
with or without following whitespace, but causes a syntax error in nonexpression context unless it is
quoted. For example, with IGNORE_SPACE enabled, both of the following statements fail with a syntax
error because the parser interprets count as a reserved word:

CREATE TABLE count(i INT);
CREATE TABLE count (i INT);

To use the function name in nonexpression context, write it as a quoted identifier:

CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);

To enable the IGNORE_SPACE SQL mode, use this statement:

SET sql_mode = 'IGNORE_SPACE';

IGNORE_SPACE is also enabled by certain other composite modes such as ANSI that include it in their
value:

SET sql_mode = 'ANSI';

Check Section 5.1.10, “Server SQL Modes”, to see which composite modes enable IGNORE_SPACE.

To minimize the dependency of SQL code on the IGNORE_SPACE setting, use these guidelines:

• Avoid creating loadable functions or stored functions that have the same name as a built-in function.

• Avoid using function names in nonexpression context. For example, these statements use count (one
of the affected function names affected by IGNORE_SPACE), so they fail with or without whitespace
following the name if IGNORE_SPACE is enabled:

CREATE TABLE count(i INT);
CREATE TABLE count (i INT);

If you must use a function name in nonexpression context, write it as a quoted identifier:

CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);

Function Name Resolution

The following rules describe how the server resolves references to function names for function creation
and invocation:

1672

Keywords and Reserved Words

• Built-in functions and loadable functions

An error occurs if you try to create a loadable function with the same name as a built-in function.

• Built-in functions and stored functions

It is possible to create a stored function with the same name as a built-in function, but to invoke
the stored function it is necessary to qualify it with a schema name. For example, if you create a
stored function named PI in the test schema, invoke it as test.PI() because the server resolves
PI() without a qualifier as a reference to the built-in function. The server generates a warning if the
stored function name collides with a built-in function name. The warning can be displayed with SHOW
WARNINGS.

• Loadable functions and stored functions

Loadable functions and stored functions share the same namespace, so you cannot create a loadable
function and a stored function with the same name.

The preceding function name resolution rules have implications for upgrading to versions of MySQL that
implement new built-in functions:

• If you have already created a loadable function with a given name and upgrade MySQL to a version that
implements a new built-in function with the same name, the loadable function becomes inaccessible. To
correct this, use DROP FUNCTION to drop the loadable function and CREATE FUNCTION to re-create
the loadable function with a different nonconflicting name. Then modify any affected code to use the new
name.

• If a new version of MySQL implements a built-in function with the same name as an existing stored

function, you have two choices: Rename the stored function to use a nonconflicting name, or change
calls to the function so that they use a schema qualifier (that is, use schema_name.func_name()
syntax). In either case, modify any affected code accordingly.

9.3 Keywords and Reserved Words

Keywords are words that have significance in SQL. Certain keywords, such as SELECT, DELETE, or
BIGINT, are reserved and require special treatment for use as identifiers such as table and column names.
This may also be true for the names of built-in functions.

Nonreserved keywords are permitted as identifiers without quoting. Reserved words are permitted as
identifiers if you quote them as described in Section 9.2, “Schema Object Names”:

mysql> CREATE TABLE interval (begin INT, end INT);
ERROR 1064 (42000): You have an error in your SQL syntax ...
near 'interval (begin INT, end INT)'

BEGIN and END are keywords but not reserved, so their use as identifiers does not require quoting.
INTERVAL is a reserved keyword and must be quoted to be used as an identifier:

mysql> CREATE TABLE `interval` (begin INT, end INT);
Query OK, 0 rows affected (0.01 sec)

Exception: A word that follows a period in a qualified name must be an identifier, so it need not be quoted
even if it is reserved:

mysql> CREATE TABLE mydb.interval (begin INT, end INT);
Query OK, 0 rows affected (0.01 sec)

Names of built-in functions are permitted as identifiers but may require care to be used as such. For
example, COUNT is acceptable as a column name. However, by default, no whitespace is permitted in

1673

MySQL 5.7 Keywords and Reserved Words

function invocations between the function name and the following ( character. This requirement enables
the parser to distinguish whether the name is used in a function call or in nonfunction context. For further
details on recognition of function names, see Section 9.2.5, “Function Name Parsing and Resolution”.

• MySQL 5.7 Keywords and Reserved Words

• MySQL 5.7 New Keywords and Reserved Words

• MySQL 5.7 Removed Keywords and Reserved Words

MySQL 5.7 Keywords and Reserved Words

The following list shows the keywords and reserved words in MySQL 5.7, along with changes to individual
words from version to version. Reserved keywords are marked with (R). In addition, _FILENAME is
reserved.

At some point, you might upgrade to a higher version, so it is a good idea to have a look at future reserved
words, too. You can find these in the manuals that cover higher versions of MySQL. Most of the reserved
words in the list are forbidden by standard SQL as column or table names (for example, GROUP). A few are
reserved because MySQL needs them and uses a yacc parser.

A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z

A

• ACCESSIBLE (R)

• ACCOUNT; added in 5.7.6 (nonreserved)

• ACTION

• ADD (R)

• AFTER

• AGAINST

• AGGREGATE

• ALGORITHM

• ALL (R)

• ALTER (R)

• ALWAYS; added in 5.7.6 (nonreserved)

• ANALYSE

• ANALYZE (R)

• AND (R)

• ANY

• AS (R)

• ASC (R)

1674

MySQL 5.7 Keywords and Reserved Words

• ASCII

• ASENSITIVE (R)

• AT

• AUTOEXTEND_SIZE

• AUTO_INCREMENT

• AVG

• AVG_ROW_LENGTH

B

• BACKUP

• BEFORE (R)

• BEGIN

• BETWEEN (R)

• BIGINT (R)

• BINARY (R)

• BINLOG

• BIT

• BLOB (R)

• BLOCK

• BOOL

• BOOLEAN

• BOTH (R)

• BTREE

• BY (R)

• BYTE

C

• CACHE

• CALL (R)

• CASCADE (R)

• CASCADED

• CASE (R)

1675

MySQL 5.7 Keywords and Reserved Words

• CATALOG_NAME

• CHAIN

• CHANGE (R)

• CHANGED

• CHANNEL; added in 5.7.6 (nonreserved)

• CHAR (R)

• CHARACTER (R)

• CHARSET

• CHECK (R)

• CHECKSUM

• CIPHER

• CLASS_ORIGIN

• CLIENT

• CLOSE

• COALESCE

• CODE

• COLLATE (R)

• COLLATION

• COLUMN (R)

• COLUMNS

• COLUMN_FORMAT

• COLUMN_NAME

• COMMENT

• COMMIT

• COMMITTED

• COMPACT

• COMPLETION

• COMPRESSED

• COMPRESSION; added in 5.7.8 (nonreserved)

• CONCURRENT

1676

MySQL 5.7 Keywords and Reserved Words

• CONDITION (R)

• CONNECTION

• CONSISTENT

• CONSTRAINT (R)

• CONSTRAINT_CATALOG

• CONSTRAINT_NAME

• CONSTRAINT_SCHEMA

• CONTAINS

• CONTEXT

• CONTINUE (R)

• CONVERT (R)

• CPU

• CREATE (R)

• CROSS (R)

• CUBE

• CURRENT

• CURRENT_DATE (R)

• CURRENT_TIME (R)

• CURRENT_TIMESTAMP (R)

• CURRENT_USER (R)

• CURSOR (R)

• CURSOR_NAME

D

• DATA

• DATABASE (R)

• DATABASES (R)

• DATAFILE

• DATE

• DATETIME

• DAY

1677

MySQL 5.7 Keywords and Reserved Words

• DAY_HOUR (R)

• DAY_MICROSECOND (R)

• DAY_MINUTE (R)

• DAY_SECOND (R)

• DEALLOCATE

• DEC (R)

• DECIMAL (R)

• DECLARE (R)

• DEFAULT (R)

• DEFAULT_AUTH

• DEFINER

• DELAYED (R)

• DELAY_KEY_WRITE

• DELETE (R)

• DESC (R)

• DESCRIBE (R)

• DES_KEY_FILE

• DETERMINISTIC (R)

• DIAGNOSTICS

• DIRECTORY

• DISABLE

• DISCARD

• DISK

• DISTINCT (R)

• DISTINCTROW (R)

• DIV (R)

• DO

• DOUBLE (R)

• DROP (R)

• DUAL (R)

1678

MySQL 5.7 Keywords and Reserved Words

• DUMPFILE

• DUPLICATE

• DYNAMIC

E

• EACH (R)

• ELSE (R)

• ELSEIF (R)

• ENABLE

• ENCLOSED (R)

• ENCRYPTION; added in 5.7.11 (nonreserved)

• END

• ENDS

• ENGINE

• ENGINES

• ENUM

• ERROR

• ERRORS

• ESCAPE

• ESCAPED (R)

• EVENT

• EVENTS

• EVERY

• EXCHANGE

• EXECUTE

• EXISTS (R)

• EXIT (R)

• EXPANSION

• EXPIRE

• EXPLAIN (R)

• EXPORT

1679

MySQL 5.7 Keywords and Reserved Words

• EXTENDED

• EXTENT_SIZE

F

• FALSE (R)

• FAST

• FAULTS

• FETCH (R)

• FIELDS

• FILE

• FILE_BLOCK_SIZE; added in 5.7.6 (nonreserved)

• FILTER; added in 5.7.3 (nonreserved)

• FIRST

• FIXED

• FLOAT (R)

• FLOAT4 (R)

• FLOAT8 (R)

• FLUSH

• FOLLOWS; added in 5.7.2 (nonreserved)

• FOR (R)

• FORCE (R)

• FOREIGN (R)

• FORMAT

• FOUND

• FROM (R)

• FULL

• FULLTEXT (R)

• FUNCTION

G

• GENERAL

• GENERATED (R); added in 5.7.6 (reserved)

1680

MySQL 5.7 Keywords and Reserved Words

• GEOMETRY

• GEOMETRYCOLLECTION

• GET (R)

• GET_FORMAT

• GLOBAL

• GRANT (R)

• GRANTS

• GROUP (R)

• GROUP_REPLICATION; added in 5.7.6 (nonreserved)

H

• HANDLER

• HASH

• HAVING (R)

• HELP

• HIGH_PRIORITY (R)

• HOST

• HOSTS

• HOUR

• HOUR_MICROSECOND (R)

• HOUR_MINUTE (R)

• HOUR_SECOND (R)

I

• IDENTIFIED

• IF (R)

• IGNORE (R)

• IGNORE_SERVER_IDS

• IMPORT

• IN (R)

• INDEX (R)

• INDEXES

1681

MySQL 5.7 Keywords and Reserved Words

• INFILE (R)

• INITIAL_SIZE

• INNER (R)

• INOUT (R)

• INSENSITIVE (R)

• INSERT (R)

• INSERT_METHOD

• INSTALL

• INSTANCE; added in 5.7.11 (nonreserved)

• INT (R)

• INT1 (R)

• INT2 (R)

• INT3 (R)

• INT4 (R)

• INT8 (R)

• INTEGER (R)

• INTERVAL (R)

• INTO (R)

• INVOKER

• IO

• IO_AFTER_GTIDS (R)

• IO_BEFORE_GTIDS (R)

• IO_THREAD

• IPC

• IS (R)

• ISOLATION

• ISSUER

• ITERATE (R)

J

• JOIN (R)

1682

MySQL 5.7 Keywords and Reserved Words

• JSON; added in 5.7.8 (nonreserved)

K

• KEY (R)

• KEYS (R)

• KEY_BLOCK_SIZE

• KILL (R)

L

• LANGUAGE

• LAST

• LEADING (R)

• LEAVE (R)

• LEAVES

• LEFT (R)

• LESS

• LEVEL

• LIKE (R)

• LIMIT (R)

• LINEAR (R)

• LINES (R)

• LINESTRING

• LIST

• LOAD (R)

• LOCAL

• LOCALTIME (R)

• LOCALTIMESTAMP (R)

• LOCK (R)

• LOCKS

• LOGFILE

• LOGS

• LONG (R)

1683

MySQL 5.7 Keywords and Reserved Words

• LONGBLOB (R)

• LONGTEXT (R)

• LOOP (R)

• LOW_PRIORITY (R)

M

• MASTER

• MASTER_AUTO_POSITION

• MASTER_BIND (R)

• MASTER_CONNECT_RETRY

• MASTER_DELAY

• MASTER_HEARTBEAT_PERIOD

• MASTER_HOST

• MASTER_LOG_FILE

• MASTER_LOG_POS

• MASTER_PASSWORD

• MASTER_PORT

• MASTER_RETRY_COUNT

• MASTER_SERVER_ID

• MASTER_SSL

• MASTER_SSL_CA

• MASTER_SSL_CAPATH

• MASTER_SSL_CERT

• MASTER_SSL_CIPHER

• MASTER_SSL_CRL

• MASTER_SSL_CRLPATH

• MASTER_SSL_KEY

• MASTER_SSL_VERIFY_SERVER_CERT (R)

• MASTER_TLS_VERSION; added in 5.7.10 (nonreserved)

• MASTER_USER

• MATCH (R)

1684

MySQL 5.7 Keywords and Reserved Words

• MAXVALUE (R)

• MAX_CONNECTIONS_PER_HOUR

• MAX_QUERIES_PER_HOUR

• MAX_ROWS

• MAX_SIZE

• MAX_STATEMENT_TIME; added in 5.7.4 (nonreserved); removed in 5.7.8

• MAX_UPDATES_PER_HOUR

• MAX_USER_CONNECTIONS

• MEDIUM

• MEDIUMBLOB (R)

• MEDIUMINT (R)

• MEDIUMTEXT (R)

• MEMORY

• MERGE

• MESSAGE_TEXT

• MICROSECOND

• MIDDLEINT (R)

• MIGRATE

• MINUTE

• MINUTE_MICROSECOND (R)

• MINUTE_SECOND (R)

• MIN_ROWS

• MOD (R)

• MODE

• MODIFIES (R)

• MODIFY

• MONTH

• MULTILINESTRING

• MULTIPOINT

• MULTIPOLYGON

1685

MySQL 5.7 Keywords and Reserved Words

• MUTEX

• MYSQL_ERRNO

N

• NAME

• NAMES

• NATIONAL

• NATURAL (R)

• NCHAR

• NDB

• NDBCLUSTER

• NEVER; added in 5.7.4 (nonreserved)

• NEW

• NEXT

• NO

• NODEGROUP

• NONBLOCKING; removed in 5.7.6

• NONE

• NOT (R)

• NO_WAIT

• NO_WRITE_TO_BINLOG (R)

• NULL (R)

• NUMBER

• NUMERIC (R)

• NVARCHAR

O

• OFFSET

• OLD_PASSWORD; removed in 5.7.5

• ON (R)

• ONE

• ONLY

1686

MySQL 5.7 Keywords and Reserved Words

• OPEN

• OPTIMIZE (R)

• OPTIMIZER_COSTS (R); added in 5.7.5 (reserved)

• OPTION (R)

• OPTIONALLY (R)

• OPTIONS

• OR (R)

• ORDER (R)

• OUT (R)

• OUTER (R)

• OUTFILE (R)

• OWNER

P

• PACK_KEYS

• PAGE

• PARSER

• PARSE_GCOL_EXPR; added in 5.7.6 (reserved); became nonreserved in 5.7.8

• PARTIAL

• PARTITION (R)

• PARTITIONING

• PARTITIONS

• PASSWORD

• PHASE

• PLUGIN

• PLUGINS

• PLUGIN_DIR

• POINT

• POLYGON

• PORT

• PRECEDES; added in 5.7.2 (nonreserved)

1687

MySQL 5.7 Keywords and Reserved Words

• PRECISION (R)

• PREPARE

• PRESERVE

• PREV

• PRIMARY (R)

• PRIVILEGES

• PROCEDURE (R)

• PROCESSLIST

• PROFILE

• PROFILES

• PROXY

• PURGE (R)

Q

• QUARTER

• QUERY

• QUICK

R

• RANGE (R)

• READ (R)

• READS (R)

• READ_ONLY

• READ_WRITE (R)

• REAL (R)

• REBUILD

• RECOVER

• REDOFILE

• REDO_BUFFER_SIZE

• REDUNDANT

• REFERENCES (R)

• REGEXP (R)

1688

MySQL 5.7 Keywords and Reserved Words

• RELAY

• RELAYLOG

• RELAY_LOG_FILE

• RELAY_LOG_POS

• RELAY_THREAD

• RELEASE (R)

• RELOAD

• REMOVE

• RENAME (R)

• REORGANIZE

• REPAIR

• REPEAT (R)

• REPEATABLE

• REPLACE (R)

• REPLICATE_DO_DB; added in 5.7.3 (nonreserved)

• REPLICATE_DO_TABLE; added in 5.7.3 (nonreserved)

• REPLICATE_IGNORE_DB; added in 5.7.3 (nonreserved)

• REPLICATE_IGNORE_TABLE; added in 5.7.3 (nonreserved)

• REPLICATE_REWRITE_DB; added in 5.7.3 (nonreserved)

• REPLICATE_WILD_DO_TABLE; added in 5.7.3 (nonreserved)

• REPLICATE_WILD_IGNORE_TABLE; added in 5.7.3 (nonreserved)

• REPLICATION

• REQUIRE (R)

• RESET

• RESIGNAL (R)

• RESTORE

• RESTRICT (R)

• RESUME

• RETURN (R)

• RETURNED_SQLSTATE

1689

MySQL 5.7 Keywords and Reserved Words

• RETURNS

• REVERSE

• REVOKE (R)

• RIGHT (R)

• RLIKE (R)

• ROLLBACK

• ROLLUP

• ROTATE; added in 5.7.11 (nonreserved)

• ROUTINE

• ROW

• ROWS

• ROW_COUNT

• ROW_FORMAT

• RTREE

S

• SAVEPOINT

• SCHEDULE

• SCHEMA (R)

• SCHEMAS (R)

• SCHEMA_NAME

• SECOND

• SECOND_MICROSECOND (R)

• SECURITY

• SELECT (R)

• SENSITIVE (R)

• SEPARATOR (R)

• SERIAL

• SERIALIZABLE

• SERVER

• SESSION

1690

MySQL 5.7 Keywords and Reserved Words

• SET (R)

• SHARE

• SHOW (R)

• SHUTDOWN

• SIGNAL (R)

• SIGNED

• SIMPLE

• SLAVE

• SLOW

• SMALLINT (R)

• SNAPSHOT

• SOCKET

• SOME

• SONAME

• SOUNDS

• SOURCE

• SPATIAL (R)

• SPECIFIC (R)

• SQL (R)

• SQLEXCEPTION (R)

• SQLSTATE (R)

• SQLWARNING (R)

• SQL_AFTER_GTIDS

• SQL_AFTER_MTS_GAPS

• SQL_BEFORE_GTIDS

• SQL_BIG_RESULT (R)

• SQL_BUFFER_RESULT

• SQL_CACHE

• SQL_CALC_FOUND_ROWS (R)

• SQL_NO_CACHE

1691

MySQL 5.7 Keywords and Reserved Words

• SQL_SMALL_RESULT (R)

• SQL_THREAD

• SQL_TSI_DAY

• SQL_TSI_HOUR

• SQL_TSI_MINUTE

• SQL_TSI_MONTH

• SQL_TSI_QUARTER

• SQL_TSI_SECOND

• SQL_TSI_WEEK

• SQL_TSI_YEAR

• SSL (R)

• STACKED

• START

• STARTING (R)

• STARTS

• STATS_AUTO_RECALC

• STATS_PERSISTENT

• STATS_SAMPLE_PAGES

• STATUS

• STOP

• STORAGE

• STORED (R); added in 5.7.6 (reserved)

• STRAIGHT_JOIN (R)

• STRING

• SUBCLASS_ORIGIN

• SUBJECT

• SUBPARTITION

• SUBPARTITIONS

• SUPER

• SUSPEND

1692

MySQL 5.7 Keywords and Reserved Words

• SWAPS

• SWITCHES

T

• TABLE (R)

• TABLES

• TABLESPACE

• TABLE_CHECKSUM

• TABLE_NAME

• TEMPORARY

• TEMPTABLE

• TERMINATED (R)

• TEXT

• THAN

• THEN (R)

• TIME

• TIMESTAMP

• TIMESTAMPADD

• TIMESTAMPDIFF

• TINYBLOB (R)

• TINYINT (R)

• TINYTEXT (R)

• TO (R)

• TRAILING (R)

• TRANSACTION

• TRIGGER (R)

• TRIGGERS

• TRUE (R)

• TRUNCATE

• TYPE

• TYPES

1693

MySQL 5.7 Keywords and Reserved Words

U

• UNCOMMITTED

• UNDEFINED

• UNDO (R)

• UNDOFILE

• UNDO_BUFFER_SIZE

• UNICODE

• UNINSTALL

• UNION (R)

• UNIQUE (R)

• UNKNOWN

• UNLOCK (R)

• UNSIGNED (R)

• UNTIL

• UPDATE (R)

• UPGRADE

• USAGE (R)

• USE (R)

• USER

• USER_RESOURCES

• USE_FRM

• USING (R)

• UTC_DATE (R)

• UTC_TIME (R)

• UTC_TIMESTAMP (R)

V

• VALIDATION; added in 5.7.5 (nonreserved)

• VALUE

• VALUES (R)

• VARBINARY (R)

1694

MySQL 5.7 Keywords and Reserved Words

• VARCHAR (R)

• VARCHARACTER (R)

• VARIABLES

• VARYING (R)

• VIEW

• VIRTUAL (R); added in 5.7.6 (reserved)

W

• WAIT

• WARNINGS

• WEEK

• WEIGHT_STRING

• WHEN (R)

• WHERE (R)

• WHILE (R)

• WITH (R)

• WITHOUT; added in 5.7.5 (nonreserved)

• WORK

• WRAPPER

• WRITE (R)

X

• X509

• XA

• XID; added in 5.7.5 (nonreserved)

• XML

• XOR (R)

Y

• YEAR

• YEAR_MONTH (R)

Z

• ZEROFILL (R)

1695

MySQL 5.7 New Keywords and Reserved Words

MySQL 5.7 New Keywords and Reserved Words

The following list shows the keywords and reserved words that are added in MySQL 5.7, compared to
MySQL 5.6. Reserved keywords are marked with (R).

A | C | E | F | G | I | J | M | N | O | P | R | S | V | W | X

A

• ACCOUNT

• ALWAYS

C

• CHANNEL

• COMPRESSION

E

• ENCRYPTION

F

• FILE_BLOCK_SIZE

• FILTER

• FOLLOWS

G

• GENERATED (R)

• GROUP_REPLICATION

I

• INSTANCE

J

• JSON

M

• MASTER_TLS_VERSION

N

• NEVER

O

• OPTIMIZER_COSTS (R)

P

• PARSE_GCOL_EXPR

1696

MySQL 5.7 Removed Keywords and Reserved Words

• PRECEDES

R

• REPLICATE_DO_DB

• REPLICATE_DO_TABLE

• REPLICATE_IGNORE_DB

• REPLICATE_IGNORE_TABLE

• REPLICATE_REWRITE_DB

• REPLICATE_WILD_DO_TABLE

• REPLICATE_WILD_IGNORE_TABLE

• ROTATE

S

• STACKED

• STORED (R)

V

• VALIDATION

• VIRTUAL (R)

W

• WITHOUT

X

• XID

MySQL 5.7 Removed Keywords and Reserved Words

The following list shows the keywords and reserved words that are removed in MySQL 5.7, compared to
MySQL 5.6. Reserved keywords are marked with (R).

• OLD_PASSWORD

9.4 User-Defined Variables

You can store a value in a user-defined variable in one statement and refer to it later in another statement.
This enables you to pass values from one statement to another.

User variables are written as @var_name, where the variable name var_name consists of alphanumeric
characters, ., _, and $. A user variable name can contain other characters if you quote it as a string or
identifier (for example, @'my-var', @"my-var", or @`my-var`).

User-defined variables are session specific. A user variable defined by one client cannot be
seen or used by other clients. (Exception: A user with access to the Performance Schema

1697

User-Defined Variables

user_variables_by_thread table can see all user variables for all sessions.) All variables for a given
client session are automatically freed when that client exits.

User variable names are not case-sensitive. Names have a maximum length of 64 characters.

One way to set a user-defined variable is by issuing a SET statement:

SET @var_name = expr [, @var_name = expr] ...

For SET, either = or := can be used as the assignment operator.

User variables can be assigned a value from a limited set of data types: integer, decimal, floating-point,
binary or nonbinary string, or NULL value. Assignment of decimal and real values does not preserve the
precision or scale of the value. A value of a type other than one of the permissible types is converted to
a permissible type. For example, a value having a temporal or spatial data type is converted to a binary
string. A value having the JSON data type is converted to a string with a character set of utf8mb4 and a
collation of utf8mb4_bin.

If a user variable is assigned a nonbinary (character) string value, it has the same character set and
collation as the string. The coercibility of user variables is implicit. (This is the same coercibility as for table
column values.)

Hexadecimal or bit values assigned to user variables are treated as binary strings. To assign a
hexadecimal or bit value as a number to a user variable, use it in numeric context. For example, add 0 or
use CAST(... AS UNSIGNED):

mysql> SET @v1 = X'41';
mysql> SET @v2 = X'41'+0;
mysql> SET @v3 = CAST(X'41' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    |   65 |   65 |
+------+------+------+
mysql> SET @v1 = b'1000001';
mysql> SET @v2 = b'1000001'+0;
mysql> SET @v3 = CAST(b'1000001' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    |   65 |   65 |
+------+------+------+

If the value of a user variable is selected in a result set, it is returned to the client as a string.

If you refer to a variable that has not been initialized, it has a value of NULL and a type of string.

User variables may be used in most contexts where expressions are permitted. This does not currently
include contexts that explicitly require a literal value, such as in the LIMIT clause of a SELECT statement,
or the IGNORE N LINES clause of a LOAD DATA statement.

It is also possible to assign a value to a user variable in statements other than SET. (This functionality is
deprecated in MySQL 8.0 and subject to removal in a subsequent release.) When making an assignment
in this way, the assignment operator must be := and not = because the latter is treated as the comparison
operator = in statements other than SET:

mysql> SET @t1=1, @t2=2, @t3:=4;
mysql> SELECT @t1, @t2, @t3, @t4 := @t1+@t2+@t3;

1698

User-Defined Variables

+------+------+------+--------------------+
| @t1  | @t2  | @t3  | @t4 := @t1+@t2+@t3 |
+------+------+------+--------------------+
|    1 |    2 |    4 |                  7 |
+------+------+------+--------------------+

As a general rule, other than in SET statements, you should never assign a value to a user variable and
read the value within the same statement. For example, to increment a variable, this is okay:

SET @a = @a + 1;

For other statements, such as SELECT, you might get the results you expect, but this is not guaranteed.
In the following statement, you might think that MySQL evaluates @a first and then does an assignment
second:

SELECT @a, @a:=@a+1, ...;

However, the order of evaluation for expressions involving user variables is undefined.

Another issue with assigning a value to a variable and reading the value within the same non-SET
statement is that the default result type of a variable is based on its type at the start of the statement. The
following example illustrates this:

mysql> SET @a='test';
mysql> SELECT @a,(@a:=20) FROM tbl_name;

For this SELECT statement, MySQL reports to the client that column one is a string and converts all
accesses of @a to strings, even though @a is set to a number for the second row. After the SELECT
statement executes, @a is regarded as a number for the next statement.

To avoid problems with this behavior, either do not assign a value to and read the value of the same
variable within a single statement, or else set the variable to 0, 0.0, or '' to define its type before you use
it.

In a SELECT statement, each select expression is evaluated only when sent to the client. This means that
in a HAVING, GROUP BY, or ORDER BY clause, referring to a variable that is assigned a value in the select
expression list does not work as expected:

mysql> SELECT (@aa:=id) AS a, (@aa+3) AS b FROM tbl_name HAVING b=5;

The reference to b in the HAVING clause refers to an alias for an expression in the select list that uses
@aa. This does not work as expected: @aa contains the value of id from the previous selected row, not
from the current row.

User variables are intended to provide data values. They cannot be used directly in an SQL statement as
an identifier or as part of an identifier, such as in contexts where a table or database name is expected, or
as a reserved word such as SELECT. This is true even if the variable is quoted, as shown in the following
example:

mysql> SELECT c1 FROM t;
+----+
| c1 |
+----+
|  0 |
+----+
|  1 |
+----+
2 rows in set (0.00 sec)

mysql> SET @col = "c1";

1699

User-Defined Variables

Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| c1   |
+------+
1 row in set (0.00 sec)

mysql> SELECT `@col` FROM t;
ERROR 1054 (42S22): Unknown column '@col' in 'field list'

mysql> SET @col = "`c1`";
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+
| @col |
+------+
| `c1` |
+------+
1 row in set (0.00 sec)

An exception to this principle that user variables cannot be used to provide identifiers, is when you are
constructing a string for use as a prepared statement to execute later. In this case, user variables can be
used to provide any part of the statement. The following example illustrates how this can be done:

mysql> SET @c = "c1";
Query OK, 0 rows affected (0.00 sec)

mysql> SET @s = CONCAT("SELECT ", @c, " FROM t");
Query OK, 0 rows affected (0.00 sec)

mysql> PREPARE stmt FROM @s;
Query OK, 0 rows affected (0.04 sec)
Statement prepared

mysql> EXECUTE stmt;
+----+
| c1 |
+----+
|  0 |
+----+
|  1 |
+----+
2 rows in set (0.00 sec)

mysql> DEALLOCATE PREPARE stmt;
Query OK, 0 rows affected (0.00 sec)

See Section 13.5, “Prepared Statements”, for more information.

A similar technique can be used in application programs to construct SQL statements using program
variables, as shown here using PHP 5:

<?php
  $mysqli = new mysqli("localhost", "user", "pass", "test");

  if( mysqli_connect_errno() )
    die("Connection failed: %s\n", mysqli_connect_error());

  $col = "c1";

  $query = "SELECT $col FROM t";

1700

Expressions

  $result = $mysqli->query($query);

  while($row = $result->fetch_assoc())
  {
    echo "<p>" . $row["$col"] . "</p>\n";
  }

  $result->close();

  $mysqli->close();
?>

Assembling an SQL statement in this fashion is sometimes known as “Dynamic SQL”.

9.5 Expressions

This section lists the grammar rules that expressions must follow in MySQL and provides additional
information about the types of terms that may appear in expressions.

• Expression Syntax

• Expression Term Notes

• Temporal Intervals

Expression Syntax

The following grammar rules define expression syntax in MySQL. The grammar shown here is based on
that given in the sql/sql_yacc.yy file of MySQL source distributions. For additional information about
some of the expression terms, see Expression Term Notes.

expr:
    expr OR expr
  | expr || expr
  | expr XOR expr
  | expr AND expr
  | expr && expr
  | NOT expr
  | ! expr
  | boolean_primary IS [NOT] {TRUE | FALSE | UNKNOWN}
  | boolean_primary

boolean_primary:
    boolean_primary IS [NOT] NULL
  | boolean_primary <=> predicate
  | boolean_primary comparison_operator predicate
  | boolean_primary comparison_operator {ALL | ANY} (subquery)
  | predicate

comparison_operator: = | >= | > | <= | < | <> | !=

predicate:
    bit_expr [NOT] IN (subquery)
  | bit_expr [NOT] IN (expr [, expr] ...)
  | bit_expr [NOT] BETWEEN bit_expr AND predicate
  | bit_expr SOUNDS LIKE bit_expr
  | bit_expr [NOT] LIKE simple_expr [ESCAPE simple_expr]
  | bit_expr [NOT] REGEXP bit_expr
  | bit_expr

bit_expr:
    bit_expr | bit_expr
  | bit_expr & bit_expr

1701

Expression Term Notes

  | bit_expr << bit_expr
  | bit_expr >> bit_expr
  | bit_expr + bit_expr
  | bit_expr - bit_expr
  | bit_expr * bit_expr
  | bit_expr / bit_expr
  | bit_expr DIV bit_expr
  | bit_expr MOD bit_expr
  | bit_expr % bit_expr
  | bit_expr ^ bit_expr
  | bit_expr + interval_expr
  | bit_expr - interval_expr
  | simple_expr

simple_expr:
    literal
  | identifier
  | function_call
  | simple_expr COLLATE collation_name
  | param_marker
  | variable
  | simple_expr || simple_expr
  | + simple_expr
  | - simple_expr
  | ~ simple_expr
  | ! simple_expr
  | BINARY simple_expr
  | (expr [, expr] ...)
  | ROW (expr, expr [, expr] ...)
  | (subquery)
  | EXISTS (subquery)
  | {identifier expr}
  | match_expr
  | case_expr
  | interval_expr

For operator precedence, see Section 12.4.1, “Operator Precedence”. The precedence and meaning of
some operators depends on the SQL mode:

• By default, || is a logical OR operator. With PIPES_AS_CONCAT enabled, || is string concatenation,

with a precedence between ^ and the unary operators.

• By default, ! has a higher precedence than NOT. With HIGH_NOT_PRECEDENCE enabled, ! and NOT

have the same precedence.

See Section 5.1.10, “Server SQL Modes”.

Expression Term Notes

For literal value syntax, see Section 9.1, “Literal Values”.

For identifier syntax, see Section 9.2, “Schema Object Names”.

Variables can be user variables, system variables, or stored program local variables or parameters:

• User variables: Section 9.4, “User-Defined Variables”

• System variables: Section 5.1.8, “Using System Variables”

• Stored program local variables: Section 13.6.4.1, “Local Variable DECLARE Statement”

• Stored program parameters: Section 13.1.16, “CREATE PROCEDURE and CREATE FUNCTION

Statements”

1702

Temporal Intervals

param_marker is ? as used in prepared statements for placeholders. See Section 13.5.1, “PREPARE
Statement”.

(subquery) indicates a subquery that returns a single value; that is, a scalar subquery. See
Section 13.2.10.1, “The Subquery as Scalar Operand”.

{identifier expr} is ODBC escape syntax and is accepted for ODBC compatibility. The value is
expr. The { and } curly braces in the syntax should be written literally; they are not metasyntax as used
elsewhere in syntax descriptions.

match_expr indicates a MATCH expression. See Section 12.9, “Full-Text Search Functions”.

case_expr indicates a CASE expression. See Section 12.5, “Flow Control Functions”.

interval_expr represents a temporal interval. See Temporal Intervals.

Temporal Intervals

interval_expr in expressions represents a temporal interval. Intervals have this syntax:

INTERVAL expr unit

expr represents a quantity. unit represents the unit for interpreting the quantity; it is a specifier such as
HOUR, DAY, or WEEK. The INTERVAL keyword and the unit specifier are not case-sensitive.

The following table shows the expected form of the expr argument for each unit value.

Table 9.2 Temporal Interval Expression and Unit Arguments

unit Value

MICROSECOND

SECOND

MINUTE

HOUR

DAY

WEEK

MONTH

QUARTER

YEAR

SECOND_MICROSECOND

MINUTE_MICROSECOND

MINUTE_SECOND

HOUR_MICROSECOND

HOUR_SECOND

HOUR_MINUTE

DAY_MICROSECOND

DAY_SECOND

DAY_MINUTE

Expected expr Format

MICROSECONDS

SECONDS

MINUTES

HOURS

DAYS

WEEKS

MONTHS

QUARTERS

YEARS

'SECONDS.MICROSECONDS'

'MINUTES:SECONDS.MICROSECONDS'

'MINUTES:SECONDS'

'HOURS:MINUTES:SECONDS.MICROSECONDS'

'HOURS:MINUTES:SECONDS'

'HOURS:MINUTES'

'DAYS
HOURS:MINUTES:SECONDS.MICROSECONDS'

'DAYS HOURS:MINUTES:SECONDS'

'DAYS HOURS:MINUTES'

1703

Temporal Intervals

unit Value

DAY_HOUR

YEAR_MONTH

Expected expr Format

'DAYS HOURS'

'YEARS-MONTHS'

MySQL permits any punctuation delimiter in the expr format. Those shown in the table are the suggested
delimiters.

Temporal intervals are used for certain functions, such as DATE_ADD() and DATE_SUB():

mysql> SELECT DATE_ADD('2018-05-01',INTERVAL 1 DAY);
        -> '2018-05-02'
mysql> SELECT DATE_SUB('2018-05-01',INTERVAL 1 YEAR);
        -> '2017-05-01'
mysql> SELECT DATE_ADD('2020-12-31 23:59:59',
    ->                 INTERVAL 1 SECOND);
        -> '2021-01-01 00:00:00'
mysql> SELECT DATE_ADD('2018-12-31 23:59:59',
    ->                 INTERVAL 1 DAY);
        -> '2019-01-01 23:59:59'
mysql> SELECT DATE_ADD('2100-12-31 23:59:59',
    ->                 INTERVAL '1:1' MINUTE_SECOND);
        -> '2101-01-01 00:01:00'
mysql> SELECT DATE_SUB('2025-01-01 00:00:00',
    ->                 INTERVAL '1 1:1:1' DAY_SECOND);
        -> '2024-12-30 22:58:59'
mysql> SELECT DATE_ADD('1900-01-01 00:00:00',
    ->                 INTERVAL '-1 10' DAY_HOUR);
        -> '1899-12-30 14:00:00'
mysql> SELECT DATE_SUB('1998-01-02', INTERVAL 31 DAY);
        -> '1997-12-02'
mysql> SELECT DATE_ADD('1992-12-31 23:59:59.000002',
    ->            INTERVAL '1.999999' SECOND_MICROSECOND);
        -> '1993-01-01 00:00:01.000001'

Temporal arithmetic also can be performed in expressions using INTERVAL together with the + or -
operator:

date + INTERVAL expr unit
date - INTERVAL expr unit

INTERVAL expr unit is permitted on either side of the + operator if the expression on the other side is
a date or datetime value. For the - operator, INTERVAL expr unit is permitted only on the right side,
because it makes no sense to subtract a date or datetime value from an interval.

mysql> SELECT '2018-12-31 23:59:59' + INTERVAL 1 SECOND;
        -> '2019-01-01 00:00:00'
mysql> SELECT INTERVAL 1 DAY + '2018-12-31';
        -> '2019-01-01'
mysql> SELECT '2025-01-01' - INTERVAL 1 SECOND;
        -> '2024-12-31 23:59:59'

The EXTRACT() function uses the same kinds of unit specifiers as DATE_ADD() or DATE_SUB(), but
extracts parts from the date rather than performing date arithmetic:

mysql> SELECT EXTRACT(YEAR FROM '2019-07-02');
        -> 2019
mysql> SELECT EXTRACT(YEAR_MONTH FROM '2019-07-02 01:02:03');
        -> 201907

Temporal intervals can be used in CREATE EVENT statements:

CREATE EVENT myevent

1704

Comments

    ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 1 HOUR
    DO
      UPDATE myschema.mytable SET mycol = mycol + 1;

If you specify an interval value that is too short (does not include all the interval parts that would be
expected from the unit keyword), MySQL assumes that you have left out the leftmost parts of the interval
value. For example, if you specify a unit of DAY_SECOND, the value of expr is expected to have days,
hours, minutes, and seconds parts. If you specify a value like '1:10', MySQL assumes that the days
and hours parts are missing and the value represents minutes and seconds. In other words, '1:10'
DAY_SECOND is interpreted in such a way that it is equivalent to '1:10' MINUTE_SECOND. This is
analogous to the way that MySQL interprets TIME values as representing elapsed time rather than as a
time of day.

expr is treated as a string, so be careful if you specify a nonstring value with INTERVAL. For example,
with an interval specifier of HOUR_MINUTE, '6/4' is treated as 6 hours, four minutes, whereas 6/4 evaluates
to 1.5000 and is treated as 1 hour, 5000 minutes:

mysql> SELECT '6/4', 6/4;
        -> 1.5000
mysql> SELECT DATE_ADD('2019-01-01', INTERVAL '6/4' HOUR_MINUTE);
        -> '2019-01-01 06:04:00'
mysql> SELECT DATE_ADD('2019-01-01', INTERVAL 6/4 HOUR_MINUTE);
        -> '2019-01-04 12:20:00'

To ensure interpretation of the interval value as you expect, a CAST() operation may be used. To treat
6/4 as 1 hour, 5 minutes, cast it to a DECIMAL value with a single fractional digit:

mysql> SELECT CAST(6/4 AS DECIMAL(3,1));
        -> 1.5
mysql> SELECT DATE_ADD('1970-01-01 12:00:00',
    ->                 INTERVAL CAST(6/4 AS DECIMAL(3,1)) HOUR_MINUTE);
        -> '1970-01-01 13:05:00'

If you add to or subtract from a date value something that contains a time part, the result is automatically
converted to a datetime value:

mysql> SELECT DATE_ADD('2023-01-01', INTERVAL 1 DAY);
        -> '2023-01-02'
mysql> SELECT DATE_ADD('2023-01-01', INTERVAL 1 HOUR);
        -> '2023-01-01 01:00:00'

If you add MONTH, YEAR_MONTH, or YEAR and the resulting date has a day that is larger than the maximum
day for the new month, the day is adjusted to the maximum days in the new month:

mysql> SELECT DATE_ADD('2019-01-30', INTERVAL 1 MONTH);
        -> '2019-02-28'

Date arithmetic operations require complete dates and do not work with incomplete dates such as
'2016-07-00' or badly malformed dates:

mysql> SELECT DATE_ADD('2016-07-00', INTERVAL 1 DAY);
        -> NULL
mysql> SELECT '2005-03-32' + INTERVAL 1 MONTH;
        -> NULL

9.6 Comments

MySQL Server supports three comment styles:

• From a # character to the end of the line.

1705

Comments

• From a --  sequence to the end of the line. In MySQL, the --  (double-dash) comment style requires
the second dash to be followed by at least one whitespace or control character, such as a space or tab.
This syntax differs slightly from standard SQL comment syntax, as discussed in Section 1.6.2.4, “'--' as
the Start of a Comment”.

• From a /* sequence to the following */ sequence, as in the C programming language. This syntax

enables a comment to extend over multiple lines because the beginning and closing sequences need not
be on the same line.

The following example demonstrates all three comment styles:

mysql> SELECT 1+1;     # This comment continues to the end of line
mysql> SELECT 1+1;     -- This comment continues to the end of line
mysql> SELECT 1 /* this is an in-line comment */ + 1;
mysql> SELECT 1+
/*
this is a
multiple-line comment
*/
1;

Nested comments are not supported. (Under some conditions, nested comments might be permitted, but
usually are not, and users should avoid them.)

MySQL Server supports certain variants of C-style comments. These enable you to write code that
includes MySQL extensions, but is still portable, by using comments of the following form:

/*! MySQL-specific code */

In this case, MySQL Server parses and executes the code within the comment as it would any other SQL
statement, but other SQL servers ignore the extensions. For example, MySQL Server recognizes the
STRAIGHT_JOIN keyword in the following statement, but other servers do not:

SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...

If you add a version number after the ! character, the syntax within the comment is executed only if the
MySQL version is greater than or equal to the specified version number. The KEY_BLOCK_SIZE keyword
in the following comment is executed only by servers from MySQL 5.1.10 or higher:

CREATE TABLE t1(a INT, KEY (a)) /*!50110 KEY_BLOCK_SIZE=1024 */;

The version number uses the format Mmmrr, where M is a major version, mm is a two-digit minor version,
and rr is a two-digit release number. For example: In a statement to be run only by a MySQL server
version 5.7.31 or later, use 50731 in the comment.

The comment syntax just described applies to how the mysqld server parses SQL statements. The mysql
client program also performs some parsing of statements before sending them to the server. (It does this to
determine statement boundaries within a multiple-statement input line.) For information about differences
between the server and mysql client parsers, see Section 4.5.1.6, “mysql Client Tips”.

Comments in /*!12345 ... */ format are not stored on the server. If this format is used to comment
stored programs, the comments are not retained in the program body.

Another variant of C-style comment syntax is used to specify optimizer hints. Hint comments include a +
character following the /* comment opening sequence. Example:

SELECT /*+ BKA(t1) */ FROM ... ;

For more information, see Section 8.9.3, “Optimizer Hints”.

1706

Comments

The use of short-form mysql commands such as \C within multiple-line /* ... */ comments is not
supported. Short-form commands do work within single-line /*! ... */ version comments, as do /
*+ ... */ optimizer-hint comments, which are stored in object definitions. If there is a concern that
optimizer-hint comments may be stored in object definitions so that dump files when reloaded with mysql
would result in execution of such commands, either invoke mysql with the --binary-mode option or use
a reload client other than mysql.

1707

1708

