Overview of MySQL Programs

4.8.4 resolveip — Resolve Host name to IP Address or Vice Versa ........................................... 650
4.8.5 zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output ........................... 650
4.9  Environment  Variables .............................................................................................................. 650
4.10 Unix Signal Handling in MySQL ............................................................................................... 653

This chapter provides a brief overview of the MySQL command-line programs provided by Oracle
Corporation. It also discusses the general syntax for specifying options when you run these programs.
Most programs have options that are specific to their own operation, but the option syntax is similar for all
of them. Finally, the chapter provides more detailed descriptions of individual programs, including which
options they recognize.

4.1 Overview of MySQL Programs

There are many different programs in a MySQL installation. This section provides a brief overview of
them. Later sections provide a more detailed description of each one, with the exception of NDB Cluster
programs. Each program's description indicates its invocation syntax and the options that it supports.
Section 21.5, “NDB Cluster Programs”, describes programs specific to NDB Cluster.

Most MySQL distributions include all of these programs, except for those programs that are platform-
specific. (For example, the server startup scripts are not used on Windows.) The exception is that RPM
distributions are more specialized. There is one RPM for the server, another for client programs, and so
forth. If you appear to be missing one or more programs, see Chapter 2, Installing and Upgrading MySQL,
for information on types of distributions and what they contain. It may be that you have a distribution that
does not include all programs and you need to install an additional package.

Each MySQL program takes many different options. Most programs provide a --help option that you can
use to get a description of the program's different options. For example, try mysql --help.

You can override default option values for MySQL programs by specifying options on the command line or
in an option file. See Section 4.2, “Using MySQL Programs”, for general information on invoking programs
and specifying program options.

The MySQL server, mysqld, is the main program that does most of the work in a MySQL installation. The
server is accompanied by several related scripts that assist you in starting and stopping the server:

•  mysqld

The SQL daemon (that is, the MySQL server). To use client programs, mysqld must be running,
because clients gain access to databases by connecting to the server. See Section 4.3.1, “mysqld —
The MySQL Server”.

•  mysqld_safe

A server startup script. mysqld_safe attempts to start mysqld. See Section 4.3.2, “mysqld_safe —
MySQL Server Startup Script”.

•  mysql.server

A server startup script. This script is used on systems that use System V-style run directories containing
scripts that start system services for particular run levels. It invokes mysqld_safe to start the MySQL
server. See Section 4.3.3, “mysql.server — MySQL Server Startup Script”.

•  mysqld_multi

A server startup script that can start or stop multiple servers installed on the system. See Section 4.3.4,
“mysqld_multi — Manage Multiple MySQL Servers”.

Several programs perform setup operations during MySQL installation or upgrading:

304

Specifying Program Options

• For options that take a numeric value, the value can be given with a suffix of K, M, or G (either uppercase
or lowercase) to indicate a multiplier of 1024, 10242 or 10243. For example, the following command tells
mysqladmin to ping the server 1024 times, sleeping 10 seconds between each ping:

mysqladmin --count=1K --sleep=10 ping

• When specifying file names as option values, avoid the use of the ~ shell metacharacter. It might not be

interpreted as you expect.

Option values that contain spaces must be quoted when given on the command line. For example, the
--execute (or -e) option can be used with mysql to pass one or more semicolon-separated SQL
statements to the server. When this option is used, mysql executes the statements in the option value and
exits. The statements must be enclosed by quotation marks. For example:

$> mysql -u root -p -e "SELECT VERSION();SELECT NOW()"
Enter password: ******
+------------+
| VERSION()  |
+------------+
| 5.7.29     |
+------------+
+---------------------+
| NOW()               |
+---------------------+
| 2019-09-03 10:36:28 |
+---------------------+
$>

Note

The long form (--execute) is followed by an equal sign (=).

To use quoted values within a statement, you must either escape the inner quotation marks, or use a
different type of quotation marks within the statement from those used to quote the statement itself. The
capabilities of your command processor dictate your choices for whether you can use single or double
quotation marks and the syntax for escaping quote characters. For example, if your command processor
supports quoting with single or double quotation marks, you can use double quotation marks around the
statement, and single quotation marks for any quoted values within the statement.

4.2.2.2 Using Option Files

Most MySQL programs can read startup options from option files (sometimes called configuration files).
Option files provide a convenient way to specify commonly used options so that they need not be entered
on the command line each time you run a program.

To determine whether a program reads option files, invoke it with the --help option. (For mysqld, use --
verbose and --help.) If the program reads option files, the help message indicates which files it looks for
and which option groups it recognizes.

Note

A MySQL program started with the --no-defaults option reads no option files
other than .mylogin.cnf.

Many option files are plain text files, created using any text editor. The exception is the .mylogin.cnf file
that contains login path options. This is an encrypted file created by the mysql_config_editor utility.
See Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”. A “login path” is an option group

311

Specifying Program Options

The [client] option group is read by all client programs provided in MySQL distributions (but not by
mysqld). To understand how third-party client programs that use the C API can use option files, see the C
API documentation at mysql_options().

The [client] group enables you to specify options that apply to all clients. For example, [client] is
the appropriate group to use to specify the password for connecting to the server. (But make sure that the
option file is accessible only by yourself, so that other people cannot discover your password.) Be sure
not to put an option in the [client] group unless it is recognized by all client programs that you use.
Programs that do not understand the option quit after displaying an error message if you try to run them.

List more general option groups first and more specific groups later. For example, a [client] group is
more general because it is read by all client programs, whereas a [mysqldump] group is read only by
mysqldump. Options specified later override options specified earlier, so putting the option groups in the
order [client], [mysqldump] enables mysqldump-specific options to override [client] options.

Here is a typical global option file:

[client]
port=3306
socket=/tmp/mysql.sock

[mysqld]
port=3306
socket=/tmp/mysql.sock
key_buffer_size=16M
max_allowed_packet=8M

[mysqldump]
quick

Here is a typical user option file:

[client]
# The following password is sent to all standard MySQL clients
password="my password"

[mysql]
no-auto-rehash
connect_timeout=2

To create option groups to be read only by mysqld servers from specific MySQL release series, use
groups with names of [mysqld-5.6], [mysqld-5.7], and so forth. The following group indicates that
the sql_mode setting should be used only by MySQL servers with 5.7.x version numbers:

[mysqld-5.7]
sql_mode=TRADITIONAL

Option File Inclusions

It is possible to use !include directives in option files to include other option files and !includedir to
search specific directories for option files. For example, to include the /home/mydir/myopt.cnf file, use
the following directive:

!include /home/mydir/myopt.cnf

To search the /home/mydir directory and read option files found there, use this directive:

!includedir /home/mydir

MySQL makes no guarantee about the order in which option files in the directory are read.

315

Specifying Program Options

Note

Any files to be found and included using the !includedir directive on Unix
operating systems must have file names ending in .cnf. On Windows, this
directive checks for files with the .ini or .cnf extension.

Write the contents of an included option file like any other option file. That is, it should contain groups of
options, each preceded by a [group] line that indicates the program to which the options apply.

While an included file is being processed, only those options in groups that the current program is looking
for are used. Other groups are ignored. Suppose that a my.cnf file contains this line:

!include /home/mydir/myopt.cnf

And suppose that /home/mydir/myopt.cnf looks like this:

[mysqladmin]
force

[mysqld]
key_buffer_size=16M

If my.cnf is processed by mysqld, only the [mysqld] group in /home/mydir/myopt.cnf is used. If
the file is processed by mysqladmin, only the [mysqladmin] group is used. If the file is processed by
any other program, no options in /home/mydir/myopt.cnf are used.

The !includedir directive is processed similarly except that all option files in the named directory are
read.

If an option file contains !include or !includedir directives, files named by those directives are
processed whenever the option file is processed, no matter where they appear in the file.

For inclusion directives to work, the file path should not be specified within quotes and should have
no escape sequences. For example, the following statements provided in my.ini read the option file
myopts.ini:

!include C:/ProgramData/MySQL/MySQL Server/myopts.ini
!include C:\ProgramData\MySQL\MySQL Server\myopts.ini
!include C:\\ProgramData\\MySQL\\MySQL Server\\myopts.ini

On Windows, if !include /path/to/extra.ini is the last line in the file, make sure that a newline is
appended at the end or the line is ignored.

4.2.2.3 Command-Line Options that Affect Option-File Handling

Most MySQL programs that support option files handle the following options. Because these options affect
option-file handling, they must be given on the command line and not in an option file. To work properly,
each of these options must be given before other options, with these exceptions:

• --print-defaults may be used immediately after --defaults-file, --defaults-extra-file,

or --login-path.

• On Windows, if the server is started with the --defaults-file and --install options, --install

must be first. See Section 2.3.4.8, “Starting MySQL as a Windows Service”.

When specifying file names as option values, avoid the use of the ~ shell metacharacter because it might
not be interpreted as you expect.

316

Specifying Program Options

Table 4.3 Option File Option Summary

Option Name

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--login-path

--no-defaults

Description

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Read login path options from .mylogin.cnf

Read no option files

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=filename

Type

Default Value

File name

[none]

Read this option file after the global option file but (on Unix) before the user option file and (on all
platforms) before the login path file. (For information about the order in which option files are used, see
Section 4.2.2.2, “Using Option Files”.) If the file does not exist or is otherwise inaccessible, an error
occurs. If file_name is not an absolute path name, it is interpreted relative to the current directory.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

• --defaults-file=file_name

Command-Line Format

--defaults-file=filename

Type

Default Value

File name

[none]

Read only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs.
file_name is interpreted relative to the current directory if given as a relative path name rather than a
full path name.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=string

Type

Default Value

String

[none]

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, the mysql client normally reads the [client] and [mysql] groups. If this option is
given as --defaults-group-suffix=_other, mysql also reads the [client_other] and
[mysql_other] groups.

317

Specifying Program Options

• --login-path=name

Command-Line Format

--login-path=name

Type

Default Value

String

[none]

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

A client program reads the option group corresponding to the named login path, in addition to option
groups that the program reads by default. Consider this command:

mysql --login-path=mypath

By default, the mysql client reads the [client] and [mysql] option groups. So for the command
shown, mysql reads [client] and [mysql] from other option files, and [client], [mysql], and
[mypath] from the login path file.

Client programs read the login path file even when the --no-defaults option is used.

To specify an alternate login path file name, set the MYSQL_TEST_LOGIN_FILE environment variable.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

• --no-defaults

Command-Line Format

--no-defaults

Type

Default Value

Boolean

false

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that client programs read the .mylogin.cnf login path file, if it exists, even when --
no-defaults is used. This permits passwords to be specified in a safer way than on the command line
even if --no-defaults is present. To create .mylogin.cnf, use the mysql_config_editor utility.
See Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

• --print-defaults

Command-Line Format

--print-defaults

Type

Default Value

Boolean

false

Print the program name and all options that it gets from option files. Password values are masked.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

318

Specifying Program Options

4.2.2.4 Program Option Modifiers

Some options are “boolean” and control behavior that can be turned on or off. For example, the mysql
client supports a --column-names option that determines whether or not to display a row of column
names at the beginning of query results. By default, this option is enabled. However, you may want to
disable it in some instances, such as when sending the output of mysql into another program that expects
to see only data and not an initial header line.

To disable column names, you can specify the option using any of these forms:

--disable-column-names
--skip-column-names
--column-names=0

The --disable and --skip prefixes and the =0 suffix all have the same effect: They turn the option off.

The “enabled” form of the option may be specified in any of these ways:

--column-names
--enable-column-names
--column-names=1

The values ON, TRUE, OFF, and FALSE are also recognized for boolean options (not case-sensitive).

If an option is prefixed by --loose, a program does not exit with an error if it does not recognize the
option, but instead issues only a warning:

$> mysql --loose-no-such-option
mysql: WARNING: unknown option '--loose-no-such-option'

The --loose prefix can be useful when you run programs from multiple installations of MySQL on the
same machine and list options in an option file. An option that may not be recognized by all versions of a
program can be given using the --loose prefix (or loose in an option file). Versions of the program that
recognize the option process it normally, and versions that do not recognize it issue a warning and ignore
it.

The --maximum prefix is available for mysqld only and permits a limit to be placed on how large client
programs can set session system variables. To do this, use a --maximum prefix with the variable name.
For example, --maximum-max_heap_table_size=32M prevents any client from making the heap table
size limit larger than 32M.

The --maximum prefix is intended for use with system variables that have a session value. If applied
to a system variable that has only a global value, an error occurs. For example, with --maximum-
back_log=200, the server produces this error:

Maximum value of 'back_log' cannot be set

4.2.2.5 Using Options to Set Program Variables

Many MySQL programs have internal variables that can be set at runtime using the SET statement. See
Section 13.7.4.1, “SET Syntax for Variable Assignment”, and Section 5.1.8, “Using System Variables”.

Most of these program variables also can be set at server startup by using the same syntax that applies
to specifying program options. For example, mysql has a max_allowed_packet variable that controls
the maximum size of its communication buffer. To set the max_allowed_packet variable for mysql to a
value of 16MB, use either of the following commands:

mysql --max_allowed_packet=16777216
mysql --max_allowed_packet=16M

319

Specifying Program Options

The first command specifies the value in bytes. The second specifies the value in megabytes. For variables
that take a numeric value, the value can be given with a suffix of K, M, or G (either uppercase or lowercase)
to indicate a multiplier of 1024, 10242 or 10243. (For example, when used to set max_allowed_packet,
the suffixes indicate units of kilobytes, megabytes, or gigabytes.)

In an option file, variable settings are given without the leading dashes:

[mysql]
max_allowed_packet=16777216

Or:

[mysql]
max_allowed_packet=16M

If you like, underscores in an option name can be specified as dashes. The following option groups are
equivalent. Both set the size of the server's key buffer to 512MB:

[mysqld]
key_buffer_size=512M

[mysqld]
key-buffer-size=512M

In older versions of MySQL, program options could be specified in full or as any unambiguous prefix. For
example, the --compress option could be given to mysqldump as --compr, but not as --comp because
the latter is ambiguous. In MySQL 5.7, option prefixes are no longer supported; only full options are
accepted. This is because prefixes can cause problems when new options are implemented for programs
and a prefix that is currently unambiguous might become ambiguous in the future. Some implications of
this change:

• The --key-buffer option must now be specified as --key-buffer-size.

• The --skip-grant option must now be specified as --skip-grant-tables.

Suffixes for specifying a value multiplier can be used when setting a variable at program invocation time,
but not to set the value with SET at runtime. On the other hand, with SET, you can assign a variable's value
using an expression, which is not true when you set a variable at server startup. For example, the first of
the following lines is legal at program invocation time, but the second is not:

$> mysql --max_allowed_packet=16M
$> mysql --max_allowed_packet=16*1024*1024

Conversely, the second of the following lines is legal at runtime, but the first is not:

mysql> SET GLOBAL max_allowed_packet=16M;
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;

4.2.2.6 Option Defaults, Options Expecting Values, and the = Sign

By convention, long forms of options that assign a value are written with an equals (=) sign, like this:

mysql --host=tonfisk --user=jon

For options that require a value (that is, not having a default value), the equal sign is not required, and so
the following is also valid:

mysql --host tonfisk --user jon

In both cases, the mysql client attempts to connect to a MySQL server running on the host named
“tonfisk” using an account with the user name “jon”.

320

Specifying Program Options

Due to this behavior, problems can occasionally arise when no value is provided for an option that expects
one. Consider the following example, where a user connects to a MySQL server running on host tonfisk
as user jon:

$> mysql --host 85.224.35.45 --user jon
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.44 Source distribution

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql> SELECT CURRENT_USER();
+----------------+
| CURRENT_USER() |
+----------------+
| jon@%          |
+----------------+
1 row in set (0.00 sec)

Omitting the required value for one of these option yields an error, such as the one shown here:

$> mysql --host 85.224.35.45 --user
mysql: option '--user' requires an argument

In this case, mysql was unable to find a value following the --user option because nothing came after it
on the command line. However, if you omit the value for an option that is not the last option to be used, you
obtain a different error that you may not be expecting:

$> mysql --host --user jon
ERROR 2005 (HY000): Unknown MySQL server host '--user' (1)

Because mysql assumes that any string following --host on the command line is a host name, --host
--user is interpreted as --host=--user, and the client attempts to connect to a MySQL server running
on a host named “--user”.

Options having default values always require an equal sign when assigning a value; failing to do
so causes an error. For example, the MySQL server --log-error option has the default value
host_name.err, where host_name is the name of the host on which MySQL is running. Assume that
you are running MySQL on a computer whose host name is “tonfisk”, and consider the following invocation
of mysqld_safe:

$> mysqld_safe &
[1] 11699
$> 080112 12:53:40 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
080112 12:53:40 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
$>

After shutting down the server, restart it as follows:

$> mysqld_safe --log-error &
[1] 11699
$> 080112 12:53:40 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
080112 12:53:40 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
$>

The result is the same, since --log-error is not followed by anything else on the command line,
and it supplies its own default value. (The & character tells the operating system to run MySQL in the
background; it is ignored by MySQL itself.) Now suppose that you wish to log errors to a file named my-
errors.err. You might try starting the server with --log-error my-errors, but this does not have
the intended effect, as shown here:

$> mysqld_safe --log-error my-errors &
[1] 31357
$> 080111 22:53:31 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.

321

Specifying Program Options

080111 22:53:32 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
080111 22:53:34 mysqld_safe mysqld from pid file /usr/local/mysql/var/tonfisk.pid ended

[1]+  Done                    ./mysqld_safe --log-error my-errors

The server attempted to start using /usr/local/mysql/var/tonfisk.err as the error log, but then
shut down. Examining the last few lines of this file shows the reason:

$> tail /usr/local/mysql/var/tonfisk.err
2013-09-24T15:36:22.278034Z 0 [ERROR] Too many arguments (first extra is 'my-errors').
2013-09-24T15:36:22.278059Z 0 [Note] Use --verbose --help to get a list of available options!
2013-09-24T15:36:22.278076Z 0 [ERROR] Aborting
2013-09-24T15:36:22.279704Z 0 [Note] InnoDB: Starting shutdown...
2013-09-24T15:36:23.777471Z 0 [Note] InnoDB: Shutdown completed; log sequence number 2319086
2013-09-24T15:36:23.780134Z 0 [Note] mysqld: Shutdown complete

Because the --log-error option supplies a default value, you must use an equal sign to assign a
different value to it, as shown here:

$> mysqld_safe --log-error=my-errors &
[1] 31437
$> 080111 22:54:15 mysqld_safe Logging to '/usr/local/mysql/var/my-errors.err'.
080111 22:54:15 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var

$>

Now the server has been started successfully, and is logging errors to the file /usr/local/mysql/var/
my-errors.err.

Similar issues can arise when specifying option values in option files. For example, consider a my.cnf file
that contains the following:

[mysql]

host
user

When the mysql client reads this file, these entries are parsed as --host --user or --host=--user,
with the result shown here:

$> mysql
ERROR 2005 (HY000): Unknown MySQL server host '--user' (1)

However, in option files, an equal sign is not assumed. Suppose the my.cnf file is as shown here:

[mysql]

user jon

Trying to start mysql in this case causes a different error:

$> mysql
mysql: unknown option '--user jon'

A similar error would occur if you were to write host tonfisk in the option file rather than
host=tonfisk. Instead, you must use the equal sign:

[mysql]

user=jon

Now the login attempt succeeds:

$> mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5

322

Command Options for Connecting to the Server

Server version: 5.7.44 Source distribution

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql> SELECT USER();
+---------------+
| USER()        |
+---------------+
| jon@localhost |
+---------------+
1 row in set (0.00 sec)

This is not the same behavior as with the command line, where the equal sign is not required:

$> mysql --user jon --host tonfisk
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 6
Server version: 5.7.44 Source distribution

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

mysql> SELECT USER();
+---------------+
| USER()        |
+---------------+
| jon@tonfisk   |
+---------------+
1 row in set (0.00 sec)

Specifying an option requiring a value without a value in an option file causes the server to abort with an
error.

4.2.3 Command Options for Connecting to the Server

This section describes options supported by most MySQL client programs that control how client programs
establish connections to the server and whether connections are encrypted. These options can be given on
the command line or in an option file.

• Command Options for Connection Establishment

• Command Options for Encrypted Connections

Command Options for Connection Establishment

This section describes options that control how client programs establish connections to the server. For
additional information and examples showing how to use them, see Section 4.2.4, “Connecting to the
MySQL Server Using Command Options”.

Table 4.4 Connection-Establishment Option Summary

Option Name

--default-auth

--host

--password

--pipe

--plugin-dir

Description

Deprecated

Authentication plugin to use

Host on which MySQL server is
located

Password to use when connecting
to server

Connect to server using named
pipe (Windows only)

Directory where plugins are
installed

323

Command Options for Connecting to the Server

Option Name

--port

--protocol

--secure-auth

--shared-memory-base-name

--socket

--user

Description

Deprecated

TCP/IP port number for
connection

Transport protocol to use

Do not send passwords to server
in old (pre-4.1) format

Yes

Shared-memory name for shared-
memory connections (Windows
only)

Unix socket file or Windows
named pipe to use

MySQL user name to use when
connecting to server

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

The host on which the MySQL server is running. The value can be a host name, IPv4 address, or IPv6
address. The default value is localhost.

• --password[=pass_val], -p[pass_val]

Command-Line Format

--password[=password]

Type

Default Value

String

[none]

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, the client program prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to send
no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that the client program should not prompt for one, use
the --skip-password option.

324

Command Options for Connecting to the Server

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used to
specify an authentication plugin but the client program does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use. The default port number is 3306.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

325

Command Options for Connecting to the Server

MEMORY

This option explicitly specifies which transport protocol to use for connecting to the server. It is useful
when other connection parameters normally result in use of a protocol other than the one you want. For
example, connections on Unix to localhost are made using a Unix socket file by default:

mysql --host=localhost

To force TCP/IP transport to be used instead, specify a --protocol option:

mysql --host=localhost --protocol=TCP

The following table shows the permissible --protocol option values and indicates the applicable
platforms for each value. The values are not case-sensitive.

--protocol Value

Transport Protocol Used

Applicable Platforms

TCP

SOCKET

PIPE

MEMORY

TCP/IP transport to local or
remote server

All

Unix socket-file transport to local
server

Unix and Unix-like systems

Named-pipe transport to local
server

Windows

Shared-memory transport to local
server

Windows

See also Section 4.2.5, “Connection Transport Protocols”

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

326

Command Options for Connecting to the Server

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

On Unix, the name of the Unix socket file to use for connections made using a named pipe to a local
server. The default Unix socket file name is /tmp/mysql.sock.

On Windows, the name of the named pipe to use for connections to a local server. The default Windows
pipe name is MySQL. The pipe name is not case-sensitive.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

Type

String

The user name of the MySQL account to use for connecting to the server. The default user name is
ODBC on Windows or your Unix login name on Unix.

Command Options for Encrypted Connections

This section describes options for client programs that specify whether to use encrypted connections to
the server, the names of certificate and key files, and other parameters related to encrypted-connection
support. For examples of suggested use and how to check whether a connection is encrypted, see
Section 6.3.1, “Configuring MySQL to Use Encrypted Connections”.

Note

These options have an effect only for connections that use a transport protocol
subject to encryption; that is, TCP/IP and Unix socket-file connections. See
Section 4.2.5, “Connection Transport Protocols”

For information about using encrypted connections from the MySQL C API, see Support for Encrypted
Connections.

Table 4.5 Connection-Encryption Option Summary

Option Name

Description

--get-server-public-key

--server-public-key-path

Request RSA public key from
server

Path name to file containing RSA
public key

Introduced

5.7.23

327

Command Options for Connecting to the Server

Option Name

Description

Introduced

--skip-ssl

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

Disable connection encryption

Enable connection encryption

File that contains list of trusted
SSL Certificate Authorities

Directory that contains trusted
SSL Certificate Authority
certificate files

File that contains X.509 certificate

Permissible ciphers for connection
encryption

File that contains certificate
revocation lists

Directory that contains certificate
revocation-list files

File that contains X.509 key

Desired security state of
connection to server

5.7.11

--ssl-verify-server-cert

--tls-version

Verify host name against server
certificate Common Name identity

Permissible TLS protocols for
encrypted connections

5.7.10

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that
plugin, the server does not send the public key unless requested. This option is ignored for accounts that
do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

328

Command Options for Connecting to the Server

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

This option is available only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

• --ssl, --skip-ssl

Command-Line Format

Disabled by

Type

Default Value

--ssl

skip-ssl

Boolean

FALSE

Command-Line Format

--skip-ssl

Note

The client-side --ssl option is deprecated as of MySQL 5.7.11 and is removed
in MySQL 8.0. For client programs, use --ssl-mode instead:

• Use --ssl-mode=REQUIRED instead of --ssl=1 or --enable-ssl.

• Use --ssl-mode=DISABLED instead of --ssl=0, --skip-ssl, or --

disable-ssl.

• No explicit --ssl-mode option is equivalent to no explicit --ssl option.

The server-side --ssl option is not deprecated.

By default, MySQL client programs attempt to establish an encrypted connection if the server supports
encrypted connections, with further control available through the --ssl option: The client-side --ssl
option works as follows:

• In the absence of an --ssl option, clients attempt to connect using encryption, falling back to an

unencrypted connection if an encrypted connection cannot be established.

• The presence of an explicit --ssl option or a synonym (--ssl=1, --enable-ssl) is prescriptive:

Clients require an encrypted connection and fail if one cannot be established.

• With an --ssl=0 option or a synonym (--skip-ssl, --disable-ssl), clients use an unencrypted

connection.

To require use of encrypted connections by a MySQL account, use CREATE USER to create the account
with a REQUIRE SSL clause, or use ALTER USER for an existing account to add a REQUIRE SSL

329

Command Options for Connecting to the Server

clause. This causes connection attempts by clients that use the account to be rejected unless MySQL
supports encrypted connections and an encrypted connection can be established.

The REQUIRE clause permits other encryption-related options, which can be used to enforce security
requirements stricter than REQUIRE SSL. For additional details about which command options may or
must be specified by clients that connect using accounts configured using the various REQUIRE options,
see CREATE USER SSL/TLS Options.

To specify additional parameters for encrypted connections, consider setting at least the ssl_cert
and ssl_key system variables on the server side and the --ssl-ca option on the client side. See
Section 6.3.1, “Configuring MySQL to Use Encrypted Connections”, which also describes server
capabilities for certificate and key file autogeneration and autodiscovery.

• --ssl-ca=file_name

Command-Line Format

--ssl-ca=file_name

Type

File name

The path name of the Certificate Authority (CA) certificate file in PEM format. The file contains a list of
trusted SSL Certificate Authorities.

To tell the client not to authenticate the server certificate when establishing an encrypted connection to
the server, specify neither --ssl-ca nor --ssl-capath. The server still verifies the client according
to any applicable requirements established for the client account, and it still uses any ssl_ca or
ssl_capath system variable values specified on the server side.

To specify the CA file for the server, set the ssl_ca system variable.

• --ssl-capath=dir_name

Command-Line Format

--ssl-capath=dir_name

Type

Directory name

The path name of the directory that contains trusted SSL certificate authority (CA) certificate files
in PEM format. Support for this capability depends on the SSL library used to compile MySQL; see
Section 6.3.4, “SSL Library-Dependent Capabilities”.

To tell the client not to authenticate the server certificate when establishing an encrypted connection to
the server, specify neither --ssl-ca nor --ssl-capath. The server still verifies the client according
to any applicable requirements established for the client account, and it still uses any ssl_ca or
ssl_capath system variable values specified on the server side.

To specify the CA directory for the server, set the ssl_capath system variable.

• --ssl-cert=file_name

Command-Line Format

--ssl-cert=file_name

Type

File name

The path name of the client SSL public key certificate file in PEM format.

To specify the server SSL public key certificate file, set the ssl_cert system variable.

330

Command Options for Connecting to the Server

• --ssl-cipher=cipher_list

Command-Line Format

--ssl-cipher=name

Type

String

The list of permissible ciphers for connection encryption. If no cipher in the list is supported, encrypted
connections do not work.

For greatest portability, cipher_list should be a list of one or more cipher names, separated by
colons. This format is understood both by OpenSSL and yaSSL. Examples:

--ssl-cipher=AES128-SHA
--ssl-cipher=DHE-RSA-AES128-GCM-SHA256:AES128-SHA

OpenSSL supports a more flexible syntax for specifying ciphers, as described in the OpenSSL
documentation at https://www.openssl.org/docs/manmaster/man1/ciphers.html. yaSSL does not, so
attempts to use that extended syntax fail for a MySQL distribution compiled using yaSSL.

For information about which encryption ciphers MySQL supports, see Section 6.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

To specify the encryption ciphers for the server, set the ssl_cipher system variable.

• --ssl-crl=file_name

Command-Line Format

--ssl-crl=file_name

Type

File name

The path name of the file containing certificate revocation lists in PEM format. Support for revocation-
list capability depends on the SSL library used to compile MySQL. See Section 6.3.4, “SSL Library-
Dependent Capabilities”.

If neither --ssl-crl nor --ssl-crlpath is given, no CRL checks are performed, even if the CA path
contains certificate revocation lists.

To specify the revocation-list file for the server, set the ssl_crl system variable.

• --ssl-crlpath=dir_name

Command-Line Format

--ssl-crlpath=dir_name

Type

Directory name

The path name of the directory that contains certificate revocation-list files in PEM format. Support for
revocation-list capability depends on the SSL library used to compile MySQL. See Section 6.3.4, “SSL
Library-Dependent Capabilities”.

If neither --ssl-crl nor --ssl-crlpath is given, no CRL checks are performed, even if the CA path
contains certificate revocation lists.

331

To specify the revocation-list directory for the server, set the ssl_crlpath system variable.

Command Options for Connecting to the Server

• --ssl-key=file_name

Command-Line Format

--ssl-key=file_name

Type

File name

The path name of the client SSL private key file in PEM format. For better security, use a certificate with
an RSA key size of at least 2048 bits.

If the key file is protected by a passphrase, the client program prompts the user for the passphrase.
The password must be given interactively; it cannot be stored in a file. If the passphrase is incorrect, the
program continues as if it could not read the key.

To specify the server SSL private key file, set the ssl_key system variable.

• --ssl-mode=mode

Command-Line Format

--ssl-mode=mode

Introduced

Type

Default Value

Valid Values

5.7.11

Enumeration

PREFERRED

DISABLED

PREFERRED

REQUIRED

VERIFY_CA

VERIFY_IDENTITY

This option specifies the desired security state of the connection to the server. These mode values are
permissible, in order of increasing strictness:

• DISABLED: Establish an unencrypted connection. This is like the legacy --ssl=0 option or its

synonyms (--skip-ssl, --disable-ssl).

• PREFERRED: Establish an encrypted connection if the server supports encrypted connections, falling
back to an unencrypted connection if an encrypted connection cannot be established. This is the
default if --ssl-mode is not specified.

Connections over Unix socket files are not encrypted with a mode of PREFERRED. To enforce
encryption for Unix socket-file connections, use a mode of REQUIRED or stricter. (However, socket-
file transport is secure by default, so encrypting a socket-file connection makes it no more secure and
increases CPU load.)

• REQUIRED: Establish an encrypted connection if the server supports encrypted connections. The

connection attempt fails if an encrypted connection cannot be established.

• VERIFY_CA: Like REQUIRED, but additionally verify the server Certificate Authority (CA) certificate

against the configured CA certificates. The connection attempt fails if no valid matching CA certificates
are found.

332

Command Options for Connecting to the Server

• VERIFY_IDENTITY: Like VERIFY_CA, but additionally perform host name identity verification

by checking the host name the client uses for connecting to the server against the identity in the
certificate that the server sends to the client:

• As of MySQL 5.7.23, if the client uses OpenSSL 1.0.2 or higher, the client checks whether the host
name that it uses for connecting matches either the Subject Alternative Name value or the Common
Name value in the server certificate. Host name identity verification also works with certificates that
specify the Common Name using wildcards.

• Otherwise, the client checks whether the host name that it uses for connecting matches the

Common Name value in the server certificate.

The connection fails if there is a mismatch. For encrypted connections, this option helps prevent man-
in-the-middle attacks. This is like the legacy --ssl-verify-server-cert option.

Note

Host name identity verification with VERIFY_IDENTITY does not work with
self-signed certificates that are created automatically by the server or manually
using mysql_ssl_rsa_setup (see Section 6.3.3.1, “Creating SSL and RSA
Certificates and Keys using MySQL”). Such self-signed certificates do not
contain the server name as the Common Name value.

Important

The default setting, --ssl-mode=PREFERRED, produces an encrypted
connection if the other default settings are unchanged. However, to help prevent
sophisticated man-in-the-middle attacks, it is important for the client to verify
the server’s identity. The settings --ssl-mode=VERIFY_CA and --ssl-
mode=VERIFY_IDENTITY are a better choice than the default setting to help
prevent this type of attack. To implement one of these settings, you must first
ensure that the CA certificate for the server is reliably available to all the clients
that use it in your environment, otherwise availability issues will result. For this
reason, they are not the default setting.

The --ssl-mode option interacts with CA certificate options as follows:

• If --ssl-mode is not explicitly set otherwise, use of --ssl-ca or --ssl-capath implies --ssl-

mode=VERIFY_CA.

• For --ssl-mode values of VERIFY_CA or VERIFY_IDENTITY, --ssl-ca or --ssl-capath is also

required, to supply a CA certificate that matches the one used by the server.

• An explicit --ssl-mode option with a value other than VERIFY_CA or VERIFY_IDENTITY, together
with an explicit --ssl-ca or --ssl-capath option, produces a warning that no verification of the
server certificate is performed, despite a CA certificate option being specified.

The --ssl-mode option was added in MySQL 5.7.11.

To require use of encrypted connections by a MySQL account, use CREATE USER to create the account
with a REQUIRE SSL clause, or use ALTER USER for an existing account to add a REQUIRE SSL

333

Command Options for Connecting to the Server

clause. This causes connection attempts by clients that use the account to be rejected unless MySQL
supports encrypted connections and an encrypted connection can be established.

The REQUIRE clause permits other encryption-related options, which can be used to enforce security
requirements stricter than REQUIRE SSL. For additional details about which command options may or
must be specified by clients that connect using accounts configured using the various REQUIRE options,
see CREATE USER SSL/TLS Options.

• --ssl-verify-server-cert

Command-Line Format

--ssl-verify-server-cert

Type

Default Value

Boolean

FALSE

Note

The --ssl-verify-server-cert option is deprecated as of MySQL 5.7.11
and is removed in MySQL 8.0. Use --ssl-mode=VERIFY_IDENTITY instead.

This option causes the client to perform host name identity verification by checking the host name the
client uses for connecting to the server against the identity in the certificate that the server sends to the
client:

• As of MySQL 5.7.23, if the client uses OpenSSL 1.0.2 or higher, the client checks whether the host
name that it uses for connecting matches either the Subject Alternative Name value or the Common
Name value in the server certificate.

• Otherwise, the client checks whether the host name that it uses for connecting matches the Common

Name value in the server certificate.

The connection fails if there is a mismatch. For encrypted connections, this option helps prevent man-in-
the-middle attacks. Host name identity verification is disabled by default.

Note

Host name identity verification does not work with self-signed certificates created
automatically by the server, or manually using mysql_ssl_rsa_setup (see
Section 6.3.3.1, “Creating SSL and RSA Certificates and Keys using MySQL”).
Such self-signed certificates do not contain the server name as the Common
Name value.

Host name identity verification also does not work with certificates that specify the
Common Name using wildcards because that name is compared verbatim to the
server name.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

5.7.10

String

334

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

Connecting to the MySQL Server Using Command Options

TLSv1,TLSv1.1 (yaSSL)

This option specifies the TLS protocols the client permits for encrypted connections. The value is a list of
one or more comma-separated protocol versions. For example:

mysql --tls-version="TLSv1.1,TLSv1.2"

The protocols that can be named for this option depend on the SSL library used to compile MySQL.
Permitted protocols should be chosen such as not to leave “holes” in the list. For example, these values
do not have holes:

--tls-version="TLSv1,TLSv1.1,TLSv1.2"
--tls-version="TLSv1.1,TLSv1.2"
--tls-version="TLSv1.2"

This value does have a hole and should not be used:

--tls-version="TLSv1,TLSv1.2"

For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and Ciphers”.

This option was added in MySQL 5.7.10.

To specify which TLS protocols the server permits, set the tls_version system variable.

4.2.4 Connecting to the MySQL Server Using Command Options

This section describes use of command-line options to specify how to establish connections to the MySQL
server, for clients such as mysql or mysqldump. For additional information if you are unable to connect,
see Section 6.2.17, “Troubleshooting Problems Connecting to MySQL”.

For a client program to connect to the MySQL server, it must use the proper connection parameters, such
as the name of the host where the server is running and the user name and password of your MySQL
account. Each connection parameter has a default value, but you can override default values as necessary
using program options specified either on the command line or in an option file.

The examples here use the mysql client program, but the principles apply to other clients such as
mysqldump, mysqladmin, or mysqlshow.

This command invokes mysql without specifying any explicit connection parameters:

mysql

Because there are no parameter options, the default values apply:

• The default host name is localhost. On Unix, this has a special meaning, as described later.

• The default user name is ODBC on Windows or your Unix login name on Unix.

• No password is sent because neither --password nor -p is given.

• For mysql, the first nonoption argument is taken as the name of the default database. Because there is

no such argument, mysql selects no default database.

To specify the host name and user name explicitly, as well as a password, supply appropriate options on
the command line. To select a default database, add a database-name argument. Examples:

mysql --host=localhost --user=myname --password=password mydb

335

Connecting to the MySQL Server Using Command Options

mysql -h localhost -u myname -ppassword mydb

For password options, the password value is optional:

• If you use a --password or -p option and specify a password value, there must be no space between

--password= or -p and the password following it.

• If you use --password or -p but do not specify a password value, the client program prompts you to
enter the password. The password is not displayed as you enter it. This is more secure than giving the
password on the command line, which might enable other users on your system to see the password line
by executing a command such as ps. See Section 6.1.2.1, “End-User Guidelines for Password Security”.

• To explicitly specify that there is no password and that the client program should not prompt for one, use

the --skip-password option.

As just mentioned, including the password value on the command line is a security risk. To avoid this risk,
specify the --password or -p option without any following password value:

mysql --host=localhost --user=myname --password mydb
mysql -h localhost -u myname -p mydb

When the --password or -p option is given with no password value, the client program prints a prompt
and waits for you to enter the password. (In these examples, mydb is not interpreted as a password
because it is separated from the preceding password option by a space.)

On some systems, the library routine that MySQL uses to prompt for a password automatically limits the
password to eight characters. That limitation is a property of the system library, not MySQL. Internally,
MySQL does not have any limit for the length of the password. To work around the limitation on systems
affected by it, specify your password in an option file (see Section 4.2.2.2, “Using Option Files”). Another
workaround is to change your MySQL password to a value that has eight or fewer characters, but that has
the disadvantage that shorter passwords tend to be less secure.

Client programs determine what type of connection to make as follows:

• If the host is not specified or is localhost, a connection to the local host occurs:

• On Windows, the client connects using shared memory, if the server was started with the

shared_memory system variable enabled to support shared-memory connections.

• On Unix, MySQL programs treat the host name localhost specially, in a way that is likely different
from what you expect compared to other network-based programs: the client connects using a Unix
socket file. The --socket option or the MYSQL_UNIX_PORT environment variable may be used to
specify the socket name.

• On Windows, if host is . (period), or TCP/IP is not enabled and --socket is not specified or the

host is empty, the client connects using a named pipe, if the server was started with the named_pipe
system variable enabled to support named-pipe connections. If named-pipe connections are not
supported or if the user making the connection is not a member of the Windows group specified by the
named_pipe_full_access_group system variable, an error occurs.

• Otherwise, the connection uses TCP/IP.

The --protocol option enables you to use a particular transport protocol even when other options
normally result in use of a different protocol. That is, --protocol specifies the transport protocol explicitly
and overrides the preceding rules, even for localhost.

Only connection options that are relevant to the selected transport protocol are used or checked. Other
connection options are ignored. For example, with --host=localhost on Unix, the client attempts to

336

Connection Transport Protocols

For more information, see Section 4.2.2.2, “Using Option Files”.

• Some connection parameters can be specified using environment variables. Examples:

• To specify the host for mysql, use MYSQL_HOST.

• On Windows, to specify the MySQL user name, use USER.

• To specify the password, use MYSQL_PWD. However, this is insecure; see Section 6.1.2.1, “End-User

Guidelines for Password Security”.

For a list of supported environment variables, see Section 4.9, “Environment Variables”.

4.2.5 Connection Transport Protocols

For programs that use the MySQL client library (for example, mysql and mysqldump), MySQL supports
connections to the server based on several transport protocols: TCP/IP, Unix socket file, named pipe,
and shared memory. This section describes how to select these protocols, and how they are similar and
different.

• Transport Protocol Selection

• Transport Support for Local and Remote Connections

• Interpretation of localhost

• Encryption and Security Characteristics

• Connection Compression

Transport Protocol Selection

For a given connection, if the transport protocol is not specified explicitly, it is determined implicitly. For
example, connections to localhost result in a socket file connection on Unix and Unix-like systems, and
a TCP/IP connection to 127.0.0.1 otherwise. For additional information, see Section 4.2.4, “Connecting
to the MySQL Server Using Command Options”.

To specify the protocol explicitly, use the --protocol command option. The following table shows the
permissible values for --protocol and indicates the applicable platforms for each value. The values are
not case-sensitive.

--protocol Value

Transport Protocol Used

Applicable Platforms

TCP

SOCKET

PIPE

MEMORY

TCP/IP

Unix socket file

Named pipe

Shared memory

All

Unix and Unix-like systems

Windows

Windows

Transport Support for Local and Remote Connections

TCP/IP transport supports connections to local or remote MySQL servers.

Socket-file, named-pipe, and shared-memory transports support connections only to local MySQL servers.
(Named-pipe transport does allow for remote connections, but this capability is not implemented in
MySQL.)

338

Connection Compression Control

Interpretation of localhost

If the transport protocol is not specified explicitly, localhost is interpreted as follows:

• On Unix and Unix-like systems, a connection to localhost results in a socket-file connection.

• Otherwise, a connection to localhost results in a TCP/IP connection to 127.0.0.1.

If the transport protocol is specified explicitly, localhost is interpreted with respect to that protocol.
For example, with --protocol=TCP, a connection to localhost results in a TCP/IP connection to
127.0.0.1 on all platforms.

Encryption and Security Characteristics

TCP/IP and socket-file transports are subject to TLS/SSL encryption, using the options described in
Command Options for Encrypted Connections. Named-pipe and shared-memory transports are not subject
to TLS/SSL encryption.

A connection is secure by default if made over a transport protocol that is secure by default. Otherwise, for
protocols that are subject to TLS/SSL encryption, a connection may be made secure using encryption:

• TCP/IP connections are not secure by default, but can be encrypted to make them secure.

• Socket-file connections are secure by default. They can also be encrypted, but encrypting a socket-file

connection makes it no more secure and increases CPU load.

• Named-pipe connections are not secure by default, and are not subject to encryption to make them

secure. However, the named_pipe_full_access_group system variable is available to control which
MySQL users are permitted to use named-pipe connections.

• Shared-memory connections are secure by default.

If the require_secure_transport system variable is enabled, the server permits only connections that
use some form of secure transport. Per the preceding remarks, connections that use TCP/IP encrypted
using TLS/SSL, a socket file, or shared memory are secure connections. TCP/IP connections not
encrypted using TLS/SSL and named-pipe connections are not secure.

See also Configuring Encrypted Connections as Mandatory.

Connection Compression

All transport protocols are subject to use of compression on the traffic between the client and server. If both
compression and encryption are used for a given connection, compression occurs before encryption. For
more information, see Section 4.2.6, “Connection Compression Control”.

4.2.6 Connection Compression Control

Connections to the server can use compression on the traffic between client and server to reduce the
number of bytes sent over the connection. By default, connections are uncompressed, but can be
compressed if the server and the client both support compression.

Compressed connections originate on the client side but affect CPU load on both the client and server
sides because both sides perform compression and decompression operations. Because enabling
compression decreases performance, its benefits occur primarily when there is low network bandwidth,
network transfer time dominates the cost of compression and decompression operations, and result sets
are large.

339

Setting Environment Variables

Compression control applies to connections to the server by client programs and by servers participating
in source/replica replication. Compression control does not apply to Group Replication connections, X
Protocol connections, or connections for FEDERATED tables.

These configuration parameters are available for controlling connection compression:

• Client programs support a --compress command-line option to specify use of compression for the

connection to the server.

• For programs that use the MySQL C API, enabling the MYSQL_OPT_COMPRESS option for the
mysql_options() function specifies use of compression for the connection to the server.

• For source/replica replication, enabling the slave_compressed_protocol system variable specifies

use of compression for replica connections to the source.

In each case, when use of compression is specified, the connection uses the zlib compression algorithm
if both sides support it, with fallback to an uncompressed connection otherwise.

4.2.7 Setting Environment Variables

Environment variables can be set at the command prompt to affect the current invocation of your command
processor, or set permanently to affect future invocations. To set a variable permanently, you can set it in
a startup file or by using the interface provided by your system for this purpose. Consult the documentation
for your command interpreter for specific details. Section 4.9, “Environment Variables”, lists all environment
variables that affect MySQL program operation.

To specify a value for an environment variable, use the syntax appropriate for your command processor.
For example, on Windows, you can set the USER variable to specify your MySQL account name. To do so,
use this syntax:

SET USER=your_name

The syntax on Unix depends on your shell. Suppose that you want to specify the TCP/IP port number using
the MYSQL_TCP_PORT variable. Typical syntax (such as for sh, ksh, bash, zsh, and so on) is as follows:

MYSQL_TCP_PORT=3306
export MYSQL_TCP_PORT

The first command sets the variable, and the export command exports the variable to the shell
environment so that its value becomes accessible to MySQL and other processes.

For csh and tcsh, use setenv to make the shell variable available to the environment:

setenv MYSQL_TCP_PORT 3306

The commands to set environment variables can be executed at your command prompt to take effect
immediately, but the settings persist only until you log out. To have the settings take effect each time you
log in, use the interface provided by your system or place the appropriate command or commands in a
startup file that your command interpreter reads each time it starts.

On Windows, you can set environment variables using the System Control Panel (under Advanced).

On Unix, typical shell startup files are .bashrc or .bash_profile for bash, or .tcshrc for tcsh.

Suppose that your MySQL programs are installed in /usr/local/mysql/bin and that you want to make
it easy to invoke these programs. To do this, set the value of the PATH environment variable to include that
directory. For example, if your shell is bash, add the following line to your .bashrc file:

340

Server and Server-Startup Programs

PATH=${PATH}:/usr/local/mysql/bin

bash uses different startup files for login and nonlogin shells, so you might want to add the setting to
.bashrc for login shells and to .bash_profile for nonlogin shells to make sure that PATH is set
regardless.

If your shell is tcsh, add the following line to your .tcshrc file:

setenv PATH ${PATH}:/usr/local/mysql/bin

If the appropriate startup file does not exist in your home directory, create it with a text editor.

After modifying your PATH setting, open a new console window on Windows or log in again on Unix so that
the setting goes into effect.

4.3 Server and Server-Startup Programs

This section describes mysqld, the MySQL server, and several programs that are used to start the server.

4.3.1 mysqld — The MySQL Server

mysqld, also known as MySQL Server, is a single multithreaded program that does most of the work
in a MySQL installation. It does not spawn additional processes. MySQL Server manages access to the
MySQL data directory that contains databases and tables. The data directory is also the default location for
other information such as log files and status files.

Note

Some installation packages contain a debugging version of the server named
mysqld-debug. Invoke this version instead of mysqld for debugging support,
memory allocation checking, and trace file support (see Section 5.8.1.2, “Creating
Trace Files”).

When MySQL server starts, it listens for network connections from client programs and manages access to
databases on behalf of those clients.

The mysqld program has many options that can be specified at startup. For a complete list of options, run
this command:

mysqld --verbose --help

MySQL Server also has a set of system variables that affect its operation as it runs. System variables
can be set at server startup, and many of them can be changed at runtime to effect dynamic server
reconfiguration. MySQL Server also has a set of status variables that provide information about its
operation. You can monitor these status variables to access runtime performance characteristics.

For a full description of MySQL Server command options, system variables, and status variables, see
Section 5.1, “The MySQL Server”. For information about installing MySQL and setting up the initial
configuration, see Chapter 2, Installing and Upgrading MySQL.

4.3.2 mysqld_safe — MySQL Server Startup Script

mysqld_safe is the recommended way to start a mysqld server on Unix. mysqld_safe adds some
safety features such as restarting the server when an error occurs and logging runtime information to an
error log. A description of error logging is given later in this section.

341

mysqld_safe — MySQL Server Startup Script

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown. On
these platforms, mysqld_safe is not installed because it is unnecessary. For more
information, see Section 2.5.10, “Managing MySQL Server with systemd”.

One implication of the non-use of mysqld_safe on platforms that use systemd for
server management is that use of [mysqld_safe] or [safe_mysqld] sections in
option files is not supported and might lead to unexpected behavior.

mysqld_safe tries to start an executable named mysqld. To override the default behavior and specify
explicitly the name of the server you want to run, specify a --mysqld or --mysqld-version option to
mysqld_safe. You can also use --ledir to indicate the directory where mysqld_safe should look for
the server.

Many of the options to mysqld_safe are the same as the options to mysqld. See Section 5.1.6, “Server
Command Options”.

Options unknown to mysqld_safe are passed to mysqld if they are specified on the command line, but
ignored if they are specified in the [mysqld_safe] group of an option file. See Section 4.2.2.2, “Using
Option Files”.

mysqld_safe reads all options from the [mysqld], [server], and [mysqld_safe] sections in option
files. For example, if you specify a [mysqld] section like this, mysqld_safe finds and uses the --log-
error option:

[mysqld]
log-error=error.log

For backward compatibility, mysqld_safe also reads [safe_mysqld] sections, but to be current you
should rename such sections to [mysqld_safe].

mysqld_safe accepts options on the command line and in option files, as described in the following table.
For information about option files used by MySQL programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.6 mysqld_safe Options

Option Name

Description

Introduced

Deprecated

--basedir

--core-file-size

Path to MySQL
installation directory

Size of core file that
mysqld should be able to
create

--datadir

Path to data directory

--defaults-extra-file

--defaults-file

--help

--ledir

Read named option file in
addition to usual option
files

Read only named option
file

Display help message
and exit

Path to directory where
server is located

342

mysqld_safe — MySQL Server Startup Script

Option Name

Description

Introduced

Deprecated

--log-error

--malloc-lib

--mysqld

--mysqld-safe-log-
timestamps

--mysqld-version

--nice

--no-defaults

--open-files-limit

--pid-file

--plugin-dir

--port

--skip-kill-mysqld

--skip-syslog

--socket

--syslog

--syslog-tag

--timezone

--user

• --help

Write error log to named
file

Alternative malloc library
to use for mysqld

Name of server program
to start (in ledir directory)

Timestamp format for
logging

5.7.11

Suffix for server program
name

Use nice program to set
server scheduling priority

Read no option files

Number of files that
mysqld should be able to
open

Path name of server
process ID file

Directory where plugins
are installed

Port number on which
to listen for TCP/IP
connections

Do not try to kill stray
mysqld processes

Do not write error
messages to syslog; use
error log file

Socket file on which to
listen for Unix socket
connections

Write error messages to
syslog

Tag suffix for messages
written to syslog

Set TZ time zone
environment variable to
named value

Run mysqld as user
having name user_name
or numeric user ID
user_id

Yes

Yes

Yes

Command-Line Format

--help

343

mysqld_safe — MySQL Server Startup Script

Command-Line Format

--help

Display a help message and exit.

• --basedir=dir_name

Command-Line Format

Type

Command-Line Format

Type

The path to the MySQL installation directory.

• --core-file-size=size

--basedir=dir_name

Directory name

--basedir=dir_name

Directory name

Command-Line Format

--core-file-size=size

Type

String

Command-Line Format

--core-file-size=size

Type

String

The size of the core file that mysqld should be able to create. The option value is passed to ulimit -
c.

• --datadir=dir_name

Command-Line Format

Type

Command-Line Format

Type

The path to the data directory.

• --defaults-extra-file=file_name

--datadir=dir_name

Directory name

--datadir=dir_name

Directory name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file in addition to the usual option files. If the file does not exist or is otherwise
inaccessible, the server exits with an error. If file_name is not an absolute path name, it is interpreted
relative to the current directory. This must be the first option on the command line if it is used.

344

mysqld_safe — MySQL Server Startup Script

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, the server exits with
an error. If file_name is not an absolute path name, it is interpreted relative to the current directory.
This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --ledir=dir_name

Command-Line Format

Type

--ledir=dir_name

Directory name

If mysqld_safe cannot find the server, use this option to indicate the path name to the directory where
the server is located.

As of MySQL 5.7.17, this option is accepted only on the command line, not in option files. On platforms
that use systemd, the value can be specified in the value of MYSQLD_OPTS. See Section 2.5.10,
“Managing MySQL Server with systemd”.

• --log-error=file_name

Command-Line Format

--log-error=file_name

Type

File name

Write the error log to the given file. See Section 5.4.2, “The Error Log”.

• --mysqld-safe-log-timestamps

Command-Line Format

--mysqld-safe-log-timestamps=type

Introduced

Type

Default Value

Valid Values

5.7.11

Enumeration

utc

system

hyphen

legacy

This option controls the format for timestamps in log output produced by mysqld_safe. The following
list describes the permitted values. For any other value, mysqld_safe logs a warning and uses UTC
format.

345

mysqld_safe — MySQL Server Startup Script

• UTC, utc

ISO 8601 UTC format (same as --log_timestamps=UTC for the server). This is the default.

• SYSTEM, system

ISO 8601 local time format (same as --log_timestamps=SYSTEM for the server).

• HYPHEN, hyphen

YY-MM-DD h:mm:ss format, as in mysqld_safe for MySQL 5.6.

• LEGACY, legacy

YYMMDD hh:mm:ss format, as in mysqld_safe prior to MySQL 5.6.

This option was added in MySQL 5.7.11.

• --malloc-lib=[lib_name]

Command-Line Format

--malloc-lib=[lib-name]

Type

String

The name of the library to use for memory allocation instead of the system malloc() library. As of
MySQL 5.7.15, the option value must be one of the directories /usr/lib, /usr/lib64, /usr/lib/
i386-linux-gnu, or /usr/lib/x86_64-linux-gnu. Prior to MySQL 5.7.15, any library can be
used by specifying its path name, but there is a shortcut form to enable use of the tcmalloc library that
is shipped with binary MySQL distributions for Linux in MySQL 5.7. It is possible for the shortcut form not
to work under certain configurations, in which case you should specify a path name instead.

Note

As of MySQL 5.7.13, MySQL distributions no longer include a tcmalloc library.

The --malloc-lib option works by modifying the LD_PRELOAD environment value to affect dynamic
linking to enable the loader to find the memory-allocation library when mysqld runs:

• If the option is not given, or is given without a value (--malloc-lib=), LD_PRELOAD is not modified

and no attempt is made to use tcmalloc.

• Prior to MySQL 5.7.31, if the option is given as --malloc-lib=tcmalloc, mysqld_safe looks for
a tcmalloc library in /usr/lib and then in the MySQL pkglibdir location (for example, /usr/
local/mysql/lib or whatever is appropriate). If tmalloc is found, its path name is added to the

346

mysqld_safe — MySQL Server Startup Script

beginning of the LD_PRELOAD value for mysqld. If tcmalloc is not found, mysqld_safe aborts with
an error.

As of MySQL 5.7.31, tcmalloc is not a permitted value for the --malloc-lib option.

• If the option is given as --malloc-lib=/path/to/some/library, that full path is added to

the beginning of the LD_PRELOAD value. If the full path points to a nonexistent or unreadable file,
mysqld_safe aborts with an error.

• For cases where mysqld_safe adds a path name to LD_PRELOAD, it adds the path to the beginning

of any existing value the variable already has.

Note

On systems that manage the server using systemd, mysqld_safe is not
available. Instead, specify the allocation library by setting LD_PRELOAD in /etc/
sysconfig/mysql.

Linux users can use the libtcmalloc_minimal.so included in binary packages by adding these lines
to the my.cnf file:

[mysqld_safe]
malloc-lib=tcmalloc

Those lines also suffice for users on any platform who have installed a tcmalloc package in /usr/
lib. To use a specific tcmalloc library, specify its full path name. Example:

[mysqld_safe]
malloc-lib=/opt/lib/libtcmalloc_minimal.so

• --mysqld=prog_name

Command-Line Format

--mysqld=file_name

Type

File name

The name of the server program (in the ledir directory) that you want to start. This option is needed
if you use the MySQL binary distribution but have the data directory outside of the binary distribution. If
mysqld_safe cannot find the server, use the --ledir option to indicate the path name to the directory
where the server is located.

As of MySQL 5.7.15, this option is accepted only on the command line, not in option files. On platforms
that use systemd, the value can be specified in the value of MYSQLD_OPTS. See Section 2.5.10,
“Managing MySQL Server with systemd”.

• --mysqld-version=suffix

Command-Line Format

--mysqld-version=suffix

Type

String

This option is similar to the --mysqld option, but you specify only the suffix for the server
program name. The base name is assumed to be mysqld. For example, if you use --mysqld-

347

mysqld_safe — MySQL Server Startup Script

version=debug, mysqld_safe starts the mysqld-debug program in the ledir directory. If the
argument to --mysqld-version is empty, mysqld_safe uses mysqld in the ledir directory.

As of MySQL 5.7.15, this option is accepted only on the command line, not in option files. On platforms
that use systemd, the value can be specified in the value of MYSQLD_OPTS. See Section 2.5.10,
“Managing MySQL Server with systemd”.

• --nice=priority

Command-Line Format

Type

--nice=priority

Numeric

Use the nice program to set the server's scheduling priority to the given value.

• --no-defaults

Command-Line Format

Type

--no-defaults

String

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read. This must be the first option on the
command line if it is used.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --open-files-limit=count

Command-Line Format

--open-files-limit=count

Type

String

The number of files that mysqld should be able to open. The option value is passed to ulimit -n.

Note

You must start mysqld_safe as root for this to function properly.

• --pid-file=file_name

Command-Line Format

--pid-file=file_name

Type

File name

The path name that mysqld should use for its process ID file.

From MySQL 5.7.2 to 5.7.17, mysqld_safe has its own process ID file, which is always named
mysqld_safe.pid and located in the MySQL data directory.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

348

mysqld_safe — MySQL Server Startup Script

Type

Directory name

The path name of the plugin directory.

• --port=port_num

Command-Line Format

Type

--port=number

Numeric

The port number that the server should use when listening for TCP/IP connections. The port number
must be 1024 or higher unless the server is started by the root operating system user.

• --skip-kill-mysqld

Command-Line Format

--skip-kill-mysqld

Do not try to kill stray mysqld processes at startup. This option works only on Linux.

• --socket=path

Command-Line Format

--socket=file_name

Type

File name

The Unix socket file that the server should use when listening for local connections.

• --syslog, --skip-syslog

Command-Line Format

Deprecated

--syslog

Yes

Command-Line Format

Deprecated

--skip-syslog

Yes

--syslog causes error messages to be sent to syslog on systems that support the logger program.
--skip-syslog suppresses the use of syslog; messages are written to an error log file.

When syslog is used for error logging, the daemon.err facility/severity is used for all log messages.

Using these options to control mysqld logging is deprecated as of MySQL 5.7.5. Use the server
log_syslog system variable instead. To control the facility, use the server log_syslog_facility
system variable. See Section 5.4.2.3, “Error Logging to the System Log”.

349

• --syslog-tag=tag

Command-Line Format

--syslog-tag=tag

mysqld_safe — MySQL Server Startup Script

Deprecated

Yes

For logging to syslog, messages from mysqld_safe and mysqld are written with identifiers of
mysqld_safe and mysqld, respectively. To specify a suffix for the identifiers, use --syslog-
tag=tag, which modifies the identifiers to be mysqld_safe-tag and mysqld-tag.

Using this option to control mysqld logging is deprecated as of MySQL 5.7.5. Use the server
log_syslog_tag system variable instead. See Section 5.4.2.3, “Error Logging to the System Log”.

• --timezone=timezone

Command-Line Format

--timezone=timezone

Type

String

Set the TZ time zone environment variable to the given option value. Consult your operating system
documentation for legal time zone specification formats.

• --user={user_name|user_id}

Command-Line Format

--user={user_name|user_id}

Type

Type

String

Numeric

Run the mysqld server as the user having the name user_name or the numeric user ID user_id.
(“User” in this context refers to a system login account, not a MySQL user listed in the grant tables.)

If you execute mysqld_safe with the --defaults-file or --defaults-extra-file option to name
an option file, the option must be the first one given on the command line or the option file is not used. For
example, this command does not use the named option file:

mysql> mysqld_safe --port=port_num --defaults-file=file_name

Instead, use the following command:

mysql> mysqld_safe --defaults-file=file_name --port=port_num

The mysqld_safe script is written so that it normally can start a server that was installed from either
a source or a binary distribution of MySQL, even though these types of distributions typically install the
server in slightly different locations. (See Section 2.1.5, “Installation Layouts”.) mysqld_safe expects one
of the following conditions to be true:

• The server and databases can be found relative to the working directory (the directory from which

mysqld_safe is invoked). For binary distributions, mysqld_safe looks under its working directory
for bin and data directories. For source distributions, it looks for libexec and var directories. This
condition should be met if you execute mysqld_safe from your MySQL installation directory (for
example, /usr/local/mysql for a binary distribution).

350

• If the server and databases cannot be found relative to the working directory, mysqld_safe attempts to
locate them by absolute path names. Typical locations are /usr/local/libexec and /usr/local/
var. The actual locations are determined from the values configured into the distribution at the time it
was built. They should be correct if MySQL is installed in the location specified at configuration time.

mysql.server — MySQL Server Startup Script

Because mysqld_safe tries to find the server and databases relative to its own working directory, you
can install a binary distribution of MySQL anywhere, as long as you run mysqld_safe from the MySQL
installation directory:

cd mysql_installation_directory
bin/mysqld_safe &

If mysqld_safe fails, even when invoked from the MySQL installation directory, specify the --ledir
and --datadir options to indicate the directories in which the server and databases are located on your
system.

mysqld_safe tries to use the sleep and date system utilities to determine how many times per second
it has attempted to start. If these utilities are present and the attempted starts per second is greater than 5,
mysqld_safe waits 1 full second before starting again. This is intended to prevent excessive CPU usage
in the event of repeated failures. (Bug #11761530, Bug #54035)

When you use mysqld_safe to start mysqld, mysqld_safe arranges for error (and notice) messages
from itself and from mysqld to go to the same destination.

There are several mysqld_safe options for controlling the destination of these messages:

• --log-error=file_name: Write error messages to the named error file.

• --syslog: Write error messages to syslog on systems that support the logger program.

• --skip-syslog: Do not write error messages to syslog. Messages are written to the default error log

file (host_name.err in the data directory), or to a named file if the --log-error option is given.

If none of these options is given, the default is --skip-syslog.

When mysqld_safe writes a message, notices go to the logging destination (syslog or the error log file)
and stdout. Errors go to the logging destination and stderr.

Note

Controlling mysqld logging from mysqld_safe is deprecated as of MySQL
5.7.5. Use the server's native syslog support instead. For more information, see
Section 5.4.2.3, “Error Logging to the System Log”.

4.3.3 mysql.server — MySQL Server Startup Script

MySQL distributions on Unix and Unix-like system include a script named mysql.server, which starts
the MySQL server using mysqld_safe. It can be used on systems such as Linux and Solaris that use
System V-style run directories to start and stop system services. It is also used by the macOS Startup Item
for MySQL.

mysql.server is the script name as used within the MySQL source tree. The installed name might be
different (for example, mysqld or mysql). In the following discussion, adjust the name mysql.server as
appropriate for your system.

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown. On
these platforms, mysql.server and mysqld_safe are not installed because they

351

mysql.server — MySQL Server Startup Script

are unnecessary. For more information, see Section 2.5.10, “Managing MySQL
Server with systemd”.

To start or stop the server manually using the mysql.server script, invoke it from the command line with
start or stop arguments:

mysql.server start
mysql.server stop

mysql.server changes location to the MySQL installation directory, then invokes mysqld_safe. To run
the server as some specific user, add an appropriate user option to the [mysqld] group of the global /
etc/my.cnf option file, as shown later in this section. (It is possible that you must edit mysql.server if
you've installed a binary distribution of MySQL in a nonstandard location. Modify it to change location into
the proper directory before it runs mysqld_safe. If you do this, your modified version of mysql.server
may be overwritten if you upgrade MySQL in the future; make a copy of your edited version that you can
reinstall.)

mysql.server stop stops the server by sending a signal to it. You can also stop the server manually by
executing mysqladmin shutdown.

To start and stop MySQL automatically on your server, you must add start and stop commands to the
appropriate places in your /etc/rc* files:

• If you use the Linux server RPM package (MySQL-server-VERSION.rpm), or a native Linux package
installation, the mysql.server script may be installed in the /etc/init.d directory with the name
mysqld or mysql. See Section 2.5.5, “Installing MySQL on Linux Using RPM Packages from Oracle”,
for more information on the Linux RPM packages.

• If you install MySQL from a source distribution or using a binary distribution format that does not install
mysql.server automatically, you can install the script manually. It can be found in the support-
files directory under the MySQL installation directory or in a MySQL source tree. Copy the script to the
/etc/init.d directory with the name mysql and make it executable:

cp mysql.server /etc/init.d/mysql
chmod +x /etc/init.d/mysql

After installing the script, the commands needed to activate it to run at system startup depend on your
operating system. On Linux, you can use chkconfig:

chkconfig --add mysql

On some Linux systems, the following command also seems to be necessary to fully enable the mysql
script:

chkconfig --level 345 mysql on

• On FreeBSD, startup scripts generally should go in /usr/local/etc/rc.d/. Install the

mysql.server script as /usr/local/etc/rc.d/mysql.server.sh to enable automatic startup.
The rc(8) manual page states that scripts in this directory are executed only if their base name
matches the *.sh shell file name pattern. Any other files or directories present within the directory are
silently ignored.

• As an alternative to the preceding setup, some operating systems also use /etc/rc.local or /etc/
init.d/boot.local to start additional services on startup. To start up MySQL using this method,
append a command like the one following to the appropriate startup file:

/bin/sh -c 'cd /usr/local/mysql; ./bin/mysqld_safe --user=mysql &'

• For other systems, consult your operating system documentation to see how to install startup scripts.

352

mysqld_multi — Manage Multiple MySQL Servers

mysql.server reads options from the [mysql.server] and [mysqld] sections of option files. For
backward compatibility, it also reads [mysql_server] sections, but to be current you should rename
such sections to [mysql.server].

You can add options for mysql.server in a global /etc/my.cnf file. A typical my.cnf file might look
like this:

[mysqld]
datadir=/usr/local/mysql/var
socket=/var/tmp/mysql.sock
port=3306
user=mysql

[mysql.server]
basedir=/usr/local/mysql

The mysql.server script supports the options shown in the following table. If specified, they must be
placed in an option file, not on the command line. mysql.server supports only start and stop as
command-line arguments.

Table 4.7 mysql.server Option-File Options

Option Name

basedir

datadir

pid-file

Description

Path to MySQL installation
directory

Type

Directory name

Path to MySQL data directory

Directory name

File in which server should write
its process ID

File name

service-startup-timeout

How long to wait for server startup Integer

• basedir=dir_name

The path to the MySQL installation directory.

• datadir=dir_name

The path to the MySQL data directory.

• pid-file=file_name

The path name of the file in which the server should write its process ID. The server creates the file in
the data directory unless an absolute path name is given to specify a different directory.

If this option is not given, mysql.server uses a default value of host_name.pid. The PID file value
passed to mysqld_safe overrides any value specified in the [mysqld_safe] option file group.
Because mysql.server reads the [mysqld] option file group but not the [mysqld_safe] group,
you can ensure that mysqld_safe gets the same value when invoked from mysql.server as when
invoked manually by putting the same pid-file setting in both the [mysqld_safe] and [mysqld]
groups.

• service-startup-timeout=seconds

How long in seconds to wait for confirmation of server startup. If the server does not start within this time,
mysql.server exits with an error. The default value is 900. A value of 0 means not to wait at all for
startup. Negative values mean to wait forever (no timeout).

4.3.4 mysqld_multi — Manage Multiple MySQL Servers

353

mysqld_multi — Manage Multiple MySQL Servers

mysqld_multi is designed to manage several mysqld processes that listen for connections on different
Unix socket files and TCP/IP ports. It can start or stop servers, or report their current status.

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown.
On these platforms, mysqld_multi is not installed because it is unnecessary.
For information about using systemd to handle multiple MySQL instances, see
Section 2.5.10, “Managing MySQL Server with systemd”.

mysqld_multi searches for groups named [mysqldN] in my.cnf (or in the file named by the --
defaults-file option). N can be any positive integer. This number is referred to in the following
discussion as the option group number, or GNR. Group numbers distinguish option groups from one
another and are used as arguments to mysqld_multi to specify which servers you want to start,
stop, or obtain a status report for. Options listed in these groups are the same that you would use in the
[mysqld] group used for starting mysqld. (See, for example, Section 2.9.5, “Starting and Stopping
MySQL Automatically”.) However, when using multiple servers, it is necessary that each one use its own
value for options such as the Unix socket file and TCP/IP port number. For more information on which
options must be unique per server in a multiple-server environment, see Section 5.7, “Running Multiple
MySQL Instances on One Machine”.

To invoke mysqld_multi, use the following syntax:

mysqld_multi [options] {start|stop|reload|report} [GNR[,GNR] ...]

start, stop, reload (stop and restart), and report indicate which operation to perform. You can
perform the designated operation for a single server or multiple servers, depending on the GNR list that
follows the option name. If there is no list, mysqld_multi performs the operation for all servers in the
option file.

Each GNR value represents an option group number or range of group numbers. The value should be
the number at the end of the group name in the option file. For example, the GNR for a group named
[mysqld17] is 17. To specify a range of numbers, separate the first and last numbers by a dash. The
GNR value 10-13 represents groups [mysqld10] through [mysqld13]. Multiple groups or group ranges
can be specified on the command line, separated by commas. There must be no whitespace characters
(spaces or tabs) in the GNR list; anything after a whitespace character is ignored.

This command starts a single server using option group [mysqld17]:

mysqld_multi start 17

This command stops several servers, using option groups [mysqld8] and [mysqld10] through
[mysqld13]:

mysqld_multi stop 8,10-13

For an example of how you might set up an option file, use this command:

mysqld_multi --example

mysqld_multi searches for option files as follows:

• With --no-defaults, no option files are read.

Command-Line Format

--no-defaults

Type

Default Value

Boolean

false

354

mysqld_multi — Manage Multiple MySQL Servers

• With --defaults-file=file_name, only the named file is read.

Command-Line Format

--defaults-file=filename

Type

Default Value

File name

[none]

• Otherwise, option files in the standard list of locations are read, including any file named by the --

defaults-extra-file=file_name option, if one is given. (If the option is given multiple times, the
last value is used.)

Command-Line Format

--defaults-extra-file=filename

Type

Default Value

File name

[none]

For additional information about these and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

Option files read are searched for [mysqld_multi] and [mysqldN] option groups. The
[mysqld_multi] group can be used for options to mysqld_multi itself. [mysqldN] groups can be
used for options passed to specific mysqld instances.

The [mysqld] or [mysqld_safe] groups can be used for common options read by all instances of
mysqld or mysqld_safe. You can specify a --defaults-file=file_name option to use a different
configuration file for that instance, in which case the [mysqld] or [mysqld_safe] groups from that file
are used for that instance.

mysqld_multi supports the following options.

• --help

Command-Line Format

Type

Default Value

Display a help message and exit.

• --example

Command-Line Format

Type

Default Value

Display a sample option file.

• --log=file_name

--help

Boolean

false

--example

Boolean

false

Command-Line Format

--log=path

355

mysqld_multi — Manage Multiple MySQL Servers

Type

Default Value

File name

/var/log/mysqld_multi.log

Specify the name of the log file. If the file exists, log output is appended to it.

• --mysqladmin=prog_name

Command-Line Format

--mysqladmin=file

Type

Default Value

File name

[none]

The mysqladmin binary to be used to stop servers.

• --mysqld=prog_name

Command-Line Format

--mysqld=file

Type

Default Value

File name

[none]

The mysqld binary to be used. Note that you can specify mysqld_safe as the value for this option
also. If you use mysqld_safe to start the server, you can include the mysqld or ledir options
in the corresponding [mysqldN] option group. These options indicate the name of the server that
mysqld_safe should start and the path name of the directory where the server is located. (See
the descriptions for these options in Section 4.3.2, “mysqld_safe — MySQL Server Startup Script”.)
Example:

[mysqld38]
mysqld = mysqld-debug
ledir  = /opt/local/mysql/libexec

• --no-log

Command-Line Format

Type

Default Value

--no-log

Boolean

false

Print log information to stdout rather than to the log file. By default, output goes to the log file.

• --password=password

Command-Line Format

--password=string

Type

Default Value

String

[none]

The password of the MySQL account to use when invoking mysqladmin. Note that the password value
is not optional for this option, unlike for other MySQL programs.

• --silent

356

mysqld_multi — Manage Multiple MySQL Servers

Command-Line Format

Type

Default Value

Silent mode; disable warnings.

• --tcp-ip

Command-Line Format

Type

Default Value

--silent

Boolean

false

--tcp-ip

Boolean

false

Connect to each MySQL server through the TCP/IP port instead of the Unix socket file. (If a socket file
is missing, the server might still be running, but accessible only through the TCP/IP port.) By default,
connections are made using the Unix socket file. This option affects stop and report operations.

• --user=user_name

Command-Line Format

--user=name

Type

Default Value

String

root

The user name of the MySQL account to use when invoking mysqladmin.

• --verbose

Command-Line Format

Type

Default Value

Be more verbose.

• --version

Command-Line Format

Type

Default Value

Display version information and exit.

Some notes about mysqld_multi:

--verbose

Boolean

false

--version

Boolean

false

• Most important: Before using mysqld_multi be sure that you understand the meanings of the options
that are passed to the mysqld servers and why you would want to have separate mysqld processes.
Beware of the dangers of using multiple mysqld servers with the same data directory. Use separate
data directories, unless you know what you are doing. Starting multiple servers with the same data

357

mysqld_multi — Manage Multiple MySQL Servers

directory does not give you extra performance in a threaded system. See Section 5.7, “Running Multiple
MySQL Instances on One Machine”.

Important

Make sure that the data directory for each server is fully accessible to the Unix
account that the specific mysqld process is started as. Do not use the Unix root
account for this, unless you know what you are doing. See Section 6.1.5, “How to
Run MySQL as a Normal User”.

• Make sure that the MySQL account used for stopping the mysqld servers (with the mysqladmin

program) has the same user name and password for each server. Also, make sure that the account
has the SHUTDOWN privilege. If the servers that you want to manage have different user names or
passwords for the administrative accounts, you might want to create an account on each server that has
the same user name and password. For example, you might set up a common multi_admin account
by executing the following commands for each server:

$> mysql -u root -S /tmp/mysql.sock -p
Enter password:
mysql> CREATE USER 'multi_admin'@'localhost' IDENTIFIED BY 'multipass';
mysql> GRANT SHUTDOWN ON *.* TO 'multi_admin'@'localhost';

See Section 6.2, “Access Control and Account Management”. You have to do this for each mysqld
server. Change the connection parameters appropriately when connecting to each one. Note that the
host name part of the account name must permit you to connect as multi_admin from the host where
you want to run mysqld_multi.

• The Unix socket file and the TCP/IP port number must be different for every mysqld. (Alternatively, if the
host has multiple network addresses, you can set the bind_address system variable to cause different
servers to listen to different interfaces.)

• The --pid-file option is very important if you are using mysqld_safe to start mysqld (for example,
--mysqld=mysqld_safe) Every mysqld should have its own process ID file. The advantage of using
mysqld_safe instead of mysqld is that mysqld_safe monitors its mysqld process and restarts it if
the process terminates due to a signal sent using kill -9 or for other reasons, such as a segmentation
fault.

• You might want to use the --user option for mysqld, but to do this you need to run the

mysqld_multi script as the Unix superuser (root). Having the option in the option file does not matter;
you just get a warning if you are not the superuser and the mysqld processes are started under your
own Unix account.

The following example shows how you might set up an option file for use with mysqld_multi. The order
in which the mysqld programs are started or stopped depends on the order in which they appear in the
option file. Group numbers need not form an unbroken sequence. The first and fifth [mysqldN] groups
were intentionally omitted from the example to illustrate that you can have “gaps” in the option file. This
gives you more flexibility.

# This is an example of a my.cnf file for mysqld_multi.
# Usually this file is located in home dir ~/.my.cnf or /etc/my.cnf

[mysqld_multi]
mysqld     = /usr/local/mysql/bin/mysqld_safe
mysqladmin = /usr/local/mysql/bin/mysqladmin
user       = multi_admin
password   = my_password

[mysqld2]
socket     = /tmp/mysql.sock2

358

Installation-Related Programs

port       = 3307
pid-file   = /usr/local/mysql/data2/hostname.pid2
datadir    = /usr/local/mysql/data2
language   = /usr/local/mysql/share/mysql/english
user       = unix_user1

[mysqld3]
mysqld     = /path/to/mysqld_safe
ledir      = /path/to/mysqld-binary/
mysqladmin = /path/to/mysqladmin
socket     = /tmp/mysql.sock3
port       = 3308
pid-file   = /usr/local/mysql/data3/hostname.pid3
datadir    = /usr/local/mysql/data3
language   = /usr/local/mysql/share/mysql/swedish
user       = unix_user2

[mysqld4]
socket     = /tmp/mysql.sock4
port       = 3309
pid-file   = /usr/local/mysql/data4/hostname.pid4
datadir    = /usr/local/mysql/data4
language   = /usr/local/mysql/share/mysql/estonia
user       = unix_user3

[mysqld6]
socket     = /tmp/mysql.sock6
port       = 3311
pid-file   = /usr/local/mysql/data6/hostname.pid6
datadir    = /usr/local/mysql/data6
language   = /usr/local/mysql/share/mysql/japanese
user       = unix_user4

See Section 4.2.2.2, “Using Option Files”.

4.4 Installation-Related Programs

The programs in this section are used when installing or upgrading MySQL.

4.4.1 comp_err — Compile MySQL Error Message File

comp_err creates the errmsg.sys file that is used by mysqld to determine the error messages to
display for different error codes. comp_err normally is run automatically when MySQL is built. It compiles
the errmsg.sys file from the text-format error information file located at sql/share/errmsg-utf8.txt
in MySQL source distributions.

comp_err also generates the mysqld_error.h, mysqld_ername.h, and sql_state.h header files.

For more information about how error messages are defined, see the MySQL Internals Manual.

Invoke comp_err like this:

comp_err [options]

comp_err supports the following options.

• --help, -?

Command-Line Format

Type

Default Value

--help

Boolean

false

359

comp_err — Compile MySQL Error Message File

Display a help message and exit.

• --charset=dir_name, -C dir_name

Command-Line Format

Type

Default Value

--charset

String

../share/charsets

The character set directory. The default is ../sql/share/charsets.

• --debug=debug_options, -# debug_options

Command-Line Format

Type

Default Value

--debug=options

String

d:t:O,/tmp/comp_err.trace

In debug builds, write a debugging log. A typical debug_options string is d:t:O,file_name. The
default is d:t:O,/tmp/comp_err.trace.

For non-debug builds, this option is non-functional and causes the program to exit with an explanatory
message.

Note

The short form of this option is -#, using a literal # character.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

false

Print some debugging information when the program exits.

• --header-file=file_name, -H file_name

Command-Line Format

--header-file=name

Type

Default Value

File name

mysqld_error.h

The name of the error header file. The default is mysqld_error.h.

• --in-file=file_name, -F file_name

Command-Line Format

--in-file=path

Type

Default Value

File name

[none]

360

mysql_install_db — Initialize MySQL Data Directory

The name of the input file that defines error messages. The default is ../sql/share/errmsg-
utf8.txt.

• --name-file=file_name, -N file_name

Command-Line Format

Type

Default Value

--name-file=name

File name

mysqld_ername.h

The name of the error name file. The default is mysqld_ername.h.

• --out-dir=dir_name, -D dir_name

Command-Line Format

--out-dir=path

Type

Default Value

String

../share/

The name of the output base directory. The default is ../sql/share/.

• --out-file=file_name, -O file_name

Command-Line Format

--out-file=name

Type

Default Value

File name

errmsg.sys

The name of the output file. The default is errmsg.sys.

• --state-file=file_name, -S file_name

Command-Line Format

--state-file=name

Type

Default Value

File name

sql_state.h

The name for the SQLSTATE header file. The default is sql_state.h.

• --version, -V

Command-Line Format

Type

Default Value

--version

Boolean

false

361

Display version information and exit.

4.4.2 mysql_install_db — Initialize MySQL Data Directory

mysql_install_db — Initialize MySQL Data Directory

Note

mysql_install_db is deprecated as of MySQL 5.7.6 because its functionality
has been integrated into mysqld, the MySQL server. To initialize a MySQL
installation, invoke mysqld with the --initialize or --initialize-
insecure option. For more information, see Section 2.9.1, “Initializing the Data
Directory”. You should expect mysql_install_db to be removed in a future
MySQL release.

mysql_install_db handles initialization tasks that must be performed before the MySQL server,
mysqld, is ready to use:

• It initializes the MySQL data directory and creates the system tables that it contains.

• It initializes the system tablespace and related data structures needed to manage InnoDB tables.

• It loads the server-side help tables.

• It installs the sys schema.

• It creates an administrative account. Older versions of mysql_install_db may create anonymous-

user accounts.

Secure-by-Default Deployment

Current versions of mysql_install_db produce a MySQL deployment that is secure by default, with
these characteristics:

• A single administrative account named 'root'@'localhost' is created with a randomly generated

password, which is marked expired.

• No anonymous-user accounts are created.

• No test database accessible by all users is created.

• --admin-xxx options are available to control characteristics of the administrative account.

• The --random-password-file option is available to control where the random password is written.

• The --insecure option is available to suppress random password generation.

 If mysql_install_db generates a random administative password, it writes the password to a file
and displays the file name. The password entry includes a timestamp to indicate when it was written.
By default, the file is .mysql_secret in the home directory of the effective user running the script.
.mysql_secret is created with mode 600 to be accessible only to the operating system user for whom it
is created.

Important

When mysql_install_db generates a random password for the administrative
account, it is necessary after mysql_install_db has been run to start the
server, connect using the administrative account with the password written to the
.mysql_secret file, and specify a new administrative password. Until this is
done, the administrative account cannot be used for anything else. To change the
password, you can use the SET PASSWORD statement (for example, with the mysql
or mysqladmin client). After resetting the password, remove the .mysql_secret
file; otherwise, if you run mysql_secure_installation, that command may see
the file and expire the root password again as part of ensuring secure deployment.

362

mysql_install_db — Initialize MySQL Data Directory

Invocation Syntax

Change location to the MySQL installation directory and use this invocation syntax:

bin/mysql_install_db --datadir=path/to/datadir [other_options]

The --datadir option is mandatory. mysql_install_db creates the data directory, which must not
already exist:

• If the data directory does already exist, you are performing an upgrade operation (not an install
operation) and should run mysql_upgrade, not mysql_install_db. See Section 4.4.7,
“mysql_upgrade — Check and Upgrade MySQL Tables”.

• If the data directory does not exist but mysql_install_db fails, you must remove any partially created

data directory before running mysql_install_db again.

Because the MySQL server, mysqld, must access the data directory when it runs later, you should either
run mysql_install_db from the same system account used for running mysqld, or run it as root and
specify the --user option to indicate the user name that mysqld runs under. It might be necessary to
specify other options such as --basedir if mysql_install_db does not use the correct location for the
installation directory. For example:

bin/mysql_install_db --user=mysql \
    --basedir=/opt/mysql/mysql \
    --datadir=/opt/mysql/mysql/data

Note

After mysql_install_db sets up the InnoDB system tablespace, changes to
some tablespace characteristics require setting up a whole new instance. This
includes the file name of the first file in the system tablespace and the number
of undo logs. If you do not want to use the default values, make sure that the
settings for the innodb_data_file_path and innodb_log_file_size
configuration parameters are in place in the MySQL configuration file before
running mysql_install_db. Also make sure to specify as necessary other
parameters that affect the creation and location of InnoDB files, such as
innodb_data_home_dir and innodb_log_group_home_dir.

If those options are in your configuration file but that file is not in a location that
MySQL reads by default, specify the file location using the --defaults-extra-
file option when you run mysql_install_db.

Note

If you have set a custom TMPDIR environment variable when performing the
installation, and the specified directory is not accessible, mysql_install_db may
fail. If so, unset TMPDIR or set TMPDIR to point to the system temporary directory
(usually /tmp).

Administrative Account Creation

mysql_install_db creates an administrative account named 'root'@'localhost' by default.

mysql_install_db provides options that enable you to control several aspects of the administrative
account:

• To change the user or host parts of the account name, use --login-path, or --admin-user and --

admin-host.

363

mysql_install_db — Initialize MySQL Data Directory

• --insecure suppresses generation of a random password.

• --admin-auth-plugin specifies the authentication plugin.

• --admin-require-ssl specifies whether the account must use SSL connections.

For more information, see the descriptions of those options.

mysql_install_db assigns mysql.user system table rows a nonempty plugin column value to set
the authentication plugin. The default value is mysql_native_password. The value can be changed
using the --admin-auth-plugin option.

Default my.cnf File

mysql_install_db creates no default my.cnf file.

Note

As of MySQL 5.7.18, my-default.cnf is no longer included in or installed by
distribution packages.

With one exception, the settings in the default option file are commented and have
no effect. The exception is that the file sets the sql_mode system variable to
NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES. This setting produces a server configuration
that results in errors rather than warnings for bad data in operations that modify transactional tables. See
Section 5.1.10, “Server SQL Modes”.

Command Options

mysql_install_db supports the following options, which can be specified on the command line or in
the [mysql_install_db] group of an option file. For information about option files used by MySQL
programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.8 mysql_install_db Options

Option Name

--admin-auth-plugin

--admin-host

--admin-require-ssl

--admin-user

--basedir

--builddir

--datadir

--defaults

--defaults-extra-file

--defaults-file

--extra-sql-file

--help

--insecure

--lc-messages

364

Description

Administrative account authentication plugin

Administrative account name host part

Require SSL for administrative account

Administrative account name user part

Path to base directory

Path to build directory (for out-of-source builds)

Path to data directory

Read default option files

Read named option file in addition to usual option
files

Read only named option file

Optional SQL file to execute during bootstrap

Display help message and exit

Do not generate administrative account random
password

Locale for error messages

mysql_install_db — Initialize MySQL Data Directory

Option Name

--lc-messages-dir

--login-file

--login-path

--mysqld-file

--no-defaults

--random-password-file

Description

Directory where error messages are installed

File to read for login path information

Read login path options from .mylogin.cnf

Path to mysqld binary

Read no option files

File in which to write administrative account random
password

--skip-sys-schema

Do not install or upgrade the sys schema

--srcdir

--user

--verbose

--version

• --help, -?

For internal use

Operating system user under which to execute
mysqld

Verbose mode

Display version information and exit

Command-Line Format

--help

Display a help message and exit.

• --admin-auth-plugin=plugin_name

Command-Line Format

--admin-auth-plugin=plugin_name

Type

String

The authentication plugin to use for the administrative account. The default is
mysql_native_password.

• --admin-host=host_name

Command-Line Format

--admin-host=host_name

Type

String

The host part to use for the adminstrative account name. The default is localhost. This option is
ignored if --login-path is also specified.

• --admin-require-ssl

Command-Line Format

--admin-require-ssl

Type

Default Value

Boolean

FALSE

365

Whether to require SSL for the administrative account. The default is not to require it. With this option
enabled, the statement that mysql_install_db uses to create the account includes a REQUIRE SSL

mysql_install_db — Initialize MySQL Data Directory

clause. As a result, the administrative account must use secure connections when connecting to the
server.

• --admin-user=user_name

Command-Line Format

--admin-user=user_name

Type

String

The user part to use for the adminstrative account name. The default is root. This option is ignored if --
login-path is also specified.

• --basedir=dir_name

Command-Line Format

Type

--basedir=dir_name

Directory name

The path to the MySQL installation directory.

• --builddir=dir_name

Command-Line Format

Type

--builddir=dir_name

Directory name

For use with --srcdir and out-of-source builds. Set this to the location of the directory where the built
files reside.

• --datadir=dir_name

Command-Line Format

Type

--datadir=dir_name

Directory name

The path to the MySQL data directory. Only the last component of the path name is created if it does not
exist; the parent directory must already exist or an error occurs.

Note

The --datadir option is mandatory and the data directory must not already
exist.

• --defaults

Command-Line Format

Type

366

Default Value

--defaults

Boolean

FALSE

This option causes mysql_install_db to invoke mysqld in such a way that it reads option files from

the default locations. If given as --no-defaults, and --defaults-file or --defaults-extra-

file is not also specified, mysql_install_db passes --no-defaults to mysqld, to prevent option

mysql_install_db — Initialize MySQL Data Directory

files from being read. This may help if program startup fails due to reading unknown options from an
option file.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

This option is passed by mysql_install_db to mysqld.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

This option is passed by mysql_install_db to mysqld.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --extra-sql-file=file_name, -f file_name

Command-Line Format

--extra-sql-file=file_name

Type

File name

This option names a file containing additional SQL statements to be executed after the standard
bootstrapping statements. Accepted statement syntax in the file is like that of the mysql command-line
client, including support for multiple-line C-style comments and delimiter handling to enable definition of
stored programs.

• --insecure

Command-Line Format

Type

Default Value

--insecure

Boolean

FALSE

Do not generate a random password for the adminstrative account.

If --insecure is not given, it is necessary after mysql_install_db has been run to start the server,

connect using the administrative account with the password written to the .mysql_secret file, and

367

mysql_install_db — Initialize MySQL Data Directory

specify a new administrative password. Until this is done, the administrative account cannot be used
for anything else. To change the password, you can use the SET PASSWORD statement (for example,
with the mysql or mysqladmin client). After resetting the password, remove the .mysql_secret file;
otherwise, if you run mysql_secure_installation, that command may see the file and expire the
root password again as part of ensuring secure deployment.

• --lc-messages=name

Command-Line Format

--lc-messages=name

Type

Default Value

String

en_US

The locale to use for error messages. The default is en_US. The argument is converted to a language
name and combined with the value of --lc-messages-dir to produce the location for the error
message file. See Section 10.12, “Setting the Error Message Language”.

• --lc-messages-dir=dir_name

Command-Line Format

--lc-messages-dir=dir_name

Type

Directory name

The directory where error messages are located. The value is used together with the value of --lc-
messages to produce the location for the error message file. See Section 10.12, “Setting the Error
Message Language”.

• --login-file=file_name

Command-Line Format

--login-file=file_name

Type

File name

The file from which to read the login path if the --login-path=file_name option is specified. The
default file is .mylogin.cnf.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. The default login
path is client. (To read a different file, use the --login-file=name option.) A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

368

If the --login-path option is specified, the user, host, and password values are taken from the login
path and used to create the administrative account. The password must be defined in the login path or

mysql_install_db — Initialize MySQL Data Directory

an error occurs, unless the --insecure option is also specified. In addition, with --login-path, any
--admin-host and --admin-user options are ignored.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --mysqld-file=file_name

Command-Line Format

--mysqld-file=file_name

Type

File name

The path name of the mysqld binary to execute. The option value must be an absolute path name or an
error occurs.

If this option is not given, mysql_install_db searches for mysqld in these locations:

• In the bin directory under the --basedir option value, if that option was given.

• In the bin directory under the --srcdir option value, if that option was given.

• In the bin directory under the --builddir option value, if that option was given.

• In the local directory and in the bin and sbin directories under the local directory.

• In /usr/bin, /usr/sbin, /usr/local/bin, /usr/local/sbin, /opt/local/bin, /opt/

local/sbin.

• --no-defaults

Command-Line Format

--no-defaults

For behavior of this option, see the description of --defaults.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --random-password-file=file_name

Command-Line Format

--random-password-file=file_name

Type

File name

The path name of the file in which to write the randomly generated password for the administrative
account. The option value must be an absolute path name or an error occurs. The default is
$HOME/.mysql_secret.

• --skip-sys-schema

Command-Line Format

Type

--skip-sys-schema

Boolean

369

mysql_plugin — Configure MySQL Server Plugins

Default Value

FALSE

mysql_install_db installs the sys schema. The --skip-sys-schema option suppresses this
behavior.

• --srcdir=dir_name

Command-Line Format

Type

--srcdir=dir_name

Directory name

For internal use. This option specifies the directory under which mysql_install_db looks for support
files such as the error message file and the file for populating the help tables.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

The system (login) user name to use for running mysqld. Files and directories created by mysqld are
owned by this user. You must be the system root user to use this option. By default, mysqld runs
using your current login name; files and directories that it creates are owned by you.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. You can use this option to see the
mysqld command that mysql_install_db invokes to start the server in bootstrap mode.

• --version, -V

Command-Line Format

--version

Display version information and exit.

4.4.3 mysql_plugin — Configure MySQL Server Plugins

Note

mysql_plugin is deprecated as of MySQL 5.7.11 and removed in MySQL 8.0.
Alternatives include loading plugins at server startup using the --plugin-load
or --plugin-load-add option, or at runtime using the INSTALL PLUGIN
statement.

The mysql_plugin utility enables MySQL administrators to manage which plugins a MySQL server
loads. It provides an alternative to manually specifying the --plugin-load option at server startup or
using the INSTALL PLUGIN and UNINSTALL PLUGIN statements at runtime.

Depending on whether mysql_plugin is invoked to enable or disable plugins, it inserts or deletes rows
in the mysql.plugin table that serves as a plugin registry. (To perform this operation, mysql_plugin
invokes the MySQL server in bootstrap mode. This means that the server must not already be running.)

370

mysql_plugin — Configure MySQL Server Plugins

For normal server startups, the server loads and enables plugins listed in mysql.plugin automatically.
For additional control over plugin activation, use --plugin_name options named for specific plugins, as
described in Section 5.5.1, “Installing and Uninstalling Plugins”.

Each invocation of mysql_plugin reads a configuration file to determine how to configure the plugins
contained in a single plugin library file. To invoke mysql_plugin, use this syntax:

mysql_plugin [options] plugin {ENABLE|DISABLE}

plugin is the name of the plugin to configure. ENABLE or DISABLE (not case-sensitive) specify whether to
enable or disable components of the plugin library named in the configuration file. The order of the plugin
and ENABLE or DISABLE arguments does not matter.

For example, to configure components of a plugin library file named myplugins.so on Linux or
myplugins.dll on Windows, specify a plugin value of myplugins. Suppose that this plugin library
contains three plugins, plugin1, plugin2, and plugin3, all of which should be configured under
mysql_plugin control. By convention, configuration files have a suffix of .ini and the same base name
as the plugin library, so the default configuration file name for this plugin library is myplugins.ini. The
configuration file contents look like this:

myplugins
plugin1
plugin2
plugin3

The first line in the myplugins.ini file is the name of the library file, without any extension such as .so
or .dll. The remaining lines are the names of the components to be enabled or disabled. Each value in
the file should be on a separate line. Lines on which the first character is '#' are taken as comments and
ignored.

To enable the plugins listed in the configuration file, invoke mysql_plugin this way:

mysql_plugin myplugins ENABLE

To disable the plugins, use DISABLE rather than ENABLE.

An error occurs if mysql_plugin cannot find the configuration file or plugin library file, or if
mysql_plugin cannot start the MySQL server.

mysql_plugin supports the following options, which can be specified on the command line or in
the [mysqld] group of any option file. For options specified in a [mysqld] group, mysql_plugin
recognizes the --basedir, --datadir, and --plugin-dir options and ignores others. For information
about option files used by MySQL programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.9 mysql_plugin Options

Option Name

--basedir

--datadir

--help

--my-print-defaults

--mysqld

--no-defaults

Description

The server base directory

The server data directory

Display help message and exit

Path to my_print_defaults

Path to server

Do not read configuration file

371

mysql_plugin — Configure MySQL Server Plugins

Description

Directory where plugins are installed

The plugin configuration file

Show configuration file defaults

Verbose mode

Display version information and exit

Option Name

--plugin-dir

--plugin-ini

--print-defaults

--verbose

--version

• --help, -?

Command-Line Format

--help

Display a help message and exit.

• --basedir=dir_name, -b dir_name

Command-Line Format

Type

The server base directory.

• --datadir=dir_name, -d dir_name

Command-Line Format

Type

The server data directory.

--basedir=dir_name

Directory name

--datadir=dir_name

Directory name

• --my-print-defaults=file_name, -b file_name

Command-Line Format

--my-print-defaults=file_name

Type

File name

The path to the my_print_defaults program.

• --mysqld=file_name, -b file_name

Command-Line Format

--mysqld=file_name

Type

File name

The path to the mysqld server.

• --no-defaults, -p

Command-Line Format

--no-defaults

Do not read values from the configuration file. This option enables an administrator to skip reading
defaults from the configuration file.

372

mysql_secure_installation — Improve MySQL Installation Security

With mysql_plugin, this option need not be given first on the command line, unlike most other MySQL
programs that support --no-defaults.

• --plugin-dir=dir_name, -p dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The server plugin directory.

• --plugin-ini=file_name, -i file_name

Command-Line Format

--plugin-ini=file_name

Type

File name

The mysql_plugin configuration file. Relative path names are interpreted relative to the current
directory. If this option is not given, the default is plugin.ini in the plugin directory, where plugin is
the plugin argument on the command line.

• --print-defaults, -P

Command-Line Format

--print-defaults

Display the default values from the configuration file. This option causes mysql_plugin to print the
defaults for --basedir, --datadir, and --plugin-dir if they are found in the configuration file. If
no value for a variable is found, nothing is shown.

With mysql_plugin, this option need not be given first on the command line, unlike most other MySQL
programs that support --print-defaults.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This option can be used multiple
times to increase the amount of information.

• --version, -V

Command-Line Format

--version

Display version information and exit.

4.4.4 mysql_secure_installation — Improve MySQL Installation Security

This program enables you to improve the security of your MySQL installation in the following ways:

• You can set a password for root accounts.

• You can remove root accounts that are accessible from outside the local host.

373

mysql_secure_installation — Improve MySQL Installation Security

• You can remove anonymous-user accounts.

• You can remove the test database (which by default can be accessed by all users, even anonymous

users), and privileges that permit anyone to access databases with names that start with test_.

mysql_secure_installation helps you implement security recommendations similar to those
described at Section 2.9.4, “Securing the Initial MySQL Account”.

Normal usage is to connect to the local MySQL server; invoke mysql_secure_installation without
arguments:

mysql_secure_installation

When executed, mysql_secure_installation prompts you to determine which actions to perform.

The validate_password plugin can be used for password strength checking. If the plugin is not
installed, mysql_secure_installation prompts the user whether to install it. Any passwords entered
later are checked using the plugin if it is enabled.

Most of the usual MySQL client options such as --host and --port can be used on the command
line and in option files. For example, to connect to the local server over IPv6 using port 3307, use this
command:

mysql_secure_installation --host=::1 --port=3307

mysql_secure_installation supports the following options, which can be specified on the command
line or in the [mysql_secure_installation] and [client] groups of an option file. For information
about option files used by MySQL programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.10 mysql_secure_installation Options

Option Name

--defaults-extra-file

Description

Introduced

Read named option file in addition
to usual option files

--defaults-file

Read only named option file

--defaults-group-suffix

Option group suffix value

--help

--host

--no-defaults

--password

--port

--print-defaults

--protocol

--socket

374

Display help message and exit

Host on which MySQL server is
located

Read no option files

Accepted but always
ignored. Whenever
mysql_secure_installation is
invoked, the user is prompted for
a password, regardless

TCP/IP port number for
connection

Print default options

Transport protocol to use

Unix socket file or Windows
named pipe to use

mysql_secure_installation — Improve MySQL Installation Security

Option Name

Description

Introduced

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--tls-version

--use-default

--user

• --help, -?

Enable connection encryption

File that contains list of trusted
SSL Certificate Authorities

Directory that contains trusted
SSL Certificate Authority
certificate files

File that contains X.509 certificate

Permissible ciphers for connection
encryption

File that contains certificate
revocation lists

Directory that contains certificate
revocation-list files

File that contains X.509 key

Desired security state of
connection to server

5.7.11

Verify host name against server
certificate Common Name identity

Permissible TLS protocols for
encrypted connections

5.7.10

Execute with no user interactivity

MySQL user name to use when
connecting to server

Command-Line Format

--help

Display a help message and exit.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

375

mysql_secure_installation — Improve MySQL Installation Security

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix
of str. For example, mysql_secure_installation normally reads the [client] and
[mysql_secure_installation] groups. If this option is given as --defaults-group-
suffix=_other, mysql_secure_installation also reads the [client_other] and
[mysql_secure_installation_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --host=host_name, -h host_name

Command-Line Format

--host

Connect to the MySQL server on the given host.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --password=password, -p password

Command-Line Format

--password=password

Type

Default Value

376

String

[none]

This option is accepted but ignored. Whether or not this option is used,
mysql_secure_installation always prompts the user for a password.

mysql_secure_installation — Improve MySQL Installation Security

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

377

mysql_ssl_rsa_setup — Create SSL/RSA Files

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --use-default

Command-Line Format

Type

--use-default

Boolean

Execute noninteractively. This option can be used for unattended installation operations.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

Type

String

The user name of the MySQL account to use for connecting to the server.

4.4.5 mysql_ssl_rsa_setup — Create SSL/RSA Files

This program creates the SSL certificate and key files and RSA key-pair files required to support secure
connections using SSL and secure password exchange using RSA over unencrypted connections, if those
files are missing. mysql_ssl_rsa_setup can also be used to create new SSL files if the existing ones
have expired.

Note

mysql_ssl_rsa_setup uses the openssl command, so its use is contingent on
having OpenSSL installed on your machine.

Another way to generate SSL and RSA files, for MySQL distributions compiled
using OpenSSL, is to have the server generate them automatically. See
Section 6.3.3.1, “Creating SSL and RSA Certificates and Keys using MySQL”.

Important

mysql_ssl_rsa_setup helps lower the barrier to using SSL by making
it easier to generate the required files. However, certificates generated by

378

mysql_ssl_rsa_setup — Create SSL/RSA Files

mysql_ssl_rsa_setup are self-signed, which is not very secure. After you gain
experience using the files created by mysql_ssl_rsa_setup, consider obtaining
a CA certificate from a registered certificate authority.

Invoke mysql_ssl_rsa_setup like this:

mysql_ssl_rsa_setup [options]

Typical options are --datadir to specify where to create the files, and --verbose to see the openssl
commands that mysql_ssl_rsa_setup executes.

mysql_ssl_rsa_setup attempts to create SSL and RSA files using a default set of file names. It works
as follows:

1. mysql_ssl_rsa_setup checks for the openssl binary at the locations specified by the PATH

environment variable. If openssl is not found, mysql_ssl_rsa_setup does nothing. If openssl
is present, mysql_ssl_rsa_setup looks for default SSL and RSA files in the MySQL data directory
specified by the --datadir option, or the compiled-in data directory if the --datadir option is not
given.

2. mysql_ssl_rsa_setup checks the data directory for SSL files with the following names:

ca.pem
server-cert.pem
server-key.pem

3.

If any of those files are present, mysql_ssl_rsa_setup creates no SSL files. Otherwise, it invokes
openssl to create them, plus some additional files:

ca.pem               Self-signed CA certificate
ca-key.pem           CA private key
server-cert.pem      Server certificate
server-key.pem       Server private key
client-cert.pem      Client certificate
client-key.pem       Client private key

These files enable secure client connections using SSL; see Section 6.3.1, “Configuring MySQL to Use
Encrypted Connections”.

4. mysql_ssl_rsa_setup checks the data directory for RSA files with the following names:

private_key.pem      Private member of private/public key pair
public_key.pem       Public member of private/public key pair

5.

If any of these files are present, mysql_ssl_rsa_setup creates no RSA files. Otherwise, it invokes
openssl to create them. These files enable secure password exchange using RSA over unencrypted
connections for accounts authenticated by the sha256_password plugin; see Section 6.4.1.5,
“SHA-256 Pluggable Authentication”.

For information about the characteristics of files created by mysql_ssl_rsa_setup, see Section 6.3.3.1,
“Creating SSL and RSA Certificates and Keys using MySQL”.

At startup, the MySQL server automatically uses the SSL files created by mysql_ssl_rsa_setup to
enable SSL if no explicit SSL options are given other than --ssl (possibly along with ssl_cipher).
If you prefer to designate the files explicitly, invoke clients with the --ssl-ca, --ssl-cert, and --
ssl-key options at startup to name the ca.pem, server-cert.pem, and server-key.pem files,
respectively.

The server also automatically uses the RSA files created by mysql_ssl_rsa_setup to enable RSA if no
explicit RSA options are given.

379

mysql_ssl_rsa_setup — Create SSL/RSA Files

If the server is SSL-enabled, clients use SSL by default for the connection. To specify certificate and key
files explicitly, use the --ssl-ca, --ssl-cert, and --ssl-key options to name the ca.pem, client-
cert.pem, and client-key.pem files, respectively. However, some additional client setup may be
required first because mysql_ssl_rsa_setup by default creates those files in the data directory. The
permissions for the data directory normally enable access only to the system account that runs the MySQL
server, so client programs cannot use files located there. To make the files available, copy them to a
directory that is readable (but not writable) by clients:

• For local clients, the MySQL installation directory can be used. For example, if the data directory is a

subdirectory of the installation directory and your current location is the data directory, you can copy the
files like this:

cp ca.pem client-cert.pem client-key.pem ..

• For remote clients, distribute the files using a secure channel to ensure they are not tampered with

during transit.

If the SSL files used for a MySQL installation have expired, you can use mysql_ssl_rsa_setup to
create new ones:

1. Stop the server.

2. Rename or remove the existing SSL files. You may wish to make a backup of them first. (The RSA files
do not expire, so you need not remove them. mysql_ssl_rsa_setup sees that they exist and not
overwrite them.)

3. Run mysql_ssl_rsa_setup with the --datadir option to specify where to create the new files.

4. Restart the server.

mysql_ssl_rsa_setup supports the following command-line options, which can be specified on the
command line or in the [mysql_ssl_rsa_setup], [mysql_install_db], and [mysqld] groups of
an option file. For information about option files used by MySQL programs, see Section 4.2.2.2, “Using
Option Files”.

Table 4.11 mysql_ssl_rsa_setup Options

Option Name

--datadir

--help

--suffix

--uid

--verbose

--version

• --help, ?

Description

Path to data directory

Display help message and exit

Suffix for X.509 certificate Common Name attribute

Name of effective user to use for file permissions

Verbose mode

Display version information and exit

Command-Line Format

--help

Display a help message and exit.

• --datadir=dir_name

380

mysql_tzinfo_to_sql — Load the Time Zone Tables

Command-Line Format

Type

--datadir=dir_name

Directory name

The path to the directory that mysql_ssl_rsa_setup should check for default SSL and RSA files and
in which it should create files if they are missing. The default is the compiled-in data directory.

• --suffix=str

Command-Line Format

Type

--suffix=str

String

The suffix for the Common Name attribute in X.509 certificates. The suffix value is limited to 17
characters. The default is based on the MySQL version number.

• --uid=name, -v

Command-Line Format

--uid=name

The name of the user who should be the owner of any created files. The value is a user name, not a
numeric user ID. In the absence of this option, files created by mysql_ssl_rsa_setup are owned by
the user who executes it. This option is valid only if you execute the program as root on a system that
supports the chown() system call.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Produce more output about what the program does. For example, the program shows
the openssl commands it runs, and produces output to indicate whether it skips SSL or RSA file
creation because some default file already exists.

• --version, -V

Command-Line Format

--version

Display version information and exit.

4.4.6 mysql_tzinfo_to_sql — Load the Time Zone Tables

The mysql_tzinfo_to_sql program loads the time zone tables in the mysql database. It is used
on systems that have a zoneinfo database (the set of files describing time zones). Examples of such
systems are Linux, FreeBSD, Solaris, and macOS. One likely location for these files is the /usr/share/
zoneinfo directory (/usr/share/lib/zoneinfo on Solaris). If your system does not have a zoneinfo
database, you can use the downloadable package described in Section 5.1.13, “MySQL Server Time Zone
Support”.

mysql_tzinfo_to_sql can be invoked several ways:

mysql_tzinfo_to_sql tz_dir

381

mysql_upgrade — Check and Upgrade MySQL Tables

mysql_tzinfo_to_sql tz_file tz_name
mysql_tzinfo_to_sql --leap tz_file

For the first invocation syntax, pass the zoneinfo directory path name to mysql_tzinfo_to_sql and
send the output into the mysql program. For example:

mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql

mysql_tzinfo_to_sql reads your system's time zone files and generates SQL statements from them.
mysql processes those statements to load the time zone tables.

The second syntax causes mysql_tzinfo_to_sql to load a single time zone file tz_file that
corresponds to a time zone name tz_name:

mysql_tzinfo_to_sql tz_file tz_name | mysql -u root mysql

If your time zone needs to account for leap seconds, invoke mysql_tzinfo_to_sql using the third
syntax, which initializes the leap second information. tz_file is the name of your time zone file:

mysql_tzinfo_to_sql --leap tz_file | mysql -u root mysql

After running mysql_tzinfo_to_sql, it is best to restart the server so that it does not continue to use
any previously cached time zone data.

4.4.7 mysql_upgrade — Check and Upgrade MySQL Tables

Each time you upgrade MySQL, you should execute mysql_upgrade, which looks for incompatibilities
with the upgraded MySQL server:

• It upgrades the system tables in the mysql schema so that you can take advantage of new privileges or

capabilities that might have been added.

• It upgrades the Performance Schema and sys schema.

• It examines user schemas.

If mysql_upgrade finds that a table has a possible incompatibility, it performs a table check and,
if problems are found, attempts a table repair. If the table cannot be repaired, see Section 2.10.12,
“Rebuilding or Repairing Tables or Indexes” for manual table repair strategies.

mysql_upgrade communicates directly with the MySQL server, sending it the SQL statements required to
perform an upgrade.

Important

In MySQL 5.7.11, the default --early-plugin-load value is the name of the
keyring_file plugin library file, causing that plugin to be loaded by default. In
MySQL 5.7.12 and higher, the default --early-plugin-load value is empty; to
load the keyring_file plugin, you must explicitly specify the option with a value
naming the keyring_file plugin library file.

InnoDB tablespace encryption requires that the keyring plugin to be used be loaded
prior to InnoDB initialization, so this change of default --early-plugin-load
value introduces an incompatibility for upgrades from 5.7.11 to 5.7.12 or higher.
Administrators who have encrypted InnoDB tablespaces must take explicit action to
ensure continued loading of the keyring plugin: Start the server with an --early-

382

mysql_upgrade — Check and Upgrade MySQL Tables

plugin-load option that names the plugin library file. For additional information,
see Section 6.4.4.1, “Keyring Plugin Installation”.

Important

If you upgrade to MySQL 5.7.2 or later from a version older than 5.7.2, a change to
the mysql.user table requires a special sequence of steps to perform an upgrade
using mysql_upgrade. For details, see Section 2.10.3, “Changes in MySQL 5.7”.

Note

On Windows, you must run mysql_upgrade with administrator privileges. You can
do this by running a Command Prompt as Administrator and running the command.
Failure to do so may result in the upgrade failing to execute correctly.

Caution

You should always back up your current MySQL installation before performing an
upgrade. See Section 7.2, “Database Backup Methods”.

Some upgrade incompatibilities may require special handling before upgrading your
MySQL installation and running mysql_upgrade. See Section 2.10, “Upgrading
MySQL”, for instructions on determining whether any such incompatibilities apply to
your installation and how to handle them.

Use mysql_upgrade like this:

1. Ensure that the server is running.

2.

Invoke mysql_upgrade to upgrade the system tables in the mysql schema and check and repair
tables in other schemas:

mysql_upgrade [options]

3. Stop the server and restart it so that any system table changes take effect.

If you have multiple MySQL server instances to upgrade, invoke mysql_upgrade with connection
parameters appropriate for connecting to each of the desired servers. For example, with servers running
on the local host on parts 3306 through 3308, upgrade each of them by connecting to the appropriate port:

mysql_upgrade --protocol=tcp -P 3306 [other_options]
mysql_upgrade --protocol=tcp -P 3307 [other_options]
mysql_upgrade --protocol=tcp -P 3308 [other_options]

For local host connections on Unix, the --protocol=tcp option forces a connection using TCP/IP rather
than the Unix socket file.

By default, mysql_upgrade runs as the MySQL root user. If the root password is expired when
you run mysql_upgrade, it displays a message telling you that your password is expired and that
mysql_upgrade failed as a result. To correct this, reset the root password to unexpire it and run
mysql_upgrade again. First, connect to the server as root:

$> mysql -u root -p
Enter password: ****  <- enter root password here

Reset the password using ALTER USER:

mysql> ALTER USER USER() IDENTIFIED BY 'root-password';

383

mysql_upgrade — Check and Upgrade MySQL Tables

Then exit mysql and run mysql_upgrade again:

$> mysql_upgrade [options]

Note

If you run the server with the disabled_storage_engines system variable set
to disable certain storage engines (for example, MyISAM), mysql_upgrade might
fail with an error like this:

mysql_upgrade: [ERROR] 3161: Storage engine MyISAM is disabled
(Table creation is disallowed).

To handle this, restart the server with disabled_storage_engines disabled.
Then you should be able to run mysql_upgrade successfully. After that, restart
the server with disabled_storage_engines set to its original value.

Unless invoked with the --upgrade-system-tables option, mysql_upgrade processes all tables in
all user schemas as necessary. Table checking might take a long time to complete. Each table is locked
and therefore unavailable to other sessions while it is being processed. Check and repair operations can
be time-consuming, particularly for large tables. Table checking uses the FOR UPGRADE option of the
CHECK TABLE statement. For details about what this option entails, see Section 13.7.2.2, “CHECK TABLE
Statement”.

mysql_upgrade marks all checked and repaired tables with the current MySQL version number. This
ensures that the next time you run mysql_upgrade with the same version of the server, it can be
determined whether there is any need to check or repair a given table again.

mysql_upgrade saves the MySQL version number in a file named mysql_upgrade_info in the data
directory. This is used to quickly check whether all tables have been checked for this release so that table-
checking can be skipped. To ignore this file and perform the check regardless, use the --force option.

mysql_upgrade checks mysql.user system table rows and, for any row with an empty plugin column,
sets that column to 'mysql_native_password' or 'mysql_old_password' depending on the hash
format of the Password column value.

Support for pre-4.1 password hashing and mysql_old_password has been removed, so
mysql_upgrade sets empty plugin values to 'mysql_native_password' if the credentials use a
hash format compatible with that plugin. Rows with a pre-4.1 password hash must be upgraded manually.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from Pre-4.1 Password Hashing
and the mysql_old_password Plugin”.

mysql_upgrade does not upgrade the contents of the time zone tables or help tables. For upgrade
instructions, see Section 5.1.13, “MySQL Server Time Zone Support”, and Section 5.1.14, “Server-Side
Help Support”.

Unless invoked with the --skip-sys-schema option, mysql_upgrade installs the sys schema if it is
not installed, and upgrades it to the current version otherwise. An error occurs if a sys schema exists but
has no version view, on the assumption that its absence indicates a user-created schema:

A sys schema exists with no sys.version view. If
you have a user created sys schema, this must be renamed for the
upgrade to succeed.

To upgrade in this case, remove or rename the existing sys schema first.

mysql_upgrade checks for partitioned InnoDB tables that were created using the generic partitioning
handler and attempts to upgrade them to InnoDB native partitioning. (Bug #76734, Bug #20727344)

384

mysql_upgrade — Check and Upgrade MySQL Tables

You can upgrade such tables individually in the mysql client using the ALTER TABLE ... UPGRADE
PARTITIONING SQL statement.

mysql_upgrade supports the following options, which can be specified on the command line or in the
[mysql_upgrade] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.12 mysql_upgrade Options

Option Name

--bind-address

--character-sets-dir

--compress

--debug

--debug-check

--debug-info

Description

Introduced

Use specified network interface to
connect to MySQL Server

Directory where character sets are
installed

Compress all information sent
between client and server

Write debugging log

Print debugging information when
program exits

Print debugging information,
memory, and CPU statistics when
program exits

--default-auth

Authentication plugin to use

--default-character-set

Specify default character set

--defaults-extra-file

Read named option file in addition
to usual option files

--defaults-file

Read only named option file

--defaults-group-suffix

Option group suffix value

--force

--help

--host

--login-path

--max-allowed-packet

--net-buffer-length

--no-defaults

--password

--pipe

Force execution even if
mysql_upgrade has already been
executed for current MySQL
version

Display help message and exit

Host on which MySQL server is
located

Read login path options
from .mylogin.cnf

Maximum packet length to send to
or receive from server

Buffer size for TCP/IP and socket
communication

Read no option files

Password to use when connecting
to server

Connect to server using named
pipe (Windows only)

385

mysql_upgrade — Check and Upgrade MySQL Tables

Option Name

--plugin-dir

--port

--print-defaults

--protocol

--shared-memory-base-name

--skip-sys-schema

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

Description

Introduced

Directory where plugins are
installed

TCP/IP port number for
connection

Print default options

Transport protocol to use

Shared-memory name for shared-
memory connections (Windows
only)

Do not install or upgrade sys
schema

Unix socket file or Windows
named pipe to use

Enable connection encryption

File that contains list of trusted
SSL Certificate Authorities

Directory that contains trusted
SSL Certificate Authority
certificate files

File that contains X.509 certificate

Permissible ciphers for connection
encryption

File that contains certificate
revocation lists

Directory that contains certificate
revocation-list files

File that contains X.509 key

Desired security state of
connection to server

5.7.11

--ssl-verify-server-cert

--tls-version

--upgrade-system-tables

--user

--verbose

--version-check

--write-binlog

• --help

Verify host name against server
certificate Common Name identity

Permissible TLS protocols for
encrypted connections

5.7.10

Update only system tables, not
user schemas

MySQL user name to use when
connecting to server

Verbose mode

Check for proper server version

Write all statements to binary log

Command-Line Format

--help

386

mysql_upgrade — Check and Upgrade MySQL Tables

Display a short help message and exit.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

Type

Default Value

--debug[=#]

String

d:t:O,/tmp/mysql_upgrade.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:O,/
tmp/mysql_upgrade.trace.

• --debug-check

Command-Line Format

Type

--debug-check

Boolean

Print some debugging information when the program exits.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

387

mysql_upgrade — Check and Upgrade MySQL Tables

Print debugging information and memory and CPU usage statistics when the program exits.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=name

Type

String

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

388

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.

For example, mysql_upgrade normally reads the [client] and [mysql_upgrade] groups. If

mysql_upgrade — Check and Upgrade MySQL Tables

this option is given as --defaults-group-suffix=_other, mysql_upgrade also reads the
[client_other] and [mysql_upgrade_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --force

Command-Line Format

Type

--force

Boolean

Ignore the mysql_upgrade_info file and force execution even if mysql_upgrade has already been
executed for the current version of MySQL.

• --host=host_name, -h host_name

Command-Line Format

Type

--host=name

String

Connect to the MySQL server on the given host.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --max-allowed-packet=value

Command-Line Format

--max-allowed-packet=value

Type

Default Value

Minimum Value

Maximum Value

Integer

25165824

4096

2147483648

The maximum size of the buffer for client/server communication. The default value is 24MB. The
minimum and maximum values are 4KB and 2GB.

• --net-buffer-length=value

Command-Line Format

--net-buffer-length=value

Type

Integer

389

mysql_upgrade — Check and Upgrade MySQL Tables

Default Value

Minimum Value

Maximum Value

1047552

4096

16777216

The initial size of the buffer for client/server communication. The default value is 1MB − 1KB. The
minimum and maximum values are 4KB and 16MB.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=name]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysql_upgrade prompts for one. If given, there must be no space between --password=
or -p and the password following it. If no password option is specified, the default is to send no
password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysql_upgrade should not prompt for one, use
the --skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

390

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

mysql_upgrade — Check and Upgrade MySQL Tables

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used to
specify an authentication plugin but mysql_upgrade does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

Type

--port=#

Numeric

For TCP/IP connections, the port number to use.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

Type

--protocol=name

String

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --skip-sys-schema

Command-Line Format

Type

--skip-sys-schema

Boolean

391

mysql_upgrade — Check and Upgrade MySQL Tables

Default Value

FALSE

By default, mysql_upgrade installs the sys schema if it is not installed, and upgrades it to the current
version otherwise. The --skip-sys-schema option suppresses this behavior.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --upgrade-system-tables, -s

Command-Line Format

--upgrade-system-tables

Type

Boolean

392

Upgrade only the system tables in the mysql schema, do not upgrade user schemas.

• --user=user_name, -u user_name

Command-Line Format

--user=name

Client Programs

Type

String

The user name of the MySQL account to use for connecting to the server. The default user name is
root.

• --verbose

Command-Line Format

Type

--verbose

Boolean

Verbose mode. Print more information about what the program does.

• --version-check, -k

Command-Line Format

Type

--version-check

Boolean

Check the version of the server to which mysql_upgrade is connecting to verify that it is the same as
the version for which mysql_upgrade was built. If not, mysql_upgrade exits. This option is enabled
by default; to disable the check, use --skip-version-check.

• --write-binlog

Command-Line Format

--write-binlog

Type

Default Value

Boolean

OFF

By default, binary logging by mysql_upgrade is disabled. Invoke the program with --write-binlog if
you want its actions to be written to the binary log.

When the server is running with global transaction identifiers (GTIDs) enabled (gtid_mode=ON), do not
enable binary logging by mysql_upgrade.

4.5 Client Programs

This section describes client programs that connect to the MySQL server.

4.5.1 mysql — The MySQL Command-Line Client

mysql is a simple SQL shell with input line editing capabilities. It supports interactive and noninteractive
use. When used interactively, query results are presented in an ASCII-table format. When used
noninteractively (for example, as a filter), the result is presented in tab-separated format. The output format
can be changed using command options.

If you have problems due to insufficient memory for large result sets, use the --quick option. This
forces mysql to retrieve results from the server a row at a time rather than retrieving the entire result
set and buffering it in memory before displaying it. This is done by returning the result set using the
mysql_use_result() C API function in the client/server library rather than mysql_store_result().

393

mysql — The MySQL Command-Line Client

Note

Alternatively, MySQL Shell offers access to the X DevAPI. For details, see MySQL
Shell 8.0.

Using mysql is very easy. Invoke it from the prompt of your command interpreter as follows:

mysql db_name

Or:

mysql --user=user_name --password db_name

In this case, you'll need to enter your password in response to the prompt that mysql displays:

Enter password: your_password

Then type an SQL statement, end it with ;, \g, or \G and press Enter.

Typing Control+C interrupts the current statement if there is one, or cancels any partial input line
otherwise.

You can execute SQL statements in a script file (batch file) like this:

mysql db_name < script.sql > output.tab

On Unix, the mysql client logs statements executed interactively to a history file. See Section 4.5.1.3,
“mysql Client Logging”.

4.5.1.1 mysql Client Options

mysql supports the following options, which can be specified on the command line or in the [mysql]
and [client] groups of an option file. For information about option files used by MySQL programs, see
Section 4.2.2.2, “Using Option Files”.

Table 4.13 mysql Client Options

Option Name

--auto-rehash

--auto-vertical-output

--batch

--binary-as-hex

--binary-mode

--bind-address

--character-sets-dir

--column-names

394

Description

Introduced

Deprecated

Enable automatic
rehashing

Enable automatic vertical
result set display

Do not use history file

Display binary values in
hexadecimal notation

5.7.19

Disable \r\n - to - \n
translation and treatment
of \0 as end-of-query

Use specified network
interface to connect to
MySQL Server

Directory where
character sets are
installed

Write column names in
results

mysql — The MySQL Command-Line Client

Option Name

Description

Introduced

Deprecated

5.7.44-ndb-7.6.35

--column-type-info

--commands

--comments

--compress

--connect-expired-
password

--connect-timeout

--database

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

Display result set
metadata

Enable or disable
processing of local mysql
client commands

Whether to retain or strip
comments in statements
sent to the server

Compress all information
sent between client and
server

Indicate to server that
client can handle expired-
password sandbox mode

Number of seconds
before connection
timeout

The database to use

Write debugging log;
supported only if MySQL
was built with debugging
support

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Specify default character
set

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--delimiter

Set the statement
delimiter

--enable-cleartext-plugin Enable cleartext

--execute

authentication plugin

Execute the statement
and quit

395

mysql — The MySQL Command-Line Client

Option Name

Description

Introduced

Deprecated

--force

Continue even if an SQL
error occurs

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--histignore

--host

--html

--ignore-spaces

--init-command

--line-numbers

--local-infile

--login-path

--max-allowed-packet

--max-join-size

--named-commands

--net-buffer-length

--no-auto-rehash

--no-beep

--no-defaults

--one-database

--pager

Display help message
and exit

Patterns specifying which
statements to ignore for
logging

Host on which MySQL
server is located

Produce HTML output

Ignore spaces after
function names

SQL statement to
execute after connecting

Write line numbers for
errors

Enable or disable for
LOCAL capability for
LOAD DATA

Read login path options
from .mylogin.cnf

Maximum packet length
to send to or receive from
server

The automatic limit for
rows in a join when using
--safe-updates

Enable named mysql
commands

Buffer size for
TCP/IP and socket
communication

Disable automatic
rehashing

Do not beep when errors
occur

Read no option files

Ignore statements except
those for the default
database named on the
command line

Use the given command
for paging query output

396

Option Name

--password

--pipe

--plugin-dir

--port

mysql — The MySQL Command-Line Client

Description

Introduced

Deprecated

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--prompt

--protocol

--quick

--raw

--reconnect

--safe-updates, --i-am-a-
dummy

--secure-auth

--select-limit

Set the prompt to the
specified format

Transport protocol to use

Do not cache each query
result

Write column values
without escape
conversion

If the connection to
the server is lost,
automatically try to
reconnect

Allow only UPDATE and
DELETE statements that
specify key values

Do not send passwords
to server in old (pre-4.1)
format

The automatic limit for
SELECT statements
when using --safe-
updates

--server-public-key-path Path name to file

--shared-memory-base-
name

--show-warnings

--sigint-ignore

containing RSA public
key

Shared-memory name
for shared-memory
connections (Windows
only)

Show warnings after
each statement if there
are any

Ignore SIGINT signals
(typically the result of
typing Control+C)

Yes

397

mysql — The MySQL Command-Line Client

Introduced

Deprecated

Option Name

--silent

--skip-auto-rehash

--skip-column-names

--skip-line-numbers

Description

Silent mode

Disable automatic
rehashing

Do not write column
names in results

Skip line numbers for
errors

--skip-named-commands Disable named mysql

--skip-pager

commands

Disable paging

--skip-reconnect

Disable reconnecting

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--syslog

--table

--tee

398

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

Verify host name
against server certificate
Common Name identity

Log interactive
statements to syslog

Display output in tabular
format

Append a copy of output
to named file

mysql — The MySQL Command-Line Client

Introduced

5.7.10

Deprecated

Option Name

--tls-version

--unbuffered

--user

--verbose

--version

--vertical

--wait

--xml

• --help, -?

Description

Permissible TLS
protocols for encrypted
connections

Flush the buffer after
each query

MySQL user name to
use when connecting to
server

Verbose mode

Display version
information and exit

Print query output rows
vertically (one line per
column value)

If the connection cannot
be established, wait and
retry instead of aborting

Produce XML output

Command-Line Format

--help

Display a help message and exit.

• --auto-rehash

Command-Line Format

Disabled by

--auto-rehash

skip-auto-rehash

Enable automatic rehashing. This option is on by default, which enables database, table, and column
name completion. Use --disable-auto-rehash to disable rehashing. That causes mysql to start
faster, but you must issue the rehash command or its \# shortcut if you want to use name completion.

To complete a name, enter the first part and press Tab. If the name is unambiguous, mysql completes
it. Otherwise, you can press Tab again to see the possible names that begin with what you have typed
so far. Completion does not occur if there is no default database.

Note

This feature requires a MySQL client that is compiled with the readline library.
Typically, the readline library is not available on Windows.

399

mysql — The MySQL Command-Line Client

• --auto-vertical-output

Command-Line Format

--auto-vertical-output

Cause result sets to be displayed vertically if they are too wide for the current window, and using normal
tabular format otherwise. (This applies to statements terminated by ; or \G.)

• --batch, -B

Command-Line Format

--batch

Print results using tab as the column separator, with each row on a new line. With this option, mysql
does not use the history file.

Batch mode results in nontabular output format and escaping of special characters. Escaping may be
disabled by using raw mode; see the description for the --raw option.

• --binary-as-hex

Command-Line Format

--binary-as-hex

Introduced

Type

Default Value

5.7.19

Boolean

FALSE

When this option is given, mysql displays binary data using hexadecimal notation (0xvalue). This
occurs whether the overall output display format is tabular, vertical, HTML, or XML.

--binary-as-hex when enabled affects display of all binary strings, including those returned by
functions such as CHAR() and UNHEX(). The following example demonstrates this using the ASCII code
for A (65 decimal, 41 hexadecimal):

• --binary-as-hex disabled:

mysql> SELECT CHAR(0x41), UNHEX('41');
+------------+-------------+
| CHAR(0x41) | UNHEX('41') |
+------------+-------------+
| A          | A           |
+------------+-------------+

• --binary-as-hex enabled:

mysql> SELECT CHAR(0x41), UNHEX('41');
+------------------------+--------------------------+
| CHAR(0x41)             | UNHEX('41')              |
+------------------------+--------------------------+
| 0x41                   | 0x41                     |
+------------------------+--------------------------+

To write a binary string expression so that it displays as a character string regardless of whether --
binary-as-hex is enabled, use these techniques:

• The CHAR() function has a USING charset clause:

mysql> SELECT CHAR(0x41 USING utf8mb4);

400

mysql — The MySQL Command-Line Client

+--------------------------+
| CHAR(0x41 USING utf8mb4) |
+--------------------------+
| A                        |
+--------------------------+

• More generally, use CONVERT() to convert an expression to a given character set:

mysql> SELECT CONVERT(UNHEX('41') USING utf8mb4);
+------------------------------------+
| CONVERT(UNHEX('41') USING utf8mb4) |
+------------------------------------+
| A                                  |
+------------------------------------+

This option was added in MySQL 5.7.19.

• --binary-mode

Command-Line Format

--binary-mode

This option helps when processing mysqlbinlog output that may contain BLOB values. By default,
mysql translates \r\n in statement strings to \n and interprets \0 as the statement terminator. --
binary-mode disables both features. It also disables all mysql commands except charset and
delimiter in noninteractive mode (for input piped to mysql or loaded using the source command).

(NDB Cluster 7.6.35 and later:) --binary-mode, when enabled, causes the server to disregard any
setting for --commands .

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --column-names

Command-Line Format

--column-names

Write column names in results.

401

mysql — The MySQL Command-Line Client

• --column-type-info

Command-Line Format

--column-type-info

Display result set metadata. This information corresponds to the contents of C API MYSQL_FIELD data
structures. See C API Basic Data Structures.

• --commands

Command-Line Format

--commands

402

mysql — The MySQL Command-Line Client

Introduced

5.7.44-ndb-7.6.35

Whether to enable or disable processing of local mysql client commands. Setting this option to FALSE
disables such processing, and has the effects listed here:

• The following mysql client commands are disabled:

• charset (/C remains enabled)

• clear

• connect

• edit

• ego

• exit

• go

• help

• nopager

• notee

• nowarning

• pager

• print

• prompt

• query_attributes

• quit

• rehash

• resetconnection

• ssl_session_data_print

• source

• status

• system

• tee

• \u (use is passed to the server)

• warnings

403

mysql — The MySQL Command-Line Client

• The \C and delimiter commands remain enabled.

• The --system-command option is ignored, and has no effect.

This option has no effect when --binary-mode is enabled.

When --commands is enabled, it is possible to disable (only) the system command using the --
system-command option.

This option was added in NDB Cluster 7.6.35.

• --comments, -c

Command-Line Format

Type

Default Value

--comments

Boolean

FALSE

Whether to strip or preserve comments in statements sent to the server. The default is --skip-
comments (strip comments), enable with --comments (preserve comments).

Note

In MySQL 5.7, the mysql client always passes optimizer hints to the server,
regardless of whether this option is given. To ensure that optimizer hints are not
stripped if you are using an older version of the mysql client with a version of
the server that understands optimizer hints, invoke mysql with the --comments
option.

Comment stripping is deprecated as of MySQL 5.7.20. You should expect this
feature and the options to control it to be removed in a future MySQL release.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --connect-expired-password

Command-Line Format

--connect-expired-password

Indicate to the server that the client can handle sandbox mode if the account used to connect has an
expired password. This can be useful for noninteractive invocations of mysql because normally the
server disconnects noninteractive clients that attempt to connect using an account with an expired
password. (See Section 6.2.12, “Server Handling of Expired Passwords”.)

404

mysql — The MySQL Command-Line Client

• --connect-timeout=value

Command-Line Format

--connect-timeout=value

Type

Default Value

Numeric

0

The number of seconds before connection timeout. (Default value is 0.)

• --database=db_name, -D db_name

Command-Line Format

--database=dbname

Type

String

The database to use. This is useful primarily in an option file.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o,/tmp/mysql.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/mysql.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

405

mysql — The MySQL Command-Line Client

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set for the client and connection.

This option can be useful if the operating system uses one character set and the mysql client by default
uses another. In this case, output may be formatted incorrectly. You can usually fix such issues by using
this option to force the client to use the system character set instead.

For more information, see Section 10.4, “Connection Character Sets and Collations”, and Section 10.15,
“Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

406

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

mysql — The MySQL Command-Line Client

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysql normally reads the [client] and [mysql] groups. If this option is given as --
defaults-group-suffix=_other, mysql also reads the [client_other] and [mysql_other]
groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --delimiter=str

Command-Line Format

--delimiter=str

Type

Default Value

String

;

Set the statement delimiter. The default is the semicolon character (;).

• --disable-named-commands

Disable named commands. Use the \* form only, or use named commands only at the beginning of
a line ending with a semicolon (;). mysql starts with this option enabled by default. However, even
with this option, long-format commands still work from the first line. See Section 4.5.1.2, “mysql Client
Commands”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

• --execute=statement, -e statement

Command-Line Format

--execute=statement

Type

String

Execute the statement and quit. The default output format is like that produced with --batch. See
Section 4.2.2.1, “Using Options on the Command Line”, for some examples. With this option, mysql
does not use the history file.

• --force, -f

Command-Line Format

--force

407

Continue even if an SQL error occurs.

mysql — The MySQL Command-Line Client

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that
plugin, the server does not send the public key unless requested. This option is ignored for accounts that
do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --histignore

Command-Line Format

--histignore=pattern_list

Type

String

A list of one or more colon-separated patterns specifying statements to ignore for logging purposes.
These patterns are added to the default pattern list ("*IDENTIFIED*:*PASSWORD*"). The value
specified for this option affects logging of statements written to the history file, and to syslog if the --
syslog option is given. For more information, see Section 4.5.1.3, “mysql Client Logging”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Connect to the MySQL server on the given host.

• --html, -H

Command-Line Format

--html

Produce HTML output.

408

mysql — The MySQL Command-Line Client

• --ignore-spaces, -i

Command-Line Format

--ignore-spaces

Ignore spaces after function names. The effect of this is described in the discussion for the
IGNORE_SPACE SQL mode (see Section 5.1.10, “Server SQL Modes”).

• --init-command=str

Command-Line Format

--init-command=str

SQL statement to execute after connecting to the server. If auto-reconnect is enabled, the statement is
executed again after reconnection occurs.

• --line-numbers

Command-Line Format

Disabled by

--line-numbers

skip-line-numbers

Write line numbers for errors. Disable this with --skip-line-numbers.

• --local-infile[={0|1}]

Command-Line Format

--local-infile[={0|1}]

Type

Default Value

Boolean

FALSE

By default, LOCAL capability for LOAD DATA is determined by the default compiled into the MySQL client
library. To enable or disable LOCAL data loading explicitly, use the --local-infile option. When
given with no value, the option enables LOCAL data loading. When given as --local-infile=0 or --
local-infile=1, the option disables or enables LOCAL data loading.

Successful use of LOCAL load operations within mysql also requires that the server permits local
loading; see Section 6.1.6, “Security Considerations for LOAD DATA LOCAL”

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

409

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line

Options that Affect Option-File Handling”.

mysql — The MySQL Command-Line Client

• --max-allowed-packet=value

Command-Line Format

--max-allowed-packet=value

Type

Default Value

Numeric

16777216

The maximum size of the buffer for client/server communication. The default is 16MB, the maximum is
1GB.

• --max-join-size=value

Command-Line Format

--max-join-size=value

Type

Default Value

Numeric

1000000

The automatic limit for rows in a join when using --safe-updates. (Default value is 1,000,000.)

• --named-commands, -G

Command-Line Format

Disabled by

--named-commands

skip-named-commands

Enable named mysql commands. Long-format commands are permitted, not just short-format
commands. For example, quit and \q both are recognized. Use --skip-named-commands to disable
named commands. See Section 4.5.1.2, “mysql Client Commands”.

• --net-buffer-length=value

Command-Line Format

--net-buffer-length=value

Type

Default Value

Numeric

16384

The buffer size for TCP/IP and socket communication. (Default value is 16KB.)

• --no-auto-rehash, -A

Command-Line Format

Deprecated

--no-auto-rehash

Yes

This has the same effect as --skip-auto-rehash. See the description for --auto-rehash.

410

• --no-beep, -b

Command-Line Format

--no-beep

Do not beep when errors occur.

mysql — The MySQL Command-Line Client

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --one-database, -o

Command-Line Format

--one-database

Ignore statements except those that occur while the default database is the one named on the command
line. This option is rudimentary and should be used with care. Statement filtering is based only on USE
statements.

Initially, mysql executes statements in the input because specifying a database db_name on the
command line is equivalent to inserting USE db_name at the beginning of the input. Then, for each
USE statement encountered, mysql accepts or rejects following statements depending on whether the
database named is the one on the command line. The content of the statements is immaterial.

Suppose that mysql is invoked to process this set of statements:

DELETE FROM db2.t2;
USE db2;
DROP TABLE db1.t1;
CREATE TABLE db1.t1 (i INT);
USE db1;
INSERT INTO t1 (i) VALUES(1);
CREATE TABLE db2.t1 (j INT);

If the command line is mysql --force --one-database db1, mysql handles the input as follows:

• The DELETE statement is executed because the default database is db1, even though the statement

names a table in a different database.

• The DROP TABLE and CREATE TABLE statements are not executed because the default database is

not db1, even though the statements name a table in db1.

• The INSERT and CREATE TABLE statements are executed because the default database is db1,

even though the CREATE TABLE statement names a table in a different database.

• --pager[=command]

Command-Line Format

Disabled by

Type

--pager[=command]

skip-pager

String

411

mysql — The MySQL Command-Line Client

Use the given command for paging query output. If the command is omitted, the default pager is the
value of your PAGER environment variable. Valid pagers are less, more, cat [> filename], and
so forth. This option works only on Unix and only in interactive mode. To disable paging, use --skip-
pager. Section 4.5.1.2, “mysql Client Commands”, discusses output paging further.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysql prompts for one. If given, there must be no space between --password= or -p and
the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysql should not prompt for one, use the --
skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is
used to specify an authentication plugin but mysql does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --print-defaults

412

mysql — The MySQL Command-Line Client

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --prompt=format_str

Command-Line Format

--prompt=format_str

Type

Default Value

String

mysql>

Set the prompt to the specified format. The default is mysql>. The special sequences that the prompt
can contain are described in Section 4.5.1.2, “mysql Client Commands”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --quick, -q

Command-Line Format

--quick

Do not cache each query result, print each row as it is received. This may slow down the server if the
output is suspended. With this option, mysql does not use the history file.

By default, mysql fetches all result rows before producing any output; while storing these, it calculates
a running maximum column length from the actual value of each column in succession. When printing
the output, it uses this maximum to format it. When --quick is specified, mysql does not have the
rows for which to calculate the length before starting, and so uses the maximum length. In the following
example, table t1 has a single column of type BIGINT and containing 4 rows. The default output is 9
characters wide; this width is equal the maximum number of characters in any of the column values in
the rows returned (5), plus 2 characters each for the spaces used as padding and the | characters used
as column delimiters). The output when using the --quick option is 25 characters wide; this is equal to
the number of characters needed to represent -9223372036854775808, which is the longest possible

413

mysql — The MySQL Command-Line Client

value that can be stored in a (signed) BIGINT column, or 19 characters, plus the 4 characters used for
padding and column delimiters. The difference can be seen here:

$> mysql -t test -e "SELECT * FROM t1"
+-------+
| c1    |
+-------+
|   100 |
|  1000 |
| 10000 |
|    10 |
+-------+

$> mysql --quick -t test -e "SELECT * FROM t1"
+----------------------+
| c1                   |
+----------------------+
|                  100 |
|                 1000 |
|                10000 |
|                   10 |
+----------------------+

• --raw, -r

Command-Line Format

--raw

For tabular output, the “boxing” around columns enables one column value to be distinguished from
another. For nontabular output (such as is produced in batch mode or when the --batch or --silent
option is given), special characters are escaped in the output so they can be identified easily. Newline,
tab, NUL, and backslash are written as \n, \t, \0, and \\. The --raw option disables this character
escaping.

The following example demonstrates tabular versus nontabular output and the use of raw mode to
disable escaping:

% mysql
mysql> SELECT CHAR(92);
+----------+
| CHAR(92) |
+----------+
| \        |
+----------+

% mysql -s
mysql> SELECT CHAR(92);
CHAR(92)
\\

% mysql -s -r
mysql> SELECT CHAR(92);
CHAR(92)
\

• --reconnect

Command-Line Format

--reconnect

414

mysql — The MySQL Command-Line Client

Disabled by

skip-reconnect

If the connection to the server is lost, automatically try to reconnect. A single reconnect attempt is made
each time the connection is lost. To suppress reconnection behavior, use --skip-reconnect.

• --safe-updates, --i-am-a-dummy, -U

Command-Line Format

Type

Default Value

--safe-updates

--i-am-a-dummy

Boolean

FALSE

If this option is enabled, UPDATE and DELETE statements that do not use a key in the WHERE clause or a
LIMIT clause produce an error. In addition, restrictions are placed on SELECT statements that produce
(or are estimated to produce) very large result sets. If you have set this option in an option file, you can
use --skip-safe-updates on the command line to override it. For more information about this option,
see Using Safe-Updates Mode (--safe-updates).

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --select-limit=value

Command-Line Format

--select-limit=value

Type

Default Value

Numeric

1000

The automatic limit for SELECT statements when using --safe-updates. (Default value is 1,000.)

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

415

mysql — The MySQL Command-Line Client

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --show-warnings

Command-Line Format

--show-warnings

Cause warnings to be shown after each statement if there are any. This option applies to interactive and
batch mode.

• --sigint-ignore

Command-Line Format

--sigint-ignore

Ignore SIGINT signals (typically the result of typing Control+C).

Without this option, typing Control+C interrupts the current statement if there is one, or cancels any
partial input line otherwise.

416

mysql — The MySQL Command-Line Client

• --silent, -s

Command-Line Format

--silent

Silent mode. Produce less output. This option can be given multiple times to produce less and less
output.

This option results in nontabular output format and escaping of special characters. Escaping may be
disabled by using raw mode; see the description for the --raw option.

• --skip-column-names, -N

Command-Line Format

--skip-column-names

Do not write column names in results. Use of this option causes the output to be right-aligned, as shown
here:

$> echo "SELECT * FROM t1" | mysql -t test
+-------+
| c1    |
+-------+
| a,c,d |
| c     |
+-------+
$> echo "SELECT * FROM t1" | ./mysql -uroot -Nt test
+-------+
| a,c,d |
|     c |
+-------+

• --skip-line-numbers, -L

Command-Line Format

--skip-line-numbers

Do not write line numbers for errors. Useful when you want to compare result files that include error
messages.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

417

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

mysql — The MySQL Command-Line Client

• --syslog, -j

Command-Line Format

--syslog

This option causes mysql to send interactive statements to the system logging facility. On Unix, this is
syslog; on Windows, it is the Windows Event Log. The destination where logged messages appear is
system dependent. On Linux, the destination is often the /var/log/messages file.

Here is a sample of output generated on Linux by using --syslog. This output is formatted for
readability; each logged message actually takes a single line.

Mar  7 12:39:25 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
  DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
Mar  7 12:39:28 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
  DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'

For more information, see Section 4.5.1.3, “mysql Client Logging”.

• --table, -t

Command-Line Format

--table

Display output in table format. This is the default for interactive use, but can be used to produce table
output in batch mode.

• --tee=file_name

Command-Line Format

Type

--tee=file_name

File name

Append a copy of output to the given file. This option works only in interactive mode. Section 4.5.1.2,
“mysql Client Commands”, discusses tee files further.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

418

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

mysql — The MySQL Command-Line Client

• --unbuffered, -n

Command-Line Format

--unbuffered

Flush the buffer after each query.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

Type

String

The user name of the MySQL account to use for connecting to the server.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Produce more output about what the program does. This option can be given multiple
times to produce more and more output. (For example, -v -v -v produces table output format even in
batch mode.)

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --vertical, -E

Command-Line Format

--vertical

Print query output rows vertically (one line per column value). Without this option, you can specify
vertical output for individual statements by terminating them with \G.

• --wait, -w

Command-Line Format

--wait

If the connection cannot be established, wait and retry instead of aborting.

• --xml, -X

Command-Line Format

--xml

Produce XML output.

<field name="column_name">NULL</field>

The output when --xml is used with mysql matches that of mysqldump --xml. See Section 4.5.4,
“mysqldump — A Database Backup Program”, for details.

419

mysql — The MySQL Command-Line Client

The XML output also uses an XML namespace, as shown here:

$> mysql --xml -uroot -e "SHOW VARIABLES LIKE 'version%'"
<?xml version="1.0"?>

<resultset statement="SHOW VARIABLES LIKE 'version%'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<row>
<field name="Variable_name">version</field>
<field name="Value">5.0.40-debug</field>
</row>

<row>
<field name="Variable_name">version_comment</field>
<field name="Value">Source distribution</field>
</row>

<row>
<field name="Variable_name">version_compile_machine</field>
<field name="Value">i686</field>
</row>

<row>
<field name="Variable_name">version_compile_os</field>
<field name="Value">suse-linux-gnu</field>
</row>
</resultset>

4.5.1.2 mysql Client Commands

mysql sends each SQL statement that you issue to the server to be executed. There is also a set of
commands that mysql itself interprets. For a list of these commands, type help or \h at the mysql>
prompt:

mysql> help

List of all MySQL commands:
Note that all text commands must be first on line and end with ';'
?         (\?) Synonym for `help'.
clear     (\c) Clear the current input statement.
connect   (\r) Reconnect to the server. Optional arguments are db and host.
delimiter (\d) Set statement delimiter.
edit      (\e) Edit command with $EDITOR.
ego       (\G) Send command to mysql server, display result vertically.
exit      (\q) Exit mysql. Same as quit.
go        (\g) Send command to mysql server.
help      (\h) Display this help.
nopager   (\n) Disable pager, print to stdout.
notee     (\t) Don't write into outfile.
pager     (\P) Set PAGER [to_pager]. Print the query results via PAGER.
print     (\p) Print current command.
prompt    (\R) Change your mysql prompt.
quit      (\q) Quit mysql.
rehash    (\#) Rebuild completion hash.
source    (\.) Execute an SQL script file. Takes a file name as an argument.
status    (\s) Get status information from the server.
system    (\!) Execute a system shell command.
tee       (\T) Set outfile [to_outfile]. Append everything into given
               outfile.
use       (\u) Use another database. Takes database name as argument.
charset   (\C) Switch to another charset. Might be needed for processing
               binlog with multi-byte charsets.
warnings  (\W) Show warnings after every statement.
nowarning (\w) Don't show warnings after every statement.
resetconnection(\x) Clean session context.

420

mysql — The MySQL Command-Line Client

For server side help, type 'help contents'

If mysql is invoked with the --binary-mode option, all mysql commands are disabled except charset
and delimiter in noninteractive mode (for input piped to mysql or loaded using the source command).

Each command has both a long and short form. The long form is not case-sensitive; the short form is. The
long form can be followed by an optional semicolon terminator, but the short form should not.

The use of short-form commands within multiple-line /* ... */ comments is not supported. Short-form
commands do work within single-line /*! ... */ version comments, as do /*+ ... */ optimizer-hint
comments, which are stored in object definitions. If there is a concern that optimizer-hint comments may be
stored in object definitions so that dump files when reloaded with mysql would result in execution of such
commands, either invoke mysql with the --binary-mode option or use a reload client other than mysql.

•   help [arg], \h [arg], \? [arg], ? [arg]

Display a help message listing the available mysql commands.

If you provide an argument to the help command, mysql uses it as a search string to access server-
side help from the contents of the MySQL Reference Manual. For more information, see Section 4.5.1.4,
“mysql Client Server-Side Help”.

•   charset charset_name, \C charset_name

Change the default character set and issue a SET NAMES statement. This enables the character set to
remain synchronized on the client and server if mysql is run with auto-reconnect enabled (which is not
recommended), because the specified character set is used for reconnects.

•   clear, \c

Clear the current input. Use this if you change your mind about executing the statement that you are
entering.

•   connect [db_name [host_name]], \r [db_name [host_name]]

Reconnect to the server. The optional database name and host name arguments may be given to
specify the default database or the host where the server is running. If omitted, the current values are
used.

•   delimiter str, \d str

Change the string that mysql interprets as the separator between SQL statements. The default is the
semicolon character (;).

The delimiter string can be specified as an unquoted or quoted argument on the delimiter command
line. Quoting can be done with either single quote ('), double quote ("), or backtick (`) characters.
To include a quote within a quoted string, either quote the string with a different quote character or
escape the quote with a backslash (\) character. Backslash should be avoided outside of quoted strings
because it is the escape character for MySQL. For an unquoted argument, the delimiter is read up to the
first space or end of line. For a quoted argument, the delimiter is read up to the matching quote on the
line.

mysql interprets instances of the delimiter string as a statement delimiter anywhere it occurs, except
within quoted strings. Be careful about defining a delimiter that might occur within other words. For
example, if you define the delimiter as X, it is not possible to use the word INDEX in statements. mysql
interprets this as INDE followed by the delimiter X.

421

mysql — The MySQL Command-Line Client

When the delimiter recognized by mysql is set to something other than the default of ;, instances of
that character are sent to the server without interpretation. However, the server itself still interprets ; as
a statement delimiter and processes statements accordingly. This behavior on the server side comes
into play for multiple-statement execution (see Multiple Statement Execution Support), and for parsing
the body of stored procedures and functions, triggers, and events (see Section 23.1, “Defining Stored
Programs”).

•   edit, \e

Edit the current input statement. mysql checks the values of the EDITOR and VISUAL environment
variables to determine which editor to use. The default editor is vi if neither variable is set.

The edit command works only in Unix.

•   ego, \G

Send the current statement to the server to be executed and display the result using vertical format.

•   exit, \q

Exit mysql.

•   go, \g

Send the current statement to the server to be executed.

•   nopager, \n

Disable output paging. See the description for pager.

The nopager command works only in Unix.

•   notee, \t

Disable output copying to the tee file. See the description for tee.

•   nowarning, \w

Disable display of warnings after each statement.

•   pager [command], \P [command]

Enable output paging. By using the --pager option when you invoke mysql, it is possible to browse or
search query results in interactive mode with Unix programs such as less, more, or any other similar
program. If you specify no value for the option, mysql checks the value of the PAGER environment
variable and sets the pager to that. Pager functionality works only in interactive mode.

Output paging can be enabled interactively with the pager command and disabled with nopager. The
command takes an optional argument; if given, the paging program is set to that. With no argument, the
pager is set to the pager that was set on the command line, or stdout if no pager was specified.

Output paging works only in Unix because it uses the popen() function, which does not exist on
Windows. For Windows, the tee option can be used instead to save query output, although it is not as
convenient as pager for browsing output in some situations.

•   print, \p

Print the current input statement without executing it.

422

mysql — The MySQL Command-Line Client

•   prompt [str], \R [str]

Reconfigure the mysql prompt to the given string. The special character sequences that can be used in
the prompt are described later in this section.

If you specify the prompt command with no argument, mysql resets the prompt to the default of
mysql>.

•   quit, \q

Exit mysql.

•   rehash, \#

Rebuild the completion hash that enables database, table, and column name completion while you are
entering statements. (See the description for the --auto-rehash option.)

•   resetconnection, \x

Reset the connection to clear the session state.

Resetting a connection has effects similar to mysql_change_user() or an auto-reconnect
except that the connection is not closed and reopened, and re-authentication is not done. See
mysql_change_user(), and Automatic Reconnection Control.

This example shows how resetconnection clears a value maintained in the session state:

mysql> SELECT LAST_INSERT_ID(3);
+-------------------+
| LAST_INSERT_ID(3) |
+-------------------+
|                 3 |
+-------------------+

mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                3 |
+------------------+

mysql> resetconnection;

mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                0 |
+------------------+

•   source file_name, \. file_name

Read the named file and executes the statements contained therein. On Windows, specify path name
separators as / or \\.

Quote characters are taken as part of the file name itself. For best results, the name should not include
space characters.

423

mysql — The MySQL Command-Line Client

•   status, \s

Provide status information about the connection and the server you are using. If you are running with --
safe-updates enabled, status also prints the values for the mysql variables that affect your queries.

•   system command, \! command

Execute the given command using your default command interpreter.

The system command works only in Unix.

•   tee [file_name], \T [file_name]

By using the --tee option when you invoke mysql, you can log statements and their output. All the
data displayed on the screen is appended into a given file. This can be very useful for debugging
purposes also. mysql flushes results to the file after each statement, just before it prints its next prompt.
Tee functionality works only in interactive mode.

You can enable this feature interactively with the tee command. Without a parameter, the previous file is
used. The tee file can be disabled with the notee command. Executing tee again re-enables logging.

•   use db_name, \u db_name

Use db_name as the default database.

•   warnings, \W

Enable display of warnings after each statement (if there are any).

Here are a few tips about the pager command:

• You can use it to write to a file and the results go only to the file:

mysql> pager cat > /tmp/log.txt

You can also pass any options for the program that you want to use as your pager:

mysql> pager less -n -i -S

• In the preceding example, note the -S option. You may find it very useful for browsing wide query

results. Sometimes a very wide result set is difficult to read on the screen. The -S option to less can
make the result set much more readable because you can scroll it horizontally using the left-arrow and
right-arrow keys. You can also use -S interactively within less to switch the horizontal-browse mode on
and off. For more information, read the less manual page:

man less

• The -F and -X options may be used with less to cause it to exit if output fits on one screen, which is

convenient when no scrolling is necessary:

mysql> pager less -n -i -S -F -X

• You can specify very complex pager commands for handling query output:

mysql> pager cat | tee /dr1/tmp/res.txt \
          | tee /dr2/tmp/res2.txt | less -n -i -S

In this example, the command would send query results to two files in two different directories on two
different file systems mounted on /dr1 and /dr2, yet still display the results onscreen using less.

424

mysql — The MySQL Command-Line Client

You can also combine the tee and pager functions. Have a tee file enabled and pager set to less, and
you are able to browse the results using the less program and still have everything appended into a file
the same time. The difference between the Unix tee used with the pager command and the mysql built-
in tee command is that the built-in tee works even if you do not have the Unix tee available. The built-
in tee also logs everything that is printed on the screen, whereas the Unix tee used with pager does not
log quite that much. Additionally, tee file logging can be turned on and off interactively from within mysql.
This is useful when you want to log some queries to a file, but not others.

The prompt command reconfigures the default mysql> prompt. The string for defining the prompt can
contain the following special sequences.

Option

\C

\c

\D

\d

\h

\l

\m

\n

\O

\o

\P

\p

\R

\r

\S

\s

\t

\U

\u

\v

\w

\Y

\y

\_

\

\'

\"

\\

Description

The current connection identifier

A counter that increments for each statement you
issue

The full current date

The default database

The server host

The current delimiter

Minutes of the current time

A newline character

The current month in three-letter format (Jan, Feb,
…)

The current month in numeric format

am/pm

The current TCP/IP port or socket file

The current time, in 24-hour military time (0–23)

The current time, standard 12-hour time (1–12)

Semicolon

Seconds of the current time

A tab character

Your full user_name@host_name account name

Your user name

The server version

The current day of the week in three-letter format
(Mon, Tue, …)

The current year, four digits

The current year, two digits

A space

A space (a space follows the backslash)

Single quote

Double quote

A literal \ backslash character

425

mysql — The MySQL Command-Line Client

Option

\x

Description

x, for any “x” not listed above

You can set the prompt in several ways:

• Use an environment variable. You can set the MYSQL_PS1 environment variable to a prompt string. For

example:

export MYSQL_PS1="(\u@\h) [\d]> "

• Use a command-line option. You can set the --prompt option on the command line to mysql. For

example:

$> mysql --prompt="(\u@\h) [\d]> "
(user@host) [database]>

• Use an option file. You can set the prompt option in the [mysql] group of any MySQL option file, such

as /etc/my.cnf or the .my.cnf file in your home directory. For example:

[mysql]
prompt=(\\u@\\h) [\\d]>\\_

In this example, note that the backslashes are doubled. If you set the prompt using the prompt option in
an option file, it is advisable to double the backslashes when using the special prompt options. There is
some overlap in the set of permissible prompt options and the set of special escape sequences that are
recognized in option files. (The rules for escape sequences in option files are listed in Section 4.2.2.2,
“Using Option Files”.) The overlap may cause you problems if you use single backslashes. For example,
\s is interpreted as a space rather than as the current seconds value. The following example shows how
to define a prompt within an option file to include the current time in hh:mm:ss> format:

[mysql]
prompt="\\r:\\m:\\s> "

• Set the prompt interactively. You can change your prompt interactively by using the prompt (or \R)

command. For example:

mysql> prompt (\u@\h) [\d]>\_
PROMPT set to '(\u@\h) [\d]>\_'
(user@host) [database]>
(user@host) [database]> prompt
Returning to default PROMPT of mysql>
mysql>

4.5.1.3 mysql Client Logging

The mysql client can do these types of logging for statements executed interactively:

• On Unix, mysql writes the statements to a history file. By default, this file is named .mysql_history
in your home directory. To specify a different file, set the value of the MYSQL_HISTFILE environment
variable.

• On all platforms, if the --syslog option is given, mysql writes the statements to the system logging
facility. On Unix, this is syslog; on Windows, it is the Windows Event Log. The destination where
logged messages appear is system dependent. On Linux, the destination is often the /var/log/
messages file.

The following discussion describes characteristics that apply to all logging types and provides information
specific to each logging type.

426

mysql — The MySQL Command-Line Client

• How Logging Occurs

• Controlling the History File

• syslog Logging Characteristics

How Logging Occurs

For each enabled logging destination, statement logging occurs as follows:

• Statements are logged only when executed interactively. Statements are noninteractive, for example,

when read from a file or a pipe. It is also possible to suppress statement logging by using the --batch
or --execute option.

• Statements are ignored and not logged if they match any pattern in the “ignore” list. This list is described

later.

• mysql logs each nonignored, nonempty statement line individually.

• If a nonignored statement spans multiple lines (not including the terminating delimiter), mysql

concatenates the lines to form the complete statement, maps newlines to spaces, and logs the result,
plus a delimiter.

Consequently, an input statement that spans multiple lines can be logged twice. Consider this input:

mysql> SELECT
    -> 'Today is'
    -> ,
    -> CURDATE()
    -> ;

In this case, mysql logs the “SELECT”, “'Today is'”, “,”, “CURDATE()”, and “;” lines as it reads them. It
also logs the complete statement, after mapping SELECT\n'Today is'\n,\nCURDATE() to SELECT
'Today is' , CURDATE(), plus a delimiter. Thus, these lines appear in logged output:

SELECT
'Today is'
,
CURDATE()
;
SELECT 'Today is' , CURDATE();

mysql ignores for logging purposes statements that match any pattern in the “ignore” list. By default, the
pattern list is "*IDENTIFIED*:*PASSWORD*", to ignore statements that refer to passwords. Pattern
matching is not case-sensitive. Within patterns, two characters are special:

• ? matches any single character.

• * matches any sequence of zero or more characters.

To specify additional patterns, use the --histignore option or set the MYSQL_HISTIGNORE
environment variable. (If both are specified, the option value takes precedence.) The value should be a list
of one or more colon-separated patterns, which are appended to the default pattern list.

Patterns specified on the command line might need to be quoted or escaped to prevent your command
interpreter from treating them specially. For example, to suppress logging for UPDATE and DELETE
statements in addition to statements that refer to passwords, invoke mysql like this:

mysql --histignore="*UPDATE*:*DELETE*"

427

mysql — The MySQL Command-Line Client

Controlling the History File

The .mysql_history file should be protected with a restrictive access mode because sensitive
information might be written to it, such as the text of SQL statements that contain passwords. See
Section 6.1.2.1, “End-User Guidelines for Password Security”. Statements in the file are accessible from
the mysql client when the up-arrow key is used to recall the history. See Disabling Interactive History.

If you do not want to maintain a history file, first remove .mysql_history if it exists. Then use either of
the following techniques to prevent it from being created again:

• Set the MYSQL_HISTFILE environment variable to /dev/null. To cause this setting to take effect each

time you log in, put it in one of your shell's startup files.

• Create .mysql_history as a symbolic link to /dev/null; this need be done only once:

ln -s /dev/null $HOME/.mysql_history

syslog Logging Characteristics

If the --syslog option is given, mysql writes interactive statements to the system logging facility.
Message logging has the following characteristics.

Logging occurs at the “information” level. This corresponds to the LOG_INFO priority for syslog on Unix/
Linux syslog capability and to EVENTLOG_INFORMATION_TYPE for the Windows Event Log. Consult
your system documentation for configuration of your logging capability.

Message size is limited to 1024 bytes.

Messages consist of the identifier MysqlClient followed by these values:

• SYSTEM_USER

The operating system user name (login name) or -- if the user is unknown.

• MYSQL_USER

The MySQL user name (specified with the --user option) or -- if the user is unknown.

• CONNECTION_ID:

The client connection identifier. This is the same as the CONNECTION_ID() function value within the
session.

• DB_SERVER

The server host or -- if the host is unknown.

• DB

The default database or -- if no database has been selected.

• QUERY

The text of the logged statement.

Here is a sample of output generated on Linux by using --syslog. This output is formatted for readability;
each logged message actually takes a single line.

Mar  7 12:39:25 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,

428

mysql — The MySQL Command-Line Client

  DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
Mar  7 12:39:28 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
  DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'

4.5.1.4 mysql Client Server-Side Help

mysql> help search_string

If you provide an argument to the help command, mysql uses it as a search string to access server-side
help from the contents of the MySQL Reference Manual. The proper operation of this command requires
that the help tables in the mysql database be initialized with help topic information (see Section 5.1.14,
“Server-Side Help Support”).

If there is no match for the search string, the search fails:

mysql> help me

Nothing found
Please try to run 'help contents' for a list of all accessible topics

Use help contents to see a list of the help categories:

mysql> help contents
You asked for help about help category: "Contents"
For more information, type 'help <item>', where <item> is one of the
following categories:
   Account Management
   Administration
   Data Definition
   Data Manipulation
   Data Types
   Functions
   Functions and Modifiers for Use with GROUP BY
   Geographic Features
   Language Structure
   Plugins
   Storage Engines
   Stored Routines
   Table Maintenance
   Transactions
   Triggers

If the search string matches multiple items, mysql shows a list of matching topics:

mysql> help logs
Many help items for your request exist.
To make a more specific request, please type 'help <item>',
where <item> is one of the following topics:
   SHOW
   SHOW BINARY LOGS
   SHOW ENGINE
   SHOW LOGS

Use a topic as the search string to see the help entry for that topic:

mysql> help show binary logs
Name: 'SHOW BINARY LOGS'
Description:
Syntax:
SHOW BINARY LOGS
SHOW MASTER LOGS

Lists the binary log files on the server. This statement is used as
part of the procedure described in [purge-binary-logs], that shows how
to determine which logs can be purged.

429

mysql — The MySQL Command-Line Client

mysql> SHOW BINARY LOGS;
+---------------+-----------+
| Log_name      | File_size |
+---------------+-----------+
| binlog.000015 |    724935 |
| binlog.000016 |    733481 |
+---------------+-----------+

The search string can contain the wildcard characters % and _. These have the same meaning as for
pattern-matching operations performed with the LIKE operator. For example, HELP rep% returns a list of
topics that begin with rep:

mysql> HELP rep%
Many help items for your request exist.
To make a more specific request, please type 'help <item>',
where <item> is one of the following
topics:
   REPAIR TABLE
   REPEAT FUNCTION
   REPEAT LOOP
   REPLACE
   REPLACE FUNCTION

4.5.1.5 Executing SQL Statements from a Text File

The mysql client typically is used interactively, like this:

mysql db_name

However, it is also possible to put your SQL statements in a file and then tell mysql to read its input from
that file. To do so, create a text file text_file that contains the statements you wish to execute. Then
invoke mysql as shown here:

mysql db_name < text_file

If you place a USE db_name statement as the first statement in the file, it is unnecessary to specify the
database name on the command line:

mysql < text_file

If you are already running mysql, you can execute an SQL script file using the source command or \.
command:

mysql> source file_name
mysql> \. file_name

Sometimes you may want your script to display progress information to the user. For this you can insert
statements like this:

SELECT '<info_to_display>' AS ' ';

The statement shown outputs <info_to_display>.

You can also invoke mysql with the --verbose option, which causes each statement to be displayed
before the result that it produces.

mysql ignores Unicode byte order mark (BOM) characters at the beginning of input files. Previously, it
read them and sent them to the server, resulting in a syntax error. Presence of a BOM does not cause
mysql to change its default character set. To do that, invoke mysql with an option such as --default-
character-set=utf8.

For more information about batch mode, see Section 3.5, “Using mysql in Batch Mode”.

430

mysql — The MySQL Command-Line Client

4.5.1.6 mysql Client Tips

This section provides information about techniques for more effective use of mysql and about mysql
operational behavior.

• Input-Line Editing

• Disabling Interactive History

• Unicode Support on Windows

• Displaying Query Results Vertically

• Using Safe-Updates Mode (--safe-updates)

• Disabling mysql Auto-Reconnect

• mysql Client Parser Versus Server Parser

Input-Line Editing

mysql supports input-line editing, which enables you to modify the current input line in place or recall
previous input lines. For example, the left-arrow and right-arrow keys move horizontally within the current
input line, and the up-arrow and down-arrow keys move up and down through the set of previously
entered lines. Backspace deletes the character before the cursor and typing new characters enters them
at the cursor position. To enter the line, press Enter.

On Windows, the editing key sequences are the same as supported for command editing in console
windows. On Unix, the key sequences depend on the input library used to build mysql (for example, the
libedit or readline library).

Documentation for the libedit and readline libraries is available online. To change the set of key
sequences permitted by a given input library, define key bindings in the library startup file. This is a file in
your home directory: .editrc for libedit and .inputrc for readline.

For example, in libedit, Control+W deletes everything before the current cursor position and Control
+U deletes the entire line. In readline, Control+W deletes the word before the cursor and Control
+U deletes everything before the current cursor position. If mysql was built using libedit, a user who
prefers the readline behavior for these two keys can put the following lines in the .editrc file (creating
the file if necessary):

bind "^W" ed-delete-prev-word
bind "^U" vi-kill-line-prev

To see the current set of key bindings, temporarily put a line that says only bind at the end of .editrc.
Then mysql shows the bindings when it starts.

Disabling Interactive History

The up-arrow key enables you to recall input lines from current and previous sessions. In cases where
a console is shared, this behavior may be unsuitable. mysql supports disabling the interactive history
partially or fully, depending on the host platform.

On Windows, the history is stored in memory. Alt+F7 deletes all input lines stored in memory for the
current history buffer. It also deletes the list of sequential numbers in front of the input lines displayed with
F7 and recalled (by number) with F9. New input lines entered after you press Alt+F7 repopulate the current
history buffer. Clearing the buffer does not prevent logging to the Windows Event Viewer, if the --syslog
option was used to start mysql. Closing the console window also clears the current history buffer.

431

mysql — The MySQL Command-Line Client

To disable interactive history on Unix, first delete the .mysql_history file, if it exists (previous entries
are recalled otherwise). Then start mysql with the --histignore="*" option to ignore all new input
lines. To re-enable the recall (and logging) behavior, restart mysql without the option.

If you prevent the .mysql_history file from being created (see Controlling the History File) and use
--histignore="*" to start the mysql client, the interactive history recall facility is disabled fully.
Alternatively, if you omit the --histignore option, you can recall the input lines entered during the
current session.

Unicode Support on Windows

Windows provides APIs based on UTF-16LE for reading from and writing to the console; the mysql client
for Windows is able to use these APIs. The Windows installer creates an item in the MySQL menu named
MySQL command line client - Unicode. This item invokes the mysql client with properties set to
communicate through the console to the MySQL server using Unicode.

To take advantage of this support manually, run mysql within a console that uses a compatible Unicode
font and set the default character set to a Unicode character set that is supported for communication with
the server:

1. Open a console window.

2. Go to the console window properties, select the font tab, and choose Lucida Console or some other
compatible Unicode font. This is necessary because console windows start by default using a DOS
raster font that is inadequate for Unicode.

3. Execute mysql.exe with the --default-character-set=utf8 (or utf8mb4) option. This option

is necessary because utf16le is one of the character sets that cannot be used as the client character
set. See Impermissible Client Character Sets.

With those changes, mysql can use the Windows APIs to communicate with the console using UTF-16LE,
and communicate with the server using UTF-8. (The menu item mentioned previously sets the font and
character set as just described.)

To avoid those steps each time you run mysql, you can create a shortcut that invokes mysql.exe. The
shortcut should set the console font to Lucida Console or some other compatible Unicode font, and pass
the --default-character-set=utf8 (or utf8mb4) option to mysql.exe.

Alternatively, create a shortcut that only sets the console font, and set the character set in the [mysql]
group of your my.ini file:

[mysql]
default-character-set=utf8

Displaying Query Results Vertically

Some query results are much more readable when displayed vertically, instead of in the usual horizontal
table format. Queries can be displayed vertically by terminating the query with \G instead of a semicolon.
For example, longer text values that include newlines often are much easier to read with vertical output:

mysql> SELECT * FROM mails WHERE LENGTH(txt) < 300 LIMIT 300,1\G
*************************** 1. row ***************************
  msg_nro: 3068
     date: 2000-03-01 23:29:50
time_zone: +0200
mail_from: Jones
    reply: jones@example.com
  mail_to: "John Smith" <smith@example.com>
      sbj: UTF-8

432

mysql — The MySQL Command-Line Client

      txt: >>>>> "John" == John Smith writes:

John> Hi.  I think this is a good idea.  Is anyone familiar
John> with UTF-8 or Unicode? Otherwise, I'll put this on my
John> TODO list and see what happens.

Yes, please do that.

Regards,
Jones
     file: inbox-jani-1
     hash: 190402944
1 row in set (0.09 sec)

Using Safe-Updates Mode (--safe-updates)

For beginners, a useful startup option is --safe-updates (or --i-am-a-dummy, which has the same
effect). Safe-updates mode is helpful for cases when you might have issued an UPDATE or DELETE
statement but forgotten the WHERE clause indicating which rows to modify. Normally, such statements
update or delete all rows in the table. With --safe-updates, you can modify rows only by specifying
the key values that identify them, or a LIMIT clause, or both. This helps prevent accidents. Safe-updates
mode also restricts SELECT statements that produce (or are estimated to produce) very large result sets.

The --safe-updates option causes mysql to execute the following statement when it connects to
the MySQL server, to set the session values of the sql_safe_updates, sql_select_limit, and
max_join_size system variables:

SET sql_safe_updates=1, sql_select_limit=1000, max_join_size=1000000;

The SET statement affects statement processing as follows:

• Enabling sql_safe_updates causes UPDATE and DELETE statements to produce an error if they do
not specify a key constraint in the WHERE clause, or provide a LIMIT clause, or both. For example:

UPDATE tbl_name SET not_key_column=val WHERE key_column=val;

UPDATE tbl_name SET not_key_column=val LIMIT 1;

• Setting sql_select_limit to 1,000 causes the server to limit all SELECT result sets to 1,000 rows

unless the statement includes a LIMIT clause.

• Setting max_join_size to 1,000,000 causes multiple-table SELECT statements to produce an error if

the server estimates it must examine more than 1,000,000 row combinations.

To specify result set limits different from 1,000 and 1,000,000, you can override the defaults by using the
--select-limit and --max-join-size options when you invoke mysql:

mysql --safe-updates --select-limit=500 --max-join-size=10000

It is possible for UPDATE and DELETE statements to produce an error in safe-updates mode even with a
key specified in the WHERE clause, if the optimizer decides not to use the index on the key column:

• Range access on the index cannot be used if memory usage exceeds that permitted by the

range_optimizer_max_mem_size system variable. The optimizer then falls back to a table scan.
See Limiting Memory Use for Range Optimization.

• If key comparisons require type conversion, the index may not be used (see Section 8.3.1, “How MySQL
Uses Indexes”). Suppose that an indexed string column c1 is compared to a numeric value using WHERE
c1 = 2222. For such comparisons, the string value is converted to a number and the operands are
compared numerically (see Section 12.3, “Type Conversion in Expression Evaluation”), preventing use
of the index. If safe-updates mode is enabled, an error occurs.

433

mysql — The MySQL Command-Line Client

As of MySQL 5.7.25, safe-updates mode also includes these behaviors:

• EXPLAIN with UPDATE and DELETE statements does not produce safe-updates errors. This enables use
of EXPLAIN plus SHOW WARNINGS to see why an index is not used, which can be helpful in cases such
as when a range_optimizer_max_mem_size violation or type conversion occurs and the optimizer
does not use an index even though a key column was specified in the WHERE clause.

• When a safe-updates error occurs, the error message includes the first diagnostic that was produced,
to provide information about the reason for failure. For example, the message may indicate that the
range_optimizer_max_mem_size value was exceeded or type conversion occurred, either of which
can preclude use of an index.

• For multiple-table deletes and updates, an error is produced with safe updates enabled only if any target

table uses a table scan.

Disabling mysql Auto-Reconnect

If the mysql client loses its connection to the server while sending a statement, it immediately and
automatically tries to reconnect once to the server and send the statement again. However, even if mysql
succeeds in reconnecting, your first connection has ended and all your previous session objects and
settings are lost: temporary tables, the autocommit mode, and user-defined and session variables. Also,
any current transaction rolls back. This behavior may be dangerous for you, as in the following example
where the server was shut down and restarted between the first and second statements without you
knowing it:

mysql> SET @a=1;
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES(@a);
ERROR 2006: MySQL server has gone away
No connection. Trying to reconnect...
Connection id:    1
Current database: test

Query OK, 1 row affected (1.30 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
| NULL |
+------+
1 row in set (0.05 sec)

The @a user variable has been lost with the connection, and after the reconnection it is undefined. If it is
important to have mysql terminate with an error if the connection has been lost, you can start the mysql
client with the --skip-reconnect option.

For more information about auto-reconnect and its effect on state information when a reconnection occurs,
see Automatic Reconnection Control.

mysql Client Parser Versus Server Parser

The mysql client uses a parser on the client side that is not a duplicate of the complete parser used by
the mysqld server on the server side. This can lead to differences in treatment of certain constructs.
Examples:

• The server parser treats strings delimited by " characters as identifiers rather than as plain strings if the

ANSI_QUOTES SQL mode is enabled.

434

mysqladmin — A MySQL Server Administration Program

The mysql client parser does not take the ANSI_QUOTES SQL mode into account. It treats strings
delimited by ", ', and ` characters the same, regardless of whether ANSI_QUOTES is enabled.

• Within /*! ... */ comments, the mysql client parser interprets short-form mysql commands. The
server parser does not interpret them because these commands have no meaning on the server side.

If it is desirable for mysql not to interpret short-form commands within comments, a partial workaround
is to use the --binary-mode option, which causes all mysql commands to be disabled except \C and
\d in noninteractive mode (for input piped to mysql or loaded using the source command).

4.5.2 mysqladmin — A MySQL Server Administration Program

mysqladmin is a client for performing administrative operations. You can use it to check the server's
configuration and current status, to create and drop databases, and more.

Invoke mysqladmin like this:

mysqladmin [options] command [command-arg] [command [command-arg]] ...

mysqladmin supports the following commands. Some of the commands take an argument following the
command name.

• create db_name

Create a new database named db_name.

• debug

Tell the server to write debug information to the error log. The connected user must have the SUPER
privilege. Format and content of this information is subject to change.

This includes information about the Event Scheduler. See Section 23.4.5, “Event Scheduler Status”.

• drop db_name

Delete the database named db_name and all its tables.

• extended-status

Display the server status variables and their values.

• flush-hosts

Flush all information in the host cache. See Section 5.1.11.2, “DNS Lookups and the Host Cache”.

• flush-logs [log_type ...]

Flush all logs.

The mysqladmin flush-logs command permits optional log types to be given, to specify which logs
to flush. Following the flush-logs command, you can provide a space-separated list of one or more of
the following log types: binary, engine, error, general, relay, slow. These correspond to the log
types that can be specified for the FLUSH LOGS SQL statement.

• flush-privileges

Reload the grant tables (same as reload).

• flush-status

435

mysqladmin — A MySQL Server Administration Program

Clear status variables.

• flush-tables

Flush all tables.

• flush-threads

Flush the thread cache.

• kill id,id,...

Kill server threads. If multiple thread ID values are given, there must be no spaces in the list.

To kill threads belonging to other users, the connected user must have the SUPER privilege.

• old-password new_password

This is like the password command but stores the password using the old (pre-4.1) password-hashing
format. (See Section 6.1.2.4, “Password Hashing in MySQL”.)

This command was removed in MySQL 5.7.5.

• password new_password

Set a new password. This changes the password to new_password for the account that you use with
mysqladmin for connecting to the server. Thus, the next time you invoke mysqladmin (or any other
client program) using the same account, you must specify the new password.

Warning

Setting a password using mysqladmin should be considered insecure. On some
systems, your password becomes visible to system status programs such as ps
that may be invoked by other users to display command lines. MySQL clients
typically overwrite the command-line password argument with zeros during their
initialization sequence. However, there is still a brief interval during which the
value is visible. Also, on some systems this overwriting strategy is ineffective and
the password remains visible to ps. (SystemV Unix systems and perhaps others
are subject to this problem.)

If the new_password value contains spaces or other characters that are special to your command
interpreter, you need to enclose it within quotation marks. On Windows, be sure to use double quotation
marks rather than single quotation marks; single quotation marks are not stripped from the password, but
rather are interpreted as part of the password. For example:

mysqladmin password "my new password"

The new password can be omitted following the password command. In this case, mysqladmin
prompts for the password value, which enables you to avoid specifying the password on the command
line. Omitting the password value should be done only if password is the final command on the
mysqladmin command line. Otherwise, the next argument is taken as the password.

Caution

Do not use this command used if the server was started with the --skip-
grant-tables option. No password change is applied. This is true even if
you precede the password command with flush-privileges on the same

436

mysqladmin — A MySQL Server Administration Program

command line to re-enable the grant tables because the flush operation occurs
after you connect. However, you can use mysqladmin flush-privileges
to re-enable the grant table and then use a separate mysqladmin password
command to change the password.

• ping

Check whether the server is available. The return status from mysqladmin is 0 if the server is running,
1 if it is not. This is 0 even in case of an error such as Access denied, because this means that the
server is running but refused the connection, which is different from the server not running.

• processlist

Show a list of active server threads. This is like the output of the SHOW PROCESSLIST statement.
If the --verbose option is given, the output is like that of SHOW FULL PROCESSLIST. (See
Section 13.7.5.29, “SHOW PROCESSLIST Statement”.)

• reload

Reload the grant tables.

• refresh

Flush all tables and close and open log files.

• shutdown

Stop the server.

• start-slave

Start replication on a replica server.

• status

Display a short server status message.

• stop-slave

Stop replication on a replica server.

• variables

Display the server system variables and their values.

• version

Display version information from the server.

All commands can be shortened to any unique prefix. For example:

$> mysqladmin proc stat
+----+-------+-----------+----+---------+------+-------+------------------+
| Id | User  | Host      | db | Command | Time | State | Info             |
+----+-------+-----------+----+---------+------+-------+------------------+
| 51 | jones | localhost |    | Query   | 0    |       | show processlist |
+----+-------+-----------+----+---------+------+-------+------------------+
Uptime: 1473624  Threads: 1  Questions: 39487
Slow queries: 0  Opens: 541  Flush tables: 1
Open tables: 19  Queries per second avg: 0.0268

437

mysqladmin — A MySQL Server Administration Program

The mysqladmin status command result displays the following values:

•  Uptime

The number of seconds the MySQL server has been running.

•  Threads

The number of active threads (clients).

•  Questions

The number of questions (queries) from clients since the server was started.

•  Slow queries

The number of queries that have taken more than long_query_time seconds. See Section 5.4.5, “The
Slow Query Log”.

•  Opens

The number of tables the server has opened.

•   Flush tables

The number of flush-*, refresh, and reload commands the server has executed.

•  Open tables

The number of tables that currently are open.

If you execute mysqladmin shutdown when connecting to a local server using a Unix socket file,
mysqladmin waits until the server's process ID file has been removed, to ensure that the server has
stopped properly.

mysqladmin supports the following options, which can be specified on the command line or in the
[mysqladmin] and [client] groups of an option file. For information about option files used by MySQL
programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.14 mysqladmin Options

Option Name

--bind-address

--character-sets-dir

--compress

--connect-timeout

--count

438

Description

Introduced

Deprecated

Use specified network
interface to connect to
MySQL Server

Directory where
character sets can be
found

Compress all information
sent between client and
server

Number of seconds
before connection
timeout

Number of iterations
to make for repeated
command execution

mysqladmin — A MySQL Server Administration Program

Option Name

Description

Introduced

Deprecated

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

Write debugging log

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Specify default character
set

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--enable-cleartext-plugin Enable cleartext

--force

authentication plugin

Continue even if an SQL
error occurs

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--host

--login-path

--no-beep

--no-defaults

--password

--pipe

--plugin-dir

--port

Display help message
and exit

Host on which MySQL
server is located

Read login path options
from .mylogin.cnf

Do not beep when errors
occur

Read no option files

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--protocol

Transport protocol to use

439

mysqladmin — A MySQL Server Administration Program

Option Name

Description

Introduced

Deprecated

--relative

--secure-auth

Show the difference
between the current and
previous values when
used with the --sleep
option

Do not send passwords
to server in old (pre-4.1)
format

--server-public-key-path Path name to file

5.7.23

Yes

--shared-memory-base-
name

--show-warnings

--shutdown-timeout

--silent

--sleep

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

containing RSA public
key

Shared-memory name
for shared-memory
connections (Windows
only)

Show warnings after
statement execution

The maximum number of
seconds to wait for server
shutdown

Silent mode

Execute commands
repeatedly, sleeping
for delay seconds in
between

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

440

mysqladmin — A MySQL Server Administration Program

Option Name

Description

Introduced

Deprecated

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--tls-version

--user

--verbose

--version

--vertical

--wait

• --help, -?

File that contains X.509
key

Desired security state of
connection to server

5.7.11

5.7.10

Verify host name
against server certificate
Common Name identity

Permissible TLS
protocols for encrypted
connections

MySQL user name to
use when connecting to
server

Verbose mode

Display version
information and exit

Print query output rows
vertically (one line per
column value)

If the connection cannot
be established, wait and
retry instead of aborting

Command-Line Format

--help

Display a help message and exit.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=path

Type

Default Value

String

[none]

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

441

mysqladmin — A MySQL Server Administration Program

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --connect-timeout=value

Command-Line Format

--connect-timeout=value

Type

Default Value

Numeric

43200

The maximum number of seconds before connection timeout. The default value is 43200 (12 hours).

• --count=N, -c N

Command-Line Format

--count=#

The number of iterations to make for repeated command execution if the --sleep option is given.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o,/tmp/mysqladmin.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/mysqladmin.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

442

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info

Command-Line Format

Type

--debug-info

Boolean

mysqladmin — A MySQL Server Administration Program

Default Value

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

443

mysqladmin — A MySQL Server Administration Program

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqladmin normally reads the [client] and [mysqladmin] groups. If this option is
given as --defaults-group-suffix=_other, mysqladmin also reads the [client_other] and
[mysqladmin_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

• --force, -f

Command-Line Format

--force

Do not ask for confirmation for the drop db_name command. With multiple commands, continue even if
an error occurs.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that
plugin, the server does not send the public key unless requested. This option is ignored for accounts that
do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

String

444

mysqladmin — A MySQL Server Administration Program

Default Value

localhost

Connect to the MySQL server on the given host.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-beep, -b

Command-Line Format

--no-beep

Suppress the warning beep that is emitted by default for errors such as a failure to connect to the server.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

445

mysqladmin — A MySQL Server Administration Program

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqladmin prompts for one. If given, there must be no space between --password= or
-p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqladmin should not prompt for one, use the
--skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqladmin does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

446

mysqladmin — A MySQL Server Administration Program

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --relative, -r

Command-Line Format

--relative

Show the difference between the current and previous values when used with the --sleep option. This
option works only with the extended-status command.

• --show-warnings

Command-Line Format

--show-warnings

Show warnings resulting from execution of statements sent to the server.

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

447

mysqladmin — A MySQL Server Administration Program

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --shutdown-timeout=value

Command-Line Format

--shutdown-timeout=seconds

Type

Default Value

Numeric

3600

The maximum number of seconds to wait for server shutdown. The default value is 3600 (1 hour).

• --silent, -s

Command-Line Format

--silent

448

Exit silently if a connection to the server cannot be established.

mysqladmin — A MySQL Server Administration Program

• --sleep=delay, -i delay

Command-Line Format

--sleep=delay

Execute commands repeatedly, sleeping for delay seconds in between. The --count option
determines the number of iterations. If --count is not given, mysqladmin executes commands
indefinitely until interrupted.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

• --verbose, -v

449

mysqlcheck — A Table Maintenance Program

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --vertical, -E

Command-Line Format

--vertical

Print output vertically. This is similar to --relative, but prints output vertically.

• --wait[=count], -w[count]

Command-Line Format

--wait

If the connection cannot be established, wait and retry instead of aborting. If a count value is given, it
indicates the number of times to retry. The default is one time.

4.5.3 mysqlcheck — A Table Maintenance Program

The mysqlcheck client performs table maintenance: It checks, repairs, optimizes, or analyzes tables.

Each table is locked and therefore unavailable to other sessions while it is being processed, although
for check operations, the table is locked with a READ lock only (see Section 13.3.5, “LOCK TABLES and
UNLOCK TABLES Statements”, for more information about READ and WRITE locks). Table maintenance
operations can be time-consuming, particularly for large tables. If you use the --databases or --all-
databases option to process all tables in one or more databases, an invocation of mysqlcheck might
take a long time. (This is also true for the MySQL upgrade procedure if it determines that table checking is
needed because it processes tables the same way.)

mysqlcheck must be used when the mysqld server is running, which means that you do not have to stop
the server to perform table maintenance.

mysqlcheck uses the SQL statements CHECK TABLE, REPAIR TABLE, ANALYZE TABLE, and
OPTIMIZE TABLE in a convenient way for the user. It determines which statements to use for the
operation you want to perform, and then sends the statements to the server to be executed. For details
about which storage engines each statement works with, see the descriptions for those statements in
Section 13.7.2, “Table Maintenance Statements”.

All storage engines do not necessarily support all four maintenance operations. In such cases, an error
message is displayed. For example, if test.t is an MEMORY table, an attempt to check it produces this
result:

$> mysqlcheck test t
test.t
note     : The storage engine for the table doesn't support check

450

mysqlcheck — A Table Maintenance Program

If mysqlcheck is unable to repair a table, see Section 2.10.12, “Rebuilding or Repairing Tables or
Indexes” for manual table repair strategies. This is the case, for example, for InnoDB tables, which can be
checked with CHECK TABLE, but not repaired with REPAIR TABLE.

Caution

It is best to make a backup of a table before performing a table repair operation;
under some circumstances the operation might cause data loss. Possible causes
include but are not limited to file system errors.

There are three general ways to invoke mysqlcheck:

mysqlcheck [options] db_name [tbl_name ...]
mysqlcheck [options] --databases db_name ...
mysqlcheck [options] --all-databases

If you do not name any tables following db_name or if you use the --databases or --all-databases
option, entire databases are checked.

mysqlcheck has a special feature compared to other client programs. The default behavior of checking
tables (--check) can be changed by renaming the binary. If you want to have a tool that repairs tables by
default, you should just make a copy of mysqlcheck named mysqlrepair, or make a symbolic link to
mysqlcheck named mysqlrepair. If you invoke mysqlrepair, it repairs tables.

The names shown in the following table can be used to change mysqlcheck default behavior.

Command

mysqlrepair

mysqlanalyze

mysqloptimize

Meaning

The default option is --repair

The default option is --analyze

The default option is --optimize

mysqlcheck supports the following options, which can be specified on the command line or in the
[mysqlcheck] and [client] groups of an option file. For information about option files used by MySQL
programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.15 mysqlcheck Options

Option Name

--all-databases

--all-in-1

--analyze

--auto-repair

--bind-address

Description

Introduced

Deprecated

Check all tables in all
databases

Execute a single
statement for each
database that names
all the tables from that
database

Analyze the tables

If a checked table is
corrupted, automatically
fix it

Use specified network
interface to connect to
MySQL Server

451

mysqlcheck — A Table Maintenance Program

Option Name

Description

Introduced

Deprecated

--character-sets-dir

--check

--check-only-changed

--check-upgrade

--compress

--databases

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

Directory where
character sets are
installed

Check the tables for
errors

Check only tables that
have changed since the
last check

Invoke CHECK TABLE
with the FOR UPGRADE
option

Compress all information
sent between client and
server

Interpret all arguments as
database names

Write debugging log

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Specify default character
set

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--enable-cleartext-plugin Enable cleartext

5.7.10

--extended

--fast

--fix-db-names

--fix-table-names

authentication plugin

Check and repair tables

Check only tables that
have not been closed
properly

Convert database names
to 5.1 format

Convert table names to
5.1 format

Yes

Yes

452

mysqlcheck — A Table Maintenance Program

Option Name

Description

Introduced

Deprecated

--force

Continue even if an SQL
error occurs

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--host

--login-path

--medium-check

--no-defaults

--optimize

--password

--pipe

--plugin-dir

--port

Display help message
and exit

Host on which MySQL
server is located

Read login path options
from .mylogin.cnf

Do a check that is faster
than an --extended
operation

Read no option files

Optimize the tables

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--protocol

--quick

--repair

--secure-auth

Transport protocol to use

The fastest method of
checking

Perform a repair that
can fix almost anything
except unique keys that
are not unique

Do not send passwords
to server in old (pre-4.1)
format

--server-public-key-path Path name to file

5.7.23

--shared-memory-base-
name

containing RSA public
key

Shared-memory name
for shared-memory
connections (Windows
only)

--silent

Silent mode

Yes

453

mysqlcheck — A Table Maintenance Program

Description

Introduced

Deprecated

Omit this database from
performed operations

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

5.7.10

Verify host name
against server certificate
Common Name identity

Overrides the --
databases or -B option

Permissible TLS
protocols for encrypted
connections

For repair operations on
MyISAM tables

MySQL user name to
use when connecting to
server

Verbose mode

Display version
information and exit

Log ANALYZE,
OPTIMIZE, REPAIR
statements to binary log.

Option Name

--skip-database

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--tables

--tls-version

--use-frm

--user

--verbose

--version

--write-binlog

454

mysqlcheck — A Table Maintenance Program

Option Name

• --help, -?

Description
--skip-write-binlog adds
NO_WRITE_TO_BINLOG
to these statements

Introduced

Deprecated

Command-Line Format

--help

Display a help message and exit.

• --all-databases, -A

Command-Line Format

--all-databases

Check all tables in all databases. This is the same as using the --databases option and naming all the
databases on the command line, except that the INFORMATION_SCHEMA and performance_schema
databases are not checked. They can be checked by explicitly naming them with the --databases
option.

• --all-in-1, -1

Command-Line Format

--all-in-1

Instead of issuing a statement for each table, execute a single statement for each database that names
all the tables from that database to be processed.

• --analyze, -a

Command-Line Format

--analyze

Analyze the tables.

• --auto-repair

Command-Line Format

--auto-repair

If a checked table is corrupted, automatically fix it. Any necessary repairs are done after all tables have
been checked.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

455

mysqlcheck — A Table Maintenance Program

Type

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --check, -c

Command-Line Format

--check

Check the tables for errors. This is the default operation.

• --check-only-changed, -C

Command-Line Format

--check-only-changed

Check only tables that have changed since the last check or that have not been closed properly.

• --check-upgrade, -g

Command-Line Format

--check-upgrade

Invoke CHECK TABLE with the FOR UPGRADE option to check tables for incompatibilities with the current
version of the server. This option automatically enables the --fix-db-names and --fix-table-
names options.

• --compress

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --databases, -B

Command-Line Format

--databases

Process all tables in the named databases. Normally, mysqlcheck treats the first name argument on
the command line as a database name and any following names as table names. With this option, it
treats all name arguments as database names.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o.

456

mysqlcheck — A Table Maintenance Program

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

457

mysqlcheck — A Table Maintenance Program

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqlcheck normally reads the [client] and [mysqlcheck] groups. If this option is
given as --defaults-group-suffix=_other, mysqlcheck also reads the [client_other] and
[mysqlcheck_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --extended, -e

Command-Line Format

--extended

If you are using this option to check tables, it ensures that they are 100% consistent but takes a long
time.

If you are using this option to repair tables, it runs an extended repair that may not only take a long time
to execute, but may produce a lot of garbage rows also!

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Introduced

Type

5.7.10

Boolean

458

mysqlcheck — A Table Maintenance Program

Default Value

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

This option was added in MySQL 5.7.10.

• --fast, -F

Command-Line Format

--fast

Check only tables that have not been closed properly.

• --fix-db-names

Command-Line Format

Deprecated

--fix-db-names

Yes

Convert database names to 5.1 format. Only database names that contain special characters are
affected.

This option is deprecated in MySQL 5.7.6; expect it to be removed in a future version of MySQL. If it is
necessary to convert MySQL 5.0 database or table names, a workaround is to upgrade a MySQL 5.0
installation to MySQL 5.1 before upgrading to a more recent release.

• --fix-table-names

Command-Line Format

Deprecated

--fix-table-names

Yes

Convert table names to 5.1 format. Only table names that contain special characters are affected. This
option also applies to views.

This option is deprecated in MySQL 5.7.6; expect it to be removed in a future version of MySQL. If it is
necessary to convert MySQL 5.0 database or table names, a workaround is to upgrade a MySQL 5.0
installation to MySQL 5.1 before upgrading to a more recent release.

• --force, -f

Command-Line Format

--force

Continue even if an SQL error occurs.

• --get-server-public-key

459

Command-Line Format

Introduced

--get-server-public-key

5.7.23

mysqlcheck — A Table Maintenance Program

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that
plugin, the server does not send the public key unless requested. This option is ignored for accounts that
do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Connect to the MySQL server on the given host.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --medium-check, -m

Command-Line Format

--medium-check

Do a check that is faster than an --extended operation. This finds only 99.99% of all errors, which
should be good enough in most cases.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

460

mysqlcheck — A Table Maintenance Program

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --optimize, -o

Command-Line Format

--optimize

Optimize the tables.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqlcheck prompts for one. If given, there must be no space between --password= or
-p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlcheck should not prompt for one, use the
--skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlcheck does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

461

mysqlcheck — A Table Maintenance Program

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --quick, -q

Command-Line Format

--quick

If you are using this option to check tables, it prevents the check from scanning the rows to check for
incorrect links. This is the fastest check method.

If you are using this option to repair tables, it tries to repair only the index tree. This is the fastest repair
method.

• --repair, -r

Command-Line Format

--repair

Perform a repair that can fix almost anything except unique keys that are not unique.

• --secure-auth

462

mysqlcheck — A Table Maintenance Program

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --shared-memory-base-name=name

Command-Line Format

--shared-memory-base-name=name

463

mysqlcheck — A Table Maintenance Program

Platform Specific

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --silent, -s

Command-Line Format

--silent

Silent mode. Print only error messages.

• --skip-database=db_name

Command-Line Format

--skip-database=db_name

Do not include the named database (case-sensitive) in the operations performed by mysqlcheck.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tables

Command-Line Format

--tables

Override the --databases or -B option. All name arguments following the option are regarded as table
names.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

5.7.10

String

Default Value (≥ 5.7.28)

TLSv1,TLSv1.1,TLSv1.2

464

mysqldump — A Database Backup Program

Default Value (≤ 5.7.27)

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --use-frm

Command-Line Format

--use-frm

For repair operations on MyISAM tables, get the table structure from the .frm file so that the table can
be repaired even if the .MYI header is corrupted.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print information about the various stages of program operation.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --write-binlog

Command-Line Format

--write-binlog

This option is enabled by default, so that ANALYZE TABLE, OPTIMIZE TABLE, and REPAIR TABLE
statements generated by mysqlcheck are written to the binary log. Use --skip-write-binlog to
cause NO_WRITE_TO_BINLOG to be added to the statements so that they are not logged. Use the --
skip-write-binlog when these statements should not be sent to replicas or run when using the
binary logs for recovery from backup.

465

4.5.4 mysqldump — A Database Backup Program

mysqldump — A Database Backup Program

The mysqldump client utility performs logical backups, producing a set of SQL statements that can be
executed to reproduce the original database object definitions and table data. It dumps one or more
MySQL databases for backup or transfer to another SQL server. The mysqldump command can also
generate output in CSV, other delimited text, or XML format.

• Performance and Scalability Considerations

• Invocation Syntax

• Option Syntax - Alphabetical Summary

• Connection Options

• Option-File Options

• DDL Options

• Debug Options

• Help Options

• Internationalization Options

• Replication Options

• Format Options

• Filtering Options

• Performance Options

• Transactional Options

• Option Groups

• Examples

• Restrictions

mysqldump requires at least the SELECT privilege for dumped tables, SHOW VIEW for dumped views,
TRIGGER for dumped triggers, LOCK TABLES if the --single-transaction option is not used, and (as
of MySQL 5.7.31) PROCESS if the --no-tablespaces option is not used. Certain options might require
other privileges as noted in the option descriptions.

To reload a dump file, you must have the privileges required to execute the statements that it contains,
such as the appropriate CREATE privileges for objects created by those statements.

mysqldump output can include ALTER DATABASE statements that change the database collation. These
may be used when dumping stored programs to preserve their character encodings. To reload a dump file
containing such statements, the ALTER privilege for the affected database is required.

Note

A dump made using PowerShell on Windows with output redirection creates a file
that has UTF-16 encoding:

mysqldump [options] > dump.sql

However, UTF-16 is not permitted as a connection character set (see Impermissible
Client Character Sets), so the dump file cannot be loaded correctly. To work around

466

mysqldump — A Database Backup Program

this issue, use the --result-file option, which creates the output in ASCII
format:

mysqldump [options] --result-file=dump.sql

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid_mode=ON), if your
dump file includes system tables. mysqldump issues DML instructions for the system tables which use the
non-transactional MyISAM storage engine, and this combination is not permitted when GTIDs are enabled.

Performance and Scalability Considerations

mysqldump advantages include the convenience and flexibility of viewing or even editing the output before
restoring. You can clone databases for development and DBA work, or produce slight variations of an
existing database for testing. It is not intended as a fast or scalable solution for backing up substantial
amounts of data. With large data sizes, even if the backup step takes a reasonable time, restoring the data
can be very slow because replaying the SQL statements involves disk I/O for insertion, index creation, and
so on.

For large-scale backup and restore, a physical backup is more appropriate, to copy the data files in their
original format that can be restored quickly:

• If your tables are primarily InnoDB tables, or if you have a mix of InnoDB and MyISAM tables, consider
using the mysqlbackup command of the MySQL Enterprise Backup product. (Available as part of the
Enterprise subscription.) It provides the best performance for InnoDB backups with minimal disruption; it
can also back up tables from MyISAM and other storage engines; and it provides a number of convenient
options to accommodate different backup scenarios. See Section 28.1, “MySQL Enterprise Backup
Overview”.

mysqldump can retrieve and dump table contents row by row, or it can retrieve the entire content from a
table and buffer it in memory before dumping it. Buffering in memory can be a problem if you are dumping
large tables. To dump tables row by row, use the --quick option (or --opt, which enables --quick).
The --opt option (and hence --quick) is enabled by default, so to enable memory buffering, use --
skip-quick.

If you are using a recent version of mysqldump to generate a dump to be reloaded into a very old MySQL
server, use the --skip-opt option instead of the --opt or --extended-insert option.

For additional information about mysqldump, see Section 7.4, “Using mysqldump for Backups”.

Invocation Syntax

There are in general three ways to use mysqldump—in order to dump a set of one or more tables, a set of
one or more complete databases, or an entire MySQL server—as shown here:

mysqldump [options] db_name [tbl_name ...]
mysqldump [options] --databases db_name ...
mysqldump [options] --all-databases

To dump entire databases, do not name any tables following db_name, or use the --databases or --
all-databases option.

To see a list of the options your version of mysqldump supports, issue the command mysqldump --
help.

Option Syntax - Alphabetical Summary

mysqldump supports the following options, which can be specified on the command line or in the
[mysqldump] and [client] groups of an option file. For information about option files used by MySQL
programs, see Section 4.2.2.2, “Using Option Files”.

467

mysqldump — A Database Backup Program

Table 4.16 mysqldump Options

Option Name

Description

Introduced

Deprecated

--add-drop-database

--add-drop-table

--add-drop-trigger

--add-locks

--all-databases

--allow-keywords

Add DROP DATABASE
statement before each
CREATE DATABASE
statement

Add DROP TABLE
statement before
each CREATE TABLE
statement

Add DROP TRIGGER
statement before each
CREATE TRIGGER
statement

Surround each table
dump with LOCK
TABLES and UNLOCK
TABLES statements

Dump all tables in all
databases

Allow creation of column
names that are keywords

--apply-slave-statements Include STOP SLAVE

--bind-address

--character-sets-dir

--comments

--compact

--compatible

--complete-insert

--compress

prior to CHANGE
MASTER statement and
START SLAVE at end of
output

Use specified network
interface to connect to
MySQL Server

Directory where
character sets are
installed

Add comments to dump
file

Produce more compact
output

Produce output that is
more compatible with
other database systems
or with older MySQL
servers

Use complete INSERT
statements that include
column names

Compress all information
sent between client and
server

468

Option Name

--create-options

--databases

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

mysqldump — A Database Backup Program

Description

Introduced

Deprecated

Include all MySQL-
specific table options
in CREATE TABLE
statements

Interpret all name
arguments as database
names

Write debugging log

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Specify default character
set

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--delete-master-logs

--disable-keys

--dump-date

--dump-slave

On a replication source
server, delete the binary
logs after performing the
dump operation

For each table, surround
INSERT statements with
statements to disable and
enable keys

Include dump date as
"Dump completed on"
comment if --comments
is given

Include CHANGE
MASTER statement
that lists binary log
coordinates of replica's
source

--enable-cleartext-plugin Enable cleartext

5.7.10

--events

authentication plugin

Dump events from
dumped databases

469

mysqldump — A Database Backup Program

Option Name

Description

Introduced

Deprecated

--extended-insert

--fields-enclosed-by

--fields-escaped-by

--fields-optionally-
enclosed-by

--fields-terminated-by

--flush-logs

--flush-privileges

--force

Use multiple-row INSERT
syntax

This option is used with
the --tab option and has
the same meaning as the
corresponding clause for
LOAD DATA

This option is used with
the --tab option and has
the same meaning as the
corresponding clause for
LOAD DATA

This option is used with
the --tab option and has
the same meaning as the
corresponding clause for
LOAD DATA

This option is used with
the --tab option and has
the same meaning as the
corresponding clause for
LOAD DATA

Flush MySQL server log
files before starting dump

Emit a FLUSH
PRIVILEGES statement
after dumping mysql
database

Continue even if an SQL
error occurs during a
table dump

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--hex-blob

--host

--ignore-error

--ignore-table

--include-master-host-
port

Display help message
and exit

Dump binary columns
using hexadecimal
notation

Host on which MySQL
server is located

Ignore specified errors

Do not dump given table

Include MASTER_HOST/
MASTER_PORT options
in CHANGE MASTER
statement produced with
--dump-slave

470

Option Name

--insert-ignore

--lines-terminated-by

--lock-all-tables

--lock-tables

--log-error

--login-path

--master-data

--max-allowed-packet

--net-buffer-length

--no-autocommit

--no-create-db

--no-create-info

--no-data

--no-defaults

--no-set-names

--no-tablespaces

mysqldump — A Database Backup Program

Description

Introduced

Deprecated

Write INSERT IGNORE
rather than INSERT
statements

This option is used with
the --tab option and has
the same meaning as the
corresponding clause for
LOAD DATA

Lock all tables across all
databases

Lock all tables before
dumping them

Append warnings and
errors to named file

Read login path options
from .mylogin.cnf

Write the binary log file
name and position to the
output

Maximum packet length
to send to or receive from
server

Buffer size for
TCP/IP and socket
communication

Enclose the INSERT
statements for each
dumped table within
SET autocommit = 0 and
COMMIT statements

Do not write CREATE
DATABASE statements

Do not write CREATE
TABLE statements that
re-create each dumped
table

Do not dump table
contents

Read no option files

Same as --skip-set-
charset

Do not write any
CREATE LOGFILE
GROUP or CREATE
TABLESPACE
statements in output

471

mysqldump — A Database Backup Program

Option Name

Description

Introduced

Deprecated

--opt

--order-by-primary

--password

--pipe

--plugin-dir

--port

Shorthand for --add-
drop-table --add-locks --
create-options --disable-
keys --extended-insert --
lock-tables --quick --set-
charset

Dump each table's rows
sorted by its primary key,
or by its first unique index

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--protocol

--quick

--quote-names

--replace

--result-file

--routines

--secure-auth

Transport protocol to use

Retrieve rows for a table
from the server a row at a
time

Quote identifiers within
backtick characters

Write REPLACE
statements rather than
INSERT statements

Direct output to a given
file

Dump stored routines
(procedures and
functions) from dumped
databases

Do not send passwords
to server in old (pre-4.1)
format

--server-public-key-path Path name to file

5.7.23

--set-charset

--set-gtid-purged

containing RSA public
key

Add SET NAMES
default_character_set to
output

Whether to add SET
@@GLOBAL.GTID_PURGED
to output

472

Yes

mysqldump — A Database Backup Program

Option Name

Description

Introduced

Deprecated

--shared-memory-base-
name

--single-transaction

--skip-add-drop-table

Shared-memory name
for shared-memory
connections (Windows
only)

Issue a BEGIN SQL
statement before
dumping data from server

Do not add a DROP
TABLE statement before
each CREATE TABLE
statement

--skip-add-locks

Do not add locks

--skip-comments

--skip-compact

Do not add comments to
dump file

Do not produce more
compact output

--skip-disable-keys

Do not disable keys

--skip-extended-insert

Turn off extended-insert

--skip-mysql-schema

Do not drop the mysql
schema

5.7.36

--skip-opt

--skip-quick

Turn off options set by --
opt

Do not retrieve rows for
a table from the server a
row at a time

--skip-quote-names

Do not quote identifiers

--skip-set-charset

Do not write SET NAMES
statement

--skip-triggers

--skip-tz-utc

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

Do not dump triggers

Turn off tz-utc

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

473

mysqldump — A Database Backup Program

Description

Introduced

Deprecated

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

5.7.10

Verify host name
against server certificate
Common Name identity

Produce tab-separated
data files

Override --databases or -
B option

Permissible TLS
protocols for encrypted
connections

Dump triggers for each
dumped table

Add SET
TIME_ZONE='+00:00' to
dump file

MySQL user name to
use when connecting to
server

Verbose mode

Display version
information and exit

Dump only rows selected
by given WHERE
condition

Produce XML output

Option Name

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--tab

--tables

--tls-version

--triggers

--tz-utc

--user

--verbose

--version

--where

--xml

Connection Options

The mysqldump command logs into a MySQL server to extract information. The following options specify
how to connect to the MySQL server, either on the same machine or a remote system.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

474

mysqldump — A Database Backup Program

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Introduced

Type

Default Value

5.7.10

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

This option was added in MySQL 5.7.10.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that
plugin, the server does not send the public key unless requested. This option is ignored for accounts that

475

mysqldump — A Database Backup Program

do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --host=host_name, -h host_name

Command-Line Format

--host

Dump data from the MySQL server on the given host. The default host is localhost.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqldump prompts for one. If given, there must be no space between --password= or -
p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqldump should not prompt for one, use the
--skip-password option.

• --pipe, -W

476

Command-Line Format

--pipe

mysqldump — A Database Backup Program

Type

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqldump does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

477

mysqldump — A Database Backup Program

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --skip-mysql-schema

Command-Line Format

--skip-mysql-schema

Introduced

Type

5.7.36

Boolean

Do not drop the mysql schema when the dump file is restored. By default, the schema is dropped.

This option was added in MySQL 5.7.36.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

478

mysqldump — A Database Backup Program

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

Type

String

The user name of the MySQL account to use for connecting to the server.

Option-File Options

These options are used to control which option files to read.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

479

mysqldump — A Database Backup Program

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqldump normally reads the [client] and [mysqldump] groups. If this option is
given as --defaults-group-suffix=_other, mysqldump also reads the [client_other] and
[mysqldump_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

480

mysqldump — A Database Backup Program

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

DDL Options

Usage scenarios for mysqldump include setting up an entire new MySQL instance (including database
tables), and replacing data inside an existing instance with existing databases and tables. The following
options let you specify which things to tear down and set up when restoring a dump, by encoding various
DDL statements within the dump file.

• --add-drop-database

Command-Line Format

--add-drop-database

Write a DROP DATABASE statement before each CREATE DATABASE statement. This option is typically
used in conjunction with the --all-databases or --databases option because no CREATE
DATABASE statements are written unless one of those options is specified.

• --add-drop-table

Command-Line Format

--add-drop-table

Write a DROP TABLE statement before each CREATE TABLE statement.

• --add-drop-trigger

Command-Line Format

--add-drop-trigger

Write a DROP TRIGGER statement before each CREATE TRIGGER statement.

• --all-tablespaces, -Y

Command-Line Format

--all-tablespaces

Adds to a table dump all SQL statements needed to create any tablespaces used by an NDB table. This
information is not otherwise included in the output from mysqldump. This option is currently relevant
only to NDB Cluster tables, which are not supported in MySQL 5.7.

• --no-create-db, -n

Command-Line Format

--no-create-db

Suppress the CREATE DATABASE statements that are otherwise included in the output if the --
databases or --all-databases option is given.

481

mysqldump — A Database Backup Program

• --no-create-info, -t

Command-Line Format

--no-create-info

Do not write CREATE TABLE statements that create each dumped table.

Note

This option does not exclude statements creating log file groups or tablespaces
from mysqldump output; however, you can use the --no-tablespaces option
for this purpose.

• --no-tablespaces, -y

Command-Line Format

--no-tablespaces

This option suppresses all CREATE LOGFILE GROUP and CREATE TABLESPACE statements in the
output of mysqldump.

• --replace

Command-Line Format

--replace

Write REPLACE statements rather than INSERT statements.

Debug Options

The following options print debugging information, encode debugging information in the dump file, or let the
dump operation proceed regardless of potential problems.

• --allow-keywords

Command-Line Format

--allow-keywords

Permit creation of column names that are keywords. This works by prefixing each column name with the
table name.

• --comments, -i

Command-Line Format

--comments

Write additional information in the dump file such as program version, server version, and host. This
option is enabled by default. To suppress this additional information, use --skip-comments.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

482

Default Value

String

d:t:o,/tmp/mysqldump.trace

mysqldump — A Database Backup Program

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default value is
d:t:o,/tmp/mysqldump.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --dump-date

Command-Line Format

Type

Default Value

--dump-date

Boolean

TRUE

If the --comments option is given, mysqldump produces a comment at the end of the dump of the
following form:

-- Dump completed on DATE

However, the date causes dump files taken at different times to appear to be different, even if the data
are otherwise identical. --dump-date and --skip-dump-date control whether the date is added to
the comment. The default is --dump-date (include the date in the comment). --skip-dump-date
suppresses date printing.

483

mysqldump — A Database Backup Program

• --force, -f

Command-Line Format

--force

Ignore all errors; continue even if an SQL error occurs during a table dump.

One use for this option is to cause mysqldump to continue executing even when it encounters a view
that has become invalid because the definition refers to a table that has been dropped. Without --
force, mysqldump exits with an error message. With --force, mysqldump prints the error message,
but it also writes an SQL comment containing the view definition to the dump output and continues
executing.

If the --ignore-error option is also given to ignore specific errors, --force takes precedence.

• --log-error=file_name

Command-Line Format

--log-error=file_name

Type

File name

Log warnings and errors by appending them to the named file. The default is to do no logging.

• --skip-comments

Command-Line Format

--skip-comments

See the description for the --comments option.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does.

Help Options

The following options display information about the mysqldump command itself.

• --help, -?

Command-Line Format

--help

Display a help message and exit.

484

• --version, -V

Command-Line Format

--version

Display version information and exit.

mysqldump — A Database Backup Program

Internationalization Options

The following options change how the mysqldump command represents character data with national
language settings.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

Default Value

String

utf8

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”. If
no character set is specified, mysqldump uses utf8.

• --no-set-names, -N

Command-Line Format

Deprecated

--no-set-names

Yes

Turns off the --set-charset setting, the same as specifying --skip-set-charset.

• --set-charset

Command-Line Format

Disabled by

--set-charset

skip-set-charset

Write SET NAMES default_character_set to the output. This option is enabled by default. To
suppress the SET NAMES statement, use --skip-set-charset.

Replication Options

The mysqldump command is frequently used to create an empty instance, or an instance including data,
on a replica server in a replication configuration. The following options apply to dumping and restoring data
on replication source and replica servers.

• --apply-slave-statements

Command-Line Format

--apply-slave-statements

Type

Default Value

Boolean

FALSE

485

mysqldump — A Database Backup Program

For a replica dump produced with the --dump-slave option, add a STOP SLAVE statement before the
CHANGE MASTER TO statement and a START SLAVE statement at the end of the output.

• --delete-master-logs

Command-Line Format

--delete-master-logs

On a source replication server, delete the binary logs by sending a PURGE BINARY LOGS statement
to the server after performing the dump operation. This option requires the RELOAD privilege as well as
privileges sufficient to execute that statement. This option automatically enables --master-data.

• --dump-slave[=value]

Command-Line Format

--dump-slave[=value]

Type

Default Value

Valid Values

Numeric

1

1

2

This option is similar to --master-data except that it is used to dump a replication replica server to
produce a dump file that can be used to set up another server as a replica that has the same source
as the dumped server. It causes the dump output to include a CHANGE MASTER TO statement that
indicates the binary log coordinates (file name and position) of the dumped replica's source. The CHANGE
MASTER TO statement reads the values of Relay_Master_Log_File and Exec_Master_Log_Pos
from the SHOW SLAVE STATUS output and uses them for MASTER_LOG_FILE and MASTER_LOG_POS
respectively. These are the source server coordinates from which the replica should start replicating.

Note

Inconsistencies in the sequence of transactions from the relay log which have
been executed can cause the wrong position to be used. See Section 16.4.1.32,
“Replication and Transaction Inconsistencies” for more information.

--dump-slave causes the coordinates from the source to be used rather than those of the dumped
server, as is done by the --master-data option. In addition, specifiying this option causes the --
master-data option to be overridden, if used, and effectively ignored.

Warning

This option should not be used if the server where the dump is going to be
applied uses gtid_mode=ON and MASTER_AUTOPOSITION=1.

The option value is handled the same way as for --master-data (setting no value or 1 causes a
CHANGE MASTER TO statement to be written to the dump, setting 2 causes the statement to be written

486

mysqldump — A Database Backup Program

but encased in SQL comments) and has the same effect as --master-data in terms of enabling or
disabling other options and in how locking is handled.

This option causes mysqldump to stop the replica SQL thread before the dump and restart it again after.

--dump-slave sends a SHOW SLAVE STATUS statement to the server to obtain information, so it
requires privileges sufficient to execute that statement.

In conjunction with --dump-slave, the --apply-slave-statements and --include-master-
host-port options can also be used.

• --include-master-host-port

Command-Line Format

--include-master-host-port

Type

Default Value

Boolean

FALSE

For the CHANGE MASTER TO statement in a replica dump produced with the --dump-slave option,
add MASTER_HOST and MASTER_PORT options for the host name and TCP/IP port number of the
replica's source.

• --master-data[=value]

Command-Line Format

--master-data[=value]

Type

Default Value

Valid Values

Numeric

1

1

2

Use this option to dump a source replication server to produce a dump file that can be used to set up
another server as a replica of the source. It causes the dump output to include a CHANGE MASTER TO
statement that indicates the binary log coordinates (file name and position) of the dumped server. These
are the source server coordinates from which the replica should start replicating after you load the dump
file into the replica.

If the option value is 2, the CHANGE MASTER TO statement is written as an SQL comment, and thus is
informative only; it has no effect when the dump file is reloaded. If the option value is 1, the statement is
not written as a comment and takes effect when the dump file is reloaded. If no option value is specified,
the default value is 1.

--master-data sends a SHOW MASTER STATUS statement to the server to obtain information, so it
requires privileges sufficient to execute that statement. This option also requires the RELOAD privilege
and the binary log must be enabled.

The --master-data option automatically turns off --lock-tables. It also turns on --lock-
all-tables, unless --single-transaction also is specified, in which case, a global read lock
is acquired only for a short time at the beginning of the dump (see the description for --single-
transaction). In all cases, any action on logs happens at the exact moment of the dump.

It is also possible to set up a replica by dumping an existing replica of the source, using the --dump-
slave option, which overrides --master-data and causes it to be ignored if both options are used.

487

mysqldump — A Database Backup Program

• --set-gtid-purged=value

Command-Line Format

--set-gtid-purged=value

Type

Default Value

Valid Values

Enumeration

AUTO

OFF

ON

AUTO

This option enables control over global transaction ID (GTID) information written to the dump file, by
indicating whether to add a SET @@GLOBAL.gtid_purged statement to the output. This option may
also cause a statement to be written to the output that disables binary logging while the dump file is
being reloaded.

The following table shows the permitted option values. The default value is AUTO.

Value

OFF

ON

AUTO

Meaning

Add no SET statement to the output.

Add a SET statement to the output. An error occurs
if GTIDs are not enabled on the server.

Add a SET statement to the output if GTIDs are
enabled on the server.

A partial dump from a server that is using GTID-based replication requires the --set-gtid-
purged={ON|OFF} option to be specified. Use ON if the intention is to deploy a new replication replica
using only some of the data from the dumped server. Use OFF if the intention is to repair a table by
copying it within a topology. Use OFF if the intention is to copy a table between replication topologies that
are disjoint and for them to remain so.

The --set-gtid-purged option has the following effect on binary logging when the dump file is
reloaded:

• --set-gtid-purged=OFF: SET @@SESSION.SQL_LOG_BIN=0; is not added to the output.

• --set-gtid-purged=ON: SET @@SESSION.SQL_LOG_BIN=0; is added to the output.

• --set-gtid-purged=AUTO: SET @@SESSION.SQL_LOG_BIN=0; is added to the output if GTIDs

are enabled on the server you are backing up (that is, if AUTO evaluates to ON).

Using this option with the --single-transaction option can lead to inconsistencies in the output. If
--set-gtid-purged=ON is required, it can be used with --lock-all-tables, but this can prevent
parallel queries while mysqldump is being run.

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid_mode=ON), if
your dump file includes system tables. mysqldump issues DML instructions for the system tables which
use the non-transactional MyISAM storage engine, and this combination is not permitted when GTIDs
are enabled. Also be aware that loading a dump file from a server with GTIDs enabled, into another
server with GTIDs enabled, causes different transaction identifiers to be generated.

488

mysqldump — A Database Backup Program

Format Options

The following options specify how to represent the entire dump file or certain kinds of data in the dump file.
They also control whether certain optional information is written to the dump file.

• --compact

Command-Line Format

--compact

Produce more compact output. This option enables the --skip-add-drop-table, --skip-add-
locks, --skip-comments, --skip-disable-keys, and --skip-set-charset options.

• --compatible=name

Command-Line Format

--compatible=name[,name,...]

Type

Default Value

Valid Values

String

''

ansi

mysql323

mysql40

postgresql

oracle

mssql

db2

maxdb

no_key_options

no_table_options

no_key_options

Produce output that is more compatible with other database systems or with older MySQL servers.
The value of name can be ansi, mysql323, mysql40, postgresql, oracle, mssql, db2, maxdb,
no_key_options, no_table_options, or no_field_options. To use several values, separate
them by commas. These values have the same meaning as the corresponding options for setting the
server SQL mode. See Section 5.1.10, “Server SQL Modes”.

This option does not guarantee compatibility with other servers. It only enables those SQL mode
values that are currently available for making dump output more compatible. For example, --
compatible=oracle does not map data types to Oracle types or use Oracle comment syntax.

• --complete-insert, -c

Command-Line Format

--complete-insert

489

mysqldump — A Database Backup Program

Use complete INSERT statements that include column names.

• --create-options

Command-Line Format

--create-options

Include all MySQL-specific table options in the CREATE TABLE statements.

• --fields-terminated-by=..., --fields-enclosed-by=..., --fields-optionally-

enclosed-by=..., --fields-escaped-by=...

Command-Line Format

--fields-terminated-by=string

Type

String

Command-Line Format

--fields-enclosed-by=string

Type

String

Command-Line Format

--fields-optionally-enclosed-
by=string

Type

String

Command-Line Format

--fields-escaped-by

Type

String

These options are used with the --tab option and have the same meaning as the corresponding
FIELDS clauses for LOAD DATA. See Section 13.2.6, “LOAD DATA Statement”.

• --hex-blob

Command-Line Format

--hex-blob

Dump binary columns using hexadecimal notation (for example, 'abc' becomes 0x616263). The
affected data types are BINARY, VARBINARY, BLOB types, BIT, all spatial data types, and other non-
binary data types when used with the binary character set.

The --hex-blob option is ignored when the --tab is used.

• --lines-terminated-by=...

Command-Line Format

--lines-terminated-by=string

Type

String

This option is used with the --tab option and has the same meaning as the corresponding LINES
clause for LOAD DATA. See Section 13.2.6, “LOAD DATA Statement”.

• --quote-names, -Q

490

mysqldump — A Database Backup Program

Command-Line Format

Disabled by

--quote-names

skip-quote-names

Quote identifiers (such as database, table, and column names) within ` characters. If the ANSI_QUOTES
SQL mode is enabled, identifiers are quoted within " characters. This option is enabled by default. It can
be disabled with --skip-quote-names, but this option should be given after any option such as --
compatible that may enable --quote-names.

• --result-file=file_name, -r file_name

Command-Line Format

--result-file=file_name

Type

File name

Direct output to the named file. The result file is created and its previous contents overwritten, even if an
error occurs while generating the dump.

This option should be used on Windows to prevent newline \n characters from being converted to \r\n
carriage return/newline sequences.

• --tab=dir_name, -T dir_name

Command-Line Format

Type

--tab=dir_name

Directory name

Produce tab-separated text-format data files. For each dumped table, mysqldump creates a
tbl_name.sql file that contains the CREATE TABLE statement that creates the table, and the server
writes a tbl_name.txt file that contains its data. The option value is the directory in which to write the
files.

Note

This option should be used only when mysqldump is run on the same machine
as the mysqld server. Because the server creates *.txt files in the directory
that you specify, the directory must be writable by the server and the MySQL
account that you use must have the FILE privilege. Because mysqldump creates
*.sql in the same directory, it must be writable by your system login account.

By default, the .txt data files are formatted using tab characters between column values and a newline
at the end of each line. The format can be specified explicitly using the --fields-xxx and --lines-
terminated-by options.

Column values are converted to the character set specified by the --default-character-set
option.

• --tz-utc

Command-Line Format

--tz-utc

491

mysqldump — A Database Backup Program

Disabled by

skip-tz-utc

This option enables TIMESTAMP columns to be dumped and reloaded between servers in different time
zones. mysqldump sets its connection time zone to UTC and adds SET TIME_ZONE='+00:00' to the
dump file. Without this option, TIMESTAMP columns are dumped and reloaded in the time zones local to
the source and destination servers, which can cause the values to change if the servers are in different
time zones. --tz-utc also protects against changes due to daylight saving time. --tz-utc is enabled
by default. To disable it, use --skip-tz-utc.

• --xml, -X

Command-Line Format

--xml

Write dump output as well-formed XML.

NULL, 'NULL', and Empty Values: For a column named column_name, the NULL value, an empty
string, and the string value 'NULL' are distinguished from one another in the output generated by this
option as follows.

Value:

NULL (unknown value)

'' (empty string)

'NULL' (string value)

XML Representation:

<field name="column_name"
xsi:nil="true" />

<field name="column_name"></field>

<field name="column_name">NULL</
field>

The output from the mysql client when run using the --xml option also follows the preceding rules.
(See Section 4.5.1.1, “mysql Client Options”.)

XML output from mysqldump includes the XML namespace, as shown here:

$> mysqldump --xml -u root world City
<?xml version="1.0"?>
<mysqldump xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<database name="world">
<table_structure name="City">
<field Field="ID" Type="int(11)" Null="NO" Key="PRI" Extra="auto_increment" />
<field Field="Name" Type="char(35)" Null="NO" Key="" Default="" Extra="" />
<field Field="CountryCode" Type="char(3)" Null="NO" Key="" Default="" Extra="" />
<field Field="District" Type="char(20)" Null="NO" Key="" Default="" Extra="" />
<field Field="Population" Type="int(11)" Null="NO" Key="" Default="0" Extra="" />
<key Table="City" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="ID"
Collation="A" Cardinality="4079" Null="" Index_type="BTREE" Comment="" />
<options Name="City" Engine="MyISAM" Version="10" Row_format="Fixed" Rows="4079"
Avg_row_length="67" Data_length="273293" Max_data_length="18858823439613951"
Index_length="43008" Data_free="0" Auto_increment="4080"
Create_time="2007-03-31 01:47:01" Update_time="2007-03-31 01:47:02"
Collation="latin1_swedish_ci" Create_options="" Comment="" />
</table_structure>
<table_data name="City">
<row>
<field name="ID">1</field>
<field name="Name">Kabul</field>
<field name="CountryCode">AFG</field>
<field name="District">Kabol</field>
<field name="Population">1780000</field>
</row>

492

mysqldump — A Database Backup Program

...

<row>
<field name="ID">4079</field>
<field name="Name">Rafah</field>
<field name="CountryCode">PSE</field>
<field name="District">Rafah</field>
<field name="Population">92020</field>
</row>
</table_data>
</database>
</mysqldump>

Filtering Options

The following options control which kinds of schema objects are written to the dump file: by category,
such as triggers or events; by name, for example, choosing which databases and tables to dump; or even
filtering rows from the table data using a WHERE clause.

• --all-databases, -A

Command-Line Format

--all-databases

Dump all tables in all databases. This is the same as using the --databases option and naming all the
databases on the command line.

• --databases, -B

Command-Line Format

--databases

Dump several databases. Normally, mysqldump treats the first name argument on the command line as
a database name and following names as table names. With this option, it treats all name arguments as
database names. CREATE DATABASE and USE statements are included in the output before each new
database.

This option may be used to dump the INFORMATION_SCHEMA and performance_schema databases,
which normally are not dumped even with the --all-databases option. (Also use the --skip-lock-
tables option.)

• --events, -E

Command-Line Format

--events

Include Event Scheduler events for the dumped databases in the output. This option requires the EVENT
privileges for those databases.

The output generated by using --events contains CREATE EVENT statements to create the events.
However, these statements do not include attributes such as the event creation and modification
timestamps, so when the events are reloaded, they are created with timestamps equal to the reload
time.

If you require events to be created with their original timestamp attributes, do not use --events.
Instead, dump and reload the contents of the mysql.event table directly, using a MySQL account that
has appropriate privileges for the mysql database.

493

mysqldump — A Database Backup Program

• --ignore-error=error[,error]...

Command-Line Format

--ignore-error=error[,error]...

Type

String

Ignore the specified errors. The option value is a list of comma-separated error numbers specifying the
errors to ignore during mysqldump execution. If the --force option is also given to ignore all errors, --
force takes precedence.

• --ignore-table=db_name.tbl_name

Command-Line Format

--ignore-table=db_name.tbl_name

Type

String

Do not dump the given table, which must be specified using both the database and table names. To
ignore multiple tables, use this option multiple times. This option also can be used to ignore views.

• --no-data, -d

Command-Line Format

--no-data

Do not write any table row information (that is, do not dump table contents). This is useful if you want to
dump only the CREATE TABLE statement for the table (for example, to create an empty copy of the table
by loading the dump file).

• --routines, -R

Command-Line Format

--routines

Include stored routines (procedures and functions) for the dumped databases in the output. This option
requires the SELECT privilege for the mysql.proc table.

The output generated by using --routines contains CREATE PROCEDURE and CREATE FUNCTION
statements to create the routines. However, these statements do not include attributes such as the
routine creation and modification timestamps, so when the routines are reloaded, they are created with
timestamps equal to the reload time.

If you require routines to be created with their original timestamp attributes, do not use --routines.
Instead, dump and reload the contents of the mysql.proc table directly, using a MySQL account that
has appropriate privileges for the mysql database.

• --tables

Command-Line Format

--tables

494

Override the --databases or -B option. mysqldump regards all name arguments following the option
as table names.

mysqldump — A Database Backup Program

• --triggers

Command-Line Format

Disabled by

--triggers

skip-triggers

Include triggers for each dumped table in the output. This option is enabled by default; disable it with --
skip-triggers.

To be able to dump a table's triggers, you must have the TRIGGER privilege for the table.

Multiple triggers are permitted. mysqldump dumps triggers in activation order so that when the dump
file is reloaded, triggers are created in the same activation order. However, if a mysqldump dump file
contains multiple triggers for a table that have the same trigger event and action time, an error occurs
for attempts to load the dump file into an older server that does not support multiple triggers. (For a
workaround, see Section 2.11.3, “Downgrade Notes”; you can convert triggers to be compatible with
older servers.)

• --where='where_condition', -w 'where_condition'

Command-Line Format

--where='where_condition'

Dump only rows selected by the given WHERE condition. Quotes around the condition are mandatory if it
contains spaces or other characters that are special to your command interpreter.

Examples:

--where="user='jimf'"
-w"userid>1"
-w"userid<1"

Performance Options

The following options are the most relevant for the performance particularly of the restore operations. For
large data sets, restore operation (processing the INSERT statements in the dump file) is the most time-
consuming part. When it is urgent to restore data quickly, plan and test the performance of this stage in
advance. For restore times measured in hours, you might prefer an alternative backup and restore solution,
such as MySQL Enterprise Backup for InnoDB-only and mixed-use databases.

Performance is also affected by the transactional options, primarily for the dump operation.

• --disable-keys, -K

Command-Line Format

--disable-keys

For each table, surround the INSERT statements with /*!40000 ALTER TABLE tbl_name DISABLE
KEYS */; and /*!40000 ALTER TABLE tbl_name ENABLE KEYS */; statements. This makes
loading the dump file faster because the indexes are created after all rows are inserted. This option is
effective only for nonunique indexes of MyISAM tables.

• --extended-insert, -e

Command-Line Format

Disabled by

--extended-insert

skip-extended-insert

495

mysqldump — A Database Backup Program

Write INSERT statements using multiple-row syntax that includes several VALUES lists. This results in a
smaller dump file and speeds up inserts when the file is reloaded.

• --insert-ignore

Command-Line Format

--insert-ignore

Write INSERT IGNORE statements rather than INSERT statements.

• --max-allowed-packet=value

Command-Line Format

--max-allowed-packet=value

Type

Default Value

Numeric

25165824

The maximum size of the buffer for client/server communication. The default is 24MB, the maximum is
1GB.

Note

The value of this option is specific to mysqldump and should not be confused
with the MySQL server's max_allowed_packet system variable; the server
value cannot be exceeded by a single packet from mysqldump, regardless of any
setting for the mysqldump option, even if the latter is larger.

• --net-buffer-length=value

Command-Line Format

--net-buffer-length=value

Type

Default Value

Numeric

16384

The initial size of the buffer for client/server communication. When creating multiple-row INSERT
statements (as with the --extended-insert or --opt option), mysqldump creates rows up to
--net-buffer-length bytes long. If you increase this variable, ensure that the MySQL server
net_buffer_length system variable has a value at least this large.

• --opt

Command-Line Format

Disabled by

--opt

skip-opt

This option, enabled by default, is shorthand for the combination of --add-drop-table --add-locks
--create-options --disable-keys --extended-insert --lock-tables --quick --set-

496

mysqldump — A Database Backup Program

charset. It gives a fast dump operation and produces a dump file that can be reloaded into a MySQL
server quickly.

Because the --opt option is enabled by default, you only specify its converse, the --skip-opt to
turn off several default settings. See the discussion of mysqldump option groups for information about
selectively enabling or disabling a subset of the options affected by --opt.

• --quick, -q

Command-Line Format

Disabled by

--quick

skip-quick

This option is useful for dumping large tables. It forces mysqldump to retrieve rows for a table from the
server a row at a time rather than retrieving the entire row set and buffering it in memory before writing it
out.

• --skip-opt

Command-Line Format

--skip-opt

See the description for the --opt option.

Transactional Options

The following options trade off the performance of the dump operation, against the reliability and
consistency of the exported data.

• --add-locks

Command-Line Format

--add-locks

Surround each table dump with LOCK TABLES and UNLOCK TABLES statements. This results in faster
inserts when the dump file is reloaded. See Section 8.2.4.1, “Optimizing INSERT Statements”.

• --flush-logs, -F

Command-Line Format

--flush-logs

Flush the MySQL server log files before starting the dump. This option requires the RELOAD privilege.
If you use this option in combination with the --all-databases option, the logs are flushed for each
database dumped. The exception is when using --lock-all-tables, --master-data, or --
single-transaction: In this case, the logs are flushed only once, corresponding to the moment that
all tables are locked by FLUSH TABLES WITH READ LOCK. If you want your dump and the log flush
to happen at exactly the same moment, you should use --flush-logs together with --lock-all-
tables, --master-data, or --single-transaction.

• --flush-privileges

497

Command-Line Format

--flush-privileges

mysqldump — A Database Backup Program

Add a FLUSH PRIVILEGES statement to the dump output after dumping the mysql database. This
option should be used any time the dump contains the mysql database and any other database that
depends on the data in the mysql database for proper restoration.

Because the dump file contains a FLUSH PRIVILEGES statement, reloading the file requires privileges
sufficient to execute that statement.

Note

For upgrades to MySQL 5.7 or higher from older versions, do not use --
flush-privileges. For upgrade instructions in this case, see Section 2.10.3,
“Changes in MySQL 5.7”.

• --lock-all-tables, -x

Command-Line Format

--lock-all-tables

Lock all tables across all databases. This is achieved by acquiring a global read lock for the duration of
the whole dump. This option automatically turns off --single-transaction and --lock-tables.

• --lock-tables, -l

Command-Line Format

--lock-tables

For each dumped database, lock all tables to be dumped before dumping them. The tables are locked
with READ LOCAL to permit concurrent inserts in the case of MyISAM tables. For transactional tables
such as InnoDB, --single-transaction is a much better option than --lock-tables because it
does not need to lock the tables at all.

Because --lock-tables locks tables for each database separately, this option does not guarantee
that the tables in the dump file are logically consistent between databases. Tables in different databases
may be dumped in completely different states.

Some options, such as --opt, automatically enable --lock-tables. If you want to override this, use
--skip-lock-tables at the end of the option list.

• --no-autocommit

Command-Line Format

--no-autocommit

Enclose the INSERT statements for each dumped table within SET autocommit = 0 and COMMIT
statements.

• --order-by-primary

Command-Line Format

--order-by-primary

Dump each table's rows sorted by its primary key, or by its first unique index, if such an index exists.
This is useful when dumping a MyISAM table to be loaded into an InnoDB table, but makes the dump
operation take considerably longer.

• --shared-memory-base-name=name

498

mysqldump — A Database Backup Program

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --single-transaction

Command-Line Format

--single-transaction

This option sets the transaction isolation mode to REPEATABLE READ and sends a START
TRANSACTION SQL statement to the server before dumping data. It is useful only with transactional
tables such as InnoDB, because then it dumps the consistent state of the database at the time when
START TRANSACTION was issued without blocking any applications.

The RELOAD or FLUSH_TABLES privilege is required with --single-transaction if both
gtid_mode=ON and --set-gtid=purged=ON|AUTO. This requirement was added in MySQL 8.0.32.

When using this option, you should keep in mind that only InnoDB tables are dumped in a consistent
state. For example, any MyISAM or MEMORY tables dumped while using this option may still change
state.

While a --single-transaction dump is in process, to ensure a valid dump file (correct table
contents and binary log coordinates), no other connection should use the following statements: ALTER
TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE. A consistent read is not
isolated from those statements, so use of them on a table to be dumped can cause the SELECT that is
performed by mysqldump to retrieve the table contents to obtain incorrect contents or fail.

The --single-transaction option and the --lock-tables option are mutually exclusive because
LOCK TABLES causes any pending transactions to be committed implicitly.

Using --single-transaction together with the --set-gtid-purged option is not recommended;
doing so can lead to inconsistencies in the output of mysqldump.

To dump large tables, combine the --single-transaction option with the --quick option.

Option Groups

• The --opt option turns on several settings that work together to perform a fast dump operation. All of

these settings are on by default, because --opt is on by default. Thus you rarely if ever specify --opt.
Instead, you can turn these settings off as a group by specifying --skip-opt, then optionally re-enable
certain settings by specifying the associated options later on the command line.

• The --compact option turns off several settings that control whether optional statements and comments
appear in the output. Again, you can follow this option with other options that re-enable certain settings,
or turn all the settings on by using the --skip-compact form.

When you selectively enable or disable the effect of a group option, order is important because options are
processed first to last. For example, --disable-keys --lock-tables --skip-opt would not have
the intended effect; it is the same as --skip-opt by itself.

499

mysqldump — A Database Backup Program

Examples

To make a backup of an entire database:

mysqldump db_name > backup-file.sql

To load the dump file back into the server:

mysql db_name < backup-file.sql

Another way to reload the dump file:

mysql -e "source /path-to-backup/backup-file.sql" db_name

mysqldump is also very useful for populating databases by copying data from one MySQL server to
another:

mysqldump --opt db_name | mysql --host=remote_host -C db_name

You can dump several databases with one command:

mysqldump --databases db_name1 [db_name2 ...] > my_databases.sql

To dump all databases, use the --all-databases option:

mysqldump --all-databases > all_databases.sql

For InnoDB tables, mysqldump provides a way of making an online backup:

mysqldump --all-databases --master-data --single-transaction > all_databases.sql

This backup acquires a global read lock on all tables (using FLUSH TABLES WITH READ LOCK) at the
beginning of the dump. As soon as this lock has been acquired, the binary log coordinates are read and
the lock is released. If long updating statements are running when the FLUSH statement is issued, the
MySQL server may get stalled until those statements finish. After that, the dump becomes lock free and
does not disturb reads and writes on the tables. If the update statements that the MySQL server receives
are short (in terms of execution time), the initial lock period should not be noticeable, even with many
updates.

For point-in-time recovery (also known as “roll-forward,” when you need to restore an old backup
and replay the changes that happened since that backup), it is often useful to rotate the binary log
(see Section 5.4.4, “The Binary Log”) or at least know the binary log coordinates to which the dump
corresponds:

mysqldump --all-databases --master-data=2 > all_databases.sql

Or:

mysqldump --all-databases --flush-logs --master-data=2 > all_databases.sql

The --master-data and --single-transaction options can be used simultaneously, which provides
a convenient way to make an online backup suitable for use prior to point-in-time recovery if tables are
stored using the InnoDB storage engine.

For more information on making backups, see Section 7.2, “Database Backup Methods”, and Section 7.3,
“Example Backup and Recovery Strategy”.

• To select the effect of --opt except for some features, use the --skip option for each feature. To
disable extended inserts and memory buffering, use --opt --skip-extended-insert --skip-
quick. (Actually, --skip-extended-insert --skip-quick is sufficient because --opt is on by
default.)

500

mysqlimport — A Data Import Program

• To reverse --opt for all features except index disabling and table locking, use --skip-opt --

disable-keys --lock-tables.

Restrictions

mysqldump does not dump the INFORMATION_SCHEMA, performance_schema, or sys schema by
default. To dump any of these, name them explicitly on the command line. You can also name them with
the --databases option. For INFORMATION_SCHEMA and performance_schema, also use the --
skip-lock-tables option.

mysqldump does not dump the NDB Cluster ndbinfo information database.

mysqldump does not dump InnoDB CREATE TABLESPACE statements.

mysqldump always strips the NO_AUTO_CREATE_USER SQL mode as NO_AUTO_CREATE_USER is
not compatible with MySQL 8.0. It remains stripped even when importing back into MySQL 5.7, which
means that stored routines could behave differently after restoring a dump if they rely upon this particular
sql_mode. It is stripped as of mysqldump 5.7.24.

It is not recommended to restore from a dump made using mysqldump to a MySQL 5.6.9 or earlier server
that has GTIDs enabled. See Section 16.1.3.6, “Restrictions on Replication with GTIDs”.

mysqldump includes statements to recreate the general_log and slow_query_log tables for dumps
of the mysql database. Log table contents are not dumped.

If you encounter problems backing up views due to insufficient privileges, see Section 23.9, “Restrictions
on Views” for a workaround.

4.5.5 mysqlimport — A Data Import Program

The mysqlimport client provides a command-line interface to the LOAD DATA SQL statement. Most
options to mysqlimport correspond directly to clauses of LOAD DATA syntax. See Section 13.2.6, “LOAD
DATA Statement”.

Invoke mysqlimport like this:

mysqlimport [options] db_name textfile1 [textfile2 ...]

For each text file named on the command line, mysqlimport strips any extension from the file name and
uses the result to determine the name of the table into which to import the file's contents. For example, files
named patient.txt, patient.text, and patient all would be imported into a table named patient.

mysqlimport supports the following options, which can be specified on the command line or in the
[mysqlimport] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.17 mysqlimport Options

Option Name

--bind-address

--character-sets-dir

--columns

Description

Introduced

Deprecated

Use specified network
interface to connect to
MySQL Server

Directory where
character sets can be
found

This option takes a
comma-separated list

501

mysqlimport — A Data Import Program

Introduced

Deprecated

Option Name

--compress

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

Description
of column names as its
value

Compress all information
sent between client and
server

Write debugging log

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Specify default character
set

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--delete

Empty the table before
importing the text file

--enable-cleartext-plugin Enable cleartext

5.7.10

--fields-enclosed-by

--fields-escaped-by

--fields-optionally-
enclosed-by

--fields-terminated-by

--force

authentication plugin

This option has the
same meaning as the
corresponding clause for
LOAD DATA

This option has the
same meaning as the
corresponding clause for
LOAD DATA

This option has the
same meaning as the
corresponding clause for
LOAD DATA

This option has the
same meaning as the
corresponding clause for
LOAD DATA

Continue even if an SQL
error occurs

502

mysqlimport — A Data Import Program

Option Name

Description

Introduced

Deprecated

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--host

--ignore

--ignore-lines

--lines-terminated-by

--local

--lock-tables

--login-path

--low-priority

--no-defaults

--password

--pipe

--plugin-dir

--port

Display help message
and exit

Host on which MySQL
server is located

See the description for
the --replace option

Ignore the first N lines of
the data file

This option has the
same meaning as the
corresponding clause for
LOAD DATA

Read input files locally
from the client host

Lock all tables for writing
before processing any
text files

Read login path options
from .mylogin.cnf

Use LOW_PRIORITY
when loading the table

Read no option files

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--protocol

--replace

--secure-auth

Transport protocol to use

The --replace and --
ignore options control
handling of input rows
that duplicate existing
rows on unique key
values

Do not send passwords
to server in old (pre-4.1)
format

Yes

503

mysqlimport — A Data Import Program

Option Name

Description

Introduced

Deprecated

--server-public-key-path Path name to file

5.7.23

--shared-memory-base-
name

--silent

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--tls-version

--use-threads

--user

containing RSA public
key

Shared-memory name
for shared-memory
connections (Windows
only)

Produce output only
when errors occur

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

5.7.10

Verify host name
against server certificate
Common Name identity

Permissible TLS
protocols for encrypted
connections

Number of threads for
parallel file-loading

MySQL user name to
use when connecting to
server

--verbose

Verbose mode

504

mysqlimport — A Data Import Program

Option Name

Description

Introduced

Deprecated

--version

• --help, -?

Display version
information and exit

Command-Line Format

--help

Display a help message and exit.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=path

Type

Default Value

String

[none]

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --columns=column_list, -c column_list

Command-Line Format

--columns=column_list

This option takes a list of comma-separated column names as its value. The order of the column names
indicates how to match data file columns with table columns.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --debug[=debug_options], -# [debug_options]

505

Command-Line Format

--debug[=debug_options]

Type

String

mysqlimport — A Data Import Program

Default Value

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

506

mysqlimport — A Data Import Program

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqlimport normally reads the [client] and [mysqlimport] groups. If this option is
given as --defaults-group-suffix=_other, mysqlimport also reads the [client_other] and
[mysqlimport_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --delete, -D

Command-Line Format

--delete

Empty the table before importing the text file.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Introduced

Type

5.7.10

Boolean

507

mysqlimport — A Data Import Program

Default Value

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

This option was added in MySQL 5.7.10.

• --fields-terminated-by=..., --fields-enclosed-by=..., --fields-optionally-

enclosed-by=..., --fields-escaped-by=...

Command-Line Format

--fields-terminated-by=string

Type

String

Command-Line Format

--fields-enclosed-by=string

Type

String

Command-Line Format

--fields-optionally-enclosed-
by=string

Type

String

Command-Line Format

--fields-escaped-by

Type

String

These options have the same meaning as the corresponding clauses for LOAD DATA. See
Section 13.2.6, “LOAD DATA Statement”.

• --force, -f

Command-Line Format

--force

Ignore errors. For example, if a table for a text file does not exist, continue processing any remaining
files. Without --force, mysqlimport exits if a table does not exist.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

508

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that

plugin, the server does not send the public key unless requested. This option is ignored for accounts that

mysqlimport — A Data Import Program

do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Import data to the MySQL server on the given host. The default host is localhost.

• --ignore, -i

Command-Line Format

--ignore

See the description for the --replace option.

• --ignore-lines=N

Command-Line Format

Type

--ignore-lines=#

Numeric

Ignore the first N lines of the data file.

• --lines-terminated-by=...

Command-Line Format

--lines-terminated-by=string

Type

String

This option has the same meaning as the corresponding clause for LOAD DATA. For example, to
import Windows files that have lines terminated with carriage return/linefeed pairs, use --lines-
terminated-by="\r\n". (You might have to double the backslashes, depending on the escaping
conventions of your command interpreter.) See Section 13.2.6, “LOAD DATA Statement”.

• --local, -L

Command-Line Format

Type

--local

Boolean

509

mysqlimport — A Data Import Program

Default Value

FALSE

By default, files are read by the server on the server host. With this option, mysqlimport reads input
files locally on the client host.

Successful use of LOCAL load operations within mysqlimport also requires that the server permits
local loading; see Section 6.1.6, “Security Considerations for LOAD DATA LOCAL”

• --lock-tables, -l

Command-Line Format

--lock-tables

Lock all tables for writing before processing any text files. This ensures that all tables are synchronized
on the server.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --low-priority

Command-Line Format

--low-priority

Use LOW_PRIORITY when loading the table. This affects only storage engines that use only table-level
locking (such as MyISAM, MEMORY, and MERGE).

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --password[=password], -p[password]

510

mysqlimport — A Data Import Program

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqlimport prompts for one. If given, there must be no space between --password= or
-p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlimport should not prompt for one, use the
--skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlimport does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

511

mysqlimport — A Data Import Program

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --replace, -r

Command-Line Format

--replace

The --replace and --ignore options control handling of input rows that duplicate existing rows
on unique key values. If you specify --replace, new rows replace existing rows that have the same
unique key value. If you specify --ignore, input rows that duplicate an existing row on a unique key
value are skipped. If you do not specify either option, an error occurs when a duplicate key value is
found, and the rest of the text file is ignored.

• --secure-auth

Command-Line Format

--secure-auth

512

mysqlimport — A Data Import Program

Deprecated

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated;expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --silent, -s

513

mysqlimport — A Data Import Program

Command-Line Format

--silent

Silent mode. Produce output only when errors occur.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

514

• --use-threads=N

Command-Line Format

--use-threads=#

mysqlpump — A Database Backup Program

Type

Numeric

Load files in parallel using N threads.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does.

• --version, -V

Command-Line Format

--version

Display version information and exit.

Here is a sample session that demonstrates use of mysqlimport:

$> mysql -e 'CREATE TABLE imptest(id INT, n VARCHAR(30))' test
$> ed
a
100     Max Sydow
101     Count Dracula
.
w imptest.txt
32
q
$> od -c imptest.txt
0000000   1   0   0  \t   M   a   x       S   y   d   o   w  \n   1   0
0000020   1  \t   C   o   u   n   t       D   r   a   c   u   l   a  \n
0000040
$> mysqlimport --local test imptest.txt
test.imptest: Records: 2  Deleted: 0  Skipped: 0  Warnings: 0
$> mysql -e 'SELECT * FROM imptest' test
+------+---------------+
| id   | n             |
+------+---------------+
|  100 | Max Sydow     |
|  101 | Count Dracula |
+------+---------------+

4.5.6 mysqlpump — A Database Backup Program

• mysqlpump Invocation Syntax

• mysqlpump Option Summary

• mysqlpump Option Descriptions

• mysqlpump Object Selection

• mysqlpump Parallel Processing

• mysqlpump Restrictions

The mysqlpump client utility performs logical backups, producing a set of SQL statements that can be
executed to reproduce the original database object definitions and table data. It dumps one or more
MySQL databases for backup or transfer to another SQL server.

515

mysqlpump — A Database Backup Program

mysqlpump features include:

• Parallel processing of databases, and of objects within databases, to speed up the dump process

• Better control over which databases and database objects (tables, stored programs, user accounts) to

dump

• Dumping of user accounts as account-management statements (CREATE USER, GRANT) rather than as

inserts into the mysql system database

• Capability of creating compressed output

• Progress indicator (the values are estimates)

• For dump file reloading, faster secondary index creation for InnoDB tables by adding indexes after rows

are inserted

mysqlpump requires at least the SELECT privilege for dumped tables, SHOW VIEW for dumped views,
TRIGGER for dumped triggers, and LOCK TABLES if the --single-transaction option is not used.
The SELECT privilege on the mysql system database is required to dump user definitions. Certain options
might require other privileges as noted in the option descriptions.

To reload a dump file, you must have the privileges required to execute the statements that it contains,
such as the appropriate CREATE privileges for objects created by those statements.

Note

A dump made using PowerShell on Windows with output redirection creates a file
that has UTF-16 encoding:

mysqlpump [options] > dump.sql

However, UTF-16 is not permitted as a connection character set (see Section 10.4,
“Connection Character Sets and Collations”), so the dump file does not load
correctly. To work around this issue, use the --result-file option, which
creates the output in ASCII format:

mysqlpump [options] --result-file=dump.sql

mysqlpump Invocation Syntax

By default, mysqlpump dumps all databases (with certain exceptions noted in mysqlpump Restrictions). To
specify this behavior explicitly, use the --all-databases option:

mysqlpump --all-databases

To dump a single database, or certain tables within that database, name the database on the command
line, optionally followed by table names:

mysqlpump db_name
mysqlpump db_name tbl_name1 tbl_name2 ...

To treat all name arguments as database names, use the --databases option:

mysqlpump --databases db_name1 db_name2 ...

By default, mysqlpump does not dump user account definitions, even if you dump the mysql system
database that contains the grant tables. To dump grant table contents as logical definitions in the form of
CREATE USER and GRANT statements, use the --users option and suppress all database dumping:

mysqlpump --exclude-databases=% --users

516

mysqlpump — A Database Backup Program

In the preceding command, % is a wildcard that matches all database names for the --exclude-
databases option.

mysqlpump supports several options for including or excluding databases, tables, stored programs, and
user definitions. See mysqlpump Object Selection.

To reload a dump file, execute the statements that it contains. For example, use the mysql client:

mysqlpump [options] > dump.sql
mysql < dump.sql

The following discussion provides additional mysqlpump usage examples.

To see a list of the options mysqlpump supports, issue the command mysqlpump --help.

mysqlpump Option Summary

mysqlpump supports the following options, which can be specified on the command line or in the
[mysqlpump] and [client] groups of an option file. (Prior to MySQL 5.7.30, mysqlpump read the
[mysql_dump] group rather than [mysqlpump]. As of 5.7.30, [mysql_dump] is still accepted but is
deprecated.) For information about option files used by MySQL programs, see Section 4.2.2.2, “Using
Option Files”.

Table 4.18 mysqlpump Options

Option Name

--add-drop-database

--add-drop-table

--add-drop-user

--add-locks

--all-databases

--bind-address

--character-sets-dir

--complete-insert

--compress

Description

Introduced

Add DROP DATABASE statement
before each CREATE DATABASE
statement

Add DROP TABLE statement
before each CREATE TABLE
statement

Add DROP USER statement
before each CREATE USER
statement

Surround each table dump with
LOCK TABLES and UNLOCK
TABLES statements

Dump all databases

Use specified network interface to
connect to MySQL Server

Directory where character sets are
installed

Use complete INSERT statements
that include column names

Compress all information sent
between client and server

--compress-output

Output compression algorithm

--databases

--debug

Interpret all name arguments as
database names

Write debugging log

517

mysqlpump — A Database Backup Program

Option Name

--debug-check

--debug-info

Description

Introduced

Print debugging information when
program exits

Print debugging information,
memory, and CPU statistics when
program exits

--default-auth

Authentication plugin to use

--default-character-set

Specify default character set

--default-parallelism

--defaults-extra-file

Default number of threads for
parallel processing

Read named option file in addition
to usual option files

--defaults-file

Read only named option file

--defaults-group-suffix

Option group suffix value

--defer-table-indexes

--events

For reloading, defer index creation
until after loading table rows

Dump events from dumped
databases

--exclude-databases

Databases to exclude from dump

--exclude-events

--exclude-routines

--exclude-tables

--exclude-triggers

--exclude-users

--extended-insert

Events to exclude from dump

Routines to exclude from dump

Tables to exclude from dump

Triggers to exclude from dump

Users to exclude from dump

Use multiple-row INSERT syntax

--get-server-public-key

Request RSA public key from
server

5.7.23

--help

--hex-blob

--host

Display help message and exit

Dump binary columns using
hexadecimal notation

Host on which MySQL server is
located

--include-databases

Databases to include in dump

--include-events

--include-routines

--include-tables

--include-triggers

--include-users

--insert-ignore

--log-error-file

Events to include in dump

Routines to include in dump

Tables to include in dump

Triggers to include in dump

Users to include in dump

Write INSERT IGNORE rather
than INSERT statements

Append warnings and errors to
named file

518

Option Name

--login-path

--max-allowed-packet

--net-buffer-length

--no-create-db

--no-create-info

--no-defaults

--parallel-schemas

--password

--plugin-dir

--port

--print-defaults

--protocol

--replace

--result-file

--routines

--secure-auth

--server-public-key-path

--set-charset

--set-gtid-purged

--single-transaction

--skip-definer

mysqlpump — A Database Backup Program

Description

Introduced

Read login path options
from .mylogin.cnf

Maximum packet length to send to
or receive from server

Buffer size for TCP/IP and socket
communication

Do not write CREATE DATABASE
statements

Do not write CREATE TABLE
statements that re-create each
dumped table

Read no option files

Specify schema-processing
parallelism

Password to use when connecting
to server

Directory where plugins are
installed

TCP/IP port number for
connection

Print default options

Transport protocol to use

Write REPLACE statements rather
than INSERT statements

Direct output to a given file

Dump stored routines (procedures
and functions) from dumped
databases

Do not send passwords to server
in old (pre-4.1) format

Path name to file containing RSA
public key

5.7.23

Add SET NAMES
default_character_set to output

Whether to add SET
@@GLOBAL.GTID_PURGED to
output

5.7.18

Dump tables within single
transaction

Omit DEFINER and SQL
SECURITY clauses from view
and stored program CREATE
statements

--skip-dump-rows

Do not dump table rows

519

Option Name

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

mysqlpump — A Database Backup Program

Description

Introduced

Unix socket file or Windows
named pipe to use

Enable connection encryption

File that contains list of trusted
SSL Certificate Authorities

Directory that contains trusted
SSL Certificate Authority
certificate files

File that contains X.509 certificate

Permissible ciphers for connection
encryption

File that contains certificate
revocation lists

Directory that contains certificate
revocation-list files

File that contains X.509 key

Desired security state of
connection to server

5.7.11

--ssl-verify-server-cert

--tls-version

Verify host name against server
certificate Common Name identity

Permissible TLS protocols for
encrypted connections

5.7.10

--triggers

--tz-utc

--user

--users

--version

Dump triggers for each dumped
table

Add SET TIME_ZONE='+00:00' to
dump file

MySQL user name to use when
connecting to server

Dump user accounts

Display version information and
exit

--watch-progress

Display progress indicator

mysqlpump Option Descriptions

• --help, -?

Command-Line Format

--help

Display a help message and exit.

• --add-drop-database

Command-Line Format

--add-drop-database

520

mysqlpump — A Database Backup Program

Write a DROP DATABASE statement before each CREATE DATABASE statement.

• --add-drop-table

Command-Line Format

--add-drop-table

Write a DROP TABLE statement before each CREATE TABLE statement.

• --add-drop-user

Command-Line Format

--add-drop-user

Write a DROP USER statement before each CREATE USER statement.

• --add-locks

Command-Line Format

--add-locks

Surround each table dump with LOCK TABLES and UNLOCK TABLES statements. This results in faster
inserts when the dump file is reloaded. See Section 8.2.4.1, “Optimizing INSERT Statements”.

This option does not work with parallelism because INSERT statements from different tables can be
interleaved and UNLOCK TABLES following the end of the inserts for one table could release locks on
tables for which inserts remain.

--add-locks and --single-transaction are mutually exclusive.

• --all-databases, -A

Command-Line Format

--all-databases

Dump all databases (with certain exceptions noted in mysqlpump Restrictions). This is the default
behavior if no other is specified explicitly.

--all-databases and --databases are mutually exclusive.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=path

521

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

mysqlpump — A Database Backup Program

• --complete-insert

Command-Line Format

--complete-insert

Write complete INSERT statements that include column names.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --compress-output=algorithm

Command-Line Format

--compress-output=algorithm

Type

Valid Values

Enumeration

LZ4

ZLIB

By default, mysqlpump does not compress output. This option specifies output compression using the
specified algorithm. Permitted algorithms are LZ4 and ZLIB.

To uncompress compressed output, you must have an appropriate utility. If the system commands
lz4 and openssl zlib are not available, as of MySQL 5.7.10, MySQL distributions include
lz4_decompress and zlib_decompress utilities that can be used to decompress mysqlpump output
that was compressed using the --compress-output=LZ4 and --compress-output=ZLIB options.
For more information, see Section 4.8.1, “lz4_decompress — Decompress mysqlpump LZ4-Compressed
Output”, and Section 4.8.5, “zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output”.

Alternatives include the lz4 and openssl commands, if they are installed on your system. For example,
lz4 can uncompress LZ4 output:

lz4 -d input_file output_file

ZLIB output can be uncompresed like this:

openssl zlib -d < input_file > output_file

• --databases, -B

Command-Line Format

--databases

522

Normally, mysqlpump treats the first name argument on the command line as a database name and
any following names as table names. With this option, it treats all name arguments as database names.
CREATE DATABASE statements are included in the output before each new database.

--all-databases and --databases are mutually exclusive.

mysqlpump — A Database Backup Program

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:O,/tmp/mysqlpump.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:O,/
tmp/mysqlpump.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

523

mysqlpump — A Database Backup Program

Default Value

utf8

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”. If
no character set is specified, mysqlpump uses utf8.

• --default-parallelism=N

Command-Line Format

--default-parallelism=N

Type

Default Value

Integer

2

The default number of threads for each parallel processing queue. The default is 2.

The --parallel-schemas option also affects parallelism and can be used to override the default
number of threads. For more information, see mysqlpump Parallel Processing.

With --default-parallelism=0 and no --parallel-schemas options, mysqlpump runs as a
single-threaded process and creates no queues.

With parallelism enabled, it is possible for output from different databases to be interleaved.

Note

Before MySQL 5.7.11, use of the --single-transaction option is mutually
exclusive with parallelism. To use --single-transaction, disable parallelism
by setting --default-parallelism to 0 and not using any instances of --
parallel-schemas:

mysqlpump --single-transaction --default-parallelism=0

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

524

mysqlpump — A Database Backup Program

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlpump normally reads the [client] and [mysqlpump] groups. If this option is
given as --defaults-group-suffix=_other, mysqlpump also reads the [client_other] and
[mysqlpump_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defer-table-indexes

Command-Line Format

--defer-table-indexes

Type

Default Value

Boolean

TRUE

In the dump output, defer index creation for each table until after its rows have been loaded. This works
for all storage engines, but for InnoDB applies only for secondary indexes.

This option is enabled by default; use --skip-defer-table-indexes to disable it.

• --events

Command-Line Format

Type

Default Value

--events

Boolean

TRUE

Include Event Scheduler events for the dumped databases in the output. Event dumping requires the
EVENT privileges for those databases.

The output generated by using --events contains CREATE EVENT statements to create the events.
However, these statements do not include attributes such as the event creation and modification
timestamps, so when the events are reloaded, they are created with timestamps equal to the reload
time.

If you require events to be created with their original timestamp attributes, do not use --events.
Instead, dump and reload the contents of the mysql.event table directly, using a MySQL account that
has appropriate privileges for the mysql database.

This option is enabled by default; use --skip-events to disable it.

• --exclude-databases=db_list

Command-Line Format

--exclude-databases=db_list

525

mysqlpump — A Database Backup Program

Type

String

Do not dump the databases in db_list, which is a list of one or more comma-separated database
names. Multiple instances of this option are additive. For more information, see mysqlpump Object
Selection.

• --exclude-events=event_list

Command-Line Format

--exclude-events=event_list

Type

String

Do not dump the databases in event_list, which is a list of one or more comma-separated event
names. Multiple instances of this option are additive. For more information, see mysqlpump Object
Selection.

• --exclude-routines=routine_list

Command-Line Format

--exclude-routines=routine_list

Type

String

Do not dump the events in routine_list, which is a list of one or more comma-separated routine
(stored procedure or function) names. Multiple instances of this option are additive. For more
information, see mysqlpump Object Selection.

• --exclude-tables=table_list

Command-Line Format

--exclude-tables=table_list

Type

String

Do not dump the tables in table_list, which is a list of one or more comma-separated table names.
Multiple instances of this option are additive. For more information, see mysqlpump Object Selection.

• --exclude-triggers=trigger_list

Command-Line Format

--exclude-triggers=trigger_list

Type

String

Do not dump the triggers in trigger_list, which is a list of one or more comma-separated trigger
names. Multiple instances of this option are additive. For more information, see mysqlpump Object
Selection.

• --exclude-users=user_list

526

Command-Line Format

--exclude-users=user_list

mysqlpump — A Database Backup Program

Type

String

Do not dump the user accounts in user_list, which is a list of one or more comma-separated account
names. Multiple instances of this option are additive. For more information, see mysqlpump Object
Selection.

• --extended-insert=N

Command-Line Format

--extended-insert=N

Write INSERT statements using multiple-row syntax that includes several VALUES lists. This results in a
smaller dump file and speeds up inserts when the file is reloaded.

The option value indicates the number of rows to include in each INSERT statement. The default is 250.
A value of 1 produces one INSERT statement per table row.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option
applies to clients that authenticate with the caching_sha2_password authentication plugin. For that
plugin, the server does not send the public key unless requested. This option is ignored for accounts that
do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --hex-blob

Command-Line Format

--hex-blob

Dump binary columns using hexadecimal notation (for example, 'abc' becomes 0x616263). The
affected data types are BINARY, VARBINARY, BLOB types, BIT, all spatial data types, and other non-
binary data types when used with the binary character set.

• --host=host_name, -h host_name

Command-Line Format

--host

Dump data from the MySQL server on the given host.

• --include-databases=db_list

527

mysqlpump — A Database Backup Program

Command-Line Format

--include-databases=db_list

Type

String

Dump the databases in db_list, which is a list of one or more comma-separated database names.
The dump includes all objects in the named databases. Multiple instances of this option are additive. For
more information, see mysqlpump Object Selection.

• --include-events=event_list

Command-Line Format

--include-events=event_list

Type

String

Dump the events in event_list, which is a list of one or more comma-separated event names.
Multiple instances of this option are additive. For more information, see mysqlpump Object Selection.

• --include-routines=routine_list

Command-Line Format

--include-routines=routine_list

Type

String

Dump the routines in routine_list, which is a list of one or more comma-separated routine (stored
procedure or function) names. Multiple instances of this option are additive. For more information, see
mysqlpump Object Selection.

• --include-tables=table_list

Command-Line Format

--include-tables=table_list

Type

String

Dump the tables in table_list, which is a list of one or more comma-separated table names. Multiple
instances of this option are additive. For more information, see mysqlpump Object Selection.

• --include-triggers=trigger_list

Command-Line Format

--include-triggers=trigger_list

Type

String

Dump the triggers in trigger_list, which is a list of one or more comma-separated trigger names.
Multiple instances of this option are additive. For more information, see mysqlpump Object Selection.

• --include-users=user_list

Command-Line Format

--include-users=user_list

Type

String

Dump the user accounts in user_list, which is a list of one or more comma-separated user names.
Multiple instances of this option are additive. For more information, see mysqlpump Object Selection.

528

mysqlpump — A Database Backup Program

• --insert-ignore

Command-Line Format

--insert-ignore

Write INSERT IGNORE statements rather than INSERT statements.

• --log-error-file=file_name

Command-Line Format

--log-error-file=file_name

Type

File name

Log warnings and errors by appending them to the named file. If this option is not given, mysqlpump
writes warnings and errors to the standard error output.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --max-allowed-packet=N

Command-Line Format

--max-allowed-packet=N

Type

Default Value

Numeric

25165824

The maximum size of the buffer for client/server communication. The default is 24MB, the maximum is
1GB.

• --net-buffer-length=N

Command-Line Format

--net-buffer-length=N

Type

Default Value

Numeric

1047552

The initial size of the buffer for client/server communication. When creating multiple-row INSERT
statements (as with the --extended-insert option), mysqlpump creates rows up to N bytes long. If
you use this option to increase the value, ensure that the MySQL server net_buffer_length system
variable has a value at least this large.

529

mysqlpump — A Database Backup Program

• --no-create-db

Command-Line Format

--no-create-db

Suppress any CREATE DATABASE statements that might otherwise be included in the output.

• --no-create-info, -t

Command-Line Format

--no-create-info

Do not write CREATE TABLE statements that create each dumped table.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --parallel-schemas=[N:]db_list

Command-Line Format

--parallel-schemas=[N:]schema_list

Type

String

Create a queue for processing the databases in db_list, which is a list of one or more comma-
separated database names. If N is given, the queue uses N threads. If N is not given, the --default-
parallelism option determines the number of queue threads.

Multiple instances of this option create multiple queues. mysqlpump also creates a default queue to
use for databases not named in any --parallel-schemas option, and for dumping user definitions if
command options select them. For more information, see mysqlpump Parallel Processing.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

530

mysqlpump — A Database Backup Program

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqlpump prompts for one. If given, there must be no space between --password= or -
p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlpump should not prompt for one, use the
--skip-password option.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlpump does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

531

mysqlpump — A Database Backup Program

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --replace

Command-Line Format

--replace

Write REPLACE statements rather than INSERT statements.

• --result-file=file_name

Command-Line Format

--result-file=file_name

Type

File name

Direct output to the named file. The result file is created and its previous contents overwritten, even if an
error occurs while generating the dump.

This option should be used on Windows to prevent newline \n characters from being converted to \r\n
carriage return/newline sequences.

• --routines

Command-Line Format

Type

Default Value

--routines

Boolean

TRUE

Include stored routines (procedures and functions) for the dumped databases in the output. This option
requires the SELECT privilege for the mysql.proc table.

The output generated by using --routines contains CREATE PROCEDURE and CREATE FUNCTION
statements to create the routines. However, these statements do not include attributes such as the
routine creation and modification timestamps, so when the routines are reloaded, they are created with
timestamps equal to the reload time.

If you require routines to be created with their original timestamp attributes, do not use --routines.
Instead, dump and reload the contents of the mysql.proc table directly, using a MySQL account that
has appropriate privileges for the mysql database.

This option is enabled by default; use --skip-routines to disable it.

532

mysqlpump — A Database Backup Program

• --secure-auth

Command-Line Format

--secure-auth

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

This option is deprecated; expect it to be removed in a future MySQL release. It is always enabled and
attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an error.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --set-charset

Command-Line Format

--set-charset

Write SET NAMES default_character_set to the output.

This option is enabled by default. To disable it and suppress the SET NAMES statement, use --skip-
set-charset.

• --set-gtid-purged=value

Command-Line Format

--set-gtid-purged=value

Introduced

Type

Default Value

Valid Values

5.7.18

Enumeration

AUTO

OFF

ON

533

mysqlpump — A Database Backup Program

AUTO

This option enables control over global transaction ID (GTID) information written to the dump file, by
indicating whether to add a SET @@GLOBAL.gtid_purged statement to the output. This option may
also cause a statement to be written to the output that disables binary logging while the dump file is
being reloaded.

The following table shows the permitted option values. The default value is AUTO.

Value

OFF

ON

AUTO

Meaning

Add no SET statement to the output.

Add a SET statement to the output. An error occurs
if GTIDs are not enabled on the server.

Add a SET statement to the output if GTIDs are
enabled on the server.

The --set-gtid-purged option has the following effect on binary logging when the dump file is
reloaded:

• --set-gtid-purged=OFF: SET @@SESSION.SQL_LOG_BIN=0; is not added to the output.

• --set-gtid-purged=ON: SET @@SESSION.SQL_LOG_BIN=0; is added to the output.

• --set-gtid-purged=AUTO: SET @@SESSION.SQL_LOG_BIN=0; is added to the output if GTIDs

are enabled on the server you are backing up (that is, if AUTO evaluates to ON).

This option was added in MySQL 5.7.18.

• --single-transaction

Command-Line Format

--single-transaction

This option sets the transaction isolation mode to REPEATABLE READ and sends a START
TRANSACTION SQL statement to the server before dumping data. It is useful only with transactional
tables such as InnoDB, because then it dumps the consistent state of the database at the time when
START TRANSACTION was issued without blocking any applications.

When using this option, you should keep in mind that only InnoDB tables are dumped in a consistent
state. For example, any MyISAM or MEMORY tables dumped while using this option may still change
state.

While a --single-transaction dump is in process, to ensure a valid dump file (correct table
contents and binary log coordinates), no other connection should use the following statements: ALTER
TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE. A consistent read is not

534

mysqlpump — A Database Backup Program

isolated from those statements, so use of them on a table to be dumped can cause the SELECT that is
performed by mysqlpump to retrieve the table contents to obtain incorrect contents or fail.

--add-locks and --single-transaction are mutually exclusive.

Note

Before MySQL 5.7.11, use of the --single-transaction option is mutually
exclusive with parallelism. To use --single-transaction, disable parallelism
by setting --default-parallelism to 0 and not using any instances of --
parallel-schemas:

mysqlpump --single-transaction --default-parallelism=0

• --skip-definer

Command-Line Format

--skip-definer

Type

Default Value

Boolean

FALSE

Omit DEFINER and SQL SECURITY clauses from the CREATE statements for views and stored
programs. The dump file, when reloaded, creates objects that use the default DEFINER and SQL
SECURITY values. See Section 23.6, “Stored Object Access Control”.

• --skip-dump-rows, -d

Command-Line Format

--skip-dump-rows

Type

Default Value

Do not dump table rows.

• --socket=path, -S path

Boolean

FALSE

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

535

mysqlpump — A Database Backup Program

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --triggers

Command-Line Format

Type

Default Value

--triggers

Boolean

TRUE

Include triggers for each dumped table in the output.

This option is enabled by default; use --skip-triggers to disable it.

• --tz-utc

Command-Line Format

--tz-utc

This option enables TIMESTAMP columns to be dumped and reloaded between servers in different time
zones. mysqlpump sets its connection time zone to UTC and adds SET TIME_ZONE='+00:00' to the
dump file. Without this option, TIMESTAMP columns are dumped and reloaded in the time zones local to
the source and destination servers, which can cause the values to change if the servers are in different
time zones. --tz-utc also protects against changes due to daylight saving time.

This option is enabled by default; use --skip-tz-utc to disable it.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

Type

String

The user name of the MySQL account to use for connecting to the server.

• --users

Command-Line Format

Type

Default Value

--users

Boolean

FALSE

536

mysqlpump — A Database Backup Program

Dump user accounts as logical definitions in the form of CREATE USER and GRANT statements.

User definitions are stored in the grant tables in the mysql system database. By default, mysqlpump
does not include the grant tables in mysql database dumps. To dump the contents of the grant tables as
logical definitions, use the --users option and suppress all database dumping:

mysqlpump --exclude-databases=% --users

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --watch-progress

Command-Line Format

--watch-progress

Type

Default Value

Boolean

TRUE

Periodically display a progress indicator that provides information about the completed and total number
of tables, rows, and other objects.

This option is enabled by default; use --skip-watch-progress to disable it.

mysqlpump Object Selection

mysqlpump has a set of inclusion and exclusion options that enable filtering of several object types and
provide flexible control over which objects to dump:

• --include-databases and --exclude-databases apply to databases and all objects within them.

• --include-tables and --exclude-tables apply to tables. These options also affect triggers

associated with tables unless the trigger-specific options are given.

• --include-triggers and --exclude-triggers apply to triggers.

• --include-routines and --exclude-routines apply to stored procedures and functions. If a

routine option matches a stored procedure name, it also matches a stored function of the same name.

• --include-events and --exclude-events apply to Event Scheduler events.

• --include-users and --exclude-users apply to user accounts.

Any inclusion or exclusion option may be given multiple times. The effect is additive. Order of these options
does not matter.

The value of each inclusion and exclusion option is a list of comma-separated names of the appropriate
object type. For example:

--exclude-databases=test,world
--include-tables=customer,invoice

Wildcard characters are permitted in the object names:

• % matches any sequence of zero or more characters.

537

mysqlpump — A Database Backup Program

• _ matches any single character.

For example, --include-tables=t%,__tmp matches all table names that begin with t and all five-
character table names that end with tmp.

For users, a name specified without a host part is interpreted with an implied host of %. For example, u1
and u1@% are equivalent. This is the same equivalence that applies in MySQL generally (see Section 6.2.4,
“Specifying Account Names”).

Inclusion and exclusion options interact as follows:

• By default, with no inclusion or exclusion options, mysqlpump dumps all databases (with certain

exceptions noted in mysqlpump Restrictions).

• If inclusion options are given in the absence of exclusion options, only the objects named as included are

dumped.

• If exclusion options are given in the absence of inclusion options, all objects are dumped except those

named as excluded.

• If inclusion and exclusion options are given, all objects named as excluded and not named as included

are not dumped. All other objects are dumped.

If multiple databases are being dumped, it is possible to name tables, triggers, and routines in a specific
database by qualifying the object names with the database name. The following command dumps
databases db1 and db2, but excludes tables db1.t1 and db2.t2:

mysqlpump --include-databases=db1,db2 --exclude-tables=db1.t1,db2.t2

The following options provide alternative ways to specify which databases to dump:

• The --all-databases option dumps all databases (with certain exceptions noted in mysqlpump

Restrictions). It is equivalent to specifying no object options at all (the default mysqlpump action is to
dump everything).

--include-databases=% is similar to --all-databases, but selects all databases for dumping,
even those that are exceptions for --all-databases.

• The --databases option causes mysqlpump to treat all name arguments as names of databases to

dump. It is equivalent to an --include-databases option that names the same databases.

mysqlpump Parallel Processing

mysqlpump can use parallelism to achieve concurrent processing. You can select concurrency between
databases (to dump multiple databases simultaneously) and within databases (to dump multiple objects
from a given database simultaneously).

By default, mysqlpump sets up one queue with two threads. You can create additional queues and control
the number of threads assigned to each one, including the default queue:

• --default-parallelism=N specifies the default number of threads used for each queue. In the

absence of this option, N is 2.

The default queue always uses the default number of threads. Additional queues use the default number
of threads unless you specify otherwise.

• --parallel-schemas=[N:]db_list sets up a processing queue for dumping the databases named
in db_list and optionally specifies how many threads the queue uses. db_list is a list of comma-

538

mysqlpump — A Database Backup Program

separated database names. If the option argument begins with N:, the queue uses N threads. Otherwise,
the --default-parallelism option determines the number of queue threads.

Multiple instances of the --parallel-schemas option create multiple queues.

Names in the database list are permitted to contain the same % and _ wildcard characters supported for
filtering options (see mysqlpump Object Selection).

mysqlpump uses the default queue for processing any databases not named explicitly with a --
parallel-schemas option, and for dumping user definitions if command options select them.

In general, with multiple queues, mysqlpump uses parallelism between the sets of databases processed
by the queues, to dump multiple databases simultaneously. For a queue that uses multiple threads,
mysqlpump uses parallelism within databases, to dump multiple objects from a given database
simultaneously. Exceptions can occur; for example, mysqlpump may block queues while it obtains from
the server lists of objects in databases.

With parallelism enabled, it is possible for output from different databases to be interleaved. For example,
INSERT statements from multiple tables dumped in parallel can be interleaved; the statements are not
written in any particular order. This does not affect reloading because output statements qualify object
names with database names or are preceded by USE statements as required.

The granularity for parallelism is a single database object. For example, a single table cannot be dumped
in parallel using multiple threads.

Examples:

mysqlpump --parallel-schemas=db1,db2 --parallel-schemas=db3

mysqlpump sets up a queue to process db1 and db2, another queue to process db3, and a default queue
to process all other databases. All queues use two threads.

mysqlpump --parallel-schemas=db1,db2 --parallel-schemas=db3
          --default-parallelism=4

This is the same as the previous example except that all queues use four threads.

mysqlpump --parallel-schemas=5:db1,db2 --parallel-schemas=3:db3

The queue for db1 and db2 uses five threads, the queue for db3 uses three threads, and the default
queue uses the default of two threads.

As a special case, with --default-parallelism=0 and no --parallel-schemas options,
mysqlpump runs as a single-threaded process and creates no queues.

Note

Before MySQL 5.7.11, use of the --single-transaction option is mutually
exclusive with parallelism. To use --single-transaction, disable parallelism
by setting --default-parallelism to 0 and not using any instances of --
parallel-schemas:

mysqlpump --single-transaction --default-parallelism=0

mysqlpump Restrictions

mysqlpump does not dump the INFORMATION_SCHEMA, performance_schema, ndbinfo, or sys
schema by default. To dump any of these, name them explicitly on the command line. You can also name
them with the --databases or --include-databases option.

539

mysqlshow — Display Database, Table, and Column Information

mysqlpump does not dump InnoDB CREATE TABLESPACE statements.

mysqlpump dumps user accounts in logical form using CREATE USER and GRANT statements (for
example, when you use the --include-users or --users option). For this reason, dumps of the
mysql system database do not by default include the grant tables that contain user definitions: user,
db, tables_priv, columns_priv, procs_priv, or proxies_priv. To dump any of the grant tables,
name the mysql database followed by the table names:

mysqlpump mysql user db ...

4.5.7 mysqlshow — Display Database, Table, and Column Information

The mysqlshow client can be used to quickly see which databases exist, their tables, or a table's columns
or indexes.

mysqlshow provides a command-line interface to several SQL SHOW statements. See Section 13.7.5,
“SHOW Statements”. The same information can be obtained by using those statements directly. For
example, you can issue them from the mysql client program.

Invoke mysqlshow like this:

mysqlshow [options] [db_name [tbl_name [col_name]]]

• If no database is given, a list of database names is shown.

• If no table is given, all matching tables in the database are shown.

• If no column is given, all matching columns and column types in the table are shown.

The output displays only the names of those databases, tables, or columns for which you have some
privileges.

If the last argument contains shell or SQL wildcard characters (*, ?, %, or _), only those names that are
matched by the wildcard are shown. If a database name contains any underscores, those should be
escaped with a backslash (some Unix shells require two) to get a list of the proper tables or columns. *
and ? characters are converted into SQL % and _ wildcard characters. This might cause some confusion
when you try to display the columns for a table with a _ in the name, because in this case, mysqlshow
shows you only the table names that match the pattern. This is easily fixed by adding an extra % last on the
command line as a separate argument.

mysqlshow supports the following options, which can be specified on the command line or in the
[mysqlshow] and [client] groups of an option file. For information about option files used by MySQL
programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.19 mysqlshow Options

Option Name

--bind-address

--character-sets-dir

--compress

540

Description

Introduced

Deprecated

Use specified network
interface to connect to
MySQL Server

Directory where
character sets can be
found

Compress all information
sent between client and
server

mysqlshow — Display Database, Table, and Column Information

Option Name

Description

Introduced

Deprecated

--count

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

Show the number of rows
per table

Write debugging log

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Specify default character
set

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--enable-cleartext-plugin Enable cleartext

5.7.10

--get-server-public-key

authentication plugin

Request RSA public key
from server

5.7.23

--help

--host

--keys

--login-path

--no-defaults

--password

--pipe

--plugin-dir

--port

Display help message
and exit

Host on which MySQL
server is located

Show table indexes

Read login path options
from .mylogin.cnf

Read no option files

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--protocol

Transport protocol to use

541

mysqlshow — Display Database, Table, and Column Information

Option Name

--secure-auth

Description

Introduced

Deprecated

Do not send passwords
to server in old (pre-4.1)
format

Yes

--server-public-key-path Path name to file

5.7.23

--shared-memory-base-
name

--show-table-type

--socket

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--status

--tls-version

containing RSA public
key

Shared-memory name
for shared-memory
connections (Windows
only)

Show a column indicating
the table type

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

Verify host name
against server certificate
Common Name identity

Display extra information
about each table

Permissible TLS
protocols for encrypted
connections

5.7.10

542

mysqlshow — Display Database, Table, and Column Information

Option Name

Description

Introduced

Deprecated

--user

--verbose

--version

• --help, -?

MySQL user name to
use when connecting to
server

Verbose mode

Display version
information and exit

Command-Line Format

--help

Display a help message and exit.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=path

Type

Default Value

String

[none]

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --count

Command-Line Format

--count

Show the number of rows per table. This can be slow for non-MyISAM tables.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

String

543

mysqlshow — Display Database, Table, and Column Information

Default Value

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 10.15, “Character Set Configuration”.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

544

mysqlshow — Display Database, Table, and Column Information

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlshow normally reads the [client] and [mysqlshow] groups. If this option is
given as --defaults-group-suffix=_other, mysqlshow also reads the [client_other] and
[mysqlshow_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Introduced

Type

Default Value

5.7.10

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

This option was added in MySQL 5.7.10.

• --get-server-public-key

Command-Line Format

Introduced

--get-server-public-key

5.7.23

545

mysqlshow — Display Database, Table, and Column Information

Type

Boolean

Request from the server the RSA public key that it uses for key pair-based password exchange.
This option applies to clients that connect to the server using an account that authenticates with the
caching_sha2_password authentication plugin. For connections by such accounts, the server does
not send the public key to the client unless requested. The option is ignored for accounts that do not
authenticate with that plugin. It is also ignored if RSA-based password exchange is not needed, as is the
case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Connect to the MySQL server on the given host.

• --keys, -k

Command-Line Format

--keys

Show table indexes.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

546

mysqlshow — Display Database, Table, and Column Information

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqlshow prompts for one. If given, there must be no space between --password= or -
p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlshow should not prompt for one, use the
--skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlshow does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

Type

--port=port_num

Numeric

547

mysqlshow — Display Database, Table, and Column Information

Default Value

3306

For TCP/IP connections, the port number to use.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --server-public-key-path=file_name

548

mysqlshow — Display Database, Table, and Column Information

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --show-table-type, -t

Command-Line Format

--show-table-type

Show a column indicating the table type, as in SHOW FULL TABLES. The type is BASE TABLE or VIEW.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

549

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

mysqlslap — A Load Emulation Client

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --status, -i

Command-Line Format

--status

Display extra information about each table.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This option can be used multiple
times to increase the amount of information.

• --version, -V

Command-Line Format

--version

Display version information and exit.

4.5.8 mysqlslap — A Load Emulation Client

550

mysqlslap — A Load Emulation Client

mysqlslap is a diagnostic program designed to emulate client load for a MySQL server and to report the
timing of each stage. It works as if multiple clients are accessing the server.

Invoke mysqlslap like this:

mysqlslap [options]

Some options such as --create or --query enable you to specify a string containing an SQL statement
or a file containing statements. If you specify a file, by default it must contain one statement per line. (That
is, the implicit statement delimiter is the newline character.) Use the --delimiter option to specify
a different delimiter, which enables you to specify statements that span multiple lines or place multiple
statements on a single line. You cannot include comments in a file; mysqlslap does not understand them.

mysqlslap runs in three stages:

1. Create schema, table, and optionally any stored programs or data to use for the test. This stage uses a

single client connection.

2. Run the load test. This stage can use many client connections.

3. Clean up (disconnect, drop table if specified). This stage uses a single client connection.

Examples:

Supply your own create and query SQL statements, with 50 clients querying and 200 selects for each
(enter the command on a single line):

mysqlslap --delimiter=";"
  --create="CREATE TABLE a (b int);INSERT INTO a VALUES (23)"
  --query="SELECT * FROM a" --concurrency=50 --iterations=200

Let mysqlslap build the query SQL statement with a table of two INT columns and three VARCHAR
columns. Use five clients querying 20 times each. Do not create the table or insert the data (that is, use the
previous test's schema and data):

mysqlslap --concurrency=5 --iterations=20
  --number-int-cols=2 --number-char-cols=3
  --auto-generate-sql

Tell the program to load the create, insert, and query SQL statements from the specified files, where the
create.sql file has multiple table creation statements delimited by ';' and multiple insert statements
delimited by ';'. The --query file has multiple queries delimited by ';'. Run all the load statements,
then run all the queries in the query file with five clients (five times each):

mysqlslap --concurrency=5
  --iterations=5 --query=query.sql --create=create.sql
  --delimiter=";"

mysqlslap supports the following options, which can be specified on the command line or in the
[mysqlslap] and [client] groups of an option file. For information about option files used by MySQL
programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.20 mysqlslap Options

Option Name

Description

Introduced

Deprecated

--auto-generate-sql

Generate SQL
statements automatically
when they are not
supplied in files or using
command options

551

mysqlslap — A Load Emulation Client

Option Name

Description

Introduced

Deprecated

--auto-generate-sql-add-
autoincrement

--auto-generate-sql-
execute-number

--auto-generate-sql-guid-
primary

--auto-generate-sql-load-
type

--auto-generate-sql-
secondary-indexes

--auto-generate-sql-
unique-query-number

--auto-generate-sql-
unique-write-number

Add AUTO_INCREMENT
column to automatically
generated tables

Specify how many
queries to generate
automatically

Add a GUID-based
primary key to
automatically generated
tables

Specify the test load type

Specify how many
secondary indexes to
add to automatically
generated tables

How many different
queries to generate for
automatic tests

How many different
queries to generate for --
auto-generate-sql-write-
number

--auto-generate-sql-write-
number

How many row inserts to
perform on each thread

--commit

--compress

--concurrency

--create

--create-schema

--csv

--debug

--debug-check

How many statements
to execute before
committing

Compress all information
sent between client and
server

Number of clients to
simulate when issuing
the SELECT statement

File or string containing
the statement to use for
creating the table

Schema in which to run
the tests

Generate output in
comma-separated values
format

Write debugging log

Print debugging
information when
program exits

552

Option Name

--debug-info

--default-auth

--defaults-extra-file

--defaults-file

mysqlslap — A Load Emulation Client

Description

Introduced

Deprecated

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--delimiter

--detach

Delimiter to use in SQL
statements

Detach (close and
reopen) each connection
after each N statements

--enable-cleartext-plugin Enable cleartext

--engine

authentication plugin

Storage engine to use for
creating the table

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--host

--iterations

--login-path

--no-defaults

--no-drop

--number-char-cols

--number-int-cols

--number-of-queries

Display help message
and exit

Host on which MySQL
server is located

Number of times to run
the tests

Read login path options
from .mylogin.cnf

Read no option files

Do not drop any schema
created during the test
run

Number of VARCHAR
columns to use if --auto-
generate-sql is specified

Number of INT columns
to use if --auto-generate-
sql is specified

Limit each client to
approximately this
number of queries

553

Option Name

--only-print

--password

--pipe

--plugin-dir

--port

--post-query

--post-system

--pre-query

--pre-system

mysqlslap — A Load Emulation Client

Description

Introduced

Deprecated

Do not connect to
databases. mysqlslap
only prints what it would
have done

Password to use when
connecting to server

Connect to server using
named pipe (Windows
only)

Directory where plugins
are installed

TCP/IP port number for
connection

File or string containing
the statement to execute
after the tests have
completed

String to execute using
system() after the tests
have completed

File or string containing
the statement to execute
before running the tests

String to execute using
system() before running
the tests

--print-defaults

Print default options

--protocol

--query

--secure-auth

Transport protocol to use

File or string containing
the SELECT statement to
use for retrieving data

Do not send passwords
to server in old (pre-4.1)
format

--server-public-key-path Path name to file

5.7.23

--shared-memory-base-
name

--silent

--socket

containing RSA public
key

Shared-memory name
for shared-memory
connections (Windows
only)

Silent mode

Unix socket file or
Windows named pipe to
use

Yes

554

mysqlslap — A Load Emulation Client

Description

Introduced

Deprecated

Set SQL mode for client
session

Enable connection
encryption

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

5.7.10

Verify host name
against server certificate
Common Name identity

Permissible TLS
protocols for encrypted
connections

MySQL user name to
use when connecting to
server

Verbose mode

Display version
information and exit

Option Name

--sql-mode

--ssl

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

--ssl-verify-server-cert

--tls-version

--user

--verbose

--version

• --help, -?

Command-Line Format

--help

Display a help message and exit.

• --auto-generate-sql, -a

Command-Line Format

--auto-generate-sql

Type

Boolean

555

mysqlslap — A Load Emulation Client

Default Value

FALSE

Generate SQL statements automatically when they are not supplied in files or using command options.

• --auto-generate-sql-add-autoincrement

Command-Line Format

--auto-generate-sql-add-autoincrement

Type

Default Value

Boolean

FALSE

Add an AUTO_INCREMENT column to automatically generated tables.

• --auto-generate-sql-execute-number=N

Command-Line Format

--auto-generate-sql-execute-number=#

Type

Numeric

Specify how many queries to generate automatically.

• --auto-generate-sql-guid-primary

Command-Line Format

--auto-generate-sql-guid-primary

Type

Default Value

Boolean

FALSE

Add a GUID-based primary key to automatically generated tables.

• --auto-generate-sql-load-type=type

Command-Line Format

--auto-generate-sql-load-type=type

Type

Default Value

Valid Values

Enumeration

mixed

read

write

key

update

mixed

556

Specify the test load type. The permissible values are read (scan tables), write (insert into tables),
key (read primary keys), update (update primary keys), or mixed (half inserts, half scanning selects).
The default is mixed.

mysqlslap — A Load Emulation Client

• --auto-generate-sql-secondary-indexes=N

Command-Line Format

Type

Default Value

--auto-generate-sql-secondary-
indexes=#

Numeric

0

Specify how many secondary indexes to add to automatically generated tables. By default, none are
added.

• --auto-generate-sql-unique-query-number=N

Command-Line Format

Type

Default Value

--auto-generate-sql-unique-query-
number=#

Numeric

10

How many different queries to generate for automatic tests. For example, if you run a key test that
performs 1000 selects, you can use this option with a value of 1000 to run 1000 unique queries, or with a
value of 50 to perform 50 different selects. The default is 10.

• --auto-generate-sql-unique-write-number=N

Command-Line Format

Type

Default Value

--auto-generate-sql-unique-write-
number=#

Numeric

10

How many different queries to generate for --auto-generate-sql-write-number. The default is
10.

• --auto-generate-sql-write-number=N

Command-Line Format

--auto-generate-sql-write-number=#

Type

Default Value

Numeric

100

How many row inserts to perform. The default is 100.

• --commit=N

Command-Line Format

Type

Default Value

--commit=#

Numeric

0

557

How many statements to execute before committing. The default is 0 (no commits are done).

mysqlslap — A Load Emulation Client

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 4.2.6,
“Connection Compression Control”.

• --concurrency=N, -c N

Command-Line Format

Type

The number of parallel clients to simulate.

• --create=value

Command-Line Format

Type

--concurrency=#

Numeric

--create=value

String

The file or string containing the statement to use for creating the table.

• --create-schema=value

Command-Line Format

--create-schema=value

Type

String

The schema in which to run the tests.

Note

If the --auto-generate-sql option is also given, mysqlslap drops the
schema at the end of the test run. To avoid this, use the --no-drop option as
well.

• --csv[=file_name]

Command-Line Format

Type

--csv=[file]

File name

Generate output in comma-separated values format. The output goes to the named file, or to the
standard output if no file is given.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

String

558

mysqlslap — A Load Emulation Client

Default Value

d:t:o,/tmp/mysqlslap.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/mysqlslap.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

559

mysqlslap — A Load Emulation Client

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlslap normally reads the [client] and [mysqlslap] groups. If this option is
given as --defaults-group-suffix=_other, mysqlslap also reads the [client_other] and
[mysqlslap_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --delimiter=str, -F str

Command-Line Format

Type

--delimiter=str

String

The delimiter to use in SQL statements supplied in files or using command options.

• --detach=N

Command-Line Format

Type

Default Value

--detach=#

Numeric

0

Detach (close and reopen) each connection after each N statements. The default is 0 (connections are
not detached).

• --enable-cleartext-plugin

560

Command-Line Format

--enable-cleartext-plugin

Type

Boolean

mysqlslap — A Load Emulation Client

Default Value

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 6.4.1.6, “Client-Side
Cleartext Pluggable Authentication”.)

• --engine=engine_name, -e engine_name

Command-Line Format

--engine=engine_name

Type

String

The storage engine to use for creating tables.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Introduced

Type

5.7.23

Boolean

Request from the server the RSA public key that it uses for key pair-based password exchange.
This option applies to clients that connect to the server using an account that authenticates with the
caching_sha2_password authentication plugin. For connections by such accounts, the server does
not send the public key to the client unless requested. The option is ignored for accounts that do not
authenticate with that plugin. It is also ignored if RSA-based password exchange is not needed, as is the
case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Connect to the MySQL server on the given host.

• --iterations=N, -i N

Command-Line Format

Type

The number of times to run the tests.

• --login-path=name

--iterations=#

Numeric

561

mysqlslap — A Load Emulation Client

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-drop

Command-Line Format

Type

Default Value

--no-drop

Boolean

FALSE

Prevent mysqlslap from dropping any schema it creates during the test run.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --number-char-cols=N, -x N

Command-Line Format

--number-char-cols=#

Type

Numeric

The number of VARCHAR columns to use if --auto-generate-sql is specified.

• --number-int-cols=N, -y N

Command-Line Format

--number-int-cols=#

562

Type

Numeric

The number of INT columns to use if --auto-generate-sql is specified.

mysqlslap — A Load Emulation Client

• --number-of-queries=N

Command-Line Format

--number-of-queries=#

Type

Numeric

Limit each client to approximately this many queries. Query counting takes into account the statement
delimiter. For example, if you invoke mysqlslap as follows, the ; delimiter is recognized so that each
instance of the query string counts as two queries. As a result, 5 rows (not 10) are inserted.

mysqlslap --delimiter=";" --number-of-queries=10
          --query="use test;insert into t values(null)"

• --only-print

Command-Line Format

--only-print

Type

Default Value

Boolean

FALSE

Do not connect to databases. mysqlslap only prints what it would have done.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqlslap prompts for one. If given, there must be no space between --password= or -
p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlslap should not prompt for one, use the
--skip-password option.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

563

mysqlslap — A Load Emulation Client

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlslap does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use.

• --post-query=value

Command-Line Format

--post-query=value

Type

String

The file or string containing the statement to execute after the tests have completed. This execution is
not counted for timing purposes.

• --post-system=str

Command-Line Format

--post-system=str

Type

String

The string to execute using system() after the tests have completed. This execution is not counted for
timing purposes.

• --pre-query=value

Command-Line Format

--pre-query=value

Type

String

The file or string containing the statement to execute before running the tests. This execution is not
counted for timing purposes.

• --pre-system=str

Command-Line Format

--pre-system=str

Type

String

The string to execute using system() before running the tests. This execution is not counted for timing
purposes.

• --print-defaults

Command-Line Format

--print-defaults

564

mysqlslap — A Load Emulation Client

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --query=value, -q value

Command-Line Format

Type

--query=value

String

The file or string containing the SELECT statement to use for retrieving data.

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --server-public-key-path=file_name

565

mysqlslap — A Load Emulation Client

Command-Line Format

--server-public-key-path=file_name

Introduced

Type

5.7.23

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --silent, -s

Command-Line Format

--silent

Silent mode. No output.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

566

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

mysqlslap — A Load Emulation Client

• --sql-mode=mode

Command-Line Format

Type

--sql-mode=mode

String

Set the SQL mode for the client session.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This option can be used multiple
times to increase the amount of information.

• --version, -V

567

Command-Line Format

--version

Display version information and exit.

Administrative and Utility Programs

4.6 Administrative and Utility Programs

This section describes administrative programs and programs that perform miscellaneous utility operations.

4.6.1 innochecksum — Offline InnoDB File Checksum Utility

innochecksum prints checksums for InnoDB files. This tool reads an InnoDB tablespace file, calculates
the checksum for each page, compares the calculated checksum to the stored checksum, and reports
mismatches, which indicate damaged pages. It was originally developed to speed up verifying the
integrity of tablespace files after power outages but can also be used after file copies. Because checksum
mismatches cause InnoDB to deliberately shut down a running server, it may be preferable to use this tool
rather than waiting for an in-production server to encounter the damaged pages.

innochecksum cannot be used on tablespace files that the server already has open. For such files, you
should use CHECK TABLE to check tables within the tablespace. Attempting to run innochecksum on a
tablespace that the server already has open results in an Unable to lock file error.

If checksum mismatches are found, restore the tablespace from backup or start the server and attempt to
use mysqldump to make a backup of the tables within the tablespace.

Invoke innochecksum like this:

innochecksum [options] file_name

innochecksum Options

innochecksum supports the following options. For options that refer to page numbers, the numbers are
zero-based.

• --help, -?

Command-Line Format

Type

Default Value

Displays command line help. Example usage:

innochecksum --help

• --info, -I

Command-Line Format

Type

Default Value

--help

Boolean

false

--info

Boolean

false

Synonym for --help. Displays command line help. Example usage:

innochecksum --info

• --version, -V

Command-Line Format

Type

--version

Boolean

568

innochecksum — Offline InnoDB File Checksum Utility

Default Value

false

Displays version information. Example usage:

innochecksum --version

• --verbose, -v

Command-Line Format

Type

Default Value

--verbose

Boolean

false

Verbose mode; prints a progress indicator to the log file every five seconds. In order for the progress
indicator to be printed, the log file must be specified using the --log option. To turn on verbose
mode, run:

innochecksum --verbose

To turn off verbose mode, run:

innochecksum --verbose=FALSE

The --verbose option and --log option can be specified at the same time. For example:

innochecksum --verbose --log=/var/lib/mysql/test/logtest.txt

To locate the progress indicator information in the log file, you can perform the following search:

cat ./logtest.txt | grep -i "okay"

The progress indicator information in the log file appears similar to the following:

page 1663 okay: 2.863% done
page 8447 okay: 14.537% done
page 13695 okay: 23.568% done
page 18815 okay: 32.379% done
page 23039 okay: 39.648% done
page 28351 okay: 48.789% done
page 33023 okay: 56.828% done
page 37951 okay: 65.308% done
page 44095 okay: 75.881% done
page 49407 okay: 85.022% done
page 54463 okay: 93.722% done
...

• --count, -c

Command-Line Format

Type

Default Value

--count

Base name

true

Print a count of the number of pages in the file and exit. Example usage:

innochecksum --count ../data/test/tab1.ibd

• --start-page=num, -s num

569

innochecksum — Offline InnoDB File Checksum Utility

Command-Line Format

--start-page=#

Type

Default Value

Numeric

0

Start at this page number. Example usage:

innochecksum --start-page=600 ../data/test/tab1.ibd

or:

innochecksum -s 600 ../data/test/tab1.ibd

• --end-page=num, -e num

Command-Line Format

Type

Default Value

Minimum Value

Maximum Value

--end-page=#

Numeric

0

0

18446744073709551615

End at this page number. Example usage:

innochecksum --end-page=700 ../data/test/tab1.ibd

or:

innochecksum --p 700 ../data/test/tab1.ibd

• --page=num, -p num

Command-Line Format

Type

Default Value

--page=#

Integer

0

Check only this page number. Example usage:

innochecksum --page=701 ../data/test/tab1.ibd

• --strict-check, -C

Command-Line Format

--strict-check=algorithm

Type

Default Value

Valid Values

570

Enumeration

crc32

innodb

crc32

innochecksum — Offline InnoDB File Checksum Utility

none

Specify a strict checksum algorithm. Options include innodb, crc32, and none.

In this example, the innodb checksum algorithm is specified:

innochecksum --strict-check=innodb ../data/test/tab1.ibd

In this example, the crc32 checksum algorithm is specified:

innochecksum -C crc32 ../data/test/tab1.ibd

The following conditions apply:

• If you do not specify the --strict-check option, innochecksum validates against innodb, crc32

and none.

• If you specify the none option, only checksums generated by none are allowed.

• If you specify the innodb option, only checksums generated by innodb are allowed.

• If you specify the crc32 option, only checksums generated by crc32 are allowed.

• --no-check, -n

Command-Line Format

Type

Default Value

--no-check

Boolean

false

Ignore the checksum verification when rewriting a checksum. This option may only be used with the
innochecksum --write option. If the --write option is not specified, innochecksum terminates.

In this example, an innodb checksum is rewritten to replace an invalid checksum:

innochecksum --no-check --write innodb ../data/test/tab1.ibd

• --allow-mismatches, -a

Command-Line Format

--allow-mismatches=#

Type

Default Value

Minimum Value

Maximum Value

Integer

0

0

18446744073709551615

The maximum number of checksum mismatches allowed before innochecksum terminates. The
default setting is 0. If --allow-mismatches=N, where N>=0, N mismatches are permitted and

571

innochecksum — Offline InnoDB File Checksum Utility

innochecksum terminates at N+1. When --allow-mismatches is set to 0, innochecksum
terminates on the first checksum mismatch.

In this example, an existing innodb checksum is rewritten to set --allow-mismatches to 1.

innochecksum --allow-mismatches=1 --write innodb ../data/test/tab1.ibd

With --allow-mismatches set to 1, if there is a mismatch at page 600 and another at page 700 on
a file with 1000 pages, the checksum is updated for pages 0-599 and 601-699. Because --allow-
mismatches is set to 1, the checksum tolerates the first mismatch and terminates on the second
mismatch, leaving page 600 and pages 700-999 unchanged.

• --write=name, -w num

Command-Line Format

Type

Default Value

Valid Values

--write=algorithm

Enumeration

crc32

innodb

crc32

none

Rewrite a checksum. When rewriting an invalid checksum, the --no-check option must be used
together with the --write option. The --no-check option tells innochecksum to ignore verification
of the invalid checksum. You do not have to specify the --no-check option if the current checksum is
valid.

An algorithm must be specified when using the --write option. Possible values for the --write option
are:

• innodb: A checksum calculated in software, using the original algorithm from InnoDB.

• crc32: A checksum calculated using the crc32 algorithm, possibly done with a hardware assist.

• none: A constant number.

The --write option rewrites entire pages to disk. If the new checksum is identical to the existing
checksum, the new checksum is not written to disk in order to minimize I/O.

innochecksum obtains an exclusive lock when the --write option is used.

In this example, a crc32 checksum is written for tab1.ibd:

innochecksum -w crc32 ../data/test/tab1.ibd

In this example, a crc32 checksum is rewritten to replace an invalid crc32 checksum:

innochecksum --no-check --write crc32 ../data/test/tab1.ibd

• --page-type-summary, -S

Command-Line Format

--page-type-summary

572

Type

Boolean

innochecksum — Offline InnoDB File Checksum Utility

Default Value

false

Display a count of each page type in a tablespace. Example usage:

innochecksum --page-type-summary ../data/test/tab1.ibd

Sample output for --page-type-summary:

File::../data/test/tab1.ibd
================PAGE TYPE SUMMARY==============
#PAGE_COUNT PAGE_TYPE
===============================================
       2        Index page
       0        Undo log page
       1        Inode page
       0        Insert buffer free list page
       2        Freshly allocated page
       1        Insert buffer bitmap
       0        System page
       0        Transaction system page
       1        File Space Header
       0        Extent descriptor page
       0        BLOB page
       0        Compressed BLOB page
       0        Other type of page
===============================================
Additional information:
Undo page type: 0 insert, 0 update, 0 other
Undo page state: 0 active, 0 cached, 0 to_free, 0 to_purge, 0 prepared, 0 other

• --page-type-dump, -D

Command-Line Format

--page-type-dump=name

Type

Default Value

String

[none]

Dump the page type information for each page in a tablespace to stderr or stdout. Example usage:

innochecksum --page-type-dump=/tmp/a.txt ../data/test/tab1.ibd

• --log, -l

Command-Line Format

Type

Default Value

--log=path

File name

[none]

Log output for the innochecksum tool. A log file name must be provided. Log output contains checksum
values for each tablespace page. For uncompressed tables, LSN values are also provided. The --log
replaces the --debug option, which was available in earlier releases. Example usage:

innochecksum --log=/tmp/log.txt ../data/test/tab1.ibd

or:

innochecksum -l /tmp/log.txt ../data/test/tab1.ibd

573

innochecksum — Offline InnoDB File Checksum Utility

• - option.

Specify the - option to read from standard input. If the - option is missing when “read from standard in”
is expected, innochecksum prints innochecksum usage information indicating that the “-” option was
omitted. Example usages:

cat t1.ibd | innochecksum -

In this example, innochecksum writes the crc32 checksum algorithm to a.ibd without changing the
original t1.ibd file.

cat t1.ibd | innochecksum --write=crc32 - > a.ibd

Running innochecksum on Multiple User-defined Tablespace Files

The following examples demonstrate how to run innochecksum on multiple user-defined tablespace files
(.ibd files).

Run innochecksum for all tablespace (.ibd) files in the “test” database:

innochecksum ./data/test/*.ibd

Run innochecksum for all tablespace files (.ibd files) that have a file name starting with “t”:

innochecksum ./data/test/t*.ibd

Run innochecksum for all tablespace files (.ibd files) in the data directory:

innochecksum ./data/*/*.ibd

Note

Running innochecksum on multiple user-defined tablespace files is not supported
on Windows operating systems, as Windows shells such as cmd.exe do not
support glob pattern expansion. On Windows systems, innochecksum must be
run separately for each user-defined tablespace file. For example:

innochecksum.exe t1.ibd
innochecksum.exe t2.ibd
innochecksum.exe t3.ibd

Running innochecksum on Multiple System Tablespace Files

By default, there is only one InnoDB system tablespace file (ibdata1) but multiple files for the system
tablespace can be defined using the innodb_data_file_path option. In the following example, three
files for the system tablespace are defined using the innodb_data_file_path option: ibdata1,
ibdata2, and ibdata3.

./bin/mysqld --no-defaults --innodb-data-file-path="ibdata1:10M;ibdata2:10M;ibdata3:10M:autoextend"

The three files (ibdata1, ibdata2, and ibdata3) form one logical system tablespace. To run
innochecksum on multiple files that form one logical system tablespace, innochecksum requires the -
option to read tablespace files in from standard input, which is equivalent to concatenating multiple files to
create one single file. For the example provided above, the following innochecksum command would be
used:

cat ibdata* | innochecksum -

574

myisam_ftdump — Display Full-Text Index information

Refer to the innochecksum options information for more information about the “-” option.

Note

Running innochecksum on multiple files in the same tablespace is not supported
on Windows operating systems, as Windows shells such as cmd.exe do not
support glob pattern expansion. On Windows systems, innochecksum must be
run separately for each system tablespace file. For example:

innochecksum.exe ibdata1
innochecksum.exe ibdata2
innochecksum.exe ibdata3

4.6.2 myisam_ftdump — Display Full-Text Index information

myisam_ftdump displays information about FULLTEXT indexes in MyISAM tables. It reads the
MyISAM index file directly, so it must be run on the server host where the table is located. Before using
myisam_ftdump, be sure to issue a FLUSH TABLES statement first if the server is running.

myisam_ftdump scans and dumps the entire index, which is not particularly fast. On the other hand, the
distribution of words changes infrequently, so it need not be run often.

Invoke myisam_ftdump like this:

myisam_ftdump [options] tbl_name index_num

The tbl_name argument should be the name of a MyISAM table. You can also specify a table by naming
its index file (the file with the .MYI suffix). If you do not invoke myisam_ftdump in the directory where
the table files are located, the table or index file name must be preceded by the path name to the table's
database directory. Index numbers begin with 0.

Example: Suppose that the test database contains a table named mytexttable that has the following
definition:

CREATE TABLE mytexttable
(
  id   INT NOT NULL,
  txt  TEXT NOT NULL,
  PRIMARY KEY (id),
  FULLTEXT (txt)
) ENGINE=MyISAM;

The index on id is index 0 and the FULLTEXT index on txt is index 1. If your working directory is the
test database directory, invoke myisam_ftdump as follows:

myisam_ftdump mytexttable 1

If the path name to the test database directory is /usr/local/mysql/data/test, you can
also specify the table name argument using that path name. This is useful if you do not invoke
myisam_ftdump in the database directory:

myisam_ftdump /usr/local/mysql/data/test/mytexttable 1

You can use myisam_ftdump to generate a list of index entries in order of frequency of occurrence like
this on Unix-like systems:

myisam_ftdump -c mytexttable 1 | sort -r

575

myisamchk — MyISAM Table-Maintenance Utility

On Windows, use:

myisam_ftdump -c mytexttable 1 | sort /R

myisam_ftdump supports the following options:

• --help, -h -?

Command-Line Format

--help

Display a help message and exit.

• --count, -c

Command-Line Format

--count

Calculate per-word statistics (counts and global weights).

• --dump, -d

Command-Line Format

--dump

Dump the index, including data offsets and word weights.

• --length, -l

Command-Line Format

--length

Report the length distribution.

• --stats, -s

Command-Line Format

--stats

Report global index statistics. This is the default operation if no other operation is specified.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more output about what the program does.

4.6.3 myisamchk — MyISAM Table-Maintenance Utility

The myisamchk utility gets information about your database tables or checks, repairs, or optimizes
them. myisamchk works with MyISAM tables (tables that have .MYD and .MYI files for storing data and
indexes).

576

You can also use the CHECK TABLE and REPAIR TABLE statements to check and repair MyISAM tables.
See Section 13.7.2.2, “CHECK TABLE Statement”, and Section 13.7.2.5, “REPAIR TABLE Statement”.

myisamchk — MyISAM Table-Maintenance Utility

The use of myisamchk with partitioned tables is not supported.

Caution

It is best to make a backup of a table before performing a table repair operation;
under some circumstances the operation might cause data loss. Possible causes
include but are not limited to file system errors.

Invoke myisamchk like this:

myisamchk [options] tbl_name ...

The options specify what you want myisamchk to do. They are described in the following sections. You
can also get a list of options by invoking myisamchk --help.

With no options, myisamchk simply checks your table as the default operation. To get more information or
to tell myisamchk to take corrective action, specify options as described in the following discussion.

tbl_name is the database table you want to check or repair. If you run myisamchk somewhere other than
in the database directory, you must specify the path to the database directory, because myisamchk has
no idea where the database is located. In fact, myisamchk does not actually care whether the files you are
working on are located in a database directory. You can copy the files that correspond to a database table
into some other location and perform recovery operations on them there.

You can name several tables on the myisamchk command line if you wish. You can also specify a table
by naming its index file (the file with the .MYI suffix). This enables you to specify all tables in a directory
by using the pattern *.MYI. For example, if you are in a database directory, you can check all the MyISAM
tables in that directory like this:

myisamchk *.MYI

If you are not in the database directory, you can check all the tables there by specifying the path to the
directory:

myisamchk /path/to/database_dir/*.MYI

You can even check all tables in all databases by specifying a wildcard with the path to the MySQL data
directory:

myisamchk /path/to/datadir/*/*.MYI

The recommended way to quickly check all MyISAM tables is:

myisamchk --silent --fast /path/to/datadir/*/*.MYI

If you want to check all MyISAM tables and repair any that are corrupted, you can use the following
command:

myisamchk --silent --force --fast --update-state \
          --key_buffer_size=64M --myisam_sort_buffer_size=64M \
          --read_buffer_size=1M --write_buffer_size=1M \
          /path/to/datadir/*/*.MYI

This command assumes that you have more than 64MB free. For more information about memory
allocation with myisamchk, see Section 4.6.3.6, “myisamchk Memory Usage”.

For additional information about using myisamchk, see Section 7.6, “MyISAM Table Maintenance and
Crash Recovery”.

577

myisamchk — MyISAM Table-Maintenance Utility

Important

You must ensure that no other program is using the tables while you are running
myisamchk. The most effective means of doing so is to shut down the MySQL
server while running myisamchk, or to lock all tables that myisamchk is being
used on.

Otherwise, when you run myisamchk, it may display the following error message:

warning: clients are using or haven't closed the table properly

This means that you are trying to check a table that has been updated by another
program (such as the mysqld server) that hasn't yet closed the file or that has died
without closing the file properly, which can sometimes lead to the corruption of one
or more MyISAM tables.

If mysqld is running, you must force it to flush any table modifications that are still
buffered in memory by using FLUSH TABLES. You should then ensure that no one
is using the tables while you are running myisamchk

However, the easiest way to avoid this problem is to use CHECK TABLE instead of
myisamchk to check tables. See Section 13.7.2.2, “CHECK TABLE Statement”.

myisamchk supports the following options, which can be specified on the command line or in the
[myisamchk] group of an option file. For information about option files used by MySQL programs, see
Section 4.2.2.2, “Using Option Files”.

Table 4.21 myisamchk Options

Option Name

--analyze

--backup

--block-search

--character-sets-dir

--check

--check-only-changed

--correct-checksum

--data-file-length

--debug

--decode_bits

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--description

578

Description

Analyze the distribution of key values

Make a backup of the .MYD file as file_name-
time.BAK

Find the record that a block at the given offset
belongs to

Directory where character sets can be found

Check the table for errors

Check only tables that have changed since the last
check

Correct the checksum information for the table

Maximum length of the data file (when re-creating
data file when it is full)

Write debugging log

Decode_bits

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Print some descriptive information about the table

myisamchk — MyISAM Table-Maintenance Utility

Option Name

--extend-check

--fast

--force

--force

--ft_max_word_len

--ft_min_word_len

--ft_stopword_file

--HELP

--help

--information

--key_buffer_size

--keys-used

--max-record-length

--medium-check

--myisam_block_size

--myisam_sort_buffer_size

--no-defaults

--parallel-recover

--print-defaults

--quick

--read_buffer_size

--read-only

--recover

--safe-recover

--set-auto-increment

--set-collation

--silent

Description

Do very thorough table check or repair that tries to
recover every possible row from the data file

Check only tables that haven't been closed properly

Do a repair operation automatically if myisamchk
finds any errors in the table

Overwrite old temporary files. For use with the -r or -
o option

Maximum word length for FULLTEXT indexes

Minimum word length for FULLTEXT indexes

Use stopwords from this file instead of built-in list

Display help message and exit

Display help message and exit

Print informational statistics about the table that is
checked

Size of buffer used for index blocks for MyISAM
tables

A bit-value that indicates which indexes to update

Skip rows larger than the given length if myisamchk
cannot allocate memory to hold them

Do a check that is faster than an --extend-check
operation

Block size to be used for MyISAM index pages

The buffer that is allocated when sorting the index
when doing a REPAIR or when creating indexes
with CREATE INDEX or ALTER TABLE

Read no option files

Uses the same technique as -r and -n, but creates
all the keys in parallel, using different threads (beta)

Print default options

Achieve a faster repair by not modifying the data file

Each thread that does a sequential scan allocates a
buffer of this size for each table it scans

Do not mark the table as checked

Do a repair that can fix almost any problem except
unique keys that aren't unique

Do a repair using an old recovery method that reads
through all rows in order and updates all index trees
based on the rows found

Force AUTO_INCREMENT numbering for new
records to start at the given value

Specify the collation to use for sorting table indexes

Silent mode

579

myisamchk — MyISAM Table-Maintenance Utility

Option Name

--sort_buffer_size

--sort-index

--sort_key_blocks

--sort-records

--sort-recover

--stats_method

--tmpdir

--unpack

--update-state

--verbose

--version

--wait

Description

The buffer that is allocated when sorting the index
when doing a REPAIR or when creating indexes
with CREATE INDEX or ALTER TABLE

Sort the index tree blocks in high-low order

sort_key_blocks

Sort records according to a particular index

Force myisamchk to use sorting to resolve the keys
even if the temporary files would be very large

Specifies how MyISAM index statistics collection
code should treat NULLs

Directory to be used for storing temporary files

Unpack a table that was packed with myisampack

Store information in the .MYI file to indicate when
the table was checked and whether the table
crashed

Verbose mode

Display version information and exit

Wait for locked table to be unlocked, instead of
terminating

--write_buffer_size

Write buffer size

4.6.3.1 myisamchk General Options

The options described in this section can be used for any type of table maintenance operation performed
by myisamchk. The sections following this one describe options that pertain only to specific operations,
such as table checking or repairing.

• --help, -?

Command-Line Format

--help

Display a help message and exit. Options are grouped by type of operation.

• --HELP, -H

Command-Line Format

--HELP

Display a help message and exit. Options are presented in a single list.

• --debug=debug_options, -# debug_options

Command-Line Format

--debug[=debug_options]

Type

580

Default Value

String

d:t:o,/tmp/myisamchk.trace

myisamchk — MyISAM Table-Maintenance Utility

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/myisamchk.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, myisamchk normally reads the [myisamchk] group. If this option is given as --defaults-
group-suffix=_other, myisamchk also reads the [myisamchk_other] group.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

581

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create

myisamchk — MyISAM Table-Maintenance Utility

.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --silent, -s

Command-Line Format

--silent

Silent mode. Write output only when errors occur. You can use -s twice (-ss) to make myisamchk very
silent.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This can be used with -d and -e.
Use -v multiple times (-vv, -vvv) for even more output.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --wait, -w

Command-Line Format

Type

Default Value

--wait

Boolean

false

Instead of terminating with an error if the table is locked, wait until the table is unlocked before
continuing. If you are running mysqld with external locking disabled, the table can be locked only by
another myisamchk command.

You can also set the following variables by using --var_name=value syntax:

Variable

decode_bits

ft_max_word_len

Default Value

9

version-dependent

582

myisamchk — MyISAM Table-Maintenance Utility

Variable

ft_min_word_len

ft_stopword_file

key_buffer_size

myisam_block_size

myisam_sort_key_blocks

read_buffer_size

sort_buffer_size

sort_key_blocks

stats_method

write_buffer_size

Default Value

4

built-in list

523264

1024

16

262136

2097144

16

nulls_unequal

262136

The possible myisamchk variables and their default values can be examined with myisamchk --help:

myisam_sort_buffer_size is used when the keys are repaired by sorting keys, which is
the normal case when you use --recover. sort_buffer_size is a deprecated synonym for
myisam_sort_buffer_size.

key_buffer_size is used when you are checking the table with --extend-check or when the keys are
repaired by inserting keys row by row into the table (like when doing normal inserts). Repairing through the
key buffer is used in the following cases:

• You use --safe-recover.

• The temporary files needed to sort the keys would be more than twice as big as when creating the

key file directly. This is often the case when you have large key values for CHAR, VARCHAR, or TEXT
columns, because the sort operation needs to store the complete key values as it proceeds. If you have
lots of temporary space and you can force myisamchk to repair by sorting, you can use the --sort-
recover option.

Repairing through the key buffer takes much less disk space than using sorting, but is also much slower.

If you want a faster repair, set the key_buffer_size and myisam_sort_buffer_size variables to
about 25% of your available memory. You can set both variables to large values, because only one of them
is used at a time.

myisam_block_size is the size used for index blocks.

stats_method influences how NULL values are treated for index statistics collection when the --
analyze option is given. It acts like the myisam_stats_method system variable. For more information,
see the description of myisam_stats_method in Section 5.1.7, “Server System Variables”, and
Section 8.3.7, “InnoDB and MyISAM Index Statistics Collection”.

ft_min_word_len and ft_max_word_len indicate the minimum and maximum word length for
FULLTEXT indexes on MyISAM tables. ft_stopword_file names the stopword file. These need to be
set under the following circumstances.

If you use myisamchk to perform an operation that modifies table indexes (such as repair or analyze), the
FULLTEXT indexes are rebuilt using the default full-text parameter values for minimum and maximum word
length and the stopword file unless you specify otherwise. This can result in queries failing.

The problem occurs because these parameters are known only by the server. They are not stored in
MyISAM index files. To avoid the problem if you have modified the minimum or maximum word length

583

myisamchk — MyISAM Table-Maintenance Utility

or the stopword file in the server, specify the same ft_min_word_len, ft_max_word_len, and
ft_stopword_file values to myisamchk that you use for mysqld. For example, if you have set the
minimum word length to 3, you can repair a table with myisamchk like this:

myisamchk --recover --ft_min_word_len=3 tbl_name.MYI

To ensure that myisamchk and the server use the same values for full-text parameters, you can place
each one in both the [mysqld] and [myisamchk] sections of an option file:

[mysqld]
ft_min_word_len=3

[myisamchk]
ft_min_word_len=3

An alternative to using myisamchk is to use the REPAIR TABLE, ANALYZE TABLE, OPTIMIZE TABLE,
or ALTER TABLE. These statements are performed by the server, which knows the proper full-text
parameter values to use.

4.6.3.2 myisamchk Check Options

myisamchk supports the following options for table checking operations:

• --check, -c

Command-Line Format

--check

Check the table for errors. This is the default operation if you specify no option that selects an operation
type explicitly.

• --check-only-changed, -C

Command-Line Format

--check-only-changed

Check only tables that have changed since the last check.

• --extend-check, -e

Command-Line Format

--extend-check

Check the table very thoroughly. This is quite slow if the table has many indexes. This option should only
be used in extreme cases. Normally, myisamchk or myisamchk --medium-check should be able to
determine whether there are any errors in the table.

If you are using --extend-check and have plenty of memory, setting the key_buffer_size variable
to a large value helps the repair operation run faster.

See also the description of this option under table repair options.

For a description of the output format, see Section 4.6.3.5, “Obtaining Table Information with
myisamchk”.

• --fast, -F

Command-Line Format

--fast

584

myisamchk — MyISAM Table-Maintenance Utility

Check only tables that haven't been closed properly.

• --force, -f

Command-Line Format

--force

Do a repair operation automatically if myisamchk finds any errors in the table. The repair type is the
same as that specified with the --recover or -r option.

• --information, -i

Command-Line Format

--information

Print informational statistics about the table that is checked.

• --medium-check, -m

Command-Line Format

--medium-check

Do a check that is faster than an --extend-check operation. This finds only 99.99% of all errors,
which should be good enough in most cases.

• --read-only, -T

Command-Line Format

--read-only

Do not mark the table as checked. This is useful if you use myisamchk to check a table that is in use
by some other application that does not use locking, such as mysqld when run with external locking
disabled.

• --update-state, -U

Command-Line Format

--update-state

Store information in the .MYI file to indicate when the table was checked and whether the table crashed.
This should be used to get full benefit of the --check-only-changed option, but you shouldn't use
this option if the mysqld server is using the table and you are running it with external locking disabled.

4.6.3.3 myisamchk Repair Options

myisamchk supports the following options for table repair operations (operations performed when an
option such as --recover or --safe-recover is given):

• --backup, -B

Command-Line Format

--backup

Make a backup of the .MYD file as file_name-time.BAK

• --character-sets-dir=dir_name

585

myisamchk — MyISAM Table-Maintenance Utility

Command-Line Format

--character-sets-dir=path

Type

Default Value

String

[none]

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --correct-checksum

Command-Line Format

--correct-checksum

Correct the checksum information for the table.

• --data-file-length=len, -D len

Command-Line Format

--data-file-length=len

Type

Numeric

The maximum length of the data file (when re-creating data file when it is “full”).

• --extend-check, -e

Command-Line Format

--extend-check

Do a repair that tries to recover every possible row from the data file. Normally, this also finds a lot of
garbage rows. Do not use this option unless you are desperate.

See also the description of this option under table checking options.

For a description of the output format, see Section 4.6.3.5, “Obtaining Table Information with
myisamchk”.

• --force, -f

Command-Line Format

--force

Overwrite old intermediate files (files with names like tbl_name.TMD) instead of aborting.

• --keys-used=val, -k val

Command-Line Format

Type

--keys-used=val

Numeric

For myisamchk, the option value is a bit value that indicates which indexes to update. Each binary bit of
the option value corresponds to a table index, where the first index is bit 0. An option value of 0 disables
updates to all indexes, which can be used to get faster inserts. Deactivated indexes can be reactivated
by using myisamchk -r.

• --max-record-length=len

586

myisamchk — MyISAM Table-Maintenance Utility

Command-Line Format

--max-record-length=len

Type

Numeric

Skip rows larger than the given length if myisamchk cannot allocate memory to hold them.

• --parallel-recover, -p

Command-Line Format

--parallel-recover

Note

This option is deprecated in MySQL 5.7.38 and removed in MySQL 5.7.39.

Use the same technique as -r and -n, but create all the keys in parallel, using different threads. This is
beta-quality code. Use at your own risk!

• --quick, -q

Command-Line Format

--quick

Achieve a faster repair by modifying only the index file, not the data file. You can specify this option twice
to force myisamchk to modify the original data file in case of duplicate keys.

• --recover, -r

Command-Line Format

--recover

Do a repair that can fix almost any problem except unique keys that are not unique (which is an
extremely unlikely error with MyISAM tables). If you want to recover a table, this is the option to try first.
You should try --safe-recover only if myisamchk reports that the table cannot be recovered using
--recover. (In the unlikely case that --recover fails, the data file remains intact.)

If you have lots of memory, you should increase the value of myisam_sort_buffer_size.

• --safe-recover, -o

Command-Line Format

--safe-recover

Do a repair using an old recovery method that reads through all rows in order and updates all index
trees based on the rows found. This is an order of magnitude slower than --recover, but can handle
a couple of very unlikely cases that --recover cannot. This recovery method also uses much less disk
space than --recover. Normally, you should repair first using --recover, and then with --safe-
recover only if --recover fails.

If you have lots of memory, you should increase the value of key_buffer_size.

• --set-collation=name

Command-Line Format

--set-collation=name

587

myisamchk — MyISAM Table-Maintenance Utility

Type

String

Specify the collation to use for sorting table indexes. The character set name is implied by the first part of
the collation name.

• --sort-recover, -n

Command-Line Format

--sort-recover

Force myisamchk to use sorting to resolve the keys even if the temporary files would be very large.

• --tmpdir=dir_name, -t dir_name

Command-Line Format

Type

--tmpdir=dir_name

Directory name

The path of the directory to be used for storing temporary files. If this is not set, myisamchk uses the
value of the TMPDIR environment variable. --tmpdir can be set to a list of directory paths that are
used successively in round-robin fashion for creating temporary files. The separator character between
directory names is the colon (:) on Unix and the semicolon (;) on Windows.

• --unpack, -u

Command-Line Format

--unpack

Unpack a table that was packed with myisampack.

4.6.3.4 Other myisamchk Options

myisamchk supports the following options for actions other than table checks and repairs:

• --analyze, -a

Command-Line Format

--analyze

Analyze the distribution of key values. This improves join performance by enabling the join optimizer to
better choose the order in which to join the tables and which indexes it should use. To obtain information
about the key distribution, use a myisamchk --description --verbose tbl_name command or
the SHOW INDEX FROM tbl_name statement.

• --block-search=offset, -b offset

Command-Line Format

--block-search=offset

Type

Numeric

Find the record that a block at the given offset belongs to.

• --description, -d

Command-Line Format

--description

588

myisamchk — MyISAM Table-Maintenance Utility

Print some descriptive information about the table. Specifying the --verbose option once or twice
produces additional information. See Section 4.6.3.5, “Obtaining Table Information with myisamchk”.

• --set-auto-increment[=value], -A[value]

Force AUTO_INCREMENT numbering for new records to start at the given value (or higher, if there are
existing records with AUTO_INCREMENT values this large). If value is not specified, AUTO_INCREMENT
numbers for new records begin with the largest value currently in the table, plus one.

• --sort-index, -S

Command-Line Format

--sort-index

Sort the index tree blocks in high-low order. This optimizes seeks and makes table scans that use
indexes faster.

• --sort-records=N, -R N

Command-Line Format

Type

--sort-records=#

Numeric

Sort records according to a particular index. This makes your data much more localized and may speed
up range-based SELECT and ORDER BY operations that use this index. (The first time you use this
option to sort a table, it may be very slow.) To determine a table's index numbers, use SHOW INDEX,
which displays a table's indexes in the same order that myisamchk sees them. Indexes are numbered
beginning with 1.

If keys are not packed (PACK_KEYS=0), they have the same length, so when myisamchk sorts and
moves records, it just overwrites record offsets in the index. If keys are packed (PACK_KEYS=1),
myisamchk must unpack key blocks first, then re-create indexes and pack the key blocks again. (In this
case, re-creating indexes is faster than updating offsets for each index.)

4.6.3.5 Obtaining Table Information with myisamchk

To obtain a description of a MyISAM table or statistics about it, use the commands shown here. The output
from these commands is explained later in this section.

• myisamchk -d tbl_name

Runs myisamchk in “describe mode” to produce a description of your table. If you start the MySQL
server with external locking disabled, myisamchk may report an error for a table that is updated while
it runs. However, because myisamchk does not change the table in describe mode, there is no risk of
destroying data.

• myisamchk -dv tbl_name

Adding -v runs myisamchk in verbose mode so that it produces more information about the table.
Adding -v a second time produces even more information.

• myisamchk -eis tbl_name

Shows only the most important information from a table. This operation is slow because it must read the
entire table.

589

myisamchk — MyISAM Table-Maintenance Utility

• myisamchk -eiv tbl_name

This is like -eis, but tells you what is being done.

The tbl_name argument can be either the name of a MyISAM table or the name of its index file, as
described in Section 4.6.3, “myisamchk — MyISAM Table-Maintenance Utility”. Multiple tbl_name
arguments can be given.

Suppose that a table named person has the following structure. (The MAX_ROWS table option is included
so that in the example output from myisamchk shown later, some values are smaller and fit the output
format more easily.)

CREATE TABLE person
(
  id         INT NOT NULL AUTO_INCREMENT,
  last_name  VARCHAR(20) NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  birth      DATE,
  death      DATE,
  PRIMARY KEY (id),
  INDEX (last_name, first_name),
  INDEX (birth)
) MAX_ROWS = 1000000 ENGINE=MYISAM;

Suppose also that the table has these data and index file sizes:

-rw-rw----  1 mysql  mysql  9347072 Aug 19 11:47 person.MYD
-rw-rw----  1 mysql  mysql  6066176 Aug 19 11:47 person.MYI

Example of myisamchk -dvv output:

MyISAM file:         person
Record format:       Packed
Character set:       latin1_swedish_ci (8)
File-version:        1
Creation time:       2009-08-19 16:47:41
Recover time:        2009-08-19 16:47:56
Status:              checked,analyzed,optimized keys
Auto increment key:              1  Last value:                306688
Data records:               306688  Deleted blocks:                 0
Datafile parts:             306688  Deleted data:                   0
Datafile pointer (bytes):        4  Keyfile pointer (bytes):        3
Datafile length:           9347072  Keyfile length:           6066176
Max datafile length:    4294967294  Max keyfile length:   17179868159
Recordlength:                   54

table description:
Key Start Len Index   Type                 Rec/key         Root  Blocksize
1   2     4   unique  long                       1        99328       1024
2   6     20  multip. varchar prefix           512      3563520       1024
    27    20          varchar                  512
3   48    3   multip. uint24 NULL           306688      6065152       1024

Field Start Length Nullpos Nullbit Type
1     1     1
2     2     4                      no zeros
3     6     21                     varchar
4     27    21                     varchar
5     48    3      1       1       no zeros
6     51    3      1       2       no zeros

Explanations for the types of information myisamchk produces are given here. “Keyfile” refers to the index
file. “Record” and “row” are synonymous, as are “field” and “column.”

The initial part of the table description contains these values:

590

myisamchk — MyISAM Table-Maintenance Utility

• MyISAM file

Name of the MyISAM (index) file.

• Record format

The format used to store table rows. The preceding examples use Fixed length. Other possible
values are Compressed and Packed. (Packed corresponds to what SHOW TABLE STATUS reports as
Dynamic.)

• Chararacter set

The table default character set.

• File-version

Version of MyISAM format. Always 1.

• Creation time

When the data file was created.

• Recover time

When the index/data file was last reconstructed.

• Status

Table status flags. Possible values are crashed, open, changed, analyzed, optimized keys, and
sorted index pages.

• Auto increment key, Last value

The key number associated the table's AUTO_INCREMENT column, and the most recently generated
value for this column. These fields do not appear if there is no such column.

• Data records

The number of rows in the table.

• Deleted blocks

How many deleted blocks still have reserved space. You can optimize your table to minimize this space.
See Section 7.6.4, “MyISAM Table Optimization”.

• Datafile parts

For dynamic-row format, this indicates how many data blocks there are. For an optimized table without
fragmented rows, this is the same as Data records.

• Deleted data

How many bytes of unreclaimed deleted data there are. You can optimize your table to minimize this
space. See Section 7.6.4, “MyISAM Table Optimization”.

• Datafile pointer

The size of the data file pointer, in bytes. It is usually 2, 3, 4, or 5 bytes. Most tables manage with 2
bytes, but this cannot be controlled from MySQL yet. For fixed tables, this is a row address. For dynamic
tables, this is a byte address.

591

myisamchk — MyISAM Table-Maintenance Utility

• Keyfile pointer

The size of the index file pointer, in bytes. It is usually 1, 2, or 3 bytes. Most tables manage with 2 bytes,
but this is calculated automatically by MySQL. It is always a block address.

• Max datafile length

How long the table data file can become, in bytes.

• Max keyfile length

How long the table index file can become, in bytes.

• Recordlength

How much space each row takes, in bytes.

The table description part of the output includes a list of all keys in the table. For each key,
myisamchk displays some low-level information:

• Key

This key's number. This value is shown only for the first column of the key. If this value is missing, the
line corresponds to the second or later column of a multiple-column key. For the table shown in the
example, there are two table description lines for the second index. This indicates that it is a
multiple-part index with two parts.

• Start

Where in the row this portion of the index starts.

• Len

How long this portion of the index is. For packed numbers, this should always be the full length of the
column. For strings, it may be shorter than the full length of the indexed column, because you can index
a prefix of a string column. The total length of a multiple-part key is the sum of the Len values for all key
parts.

• Index

Whether a key value can exist multiple times in the index. Possible values are unique or multip.
(multiple).

• Type

What data type this portion of the index has. This is a MyISAM data type with the possible values
packed, stripped, or empty.

• Root

Address of the root index block.

• Blocksize

The size of each index block. By default this is 1024, but the value may be changed at compile time
when MySQL is built from source.

• Rec/key

592

myisamchk — MyISAM Table-Maintenance Utility

This is a statistical value used by the optimizer. It tells how many rows there are per value for this index.
A unique index always has a value of 1. This may be updated after a table is loaded (or greatly changed)
with myisamchk -a. If this is not updated at all, a default value of 30 is given.

The last part of the output provides information about each column:

• Field

The column number.

• Start

The byte position of the column within table rows.

• Length

The length of the column in bytes.

• Nullpos, Nullbit

For columns that can be NULL, MyISAM stores NULL values as a flag in a byte. Depending on how
many nullable columns there are, there can be one or more bytes used for this purpose. The Nullpos
and Nullbit values, if nonempty, indicate which byte and bit contains that flag indicating whether the
column is NULL.

The position and number of bytes used to store NULL flags is shown in the line for field 1. This is why
there are six Field lines for the person table even though it has only five columns.

• Type

The data type. The value may contain any of the following descriptors:

• constant

All rows have the same value.

• no endspace

Do not store endspace.

• no endspace, not_always

Do not store endspace and do not do endspace compression for all values.

• no endspace, no empty

Do not store endspace. Do not store empty values.

• table-lookup

The column was converted to an ENUM.

• zerofill(N)

The most significant N bytes in the value are always 0 and are not stored.

• no zeros

593

myisamchk — MyISAM Table-Maintenance Utility

Do not store zeros.

• always zero

Zero values are stored using one bit.

• Huff tree

The number of the Huffman tree associated with the column.

• Bits

The number of bits used in the Huffman tree.

The Huff tree and Bits fields are displayed if the table has been compressed with myisampack. See
Section 4.6.5, “myisampack — Generate Compressed, Read-Only MyISAM Tables”, for an example of this
information.

Example of myisamchk -eiv output:

Checking MyISAM file: person
Data records:  306688   Deleted blocks:       0
- check file-size
- check record delete-chain
No recordlinks
- check key delete-chain
block_size 1024:
- check index reference
- check data record references index: 1
Key:  1:  Keyblocks used:  98%  Packed:    0%  Max levels:  3
- check data record references index: 2
Key:  2:  Keyblocks used:  99%  Packed:   97%  Max levels:  3
- check data record references index: 3
Key:  3:  Keyblocks used:  98%  Packed:  -14%  Max levels:  3
Total:    Keyblocks used:  98%  Packed:   89%

- check records and index references
*** LOTS OF ROW NUMBERS DELETED ***

Records:            306688  M.recordlength:       25  Packed:            83%
Recordspace used:       97% Empty space:           2% Blocks/Record:   1.00
Record blocks:      306688  Delete blocks:         0
Record data:       7934464  Deleted data:          0
Lost space:         256512  Linkdata:        1156096

User time 43.08, System time 1.68
Maximum resident set size 0, Integral resident set size 0
Non-physical pagefaults 0, Physical pagefaults 0, Swaps 0
Blocks in 0 out 7, Messages in 0 out 0, Signals 0
Voluntary context switches 0, Involuntary context switches 0
Maximum memory usage: 1046926 bytes (1023k)

myisamchk -eiv output includes the following information:

• Data records

The number of rows in the table.

• Deleted blocks

How many deleted blocks still have reserved space. You can optimize your table to minimize this space.
See Section 7.6.4, “MyISAM Table Optimization”.

594

myisamchk — MyISAM Table-Maintenance Utility

• Key

The key number.

• Keyblocks used

What percentage of the keyblocks are used. When a table has just been reorganized with myisamchk,
the values are very high (very near theoretical maximum).

• Packed

MySQL tries to pack key values that have a common suffix. This can only be used for indexes on CHAR
and VARCHAR columns. For long indexed strings that have similar leftmost parts, this can significantly
reduce the space used. In the preceding example, the second key is 40 bytes long and a 97% reduction
in space is achieved.

• Max levels

How deep the B-tree for this key is. Large tables with long key values get high values.

• Records

How many rows are in the table.

• M.recordlength

The average row length. This is the exact row length for tables with fixed-length rows, because all rows
have the same length.

• Packed

MySQL strips spaces from the end of strings. The Packed value indicates the percentage of savings
achieved by doing this.

• Recordspace used

What percentage of the data file is used.

• Empty space

What percentage of the data file is unused.

• Blocks/Record

Average number of blocks per row (that is, how many links a fragmented row is composed of). This is
always 1.0 for fixed-format tables. This value should stay as close to 1.0 as possible. If it gets too large,
you can reorganize the table. See Section 7.6.4, “MyISAM Table Optimization”.

• Recordblocks

How many blocks (links) are used. For fixed-format tables, this is the same as the number of rows.

• Deleteblocks

How many blocks (links) are deleted.

• Recorddata

How many bytes in the data file are used.

595

myisamlog — Display MyISAM Log File Contents

• Deleted data

How many bytes in the data file are deleted (unused).

• Lost space

If a row is updated to a shorter length, some space is lost. This is the sum of all such losses, in bytes.

• Linkdata

When the dynamic table format is used, row fragments are linked with pointers (4 to 7 bytes each).
Linkdata is the sum of the amount of storage used by all such pointers.

4.6.3.6 myisamchk Memory Usage

Memory allocation is important when you run myisamchk. myisamchk uses no more memory than its
memory-related variables are set to. If you are going to use myisamchk on very large tables, you should
first decide how much memory you want it to use. The default is to use only about 3MB to perform repairs.
By using larger values, you can get myisamchk to operate faster. For example, if you have more than
512MB RAM available, you could use options such as these (in addition to any other options you might
specify):

myisamchk --myisam_sort_buffer_size=256M \
           --key_buffer_size=512M \
           --read_buffer_size=64M \
           --write_buffer_size=64M ...

Using --myisam_sort_buffer_size=16M is probably enough for most cases.

Be aware that myisamchk uses temporary files in TMPDIR. If TMPDIR points to a memory file system, out
of memory errors can easily occur. If this happens, run myisamchk with the --tmpdir=dir_name option
to specify a directory located on a file system that has more space.

When performing repair operations, myisamchk also needs a lot of disk space:

• Twice the size of the data file (the original file and a copy). This space is not needed if you do a repair
with --quick; in this case, only the index file is re-created. This space must be available on the same
file system as the original data file, as the copy is created in the same directory as the original.

• Space for the new index file that replaces the old one. The old index file is truncated at the start of the

repair operation, so you usually ignore this space. This space must be available on the same file system
as the original data file.

• When using --recover or --sort-recover (but not when using --safe-recover), you need

space on disk for sorting. This space is allocated in the temporary directory (specified by TMPDIR or --
tmpdir=dir_name). The following formula yields the amount of space required:

(largest_key + row_pointer_length) * number_of_rows * 2

You can check the length of the keys and the row_pointer_length with myisamchk -
dv tbl_name (see Section 4.6.3.5, “Obtaining Table Information with myisamchk”). The
row_pointer_length and number_of_rows values are the Datafile pointer and Data
records values in the table description. To determine the largest_key value, check the Key lines in
the table description. The Len column indicates the number of bytes for each key part. For a multiple-
column index, the key size is the sum of the Len values for all key parts.

If you have a problem with disk space during repair, you can try --safe-recover instead of --recover.

4.6.4 myisamlog — Display MyISAM Log File Contents

596

myisamlog — Display MyISAM Log File Contents

myisamlog processes the contents of a MyISAM log file. To create such a file, start the server with a --
log-isam=log_file option.

Invoke myisamlog like this:

myisamlog [options] [file_name [tbl_name] ...]

The default operation is update (-u). If a recovery is done (-r), all writes and possibly updates and deletes
are done and errors are only counted. The default log file name is myisam.log if no log_file argument
is given. If tables are named on the command line, only those tables are updated.

myisamlog supports the following options:

• -?, -I

Display a help message and exit.

• -c N

Execute only N commands.

• -f N

Specify the maximum number of open files.

• -F filepath/

Specify the file path with a trailing slash.

• -i

Display extra information before exiting.

• -o offset

Specify the starting offset.

• -p N

Remove N components from path.

• -r

Perform a recovery operation.

• -R record_pos_file record_pos

Specify record position file and record position.

• -u

Perform an update operation.

• -v

Verbose mode. Print more output about what the program does. This option can be given multiple times
to produce more and more output.

• -w write_file

Specify the write file.

597

myisampack — Generate Compressed, Read-Only MyISAM Tables

• -V

Display version information.

4.6.5 myisampack — Generate Compressed, Read-Only MyISAM Tables

The myisampack utility compresses MyISAM tables. myisampack works by compressing each column in
the table separately. Usually, myisampack packs the data file 40% to 70%.

When the table is used later, the server reads into memory the information needed to decompress
columns. This results in much better performance when accessing individual rows, because you only have
to uncompress exactly one row.

MySQL uses mmap() when possible to perform memory mapping on compressed tables. If mmap() does
not work, MySQL falls back to normal read/write file operations.

Please note the following:

• If the mysqld server was invoked with external locking disabled, it is not a good idea to invoke

myisampack if the table might be updated by the server during the packing process. It is safest to
compress tables with the server stopped.

• After packing a table, it becomes read only. This is generally intended (such as when accessing packed

tables on a CD).

• myisampack does not support partitioned tables.

Invoke myisampack like this:

myisampack [options] file_name ...

Each file name argument should be the name of an index (.MYI) file. If you are not in the database
directory, you should specify the path name to the file. It is permissible to omit the .MYI extension.

After you compress a table with myisampack, use myisamchk -rq to rebuild its indexes. Section 4.6.3,
“myisamchk — MyISAM Table-Maintenance Utility”.

myisampack supports the following options. It also reads option files and supports the options for
processing them described at Section 4.2.2.3, “Command-Line Options that Affect Option-File Handling”.

• --help, -?

Command-Line Format

--help

Display a help message and exit.

• --backup, -b

Command-Line Format

--backup

Make a backup of each table's data file using the name tbl_name.OLD.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

598

myisampack — Generate Compressed, Read-Only MyISAM Tables

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --force, -f

Command-Line Format

--force

Produce a packed table even if it becomes larger than the original or if the intermediate file from
an earlier invocation of myisampack exists. (myisampack creates an intermediate file named
tbl_name.TMD in the database directory while it compresses the table. If you kill myisampack, the
.TMD file might not be deleted.) Normally, myisampack exits with an error if it finds that tbl_name.TMD
exists. With --force, myisampack packs the table anyway.

• --join=big_tbl_name, -j big_tbl_name

Command-Line Format

--join=big_tbl_name

Type

String

Join all tables named on the command line into a single packed table big_tbl_name. All tables that are
to be combined must have identical structure (same column names and types, same indexes, and so
forth).

big_tbl_name must not exist prior to the join operation. All source tables named on the command line
to be merged into big_tbl_name must exist. The source tables are read for the join operation but not
modified.

• --silent, -s

Command-Line Format

--silent

Silent mode. Write output only when errors occur.

• --test, -t

Command-Line Format

--test

Do not actually pack the table, just test packing it.

• --tmpdir=dir_name, -T dir_name

599

myisampack — Generate Compressed, Read-Only MyISAM Tables

Command-Line Format

Type

--tmpdir=dir_name

Directory name

Use the named directory as the location where myisampack creates temporary files.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Write information about the progress of the packing operation and its result.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --wait, -w

Command-Line Format

--wait

Wait and retry if the table is in use. If the mysqld server was invoked with external locking disabled, it
is not a good idea to invoke myisampack if the table might be updated by the server during the packing
process.

The following sequence of commands illustrates a typical table compression session:

$> ls -l station.*
-rw-rw-r--   1 jones    my         994128 Apr 17 19:00 station.MYD
-rw-rw-r--   1 jones    my          53248 Apr 17 19:00 station.MYI
-rw-rw-r--   1 jones    my           5767 Apr 17 19:00 station.frm

$> myisamchk -dvv station

MyISAM file:     station
Isam-version:  2
Creation time: 1996-03-13 10:08:58
Recover time:  1997-02-02  3:06:43
Data records:              1192  Deleted blocks:              0
Datafile parts:            1192  Deleted data:                0
Datafile pointer (bytes):     2  Keyfile pointer (bytes):     2
Max datafile length:   54657023  Max keyfile length:   33554431
Recordlength:               834
Record format: Fixed length

table description:
Key Start Len Index   Type                 Root  Blocksize    Rec/key
1   2     4   unique  unsigned long        1024       1024          1
2   32    30  multip. text                10240       1024          1

Field Start Length Type
1     1     1
2     2     4
3     6     4
4     10    1

600

myisampack — Generate Compressed, Read-Only MyISAM Tables

5     11    20
6     31    1
7     32    30
8     62    35
9     97    35
10    132   35
11    167   4
12    171   16
13    187   35
14    222   4
15    226   16
16    242   20
17    262   20
18    282   20
19    302   30
20    332   4
21    336   4
22    340   1
23    341   8
24    349   8
25    357   8
26    365   2
27    367   2
28    369   4
29    373   4
30    377   1
31    378   2
32    380   8
33    388   4
34    392   4
35    396   4
36    400   4
37    404   1
38    405   4
39    409   4
40    413   4
41    417   4
42    421   4
43    425   4
44    429   20
45    449   30
46    479   1
47    480   1
48    481   79
49    560   79
50    639   79
51    718   79
52    797   8
53    805   1
54    806   1
55    807   20
56    827   4
57    831   4

$> myisampack station.MYI
Compressing station.MYI: (1192 records)
- Calculating statistics

normal:     20  empty-space:   16  empty-zero:     12  empty-fill:  11
pre-space:   0  end-space:     12  table-lookups:   5  zero:         7
Original trees:  57  After join: 17
- Compressing file
87.14%
Remember to run myisamchk -rq on compressed tables

$> myisamchk -rq station
- check record delete-chain

601

myisampack — Generate Compressed, Read-Only MyISAM Tables

- recovering (with sort) MyISAM-table 'station'
Data records: 1192
- Fixing index 1
- Fixing index 2

$> mysqladmin -uroot flush-tables

$> ls -l station.*
-rw-rw-r--   1 jones    my         127874 Apr 17 19:00 station.MYD
-rw-rw-r--   1 jones    my          55296 Apr 17 19:04 station.MYI
-rw-rw-r--   1 jones    my           5767 Apr 17 19:00 station.frm

$> myisamchk -dvv station

MyISAM file:     station
Isam-version:  2
Creation time: 1996-03-13 10:08:58
Recover time:  1997-04-17 19:04:26
Data records:               1192  Deleted blocks:              0
Datafile parts:             1192  Deleted data:                0
Datafile pointer (bytes):      3  Keyfile pointer (bytes):     1
Max datafile length:    16777215  Max keyfile length:     131071
Recordlength:                834
Record format: Compressed

table description:
Key Start Len Index   Type                 Root  Blocksize    Rec/key
1   2     4   unique  unsigned long       10240       1024          1
2   32    30  multip. text                54272       1024          1

Field Start Length Type                         Huff tree  Bits
1     1     1      constant                             1     0
2     2     4      zerofill(1)                          2     9
3     6     4      no zeros, zerofill(1)                2     9
4     10    1                                           3     9
5     11    20     table-lookup                         4     0
6     31    1                                           3     9
7     32    30     no endspace, not_always              5     9
8     62    35     no endspace, not_always, no empty    6     9
9     97    35     no empty                             7     9
10    132   35     no endspace, not_always, no empty    6     9
11    167   4      zerofill(1)                          2     9
12    171   16     no endspace, not_always, no empty    5     9
13    187   35     no endspace, not_always, no empty    6     9
14    222   4      zerofill(1)                          2     9
15    226   16     no endspace, not_always, no empty    5     9
16    242   20     no endspace, not_always              8     9
17    262   20     no endspace, no empty                8     9
18    282   20     no endspace, no empty                5     9
19    302   30     no endspace, no empty                6     9
20    332   4      always zero                          2     9
21    336   4      always zero                          2     9
22    340   1                                           3     9
23    341   8      table-lookup                         9     0
24    349   8      table-lookup                        10     0
25    357   8      always zero                          2     9
26    365   2                                           2     9
27    367   2      no zeros, zerofill(1)                2     9
28    369   4      no zeros, zerofill(1)                2     9
29    373   4      table-lookup                        11     0
30    377   1                                           3     9
31    378   2      no zeros, zerofill(1)                2     9
32    380   8      no zeros                             2     9
33    388   4      always zero                          2     9
34    392   4      table-lookup                        12     0
35    396   4      no zeros, zerofill(1)               13     9
36    400   4      no zeros, zerofill(1)                2     9

602

myisampack — Generate Compressed, Read-Only MyISAM Tables

37    404   1                                           2     9
38    405   4      no zeros                             2     9
39    409   4      always zero                          2     9
40    413   4      no zeros                             2     9
41    417   4      always zero                          2     9
42    421   4      no zeros                             2     9
43    425   4      always zero                          2     9
44    429   20     no empty                             3     9
45    449   30     no empty                             3     9
46    479   1                                          14     4
47    480   1                                          14     4
48    481   79     no endspace, no empty               15     9
49    560   79     no empty                             2     9
50    639   79     no empty                             2     9
51    718   79     no endspace                         16     9
52    797   8      no empty                             2     9
53    805   1                                          17     1
54    806   1                                           3     9
55    807   20     no empty                             3     9
56    827   4      no zeros, zerofill(2)                2     9
57    831   4      no zeros, zerofill(1)                2     9

myisampack displays the following kinds of information:

• normal

The number of columns for which no extra packing is used.

• empty-space

The number of columns containing values that are only spaces. These occupy one bit.

• empty-zero

The number of columns containing values that are only binary zeros. These occupy one bit.

• empty-fill

The number of integer columns that do not occupy the full byte range of their type. These are changed to
a smaller type. For example, a BIGINT column (eight bytes) can be stored as a TINYINT column (one
byte) if all its values are in the range from -128 to 127.

• pre-space

The number of decimal columns that are stored with leading spaces. In this case, each value contains a
count for the number of leading spaces.

• end-space

The number of columns that have a lot of trailing spaces. In this case, each value contains a count for
the number of trailing spaces.

• table-lookup

The column had only a small number of different values, which were converted to an ENUM before
Huffman compression.

• zero

The number of columns for which all values are zero.

• Original trees

603

myisampack — Generate Compressed, Read-Only MyISAM Tables

The initial number of Huffman trees.

• After join

The number of distinct Huffman trees left after joining trees to save some header space.

After a table has been compressed, the Field lines displayed by myisamchk -dvv include additional
information about each column:

• Type

The data type. The value may contain any of the following descriptors:

• constant

All rows have the same value.

• no endspace

Do not store endspace.

• no endspace, not_always

Do not store endspace and do not do endspace compression for all values.

• no endspace, no empty

Do not store endspace. Do not store empty values.

• table-lookup

The column was converted to an ENUM.

• zerofill(N)

The most significant N bytes in the value are always 0 and are not stored.

• no zeros

Do not store zeros.

• always zero

Zero values are stored using one bit.

• Huff tree

The number of the Huffman tree associated with the column.

• Bits

The number of bits used in the Huffman tree.

After you run myisampack, use myisamchk to re-create any indexes. At this time, you can also sort the
index blocks and create statistics needed for the MySQL optimizer to work more efficiently:

myisamchk -rq --sort-index --analyze tbl_name.MYI

604

mysql_config_editor — MySQL Configuration Utility

After you have installed the packed table into the MySQL database directory, you should execute
mysqladmin flush-tables to force mysqld to start using the new table.

To unpack a packed table, use the --unpack option to myisamchk.

4.6.6 mysql_config_editor — MySQL Configuration Utility

The mysql_config_editor utility enables you to store authentication credentials in an obfuscated login
path file named .mylogin.cnf. The file location is the %APPDATA%\MySQL directory on Windows and
the current user's home directory on non-Windows systems. The file can be read later by MySQL client
programs to obtain authentication credentials for connecting to MySQL Server.

The unobfuscated format of the .mylogin.cnf login path file consists of option groups, similar to other
option files. Each option group in .mylogin.cnf is called a “login path,” which is a group that permits only
certain options: host, user, password, port and socket. Think of a login path option group as a set of
options that specify which MySQL server to connect to and which account to authenticate as. Here is an
unobfuscated example:

[client]
user = mydefaultname
password = mydefaultpass
host = 127.0.0.1
[mypath]
user = myothername
password = myotherpass
host = localhost

When you invoke a client program to connect to the server, the client uses .mylogin.cnf in conjunction
with other option files. Its precedence is higher than other option files, but less than options specified
explicitly on the client command line. For information about the order in which option files are used, see
Section 4.2.2.2, “Using Option Files”.

To specify an alternate login path file name, set the MYSQL_TEST_LOGIN_FILE environment
variable. This variable is recognized by mysql_config_editor, by standard MySQL clients (mysql,
mysqladmin, and so forth), and by the mysql-test-run.pl testing utility.

Programs use groups in the login path file as follows:

• mysql_config_editor operates on the client login path by default if you specify no --login-

path=name option to indicate explicitly which login path to use.

• Without a --login-path option, client programs read the same option groups from the login path file

that they read from other option files. Consider this command:

mysql

By default, the mysql client reads the [client] and [mysql] groups from other option files, so it
reads them from the login path file as well.

• With a --login-path option, client programs additionally read the named login path from the login
path file. The option groups read from other option files remain the same. Consider this command:

mysql --login-path=mypath

The mysql client reads [client] and [mysql] from other option files, and [client], [mysql], and
[mypath] from the login path file.

• Client programs read the login path file even when the --no-defaults option is used, unless --no-
login-paths is set. This permits passwords to be specified in a safer way than on the command line
even if --no-defaults is present.

605

mysql_config_editor — MySQL Configuration Utility

mysql_config_editor obfuscates the .mylogin.cnf file so it cannot be read as cleartext, and its
contents when unobfuscated by client programs are used only in memory. In this way, passwords can be
stored in a file in non-cleartext format and used later without ever needing to be exposed on the command
line or in an environment variable. mysql_config_editor provides a print command for displaying the
login path file contents, but even in this case, password values are masked so as never to appear in a way
that other users can see them.

The obfuscation used by mysql_config_editor prevents passwords from appearing in .mylogin.cnf
as cleartext and provides a measure of security by preventing inadvertent password exposure. For
example, if you display a regular unobfuscated my.cnf option file on the screen, any passwords it contains
are visible for anyone to see. With .mylogin.cnf, that is not true, but the obfuscation used is not likely
to deter a determined attacker and you should not consider it unbreakable. A user who can gain system
administration privileges on your machine to access your files could unobfuscate the .mylogin.cnf file
with some effort.

The login path file must be readable and writable to the current user, and inaccessible to other users.
Otherwise, mysql_config_editor ignores it, and client programs do not use it, either.

Invoke mysql_config_editor like this:

mysql_config_editor [program_options] command [command_options]

If the login path file does not exist, mysql_config_editor creates it.

Command arguments are given as follows:

• program_options consists of general mysql_config_editor options.

• command indicates what action to perform on the .mylogin.cnf login path file. For example, set

writes a login path to the file, remove removes a login path, and print displays login path contents.

• command_options indicates any additional options specific to the command, such as the login path

name and the values to use in the login path.

The position of the command name within the set of program arguments is significant. For example, these
command lines have the same arguments, but produce different results:

mysql_config_editor --help set
mysql_config_editor set --help

The first command line displays a general mysql_config_editor help message, and ignores the set
command. The second command line displays a help message specific to the set command.

Suppose that you want to establish a client login path that defines your default connection
parameters, and an additional login path named remote for connecting to the MySQL server the host
remote.example.com. You want to log in as follows:

• By default, to the local server with a user name and password of localuser and localpass

• To the remote server with a user name and password of remoteuser and remotepass

To set up the login paths in the .mylogin.cnf file, use the following set commands. Enter each
command on a single line, and enter the appropriate passwords when prompted:

$> mysql_config_editor set --login-path=client
         --host=localhost --user=localuser --password
Enter password: enter password "localpass" here
$> mysql_config_editor set --login-path=remote
         --host=remote.example.com --user=remoteuser --password
Enter password: enter password "remotepass" here

606

mysql_config_editor — MySQL Configuration Utility

mysql_config_editor uses the client login path by default, so the --login-path=client option
can be omitted from the first command without changing its effect.

To see what mysql_config_editor writes to the .mylogin.cnf file, use the print command:

$> mysql_config_editor print --all
[client]
user = localuser
password = *****
host = localhost
[remote]
user = remoteuser
password = *****
host = remote.example.com

The print command displays each login path as a set of lines beginning with a group header indicating
the login path name in square brackets, followed by the option values for the login path. Password values
are masked and do not appear as cleartext.

If you do not specify --all to display all login paths or --login-path=name to display a named login
path, the print command displays the client login path by default, if there is one.

As shown by the preceding example, the login path file can contain multiple login paths. In this way,
mysql_config_editor makes it easy to set up multiple “personalities” for connecting to different MySQL
servers, or for connecting to a given server using different accounts. Any of these can be selected by name
later using the --login-path option when you invoke a client program. For example, to connect to the
remote server, use this command:

mysql --login-path=remote

Here, mysql reads the [client] and [mysql] option groups from other option files, and the [client],
[mysql], and [remote] groups from the login path file.

To connect to the local server, use this command:

mysql --login-path=client

Because mysql reads the client and mysql login paths by default, the --login-path option does not
add anything in this case. That command is equivalent to this one:

mysql

Options read from the login path file take precedence over options read from other option files. Options
read from login path groups appearing later in the login path file take precedence over options read from
groups appearing earlier in the file.

mysql_config_editor adds login paths to the login path file in the order you create them, so you
should create more general login paths first and more specific paths later. If you need to move a login path
within the file, you can remove it, then recreate it to add it to the end. For example, a client login path
is more general because it is read by all client programs, whereas a mysqldump login path is read only
by mysqldump. Options specified later override options specified earlier, so putting the login paths in the
order client, mysqldump enables mysqldump-specific options to override client options.

When you use the set command with mysql_config_editor to create a login path, you need not
specify all possible option values (host name, user name, password, port, socket). Only those values given
are written to the path. Any missing values required later can be specified when you invoke a client path
to connect to the MySQL server, either in other option files or on the command line. Any options specified
on the command line override those specified in the login path file or other option files. For example, if
the credentials in the remote login path also apply for the host remote2.example.com, connect to the
server on that host like this:

607

mysql_config_editor — MySQL Configuration Utility

mysql --login-path=remote --host=remote2.example.com

mysql_config_editor General Options

mysql_config_editor supports the following general options, which may be used preceding
any command named on the command line. For descriptions of command-specific options, see
mysql_config_editor Commands and Command-Specific Options.

Table 4.22 mysql_config_editor General Options

Option Name

--debug

--help

--verbose

--version

• --help, -?

Description

Write debugging log

Display help message and exit

Verbose mode

Display version information and exit

Command-Line Format

--help

Display a general help message and exit.

To see a command-specific help message, invoke mysql_config_editor as follows, where command
is a command other than help:

mysql_config_editor command --help

• --debug[=debug_options], -# debug_options

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/mysql_config_editor.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This option may be helpful in
diagnosing problems if an operation does not have the effect you expect.

• --version, -V

Command-Line Format

--version

Display version information and exit.

608

mysql_config_editor — MySQL Configuration Utility

mysql_config_editor Commands and Command-Specific Options

This section describes the permitted mysql_config_editor commands, and, for each one, the
command-specific options permitted following the command name on the command line.

In addition, mysql_config_editor supports general options that can be used preceding any command.
For descriptions of these options, see mysql_config_editor General Options.

mysql_config_editor supports these commands:

• help

Display a general help message and exit. This command takes no following options.

To see a command-specific help message, invoke mysql_config_editor as follows, where command
is a command other than help:

mysql_config_editor command --help

• print [options]

Print the contents of the login path file in unobfuscated form, with the exception that passwords are
displayed as *****.

The default login path name is client if no login path is named. If both --all and --login-path are
given, --all takes precedence.

The print command permits these options following the command name:

• --help, -?

Display a help message for the print command and exit.

To see a general help message, use mysql_config_editor --help.

• --all

Print the contents of all login paths in the login path file.

• --login-path=name, -G name

Print the contents of the named login path.

• remove [options]

Remove a login path from the login path file, or modify a login path by removing options from it.

This command removes from the login path only such options as are specified with the --host, --
password, --port, --socket, and --user options. If none of those options are given, remove
removes the entire login path. For example, this command removes only the user option from the
mypath login path rather than the entire mypath login path:

mysql_config_editor remove --login-path=mypath --user

This command removes the entire mypath login path:

mysql_config_editor remove --login-path=mypath

The remove command permits these options following the command name:

609

mysql_config_editor — MySQL Configuration Utility

• --help, -?

Display a help message for the remove command and exit.

To see a general help message, use mysql_config_editor --help.

• --host, -h

Remove the host name from the login path.

• --login-path=name, -G name

The login path to remove or modify. The default login path name is client if this option is not given.

• --password, -p

Remove the password from the login path.

• --port, -P

Remove the TCP/IP port number from the login path.

• --socket, -S

Remove the Unix socket file name from the login path.

• --user, -u

Remove the user name from the login path.

• --warn, -w

Warn and prompt the user for confirmation if the command attempts to remove the default login path
(client) and --login-path=client was not specified. This option is enabled by default; use --
skip-warn to disable it.

• reset [options]

Empty the contents of the login path file.

The reset command permits these options following the command name:

• --help, -?

Display a help message for the reset command and exit.

To see a general help message, use mysql_config_editor --help.

610

mysqlbinlog — Utility for Processing Binary Log Files

• set [options]

Write a login path to the login path file.

This command writes to the login path only such options as are specified with the --host,
--password, --port, --socket, and --user options. If none of those options are given,
mysql_config_editor writes the login path as an empty group.

The set command permits these options following the command name:

• --help, -?

Display a help message for the set command and exit.

To see a general help message, use mysql_config_editor --help.

• --host=host_name, -h host_name

The host name to write to the login path.

• --login-path=name, -G name

The login path to create. The default login path name is client if this option is not given.

• --password, -p

Prompt for a password to write to the login path. After mysql_config_editor displays the
prompt, type the password and press Enter. To prevent other users from seeing the password,
mysql_config_editor does not echo it.

To specify an empty password, press Enter at the password prompt. The resulting login path written to
the login path file includes a line like this:

password =

• --port=port_num, -P port_num

The TCP/IP port number to write to the login path.

• --socket=file_name, -S file_name

The Unix socket file name to write to the login path.

• --user=user_name, -u user_name

The user name to write to the login path.

• --warn, -w

Warn and prompt the user for confirmation if the command attempts to overwrite an existing login
path. This option is enabled by default; use --skip-warn to disable it.

4.6.7 mysqlbinlog — Utility for Processing Binary Log Files

The server's binary log consists of files containing “events” that describe modifications to database
contents. The server writes these files in binary format. To display their contents in text format, use the
mysqlbinlog utility. You can also use mysqlbinlog to display the contents of relay log files written by a
replica server in a replication setup because relay logs have the same format as binary logs. The binary log

611

mysqlbinlog — Utility for Processing Binary Log Files

and relay log are discussed further in Section 5.4.4, “The Binary Log”, and Section 16.2.4, “Relay Log and
Replication Metadata Repositories”.

Invoke mysqlbinlog like this:

mysqlbinlog [options] log_file ...

For example, to display the contents of the binary log file named binlog.000003, use this command:

mysqlbinlog binlog.000003

The output includes events contained in binlog.000003. For statement-based logging, event information
includes the SQL statement, the ID of the server on which it was executed, the timestamp when the
statement was executed, how much time it took, and so forth. For row-based logging, the event indicates
a row change rather than an SQL statement. See Section 16.2.1, “Replication Formats”, for information
about logging modes.

Events are preceded by header comments that provide additional information. For example:

# at 141
#100309  9:28:36 server id 123  end_log_pos 245
  Query thread_id=3350  exec_time=11  error_code=0

In the first line, the number following at indicates the file offset, or starting position, of the event in the
binary log file.

The second line starts with a date and time indicating when the statement started on the server where
the event originated. For replication, this timestamp is propagated to replica servers. server id is the
server_id value of the server where the event originated. end_log_pos indicates where the next event
starts (that is, it is the end position of the current event + 1). thread_id indicates which thread executed
the event. exec_time is the time spent executing the event, on a replication source server. On a replica, it
is the difference of the end execution time on the replica minus the beginning execution time on the source.
The difference serves as an indicator of how much replication lags behind the source. error_code
indicates the result from executing the event. Zero means that no error occurred.

Note

When using event groups, the file offsets of events may be grouped together and
the comments of events may be grouped together. Do not mistake these grouped
events for blank file offsets.

The output from mysqlbinlog can be re-executed (for example, by using it as input to mysql) to redo
the statements in the log. This is useful for recovery operations after an unexpected server exit. For other
usage examples, see the discussion later in this section and in Section 7.5, “Point-in-Time (Incremental)
Recovery”.

You can use mysqlbinlog to read binary log files directly and apply them to the local MySQL server. You
can also read binary logs from a remote server by using the --read-from-remote-server option. To
read remote binary logs, the connection parameter options can be given to indicate how to connect to the
server. These options are --host, --password, --port, --protocol, --socket, and --user.

When running mysqlbinlog against a large binary log, be careful that the filesystem has enough space
for the resulting files. To configure the directory that mysqlbinlog uses for temporary files, use the
TMPDIR environment variable.

mysqlbinlog sets the value of pseudo_slave_mode to true before executing any SQL statements. This
system variable affects the handling of XA transactions.

612

mysqlbinlog — Utility for Processing Binary Log Files

mysqlbinlog supports the following options, which can be specified on the command line or in the
[mysqlbinlog] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 4.2.2.2, “Using Option Files”.

Table 4.23 mysqlbinlog Options

Option Name

--base64-output

--bind-address

--binlog-row-event-max-
size

--character-sets-dir

--connection-server-id

--database

--debug

--debug-check

--debug-info

--default-auth

--defaults-extra-file

--defaults-file

Description

Introduced

Deprecated

Print binary log entries
using base-64 encoding

Use specified network
interface to connect to
MySQL Server

Binary log max event size

Directory where
character sets are
installed

Used for testing and
debugging. See text for
applicable default values
and other particulars

List entries for just this
database

Write debugging log

Print debugging
information when
program exits

Print debugging
information, memory,
and CPU statistics when
program exits

Authentication plugin to
use

Read named option file in
addition to usual option
files

Read only named option
file

--defaults-group-suffix

Option group suffix value

--disable-log-bin

Disable binary logging

--exclude-gtids

--force-if-open

--force-read

Do not show any of the
groups in the GTID set
provided

Read binary log files
even if open or not
closed properly

If mysqlbinlog reads a
binary log event that it

613

mysqlbinlog — Utility for Processing Binary Log Files

Option Name

Description
does not recognize, it
prints a warning

Introduced

Deprecated

--get-server-public-key

Request RSA public key
from server

5.7.23

--help

--hexdump

--host

--idempotent

--include-gtids

--local-load

--login-path

--no-defaults

--offset

--open-files-limit

--password

--plugin-dir

--port

Display help message
and exit

Display a hex dump of
the log in comments

Host on which MySQL
server is located

Cause the server to use
idempotent mode while
processing binary log
updates from this session
only

Show only the groups in
the GTID set provided

Prepare local temporary
files for LOAD DATA in
the specified directory

Read login path options
from .mylogin.cnf

Read no option files

Skip the first N entries in
the log

Specify the number of
open file descriptors to
reserve

Password to use when
connecting to server

Directory where plugins
are installed

TCP/IP port number for
connection

--print-defaults

Print default options

--protocol

--raw

--read-from-remote-
master

Transport protocol to use

Write events in raw
(binary) format to output
files

Read the binary log from
a MySQL replication
source server rather than
reading a local log file

614

mysqlbinlog — Utility for Processing Binary Log Files

Option Name

Description

Introduced

Deprecated

--read-from-remote-
server

--result-file

--rewrite-db

--secure-auth

--server-id

--server-id-bits

Read binary log from
MySQL server rather
than local log file

Direct output to named
file

Create rewrite rules for
databases when playing
back from logs written in
row-based format. Can
be used multiple times

Do not send passwords
to server in old (pre-4.1)
format

Extract only those events
created by the server
having the given server
ID

Tell mysqlbinlog how
to interpret server IDs
in binary log when log
was written by a mysqld
having its server-id-
bits set to less than the
maximum; supported
only by MySQL Cluster
version of mysqlbinlog

--server-public-key-path Path name to file

5.7.23

--set-charset

--shared-memory-base-
name

--short-form

--skip-gtids

--socket

--ssl

containing RSA public
key

Add a SET NAMES
charset_name statement
to the output

Shared-memory name
for shared-memory
connections (Windows
only)

Display only the
statements contained in
the log

Do not include the GTIDs
from the binary log files in
the output dump file

Unix socket file or
Windows named pipe to
use

Enable connection
encryption

Yes

615

mysqlbinlog — Utility for Processing Binary Log Files

Option Name

Description

Introduced

Deprecated

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-key

--ssl-mode

File that contains list of
trusted SSL Certificate
Authorities

Directory that contains
trusted SSL Certificate
Authority certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains
certificate revocation lists

Directory that contains
certificate revocation-list
files

File that contains X.509
key

Desired security state of
connection to server

5.7.11

--ssl-verify-server-cert

--start-datetime

--start-position

--stop-datetime

--stop-never

--stop-never-slave-
server-id

--stop-position

Verify host name
against server certificate
Common Name identity

Read binary log from first
event with timestamp
equal to or later than
datetime argument

Decode binary log from
first event with position
equal to or greater than
argument

Stop reading binary log at
first event with timestamp
equal to or greater than
datetime argument

Stay connected to server
after reading last binary
log file

Slave server ID to report
when connecting to
server

Stop decoding binary log
at first event with position
equal to or greater than
argument

616

mysqlbinlog — Utility for Processing Binary Log Files

Introduced

5.7.10

Deprecated

Option Name

--tls-version

--to-last-log

--user

--verbose

Description

Permissible TLS
protocols for encrypted
connections

Do not stop at the end of
requested binary log from
a MySQL server, but
rather continue printing to
end of last binary log

MySQL user name to
use when connecting to
server

Reconstruct row events
as SQL statements

--verify-binlog-checksum Verify checksums in

binary log

Display version
information and exit

--version

• --help, -?

Command-Line Format

--help

Display a help message and exit.

• --base64-output=value

Command-Line Format

--base64-output=value

Type

Default Value

Valid Values

String

AUTO

AUTO

NEVER

DECODE-ROWS

This option determines when events should be displayed encoded as base-64 strings using BINLOG
statements. The option has these permissible values (not case-sensitive):

• AUTO ("automatic") or UNSPEC ("unspecified") displays BINLOG statements automatically when

necessary (that is, for format description events and row events). If no --base64-output option is
given, the effect is the same as --base64-output=AUTO.

Note

Automatic BINLOG display is the only safe behavior if you intend to use the
output of mysqlbinlog to re-execute binary log file contents. The other option
values are intended only for debugging or testing purposes because they may
produce output that does not include all events in executable form.

617

mysqlbinlog — Utility for Processing Binary Log Files

• NEVER causes BINLOG statements not to be displayed. mysqlbinlog exits with an error if a row

event is found that must be displayed using BINLOG.

• DECODE-ROWS specifies to mysqlbinlog that you intend for row events to be decoded and displayed
as commented SQL statements by also specifying the --verbose option. Like NEVER, DECODE-ROWS
suppresses display of BINLOG statements, but unlike NEVER, it does not exit with an error if a row
event is found.

For examples that show the effect of --base64-output and --verbose on row event output, see
Section 4.6.7.2, “mysqlbinlog Row Event Display”.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --binlog-row-event-max-size=N

Command-Line Format

--binlog-row-event-max-size=#

Type

Default Value

Minimum Value

Maximum Value

Numeric

4294967040

256

18446744073709547520

Specify the maximum size of a row-based binary log event, in bytes. Rows are grouped into events
smaller than this size if possible. The value should be a multiple of 256. The default is 4GB.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• --connection-server-id=server_id

Command-Line Format

--connection-server-id=#]

Type

Default Value

Minimum Value

Integer

0 (1)

0 (1)

618

mysqlbinlog — Utility for Processing Binary Log Files

Maximum Value

4294967295

This option is used to test a MySQL server for support of the BINLOG_DUMP_NON_BLOCK connection
flag. It is not required for normal operations.

The effective default and minimum values for this option depend on whether mysqlbinlog is run in
blocking mode or non-blocking mode. When mysqlbinlog is run in blocking mode, the default (and
minimum) value is 1; when run in non-blocking mode, the default (and minimum) value is 0.

• --database=db_name, -d db_name

Command-Line Format

--database=db_name

Type

String

This option causes mysqlbinlog to output entries from the binary log (local log only) that occur while
db_name is been selected as the default database by USE.

The --database option for mysqlbinlog is similar to the --binlog-do-db option for mysqld, but
can be used to specify only one database. If --database is given multiple times, only the last instance
is used.

The effects of this option depend on whether the statement-based or row-based logging format is in
use, in the same way that the effects of --binlog-do-db depend on whether statement-based or row-
based logging is in use.

Statement-based logging.

 The --database option works as follows:

• While db_name is the default database, statements are output whether they modify tables in db_name

or a different database.

• Unless db_name is selected as the default database, statements are not output, even if they modify

tables in db_name.

• There is an exception for CREATE DATABASE, ALTER DATABASE, and DROP DATABASE. The
database being created, altered, or dropped is considered to be the default database when
determining whether to output the statement.

Suppose that the binary log was created by executing these statements using statement-based-logging:

INSERT INTO test.t1 (i) VALUES(100);
INSERT INTO db2.t2 (j)  VALUES(200);
USE test;
INSERT INTO test.t1 (i) VALUES(101);
INSERT INTO t1 (i)      VALUES(102);
INSERT INTO db2.t2 (j)  VALUES(201);
USE db2;
INSERT INTO test.t1 (i) VALUES(103);
INSERT INTO db2.t2 (j)  VALUES(202);

619

mysqlbinlog — Utility for Processing Binary Log Files

INSERT INTO t2 (j)      VALUES(203);

mysqlbinlog --database=test does not output the first two INSERT statements because there
is no default database. It outputs the three INSERT statements following USE test, but not the three
INSERT statements following USE db2.

mysqlbinlog --database=db2 does not output the first two INSERT statements because there is no
default database. It does not output the three INSERT statements following USE test, but does output
the three INSERT statements following USE db2.

 mysqlbinlog outputs only entries that change tables belonging to db_name.

Row-based logging.
The default database has no effect on this. Suppose that the binary log just described was created using
row-based logging rather than statement-based logging. mysqlbinlog --database=test outputs
only those entries that modify t1 in the test database, regardless of whether USE was issued or what the
default database is.

If a server is running with binlog_format set to MIXED and you want it to be possible to use
mysqlbinlog with the --database option, you must ensure that tables that are modified are in the
database selected by USE. (In particular, no cross-database updates should be used.)

When used together with the --rewrite-db option, the --rewrite-db option is applied first; then the
--database option is applied, using the rewritten database name. The order in which the options are
provided makes no difference in this regard.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o,/tmp/mysqlbinlog.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/mysqlbinlog.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

620

mysqlbinlog — Utility for Processing Binary Log Files

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 6.2.13, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqlbinlog normally reads the [client] and [mysqlbinlog] groups. If this option is

621

mysqlbinlog — Utility for Processing Binary Log Files

given as --defaults-group-suffix=_other, mysqlbinlog also reads the [client_other] and
[mysqlbinlog_other] groups.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --disable-log-bin, -D

Command-Line Format

--disable-log-bin

Disable binary logging. This is useful for avoiding an endless loop if you use the --to-last-log option
and are sending the output to the same MySQL server. This option also is useful when restoring after an
unexpected exit to avoid duplication of the statements you have logged.

This option causes mysqlbinlog to include a SET sql_log_bin = 0 statement in its output to
disable binary logging of the remaining output. Manipulating the session value of the sql_log_bin
system variable is a restricted operation, so this option requires that you have privileges sufficient to set
restricted session variables. See Section 5.1.8.1, “System Variable Privileges”.

• --exclude-gtids=gtid_set

Command-Line Format

--exclude-gtids=gtid_set

Type

Default Value

String

Do not display any of the groups listed in the gtid_set.

• --force-if-open, -F

Command-Line Format

--force-if-open

Read binary log files even if they are open or were not closed properly.

• --force-read, -f

Command-Line Format

--force-read

With this option, if mysqlbinlog reads a binary log event that it does not recognize, it prints a warning,
ignores the event, and continues. Without this option, mysqlbinlog stops if it reads such an event.

• --get-server-public-key

Command-Line Format

--get-server-public-key

622

Introduced

Type

5.7.23

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This option

applies to clients that authenticate with the caching_sha2_password authentication plugin. For that

plugin, the server does not send the public key unless requested. This option is ignored for accounts that

mysqlbinlog — Utility for Processing Binary Log Files

do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not used, as is
the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 6.4.1.4, “Caching SHA-2
Pluggable Authentication”.

The --get-server-public-key option was added in MySQL 5.7.23.

• --hexdump, -H

Command-Line Format

--hexdump

Display a hex dump of the log in comments, as described in Section 4.6.7.1, “mysqlbinlog Hex Dump
Format”. The hex output can be helpful for replication debugging.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Get the binary log from the MySQL server on the given host.

• --idempotent

Command-Line Format

--idempotent

Type

Default Value

Boolean

true

Tell the MySQL Server to use idempotent mode while processing updates; this causes suppression
of any duplicate-key or key-not-found errors that the server encounters in the current session while
processing updates. This option may prove useful whenever it is desirable or necessary to replay one or
more binary logs to a MySQL Server which may not contain all of the data to which the logs refer.

The scope of effect for this option includes the current mysqlbinlog client and session only.

• --include-gtids=gtid_set

Command-Line Format

--include-gtids=gtid_set

Type

Default Value

String

Display only the groups listed in the gtid_set.

• --local-load=dir_name, -l dir_name

Command-Line Format

--local-load=dir_name

623

mysqlbinlog — Utility for Processing Binary Log Files

Type

Directory name

For data loading operations corresponding to LOAD DATA statements, mysqlbinlog extracts the files
from the binary log events, writes them as temporary files to the local file system, and writes LOAD DATA
LOCAL statements to cause the files to be loaded. By default, mysqlbinlog writes these temporary files
to an operating system-specific directory. The --local-load option can be used to explicitly specify
the directory where mysqlbinlog should prepare local temporary files.

Important

These temporary files are not automatically removed by mysqlbinlog or any
other MySQL program.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits passwords to
be specified in a safer way than on the command line even when --no-defaults is used. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 4.6.6, “mysql_config_editor —
MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --offset=N, -o N

Command-Line Format

Type

Skip the first N entries in the log.

• --open-files-limit=N

--offset=#

Numeric

Command-Line Format

--open-files-limit=#

624

mysqlbinlog — Utility for Processing Binary Log Files

Type

Default Value

Minimum Value

Maximum Value

Numeric

8

1

[platform dependent]

Specify the number of open file descriptors to reserve.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is optional.
If not given, mysqlbinlog prompts for one. If given, there must be no space between --password= or
-p and the password following it. If no password option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 6.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlbinlog should not prompt for one, use the
--skip-password option.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlbinlog does not find it. See Section 6.2.13, “Pluggable
Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

The TCP/IP port number to use for connecting to a remote server.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

625

mysqlbinlog — Utility for Processing Binary Log Files

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

String

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 4.2.5, “Connection Transport Protocols”.

• --raw

Command-Line Format

Type

Default Value

--raw

Boolean

FALSE

By default, mysqlbinlog reads binary log files and writes events in text format. The --raw option
tells mysqlbinlog to write them in their original binary format. Its use requires that --read-from-
remote-server also be used because the files are requested from a server. mysqlbinlog writes
one output file for each file read from the server. The --raw option can be used to make a backup of a
server's binary log. With the --stop-never option, the backup is “live” because mysqlbinlog stays
connected to the server. By default, output files are written in the current directory with the same names
as the original log files. Output file names can be modified using the --result-file option. For more
information, see Section 4.6.7.3, “Using mysqlbinlog to Back Up Binary Log Files”.

• --read-from-remote-master=type

Command-Line Format

--read-from-remote-master=type

Read binary logs from a MySQL server with the COM_BINLOG_DUMP or COM_BINLOG_DUMP_GTID
commands by setting the option value to either BINLOG-DUMP-NON-GTIDS or BINLOG-DUMP-
GTIDS, respectively. If --read-from-remote-master=BINLOG-DUMP-GTIDS is combined with --
exclude-gtids, transactions can be filtered out on the source, avoiding unnecessary network traffic.

The connection parameter options are used with this option or the --read-from-remote-server
option. These options are --host, --password, --port, --protocol, --socket, and --user. If
neither of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use this option.

• --read-from-remote-server=file_name, -R

Command-Line Format

--read-from-remote-server=file_name

626

mysqlbinlog — Utility for Processing Binary Log Files

Read the binary log from a MySQL server rather than reading a local log file. This option requires that
the remote server be running. It works only for binary log files on the remote server, not relay log files,
and takes only the binary log file name (including the numeric suffix) as its argument, while ignoring any
path.

The connection parameter options are used with this option or the --read-from-remote-master
option. These options are --host, --password, --port, --protocol, --socket, and --user. If
neither of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use this option.

This option is like --read-from-remote-master=BINLOG-DUMP-NON-GTIDS.

• --result-file=name, -r name

Command-Line Format

--result-file=name

Without the --raw option, this option indicates the file to which mysqlbinlog writes text output. With
--raw, mysqlbinlog writes one binary output file for each log file transferred from the server, writing
them by default in the current directory using the same names as the original log file. In this case, the --
result-file option value is treated as a prefix that modifies output file names.

• --rewrite-db='from_name->to_name'

Command-Line Format

--rewrite-db='oldname->newname'

Type

Default Value

String

[none]

When reading from a row-based or statement-based log, rewrite all occurrences of from_name
to to_name. Rewriting is done on the rows, for row-based logs, as well as on the USE clauses, for
statement-based logs. In MySQL versions prior to 5.7.8, this option was only for use when restoring
tables logged using the row-based format.

Warning

Statements in which table names are qualified with database names are not
rewritten to use the new name when using this option.

The rewrite rule employed as a value for this option is a string having the form 'from_name-
>to_name', as shown previously, and for this reason must be enclosed by quotation marks.

To employ multiple rewrite rules, specify the option multiple times, as shown here:

mysqlbinlog --rewrite-db='dbcurrent->dbold' --rewrite-db='dbtest->dbcurrent' \
    binlog.00001 > /tmp/statements.sql

When used together with the --database option, the --rewrite-db option is applied first; then --
database option is applied, using the rewritten database name. The order in which the options are
provided makes no difference in this regard.

This means that, for example, if mysqlbinlog is started with --rewrite-db='mydb->yourdb' --
database=yourdb, then all updates to any tables in databases mydb and yourdb are included in the
output. On the other hand, if it is started with --rewrite-db='mydb->yourdb' --database=mydb,

627

mysqlbinlog — Utility for Processing Binary Log Files

then mysqlbinlog outputs no statements at all: since all updates to mydb are first rewritten as
updates to yourdb before applying the --database option, there remain no updates that match --
database=mydb.

• --secure-auth

Command-Line Format

Deprecated

--secure-auth

Yes

Do not send passwords to the server in old (pre-4.1) format. This prevents connections except for
servers that use the newer password format.

As of MySQL 5.7.5, this option is deprecated; expect it to be removed in a future MySQL release. It is
always enabled and attempting to disable it (--skip-secure-auth, --secure-auth=0) produces an
error. Before MySQL 5.7.5, this option is enabled by default but can be disabled.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them was removed in MySQL 5.7.5.
For account upgrade instructions, see Section 6.4.1.3, “Migrating Away from
Pre-4.1 Password Hashing and the mysql_old_password Plugin”.

• --server-id=id

Command-Line Format

Type

--server-id=id

Numeric

Display only those events created by the server having the given server ID.

• --server-id-bits=N

Command-Line Format

--server-id-bits=#

Type

Default Value

Minimum Value

Maximum Value

Numeric

32

7

32

Use only the first N bits of the server_id to identify the server. If the binary log was written by a
mysqld with server-id-bits set to less than 32 and user data stored in the most significant bit, running
mysqlbinlog with --server-id-bits set to 32 enables this data to be seen.

This option is supported only by the version of mysqlbinlog supplied with the NDB Cluster distribution,
or built with NDB Cluster support.

• --server-public-key-path=file_name

Command-Line Format

Introduced

--server-public-key-path=file_name

5.7.23

628

mysqlbinlog — Utility for Processing Binary Log Files

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate with
the sha256_password or caching_sha2_password authentication plugin. This option is ignored for
accounts that do not authenticate with one of those plugins. It is also ignored if RSA-based password
exchange is not used, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password, this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 6.4.1.5, “SHA-256 Pluggable Authentication”, and Section 6.4.1.4, “Caching SHA-2 Pluggable
Authentication”.

The --server-public-key-path option was added in MySQL 5.7.23.

• --set-charset=charset_name

Command-Line Format

--set-charset=charset_name

Type

String

Add a SET NAMES charset_name statement to the output to specify the character set to be used for
processing log files.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled to
support shared-memory connections.

• --short-form, -s

Command-Line Format

--short-form

Display only the statements contained in the log, without any extra information or row-based events. This
is for testing only, and should not be used in production systems.

• --skip-gtids[=(true|false)]

629

Command-Line Format

--skip-gtids[=true|false]

Type

Boolean

mysqlbinlog — Utility for Processing Binary Log Files

Default Value

false

Do not include the GTIDs from the binary log files in the output dump file. For example:

mysqlbinlog --skip-gtids binlog.000001 >  /tmp/dump.sql
mysql -u root -p -e "source /tmp/dump.sql"

You should not normally use this option in production or in recovery, except in the specific, and rare,
scenarios where the GTIDs are actively unwanted. For example, an administrator might want to
duplicate selected transactions (such as table definitions) from a deployment to another, unrelated,
deployment that will not replicate to or from the original. In that scenario, --skip-gtids can be used to
enable the administrator to apply the transactions as if they were new, and ensure that the deployments
remain unrelated. However, you should only use this option if the inclusion of the GTIDs causes a known
issue for your use case.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named pipe
to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be a
member of the Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --start-datetime=datetime

Command-Line Format

--start-datetime=datetime

Type

Datetime

Start reading the binary log at the first event having a timestamp equal to or later than the datetime
argument. The datetime value is relative to the local time zone on the machine where you run
mysqlbinlog. The value should be in a format accepted for the DATETIME or TIMESTAMP data types.
For example:

mysqlbinlog --start-datetime="2005-12-25 11:25:56" binlog.000003

This option is useful for point-in-time recovery. See Section 7.5, “Point-in-Time (Incremental) Recovery”.

• --start-position=N, -j N

630

Command-Line Format

--start-position=#

mysqlbinlog — Utility for Processing Binary Log Files

Type

Numeric

Start reading the binary log at the first event having a position equal to or greater than N. This option
applies to the first log file named on the command line.

This option is useful for point-in-time recovery. See Section 7.5, “Point-in-Time (Incremental) Recovery”.

• --stop-datetime=datetime

Command-Line Format

--stop-datetime=datetime

Stop reading the binary log at the first event having a timestamp equal to or later than the datetime
argument. See the description of the --start-datetime option for information about the datetime
value.

This option is useful for point-in-time recovery. See Section 7.5, “Point-in-Time (Incremental) Recovery”.

• --stop-never

Command-Line Format

--stop-never

Type

Default Value

Boolean

FALSE

This option is used with --read-from-remote-server. It tells mysqlbinlog to remain connected
to the server. Otherwise mysqlbinlog exits when the last log file has been transferred from the server.
--stop-never implies --to-last-log, so only the first log file to transfer need be named on the
command line.

--stop-never is commonly used with --raw to make a live binary log backup, but also can be used
without --raw to maintain a continuous text display of log events as the server generates them.

• --stop-never-slave-server-id=id

Command-Line Format

--stop-never-slave-server-id=#

Type

Default Value

Minimum Value

Numeric

65535

1

With --stop-never, mysqlbinlog reports a server ID of 65535 when it connects to the server.
--stop-never-slave-server-id explicitly specifies the server ID to report. It can be used to
avoid a conflict with the ID of a replica server or another mysqlbinlog process. See Section 4.6.7.4,
“Specifying the mysqlbinlog Server ID”.

• --stop-position=N

Command-Line Format

--stop-position=#

631

mysqlbinlog — Utility for Processing Binary Log Files

Type

Numeric

Stop reading the binary log at the first event having a position equal to or greater than N. This option
applies to the last log file named on the command line.

This option is useful for point-in-time recovery. See Section 7.5, “Point-in-Time (Incremental) Recovery”.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Introduced

Type

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

5.7.10

String

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL library
used to compile MySQL. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and
Ciphers”.

This option was added in MySQL 5.7.10.

• --to-last-log, -t

Command-Line Format

--to-last-log

Do not stop at the end of the requested binary log from a MySQL server, but rather continue printing
until the end of the last binary log. If you send the output to the same MySQL server, this may lead to an
endless loop. This option requires --read-from-remote-server.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use when connecting to a remote server.

• --verbose, -v

Command-Line Format

--verbose

Reconstruct row events and display them as commented SQL statements. If this option is given twice
(by passing in either "-vv" or "--verbose --verbose"), the output includes comments to indicate column
data types and some metadata, and row query log events if so configured.

For examples that show the effect of --base64-output and --verbose on row event output, see
Section 4.6.7.2, “mysqlbinlog Row Event Display”.

632

mysqlbinlog — Utility for Processing Binary Log Files

• --verify-binlog-checksum, -c

Command-Line Format

--verify-binlog-checksum

Verify checksums in binary log files.

• --version, -V

Command-Line Format

--version

Display version information and exit.

In MySQL 5.7, the version number shown by mysqlbinlog when using this option is 3.4.

You can pipe the output of mysqlbinlog into the mysql client to execute the events contained in the
binary log. This technique is used to recover from an unexpected exit when you have an old backup (see
Section 7.5, “Point-in-Time (Incremental) Recovery”). For example:

mysqlbinlog binlog.000001 | mysql -u root -p

Or:

mysqlbinlog binlog.[0-9]* | mysql -u root -p

If the statements produced by mysqlbinlog may contain BLOB values, these may cause problems when
mysql processes them. In this case, invoke mysql with the --binary-mode option.

You can also redirect the output of mysqlbinlog to a text file instead, if you need to modify the statement
log first (for example, to remove statements that you do not want to execute for some reason). After editing
the file, execute the statements that it contains by using it as input to the mysql program:

mysqlbinlog binlog.000001 > tmpfile
... edit tmpfile ...
mysql -u root -p < tmpfile

When mysqlbinlog is invoked with the --start-position option, it displays only those events with
an offset in the binary log greater than or equal to a given position (the given position must match the start
of one event). It also has options to stop and start when it sees an event with a given date and time. This
enables you to perform point-in-time recovery using the --stop-datetime option (to be able to say, for
example, “roll forward my databases to how they were today at 10:30 a.m.”).

Processing multiple files.
the safe method is to process them all using a single connection to the server. Here is an example that
demonstrates what may be unsafe:

 If you have more than one binary log to execute on the MySQL server,

mysqlbinlog binlog.000001 | mysql -u root -p # DANGER!!
mysqlbinlog binlog.000002 | mysql -u root -p # DANGER!!

Processing binary logs this way using multiple connections to the server causes problems if the first log file
contains a CREATE TEMPORARY TABLE statement and the second log contains a statement that uses the
temporary table. When the first mysql process terminates, the server drops the temporary table. When the
second mysql process attempts to use the table, the server reports “unknown table.”

To avoid problems like this, use a single mysql process to execute the contents of all binary logs that you
want to process. Here is one way to do so:

mysqlbinlog binlog.000001 binlog.000002 | mysql -u root -p

633

mysqlbinlog — Utility for Processing Binary Log Files

Another approach is to write all the logs to a single file and then process the file:

mysqlbinlog binlog.000001 >  /tmp/statements.sql
mysqlbinlog binlog.000002 >> /tmp/statements.sql
mysql -u root -p -e "source /tmp/statements.sql"

mysqlbinlog can produce output that reproduces a LOAD DATA operation without the original data file.
mysqlbinlog copies the data to a temporary file and writes a LOAD DATA LOCAL statement that refers
to the file. The default location of the directory where these files are written is system-specific. To specify a
directory explicitly, use the --local-load option.

Because mysqlbinlog converts LOAD DATA statements to LOAD DATA LOCAL statements (that is, it
adds LOCAL), both the client and the server that you use to process the statements must be configured
with the LOCAL capability enabled. See Section 6.1.6, “Security Considerations for LOAD DATA LOCAL”.

Warning

The temporary files created for LOAD DATA LOCAL statements are not
automatically deleted because they are needed until you actually execute those
statements. You should delete the temporary files yourself after you no longer need
the statement log. The files can be found in the temporary file directory and have
names like original_file_name-#-#.

4.6.7.1 mysqlbinlog Hex Dump Format

The --hexdump option causes mysqlbinlog to produce a hex dump of the binary log contents:

mysqlbinlog --hexdump master-bin.000001

The hex output consists of comment lines beginning with #, so the output might look like this for the
preceding command:

/*!40019 SET @@SESSION.max_insert_delayed_threads=0*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
# at 4
#051024 17:24:13 server id 1  end_log_pos 98
# Position  Timestamp   Type   Master ID        Size      Master Pos    Flags
# 00000004 9d fc 5c 43   0f   01 00 00 00   5e 00 00 00   62 00 00 00   00 00
# 00000017 04 00 35 2e 30 2e 31 35  2d 64 65 62 75 67 2d 6c |..5.0.15.debug.l|
# 00000027 6f 67 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |og..............|
# 00000037 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |................|
# 00000047 00 00 00 00 9d fc 5c 43  13 38 0d 00 08 00 12 00 |.......C.8......|
# 00000057 04 04 04 04 12 00 00 4b  00 04 1a                |.......K...|
#       Start: binlog v 4, server v 5.0.15-debug-log created 051024 17:24:13
#       at startup
ROLLBACK;

Hex dump output currently contains the elements in the following list. This format is subject to change. For
more information about binary log format, see MySQL Internals: The Binary Log.

• Position: The byte position within the log file.

• Timestamp: The event timestamp. In the example shown, '9d fc 5c 43' is the representation of

'051024 17:24:13' in hexadecimal.

• Type: The event type code.

• Master ID: The server ID of the replication source server that created the event.

• Size: The size in bytes of the event.

634

mysqlbinlog — Utility for Processing Binary Log Files

• Master Pos: The position of the next event in the original source log file.

• Flags: Event flag values.

4.6.7.2 mysqlbinlog Row Event Display

The following examples illustrate how mysqlbinlog displays row events that specify data
modifications. These correspond to events with the WRITE_ROWS_EVENT, UPDATE_ROWS_EVENT, and
DELETE_ROWS_EVENT type codes. The --base64-output=DECODE-ROWS and --verbose options may
be used to affect row event output.

Suppose that the server is using row-based binary logging and that you execute the following sequence of
statements:

CREATE TABLE t
(
  id   INT NOT NULL,
  name VARCHAR(20) NOT NULL,
  date DATE NULL
) ENGINE = InnoDB;

START TRANSACTION;
INSERT INTO t VALUES(1, 'apple', NULL);
UPDATE t SET name = 'pear', date = '2009-01-01' WHERE id = 1;
DELETE FROM t WHERE id = 1;
COMMIT;

By default, mysqlbinlog displays row events encoded as base-64 strings using BINLOG statements.
Omitting extraneous lines, the output for the row events produced by the preceding statement sequence
looks like this:

$> mysqlbinlog log_file
...
# at 218
#080828 15:03:08 server id 1  end_log_pos 258   Write_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAANoAAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBcBAAAAKAAAAAIBAAAQABEAAAAAAAEAA//8AQAAAAVhcHBsZQ==
'/*!*/;
...
# at 302
#080828 15:03:08 server id 1  end_log_pos 356   Update_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAAC4BAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBgBAAAANgAAAGQBAAAQABEAAAAAAAEAA////AEAAAAFYXBwbGX4AQAAAARwZWFyIbIP
'/*!*/;
...
# at 400
#080828 15:03:08 server id 1  end_log_pos 442   Delete_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAAJABAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBkBAAAAKgAAALoBAAAQABEAAAAAAAEAA//4AQAAAARwZWFyIbIP
'/*!*/;

To see the row events as comments in the form of “pseudo-SQL” statements, run mysqlbinlog with the
--verbose or -v option. The output contains lines beginning with ###:

$> mysqlbinlog -v log_file
...
# at 218
#080828 15:03:08 server id 1  end_log_pos 258   Write_rows: table id 17 flags: STMT_END_F

635

mysqlbinlog — Utility for Processing Binary Log Files

BINLOG '
fAS3SBMBAAAALAAAANoAAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBcBAAAAKAAAAAIBAAAQABEAAAAAAAEAA//8AQAAAAVhcHBsZQ==
'/*!*/;
### INSERT INTO test.t
### SET
###   @1=1
###   @2='apple'
###   @3=NULL
...
# at 302
#080828 15:03:08 server id 1  end_log_pos 356   Update_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAAC4BAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBgBAAAANgAAAGQBAAAQABEAAAAAAAEAA////AEAAAAFYXBwbGX4AQAAAARwZWFyIbIP
'/*!*/;
### UPDATE test.t
### WHERE
###   @1=1
###   @2='apple'
###   @3=NULL
### SET
###   @1=1
###   @2='pear'
###   @3='2009:01:01'
...
# at 400
#080828 15:03:08 server id 1  end_log_pos 442   Delete_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAAJABAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBkBAAAAKgAAALoBAAAQABEAAAAAAAEAA//4AQAAAARwZWFyIbIP
'/*!*/;
### DELETE FROM test.t
### WHERE
###   @1=1
###   @2='pear'
###   @3='2009:01:01'

Specify --verbose or -v twice to also display data types and some metadata for each column. The
output contains an additional comment following each column change:

$> mysqlbinlog -vv log_file
...
# at 218
#080828 15:03:08 server id 1  end_log_pos 258   Write_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAANoAAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBcBAAAAKAAAAAIBAAAQABEAAAAAAAEAA//8AQAAAAVhcHBsZQ==
'/*!*/;
### INSERT INTO test.t
### SET
###   @1=1 /* INT meta=0 nullable=0 is_null=0 */
###   @2='apple' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
###   @3=NULL /* VARSTRING(20) meta=0 nullable=1 is_null=1 */
...
# at 302
#080828 15:03:08 server id 1  end_log_pos 356   Update_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAAC4BAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBgBAAAANgAAAGQBAAAQABEAAAAAAAEAA////AEAAAAFYXBwbGX4AQAAAARwZWFyIbIP
'/*!*/;
### UPDATE test.t

636

mysqlbinlog — Utility for Processing Binary Log Files

### WHERE
###   @1=1 /* INT meta=0 nullable=0 is_null=0 */
###   @2='apple' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
###   @3=NULL /* VARSTRING(20) meta=0 nullable=1 is_null=1 */
### SET
###   @1=1 /* INT meta=0 nullable=0 is_null=0 */
###   @2='pear' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
###   @3='2009:01:01' /* DATE meta=0 nullable=1 is_null=0 */
...
# at 400
#080828 15:03:08 server id 1  end_log_pos 442   Delete_rows: table id 17 flags: STMT_END_F

BINLOG '
fAS3SBMBAAAALAAAAJABAAAAABEAAAAAAAAABHRlc3QAAXQAAwMPCgIUAAQ=
fAS3SBkBAAAAKgAAALoBAAAQABEAAAAAAAEAA//4AQAAAARwZWFyIbIP
'/*!*/;
### DELETE FROM test.t
### WHERE
###   @1=1 /* INT meta=0 nullable=0 is_null=0 */
###   @2='pear' /* VARSTRING(20) meta=20 nullable=0 is_null=0 */
###   @3='2009:01:01' /* DATE meta=0 nullable=1 is_null=0 */

You can tell mysqlbinlog to suppress the BINLOG statements for row events by using the --base64-
output=DECODE-ROWS option. This is similar to --base64-output=NEVER but does not exit with an
error if a row event is found. The combination of --base64-output=DECODE-ROWS and --verbose
provides a convenient way to see row events only as SQL statements:

$> mysqlbinlog -v --base64-output=DECODE-ROWS log_file
...
# at 218
#080828 15:03:08 server id 1  end_log_pos 258   Write_rows: table id 17 flags: STMT_END_F
### INSERT INTO test.t
### SET
###   @1=1
###   @2='apple'
###   @3=NULL
...
# at 302
#080828 15:03:08 server id 1  end_log_pos 356   Update_rows: table id 17 flags: STMT_END_F
### UPDATE test.t
### WHERE
###   @1=1
###   @2='apple'
###   @3=NULL
### SET
###   @1=1
###   @2='pear'
###   @3='2009:01:01'
...
# at 400
#080828 15:03:08 server id 1  end_log_pos 442   Delete_rows: table id 17 flags: STMT_END_F
### DELETE FROM test.t
### WHERE
###   @1=1
###   @2='pear'
###   @3='2009:01:01'

Note

You should not suppress BINLOG statements if you intend to re-execute
mysqlbinlog output.

The SQL statements produced by --verbose for row events are much more readable than the
corresponding BINLOG statements. However, they do not correspond exactly to the original SQL
statements that generated the events. The following limitations apply:

637

mysqlbinlog — Utility for Processing Binary Log Files

• The original column names are lost and replaced by @N, where N is a column number.

• Character set information is not available in the binary log, which affects string column display:

• There is no distinction made between corresponding binary and nonbinary string types (BINARY and
CHAR, VARBINARY and VARCHAR, BLOB and TEXT). The output uses a data type of STRING for fixed-
length strings and VARSTRING for variable-length strings.

• For multibyte character sets, the maximum number of bytes per character is not present in the

binary log, so the length for string types is displayed in bytes rather than in characters. For example,
STRING(4) is used as the data type for values from either of these column types:

CHAR(4) CHARACTER SET latin1
CHAR(2) CHARACTER SET ucs2

• Due to the storage format for events of type UPDATE_ROWS_EVENT, UPDATE statements are displayed

with the WHERE clause preceding the SET clause.

Proper interpretation of row events requires the information from the format description event at the
beginning of the binary log. Because mysqlbinlog does not know in advance whether the rest of the log
contains row events, by default it displays the format description event using a BINLOG statement in the
initial part of the output.

If the binary log is known not to contain any events requiring a BINLOG statement (that is, no row events),
the --base64-output=NEVER option can be used to prevent this header from being written.

4.6.7.3 Using mysqlbinlog to Back Up Binary Log Files

By default, mysqlbinlog reads binary log files and displays their contents in text format. This enables you
to examine events within the files more easily and to re-execute them (for example, by using the output as
input to mysql). mysqlbinlog can read log files directly from the local file system, or, with the --read-
from-remote-server option, it can connect to a server and request binary log contents from that server.
mysqlbinlog writes text output to its standard output, or to the file named as the value of the --result-
file=file_name option if that option is given.

• mysqlbinlog Backup Capabilities

• mysqlbinlog Backup Options

• Static and Live Backups

• Output File Naming

• Example: mysqldump + mysqlbinlog for Backup and Restore

• mysqlbinlog Backup Restrictions

mysqlbinlog Backup Capabilities

mysqlbinlog can read binary log files and write new files containing the same content—that is, in binary
format rather than text format. This capability enables you to easily back up a binary log in its original
format. mysqlbinlog can make a static backup, backing up a set of log files and stopping when the end
of the last file is reached. It can also make a continuous (“live”) backup, staying connected to the server
when it reaches the end of the last log file and continuing to copy new events as they are generated. In
continuous-backup operation, mysqlbinlog runs until the connection ends (for example, when the server
exits) or mysqlbinlog is forcibly terminated. When the connection ends, mysqlbinlog does not wait
and retry the connection, unlike a replica server. To continue a live backup after the server has been
restarted, you must also restart mysqlbinlog.

638

mysqlbinlog — Utility for Processing Binary Log Files

mysqlbinlog Backup Options

Binary log backup requires that you invoke mysqlbinlog with two options at minimum:

• The --read-from-remote-server (or -R) option tells mysqlbinlog to connect to a server and
request its binary log. (This is similar to a replica server connecting to its replication source server.)

• The --raw option tells mysqlbinlog to write raw (binary) output, not text output.

Along with --read-from-remote-server, it is common to specify other options: --host indicates
where the server is running, and you may also need to specify connection options such as --user and --
password.

Several other options are useful in conjunction with --raw:

• --stop-never: Stay connected to the server after reaching the end of the last log file and continue to

read new events.

• --stop-never-slave-server-id=id: The server ID that mysqlbinlog reports to the server

when --stop-never is used. The default is 65535. This can be used to avoid a conflict with the ID of
a replica server or another mysqlbinlog process. See Section 4.6.7.4, “Specifying the mysqlbinlog
Server ID”.

• --result-file: A prefix for output file names, as described later.

Static and Live Backups

To back up a server's binary log files with mysqlbinlog, you must specify file names that actually exist
on the server. If you do not know the names, connect to the server and use the SHOW BINARY LOGS
statement to see the current names. Suppose that the statement produces this output:

mysql> SHOW BINARY LOGS;
+---------------+-----------+
| Log_name      | File_size |
+---------------+-----------+
| binlog.000130 |     27459 |
| binlog.000131 |     13719 |
| binlog.000132 |     43268 |
+---------------+-----------+

With that information, you can use mysqlbinlog to back up the binary log to the current directory as
follows (enter each command on a single line):

• To make a static backup of binlog.000130 through binlog.000132, use either of these commands:

mysqlbinlog --read-from-remote-server --host=host_name --raw
  binlog.000130 binlog.000131 binlog.000132

mysqlbinlog --read-from-remote-server --host=host_name --raw
  --to-last-log binlog.000130

The first command specifies every file name explicitly. The second names only the first file and uses
--to-last-log to read through the last. A difference between these commands is that if the server
happens to open binlog.000133 before mysqlbinlog reaches the end of binlog.000132, the first
command does not read it, but the second command does.

• To make a live backup in which mysqlbinlog starts with binlog.000130 to copy existing log files,

then stays connected to copy new events as the server generates them:

mysqlbinlog --read-from-remote-server --host=host_name --raw
  --stop-never binlog.000130

639

mysqlbinlog — Utility for Processing Binary Log Files

With --stop-never, it is not necessary to specify --to-last-log to read to the last log file because
that option is implied.

Output File Naming

Without --raw, mysqlbinlog produces text output and the --result-file option, if given, specifies
the name of the single file to which all output is written. With --raw, mysqlbinlog writes one binary
output file for each log file transferred from the server. By default, mysqlbinlog writes the files in the
current directory with the same names as the original log files. To modify the output file names, use the --
result-file option. In conjunction with --raw, the --result-file option value is treated as a prefix
that modifies the output file names.

Suppose that a server currently has binary log files named binlog.000999 and up. If you use
mysqlbinlog --raw to back up the files, the --result-file option produces output file names as
shown in the following table. You can write the files to a specific directory by beginning the --result-
file value with the directory path. If the --result-file value consists only of a directory name, the
value must end with the pathname separator character. Output files are overwritten if they exist.

--result-file Option

--result-file=x

--result-file=/tmp/

--result-file=/tmp/x

Output File Names

xbinlog.000999 and up

/tmp/binlog.000999 and up

/tmp/xbinlog.000999 and up

Example: mysqldump + mysqlbinlog for Backup and Restore

The following example describes a simple scenario that shows how to use mysqldump and mysqlbinlog
together to back up a server's data and binary log, and how to use the backup to restore the server if data
loss occurs. The example assumes that the server is running on host host_name and its first binary log
file is named binlog.000999. Enter each command on a single line.

Use mysqlbinlog to make a continuous backup of the binary log:

mysqlbinlog --read-from-remote-server --host=host_name --raw
  --stop-never binlog.000999

Use mysqldump to create a dump file as a snapshot of the server's data. Use --all-databases, --
events, and --routines to back up all data, and --master-data=2 to include the current binary log
coordinates in the dump file.

mysqldump --host=host_name --all-databases --events --routines --master-data=2> dump_file

Execute the mysqldump command periodically to create newer snapshots as desired.

If data loss occurs (for example, if the server unexpectedly exits), use the most recent dump file to restore
the data:

mysql --host=host_name -u root -p < dump_file

Then use the binary log backup to re-execute events that were written after the coordinates listed in the
dump file. Suppose that the coordinates in the file look like this:

-- CHANGE MASTER TO MASTER_LOG_FILE='binlog.001002', MASTER_LOG_POS=27284;

If the most recent backed-up log file is named binlog.001004, re-execute the log events like this:

mysqlbinlog --start-position=27284 binlog.001002 binlog.001003 binlog.001004
  | mysql --host=host_name -u root -p

640

mysqldumpslow — Summarize Slow Query Log Files

You might find it easier to copy the backup files (dump file and binary log files) to the server host to make it
easier to perform the restore operation, or if MySQL does not allow remote root access.

mysqlbinlog Backup Restrictions

Binary log backups with mysqlbinlog are subject to these restrictions:

• mysqlbinlog does not automatically reconnect to the MySQL server if the connection is lost (for

example, if a server restart occurs or there is a network outage).

• Prior to MySQL 5.7.19, mysqlbinlog does not get all events as they are committed, even if the server
is configured with sync_binlog=1. This means that some of the most recent events may be missing.
To ensure that mysqlbinlog sees the most recent events, flush the binary log on the server that you
are backing up.

• The delay for a backup is similar to the delay for a replica server.

4.6.7.4 Specifying the mysqlbinlog Server ID

When invoked with the --read-from-remote-server option, mysqlbinlog connects to a MySQL
server, specifies a server ID to identify itself, and requests binary log files from the server. You can use
mysqlbinlog to request log files from a server in several ways:

• Specify an explicitly named set of files: For each file, mysqlbinlog connects and issues a Binlog

dump command. The server sends the file and disconnects. There is one connection per file.

• Specify the beginning file and --to-last-log: mysqlbinlog connects and issues a Binlog dump

command for all files. The server sends all files and disconnects.

• Specify the beginning file and --stop-never (which implies --to-last-log): mysqlbinlog

connects and issues a Binlog dump command for all files. The server sends all files, but does not
disconnect after sending the last one.

With --read-from-remote-server only, mysqlbinlog connects using a server ID of 0, which tells
the server to disconnect after sending the last requested log file.

With --read-from-remote-server and --stop-never, mysqlbinlog connects using a nonzero
server ID, so the server does not disconnect after sending the last log file. The server ID is 65535 by
default, but this can be changed with --stop-never-slave-server-id.

Thus, for the first two ways of requesting files, the server disconnects because mysqlbinlog specifies
a server ID of 0. It does not disconnect if --stop-never is given because mysqlbinlog specifies a
nonzero server ID.

4.6.8 mysqldumpslow — Summarize Slow Query Log Files

The MySQL slow query log contains information about queries that take a long time to execute (see
Section 5.4.5, “The Slow Query Log”). mysqldumpslow parses MySQL slow query log files and
summarizes their contents.

Normally, mysqldumpslow groups queries that are similar except for the particular values of number and
string data values. It “abstracts” these values to N and 'S' when displaying summary output. To modify
value abstracting behavior, use the -a and -n options.

Invoke mysqldumpslow like this:

mysqldumpslow [options] [log_file ...]

641

mysqldumpslow — Summarize Slow Query Log Files

Example output with no options given:

Reading mysql slow query log from /usr/local/mysql/data/mysqld57-slow.log
Count: 1  Time=4.32s (4s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1

Count: 3  Time=2.53s (7s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1 limit N

Count: 3  Time=2.13s (6s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t1 select * from t1

mysqldumpslow supports the following options.

Table 4.24 mysqldumpslow Options

Option Name

Description

-a

-n

--debug

-g

--help

-h

-i

-l

-r

-s

-t

--verbose

• --help

Do not abstract all numbers to N and strings to 'S'

Abstract numbers with at least the specified digits

Write debugging information

Only consider statements that match the pattern

Display help message and exit

Host name of the server in the log file name

Name of the server instance

Do not subtract lock time from total time

Reverse the sort order

How to sort output

Display only first num queries

Verbose mode

Command-Line Format

--help

Display a help message and exit.

• -a

Do not abstract all numbers to N and strings to 'S'.

• --debug, -d

Command-Line Format

--debug

Run in debug mode.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries provided
by Oracle are not built using this option.

• -g pattern

Type

String

642

mysqldumpslow — Summarize Slow Query Log Files

Consider only queries that match the (grep-style) pattern.

• -h host_name

Type

Default Value

String

*

Host name of MySQL server for *-slow.log file name. The value can contain a wildcard. The default is
* (match all).

• -i name

Type

String

Name of server instance (if using mysql.server startup script).

• -l

Do not subtract lock time from total time.

• -n N

Type

Abstract numbers with at least N digits within names.

• -r

Reverse the sort order.

• -s sort_type

Type

Default Value

Numeric

String

at

How to sort the output. The value of sort_type should be chosen from the following list:

• t, at: Sort by query time or average query time

• l, al: Sort by lock time or average lock time

• r, ar: Sort by rows sent or average rows sent

• c: Sort by count

By default, mysqldumpslow sorts by average query time (equivalent to -s at).

• -t N

Type

Numeric

643

Program Development Utilities

Display only the first N queries in the output.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does.

4.7 Program Development Utilities

This section describes some utilities that you may find useful when developing MySQL programs.

In shell scripts, you can use the my_print_defaults program to parse option files and see what options
would be used by a given program. The following example shows the output that my_print_defaults
might produce when asked to show the options found in the [client] and [mysql] groups:

$> my_print_defaults client mysql
--port=3306
--socket=/tmp/mysql.sock
--no-auto-rehash

Note for developers: Option file handling is implemented in the C client library simply by processing all
options in the appropriate group or groups before any command-line arguments. This works well for
programs that use the last instance of an option that is specified multiple times. If you have a C or C++
program that handles multiply specified options this way but that does not read option files, you need add
only two lines to give it that capability. Check the source code of any of the standard MySQL clients to see
how to do this.

Several other language interfaces to MySQL are based on the C client library, and some of them provide a
way to access option file contents. These include Perl and Python. For details, see the documentation for
your preferred interface.

4.7.1 mysql_config — Display Options for Compiling Clients

mysql_config provides you with useful information for compiling your MySQL client and connecting it to
MySQL. It is a shell script, so it is available only on Unix and Unix-like systems.

Note

As of MySQL 5.7.9, pkg-config can be used as an alternative to mysql_config
for obtaining information such as compiler flags or link libraries required to compile
MySQL applications. For more information, see Building C API Client Programs
Using pkg-config.

Note

As of MySQL 5.7.4, for binary distributions for Solaris, mysql_config does not
provide arguments for linking with the embedded library. To get linking arguments
for the embedded library, use the mysql_server_config script instead.

mysql_config supports the following options.

• --cflags

C Compiler flags to find include files and critical compiler flags and defines used when compiling the
libmysqlclient library. The options returned are tied to the specific compiler that was used when the

644

mysql_config — Display Options for Compiling Clients

library was created and might clash with the settings for your own compiler. Use --include for more
portable options that contain only include paths.

• --cxxflags

Like --cflags, but for C++ compiler flags.

• --include

Compiler options to find MySQL include files.

• --libmysqld-libs, --embedded-libs, --embedded

Libraries and options required to link with libmysqld, the MySQL embedded server.

Note

The libmysqld embedded server library is deprecated as of MySQL 5.7.19 and
has been removed in MySQL 8.0.

• --libs

Libraries and options required to link with the MySQL client library.

• --libs_r

Libraries and options required to link with the thread-safe MySQL client library. In MySQL 5.7, all client
libraries are thread-safe, so this option need not be used. The --libs option can be used in all cases.

• --plugindir

The default plugin directory path name, defined when configuring MySQL.

• --port

The default TCP/IP port number, defined when configuring MySQL.

• --socket

The default Unix socket file, defined when configuring MySQL.

• --variable=var_name

Display the value of the named configuration variable. Permitted var_name values are pkgincludedir
(the header file directory), pkglibdir (the library directory), and plugindir (the plugin directory).

• --version

Version number for the MySQL distribution.

If you invoke mysql_config with no options, it displays a list of all options that it supports, and their
values:

$> mysql_config
Usage: /usr/local/mysql/bin/mysql_config [options]
Options:
  --cflags         [-I/usr/local/mysql/include/mysql -mcpu=pentiumpro]
  --cxxflags       [-I/usr/local/mysql/include/mysql -mcpu=pentiumpro]
  --include        [-I/usr/local/mysql/include/mysql]
  --libs           [-L/usr/local/mysql/lib/mysql -lmysqlclient
                    -lpthread -lm -lrt -lssl -lcrypto -ldl]

645

my_print_defaults — Display Options from Option Files

  --libs_r         [-L/usr/local/mysql/lib/mysql -lmysqlclient_r
                    -lpthread -lm -lrt -lssl -lcrypto -ldl]
  --plugindir      [/usr/local/mysql/lib/plugin]
  --socket         [/tmp/mysql.sock]
  --port           [3306]
  --version        [5.7.9]
  --libmysqld-libs [-L/usr/local/mysql/lib/mysql -lmysqld
                    -lpthread -lm -lrt -lssl -lcrypto -ldl -lcrypt]
  --variable=VAR   VAR is one of:
          pkgincludedir [/usr/local/mysql/include]
          pkglibdir     [/usr/local/mysql/lib]
          plugindir     [/usr/local/mysql/lib/plugin]

You can use mysql_config within a command line using backticks to include the output that it produces
for particular options. For example, to compile and link a MySQL client program, use mysql_config as
follows:

gcc -c `mysql_config --cflags` progname.c
gcc -o progname progname.o `mysql_config --libs`

4.7.2 my_print_defaults — Display Options from Option Files

my_print_defaults displays the options that are present in option groups of option files. The output
indicates what options are used by programs that read the specified option groups. For example, the
mysqlcheck program reads the [mysqlcheck] and [client] option groups. To see what options are
present in those groups in the standard option files, invoke my_print_defaults like this:

$> my_print_defaults mysqlcheck client
--user=myusername
--password=password
--host=localhost

The output consists of options, one per line, in the form that they would be specified on the command line.

my_print_defaults supports the following options.

• --help, -?

Display a help message and exit.

• --config-file=file_name, --defaults-file=file_name, -c file_name

Read only the given option file.

• --debug=debug_options, -# debug_options

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is d:t:o,/
tmp/my_print_defaults.trace.

• --defaults-extra-file=file_name, --extra-file=file_name, -e file_name

Read this option file after the global option file but (on Unix) before the user option file.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=suffix, -g suffix

In addition to the groups named on the command line, read groups that have the given suffix.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

646

resolve_stack_dump — Resolve Numeric Stack Trace Dump to Symbols

• --login-path=name, -l name

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 4.6.6, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --no-defaults, -n

Return an empty string.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --show, -s

As of MySQL 5.7.8, my_print_defaults masks passwords by default. Use this option to display
passwords in cleartext.

• --verbose, -v

Verbose mode. Print more information about what the program does.

• --version, -V

Display version information and exit.

4.7.3 resolve_stack_dump — Resolve Numeric Stack Trace Dump to Symbols

resolve_stack_dump resolves a numeric stack dump to symbols.

Note

resolve_stack_dump is deprecated and is removed in MySQL 8.0. Stack traces
from official MySQL builds are always symbolized, so there is no need to use
resolve_stack_dump.

Invoke resolve_stack_dump like this:

resolve_stack_dump [options] symbols_file [numeric_dump_file]

The symbols file should include the output from the nm --numeric-sort mysqld command. The
numeric dump file should contain a numeric stack track from mysqld. If no numeric dump file is named on
the command line, the stack trace is read from the standard input.

resolve_stack_dump supports the following options.

• --help, -h

Display a help message and exit.

• --numeric-dump-file=file_name, -n file_name

Read the stack trace from the given file.

• --symbols-file=file_name, -s file_name

647

Miscellaneous Programs

Use the given symbols file.

• --version, -V

Display version information and exit.

For more information, see Section 5.8.1.5, “Using a Stack Trace”.

4.8 Miscellaneous Programs

4.8.1 lz4_decompress — Decompress mysqlpump LZ4-Compressed Output

The lz4_decompress utility decompresses mysqlpump output that was created using LZ4 compression.
lz4_decompress was added in MySQL 5.7.10.

Invoke lz4_decompress like this:

lz4_decompress input_file output_file

Example:

mysqlpump --compress-output=LZ4 > dump.lz4
lz4_decompress dump.lz4 dump.txt

To see a help message, invoke lz4_decompress with no arguments.

To decompress mysqlpump ZLIB-compressed output, use zlib_decompress. See Section 4.8.5,
“zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output”.

4.8.2 perror — Display MySQL Error Message Information

For most system errors, MySQL displays, in addition to an internal text message, the system error code in
one of the following styles:

message ... (errno: #)
message ... (Errcode: #)

You can find out what the error code means by examining the documentation for your system or by using
the perror utility.

perror prints a description for a system error code or for a storage engine (table handler) error code.

Invoke perror like this:

perror [options] errorcode ...

Examples:

$> perror 1231
MySQL error code 1231 (ER_WRONG_VALUE_FOR_VAR): Variable '%-.64s' can't
be set to the value of '%-.200s'

$> perror 13 64
OS error code  13:  Permission denied
OS error code  64:  Machine is not on the network

To obtain the error message for a MySQL Cluster error code, use the ndb_perror utility.

The meaning of system error messages may be dependent on your operating system. A given error code
may mean different things on different operating systems.

perror supports the following options.

648

replace — A String-Replacement Utility

• --help, --info, -I, -?

Display a help message and exit.

• --ndb

Print the error message for an NDB Cluster error code.

This option is deprecated in NDB 7.6.4 and later, where perror prints a warning if it is used, and is
removed in NDB Cluster 8.0. Use the ndb_perror utility instead.

• --silent, -s

Silent mode. Print only the error message.

• --verbose, -v

Verbose mode. Print error code and message. This is the default behavior.

• --version, -V

Display version information and exit.

4.8.3 replace — A String-Replacement Utility

The replace utility program changes strings in place in files or on the standard input.

Note

The replace utility is deprecated as of MySQL 5.7.18 and is removed in MySQL
8.0.

Invoke replace in one of the following ways:

replace from to [from to] ... -- file_name [file_name] ...
replace from to [from to] ... < file_name

from represents a string to look for and to represents its replacement. There can be one or more pairs of
strings.

Use the -- option to indicate where the string-replacement list ends and the file names begin. In this case,
any file named on the command line is modified in place, so you may want to make a copy of the original
before converting it. replace prints a message indicating which of the input files it actually modifies.

If the -- option is not given, replace reads the standard input and writes to the standard output.

replace uses a finite state machine to match longer strings first. It can be used to swap strings. For
example, the following command swaps a and b in the given files, file1 and file2:

replace a b b a -- file1 file2 ...

replace supports the following options.

• -?, -I

Display a help message and exit.

• -#debug_options

Enable debugging.

649

resolveip — Resolve Host name to IP Address or Vice Versa

• -s

Silent mode. Print less information what the program does.

• -v

Verbose mode. Print more information about what the program does.

• -V

Display version information and exit.

4.8.4 resolveip — Resolve Host name to IP Address or Vice Versa

The resolveip utility resolves host names to IP addresses and vice versa.

Note

resolveip is deprecated and is removed in MySQL 8.0. nslookup, host, or dig
can be used instead.

Invoke resolveip like this:

resolveip [options] {host_name|ip-addr} ...

resolveip supports the following options.

• --help, --info, -?, -I

Display a help message and exit.

• --silent, -s

Silent mode. Produce less output.

• --version, -V

Display version information and exit.

4.8.5 zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output

The zlib_decompress utility decompresses mysqlpump output that was created using ZLIB
compression. zlib_decompress was added in MySQL 5.7.10.

Invoke zlib_decompress like this:

zlib_decompress input_file output_file

Example:

mysqlpump --compress-output=ZLIB > dump.zlib
zlib_decompress dump.zlib dump.txt

To see a help message, invoke zlib_decompress with no arguments.

To decompress mysqlpump LZ4-compressed output, use lz4_decompress. See Section 4.8.1,
“lz4_decompress — Decompress mysqlpump LZ4-Compressed Output”.

4.9 Environment Variables

650

Environment Variables

This section lists environment variables that are used directly or indirectly by MySQL. Most of these can
also be found in other places in this manual.

Options on the command line take precedence over values specified in option files and environment
variables, and values in option files take precedence over values in environment variables. In many cases,
it is preferable to use an option file instead of environment variables to modify the behavior of MySQL. See
Section 4.2.2.2, “Using Option Files”.

Variable

Description

AUTHENTICATION_LDAP_CLIENT_LOG

Client-side LDAP authentication logging level.

AUTHENTICATION_PAM_LOG

PAM authentication plugin debug logging settings.

CC

CXX

CC

DBI_USER

DBI_TRACE

HOME

LD_RUN_PATH

LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN

LIBMYSQL_PLUGIN_DIR

LIBMYSQL_PLUGINS

MYSQL_DEBUG

MYSQL_GROUP_SUFFIX

MYSQL_HISTFILE

MYSQL_HISTIGNORE

MYSQL_HOME

MYSQL_HOST

MYSQL_OPENSSL_UDF_DH_BITS_THRESHOLD

MYSQL_OPENSSL_UDF_DSA_BITS_THRESHOLD

The name of your C compiler (for running CMake).

The name of your C++ compiler (for running
CMake).

The name of your C compiler (for running CMake).

The default user name for Perl DBI.

Trace options for Perl DBI.

The default path for the mysql history file is
$HOME/.mysql_history.

Used to specify the location of
libmysqlclient.so.

Enable mysql_clear_password authentication
plugin; see Section 6.4.1.6, “Client-Side Cleartext
Pluggable Authentication”.

Directory in which to look for client plugins.

Client plugins to preload.

Debug trace options when debugging.

Option group suffix value (like specifying --
defaults-group-suffix).

The path to the mysql history file. If this
variable is set, its value overrides the default for
$HOME/.mysql_history.

Patterns specifying statements that mysql should
not log to $HOME/.mysql_history, or syslog if
--syslog is given.

The path to the directory in which the server-specific
my.cnf file resides.

The default host name used by the mysql
command-line client.

Maximum key length for
create_dh_parameters(). See Section 6.6.2,
“MySQL Enterprise Encryption Usage and
Examples”.

Maximum DSA key length for
create_asymmetric_priv_key(). See
Section 6.6.2, “MySQL Enterprise Encryption Usage
and Examples”.

651

Environment Variables

Variable

Description

MYSQL_OPENSSL_UDF_RSA_BITS_THRESHOLD

MYSQL_PS1

MYSQL_PWD

MYSQL_TCP_PORT

MYSQL_TEST_LOGIN_FILE

MYSQL_TEST_TRACE_CRASH

MYSQL_TEST_TRACE_DEBUG

MYSQL_UNIX_PORT

MYSQLX_TCP_PORT

MYSQLX_UNIX_PORT

PATH

PKG_CONFIG_PATH

TMPDIR

TZ

UMASK

UMASK_DIR

USER

Maximum RSA key length for
create_asymmetric_priv_key(). See
Section 6.6.2, “MySQL Enterprise Encryption Usage
and Examples”.

The command prompt to use in the mysql
command-line client.

The default password when connecting to mysqld.
Using this is insecure. See Section 6.1.2.1, “End-
User Guidelines for Password Security”.

The default TCP/IP port number.

The name of the .mylogin.cnf login path file.

Whether the test protocol trace plugin crashes
clients. See note following table.

Whether the test protocol trace plugin produces
output. See note following table.

The default Unix socket file name; used for
connections to localhost.

The X Plugin default TCP/IP port number.

The X Plugin default Unix socket file name; used for
connections to localhost.

Used by the shell to find MySQL programs.

Location of mysqlclient.pc pkg-config file.
See note following table.

The directory in which temporary files are created.

This should be set to your local time zone. See
Section B.3.3.7, “Time Zone Problems”.

The user-file creation mode when creating files. See
note following table.

The user-directory creation mode when creating
directories. See note following table.

The default user name on Windows when
connecting to mysqld.

For information about the mysql history file, see Section 4.5.1.3, “mysql Client Logging”.

MYSQL_TEST_LOGIN_FILE is the path name of the login path file (the file created by
mysql_config_editor). If not set, the default value is %APPDATA%\MySQL\.mylogin.cnf
directory on Windows and $HOME/.mylogin.cnf on non-Windows systems. See Section 4.6.6,
“mysql_config_editor — MySQL Configuration Utility”.

The MYSQL_TEST_TRACE_DEBUG and MYSQL_TEST_TRACE_CRASH variables control the test protocol
trace client plugin, if MySQL is built with that plugin enabled. For more information, see Using the Test
Protocol Trace Plugin.

The default UMASK and UMASK_DIR values are 0640 and 0750, respectively. MySQL assumes that the
value for UMASK or UMASK_DIR is in octal if it starts with a zero. For example, setting UMASK=0600 is
equivalent to UMASK=384 because 0600 octal is 384 decimal.

652

Unix Signal Handling in MySQL

The UMASK and UMASK_DIR variables, despite their names, are used as modes, not masks:

• If UMASK is set, mysqld uses ($UMASK | 0600) as the mode for file creation, so that newly created

files have a mode in the range from 0600 to 0666 (all values octal).

• If UMASK_DIR is set, mysqld uses ($UMASK_DIR | 0700) as the base mode for directory creation,

which then is AND-ed with ~(~$UMASK & 0666), so that newly created directories have a mode in the
range from 0700 to 0777 (all values octal). The AND operation may remove read and write permissions
from the directory mode, but not execute permissions.

See also Section B.3.3.1, “Problems with File Permissions”.

It may be necessary to set PKG_CONFIG_PATH if you use pkg-config for building MySQL programs.
See Building C API Client Programs Using pkg-config.

4.10 Unix Signal Handling in MySQL

On Unix and Unix-like systems, a process can be the recipient of signals sent to it by the root system
account or the system account that owns the process. Signals can be sent using the kill command.
Some command interpreters associate certain key sequences with signals, such as Control+C to send a
SIGINT signal. This section describes how the MySQL server and client programs respond to signals.

• Server Response to Signals

• Client Response to Signals

Server Response to Signals

mysqld responds to signals as follows:

• SIGTERM causes the server to shut down. This is like executing a SHUTDOWN statement without having
to connect to the server (which for shutdown requires an account that has the SHUTDOWN privilege).

• SIGHUP causes the server to reload the grant tables and to flush tables, logs, the thread cache, and the
host cache. These actions are like various forms of the FLUSH statement. Sending the signal enables
the flush operations to be performed without having to connect to the server, which requires a MySQL
account that has privileges sufficient for those operations. The server also writes a status report to the
error log that has this format:

Status information:

Current dir: /var/mysql/data/
Running threads: 4  Stack size: 262144
Current locks:
lock: 0x7f742c02c0e0:

lock: 0x2cee2a20:
:
lock: 0x207a080:

Key caches:
default
Buffer_size:       8388608
Block_size:           1024
Division_limit:        100
Age_limit:             300
blocks used:             4
not flushed:             0
w_requests:              0
writes:                  0
r_requests:              8

653

Server Response to Signals

reads:                   4

handler status:
read_key:           13
read_next:           4
read_rnd             0
read_first:         13
write:               1
delete               0
update:              0

Table status:
Opened tables:        121
Open tables:          114
Open files:            18
Open streams:           0

Memory status:
<malloc version="1">
<heap nr="0">
<sizes>
  <size from="17" to="32" total="32" count="1"/>
  <size from="33" to="48" total="96" count="2"/>
  <size from="33" to="33" total="33" count="1"/>
  <size from="97" to="97" total="6014" count="62"/>
  <size from="113" to="113" total="904" count="8"/>
  <size from="193" to="193" total="193" count="1"/>
  <size from="241" to="241" total="241" count="1"/>
  <size from="609" to="609" total="609" count="1"/>
  <size from="16369" to="16369" total="49107" count="3"/>
  <size from="24529" to="24529" total="98116" count="4"/>
  <size from="32689" to="32689" total="32689" count="1"/>
  <unsorted from="241" to="7505" total="7746" count="2"/>
</sizes>
<total type="fast" count="3" size="128"/>
<total type="rest" count="84" size="195652"/>
<system type="current" size="690774016"/>
<system type="max" size="690774016"/>
<aspace type="total" size="690774016"/>
<aspace type="mprotect" size="690774016"/>
</heap>
:
<total type="fast" count="85" size="5520"/>
<total type="rest" count="116" size="316820"/>
<total type="mmap" count="82" size="939954176"/>
<system type="current" size="695717888"/>
<system type="max" size="695717888"/>
<aspace type="total" size="695717888"/>
<aspace type="mprotect" size="695717888"/>
</malloc>

Events status:
LLA = Last Locked At  LUA = Last Unlocked At
WOC = Waiting On Condition  DL = Data Locked

Event scheduler status:
State      : INITIALIZED
Thread id  : 0
LLA        : n/a:0
LUA        : n/a:0
WOC        : NO
Workers    : 0
Executed   : 0
Data locked: NO

Event queue status:
Element count   : 0

654

Client Response to Signals

Data locked     : NO
Attempting lock : NO
LLA             : init_queue:95
LUA             : init_queue:103
WOC             : NO
Next activation : never

• SIGINT normally is ignored by the server. Starting the server with the --gdb option installs an interrupt

handler for SIGINT for debugging purposes. See Section 5.8.1.4, “Debugging mysqld under gdb”.

Client Response to Signals

MySQL client programs respond to signals as follows:

• The mysql client interprets SIGINT (typically the result of typing Control+C) as instruction to interrupt
the current statement if there is one, or to cancel any partial input line otherwise. This behavior can be
disabled using the --sigint-ignore option to ignore SIGINT signals.

• Client programs that use the MySQL client library block SIGPIPE signals by default. These variations

are possible:

• Client can install their own SIGPIPE handler to override the default behavior. See Writing C API

Threaded Client Programs.

• Clients can prevent installation of SIGPIPE handlers by specifying the CLIENT_IGNORE_SIGPIPE

option to mysql_real_connect() at connect time. See mysql_real_connect().

655

656

