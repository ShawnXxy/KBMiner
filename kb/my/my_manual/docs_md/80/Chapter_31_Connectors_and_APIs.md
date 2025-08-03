MySQL Connector/C++

Environment

API

Type

Notes

hsql-mysql

libmysqlclient

Java/JDBC

Connector/J

Native Driver

See MySQL driver for
Haskell.

See MySQL Connector/
J Developer Guide.

Kaya

Lua

MyDB

LuaSQL

libmysqlclient

See MyDB.

libmysqlclient

See LuaSQL.

.NET/Mono

Connector/NET

Native Driver

Objective Caml

Octave

ODBC

Perl

PHP

OBjective Caml MySQL
Bindings

Database bindings for
GNU Octave

libmysqlclient

libmysqlclient

Connector/ODBC

libmysqlclient

DBI/DBD::mysql

libmysqlclient

Net::MySQL

Native Driver

See MySQL Connector/
NET Developer Guide.

See MySQL Bindings for
Objective Caml.

See Database bindings
for GNU Octave.

See MySQL Connector/
ODBC Developer Guide.

See Section 31.9,
“MySQL Perl API”.

See Net::MySQL at
CPAN

mysql, ext/mysql
interface (deprecated)

mysqli, ext/mysqli
interface

PDO_MYSQL

PDO mysqlnd

libmysqlclient

See MySQL and PHP.

libmysqlclient

See MySQL and PHP.

libmysqlclient

See MySQL and PHP.

Native Driver

Python

Connector/Python

Native Driver

Python

Connector/Python C
Extension

libmysqlclient

MySQLdb

libmysqlclient

Ruby

mysql2

libmysqlclient

See MySQL Connector/
Python Developer
Guide.

See MySQL Connector/
Python Developer
Guide.

See Section 31.10,
“MySQL Python API”.

Uses
libmysqlclient. See
Section 31.11, “MySQL
Ruby APIs”.

Scheme

SPL

Tcl

Myscsh

sql_mysql

libmysqlclient

See Myscsh.

libmysqlclient

MySQLtcl

libmysqlclient

See sql_mysql for
SPL.

See Section 31.12,
“MySQL Tcl API”.

31.1 MySQL Connector/C++

The MySQL Connector/C++ manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Main manual: MySQL Connector/C++ 9.3 Developer Guide

5441

MySQL Connector/J

• Release notes: MySQL Connector/C++ Release Notes

31.2 MySQL Connector/J

The MySQL Connector/J manual is published in standalone form, not as part of the MySQL Reference
Manual. For information, see these documents:

• Main manual: MySQL Connector/J Developer Guide

• Release notes: MySQL Connector/J Release Notes

31.3 MySQL Connector/NET

The MySQL Connector/NET manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Main manual: MySQL Connector/NET Developer Guide

• Release notes: MySQL Connector/NET Release Notes

31.4 MySQL Connector/ODBC

The MySQL Connector/ODBC manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Main manual: MySQL Connector/ODBC Developer Guide

• Release notes: MySQL Connector/ODBC Release Notes

31.5 MySQL Connector/Python

The MySQL Connector/Python manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Main manual: MySQL Connector/Python Developer Guide

• Release notes: MySQL Connector/Python Release Notes

31.6 MySQL Connector/Node.js

The MySQL Connector/Node.js manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Release notes: MySQL Connector/Node.js Release Notes

31.7 MySQL C API

The MySQL C API Developer Guide is published in standalone form, not as part of the MySQL
Reference Manual. See MySQL 8.0 C API Developer Guide.

31.8 MySQL PHP API

The MySQL PHP API manual is now published in standalone form, not as part of the MySQL
Reference Manual. See MySQL and PHP.

31.9 MySQL Perl API

5442

MySQL Python API

The Perl DBI module provides a generic interface for database access. You can write a DBI script
that works with many different database engines without change. To use DBI with MySQL, install the
following:

1. The DBI module.

2. The DBD::mysql module. This is the DataBase Driver (DBD) module for Perl.

3. Optionally, the DBD module for any other type of database server you want to access.

Perl DBI is the recommended Perl interface. It replaces an older interface called mysqlperl, which
should be considered obsolete.

These sections contain information about using Perl with MySQL and writing MySQL applications in
Perl:

• For installation instructions for Perl DBI support, see Section 2.10, “Perl Installation Notes”.

• For an example of reading options from option files, see Section 7.8.4, “Using Client Programs in a

Multiple-Server Environment”.

• For secure coding tips, see Section 8.1.1, “Security Guidelines”.

• For debugging tips, see Section 7.9.1.4, “Debugging mysqld under gdb”.

• For some Perl-specific environment variables, see Section 6.9, “Environment Variables”.

• For considerations for running on macOS, see Section 2.4, “Installing MySQL on macOS”.

• For ways to quote string literals, see Section 11.1.1, “String Literals”.

DBI information is available at the command line, online, or in printed form:

• Once you have the DBI and DBD::mysql modules installed, you can get information about them at

the command line with the perldoc command:

$> perldoc DBI
$> perldoc DBI::FAQ
$> perldoc DBD::mysql

You can also use pod2man, pod2html, and so on to translate this information into other formats.

• For online information about Perl DBI, visit the DBI website, http://dbi.perl.org/. That site hosts a

general DBI mailing list.

• For printed information, the official DBI book is Programming the Perl DBI (Alligator Descartes and

Tim Bunce, O'Reilly & Associates, 2000). Information about the book is available at the DBI website,
http://dbi.perl.org/.

31.10 MySQL Python API

MySQLdb is a third-party driver that provides MySQL support for Python, compliant with the Python DB
API version 2.0. It can be found at http://sourceforge.net/projects/mysql-python/.

The new MySQL Connector/Python component provides an interface to the same Python API, and is
built into the MySQL Server and supported by Oracle. See MySQL Connector/Python Developer Guide
for details on the Connector, as well as coding guidelines for Python applications and sample Python
code.

31.11 MySQL Ruby APIs

5443

The MySQL/Ruby API

The mysql2 Ruby gem provides an API for connecting to MySQL, performing queries, and iterating
through results; it is intended to support MySQL 5.7 and MySQL 8.0. For more information, see the
mysql2 page at RubyGems.org or the project's GitHub page.

For background and syntax information about the Ruby language, see Ruby Programming Language.

31.11.1 The MySQL/Ruby API

The MySQL/Ruby module provides access to MySQL databases using Ruby through
libmysqlclient.

For information on installing the module, and the functions exposed, see MySQL/Ruby.

31.11.2 The Ruby/MySQL API

The Ruby/MySQL module provides access to MySQL databases using Ruby through a native driver
interface using the MySQL network protocol.

For information on installing the module, and the functions exposed, see Ruby/MySQL.

31.12 MySQL Tcl API

MySQLtcl is a simple API for accessing a MySQL database server from the Tcl programming
language. It can be found at http://www.xdobry.de/mysqltcl/.

31.13 MySQL Eiffel Wrapper

Eiffel MySQL is an interface to the MySQL database server using the Eiffel programming language,
written by Michael Ravits. It can be found at http://efsa.sourceforge.net/archive/ravits/mysql.htm.

5444

