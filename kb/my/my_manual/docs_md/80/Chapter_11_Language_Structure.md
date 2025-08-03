Numeric Literals

can use the QUOTE() function. The Perl DBI interface provides a quote method to convert special
characters to the proper escape sequences. See Section 31.9, “MySQL Perl API”. Other language
interfaces may provide a similar capability.

• As an alternative to explicitly escaping special characters, many MySQL APIs provide a placeholder

capability that enables you to insert special markers into a statement string, and then bind data
values to them when you issue the statement. In this case, the API takes care of escaping special
characters in the values for you.

11.1.2 Numeric Literals

Number literals include exact-value (integer and DECIMAL) literals and approximate-value (floating-
point) literals.

Integers are represented as a sequence of digits. Numbers may include . as a decimal separator.
Numbers may be preceded by - or + to indicate a negative or positive value, respectively. Numbers
represented in scientific notation with a mantissa and exponent are approximate-value numbers.

Exact-value numeric literals have an integer part or fractional part, or both. They may be signed.
Examples: 1, .2, 3.4, -5, -6.78, +9.10.

Approximate-value numeric literals are represented in scientific notation with a mantissa and exponent.
Either or both parts may be signed. Examples: 1.2E3, 1.2E-3, -1.2E3, -1.2E-3.

Two numbers that look similar may be treated differently. For example, 2.34 is an exact-value (fixed-
point) number, whereas 2.34E0 is an approximate-value (floating-point) number.

The DECIMAL data type is a fixed-point type and calculations are exact. In MySQL, the DECIMAL type
has several synonyms: NUMERIC, DEC, FIXED. The integer types also are exact-value types. For more
information about exact-value calculations, see Section 14.24, “Precision Math”.

The FLOAT and DOUBLE data types are floating-point types and calculations are approximate. In
MySQL, types that are synonymous with FLOAT or DOUBLE are DOUBLE PRECISION and REAL.

An integer may be used in floating-point context; it is interpreted as the equivalent floating-point
number.

11.1.3 Date and Time Literals

• Standard SQL and ODBC Date and Time Literals

• String and Numeric Literals in Date and Time Context

Date and time values can be represented in several formats, such as quoted strings or as numbers,
depending on the exact type of the value and other factors. For example, in contexts where MySQL
expects a date, it interprets any of '2015-07-21', '20150721', and 20150721 as a date.

This section describes the acceptable formats for date and time literals. For more information about the
temporal data types, such as the range of permitted values, see Section 13.2, “Date and Time Data
Types”.

Standard SQL and ODBC Date and Time Literals

Standard SQL requires temporal literals to be specified using a type keyword and a string. The space
between the keyword and string is optional.

DATE 'str'
TIME 'str'
TIMESTAMP 'str'

MySQL recognizes but, unlike standard SQL, does not require the type keyword. Applications that are
to be standard-compliant should include the type keyword for temporal literals.

2052

Date and Time Literals

   Code: 4095
Message: Delimiter '^' in position 4 in datetime value '2012^12^31 11*30*45' at
row 1 is deprecated. Prefer the standard '-'.
1 row in set (0.00 sec)

The only delimiter recognized between a date and time part and a fractional seconds part is the
decimal point.

The date and time parts can be separated by T rather than a space. For example, '2012-12-31
11:30:45' '2012-12-31T11:30:45' are equivalent.

Previously, MySQL supported arbitrary numbers of leading and trailing whitespace characters in date
and time values, as well as between the date and time parts of DATETIME and TIMESTAMP values.
In MySQL 8.0.29 and later, this behavior is deprecated, and the presence of excess whitespace
characters triggers a warning, as shown here:

mysql> SELECT TIMESTAMP'2012-12-31   11-30-45';
+----------------------------------+
| TIMESTAMP'2012-12-31   11-30-45' |
+----------------------------------+
| 2012-12-31 11:30:45              |
+----------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
  Level: Warning
   Code: 4096
Message: Delimiter ' ' in position 11 in datetime value '2012-12-31   11-30-45'
at row 1 is superfluous and is deprecated. Please remove.
1 row in set (0.00 sec)

Also beginning with MySQL 8.0.29, a warning is raised when whitespace characters other than the
space character is used, like this:

mysql> SELECT TIMESTAMP'2021-06-06
    '> 11:15:25';
+--------------------------------+
| TIMESTAMP'2021-06-06
 11:15:25'                       |
+--------------------------------+
| 2021-06-06 11:15:25            |
+--------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
  Level: Warning
   Code: 4095
Message: Delimiter '\n' in position 10 in datetime value '2021-06-06
11:15:25' at row 1 is deprecated. Prefer the standard ' '.
1 row in set (0.00 sec)

Only one such warning is raised per temporal value, even though multiple issues may exist with
delimiters, whitespace, or both, as shown in the following series of statements:

mysql> SELECT TIMESTAMP'2012!-12-31  11:30:45';
+----------------------------------+
| TIMESTAMP'2012!-12-31  11:30:45' |
+----------------------------------+
| 2012-12-31 11:30:45              |
+----------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
  Level: Warning
   Code: 4095
Message: Delimiter '!' in position 4 in datetime value '2012!-12-31  11:30:45'

2054

Date and Time Literals

month, day, hour, minute, and second values, for as many parts as are present in the string. This
means you should not use strings that have fewer than 6 characters. For example, if you specify
'9903', thinking that represents March, 1999, MySQL converts it to the “zero” date value. This occurs
because the year and month values are 99 and 03, but the day part is completely missing. However,
you can explicitly specify a value of zero to represent missing month or day parts. For example, to
insert the value '1999-03-00', use '990300'.

MySQL recognizes TIME values in these formats:

• As a string in 'D hh:mm:ss' format. You can also use one of the following “relaxed” syntaxes:

'hh:mm:ss', 'hh:mm', 'D hh:mm', 'D hh', or 'ss'. Here D represents days and can have a
value from 0 to 34.

• As a string with no delimiters in 'hhmmss' format, provided that it makes sense as a time. For

example, '101112' is understood as '10:11:12', but '109712' is illegal (it has a nonsensical
minute part) and becomes '00:00:00'.

• As a number in hhmmss format, provided that it makes sense as a time. For example, 101112 is
understood as '10:11:12'. The following alternative formats are also understood: ss, mmss, or
hhmmss.

A trailing fractional seconds part is recognized in the 'D hh:mm:ss.fraction',
'hh:mm:ss.fraction', 'hhmmss.fraction', and hhmmss.fraction time formats, where
fraction is the fractional part in up to microseconds (6 digits) precision. The fractional part should
always be separated from the rest of the time by a decimal point; no other fractional seconds delimiter
is recognized. For information about fractional seconds support in MySQL, see Section 13.2.6,
“Fractional Seconds in Time Values”.

For TIME values specified as strings that include a time part delimiter, it is unnecessary to specify
two digits for hours, minutes, or seconds values that are less than 10. '8:3:2' is the same as
'08:03:02'.

Beginning with MySQL 8.0.19, you can specify a time zone offset when inserting TIMESTAMP and
DATETIME values into a table. The offset is appended to the time part of a datetime literal, with no
intravening spaces, and uses the same format used for setting the time_zone system variable, with
the following exceptions:

• For hour values less than 10, a leading zero is required.

• The value '-00:00' is rejected.

• Time zone names such as 'EET' and 'Asia/Shanghai' cannot be used; 'SYSTEM' also cannot

be used in this context.

The value inserted must not have a zero for the month part, the day part, or both parts. This is enforced
beginning with MySQL 8.0.22, regardless of the server SQL mode setting.

This example illustrates inserting datetime values with time zone offsets into TIMESTAMP and
DATETIME columns using different time_zone settings, and then retrieving them:

mysql> CREATE TABLE ts (
    ->     id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ->     col TIMESTAMP NOT NULL
    -> ) AUTO_INCREMENT = 1;

mysql> CREATE TABLE dt (
    ->     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ->     col DATETIME NOT NULL
    -> ) AUTO_INCREMENT = 1;

mysql> SET @@time_zone = 'SYSTEM';

mysql> INSERT INTO ts (col) VALUES ('2020-01-01 10:10:10'),

2056

Hexadecimal Literals

    ->     ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');

mysql> SET @@time_zone = '+00:00';

mysql> INSERT INTO ts (col) VALUES ('2020-01-01 10:10:10'),
    ->     ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');

mysql> SET @@time_zone = 'SYSTEM';

mysql> INSERT INTO dt (col) VALUES ('2020-01-01 10:10:10'),
    ->     ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');

mysql> SET @@time_zone = '+00:00';

mysql> INSERT INTO dt (col) VALUES ('2020-01-01 10:10:10'),
    ->     ('2020-01-01 10:10:10+05:30'), ('2020-01-01 10:10:10-08:00');

mysql> SET @@time_zone = 'SYSTEM';

mysql> SELECT @@system_time_zone;
+--------------------+
| @@system_time_zone |
+--------------------+
| EST                |
+--------------------+

mysql> SELECT col, UNIX_TIMESTAMP(col) FROM dt ORDER BY id;
+---------------------+---------------------+
| col                 | UNIX_TIMESTAMP(col) |
+---------------------+---------------------+
| 2020-01-01 10:10:10 |          1577891410 |
| 2019-12-31 23:40:10 |          1577853610 |
| 2020-01-01 13:10:10 |          1577902210 |
| 2020-01-01 10:10:10 |          1577891410 |
| 2020-01-01 04:40:10 |          1577871610 |
| 2020-01-01 18:10:10 |          1577920210 |
+---------------------+---------------------+

mysql> SELECT col, UNIX_TIMESTAMP(col) FROM ts ORDER BY id;
+---------------------+---------------------+
| col                 | UNIX_TIMESTAMP(col) |
+---------------------+---------------------+
| 2020-01-01 10:10:10 |          1577891410 |
| 2019-12-31 23:40:10 |          1577853610 |
| 2020-01-01 13:10:10 |          1577902210 |
| 2020-01-01 05:10:10 |          1577873410 |
| 2019-12-31 23:40:10 |          1577853610 |
| 2020-01-01 13:10:10 |          1577902210 |
+---------------------+---------------------+

The offset is not displayed when selecting a datetime value, even if one was used when inserting it.

The range of supported offset values is -13:59 to +14:00, inclusive.

Datetime literals that include time zone offsets are accepted as parameter values by prepared
statements.

11.1.4 Hexadecimal Literals

Hexadecimal literal values are written using X'val' or 0xval notation, where val contains
hexadecimal digits (0..9, A..F). Lettercase of the digits and of any leading X does not matter. A
leading 0x is case-sensitive and cannot be written as 0X.

Legal hexadecimal literals:

X'01AF'
X'01af'
x'01AF'
x'01af'
0x01AF

2057

Bit-Value Literals

mysql> SELECT CHARSET(X''), LENGTH(X'');
+--------------+-------------+
| CHARSET(X'') | LENGTH(X'') |
+--------------+-------------+
| binary       |           0 |
+--------------+-------------+
mysql> SELECT X''+0;
+-------+
| X''+0 |
+-------+
|     0 |
+-------+

The X'val' notation is based on standard SQL. The 0x notation is based on ODBC, for which
hexadecimal strings are often used to supply values for BLOB columns.

To convert a string or a number to a string in hexadecimal format, use the HEX() function:

mysql> SELECT HEX('cat');
+------------+
| HEX('cat') |
+------------+
| 636174     |
+------------+
mysql> SELECT X'636174';
+-----------+
| X'636174' |
+-----------+
| cat       |
+-----------+

For hexadecimal literals, bit operations are considered numeric context, but bit operations permit
numeric or binary string arguments in MySQL 8.0 and higher. To explicitly specify binary string context
for hexadecimal literals, use a _binary introducer for at least one of the arguments:

mysql> SET @v1 = X'000D' | X'0BC0';
mysql> SET @v2 = _binary X'000D' | X'0BC0';
mysql> SELECT HEX(@v1), HEX(@v2);
+----------+----------+
| HEX(@v1) | HEX(@v2) |
+----------+----------+
| BCD      | 0BCD     |
+----------+----------+

The displayed result appears similar for both bit operations, but the result without _binary is a
BIGINT value, whereas the result with _binary is a binary string. Due to the difference in result types,
the displayed values differ: High-order 0 digits are not displayed for the numeric result.

11.1.5 Bit-Value Literals

Bit-value literals are written using b'val' or 0bval notation. val is a binary value written using zeros
and ones. Lettercase of any leading b does not matter. A leading 0b is case-sensitive and cannot be
written as 0B.

Legal bit-value literals:

b'01'
B'01'
0b01

Illegal bit-value literals:

b'2'    (2 is not a binary digit)
0B01    (0B must be written as 0b)

By default, a bit-value literal is a binary string:

2059

Bit-Value Literals

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

A bit-value literal may have an optional character set introducer and COLLATE clause, to designate it as
a string that uses a particular character set and collation:

[_charset_name] b'val' [COLLATE collation_name]

Examples:

SELECT _latin1 b'1000001';
SELECT _utf8mb4 0b1000001 COLLATE utf8mb4_danish_ci;

The examples use b'val' notation, but 0bval notation permits introducers as well. For information
about introducers, see Section 12.3.8, “Character Set Introducers”.

In numeric contexts, MySQL treats a bit literal like an integer. To ensure numeric treatment of a bit
literal, use it in numeric context. Ways to do this include adding 0 or using CAST(... AS UNSIGNED).
For example, a bit literal assigned to a user-defined variable is a binary string by default. To assign the
value as a number, use it in numeric context:

mysql> SET @v1 = b'1100001';
mysql> SET @v2 = b'1100001'+0;
mysql> SET @v3 = CAST(b'1100001' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| a    |   97 |   97 |
+------+------+------+

An empty bit value (b'') evaluates to a zero-length binary string. Converted to a number, it produces
0:

mysql> SELECT CHARSET(b''), LENGTH(b'');
+--------------+-------------+
| CHARSET(b'') | LENGTH(b'') |
+--------------+-------------+
| binary       |           0 |
+--------------+-------------+
mysql> SELECT b''+0;
+-------+
| b''+0 |
+-------+
|     0 |
+-------+

Bit-value notation is convenient for specifying values to be assigned to BIT columns:

mysql> CREATE TABLE t (b BIT(8));
mysql> INSERT INTO t SET b = b'11111111';
mysql> INSERT INTO t SET b = b'1010';
mysql> INSERT INTO t SET b = b'0101';

Bit values in result sets are returned as binary values, which may not display well. To convert a bit
value to printable form, use it in numeric context or use a conversion function such as BIN() or
HEX(). High-order 0 digits are not displayed in the converted value.

2060

Schema Object Names

• Permitted characters in unquoted identifiers:

• ASCII: [0-9,a-z,A-Z$_] (basic Latin letters, digits 0-9, dollar, underscore)

• Extended: U+0080 .. U+FFFF

• Permitted characters in quoted identifiers include the full Unicode Basic Multilingual Plane (BMP),

except U+0000:

• ASCII: U+0001 .. U+007F

• Extended: U+0080 .. U+FFFF

• ASCII NUL (U+0000) and supplementary characters (U+10000 and higher) are not permitted in

quoted or unquoted identifiers.

• Identifiers may begin with a digit but unless quoted may not consist solely of digits.

• Database, table, and column names cannot end with space characters.

• Beginning with MySQL 8.0.32, use of the dollar sign as the first character in the unquoted name of a
database, table, view, column, stored program, or alias is deprecated and produces a warning. This
includes such names used with qualifiers (see Section 11.2.2, “Identifier Qualifiers”). The dollar sign
can still be used as the leading character of such an identifier when it is quoted according to the rules
given later in this section.

The identifier quote character is the backtick (`):

mysql> SELECT * FROM `select` WHERE `select`.id > 100;

If the ANSI_QUOTES SQL mode is enabled, it is also permissible to quote identifiers within double
quotation marks:

mysql> CREATE TABLE "test" (col INT);
ERROR 1064: You have an error in your SQL syntax...
mysql> SET sql_mode='ANSI_QUOTES';
mysql> CREATE TABLE "test" (col INT);
Query OK, 0 rows affected (0.00 sec)

The ANSI_QUOTES mode causes the server to interpret double-quoted strings as identifiers.
Consequently, when this mode is enabled, string literals must be enclosed within single quotation
marks. They cannot be enclosed within double quotation marks. The server SQL mode is controlled as
described in Section 7.1.11, “Server SQL Modes”.

Identifier quote characters can be included within an identifier if you quote the identifier. If the character
to be included within the identifier is the same as that used to quote the identifier itself, then you need
to double the character. The following statement creates a table named a`b that contains a column
named c"d:

mysql> CREATE TABLE `a``b` (`c"d` INT);

In the select list of a query, a quoted column alias can be specified using identifier or string quoting
characters:

mysql> SELECT 1 AS `one`, 2 AS 'two';
+-----+-----+
| one | two |
+-----+-----+
|   1 |   2 |
+-----+-----+

Elsewhere in the statement, quoted references to the alias must use identifier quoting or the reference
is treated as a string literal.

2062

Identifier Qualifiers

Values such as user name and host names in MySQL account names are strings rather than
identifiers. For information about the maximum length of such values as stored in grant tables, see
Grant Table Scope Column Properties.

11.2.2 Identifier Qualifiers

Object names may be unqualified or qualified. An unqualified name is permitted in contexts where
interpretation of the name is unambiguous. A qualified name includes at least one qualifier to clarify the
interpretive context by overriding a default context or providing missing context.

For example, this statement creates a table using the unqualified name t1:

CREATE TABLE t1 (i INT);

Because t1 includes no qualifier to specify a database, the statement creates the table in the default
database. If there is no default database, an error occurs.

This statement creates a table using the qualified name db1.t1:

CREATE TABLE db1.t1 (i INT);

Because db1.t1 includes a database qualifier db1, the statement creates t1 in the database named
db1, regardless of the default database. The qualifier must be specified if there is no default database.
The qualifier may be specified if there is a default database, to specify a database different from the
default, or to make the database explicit if the default is the same as the one specified.

Qualifiers have these characteristics:

• An unqualified name consists of a single identifier. A qualified name consists of multiple identifiers.

• The components of a multiple-part name must be separated by period (.) characters. The initial

parts of a multiple-part name act as qualifiers that affect the context within which to interpret the final
identifier.

• The qualifier character is a separate token and need not be contiguous with the associated

identifiers. For example, tbl_name.col_name and tbl_name . col_name are equivalent.

• If any components of a multiple-part name require quoting, quote them individually rather than
quoting the name as a whole. For example, write `my-table`.`my-column`, not `my-
table.my-column`.

• A reserved word that follows a period in a qualified name must be an identifier, so in that context it

need not be quoted.

The permitted qualifiers for object names depend on the object type:

• A database name is fully qualified and takes no qualifier:

CREATE DATABASE db1;

• A table, view, or stored program name may be given a database-name qualifier. Examples of

unqualified and qualified names in CREATE statements:

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

2064

Identifier Case Sensitivity

system variable also affects how the server handles identifier case sensitivity, as described later in this
section.

Note

Although database, table, and trigger names are not case-sensitive on some
platforms, you should not refer to one of these using different cases within the
same statement. The following statement would not work because it refers to a
table both as my_table and as MY_TABLE:

mysql> SELECT * FROM my_table WHERE MY_TABLE.col=1;

Partition, subpartition, column, index, stored routine, event, and resource group names are not case-
sensitive on any platform, nor are column aliases.

However, names of logfile groups are case-sensitive. This differs from standard SQL.

By default, table aliases are case-sensitive on Unix, but not so on Windows or macOS. The following
statement would not work on Unix, because it refers to the alias both as a and as A:

mysql> SELECT col_name FROM tbl_name AS a
       WHERE a.col_name = 1 OR A.col_name = 2;

However, this same statement is permitted on Windows. To avoid problems caused by such
differences, it is best to adopt a consistent convention, such as always creating and referring to
databases and tables using lowercase names. This convention is recommended for maximum
portability and ease of use.

How table and database names are stored on disk and used in MySQL is affected by the
lower_case_table_names system variable. lower_case_table_names can take the values
shown in the following table. This variable does not affect case sensitivity of trigger identifiers. On Unix,
the default value of lower_case_table_names is 0. On Windows, the default value is 1. On macOS,
the default value is 2.

lower_case_table_names can only be configured when initializing the server. Changing the
lower_case_table_names setting after the server is initialized is prohibited.

Value

0

1

2

2066

Meaning

Table and database names are stored on disk
using the lettercase specified in the CREATE
TABLE or CREATE DATABASE statement. Name
comparisons are case-sensitive. You should not
set this variable to 0 if you are running MySQL
on a system that has case-insensitive file names
(such as Windows or macOS). If you force this
variable to 0 with --lower-case-table-
names=0 on a case-insensitive file system and
access MyISAM tablenames using different
lettercases, index corruption may result.

Table names are stored in lowercase on disk
and name comparisons are not case-sensitive.
MySQL converts all table names to lowercase on
storage and lookup. This behavior also applies to
database names and table aliases.

Table and database names are stored on disk
using the lettercase specified in the CREATE
TABLE or CREATE DATABASE statement, but
MySQL converts them to lowercase on lookup.
Name comparisons are not case-sensitive.
This works only on file systems that are not

Mapping of Identifiers to File Names

Value

Meaning
case-sensitive! InnoDB table names and
view names are stored in lowercase, as for
lower_case_table_names=1.

If you are using MySQL on only one platform, you do not normally have to use a
lower_case_table_names setting other than the default. However, you may encounter difficulties if
you want to transfer tables between platforms that differ in file system case sensitivity. For example, on
Unix, you can have two different tables named my_table and MY_TABLE, but on Windows these two
names are considered identical. To avoid data transfer problems arising from lettercase of database or
table names, you have two options:

• Use lower_case_table_names=1 on all systems. The main disadvantage with this is that when
you use SHOW TABLES or SHOW DATABASES, you do not see the names in their original lettercase.

• Use lower_case_table_names=0 on Unix and lower_case_table_names=2 on Windows.
This preserves the lettercase of database and table names. The disadvantage of this is that you
must ensure that your statements always refer to your database and table names with the correct
lettercase on Windows. If you transfer your statements to Unix, where lettercase is significant, they
do not work if the lettercase is incorrect.

Exception: If you are using InnoDB tables and you are trying to avoid these data transfer problems,
you should use lower_case_table_names=1 on all platforms to force names to be converted to
lowercase.

Object names may be considered duplicates if their uppercase forms are equal according to a binary
collation. That is true for names of cursors, conditions, procedures, functions, savepoints, stored
routine parameters, stored program local variables, and plugins. It is not true for names of columns,
constraints, databases, partitions, statements prepared with PREPARE, tables, triggers, users, and
user-defined variables.

File system case sensitivity can affect searches in string columns of INFORMATION_SCHEMA tables.
For more information, see Section 12.8.7, “Using Collation in INFORMATION_SCHEMA Searches”.

11.2.4 Mapping of Identifiers to File Names

There is a correspondence between database and table identifiers and names in the file system.
For the basic structure, MySQL represents each database as a directory in the data directory, and
depending upon the storage engine, each table may be represented by one or more files in the
appropriate database directory.

For the data and index files, the exact representation on disk is storage engine specific. These files
may be stored in the database directory, or the information may be stored in a separate file. InnoDB
data is stored in the InnoDB data files. If you are using tablespaces with InnoDB, then the specific
tablespace files you create are used instead.

Any character is legal in database or table identifiers except ASCII NUL (X'00'). MySQL encodes
any characters that are problematic in the corresponding file system objects when it creates database
directories or table files:

• Basic Latin letters (a..zA..Z), digits (0..9) and underscore (_) are encoded as is. Consequently,

their case sensitivity directly depends on file system features.

• All other national letters from alphabets that have uppercase/lowercase mapping are encoded as

shown in the following table. Values in the Code Range column are UCS-2 values.

Code Range

Pattern

Number

Used

Unused

Blocks

00C0..017F

[@][0..4][g..z]

5*20= 100

97

3

Latin-1
Supplement +

2067

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

137

0530..058F

[@][g..z][7..8]

20*2= 40

2160..217F

[@][g..z][9]

20*1= 20

0180..02AF

[@][g..z][a..k]

20*11=220

38

16

203

1E00..1EFF

[@][g..z][l..r]

20*7= 140

136

1F00..1FFF

[@][g..z][s..z]

20*8= 160

144

.... ....

[@][a..f][g..z]

6*20= 120

24B6..24E9

[@][@][a..z]

FF21..FF5A

[@][a..z][@]

26

26

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

Cyrillic
+ Cyrillic
Supplement

Armenian

Number Forms

Latin Extended-
B + IPA
Extensions

Latin Extended
Additional

Greek
Extended

RESERVED

Enclosed
Alphanumerics

Halfwidth and
Fullwidth forms

One of the bytes in the sequence encodes lettercase. For example: LATIN CAPITAL LETTER A
WITH GRAVE is encoded as @0G, whereas LATIN SMALL LETTER A WITH GRAVE is encoded as
@0g. Here the third byte (G or g) indicates lettercase. (On a case-insensitive file system, both letters
are treated as the same.)

For some blocks, such as Cyrillic, the second byte determines lettercase. For other blocks, such as
Latin1 Supplement, the third byte determines lettercase. If two bytes in the sequence are letters (as
in Greek Extended), the leftmost letter character stands for lettercase. All other letter bytes must be
in lowercase.

• All nonletter characters except underscore (_), as well as letters from alphabets that do not have
uppercase/lowercase mapping (such as Hebrew) are encoded using hexadecimal representation
using lowercase letters for hexadecimal digits a..f:

0x003F -> @003f
0xFFFF -> @ffff

The hexadecimal values correspond to character values in the ucs2 double-byte character set.

On Windows, some names such as nul, prn, and aux are encoded by appending @@@ to the name
when the server creates the corresponding file or directory. This occurs on all platforms for portability of
the corresponding database object between platforms.

The following names are reserved and appended with @@@ if used in schema or table names:

• CON

• PRN

• AUX

• NUL

• COM1 through COM9

2068

Function Name Parsing and Resolution

• LPT1 through LPT9

CLOCK$ is also a member of this group of reserved names, but is not appended with @@@, but @0024
instead. That is, if CLOCK$ is used as a schema or table name, it is written to the file system as
CLOCK@0024. The same is true for any use of $ (dollar sign) in a schema or table name; it is replaced
with @0024 on the filesystem.

Note

These names are also written to INNODB_TABLES in their appended forms, but
are written to TABLES in their unappended form, as entered by the user.

11.2.5 Function Name Parsing and Resolution

MySQL supports built-in (native) functions, loadable functions, and stored functions. This section
describes how the server recognizes whether the name of a built-in function is used as a function call
or as an identifier, and how the server determines which function to use in cases when functions of
different types exist with a given name.

• Built-In Function Name Parsing

• Function Name Resolution

Built-In Function Name Parsing

The parser uses default rules for parsing names of built-in functions. These rules can be changed by
enabling the IGNORE_SPACE SQL mode.

When the parser encounters a word that is the name of a built-in function, it must determine whether
the name signifies a function call or is instead a nonexpression reference to an identifier such as a
table or column name. For example, in the following statements, the first reference to count is a
function call, whereas the second reference is a table name:

SELECT COUNT(*) FROM mytable;
CREATE TABLE count (i INT);

The parser should recognize the name of a built-in function as indicating a function call only when
parsing what is expected to be an expression. That is, in nonexpression context, function names are
permitted as identifiers.

However, some built-in functions have special parsing or implementation considerations, so the parser
uses the following rules by default to distinguish whether their names are being used as function calls
or as identifiers in nonexpression context:

• To use the name as a function call in an expression, there must be no whitespace between the name

and the following ( parenthesis character.

• Conversely, to use the function name as an identifier, it must not be followed immediately by a

parenthesis.

The requirement that function calls be written with no whitespace between the name and the
parenthesis applies only to the built-in functions that have special considerations. COUNT is one such
name. The sql/lex.h source file lists the names of these special functions for which following
whitespace determines their interpretation: names defined by the SYM_FN() macro in the symbols[]
array.

The following list names the functions in MySQL 8.0 that are affected by the IGNORE_SPACE setting
and listed as special in the sql/lex.h source file. You may find it easiest to treat the no-whitespace
requirement as applying to all function calls.

• ADDDATE

2069

Function Name Parsing and Resolution

• BIT_AND

• BIT_OR

• BIT_XOR

• CAST

• COUNT

• CURDATE

• CURTIME

• DATE_ADD

• DATE_SUB

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
function calls only when used in expression context and may be used freely as identifiers otherwise.
ASCII is one such name. However, for these nonaffected function names, interpretation may vary in

2070

Function Name Parsing and Resolution

expression context: func_name () is interpreted as a built-in function if there is one with the given
name; if not, func_name () is interpreted as a loadable function or stored function if one exists with
that name.

The IGNORE_SPACE SQL mode can be used to modify how the parser treats function names that are
whitespace-sensitive:

• With IGNORE_SPACE disabled, the parser interprets the name as a function call when there is no
whitespace between the name and the following parenthesis. This occurs even when the function
name is used in nonexpression context:

mysql> CREATE TABLE count(i INT);
ERROR 1064 (42000): You have an error in your SQL syntax ...
near 'count(i INT)'

To eliminate the error and cause the name to be treated as an identifier, either use whitespace
following the name or write it as a quoted identifier (or both):

CREATE TABLE count (i INT);
CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);

• With IGNORE_SPACE enabled, the parser loosens the requirement that there be no whitespace

between the function name and the following parenthesis. This provides more flexibility in writing
function calls. For example, either of the following function calls are legal:

SELECT COUNT(*) FROM mytable;
SELECT COUNT (*) FROM mytable;

However, enabling IGNORE_SPACE also has the side effect that the parser treats the affected
function names as reserved words (see Section 11.3, “Keywords and Reserved Words”). This means
that a space following the name no longer signifies its use as an identifier. The name can be used
in function calls with or without following whitespace, but causes a syntax error in nonexpression
context unless it is quoted. For example, with IGNORE_SPACE enabled, both of the following
statements fail with a syntax error because the parser interprets count as a reserved word:

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

Check Section 7.1.11, “Server SQL Modes”, to see which composite modes enable IGNORE_SPACE.

To minimize the dependency of SQL code on the IGNORE_SPACE setting, use these guidelines:

• Avoid creating loadable functions or stored functions that have the same name as a built-in function.

• Avoid using function names in nonexpression context. For example, these statements use count

(one of the affected function names affected by IGNORE_SPACE), so they fail with or without
whitespace following the name if IGNORE_SPACE is enabled:

CREATE TABLE count(i INT);
CREATE TABLE count (i INT);

2071

Keywords and Reserved Words

If you must use a function name in nonexpression context, write it as a quoted identifier:

CREATE TABLE `count`(i INT);
CREATE TABLE `count` (i INT);

Function Name Resolution

The following rules describe how the server resolves references to function names for function creation
and invocation:

• Built-in functions and loadable functions

An error occurs if you try to create a loadable function with the same name as a built-in function.

IF NOT EXISTS (available beginning with MySQL 8.0.29) has no effect in such cases. See
Section 15.7.4.1, “CREATE FUNCTION Statement for Loadable Functions”, for more information.

• Built-in functions and stored functions

It is possible to create a stored function with the same name as a built-in function, but to invoke
the stored function it is necessary to qualify it with a schema name. For example, if you create a
stored function named PI in the test schema, invoke it as test.PI() because the server resolves
PI() without a qualifier as a reference to the built-in function. The server generates a warning if the
stored function name collides with a built-in function name. The warning can be displayed with SHOW
WARNINGS.

IF NOT EXISTS (MySQL 8.0.29 and later) has no effect in such cases; see Section 15.1.17,
“CREATE PROCEDURE and CREATE FUNCTION Statements”.

• Loadable functions and stored functions

It is possible to create a stored function with the same name as an existing loadable function, or the
other way around. The server generates a warning if a proposed stored function name collides with
an existing loadable function name, or if a proposed loadable function name would be the same as
that of an existing stored function. In either case, once both functions exist, it is necessary thereafter
to qualify the stored function with a schema name when invoking it; the server assumes in such
cases that the unqualified name refers to the loadable function.

Beginning with MySQL 8.0.29, IF NOT EXISTS is supported with CREATE FUNCTION statements,
but has no effect in such cases.

Prior to MySQL 8.0.28, it was possible to create a stored function with the same name as an existing
loadable function, but not the other way around (Bug #33301931 ).

The preceding function name resolution rules have implications for upgrading to versions of MySQL
that implement new built-in functions:

• If you have already created a loadable function with a given name and upgrade MySQL to a

version that implements a new built-in function with the same name, the loadable function becomes
inaccessible. To correct this, use DROP FUNCTION to drop the loadable function and CREATE
FUNCTION to re-create the loadable function with a different nonconflicting name. Then modify any
affected code to use the new name.

• If a new version of MySQL implements a built-in function or loadable function with the same

name as an existing stored function, you have two choices: Rename the stored function to use
a nonconflicting name, or change any calls to the function that do not do so already to use a
schema qualifier (schema_name.func_name() syntax). In either case, modify any affected code
accordingly.

11.3 Keywords and Reserved Words

2072

MySQL 8.0 Keywords and Reserved Words

• ACCESSIBLE (R)

• ACCOUNT

• ACTION

• ACTIVE; added in 8.0.14 (nonreserved)

• ADD (R)

• ADMIN; became nonreserved in 8.0.12

• AFTER

• AGAINST

• AGGREGATE

• ALGORITHM

• ALL (R)

• ALTER (R)

• ALWAYS

• ANALYSE; removed in 8.0.1

• ANALYZE (R)

• AND (R)

• ANY

• ARRAY; added in 8.0.17 (reserved); became nonreserved in 8.0.19

• AS (R)

• ASC (R)

• ASCII

• ASENSITIVE (R)

• AT

• ATTRIBUTE; added in 8.0.21 (nonreserved)

• AUTHENTICATION; added in 8.0.27 (nonreserved)

• AUTOEXTEND_SIZE

• AUTO_INCREMENT

• AVG

• AVG_ROW_LENGTH

B

• BACKUP

• BEFORE (R)

• BEGIN

2074

MySQL 8.0 Keywords and Reserved Words

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

• BUCKETS; added in 8.0.2 (nonreserved)

• BULK; added in 8.0.32 (nonreserved)

• BY (R)

• BYTE

C

• CACHE

• CALL (R)

• CASCADE (R)

• CASCADED

• CASE (R)

• CATALOG_NAME

• CHAIN

• CHALLENGE_RESPONSE; added in 8.0.27 (nonreserved)

• CHANGE (R)

• CHANGED

• CHANNEL

• CHAR (R)

• CHARACTER (R)

• CHARSET

• CHECK (R)

• CHECKSUM

• CIPHER

2075

MySQL 8.0 Keywords and Reserved Words

• CLASS_ORIGIN

• CLIENT

• CLONE; added in 8.0.3 (nonreserved)

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

• COMPONENT

• COMPRESSED

• COMPRESSION

• CONCURRENT

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

2076

MySQL 8.0 Keywords and Reserved Words

• CREATE (R)

• CROSS (R)

• CUBE (R); became reserved in 8.0.1

• CUME_DIST (R); added in 8.0.2 (reserved)

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

• DEFINITION; added in 8.0.4 (nonreserved)

• DELAYED (R)

• DELAY_KEY_WRITE

2077

MySQL 8.0 Keywords and Reserved Words

• DELETE (R)

• DENSE_RANK (R); added in 8.0.2 (reserved)

• DESC (R)

• DESCRIBE (R)

• DESCRIPTION; added in 8.0.4 (nonreserved)

• DES_KEY_FILE; removed in 8.0.3

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

• DUMPFILE

• DUPLICATE

• DYNAMIC

E

• EACH (R)

• ELSE (R)

• ELSEIF (R)

• EMPTY (R); added in 8.0.4 (reserved)

• ENABLE

• ENCLOSED (R)

• ENCRYPTION

• END

• ENDS

• ENFORCED; added in 8.0.16 (nonreserved)

2078

MySQL 8.0 Keywords and Reserved Words

• ENGINE

• ENGINES

• ENGINE_ATTRIBUTE; added in 8.0.21 (nonreserved)

• ENUM

• ERROR

• ERRORS

• ESCAPE

• ESCAPED (R)

• EVENT

• EVENTS

• EVERY

• EXCEPT (R)

• EXCHANGE

• EXCLUDE; added in 8.0.2 (nonreserved)

• EXECUTE

• EXISTS (R)

• EXIT (R)

• EXPANSION

• EXPIRE

• EXPLAIN (R)

• EXPORT

• EXTENDED

• EXTENT_SIZE

F

• FACTOR; added in 8.0.27 (nonreserved)

• FAILED_LOGIN_ATTEMPTS; added in 8.0.19 (nonreserved)

• FALSE (R)

• FAST

• FAULTS

• FETCH (R)

• FIELDS

• FILE

• FILE_BLOCK_SIZE

2079

MySQL 8.0 Keywords and Reserved Words

• FILTER

• FINISH; added in 8.0.27 (nonreserved)

• FIRST

• FIRST_VALUE (R); added in 8.0.2 (reserved)

• FIXED

• FLOAT (R)

• FLOAT4 (R)

• FLOAT8 (R)

• FLUSH

• FOLLOWING; added in 8.0.2 (nonreserved)

• FOLLOWS

• FOR (R)

• FORCE (R)

• FOREIGN (R)

• FORMAT

• FOUND

• FROM (R)

• FULL

• FULLTEXT (R)

• FUNCTION (R); became reserved in 8.0.1

G

• GENERAL

• GENERATE; added in 8.0.32 (nonreserved)

• GENERATED (R)

• GEOMCOLLECTION; added in 8.0.11 (nonreserved)

• GEOMETRY

• GEOMETRYCOLLECTION

• GET (R)

• GET_FORMAT

• GET_MASTER_PUBLIC_KEY; added in 8.0.4 (reserved); became nonreserved in 8.0.11

• GET_SOURCE_PUBLIC_KEY; added in 8.0.23 (nonreserved)

• GLOBAL

• GRANT (R)

2080

MySQL 8.0 Keywords and Reserved Words

• GRANTS

• GROUP (R)

• GROUPING (R); added in 8.0.1 (reserved)

• GROUPS (R); added in 8.0.2 (reserved)

• GROUP_REPLICATION

• GTID_ONLY; added in 8.0.27 (nonreserved)

H

• HANDLER

• HASH

• HAVING (R)

• HELP

• HIGH_PRIORITY (R)

• HISTOGRAM; added in 8.0.2 (nonreserved)

• HISTORY; added in 8.0.3 (nonreserved)

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

• INACTIVE; added in 8.0.14 (nonreserved)

• INDEX (R)

• INDEXES

• INFILE (R)

• INITIAL; added in 8.0.27 (nonreserved)

• INITIAL_SIZE

2081

MySQL 8.0 Keywords and Reserved Words

• INITIATE; added in 8.0.27 (nonreserved)

• INNER (R)

• INOUT (R)

• INSENSITIVE (R)

• INSERT (R)

• INSERT_METHOD

• INSTALL

• INSTANCE

• INT (R)

• INT1 (R)

• INT2 (R)

• INT3 (R)

• INT4 (R)

• INT8 (R)

• INTEGER (R)

• INTERSECT (R); added in 8.0.31 (reserved)

• INTERVAL (R)

• INTO (R)

• INVISIBLE

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

• JSON

• JSON_TABLE (R); added in 8.0.4 (reserved)

2082

MySQL 8.0 Keywords and Reserved Words

• JSON_VALUE; added in 8.0.21 (nonreserved)

K

• KEY (R)

• KEYRING; added in 8.0.24 (nonreserved)

• KEYS (R)

• KEY_BLOCK_SIZE

• KILL (R)

L

• LAG (R); added in 8.0.2 (reserved)

• LANGUAGE

• LAST

• LAST_VALUE (R); added in 8.0.2 (reserved)

• LATERAL (R); added in 8.0.14 (reserved)

• LEAD (R); added in 8.0.2 (reserved)

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

• LOCKED; added in 8.0.1 (nonreserved)

• LOCKS

2083

MySQL 8.0 Keywords and Reserved Words

• LOGFILE

• LOGS

• LONG (R)

• LONGBLOB (R)

• LONGTEXT (R)

• LOOP (R)

• LOW_PRIORITY (R)

M

• MASTER

• MASTER_AUTO_POSITION

• MASTER_BIND (R)

• MASTER_COMPRESSION_ALGORITHMS; added in 8.0.18 (nonreserved)

• MASTER_CONNECT_RETRY

• MASTER_DELAY

• MASTER_HEARTBEAT_PERIOD

• MASTER_HOST

• MASTER_LOG_FILE

• MASTER_LOG_POS

• MASTER_PASSWORD

• MASTER_PORT

• MASTER_PUBLIC_KEY_PATH; added in 8.0.4 (nonreserved)

• MASTER_RETRY_COUNT

• MASTER_SERVER_ID; removed in 8.0.23

• MASTER_SSL

• MASTER_SSL_CA

• MASTER_SSL_CAPATH

• MASTER_SSL_CERT

• MASTER_SSL_CIPHER

• MASTER_SSL_CRL

• MASTER_SSL_CRLPATH

• MASTER_SSL_KEY

• MASTER_SSL_VERIFY_SERVER_CERT (R)

• MASTER_TLS_CIPHERSUITES; added in 8.0.19 (nonreserved)

2084

MySQL 8.0 Keywords and Reserved Words

• MASTER_TLS_VERSION

• MASTER_USER

• MASTER_ZSTD_COMPRESSION_LEVEL; added in 8.0.18 (nonreserved)

• MATCH (R)

• MAXVALUE (R)

• MAX_CONNECTIONS_PER_HOUR

• MAX_QUERIES_PER_HOUR

• MAX_ROWS

• MAX_SIZE

• MAX_UPDATES_PER_HOUR

• MAX_USER_CONNECTIONS

• MEDIUM

• MEDIUMBLOB (R)

• MEDIUMINT (R)

• MEDIUMTEXT (R)

• MEMBER; added in 8.0.17 (reserved); became nonreserved in 8.0.19

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

2085

MySQL 8.0 Keywords and Reserved Words

• MULTIPOLYGON

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

• NESTED; added in 8.0.4 (nonreserved)

• NETWORK_NAMESPACE; added in 8.0.16 (nonreserved)

• NEVER

• NEW

• NEXT

• NO

• NODEGROUP

• NONE

• NOT (R)

• NOWAIT; added in 8.0.1 (nonreserved)

• NO_WAIT

• NO_WRITE_TO_BINLOG (R)

• NTH_VALUE (R); added in 8.0.2 (reserved)

• NTILE (R); added in 8.0.2 (reserved)

• NULL (R)

• NULLS; added in 8.0.2 (nonreserved)

• NUMBER

• NUMERIC (R)

• NVARCHAR

O

• OF (R); added in 8.0.1 (reserved)

• OFF; added in 8.0.20 (nonreserved)

2086

MySQL 8.0 Keywords and Reserved Words

• OFFSET

• OJ; added in 8.0.16 (nonreserved)

• OLD; added in 8.0.14 (nonreserved)

• ON (R)

• ONE

• ONLY

• OPEN

• OPTIMIZE (R)

• OPTIMIZER_COSTS (R)

• OPTION (R)

• OPTIONAL; added in 8.0.13 (nonreserved)

• OPTIONALLY (R)

• OPTIONS

• OR (R)

• ORDER (R)

• ORDINALITY; added in 8.0.4 (nonreserved)

• ORGANIZATION; added in 8.0.4 (nonreserved)

• OTHERS; added in 8.0.2 (nonreserved)

• OUT (R)

• OUTER (R)

• OUTFILE (R)

• OVER (R); added in 8.0.2 (reserved)

• OWNER

P

• PACK_KEYS

• PAGE

• PARSER

• PARTIAL

• PARTITION (R)

• PARTITIONING

• PARTITIONS

• PASSWORD

• PASSWORD_LOCK_TIME; added in 8.0.19 (nonreserved)

2087

MySQL 8.0 Keywords and Reserved Words

• PATH; added in 8.0.4 (nonreserved)

• PERCENT_RANK (R); added in 8.0.2 (reserved)

• PERSIST; became nonreserved in 8.0.16

• PERSIST_ONLY; added in 8.0.2 (reserved); became nonreserved in 8.0.16

• PHASE

• PLUGIN

• PLUGINS

• PLUGIN_DIR

• POINT

• POLYGON

• PORT

• PRECEDES

• PRECEDING; added in 8.0.2 (nonreserved)

• PRECISION (R)

• PREPARE

• PRESERVE

• PREV

• PRIMARY (R)

• PRIVILEGES

• PRIVILEGE_CHECKS_USER; added in 8.0.18 (nonreserved)

• PROCEDURE (R)

• PROCESS; added in 8.0.11 (nonreserved)

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

• RANDOM; added in 8.0.18 (nonreserved)

2088

MySQL 8.0 Keywords and Reserved Words

• RANGE (R)

• RANK (R); added in 8.0.2 (reserved)

• READ (R)

• READS (R)

• READ_ONLY

• READ_WRITE (R)

• REAL (R)

• REBUILD

• RECOVER

• RECURSIVE (R); added in 8.0.1 (reserved)

• REDOFILE; removed in 8.0.3

• REDO_BUFFER_SIZE

• REDUNDANT

• REFERENCE; added in 8.0.4 (nonreserved)

• REFERENCES (R)

• REGEXP (R)

• REGISTRATION; added in 8.0.27 (nonreserved)

• RELAY

• RELAYLOG

• RELAY_LOG_FILE

• RELAY_LOG_POS

• RELAY_THREAD

• RELEASE (R)

• RELOAD

• REMOTE; added in 8.0.3 (nonreserved); removed in 8.0.14

• REMOVE

• RENAME (R)

• REORGANIZE

• REPAIR

• REPEAT (R)

• REPEATABLE

• REPLACE (R)

• REPLICA; added in 8.0.22 (nonreserved)

2089

MySQL 8.0 Keywords and Reserved Words

• REPLICAS; added in 8.0.22 (nonreserved)

• REPLICATE_DO_DB

• REPLICATE_DO_TABLE

• REPLICATE_IGNORE_DB

• REPLICATE_IGNORE_TABLE

• REPLICATE_REWRITE_DB

• REPLICATE_WILD_DO_TABLE

• REPLICATE_WILD_IGNORE_TABLE

• REPLICATION

• REQUIRE (R)

• REQUIRE_ROW_FORMAT; added in 8.0.19 (nonreserved)

• RESET

• RESIGNAL (R)

• RESOURCE; added in 8.0.3 (nonreserved)

• RESPECT; added in 8.0.2 (nonreserved)

• RESTART; added in 8.0.4 (nonreserved)

• RESTORE

• RESTRICT (R)

• RESUME

• RETAIN; added in 8.0.14 (nonreserved)

• RETURN (R)

• RETURNED_SQLSTATE

• RETURNING; added in 8.0.21 (nonreserved)

• RETURNS

• REUSE; added in 8.0.3 (nonreserved)

• REVERSE

• REVOKE (R)

• RIGHT (R)

• RLIKE (R)

• ROLE; became nonreserved in 8.0.1

• ROLLBACK

• ROLLUP

• ROTATE

2090

MySQL 8.0 Keywords and Reserved Words

• ROUTINE

• ROW (R); became reserved in 8.0.2

• ROWS (R); became reserved in 8.0.2

• ROW_COUNT

• ROW_FORMAT

• ROW_NUMBER (R); added in 8.0.2 (reserved)

• RTREE

S

• SAVEPOINT

• SCHEDULE

• SCHEMA (R)

• SCHEMAS (R)

• SCHEMA_NAME

• SECOND

• SECONDARY; added in 8.0.16 (nonreserved)

• SECONDARY_ENGINE; added in 8.0.13 (nonreserved)

• SECONDARY_ENGINE_ATTRIBUTE; added in 8.0.21 (nonreserved)

• SECONDARY_LOAD; added in 8.0.13 (nonreserved)

• SECONDARY_UNLOAD; added in 8.0.13 (nonreserved)

• SECOND_MICROSECOND (R)

• SECURITY

• SELECT (R)

• SENSITIVE (R)

• SEPARATOR (R)

• SERIAL

• SERIALIZABLE

• SERVER

• SESSION

• SET (R)

• SHARE

• SHOW (R)

• SHUTDOWN

• SIGNAL (R)

2091

MySQL 8.0 Keywords and Reserved Words

• SIGNED

• SIMPLE

• SKIP; added in 8.0.1 (nonreserved)

• SLAVE

• SLOW

• SMALLINT (R)

• SNAPSHOT

• SOCKET

• SOME

• SONAME

• SOUNDS

• SOURCE

• SOURCE_AUTO_POSITION; added in 8.0.23 (nonreserved)

• SOURCE_BIND; added in 8.0.23 (nonreserved)

• SOURCE_COMPRESSION_ALGORITHMS; added in 8.0.23 (nonreserved)

• SOURCE_CONNECT_RETRY; added in 8.0.23 (nonreserved)

• SOURCE_DELAY; added in 8.0.23 (nonreserved)

• SOURCE_HEARTBEAT_PERIOD; added in 8.0.23 (nonreserved)

• SOURCE_HOST; added in 8.0.23 (nonreserved)

• SOURCE_LOG_FILE; added in 8.0.23 (nonreserved)

• SOURCE_LOG_POS; added in 8.0.23 (nonreserved)

• SOURCE_PASSWORD; added in 8.0.23 (nonreserved)

• SOURCE_PORT; added in 8.0.23 (nonreserved)

• SOURCE_PUBLIC_KEY_PATH; added in 8.0.23 (nonreserved)

• SOURCE_RETRY_COUNT; added in 8.0.23 (nonreserved)

• SOURCE_SSL; added in 8.0.23 (nonreserved)

• SOURCE_SSL_CA; added in 8.0.23 (nonreserved)

• SOURCE_SSL_CAPATH; added in 8.0.23 (nonreserved)

• SOURCE_SSL_CERT; added in 8.0.23 (nonreserved)

• SOURCE_SSL_CIPHER; added in 8.0.23 (nonreserved)

• SOURCE_SSL_CRL; added in 8.0.23 (nonreserved)

• SOURCE_SSL_CRLPATH; added in 8.0.23 (nonreserved)

• SOURCE_SSL_KEY; added in 8.0.23 (nonreserved)

2092

MySQL 8.0 Keywords and Reserved Words

• SOURCE_SSL_VERIFY_SERVER_CERT; added in 8.0.23 (nonreserved)

• SOURCE_TLS_CIPHERSUITES; added in 8.0.23 (nonreserved)

• SOURCE_TLS_VERSION; added in 8.0.23 (nonreserved)

• SOURCE_USER; added in 8.0.23 (nonreserved)

• SOURCE_ZSTD_COMPRESSION_LEVEL; added in 8.0.23 (nonreserved)

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

• SQL_CACHE; removed in 8.0.3

• SQL_CALC_FOUND_ROWS (R)

• SQL_NO_CACHE

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

• SRID; added in 8.0.3 (nonreserved)

• SSL (R)

• STACKED

• START

2093

MySQL 8.0 Keywords and Reserved Words

• STARTING (R)

• STARTS

• STATS_AUTO_RECALC

• STATS_PERSISTENT

• STATS_SAMPLE_PAGES

• STATUS

• STOP

• STORAGE

• STORED (R)

• STRAIGHT_JOIN (R)

• STREAM; added in 8.0.20 (nonreserved)

• STRING

• SUBCLASS_ORIGIN

• SUBJECT

• SUBPARTITION

• SUBPARTITIONS

• SUPER

• SUSPEND

• SWAPS

• SWITCHES

• SYSTEM (R); added in 8.0.3 (reserved)

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

2094

MySQL 8.0 Keywords and Reserved Words

• THREAD_PRIORITY; added in 8.0.3 (nonreserved)

• TIES; added in 8.0.2 (nonreserved)

• TIME

• TIMESTAMP

• TIMESTAMPADD

• TIMESTAMPDIFF

• TINYBLOB (R)

• TINYINT (R)

• TINYTEXT (R)

• TLS; added in 8.0.21 (nonreserved)

• TO (R)

• TRAILING (R)

• TRANSACTION

• TRIGGER (R)

• TRIGGERS

• TRUE (R)

• TRUNCATE

• TYPE

• TYPES

U

• UNBOUNDED; added in 8.0.2 (nonreserved)

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

• UNREGISTER; added in 8.0.27 (nonreserved)

2095

MySQL 8.0 Keywords and Reserved Words

• UNSIGNED (R)

• UNTIL

• UPDATE (R)

• UPGRADE

• URL; added in 8.0.32 (nonreserved)

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

• VALIDATION

• VALUE

• VALUES (R)

• VARBINARY (R)

• VARCHAR (R)

• VARCHARACTER (R)

• VARIABLES

• VARYING (R)

• VCPU; added in 8.0.3 (nonreserved)

• VIEW

• VIRTUAL (R)

• VISIBLE

W

• WAIT

• WARNINGS

• WEEK

• WEIGHT_STRING

• WHEN (R)

2096

MySQL 8.0 New Keywords and Reserved Words

• WHERE (R)

• WHILE (R)

• WINDOW (R); added in 8.0.2 (reserved)

• WITH (R)

• WITHOUT

• WORK

• WRAPPER

• WRITE (R)

X

• X509

• XA

• XID

• XML

• XOR (R)

Y

• YEAR

• YEAR_MONTH (R)

Z

• ZEROFILL (R)

• ZONE; added in 8.0.22 (nonreserved)

MySQL 8.0 New Keywords and Reserved Words

The following list shows the keywords and reserved words that are added in MySQL 8.0, compared to
MySQL 5.7. Reserved keywords are marked with (R).

A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | R | S | T | U | V | W | Z

A

• ACTIVE

• ADMIN

• ARRAY

• ATTRIBUTE

• AUTHENTICATION

B

• BUCKETS

• BULK

2097

MySQL 8.0 New Keywords and Reserved Words

C

• CHALLENGE_RESPONSE

• CLONE

• COMPONENT

• CUME_DIST (R)

D

• DEFINITION

• DENSE_RANK (R)

• DESCRIPTION

E

• EMPTY (R)

• ENFORCED

• ENGINE_ATTRIBUTE

• EXCEPT (R)

• EXCLUDE

F

• FACTOR

• FAILED_LOGIN_ATTEMPTS

• FINISH

• FIRST_VALUE (R)

• FOLLOWING

G

• GENERATE

• GEOMCOLLECTION

• GET_MASTER_PUBLIC_KEY

• GET_SOURCE_PUBLIC_KEY

• GROUPING (R)

• GROUPS (R)

• GTID_ONLY

H

• HISTOGRAM

• HISTORY

2098

MySQL 8.0 New Keywords and Reserved Words

I

• INACTIVE

• INITIAL

• INITIATE

• INTERSECT (R)

• INVISIBLE

J

• JSON_TABLE (R)

• JSON_VALUE

K

• KEYRING

L

• LAG (R)

• LAST_VALUE (R)

• LATERAL (R)

• LEAD (R)

• LOCKED

M

• MASTER_COMPRESSION_ALGORITHMS

• MASTER_PUBLIC_KEY_PATH

• MASTER_TLS_CIPHERSUITES

• MASTER_ZSTD_COMPRESSION_LEVEL

• MEMBER

N

• NESTED

• NETWORK_NAMESPACE

• NOWAIT

• NTH_VALUE (R)

• NTILE (R)

• NULLS

O

• OF (R)

2099

MySQL 8.0 New Keywords and Reserved Words

• OFF

• OJ

• OLD

• OPTIONAL

• ORDINALITY

• ORGANIZATION

• OTHERS

• OVER (R)

P

• PASSWORD_LOCK_TIME

• PATH

• PERCENT_RANK (R)

• PERSIST

• PERSIST_ONLY

• PRECEDING

• PRIVILEGE_CHECKS_USER

• PROCESS

R

• RANDOM

• RANK (R)

• RECURSIVE (R)

• REFERENCE

• REGISTRATION

• REPLICA

• REPLICAS

• REQUIRE_ROW_FORMAT

• RESOURCE

• RESPECT

• RESTART

• RETAIN

• RETURNING

• REUSE

• ROLE

2100

MySQL 8.0 New Keywords and Reserved Words

• ROW_NUMBER (R)

S

• SECONDARY

• SECONDARY_ENGINE

• SECONDARY_ENGINE_ATTRIBUTE

• SECONDARY_LOAD

• SECONDARY_UNLOAD

• SKIP

• SOURCE_AUTO_POSITION

• SOURCE_BIND

• SOURCE_COMPRESSION_ALGORITHMS

• SOURCE_CONNECT_RETRY

• SOURCE_DELAY

• SOURCE_HEARTBEAT_PERIOD

• SOURCE_HOST

• SOURCE_LOG_FILE

• SOURCE_LOG_POS

• SOURCE_PASSWORD

• SOURCE_PORT

• SOURCE_PUBLIC_KEY_PATH

• SOURCE_RETRY_COUNT

• SOURCE_SSL

• SOURCE_SSL_CA

• SOURCE_SSL_CAPATH

• SOURCE_SSL_CERT

• SOURCE_SSL_CIPHER

• SOURCE_SSL_CRL

• SOURCE_SSL_CRLPATH

• SOURCE_SSL_KEY

• SOURCE_SSL_VERIFY_SERVER_CERT

• SOURCE_TLS_CIPHERSUITES

• SOURCE_TLS_VERSION

• SOURCE_USER

2101

MySQL 8.0 Removed Keywords and Reserved Words

• SOURCE_ZSTD_COMPRESSION_LEVEL

• SRID

• STREAM

• SYSTEM (R)

T

• THREAD_PRIORITY

• TIES

• TLS

U

• UNBOUNDED

• UNREGISTER

• URL

V

• VCPU

• VISIBLE

W

• WINDOW (R)

Z

• ZONE

MySQL 8.0 Removed Keywords and Reserved Words

The following list shows the keywords and reserved words that are removed in MySQL 8.0, compared
to MySQL 5.7. Reserved keywords are marked with (R).

• ANALYSE

• DES_KEY_FILE

• MASTER_SERVER_ID

• PARSE_GCOL_EXPR

• REDOFILE

• SQL_CACHE

MySQL 8.0 Restricted Keywords

Some MySQL keywords are not reserved but even so must be quoted in certain circumstances. This
section provides listings of these keywords.

• Keywords which must be quoted when used as labels

• Keywords which must be quoted when used as role names

2102

MySQL 8.0 Restricted Keywords

• Keywords which must be quoted when used as labels or role names

Keywords which must be quoted when used as labels

The keywords listed here must be quoted when used as labels in MySQL stored programs:

A | B | C | D | E | F | H | I | L | N | P | R | S | T | U | X

A

• ASCII

B

• BEGIN

• BYTE

C

• CACHE

• CHARSET

• CHECKSUM

• CLONE

• COMMENT

• COMMIT

• CONTAINS

D

• DEALLOCATE

• DO

E

• END

F

• FLUSH

• FOLLOWS

H

• HANDLER

• HELP

I

• IMPORT

• INSTALL

L

2103

MySQL 8.0 Restricted Keywords

• LANGUAGE

N

• NO

P

• PRECEDES

• PREPARE

R

• REPAIR

• RESET

• ROLLBACK

S

• SAVEPOINT

• SIGNED

• SLAVE

• START

• STOP

T

• TRUNCATE

U

• UNICODE

• UNINSTALL

X

• XA

Keywords which must be quoted when used as role names

The keywords listed here must be quoted when used as names of roles:

• EVENT

• FILE

• NONE

• PROCESS

• PROXY

• RELOAD

• REPLICATION

2104

User-Defined Variables

• RESOURCE

• SUPER

Keywords which must be quoted when used as labels or role names

The keywords listed here must be quoted when used as labels in stored programs, or as names of
roles:

• EXECUTE

• RESTART

• SHUTDOWN

11.4 User-Defined Variables

You can store a value in a user-defined variable in one statement and refer to it later in another
statement. This enables you to pass values from one statement to another.

User variables are written as @var_name, where the variable name var_name consists of
alphanumeric characters, ., _, and $. A user variable name can contain other characters if you quote it
as a string or identifier (for example, @'my-var', @"my-var", or @`my-var`).

User-defined variables are session specific. A user variable defined by one client cannot be
seen or used by other clients. (Exception: A user with access to the Performance Schema
user_variables_by_thread table can see all user variables for all sessions.) All variables for a
given client session are automatically freed when that client exits.

User variable names are not case-sensitive. Names have a maximum length of 64 characters.

One way to set a user-defined variable is by issuing a SET statement:

SET @var_name = expr [, @var_name = expr] ...

For SET, either = or := can be used as the assignment operator.

User variables can be assigned a value from a limited set of data types: integer, decimal, floating-point,
binary or nonbinary string, or NULL value. Assignment of decimal and real values does not preserve the
precision or scale of the value. A value of a type other than one of the permissible types is converted to
a permissible type. For example, a value having a temporal or spatial data type is converted to a binary
string. A value having the JSON data type is converted to a string with a character set of utf8mb4 and
a collation of utf8mb4_bin.

If a user variable is assigned a nonbinary (character) string value, it has the same character set and
collation as the string. The coercibility of user variables is implicit. (This is the same coercibility as for
table column values.)

Hexadecimal or bit values assigned to user variables are treated as binary strings. To assign a
hexadecimal or bit value as a number to a user variable, use it in numeric context. For example, add 0
or use CAST(... AS UNSIGNED):

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

2105

User-Defined Variables

mysql> SET @v3 = CAST(b'1000001' AS UNSIGNED);
mysql> SELECT @v1, @v2, @v3;
+------+------+------+
| @v1  | @v2  | @v3  |
+------+------+------+
| A    |   65 |   65 |
+------+------+------+

If the value of a user variable is selected in a result set, it is returned to the client as a string.

If you refer to a variable that has not been initialized, it has a value of NULL and a type of string.

Beginning with MySQL 8.0.22, a reference to a user variable in a prepared statement has its type
determined when the statement is first prepared, and retains this type each time the statement is
executed thereafter. Similarly, the type of a user variable employed in a statement within a stored
procedure is determined the first time the stored procedure is invoked, and retains this type with each
subsequent invocation.

User variables may be used in most contexts where expressions are permitted. This does not currently
include contexts that explicitly require a literal value, such as in the LIMIT clause of a SELECT
statement, or the IGNORE N LINES clause of a LOAD DATA statement.

Previous releases of MySQL made it possible to assign a value to a user variable in statements other
than SET. This functionality is supported in MySQL 8.0 for backward compatibility but is subject to
removal in a future release of MySQL.

When making an assignment in this way, you must use := as the assignment operator; = is treated as
the comparison operator in statements other than SET.

The order of evaluation for expressions involving user variables is undefined. For example, there is no
guarantee that SELECT @a, @a:=@a+1 evaluates @a first and then performs the assignment.

In addition, the default result type of a variable is based on its type at the beginning of the statement.
This may have unintended effects if a variable holds a value of one type at the beginning of a
statement in which it is also assigned a new value of a different type.

To avoid problems with this behavior, either do not assign a value to and read the value of the same
variable within a single statement, or else set the variable to 0, 0.0, or '' to define its type before you
use it.

HAVING, GROUP BY, and ORDER BY, when referring to a variable that is assigned a value in the select
expression list do not work as expected because the expression is evaluated on the client and thus can
use stale column values from a previous row.

User variables are intended to provide data values. They cannot be used directly in an SQL statement
as an identifier or as part of an identifier, such as in contexts where a table or database name is
expected, or as a reserved word such as SELECT. This is true even if the variable is quoted, as shown
in the following example:

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
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @col FROM t;
+------+

2106

Expressions

  $mysqli->close();
?>

Assembling an SQL statement in this fashion is sometimes known as “Dynamic SQL”.

11.5 Expressions

This section lists the grammar rules that expressions must follow in MySQL and provides additional
information about the types of terms that may appear in expressions.

• Expression Syntax

• Expression Term Notes

• Temporal Intervals

Expression Syntax

The following grammar rules define expression syntax in MySQL. The grammar shown here is based
on that given in the sql/sql_yacc.yy file of MySQL source distributions. For additional information
about some of the expression terms, see Expression Term Notes.

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

2108

Expression Term Notes

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

For operator precedence, see Section 14.4.1, “Operator Precedence”. The precedence and meaning of
some operators depends on the SQL mode:

• By default, || is a logical OR operator. With PIPES_AS_CONCAT enabled, || is string concatenation,

with a precedence between ^ and the unary operators.

• By default, ! has a higher precedence than NOT. With HIGH_NOT_PRECEDENCE enabled, ! and NOT

have the same precedence.

See Section 7.1.11, “Server SQL Modes”.

Expression Term Notes

For literal value syntax, see Section 11.1, “Literal Values”.

For identifier syntax, see Section 11.2, “Schema Object Names”.

Variables can be user variables, system variables, or stored program local variables or parameters:

• User variables: Section 11.4, “User-Defined Variables”

• System variables: Section 7.1.9, “Using System Variables”

• Stored program local variables: Section 15.6.4.1, “Local Variable DECLARE Statement”

• Stored program parameters: Section 15.1.17, “CREATE PROCEDURE and CREATE FUNCTION

Statements”

param_marker is ? as used in prepared statements for placeholders. See Section 15.5.1, “PREPARE
Statement”.

(subquery) indicates a subquery that returns a single value; that is, a scalar subquery. See
Section 15.2.15.1, “The Subquery as Scalar Operand”.

{identifier expr} is ODBC escape syntax and is accepted for ODBC compatibility. The value is
expr. The { and } curly braces in the syntax should be written literally; they are not metasyntax as
used elsewhere in syntax descriptions.

match_expr indicates a MATCH expression. See Section 14.9, “Full-Text Search Functions”.

case_expr indicates a CASE expression. See Section 14.5, “Flow Control Functions”.

interval_expr represents a temporal interval. See Temporal Intervals.

2109

Temporal Intervals

Temporal Intervals

interval_expr in expressions represents a temporal interval. Intervals have this syntax:

INTERVAL expr unit

expr represents a quantity. unit represents the unit for interpreting the quantity; it is a specifier such
as HOUR, DAY, or WEEK. The INTERVAL keyword and the unit specifier are not case-sensitive.

The following table shows the expected form of the expr argument for each unit value.

Table 11.2 Temporal Interval Expression and Unit Arguments

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

DAY_HOUR

YEAR_MONTH

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

'DAYS HOURS'

'YEARS-MONTHS'

MySQL permits any punctuation delimiter in the expr format. Those shown in the table are the
suggested delimiters.

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

2110

Query Attributes

        -> 1.5
mysql> SELECT DATE_ADD('1970-01-01 12:00:00',
    ->                 INTERVAL CAST(6/4 AS DECIMAL(3,1)) HOUR_MINUTE);
        -> '1970-01-01 13:05:00'

If you add to or subtract from a date value something that contains a time part, the result is
automatically converted to a datetime value:

mysql> SELECT DATE_ADD('2023-01-01', INTERVAL 1 DAY);
        -> '2023-01-02'
mysql> SELECT DATE_ADD('2023-01-01', INTERVAL 1 HOUR);
        -> '2023-01-01 01:00:00'

If you add MONTH, YEAR_MONTH, or YEAR and the resulting date has a day that is larger than the
maximum day for the new month, the day is adjusted to the maximum days in the new month:

mysql> SELECT DATE_ADD('2019-01-30', INTERVAL 1 MONTH);
        -> '2019-02-28'

Date arithmetic operations require complete dates and do not work with incomplete dates such as
'2016-07-00' or badly malformed dates:

mysql> SELECT DATE_ADD('2016-07-00', INTERVAL 1 DAY);
        -> NULL
mysql> SELECT '2005-03-32' + INTERVAL 1 MONTH;
        -> NULL

11.6 Query Attributes

The most visible part of an SQL statement is the text of the statement. As of MySQL 8.0.23, clients can
also define query attributes that apply to the next statement sent to the server for execution:

• Attributes are defined prior to sending the statement.

• Attributes exist until statement execution ends, at which point the attribute set is cleared.

• While attributes exist, they can be accessed on the server side.

Examples of the ways query attributes may be used:

• A web application produces pages that generate database queries, and for each query must track

the URL of the page that generated it.

• An application passes extra processing information with each query, for use by a plugin such as an

audit plugin or query rewrite plugin.

MySQL supports these capabilities without the use of workarounds such as specially formatted
comments included in query strings. The remainder of this section describes how to use query attribute
support, including the prerequisites that must be satisfied.

• Defining and Accessing Query Attributes

• Prerequisites for Using Query Attributes

• Query Attribute Loadable Functions

Defining and Accessing Query Attributes

Applications that use the MySQL C API define query attributes by calling the mysql_bind_param()
function. See mysql_bind_param(). Other MySQL connectors may also provide query-attribute support.
See the documentation for individual connectors.

The mysql client has a query_attributes command that enables defining up to 32 pairs of
attribute names and values. See Section 6.5.1.2, “mysql Client Commands”.

2112

Defining and Accessing Query Attributes

Query attribute names are transmitted using the character set indicated by the
character_set_client system variable.

To access query attributes within SQL statements for which attributes have been defined, install
the query_attributes component as described in Prerequisites for Using Query Attributes. The
component implements a mysql_query_attribute_string() loadable function that takes an
attribute name argument and returns the attribute value as a string, or NULL if the attribute does not
exist. See Query Attribute Loadable Functions.

The following examples use the mysql client query_attributes command to define attribute name/
value pairs, and the mysql_query_attribute_string() function to access attribute values by
name.

This example defines two attributes named n1 and n2. The first SELECT shows how to retrieve those
attributes, and also demonstrates that retrieving a nonexistent attribute (n3) returns NULL. The second
SELECT shows that attributes do not persist across statements.

mysql> query_attributes n1 v1 n2 v2;
mysql> SELECT
         mysql_query_attribute_string('n1') AS 'attr 1',
         mysql_query_attribute_string('n2') AS 'attr 2',
         mysql_query_attribute_string('n3') AS 'attr 3';
+--------+--------+--------+
| attr 1 | attr 2 | attr 3 |
+--------+--------+--------+
| v1     | v2     | NULL   |
+--------+--------+--------+

mysql> SELECT
         mysql_query_attribute_string('n1') AS 'attr 1',
         mysql_query_attribute_string('n2') AS 'attr 2';
+--------+--------+
| attr 1 | attr 2 |
+--------+--------+
| NULL   | NULL   |
+--------+--------+

As shown by the second SELECT statement, attributes defined prior to a given statement are available
only to that statement and are cleared after the statement executes. To use an attribute value across
multiple statements, assign it to a variable. The following example shows how to do this, and illustrates
that attribute values are available in subsequent statements by means of the variables, but not by
calling mysql_query_attribute_string():

mysql> query_attributes n1 v1 n2 v2;
mysql> SET
         @attr1 = mysql_query_attribute_string('n1'),
         @attr2 = mysql_query_attribute_string('n2');

mysql> SELECT
         @attr1, mysql_query_attribute_string('n1') AS 'attr 1',
         @attr2, mysql_query_attribute_string('n2') AS 'attr 2';
+--------+--------+--------+--------+
| @attr1 | attr 1 | @attr2 | attr 2 |
+--------+--------+--------+--------+
| v1     | NULL   | v2     | NULL   |
+--------+--------+--------+--------+

Attributes can also be saved for later use by storing them in a table:

mysql> CREATE TABLE t1 (c1 CHAR(20), c2 CHAR(20));

mysql> query_attributes n1 v1 n2 v2;
mysql> INSERT INTO t1 (c1, c2) VALUES(
         mysql_query_attribute_string('n1'),
         mysql_query_attribute_string('n2')
       );

mysql> SELECT * FROM t1;

2113

Prerequisites for Using Query Attributes

+------+------+
| c1   | c2   |
+------+------+
| v1   | v2   |
+------+------+

Query attributes are subject to these limitations and restrictions:

• If multiple attribute-definition operations occur prior to sending a statement to the server for

execution, the most recent definition operation applies and replaces attributes defined in earlier
operations.

• If multiple attributes are defined with the same name, attempts to retrieve the attribute value have an

undefined result.

• An attribute defined with an empty name cannot be retrieved by name.

• Attributes are not available to statements prepared with PREPARE.

• The mysql_query_attribute_string() function cannot be used in DDL statements.

• Attributes are not replicated. Statements that invoke the mysql_query_attribute_string()

function will not get the same value on all servers.

Prerequisites for Using Query Attributes

To access query attributes within SQL statements for which attributes have been defined, the
query_attributes component must be installed. Do so using this statement:

INSTALL COMPONENT "file://component_query_attributes";

Component installation is a one-time operation that need not be done per server startup. INSTALL
COMPONENT loads the component, and also registers it in the mysql.component system table to
cause it to be loaded during subsequent server startups.

The query_attributes component accesses query attributes to implement a
mysql_query_attribute_string() function. See Section 7.5.4, “Query Attribute Components”.

To uninstall the query_attributes component, use this statement:

UNINSTALL COMPONENT "file://component_query_attributes";

UNINSTALL COMPONENT unloads the component, and unregisters it from the mysql.component
system table to cause it not to be loaded during subsequent server startups.

Because installing and uninstalling the query_attributes component installs and uninstalls the
mysql_query_attribute_string() function that the component implements, it is not necessary to
use CREATE FUNCTION or DROP FUNCTION to do so.

Query Attribute Loadable Functions

• mysql_query_attribute_string(name)

Applications can define attributes that apply to the next query sent to the server. The
mysql_query_attribute_string() function, available as of MySQL 8.0.23, returns an attribute
value as a string, given the attribute name. This function enables a query to access and incorporate
values of the attributes that apply to it.

mysql_query_attribute_string() is installed by installing the query_attributes
component. See Section 11.6, “Query Attributes”, which also discusses the purpose and use of
query attributes.

Arguments:

2114

Comments

• name: The attribute name.

Return value:

Returns the attribute value as a string for success, or NULL if the attribute does not exist.

Example:

The following example uses the mysql client query_attributes command to define query
attributes that can be retrieved by mysql_query_attribute_string(). The SELECT shows that
retrieving a nonexistent attribute (n3) returns NULL.

mysql> query_attributes n1 v1 n2 v2;
mysql> SELECT
    ->   mysql_query_attribute_string('n1') AS 'attr 1',
    ->   mysql_query_attribute_string('n2') AS 'attr 2',
    ->   mysql_query_attribute_string('n3') AS 'attr 3';
+--------+--------+--------+
| attr 1 | attr 2 | attr 3 |
+--------+--------+--------+
| v1     | v2     | NULL   |
+--------+--------+--------+

11.7 Comments

MySQL Server supports three comment styles:

• From a # character to the end of the line.

• From a --  sequence to the end of the line. In MySQL, the --  (double-dash) comment style

requires the second dash to be followed by at least one whitespace or control character, such as
a space or tab. This syntax differs slightly from standard SQL comment syntax, as discussed in
Section 1.6.2.4, “'--' as the Start of a Comment”.

• From a /* sequence to the following */ sequence, as in the C programming language. This syntax

enables a comment to extend over multiple lines because the beginning and closing sequences need
not be on the same line.

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

Nested comments are not supported, and are deprecated; expect them to be removed in a future
MySQL release. (Under some conditions, nested comments might be permitted, but usually are not,
and users should avoid them.)

MySQL Server supports certain variants of C-style comments. These enable you to write code that
includes MySQL extensions, but is still portable, by using comments of the following form:

/*! MySQL-specific code */

In this case, MySQL Server parses and executes the code within the comment as it would any other
SQL statement, but other SQL servers should ignore the extensions. For example, MySQL Server
recognizes the STRAIGHT_JOIN keyword in the following statement, but other servers should not:

SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...

2115

