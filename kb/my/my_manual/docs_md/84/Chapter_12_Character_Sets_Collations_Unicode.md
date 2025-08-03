Character Sets and Collations in General

12.14.1 Collation Implementation Types ........................................................................... 1991
12.14.2 Choosing a Collation ID ...................................................................................... 1994
12.14.3 Adding a Simple Collation to an 8-Bit Character Set ............................................. 1995
12.14.4 Adding a UCA Collation to a Unicode Character Set ............................................. 1996
12.15 Character Set Configuration ........................................................................................... 2002
12.16 MySQL Server Locale Support ....................................................................................... 2003

MySQL includes character set support that enables you to store data using a variety of character sets
and perform comparisons according to a variety of collations. The default MySQL server character
set and collation are utf8mb4 and utf8mb4_0900_ai_ci, but you can specify character sets at
the server, database, table, column, and string literal levels. To maximize interoperability and future-
proofing of your data and applications, we recommend that you use the utf8mb4 character set
whenever possible.

Note

UTF8 is a deprecated synonym for utf8mb3, and you should expect it to be
removed in a future version of MySQL. Specify utfmb3 or (preferably) utfmb4
instead.

This chapter discusses the following topics:

• What are character sets and collations?

• The multiple-level default system for character set assignment.

• Syntax for specifying character sets and collations.

• Affected functions and operations.

• Unicode support.

• The character sets and collations that are available, with notes.

• Selecting the language for error messages.

• Selecting the locale for day and month names.

Character set issues affect not only data storage, but also communication between client programs and
the MySQL server. If you want the client program to communicate with the server using a character set
different from the default, you need to indicate which one. For example, to use the latin1 Unicode
character set, issue this statement after connecting to the server:

SET NAMES 'latin1';

For more information about configuring character sets for application use and character set-related
issues in client/server communication, see Section 12.5, “Configuring Application Character Set and
Collation”, and Section 12.4, “Connection Character Sets and Collations”.

12.1 Character Sets and Collations in General

A character set is a set of symbols and encodings. A collation is a set of rules for comparing characters
in a character set. Let's make the distinction clear with an example of an imaginary character set.

Suppose that we have an alphabet with four letters: A, B, a, b. We give each letter a number: A = 0, B =
1, a = 2, b = 3. The letter A is a symbol, the number 0 is the encoding for A, and the combination of all
four letters and their encodings is a character set.

Suppose that we want to compare two string values, A and B. The simplest way to do this is to look at
the encodings: 0 for A and 1 for B. Because 0 is less than 1, we say A is less than B. What we've just

1928

Character Set Repertoire

• The repertoire for a string constant depends on string content and may differ from the repertoire of

the string character set. Consider these statements:

SET NAMES utf8mb4; SELECT 'abc';
SELECT _utf8mb4'def';

Although the character set is utf8mb4 in each of the preceding cases, the strings do not actually
contain any characters outside the ASCII range, so their repertoire is ASCII rather than UNICODE.

• A column having the ascii character set has ASCII repertoire because of its character set. In the

following table, c1 has ASCII repertoire:

CREATE TABLE t1 (c1 CHAR(1) CHARACTER SET ascii);

The following example illustrates how repertoire enables a result to be determined in a case where
an error occurs without repertoire:

CREATE TABLE t1 (
  c1 CHAR(1) CHARACTER SET latin1,
  c2 CHAR(1) CHARACTER SET ascii
);
INSERT INTO t1 VALUES ('a','b');
SELECT CONCAT(c1,c2) FROM t1;

Without repertoire, this error occurs:

ERROR 1267 (HY000): Illegal mix of collations (latin1_swedish_ci,IMPLICIT)
and (ascii_general_ci,IMPLICIT) for operation 'concat'

Using repertoire, subset to superset (ascii to latin1) conversion can occur and a result is
returned:

+---------------+
| CONCAT(c1,c2) |
+---------------+
| ab            |
+---------------+

• Functions with one string argument inherit the repertoire of their argument. The result of

UPPER(_utf8mb4'abc') has ASCII repertoire because its argument has ASCII repertoire.
(Despite the _utf8mb4 introducer, the string 'abc' contains no characters outside the ASCII
range.)

• For functions that return a string but do not have string arguments and use

character_set_connection as the result character set, the result repertoire is ASCII if
character_set_connection is ascii, and UNICODE otherwise:

FORMAT(numeric_column, 4);

Use of repertoire changes how MySQL evaluates the following example:

SET NAMES ascii;
CREATE TABLE t1 (a INT, b VARCHAR(10) CHARACTER SET latin1);
INSERT INTO t1 VALUES (1,'b');
SELECT CONCAT(FORMAT(a, 4), b) FROM t1;

Without repertoire, this error occurs:

ERROR 1267 (HY000): Illegal mix of collations (ascii_general_ci,COERCIBLE)
and (latin1_swedish_ci,IMPLICIT) for operation 'concat'

With repertoire, a result is returned:

+-------------------------+
| CONCAT(FORMAT(a, 4), b) |
+-------------------------+
| 1.0000b                 |

1932

Server Character Set and Collation

• Collation suffixes indicate whether a collation is case-sensitive, accent-sensitive, or kana-sensitive
(or some combination thereof), or binary. The following table shows the suffixes used to indicate
these characteristics.

Table 12.1 Collation Suffix Meanings

Suffix

_ai

_as

_ci

_cs

_ks

_bin

Meaning

Accent-insensitive

Accent-sensitive

Case-insensitive

Case-sensitive

Kana-sensitive

Binary

For nonbinary collation names that do not specify accent sensitivity, it is determined by case
sensitivity. If a collation name does not contain _ai or _as, _ci in the name implies _ai and _cs
in the name implies _as. For example, latin1_general_ci is explicitly case-insensitive and
implicitly accent-insensitive, latin1_general_cs is explicitly case-sensitive and implicitly accent-
sensitive, and utf8mb4_0900_ai_ci is explicitly case-insensitive and accent-insensitive.

For Japanese collations, the _ks suffix indicates that a collation is kana-sensitive; that is, it
distinguishes Katakana characters from Hiragana characters. Japanese collations without the _ks
suffix are not kana-sensitive and treat Katakana and Hiragana characters equal for sorting.

For the binary collation of the binary character set, comparisons are based on numeric byte
values. For the _bin collation of a nonbinary character set, comparisons are based on numeric
character code values, which differ from byte values for multibyte characters. For information about
the differences between the binary collation of the binary character set and the _bin collations of
nonbinary character sets, see Section 12.8.5, “The binary Collation Compared to _bin Collations”.

• Collation names for Unicode character sets may include a version number to indicate the version of

the Unicode Collation Algorithm (UCA) on which the collation is based. UCA-based collations without
a version number in the name use the version-4.0.0 UCA weight keys. For example:

• utf8mb4_0900_ai_ci is based on UCA 9.0.0 weight keys (http://www.unicode.org/Public/

UCA/9.0.0/allkeys.txt).

• utf8mb4_unicode_520_ci is based on UCA 5.2.0 weight keys (http://www.unicode.org/Public/

UCA/5.2.0/allkeys.txt).

• utf8mb4_unicode_ci (with no version named) is based on UCA 4.0.0 weight keys (http://

www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt).

• For Unicode character sets, the xxx_general_mysql500_ci collations preserve the pre-5.1.24
ordering of the original xxx_general_ci collations and permit upgrades for tables created before
MySQL 5.1.24 (Bug #27877).

12.3.2 Server Character Set and Collation

MySQL Server has a server character set and a server collation. By default, these are utf8mb4 and
utf8mb4_0900_ai_ci, but they can be set explicitly at server startup on the command line or in an
option file and changed at runtime.

Initially, the server character set and collation depend on the options that you use when you start
mysqld. You can use --character-set-server for the character set. Along with it, you can
add --collation-server for the collation. If you don't specify a character set, that is the same
as saying --character-set-server=utf8mb4. If you specify only a character set (for example,
utf8mb4) but not a collation, that is the same as saying --character-set-server=utf8mb4

1935

Database Character Set and Collation

--collation-server=utf8mb4_0900_ai_ci because utf8mb4_0900_ai_ci is the default
collation for utf8mb4. Therefore, the following three commands all have the same effect:

mysqld
mysqld --character-set-server=utf8mb4
mysqld --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_0900_ai_ci

One way to change the settings is by recompiling. To change the default server character set and
collation when building from sources, use the DEFAULT_CHARSET and DEFAULT_COLLATION options
for CMake. For example:

cmake . -DDEFAULT_CHARSET=latin1

Or:

cmake . -DDEFAULT_CHARSET=latin1 \
  -DDEFAULT_COLLATION=latin1_german1_ci

Both mysqld and CMake verify that the character set/collation combination is valid. If not, each
program displays an error message and terminates.

The server character set and collation are used as default values if the database character set and
collation are not specified in CREATE DATABASE statements. They have no other purpose.

The current server character set and collation can be determined from the values of the
character_set_server and collation_server system variables. These variables can be
changed at runtime.

12.3.3 Database Character Set and Collation

Every database has a database character set and a database collation. The CREATE DATABASE and
ALTER DATABASE statements have optional clauses for specifying the database character set and
collation:

CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

The keyword SCHEMA can be used instead of DATABASE.

The CHARACTER SET and COLLATE clauses make it possible to create databases with different
character sets and collations on the same MySQL server.

Database options are stored in the data dictionary and can be examined by checking the Information
Schema SCHEMATA table.

Example:

CREATE DATABASE db_name CHARACTER SET latin1 COLLATE latin1_swedish_ci;

MySQL chooses the database character set and database collation in the following manner:

• If both CHARACTER SET charset_name and COLLATE collation_name are specified,

character set charset_name and collation collation_name are used.

• If CHARACTER SET charset_name is specified without COLLATE, character set charset_name
and its default collation are used. To see the default collation for each character set, use the SHOW
CHARACTER SET statement or query the INFORMATION_SCHEMA CHARACTER_SETS table.

• If COLLATE collation_name is specified without CHARACTER SET, the character set associated

with collation_name and collation collation_name are used.

1936

Table Character Set and Collation

• Otherwise (neither CHARACTER SET nor COLLATE is specified), the server character set and server

collation are used.

The character set and collation for the default database can be determined from the values of the
character_set_database and collation_database system variables. The server sets these
variables whenever the default database changes. If there is no default database, the variables have
the same value as the corresponding server-level system variables, character_set_server and
collation_server.

To see the default character set and collation for a given database, use these statements:

USE db_name;
SELECT @@character_set_database, @@collation_database;

Alternatively, to display the values without changing the default database:

SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';

The database character set and collation affect these aspects of server operation:

• For CREATE TABLE statements, the database character set and collation are used as default values
for table definitions if the table character set and collation are not specified. To override this, provide
explicit CHARACTER SET and COLLATE table options.

• For LOAD DATA statements that include no CHARACTER SET clause, the server uses the character
set indicated by the character_set_database system variable to interpret the information in the
file. To override this, provide an explicit CHARACTER SET clause.

• For stored routines (procedures and functions), the database character set and collation in effect at
routine creation time are used as the character set and collation of character data parameters for
which the declaration includes no CHARACTER SET or a COLLATE attribute. To override this, provide
CHARACTER SET and COLLATE explicitly.

12.3.4 Table Character Set and Collation

Every table has a table character set and a table collation. The CREATE TABLE and ALTER TABLE
statements have optional clauses for specifying the table character set and collation:

CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]

Example:

CREATE TABLE t1 ( ... )
CHARACTER SET latin1 COLLATE latin1_danish_ci;

MySQL chooses the table character set and collation in the following manner:

• If both CHARACTER SET charset_name and COLLATE collation_name are specified,

character set charset_name and collation collation_name are used.

• If CHARACTER SET charset_name is specified without COLLATE, character set charset_name
and its default collation are used. To see the default collation for each character set, use the SHOW
CHARACTER SET statement or query the INFORMATION_SCHEMA CHARACTER_SETS table.

• If COLLATE collation_name is specified without CHARACTER SET, the character set associated

with collation_name and collation collation_name are used.

• Otherwise (neither CHARACTER SET nor COLLATE is specified), the database character set and

collation are used.

1937

Column Character Set and Collation

The table character set and collation are used as default values for column definitions if the column
character set and collation are not specified in individual column definitions. The table character set
and collation are MySQL extensions; there are no such things in standard SQL.

12.3.5 Column Character Set and Collation

Every “character” column (that is, a column of type CHAR, VARCHAR, a TEXT type, or any synonym)
has a column character set and a column collation. Column definition syntax for CREATE TABLE and
ALTER TABLE has optional clauses for specifying the column character set and collation:

col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

These clauses can also be used for ENUM and SET columns:

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

Examples:

CREATE TABLE t1
(
    col1 VARCHAR(5)
      CHARACTER SET latin1
      COLLATE latin1_german1_ci
);

ALTER TABLE t1 MODIFY
    col1 VARCHAR(5)
      CHARACTER SET latin1
      COLLATE latin1_swedish_ci;

MySQL chooses the column character set and collation in the following manner:

• If both CHARACTER SET charset_name and COLLATE collation_name are specified,

character set charset_name and collation collation_name are used.

CREATE TABLE t1
(
    col1 CHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) CHARACTER SET latin1 COLLATE latin1_bin;

The character set and collation are specified for the column, so they are used. The column has
character set utf8mb4 and collation utf8mb4_unicode_ci.

• If CHARACTER SET charset_name is specified without COLLATE, character set charset_name

and its default collation are used.

CREATE TABLE t1
(
    col1 CHAR(10) CHARACTER SET utf8mb4
) CHARACTER SET latin1 COLLATE latin1_bin;

The character set is specified for the column, but the collation is not. The column has character
set utf8mb4 and the default collation for utf8mb4, which is utf8mb4_0900_ai_ci. To see the
default collation for each character set, use the SHOW CHARACTER SET statement or query the
INFORMATION_SCHEMA CHARACTER_SETS table.

• If COLLATE collation_name is specified without CHARACTER SET, the character set associated

with collation_name and collation collation_name are used.

CREATE TABLE t1
(
    col1 CHAR(10) COLLATE utf8mb4_polish_ci

1938

Character String Literal Character Set and Collation

) CHARACTER SET latin1 COLLATE latin1_bin;

The collation is specified for the column, but the character set is not. The column has collation
utf8mb4_polish_ci and the character set is the one associated with the collation, which is
utf8mb4.

• Otherwise (neither CHARACTER SET nor COLLATE is specified), the table character set and collation

are used.

CREATE TABLE t1
(
    col1 CHAR(10)
) CHARACTER SET latin1 COLLATE latin1_bin;

Neither the character set nor collation is specified for the column, so the table defaults are used. The
column has character set latin1 and collation latin1_bin.

The CHARACTER SET and COLLATE clauses are standard SQL.

If you use ALTER TABLE to convert a column from one character set to another, MySQL attempts to
map the data values, but if the character sets are incompatible, there may be data loss.

12.3.6 Character String Literal Character Set and Collation

Every character string literal has a character set and a collation.

For the simple statement SELECT 'string', the string has the connection default character set
and collation defined by the character_set_connection and collation_connection system
variables.

A character string literal may have an optional character set introducer and COLLATE clause, to
designate it as a string that uses a particular character set and collation:

[_charset_name]'string' [COLLATE collation_name]

The _charset_name expression is formally called an introducer. It tells the parser, “the string that
follows uses character set charset_name.” An introducer does not change the string to the introducer
character set like CONVERT() would do. It does not change the string value, although padding may
occur. The introducer is just a signal. See Section 12.3.8, “Character Set Introducers”.

Examples:

SELECT 'abc';
SELECT _latin1'abc';
SELECT _binary'abc';
SELECT _utf8mb4'abc' COLLATE utf8mb4_danish_ci;

Character set introducers and the COLLATE clause are implemented according to standard SQL
specifications.

MySQL determines the character set and collation of a character string literal in the following manner:

• If both _charset_name and COLLATE collation_name are specified, character set

charset_name and collation collation_name are used. collation_name must be a permitted
collation for charset_name.

• If _charset_name is specified but COLLATE is not specified, character set charset_name and
its default collation are used. To see the default collation for each character set, use the SHOW
CHARACTER SET statement or query the INFORMATION_SCHEMA CHARACTER_SETS table.

• If _charset_name is not specified but COLLATE collation_name is specified, the connection
default character set given by the character_set_connection system variable and collation
collation_name are used. collation_name must be a permitted collation for the connection
default character set.

1939

Character String Literal Character Set and Collation

• Otherwise (neither _charset_name nor COLLATE collation_name is specified), the

connection default character set and collation given by the character_set_connection and
collation_connection system variables are used.

Examples:

• A nonbinary string with latin1 character set and latin1_german1_ci collation:

SELECT _latin1'Müller' COLLATE latin1_german1_ci;

• A nonbinary string with utf8mb4 character set and its default collation (that is,

utf8mb4_0900_ai_ci):

SELECT _utf8mb4'Müller';

• A binary string with binary character set and its default collation (that is, binary):

SELECT _binary'Müller';

• A nonbinary string with the connection default character set and utf8mb4_0900_ai_ci collation

(fails if the connection character set is not utf8mb4):

SELECT 'Müller' COLLATE utf8mb4_0900_ai_ci;

• A string with the connection default character set and collation:

SELECT 'Müller';

An introducer indicates the character set for the following string, but does not change how the parser
performs escape processing within the string. Escapes are always interpreted by the parser according
to the character set given by character_set_connection.

The following examples show that escape processing occurs using character_set_connection
even in the presence of an introducer. The examples use SET NAMES (which changes
character_set_connection, as discussed in Section 12.4, “Connection Character Sets and
Collations”), and display the resulting strings using the HEX() function so that the exact string contents
can be seen.

Example 1:

mysql> SET NAMES latin1;
mysql> SELECT HEX('à\n'), HEX(_sjis'à\n');
+------------+-----------------+
| HEX('à\n')  | HEX(_sjis'à\n')  |
+------------+-----------------+
| E00A       | E00A            |
+------------+-----------------+

Here, à (hexadecimal value E0) is followed by \n, the escape sequence for newline. The escape
sequence is interpreted using the character_set_connection value of latin1 to produce a
literal newline (hexadecimal value 0A). This happens even for the second string. That is, the _sjis
introducer does not affect the parser's escape processing.

Example 2:

mysql> SET NAMES sjis;
mysql> SELECT HEX('à\n'), HEX(_latin1'à\n');
+------------+-------------------+
| HEX('à\n')  | HEX(_latin1'à\n')  |
+------------+-------------------+
| E05C6E     | E05C6E            |
+------------+-------------------+

Here, character_set_connection is sjis, a character set in which the sequence of à followed by
\ (hexadecimal values 05 and 5C) is a valid multibyte character. Hence, the first two bytes of the string
are interpreted as a single sjis character, and the \ is not interpreted as an escape character. The

1940

The National Character Set

following n (hexadecimal value 6E) is not interpreted as part of an escape sequence. This is true even
for the second string; the _latin1 introducer does not affect escape processing.

12.3.7 The National Character Set

Standard SQL defines NCHAR or NATIONAL CHAR as a way to indicate that a CHAR column should
use some predefined character set. MySQL uses utf8 as this predefined character set. For example,
these data type declarations are equivalent:

CHAR(10) CHARACTER SET utf8
NATIONAL CHARACTER(10)
NCHAR(10)

As are these:

VARCHAR(10) CHARACTER SET utf8
NATIONAL VARCHAR(10)
NVARCHAR(10)
NCHAR VARCHAR(10)
NATIONAL CHARACTER VARYING(10)
NATIONAL CHAR VARYING(10)

You can use N'literal' (or n'literal') to create a string in the national character set. These
statements are equivalent:

SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';

MySQL 8.4 interprets the national character set as utf8mb3, which is now deprecated. Thus, using
NATIONAL CHARACTER or one of its synonyms to define the character set for a database, table, or
column raises a warning similar to this one:

NATIONAL/NCHAR/NVARCHAR implies the character set UTF8MB3, which will be
replaced by UTF8MB4 in a future release. Please consider using CHAR(x) CHARACTER
SET UTF8MB4 in order to be unambiguous.

12.3.8 Character Set Introducers

A character string literal, hexadecimal literal, or bit-value literal may have an optional character set
introducer and COLLATE clause, to designate it as a string that uses a particular character set and
collation:

[_charset_name] literal [COLLATE collation_name]

The _charset_name expression is formally called an introducer. It tells the parser, “the string that
follows uses character set charset_name.” An introducer does not change the string to the introducer
character set like CONVERT() would do. It does not change the string value, although padding may
occur. The introducer is just a signal.

For character string literals, space between the introducer and the string is permitted but optional.

For character set literals, an introducer indicates the character set for the following string, but does not
change how the parser performs escape processing within the string. Escapes are always interpreted
by the parser according to the character set given by character_set_connection. For additional
discussion and examples, see Section 12.3.6, “Character String Literal Character Set and Collation”.

Examples:

SELECT 'abc';
SELECT _latin1'abc';
SELECT _binary'abc';
SELECT _utf8mb4'abc' COLLATE utf8mb4_danish_ci;

SELECT _latin1 X'4D7953514C';
SELECT _utf8mb4 0x4D7953514C COLLATE utf8mb4_danish_ci;

1941

Character Set Introducers

SELECT _latin1 b'1000001';
SELECT _utf8mb4 0b1000001 COLLATE utf8mb4_danish_ci;

Character set introducers and the COLLATE clause are implemented according to standard SQL
specifications.

Character string literals can be designated as binary strings by using the _binary introducer.
Hexadecimal literals and bit-value literals are binary strings by default, so _binary is permitted, but
normally unnecessary. _binary may be useful to preserve a hexadecimal or bit literal as a binary
string in contexts for which the literal is otherwise treated as a number. For example, bit operations
permit numeric or binary string arguments in MySQL 8.4 and higher, but treat hexadecimal and
bit literals as numbers by default. To explicitly specify binary string context for such literals, use a
_binary introducer for at least one of the arguments:

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

MySQL determines the character set and collation of a character string literal, hexadecimal literal, or
bit-value literal in the following manner:

• If both _charset_name and COLLATE collation_name are specified, character set

charset_name and collation collation_name are used. collation_name must be a permitted
collation for charset_name.

• If _charset_name is specified but COLLATE is not specified, character set charset_name and
its default collation are used. To see the default collation for each character set, use the SHOW
CHARACTER SET statement or query the INFORMATION_SCHEMA CHARACTER_SETS table.

• If _charset_name is not specified but COLLATE collation_name is specified:

• For a character string literal, the connection default character set given by the

character_set_connection system variable and collation collation_name are used.
collation_name must be a permitted collation for the connection default character set.

• For a hexadecimal literal or bit-value literal, the only permitted collation is binary because these

types of literals are binary strings by default.

• Otherwise (neither _charset_name nor COLLATE collation_name is specified):

• For a character string literal, the connection default character set and collation given by the

character_set_connection and collation_connection system variables are used.

• For a hexadecimal literal or bit-value literal, the character set and collation are binary.

Examples:

• Nonbinary strings with latin1 character set and latin1_german1_ci collation:

SELECT _latin1'Müller' COLLATE latin1_german1_ci;
SELECT _latin1 X'0A0D' COLLATE latin1_german1_ci;
SELECT _latin1 b'0110' COLLATE latin1_german1_ci;

• Nonbinary strings with utf8mb4 character set and its default collation (that is,

utf8mb4_0900_ai_ci):

1942

Examples of Character Set and Collation Assignment

SELECT _utf8mb4'Müller';
SELECT _utf8mb4 X'0A0D';
SELECT _utf8mb4 b'0110';

• Binary strings with binary character set and its default collation (that is, binary):

SELECT _binary'Müller';
SELECT X'0A0D';
SELECT b'0110';

The hexadecimal literal and bit-value literal need no introducer because they are binary strings by
default.

• A nonbinary string with the connection default character set and utf8mb4_0900_ai_ci collation

(fails if the connection character set is not utf8mb4):

SELECT 'Müller' COLLATE utf8mb4_0900_ai_ci;

This construction (COLLATE only) does not work for hexadecimal literals or bit literals because their
character set is binary no matter the connection character set, and binary is not compatible with
the utf8mb4_0900_ai_ci collation. The only permitted COLLATE clause in the absence of an
introducer is COLLATE binary.

• A string with the connection default character set and collation:

SELECT 'Müller';

12.3.9 Examples of Character Set and Collation Assignment

The following examples show how MySQL determines default character set and collation values.

Example 1: Table and Column Definition

CREATE TABLE t1
(
    c1 CHAR(10) CHARACTER SET latin1 COLLATE latin1_german1_ci
) DEFAULT CHARACTER SET latin2 COLLATE latin2_bin;

Here we have a column with a latin1 character set and a latin1_german1_ci collation. The
definition is explicit, so that is straightforward. Notice that there is no problem with storing a latin1
column in a latin2 table.

Example 2: Table and Column Definition

CREATE TABLE t1
(
    c1 CHAR(10) CHARACTER SET latin1
) DEFAULT CHARACTER SET latin1 COLLATE latin1_danish_ci;

This time we have a column with a latin1 character set and a default collation. Although it
might seem natural, the default collation is not taken from the table level. Instead, because the
default collation for latin1 is always latin1_swedish_ci, column c1 has a collation of
latin1_swedish_ci (not latin1_danish_ci).

Example 3: Table and Column Definition

CREATE TABLE t1
(
    c1 CHAR(10)
) DEFAULT CHARACTER SET latin1 COLLATE latin1_danish_ci;

We have a column with a default character set and a default collation. In this circumstance, MySQL
checks the table level to determine the column character set and collation. Consequently, the character
set for column c1 is latin1 and its collation is latin1_danish_ci.

Example 4: Database, Table, and Column Definition

1943

Compatibility with Other DBMSs

CREATE DATABASE d1
    DEFAULT CHARACTER SET latin2 COLLATE latin2_czech_cs;
USE d1;
CREATE TABLE t1
(
    c1 CHAR(10)
);

We create a column without specifying its character set and collation. We're also not specifying a
character set and a collation at the table level. In this circumstance, MySQL checks the database
level to determine the table settings, which thereafter become the column settings.) Consequently, the
character set for column c1 is latin2 and its collation is latin2_czech_cs.

12.3.10 Compatibility with Other DBMSs

For MaxDB compatibility these two statements are the same:

CREATE TABLE t1 (f1 CHAR(N) UNICODE);
CREATE TABLE t1 (f1 CHAR(N) CHARACTER SET ucs2);

Both the UNICODE attribute and the ucs2 character set are deprecated; you should expect them to be
removed in a future version of MySQL.

12.4 Connection Character Sets and Collations

A “connection” is what a client program makes when it connects to the server, to begin a session within
which it interacts with the server. The client sends SQL statements, such as queries, over the session
connection. The server sends responses, such as result sets or error messages, over the connection
back to the client.

• Connection Character Set and Collation System Variables

• Impermissible Client Character Sets

• Client Program Connection Character Set Configuration

• SQL Statements for Connection Character Set Configuration

• Connection Character Set Error Handling

Connection Character Set and Collation System Variables

Several character set and collation system variables relate to a client's interaction with the server.
Some of these have been mentioned in earlier sections:

• The character_set_server and collation_server system variables indicate the server

character set and collation. See Section 12.3.2, “Server Character Set and Collation”.

• The character_set_database and collation_database system variables indicate the

character set and collation of the default database. See Section 12.3.3, “Database Character Set and
Collation”.

Additional character set and collation system variables are involved in handling traffic for the
connection between a client and the server. Every client has session-specific connection-related
character set and collation system variables. These session system variable values are initialized at
connect time, but can be changed within the session.

Several questions about character set and collation handling for client connections can be answered in
terms of system variables:

• What character set are statements in when they leave the client?

The server takes the character_set_client system variable to be the character set in which
statements are sent by the client.

1944

Impermissible Client Character Sets

Note

Some character sets cannot be used as the client character set. See
Impermissible Client Character Sets.

• What character set should the server translate statements to after receiving them?

To determine this, the server uses the character_set_connection and
collation_connection system variables:

• The server converts statements sent by the client from character_set_client to

character_set_connection. Exception: For string literals that have an introducer such
as _utf8mb4 or _latin2, the introducer determines the character set. See Section 12.3.8,
“Character Set Introducers”.

• collation_connection is important for comparisons of literal strings. For comparisons of

strings with column values, collation_connection does not matter because columns have
their own collation, which has a higher collation precedence (see Section 12.8.4, “Collation
Coercibility in Expressions”).

• What character set should the server translate query results to before shipping them back to the

client?

The character_set_results system variable indicates the character set in which the server
returns query results to the client. This includes result data such as column values, result metadata
such as column names, and error messages.

To tell the server to perform no conversion of result sets or error messages, set
character_set_results to NULL or binary:

SET character_set_results = NULL;
SET character_set_results = binary;

For more information about character sets and error messages, see Section 12.6, “Error Message
Character Set”.

To see the values of the character set and collation system variables that apply to the current session,
use this statement:

SELECT * FROM performance_schema.session_variables
WHERE VARIABLE_NAME IN (
  'character_set_client', 'character_set_connection',
  'character_set_results', 'collation_connection'
) ORDER BY VARIABLE_NAME;

The following simpler statements also display the connection variables, but include other related
variables as well. They can be useful to see all character set and collation system variables:

SHOW SESSION VARIABLES LIKE 'character\_set\_%';
SHOW SESSION VARIABLES LIKE 'collation\_%';

Clients can fine-tune the settings for these variables, or depend on the defaults (in which case, you can
skip the rest of this section). If you do not use the defaults, you must change the character settings for
each connection to the server.

Impermissible Client Character Sets

The character_set_client system variable cannot be set to certain character sets:

ucs2
utf16
utf16le
utf32

1945

Connection Character Set Error Handling

character_set_connection = @@character_set_database). It is unnecessary to set
character_set_connection explicitly.

Note

Some character sets cannot be used as the client character set. Attempting to
use them with SET NAMES or SET CHARACTER SET produces an error. See
Impermissible Client Character Sets.

Example: Suppose that column1 is defined as CHAR(5) CHARACTER SET latin2. If you do not say
SET NAMES or SET CHARACTER SET, then for SELECT column1 FROM t, the server sends back
all the values for column1 using the character set that the client specified when it connected. On the
other hand, if you say SET NAMES 'latin1' or SET CHARACTER SET 'latin1' before issuing
the SELECT statement, the server converts the latin2 values to latin1 just before sending results
back. Conversion may be lossy for characters that are not in both character sets.

Connection Character Set Error Handling

Attempts to use an inappropriate connection character set or collation can produce an error, or cause
the server to fall back to its default character set and collation for a given connection. This section
describes problems that can occur when configuring the connection character set. These problems
can occur when establishing a connection or when changing the character set within an established
connection.

• Connect-Time Error Handling

• Runtime Error Handling

Connect-Time Error Handling

Some character sets cannot be used as the client character set; see Impermissible Client Character
Sets. If you specify a character set that is valid but not permitted as a client character set, the server
returns an error:

$> mysql --default-character-set=ucs2
ERROR 1231 (42000): Variable 'character_set_client' can't be set to
the value of 'ucs2'

If you specify a character set that the client does not recognize, it produces an error:

$> mysql --default-character-set=bogus
mysql: Character set 'bogus' is not a compiled character set and is
not specified in the '/usr/local/mysql/share/charsets/Index.xml' file
ERROR 2019 (HY000): Can't initialize character set bogus
(path: /usr/local/mysql/share/charsets/)

If you specify a character set that the client recognizes but the server does not, the server falls back
to its default character set and collation. Suppose that the server is configured to use latin1 and
latin1_swedish_ci as its defaults, and that it does not recognize gb18030 as a valid character set.
A client that specifies --default-character-set=gb18030 is able to connect to the server, but
the resulting character set is not what the client wants:

mysql> SHOW SESSION VARIABLES LIKE 'character\_set\_%';
+--------------------------+--------+
| Variable_name            | Value  |
+--------------------------+--------+
| character_set_client     | latin1 |
| character_set_connection | latin1 |
...
| character_set_results    | latin1 |
...
+--------------------------+--------+
mysql> SHOW SESSION VARIABLES LIKE 'collation_connection';
+----------------------+-------------------+
| Variable_name        | Value             |
+----------------------+-------------------+

1948

Configuring Application Character Set and Collation

| collation_connection | latin1_swedish_ci |
+----------------------+-------------------+

You can see that the connection system variables have been set to reflect a character set and collation
of latin1 and latin1_swedish_ci. This occurs because the server cannot satisfy the client
character set request and falls back to its defaults.

In this case, the client cannot use the character set that it wants because the server does not support
it. The client must either be willing to use a different character set, or connect to a different server that
supports the desired character set.

The same problem occurs when the client tells the server to use a character set that the server
recognizes, but the default collation for that character set on the client side is not known on the server
side.

Runtime Error Handling

Within an established connection, the client can request a change of connection character set and
collation with SET NAMES or SET CHARACTER SET.

Some character sets cannot be used as the client character set; see Impermissible Client Character
Sets. If you specify a character set that is valid but not permitted as a client character set, the server
returns an error:

mysql> SET NAMES 'ucs2';
ERROR 1231 (42000): Variable 'character_set_client' can't be set to
the value of 'ucs2'

If the server does not recognize the character set (or the collation), it produces an error:

mysql> SET NAMES 'bogus';
ERROR 1115 (42000): Unknown character set: 'bogus'

mysql> SET NAMES 'utf8mb4' COLLATE 'bogus';
ERROR 1273 (HY000): Unknown collation: 'bogus'

Tip

A client that wants to verify whether its requested character set was honored by
the server can execute the following statement after connecting and checking
that the result is the expected character set:

SELECT @@character_set_client;

12.5 Configuring Application Character Set and Collation

For applications that store data using the default MySQL character set and collation (utf8mb4,
utf8mb4_0900_ai_ci), no special configuration should be needed. If applications require data
storage using a different character set or collation, you can configure character set information several
ways:

• Specify character settings per database. For example, applications that use one database might use

the default of utf8mb4, whereas applications that use another database might use sjis.

• Specify character settings at server startup. This causes the server to use the given settings for all

applications that do not make other arrangements.

• Specify character settings at configuration time, if you build MySQL from source. This causes the

server to use the given settings as the defaults for all applications, without having to specify them at
server startup.

When different applications require different character settings, the per-database technique provides
a good deal of flexibility. If most or all applications use the same character set, specifying character
settings at server startup or configuration time may be most convenient.

1949

Configuring Application Character Set and Collation

For the per-database or server-startup techniques, the settings control the character set for
data storage. Applications must also tell the server which character set to use for client/server
communications, as described in the following instructions.

The examples shown here assume use of the latin1 character set and latin1_swedish_ci
collation in particular contexts as an alternative to the defaults of utf8mb4 and
utf8mb4_0900_ai_ci.

• Specify character settings per database.

 To create a database such that its tables use a given

default character set and collation for data storage, use a CREATE DATABASE statement like this:

CREATE DATABASE mydb
  CHARACTER SET latin1
  COLLATE latin1_swedish_ci;

Tables created in the database use latin1 and latin1_swedish_ci by default for any character
columns.

Applications that use the database should also configure their connection to the server each time
they connect. This can be done by executing a SET NAMES 'latin1' statement after connecting.
The statement can be used regardless of connection method (the mysql client, PHP scripts, and so
forth).

In some cases, it may be possible to configure the connection to use the desired character set some
other way. For example, to connect using mysql, you can specify the --default-character-
set=latin1 command-line option to achieve the same effect as SET NAMES 'latin1'.

For more information about configuring client connections, see Section 12.4, “Connection Character
Sets and Collations”.

Note

If you use ALTER DATABASE to change the database default character set
or collation, existing stored routines in the database that use those defaults
must be dropped and recreated so that they use the new defaults. (In a stored
routine, variables with character data types use the database defaults if the
character set or collation are not specified explicitly. See Section 15.1.17,
“CREATE PROCEDURE and CREATE FUNCTION Statements”.)

• Specify character settings at server startup.

 To select a character set and collation at server

startup, use the --character-set-server and --collation-server options. For example, to
specify the options in an option file, include these lines:

[mysqld]
character-set-server=latin1
collation-server=latin1_swedish_ci

These settings apply server-wide and apply as the defaults for databases created by any application,
and for tables created in those databases.

It is still necessary for applications to configure their connection using SET NAMES or equivalent
after they connect, as described previously. You might be tempted to start the server with the
--init_connect="SET NAMES 'latin1'" option to cause SET NAMES to be executed
automatically for each client that connects. However, this may yield inconsistent results because the
init_connect value is not executed for users who have the CONNECTION_ADMIN privilege (or the
deprecated SUPER privilege).

• Specify character settings at MySQL configuration time.

 To select a character set and

collation if you configure and build MySQL from source, use the DEFAULT_CHARSET and
DEFAULT_COLLATION CMake options:

cmake . -DDEFAULT_CHARSET=latin1 \

1950

Error Message Character Set

  -DDEFAULT_COLLATION=latin1_swedish_ci

The resulting server uses latin1 and latin1_swedish_ci as the default for databases and
tables and for client connections. It is unnecessary to use --character-set-server and
--collation-server to specify those defaults at server startup. It is also unnecessary for
applications to configure their connection using SET NAMES or equivalent after they connect to the
server.

Regardless of how you configure the MySQL character set for application use, you must also consider
the environment within which those applications execute. For example, if you intend to send statements
using UTF-8 text taken from a file that you create in an editor, you should edit the file with the locale
of your environment set to UTF-8 so that the file encoding is correct and so that the operating system
handles it correctly. If you use the mysql client from within a terminal window, the window must be
configured to use UTF-8 or characters may not display properly. For a script that executes in a Web
environment, the script must handle character encoding properly for its interaction with the MySQL
server, and it must generate pages that correctly indicate the encoding so that browsers know how to
display the content of the pages. For example, you can include this <meta> tag within your <head>
element:

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

12.6 Error Message Character Set

This section describes how the MySQL server uses character sets for constructing error messages. For
information about the language of error messages (rather than the character set), see Section 12.12,
“Setting the Error Message Language”. For general information about configuring error logging, see
Section 7.4.2, “The Error Log”.

• Character Set for Error Message Construction

• Character Set for Error Message Disposition

Character Set for Error Message Construction

The server constructs error messages as follows:

• The message template uses UTF-8 (utf8mb3).

• Parameters in the message template are replaced with values that apply to a specific error

occurrence:

• Identifiers such as table or column names use UTF-8 internally so they are copied as is.

• Character (nonbinary) string values are converted from their character set to UTF-8.

• Binary string values are copied as is for bytes in the range 0x20 to 0x7E, and using \x

hexadecimal encoding for bytes outside that range. For example, if a duplicate-key error occurs
for an attempt to insert 0x41CF9F into a VARBINARY unique column, the resulting error message
uses UTF-8 with some bytes hexadecimal encoded:

Duplicate entry 'A\xCF\x9F' for key 1

Character Set for Error Message Disposition

An error message, once constructed, can be written by the server to the error log or sent to clients:

• If the server writes the error message to the error log, it writes it in UTF-8, as constructed, without

conversion to another character set.

• If the server sends the error message to a client program, the server converts it from

UTF-8 to the character set specified by the character_set_results system variable. If

1951

Column Character Set Conversion

character_set_results has a value of NULL or binary, no conversion occurs. No conversion
occurs if the variable value is utf8mb3 or utf8mb4, either, because those character sets have a
repertoire that includes all UTF-8 characters used in message construction.

If characters cannot be represented in character_set_results, some encoding may occur
during the conversion. The encoding uses Unicode code point values:

• Characters in the Basic Multilingual Plane (BMP) range (0x0000 to 0xFFFF) are written using

\nnnn notation.

• Characters outside the BMP range (0x10000 to 0x10FFFF) are written using \+nnnnnn notation.

Clients can set character_set_results to control the character set in which they receive error
messages. The variable can be set directly, or indirectly by means such as SET NAMES. For more
information about character_set_results, see Section 12.4, “Connection Character Sets and
Collations”.

12.7 Column Character Set Conversion

To convert a binary or nonbinary string column to use a particular character set, use ALTER TABLE.
For successful conversion to occur, one of the following conditions must apply:

• If the column has a binary data type (BINARY, VARBINARY, BLOB), all the values that it contains

must be encoded using a single character set (the character set you're converting the column to). If
you use a binary column to store information in multiple character sets, MySQL has no way to know
which values use which character set and cannot convert the data properly.

• If the column has a nonbinary data type (CHAR, VARCHAR, TEXT), its contents should be encoded

in the column character set, not some other character set. If the contents are encoded in a different
character set, you can convert the column to use a binary data type first, and then to a nonbinary
column with the desired character set.

Suppose that a table t has a binary column named col1 defined as VARBINARY(50). Assuming that
the information in the column is encoded using a single character set, you can convert it to a nonbinary
column that has that character set. For example, if col1 contains binary data representing characters
in the greek character set, you can convert it as follows:

ALTER TABLE t MODIFY col1 VARCHAR(50) CHARACTER SET greek;

If your original column has a type of BINARY(50), you could convert it to CHAR(50), but the resulting
values are padded with 0x00 bytes at the end, which may be undesirable. To remove these bytes, use
the TRIM() function:

UPDATE t SET col1 = TRIM(TRAILING 0x00 FROM col1);

Suppose that table t has a nonbinary column named col1 defined as CHAR(50) CHARACTER SET
latin1 but you want to convert it to use utf8mb4 so that you can store values from many languages.
The following statement accomplishes this:

ALTER TABLE t MODIFY col1 CHAR(50) CHARACTER SET utf8mb4;

Conversion may be lossy if the column contains characters that are not in both character sets.

A special case occurs if you have old tables from before MySQL 4.1 where a nonbinary column
contains values that actually are encoded in a character set different from the server's default character
set. For example, an application might have stored sjis values in a column, even though MySQL's
default character set was different. It is possible to convert the column to use the proper character set
but an additional step is required. Suppose that the server's default character set was latin1 and
col1 is defined as CHAR(50) but its contents are sjis values. The first step is to convert the column
to a binary data type, which removes the existing character set information without performing any
character conversion:

1952

COLLATE Clause Precedence

FROM t1
WHERE _latin1 'Müller' COLLATE latin1_german2_ci = k;

SELECT *
FROM t1
WHERE k LIKE _latin1 'Müller' COLLATE latin1_german2_ci;

• With HAVING:

SELECT k
FROM t1
GROUP BY k
HAVING k = _latin1 'Müller' COLLATE latin1_german2_ci;

12.8.2 COLLATE Clause Precedence

The COLLATE clause has high precedence (higher than ||), so the following two expressions are
equivalent:

x || y COLLATE z
x || (y COLLATE z)

12.8.3 Character Set and Collation Compatibility

Each character set has one or more collations, but each collation is associated with one and only one
character set. Therefore, the following statement causes an error message because the latin2_bin
collation is not legal with the latin1 character set:

mysql> SELECT _latin1 'x' COLLATE latin2_bin;
ERROR 1253 (42000): COLLATION 'latin2_bin' is not valid
for CHARACTER SET 'latin1'

12.8.4 Collation Coercibility in Expressions

In the great majority of statements, it is obvious what collation MySQL uses to resolve a comparison
operation. For example, in the following cases, it should be clear that the collation is the collation of
column x:

SELECT x FROM T ORDER BY x;
SELECT x FROM T WHERE x = x;
SELECT DISTINCT x FROM T;

However, with multiple operands, there can be ambiguity. For example, this statement performs a
comparison between the column x and the string literal 'Y':

SELECT x FROM T WHERE x = 'Y';

If x and 'Y' have the same collation, there is no ambiguity about the collation to use for the
comparison. But if they have different collations, should the comparison use the collation of x, or of
'Y'? Both x and 'Y' have collations, so which collation takes precedence?

A mix of collations may also occur in contexts other than comparison. For example, a multiple-
argument concatenation operation such as CONCAT(x,'Y') combines its arguments to produce a
single string. What collation should the result have?

To resolve questions like these, MySQL checks whether the collation of one item can be coerced to the
collation of the other. MySQL assigns coercibility values as follows:

• An explicit COLLATE clause has a coercibility of 0 (not coercible at all).

• The concatenation of two strings with different collations has a coercibility of 1.

• The collation of a column or a stored routine parameter or local variable has a coercibility of 2.

1954

Collation Coercibility in Expressions

• A “system constant” (the string returned by functions such as USER() or VERSION()) has a

coercibility of 3.

• The collation of a literal has a coercibility of 4.

• The collation of a numeric or temporal value has a coercibility of 5.

• NULL or an expression that is derived from NULL has a coercibility of 6.

MySQL uses coercibility values with the following rules to resolve ambiguities:

• Use the collation with the lowest coercibility value.

• If both sides have the same coercibility, then:

• If both sides are Unicode, or both sides are not Unicode, it is an error.

• If one of the sides has a Unicode character set, and another side has a non-Unicode character set,
the side with Unicode character set wins, and automatic character set conversion is applied to the
non-Unicode side. For example, the following statement does not return an error:

SELECT CONCAT(utf8mb4_column, latin1_column) FROM t1;

It returns a result that has a character set of utf8mb4 and the same collation as
utf8mb4_column. Values of latin1_column are automatically converted to utf8mb4 before
concatenating.

• For an operation with operands from the same character set but that mix a _bin collation and
a _ci or _cs collation, the _bin collation is used. This is similar to how operations that mix
nonbinary and binary strings evaluate the operands as binary strings, applied to collations rather
than data types.

Although automatic conversion is not in the SQL standard, the standard does say that every character
set is (in terms of supported characters) a “subset” of Unicode. Because it is a well-known principle
that “what applies to a superset can apply to a subset,” we believe that a collation for Unicode can
apply for comparisons with non-Unicode strings. More generally, MySQL uses the concept of character
set repertoire, which can sometimes be used to determine subset relationships among character
sets and enable conversion of operands in operations that would otherwise produce an error. See
Section 12.2.1, “Character Set Repertoire”.

The following table illustrates some applications of the preceding rules.

Comparison

column1 = 'A'

Collation Used

Use collation of column1

column1 = 'A' COLLATE x

Use collation of 'A' COLLATE x

column1 COLLATE x = 'A' COLLATE y

Error

To determine the coercibility of a string expression, use the COERCIBILITY() function (see
Section 14.15, “Information Functions”):

mysql> SELECT COERCIBILITY(_utf8mb4'A' COLLATE utf8mb4_bin);
        -> 0
mysql> SELECT COERCIBILITY(VERSION());
        -> 3
mysql> SELECT COERCIBILITY('A');
        -> 4
mysql> SELECT COERCIBILITY(1000);
        -> 5
mysql> SELECT COERCIBILITY(NULL);
        -> 6

For implicit conversion of a numeric or temporal value to a string, such as occurs for the argument 1 in
the expression CONCAT(1, 'abc'), the result is a character (nonbinary) string that has a character

1955

The binary Collation Compared to _bin Collations

set and collation determined by the character_set_connection and collation_connection
system variables. See Section 14.3, “Type Conversion in Expression Evaluation”.

12.8.5 The binary Collation Compared to _bin Collations

This section describes how the binary collation for binary strings compares to _bin collations for
nonbinary strings.

Binary strings (as stored using the BINARY, VARBINARY, and BLOB data types) have a character set
and collation named binary. Binary strings are sequences of bytes and the numeric values of those
bytes determine comparison and sort order. See Section 12.10.8, “The Binary Character Set”.

Nonbinary strings (as stored using the CHAR, VARCHAR, and TEXT data types) have a character set
and collation other than binary. A given nonbinary character set can have several collations, each of
which defines a particular comparison and sort order for the characters in the set. For most character
sets, one of these is the binary collation, indicated by a _bin suffix in the collation name. For example,
the binary collations for latin1 and big5 are named latin1_bin and big5_bin, respectively.
utf8mb4 is an exception that has two binary collations, utf8mb4_bin and utf8mb4_0900_bin; see
Section 12.10.1, “Unicode Character Sets”.

The binary collation differs from _bin collations in several respects, discussed in the following
sections:

• The Unit for Comparison and Sorting

• Character Set Conversion

• Lettercase Conversion

• Trailing Space Handling in Comparisons

• Trailing Space Handling for Inserts and Retrievals

The Unit for Comparison and Sorting

Binary strings are sequences of bytes. For the binary collation, comparison and sorting are based
on numeric byte values. Nonbinary strings are sequences of characters, which might be multibyte.
Collations for nonbinary strings define an ordering of the character values for comparison and sorting.
For _bin collations, this ordering is based on numeric character code values, which is similar to
ordering for binary strings except that character code values might be multibyte.

Character Set Conversion

A nonbinary string has a character set and is automatically converted to another character set in many
cases, even when the string has a _bin collation:

• When assigning column values to another column that has a different character set:

UPDATE t1 SET utf8mb4_bin_column=latin1_column;
INSERT INTO t1 (latin1_column) SELECT utf8mb4_bin_column FROM t2;

• When assigning column values for INSERT or UPDATE using a string literal:

SET NAMES latin1;
INSERT INTO t1 (utf8mb4_bin_column) VALUES ('string-in-latin1');

• When sending results from the server to a client:

SET NAMES latin1;
SELECT utf8mb4_bin_column FROM t2;

For binary string columns, no conversion occurs. For cases similar to those preceding, the string value
is copied byte-wise.

1956

The binary Collation Compared to _bin Collations

Lettercase Conversion

Collations for nonbinary character sets provide information about lettercase of characters, so
characters in a nonbinary string can be converted from one lettercase to another, even for _bin
collations that ignore lettercase for ordering:

mysql> SET NAMES utf8mb4 COLLATE utf8mb4_bin;
mysql> SELECT LOWER('aA'), UPPER('zZ');
+-------------+-------------+
| LOWER('aA') | UPPER('zZ') |
+-------------+-------------+
| aa          | ZZ          |
+-------------+-------------+

The concept of lettercase does not apply to bytes in a binary string. To perform lettercase conversion,
the string must first be converted to a nonbinary string using a character set appropriate for the data
stored in the string:

mysql> SET NAMES binary;
mysql> SELECT LOWER('aA'), LOWER(CONVERT('aA' USING utf8mb4));
+-------------+------------------------------------+
| LOWER('aA') | LOWER(CONVERT('aA' USING utf8mb4)) |
+-------------+------------------------------------+
| aA          | aa                                 |
+-------------+------------------------------------+

Trailing Space Handling in Comparisons

MySQL collations have a pad attribute, which has a value of PAD SPACE or NO PAD:

• Most MySQL collations have a pad attribute of PAD SPACE.

• The Unicode collations based on UCA 9.0.0 and higher have a pad attribute of NO PAD; see

Section 12.10.1, “Unicode Character Sets”.

For nonbinary strings (CHAR, VARCHAR, and TEXT values), the string collation pad attribute determines
treatment in comparisons of trailing spaces at the end of strings:

• For PAD SPACE collations, trailing spaces are insignificant in comparisons; strings are compared

without regard to trailing spaces.

• NO PAD collations treat trailing spaces as significant in comparisons, like any other character.

The differing behaviors can be demonstrated using the two utf8mb4 binary collations, one of
which is PAD SPACE, the other of which is NO PAD. The example also shows how to use the
INFORMATION_SCHEMA COLLATIONS table to determine the pad attribute for collations.

mysql> SELECT COLLATION_NAME, PAD_ATTRIBUTE
       FROM INFORMATION_SCHEMA.COLLATIONS
       WHERE COLLATION_NAME LIKE 'utf8mb4%bin';
+------------------+---------------+
| COLLATION_NAME   | PAD_ATTRIBUTE |
+------------------+---------------+
| utf8mb4_bin      | PAD SPACE     |
| utf8mb4_0900_bin | NO PAD        |
+------------------+---------------+
mysql> SET NAMES utf8mb4 COLLATE utf8mb4_bin;
mysql> SELECT 'a ' = 'a';
+------------+
| 'a ' = 'a' |
+------------+
|          1 |
+------------+
mysql> SET NAMES utf8mb4 COLLATE utf8mb4_0900_bin;
mysql> SELECT 'a ' = 'a';
+------------+
| 'a ' = 'a' |

1957

Examples of the Effect of Collation

+------------+
|          0 |
+------------+

Note

“Comparison” in this context does not include the LIKE pattern-matching
operator, for which trailing spaces are significant, regardless of collation.

For binary strings (BINARY, VARBINARY, and BLOB values), all bytes are significant in comparisons,
including trailing spaces:

mysql> SET NAMES binary;
mysql> SELECT 'a ' = 'a';
+------------+
| 'a ' = 'a' |
+------------+
|          0 |
+------------+

Trailing Space Handling for Inserts and Retrievals

CHAR(N) columns store nonbinary strings N characters long. For inserts, values shorter than N
characters are extended with spaces. For retrievals, trailing spaces are removed.

BINARY(N) columns store binary strings N bytes long. For inserts, values shorter than N bytes are
extended with 0x00 bytes. For retrievals, nothing is removed; a value of the declared length is always
returned.

mysql> CREATE TABLE t1 (
         a CHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
         b BINARY(10)
       );
mysql> INSERT INTO t1 VALUES ('x','x');
mysql> INSERT INTO t1 VALUES ('x ','x ');
mysql> SELECT a, b, HEX(a), HEX(b) FROM t1;
+------+------------------------+--------+----------------------+
| a    | b                      | HEX(a) | HEX(b)               |
+------+------------------------+--------+----------------------+
| x    | 0x78000000000000000000 | 78     | 78000000000000000000 |
| x    | 0x78200000000000000000 | 78     | 78200000000000000000 |
+------+------------------------+--------+----------------------+

12.8.6 Examples of the Effect of Collation

Example 1: Sorting German Umlauts

Suppose that column X in table T has these latin1 column values:

Muffler
Müller
MX Systems
MySQL

Suppose also that the column values are retrieved using the following statement:

SELECT X FROM T ORDER BY X COLLATE collation_name;

The following table shows the resulting order of the values if we use ORDER BY with different collations.

latin1_swedish_ci

latin1_german1_ci

latin1_german2_ci

Muffler

MX Systems

Müller

MySQL

Muffler

Müller

MX Systems

MySQL

Müller

Muffler

MX Systems

MySQL

1958

Using Collation in INFORMATION_SCHEMA Searches

The character that causes the different sort orders in this example is ü (German “U-umlaut”).

• The first column shows the result of the SELECT using the Swedish/Finnish collating rule, which says

that U-umlaut sorts with Y.

• The second column shows the result of the SELECT using the German DIN-1 rule, which says that U-

umlaut sorts with U.

• The third column shows the result of the SELECT using the German DIN-2 rule, which says that U-

umlaut sorts with UE.

Example 2: Searching for German Umlauts

Suppose that you have three tables that differ only by the character set and collation used:

mysql> SET NAMES utf8mb4;
mysql> CREATE TABLE german1 (
         c CHAR(10)
       ) CHARACTER SET latin1 COLLATE latin1_german1_ci;
mysql> CREATE TABLE german2 (
         c CHAR(10)
       ) CHARACTER SET latin1 COLLATE latin1_german2_ci;
mysql> CREATE TABLE germanutf8 (
         c CHAR(10)
       ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Each table contains two records:

mysql> INSERT INTO german1 VALUES ('Bar'), ('Bär');
mysql> INSERT INTO german2 VALUES ('Bar'), ('Bär');
mysql> INSERT INTO germanutf8 VALUES ('Bar'), ('Bär');

Two of the above collations have an A = Ä equality, and one has no such equality
(latin1_german2_ci). For that reason, comparisons yield the results shown here:

mysql> SELECT * FROM german1 WHERE c = 'Bär';
+------+
| c    |
+------+
| Bar  |
| Bär  |
+------+
mysql> SELECT * FROM german2 WHERE c = 'Bär';
+------+
| c    |
+------+
| Bär  |
+------+
mysql> SELECT * FROM germanutf8 WHERE c = 'Bär';
+------+
| c    |
+------+
| Bar  |
| Bär  |
+------+

This is not a bug but rather a consequence of the sorting properties of latin1_german1_ci and
utf8mb4_unicode_ci (the sorting shown is done according to the German DIN 5007 standard).

12.8.7 Using Collation in INFORMATION_SCHEMA Searches

String columns in INFORMATION_SCHEMA tables have a collation of utf8mb3_general_ci, which is
case-insensitive. However, for values that correspond to objects that are represented in the file system,
such as databases and tables, searches in INFORMATION_SCHEMA string columns can be case-
sensitive or case-insensitive, depending on the characteristics of the underlying file system and the
lower_case_table_names system variable setting. For example, searches may be case-sensitive if
the file system is case-sensitive. This section describes this behavior and how to modify it if necessary.

1959

Using Collation in INFORMATION_SCHEMA Searches

Suppose that a query searches the SCHEMATA.SCHEMA_NAME column for the test database. On
Linux, file systems are case-sensitive, so comparisons of SCHEMATA.SCHEMA_NAME with 'test'
match, but comparisons with 'TEST' do not:

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME = 'test';
+-------------+
| SCHEMA_NAME |
+-------------+
| test        |
+-------------+

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME = 'TEST';
Empty set (0.00 sec)

These results occur with the lower_case_table_names system variable set to 0. A
lower_case_table_names setting of 1 or 2 causes the second query to return the same (nonempty)
result as the first query.

Note

It is prohibited to start the server with a lower_case_table_names setting
that is different from the setting used when the server was initialized.

On Windows or macOS, file systems are not case-sensitive, so comparisons match both 'test' and
'TEST':

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME = 'test';
+-------------+
| SCHEMA_NAME |
+-------------+
| test        |
+-------------+

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME = 'TEST';
+-------------+
| SCHEMA_NAME |
+-------------+
| TEST        |
+-------------+

The value of lower_case_table_names makes no difference in this context.

The preceding behavior occurs because the utf8mb3_general_ci collation is not used for
INFORMATION_SCHEMA queries when searching for values that correspond to objects represented in
the file system.

If the result of a string operation on an INFORMATION_SCHEMA column differs from expectations, a
workaround is to use an explicit COLLATE clause to force a suitable collation (see Section 12.8.1,
“Using COLLATE in SQL Statements”). For example, to perform a case-insensitive search, use
COLLATE with the INFORMATION_SCHEMA column name:

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME COLLATE utf8mb3_general_ci = 'test';
+-------------+
| SCHEMA_NAME |
+-------------+
| test        |
+-------------+

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME COLLATE utf8mb3_general_ci = 'TEST';
+-------------+
| SCHEMA_NAME |

1960

Unicode Support

+-------------+
| test        |
+-------------+

You can also use the UPPER() or LOWER() function:

WHERE UPPER(SCHEMA_NAME) = 'TEST'
WHERE LOWER(SCHEMA_NAME) = 'test'

Although a case-insensitive comparison can be performed even on platforms with case-sensitive
file systems, as just shown, it is not necessarily always the right thing to do. On such platforms, it is
possible to have multiple objects with names that differ only in lettercase. For example, tables named
city, CITY, and City can all exist simultaneously. Consider whether a search should match all
such names or just one and write queries accordingly. The first of the following comparisons (with
utf8mb3_bin) is case-sensitive; the others are not:

WHERE TABLE_NAME COLLATE utf8mb3_bin = 'City'
WHERE TABLE_NAME COLLATE utf8mb3_general_ci = 'city'
WHERE UPPER(TABLE_NAME) = 'CITY'
WHERE LOWER(TABLE_NAME) = 'city'

Searches in INFORMATION_SCHEMA string columns for values that refer to INFORMATION_SCHEMA
itself do use the utf8mb3_general_ci collation because INFORMATION_SCHEMA is
a “virtual” database not represented in the file system. For example, comparisons with
SCHEMATA.SCHEMA_NAME match 'information_schema' or 'INFORMATION_SCHEMA' regardless
of platform:

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME = 'information_schema';
+--------------------+
| SCHEMA_NAME        |
+--------------------+
| information_schema |
+--------------------+

mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
       WHERE SCHEMA_NAME = 'INFORMATION_SCHEMA';
+--------------------+
| SCHEMA_NAME        |
+--------------------+
| information_schema |
+--------------------+

12.9 Unicode Support

The Unicode Standard includes characters from the Basic Multilingual Plane (BMP) and supplementary
characters that lie outside the BMP. This section describes support for Unicode in MySQL. For
information about the Unicode Standard itself, visit the Unicode Consortium website.

BMP characters have these characteristics:

• Their code point values are between 0 and 65535 (or U+0000 and U+FFFF).

• They can be encoded in a variable-length encoding using 8, 16, or 24 bits (1 to 3 bytes).

• They can be encoded in a fixed-length encoding using 16 bits (2 bytes).

• They are sufficient for almost all characters in major languages.

Supplementary characters lie outside the BMP:

• Their code point values are between U+10000 and U+10FFFF).

• Unicode support for supplementary characters requires character sets that have a range outside

BMP characters and therefore take more space than BMP characters (up to 4 bytes per character).

1961

Unicode Support

The UTF-8 (Unicode Transformation Format with 8-bit units) method for encoding Unicode data is
implemented according to RFC 3629, which describes encoding sequences that take from one to four
bytes. The idea of UTF-8 is that various Unicode characters are encoded using byte sequences of
different lengths:

• Basic Latin letters, digits, and punctuation signs use one byte.

• Most European and Middle East script letters fit into a 2-byte sequence: extended Latin letters (with
tilde, macron, acute, grave and other accents), Cyrillic, Greek, Armenian, Hebrew, Arabic, Syriac,
and others.

• Korean, Chinese, and Japanese ideographs use 3-byte or 4-byte sequences.

MySQL supports these Unicode character sets:

• utf8mb4: A UTF-8 encoding of the Unicode character set using one to four bytes per character.

• utf8mb3: A UTF-8 encoding of the Unicode character set using one to three bytes per character.
This character set is deprecated andsubject to removal in a future release; use utf8mb4 instead.

• utf8: A deprecated alias for utf8mb3; use utf8mb4 instead.

Note

utf8 is expected in a future version of MySQL to become an alias for
utf8mb4.

• ucs2: The UCS-2 encoding of the Unicode character set using two bytes per character. Deprecated;

expect support for this character set to be removed in a future release.

• utf16: The UTF-16 encoding for the Unicode character set using two or four bytes per character.

Like ucs2 but with an extension for supplementary characters.

• utf16le: The UTF-16LE encoding for the Unicode character set. Like utf16 but little-endian rather

than big-endian.

• utf32: The UTF-32 encoding for the Unicode character set using four bytes per character.

Note

The utf8mb3 character set is deprecated and you should expect it to be
removed in a future MySQL release. Please use utf8mb4 instead. utf8 is
currently an alias for utf8mb3, but it is now deprecated as such, and utf8 is
expected subsequently to become a reference to utf8mb4. MySQL 8.4 also
displays utf8mb3 in place of utf8 in the columns of Information Schema
tables, and in the output of SQL SHOW statements.

In addition, you should be aware that collations using the utf8_ prefix in older
releases of MySQL have since been renamed using the prefix utf8mb3_,
instead.

To avoid ambiguity about the meaning of utf8, consider specifying utf8mb4
explicitly for character set references.

Table 12.2, “Unicode Character Set General Characteristics”, summarizes the general characteristics
of Unicode character sets supported by MySQL.

Table 12.2 Unicode Character Set General Characteristics

Character Set

Supported Characters

utf8mb3, utf8 (deprecated)

BMP only

Required Storage Per
Character

1, 2, or 3 bytes

1962

The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding)

Character Set

Supported Characters

Required Storage Per
Character

ucs2

utf8mb4

utf16

utf16le

utf32

BMP only

2 bytes

BMP and supplementary

1, 2, 3, or 4 bytes

BMP and supplementary

BMP and supplementary

2 or 4 bytes

2 or 4 bytes

BMP and supplementary

4 bytes

Characters outside the BMP compare as REPLACEMENT CHARACTER and convert to '?' when
converted to a Unicode character set that supports only BMP characters (utf8mb3 or ucs2).

If you use character sets that support supplementary characters and thus are “wider” than the BMP-
only utf8mb3 and ucs2 character sets, there are potential incompatibility issues for your applications;
see Section 12.9.8, “Converting Between 3-Byte and 4-Byte Unicode Character Sets”. That section
also describes how to convert tables from the (3-byte) utf8mb3 to the (4-byte) utf8mb4, and what
constraints may apply in doing so.

A similar set of collations is available for most Unicode character sets. For example, each has a
Danish collation, the names of which are utf8mb4_danish_ci, utf8mb3_danish_ci (deprecated),
utf8_danish_ci (deprecated), ucs2_danish_ci, utf16_danish_ci, and utf32_danish_ci.
The exception is utf16le, which has only two collations. For information about Unicode collations
and their differentiating properties, including collation properties for supplementary characters, see
Section 12.10.1, “Unicode Character Sets”.

The MySQL implementation of UCS-2, UTF-16, and UTF-32 stores characters in big-endian byte order
and does not use a byte order mark (BOM) at the beginning of values. Other database systems might
use little-endian byte order or a BOM. In such cases, conversion of values needs to be performed when
transferring data between those systems and MySQL. The implementation of UTF-16LE is little-endian.

MySQL uses no BOM for UTF-8 values.

Client applications that communicate with the server using Unicode should set the client character
set accordingly (for example, by issuing a SET NAMES 'utf8mb4' statement). Some character
sets cannot be used as the client character set. Attempting to use them with SET NAMES or SET
CHARACTER SET produces an error. See Impermissible Client Character Sets.

The following sections provide additional detail on the Unicode character sets in MySQL.

12.9.1 The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding)

The utf8mb4 character set has these characteristics:

• Supports BMP and supplementary characters.

• Requires a maximum of four bytes per multibyte character.

utf8mb4 contrasts with the utf8mb3 character set, which supports only BMP characters and uses a
maximum of three bytes per character:

• For a BMP character, utf8mb4 and utf8mb3 have identical storage characteristics: same code

values, same encoding, same length.

• For a supplementary character, utf8mb4 requires four bytes to store it, whereas utf8mb3 cannot

store the character at all. When converting utf8mb3 columns to utf8mb4, you need not worry about
converting supplementary characters because there are none.

utf8mb4 is a superset of utf8mb3, so for an operation such as the following concatenation, the result
has character set utf8mb4 and the collation of utf8mb4_col:

SELECT CONCAT(utf8mb3_col, utf8mb4_col);

1963

The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding)

Similarly, the following comparison in the WHERE clause works according to the collation of
utf8mb4_col:

SELECT * FROM utf8mb3_tbl, utf8mb4_tbl
WHERE utf8mb3_tbl.utf8mb3_col = utf8mb4_tbl.utf8mb4_col;

For information about data type storage as it relates to multibyte character sets, see String Type
Storage Requirements.

12.9.2 The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding)

The utf8mb3 character set has these characteristics:

• Supports BMP characters only (no support for supplementary characters)

• Requires a maximum of three bytes per multibyte character.

Applications that use UTF-8 data but require supplementary character support should use utf8mb4
rather than utf8mb3 (see Section 12.9.1, “The utf8mb4 Character Set (4-Byte UTF-8 Unicode
Encoding)”).

Exactly the same set of characters is available in utf8mb3 and ucs2. That is, they have the same
repertoire.

Note

The recommended character set for MySQL is utf8mb4. All new applications
should use utf8mb4.

The utf8mb3 character set is deprecated. utf8mb3 remains supported for the
lifetimes of the MySQL 8.0.x and MySQL 8.4.x LTS release series.

Expect utf8mb3 to be removed in a future major release of MySQL.

Since changing character sets can be a complex and time-consuming task,
you should begin to prepare for this change now by using utf8mb4 for new
applications. For guidance in converting existing applications which use utfmb3,
see Section 12.9.8, “Converting Between 3-Byte and 4-Byte Unicode Character
Sets”.

utf8mb3 can be used in CHARACTER SET clauses, and utf8mb3_collation_substring in
COLLATE clauses, where collation_substring is bin, czech_ci, danish_ci, esperanto_ci,
estonian_ci, and so forth. For example:

CREATE TABLE t (s1 CHAR(1)) CHARACTER SET utf8mb3;
SELECT * FROM t WHERE s1 COLLATE utf8mb3_general_ci = 'x';
DECLARE x VARCHAR(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_danish_ci;
SELECT CAST('a' AS CHAR CHARACTER SET utf8mb4) COLLATE utf8mb4_czech_ci;

In statements such as SHOW CREATE TABLE or SELECT CHARACTER_SET_NAME
FROM INFORMATION_SCHEMA.COLUMNS or SELECT COLLATION_NAME FROM
INFORMATION_SCHEMA.COLUMNS, character sets or collation names prefixed with utf8 or utf8_ are
displayed using utf8mb3 or utf8mb3_, respectively.

utf8mb3 is also valid (but deprecated) in contexts other than CHARACTER SET clauses. For example:

mysqld --character-set-server=utf8mb3

SET NAMES 'utf8mb3'; /* and other SET statements that have similar effect */
SELECT _utf8mb3 'a';

For information about data type storage as it relates to multibyte character sets, see String Type
Storage Requirements.

1964

The utf16le Character Set (UTF-16LE Unicode Encoding)

INSERT INTO t (ucs2_column) VALUES (0xd800); /* legal */
INSERT INTO t (utf16_column)VALUES (0xd800); /* illegal */

There is no validity check for characters that are technically valid but are not true Unicode (that is,
characters that Unicode considers to be “unassigned code points” or “private use” characters or even
“illegals” like 0xffff). For example, since U+F8FF is the Apple Logo, this is legal:

INSERT INTO t (utf16_column)VALUES (0xf8ff); /* legal */

Such characters cannot be expected to mean the same thing to everyone.

Because MySQL must allow for the worst case (that one character requires four bytes) the maximum
length of a utf16 column or index is only half of the maximum length for a ucs2 column or index. For
example, the maximum length of a MEMORY table index key is 3072 bytes, so these statements create
tables with the longest permitted indexes for ucs2 and utf16 columns:

CREATE TABLE tf (s1 VARCHAR(1536) CHARACTER SET ucs2) ENGINE=MEMORY;
CREATE INDEX i ON tf (s1);
CREATE TABLE tg (s1 VARCHAR(768) CHARACTER SET utf16) ENGINE=MEMORY;
CREATE INDEX i ON tg (s1);

12.9.6 The utf16le Character Set (UTF-16LE Unicode Encoding)

This is the same as utf16 but is little-endian rather than big-endian.

12.9.7 The utf32 Character Set (UTF-32 Unicode Encoding)

The utf32 character set is fixed length (like ucs2 and unlike utf16). utf32 uses 32 bits for every
character, unlike ucs2 (which uses 16 bits for every character), and unlike utf16 (which uses 16 bits
for some characters and 32 bits for others).

utf32 takes twice as much space as ucs2 and more space than utf16, but utf32 has the same
advantage as ucs2 that it is predictable for storage: The required number of bytes for utf32 equals
the number of characters times 4. Also, unlike utf16, there are no tricks for encoding in utf32, so the
stored value equals the code value.

To demonstrate how the latter advantage is useful, here is an example that shows how to determine a
utf8mb4 value given the utf32 code value:

/* Assume code value = 100cc LINEAR B WHEELED CHARIOT */
CREATE TABLE tmp (utf32_col CHAR(1) CHARACTER SET utf32,
                  utf8mb4_col CHAR(1) CHARACTER SET utf8mb4);
INSERT INTO tmp VALUES (0x000100cc,NULL);
UPDATE tmp SET utf8mb4_col = utf32_col;
SELECT HEX(utf32_col),HEX(utf8mb4_col) FROM tmp;

MySQL is very forgiving about additions of unassigned Unicode characters or private-use-area
characters. There is in fact only one validity check for utf32: No code value may be greater than
0x10ffff. For example, this is illegal:

INSERT INTO t (utf32_column) VALUES (0x110000); /* illegal */

12.9.8 Converting Between 3-Byte and 4-Byte Unicode Character Sets

This section describes issues that you may face when converting character data between the utf8mb3
and utf8mb4 character sets.

Note

This discussion focuses primarily on converting between utf8mb3 and
utf8mb4, but similar principles apply to converting between the ucs2 character
set and character sets such as utf16 or utf32.

The utf8mb3 and utf8mb4 character sets differ as follows:

1966

Converting Between 3-Byte and 4-Byte Unicode Character Sets

• utf8mb3 supports only characters in the Basic Multilingual Plane (BMP). utf8mb4 additionally

supports supplementary characters that lie outside the BMP.

• utf8mb3 uses a maximum of three bytes per character. utf8mb4 uses a maximum of four bytes per

character.

Note

This discussion refers to the utf8mb3 and utf8mb4 character set names to be
explicit about referring to 3-byte and 4-byte UTF-8 character set data.

One advantage of converting from utf8mb3 to utf8mb4 is that this enables applications to use
supplementary characters. One tradeoff is that this may increase data storage space requirements.

In terms of table content, conversion from utf8mb3 to utf8mb4 presents no problems:

• For a BMP character, utf8mb4 and utf8mb3 have identical storage characteristics: same code

values, same encoding, same length.

• For a supplementary character, utf8mb4 requires four bytes to store it, whereas utf8mb3 cannot

store the character at all. When converting utf8mb3 columns to utf8mb4, you need not worry about
converting supplementary characters because there are none.

In terms of table structure, these are the primary potential incompatibilities:

• For the variable-length character data types (VARCHAR and the TEXT types), the maximum permitted

length in characters is less for utf8mb4 columns than for utf8mb3 columns.

• For all character data types (CHAR, VARCHAR, and the TEXT types), the maximum number of
characters that can be indexed is less for utf8mb4 columns than for utf8mb3 columns.

Consequently, to convert tables from utf8mb3 to utf8mb4, it may be necessary to change some
column or index definitions.

Tables can be converted from utf8mb3 to utf8mb4 by using ALTER TABLE. Suppose that a table
has this definition:

CREATE TABLE t1 (
  col1 CHAR(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  col2 CHAR(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL
) CHARACTER SET utf8mb3;

The following statement converts t1 to use utf8mb4:

ALTER TABLE t1
  DEFAULT CHARACTER SET utf8mb4,
  MODIFY col1 CHAR(10)
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  MODIFY col2 CHAR(10)
    CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL;

The catch when converting from utf8mb3 to utf8mb4 is that the maximum length of a column or
index key is unchanged in terms of bytes. Therefore, it is smaller in terms of characters because the
maximum length of a character is four bytes instead of three. For the CHAR, VARCHAR, and TEXT data
types, watch for these issues when converting your MySQL tables:

• Check all definitions of utf8mb3 columns and make sure they do not exceed the maximum length

for the storage engine.

• Check all indexes on utf8mb3 columns and make sure they do not exceed the maximum length for
the storage engine. Sometimes the maximum can change due to storage engine enhancements.

If the preceding conditions apply, you must either reduce the defined length of columns or indexes, or
continue to use utf8mb3 rather than utf8mb4.

1967

Supported Character Sets and Collations

in the older server, as long as there are no 4-byte characters in the data. The older server sees utf8
in the dump file object definitions and create new objects that use the (3-byte) utf8 character set.

12.10 Supported Character Sets and Collations

This section indicates which character sets MySQL supports. There is one subsection for each group of
related character sets. For each character set, the permissible collations are listed.

To list the available character sets and their default collations, use the SHOW CHARACTER SET
statement or query the INFORMATION_SCHEMA CHARACTER_SETS table. For example:

mysql> SHOW CHARACTER SET;
+----------+---------------------------------+---------------------+--------+
| Charset  | Description                     | Default collation   | Maxlen |
+----------+---------------------------------+---------------------+--------+
| armscii8 | ARMSCII-8 Armenian              | armscii8_general_ci |      1 |
| ascii    | US ASCII                        | ascii_general_ci    |      1 |
| big5     | Big5 Traditional Chinese        | big5_chinese_ci     |      2 |
| binary   | Binary pseudo charset           | binary              |      1 |
| cp1250   | Windows Central European        | cp1250_general_ci   |      1 |
| cp1251   | Windows Cyrillic                | cp1251_general_ci   |      1 |
| cp1256   | Windows Arabic                  | cp1256_general_ci   |      1 |
| cp1257   | Windows Baltic                  | cp1257_general_ci   |      1 |
| cp850    | DOS West European               | cp850_general_ci    |      1 |
| cp852    | DOS Central European            | cp852_general_ci    |      1 |
| cp866    | DOS Russian                     | cp866_general_ci    |      1 |
| cp932    | SJIS for Windows Japanese       | cp932_japanese_ci   |      2 |
| dec8     | DEC West European               | dec8_swedish_ci     |      1 |
| eucjpms  | UJIS for Windows Japanese       | eucjpms_japanese_ci |      3 |
| euckr    | EUC-KR Korean                   | euckr_korean_ci     |      2 |
| gb18030  | China National Standard GB18030 | gb18030_chinese_ci  |      4 |
| gb2312   | GB2312 Simplified Chinese       | gb2312_chinese_ci   |      2 |
| gbk      | GBK Simplified Chinese          | gbk_chinese_ci      |      2 |
| geostd8  | GEOSTD8 Georgian                | geostd8_general_ci  |      1 |
| greek    | ISO 8859-7 Greek                | greek_general_ci    |      1 |
| hebrew   | ISO 8859-8 Hebrew               | hebrew_general_ci   |      1 |
| hp8      | HP West European                | hp8_english_ci      |      1 |
| keybcs2  | DOS Kamenicky Czech-Slovak      | keybcs2_general_ci  |      1 |
| koi8r    | KOI8-R Relcom Russian           | koi8r_general_ci    |      1 |
| koi8u    | KOI8-U Ukrainian                | koi8u_general_ci    |      1 |
| latin1   | cp1252 West European            | latin1_swedish_ci   |      1 |
| latin2   | ISO 8859-2 Central European     | latin2_general_ci   |      1 |
| latin5   | ISO 8859-9 Turkish              | latin5_turkish_ci   |      1 |
| latin7   | ISO 8859-13 Baltic              | latin7_general_ci   |      1 |
| macce    | Mac Central European            | macce_general_ci    |      1 |
| macroman | Mac West European               | macroman_general_ci |      1 |
| sjis     | Shift-JIS Japanese              | sjis_japanese_ci    |      2 |
| swe7     | 7bit Swedish                    | swe7_swedish_ci     |      1 |
| tis620   | TIS620 Thai                     | tis620_thai_ci      |      1 |
| ucs2     | UCS-2 Unicode                   | ucs2_general_ci     |      2 |
| ujis     | EUC-JP Japanese                 | ujis_japanese_ci    |      3 |
| utf16    | UTF-16 Unicode                  | utf16_general_ci    |      4 |
| utf16le  | UTF-16LE Unicode                | utf16le_general_ci  |      4 |
| utf32    | UTF-32 Unicode                  | utf32_general_ci    |      4 |
| utf8mb3  | UTF-8 Unicode                   | utf8mb3_general_ci  |      3 |
| utf8mb4  | UTF-8 Unicode                   | utf8mb4_0900_ai_ci  |      4 |
+----------+---------------------------------+---------------------+--------+

In cases where a character set has multiple collations, it might not be clear which collation is most
suitable for a given application. To avoid choosing the wrong collation, it can be helpful to perform
some comparisons with representative data values to make sure that a given collation sorts values the
way you expect.

12.10.1 Unicode Character Sets

This section describes the collations available for Unicode character sets and their differentiating
properties. For general information about Unicode, see Section 12.9, “Unicode Support”.

1969

Unicode Character Sets

MySQL supports multiple Unicode character sets:

• utf8mb4: A UTF-8 encoding of the Unicode character set using one to four bytes per character.

• utf8mb3: A UTF-8 encoding of the Unicode character set using one to three bytes per character.

This character set is deprecated; please use utf8mb4 instead.

• utf8: A deprecated alias for utf8mb3. Use utf8mb4 instead.

Note

utf8 is expected in a future release to become an alias for utf8mb4.

• ucs2: The UCS-2 encoding of the Unicode character set using two bytes per character. Deprecated;

expect support for this character set to be removed in a future version of MySQL.

• utf16: The UTF-16 encoding for the Unicode character set using two or four bytes per character.

Like ucs2 but with an extension for supplementary characters.

• utf16le: The UTF-16LE encoding for the Unicode character set. Like utf16 but little-endian rather

than big-endian.

• utf32: The UTF-32 encoding for the Unicode character set using four bytes per character.

Note

The utf8mb3 character set is deprecated and you should expect it to be
removed in a future MySQL release. Please use utf8mb4 instead. utf8 is
currently an alias for utf8mb3, but it is now deprecated as such, and utf8 is
expected subsequently to become a reference to utf8mb4. utf8mb3 is also
displayed in place of utf8 in columns of Information Schema tables, and in the
output of SQL SHOW statements.

To avoid ambiguity about the meaning of utf8, consider specifying utf8mb4
explicitly for character set references.

utf8mb4, utf16, utf16le, and utf32 support Basic Multilingual Plane (BMP) characters and
supplementary characters that lie outside the BMP. utf8mb3 and ucs2 support only BMP characters.

Most Unicode character sets have a general collation (indicated by _general in the name or
by the absence of a language specifier), a binary collation (indicated by _bin in the name),
and several language-specific collations (indicated by language specifiers). For example, for
utf8mb4, utf8mb4_general_ci and utf8mb4_bin are its general and binary collations, and
utf8mb4_danish_ci is one of its language-specific collations.

Most character sets have a single binary collation. utf8mb4 is an exception that has two:
utf8mb4_bin and utf8mb4_0900_bin. These two binary collations have the same sort order
but are distinguished by their pad attribute and collating weight characteristics. See Collation Pad
Attributes, and Character Collating Weights.

Collation support for utf16le is limited. The only collations available are utf16le_general_ci and
utf16le_bin. These are similar to utf16_general_ci and utf16_bin.

• Unicode Collation Algorithm (UCA) Versions

• Collation Pad Attributes

• Language-Specific Collations

• _general_ci Versus _unicode_ci Collations

• Character Collating Weights

1970

Unicode Character Sets

• Miscellaneous Information

Unicode Collation Algorithm (UCA) Versions

MySQL implements the xxx_unicode_ci collations according to the Unicode Collation Algorithm
(UCA) described at http://www.unicode.org/reports/tr10/. The collation uses the version-4.0.0 UCA
weight keys: http://www.unicode.org/Public/UCA/4.0.0/allkeys-4.0.0.txt. The xxx_unicode_ci
collations have only partial support for the Unicode Collation Algorithm. Some characters are not
supported, and combining marks are not fully supported. This affects languages such as Vietnamese,
Yoruba, and Navajo. A combined character is considered different from the same character written
with a single unicode character in string comparisons, and the two characters are considered to have a
different length (for example, as returned by the CHAR_LENGTH() function or in result set metadata).

Unicode collations based on UCA versions higher than 4.0.0 include the version in the collation name.
Examples:

• utf8mb4_unicode_520_ci is based on UCA 5.2.0 weight keys (http://www.unicode.org/Public/

UCA/5.2.0/allkeys.txt),

• utf8mb4_0900_ai_ci is based on UCA 9.0.0 weight keys (http://www.unicode.org/Public/

UCA/9.0.0/allkeys.txt).

The LOWER() and UPPER() functions perform case folding according to the collation of their argument.
A character that has uppercase and lowercase versions only in a Unicode version higher than 4.0.0 is
converted by these functions only if the argument collation uses a high enough UCA version.

Collation Pad Attributes

Collations based on UCA 9.0.0 and higher are faster than collations based on UCA versions prior to
9.0.0. They also have a pad attribute of NO PAD, in contrast to PAD SPACE as used in collations based
on UCA versions prior to 9.0.0. For comparison of nonbinary strings, NO PAD collations treat spaces at
the end of strings like any other character (see Trailing Space Handling in Comparisons).

To determine the pad attribute for a collation, use the INFORMATION_SCHEMA COLLATIONS table,
which has a PAD_ATTRIBUTE column. For example:

mysql> SELECT COLLATION_NAME, PAD_ATTRIBUTE
       FROM INFORMATION_SCHEMA.COLLATIONS
       WHERE CHARACTER_SET_NAME = 'utf8mb4';
+----------------------------+---------------+
| COLLATION_NAME             | PAD_ATTRIBUTE |
+----------------------------+---------------+
| utf8mb4_general_ci         | PAD SPACE     |
| utf8mb4_bin                | PAD SPACE     |
| utf8mb4_unicode_ci         | PAD SPACE     |
| utf8mb4_icelandic_ci       | PAD SPACE     |
...
| utf8mb4_0900_ai_ci         | NO PAD        |
| utf8mb4_de_pb_0900_ai_ci   | NO PAD        |
| utf8mb4_is_0900_ai_ci      | NO PAD        |
...
| utf8mb4_ja_0900_as_cs      | NO PAD        |
| utf8mb4_ja_0900_as_cs_ks   | NO PAD        |
| utf8mb4_0900_as_ci         | NO PAD        |
| utf8mb4_ru_0900_ai_ci      | NO PAD        |
| utf8mb4_ru_0900_as_cs      | NO PAD        |
| utf8mb4_zh_0900_as_cs      | NO PAD        |
| utf8mb4_0900_bin           | NO PAD        |
+----------------------------+---------------+

Comparison of nonbinary string values (CHAR, VARCHAR, and TEXT) that have a NO PAD collation
differ from other collations with respect to trailing spaces. For example, 'a' and 'a ' compare as
different strings, not the same string. This can be seen using the binary collations for utf8mb4. The
pad attribute for utf8mb4_bin is PAD SPACE, whereas for utf8mb4_0900_bin it is NO PAD.

1971

Unicode Character Sets

Consequently, operations involving utf8mb4_0900_bin do not add trailing spaces, and comparisons
involving strings with trailing spaces may differ for the two collations:

mysql> CREATE TABLE t1 (c CHAR(10) COLLATE utf8mb4_bin);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t1 VALUES('a');
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t1 WHERE c = 'a ';
+------+
| c    |
+------+
| a    |
+------+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 MODIFY c CHAR(10) COLLATE utf8mb4_0900_bin;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1 WHERE c = 'a ';
Empty set (0.00 sec)

Language-Specific Collations

MySQL implements language-specific Unicode collations if the ordering based only on the Unicode
Collation Algorithm (UCA) does not work well for a language. Language-specific collations are UCA-
based, with additional language tailoring rules. Examples of such rules appear later in this section.
For questions about particular language orderings, http://unicode.org provides Common Locale Data
Repository (CLDR) collation charts at http://www.unicode.org/cldr/charts/30/collation/index.html.

For example, the nonlanguage-specific utf8mb4_0900_ai_ci and language-specific
utf8mb4_LOCALE_0900_ai_ci Unicode collations each have these characteristics:

• The collation is based on UCA 9.0.0 and CLDR v30, is accent-insensitive and case-insensitive.
These characteristics are indicated by _0900, _ai, and _ci in the collation name. Exception:
utf8mb4_la_0900_ai_ci is not based on CLDR because Classical Latin is not defined in CLDR.

• The collation works for all characters in the range [U+0, U+10FFFF].

• If the collation is not language specific, it sorts all characters, including supplementary characters,
in default order (described following). If the collation is language specific, it sorts characters of the
language correctly according to language-specific rules, and characters not in the language in default
order.

• By default, the collation sorts characters having a code point listed in the DUCET table (Default

Unicode Collation Element Table) according to the weight value assigned in the table. The collation
sorts characters not having a code point listed in the DUCET table using their implicit weight value,
which is constructed according to the UCA.

• For non-language-specific collations, characters in contraction sequences are treated as separate
characters. For language-specific collations, contractions might change character sorting order.

A collation name that includes a locale code or language name shown in the following table is a
language-specific collation. Unicode character sets may include collations for one or more of these
languages.

Table 12.3 Unicode Collation Language Specifiers

Language

Bosnian

Bulgarian

1972

Language Specifier

bs

bg

Language

Chinese

Classical Latin

Croatian

Czech

Danish

Esperanto

Estonian

Galician

German phone book order

Hungarian

Icelandic

Japanese

Latvian

Lithuanian

Mongolian

Norwegian / Bokmål

Norwegian / Nynorsk

Persian

Polish

Romanian

Russian

Serbian

Sinhala

Slovak

Slovenian

Modern Spanish

Traditional Spanish

Swedish

Turkish

Vietnamese

Unicode Character Sets

Language Specifier

zh

la or roman

hr or croatian

cs or czech

da or danish

eo or esperanto

et or estonian

gl

de_pb or german2

hu or hungarian

is or icelandic

ja

lv or latvian

lt or lithuanian

mn

nb

nn

persian

pl or polish

ro or romanian

ru

sr

sinhala

sk or slovak

sl or slovenian

es or spanish

es_trad or spanish2

sv or swedish

tr or turkish

vi or vietnamese

MySQL provides the Bulgarian collations utf8mb4_bg_0900_ai_ci and
utf8mb4_bg_0900_as_cs.

Croatian collations are tailored for these Croatian letters: Č, Ć, Dž, Đ, Lj, Nj, Š, Ž.

MySQL provides the utf8mb4_sr_latn_0900_ai_ci and utf8mb4_sr_latn_0900_as_cs
collations for Serbian and the utf8mb4_bs_0900_ai_ci and utf8mb4_bs_0900_as_cs collations
for Bosnian, when these languages are written with the Latin alphabet.

MySQL provides collations for both major varieties of Norwegian: for Bokmål, you can use
utf8mb4_nb_0900_ai_ci and utf8mb4_nb_0900_as_cs; for Nynorsk, MySQL now provides
utf8mb4_nn_0900_ai_ci and utf8mb4_nn_0900_as_cs.

For Japanese, the utf8mb4 character set includes utf8mb4_ja_0900_as_cs and
utf8mb4_ja_0900_as_cs_ks collations. Both collations are accent-sensitive and case-sensitive.

1973

Unicode Character Sets

utf8mb4_ja_0900_as_cs_ks is also kana-sensitive and distinguishes Katakana characters from
Hiragana characters, whereas utf8mb4_ja_0900_as_cs treats Katakana and Hiragana characters
as equal for sorting. Applications that require a Japanese collation but not kana sensitivity may use
utf8mb4_ja_0900_as_cs for better sort performance. utf8mb4_ja_0900_as_cs uses three
weight levels for sorting; utf8mb4_ja_0900_as_cs_ks uses four.

For Classical Latin collations that are accent-insensitive, I and J compare as equal, and U and V
compare as equal. I and J, and U and V compare as equal on the base letter level. In other words, J is
regarded as an accented I, and U is regarded as an accented V.

MySQL provides collations for the Mongolian language when written with Cyrillic characters,
utf8mb4_mn_cyrl_0900_ai_ci and utf8mb4_mn_cyrl_0900_as_cs.

Spanish collations are available for modern and traditional Spanish. For both, ñ (n-tilde) is a separate
letter between n and o. In addition, for traditional Spanish, ch is a separate letter between c and d, and
ll is a separate letter between l and m.

Traditional Spanish collations may also be used for Asturian and Galician. MySQL also provides
utf8mb4_gl_0900_ai_ci and utf8mb4_gl_0900_as_cs collations for Galician. (These are the
same collations as utf8mb4_es_0900_ai_ci and utf8mb4_es_0900_as_cs, respectively.)

Swedish collations include Swedish rules. For example, in Swedish, the following relationship holds,
which is not something expected by a German or French speaker:

Ü = Y < Ö

_general_ci Versus _unicode_ci Collations

For any Unicode character set, operations performed using the xxx_general_ci collation
are faster than those for the xxx_unicode_ci collation. For example, comparisons for the
utf8mb4_general_ci collation are faster, but slightly less correct, than comparisons for
utf8mb4_unicode_ci. The reason is that utf8mb4_unicode_ci supports mappings such as
expansions; that is, when one character compares as equal to combinations of other characters.
For example, ß is equal to ss in German and some other languages. utf8mb4_unicode_ci also
supports contractions and ignorable characters. utf8mb4_general_ci is a legacy collation that
does not support expansions, contractions, or ignorable characters. It can make only one-to-one
comparisons between characters.

To further illustrate, the following equalities hold in both utf8mb4_general_ci and
utf8mb4_unicode_ci (for the effect of this in comparisons or searches, see Section 12.8.6,
“Examples of the Effect of Collation”):

Ä = A
Ö = O
Ü = U

A difference between the collations is that this is true for utf8mb4_general_ci:

ß = s

Whereas this is true for utf8mb4_unicode_ci, which supports the German DIN-1 ordering (also
known as dictionary order):

ß = ss

MySQL implements language-specific Unicode collations if the ordering with utf8mb4_unicode_ci
does not work well for a language. For example, utf8mb4_unicode_ci works fine for German
dictionary order and French, so there is no need to create special utf8mb4 collations.

utf8mb4_general_ci also is satisfactory for both German and French, except that ß is equal to
s, and not to ss. If this is acceptable for your application, you should use utf8mb4_general_ci
because it is faster. If this is not acceptable (for example, if you require German dictionary order), use
utf8mb4_unicode_ci because it is more accurate.

1974

Unicode Character Sets

If you require German DIN-2 (phone book) ordering, use the utf8mb4_german2_ci collation, which
compares the following sets of characters equal:

Ä = Æ = AE
Ö = Œ = OE
Ü = UE
ß = ss

utf8mb4_german2_ci is similar to latin1_german2_ci, but the latter does not compare Æ equal
to AE or Œ equal to OE. There is no utf8mb4_german_ci corresponding to latin1_german_ci for
German dictionary order because utf8mb4_general_ci suffices.

Character Collating Weights

A character's collating weight is determined as follows:

• For all Unicode collations except the _bin (binary) collations, MySQL performs a table lookup to find

a character's collating weight.

• For _bin collations except utf8mb4_0900_bin, the weight is based on the code point, possibly

with leading zero bytes added.

• For utf8mb4_0900_bin, the weight is the utf8mb4 encoding bytes. The sort order is the same as

for utf8mb4_bin, but much faster.

Collating weights can be displayed using the WEIGHT_STRING() function. (See Section 14.8, “String
Functions and Operators”.) If a collation uses a weight lookup table, but a character is not in the table
(for example, because it is a “new” character), collating weight determination becomes more complex:

• For BMP characters in general collations (xxx_general_ci), the weight is the code point.

• For BMP characters in UCA collations (for example, xxx_unicode_ci and language-specific

collations), the following algorithm applies:

if (code >= 0x3400 && code <= 0x4DB5)
  base= 0xFB80; /* CJK Ideograph Extension */
else if (code >= 0x4E00 && code <= 0x9FA5)
  base= 0xFB40; /* CJK Ideograph */
else
  base= 0xFBC0; /* All other characters */
aaaa= base +  (code >> 15);
bbbb= (code & 0x7FFF) | 0x8000;

The result is a sequence of two collating elements, aaaa followed by bbbb. For example:

mysql> SELECT HEX(WEIGHT_STRING(_ucs2 0x04CF COLLATE ucs2_unicode_ci));
+----------------------------------------------------------+
| HEX(WEIGHT_STRING(_ucs2 0x04CF COLLATE ucs2_unicode_ci)) |
+----------------------------------------------------------+
| FBC084CF                                                 |
+----------------------------------------------------------+

Thus, U+04cf CYRILLIC SMALL LETTER PALOCHKA (ӏ) is, with all UCA 4.0.0 collations, greater
than U+04c0 CYRILLIC LETTER PALOCHKA (Ӏ). With UCA 5.2.0 collations, all palochkas sort
together.

• For supplementary characters in general collations, the weight is the weight for 0xfffd

REPLACEMENT CHARACTER. For supplementary characters in UCA 4.0.0 collations, their collating
weight is 0xfffd. That is, to MySQL, all supplementary characters are equal to each other, and
greater than almost all BMP characters.

An example with Deseret characters and COUNT(DISTINCT):

CREATE TABLE t (s1 VARCHAR(5) CHARACTER SET utf32 COLLATE utf32_unicode_ci);
INSERT INTO t VALUES (0xfffd);   /* REPLACEMENT CHARACTER */
INSERT INTO t VALUES (0x010412); /* DESERET CAPITAL LETTER BEE */

1975

Unicode Character Sets

INSERT INTO t VALUES (0x010413); /* DESERET CAPITAL LETTER TEE */
SELECT COUNT(DISTINCT s1) FROM t;

The result is 2 because in the MySQL xxx_unicode_ci collations, the replacement character has
a weight of 0x0dc6, whereas Deseret Bee and Deseret Tee both have a weight of 0xfffd. (Were
the utf32_general_ci collation used instead, the result is 1 because all three characters have a
weight of 0xfffd in that collation.)

An example with cuneiform characters and WEIGHT_STRING():

/*
The four characters in the INSERT string are
00000041  # LATIN CAPITAL LETTER A
0001218F  # CUNEIFORM SIGN KAB
000121A7  # CUNEIFORM SIGN KISH
00000042  # LATIN CAPITAL LETTER B
*/
CREATE TABLE t (s1 CHAR(4) CHARACTER SET utf32 COLLATE utf32_unicode_ci);
INSERT INTO t VALUES (0x000000410001218f000121a700000042);
SELECT HEX(WEIGHT_STRING(s1)) FROM t;

The result is:

0E33 FFFD FFFD 0E4A

0E33 and 0E4A are primary weights as in UCA 4.0.0. FFFD is the weight for KAB and also for KISH.

The rule that all supplementary characters are equal to each other is nonoptimal but is not expected
to cause trouble. These characters are very rare, so it is very rare that a multi-character string
consists entirely of supplementary characters. In Japan, since the supplementary characters are
obscure Kanji ideographs, the typical user does not care what order they are in, anyway. If you really
want rows sorted by the MySQL rule and secondarily by code point value, it is easy:

ORDER BY s1 COLLATE utf32_unicode_ci, s1 COLLATE utf32_bin

• For supplementary characters based on UCA versions higher than 4.0.0 (for example,

xxx_unicode_520_ci), supplementary characters do not necessarily all have the same collating
weight. Some have explicit weights from the UCA allkeys.txt file. Others have weights calculated
from this algorithm:

aaaa= base +  (code >> 15);
bbbb= (code & 0x7FFF) | 0x8000;

There is a difference between “ordering by the character's code value” and “ordering by the character's
binary representation,” a difference that appears only with utf16_bin, because of surrogates.

Suppose that utf16_bin (the binary collation for utf16) was a binary comparison “byte by byte”
rather than “character by character.” If that were so, the order of characters in utf16_bin would differ
from the order in utf8mb4_bin. For example, the following chart shows two rare characters. The first
character is in the range E000-FFFF, so it is greater than a surrogate but less than a supplementary.
The second character is a supplementary.

Code point  Character                    utf8mb4      utf16
----------  ---------                    -------      -----
0FF9D       HALFWIDTH KATAKANA LETTER N  EF BE 9D     FF 9D
10384       UGARITIC LETTER DELTA        F0 90 8E 84  D8 00 DF 84

The two characters in the chart are in order by code point value because 0xff9d < 0x10384. And
they are in order by utf8mb4 value because 0xef < 0xf0. But they are not in order by utf16 value, if
we use byte-by-byte comparison, because 0xff > 0xd8.

So MySQL's utf16_bin collation is not “byte by byte.” It is “by code point.” When MySQL sees a
supplementary-character encoding in utf16, it converts to the character's code-point value, and then
compares. Therefore, utf8mb4_bin and utf16_bin are the same ordering. This is consistent with

1976

West European Character Sets

the SQL:2008 standard requirement for a UCS_BASIC collation: “UCS_BASIC is a collation in which
the ordering is determined entirely by the Unicode scalar values of the characters in the strings being
sorted. It is applicable to the UCS character repertoire. Since every character repertoire is a subset of
the UCS repertoire, the UCS_BASIC collation is potentially applicable to every character set. NOTE 11:
The Unicode scalar value of a character is its code point treated as an unsigned integer.”

If the character set is ucs2, comparison is byte-by-byte, but ucs2 strings should not contain
surrogates, anyway.

Miscellaneous Information

The xxx_general_mysql500_ci collations preserve the pre-5.1.24 ordering of the original
xxx_general_ci collations and permit upgrades for tables created before MySQL 5.1.24 (Bug
#27877).

12.10.2 West European Character Sets

Western European character sets cover most West European languages, such as French, Spanish,
Catalan, Basque, Portuguese, Italian, Albanian, Dutch, German, Danish, Swedish, Norwegian, Finnish,
Faroese, Icelandic, Irish, Scottish, and English.

• ascii (US ASCII) collations:

• ascii_bin

• ascii_general_ci (default)

• cp850 (DOS West European) collations:

• cp850_bin

• cp850_general_ci (default)

• dec8 (DEC Western European) collations:

• dec8_bin

• dec8_swedish_ci (default)

The dec character set is deprecated; expect support for it to be removed in a subsequent MySQL
release.

• hp8 (HP Western European) collations:

• hp8_bin

• hp8_english_ci (default)

The hp8 character set is deprecated; expect support for it to be removed in a subsequent MySQL
release.

• latin1 (cp1252 West European) collations:

• latin1_bin

• latin1_danish_ci

• latin1_general_ci

• latin1_general_cs

• latin1_german1_ci

1977

Central European Character Sets

• latin1_german2_ci

• latin1_spanish_ci

• latin1_swedish_ci (default)

MySQL's latin1 is the same as the Windows cp1252 character set. This means it is the same
as the official ISO 8859-1 or IANA (Internet Assigned Numbers Authority) latin1, except that
IANA latin1 treats the code points between 0x80 and 0x9f as “undefined,” whereas cp1252, and
therefore MySQL's latin1, assign characters for those positions. For example, 0x80 is the Euro
sign. For the “undefined” entries in cp1252, MySQL translates 0x81 to Unicode 0x0081, 0x8d to
0x008d, 0x8f to 0x008f, 0x90 to 0x0090, and 0x9d to 0x009d.

The latin1_swedish_ci collation is the default that probably is used by the majority of MySQL
customers. Although it is frequently said that it is based on the Swedish/Finnish collation rules, there
are Swedes and Finns who disagree with this statement.

The latin1_german1_ci and latin1_german2_ci collations are based on the DIN-1 and
DIN-2 standards, where DIN stands for Deutsches Institut für Normung (the German equivalent
of ANSI). DIN-1 is called the “dictionary collation” and DIN-2 is called the “phone book collation.”
For an example of the effect this has in comparisons or when doing searches, see Section 12.8.6,
“Examples of the Effect of Collation”.

• latin1_german1_ci (dictionary) rules:

Ä = A
Ö = O
Ü = U
ß = s

• latin1_german2_ci (phone-book) rules:

Ä = AE
Ö = OE
Ü = UE
ß = ss

In the latin1_spanish_ci collation, ñ (n-tilde) is a separate letter between n and o.

• macroman (Mac West European) collations:

• macroman_bin

• macroman_general_ci (default)

macroroman is deprecated; expect support for it to be removed in a subsequent MySQL release.

• swe7 (7bit Swedish) collations:

• swe7_bin

• swe7_swedish_ci (default)

12.10.3 Central European Character Sets

MySQL provides some support for character sets used in the Czech Republic, Slovakia, Hungary,
Romania, Slovenia, Croatia, Poland, and Serbia (Latin).

• cp1250 (Windows Central European) collations:

• cp1250_bin

• cp1250_croatian_ci

1978

South European and Middle East Character Sets

• cp1250_czech_cs

• cp1250_general_ci (default)

• cp1250_polish_ci

• cp852 (DOS Central European) collations:

• cp852_bin

• cp852_general_ci (default)

• keybcs2 (DOS Kamenicky Czech-Slovak) collations:

• keybcs2_bin

• keybcs2_general_ci (default)

• latin2 (ISO 8859-2 Central European) collations:

• latin2_bin

• latin2_croatian_ci

• latin2_czech_cs

• latin2_general_ci (default)

• latin2_hungarian_ci

• macce (Mac Central European) collations:

• macce_bin

• macce_general_ci (default)

macce is deprecated; expect support for it to be removed in a subsequent MySQL release.

12.10.4 South European and Middle East Character Sets

South European and Middle Eastern character sets supported by MySQL include Armenian, Arabic,
Georgian, Greek, Hebrew, and Turkish.

• armscii8 (ARMSCII-8 Armenian) collations:

• armscii8_bin

• armscii8_general_ci (default)

• cp1256 (Windows Arabic) collations:

• cp1256_bin

• cp1256_general_ci (default)

• geostd8 (GEOSTD8 Georgian) collations:

• geostd8_bin

• geostd8_general_ci (default)

• greek (ISO 8859-7 Greek) collations:

1979

Baltic Character Sets

• greek_bin

• greek_general_ci (default)

• hebrew (ISO 8859-8 Hebrew) collations:

• hebrew_bin

• hebrew_general_ci (default)

• latin5 (ISO 8859-9 Turkish) collations:

• latin5_bin

• latin5_turkish_ci (default)

12.10.5 Baltic Character Sets

The Baltic character sets cover Estonian, Latvian, and Lithuanian languages.

• cp1257 (Windows Baltic) collations:

• cp1257_bin

• cp1257_general_ci (default)

• cp1257_lithuanian_ci

• latin7 (ISO 8859-13 Baltic) collations:

• latin7_bin

• latin7_estonian_cs

• latin7_general_ci (default)

• latin7_general_cs

12.10.6 Cyrillic Character Sets

The Cyrillic character sets and collations are for use with Belarusian, Bulgarian, Russian, Ukrainian,
and Serbian (Cyrillic) languages.

• cp1251 (Windows Cyrillic) collations:

• cp1251_bin

• cp1251_bulgarian_ci

• cp1251_general_ci (default)

• cp1251_general_cs

• cp1251_ukrainian_ci

• cp866 (DOS Russian) collations:

• cp866_bin

• cp866_general_ci (default)

• koi8r (KOI8-R Relcom Russian) collations:

1980

Asian Character Sets

• gb18030_unicode_520_ci

• sjis (Shift-JIS Japanese) collations:

• sjis_bin

• sjis_japanese_ci (default)

• tis620 (TIS620 Thai) collations:

• tis620_bin

• tis620_thai_ci (default)

• ujis (EUC-JP Japanese) collations:

• ujis_bin

• ujis_japanese_ci (default)

The big5_chinese_ci collation sorts on number of strokes.

12.10.7.1 The cp932 Character Set

Why is cp932 needed?

In MySQL, the sjis character set corresponds to the Shift_JIS character set defined by IANA,
which supports JIS X0201 and JIS X0208 characters. (See http://www.iana.org/assignments/character-
sets.)

However, the meaning of “SHIFT JIS” as a descriptive term has become very vague and it often
includes the extensions to Shift_JIS that are defined by various vendors.

For example, “SHIFT JIS” used in Japanese Windows environments is a Microsoft extension of
Shift_JIS and its exact name is Microsoft Windows Codepage : 932 or cp932. In addition to
the characters supported by Shift_JIS, cp932 supports extension characters such as NEC special
characters, NEC selected—IBM extended characters, and IBM selected characters.

Many Japanese users have experienced problems using these extension characters. These problems
stem from the following factors:

• MySQL automatically converts character sets.

• Character sets are converted using Unicode (ucs2).

• The sjis character set does not support the conversion of these extension characters.

• There are several conversion rules from so-called “SHIFT JIS” to Unicode, and some characters

are converted to Unicode differently depending on the conversion rule. MySQL supports only one of
these rules (described later).

The MySQL cp932 character set is designed to solve these problems.

Because MySQL supports character set conversion, it is important to separate IANA Shift_JIS and
cp932 into two different character sets because they provide different conversion rules.

How does cp932 differ from sjis?

The cp932 character set differs from sjis in the following ways:

• cp932 supports NEC special characters, NEC selected—IBM extended characters, and IBM

selected characters.

1982

Asian Character Sets

• Some cp932 characters have two different code points, both of which convert to the same Unicode

code point. When converting from Unicode back to cp932, one of the code points must be
selected. For this “round trip conversion,” the rule recommended by Microsoft is used. (See http://
support.microsoft.com/kb/170559/EN-US/.)

The conversion rule works like this:

• If the character is in both JIS X 0208 and NEC special characters, use the code point of JIS X

0208.

• If the character is in both NEC special characters and IBM selected characters, use the code point

of NEC special characters.

• If the character is in both IBM selected characters and NEC selected—IBM extended characters,

use the code point of IBM extended characters.

The table shown at https://msdn.microsoft.com/en-us/goglobal/cc305152.aspx provides information
about the Unicode values of cp932 characters. For cp932 table entries with characters under which
a four-digit number appears, the number represents the corresponding Unicode (ucs2) encoding.
For table entries with an underlined two-digit value appears, there is a range of cp932 character
values that begin with those two digits. Clicking such a table entry takes you to a page that displays
the Unicode value for each of the cp932 characters that begin with those digits.

The following links are of special interest. They correspond to the encodings for the following sets of
characters:

• NEC special characters (lead byte 0x87):

https://msdn.microsoft.com/en-us/goglobal/gg674964

• NEC selected—IBM extended characters (lead byte 0xED and 0xEE):

https://msdn.microsoft.com/en-us/goglobal/gg671837
https://msdn.microsoft.com/en-us/goglobal/gg671838

• IBM selected characters (lead byte 0xFA, 0xFB, 0xFC):

https://msdn.microsoft.com/en-us/goglobal/gg671839
https://msdn.microsoft.com/en-us/goglobal/gg671840
https://msdn.microsoft.com/en-us/goglobal/gg671841

• cp932 supports conversion of user-defined characters in combination with eucjpms, and solves
the problems with sjis/ujis conversion. For details, please refer to http://www.sljfaq.org/afaq/
encodings.html.

For some characters, conversion to and from ucs2 is different for sjis and cp932. The following
tables illustrate these differences.

Conversion to ucs2:

sjis/cp932 Value

sjis -> ucs2 Conversion

cp932 -> ucs2 Conversion

5C

7E

815C

815F

8160

8161

817C

8191

005C

007E

2015

005C

301C

2016

2212

00A2

005C

007E

2015

FF3C

FF5E

2225

FF0D

FFE0

1983

Asian Character Sets

sjis/cp932 Value

sjis -> ucs2 Conversion

cp932 -> ucs2 Conversion

8192

81CA

00A3

00AC

FFE1

FFE2

Conversion from ucs2:

ucs2 value

ucs2 -> sjis Conversion

ucs2 -> cp932 Conversion

005C

007E

00A2

00A3

00AC

2015

2016

2212

2225

301C

FF0D

FF3C

FF5E

FFE0

FFE1

FFE2

815F

7E

8191

8192

81CA

815C

8161

817C

3F

8160

3F

3F

3F

3F

3F

3F

5C

7E

3F

3F

3F

815C

3F

3F

8161

3F

817C

815F

8160

8191

8192

81CA

12.10.7.2 The gb18030 Character Set

In MySQL, the gb18030 character set corresponds to the Chinese National Standard GB 18030-2005:
Information technology —Chinese coded character set, which is the official character set of the
People's Republic of China (PRC).

Characteristics of the MySQL gb18030 Character Set

• Supports all code points defined by the GB 18030-2005 standard. Unassigned code points in the
ranges (GB+8431A439, GB+90308130) and (GB+E3329A36, GB+EF39EF39) are treated as
'?' (0x3F). Conversion of unassigned code points returns '?'.

• Supports UPPER and LOWER conversion for all GB18030 code points. Case folding defined by

Unicode is also supported (based on CaseFolding-6.3.0.txt).

• Supports Conversion of data to and from other character sets.

• Supports SQL statements such as SET NAMES.

• Supports comparison between gb18030 strings, and between gb18030 strings and strings of other

character sets. There is a conversion if strings have different character sets. Comparisons that
include or ignore trailing spaces are also supported.

• The private use area (U+E000, U+F8FF) in Unicode is mapped to gb18030.

• There is no mapping between (U+D800, U+DFFF) and GB18030. Attempted conversion of code

points in this range returns '?'.

• If an incoming sequence is illegal, an error or warning is returned. If an illegal sequence is used in

CONVERT(), an error is returned. Otherwise, a warning is returned.

1984

The Binary Character Set

• For consistency with utf8mb3 and utf8mb4, UPPER is not supported for ligatures.

• Searches for ligatures also match uppercase ligatures when using the gb18030_unicode_520_ci

collation.

• If a character has more than one uppercase character, the chosen uppercase character is the one

whose lowercase is the character itself.

• The minimum multibyte length is 1 and the maximum is 4. The character set determines the length of

a sequence using the first 1 or 2 bytes.

Supported Collations

• gb18030_bin: A binary collation.

• gb18030_chinese_ci: The default collation, which supports Pinyin. Sorting of non-Chinese

characters is based on the order of the original sort key. The original sort key is GB(UPPER(ch))
if UPPER(ch) exists. Otherwise, the original sort key is GB(ch). Chinese characters are sorted
according to the Pinyin collation defined in the Unicode Common Locale Data Repository (CLDR 24).
Non-Chinese characters are sorted before Chinese characters with the exception of GB+FE39FE39,
which is the code point maximum.

• gb18030_unicode_520_ci: A Unicode collation. Use this collation if you need to ensure that

ligatures are sorted correctly.

12.10.8 The Binary Character Set

The binary character set is the character set for binary strings, which are sequences of bytes. The
binary character set has one collation, also named binary. Comparison and sorting are based on
numeric byte values, rather than on numeric character code values (which for multibyte characters
differ from numeric byte values). For information about the differences between the binary collation
of the binary character set and the _bin collations of nonbinary character sets, see Section 12.8.5,
“The binary Collation Compared to _bin Collations”.

For the binary character set, the concepts of lettercase and accent equivalence do not apply:

• For single-byte characters stored as binary strings, character and byte boundaries are the same,

so lettercase and accent differences are significant in comparisons. That is, the binary collation is
case-sensitive and accent-sensitive.

mysql> SET NAMES 'binary';
mysql> SELECT CHARSET('abc'), COLLATION('abc');
+----------------+------------------+
| CHARSET('abc') | COLLATION('abc') |
+----------------+------------------+
| binary         | binary           |
+----------------+------------------+
mysql> SELECT 'abc' = 'ABC', 'a' = 'ä';
+---------------+------------+
| 'abc' = 'ABC' | 'a' = 'ä'  |
+---------------+------------+
|             0 |          0 |
+---------------+------------+

• For multibyte characters stored as binary strings, character and byte boundaries differ. Character

boundaries are lost, so comparisons that depend on them are not meaningful.

To perform lettercase conversion of a binary string, first convert it to a nonbinary string using a
character set appropriate for the data stored in the string:

mysql> SET @str = BINARY 'New York';
mysql> SELECT LOWER(@str), LOWER(CONVERT(@str USING utf8mb4));
+-------------+------------------------------------+
| LOWER(@str) | LOWER(CONVERT(@str USING utf8mb4)) |
+-------------+------------------------------------+

1985

Restrictions on Character Sets

| New York    | new york                           |
+-------------+------------------------------------+

To convert a string expression to a binary string, these constructs are equivalent:

BINARY expr
CAST(expr AS BINARY)
CONVERT(expr USING BINARY)

If a value is a character string literal, the _binary introducer may be used to designate it as a binary
string. For example:

_binary 'a'

The _binary introducer is permitted for hexadecimal literals and bit-value literals as well, but
unnecessary; such literals are binary strings by default.

For more information about introducers, see Section 12.3.8, “Character Set Introducers”.

Note

Within the mysql client, binary strings display using hexadecimal notation,
depending on the value of the --binary-as-hex. For more information about
that option, see Section 6.5.1, “mysql — The MySQL Command-Line Client”.

12.11 Restrictions on Character Sets

• Identifiers are stored in mysql database tables (user, db, and so forth) using utf8mb3, but
identifiers can contain only characters in the Basic Multilingual Plane (BMP). Supplementary
characters are not permitted in identifiers.

• The ucs2, utf16, utf16le, and utf32 character sets have the following restrictions:

• None of them can be used as the client character set. See Impermissible Client Character Sets.

• It is currently not possible to use LOAD DATA to load data files that use these character sets.

• FULLTEXT indexes cannot be created on a column that uses any of these character sets.
However, you can perform IN BOOLEAN MODE searches on the column without an index.

• The REGEXP and RLIKE operators work in byte-wise fashion, so they are not multibyte safe and

may produce unexpected results with multibyte character sets. In addition, these operators compare
characters by their byte values and accented characters may not compare as equal even if a given
collation treats them as equal.

12.12 Setting the Error Message Language

By default, mysqld produces error messages in English, but they can be displayed instead in any
of several other languages: Czech, Danish, Dutch, Estonian, French, German, Greek, Hungarian,
Italian, Japanese, Korean, Norwegian, Norwegian-ny, Polish, Portuguese, Romanian, Russian, Slovak,
Spanish, or Swedish. This applies to messages the server writes to the error log and sends to clients.

To select the language in which the server writes error messages, follow the instructions in this section.
For information about changing the character set for error messages (rather than the language), see
Section 12.6, “Error Message Character Set”. For general information about configuring error logging,
see Section 7.4.2, “The Error Log”.

The server searches for the error message file using these rules:

• It looks for the file in a directory constructed from two system variable values, lc_messages_dir

and lc_messages, with the latter converted to a language name. Suppose that you start the server
using this command:

1986

Adding a Character Set

mysqld --lc_messages_dir=/usr/share/mysql --lc_messages=fr_FR

In this case, mysqld maps the locale fr_FR to the language french and looks for the error file in
the /usr/share/mysql/french directory.

By default, the language files are located in the share/mysql/LANGUAGE directory under the
MySQL base directory.

• If the message file cannot be found in the directory constructed as just described, the server ignores
the lc_messages value and uses only the lc_messages_dir value as the location in which to
look.

• If the server cannot find the configured message file, it writes a message to the error log to indicate

the problem and defaults to built-in English messages.

The lc_messages_dir system variable can be set only at server startup and has only a global
read-only value at runtime. lc_messages can be set at server startup and has global and session
values that can be modified at runtime. Thus, the error message language can be changed while the
server is running, and each client can have its own error message language by setting its session
lc_messages value to the desired locale name. For example, if the server is using the fr_FR locale
for error messages, a client can execute this statement to receive error messages in English:

SET lc_messages = 'en_US';

12.13 Adding a Character Set

This section discusses the procedure for adding a character set to MySQL. The proper procedure
depends on whether the character set is simple or complex:

• If the character set does not need special string collating routines for sorting and does not need

multibyte character support, it is simple.

• If the character set needs either of those features, it is complex.

For example, greek and swe7 are simple character sets, whereas big5 and czech are complex
character sets.

To use the following instructions, you must have a MySQL source distribution. In the instructions,
MYSET represents the name of the character set that you want to add.

1. Add a <charset> element for MYSET to the sql/share/charsets/Index.xml file. Use the
existing contents in the file as a guide to adding new contents. A partial listing for the latin1
<charset> element follows:

<charset name="latin1">
  <family>Western</family>
  <description>cp1252 West European</description>
  ...
  <collation name="latin1_swedish_ci" id="8" order="Finnish, Swedish">
    <flag>primary</flag>
    <flag>compiled</flag>
  </collation>
  <collation name="latin1_danish_ci" id="15" order="Danish"/>
  ...
  <collation name="latin1_bin" id="47" order="Binary">
    <flag>binary</flag>
    <flag>compiled</flag>
  </collation>
  ...
</charset>

The <charset> element must list all the collations for the character set. These must include at
least a binary collation and a default (primary) collation. The default collation is often named using
a suffix of general_ci (general, case-insensitive). It is possible for the binary collation to be the

1987

Adding a Character Set

default collation, but usually they are different. The default collation should have a primary flag.
The binary collation should have a binary flag.

You must assign a unique ID number to each collation. The range of IDs from 1024 to 2047 is
reserved for user-defined collations. To find the maximum of the currently used collation IDs, use
this query:

SELECT MAX(ID) FROM INFORMATION_SCHEMA.COLLATIONS;

2. This step depends on whether you are adding a simple or complex character set. A simple

character set requires only a configuration file, whereas a complex character set requires C source
file that defines collation functions, multibyte functions, or both.

For a simple character set, create a configuration file, MYSET.xml, that describes the character
set properties. Create this file in the sql/share/charsets directory. You can use a copy of
latin1.xml as the basis for this file. The syntax for the file is very simple:

• Comments are written as ordinary XML comments (<!-- text -->).

• Words within <map> array elements are separated by arbitrary amounts of whitespace.

• Each word within <map> array elements must be a number in hexadecimal format.

• The <map> array element for the <ctype> element has 257 words. The other <map> array
elements after that have 256 words. See Section 12.13.1, “Character Definition Arrays”.

• For each collation listed in the <charset> element for the character set in Index.xml,
MYSET.xml must contain a <collation> element that defines the character ordering.

For a complex character set, create a C source file that describes the character set properties and
defines the support routines necessary to properly perform operations on the character set:

• Create the file ctype-MYSET.c in the strings directory. Look at one of the existing ctype-

*.c files (such as ctype-big5.c) to see what needs to be defined. The arrays in your file must
have names like ctype_MYSET, to_lower_MYSET, and so on. These correspond to the arrays
for a simple character set. See Section 12.13.1, “Character Definition Arrays”.

• For each <collation> element listed in the <charset> element for the character set in
Index.xml, the ctype-MYSET.c file must provide an implementation of the collation.

• If the character set requires string collating functions, see Section 12.13.2, “String Collating

Support for Complex Character Sets”.

• If the character set requires multibyte character support, see Section 12.13.3, “Multi-Byte

Character Support for Complex Character Sets”.

3. Modify the configuration information. Use the existing configuration information as a guide to adding
information for MYSYS. The example here assumes that the character set has default and binary
collations, but more lines are needed if MYSET has additional collations.

a. Edit mysys/charset-def.c, and “register” the collations for the new character set.

Add these lines to the “declaration” section:

#ifdef HAVE_CHARSET_MYSET
extern CHARSET_INFO my_charset_MYSET_general_ci;
extern CHARSET_INFO my_charset_MYSET_bin;
#endif

Add these lines to the “registration” section:

#ifdef HAVE_CHARSET_MYSET
  add_compiled_collation(&my_charset_MYSET_general_ci);

1988

Character Definition Arrays

  add_compiled_collation(&my_charset_MYSET_bin);
#endif

b.

If the character set uses ctype-MYSET.c, edit strings/CMakeLists.txt and add
ctype-MYSET.c to the definition of the STRINGS_SOURCES variable.

c. Edit cmake/character_sets.cmake:

i. Add MYSET to the value of with CHARSETS_AVAILABLE in alphabetic order.

ii. Add MYSET to the value of CHARSETS_COMPLEX in alphabetic order. This is needed even
for simple character sets, so that CMake can recognize -DDEFAULT_CHARSET=MYSET.

4. Reconfigure, recompile, and test.

12.13.1 Character Definition Arrays

Each simple character set has a configuration file located in the sql/share/charsets directory.
For a character set named MYSYS, the file is named MYSET.xml. It uses <map> array elements to list
character set properties. <map> elements appear within these elements:

• <ctype> defines attributes for each character.

• <lower> and <upper> list the lowercase and uppercase characters.

• <unicode> maps 8-bit character values to Unicode values.

• <collation> elements indicate character ordering for comparison and sorting, one element per

collation. Binary collations need no <map> element because the character codes themselves provide
the ordering.

For a complex character set as implemented in a ctype-MYSET.c file in the strings directory,
there are corresponding arrays: ctype_MYSET[], to_lower_MYSET[], and so forth. Not every
complex character set has all of the arrays. See also the existing ctype-*.c files for examples. See
the CHARSET_INFO.txt file in the strings directory for additional information.

Most of the arrays are indexed by character value and have 256 elements. The <ctype> array is
indexed by character value + 1 and has 257 elements. This is a legacy convention for handling EOF.

<ctype> array elements are bit values. Each element describes the attributes of a single character in
the character set. Each attribute is associated with a bitmask, as defined in include/m_ctype.h:

#define _MY_U   01      /* Upper case */
#define _MY_L   02      /* Lower case */
#define _MY_NMR 04      /* Numeral (digit) */
#define _MY_SPC 010     /* Spacing character */
#define _MY_PNT 020     /* Punctuation */
#define _MY_CTR 040     /* Control character */
#define _MY_B   0100    /* Blank */
#define _MY_X   0200    /* heXadecimal digit */

The <ctype> value for a given character should be the union of the applicable bitmask values that
describe the character. For example, 'A' is an uppercase character (_MY_U) as well as a hexadecimal
digit (_MY_X), so its ctype value should be defined like this:

ctype['A'+1] = _MY_U | _MY_X = 01 | 0200 = 0201

The bitmask values in m_ctype.h are octal values, but the elements of the <ctype> array in
MYSET.xml should be written as hexadecimal values.

The <lower> and <upper> arrays hold the lowercase and uppercase characters corresponding to
each member of the character set. For example:

lower['A'] should contain 'a'
upper['a'] should contain 'A'

1989

String Collating Support for Complex Character Sets

Each <collation> array indicates how characters should be ordered for comparison and sorting
purposes. MySQL sorts characters based on the values of this information. In some cases, this is
the same as the <upper> array, which means that sorting is case-insensitive. For more complicated
sorting rules (for complex character sets), see the discussion of string collating in Section 12.13.2,
“String Collating Support for Complex Character Sets”.

12.13.2 String Collating Support for Complex Character Sets

For a simple character set named MYSET, sorting rules are specified in the MYSET.xml configuration
file using <map> array elements within <collation> elements. If the sorting rules for your language
are too complex to be handled with simple arrays, you must define string collating functions in the
ctype-MYSET.c source file in the strings directory.

The existing character sets provide the best documentation and examples to show how these functions
are implemented. Look at the ctype-*.c files in the strings directory, such as the files for the
big5, czech, gbk, sjis, and tis160 character sets. Take a look at the MY_COLLATION_HANDLER
structures to see how they are used. See also the CHARSET_INFO.txt file in the strings directory
for additional information.

12.13.3 Multi-Byte Character Support for Complex Character Sets

If you want to add support for a new character set named MYSET that includes multibyte characters,
you must use multibyte character functions in the ctype-MYSET.c source file in the strings
directory.

The existing character sets provide the best documentation and examples to show how these functions
are implemented. Look at the ctype-*.c files in the strings directory, such as the files for the
euc_kr, gb2312, gbk, sjis, and ujis character sets. Take a look at the MY_CHARSET_HANDLER
structures to see how they are used. See also the CHARSET_INFO.txt file in the strings directory
for additional information.

12.14 Adding a Collation to a Character Set

Warning

User-defined collations are deprecated; you should expect support for them
to be removed in a future version of MySQL. The MySQL 8.4 server issues
a warning for any use of COLLATE user_defined_collation in an
SQL statement; a warning is also issued when the server is started with --
collation-server set equal to the name of a user-defined collation.

A collation is a set of rules that defines how to compare and sort character strings. Each collation in
MySQL belongs to a single character set. Every character set has at least one collation, and most have
two or more collations.

A collation orders characters based on weights. Each character in a character set maps to a weight.
Characters with equal weights compare as equal, and characters with unequal weights compare
according to the relative magnitude of their weights.

The WEIGHT_STRING() function can be used to see the weights for the characters in a
string. The value that it returns to indicate weights is a binary string, so it is convenient to use
HEX(WEIGHT_STRING(str)) to display the weights in printable form. The following example shows
that weights do not differ for lettercase for the letters in 'AaBb' if it is a nonbinary case-insensitive
string, but do differ if it is a binary string:

mysql> SELECT HEX(WEIGHT_STRING('AaBb' COLLATE latin1_swedish_ci));
+------------------------------------------------------+
| HEX(WEIGHT_STRING('AaBb' COLLATE latin1_swedish_ci)) |
+------------------------------------------------------+
| 41414242                                             |
+------------------------------------------------------+

1990

Additional Resources

mysql> SELECT HEX(WEIGHT_STRING(BINARY 'AaBb'));
+-----------------------------------+
| HEX(WEIGHT_STRING(BINARY 'AaBb')) |
+-----------------------------------+
| 41614262                          |
+-----------------------------------+

MySQL supports several collation implementations, as discussed in Section 12.14.1, “Collation
Implementation Types”. Some of these can be added to MySQL without recompiling:

• Simple collations for 8-bit character sets.

• UCA-based collations for Unicode character sets.

• Binary (xxx_bin) collations.

The following sections describe how to add user-defined collations of the first two types to existing
character sets. All existing character sets already have a binary collation, so there is no need here to
describe how to add one.

Warning

Redefining built-in collations is not supported and may result in unexpected
server behavior.

Summary of the procedure for adding a new user-defined collation:

1. Choose a collation ID.

2. Add configuration information that names the collation and describes the character-ordering rules.

3. Restart the server.

4. Verify that the server recognizes the collation.

The instructions here cover only user-defined collations that can be added without recompiling MySQL.
To add a collation that does require recompiling (as implemented by means of functions in a C source
file), use the instructions in Section 12.13, “Adding a Character Set”. However, instead of adding all
the information required for a complete character set, just modify the appropriate files for an existing
character set. That is, based on what is already present for the character set's current collations, add
data structures, functions, and configuration information for the new collation.

Note

If you modify an existing user-defined collation, that may affect the ordering
of rows for indexes on columns that use the collation. In this case, rebuild
any such indexes to avoid problems such as incorrect query results. See
Section 3.14, “Rebuilding or Repairing Tables or Indexes”.

Additional Resources

• Example showing how to add a collation for full-text searches: Section 14.9.7, “Adding a User-

Defined Collation for Full-Text Indexing”

• The Unicode Collation Algorithm (UCA) specification: http://www.unicode.org/reports/tr10/

• The Locale Data Markup Language (LDML) specification: http://www.unicode.org/reports/tr35/

12.14.1 Collation Implementation Types

MySQL implements several types of collations:

Simple collations for 8-bit character sets

1991

Collation Implementation Types

This kind of collation is implemented using an array of 256 weights that defines a one-to-one mapping
from character codes to weights. latin1_swedish_ci is an example. It is a case-insensitive
collation, so the uppercase and lowercase versions of a character have the same weights and they
compare as equal.

mysql> SET NAMES 'latin1' COLLATE 'latin1_swedish_ci';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT HEX(WEIGHT_STRING('a')), HEX(WEIGHT_STRING('A'));
+-------------------------+-------------------------+
| HEX(WEIGHT_STRING('a')) | HEX(WEIGHT_STRING('A')) |
+-------------------------+-------------------------+
| 41                      | 41                      |
+-------------------------+-------------------------+
1 row in set (0.01 sec)

mysql> SELECT 'a' = 'A';
+-----------+
| 'a' = 'A' |
+-----------+
|         1 |
+-----------+
1 row in set (0.12 sec)

For implementation instructions, see Section 12.14.3, “Adding a Simple Collation to an 8-Bit Character
Set”.

Complex collations for 8-bit character sets

This kind of collation is implemented using functions in a C source file that define how to order
characters, as described in Section 12.13, “Adding a Character Set”.

Collations for non-Unicode multibyte character sets

For this type of collation, 8-bit (single-byte) and multibyte characters are handled differently. For 8-bit
characters, character codes map to weights in case-insensitive fashion. (For example, the single-byte
characters 'a' and 'A' both have a weight of 0x41.) For multibyte characters, there are two types of
relationship between character codes and weights:

• Weights equal character codes. sjis_japanese_ci is an example of this kind of collation. The

multibyte character 'ぢ' has a character code of 0x82C0, and the weight is also 0x82C0.

mysql> CREATE TABLE t1
       (c1 VARCHAR(2) CHARACTER SET sjis COLLATE sjis_japanese_ci);
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO t1 VALUES ('a'),('A'),(0x82C0);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT c1, HEX(c1), HEX(WEIGHT_STRING(c1)) FROM t1;
+------+---------+------------------------+
| c1   | HEX(c1) | HEX(WEIGHT_STRING(c1)) |
+------+---------+------------------------+
| a    | 61      | 41                     |
| A    | 41      | 41                     |
| ぢ    | 82C0    | 82C0                   |
+------+---------+------------------------+
3 rows in set (0.00 sec)

• Character codes map one-to-one to weights, but a code is not necessarily equal to the weight.
gbk_chinese_ci is an example of this kind of collation. The multibyte character '膰' has a
character code of 0x81B0 but a weight of 0xC286.

mysql> CREATE TABLE t1
       (c1 VARCHAR(2) CHARACTER SET gbk COLLATE gbk_chinese_ci);
Query OK, 0 rows affected (0.33 sec)

1992

Collation Implementation Types

mysql> INSERT INTO t1 VALUES ('a'),('A'),(0x81B0);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT c1, HEX(c1), HEX(WEIGHT_STRING(c1)) FROM t1;
+------+---------+------------------------+
| c1   | HEX(c1) | HEX(WEIGHT_STRING(c1)) |
+------+---------+------------------------+
| a    | 61      | 41                     |
| A    | 41      | 41                     |
| 膰    | 81B0    | C286                   |
+------+---------+------------------------+
3 rows in set (0.00 sec)

For implementation instructions, see Section 12.13, “Adding a Character Set”.

Collations for Unicode multibyte character sets

Some of these collations are based on the Unicode Collation Algorithm (UCA), others are not.

Non-UCA collations have a one-to-one mapping from character code to weight. In MySQL, such
collations are case-insensitive and accent-insensitive. utf8mb4_general_ci is an example: 'a',
'A', 'À', and 'á' each have different character codes but all have a weight of 0x0041 and compare
as equal.

mysql> SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1
       (c1 CHAR(1) CHARACTER SET UTF8MB4 COLLATE utf8mb4_general_ci);
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO t1 VALUES ('a'),('A'),('À'),('á');
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT c1, HEX(c1), HEX(WEIGHT_STRING(c1)) FROM t1;
+------+---------+------------------------+
| c1   | HEX(c1) | HEX(WEIGHT_STRING(c1)) |
+------+---------+------------------------+
| a    | 61      | 0041                   |
| A    | 41      | 0041                   |
| À    | C380    | 0041                   |
| á    | C3A1    | 0041                   |
+------+---------+------------------------+
4 rows in set (0.00 sec)

UCA-based collations in MySQL have these properties:

• If a character has weights, each weight uses 2 bytes (16 bits).

• A character may have zero weights (or an empty weight). In this case, the character is ignorable.

Example: "U+0000 NULL" does not have a weight and is ignorable.

• A character may have one weight. Example: 'a' has a weight of 0x0E33.

mysql> SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
Query OK, 0 rows affected (0.05 sec)

mysql> SELECT HEX('a'), HEX(WEIGHT_STRING('a'));
+----------+-------------------------+
| HEX('a') | HEX(WEIGHT_STRING('a')) |
+----------+-------------------------+
| 61       | 0E33                    |
+----------+-------------------------+
1 row in set (0.02 sec)

• A character may have many weights. This is an expansion. Example: The German letter 'ß' (SZ

ligature, or SHARP S) has a weight of 0x0FEA0FEA.

1993

Choosing a Collation ID

mysql> SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT HEX('ß'), HEX(WEIGHT_STRING('ß'));
+-----------+--------------------------+
| HEX('ß')  | HEX(WEIGHT_STRING('ß'))  |
+-----------+--------------------------+
| C39F      | 0FEA0FEA                 |
+-----------+--------------------------+
1 row in set (0.00 sec)

• Many characters may have one weight. This is a contraction. Example: 'ch' is a single letter in

Czech and has a weight of 0x0EE2.

mysql> SET NAMES 'utf8mb4' COLLATE 'utf8mb4_czech_ci';
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT HEX('ch'), HEX(WEIGHT_STRING('ch'));
+-----------+--------------------------+
| HEX('ch') | HEX(WEIGHT_STRING('ch')) |
+-----------+--------------------------+
| 6368      | 0EE2                     |
+-----------+--------------------------+
1 row in set (0.00 sec)

A many-characters-to-many-weights mapping is also possible (this is contraction with expansion), but
is not supported by MySQL.

For implementation instructions, for a non-UCA collation, see Section 12.13, “Adding a Character Set”.
For a UCA collation, see Section 12.14.4, “Adding a UCA Collation to a Unicode Character Set”.

Miscellaneous collations

There are also a few collations that do not fall into any of the previous categories.

12.14.2 Choosing a Collation ID

Each collation must have a unique ID. To add a collation, you must choose an ID value that is not
currently used. MySQL supports two-byte collation IDs. The range of IDs from 1024 to 2047 is reserved
for user-defined collations.

The collation ID that you choose appears in these contexts:

• The ID column of the Information Schema COLLATIONS table.

• The Id column of SHOW COLLATION output.

• The charsetnr member of the MYSQL_FIELD C API data structure.

• The number member of the MY_CHARSET_INFO data structure returned by the

mysql_get_character_set_info() C API function.

To determine the largest currently used ID, issue the following statement:

mysql> SELECT MAX(ID) FROM INFORMATION_SCHEMA.COLLATIONS;
+---------+
| MAX(ID) |
+---------+
|     247 |
+---------+

To display a list of all currently used IDs, issue this statement:

mysql> SELECT ID FROM INFORMATION_SCHEMA.COLLATIONS ORDER BY ID;
+-----+
| ID  |

1994

Adding a Simple Collation to an 8-Bit Character Set

+-----+
|   1 |
|   2 |
| ... |
|  52 |
|  53 |
|  57 |
|  58 |
| ... |
|  98 |
|  99 |
| 128 |
| 129 |
| ... |
| 247 |
+-----+

Warning

Before upgrading, you should save the configuration files that you change. If
you upgrade in place, the process replaces the modified files.

12.14.3 Adding a Simple Collation to an 8-Bit Character Set

This section describes how to add a simple collation for an 8-bit character set by writing the
<collation> elements associated with a <charset> character set description in the MySQL
Index.xml file. The procedure described here does not require recompiling MySQL. The example
adds a collation named latin1_test_ci to the latin1 character set.

1. Choose a collation ID, as shown in Section 12.14.2, “Choosing a Collation ID”. The following steps

use an ID of 1024.

2. Modify the Index.xml and latin1.xml configuration files. These files are located in the directory

named by the character_sets_dir system variable. You can check the variable value as
follows, although the path name might be different on your system:

mysql> SHOW VARIABLES LIKE 'character_sets_dir';
+--------------------+-----------------------------------------+
| Variable_name      | Value                                   |
+--------------------+-----------------------------------------+
| character_sets_dir | /user/local/mysql/share/mysql/charsets/ |
+--------------------+-----------------------------------------+

3. Choose a name for the collation and list it in the Index.xml file. Find the <charset> element

for the character set to which the collation is being added, and add a <collation> element that
indicates the collation name and ID, to associate the name with the ID. For example:

<charset name="latin1">
  ...
  <collation name="latin1_test_ci" id="1024"/>
  ...
</charset>

4.

In the latin1.xml configuration file, add a <collation> element that names the collation and
that contains a <map> element that defines a character code-to-weight mapping table for character
codes 0 to 255. Each value within the <map> element must be a number in hexadecimal format.

<collation name="latin1_test_ci">
<map>
 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F
 20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
 30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F
 40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
 50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F
 60 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
 50 51 52 53 54 55 56 57 58 59 5A 7B 7C 7D 7E 7F

1995

Adding a UCA Collation to a Unicode Character Set

 80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F
 90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F
 A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF
 B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF
 41 41 41 41 5B 5D 5B 43 45 45 45 45 49 49 49 49
 44 4E 4F 4F 4F 4F 5C D7 5C 55 55 55 59 59 DE DF
 41 41 41 41 5B 5D 5B 43 45 45 45 45 49 49 49 49
 44 4E 4F 4F 4F 4F 5C F7 5C 55 55 55 59 59 DE FF
</map>
</collation>

5. Restart the server and use this statement to verify that the collation is present:

mysql> SHOW COLLATION WHERE Collation = 'latin1_test_ci';
+----------------+---------+------+---------+----------+---------+
| Collation      | Charset | Id   | Default | Compiled | Sortlen |
+----------------+---------+------+---------+----------+---------+
| latin1_test_ci | latin1  | 1024 |         |          |       1 |
+----------------+---------+------+---------+----------+---------+

12.14.4 Adding a UCA Collation to a Unicode Character Set

This section describes how to add a UCA collation for a Unicode character set by writing the
<collation> element within a <charset> character set description in the MySQL Index.xml file.
The procedure described here does not require recompiling MySQL. It uses a subset of the Locale
Data Markup Language (LDML) specification, which is available at http://www.unicode.org/reports/tr35/.
With this method, you need not define the entire collation. Instead, you begin with an existing “base”
collation and describe the new collation in terms of how it differs from the base collation. The following
table lists the base collations of the Unicode character sets for which UCA collations can be defined. It
is not possible to create user-defined UCA collations for utf16le; there is no utf16le_unicode_ci
collation that would serve as the basis for such collations.

Table 12.4 MySQL Character Sets Available for User-Defined UCA Collations

Character Set

utf8mb4

ucs2

utf16

utf32

Base Collation

utf8mb4_unicode_ci

ucs2_unicode_ci

utf16_unicode_ci

utf32_unicode_ci

The following sections show how to add a collation that is defined using LDML syntax, and provide a
summary of LDML rules supported in MySQL.

12.14.4.1 Defining a UCA Collation Using LDML Syntax

To add a UCA collation for a Unicode character set without recompiling MySQL, use the
following procedure. If you are unfamiliar with the LDML rules used to describe the collation's sort
characteristics, see Section 12.14.4.2, “LDML Syntax Supported in MySQL”.

The example adds a collation named utf8mb4_phone_ci to the utf8mb4 character set. The
collation is designed for a scenario involving a Web application for which users post their names and
phone numbers. Phone numbers can be given in very different formats:

+7-12345-67
+7-12-345-67
+7 12 345 67
+7 (12) 345 67
+71234567

The problem raised by dealing with these kinds of values is that the varying permissible formats make
searching for a specific phone number very difficult. The solution is to define a new collation that
reorders punctuation characters, making them ignorable.

1996

Adding a UCA Collation to a Unicode Character Set

1. Choose a collation ID, as shown in Section 12.14.2, “Choosing a Collation ID”. The following steps

use an ID of 1029.

2. To modify the Index.xml configuration file. This file is located in the directory named by the

character_sets_dir system variable. You can check the variable value as follows, although the
path name might be different on your system:

mysql> SHOW VARIABLES LIKE 'character_sets_dir';
+--------------------+-----------------------------------------+
| Variable_name      | Value                                   |
+--------------------+-----------------------------------------+
| character_sets_dir | /user/local/mysql/share/mysql/charsets/ |
+--------------------+-----------------------------------------+

3. Choose a name for the collation and list it in the Index.xml file. In addition, you must provide the
collation ordering rules. Find the <charset> element for the character set to which the collation
is being added, and add a <collation> element that indicates the collation name and ID, to
associate the name with the ID. Within the <collation> element, provide a <rules> element
containing the ordering rules:

<charset name="utf8mb4">
  ...
  <collation name="utf8mb4_phone_ci" id="1029">
    <rules>
      <reset>\u0000</reset>
      <i>\u0020</i> <!-- space -->
      <i>\u0028</i> <!-- left parenthesis -->
      <i>\u0029</i> <!-- right parenthesis -->
      <i>\u002B</i> <!-- plus -->
      <i>\u002D</i> <!-- hyphen -->
    </rules>
  </collation>
  ...
</charset>

4.

If you want a similar collation for other Unicode character sets, add other <collation> elements.
For example, to define ucs2_phone_ci, add a <collation> element to the <charset
name="ucs2"> element. Remember that each collation must have its own unique ID.

5. Restart the server and use this statement to verify that the collation is present:

mysql> SHOW COLLATION WHERE Collation = 'utf8mb4_phone_ci';
+------------------+---------+------+---------+----------+---------+
| Collation        | Charset | Id   | Default | Compiled | Sortlen |
+------------------+---------+------+---------+----------+---------+
| utf8mb4_phone_ci | utf8mb4 | 1029 |         |          |       8 |
+------------------+---------+------+---------+----------+---------+

Now test the collation to make sure that it has the desired properties.

Create a table containing some sample phone numbers using the new collation:

mysql> CREATE TABLE phonebook (
         name VARCHAR(64),
         phone VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_phone_ci
       );
Query OK, 0 rows affected (0.09 sec)

mysql> INSERT INTO phonebook VALUES ('Svoj','+7 912 800 80 02');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO phonebook VALUES ('Hf','+7 (912) 800 80 04');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO phonebook VALUES ('Bar','+7-912-800-80-01');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO phonebook VALUES ('Ramil','(7912) 800 80 03');
Query OK, 1 row affected (0.00 sec)

1997

Adding a UCA Collation to a Unicode Character Set

mysql> INSERT INTO phonebook VALUES ('Sanja','+380 (912) 8008005');
Query OK, 1 row affected (0.00 sec)

Run some queries to see whether the ignored punctuation characters are in fact ignored for
comparison and sorting:

mysql> SELECT * FROM phonebook ORDER BY phone;
+-------+--------------------+
| name  | phone              |
+-------+--------------------+
| Sanja | +380 (912) 8008005 |
| Bar   | +7-912-800-80-01   |
| Svoj  | +7 912 800 80 02   |
| Ramil | (7912) 800 80 03   |
| Hf    | +7 (912) 800 80 04 |
+-------+--------------------+
5 rows in set (0.00 sec)

mysql> SELECT * FROM phonebook WHERE phone='+7(912)800-80-01';
+------+------------------+
| name | phone            |
+------+------------------+
| Bar  | +7-912-800-80-01 |
+------+------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM phonebook WHERE phone='79128008001';
+------+------------------+
| name | phone            |
+------+------------------+
| Bar  | +7-912-800-80-01 |
+------+------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM phonebook WHERE phone='7 9 1 2 8 0 0 8 0 0 1';
+------+------------------+
| name | phone            |
+------+------------------+
| Bar  | +7-912-800-80-01 |
+------+------------------+
1 row in set (0.00 sec)

12.14.4.2 LDML Syntax Supported in MySQL

This section describes the LDML syntax that MySQL recognizes. This is a subset of the syntax
described in the LDML specification available at http://www.unicode.org/reports/tr35/, which should
be consulted for further information. MySQL recognizes a large enough subset of the syntax that, in
many cases, it is possible to download a collation definition from the Unicode Common Locale Data
Repository and paste the relevant part (that is, the part between the <rules> and </rules> tags)
into the MySQL Index.xml file. The rules described here are all supported except that character
sorting occurs only at the primary level. Rules that specify differences at secondary or higher sort levels
are recognized (and thus can be included in collation definitions) but are treated as equality at the
primary level.

The MySQL server generates diagnostics when it finds problems while parsing the Index.xml file.
See Section 12.14.4.3, “Diagnostics During Index.xml Parsing”.

Character Representation

Characters named in LDML rules can be written literally or in \unnnn format, where nnnn is the
hexadecimal Unicode code point value. For example, A and á can be written literally or as \u0041
and \u00E1. Within hexadecimal values, the digits A through F are not case-sensitive; \u00E1
and \u00e1 are equivalent. For UCA 4.0.0 collations, hexadecimal notation can be used only for
characters in the Basic Multilingual Plane, not for characters outside the BMP range of 0000 to FFFF.
For UCA 5.2.0 collations, hexadecimal notation can be used for any character.

1998

Adding a UCA Collation to a Unicode Character Set

The Index.xml file itself should be written using UTF-8 encoding.

Syntax Rules

LDML has reset rules and shift rules to specify character ordering. Orderings are given as a set of rules
that begin with a reset rule that establishes an anchor point, followed by shift rules that indicate how
characters sort relative to the anchor point.

• A <reset> rule does not specify any ordering in and of itself. Instead, it “resets” the ordering for
subsequent shift rules to cause them to be taken in relation to a given character. Either of the
following rules resets subsequent shift rules to be taken in relation to the letter 'A':

<reset>A</reset>

<reset>\u0041</reset>

• The <p>, <s>, and <t> shift rules define primary, secondary, and tertiary differences of a character

from another character:

• Use primary differences to distinguish separate letters.

• Use secondary differences to distinguish accent variations.

• Use tertiary differences to distinguish lettercase variations.

Either of these rules specifies a primary shift rule for the 'G' character:

<p>G</p>

<p>\u0047</p>

• The <i> shift rule indicates that one character sorts identically to another. The following rules cause

'b' to sort the same as 'a':

<reset>a</reset>
<i>b</i>

• Abbreviated shift syntax specifies multiple shift rules using a single pair of tags. The following table
shows the correspondence between abbreviated syntax rules and the equivalent nonabbreviated
rules.

Table 12.5 Abbreviated Shift Syntax

Abbreviated Syntax

<pc>xyz</pc>

<sc>xyz</sc>

<tc>xyz</tc>

<ic>xyz</ic>

Nonabbreviated Syntax

<p>x</p><p>y</p><p>z</p>

<s>x</s><s>y</s><s>z</s>

<t>x</t><t>y</t><t>z</t>

<i>x</i><i>y</i><i>z</i>

• An expansion is a reset rule that establishes an anchor point for a multiple-character sequence.
MySQL supports expansions 2 to 6 characters long. The following rules put 'z' greater at the
primary level than the sequence of three characters 'abc':

<reset>abc</reset>
<p>z</p>

• A contraction is a shift rule that sorts a multiple-character sequence. MySQL supports contractions 2
to 6 characters long. The following rules put the sequence of three characters 'xyz' greater at the
primary level than 'a':

<reset>a</reset>
<p>xyz</p>

1999

Adding a UCA Collation to a Unicode Character Set

• Long expansions and long contractions can be used together. These rules put the sequence of three

characters 'xyz' greater at the primary level than the sequence of three characters 'abc':

<reset>abc</reset>
<p>xyz</p>

• Normal expansion syntax uses <x> plus <extend> elements to specify an expansion. The following
rules put the character 'k' greater at the secondary level than the sequence 'ch'. That is, 'k'
behaves as if it expands to a character after 'c' followed by 'h':

<reset>c</reset>
<x><s>k</s><extend>h</extend></x>

This syntax permits long sequences. These rules sort the sequence 'ccs' greater at the tertiary
level than the sequence 'cscs':

<reset>cs</reset>
<x><t>ccs</t><extend>cs</extend></x>

The LDML specification describes normal expansion syntax as “tricky.” See that specification for
details.

• Previous context syntax uses <x> plus <context> elements to specify that the context before a

character affects how it sorts. The following rules put '-' greater at the secondary level than 'a',
but only when '-' occurs after 'b':

<reset>a</reset>
<x><context>b</context><s>-</s></x>

• Previous context syntax can include the <extend> element. These rules put 'def' greater at the

primary level than 'aghi', but only when 'def' comes after 'abc':

<reset>a</reset>
<x><context>abc</context><p>def</p><extend>ghi</extend></x>

• Reset rules permit a before attribute. Normally, shift rules after a reset rule indicate characters

that sort after the reset character. Shift rules after a reset rule that has the before attribute indicate
characters that sort before the reset character. The following rules put the character 'b' immediately
before 'a' at the primary level:

<reset before="primary">a</reset>
<p>b</p>

Permissible before attribute values specify the sort level by name or the equivalent numeric value:

<reset before="primary">
<reset before="1">

<reset before="secondary">
<reset before="2">

<reset before="tertiary">
<reset before="3">

• A reset rule can name a logical reset position rather than a literal character:

<first_tertiary_ignorable/>
<last_tertiary_ignorable/>
<first_secondary_ignorable/>
<last_secondary_ignorable/>
<first_primary_ignorable/>
<last_primary_ignorable/>
<first_variable/>
<last_variable/>
<first_non_ignorable/>
<last_non_ignorable/>
<first_trailing/>
<last_trailing/>

2000

Adding a UCA Collation to a Unicode Character Set

These rules put 'z' greater at the primary level than nonignorable characters that have a Default
Unicode Collation Element Table (DUCET) entry and that are not CJK:

<reset><last_non_ignorable/></reset>
<p>z</p>

Logical positions have the code points shown in the following table.

Table 12.6 Logical Reset Position Code Points

Logical Position

Unicode 4.0.0 Code Point

Unicode 5.2.0 Code Point

<first_non_ignorable/>

U+02D0

<last_non_ignorable/>

U+A48C

<first_primary_ignorable/
>

U+0332

<last_primary_ignorable/
>

U+20EA

<first_secondary_ignorable/
>

U+0000

<last_secondary_ignorable/
>

U+FE73

<first_tertiary_ignorable/
>

U+0000

<last_tertiary_ignorable/
>

U+FE73

<first_trailing/>

<last_trailing/>

<first_variable/>

<last_variable/>

U+0000

U+0000

U+0009

U+2183

U+02D0

U+1342E

U+0332

U+101FD

U+0000

U+FE73

U+0000

U+FE73

U+0000

U+0000

U+0009

U+1D371

• The <collation> element permits a shift-after-method attribute that affects character weight

calculation for shift rules. The attribute has these permitted values:

• simple: Calculate character weights as for reset rules that do not have a before attribute. This is

the default if the attribute is not given.

• expand: Use expansions for shifts after reset rules.

Suppose that '0' and '1' have weights of 0E29 and 0E2A and we want to put all basic Latin letters
between '0' and '1':

<reset>0</reset>
<pc>abcdefghijklmnopqrstuvwxyz</pc>

For simple shift mode, weights are calculated as follows:

'a' has weight 0E29+1
'b' has weight 0E29+2
'c' has weight 0E29+3
...

However, there are not enough vacant positions to put 26 characters between '0' and '1'. The
result is that digits and letters are intermixed.

To solve this, use shift-after-method="expand". Then weights are calculated like this:

'a' has weight [0E29][233D+1]

2001

Character Set Configuration

'b' has weight [0E29][233D+2]
'c' has weight [0E29][233D+3]
...

233D is the UCA 4.0.0 weight for character 0xA48C, which is the last nonignorable character (a sort
of the greatest character in the collation, excluding CJK). UCA 5.2.0 is similar but uses 3ACA, for
character 0x1342E.

MySQL-Specific LDML Extensions

An extension to LDML rules permits the <collation> element to include an optional version
attribute in <collation> tags to indicate the UCA version on which the collation is based. If the
version attribute is omitted, its default value is 4.0.0. For example, this specification indicates a
collation that is based on UCA 5.2.0:

<collation id="nnn" name="utf8mb4_xxx_ci" version="5.2.0">
...
</collation>

12.14.4.3 Diagnostics During Index.xml Parsing

The MySQL server generates diagnostics when it finds problems while parsing the Index.xml file:

• Unknown tags are written to the error log. For example, the following message results if a collation

definition contains a <aaa> tag:

[Warning] Buffered warning: Unknown LDML tag:
'charsets/charset/collation/rules/aaa'

• If collation initialization is not possible, the server reports an “Unknown collation” error, and also

generates warnings explaining the problems, such as in the previous example. In other cases, when
a collation description is generally correct but contains some unknown tags, the collation is initialized
and is available for use. The unknown parts are ignored, but a warning is generated in the error log.

• Problems with collations generate warnings that clients can display with SHOW WARNINGS. Suppose
that a reset rule contains an expansion longer than the maximum supported length of 6 characters:

<reset>abcdefghi</reset>
<i>x</i>

An attempt to use the collation produces warnings:

mysql> SELECT _utf8mb4'test' COLLATE utf8mb4_test_ci;
ERROR 1273 (HY000): Unknown collation: 'utf8mb4_test_ci'
mysql> SHOW WARNINGS;
+---------+------+----------------------------------------+
| Level   | Code | Message                                |
+---------+------+----------------------------------------+
| Error   | 1273 | Unknown collation: 'utf8mb4_test_ci'   |
| Warning | 1273 | Expansion is too long at 'abcdefghi=x' |
+---------+------+----------------------------------------+

12.15 Character Set Configuration

The MySQL server has a compiled-in default character set and collation. To change these defaults,
use the --character-set-server and --collation-server options when you start the server.
See Section 7.1.7, “Server Command Options”. The collation must be a legal collation for the default
character set. To determine which collations are available for each character set, use the SHOW
COLLATION statement or query the INFORMATION_SCHEMA COLLATIONS table.

If you try to use a character set that is not compiled into your binary, you might run into the following
problems:

• If your program uses an incorrect path to determine where the character sets are stored (which is

typically the share/mysql/charsets or share/charsets directory under the MySQL installation

2002

MySQL Server Locale Support

directory), this can be fixed by using the --character-sets-dir option when you run the
program. For example, to specify a directory to be used by MySQL client programs, list it in the
[client] group of your option file. The examples given here show what the setting might look like
for Unix or Windows, respectively:

[client]
character-sets-dir=/usr/local/mysql/share/mysql/charsets

[client]
character-sets-dir="C:/Program Files/MySQL/MySQL Server 8.4/share/charsets"

• If the character set is a complex character set that cannot be loaded dynamically, you must

recompile the program with support for the character set.

For Unicode character sets, you can define collations without recompiling by using LDML notation.
See Section 12.14.4, “Adding a UCA Collation to a Unicode Character Set”.

• If the character set is a dynamic character set, but you do not have a configuration file for it, you

should install the configuration file for the character set from a new MySQL distribution.

• If your character set index file (Index.xml) does not contain the name for the character set, your

program displays an error message:

Character set 'charset_name' is not a compiled character set and is not
specified in the '/usr/share/mysql/charsets/Index.xml' file

To solve this problem, you should either get a new index file or manually add the name of any
missing character sets to the current file.

You can force client programs to use specific character set as follows:

[client]
default-character-set=charset_name

This is normally unnecessary. However, when character_set_system differs from
character_set_server or character_set_client, and you input characters manually (as
database object identifiers, column values, or both), these may be displayed incorrectly in output from
the client or the output itself may be formatted incorrectly. In such cases, starting the mysql client with
--default-character-set=system_character_set—that is, setting the client character set to
match the system character set—should fix the problem.

12.16 MySQL Server Locale Support

The locale indicated by the lc_time_names system variable controls the language used to display
day and month names and abbreviations. This variable affects the output from the DATE_FORMAT(),
DAYNAME(), and MONTHNAME() functions.

lc_time_names does not affect the STR_TO_DATE() or GET_FORMAT() function.

The lc_time_names value does not affect the result from FORMAT(), but this function takes an
optional third parameter that enables a locale to be specified to be used for the result number's decimal
point, thousands separator, and grouping between separators. Permissible locale values are the same
as the legal values for the lc_time_names system variable.

Locale names have language and region subtags listed by IANA (http://www.iana.org/assignments/
language-subtag-registry) such as 'ja_JP' or 'pt_BR'. The default value is 'en_US' regardless
of your system's locale setting, but you can set the value at server startup, or set the GLOBAL value at
runtime if you have privileges sufficient to set global system variables; see Section 7.1.9.1, “System
Variable Privileges”. Any client can examine the value of lc_time_names or set its SESSION value to
affect the locale for its own connection.

(The first SET NAMES statement in the following example may not be necessary if no settings relating
to character set and collation have been changed from their defaults; we include it for completeness.)

2003

MySQL Server Locale Support

mysql> SET NAMES 'utf8mb4';
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT @@lc_time_names;
+-----------------+
| @@lc_time_names |
+-----------------+
| en_US           |
+-----------------+
1 row in set (0.00 sec)

mysql> SELECT DAYNAME('2020-01-01'), MONTHNAME('2020-01-01');
+-----------------------+-------------------------+
| DAYNAME('2020-01-01') | MONTHNAME('2020-01-01') |
+-----------------------+-------------------------+
| Wednesday             | January                 |
+-----------------------+-------------------------+
1 row in set (0.00 sec)

mysql> SELECT DATE_FORMAT('2020-01-01','%W %a %M %b');
+-----------------------------------------+
| DATE_FORMAT('2020-01-01','%W %a %M %b') |
+-----------------------------------------+
| Wednesday Wed January Jan               |
+-----------------------------------------+
1 row in set (0.00 sec)

mysql> SET lc_time_names = 'es_MX';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @@lc_time_names;
+-----------------+
| @@lc_time_names |
+-----------------+
| es_MX           |
+-----------------+
1 row in set (0.00 sec)

mysql> SELECT DAYNAME('2020-01-01'), MONTHNAME('2020-01-01');
+-----------------------+-------------------------+
| DAYNAME('2020-01-01') | MONTHNAME('2020-01-01') |
+-----------------------+-------------------------+
| miércoles             | enero                   |
+-----------------------+-------------------------+
1 row in set (0.00 sec)

mysql> SELECT DATE_FORMAT('2020-01-01','%W %a %M %b');
+-----------------------------------------+
| DATE_FORMAT('2020-01-01','%W %a %M %b') |
+-----------------------------------------+
| miércoles mié enero ene                 |
+-----------------------------------------+
1 row in set (0.00 sec)

The day or month name for each of the affected functions is converted from utf8mb4 to the character
set indicated by the character_set_connection system variable.

lc_time_names may be set to any of the following locale values. The set of locales supported by
MySQL may differ from those supported by your operating system.

Locale Value

Meaning

ar_AE

ar_BH

ar_DZ

ar_EG

ar_IN

ar_IQ

2004

Arabic - United Arab Emirates

Arabic - Bahrain

Arabic - Algeria

Arabic - Egypt

Arabic - India

Arabic - Iraq

Locale Value

ar_JO

ar_KW

ar_LB

ar_LY

ar_MA

ar_OM

ar_QA

ar_SA

ar_SD

ar_SY

ar_TN

ar_YE

be_BY

bg_BG

ca_ES

cs_CZ

da_DK

de_AT

de_BE

de_CH

de_DE

de_LU

el_GR

en_AU

en_CA

en_GB

en_IN

en_NZ

en_PH

en_US

en_ZA

en_ZW

es_AR

es_BO

es_CL

es_CO

es_CR

es_DO

es_EC

es_ES

es_GT

MySQL Server Locale Support

Meaning

Arabic - Jordan

Arabic - Kuwait

Arabic - Lebanon

Arabic - Libya

Arabic - Morocco

Arabic - Oman

Arabic - Qatar

Arabic - Saudi Arabia

Arabic - Sudan

Arabic - Syria

Arabic - Tunisia

Arabic - Yemen

Belarusian - Belarus

Bulgarian - Bulgaria

Catalan - Spain

Czech - Czech Republic

Danish - Denmark

German - Austria

German - Belgium

German - Switzerland

German - Germany

German - Luxembourg

Greek - Greece

English - Australia

English - Canada

English - United Kingdom

English - India

English - New Zealand

English - Philippines

English - United States

English - South Africa

English - Zimbabwe

Spanish - Argentina

Spanish - Bolivia

Spanish - Chile

Spanish - Colombia

Spanish - Costa Rica

Spanish - Dominican Republic

Spanish - Ecuador

Spanish - Spain

Spanish - Guatemala

2005

MySQL Server Locale Support

Meaning

Spanish - Honduras

Spanish - Mexico

Spanish - Nicaragua

Spanish - Panama

Spanish - Peru

Spanish - Puerto Rico

Spanish - Paraguay

Spanish - El Salvador

Spanish - United States

Spanish - Uruguay

Spanish - Venezuela

Estonian - Estonia

Basque - Spain

Finnish - Finland

Faroese - Faroe Islands

French - Belgium

French - Canada

French - Switzerland

French - France

French - Luxembourg

Galician - Spain

Gujarati - India

Hebrew - Israel

Hindi - India

Croatian - Croatia

Hungarian - Hungary

Indonesian - Indonesia

Icelandic - Iceland

Italian - Switzerland

Italian - Italy

Japanese - Japan

Korean - Republic of Korea

Lithuanian - Lithuania

Latvian - Latvia

Macedonian - North Macedonia

Mongolia - Mongolian

Malay - Malaysia

Norwegian(Bokmål) - Norway

Dutch - Belgium

Dutch - The Netherlands

Norwegian - Norway

Locale Value

es_HN

es_MX

es_NI

es_PA

es_PE

es_PR

es_PY

es_SV

es_US

es_UY

es_VE

et_EE

eu_ES

fi_FI

fo_FO

fr_BE

fr_CA

fr_CH

fr_FR

fr_LU

gl_ES

gu_IN

he_IL

hi_IN

hr_HR

hu_HU

id_ID

is_IS

it_CH

it_IT

ja_JP

ko_KR

lt_LT

lv_LV

mk_MK

mn_MN

ms_MY

nb_NO

nl_BE

nl_NL

no_NO

2006

Locale Value

pl_PL

pt_BR

pt_PT

rm_CH

ro_RO

ru_RU

ru_UA

sk_SK

sl_SI

sq_AL

sr_RS

sv_FI

sv_SE

ta_IN

te_IN

th_TH

tr_TR

uk_UA

ur_PK

vi_VN

zh_CN

zh_HK

zh_TW

MySQL Server Locale Support

Meaning

Polish - Poland

Portugese - Brazil

Portugese - Portugal

Romansh - Switzerland

Romanian - Romania

Russian - Russia

Russian - Ukraine

Slovak - Slovakia

Slovenian - Slovenia

Albanian - Albania

Serbian - Serbia

Swedish - Finland

Swedish - Sweden

Tamil - India

Telugu - India

Thai - Thailand

Turkish - Turkey

Ukrainian - Ukraine

Urdu - Pakistan

Vietnamese - Vietnam

Chinese - China

Chinese - Hong Kong

Chinese - Taiwan

2007

2008

