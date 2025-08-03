Third-Party MySQL APIs

Environment

API

Type

Notes

MySQL wrapped

libmysqlclient

See MySQL wrapped.

Cocoa

MySQL-Cocoa

libmysqlclient

Compatible with
the Objective-C
Cocoa environment.
See http://mysql-
cocoa.sourceforge.net/

MySQL for D

Eiffel MySQL

libmysqlclient

See MySQL for D.

libmysqlclient

D

Eiffel

Erlang

Haskell

Objective Caml

Octave

ODBC

Perl

PHP

Python

Python

Java/JDBC

Connector/J

Native Driver

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

erlang-mysql-driver libmysqlclient

Haskell MySQL Bindings Native Driver

hsql-mysql

libmysqlclient

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

See Section 27.13,
“MySQL Eiffel Wrapper”.

See erlang-mysql-
driver.

See Brian O'Sullivan's
pure Haskell MySQL
bindings.

See MySQL driver for
Haskell.

See MySQL Connector/J
Developer Guide.

See MySQL Connector/
NET Developer Guide.

See MySQL Bindings for
Objective Caml.

See Database bindings
for GNU Octave.

See MySQL Connector/
ODBC Developer Guide.

See Section 27.9,
“MySQL Perl API”.

See Net::MySQL at
CPAN

mysql, ext/mysql
interface (deprecated)

mysqli, ext/mysqli
interface

PDO_MYSQL

PDO mysqlnd

Connector/Python

libmysqlclient

See MySQL and PHP.

libmysqlclient

See MySQL and PHP.

libmysqlclient

See MySQL and PHP.

Native Driver

Native Driver

Connector/Python C
Extension

libmysqlclient

MySQLdb

libmysqlclient

See MySQL Connector/
Python Developer Guide.

See MySQL Connector/
Python Developer Guide.

See Section 27.10,
“MySQL Python API”.

4475

MySQL Connector/C++

Environment

Ruby

API

mysql2

Scheme

SPL

Tcl

Myscsh

sql_mysql

MySQLtcl

Type

Notes

libmysqlclient

Uses libmysqlclient.
See Section 27.11,
“MySQL Ruby APIs”.

libmysqlclient

See Myscsh.

libmysqlclient

See sql_mysql for SPL.

libmysqlclient

See Section 27.12,
“MySQL Tcl API”.

27.1 MySQL Connector/C++

The MySQL Connector/C++ manual is published in standalone form, not as part of the MySQL Reference
Manual. For information, see these documents:

• Main manual: MySQL Connector/C++ 9.3 Developer Guide

• Release notes: MySQL Connector/C++ Release Notes

27.2 MySQL Connector/J

The MySQL Connector/J manual is published in standalone form, not as part of the MySQL Reference
Manual. For information, see these documents:

• Main manual: MySQL Connector/J Developer Guide

• Release notes: MySQL Connector/J Release Notes

27.3 MySQL Connector/NET

The MySQL Connector/NET manual is published in standalone form, not as part of the MySQL Reference
Manual. For information, see these documents:

• Main manual: MySQL Connector/NET Developer Guide

• Release notes: MySQL Connector/NET Release Notes

27.4 MySQL Connector/ODBC

The MySQL Connector/ODBC manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Main manual: MySQL Connector/ODBC Developer Guide

• Release notes: MySQL Connector/ODBC Release Notes

27.5 MySQL Connector/Python

The MySQL Connector/Python manual is published in standalone form, not as part of the MySQL
Reference Manual. For information, see these documents:

• Main manual: MySQL Connector/Python Developer Guide

• Release notes: MySQL Connector/Python Release Notes

27.6 libmysqld, the Embedded MySQL Server Library

4476

Embedded Server Examples

Using option files can make it easier to switch between a client/server application and one where MySQL
is embedded. Put common options under the [server] group. These are read by both MySQL versions.
Client/server-specific options should go under the [mysqld] section. Put options specific to the embedded
MySQL server library in the [embedded] section. Options specific to applications go under section labeled
[ApplicationName_SERVER]. See Section 4.2.2.2, “Using Option Files”.

27.6.4 Embedded Server Examples

These two example programs should work without any changes on a Linux or FreeBSD system. For other
operating systems, minor changes are needed, mostly with file paths. These examples are designed to
give enough details for you to understand the problem, without the clutter that is a necessary part of a real
application. The first example is very straightforward. The second example is a little more advanced with
some error checking. The first is followed by a command-line entry for compiling the program. The second
is followed by a GNUmake file that may be used for compiling instead.

Example 1

test1_libmysqld.c

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include "mysql.h"

MYSQL *mysql;
MYSQL_RES *results;
MYSQL_ROW record;

static char *server_options[] = \
       { "mysql_test", "--defaults-file=my.cnf", NULL };
int num_elements = (sizeof(server_options) / sizeof(char *)) - 1;

static char *server_groups[] = { "libmysqld_server",
                                 "libmysqld_client", NULL };

int main(void)
{
   mysql_library_init(num_elements, server_options, server_groups);
   mysql = mysql_init(NULL);
   mysql_options(mysql, MYSQL_READ_DEFAULT_GROUP, "libmysqld_client");
   mysql_options(mysql, MYSQL_OPT_USE_EMBEDDED_CONNECTION, NULL);

   mysql_real_connect(mysql, NULL,NULL,NULL, "database1", 0,NULL,0);

   mysql_query(mysql, "SELECT column1, column2 FROM table1");

   results = mysql_store_result(mysql);

   while((record = mysql_fetch_row(results))) {
      printf("%s - %s \n", record[0], record[1]);
   }

   mysql_free_result(results);
   mysql_close(mysql);
   mysql_library_end();

   return 0;
}

Here is the command line for compiling the above program:

gcc test1_libmysqld.c -o test1_libmysqld \
 `/usr/local/mysql/bin/mysql_config --include --libmysqld-libs`

4479

Embedded Server Examples

Example 2

To try the example, create an test2_libmysqld directory at the same level as the MySQL source
directory. Save the test2_libmysqld.c source and the GNUmakefile in the directory, and run GNU
make from inside the test2_libmysqld directory.

test2_libmysqld.c

/*
 * A simple example client, using the embedded MySQL server library
*/

#include <mysql.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

MYSQL *db_connect(const char *dbname);
void db_disconnect(MYSQL *db);
void db_do_query(MYSQL *db, const char *query);

const char *server_groups[] = {
  "test2_libmysqld_SERVER", "embedded", "server", NULL
};

int
main(int argc, char **argv)
{
  MYSQL *one, *two;

  /* mysql_library_init() must be called before any other mysql
   * functions.
   *
   * You can use mysql_library_init(0, NULL, NULL), and it
   * initializes the server using groups = {
   *   "server", "embedded", NULL
   *  }.
   *
   * In your $HOME/.my.cnf file, you probably want to put:

[test2_libmysqld_SERVER]
language = /path/to/source/of/mysql/sql/share/english

   * You could, of course, modify argc and argv before passing
   * them to this function.  Or you could create new ones in any
   * way you like.  But all of the arguments in argv (except for
   * argv[0], which is the program name) should be valid options
   * for the MySQL server.
   *
   * If you link this client against the normal mysqlclient
   * library, this function is just a stub that does nothing.
   */
  mysql_library_init(argc, argv, (char **)server_groups);

  one = db_connect("test");
  two = db_connect(NULL);

  db_do_query(one, "SHOW TABLE STATUS");
  db_do_query(two, "SHOW DATABASES");

  mysql_close(two);
  mysql_close(one);

  /* This must be called after all other mysql functions */
  mysql_library_end();

4480

Embedded Server Examples

  exit(EXIT_SUCCESS);
}

static void
die(MYSQL *db, char *fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap);
  va_end(ap);
  (void)putc('\n', stderr);
  if (db)
    db_disconnect(db);
  exit(EXIT_FAILURE);
}

MYSQL *
db_connect(const char *dbname)
{
  MYSQL *db = mysql_init(NULL);
  if (!db)
    die(db, "mysql_init failed: no memory");
  /*
   * Notice that the client and server use separate group names.
   * This is critical, because the server does not accept the
   * client's options, and vice versa.
   */
  mysql_options(db, MYSQL_READ_DEFAULT_GROUP, "test2_libmysqld_CLIENT");
  if (!mysql_real_connect(db, NULL, NULL, NULL, dbname, 0, NULL, 0))
    die(db, "mysql_real_connect failed: %s", mysql_error(db));

  return db;
}

void
db_disconnect(MYSQL *db)
{
  mysql_close(db);
}

void
db_do_query(MYSQL *db, const char *query)
{
  if (mysql_query(db, query) != 0)
    goto err;

  if (mysql_field_count(db) > 0)
  {
    MYSQL_RES   *res;
    MYSQL_ROW    row, end_row;
    int num_fields;

    if (!(res = mysql_store_result(db)))
      goto err;
    num_fields = mysql_num_fields(res);
    while ((row = mysql_fetch_row(res)))
    {
      (void)fputs(">> ", stdout);
      for (end_row = row + num_fields; row < end_row; ++row)
        (void)printf("%s\t", row ? (char*)*row : "NULL");
      (void)fputc('\n', stdout);
    }
    (void)fputc('\n', stdout);
    mysql_free_result(res);
  }
  else
    (void)printf("Affected rows: %lld\n", mysql_affected_rows(db));

4481

MySQL C API

  return;

err:
  die(db, "db_do_query failed: %s [%s]", mysql_error(db), query);
}

GNUmakefile

# This assumes the MySQL software is installed in /usr/local/mysql
inc      := /usr/local/mysql/include/mysql
lib      := /usr/local/mysql/lib

# If you have not installed the MySQL software yet, try this instead
#inc      := $(HOME)/mysql-5.7/include
#lib      := $(HOME)/mysql-5.7/libmysqld

CC       := gcc
CPPFLAGS := -I$(inc) -D_THREAD_SAFE -D_REENTRANT
CFLAGS   := -g -W -Wall
LDFLAGS  := -static
# You can change -lmysqld to -lmysqlclient to use the
# client/server library
LDLIBS    = -L$(lib) -lmysqld -lm -ldl -lcrypt

ifneq (,$(shell grep FreeBSD /COPYRIGHT 2>/dev/null))
# FreeBSD
LDFLAGS += -pthread
else
# Assume Linux
LDLIBS += -lpthread
endif

# This works for simple one-file test programs
sources := $(wildcard *.c)
objects := $(patsubst %c,%o,$(sources))
targets := $(basename $(sources))

all: $(targets)

clean:
        rm -f $(targets) $(objects) *.core

27.7 MySQL C API

The MySQL C API Developer Guide is published in standalone form, not as part of the MySQL Reference
Manual. See MySQL 5.7 C API Developer Guide.

27.8 MySQL PHP API

The MySQL PHP API manual is now published in standalone form, not as part of the MySQL Reference
Manual. See MySQL and PHP.

27.9 MySQL Perl API

The Perl DBI module provides a generic interface for database access. You can write a DBI script that
works with many different database engines without change. To use DBI with MySQL, install the following:

1. The DBI module.

2. The DBD::mysql module. This is the DataBase Driver (DBD) module for Perl.

4482

MySQL Python API

3. Optionally, the DBD module for any other type of database server you want to access.

Perl DBI is the recommended Perl interface. It replaces an older interface called mysqlperl, which should
be considered obsolete.

These sections contain information about using Perl with MySQL and writing MySQL applications in Perl:

• For installation instructions for Perl DBI support, see Section 2.12, “Perl Installation Notes”.

• For an example of reading options from option files, see Section 5.7.4, “Using Client Programs in a

Multiple-Server Environment”.

• For secure coding tips, see Section 6.1.1, “Security Guidelines”.

• For debugging tips, see Section 5.8.1.4, “Debugging mysqld under gdb”.

• For some Perl-specific environment variables, see Section 4.9, “Environment Variables”.

• For considerations for running on macOS, see Section 2.4, “Installing MySQL on macOS”.

• For ways to quote string literals, see Section 9.1.1, “String Literals”.

DBI information is available at the command line, online, or in printed form:

• Once you have the DBI and DBD::mysql modules installed, you can get information about them at the

command line with the perldoc command:

$> perldoc DBI
$> perldoc DBI::FAQ
$> perldoc DBD::mysql

You can also use pod2man, pod2html, and so on to translate this information into other formats.

• For online information about Perl DBI, visit the DBI website, http://dbi.perl.org/. That site hosts a general

DBI mailing list.

• For printed information, the official DBI book is Programming the Perl DBI (Alligator Descartes and Tim
Bunce, O'Reilly & Associates, 2000). Information about the book is available at the DBI website, http://
dbi.perl.org/.

27.10 MySQL Python API

MySQLdb is a third-party driver that provides MySQL support for Python, compliant with the Python DB API
version 2.0. It can be found at http://sourceforge.net/projects/mysql-python/.

The new MySQL Connector/Python component provides an interface to the same Python API, and is built
into the MySQL Server and supported by Oracle. See MySQL Connector/Python Developer Guide for
details on the Connector, as well as coding guidelines for Python applications and sample Python code.

27.11 MySQL Ruby APIs

The mysql2 Ruby gem provides an API for connecting to MySQL, performing queries, and iterating
through results; it is intended to support MySQL 5.7 and MySQL 8.0. For more information, see the
mysql2 page at RubyGems.org or the project's GitHub page.

For background and syntax information about the Ruby language, see Ruby Programming Language.

4483

The MySQL/Ruby API

27.11.1 The MySQL/Ruby API

The MySQL/Ruby module provides access to MySQL databases using Ruby through libmysqlclient.

For information on installing the module, and the functions exposed, see MySQL/Ruby.

27.11.2 The Ruby/MySQL API

The Ruby/MySQL module provides access to MySQL databases using Ruby through a native driver
interface using the MySQL network protocol.

For information on installing the module, and the functions exposed, see Ruby/MySQL.

27.12 MySQL Tcl API

MySQLtcl is a simple API for accessing a MySQL database server from the Tcl programming language. It
can be found at http://www.xdobry.de/mysqltcl/.

27.13 MySQL Eiffel Wrapper

Eiffel MySQL is an interface to the MySQL database server using the Eiffel programming language, written
by Michael Ravits. It can be found at http://efsa.sourceforge.net/archive/ravits/mysql.htm.

4484

