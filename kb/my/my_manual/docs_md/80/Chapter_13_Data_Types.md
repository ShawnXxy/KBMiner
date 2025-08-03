Numeric Data Types

• For integer types, M indicates the maximum display width. For floating-point and fixed-point types,

M is the total number of digits that can be stored (the precision). For string types, M is the maximum
length. The maximum permissible value of M depends on the data type.

•     D applies to floating-point and fixed-point types and indicates the number of digits following the
decimal point (the scale). The maximum possible value is 30, but should be no greater than M−2.

• fsp applies to the TIME, DATETIME, and TIMESTAMP types and represents fractional seconds

precision; that is, the number of digits following the decimal point for fractional parts of seconds. The
fsp value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional part.
If omitted, the default precision is 0. (This differs from the standard SQL default of 6, for compatibility
with previous MySQL versions.)

• Square brackets ([ and ]) indicate optional parts of type definitions.

13.1 Numeric Data Types

MySQL supports all standard SQL numeric data types. These types include the exact numeric data
types (INTEGER, SMALLINT, DECIMAL, and NUMERIC), as well as the approximate numeric data
types (FLOAT, REAL, and DOUBLE PRECISION). The keyword INT is a synonym for INTEGER, and
the keywords DEC and FIXED are synonyms for DECIMAL. MySQL treats DOUBLE as a synonym for
DOUBLE PRECISION (a nonstandard extension). MySQL also treats REAL as a synonym for DOUBLE
PRECISION (a nonstandard variation), unless the REAL_AS_FLOAT SQL mode is enabled.

The BIT data type stores bit values and is supported for MyISAM, MEMORY, InnoDB, and NDB tables.

For information about how MySQL handles assignment of out-of-range values to columns and overflow
during expression evaluation, see Section 13.1.7, “Out-of-Range and Overflow Handling”.

For information about storage requirements of the numeric data types, see Section 13.7, “Data Type
Storage Requirements”.

For descriptions of functions that operate on numeric values, see Section 14.6, “Numeric Functions
and Operators”. The data type used for the result of a calculation on numeric operands depends
on the types of the operands and the operations performed on them. For more information, see
Section 14.6.1, “Arithmetic Operators”.

13.1.1 Numeric Data Type Syntax

For integer data types, M indicates the minimum display width. The maximum display width is 255.
Display width is unrelated to the range of values a type can store, as described in Section 13.1.6,
“Numeric Type Attributes”.

For floating-point and fixed-point data types, M is the total number of digits that can be stored.

As of MySQL 8.0.17, the display width attribute is deprecated for integer data types; you should expect
support for it to be removed in a future version of MySQL.

If you specify ZEROFILL for a numeric column, MySQL automatically adds the UNSIGNED attribute to
the column.

As of MySQL 8.0.17, the ZEROFILL attribute is deprecated for numeric data types; you should expect
support for it to be removed in a future version of MySQL. Consider using an alternative means of
producing the effect of this attribute. For example, applications could use the LPAD() function to zero-
pad numbers up to the desired width, or they could store the formatted numbers in CHAR columns.

Numeric data types that permit the UNSIGNED attribute also permit SIGNED. However, these data types
are signed by default, so the SIGNED attribute has no effect.

2200

Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT

based on the IEEE standard. The actual range might be slightly smaller depending on your hardware
or operating system.

M is the total number of digits and D is the number of digits following the decimal point. If M and D are
omitted, values are stored to the limits permitted by the hardware. A double-precision floating-point
number is accurate to approximately 15 decimal places.

DOUBLE(M,D) is a nonstandard MySQL extension. As of MySQL 8.0.17, this syntax is deprecated
and you should expect support for it to be removed in a future version of MySQL.

UNSIGNED, if specified, disallows negative values. As of MySQL 8.0.17, the UNSIGNED attribute is
deprecated for columns of type DOUBLE (and any synonyms) and you should expect support for it to
be removed in a future version of MySQL. Consider using a simple CHECK constraint instead for such
columns.

•     DOUBLE PRECISION[(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED]

[ZEROFILL]

These types are synonyms for DOUBLE. Exception: If the REAL_AS_FLOAT SQL mode is enabled,
REAL is a synonym for FLOAT rather than DOUBLE.

13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT,
MEDIUMINT, BIGINT

MySQL supports the SQL standard integer types INTEGER (or INT) and SMALLINT. As an extension
to the standard, MySQL also supports the integer types TINYINT, MEDIUMINT, and BIGINT. The
following table shows the required storage and range for each integer type.

Table 13.1 Required Storage and Range for Integer Types Supported by MySQL

Type

Storage
(Bytes)

Minimum
Value Signed

Minimum
Value
Unsigned

Maximum
Value Signed

TINYINT

SMALLINT

MEDIUMINT

INT

BIGINT

1

2

3

4

8

-128

-32768

-8388608

0

0

0

-2147483648 0
-263

0

Maximum
Value
Unsigned

255

65535

127

32767

8388607

16777215

2147483647
263-1

4294967295
264-1

13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC

The DECIMAL and NUMERIC types store exact numeric data values. These types are used when it
is important to preserve exact precision, for example with monetary data. In MySQL, NUMERIC is
implemented as DECIMAL, so the following remarks about DECIMAL apply equally to NUMERIC.

MySQL stores DECIMAL values in binary format. See Section 14.24, “Precision Math”.

In a DECIMAL column declaration, the precision and scale can be (and usually is) specified. For
example:

salary DECIMAL(5,2)

In this example, 5 is the precision and 2 is the scale. The precision represents the number of significant
digits that are stored for values, and the scale represents the number of digits that can be stored
following the decimal point.

Standard SQL requires that DECIMAL(5,2) be able to store any value with five digits and two
decimals, so values that can be stored in the salary column range from -999.99 to 999.99.

2204

Floating-Point Types (Approximate Value) - FLOAT, DOUBLE

In standard SQL, the syntax DECIMAL(M) is equivalent to DECIMAL(M,0). Similarly, the syntax
DECIMAL is equivalent to DECIMAL(M,0), where the implementation is permitted to decide the value
of M. MySQL supports both of these variant forms of DECIMAL syntax. The default value of M is 10.

If the scale is 0, DECIMAL values contain no decimal point or fractional part.

The maximum number of digits for DECIMAL is 65, but the actual range for a given DECIMAL column
can be constrained by the precision or scale for a given column. When such a column is assigned a
value with more digits following the decimal point than are permitted by the specified scale, the value is
converted to that scale. (The precise behavior is operating system-specific, but generally the effect is
truncation to the permissible number of digits.)

13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE

The FLOAT and DOUBLE types represent approximate numeric data values. MySQL uses four bytes for
single-precision values and eight bytes for double-precision values.

For FLOAT, the SQL standard permits an optional specification of the precision (but not the range of
the exponent) in bits following the keyword FLOAT in parentheses, that is, FLOAT(p). MySQL also
supports this optional precision specification, but the precision value in FLOAT(p) is used only to
determine storage size. A precision from 0 to 23 results in a 4-byte single-precision FLOAT column. A
precision from 24 to 53 results in an 8-byte double-precision DOUBLE column.

MySQL permits a nonstandard syntax: FLOAT(M,D) or REAL(M,D) or DOUBLE PRECISION(M,D).
Here, (M,D) means than values can be stored with up to M digits in total, of which D digits may be
after the decimal point. For example, a column defined as FLOAT(7,4) is displayed as -999.9999.
MySQL performs rounding when storing values, so if you insert 999.00009 into a FLOAT(7,4)
column, the approximate result is 999.0001.

As of MySQL 8.0.17, the nonstandard FLOAT(M,D) and DOUBLE(M,D) syntax is deprecated and you
should expect support for it to be removed in a future version of MySQL.

Because floating-point values are approximate and not stored as exact values, attempts to treat them
as exact in comparisons may lead to problems. They are also subject to platform or implementation
dependencies. For more information, see Section B.3.4.8, “Problems with Floating-Point Values”.

For maximum portability, code requiring storage of approximate numeric data values should use FLOAT
or DOUBLE PRECISION with no specification of precision or number of digits.

13.1.5 Bit-Value Type - BIT

The BIT data type is used to store bit values. A type of BIT(M) enables storage of M-bit values. M can
range from 1 to 64.

To specify bit values, b'value' notation can be used. value is a binary value written using zeros and
ones. For example, b'111' and b'10000000' represent 7 and 128, respectively. See Section 11.1.5,
“Bit-Value Literals”.

If you assign a value to a BIT(M) column that is less than M bits long, the value is padded on the left
with zeros. For example, assigning a value of b'101' to a BIT(6) column is, in effect, the same as
assigning b'000101'.

NDB Cluster.
exceed 4096 bits.

 The maximum combined size of all BIT columns used in a given NDB table must not

13.1.6 Numeric Type Attributes

MySQL supports an extension for optionally specifying the display width of integer data types in
parentheses following the base keyword for the type. For example, INT(4) specifies an INT with a
display width of four digits. This optional display width may be used by applications to display integer

2205

Out-of-Range and Overflow Handling

As of MySQL 8.0.17, AUTO_INCREMENT support is deprecated for FLOAT and DOUBLE columns;
you should expect it to be removed in a future version of MySQL. Consider removing the
AUTO_INCREMENT attribute from such columns, or convert them to an integer type.

13.1.7 Out-of-Range and Overflow Handling

When MySQL stores a value in a numeric column that is outside the permissible range of the column
data type, the result depends on the SQL mode in effect at the time:

• If strict SQL mode is enabled, MySQL rejects the out-of-range value with an error, and the insert

fails, in accordance with the SQL standard.

• If no restrictive modes are enabled, MySQL clips the value to the appropriate endpoint of the column

data type range and stores the resulting value instead.

When an out-of-range value is assigned to an integer column, MySQL stores the value representing
the corresponding endpoint of the column data type range.

When a floating-point or fixed-point column is assigned a value that exceeds the range implied by the
specified (or default) precision and scale, MySQL stores the value representing the corresponding
endpoint of that range.

Suppose that a table t1 has this definition:

CREATE TABLE t1 (i1 TINYINT, i2 TINYINT UNSIGNED);

With strict SQL mode enabled, an out of range error occurs:

mysql> SET sql_mode = 'TRADITIONAL';
mysql> INSERT INTO t1 (i1, i2) VALUES(256, 256);
ERROR 1264 (22003): Out of range value for column 'i1' at row 1
mysql> SELECT * FROM t1;
Empty set (0.00 sec)

With strict SQL mode not enabled, clipping with warnings occurs:

mysql> SET sql_mode = '';
mysql> INSERT INTO t1 (i1, i2) VALUES(256, 256);
mysql> SHOW WARNINGS;
+---------+------+---------------------------------------------+
| Level   | Code | Message                                     |
+---------+------+---------------------------------------------+
| Warning | 1264 | Out of range value for column 'i1' at row 1 |
| Warning | 1264 | Out of range value for column 'i2' at row 1 |
+---------+------+---------------------------------------------+
mysql> SELECT * FROM t1;
+------+------+
| i1   | i2   |
+------+------+
|  127 |  255 |
+------+------+

When strict SQL mode is not enabled, column-assignment conversions that occur due to clipping are
reported as warnings for ALTER TABLE, LOAD DATA, UPDATE, and multiple-row INSERT statements.
In strict mode, these statements fail, and some or all the values are not inserted or changed, depending
on whether the table is a transactional table and other factors. For details, see Section 7.1.11, “Server
SQL Modes”.

Overflow during numeric expression evaluation results in an error. For example, the largest signed
BIGINT value is 9223372036854775807, so the following expression produces an error:

mysql> SELECT 9223372036854775807 + 1;
ERROR 1690 (22003): BIGINT value is out of range in '(9223372036854775807 + 1)'

To enable the operation to succeed in this case, convert the value to unsigned;

mysql> SELECT CAST(9223372036854775807 AS UNSIGNED) + 1;

2207

The DATE, DATETIME, and TIMESTAMP Types

TIMESTAMP useful for recording the timestamp of an INSERT or UPDATE operation. You can also set
any TIMESTAMP column to the current date and time by assigning it a NULL value, unless it has been
defined with the NULL attribute to permit NULL values.

Automatic initialization and updating to the current date and time can be specified using DEFAULT
CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP column definition clauses. By
default, the first TIMESTAMP column has these properties, as previously noted. However, any
TIMESTAMP column in a table can be defined to have these properties.

•   TIME[(fsp)]

A time. The range is '-838:59:59.000000' to '838:59:59.000000'. MySQL displays TIME
values in 'hh:mm:ss[.fraction]' format, but permits assignment of values to TIME columns
using either strings or numbers.

An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision.
A value of 0 signifies that there is no fractional part. If omitted, the default precision is 0.

•   YEAR[(4)]

A year in 4-digit format. MySQL displays YEAR values in YYYY format, but permits assignment of
values to YEAR columns using either strings or numbers. Values display as 1901 to 2155, or 0000.

For additional information about YEAR display format and interpretation of input values, see
Section 13.2.4, “The YEAR Type”.

Note

As of MySQL 8.0.19, the YEAR(4) data type with an explicit display width is
deprecated; you should expect support for it to be removed in a future version
of MySQL. Instead, use YEAR without a display width, which has the same
meaning.

MySQL 8.0 does not support the 2-digit YEAR(2) data type permitted in older
versions of MySQL. For instructions on converting to 4-digit YEAR, see 2-Digit
YEAR(2) Limitations and Migrating to 4-Digit YEAR, in MySQL 5.7 Reference
Manual.

The SUM() and AVG() aggregate functions do not work with temporal values. (They convert the values
to numbers, losing everything after the first nonnumeric character.) To work around this problem,
convert to numeric units, perform the aggregate operation, and convert back to a temporal value.
Examples:

SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(time_col))) FROM tbl_name;
SELECT FROM_DAYS(SUM(TO_DAYS(date_col))) FROM tbl_name;

13.2.2 The DATE, DATETIME, and TIMESTAMP Types

The DATE, DATETIME, and TIMESTAMP types are related. This section describes their characteristics,
how they are similar, and how they differ. MySQL recognizes DATE, DATETIME, and TIMESTAMP
values in several formats, described in Section 11.1.3, “Date and Time Literals”. For the DATE and
DATETIME range descriptions, “supported” means that although earlier values might work, there is no
guarantee.

The DATE type is used for values with a date part but no time part. MySQL retrieves and displays DATE
values in 'YYYY-MM-DD' format. The supported range is '1000-01-01' to '9999-12-31'.

The DATETIME type is used for values that contain both date and time parts. MySQL retrieves
and displays DATETIME values in 'YYYY-MM-DD hh:mm:ss' format. The supported range is
'1000-01-01 00:00:00' to '9999-12-31 23:59:59'.

2211

The DATE, DATETIME, and TIMESTAMP Types

The TIMESTAMP data type is used for values that contain both date and time parts. TIMESTAMP has a
range of '1970-01-01 00:00:01' UTC to '2038-01-19 03:14:07' UTC.

A DATETIME or TIMESTAMP value can include a trailing fractional seconds part in up to microseconds
(6 digits) precision. In particular, any fractional part in a value inserted into a DATETIME or TIMESTAMP
column is stored rather than discarded. With the fractional part included, the format for these values
is 'YYYY-MM-DD hh:mm:ss[.fraction]', the range for DATETIME values is '1000-01-01
00:00:00.000000' to '9999-12-31 23:59:59.499999', and the range for TIMESTAMP values
is '1970-01-01 00:00:01.000000' to '2038-01-19 03:14:07.499999'. The fractional
part should always be separated from the rest of the time by a decimal point; no other fractional
seconds delimiter is recognized. For information about fractional seconds support in MySQL, see
Section 13.2.6, “Fractional Seconds in Time Values”.

The TIMESTAMP and DATETIME data types offer automatic initialization and updating to the current
date and time. For more information, see Section 13.2.5, “Automatic Initialization and Updating for
TIMESTAMP and DATETIME”.

MySQL converts TIMESTAMP values from the current time zone to UTC for storage, and back from
UTC to the current time zone for retrieval. (This does not occur for other types such as DATETIME.) By
default, the current time zone for each connection is the server's time. The time zone can be set on a
per-connection basis. As long as the time zone setting remains constant, you get back the same value
you store. If you store a TIMESTAMP value, and then change the time zone and retrieve the value,
the retrieved value is different from the value you stored. This occurs because the same time zone
was not used for conversion in both directions. The current time zone is available as the value of the
time_zone system variable. For more information, see Section 7.1.15, “MySQL Server Time Zone
Support”.

In MySQL 8.0.19 and later, you can specify a time zone offset when inserting a TIMESTAMP or
DATETIME value into a table. See Section 11.1.3, “Date and Time Literals”, for more information and
examples.

Invalid DATE, DATETIME, or TIMESTAMP values are converted to the “zero” value of the appropriate
type ('0000-00-00' or '0000-00-00 00:00:00'), if the SQL mode permits this conversion. The
precise behavior depends on which if any of strict SQL mode and the NO_ZERO_DATE SQL mode are
enabled; see Section 7.1.11, “Server SQL Modes”.

In MySQL 8.0.22 and later, you can convert TIMESTAMP values to UTC DATETIME values when
retrieving them using CAST() with the AT TIME ZONE operator, as shown here:

mysql> SELECT col,
     >     CAST(col AT TIME ZONE INTERVAL '+00:00' AS DATETIME) AS ut
     >     FROM ts ORDER BY id;
+---------------------+---------------------+
| col                 | ut                  |
+---------------------+---------------------+
| 2020-01-01 10:10:10 | 2020-01-01 15:10:10 |
| 2019-12-31 23:40:10 | 2020-01-01 04:40:10 |
| 2020-01-01 13:10:10 | 2020-01-01 18:10:10 |
| 2020-01-01 10:10:10 | 2020-01-01 15:10:10 |
| 2020-01-01 04:40:10 | 2020-01-01 09:40:10 |
| 2020-01-01 18:10:10 | 2020-01-01 23:10:10 |
+---------------------+---------------------+

For complete information regarding syntax and additional examples, see the description of the CAST()
function.

Be aware of certain properties of date value interpretation in MySQL:

• MySQL permits a “relaxed” format for values specified as strings, in which any punctuation character
may be used as the delimiter between date parts or time parts. In some cases, this syntax can be
deceiving. For example, a value such as '10:11:12' might look like a time value because of the
:, but is interpreted as the year '2010-11-12' if used in date context. The value '10:45:15' is
converted to '0000-00-00' because '45' is not a valid month.

2212

The TIME Type

The only delimiter recognized between a date and time part and a fractional seconds part is the
decimal point.

• The server requires that month and day values be valid, and not merely in the range 1 to 12 and 1
to 31, respectively. With strict mode disabled, invalid dates such as '2004-04-31' are converted
to '0000-00-00' and a warning is generated. With strict mode enabled, invalid dates generate
an error. To permit such dates, enable ALLOW_INVALID_DATES. See Section 7.1.11, “Server SQL
Modes”, for more information.

• MySQL does not accept TIMESTAMP values that include a zero in the day or month column or values
that are not a valid date. The sole exception to this rule is the special “zero” value '0000-00-00
00:00:00', if the SQL mode permits this value. The precise behavior depends on which if any of
strict SQL mode and the NO_ZERO_DATE SQL mode are enabled; see Section 7.1.11, “Server SQL
Modes”.

• Dates containing 2-digit year values are ambiguous because the century is unknown. MySQL

interprets 2-digit year values using these rules:

• Year values in the range 00-69 become 2000-2069.

• Year values in the range 70-99 become 1970-1999.

See also Section 13.2.9, “2-Digit Years in Dates”.

13.2.3 The TIME Type

MySQL retrieves and displays TIME values in 'hh:mm:ss' format (or 'hhh:mm:ss' format for large
hours values). TIME values may range from '-838:59:59' to '838:59:59'. The hours part may
be so large because the TIME type can be used not only to represent a time of day (which must be
less than 24 hours), but also elapsed time or a time interval between two events (which may be much
greater than 24 hours, or even negative).

MySQL recognizes TIME values in several formats, some of which can include a trailing fractional
seconds part in up to microseconds (6 digits) precision. See Section 11.1.3, “Date and Time
Literals”. For information about fractional seconds support in MySQL, see Section 13.2.6, “Fractional
Seconds in Time Values”. In particular, any fractional part in a value inserted into a TIME column
is stored rather than discarded. With the fractional part included, the range for TIME values is
'-838:59:59.000000' to '838:59:59.000000'.

Be careful about assigning abbreviated values to a TIME column. MySQL interprets abbreviated TIME
values with colons as time of the day. That is, '11:12' means '11:12:00', not '00:11:12'.
MySQL interprets abbreviated values without colons using the assumption that the two rightmost digits
represent seconds (that is, as elapsed time rather than as time of day). For example, you might think of
'1112' and 1112 as meaning '11:12:00' (12 minutes after 11 o'clock), but MySQL interprets them
as '00:11:12' (11 minutes, 12 seconds). Similarly, '12' and 12 are interpreted as '00:00:12'.

The only delimiter recognized between a time part and a fractional seconds part is the decimal point.

By default, values that lie outside the TIME range but are otherwise valid are clipped to the
closest endpoint of the range. For example, '-850:00:00' and '850:00:00' are converted to
'-838:59:59' and '838:59:59'. Invalid TIME values are converted to '00:00:00'. Note that
because '00:00:00' is itself a valid TIME value, there is no way to tell, from a value of '00:00:00'
stored in a table, whether the original value was specified as '00:00:00' or whether it was invalid.

For more restrictive treatment of invalid TIME values, enable strict SQL mode to cause errors to occur.
See Section 7.1.11, “Server SQL Modes”.

13.2.4 The YEAR Type

2213

Automatic Initialization and Updating for TIMESTAMP and DATETIME

The YEAR type is a 1-byte type used to represent year values. It can be declared as YEAR with an
implicit display width of 4 characters, or equivalently as YEAR(4) with an explicit display width.

Note

As of MySQL 8.0.19, the YEAR(4) data type with an explicit display width
is deprecated and you should expect support for it to be removed in a future
version of MySQL. Instead, use YEAR without a display width, which has the
same meaning.

MySQL 8.0 does not support the 2-digit YEAR(2) data type permitted in older
versions of MySQL. For instructions on converting to 4-digit YEAR, see 2-Digit
YEAR(2) Limitations and Migrating to 4-Digit YEAR, in MySQL 5.7 Reference
Manual.

MySQL displays YEAR values in YYYY format, with a range of 1901 to 2155, and 0000.

YEAR accepts input values in a variety of formats:

• As 4-digit strings in the range '1901' to '2155'.

• As 4-digit numbers in the range 1901 to 2155.

• As 1- or 2-digit strings in the range '0' to '99'. MySQL converts values in the ranges '0' to '69'

and '70' to '99' to YEAR values in the ranges 2000 to 2069 and 1970 to 1999.

• As 1- or 2-digit numbers in the range 0 to 99. MySQL converts values in the ranges 1 to 69 and 70

to 99 to YEAR values in the ranges 2001 to 2069 and 1970 to 1999.

The result of inserting a numeric 0 has a display value of 0000 and an internal value of 0000. To
insert zero and have it be interpreted as 2000, specify it as a string '0' or '00'.

• As the result of functions that return a value that is acceptable in YEAR context, such as NOW().

If strict SQL mode is not enabled, MySQL converts invalid YEAR values to 0000. In strict SQL mode,
attempting to insert an invalid YEAR value produces an error.

See also Section 13.2.9, “2-Digit Years in Dates”.

13.2.5 Automatic Initialization and Updating for TIMESTAMP and DATETIME

TIMESTAMP and DATETIME columns can be automatically initialized and updated to the current date
and time (that is, the current timestamp).

For any TIMESTAMP or DATETIME column in a table, you can assign the current timestamp as the
default value, the auto-update value, or both:

• An auto-initialized column is set to the current timestamp for inserted rows that specify no value for

the column.

• An auto-updated column is automatically updated to the current timestamp when the value of

any other column in the row is changed from its current value. An auto-updated column remains
unchanged if all other columns are set to their current values. To prevent an auto-updated column
from updating when other columns change, explicitly set it to its current value. To update an auto-
updated column even when other columns do not change, explicitly set it to the value it should have
(for example, set it to CURRENT_TIMESTAMP).

In addition, if the explicit_defaults_for_timestamp system variable is disabled, you can
initialize or update any TIMESTAMP (but not DATETIME) column to the current date and time by
assigning it a NULL value, unless it has been defined with the NULL attribute to permit NULL values.

To specify automatic properties, use the DEFAULT CURRENT_TIMESTAMP and ON UPDATE
CURRENT_TIMESTAMP clauses in column definitions. The order of the clauses does not

2214

Automatic Initialization and Updating for TIMESTAMP and DATETIME

matter. If both are present in a column definition, either can occur first. Any of the synonyms
for CURRENT_TIMESTAMP have the same meaning as CURRENT_TIMESTAMP. These are
CURRENT_TIMESTAMP(), NOW(), LOCALTIME, LOCALTIME(), LOCALTIMESTAMP, and
LOCALTIMESTAMP().

Use of DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP is specific
to TIMESTAMP and DATETIME. The DEFAULT clause also can be used to specify a constant
(nonautomatic) default value (for example, DEFAULT 0 or DEFAULT '2000-01-01 00:00:00').

Note

The following examples use DEFAULT 0, a default that can produce warnings
or errors depending on whether strict SQL mode or the NO_ZERO_DATE SQL
mode is enabled. Be aware that the TRADITIONAL SQL mode includes strict
mode and NO_ZERO_DATE. See Section 7.1.11, “Server SQL Modes”.

TIMESTAMP or DATETIME column definitions can specify the current timestamp for both the default
and auto-update values, for one but not the other, or for neither. Different columns can have different
combinations of automatic properties. The following rules describe the possibilities:

• With both DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP, the column

has the current timestamp for its default value and is automatically updated to the current timestamp.

CREATE TABLE t1 (
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

• With a DEFAULT clause but no ON UPDATE CURRENT_TIMESTAMP clause, the column has the

given default value and is not automatically updated to the current timestamp.

The default depends on whether the DEFAULT clause specifies CURRENT_TIMESTAMP or a constant
value. With CURRENT_TIMESTAMP, the default is the current timestamp.

CREATE TABLE t1 (
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dt DATETIME DEFAULT CURRENT_TIMESTAMP
);

With a constant, the default is the given value. In this case, the column has no automatic properties
at all.

CREATE TABLE t1 (
  ts TIMESTAMP DEFAULT 0,
  dt DATETIME DEFAULT 0
);

• With an ON UPDATE CURRENT_TIMESTAMP clause and a constant DEFAULT clause, the column is

automatically updated to the current timestamp and has the given constant default value.

CREATE TABLE t1 (
  ts TIMESTAMP DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP,
  dt DATETIME DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP
);

• With an ON UPDATE CURRENT_TIMESTAMP clause but no DEFAULT clause, the column is

automatically updated to the current timestamp but does not have the current timestamp for its
default value.

The default in this case is type dependent. TIMESTAMP has a default of 0 unless defined with the
NULL attribute, in which case the default is NULL.

CREATE TABLE t1 (
  ts1 TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,     -- default 0
  ts2 TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP -- default NULL

2215

Automatic Initialization and Updating for TIMESTAMP and DATETIME

);

DATETIME has a default of NULL unless defined with the NOT NULL attribute, in which case the
default is 0.

CREATE TABLE t1 (
  dt1 DATETIME ON UPDATE CURRENT_TIMESTAMP,         -- default NULL
  dt2 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP -- default 0
);

TIMESTAMP and DATETIME columns have no automatic properties unless they are specified
explicitly, with this exception: If the explicit_defaults_for_timestamp system variable is
disabled, the first TIMESTAMP column has both DEFAULT CURRENT_TIMESTAMP and ON UPDATE
CURRENT_TIMESTAMP if neither is specified explicitly. To suppress automatic properties for the first
TIMESTAMP column, use one of these strategies:

• Enable the explicit_defaults_for_timestamp system variable. In this case, the DEFAULT
CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP clauses that specify automatic
initialization and updating are available, but are not assigned to any TIMESTAMP column unless
explicitly included in the column definition.

• Alternatively, if explicit_defaults_for_timestamp is disabled, do either of the following:

• Define the column with a DEFAULT clause that specifies a constant default value.

• Specify the NULL attribute. This also causes the column to permit NULL values, which means that
you cannot assign the current timestamp by setting the column to NULL. Assigning NULL sets the
column to NULL, not the current timestamp. To assign the current timestamp, set the column to
CURRENT_TIMESTAMP or a synonym such as NOW().

Consider these table definitions:

CREATE TABLE t1 (
  ts1 TIMESTAMP DEFAULT 0,
  ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP);
CREATE TABLE t2 (
  ts1 TIMESTAMP NULL,
  ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP);
CREATE TABLE t3 (
  ts1 TIMESTAMP NULL DEFAULT 0,
  ts2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP);

The tables have these properties:

• In each table definition, the first TIMESTAMP column has no automatic initialization or updating.

• The tables differ in how the ts1 column handles NULL values. For t1, ts1 is NOT NULL and

assigning it a value of NULL sets it to the current timestamp. For t2 and t3, ts1 permits NULL and
assigning it a value of NULL sets it to NULL.

• t2 and t3 differ in the default value for ts1. For t2, ts1 is defined to permit NULL, so the default
is also NULL in the absence of an explicit DEFAULT clause. For t3, ts1 permits NULL but has an
explicit default of 0.

If a TIMESTAMP or DATETIME column definition includes an explicit fractional seconds precision value
anywhere, the same value must be used throughout the column definition. This is permitted:

CREATE TABLE t1 (
  ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
);

This is not permitted:

2216

Fractional Seconds in Time Values

CREATE TABLE t1 (
  ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(3)
);

TIMESTAMP Initialization and the NULL Attribute

If the explicit_defaults_for_timestamp system variable is disabled, TIMESTAMP columns
by default are NOT NULL, cannot contain NULL values, and assigning NULL assigns the current
timestamp. To permit a TIMESTAMP column to contain NULL, explicitly declare it with the NULL
attribute. In this case, the default value also becomes NULL unless overridden with a DEFAULT clause
that specifies a different default value. DEFAULT NULL can be used to explicitly specify NULL as
the default value. (For a TIMESTAMP column not declared with the NULL attribute, DEFAULT NULL
is invalid.) If a TIMESTAMP column permits NULL values, assigning NULL sets it to NULL, not to the
current timestamp.

The following table contains several TIMESTAMP columns that permit NULL values:

CREATE TABLE t
(
  ts1 TIMESTAMP NULL DEFAULT NULL,
  ts2 TIMESTAMP NULL DEFAULT 0,
  ts3 TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
);

A TIMESTAMP column that permits NULL values does not take on the current timestamp at insert time
except under one of the following conditions:

• Its default value is defined as CURRENT_TIMESTAMP and no value is specified for the column

• CURRENT_TIMESTAMP or any of its synonyms such as NOW() is explicitly inserted into the column

In other words, a TIMESTAMP column defined to permit NULL values auto-initializes only if its definition
includes DEFAULT CURRENT_TIMESTAMP:

CREATE TABLE t (ts TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);

If the TIMESTAMP column permits NULL values but its definition does not include DEFAULT
CURRENT_TIMESTAMP, you must explicitly insert a value corresponding to the current date and time.
Suppose that tables t1 and t2 have these definitions:

CREATE TABLE t1 (ts TIMESTAMP NULL DEFAULT '0000-00-00 00:00:00');
CREATE TABLE t2 (ts TIMESTAMP NULL DEFAULT NULL);

To set the TIMESTAMP column in either table to the current timestamp at insert time, explicitly assign it
that value. For example:

INSERT INTO t2 VALUES (CURRENT_TIMESTAMP);
INSERT INTO t1 VALUES (NOW());

If the explicit_defaults_for_timestamp system variable is enabled, TIMESTAMP columns
permit NULL values only if declared with the NULL attribute. Also, TIMESTAMP columns do not permit
assigning NULL to assign the current timestamp, whether declared with the NULL or NOT NULL
attribute. To assign the current timestamp, set the column to CURRENT_TIMESTAMP or a synonym
such as NOW().

13.2.6 Fractional Seconds in Time Values

MySQL has fractional seconds support for TIME, DATETIME, and TIMESTAMP values, with up to
microseconds (6 digits) precision:

• To define a column that includes a fractional seconds part, use the syntax type_name(fsp), where
type_name is TIME, DATETIME, or TIMESTAMP, and fsp is the fractional seconds precision. For
example:

CREATE TABLE t1 (t TIME(3), dt DATETIME(6));

2217

What Calendar Is Used By MySQL?

The fsp value, if given, must be in the range 0 to 6. A value of 0 signifies that there is no fractional
part. If omitted, the default precision is 0. (This differs from the standard SQL default of 6, for
compatibility with previous MySQL versions.)

• Inserting a TIME, DATE, or TIMESTAMP value with a fractional seconds part into a column of the
same type but having fewer fractional digits results in rounding. Consider a table created and
populated as follows:

CREATE TABLE fractest( c1 TIME(2), c2 DATETIME(2), c3 TIMESTAMP(2) );
INSERT INTO fractest VALUES
('17:51:04.777', '2018-09-08 17:51:04.777', '2018-09-08 17:51:04.777');

The temporal values are inserted into the table with rounding:

mysql> SELECT * FROM fractest;
+-------------+------------------------+------------------------+
| c1          | c2                     | c3                     |
+-------------+------------------------+------------------------+
| 17:51:04.78 | 2018-09-08 17:51:04.78 | 2018-09-08 17:51:04.78 |
+-------------+------------------------+------------------------+

No warning or error is given when such rounding occurs. This behavior follows the SQL standard.

To insert the values with truncation instead, enable the TIME_TRUNCATE_FRACTIONAL SQL mode:

SET @@sql_mode = sys.list_add(@@sql_mode, 'TIME_TRUNCATE_FRACTIONAL');

With that SQL mode enabled, the temporal values are inserted with truncation:

mysql> SELECT * FROM fractest;
+-------------+------------------------+------------------------+
| c1          | c2                     | c3                     |
+-------------+------------------------+------------------------+
| 17:51:04.77 | 2018-09-08 17:51:04.77 | 2018-09-08 17:51:04.77 |
+-------------+------------------------+------------------------+

• Functions that take temporal arguments accept values with fractional seconds. Return values from

temporal functions include fractional seconds as appropriate. For example, NOW() with no argument
returns the current date and time with no fractional part, but takes an optional argument from 0 to 6
to specify that the return value includes a fractional seconds part of that many digits.

• Syntax for temporal literals produces temporal values: DATE 'str', TIME 'str', and TIMESTAMP
'str', and the ODBC-syntax equivalents. The resulting value includes a trailing fractional seconds
part if specified. Previously, the temporal type keyword was ignored and these constructs produced
the string value. See Standard SQL and ODBC Date and Time Literals

13.2.7 What Calendar Is Used By MySQL?

MySQL uses what is known as a proleptic Gregorian calendar.

Every country that has switched from the Julian to the Gregorian calendar has had to discard at least
ten days during the switch. To see how this works, consider the month of October 1582, when the first
Julian-to-Gregorian switch occurred.

Monday

Tuesday

Wednesday Thursday

Friday

Saturday

Sunday

1

18

25

2

19

26

3

20

27

4

21

28

15

22

29

16

23

30

17

24

31

There are no dates between October 4 and October 15. This discontinuity is called the cutover. Any
dates before the cutover are Julian, and any dates following the cutover are Gregorian. Dates during a
cutover are nonexistent.

2218

Conversion Between Date and Time Types

A calendar applied to dates when it was not actually in use is called proleptic. Thus, if we assume there
was never a cutover and Gregorian rules always rule, we have a proleptic Gregorian calendar. This
is what is used by MySQL, as is required by standard SQL. For this reason, dates prior to the cutover
stored as MySQL DATE or DATETIME values must be adjusted to compensate for the difference. It
is important to realize that the cutover did not occur at the same time in all countries, and that the
later it happened, the more days were lost. For example, in Great Britain, it took place in 1752, when
Wednesday September 2 was followed by Thursday September 14. Russia remained on the Julian
calendar until 1918, losing 13 days in the process, and what is popularly referred to as its “October
Revolution” occurred in November according to the Gregorian calendar.

13.2.8 Conversion Between Date and Time Types

To some extent, you can convert a value from one temporal type to another. However, there may be
some alteration of the value or loss of information. In all cases, conversion between temporal types
is subject to the range of valid values for the resulting type. For example, although DATE, DATETIME,
and TIMESTAMP values all can be specified using the same set of formats, the types do not all
have the same range of values. TIMESTAMP values cannot be earlier than 1970 UTC or later than
'2038-01-19 03:14:07' UTC. This means that a date such as '1968-01-01', while valid as a
DATE or DATETIME value, is not valid as a TIMESTAMP value and is converted to 0.

Conversion of DATE values:

• Conversion to a DATETIME or TIMESTAMP value adds a time part of '00:00:00' because the

DATE value contains no time information.

• Conversion to a TIME value is not useful; the result is '00:00:00'.

Conversion of DATETIME and TIMESTAMP values:

• Conversion to a DATE value takes fractional seconds into account and rounds the time part. For
example, '1999-12-31 23:59:59.499' becomes '1999-12-31', whereas '1999-12-31
23:59:59.500' becomes '2000-01-01'.

• Conversion to a TIME value discards the date part because the TIME type contains no date

information.

For conversion of TIME values to other temporal types, the value of CURRENT_DATE() is used for the
date part. The TIME is interpreted as elapsed time (not time of day) and added to the date. This means
that the date part of the result differs from the current date if the time value is outside the range from
'00:00:00' to '23:59:59'.

Suppose that the current date is '2012-01-01'. TIME values of '12:00:00', '24:00:00',
and '-12:00:00', when converted to DATETIME or TIMESTAMP values, result in '2012-01-01
12:00:00', '2012-01-02 00:00:00', and '2011-12-31 12:00:00', respectively.

Conversion of TIME to DATE is similar but discards the time part from the result: '2012-01-01',
'2012-01-02', and '2011-12-31', respectively.

Explicit conversion can be used to override implicit conversion. For example, in comparison of DATE
and DATETIME values, the DATE value is coerced to the DATETIME type by adding a time part of
'00:00:00'. To perform the comparison by ignoring the time part of the DATETIME value instead,
use the CAST() function in the following way:

date_col = CAST(datetime_col AS DATE)

Conversion of TIME and DATETIME values to numeric form (for example, by adding +0) depends
on whether the value contains a fractional seconds part. TIME(N) or DATETIME(N) is converted to
integer when N is 0 (or omitted) and to a DECIMAL value with N decimal digits when N is greater than 0:

mysql> SELECT CURTIME(), CURTIME()+0, CURTIME(3)+0;
+-----------+-------------+--------------+
| CURTIME() | CURTIME()+0 | CURTIME(3)+0 |

2219

2-Digit Years in Dates

+-----------+-------------+--------------+
| 09:28:00  |       92800 |    92800.887 |
+-----------+-------------+--------------+
mysql> SELECT NOW(), NOW()+0, NOW(3)+0;
+---------------------+----------------+--------------------+
| NOW()               | NOW()+0        | NOW(3)+0           |
+---------------------+----------------+--------------------+
| 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
+---------------------+----------------+--------------------+

13.2.9 2-Digit Years in Dates

Date values with 2-digit years are ambiguous because the century is unknown. Such values must be
interpreted into 4-digit form because MySQL stores years internally using 4 digits.

For DATETIME, DATE, and TIMESTAMP types, MySQL interprets dates specified with ambiguous year
values using these rules:

• Year values in the range 00-69 become 2000-2069.

• Year values in the range 70-99 become 1970-1999.

For YEAR, the rules are the same, with this exception: A numeric 00 inserted into YEAR results in 0000
rather than 2000. To specify zero for YEAR and have it be interpreted as 2000, specify it as a string
'0' or '00'.

Remember that these rules are only heuristics that provide reasonable guesses as to what your data
values mean. If the rules used by MySQL do not produce the values you require, you must provide
unambiguous input containing 4-digit year values.

ORDER BY properly sorts YEAR values that have 2-digit years.

Some functions like MIN() and MAX() convert a YEAR to a number. This means that a value with a 2-
digit year does not work properly with these functions. The fix in this case is to convert the YEAR to 4-
digit year format.

13.3 String Data Types

The string data types are CHAR, VARCHAR, BINARY, VARBINARY, BLOB, TEXT, ENUM, and SET.

For information about storage requirements of the string data types, see Section 13.7, “Data Type
Storage Requirements”.

For descriptions of functions that operate on string values, see Section 14.8, “String Functions and
Operators”.

13.3.1 String Data Type Syntax

The string data types are CHAR, VARCHAR, BINARY, VARBINARY, BLOB, TEXT, ENUM, and SET.

In some cases, MySQL may change a string column to a type different from that given in a CREATE
TABLE or ALTER TABLE statement. See Section 15.1.20.7, “Silent Column Specification Changes”.

For definitions of character string columns (CHAR, VARCHAR, and the TEXT types), MySQL interprets
length specifications in character units. For definitions of binary string columns (BINARY, VARBINARY,
and the BLOB types), MySQL interprets length specifications in byte units.

Column definitions for character string data types CHAR, VARCHAR, the TEXT types, ENUM, SET, and
any synonyms) can specify the column character set and collation:

• CHARACTER SET specifies the character set. If desired, a collation for the character set can be

specified with the COLLATE attribute, along with any other attributes. For example:

CREATE TABLE t

2220

String Data Type Syntax

(
    c1 VARCHAR(20) CHARACTER SET utf8mb4,
    c2 TEXT CHARACTER SET latin1 COLLATE latin1_general_cs
);

This table definition creates a column named c1 that has a character set of utf8mb4 with the default
collation for that character set, and a column named c2 that has a character set of latin1 and a
case-sensitive (_cs) collation.

The rules for assigning the character set and collation when either or both of CHARACTER SET and
the COLLATE attribute are missing are described in Section 12.3.5, “Column Character Set and
Collation”.

CHARSET is a synonym for CHARACTER SET.

• Specifying the CHARACTER SET binary attribute for a character string data type causes the
column to be created as the corresponding binary string data type: CHAR becomes BINARY,
VARCHAR becomes VARBINARY, and TEXT becomes BLOB. For the ENUM and SET data types, this
does not occur; they are created as declared. Suppose that you specify a table using this definition:

CREATE TABLE t
(
  c1 VARCHAR(10) CHARACTER SET binary,
  c2 TEXT CHARACTER SET binary,
  c3 ENUM('a','b','c') CHARACTER SET binary
);

The resulting table has this definition:

CREATE TABLE t
(
  c1 VARBINARY(10),
  c2 BLOB,
  c3 ENUM('a','b','c') CHARACTER SET binary
);

• The BINARY attribute is a nonstandard MySQL extension that is shorthand for specifying the binary

(_bin) collation of the column character set (or of the table default character set if no column
character set is specified). In this case, comparison and sorting are based on numeric character
code values. Suppose that you specify a table using this definition:

CREATE TABLE t
(
  c1 VARCHAR(10) CHARACTER SET latin1 BINARY,
  c2 TEXT BINARY
) CHARACTER SET utf8mb4;

The resulting table has this definition:

CREATE TABLE t (
  c1 VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_bin,
  c2 TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
) CHARACTER SET utf8mb4;

In MySQL 8.0, this nonstandard use of the BINARY attribute is ambiguous because the utf8mb4
character set has multiple _bin collations. As of MySQL 8.0.17, the BINARY attribute is deprecated
and you should expect support for it to be removed in a future version of MySQL. Applications should
be adjusted to use an explicit _bin collation instead.

The use of BINARY to specify a data type or character set remains unchanged.

• The ASCII attribute is shorthand for CHARACTER SET latin1. Supported in older MySQL
releases, ASCII is deprecated in MySQL 8.0.28 and later; use CHARACTER SET instead.

• The UNICODE attribute is shorthand for CHARACTER SET ucs2. Supported in older MySQL
releases, UNICODE is deprecated in MySQL 8.0.28 and later; use CHARACTER SET instead.

2221

String Data Type Syntax

•   VARBINARY(M)

The VARBINARY type is similar to the VARCHAR type, but stores binary byte strings rather than
nonbinary character strings. M represents the maximum column length in bytes.

•   TINYBLOB

A BLOB column with a maximum length of 255 (28 − 1) bytes. Each TINYBLOB value is stored using
a 1-byte length prefix that indicates the number of bytes in the value.

•   TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]

A TEXT column with a maximum length of 255 (28 − 1) characters. The effective maximum length is
less if the value contains multibyte characters. Each TINYTEXT value is stored using a 1-byte length
prefix that indicates the number of bytes in the value.

•   BLOB[(M)]

A BLOB column with a maximum length of 65,535 (216 − 1) bytes. Each BLOB value is stored using a
2-byte length prefix that indicates the number of bytes in the value.

An optional length M can be given for this type. If this is done, MySQL creates the column as the
smallest BLOB type large enough to hold values M bytes long.

•   TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]

A TEXT column with a maximum length of 65,535 (216 − 1) characters. The effective maximum length
is less if the value contains multibyte characters. Each TEXT value is stored using a 2-byte length
prefix that indicates the number of bytes in the value.

An optional length M can be given for this type. If this is done, MySQL creates the column as the
smallest TEXT type large enough to hold values M characters long.

•   MEDIUMBLOB

A BLOB column with a maximum length of 16,777,215 (224 − 1) bytes. Each MEDIUMBLOB value is
stored using a 3-byte length prefix that indicates the number of bytes in the value.

•   MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]

A TEXT column with a maximum length of 16,777,215 (224 − 1) characters. The effective maximum
length is less if the value contains multibyte characters. Each MEDIUMTEXT value is stored using a 3-
byte length prefix that indicates the number of bytes in the value.

•   LONGBLOB

A BLOB column with a maximum length of 4,294,967,295 or 4GB (232 − 1) bytes. The effective
maximum length of LONGBLOB columns depends on the configured maximum packet size in the
client/server protocol and available memory. Each LONGBLOB value is stored using a 4-byte length
prefix that indicates the number of bytes in the value.

•   LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]

A TEXT column with a maximum length of 4,294,967,295 or 4GB (232 − 1) characters. The effective
maximum length is less if the value contains multibyte characters. The effective maximum length
of LONGTEXT columns also depends on the configured maximum packet size in the client/server
protocol and available memory. Each LONGTEXT value is stored using a 4-byte length prefix that
indicates the number of bytes in the value.

2223

The CHAR and VARCHAR Types

•   ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE

collation_name]

An enumeration. A string object that can have only one value, chosen from the list of values
'value1', 'value2', ..., NULL or the special '' error value. ENUM values are represented
internally as integers.

An ENUM column can have a maximum of 65,535 distinct elements.

The maximum supported length of an individual ENUM element is M <= 255 and (M x w) <= 1020,
where M is the element literal length and w is the number of bytes required for the maximum-length
character in the character set.

•   SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE

collation_name]

A set. A string object that can have zero or more values, each of which must be chosen from the list
of values 'value1', 'value2', ... SET values are represented internally as integers.

A SET column can have a maximum of 64 distinct members.

The maximum supported length of an individual SET element is M <= 255 and (M x w) <= 1020,
where M is the element literal length and w is the number of bytes required for the maximum-length
character in the character set.

13.3.2 The CHAR and VARCHAR Types

The CHAR and VARCHAR types are similar, but differ in the way they are stored and retrieved. They also
differ in maximum length and in whether trailing spaces are retained.

The CHAR and VARCHAR types are declared with a length that indicates the maximum number of
characters you want to store. For example, CHAR(30) can hold up to 30 characters.

The length of a CHAR column is fixed to the length that you declare when you create the table. The
length can be any value from 0 to 255. When CHAR values are stored, they are right-padded with
spaces to the specified length. When CHAR values are retrieved, trailing spaces are removed unless
the PAD_CHAR_TO_FULL_LENGTH SQL mode is enabled.

Values in VARCHAR columns are variable-length strings. The length can be specified as a value from
0 to 65,535. The effective maximum length of a VARCHAR is subject to the maximum row size (65,535
bytes, which is shared among all columns) and the character set used. See Section 10.4.7, “Limits on
Table Column Count and Row Size”.

In contrast to CHAR, VARCHAR values are stored as a 1-byte or 2-byte length prefix plus data. The
length prefix indicates the number of bytes in the value. A column uses one length byte if values
require no more than 255 bytes, two length bytes if values may require more than 255 bytes.

If strict SQL mode is not enabled and you assign a value to a CHAR or VARCHAR column that exceeds
the column's maximum length, the value is truncated to fit and a warning is generated. For truncation of
nonspace characters, you can cause an error to occur (rather than a warning) and suppress insertion
of the value by using strict SQL mode. See Section 7.1.11, “Server SQL Modes”.

For VARCHAR columns, trailing spaces in excess of the column length are truncated prior to insertion
and a warning is generated, regardless of the SQL mode in use. For CHAR columns, truncation of
excess trailing spaces from inserted values is performed silently regardless of the SQL mode.

VARCHAR values are not padded when they are stored. Trailing spaces are retained when values are
stored and retrieved, in conformance with standard SQL.

The following table illustrates the differences between CHAR and VARCHAR by showing the result of
storing various string values into CHAR(4) and VARCHAR(4) columns (assuming that the column uses
a single-byte character set such as latin1).

2224

The BINARY and VARBINARY Types

Value

''

'ab'

'abcd'

'abcdefgh'

CHAR(4)

Storage Required VARCHAR(4)

Storage Required

'    '

'ab  '

'abcd'

'abcd'

4 bytes

4 bytes

4 bytes

4 bytes

''

'ab'

'abcd'

'abcd'

1 byte

3 bytes

5 bytes

5 bytes

The values shown as stored in the last row of the table apply only when not using strict SQL mode; if
strict mode is enabled, values that exceed the column length are not stored, and an error results.

InnoDB encodes fixed-length fields greater than or equal to 768 bytes in length as variable-length
fields, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the
maximum byte length of the character set is greater than 3, as it is with utf8mb4.

If a given value is stored into the CHAR(4) and VARCHAR(4) columns, the values retrieved from the
columns are not always the same because trailing spaces are removed from CHAR columns upon
retrieval. The following example illustrates this difference:

mysql> CREATE TABLE vc (v VARCHAR(4), c CHAR(4));
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO vc VALUES ('ab  ', 'ab  ');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT CONCAT('(', v, ')'), CONCAT('(', c, ')') FROM vc;
+---------------------+---------------------+
| CONCAT('(', v, ')') | CONCAT('(', c, ')') |
+---------------------+---------------------+
| (ab  )              | (ab)                |
+---------------------+---------------------+
1 row in set (0.06 sec)

Values in CHAR, VARCHAR, and TEXT columns are sorted and compared according to the character set
collation assigned to the column.

MySQL collations have a pad attribute of PAD SPACE, other than Unicode collations based on UCA
9.0.0 and higher, which have a pad attribute of NO PAD. (see Section 12.10.1, “Unicode Character
Sets”).

To determine the pad attribute for a collation, use the INFORMATION_SCHEMA COLLATIONS table,
which has a PAD_ATTRIBUTE column.

For nonbinary strings (CHAR, VARCHAR, and TEXT values), the string collation pad attribute determines
treatment in comparisons of trailing spaces at the end of strings. NO PAD collations treat trailing spaces
as significant in comparisons, like any other character. PAD SPACE collations treat trailing spaces as
insignificant in comparisons; strings are compared without regard to trailing spaces. See Trailing Space
Handling in Comparisons. The server SQL mode has no effect on comparison behavior with respect to
trailing spaces.

Note

For more information about MySQL character sets and collations, see
Chapter 12, Character Sets, Collations, Unicode. For additional information
about storage requirements, see Section 13.7, “Data Type Storage
Requirements”.

For those cases where trailing pad characters are stripped or comparisons ignore them, if a column
has an index that requires unique values, inserting into the column values that differ only in number of
trailing pad characters results in a duplicate-key error. For example, if a table contains 'a', an attempt
to store 'a ' causes a duplicate-key error.

13.3.3 The BINARY and VARBINARY Types

2225

The BLOB and TEXT Types

Note

Within the mysql client, binary strings display using hexadecimal notation,
depending on the value of the --binary-as-hex. For more information about
that option, see Section 6.5.1, “mysql — The MySQL Command-Line Client”.

13.3.4 The BLOB and TEXT Types

A BLOB is a binary large object that can hold a variable amount of data. The four BLOB types are
TINYBLOB, BLOB, MEDIUMBLOB, and LONGBLOB. These differ only in the maximum length of the
values they can hold. The four TEXT types are TINYTEXT, TEXT, MEDIUMTEXT, and LONGTEXT. These
correspond to the four BLOB types and have the same maximum lengths and storage requirements.
See Section 13.7, “Data Type Storage Requirements”.

BLOB values are treated as binary strings (byte strings). They have the binary character set and
collation, and comparison and sorting are based on the numeric values of the bytes in column values.
TEXT values are treated as nonbinary strings (character strings). They have a character set other than
binary, and values are sorted and compared based on the collation of the character set.

If strict SQL mode is not enabled and you assign a value to a BLOB or TEXT column that exceeds the
column's maximum length, the value is truncated to fit and a warning is generated. For truncation of
nonspace characters, you can cause an error to occur (rather than a warning) and suppress insertion
of the value by using strict SQL mode. See Section 7.1.11, “Server SQL Modes”.

Truncation of excess trailing spaces from values to be inserted into TEXT columns always generates a
warning, regardless of the SQL mode.

For TEXT and BLOB columns, there is no padding on insert and no bytes are stripped on select.

If a TEXT column is indexed, index entry comparisons are space-padded at the end. This means that, if
the index requires unique values, duplicate-key errors occur for values that differ only in the number of
trailing spaces. For example, if a table contains 'a', an attempt to store 'a ' causes a duplicate-key
error. This is not true for BLOB columns.

In most respects, you can regard a BLOB column as a VARBINARY column that can be as large as
you like. Similarly, you can regard a TEXT column as a VARCHAR column. BLOB and TEXT differ from
VARBINARY and VARCHAR in the following ways:

• For indexes on BLOB and TEXT columns, you must specify an index prefix length. For CHAR and

VARCHAR, a prefix length is optional. See Section 10.3.5, “Column Indexes”.

•    BLOB and TEXT columns cannot have DEFAULT values.

If you use the BINARY attribute with a TEXT data type, the column is assigned the binary (_bin)
collation of the column character set.

LONG and LONG VARCHAR map to the MEDIUMTEXT data type. This is a compatibility feature.

MySQL Connector/ODBC defines BLOB values as LONGVARBINARY and TEXT values as
LONGVARCHAR.

Because BLOB and TEXT values can be extremely long, you might encounter some constraints in using
them:

• Only the first max_sort_length bytes of the column are used when sorting. The default value
of max_sort_length is 1024. You can make more bytes significant in sorting or grouping by
increasing the value of max_sort_length at server startup or runtime. Any client can change the
value of its session max_sort_length variable:

mysql> SET max_sort_length = 2000;
mysql> SELECT id, comment FROM t
    -> ORDER BY comment;

2227

The ENUM Type

• Instances of BLOB or TEXT columns in the result of a query that is processed using a temporary table
causes the server to use a table on disk rather than in memory because the MEMORY storage engine
does not support those data types (see Section 10.4.4, “Internal Temporary Table Use in MySQL”).
Use of disk incurs a performance penalty, so include BLOB or TEXT columns in the query result only
if they are really needed. For example, avoid using SELECT *, which selects all columns.

• The maximum size of a BLOB or TEXT object is determined by its type, but the largest value you

actually can transmit between the client and server is determined by the amount of available memory
and the size of the communications buffers. You can change the message buffer size by changing
the value of the max_allowed_packet variable, but you must do so for both the server and your
client program. For example, both mysql and mysqldump enable you to change the client-side
max_allowed_packet value. See Section 7.1.1, “Configuring the Server”, Section 6.5.1, “mysql
— The MySQL Command-Line Client”, and Section 6.5.4, “mysqldump — A Database Backup
Program”. You may also want to compare the packet sizes and the size of the data objects you are
storing with the storage requirements, see Section 13.7, “Data Type Storage Requirements”

Each BLOB or TEXT value is represented internally by a separately allocated object. This is in contrast
to all other data types, for which storage is allocated once per column when the table is opened.

In some cases, it may be desirable to store binary data such as media files in BLOB or TEXT columns.
You may find MySQL's string handling functions useful for working with such data. See Section 14.8,
“String Functions and Operators”. For security and other reasons, it is usually preferable to do so using
application code rather than giving application users the FILE privilege. You can discuss specifics for
various languages and platforms in the MySQL Forums (http://forums.mysql.com/).

Note

Within the mysql client, binary strings display using hexadecimal notation,
depending on the value of the --binary-as-hex. For more information about
that option, see Section 6.5.1, “mysql — The MySQL Command-Line Client”.

13.3.5 The ENUM Type

An ENUM is a string object with a value chosen from a list of permitted values that are enumerated
explicitly in the column specification at table creation time.

See Section 13.3.1, “String Data Type Syntax” for ENUM type syntax and length limits.

The ENUM type has these advantages:

• Compact data storage in situations where a column has a limited set of possible values. The strings
you specify as input values are automatically encoded as numbers. See Section 13.7, “Data Type
Storage Requirements” for storage requirements for the ENUM type.

• Readable queries and output. The numbers are translated back to the corresponding strings in query

results.

and these potential issues to consider:

• If you make enumeration values that look like numbers, it is easy to mix up the literal values with

their internal index numbers, as explained in Enumeration Limitations.

• Using ENUM columns in ORDER BY clauses requires extra care, as explained in Enumeration Sorting.

• Creating and Using ENUM Columns

• Index Values for Enumeration Literals

• Handling of Enumeration Literals

• Empty or NULL Enumeration Values

2228

The ENUM Type

• Enumeration Sorting

• Enumeration Limitations

Creating and Using ENUM Columns

An enumeration value must be a quoted string literal. For example, you can create a table with an
ENUM column like this:

CREATE TABLE shirts (
    name VARCHAR(40),
    size ENUM('x-small', 'small', 'medium', 'large', 'x-large')
);
INSERT INTO shirts (name, size) VALUES ('dress shirt','large'), ('t-shirt','medium'),
  ('polo shirt','small');
SELECT name, size FROM shirts WHERE size = 'medium';
+---------+--------+
| name    | size   |
+---------+--------+
| t-shirt | medium |
+---------+--------+
UPDATE shirts SET size = 'small' WHERE size = 'large';
COMMIT;

Inserting 1 million rows into this table with a value of 'medium' would require 1 million bytes of
storage, as opposed to 6 million bytes if you stored the actual string 'medium' in a VARCHAR column.

Index Values for Enumeration Literals

Each enumeration value has an index:

• The elements listed in the column specification are assigned index numbers, beginning with 1.

• The index value of the empty string error value is 0. This means that you can use the following

SELECT statement to find rows into which invalid ENUM values were assigned:

mysql> SELECT * FROM tbl_name WHERE enum_col=0;

• The index of the NULL value is NULL.

• The term “index” here refers to a position within the list of enumeration values. It has nothing to do

with table indexes.

For example, a column specified as ENUM('Mercury', 'Venus', 'Earth') can have any of the
values shown here. The index of each value is also shown.

Value

NULL

''

'Mercury'

'Venus'

'Earth'

Index

NULL

0

1

2

3

An ENUM column can have a maximum of 65,535 distinct elements.

If you retrieve an ENUM value in a numeric context, the column value's index is returned. For example,
you can retrieve numeric values from an ENUM column like this:

mysql> SELECT enum_col+0 FROM tbl_name;

Functions such as SUM() or AVG() that expect a numeric argument cast the argument to a number if
necessary. For ENUM values, the index number is used in the calculation.

2229

The ENUM Type

Handling of Enumeration Literals

Trailing spaces are automatically deleted from ENUM member values in the table definition when a table
is created.

When retrieved, values stored into an ENUM column are displayed using the lettercase that was used
in the column definition. Note that ENUM columns can be assigned a character set and collation. For
binary or case-sensitive collations, lettercase is taken into account when assigning values to the
column.

If you store a number into an ENUM column, the number is treated as the index into the possible values,
and the value stored is the enumeration member with that index. (However, this does not work with
LOAD DATA, which treats all input as strings.) If the numeric value is quoted, it is still interpreted as
an index if there is no matching string in the list of enumeration values. For these reasons, it is not
advisable to define an ENUM column with enumeration values that look like numbers, because this can
easily become confusing. For example, the following column has enumeration members with string
values of '0', '1', and '2', but numeric index values of 1, 2, and 3:

numbers ENUM('0','1','2')

If you store 2, it is interpreted as an index value, and becomes '1' (the value with index 2). If you store
'2', it matches an enumeration value, so it is stored as '2'. If you store '3', it does not match any
enumeration value, so it is treated as an index and becomes '2' (the value with index 3).

mysql> INSERT INTO t (numbers) VALUES(2),('2'),('3');
mysql> SELECT * FROM t;
+---------+
| numbers |
+---------+
| 1       |
| 2       |
| 2       |
+---------+

To determine all possible values for an ENUM column, use SHOW COLUMNS FROM tbl_name LIKE
'enum_col' and parse the ENUM definition in the Type column of the output.

In the C API, ENUM values are returned as strings. For information about using result set metadata to
distinguish them from other strings, see C API Basic Data Structures.

Empty or NULL Enumeration Values

An enumeration value can also be the empty string ('') or NULL under certain circumstances:

• If you insert an invalid value into an ENUM (that is, a string not present in the list of permitted values),
the empty string is inserted instead as a special error value. This string can be distinguished from
a “normal” empty string by the fact that this string has the numeric value 0. See Index Values for
Enumeration Literals for details about the numeric indexes for the enumeration values.

If strict SQL mode is enabled, attempts to insert invalid ENUM values result in an error.

• If an ENUM column is declared to permit NULL, the NULL value is a valid value for the column, and the
default value is NULL. If an ENUM column is declared NOT NULL, its default value is the first element
of the list of permitted values.

Enumeration Sorting

ENUM values are sorted based on their index numbers, which depend on the order in which the
enumeration members were listed in the column specification. For example, 'b' sorts before 'a' for
ENUM('b', 'a'). The empty string sorts before nonempty strings, and NULL values sort before all
other enumeration values.

2230

The SET Type

To prevent unexpected results when using the ORDER BY clause on an ENUM column, use one of these
techniques:

• Specify the ENUM list in alphabetic order.

• Make sure that the column is sorted lexically rather than by index number by coding ORDER BY

CAST(col AS CHAR) or ORDER BY CONCAT(col).

Enumeration Limitations

An enumeration value cannot be an expression, even one that evaluates to a string value.

For example, this CREATE TABLE statement does not work because the CONCAT function cannot be
used to construct an enumeration value:

CREATE TABLE sizes (
    size ENUM('small', CONCAT('med','ium'), 'large')
);

You also cannot employ a user variable as an enumeration value. This pair of statements do not work:

SET @mysize = 'medium';

CREATE TABLE sizes (
    size ENUM('small', @mysize, 'large')
);

We strongly recommend that you do not use numbers as enumeration values, because it does not
save on storage over the appropriate TINYINT or SMALLINT type, and it is easy to mix up the strings
and the underlying number values (which might not be the same) if you quote the ENUM values
incorrectly. If you do use a number as an enumeration value, always enclose it in quotation marks. If
the quotation marks are omitted, the number is regarded as an index. See Handling of Enumeration
Literals to see how even a quoted number could be mistakenly used as a numeric index value.

Duplicate values in the definition cause a warning, or an error if strict SQL mode is enabled.

13.3.6 The SET Type

A SET is a string object that can have zero or more values, each of which must be chosen from a list
of permitted values specified when the table is created. SET column values that consist of multiple set
members are specified with members separated by commas (,). A consequence of this is that SET
member values should not themselves contain commas.

For example, a column specified as SET('one', 'two') NOT NULL can have any of these values:

''
'one'
'two'
'one,two'

A SET column can have a maximum of 64 distinct members.

Duplicate values in the definition cause a warning, or an error if strict SQL mode is enabled.

Trailing spaces are automatically deleted from SET member values in the table definition when a table
is created.

See String Type Storage Requirements for storage requirements for the SET type.

See Section 13.3.1, “String Data Type Syntax” for SET type syntax and length limits.

When retrieved, values stored in a SET column are displayed using the lettercase that was used in the
column definition. Note that SET columns can be assigned a character set and collation. For binary or
case-sensitive collations, lettercase is taken into account when assigning values to the column.

2231

The SET Type

MySQL stores SET values numerically, with the low-order bit of the stored value corresponding to
the first set member. If you retrieve a SET value in a numeric context, the value retrieved has bits set
corresponding to the set members that make up the column value. For example, you can retrieve
numeric values from a SET column like this:

mysql> SELECT set_col+0 FROM tbl_name;

If a number is stored into a SET column, the bits that are set in the binary representation of the number
determine the set members in the column value. For a column specified as SET('a','b','c','d'),
the members have the following decimal and binary values.

SET Member

Decimal Value

Binary Value

'a'

'b'

'c'

'd'

1

2

4

8

0001

0010

0100

1000

If you assign a value of 9 to this column, that is 1001 in binary, so the first and fourth SET value
members 'a' and 'd' are selected and the resulting value is 'a,d'.

For a value containing more than one SET element, it does not matter what order the elements are
listed in when you insert the value. It also does not matter how many times a given element is listed in
the value. When the value is retrieved later, each element in the value appears once, with elements
listed according to the order in which they were specified at table creation time. Suppose that a column
is specified as SET('a','b','c','d'):

mysql> CREATE TABLE myset (col SET('a', 'b', 'c', 'd'));

If you insert the values 'a,d', 'd,a', 'a,d,d', 'a,d,a', and 'd,a,d':

mysql> INSERT INTO myset (col) VALUES
-> ('a,d'), ('d,a'), ('a,d,a'), ('a,d,d'), ('d,a,d');
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

Then all these values appear as 'a,d' when retrieved:

mysql> SELECT col FROM myset;
+------+
| col  |
+------+
| a,d  |
| a,d  |
| a,d  |
| a,d  |
| a,d  |
+------+
5 rows in set (0.04 sec)

If you set a SET column to an unsupported value, the value is ignored and a warning is issued:

mysql> INSERT INTO myset (col) VALUES ('a,d,d,s');
Query OK, 1 row affected, 1 warning (0.03 sec)

mysql> SHOW WARNINGS;
+---------+------+------------------------------------------+
| Level   | Code | Message                                  |
+---------+------+------------------------------------------+
| Warning | 1265 | Data truncated for column 'col' at row 1 |
+---------+------+------------------------------------------+
1 row in set (0.04 sec)

mysql> SELECT col FROM myset;
+------+
| col  |

2232

Spatial Data Types

+------+
| a,d  |
| a,d  |
| a,d  |
| a,d  |
| a,d  |
| a,d  |
+------+
6 rows in set (0.01 sec)

If strict SQL mode is enabled, attempts to insert invalid SET values result in an error.

SET values are sorted numerically. NULL values sort before non-NULL SET values.

Functions such as SUM() or AVG() that expect a numeric argument cast the argument to a number if
necessary. For SET values, the cast operation causes the numeric value to be used.

Normally, you search for SET values using the FIND_IN_SET() function or the LIKE operator:

mysql> SELECT * FROM tbl_name WHERE FIND_IN_SET('value',set_col)>0;
mysql> SELECT * FROM tbl_name WHERE set_col LIKE '%value%';

The first statement finds rows where set_col contains the value set member. The second is similar,
but not the same: It finds rows where set_col contains value anywhere, even as a substring of
another set member.

The following statements also are permitted:

mysql> SELECT * FROM tbl_name WHERE set_col & 1;
mysql> SELECT * FROM tbl_name WHERE set_col = 'val1,val2';

The first of these statements looks for values containing the first set member. The second looks for an
exact match. Be careful with comparisons of the second type. Comparing set values to 'val1,val2'
returns different results than comparing values to 'val2,val1'. You should specify the values in the
same order they are listed in the column definition.

To determine all possible values for a SET column, use SHOW COLUMNS FROM tbl_name LIKE
set_col and parse the SET definition in the Type column of the output.

In the C API, SET values are returned as strings. For information about using result set metadata to
distinguish them from other strings, see C API Basic Data Structures.

13.4 Spatial Data Types

The Open Geospatial Consortium (OGC) is an international consortium of more than 250 companies,
agencies, and universities participating in the development of publicly available conceptual solutions
that can be useful with all kinds of applications that manage spatial data.

The Open Geospatial Consortium publishes the OpenGIS® Implementation Standard for Geographic
information - Simple feature access - Part 2: SQL option, a document that proposes several conceptual
ways for extending an SQL RDBMS to support spatial data. This specification is available from the
OGC website at http://www.opengeospatial.org/standards/sfs.

Following the OGC specification, MySQL implements spatial extensions as a subset of the SQL with
Geometry Types environment. This term refers to an SQL environment that has been extended
with a set of geometry types. A geometry-valued SQL column is implemented as a column that has a
geometry type. The specification describes a set of SQL geometry types, as well as functions on those
types to create and analyze geometry values.

MySQL spatial extensions enable the generation, storage, and analysis of geographic features:

• Data types for representing spatial values

• Functions for manipulating spatial values

2233

Additional Resources

• Spatial indexing for improved access times to spatial columns

The spatial data types and functions are available for MyISAM, InnoDB, NDB, and ARCHIVE tables.
For indexing spatial columns, MyISAM and InnoDB support both SPATIAL and non-SPATIAL indexes.
The other storage engines support non-SPATIAL indexes, as described in Section 15.1.15, “CREATE
INDEX Statement”.

A geographic feature is anything in the world that has a location. A feature can be:

• An entity. For example, a mountain, a pond, a city.

• A space. For example, town district, the tropics.

• A definable location. For example, a crossroad, as a particular place where two streets intersect.

Some documents use the term geospatial feature to refer to geographic features.

Geometry is another word that denotes a geographic feature. Originally the word geometry meant
measurement of the earth. Another meaning comes from cartography, referring to the geometric
features that cartographers use to map the world.

The discussion here considers these terms synonymous: geographic feature, geospatial feature,
feature, or geometry. The term most commonly used is geometry, defined as a point or an aggregate
of points representing anything in the world that has a location.

The following material covers these topics:

• The spatial data types implemented in MySQL model

• The basis of the spatial extensions in the OpenGIS geometry model

• Data formats for representing spatial data

• How to use spatial data in MySQL

• Use of indexing for spatial data

• MySQL differences from the OpenGIS specification

For information about functions that operate on spatial data, see Section 14.16, “Spatial Analysis
Functions”.

Additional Resources

These standards are important for the MySQL implementation of spatial operations:

• SQL/MM Part 3: Spatial.

• The Open Geospatial Consortium publishes the OpenGIS® Implementation Standard for Geographic

information, a document that proposes several conceptual ways for extending an SQL RDBMS
to support spatial data. See in particular Simple Feature Access - Part 1: Common Architecture,
and Simple Feature Access - Part 2: SQL Option. The Open Geospatial Consortium (OGC)
maintains a website at http://www.opengeospatial.org/. The specification is available there at http://
www.opengeospatial.org/standards/sfs. It contains additional information relevant to the material
here.

• The grammar for spatial reference system (SRS) definitions is based on the grammar defined
in OpenGIS Implementation Specification: Coordinate Transformation Services, Revision
1.00, OGC 01-009, January 12, 2001, Section 7.2. This specification is available at http://
www.opengeospatial.org/standards/ct. For differences from that specification in SRS definitions
as implemented in MySQL, see Section 15.1.19, “CREATE SPATIAL REFERENCE SYSTEM
Statement”.

2234

Spatial Data Types

If you have questions or concerns about the use of the spatial extensions to MySQL, you can discuss
them in the GIS forum: https://forums.mysql.com/list.php?23.

13.4.1 Spatial Data Types

MySQL has spatial data types that correspond to OpenGIS classes. The basis for these types is
described in Section 13.4.2, “The OpenGIS Geometry Model”.

Some spatial data types hold single geometry values:

• GEOMETRY

• POINT

• LINESTRING

• POLYGON

GEOMETRY can store geometry values of any type. The other single-value types (POINT, LINESTRING,
and POLYGON) restrict their values to a particular geometry type.

The other spatial data types hold collections of values:

• MULTIPOINT

• MULTILINESTRING

• MULTIPOLYGON

• GEOMETRYCOLLECTION

GEOMETRYCOLLECTION can store a collection of objects of any type. The other collection types
(MULTIPOINT, MULTILINESTRING, and MULTIPOLYGON) restrict collection members to those having
a particular geometry type.

Example: To create a table named geom that has a column named g that can store values of any
geometry type, use this statement:

CREATE TABLE geom (g GEOMETRY);

Columns with a spatial data type can have an SRID attribute, to explicitly indicate the spatial reference
system (SRS) for values stored in the column. For example:

CREATE TABLE geom (
    p POINT SRID 0,
    g GEOMETRY NOT NULL SRID 4326
);

SPATIAL indexes can be created on spatial columns if they are NOT NULL and have a specific SRID,
so if you plan to index the column, declare it with the NOT NULL and SRID attributes:

CREATE TABLE geom (g GEOMETRY NOT NULL SRID 4326);

InnoDB tables permit SRID values for Cartesian and geographic SRSs. MyISAM tables permit SRID
values for Cartesian SRSs.

The SRID attribute makes a spatial column SRID-restricted, which has these implications:

• The column can contain only values with the given SRID. Attempts to insert values with a different

SRID produce an error.

• The optimizer can use SPATIAL indexes on the column. See Section 10.3.3, “SPATIAL Index

Optimization”.

2235

The OpenGIS Geometry Model

Spatial columns with no SRID attribute are not SRID-restricted and accept values with any SRID.
However, the optimizer cannot use SPATIAL indexes on them until the column definition is modified
to include an SRID attribute, which may require that the column contents first be modified so that all
values have the same SRID.

For other examples showing how to use spatial data types in MySQL, see Section 13.4.6, “Creating
Spatial Columns”. For information about spatial reference systems, see Section 13.4.5, “Spatial
Reference System Support”.

13.4.2 The OpenGIS Geometry Model

The set of geometry types proposed by OGC's SQL with Geometry Types environment is based
on the OpenGIS Geometry Model. In this model, each geometric object has the following general
properties:

• It is associated with a spatial reference system, which describes the coordinate space in which the

object is defined.

• It belongs to some geometry class.

13.4.2.1 The Geometry Class Hierarchy

The geometry classes define a hierarchy as follows:

• Geometry (noninstantiable)

• Point (instantiable)

• Curve (noninstantiable)

• LineString (instantiable)

• Line

• LinearRing

• Surface (noninstantiable)

• Polygon (instantiable)

• GeometryCollection (instantiable)

• MultiPoint (instantiable)

• MultiCurve (noninstantiable)

• MultiLineString (instantiable)

• MultiSurface (noninstantiable)

• MultiPolygon (instantiable)

It is not possible to create objects in noninstantiable classes. It is possible to create objects in
instantiable classes. All classes have properties, and instantiable classes may also have assertions
(rules that define valid class instances).

Geometry is the base class. It is an abstract class. The instantiable subclasses of Geometry
are restricted to zero-, one-, and two-dimensional geometric objects that exist in two-dimensional
coordinate space. All instantiable geometry classes are defined so that valid instances of a geometry
class are topologically closed (that is, all defined geometries include their boundary).

The base Geometry class has subclasses for Point, Curve, Surface, and GeometryCollection:

2236

The OpenGIS Geometry Model

• Point represents zero-dimensional objects.

• Curve represents one-dimensional objects, and has subclass LineString, with sub-subclasses

Line and LinearRing.

• Surface is designed for two-dimensional objects and has subclass Polygon.

• GeometryCollection has specialized zero-, one-, and two-dimensional collection classes named
MultiPoint, MultiLineString, and MultiPolygon for modeling geometries corresponding
to collections of Points, LineStrings, and Polygons, respectively. MultiCurve and
MultiSurface are introduced as abstract superclasses that generalize the collection interfaces to
handle Curves and Surfaces.

Geometry, Curve, Surface, MultiCurve, and MultiSurface are defined as noninstantiable
classes. They define a common set of methods for their subclasses and are included for extensibility.

Point, LineString, Polygon, GeometryCollection, MultiPoint, MultiLineString, and
MultiPolygon are instantiable classes.

13.4.2.2 Geometry Class

Geometry is the root class of the hierarchy. It is a noninstantiable class but has a number of
properties, described in the following list, that are common to all geometry values created from any of
the Geometry subclasses. Particular subclasses have their own specific properties, described later.

Geometry Properties

A geometry value has the following properties:

• Its type. Each geometry belongs to one of the instantiable classes in the hierarchy.

• Its SRID, or spatial reference identifier. This value identifies the geometry's associated spatial
reference system that describes the coordinate space in which the geometry object is defined.

In MySQL, the SRID value is an integer associated with the geometry value. The maximum usable
SRID value is 232

−1. If a larger value is given, only the lower 32 bits are used.

SRID 0 represents an infinite flat Cartesian plane with no units assigned to its axes. To ensure SRID
0 behavior, create geometry values using SRID 0. SRID 0 is the default for new geometry values if
no SRID is specified.

For computations on multiple geometry values, all values must have the same SRID or an error
occurs.

• Its coordinates in its spatial reference system, represented as double-precision (8-byte) numbers.

All nonempty geometries include at least one pair of (X,Y) coordinates. Empty geometries contain no
coordinates.

Coordinates are related to the SRID. For example, in different coordinate systems, the distance
between two objects may differ even when objects have the same coordinates, because the distance
on the planar coordinate system and the distance on the geodetic system (coordinates on the
Earth's surface) are different things.

• Its interior, boundary, and exterior.

Every geometry occupies some position in space. The exterior of a geometry is all space not
occupied by the geometry. The interior is the space occupied by the geometry. The boundary is the
interface between the geometry's interior and exterior.

• Its MBR (minimum bounding rectangle), or envelope. This is the bounding geometry, formed by the

minimum and maximum (X,Y) coordinates:

2237

The OpenGIS Geometry Model

((MINX MINY, MAXX MINY, MAXX MAXY, MINX MAXY, MINX MINY))

• Whether the value is simple or nonsimple. Geometry values of types (LineString, MultiPoint,
MultiLineString) are either simple or nonsimple. Each type determines its own assertions for
being simple or nonsimple.

• Whether the value is closed or not closed. Geometry values of types (LineString,

MultiString) are either closed or not closed. Each type determines its own assertions for being
closed or not closed.

• Whether the value is empty or nonempty A geometry is empty if it does not have any points.

Exterior, interior, and boundary of an empty geometry are not defined (that is, they are represented
by a NULL value). An empty geometry is defined to be always simple and has an area of 0.

• Its dimension. A geometry can have a dimension of −1, 0, 1, or 2:

• −1 for an empty geometry.

• 0 for a geometry with no length and no area.

• 1 for a geometry with nonzero length and zero area.

• 2 for a geometry with nonzero area.

Point objects have a dimension of zero. LineString objects have a dimension of 1. Polygon
objects have a dimension of 2. The dimensions of MultiPoint, MultiLineString, and
MultiPolygon objects are the same as the dimensions of the elements they consist of.

13.4.2.3 Point Class

A Point is a geometry that represents a single location in coordinate space.

Point Examples

• Imagine a large-scale map of the world with many cities. A Point object could represent each city.

• On a city map, a Point object could represent a bus stop.

Point Properties

• X-coordinate value.

• Y-coordinate value.

• Point is defined as a zero-dimensional geometry.

• The boundary of a Point is the empty set.

13.4.2.4 Curve Class

A Curve is a one-dimensional geometry, usually represented by a sequence of points. Particular
subclasses of Curve define the type of interpolation between points. Curve is a noninstantiable class.

Curve Properties

• A Curve has the coordinates of its points.

• A Curve is defined as a one-dimensional geometry.

• A Curve is simple if it does not pass through the same point twice, with the exception that a curve

can still be simple if the start and end points are the same.

• A Curve is closed if its start point is equal to its endpoint.

2238

The OpenGIS Geometry Model

• The boundary of a closed Curve is empty.

• The boundary of a nonclosed Curve consists of its two endpoints.

• A Curve that is simple and closed is a LinearRing.

13.4.2.5 LineString Class

A LineString is a Curve with linear interpolation between points.

LineString Examples

• On a world map, LineString objects could represent rivers.

• In a city map, LineString objects could represent streets.

LineString Properties

• A LineString has coordinates of segments, defined by each consecutive pair of points.

• A LineString is a Line if it consists of exactly two points.

• A LineString is a LinearRing if it is both closed and simple.

13.4.2.6 Surface Class

A Surface is a two-dimensional geometry. It is a noninstantiable class. Its only instantiable subclass is
Polygon.

Simple surfaces in three-dimensional space are isomorphic to planar surfaces.

Polyhedral surfaces are formed by “stitching” together simple surfaces along their boundaries,
polyhedral surfaces in three-dimensional space may not be planar as a whole.

Surface Properties

• A Surface is defined as a two-dimensional geometry.

• The OpenGIS specification defines a simple Surface as a geometry that consists of a single “patch”

that is associated with a single exterior boundary and zero or more interior boundaries.

• The boundary of a simple Surface is the set of closed curves corresponding to its exterior and

interior boundaries.

13.4.2.7 Polygon Class

A Polygon is a planar Surface representing a multisided geometry. It is defined by a single exterior
boundary and zero or more interior boundaries, where each interior boundary defines a hole in the
Polygon.

Polygon Examples

• On a region map, Polygon objects could represent forests, districts, and so on.

Polygon Assertions

• The boundary of a Polygon consists of a set of LinearRing objects (that is, LineString objects

that are both simple and closed) that make up its exterior and interior boundaries.

• A Polygon has no rings that cross. The rings in the boundary of a Polygon may intersect at a

Point, but only as a tangent.

• A Polygon has no lines, spikes, or punctures.

2239

The OpenGIS Geometry Model

• A Polygon has an interior that is a connected point set.

• A Polygon may have holes. The exterior of a Polygon with holes is not connected. Each hole

defines a connected component of the exterior.

The preceding assertions make a Polygon a simple geometry.

13.4.2.8 GeometryCollection Class

A GeomCollection is a geometry that is a collection of zero or more geometries of any class.

GeomCollection and GeometryCollection are synonymous, with GeomCollection the
preferred type name.

All the elements in a geometry collection must be in the same spatial reference system (that is, in the
same coordinate system). There are no other constraints on the elements of a geometry collection,
although the subclasses of GeomCollection described in the following sections may restrict
membership. Restrictions may be based on:

• Element type (for example, a MultiPoint may contain only Point elements)

• Dimension

• Constraints on the degree of spatial overlap between elements

13.4.2.9 MultiPoint Class

A MultiPoint is a geometry collection composed of Point elements. The points are not connected
or ordered in any way.

MultiPoint Examples

• On a world map, a MultiPoint could represent a chain of small islands.

• On a city map, a MultiPoint could represent the outlets for a ticket office.

MultiPoint Properties

• A MultiPoint is a zero-dimensional geometry.

• A MultiPoint is simple if no two of its Point values are equal (have identical coordinate values).

• The boundary of a MultiPoint is the empty set.

13.4.2.10 MultiCurve Class

A MultiCurve is a geometry collection composed of Curve elements. MultiCurve is a
noninstantiable class.

MultiCurve Properties

• A MultiCurve is a one-dimensional geometry.

• A MultiCurve is simple if and only if all of its elements are simple; the only intersections between

any two elements occur at points that are on the boundaries of both elements.

• A MultiCurve boundary is obtained by applying the “mod 2 union rule” (also known as the “odd-

even rule”): A point is in the boundary of a MultiCurve if it is in the boundaries of an odd number of
Curve elements.

• A MultiCurve is closed if all of its elements are closed.

• The boundary of a closed MultiCurve is always empty.

2240

Supported Spatial Data Formats

13.4.2.11 MultiLineString Class

A MultiLineString is a MultiCurve geometry collection composed of LineString elements.

MultiLineString Examples

• On a region map, a MultiLineString could represent a river system or a highway system.

13.4.2.12 MultiSurface Class

A MultiSurface is a geometry collection composed of surface elements. MultiSurface is a
noninstantiable class. Its only instantiable subclass is MultiPolygon.

MultiSurface Assertions

• Surfaces within a MultiSurface have no interiors that intersect.

• Surfaces within a MultiSurface have boundaries that intersect at most at a finite number of points.

13.4.2.13 MultiPolygon Class

A MultiPolygon is a MultiSurface object composed of Polygon elements.

MultiPolygon Examples

• On a region map, a MultiPolygon could represent a system of lakes.

MultiPolygon Assertions

• A MultiPolygon has no two Polygon elements with interiors that intersect.

• A MultiPolygon has no two Polygon elements that cross (crossing is also forbidden by the

previous assertion), or that touch at an infinite number of points.

• A MultiPolygon may not have cut lines, spikes, or punctures. A MultiPolygon is a regular,

closed point set.

• A MultiPolygon that has more than one Polygon has an interior that is not connected. The
number of connected components of the interior of a MultiPolygon is equal to the number of
Polygon values in the MultiPolygon.

MultiPolygon Properties

• A MultiPolygon is a two-dimensional geometry.

• A MultiPolygon boundary is a set of closed curves (LineString values) corresponding to the

boundaries of its Polygon elements.

• Each Curve in the boundary of the MultiPolygon is in the boundary of exactly one Polygon

element.

• Every Curve in the boundary of an Polygon element is in the boundary of the MultiPolygon.

13.4.3 Supported Spatial Data Formats

Two standard spatial data formats are used to represent geometry objects in queries:

• Well-Known Text (WKT) format

• Well-Known Binary (WKB) format

Internally, MySQL stores geometry values in a format that is not identical to either WKT or WKB format.
(Internal format is like WKB but with an initial 4 bytes to indicate the SRID.)

2241

Supported Spatial Data Formats

There are functions available to convert between different data formats; see Section 14.16.6,
“Geometry Format Conversion Functions”.

The following sections describe the spatial data formats MySQL uses:

• Well-Known Text (WKT) Format

• Well-Known Binary (WKB) Format

• Internal Geometry Storage Format

Well-Known Text (WKT) Format

The Well-Known Text (WKT) representation of geometry values is designed for exchanging geometry
data in ASCII form. The OpenGIS specification provides a Backus-Naur grammar that specifies the
formal production rules for writing WKT values (see Section 13.4, “Spatial Data Types”).

Examples of WKT representations of geometry objects:

• A Point:

POINT(15 20)

The point coordinates are specified with no separating comma. This differs from the syntax for the
SQL Point() function, which requires a comma between the coordinates. Take care to use the
syntax appropriate to the context of a given spatial operation. For example, the following statements
both use ST_X() to extract the X-coordinate from a Point object. The first produces the object
directly using the Point() function. The second uses a WKT representation converted to a Point
with ST_GeomFromText().

mysql> SELECT ST_X(Point(15, 20));
+---------------------+
| ST_X(POINT(15, 20)) |
+---------------------+
|                  15 |
+---------------------+

mysql> SELECT ST_X(ST_GeomFromText('POINT(15 20)'));
+---------------------------------------+
| ST_X(ST_GeomFromText('POINT(15 20)')) |
+---------------------------------------+
|                                    15 |
+---------------------------------------+

• A LineString with four points:

LINESTRING(0 0, 10 10, 20 25, 50 60)

The point coordinate pairs are separated by commas.

• A Polygon with one exterior ring and one interior ring:

POLYGON((0 0,10 0,10 10,0 10,0 0),(5 5,7 5,7 7,5 7, 5 5))

• A MultiPoint with three Point values:

MULTIPOINT(0 0, 20 20, 60 60)

Spatial functions such as ST_MPointFromText() and ST_GeomFromText() that accept
WKT-format representations of MultiPoint values permit individual points within values to be
surrounded by parentheses. For example, both of the following function calls are valid:

ST_MPointFromText('MULTIPOINT (1 1, 2 2, 3 3)')
ST_MPointFromText('MULTIPOINT ((1 1), (2 2), (3 3))')

• A MultiLineString with two LineString values:

2242

Supported Spatial Data Formats

MULTILINESTRING((10 10, 20 20), (15 15, 30 15))

• A MultiPolygon with two Polygon values:

MULTIPOLYGON(((0 0,10 0,10 10,0 10,0 0)),((5 5,7 5,7 7,5 7, 5 5)))

• A GeometryCollection consisting of two Point values and one LineString:

GEOMETRYCOLLECTION(POINT(10 10), POINT(30 30), LINESTRING(15 15, 20 20))

Well-Known Binary (WKB) Format

The Well-Known Binary (WKB) representation of geometric values is used for exchanging geometry
data as binary streams represented by BLOB values containing geometric WKB information. This
format is defined by the OpenGIS specification (see Section 13.4, “Spatial Data Types”). It is also
defined in the ISO SQL/MM Part 3: Spatial standard.

WKB uses 1-byte unsigned integers, 4-byte unsigned integers, and 8-byte double-precision numbers
(IEEE 754 format). A byte is eight bits.

For example, a WKB value that corresponds to POINT(1 -1) consists of this sequence of 21 bytes,
each represented by two hexadecimal digits:

0101000000000000000000F03F000000000000F0BF

The sequence consists of the components shown in the following table.

Table 13.2 WKB Components Example

Component

Byte order

WKB type

X coordinate

Y coordinate

Size

1 byte

4 bytes

8 bytes

8 bytes

Component representation is as follows:

Value

01

01000000

000000000000F03F

000000000000F0BF

• The byte order indicator is either 1 or 0 to signify little-endian or big-endian storage. The little-endian
and big-endian byte orders are also known as Network Data Representation (NDR) and External
Data Representation (XDR), respectively.

• The WKB type is a code that indicates the geometry type. MySQL uses values from 1 through 7 to

indicate Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, and
GeometryCollection.

• A Point value has X and Y coordinates, each represented as a double-precision value.

WKB values for more complex geometry values have more complex data structures, as detailed in the
OpenGIS specification.

Internal Geometry Storage Format

MySQL stores geometry values using 4 bytes to indicate the SRID followed by the WKB representation
of the value. For a description of WKB format, see Well-Known Binary (WKB) Format.

For the WKB part, these MySQL-specific considerations apply:

• The byte-order indicator byte is 1 because MySQL stores geometries as little-endian values.

• MySQL supports geometry types of Point, LineString, Polygon, MultiPoint,

MultiLineString, MultiPolygon, and GeometryCollection. Other geometry types are not
supported.

2243

Geometry Well-Formedness and Validity

• Only GeometryCollection can be empty. Such a value is stored with 0 elements.

• Polygon rings can be specified both clockwise and counterclockwise. MySQL flips the rings

automatically when reading data.

Cartesian coordinates are stored in the length unit of the spatial reference system, with X values in
the X coordinates and Y values in the Y coordinates. Axis directions are those specified by the spatial
reference system.

Geographic coordinates are stored in the angle unit of the spatial reference system, with longitudes
in the X coordinates and latitudes in the Y coordinates. Axis directions and the meridian are those
specified by the spatial reference system.

The LENGTH() function returns the space in bytes required for value storage. Example:

mysql> SET @g = ST_GeomFromText('POINT(1 -1)');
mysql> SELECT LENGTH(@g);
+------------+
| LENGTH(@g) |
+------------+
|         25 |
+------------+
mysql> SELECT HEX(@g);
+----------------------------------------------------+
| HEX(@g)                                            |
+----------------------------------------------------+
| 000000000101000000000000000000F03F000000000000F0BF |
+----------------------------------------------------+

The value length is 25 bytes, made up of these components (as can be seen from the hexadecimal
value):

• 4 bytes for integer SRID (0)

• 1 byte for integer byte order (1 = little-endian)

• 4 bytes for integer type information (1 = Point)

• 8 bytes for double-precision X coordinate (1)

• 8 bytes for double-precision Y coordinate (−1)

13.4.4 Geometry Well-Formedness and Validity

For geometry values, MySQL distinguishes between the concepts of syntactically well-formed and
geometrically valid.

A geometry is syntactically well-formed if it satisfies conditions such as those in this (nonexhaustive)
list:

• Linestrings have at least two points

• Polygons have at least one ring

• Polygon rings are closed (first and last points the same)

• Polygon rings have at least 4 points (minimum polygon is a triangle with first and last points the

same)

• Collections are not empty (except GeometryCollection)

A geometry is geometrically valid if it is syntactically well-formed and satisfies conditions such as those
in this (nonexhaustive) list:

• Polygons are not self-intersecting

2244

Spatial Reference System Support

• Polygon interior rings are inside the exterior ring

• Multipolygons do not have overlapping polygons

Spatial functions fail if a geometry is not syntactically well-formed. Spatial import functions that parse
WKT or WKB values raise an error for attempts to create a geometry that is not syntactically well-
formed. Syntactic well-formedness is also checked for attempts to store geometries into tables.

It is permitted to insert, select, and update geometrically invalid geometries, but they must be
syntactically well-formed. Due to the computational expense, MySQL does not check explicitly for
geometric validity. Spatial computations may detect some cases of invalid geometries and raise an
error, but they may also return an undefined result without detecting the invalidity. Applications that
require geometrically-valid geometries should check them using the ST_IsValid() function.

13.4.5 Spatial Reference System Support

A spatial reference system (SRS) for spatial data is a coordinate-based system for geographic
locations.

There are different types of spatial reference systems:

• A projected SRS is a projection of a globe onto a flat surface; that is, a flat map. For example, a light
bulb inside a globe that shines on a paper cylinder surrounding the globe projects a map onto the
paper. The result is georeferenced: Each point maps to a place on the globe. The coordinate system
on that plane is Cartesian using a length unit (meters, feet, and so forth), rather than degrees of
longitude and latitude.

The globes in this case are ellipsoids; that is, flattened spheres. Earth is a bit shorter in its North-
South axis than its East-West axis, so a slightly flattened sphere is more correct, but perfect spheres
permit faster calculations.

• A geographic SRS is a nonprojected SRS representing longitude-latitude (or latitude-longitude)

coordinates on an ellipsoid, in any angular unit.

• The SRS denoted in MySQL by SRID 0 represents an infinite flat Cartesian plane with no units
assigned to its axes. Unlike projected SRSs, it is not georeferenced and it does not necessarily
represent Earth. It is an abstract plane that can be used for anything. SRID 0 is the default SRID for
spatial data in MySQL.

MySQL maintains information about available spatial reference systems for spatial data in the
data dictionary mysql.st_spatial_reference_systems table, which can store entries for
projected and geographic SRSs. This data dictionary table is invisible, but SRS entry contents
are available through the INFORMATION_SCHEMA ST_SPATIAL_REFERENCE_SYSTEMS table,
implemented as a view on mysql.st_spatial_reference_systems (see Section 28.3.36, “The
INFORMATION_SCHEMA ST_SPATIAL_REFERENCE_SYSTEMS Table”).

The following example shows what an SRS entry looks like:

mysql> SELECT *
       FROM INFORMATION_SCHEMA.ST_SPATIAL_REFERENCE_SYSTEMS
       WHERE SRS_ID = 4326\G
*************************** 1. row ***************************
                SRS_NAME: WGS 84
                  SRS_ID: 4326
            ORGANIZATION: EPSG
ORGANIZATION_COORDSYS_ID: 4326
              DEFINITION: GEOGCS["WGS 84",DATUM["World Geodetic System 1984",
                          SPHEROID["WGS 84",6378137,298.257223563,
                          AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],
                          PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],
                          UNIT["degree",0.017453292519943278,
                          AUTHORITY["EPSG","9122"]],
                          AXIS["Lat",NORTH],AXIS["Long",EAST],
                          AUTHORITY["EPSG","4326"]]

2245

Creating Spatial Columns

             DESCRIPTION:

This entry describes the SRS used for GPS systems. It has the name (SRS_NAME) WGS 84 and the ID
(SRS_ID) 4326, which is the ID used by the European Petroleum Survey Group (EPSG).

SRS definitions in the DEFINITION column are WKT values, represented as specified in the Open
Geospatial Consortium document OGC 12-063r5.

SRS_ID values represent the same kind of values as the SRID of geometry values or passed as the
SRID argument to spatial functions. SRID 0 (the unitless Cartesian plane) is special. It is always a legal
spatial reference system ID and can be used in any computations on spatial data that depend on SRID
values.

For computations on multiple geometry values, all values must have the same SRID or an error occurs.

SRS definition parsing occurs on demand when definitions are needed by GIS functions. Parsed
definitions are stored in the data dictionary cache to enable reuse and avoid incurring parsing overhead
for every statement that needs SRS information.

To enable manipulation of SRS entries stored in the data dictionary, MySQL provides these SQL
statements:

• CREATE SPATIAL REFERENCE SYSTEM: See Section 15.1.19, “CREATE SPATIAL REFERENCE
SYSTEM Statement”. The description for this statement includes additional information about SRS
components.

• DROP SPATIAL REFERENCE SYSTEM: See Section 15.1.31, “DROP SPATIAL REFERENCE

SYSTEM Statement”.

13.4.6 Creating Spatial Columns

MySQL provides a standard way of creating spatial columns for geometry types, for example, with
CREATE TABLE or ALTER TABLE. Spatial columns are supported for MyISAM, InnoDB, NDB, and
ARCHIVE tables. See also the notes about spatial indexes under Section 13.4.10, “Creating Spatial
Indexes”.

Columns with a spatial data type can have an SRID attribute, to explicitly indicate the spatial reference
system (SRS) for values stored in the column. For implications of an SRID-restricted column, see
Section 13.4.1, “Spatial Data Types”.

• Use the CREATE TABLE statement to create a table with a spatial column:

CREATE TABLE geom (g GEOMETRY);

• Use the ALTER TABLE statement to add or drop a spatial column to or from an existing table:

ALTER TABLE geom ADD pt POINT;
ALTER TABLE geom DROP pt;

13.4.7 Populating Spatial Columns

After you have created spatial columns, you can populate them with spatial data.

Values should be stored in internal geometry format, but you can convert them to that format
from either Well-Known Text (WKT) or Well-Known Binary (WKB) format. The following examples
demonstrate how to insert geometry values into a table by converting WKT values to internal geometry
format:

• Perform the conversion directly in the INSERT statement:

INSERT INTO geom VALUES (ST_GeomFromText('POINT(1 1)'));

SET @g = 'POINT(1 1)';

2246

Fetching Spatial Data

INSERT INTO geom VALUES (ST_GeomFromText(@g));

• Perform the conversion prior to the INSERT:

SET @g = ST_GeomFromText('POINT(1 1)');
INSERT INTO geom VALUES (@g);

The following examples insert more complex geometries into the table:

SET @g = 'LINESTRING(0 0,1 1,2 2)';
INSERT INTO geom VALUES (ST_GeomFromText(@g));

SET @g = 'POLYGON((0 0,10 0,10 10,0 10,0 0),(5 5,7 5,7 7,5 7, 5 5))';
INSERT INTO geom VALUES (ST_GeomFromText(@g));

SET @g =
'GEOMETRYCOLLECTION(POINT(1 1),LINESTRING(0 0,1 1,2 2,3 3,4 4))';
INSERT INTO geom VALUES (ST_GeomFromText(@g));

The preceding examples use ST_GeomFromText() to create geometry values. You can also use
type-specific functions:

SET @g = 'POINT(1 1)';
INSERT INTO geom VALUES (ST_PointFromText(@g));

SET @g = 'LINESTRING(0 0,1 1,2 2)';
INSERT INTO geom VALUES (ST_LineStringFromText(@g));

SET @g = 'POLYGON((0 0,10 0,10 10,0 10,0 0),(5 5,7 5,7 7,5 7, 5 5))';
INSERT INTO geom VALUES (ST_PolygonFromText(@g));

SET @g =
'GEOMETRYCOLLECTION(POINT(1 1),LINESTRING(0 0,1 1,2 2,3 3,4 4))';
INSERT INTO geom VALUES (ST_GeomCollFromText(@g));

A client application program that wants to use WKB representations of geometry values is responsible
for sending correctly formed WKB in queries to the server. There are several ways to satisfy this
requirement. For example:

• Inserting a POINT(1 1) value with hex literal syntax:

INSERT INTO geom VALUES
(ST_GeomFromWKB(X'0101000000000000000000F03F000000000000F03F'));

• An ODBC application can send a WKB representation, binding it to a placeholder using an argument

of BLOB type:

INSERT INTO geom VALUES (ST_GeomFromWKB(?))

Other programming interfaces may support a similar placeholder mechanism.

• In a C program, you can escape a binary value using mysql_real_escape_string_quote()

and include the result in a query string that is sent to the server. See
mysql_real_escape_string_quote().

13.4.8 Fetching Spatial Data

Geometry values stored in a table can be fetched in internal format. You can also convert them to WKT
or WKB format.

• Fetching spatial data in internal format:

Fetching geometry values using internal format can be useful in table-to-table transfers:

CREATE TABLE geom2 (g GEOMETRY) SELECT g FROM geom;

• Fetching spatial data in WKT format:

2247

Optimizing Spatial Analysis

The ST_AsText() function converts a geometry from internal format to a WKT string.

SELECT ST_AsText(g) FROM geom;

• Fetching spatial data in WKB format:

The ST_AsBinary() function converts a geometry from internal format to a BLOB containing the
WKB value.

SELECT ST_AsBinary(g) FROM geom;

13.4.9 Optimizing Spatial Analysis

For MyISAM and InnoDB tables, search operations in columns containing spatial data can be
optimized using SPATIAL indexes. The most typical operations are:

• Point queries that search for all objects that contain a given point

• Region queries that search for all objects that overlap a given region

MySQL uses R-Trees with quadratic splitting for SPATIAL indexes on spatial columns. A SPATIAL
index is built using the minimum bounding rectangle (MBR) of a geometry. For most geometries, the
MBR is a minimum rectangle that surrounds the geometries. For a horizontal or a vertical linestring, the
MBR is a rectangle degenerated into the linestring. For a point, the MBR is a rectangle degenerated
into the point.

It is also possible to create normal indexes on spatial columns. In a non-SPATIAL index, you must
declare a prefix for any spatial column except for POINT columns.

MyISAM and InnoDB support both SPATIAL and non-SPATIAL indexes. Other storage engines
support non-SPATIAL indexes, as described in Section 15.1.15, “CREATE INDEX Statement”.

13.4.10 Creating Spatial Indexes

For InnoDB and MyISAM tables, MySQL can create spatial indexes using syntax similar to that
for creating regular indexes, but using the SPATIAL keyword. Columns in spatial indexes must be
declared NOT NULL. The following examples demonstrate how to create spatial indexes:

• With CREATE TABLE:

CREATE TABLE geom (g GEOMETRY NOT NULL SRID 4326, SPATIAL INDEX(g));

• With ALTER TABLE:

CREATE TABLE geom (g GEOMETRY NOT NULL SRID 4326);
ALTER TABLE geom ADD SPATIAL INDEX(g);

• With CREATE INDEX:

CREATE TABLE geom (g GEOMETRY NOT NULL SRID 4326);
CREATE SPATIAL INDEX g ON geom (g);

SPATIAL INDEX creates an R-tree index. For storage engines that support nonspatial indexing of
spatial columns, the engine creates a B-tree index. A B-tree index on spatial values is useful for exact-
value lookups, but not for range scans.

The optimizer can use spatial indexes defined on columns that are SRID-restricted. For more
information, see Section 13.4.1, “Spatial Data Types”, and Section 10.3.3, “SPATIAL Index
Optimization”.

For more information on indexing spatial columns, see Section 15.1.15, “CREATE INDEX Statement”.

To drop spatial indexes, use ALTER TABLE or DROP INDEX:

2248

Using Spatial Indexes

• With ALTER TABLE:

ALTER TABLE geom DROP INDEX g;

• With DROP INDEX:

DROP INDEX g ON geom;

Example: Suppose that a table geom contains more than 32,000 geometries, which are stored in the
column g of type GEOMETRY. The table also has an AUTO_INCREMENT column fid for storing object
ID values.

mysql> DESCRIBE geom;
+-------+----------+------+-----+---------+----------------+
| Field | Type     | Null | Key | Default | Extra          |
+-------+----------+------+-----+---------+----------------+
| fid   | int(11)  |      | PRI | NULL    | auto_increment |
| g     | geometry |      |     |         |                |
+-------+----------+------+-----+---------+----------------+
2 rows in set (0.00 sec)

mysql> SELECT COUNT(*) FROM geom;
+----------+
| count(*) |
+----------+
|    32376 |
+----------+
1 row in set (0.00 sec)

To add a spatial index on the column g, use this statement:

mysql> ALTER TABLE geom ADD SPATIAL INDEX(g);
Query OK, 32376 rows affected (4.05 sec)
Records: 32376  Duplicates: 0  Warnings: 0

13.4.11 Using Spatial Indexes

The optimizer investigates whether available spatial indexes can be involved in the search for queries
that use a function such as MBRContains() or MBRWithin() in the WHERE clause. The following
query finds all objects that are in the given rectangle:

mysql> SET @poly =
    -> 'Polygon((30000 15000,
                 31000 15000,
                 31000 16000,
                 30000 16000,
                 30000 15000))';
mysql> SELECT fid,ST_AsText(g) FROM geom WHERE
    -> MBRContains(ST_GeomFromText(@poly),g);
+-----+---------------------------------------------------------------+
| fid | ST_AsText(g)                                                  |
+-----+---------------------------------------------------------------+
|  21 | LINESTRING(30350.4 15828.8,30350.6 15845,30333.8 15845,30 ... |
|  22 | LINESTRING(30350.6 15871.4,30350.6 15887.8,30334 15887.8, ... |
|  23 | LINESTRING(30350.6 15914.2,30350.6 15930.4,30334 15930.4, ... |
|  24 | LINESTRING(30290.2 15823,30290.2 15839.4,30273.4 15839.4, ... |
|  25 | LINESTRING(30291.4 15866.2,30291.6 15882.4,30274.8 15882. ... |
|  26 | LINESTRING(30291.6 15918.2,30291.6 15934.4,30275 15934.4, ... |
| 249 | LINESTRING(30337.8 15938.6,30337.8 15946.8,30320.4 15946. ... |
|   1 | LINESTRING(30250.4 15129.2,30248.8 15138.4,30238.2 15136. ... |
|   2 | LINESTRING(30220.2 15122.8,30217.2 15137.8,30207.6 15136, ... |
|   3 | LINESTRING(30179 15114.4,30176.6 15129.4,30167 15128,3016 ... |
|   4 | LINESTRING(30155.2 15121.4,30140.4 15118.6,30142 15109,30 ... |
|   5 | LINESTRING(30192.4 15085,30177.6 15082.2,30179.2 15072.4, ... |
|   6 | LINESTRING(30244 15087,30229 15086.2,30229.4 15076.4,3024 ... |
|   7 | LINESTRING(30200.6 15059.4,30185.6 15058.6,30186 15048.8, ... |
|  10 | LINESTRING(30179.6 15017.8,30181 15002.8,30190.8 15003.6, ... |
|  11 | LINESTRING(30154.2 15000.4,30168.6 15004.8,30166 15014.2, ... |
|  13 | LINESTRING(30105 15065.8,30108.4 15050.8,30118 15053,3011 ... |
| 154 | LINESTRING(30276.2 15143.8,30261.4 15141,30263 15131.4,30 ... |

2249

Using Spatial Indexes

| 155 | LINESTRING(30269.8 15084,30269.4 15093.4,30258.6 15093,30 ... |
| 157 | LINESTRING(30128.2 15011,30113.2 15010.2,30113.6 15000.4, ... |
+-----+---------------------------------------------------------------+
20 rows in set (0.00 sec)

Use EXPLAIN to check the way this query is executed:

mysql> SET @poly =
    -> 'Polygon((30000 15000,
                 31000 15000,
                 31000 16000,
                 30000 16000,
                 30000 15000))';
mysql> EXPLAIN SELECT fid,ST_AsText(g) FROM geom WHERE
    -> MBRContains(ST_GeomFromText(@poly),g)\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: geom
         type: range
possible_keys: g
          key: g
      key_len: 32
          ref: NULL
         rows: 50
        Extra: Using where
1 row in set (0.00 sec)

Check what would happen without a spatial index:

mysql> SET @poly =
    -> 'Polygon((30000 15000,
                 31000 15000,
                 31000 16000,
                 30000 16000,
                 30000 15000))';
mysql> EXPLAIN SELECT fid,ST_AsText(g) FROM g IGNORE INDEX (g) WHERE
    -> MBRContains(ST_GeomFromText(@poly),g)\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: geom
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 32376
        Extra: Using where
1 row in set (0.00 sec)

Executing the SELECT statement without the spatial index yields the same result but causes the
execution time to rise from 0.00 seconds to 0.46 seconds:

mysql> SET @poly =
    -> 'Polygon((30000 15000,
                 31000 15000,
                 31000 16000,
                 30000 16000,
                 30000 15000))';
mysql> SELECT fid,ST_AsText(g) FROM geom IGNORE INDEX (g) WHERE
    -> MBRContains(ST_GeomFromText(@poly),g);
+-----+---------------------------------------------------------------+
| fid | ST_AsText(g)                                                  |
+-----+---------------------------------------------------------------+
|   1 | LINESTRING(30250.4 15129.2,30248.8 15138.4,30238.2 15136. ... |
|   2 | LINESTRING(30220.2 15122.8,30217.2 15137.8,30207.6 15136, ... |
|   3 | LINESTRING(30179 15114.4,30176.6 15129.4,30167 15128,3016 ... |
|   4 | LINESTRING(30155.2 15121.4,30140.4 15118.6,30142 15109,30 ... |
|   5 | LINESTRING(30192.4 15085,30177.6 15082.2,30179.2 15072.4, ... |
|   6 | LINESTRING(30244 15087,30229 15086.2,30229.4 15076.4,3024 ... |

2250

The JSON Data Type

|   7 | LINESTRING(30200.6 15059.4,30185.6 15058.6,30186 15048.8, ... |
|  10 | LINESTRING(30179.6 15017.8,30181 15002.8,30190.8 15003.6, ... |
|  11 | LINESTRING(30154.2 15000.4,30168.6 15004.8,30166 15014.2, ... |
|  13 | LINESTRING(30105 15065.8,30108.4 15050.8,30118 15053,3011 ... |
|  21 | LINESTRING(30350.4 15828.8,30350.6 15845,30333.8 15845,30 ... |
|  22 | LINESTRING(30350.6 15871.4,30350.6 15887.8,30334 15887.8, ... |
|  23 | LINESTRING(30350.6 15914.2,30350.6 15930.4,30334 15930.4, ... |
|  24 | LINESTRING(30290.2 15823,30290.2 15839.4,30273.4 15839.4, ... |
|  25 | LINESTRING(30291.4 15866.2,30291.6 15882.4,30274.8 15882. ... |
|  26 | LINESTRING(30291.6 15918.2,30291.6 15934.4,30275 15934.4, ... |
| 154 | LINESTRING(30276.2 15143.8,30261.4 15141,30263 15131.4,30 ... |
| 155 | LINESTRING(30269.8 15084,30269.4 15093.4,30258.6 15093,30 ... |
| 157 | LINESTRING(30128.2 15011,30113.2 15010.2,30113.6 15000.4, ... |
| 249 | LINESTRING(30337.8 15938.6,30337.8 15946.8,30320.4 15946. ... |
+-----+---------------------------------------------------------------+
20 rows in set (0.46 sec)

13.5 The JSON Data Type

• Creating JSON Values

• Normalization, Merging, and Autowrapping of JSON Values

• Searching and Modifying JSON Values

• JSON Path Syntax

• Comparison and Ordering of JSON Values

• Converting between JSON and non-JSON values

• Aggregation of JSON Values

MySQL supports a native JSON (JavaScript Object Notation) data type defined by RFC 8259 that
enables efficient access to data in JSON documents. The JSON data type provides these advantages
over storing JSON-format strings in a string column:

• Automatic validation of JSON documents stored in JSON columns. Invalid documents produce an

error.

• Optimized storage format. JSON documents stored in JSON columns are converted to an internal
format that permits quick read access to document elements. When the server later must read a
JSON value stored in this binary format, the value need not be parsed from a text representation.
The binary format is structured to enable the server to look up subobjects or nested values directly
by key or array index without reading all values before or after them in the document.

MySQL also supports the JSON Merge Patch format defined in RFC 7396, using the
JSON_MERGE_PATCH() function. See the description of this function, as well as Normalization,
Merging, and Autowrapping of JSON Values, for examples and further information.

Note

This discussion uses JSON in monotype to indicate specifically the JSON data
type and “JSON” in regular font to indicate JSON data in general.

The space required to store a JSON document is roughly the same as for LONGBLOB or LONGTEXT;
see Section 13.7, “Data Type Storage Requirements”, for more information. It is important to keep
in mind that the size of any JSON document stored in a JSON column is limited to the value of the
max_allowed_packet system variable. (When the server is manipulating a JSON value internally
in memory, it can be larger than this; the limit applies when the server stores it.) You can obtain the
amount of space required to store a JSON document using the JSON_STORAGE_SIZE() function; note
that for a JSON column, the storage size—and thus the value returned by this function—is that used by
the column prior to any partial updates that may have been performed on it (see the discussion of the
JSON partial update optimization later in this section).

2251

Partial Updates of JSON Values

Prior to MySQL 8.0.13, a JSON column cannot have a non-NULL default value.

Along with the JSON data type, a set of SQL functions is available to enable operations on JSON
values, such as creation, manipulation, and searching. The following discussion shows examples of
these operations. For details about individual functions, see Section 14.17, “JSON Functions”.

A set of spatial functions for operating on GeoJSON values is also available. See Section 14.16.11,
“Spatial GeoJSON Functions”.

JSON columns, like columns of other binary types, are not indexed directly; instead, you can create
an index on a generated column that extracts a scalar value from the JSON column. See Indexing a
Generated Column to Provide a JSON Column Index, for a detailed example.

The MySQL optimizer also looks for compatible indexes on virtual columns that match JSON
expressions.

In MySQL 8.0.17 and later, the InnoDB storage engine supports multi-valued indexes on JSON arrays.
See Multi-Valued Indexes.

MySQL NDB Cluster 8.0 supports JSON columns and MySQL JSON functions, including creation of an
index on a column generated from a JSON column as a workaround for being unable to index a JSON
column. A maximum of 3 JSON columns per NDB table is supported.

Partial Updates of JSON Values

In MySQL 8.0, the optimizer can perform a partial, in-place update of a JSON column instead
of removing the old document and writing the new document in its entirety to the column. This
optimization can be performed for an update that meets the following conditions:

• The column being updated was declared as JSON.

• The UPDATE statement uses any of the three functions JSON_SET(), JSON_REPLACE(), or

JSON_REMOVE() to update the column. A direct assignment of the column value (for example,
UPDATE mytable SET jcol = '{"a": 10, "b": 25}') cannot be performed as a partial
update.

Updates of multiple JSON columns in a single UPDATE statement can be optimized in this fashion;
MySQL can perform partial updates of only those columns whose values are updated using the three
functions just listed.

• The input column and the target column must be the same column; a statement such as UPDATE
mytable SET jcol1 = JSON_SET(jcol2, '$.a', 100) cannot be performed as a partial
update.

The update can use nested calls to any of the functions listed in the previous item, in any
combination, as long as the input and target columns are the same.

• All changes replace existing array or object values with new ones, and do not add any new elements

to the parent object or array.

• The value being replaced must be at least as large as the replacement value. In other words, the

new value cannot be any larger than the old one.

A possible exception to this requirement occurs when a previous partial update has left sufficient
space for the larger value. You can use the function JSON_STORAGE_FREE() see how much space
has been freed by any partial updates of a JSON column.

Such partial updates can be written to the binary log using a compact format that saves space; this can
be enabled by setting the binlog_row_value_options system variable to PARTIAL_JSON.

It is important to distinguish the partial update of a JSON column value stored in a table from writing
the partial update of a row to the binary log. It is possible for the complete update of a JSON column to

2252

Creating JSON Values

be recorded in the binary log as a partial update. This can happen when either (or both) of the last two
conditions from the previous list is not met but the other conditions are satisfied.

See also the description of binlog_row_value_options.

The next few sections provide basic information regarding the creation and manipulation of JSON
values.

Creating JSON Values

A JSON array contains a list of values separated by commas and enclosed within [ and ] characters:

["abc", 10, null, true, false]

A JSON object contains a set of key-value pairs separated by commas and enclosed within { and }
characters:

{"k1": "value", "k2": 10}

As the examples illustrate, JSON arrays and objects can contain scalar values that are strings or
numbers, the JSON null literal, or the JSON boolean true or false literals. Keys in JSON objects must
be strings. Temporal (date, time, or datetime) scalar values are also permitted:

["12:18:29.000000", "2015-07-29", "2015-07-29 12:18:29.000000"]

Nesting is permitted within JSON array elements and JSON object key values:

[99, {"id": "HK500", "cost": 75.99}, ["hot", "cold"]]
{"k1": "value", "k2": [10, 20]}

You can also obtain JSON values from a number of functions supplied by MySQL for this purpose (see
Section 14.17.2, “Functions That Create JSON Values”) as well as by casting values of other types to
the JSON type using CAST(value AS JSON) (see Converting between JSON and non-JSON values).
The next several paragraphs describe how MySQL handles JSON values provided as input.

In MySQL, JSON values are written as strings. MySQL parses any string used in a context that
requires a JSON value, and produces an error if it is not valid as JSON. These contexts include
inserting a value into a column that has the JSON data type and passing an argument to a function that
expects a JSON value (usually shown as json_doc or json_val in the documentation for MySQL
JSON functions), as the following examples demonstrate:

• Attempting to insert a value into a JSON column succeeds if the value is a valid JSON value, but fails

if it is not:

mysql> CREATE TABLE t1 (jdoc JSON);
Query OK, 0 rows affected (0.20 sec)

mysql> INSERT INTO t1 VALUES('{"key1": "value1", "key2": "value2"}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t1 VALUES('[1, 2,');
ERROR 3140 (22032) at line 2: Invalid JSON text:
"Invalid value." at position 6 in value (or column) '[1, 2,'.

Positions for “at position N” in such error messages are 0-based, but should be considered rough
indications of where the problem in a value actually occurs.

• The JSON_TYPE() function expects a JSON argument and attempts to parse it into a JSON value. It

returns the value's JSON type if it is valid and produces an error otherwise:

mysql> SELECT JSON_TYPE('["a", "b", 1]');
+----------------------------+
| JSON_TYPE('["a", "b", 1]') |
+----------------------------+
| ARRAY                      |

2253

Creating JSON Values

does not have the JSON data type. Instead, the result from JSON_OBJECT() is converted to a string
when assigned to the variable.

Strings produced by converting JSON values have a character set of utf8mb4 and a collation of
utf8mb4_bin:

mysql> SELECT CHARSET(@j), COLLATION(@j);
+-------------+---------------+
| CHARSET(@j) | COLLATION(@j) |
+-------------+---------------+
| utf8mb4     | utf8mb4_bin   |
+-------------+---------------+

Because utf8mb4_bin is a binary collation, comparison of JSON values is case-sensitive.

mysql> SELECT JSON_ARRAY('x') = JSON_ARRAY('X');
+-----------------------------------+
| JSON_ARRAY('x') = JSON_ARRAY('X') |
+-----------------------------------+
|                                 0 |
+-----------------------------------+

Case sensitivity also applies to the JSON null, true, and false literals, which always must be
written in lowercase:

mysql> SELECT JSON_VALID('null'), JSON_VALID('Null'), JSON_VALID('NULL');
+--------------------+--------------------+--------------------+
| JSON_VALID('null') | JSON_VALID('Null') | JSON_VALID('NULL') |
+--------------------+--------------------+--------------------+
|                  1 |                  0 |                  0 |
+--------------------+--------------------+--------------------+

mysql> SELECT CAST('null' AS JSON);
+----------------------+
| CAST('null' AS JSON) |
+----------------------+
| null                 |
+----------------------+
1 row in set (0.00 sec)

mysql> SELECT CAST('NULL' AS JSON);
ERROR 3141 (22032): Invalid JSON text in argument 1 to function cast_as_json:
"Invalid value." at position 0 in 'NULL'.

Case sensitivity of the JSON literals differs from that of the SQL NULL, TRUE, and FALSE literals, which
can be written in any lettercase:

mysql> SELECT ISNULL(null), ISNULL(Null), ISNULL(NULL);
+--------------+--------------+--------------+
| ISNULL(null) | ISNULL(Null) | ISNULL(NULL) |
+--------------+--------------+--------------+
|            1 |            1 |            1 |
+--------------+--------------+--------------+

Sometimes it may be necessary or desirable to insert quote characters (" or ') into a JSON document.
Assume for this example that you want to insert some JSON objects containing strings representing
sentences that state some facts about MySQL, each paired with an appropriate keyword, into a table
created using the SQL statement shown here:

mysql> CREATE TABLE facts (sentence JSON);

Among these keyword-sentence pairs is this one:

mascot: The MySQL mascot is a dolphin named "Sakila".

One way to insert this as a JSON object into the facts table is to use the MySQL JSON_OBJECT()
function. In this case, you must escape each quote character using a backslash, as shown here:

2255

Normalization, Merging, and Autowrapping of JSON Values

mysql> INSERT INTO facts VALUES
     >   (JSON_OBJECT("mascot", "Our mascot is a dolphin named \"Sakila\"."));

This does not work in the same way if you insert the value as a JSON object literal, in which case, you
must use the double backslash escape sequence, like this:

mysql> INSERT INTO facts VALUES
     >   ('{"mascot": "Our mascot is a dolphin named \\"Sakila\\"."}');

Using the double backslash keeps MySQL from performing escape sequence processing, and instead
causes it to pass the string literal to the storage engine for processing. After inserting the JSON object
in either of the ways just shown, you can see that the backslashes are present in the JSON column
value by doing a simple SELECT, like this:

mysql> SELECT sentence FROM facts;
+---------------------------------------------------------+
| sentence                                                |
+---------------------------------------------------------+
| {"mascot": "Our mascot is a dolphin named \"Sakila\"."} |
+---------------------------------------------------------+

To look up this particular sentence employing mascot as the key, you can use the column-path
operator ->, as shown here:

mysql> SELECT col->"$.mascot" FROM qtest;
+---------------------------------------------+
| col->"$.mascot"                             |
+---------------------------------------------+
| "Our mascot is a dolphin named \"Sakila\"." |
+---------------------------------------------+
1 row in set (0.00 sec)

This leaves the backslashes intact, along with the surrounding quote marks. To display the desired
value using mascot as the key, but without including the surrounding quote marks or any escapes, use
the inline path operator ->>, like this:

mysql> SELECT sentence->>"$.mascot" FROM facts;
+-----------------------------------------+
| sentence->>"$.mascot"                   |
+-----------------------------------------+
| Our mascot is a dolphin named "Sakila". |
+-----------------------------------------+

Note

The previous example does not work as shown if the
NO_BACKSLASH_ESCAPES server SQL mode is enabled. If this mode is
set, a single backslash instead of double backslashes can be used to insert
the JSON object literal, and the backslashes are preserved. If you use the
JSON_OBJECT() function when performing the insert and this mode is set, you
must alternate single and double quotes, like this:

mysql> INSERT INTO facts VALUES
     > (JSON_OBJECT('mascot', 'Our mascot is a dolphin named "Sakila".'));

See the description of the JSON_UNQUOTE() function for more information
about the effects of this mode on escaped characters in JSON values.

Normalization, Merging, and Autowrapping of JSON Values

When a string is parsed and found to be a valid JSON document, it is also normalized. This means
that members with keys that duplicate a key found later in the document, reading from left to right, are
discarded. The object value produced by the following JSON_OBJECT() call includes only the second
key1 element because that key name occurs earlier in the value, as shown here:

mysql> SELECT JSON_OBJECT('key1', 1, 'key2', 'abc', 'key1', 'def');

2256

Normalization, Merging, and Autowrapping of JSON Values

+------------------------------------------------------+
| JSON_OBJECT('key1', 1, 'key2', 'abc', 'key1', 'def') |
+------------------------------------------------------+
| {"key1": "def", "key2": "abc"}                       |
+------------------------------------------------------+

Normalization is also performed when values are inserted into JSON columns, as shown here:

mysql> CREATE TABLE t1 (c1 JSON);

mysql> INSERT INTO t1 VALUES
     >     ('{"x": 17, "x": "red"}'),
     >     ('{"x": 17, "x": "red", "x": [3, 5, 7]}');

mysql> SELECT c1 FROM t1;
+------------------+
| c1               |
+------------------+
| {"x": "red"}     |
| {"x": [3, 5, 7]} |
+------------------+

This “last duplicate key wins” behavior is suggested by RFC 7159 and is implemented by most
JavaScript parsers. (Bug #86866, Bug #26369555)

In versions of MySQL prior to 8.0.3, members with keys that duplicated a key found earlier in the
document were discarded. The object value produced by the following JSON_OBJECT() call does not
include the second key1 element because that key name occurs earlier in the value:

mysql> SELECT JSON_OBJECT('key1', 1, 'key2', 'abc', 'key1', 'def');
+------------------------------------------------------+
| JSON_OBJECT('key1', 1, 'key2', 'abc', 'key1', 'def') |
+------------------------------------------------------+
| {"key1": 1, "key2": "abc"}                           |
+------------------------------------------------------+

Prior to MySQL 8.0.3, this “first duplicate key wins” normalization was also performed when inserting
values into JSON columns.

mysql> CREATE TABLE t1 (c1 JSON);

mysql> INSERT INTO t1 VALUES
     >     ('{"x": 17, "x": "red"}'),
     >     ('{"x": 17, "x": "red", "x": [3, 5, 7]}');

mysql> SELECT c1 FROM t1;
+-----------+
| c1        |
+-----------+
| {"x": 17} |
| {"x": 17} |
+-----------+

MySQL also discards extra whitespace between keys, values, or elements in the original JSON
document, and leaves (or inserts, when necessary) a single space following each comma (,) or colon
(:) when displaying it. This is done to enhance readability.

MySQL functions that produce JSON values (see Section 14.17.2, “Functions That Create JSON
Values”) always return normalized values.

To make lookups more efficient, MySQL also sorts the keys of a JSON object. You should be aware
that the result of this ordering is subject to change and not guaranteed to be consistent across
releases.

Merging JSON Values

Two merging algorithms are supported in MySQL 8.0.3 (and later), implemented by the functions
JSON_MERGE_PRESERVE() and JSON_MERGE_PATCH(). These differ in how they handle duplicate

2257

Searching and Modifying JSON Values

keys: JSON_MERGE_PRESERVE() retains values for duplicate keys, while JSON_MERGE_PATCH()
discards all but the last value. The next few paragraphs explain how each of these two functions
handles the merging of different combinations of JSON documents (that is, of objects and arrays).

Note

JSON_MERGE_PRESERVE() is the same as the JSON_MERGE() function found
in previous versions of MySQL (renamed in MySQL 8.0.3). JSON_MERGE() is
still supported as an alias for JSON_MERGE_PRESERVE() in MySQL 8.0, but is
deprecated and subject to removal in a future release.

Merging arrays.
 In contexts that combine multiple arrays, the arrays are merged into a single array.
JSON_MERGE_PRESERVE() does this by concatenating arrays named later to the end of the first array.
JSON_MERGE_PATCH() considers each argument as an array consisting of a single element (thus
having 0 as its index) and then applies “last duplicate key wins” logic to select only the last argument.
You can compare the results shown by this query:

mysql> SELECT
    ->   JSON_MERGE_PRESERVE('[1, 2]', '["a", "b", "c"]', '[true, false]') AS Preserve,
    ->   JSON_MERGE_PATCH('[1, 2]', '["a", "b", "c"]', '[true, false]') AS Patch\G
*************************** 1. row ***************************
Preserve: [1, 2, "a", "b", "c", true, false]
   Patch: [true, false]

Multiple objects when merged produce a single object. JSON_MERGE_PRESERVE() handles multiple
objects having the same key by combining all unique values for that key in an array; this array is then
used as the value for that key in the result. JSON_MERGE_PATCH() discards values for which duplicate
keys are found, working from left to right, so that the result contains only the last value for that key. The
following query illustrates the difference in the results for the duplicate key a:

mysql> SELECT
    ->   JSON_MERGE_PRESERVE('{"a": 1, "b": 2}', '{"c": 3, "a": 4}', '{"c": 5, "d": 3}') AS Preserve,
    ->   JSON_MERGE_PATCH('{"a": 3, "b": 2}', '{"c": 3, "a": 4}', '{"c": 5, "d": 3}') AS Patch\G
*************************** 1. row ***************************
Preserve: {"a": [1, 4], "b": 2, "c": [3, 5], "d": 3}
   Patch: {"a": 4, "b": 2, "c": 5, "d": 3}

Nonarray values used in a context that requires an array value are autowrapped: The value is
surrounded by [ and ] characters to convert it to an array. In the following statement, each argument
is autowrapped as an array ([1], [2]). These are then merged to produce a single result array; as
in the previous two cases, JSON_MERGE_PRESERVE() combines values having the same key while
JSON_MERGE_PATCH() discards values for all duplicate keys except the last, as shown here:

mysql> SELECT
   ->   JSON_MERGE_PRESERVE('1', '2') AS Preserve,
   ->   JSON_MERGE_PATCH('1', '2') AS Patch\G
*************************** 1. row ***************************
Preserve: [1, 2]
   Patch: 2

Array and object values are merged by autowrapping the object as an array and merging the arrays
by combining values or by “last duplicate key wins” according to the choice of merging function
(JSON_MERGE_PRESERVE() or JSON_MERGE_PATCH(), respectively), as can be seen in this
example:

mysql> SELECT
   ->   JSON_MERGE_PRESERVE('[10, 20]', '{"a": "x", "b": "y"}') AS Preserve,
   ->   JSON_MERGE_PATCH('[10, 20]', '{"a": "x", "b": "y"}') AS Patch\G
*************************** 1. row ***************************
Preserve: [10, 20, {"a": "x", "b": "y"}]
   Patch: {"a": "x", "b": "y"}

Searching and Modifying JSON Values

A JSON path expression selects a value within a JSON document.

2258

Searching and Modifying JSON Values

Path expressions are useful with functions that extract parts of or modify a JSON document, to specify
where within that document to operate. For example, the following query extracts from a JSON
document the value of the member with the name key:

mysql> SELECT JSON_EXTRACT('{"id": 14, "name": "Aztalan"}', '$.name');
+---------------------------------------------------------+
| JSON_EXTRACT('{"id": 14, "name": "Aztalan"}', '$.name') |
+---------------------------------------------------------+
| "Aztalan"                                               |
+---------------------------------------------------------+

Path syntax uses a leading $ character to represent the JSON document under consideration,
optionally followed by selectors that indicate successively more specific parts of the document:

• A period followed by a key name names the member in an object with the given key. The key name
must be specified within double quotation marks if the name without quotes is not legal within path
expressions (for example, if it contains a space).

• [N] appended to a path that selects an array names the value at position N within the array. Array

positions are integers beginning with zero. If path does not select an array value, path[0] evaluates
to the same value as path:

mysql> SELECT JSON_SET('"x"', '$[0]', 'a');
+------------------------------+
| JSON_SET('"x"', '$[0]', 'a') |
+------------------------------+
| "a"                          |
+------------------------------+
1 row in set (0.00 sec)

• [M to N] specifies a subset or range of array values starting with the value at position M, and

ending with the value at position N.

last is supported as a synonym for the index of the rightmost array element. Relative addressing of
array elements is also supported. If path does not select an array value, path[last] evaluates to the
same value as path, as shown later in this section (see Rightmost array element).

• Paths can contain * or ** wildcards:

• .[*] evaluates to the values of all members in a JSON object.

• [*] evaluates to the values of all elements in a JSON array.

• prefix**suffix evaluates to all paths that begin with the named prefix and end with the named

suffix.

• A path that does not exist in the document (evaluates to nonexistent data) evaluates to NULL.

Let $ refer to this JSON array with three elements:

[3, {"a": [5, 6], "b": 10}, [99, 100]]

Then:

• $[0] evaluates to 3.

• $[1] evaluates to {"a": [5, 6], "b": 10}.

• $[2] evaluates to [99, 100].

• $[3] evaluates to NULL (it refers to the fourth array element, which does not exist).

Because $[1] and $[2] evaluate to nonscalar values, they can be used as the basis for more-specific
path expressions that select nested values. Examples:

• $[1].a evaluates to [5, 6].

2259

Searching and Modifying JSON Values

• $[1].a[1] evaluates to 6.

• $[1].b evaluates to 10.

• $[2][0] evaluates to 99.

As mentioned previously, path components that name keys must be quoted if the unquoted key name
is not legal in path expressions. Let $ refer to this value:

{"a fish": "shark", "a bird": "sparrow"}

The keys both contain a space and must be quoted:

• $."a fish" evaluates to shark.

• $."a bird" evaluates to sparrow.

Paths that use wildcards evaluate to an array that can contain multiple values:

mysql> SELECT JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.*');
+---------------------------------------------------------+
| JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.*') |
+---------------------------------------------------------+
| [1, 2, [3, 4, 5]]                                       |
+---------------------------------------------------------+
mysql> SELECT JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.c[*]');
+------------------------------------------------------------+
| JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.c[*]') |
+------------------------------------------------------------+
| [3, 4, 5]                                                  |
+------------------------------------------------------------+

In the following example, the path $**.b evaluates to multiple paths ($.a.b and $.c.b) and
produces an array of the matching path values:

mysql> SELECT JSON_EXTRACT('{"a": {"b": 1}, "c": {"b": 2}}', '$**.b');
+---------------------------------------------------------+
| JSON_EXTRACT('{"a": {"b": 1}, "c": {"b": 2}}', '$**.b') |
+---------------------------------------------------------+
| [1, 2]                                                  |
+---------------------------------------------------------+

Ranges from JSON arrays.
arrays. For example, $[1 to 3] includes the second, third, and fourth elements of an array, as shown
here:

 You can use ranges with the to keyword to specify subsets of JSON

mysql> SELECT JSON_EXTRACT('[1, 2, 3, 4, 5]', '$[1 to 3]');
+----------------------------------------------+
| JSON_EXTRACT('[1, 2, 3, 4, 5]', '$[1 to 3]') |
+----------------------------------------------+
| [2, 3, 4]                                    |
+----------------------------------------------+
1 row in set (0.00 sec)

The syntax is M to N, where M and N are, respectively, the first and last indexes of a range of
elements from a JSON array. N must be greater than M; M must be greater than or equal to 0. Array
elements are indexed beginning with 0.

You can use ranges in contexts where wildcards are supported.

Rightmost array element.
element in an array. Expressions of the form last - N can be used for relative addressing, and within
range definitions, like this:

 The last keyword is supported as a synonym for the index of the last

mysql> SELECT JSON_EXTRACT('[1, 2, 3, 4, 5]', '$[last-3 to last-1]');
+--------------------------------------------------------+
| JSON_EXTRACT('[1, 2, 3, 4, 5]', '$[last-3 to last-1]') |
+--------------------------------------------------------+

2260

Searching and Modifying JSON Values

| [2, 3, 4]                                              |
+--------------------------------------------------------+
1 row in set (0.01 sec)

If the path is evaluated against a value that is not an array, the result of the evaluation is the same as if
the value had been wrapped in a single-element array:

mysql> SELECT JSON_REPLACE('"Sakila"', '$[last]', 10);
+-----------------------------------------+
| JSON_REPLACE('"Sakila"', '$[last]', 10) |
+-----------------------------------------+
| 10                                      |
+-----------------------------------------+
1 row in set (0.00 sec)

You can use column->path with a JSON column identifier and JSON path expression as a synonym
for JSON_EXTRACT(column, path). See Section 14.17.3, “Functions That Search JSON Values”,
for more information. See also Indexing a Generated Column to Provide a JSON Column Index.

Some functions take an existing JSON document, modify it in some way, and return the resulting
modified document. Path expressions indicate where in the document to make changes. For example,
the JSON_SET(), JSON_INSERT(), and JSON_REPLACE() functions each take a JSON document,
plus one or more path-value pairs that describe where to modify the document and the values to use.
The functions differ in how they handle existing and nonexisting values within the document.

Consider this document:

mysql> SET @j = '["a", {"b": [true, false]}, [10, 20]]';

JSON_SET() replaces values for paths that exist and adds values for paths that do not exist:.

mysql> SELECT JSON_SET(@j, '$[1].b[0]', 1, '$[2][2]', 2);
+--------------------------------------------+
| JSON_SET(@j, '$[1].b[0]', 1, '$[2][2]', 2) |
+--------------------------------------------+
| ["a", {"b": [1, false]}, [10, 20, 2]]      |
+--------------------------------------------+

In this case, the path $[1].b[0] selects an existing value (true), which is replaced with the value
following the path argument (1). The path $[2][2] does not exist, so the corresponding value (2) is
added to the value selected by $[2].

JSON_INSERT() adds new values but does not replace existing values:

mysql> SELECT JSON_INSERT(@j, '$[1].b[0]', 1, '$[2][2]', 2);
+-----------------------------------------------+
| JSON_INSERT(@j, '$[1].b[0]', 1, '$[2][2]', 2) |
+-----------------------------------------------+
| ["a", {"b": [true, false]}, [10, 20, 2]]      |
+-----------------------------------------------+

JSON_REPLACE() replaces existing values and ignores new values:

mysql> SELECT JSON_REPLACE(@j, '$[1].b[0]', 1, '$[2][2]', 2);
+------------------------------------------------+
| JSON_REPLACE(@j, '$[1].b[0]', 1, '$[2][2]', 2) |
+------------------------------------------------+
| ["a", {"b": [1, false]}, [10, 20]]             |
+------------------------------------------------+

The path-value pairs are evaluated left to right. The document produced by evaluating one pair
becomes the new value against which the next pair is evaluated.

JSON_REMOVE() takes a JSON document and one or more paths that specify values to be removed
from the document. The return value is the original document minus the values selected by paths that
exist within the document:

mysql> SELECT JSON_REMOVE(@j, '$[2]', '$[1].b[1]', '$[1].b[1]');

2261

JSON Path Syntax

+---------------------------------------------------+
| JSON_REMOVE(@j, '$[2]', '$[1].b[1]', '$[1].b[1]') |
+---------------------------------------------------+
| ["a", {"b": [true]}]                              |
+---------------------------------------------------+

The paths have these effects:

• $[2] matches [10, 20] and removes it.

• The first instance of $[1].b[1] matches false in the b element and removes it.

• The second instance of $[1].b[1] matches nothing: That element has already been removed, the

path no longer exists, and has no effect.

JSON Path Syntax

Many of the JSON functions supported by MySQL and described elsewhere in this Manual (see
Section 14.17, “JSON Functions”) require a path expression in order to identify a specific element in
a JSON document. A path consists of the path's scope followed by one or more path legs. For paths
used in MySQL JSON functions, the scope is always the document being searched or otherwise
operated on, represented by a leading $ character. Path legs are separated by period characters
(.). Cells in arrays are represented by [N], where N is a non-negative integer. Names of keys must
be double-quoted strings or valid ECMAScript identifiers (see Identifier Names and Identifiers, in the
ECMAScript Language Specification). Path expressions, like JSON text, should be encoded using
the ascii, utf8mb3, or utf8mb4 character set. Other character encodings are implicitly coerced to
utf8mb4. The complete syntax is shown here:

pathExpression:
    scope[(pathLeg)*]

pathLeg:
    member | arrayLocation | doubleAsterisk

member:
    period ( keyName | asterisk )

arrayLocation:
    leftBracket ( nonNegativeInteger | asterisk ) rightBracket

keyName:
    ESIdentifier | doubleQuotedString

doubleAsterisk:
    '**'

period:
    '.'

asterisk:
    '*'

leftBracket:
    '['

rightBracket:
    ']'

As noted previously, in MySQL, the scope of the path is always the document being operated on,
represented as $. You can use '$' as a synonym for the document in JSON path expressions.

Note

Some implementations support column references for scopes of JSON paths;
MySQL 8.0 does not support these.

The wildcard * and ** tokens are used as follows:

2262

Comparison and Ordering of JSON Values

• .* represents the values of all members in the object.

• [*] represents the values of all cells in the array.

• [prefix]**suffix represents all paths beginning with prefix and ending with suffix. prefix

is optional, while suffix is required; in other words, a path may not end in **.

In addition, a path may not contain the sequence ***.

For path syntax examples, see the descriptions of the various JSON functions that take paths as
arguments, such as JSON_CONTAINS_PATH(), JSON_SET(), and JSON_REPLACE(). For examples
which include the use of the * and ** wildcards, see the description of the JSON_SEARCH() function.

MySQL 8.0 also supports range notation for subsets of JSON arrays using the to keyword (such as
$[2 to 10]), as well as the last keyword as a synonym for the rightmost element of an array. See
Searching and Modifying JSON Values, for more information and examples.

Comparison and Ordering of JSON Values

JSON values can be compared using the =, <, <=, >, >=, <>, !=, and <=> operators.

The following comparison operators and functions are not yet supported with JSON values:

• BETWEEN

• IN()

• GREATEST()

• LEAST()

A workaround for the comparison operators and functions just listed is to cast JSON values to a native
MySQL numeric or string data type so they have a consistent non-JSON scalar type.

Comparison of JSON values takes place at two levels. The first level of comparison is based on the
JSON types of the compared values. If the types differ, the comparison result is determined solely
by which type has higher precedence. If the two values have the same JSON type, a second level of
comparison occurs using type-specific rules.

The following list shows the precedences of JSON types, from highest precedence to the lowest. (The
type names are those returned by the JSON_TYPE() function.) Types shown together on a line have
the same precedence. Any value having a JSON type listed earlier in the list compares greater than
any value having a JSON type listed later in the list.

BLOB
BIT
OPAQUE
DATETIME
TIME
DATE
BOOLEAN
ARRAY
OBJECT
STRING
INTEGER, DOUBLE
NULL

For JSON values of the same precedence, the comparison rules are type specific:

• BLOB

The first N bytes of the two values are compared, where N is the number of bytes in the shorter value.
If the first N bytes of the two values are identical, the shorter value is ordered before the longer value.

• BIT

2263

Comparison and Ordering of JSON Values

Same rules as for BLOB.

• OPAQUE

Same rules as for BLOB. OPAQUE values are values that are not classified as one of the other types.

• DATETIME

A value that represents an earlier point in time is ordered before a value that represents a later
point in time. If two values originally come from the MySQL DATETIME and TIMESTAMP types,
respectively, they are equal if they represent the same point in time.

• TIME

The smaller of two time values is ordered before the larger one.

• DATE

The earlier date is ordered before the more recent date.

• ARRAY

Two JSON arrays are equal if they have the same length and values in corresponding positions in
the arrays are equal.

If the arrays are not equal, their order is determined by the elements in the first position where there
is a difference. The array with the smaller value in that position is ordered first. If all values of the
shorter array are equal to the corresponding values in the longer array, the shorter array is ordered
first.

Example:

[] < ["a"] < ["ab"] < ["ab", "cd", "ef"] < ["ab", "ef"]

• BOOLEAN

The JSON false literal is less than the JSON true literal.

• OBJECT

Two JSON objects are equal if they have the same set of keys, and each key has the same value in
both objects.

Example:

{"a": 1, "b": 2} = {"b": 2, "a": 1}

The order of two objects that are not equal is unspecified but deterministic.

• STRING

Strings are ordered lexically on the first N bytes of the utf8mb4 representation of the two strings
being compared, where N is the length of the shorter string. If the first N bytes of the two strings are
identical, the shorter string is considered smaller than the longer string.

Example:

"a" < "ab" < "b" < "bc"

This ordering is equivalent to the ordering of SQL strings with collation utf8mb4_bin. Because
utf8mb4_bin is a binary collation, comparison of JSON values is case-sensitive:

"A" < "a"

2264

Converting between JSON and non-JSON values

• INTEGER, DOUBLE

JSON values can contain exact-value numbers and approximate-value numbers. For a general
discussion of these types of numbers, see Section 11.1.2, “Numeric Literals”.

The rules for comparing native MySQL numeric types are discussed in Section 14.3, “Type
Conversion in Expression Evaluation”, but the rules for comparing numbers within JSON values differ
somewhat:

• In a comparison between two columns that use the native MySQL INT and DOUBLE numeric

types, respectively, it is known that all comparisons involve an integer and a double, so the integer
is converted to double for all rows. That is, exact-value numbers are converted to approximate-
value numbers.

• On the other hand, if the query compares two JSON columns containing numbers, it cannot

be known in advance whether numbers are integer or double. To provide the most consistent
behavior across all rows, MySQL converts approximate-value numbers to exact-value
numbers. The resulting ordering is consistent and does not lose precision for the exact-value
numbers. For example, given the scalars 9223372036854775805, 9223372036854775806,
9223372036854775807 and 9.223372036854776e18, the order is such as this:

9223372036854775805 < 9223372036854775806 < 9223372036854775807
< 9.223372036854776e18 = 9223372036854776000 < 9223372036854776001

Were JSON comparisons to use the non-JSON numeric comparison rules, inconsistent ordering
could occur. The usual MySQL comparison rules for numbers yield these orderings:

• Integer comparison:

9223372036854775805 < 9223372036854775806 < 9223372036854775807

(not defined for 9.223372036854776e18)

• Double comparison:

9223372036854775805 = 9223372036854775806 = 9223372036854775807 = 9.223372036854776e18

For comparison of any JSON value to SQL NULL, the result is UNKNOWN.

For comparison of JSON and non-JSON values, the non-JSON value is converted to JSON according
to the rules in the following table, then the values compared as described previously.

Converting between JSON and non-JSON values

The following table provides a summary of the rules that MySQL follows when casting between JSON
values and values of other types:

Table 13.3 JSON Conversion Rules

other type

JSON

CAST(other type AS JSON)

CAST(JSON AS other type)

No change

No change

utf8 character type (utf8mb4,
utf8mb3, ascii)

The string is parsed into a JSON
value.

The JSON value is serialized into
a utf8mb4 string.

Other character types

Other character encodings are
implicitly converted to utf8mb4
and treated as described for this
character type.

The JSON value is serialized
into a utf8mb4 string, then
cast to the other character
encoding. The result may not be
meaningful.

NULL

Results in a NULL value of type
JSON.

Not applicable.

2265

Explicit Default Handling as of MySQL 8.0.13

• Explicit Default Handling as of MySQL 8.0.13

• Explicit Default Handling Prior to MySQL 8.0.13

• Implicit Default Handling

Explicit Default Handling as of MySQL 8.0.13

The default value specified in a DEFAULT clause can be a literal constant or an expression. With
one exception, enclose expression default values within parentheses to distinguish them from literal
constant default values. Examples:

CREATE TABLE t1 (
  -- literal defaults
  i INT         DEFAULT 0,
  c VARCHAR(10) DEFAULT '',
  -- expression defaults
  f FLOAT       DEFAULT (RAND() * RAND()),
  b BINARY(16)  DEFAULT (UUID_TO_BIN(UUID())),
  d DATE        DEFAULT (CURRENT_DATE + INTERVAL 1 YEAR),
  p POINT       DEFAULT (Point(0,0)),
  j JSON        DEFAULT (JSON_ARRAY())
);

The exception is that, for TIMESTAMP and DATETIME columns, you can specify the
CURRENT_TIMESTAMP function as the default, without enclosing parentheses. See Section 13.2.5,
“Automatic Initialization and Updating for TIMESTAMP and DATETIME”.

The BLOB, TEXT, GEOMETRY, and JSON data types can be assigned a default value only if the value is
written as an expression, even if the expression value is a literal:

• This is permitted (literal default specified as expression):

CREATE TABLE t2 (b BLOB DEFAULT ('abc'));

• This produces an error (literal default not specified as expression):

CREATE TABLE t2 (b BLOB DEFAULT 'abc');

Expression default values must adhere to the following rules. An error occurs if an expression contains
disallowed constructs.

• Literals, built-in functions (both deterministic and nondeterministic), and operators are permitted.

• Subqueries, parameters, variables, stored functions, and loadable functions are not permitted.

• An expression default value cannot depend on a column that has the AUTO_INCREMENT attribute.

• An expression default value for one column can refer to other table columns, with the exception that
references to generated columns or columns with expression default values must be to columns
that occur earlier in the table definition. That is, expression default values cannot contain forward
references to generated columns or columns with expression default values.

The ordering constraint also applies to the use of ALTER TABLE to reorder table columns. If the
resulting table would have an expression default value that contains a forward reference to a
generated column or column with an expression default value, the statement fails.

Note

If any component of an expression default value depends on the SQL mode,
different results may occur for different uses of the table unless the SQL mode
is the same during all uses.

For CREATE TABLE ... LIKE and CREATE TABLE ... SELECT, the destination table preserves
expression default values from the original table.

2267

Explicit Default Handling Prior to MySQL 8.0.13

If an expression default value refers to a nondeterministic function, any statement that causes the
expression to be evaluated is unsafe for statement-based replication. This includes statements such
as INSERT and UPDATE. In this situation, if binary logging is disabled, the statement is executed as
normal. If binary logging is enabled and binlog_format is set to STATEMENT, the statement is
logged and executed but a warning message is written to the error log, because replication slaves
might diverge. When binlog_format is set to MIXED or ROW, the statement is executed as normal.

When inserting a new row, the default value for a column with an expression default can be inserted
either by omitting the column name or by specifying the column as DEFAULT (just as for columns with
literal defaults):

mysql> CREATE TABLE t4 (uid BINARY(16) DEFAULT (UUID_TO_BIN(UUID())));
mysql> INSERT INTO t4 () VALUES();
mysql> INSERT INTO t4 () VALUES(DEFAULT);
mysql> SELECT BIN_TO_UUID(uid) AS uid FROM t4;
+--------------------------------------+
| uid                                  |
+--------------------------------------+
| f1109174-94c9-11e8-971d-3bf1095aa633 |
| f110cf9a-94c9-11e8-971d-3bf1095aa633 |
+--------------------------------------+

However, the use of DEFAULT(col_name) to specify the default value for a named column is
permitted only for columns that have a literal default value, not for columns that have an expression
default value.

Not all storage engines permit expression default values. For those that do not, an
ER_UNSUPPORTED_ACTION_ON_DEFAULT_VAL_GENERATED error occurs.

If a default value evaluates to a data type that differs from the declared column type, implicit coercion to
the declared type occurs according to the usual MySQL type-conversion rules. See Section 14.3, “Type
Conversion in Expression Evaluation”.

Explicit Default Handling Prior to MySQL 8.0.13

With one exception, the default value specified in a DEFAULT clause must be a literal constant; it
cannot be a function or an expression. This means, for example, that you cannot set the default for a
date column to be the value of a function such as NOW() or CURRENT_DATE. The exception is that,
for TIMESTAMP and DATETIME columns, you can specify CURRENT_TIMESTAMP as the default. See
Section 13.2.5, “Automatic Initialization and Updating for TIMESTAMP and DATETIME”.

The BLOB, TEXT, GEOMETRY, and JSON data types cannot be assigned a default value.

If a default value evaluates to a data type that differs from the declared column type, implicit coercion to
the declared type occurs according to the usual MySQL type-conversion rules. See Section 14.3, “Type
Conversion in Expression Evaluation”.

Implicit Default Handling

If a data type specification includes no explicit DEFAULT value, MySQL determines the default value as
follows:

If the column can take NULL as a value, the column is defined with an explicit DEFAULT NULL clause.

If the column cannot take NULL as a value, MySQL defines the column with no explicit DEFAULT
clause.

For data entry into a NOT NULL column that has no explicit DEFAULT clause, if an INSERT or REPLACE
statement includes no value for the column, or an UPDATE statement sets the column to NULL, MySQL
handles the column according to the SQL mode in effect at the time:

2268

Data Type Storage Requirements

• If strict SQL mode is enabled, an error occurs for transactional tables and the statement is rolled

back. For nontransactional tables, an error occurs, but if this happens for the second or subsequent
row of a multiple-row statement, the preceding rows are inserted.

• If strict mode is not enabled, MySQL sets the column to the implicit default value for the column data

type.

Suppose that a table t is defined as follows:

CREATE TABLE t (i INT NOT NULL);

In this case, i has no explicit default, so in strict mode each of the following statements produce an
error and no row is inserted. When not using strict mode, only the third statement produces an error;
the implicit default is inserted for the first two statements, but the third fails because DEFAULT(i)
cannot produce a value:

INSERT INTO t VALUES();
INSERT INTO t VALUES(DEFAULT);
INSERT INTO t VALUES(DEFAULT(i));

See Section 7.1.11, “Server SQL Modes”.

For a given table, the SHOW CREATE TABLE statement displays which columns have an explicit
DEFAULT clause.

Implicit defaults are defined as follows:

• For numeric types, the default is 0, with the exception that for integer or floating-point types declared

with the AUTO_INCREMENT attribute, the default is the next value in the sequence.

• For date and time types other than TIMESTAMP, the default is the appropriate “zero” value

for the type. This is also true for TIMESTAMP if the explicit_defaults_for_timestamp
system variable is enabled (see Section 7.1.8, “Server System Variables”). Otherwise, for the first
TIMESTAMP column in a table, the default value is the current date and time. See Section 13.2, “Date
and Time Data Types”.

• For string types other than ENUM, the default value is the empty string. For ENUM, the default is the

first enumeration value.

13.7 Data Type Storage Requirements

• InnoDB Table Storage Requirements

• NDB Table Storage Requirements

• Numeric Type Storage Requirements

• Date and Time Type Storage Requirements

• String Type Storage Requirements

• Spatial Type Storage Requirements

• JSON Storage Requirements

The storage requirements for table data on disk depend on several factors. Different storage engines
represent data types and store raw data differently. Table data might be compressed, either for a
column or an entire row, complicating the calculation of storage requirements for a table or column.

Despite differences in storage layout on disk, the internal MySQL APIs that communicate and
exchange information about table rows use a consistent data structure that applies across all storage
engines.

2269

Date and Time Type Storage Requirements

Data Type

Storage Required

DOUBLE [PRECISION], REAL

8 bytes

DECIMAL(M,D), NUMERIC(M,D)

Varies; see following discussion

BIT(M)

approximately (M+7)/8 bytes

Values for DECIMAL (and NUMERIC) columns are represented using a binary format that packs nine
decimal (base 10) digits into four bytes. Storage for the integer and fractional parts of each value are
determined separately. Each multiple of nine digits requires four bytes, and the “leftover” digits require
some fraction of four bytes. The storage required for excess digits is given by the following table.

Leftover Digits

Number of Bytes

0

1

2

3

4

5

6

7

8

0

1

1

2

2

3

3

4

4

Date and Time Type Storage Requirements

For TIME, DATETIME, and TIMESTAMP columns, the storage required for tables created before MySQL
5.6.4 differs from tables created from 5.6.4 on. This is due to a change in 5.6.4 that permits these types
to have a fractional part, which requires from 0 to 3 bytes.

Data Type

YEAR

DATE

TIME

DATETIME

TIMESTAMP

Storage Required Before
MySQL 5.6.4

Storage Required as of MySQL
5.6.4

1 byte

3 bytes

3 bytes

8 bytes

4 bytes

1 byte

3 bytes

3 bytes + fractional seconds
storage

5 bytes + fractional seconds
storage

4 bytes + fractional seconds
storage

As of MySQL 5.6.4, storage for YEAR and DATE remains unchanged. However, TIME, DATETIME, and
TIMESTAMP are represented differently. DATETIME is packed more efficiently, requiring 5 rather than 8
bytes for the nonfractional part, and all three parts have a fractional part that requires from 0 to 3 bytes,
depending on the fractional seconds precision of stored values.

Fractional Seconds Precision

Storage Required

0

1, 2

3, 4

5, 6

0 bytes

1 byte

2 bytes

3 bytes

2271

String Type Storage Requirements

For example, TIME(0), TIME(2), TIME(4), and TIME(6) use 3, 4, 5, and 6 bytes, respectively.
TIME and TIME(0) are equivalent and require the same storage.

For details about internal representation of temporal values, see MySQL Internals: Important
Algorithms and Structures.

String Type Storage Requirements

In the following table, M represents the declared column length in characters for nonbinary string types
and bytes for binary string types. L represents the actual length in bytes of a given string value.

Data Type

CHAR(M)

BINARY(M)

VARCHAR(M), VARBINARY(M)

TINYBLOB, TINYTEXT

BLOB, TEXT

MEDIUMBLOB, MEDIUMTEXT

LONGBLOB, LONGTEXT

ENUM('value1','value2',...)

SET('value1','value2',...)

Storage Required

The compact family of InnoDB row formats
optimize storage for variable-length character
sets. See COMPACT Row Format Storage
Characteristics. Otherwise, M × w bytes, <= M <=
255, where w is the number of bytes required for
the maximum-length character in the character
set.

M bytes, 0 <= M <= 255

L + 1 bytes if column values require 0 − 255 bytes,
L + 2 bytes if values may require more than 255
bytes
L + 1 bytes, where L < 28
L + 2 bytes, where L < 216
L + 3 bytes, where L < 224
L + 4 bytes, where L < 232
1 or 2 bytes, depending on the number of
enumeration values (65,535 values maximum)

1, 2, 3, 4, or 8 bytes, depending on the number of
set members (64 members maximum)

Variable-length string types are stored using a length prefix plus data. The length prefix requires from
one to four bytes depending on the data type, and the value of the prefix is L (the byte length of the
string). For example, storage for a MEDIUMTEXT value requires L bytes to store the value plus three
bytes to store the length of the value.

To calculate the number of bytes used to store a particular CHAR, VARCHAR, or TEXT column value, you
must take into account the character set used for that column and whether the value contains multibyte
characters. In particular, when using a UTF-8 Unicode character set, you must keep in mind that not
all characters use the same number of bytes. utf8mb3 and utf8mb4 character sets can require up
to three and four bytes per character, respectively. For a breakdown of the storage used for different
categories of utf8mb3 or utf8mb4 characters, see Section 12.9, “Unicode Support”.

VARCHAR, VARBINARY, and the BLOB and TEXT types are variable-length types. For each, the storage
requirements depend on these factors:

• The actual length of the column value

• The column's maximum possible length

• The character set used for the column, because some character sets contain multibyte characters

For example, a VARCHAR(255) column can hold a string with a maximum length of 255 characters.
Assuming that the column uses the latin1 character set (one byte per character), the actual storage

2272

Spatial Type Storage Requirements

required is the length of the string (L), plus one byte to record the length of the string. For the string
'abcd', L is 4 and the storage requirement is five bytes. If the same column is instead declared to use
the ucs2 double-byte character set, the storage requirement is 10 bytes: The length of 'abcd' is eight
bytes and the column requires two bytes to store lengths because the maximum length is greater than
255 (up to 510 bytes).

The effective maximum number of bytes that can be stored in a VARCHAR or VARBINARY column is
subject to the maximum row size of 65,535 bytes, which is shared among all columns. For a VARCHAR
column that stores multibyte characters, the effective maximum number of characters is less. For
example, utf8mb4 characters can require up to four bytes per character, so a VARCHAR column
that uses the utf8mb4 character set can be declared to be a maximum of 16,383 characters. See
Section 10.4.7, “Limits on Table Column Count and Row Size”.

InnoDB encodes fixed-length fields greater than or equal to 768 bytes in length as variable-length
fields, which can be stored off-page. For example, a CHAR(255) column can exceed 768 bytes if the
maximum byte length of the character set is greater than 3, as it is with utf8mb4.

The NDB storage engine supports variable-width columns. This means that a VARCHAR column in an
NDB Cluster table requires the same amount of storage as would any other storage engine, with the
exception that such values are 4-byte aligned. Thus, the string 'abcd' stored in a VARCHAR(50)
column using the latin1 character set requires 8 bytes (rather than 5 bytes for the same column
value in a MyISAM table).

TEXT, BLOB, and JSON columns are implemented differently in the NDB storage engine, wherein each
row in the column is made up of two separate parts. One of these is of fixed size (256 bytes for TEXT
and BLOB, 4000 bytes for JSON), and is actually stored in the original table. The other consists of any
data in excess of 256 bytes, which is stored in a hidden blob parts table. The size of the rows in this
second table are determined by the exact type of the column, as shown in the following table:

Type

BLOB, TEXT

MEDIUMBLOB, MEDIUMTEXT

LONGBLOB, LONGTEXT

JSON

Blob Part Size

2000

4000

13948

8100

This means that the size of a TEXT column is 256 if size <= 256 (where size represents the size of
the row); otherwise, the size is 256 + size + (2000 × (size − 256) % 2000).

No blob parts are stored separately by NDB for TINYBLOB or TINYTEXT column values.

You can increase the size of an NDB blob column's blob part to the maximum of 13948 using
NDB_COLUMN in a column comment when creating or altering the parent table. In NDB 8.0.30 and
later, it is also possible to set the inline size for a TEXT, BLOB, or JSON column, using NDB_TABLE in a
column comment. See NDB_COLUMN Options, for more information.

The size of an ENUM object is determined by the number of different enumeration values. One byte is
used for enumerations with up to 255 possible values. Two bytes are used for enumerations having
between 256 and 65,535 possible values. See Section 13.3.5, “The ENUM Type”.

The size of a SET object is determined by the number of different set members. If the set size is N, the
object occupies (N+7)/8 bytes, rounded up to 1, 2, 3, 4, or 8 bytes. A SET can have a maximum of 64
members. See Section 13.3.6, “The SET Type”.

Spatial Type Storage Requirements

MySQL stores geometry values using 4 bytes to indicate the SRID followed by the WKB representation
of the value. The LENGTH() function returns the space in bytes required for value storage.

2273

JSON Storage Requirements

For descriptions of WKB and internal storage formats for spatial values, see Section 13.4.3, “Supported
Spatial Data Formats”.

JSON Storage Requirements

In general, the storage requirement for a JSON column is approximately the same as for a LONGBLOB
or LONGTEXT column; that is, the space consumed by a JSON document is roughly the same as it
would be for the document's string representation stored in a column of one of these types. However,
there is an overhead imposed by the binary encoding, including metadata and dictionaries needed for
lookup, of the individual values stored in the JSON document. For example, a string stored in a JSON
document requires 4 to 10 bytes additional storage, depending on the length of the string and the size
of the object or array in which it is stored.

In addition, MySQL imposes a limit on the size of any JSON document stored in a JSON column such
that it cannot be any larger than the value of max_allowed_packet.

13.8 Choosing the Right Type for a Column

For optimum storage, you should try to use the most precise type in all cases. For example, if an
integer column is used for values in the range from 1 to 99999, MEDIUMINT UNSIGNED is the best
type. Of the types that represent all the required values, this type uses the least amount of storage.

All basic calculations (+, -, *, and /) with DECIMAL columns are done with precision of 65 decimal
(base 10) digits. See Section 13.1.1, “Numeric Data Type Syntax”.

If accuracy is not too important or if speed is the highest priority, the DOUBLE type may be good
enough. For high precision, you can always convert to a fixed-point type stored in a BIGINT. This
enables you to do all calculations with 64-bit integers and then convert results back to floating-point
values as necessary.

13.9 Using Data Types from Other Database Engines

To facilitate the use of code written for SQL implementations from other vendors, MySQL maps data
types as shown in the following table. These mappings make it easier to import table definitions from
other database systems into MySQL.

Other Vendor Type

BOOL

BOOLEAN

CHARACTER VARYING(M)

FIXED

FLOAT4

FLOAT8

INT1

INT2

INT3

INT4

INT8

LONG VARBINARY

LONG VARCHAR

LONG

MIDDLEINT

2274

MySQL Type

TINYINT

TINYINT

VARCHAR(M)

DECIMAL

FLOAT

DOUBLE

TINYINT

SMALLINT

MEDIUMINT

INT

BIGINT

MEDIUMBLOB

MEDIUMTEXT

MEDIUMTEXT

MEDIUMINT

Using Data Types from Other Database Engines

Other Vendor Type

NUMERIC

MySQL Type

DECIMAL

Data type mapping occurs at table creation time, after which the original type specifications are
discarded. If you create a table with types used by other vendors and then issue a DESCRIBE
tbl_name statement, MySQL reports the table structure using the equivalent MySQL types. For
example:

mysql> CREATE TABLE t (a BOOL, b FLOAT8, c LONG VARCHAR, d NUMERIC);
Query OK, 0 rows affected (0.00 sec)

mysql> DESCRIBE t;
+-------+---------------+------+-----+---------+-------+
| Field | Type          | Null | Key | Default | Extra |
+-------+---------------+------+-----+---------+-------+
| a     | tinyint(1)    | YES  |     | NULL    |       |
| b     | double        | YES  |     | NULL    |       |
| c     | mediumtext    | YES  |     | NULL    |       |
| d     | decimal(10,0) | YES  |     | NULL    |       |
+-------+---------------+------+-----+---------+-------+
4 rows in set (0.01 sec)

2275

2276

