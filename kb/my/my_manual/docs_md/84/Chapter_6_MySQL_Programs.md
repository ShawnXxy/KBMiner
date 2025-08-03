Overview of MySQL Programs

6.1 Overview of MySQL Programs

There are many different programs in a MySQL installation. This section provides a brief overview
of them. Later sections provide a more detailed description of each one, with the exception of NDB
Cluster programs. Each program's description indicates its invocation syntax and the options that it
supports. Section 25.5, “NDB Cluster Programs”, describes programs specific to NDB Cluster.

Most MySQL distributions include all of these programs, except for those programs that are platform-
specific. (For example, the server startup scripts are not used on Windows.) The exception is that
RPM distributions are more specialized. There is one RPM for the server, another for client programs,
and so forth. If you appear to be missing one or more programs, see Chapter 2, Installing MySQL, for
information on types of distributions and what they contain. It may be that you have a distribution that
does not include all programs and you need to install an additional package.

Each MySQL program takes many different options. Most programs provide a --help option that you
can use to get a description of the program's different options. For example, try mysql --help.

You can override default option values for MySQL programs by specifying options on the command
line or in an option file. See Section 6.2, “Using MySQL Programs”, for general information on invoking
programs and specifying program options.

The MySQL server, mysqld, is the main program that does most of the work in a MySQL installation.
The server is accompanied by several related scripts that assist you in starting and stopping the server:

•  mysqld

The SQL daemon (that is, the MySQL server). To use client programs, mysqld must be running,
because clients gain access to databases by connecting to the server. See Section 6.3.1, “mysqld —
The MySQL Server”.

•  mysqld_safe

A server startup script. mysqld_safe attempts to start mysqld. See Section 6.3.2, “mysqld_safe —
MySQL Server Startup Script”.

•  mysql.server

A server startup script. This script is used on systems that use System V-style run directories
containing scripts that start system services for particular run levels. It invokes mysqld_safe to start
the MySQL server. See Section 6.3.3, “mysql.server — MySQL Server Startup Script”.

•  mysqld_multi

A server startup script that can start or stop multiple servers installed on the system. See
Section 6.3.4, “mysqld_multi — Manage Multiple MySQL Servers”.

Several programs perform setup operations during MySQL installation or upgrading:

•  comp_err

This program is used during the MySQL build/installation process. It compiles error message files
from the error source files. See Section 6.4.1, “comp_err — Compile MySQL Error Message File”.

•  mysql_secure_installation

This program enables you to improve the security of your MySQL installation. See Section 6.4.2,
“mysql_secure_installation — Improve MySQL Installation Security”.

•  mysql_tzinfo_to_sql

This program loads the time zone tables in the mysql database using the contents of the
host system zoneinfo database (the set of files describing time zones). See Section 6.4.3,
“mysql_tzinfo_to_sql — Load the Time Zone Tables”.

282

Specifying Program Options

• opt_name

This is equivalent to --opt_name on the command line.

• opt_name=value

This is equivalent to --opt_name=value on the command line. In an option file, you can have
spaces around the = character, something that is not true on the command line. The value optionally
can be enclosed within single quotation marks or double quotation marks, which is useful if the value
contains a # comment character.

Leading and trailing spaces are automatically deleted from option names and values.

You can use the escape sequences \b, \t, \n, \r, \\, and \s in option values to represent the
backspace, tab, newline, carriage return, backslash, and space characters. In option files, these
escaping rules apply:

• A backslash followed by a valid escape sequence character is converted to the character

represented by the sequence. For example, \s is converted to a space.

• A backslash not followed by a valid escape sequence character remains unchanged. For example,

\S is retained as is.

The preceding rules mean that a literal backslash can be given as \\, or as \ if it is not followed by a
valid escape sequence character.

The rules for escape sequences in option files differ slightly from the rules for escape sequences in
string literals in SQL statements. In the latter context, if “x” is not a valid escape sequence character,
\x becomes “x” rather than \x. See Section 11.1.1, “String Literals”.

The escaping rules for option file values are especially pertinent for Windows path names, which use \
as a path name separator. A separator in a Windows path name must be written as \\ if it is followed
by an escape sequence character. It can be written as \\ or \ if it is not. Alternatively, / may be used
in Windows path names and is treated as \. Suppose that you want to specify a base directory of C:
\Program Files\MySQL\MySQL Server 8.4 in an option file. This can be done several ways.
Some examples:

basedir="C:\Program Files\MySQL\MySQL Server 8.4"
basedir="C:\\Program Files\\MySQL\\MySQL Server 8.4"
basedir="C:/Program Files/MySQL/MySQL Server 8.4"
basedir=C:\\Program\sFiles\\MySQL\\MySQL\sServer\s8.4

If an option group name is the same as a program name, options in the group apply specifically to
that program. For example, the [mysqld] and [mysql] groups apply to the mysqld server and the
mysql client program, respectively.

The [client] option group is read by all client programs provided in MySQL distributions (but not by
mysqld). To understand how third-party client programs that use the C API can use option files, see
the C API documentation at mysql_options().

The [client] group enables you to specify options that apply to all clients. For example, [client]
is the appropriate group to use to specify the password for connecting to the server. (But make sure
that the option file is accessible only by yourself, so that other people cannot discover your password.)
Be sure not to put an option in the [client] group unless it is recognized by all client programs that
you use. Programs that do not understand the option quit after displaying an error message if you try to
run them.

List more general option groups first and more specific groups later. For example, a [client] group
is more general because it is read by all client programs, whereas a [mysqldump] group is read only
by mysqldump. Options specified later override options specified earlier, so putting the option groups
in the order [client], [mysqldump] enables mysqldump-specific options to override [client]
options.

291

Specifying Program Options

Here is a typical global option file:

[client]
port=3306
socket=/tmp/mysql.sock

[mysqld]
port=3306
socket=/tmp/mysql.sock
key_buffer_size=16M
max_allowed_packet=128M

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
groups with names of [mysqld-8.3], [mysqld-8.4], and so forth. The following group indicates
that the sql_mode setting should be used only by MySQL servers with 8.4.x version numbers:

[mysqld-8.4]
sql_mode=TRADITIONAL

Option File Inclusions

It is possible to use !include directives in option files to include other option files and !includedir
to search specific directories for option files. For example, to include the /home/mydir/myopt.cnf
file, use the following directive:

!include /home/mydir/myopt.cnf

To search the /home/mydir directory and read option files found there, use this directive:

!includedir /home/mydir

MySQL makes no guarantee about the order in which option files in the directory are read.

Note

Any files to be found and included using the !includedir directive on Unix
operating systems must have file names ending in .cnf. On Windows, this
directive checks for files with the .ini or .cnf extension.

Write the contents of an included option file like any other option file. That is, it should contain groups of
options, each preceded by a [group] line that indicates the program to which the options apply.

While an included file is being processed, only those options in groups that the current program is
looking for are used. Other groups are ignored. Suppose that a my.cnf file contains this line:

!include /home/mydir/myopt.cnf

And suppose that /home/mydir/myopt.cnf looks like this:

[mysqladmin]
force

[mysqld]
key_buffer_size=16M

292

Specifying Program Options

If my.cnf is processed by mysqld, only the [mysqld] group in /home/mydir/myopt.cnf is used.
If the file is processed by mysqladmin, only the [mysqladmin] group is used. If the file is processed
by any other program, no options in /home/mydir/myopt.cnf are used.

The !includedir directive is processed similarly except that all option files in the named directory
are read.

If an option file contains !include or !includedir directives, files named by those directives are
processed whenever the option file is processed, no matter where they appear in the file.

For inclusion directives to work, the file path should not be specified within quotes and should have
no escape sequences. For example, the following statements provided in my.ini read the option file
myopts.ini:

!include C:/ProgramData/MySQL/MySQL Server/myopts.ini
!include C:\ProgramData\MySQL\MySQL Server\myopts.ini
!include C:\\ProgramData\\MySQL\\MySQL Server\\myopts.ini

On Windows, if !include /path/to/extra.ini is the last line in the file, make sure that a newline
is appended at the end; otherwise, the line is ignored.

6.2.2.3 Command-Line Options that Affect Option-File Handling

Most MySQL programs that support option files handle the following options. Because these options
affect option-file handling, they must be given on the command line and not in an option file. To work
properly, each of these options must be given before other options, with these exceptions:

• --print-defaults may be used immediately after --defaults-file, --defaults-extra-

file, --login-path, or --no-login-paths.

• On Windows, if the server is started with the --defaults-file and --install options, --

install must be first. See Section 2.3.3.8, “Starting MySQL as a Windows Service”.

When specifying file names as option values, avoid the use of the ~ shell metacharacter because it
might not be interpreted as you expect.

Table 6.3 Option File Option Summary

Option Name

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--login-path

--no-defaults

--no-login-paths

Description

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Read login path options from .mylogin.cnf

Read no option files

Do not read options from login path file

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=filename

Type

Default Value

File name

[none]

Read this option file after the global option file but (on Unix) before the user option file and (on all
platforms) before the login path file. (For information about the order in which option files are used,
see Section 6.2.2.2, “Using Option Files”.) If the file does not exist or is otherwise inaccessible, an
error occurs. If file_name is not an absolute path name, it is interpreted relative to the current
directory.

293

Specifying Program Options

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
file_name is interpreted relative to the current directory if given as a relative path name rather than
a full path name.

Exceptions: Even with --defaults-file, mysqld reads mysqld-auto.cnf and client programs
read .mylogin.cnf.

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

• --login-path=name

Command-Line Format

--login-path=name

Type

Default Value

String

[none]

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to

294

Specifying Program Options

authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

A client program reads the option group corresponding to the named login path, in addition to option
groups that the program reads by default. Consider this command:

mysql --login-path=mypath

By default, the mysql client reads the [client] and [mysql] option groups. So for the command
shown, mysql reads [client] and [mysql] from other option files, and [client], [mysql],
and [mypath] from the login path file.

Client programs read the login path file even when the --no-defaults option is used, unless --
no-login-paths is set.

To specify an alternate login path file name, set the MYSQL_TEST_LOGIN_FILE environment
variable.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

• --no-login-paths

Command-Line Format

--no-login-paths

Type

Default Value

Boolean

false

Skips reading options from the login path file. Client programs always read the login path file without
this option even when the --no-defaults option is used.

See --login-path for related information.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

• --no-defaults

Command-Line Format

--no-defaults

Type

Default Value

Boolean

false

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that client programs read the .mylogin.cnf login path file, if it exists, even
when --no-defaults is used unless --no-login-paths is set. This permits passwords to be
specified in a safer way than on the command line even if --no-defaults is present. To create
.mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7, “mysql_config_editor
— MySQL Configuration Utility”.

• --print-defaults

Command-Line Format

Type

--print-defaults

Boolean

295

Specifying Program Options

Default Value

false

Print the program name and all options that it gets from option files. Password values are masked.

See the introduction to this section regarding constraints on the position in which this option may be
specified.

6.2.2.4 Program Option Modifiers

Some options are “boolean” and control behavior that can be turned on or off. For example, the mysql
client supports a --column-names option that determines whether or not to display a row of column
names at the beginning of query results. By default, this option is enabled. However, you may want
to disable it in some instances, such as when sending the output of mysql into another program that
expects to see only data and not an initial header line.

To disable column names, you can specify the option using any of these forms:

--disable-column-names
--skip-column-names
--column-names=0

The --disable and --skip prefixes and the =0 suffix all have the same effect: They turn the option
off.

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
same machine and list options in an option file. An option that may not be recognized by all versions of
a program can be given using the --loose prefix (or loose in an option file). Versions of the program
that recognize the option process it normally, and versions that do not recognize it issue a warning and
ignore it.

The --maximum prefix is available for mysqld only and permits a limit to be placed on how large client
programs can set session system variables. To do this, use a --maximum prefix with the variable
name. For example, --maximum-max_heap_table_size=32M prevents any client from making the
heap table size limit larger than 32M.

The --maximum prefix is intended for use with system variables that have a session value. If applied
to a system variable that has only a global value, an error occurs. For example, with --maximum-
back_log=200, the server produces this error:

Maximum value of 'back_log' cannot be set

6.2.2.5 Using Options to Set Program Variables

Many MySQL programs have internal variables that can be set at runtime using the SET statement.
See Section 15.7.6.1, “SET Syntax for Variable Assignment”, and Section 7.1.9, “Using System
Variables”.

296

Specifying Program Options

Most of these program variables also can be set at server startup by using the same syntax that
applies to specifying program options. For example, mysql has a max_allowed_packet variable that
controls the maximum size of its communication buffer. To set the max_allowed_packet variable for
mysql to a value of 16MB, use either of the following commands:

mysql --max_allowed_packet=16777216
mysql --max_allowed_packet=16M

The first command specifies the value in bytes. The second specifies the value in megabytes. For
variables that take a numeric value, the value can be given with a suffix of K, M, or G to indicate a
multiplier of 1024, 10242 or 10243. (For example, when used to set max_allowed_packet, the
suffixes indicate units of kilobytes, megabytes, or gigabytes.) As of MySQL 8.0.14, a suffix can also
be T, P, and E to indicate a multiplier of 10244, 10245 or 10246. Suffix letters can be uppercase or
lowercase.

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

Suffixes for specifying a value multiplier can be used when setting a variable at program invocation
time, but not to set the value with SET at runtime. On the other hand, with SET, you can assign a
variable's value using an expression, which is not true when you set a variable at server startup. For
example, the first of the following lines is legal at program invocation time, but the second is not:

$> mysql --max_allowed_packet=16M
$> mysql --max_allowed_packet=16*1024*1024

Conversely, the second of the following lines is legal at runtime, but the first is not:

mysql> SET GLOBAL max_allowed_packet=16M;
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;

6.2.2.6 Option Defaults, Options Expecting Values, and the = Sign

By convention, long forms of options that assign a value are written with an equals (=) sign, like this:

mysql --host=tonfisk --user=jon

For options that require a value (that is, not having a default value), the equal sign is not required, and
so the following is also valid:

mysql --host tonfisk --user jon

In both cases, the mysql client attempts to connect to a MySQL server running on the host named
“tonfisk” using an account with the user name “jon”.

Due to this behavior, problems can occasionally arise when no value is provided for an option that
expects one. Consider the following example, where a user connects to a MySQL server running on
host tonfisk as user jon:

297

Specifying Program Options

$> mysql --host 85.224.35.45 --user jon
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 8.4.5 Source distribution

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

In this case, mysql was unable to find a value following the --user option because nothing came
after it on the command line. However, if you omit the value for an option that is not the last option to
be used, you obtain a different error that you may not be expecting:

$> mysql --host --user jon
ERROR 2005 (HY000): Unknown MySQL server host '--user' (1)

Because mysql assumes that any string following --host on the command line is a host name, --
host --user is interpreted as --host=--user, and the client attempts to connect to a MySQL
server running on a host named “--user”.

Options having default values always require an equal sign when assigning a value; failing to do
so causes an error. For example, the MySQL server --log-error option has the default value
host_name.err, where host_name is the name of the host on which MySQL is running. Assume
that you are running MySQL on a computer whose host name is “tonfisk”, and consider the following
invocation of mysqld_safe:

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
background; it is ignored by MySQL itself.) Now suppose that you wish to log errors to a file named
my-errors.err. You might try starting the server with --log-error my-errors, but this does not
have the intended effect, as shown here:

$> mysqld_safe --log-error my-errors &
[1] 31357
$> 080111 22:53:31 mysqld_safe Logging to '/usr/local/mysql/var/tonfisk.err'.
080111 22:53:32 mysqld_safe Starting mysqld daemon with databases from /usr/local/mysql/var
080111 22:53:34 mysqld_safe mysqld from pid file /usr/local/mysql/var/tonfisk.pid ended

[1]+  Done                    ./mysqld_safe --log-error my-errors

The server attempted to start using /usr/local/mysql/var/tonfisk.err as the error log, but
then shut down. Examining the last few lines of this file shows the reason:

298

Command Options for Connecting to the Server

Option Name

--socket

--user

Description

Unix socket file or Windows named pipe to use

MySQL user name to use when connecting to
server

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

The host on which the MySQL server is running. The value can be a host name, IPv4 address, or
IPv6 address. The default value is localhost.

• --password[=pass_val], -p[pass_val]

Command-Line Format

--password[=password]

Type

Default Value

String

[none]

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, the client program prompts for one. If given, there must be no space between
--password= or -p and the password following it. If no password option is specified, the default is
to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that the client program should not prompt for one,
use the --skip-password option.

• --password1[=pass_val]

Command-Line Format

--password1[=password]

Type

String

The password for multifactor authentication factor 1 of the MySQL account used for connecting to
the server. The password value is optional. If not given, the client program prompts for one. If given,
there must be no space between --password1= and the password following it. If no password
option is specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

301

Command Options for Connecting to the Server

To explicitly specify that there is no password and that the client program should not prompt for one,
use the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

Command-Line Format

--password2[=password]

Type

String

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

Command-Line Format

--password3[=password]

Type

String

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

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
used to specify an authentication plugin but the client program does not find it. See Section 8.2.17,
“Pluggable Authentication”.

• --port=port_num, -P port_num

Command-Line Format

--port=port_num

Type

Default Value

Numeric

3306

For TCP/IP connections, the port number to use. The default port number is 3306.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

302

Command Options for Connecting to the Server

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

This option explicitly specifies which transport protocol to use for connecting to the server. It is useful
when other connection parameters normally result in use of a protocol other than the one you want.
For example, connections on Unix to localhost are made using a Unix socket file by default:

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

Shared-memory transport to
local server

Windows

Windows

See also Section 6.2.7, “Connection Transport Protocols”

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

303

Command Options for Connecting to the Server

Type

String

On Unix, the name of the Unix socket file to use for connections made using a named pipe to a local
server. The default Unix socket file name is /tmp/mysql.sock.

On Windows, the name of the named pipe to use for connections to a local server. The default
Windows pipe name is MySQL. The pipe name is not case-sensitive.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

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
Section 8.3.1, “Configuring MySQL to Use Encrypted Connections”.

Note

These options have an effect only for connections that use a transport protocol
subject to encryption; that is, TCP/IP and Unix socket-file connections. See
Section 6.2.7, “Connection Transport Protocols”

For information about using encrypted connections from the MySQL C API, see Support for Encrypted
Connections.

Table 6.5 Connection-Encryption Option Summary

Option Name

--get-server-public-key

--server-public-key-path

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

304

Description

Request RSA public key from server

Path name to file containing RSA public key

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

Command Options for Connecting to the Server

Option Name

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tls-ciphersuites

--tls-version

• --get-server-public-key

Description

File that contains SSL session data

Whether to establish connections if session reuse
fails

Permissible TLSv1.3 ciphersuites for encrypted
connections

Permissible TLS protocols for encrypted
connections

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

This option is available only if MySQL was built using OpenSSL.

For information about the sha256_password (deprecated) and caching_sha2_password
plugins, see Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching
SHA-2 Pluggable Authentication”.

• --ssl-ca=file_name

Command-Line Format

--ssl-ca=file_name

305

Command Options for Connecting to the Server

Type

File name

The path name of the Certificate Authority (CA) certificate file in PEM format. The file contains a list
of trusted SSL Certificate Authorities.

To tell the client not to authenticate the server certificate when establishing an encrypted connection
to the server, specify neither --ssl-ca nor --ssl-capath. The server still verifies the client
according to any applicable requirements established for the client account, and it still uses any
ssl_ca or ssl_capath system variable values specified on the server side.

To specify the CA file for the server, set the ssl_ca system variable.

• --ssl-capath=dir_name

Command-Line Format

--ssl-capath=dir_name

Type

Directory name

The path name of the directory that contains trusted SSL certificate authority (CA) certificate files in
PEM format.

To tell the client not to authenticate the server certificate when establishing an encrypted connection
to the server, specify neither --ssl-ca nor --ssl-capath. The server still verifies the client
according to any applicable requirements established for the client account, and it still uses any
ssl_ca or ssl_capath system variable values specified on the server side.

To specify the CA directory for the server, set the ssl_capath system variable.

• --ssl-cert=file_name

Command-Line Format

--ssl-cert=file_name

Type

File name

The path name of the client SSL public key certificate file in PEM format. Chained SSL certificates
are supported.

To specify the server SSL public key certificate file, set the ssl_cert system variable.

• --ssl-cipher=cipher_list

Command-Line Format

--ssl-cipher=name

Type

String

The list of permissible encryption ciphers for connections that use TLSv1.2. If no cipher in the list is
supported, encrypted connections that use these TLS protocols do not work.

For greatest portability, cipher_list should be a list of one or more cipher names, separated by
colons. Examples:

--ssl-cipher=AES128-SHA
--ssl-cipher=DHE-RSA-AES128-GCM-SHA256:AES128-SHA

OpenSSL supports the syntax for specifying ciphers described in the OpenSSL documentation at
https://www.openssl.org/docs/manmaster/man1/ciphers.html.

For information about which encryption ciphers MySQL supports, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

306

Command Options for Connecting to the Server

To specify the encryption ciphers for the server, set the ssl_cipher system variable.

• --ssl-crl=file_name

Command-Line Format

--ssl-crl=file_name

Type

File name

The path name of the file containing certificate revocation lists in PEM format.

If neither --ssl-crl nor --ssl-crlpath is given, no CRL checks are performed, even if the CA
path contains certificate revocation lists.

To specify the revocation-list file for the server, set the ssl_crl system variable.

• --ssl-crlpath=dir_name

Command-Line Format

--ssl-crlpath=dir_name

Type

Directory name

The path name of the directory that contains certificate revocation-list files in PEM format.

If neither --ssl-crl nor --ssl-crlpath is given, no CRL checks are performed, even if the CA
path contains certificate revocation lists.

To specify the revocation-list directory for the server, set the ssl_crlpath system variable.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permissible:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permissible
value for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-

307

Command Options for Connecting to the Server

mode to ON or STRICT causes the client to produce a warning at startup and
to operate in non-FIPS mode.

To specify the FIPS mode for the server, set the ssl_fips_mode system variable.

• --ssl-key=file_name

Command-Line Format

--ssl-key=file_name

Type

File name

The path name of the client SSL private key file in PEM format. For better security, use a certificate
with an RSA key size of at least 2048 bits.

If the key file is protected by a passphrase, the client program prompts the user for the passphrase.
The password must be given interactively; it cannot be stored in a file. If the passphrase is incorrect,
the program continues as if it could not read the key.

To specify the server SSL private key file, set the ssl_key system variable.

• --ssl-mode=mode

Command-Line Format

--ssl-mode=mode

Type

Default Value

Valid Values

Enumeration

PREFERRED

DISABLED

PREFERRED

REQUIRED

VERIFY_CA

VERIFY_IDENTITY

This option specifies the desired security state of the connection to the server. These mode values
are permissible, in order of increasing strictness:

• DISABLED: Establish an unencrypted connection.

• PREFERRED: Establish an encrypted connection if the server supports encrypted connections,

falling back to an unencrypted connection if an encrypted connection cannot be established. This
is the default if --ssl-mode is not specified.

Connections over Unix socket files are not encrypted with a mode of PREFERRED. To enforce
encryption for Unix socket-file connections, use a mode of REQUIRED or stricter. (However,
socket-file transport is secure by default, so encrypting a socket-file connection makes it no more
secure and increases CPU load.)

• REQUIRED: Establish an encrypted connection if the server supports encrypted connections. The

connection attempt fails if an encrypted connection cannot be established.

• VERIFY_CA: Like REQUIRED, but additionally verify the server Certificate Authority (CA) certificate

against the configured CA certificates. The connection attempt fails if no valid matching CA
certificates are found.

308

Command Options for Connecting to the Server

• VERIFY_IDENTITY: Like VERIFY_CA, but additionally perform host name identity verification

by checking the host name the client uses for connecting to the server against the identity in the
certificate that the server sends to the client:

• If the client uses OpenSSL 1.0.2 or higher, the client checks whether the host name that it uses
for connecting matches either the Subject Alternative Name value or the Common Name value
in the server certificate. Host name identity verification also works with certificates that specify
the Common Name using wildcards.

• Otherwise, the client checks whether the host name that it uses for connecting matches the

Common Name value in the server certificate.

The connection fails if there is a mismatch. For encrypted connections, this option helps prevent
man-in-the-middle attacks.

Note

Host name identity verification with VERIFY_IDENTITY does not work
with self-signed certificates that are created automatically by the server
(see Section 8.3.3.1, “Creating SSL and RSA Certificates and Keys using
MySQL”). Such self-signed certificates do not contain the server name as
the Common Name value.

Important

The default setting, --ssl-mode=PREFERRED, produces an encrypted
connection if the other default settings are unchanged. However, to help
prevent sophisticated man-in-the-middle attacks, it is important for the client
to verify the server’s identity. The settings --ssl-mode=VERIFY_CA and --
ssl-mode=VERIFY_IDENTITY are a better choice than the default setting to
help prevent this type of attack. To implement one of these settings, you must
first ensure that the CA certificate for the server is reliably available to all the
clients that use it in your environment, otherwise availability issues will result.
For this reason, they are not the default setting.

The --ssl-mode option interacts with CA certificate options as follows:

• If --ssl-mode is not explicitly set otherwise, use of --ssl-ca or --ssl-capath implies --

ssl-mode=VERIFY_CA.

• For --ssl-mode values of VERIFY_CA or VERIFY_IDENTITY, --ssl-ca or --ssl-capath is

also required, to supply a CA certificate that matches the one used by the server.

• An explicit --ssl-mode option with a value other than VERIFY_CA or VERIFY_IDENTITY,
together with an explicit --ssl-ca or --ssl-capath option, produces a warning that no
verification of the server certificate is performed, despite a CA certificate option being specified.

To require use of encrypted connections by a MySQL account, use CREATE USER to create the
account with a REQUIRE SSL clause, or use ALTER USER for an existing account to add a REQUIRE
SSL clause. This causes connection attempts by clients that use the account to be rejected unless
MySQL supports encrypted connections and an encrypted connection can be established.

The REQUIRE clause permits other encryption-related options, which can be used to enforce security
requirements stricter than REQUIRE SSL. For additional details about which command options may
or must be specified by clients that connect using accounts configured using the various REQUIRE
options, see CREATE USER SSL/TLS Options.

309

Command Options for Connecting to the Server

• --ssl-session-data=file_name

Command-Line Format

--ssl-session-data=file_name

Type

File name

The path name of the client SSL session data file in PEM format for session reuse.

When you invoke a MySQL client program with the --ssl-session-data option, the client
attempts to deserialize session data from the file, if provided, and then use it to establish a new
connection. If you supply a file, but the session is not reused, then the connection fails unless you
also specified the --ssl-session-data-continue-on-failed-reuse option on the command
line when you invoked the client program.

The mysql command, ssl_session_data_print, generates the session data file (see
Section 6.5.1.2, “mysql Client Commands”).

• ssl-session-data-continue-on-failed-reuse

Command-Line Format

Type

Default Value

--ssl-session-data-continue-on-
failed-reuse

Boolean

OFF

Controls whether a new connection is started to replace an attempted connection that tried but failed
to reuse session data specified with the --ssl-session-data command-line option. By default,
the --ssl-session-data-continue-on-failed-reuse command-line option is off, which
causes a client program to return a connect failure when session data are supplied and not reused.

To ensure that a new, unrelated connection opens after session reuse fails silently, invoke MySQL
client programs with both the --ssl-session-data and --ssl-session-data-continue-on-
failed-reuse command-line options.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

Default Value

String

empty string

This option specifies which ciphersuites the client permits for encrypted connections that use
TLSv1.3. The value is a list of zero or more colon-separated ciphersuite names. For example:

mysql --tls-ciphersuites="suite1:suite2:suite3"

The ciphersuites that can be named for this option depend on the SSL library used to compile
MySQL. If this option is not set, the client permits the default set of ciphersuites. If the option is set to
the empty string, no ciphersuites are enabled and encrypted connections cannot be established. For
more information, see Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”.

To specify which ciphersuites the server permits, set the tls_ciphersuites system variable.

• --tls-version=protocol_list

310

Command-Line Format

--tls-version=protocol_list

Type

String

Command Options for Connecting to the Server

Default Value

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

This option specifies the TLS protocols the client permits for encrypted connections. The value is a
list of one or more comma-separated protocol versions. For example:

mysql --tls-version="TLSv1.2,TLSv1.3"

The protocols that can be named for this option depend on the SSL library used to compile MySQL,
and on the MySQL Server release.

Important

• Clients, including MySQL Shell, that support the --tls-version option
cannot make a TLS/SSL connection with the protocol set to TLSv1 or
TLSv1.1. If a client attempts to connect using these protocols, for TCP
connections, the connection fails, and an error is returned to the client. For
socket connections, if --ssl-mode is set to REQUIRED, the connection
fails, otherwise the connection is made but with TLS/SSL disabled. See
Removal of Support for the TLSv1 and TLSv1.1 Protocols for more
information.

• Support for the TLSv1.3 protocol is available in MySQL Server, provided
that MySQL Server was compiled using OpenSSL 1.1.1 or higher. The
server checks the version of OpenSSL at startup, and if it is lower than
1.1.1, TLSv1.3 is removed from the default value for the server system
variables relating to the TLS version (such as the tls_version system
variable).

Permitted protocols should be chosen such as not to leave “holes” in the list. For example, these
values do not have holes:

--tls-version="TLSv1.2,TLSv1.3"
--tls-version="TLSv1.3"

For details, see Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”.

To specify which TLS protocols the server permits, set the tls_version system variable.

Command Options for Connection Compression

This section describes options that enable client programs to control use of compression for
connections to the server. For additional information and examples showing how to use them, see
Section 6.2.8, “Connection Compression Control”.

Table 6.6 Connection-Compression Option Summary

Option Name

--compress

--compression-algorithms

--zstd-compression-level

• --compress, -C

Description

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Compression level for connections to server that
use zstd compression

311

Connecting to the MySQL Server Using Command Options

mysql

Because there are no parameter options, the default values apply:

• The default host name is localhost. On Unix, this has a special meaning, as described later.

• The default user name is ODBC on Windows or your Unix login name on Unix.

• No password is sent because neither --password nor -p is given.

• For mysql, the first nonoption argument is taken as the name of the default database. Because

there is no such argument, mysql selects no default database.

To specify the host name and user name explicitly, as well as a password, supply appropriate options
on the command line. To select a default database, add a database-name argument. Examples:

mysql --host=localhost --user=myname --password=password mydb
mysql -h localhost -u myname -ppassword mydb

For password options, the password value is optional:

• If you use a --password or -p option and specify a password value, there must be no space

between --password= or -p and the password following it.

• If you use --password or -p but do not specify a password value, the client program prompts

you to enter the password. The password is not displayed as you enter it. This is more secure than
giving the password on the command line, which might enable other users on your system to see the
password line by executing a command such as ps. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

• To explicitly specify that there is no password and that the client program should not prompt for one,

use the --skip-password option.

As just mentioned, including the password value on the command line is a security risk. To avoid this
risk, specify the --password or -p option without any following password value:

mysql --host=localhost --user=myname --password mydb
mysql -h localhost -u myname -p mydb

When the --password or -p option is given with no password value, the client program prints a
prompt and waits for you to enter the password. (In these examples, mydb is not interpreted as a
password because it is separated from the preceding password option by a space.)

On some systems, the library routine that MySQL uses to prompt for a password automatically limits
the password to eight characters. That limitation is a property of the system library, not MySQL.
Internally, MySQL does not have any limit for the length of the password. To work around the limitation
on systems affected by it, specify your password in an option file (see Section 6.2.2.2, “Using Option
Files”). Another workaround is to change your MySQL password to a value that has eight or fewer
characters, but that has the disadvantage that shorter passwords tend to be less secure.

Client programs determine what type of connection to make as follows:

• If the host is not specified or is localhost, a connection to the local host occurs:

• On Windows, the client connects using shared memory, if the server was started with the

shared_memory system variable enabled to support shared-memory connections.

• On Unix, MySQL programs treat the host name localhost specially, in a way that is likely

different from what you expect compared to other network-based programs: the client connects
using a Unix socket file. The --socket option or the MYSQL_UNIX_PORT environment variable
may be used to specify the socket name.

• On Windows, if host is . (period), or TCP/IP is not enabled and --socket is not specified
or the host is empty, the client connects using a named pipe, if the server was started with
the named_pipe system variable enabled to support named-pipe connections. If named-pipe

313

Connecting to the MySQL Server Using Command Options

connections are not supported or if the user making the connection is not a member of the Windows
group specified by the named_pipe_full_access_group system variable, an error occurs.

• Otherwise, the connection uses TCP/IP.

The --protocol option enables you to use a particular transport protocol even when other options
normally result in use of a different protocol. That is, --protocol specifies the transport protocol
explicitly and overrides the preceding rules, even for localhost.

Only connection options that are relevant to the selected transport protocol are used or checked. Other
connection options are ignored. For example, with --host=localhost on Unix, the client attempts to
connect to the local server using a Unix socket file, even if a --port or -P option is given to specify a
TCP/IP port number.

To ensure that the client makes a TCP/IP connection to the local server, use --host or -h to specify
a host name value of 127.0.0.1 (instead of localhost), or the IP address or name of the local
server. You can also specify the transport protocol explicitly, even for localhost, by using the --
protocol=TCP option. Examples:

mysql --host=127.0.0.1
mysql --protocol=TCP

If the server is configured to accept IPv6 connections, clients can connect to the local server over IPv6
using --host=::1. See Section 7.1.13, “IPv6 Support”.

On Windows, to force a MySQL client to use a named-pipe connection, specify the --pipe
or --protocol=PIPE option, or specify . (period) as the host name. If the server was not
started with the named_pipe system variable enabled to support named-pipe connections
or if the user making the connection is not a member of the Windows group specified by the
named_pipe_full_access_group system variable, an error occurs. Use the --socket option to
specify the name of the pipe if you do not want to use the default pipe name.

Connections to remote servers use TCP/IP. This command connects to the server running on
remote.example.com using the default port number (3306):

mysql --host=remote.example.com

To specify a port number explicitly, use the --port or -P option:

mysql --host=remote.example.com --port=13306

You can specify a port number for connections to a local server, too. However, as indicated previously,
connections to localhost on Unix use a socket file by default, so unless you force a TCP/IP
connection as previously described, any option that specifies a port number is ignored.

For this command, the program uses a socket file on Unix and the --port option is ignored:

mysql --port=13306 --host=localhost

To cause the port number to be used, force a TCP/IP connection. For example, invoke the program in
either of these ways:

mysql --port=13306 --host=127.0.0.1
mysql --port=13306 --protocol=TCP

For additional information about options that control how client programs establish connections to the
server, see Section 6.2.3, “Command Options for Connecting to the Server”.

It is possible to specify connection parameters without entering them on the command line each time
you invoke a client program:

• Specify the connection parameters in the [client] section of an option file. The relevant section of

the file might look like this:

[client]
host=host_name

314

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

user=user_name
password=password

For more information, see Section 6.2.2.2, “Using Option Files”.

• Some connection parameters can be specified using environment variables. Examples:

• To specify the host for mysql, use MYSQL_HOST.

• On Windows, to specify the MySQL user name, use USER.

For a list of supported environment variables, see Section 6.9, “Environment Variables”.

6.2.5 Connecting to the Server Using URI-Like Strings or Key-Value Pairs

This section describes use of URI-like connection strings or key-value pairs to specify how to establish
connections to the MySQL server, for clients such as MySQL Shell. For information on establishing
connections using command-line options, for clients such as mysql or mysqldump, see Section 6.2.4,
“Connecting to the MySQL Server Using Command Options”. For additional information if you are
unable to connect, see Section 8.2.22, “Troubleshooting Problems Connecting to MySQL”.

Note

The term “URI-like” signifies connection-string syntax that is similar to but not
identical to the URI (uniform resource identifier) syntax defined by RFC 3986.

The following MySQL clients support connecting to a MySQL server using a URI-like connection string
or key-value pairs:

• MySQL Shell

• MySQL Connectors which implement X DevAPI

This section documents all valid URI-like string and key-value pair connection parameters, many of
which are similar to those specified with command-line options:

• Parameters specified with a URI-like string use a syntax such as myuser@example.com:3306/

main-schema. For the full syntax, see Connecting Using URI-Like Connection Strings.

• Parameters specified with key-value pairs use a syntax such as {user:'myuser',

host:'example.com', port:3306, schema:'main-schema'}. For the full syntax, see
Connecting Using Key-Value Pairs.

Connection parameters are not case-sensitive. Each parameter, if specified, can be given only once. If
a parameter is specified more than once, an error occurs.

This section covers the following topics:

• Base Connection Parameters

• Additional Connection parameters

• Connecting Using URI-Like Connection Strings

• Connecting Using Key-Value Pairs

Base Connection Parameters

The following discussion describes the parameters available when specifying a connection to MySQL.
These parameters can be provided using either a string that conforms to the base URI-like syntax (see
Connecting Using URI-Like Connection Strings), or as key-value pairs (see Connecting Using Key-
Value Pairs).

• scheme: The transport protocol to use. Use mysqlx for X Protocol connections and mysql for

classic MySQL protocol connections. If no protocol is specified, the server attempts to guess the

315

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

protocol. Connectors that support DNS SRV can use the mysqlx+srv scheme (see Connections
Using DNS SRV Records).

• user: The MySQL user account to provide for the authentication process.

• password: The password to use for the authentication process.

Warning

Specifying an explicit password in the connection specification is insecure
and not recommended. Later discussion shows how to cause an interactive
prompt for the password to occur.

• host: The host on which the server instance is running. The value can be a host name, IPv4

address, or IPv6 address. If no host is specified, the default is localhost.

• port: The TCP/IP network port on which the target MySQL server is listening for connections. If
no port is specified, the default is 33060 for X Protocol connections and 3306 for classic MySQL
protocol connections.

• socket: The path to a Unix socket file or the name of a Windows named pipe. Values are local file
paths. In URI-like strings, they must be encoded, using either percent encoding or by surrounding
the path with parentheses. Parentheses eliminate the need to percent encode characters such
as the / directory separator character. For example, to connect as root@localhost using the
Unix socket /tmp/mysql.sock, specify the path using percent encoding as root@localhost?
socket=%2Ftmp%2Fmysql.sock, or using parentheses as root@localhost?socket=(/tmp/
mysql.sock).

• schema: The default database for the connection. If no database is specified, the connection has no

default database.

The handling of localhost on Unix depends on the type of transport protocol. Connections using
classic MySQL protocol handle localhost the same way as other MySQL clients, which means that
localhost is assumed to be for socket-based connections. For connections using X Protocol, the
behavior of localhost differs in that it is assumed to represent the loopback address, for example,
IPv4 address 127.0.0.1.

Additional Connection parameters

You can specify options for the connection, either as attributes in a URI-like string by appending
?attribute=value, or as key-value pairs. The following options are available:

• ssl-mode: The desired security state for the connection. The following modes are permissible:

• DISABLED

• PREFERRED

• REQUIRED

• VERIFY_CA

• VERIFY_IDENTITY

Important

VERIFY_CA and VERIFY_IDENTITY are better choices than the default
PREFERRED, because they help prevent man-in-the-middle attacks.

For information about these modes, see the --ssl-mode option description in Command Options
for Encrypted Connections.

• ssl-ca: The path to the X.509 certificate authority file in PEM format.

316

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

• ssl-capath: The path to the directory that contains the X.509 certificates authority files in PEM

format.

• ssl-cert: The path to the X.509 certificate file in PEM format.

• ssl-cipher: The encryption cipher to use for connections that use TLS protocols up through

TLSv1.2.

• ssl-crl: The path to the file that contains certificate revocation lists in PEM format.

• ssl-crlpath: The path to the directory that contains certificate revocation-list files in PEM format.

• ssl-key: The path to the X.509 key file in PEM format.

• tls-version: The TLS protocols permitted for classic MySQL protocol encrypted connections.
This option is supported by MySQL Shell only. The value of tls-version (singular) is a comma
separated list, for example TLSv1.2,TLSv1.3. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”. This option depends on the ssl-mode option not being set
to DISABLED.

• tls-versions: The permissible TLS protocols for encrypted X Protocol connections. The value of
tls-versions (plural) is an array such as [TLSv1.2,TLSv1.3]. For details, see Section 8.3.2,
“Encrypted Connection TLS Protocols and Ciphers”. This option depends on the ssl-mode option
not being set to DISABLED.

• tls-ciphersuites: The permitted TLS cipher suites. The value of tls-ciphersuites is a list
of IANA cipher suite names as listed at TLS Ciphersuites. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”. This option depends on the ssl-mode option not being set
to DISABLED.

• auth-method: The authentication method to use for the connection. The default is AUTO, meaning

that the server attempts to guess. The following methods are permissible:

• AUTO

• MYSQL41

• SHA256_MEMORY

• FROM_CAPABILITIES

• FALLBACK

• PLAIN

For X Protocol connections, any configured auth-method is overridden to this sequence of
authentication methods: MYSQL41, SHA256_MEMORY, PLAIN.

• get-server-public-key: Request from the server the public key required for RSA key pair-

based password exchange. Use when connecting to MySQL 8+ servers over classic MySQL protocol
with SSL mode DISABLED. You must specify the protocol in this case. For example:

mysql://user@localhost:3306?get-server-public-key=true

This option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over get-server-public-key.

317

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• server-public-key-path: The path name to a file in PEM format containing a client-side copy
of the public key required by the server for RSA key pair-based password exchange. Use when
connecting to MySQL 8+ servers over classic MySQL protocol with SSL mode DISABLED.

This option applies to clients that authenticate with the sha256_password (deprecated) or
caching_sha2_password authentication plugin. This option is ignored for accounts that do not
authenticate with one of those plugins. It is also ignored if RSA-based password exchange is not
used, as is the case when the client connects to the server using a secure connection.

If server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over get-server-public-key.

For information about the sha256_password (deprecated) and caching_sha2_password
plugins, see Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching
SHA-2 Pluggable Authentication”.

• ssh: The URI for connection to an SSH server to access a MySQL server instance using SSH

tunneling. The URI format is [user@]host[:port]. Use the uri option to specify the URI of the
target MySQL server instance. For information on SSH tunnel connections from MySQL Shell, see
Using an SSH Tunnel.

• uri: The URI for a MySQL server instance that is to be accessed through an SSH tunnel from the
server specified by the ssh option. The URI format is [scheme://][user@]host[:port]. Do
not use the base connection parameters (scheme, user, host, port) to specify the MySQL server
connection for SSH tunneling, just use the uri option.

• ssh-password: The password for the connection to the SSH server.

Warning

Specifying an explicit password in the connection specification is insecure
and not recommended. MySQL Shell prompts for a password interactively
when one is required.

• ssh-config-file: The SSH configuration file for the connection to the SSH server. You can

use the MySQL Shell configuration option ssh.configFile to set a custom file as the default if
this option is not specified. If ssh.configFile has not been set, the default is the standard SSH
configuration file ~/.ssh/config.

• ssh-identity-file: The identity file to use for the connection to the SSH server. The default

if this option is not specified is any identity file configured in an SSH agent (if used), or in the SSH
configuration file, or the standard private key file in the SSH configuration folder (~/.ssh/id_rsa).

• ssh-identity-pass: The passphrase for the identity file specified by the ssh-identity-file

option.

Warning

Specifying an explicit password in the connection specification is insecure
and not recommended. MySQL Shell prompts for a password interactively
when one is required.

• connect-timeout: An integer value used to configure the number of seconds that clients, such as

MySQL Shell, wait until they stop trying to connect to an unresponsive MySQL server.

318

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

• compression: This option requests or disables compression for the connection.

The values available for this option are: required, which requests compression and fails if
the server does not support it; preferred, which requests compression and falls back to an
uncompressed connection; and disabled, which requests an uncompressed connection and
fails if the server does not permit those. preferred is the default for X Protocol connections,
and disabled is the default for classic MySQL protocol connections. For information on X Plugin
connection compression control, see Section 22.5.5, “Connection Compression with X Plugin”.

Note

Different MySQL clients implement their support for connection compression
differently. Consult your client's documentation for details.

• compression-algorithms and compression-level: These options are available in MySQL

Shell for more control over connection compression. You can specify them to select the compression
algorithm used for the connection, and the numeric compression level used with that algorithm.
You can also use compression-algorithms in place of compression to request compression
for the connection. For information on MySQL Shell's connection compression control, see Using
Compressed Connections.

• connection-attributes: Controls the key-value pairs that application programs pass to the
server at connect time. For general information about connection attributes, see Section 29.12.9,
“Performance Schema Connection Attribute Tables”. Clients usually define a default set of attributes,
which can be disabled or enabled. For example:

mysqlx://user@host?connection-attributes
mysqlx://user@host?connection-attributes=true
mysqlx://user@host?connection-attributes=false

The default behavior is to send the default attribute set. Applications can specify attributes to
be passed in addition to the default attributes. You specify additional connection attributes as a
connection-attributes parameter in a connection string. The connection-attributes
parameter value must be empty (the same as specifying true), a Boolean value (true or false to
enable or disable the default attribute set), or a list or zero or more key=value specifiers separated
by commas (to be sent in addition to the default attribute set). Within a list, a missing key value
evaluates as an empty string. Further examples:

mysqlx://user@host?connection-attributes=[attr1=val1,attr2,attr3=]
mysqlx://user@host?connection-attributes=[]

Application-defined attribute names cannot begin with _ because such names are reserved for
internal attributes.

Connecting Using URI-Like Connection Strings

You can specify a connection to MySQL Server using a URI-like string. Such strings can be used
with the MySQL Shell with the --uri command option, the MySQL Shell \connect command, and
MySQL Connectors which implement X DevAPI.

Note

The term “URI-like” signifies connection-string syntax that is similar to but not
identical to the URI (uniform resource identifier) syntax defined by RFC 3986.

A URI-like connection string has the following syntax:

[scheme://][user[:[password]]@]host[:port][/schema][?attribute1=value1&attribute2=value2...

Important

Percent encoding must be used for reserved characters in the elements of the
URI-like string. For example, if you specify a string that includes the @ character,

319

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

the character must be replaced by %40. If you include a zone ID in an IPv6
address, the % character used as the separator must be replaced with %25.

The parameters you can use in a URI-like connection string are described at Base Connection
Parameters.

MySQL Shell's shell.parseUri() and shell.unparseUri() methods can be used
to deconstruct and assemble a URI-like connection string. Given a URI-like connection
string, shell.parseUri() returns a dictionary containing each element found in the string.
shell.unparseUri() converts a dictionary of URI components and connection options into a valid
URI-like connection string for connecting to MySQL, which can be used in MySQL Shell or by MySQL
Connectors which implement X DevAPI.

If no password is specified in the URI-like string, which is recommended, interactive clients prompt
for the password. The following examples show how to specify URI-like strings with the user name
user_name. In each case, the password is prompted for.

• An X Protocol connection to a local server instance listening at port 33065.

mysqlx://user_name@localhost:33065

• A classic MySQL protocol connection to a local server instance listening at port 3333.

mysql://user_name@localhost:3333

• An X Protocol connection to a remote server instance, using a host name, an IPv4 address, and an

IPv6 address.

mysqlx://user_name@server.example.com/
mysqlx://user_name@198.51.100.14:123
mysqlx://user_name@[2001:db8:85a3:8d3:1319:8a2e:370:7348]

• An X Protocol connection using a socket, with the path provided using either percent encoding or

parentheses.

mysqlx://user_name@/path%2Fto%2Fsocket.sock
mysqlx://user_name@(/path/to/socket.sock)

• An optional path can be specified, which represents a database.

# use 'world' as the default database
mysqlx://user_name@198.51.100.1/world

# use 'world_x' as the default database, encoding _ as %5F
mysqlx://user_name@198.51.100.2:33060/world%5Fx

• An optional query can be specified, consisting of values each given as a key=value pair or as a

single key. To specify multiple values, separate them by , characters. A mix of key=value and key
values is permissible. Values can be of type list, with list values ordered by appearance. Strings must
be either percent encoded or surrounded by parentheses. The following are equivalent.

ssluser@127.0.0.1?ssl-ca=%2Froot%2Fclientcert%2Fca-cert.pem\
&ssl-cert=%2Froot%2Fclientcert%2Fclient-cert.pem\
&ssl-key=%2Froot%2Fclientcert%2Fclient-key

ssluser@127.0.0.1?ssl-ca=(/root/clientcert/ca-cert.pem)\
&ssl-cert=(/root/clientcert/client-cert.pem)\
&ssl-key=(/root/clientcert/client-key)

• To specify a TLS version and ciphersuite to use for encrypted connections:

mysql://user_name@198.51.100.2:3306/world%5Fx?\
tls-versions=[TLSv1.2,TLSv1.3]&tls-ciphersuites=[TLS_DHE_PSK_WITH_AES_128_\
GCM_SHA256, TLS_CHACHA20_POLY1305_SHA256]

The previous examples assume that connections require a password. With interactive clients, the
specified user's password is requested at the login prompt. If the user account has no password (which

320

Connecting to the Server Using URI-Like Strings or Key-Value Pairs

is insecure and not recommended), or if socket peer-credential authentication is in use (for example,
with Unix socket connections), you must explicitly specify in the connection string that no password is
being provided and the password prompt is not required. To do this, place a : after the user_name in
the string but do not specify a password after it. For example:

mysqlx://user_name:@localhost

Connecting Using Key-Value Pairs

In MySQL Shell and some MySQL Connectors which implement X DevAPI, you can specify a
connection to MySQL Server using key-value pairs, supplied in language-natural constructs for the
implementation. For example, you can supply connection parameters using key-value pairs as a
JSON object in JavaScript, or as a dictionary in Python. Regardless of the way the key-value pairs are
supplied, the concept remains the same: the keys as described in this section can be assigned values
that are used to specify a connection. You can specify connections using key-value pairs in MySQL
Shell's shell.connect() method or InnoDB Cluster's dba.createCluster() method, and with
some of the MySQL Connectors which implement X DevAPI.

Generally, key-value pairs are surrounded by { and } characters and the , character is used as a
separator between key-value pairs. The : character is used between keys and values, and strings
must be delimited (for example, using the ' character). It is not necessary to percent encode strings,
unlike URI-like connection strings.

A connection specified as key-value pairs has the following format:

{ key: value, key: value, ...}

The parameters you can use as keys for a connection are described at Base Connection Parameters.

If no password is specified in the key-value pairs, which is recommended, interactive clients prompt for
the password. The following examples show how to specify connections using key-value pairs with the
user name 'user_name'. In each case, the password is prompted for.

• An X Protocol connection to a local server instance listening at port 33065.

{user:'user_name', host:'localhost', port:33065}

• A classic MySQL protocol connection to a local server instance listening at port 3333.

{user:'user_name', host:'localhost', port:3333}

• An X Protocol connection to a remote server instance, using a host name, an IPv4 address, and an

IPv6 address.

{user:'user_name', host:'server.example.com'}
{user:'user_name', host:198.51.100.14:123}
{user:'user_name', host:[2001:db8:85a3:8d3:1319:8a2e:370:7348]}

• An X Protocol connection using a socket.

{user:'user_name', socket:'/path/to/socket/file'}

• An optional schema can be specified, which represents a database.

{user:'user_name', host:'localhost', schema:'world'}

The previous examples assume that connections require a password. With interactive clients, the
specified user's password is requested at the login prompt. If the user account has no password (which
is insecure and not recommended), or if socket peer-credential authentication is in use (for example,
with Unix socket connections), you must explicitly specify that no password is being provided and the
password prompt is not required. To do this, provide an empty string using '' after the password key.
For example:

{user:'user_name', password:'', host:'localhost'}

321

Connecting to the Server Using DNS SRV Records

6.2.6 Connecting to the Server Using DNS SRV Records

In the Domain Name System (DNS), a SRV record (service location record) is a type of resource
record that enables a client to specify a name that indicates a service, protocol, and domain. A DNS
lookup on the name returns a reply containing the names of multiple available servers in the domain
that provide the required service. For information about DNS SRV, including how a record defines the
preference order of the listed servers, see RFC 2782.

MySQL supports the use of DNS SRV records for connecting to servers. A client that receives a DNS
SRV lookup result attempts to connect to the MySQL server on each of the listed hosts in order of
preference, based on the priority and weighting assigned to each host by the DNS administrator. A
failure to connect occurs only if the client cannot connect to any of the servers.

When multiple MySQL instances, such as a cluster of servers, provide the same service for your
applications, DNS SRV records can be used to assist with failover, load balancing, and replication
services. It is cumbersome for applications to directly manage the set of candidate servers for
connection attempts, and DNS SRV records provide an alternative:

• DNS SRV records enable a DNS administrator to map a single DNS domain to multiple servers. DNS
SRV records also can be updated centrally by administrators when servers are added or removed
from the configuration or when their host names are changed.

• Central management of DNS SRV records eliminates the need for individual clients to identify each
possible host in connection requests, or for connections to be handled by an additional software
component. An application can use the DNS SRV record to obtain information about candidate
MySQL servers, instead of managing the server information itself.

• DNS SRV records can be used in combination with connection pooling, in which case connections to
hosts that are no longer in the current list of DNS SRV records are removed from the pool when they
become idle.

MySQL supports use of DNS SRV records to connect to servers in these contexts:

• Several MySQL Connectors implement DNS SRV support; connector-specific options enable

requesting DNS SRV record lookup both for X Protocol connections and for classic MySQL protocol
connections. For general information, see Connections Using DNS SRV Records. For details, see
the documentation for individual MySQL Connectors.

• The C API provides a mysql_real_connect_dns_srv() function that is similar to

mysql_real_connect(), except that the argument list does not specify the particular host of the
MySQL server to connect to. Instead, it names a DNS SRV record that specifies a group of servers.
See mysql_real_connect_dns_srv().

• The mysql client has a --dns-srv-name option to indicate a DNS SRV record that specifies a

group of servers. See Section 6.5.1, “mysql — The MySQL Command-Line Client”.

A DNS SRV name consists of a service, protocol, and domain, with the service and protocol each
prefixed by an underscore:

_service._protocol.domain

The following DNS SRV record identifies multiple candidate servers, such as might be used by clients
for establishing X Protocol connections:

Name                      TTL   Class  Priority Weight Port  Target
_mysqlx._tcp.example.com. 86400 IN SRV 0        5      33060 server1.example.com.
_mysqlx._tcp.example.com. 86400 IN SRV 0        10     33060 server2.example.com.
_mysqlx._tcp.example.com. 86400 IN SRV 10       5      33060 server3.example.com.
_mysqlx._tcp.example.com. 86400 IN SRV 20       5      33060 server4.example.com.

Here, mysqlx indicates the X Protocol service and tcp indicates the TCP protocol. A client can
request this DNS SRV record using the name _mysqlx._tcp.example.com. The particular syntax

322

Connection Transport Protocols

for specifying the name in the connection request depends on the type of client. For example, a client
might support specifying the name within a URI-like connection string or as a key-value pair.

A DNS SRV record for classic protocol connections might look like this:

Name                     TTL   Class  Priority Weight  Port Target
_mysql._tcp.example.com. 86400 IN SRV 0        5       3306 server1.example.com.
_mysql._tcp.example.com. 86400 IN SRV 0        10      3306 server2.example.com.
_mysql._tcp.example.com. 86400 IN SRV 10       5       3306 server3.example.com.
_mysql._tcp.example.com. 86400 IN SRV 20       5       3306 server4.example.com.

Here, the name mysql designates the classic MySQL protocol service, and the port is 3306 (the
default classic MySQL protocol port) rather than 33060 (the default X Protocol port).

When DNS SRV record lookup is used, clients generally must apply these rules for connection
requests (there may be client- or connector-specific exceptions):

• The request must specify the full DNS SRV record name, with the service and protocol names

prefixed by underscores.

• The request must not specify multiple host names.

• The request must not specify a port number.

• Only TCP connections are supported. Unix socket files, Windows named pipes, and shared memory

cannot be used.

For more information on using DNS SRV based connections in X DevAPI, see Connections Using DNS
SRV Records.

6.2.7 Connection Transport Protocols

For programs that use the MySQL client library (for example, mysql and mysqldump), MySQL
supports connections to the server based on several transport protocols: TCP/IP, Unix socket file,
named pipe, and shared memory. This section describes how to select these protocols, and how they
are similar and different.

• Transport Protocol Selection

• Transport Support for Local and Remote Connections

• Interpretation of localhost

• Encryption and Security Characteristics

• Connection Compression

Transport Protocol Selection

For a given connection, if the transport protocol is not specified explicitly, it is determined implicitly. For
example, connections to localhost result in a socket file connection on Unix and Unix-like systems,
and a TCP/IP connection to 127.0.0.1 otherwise. For additional information, see Section 6.2.4,
“Connecting to the MySQL Server Using Command Options”.

To specify the protocol explicitly, use the --protocol command option. The following table shows the
permissible values for --protocol and indicates the applicable platforms for each value. The values
are not case-sensitive.

--protocol Value

Transport Protocol Used

Applicable Platforms

TCP

SOCKET

PIPE

TCP/IP

Unix socket file

Named pipe

All

Unix and Unix-like systems

Windows

323

Connection Compression Control

--protocol Value

Transport Protocol Used

Applicable Platforms

MEMORY

Shared memory

Windows

Transport Support for Local and Remote Connections

TCP/IP transport supports connections to local or remote MySQL servers.

Socket-file, named-pipe, and shared-memory transports support connections only to local MySQL
servers. (Named-pipe transport does allow for remote connections, but this capability is not
implemented in MySQL.)

Interpretation of localhost

If the transport protocol is not specified explicitly, localhost is interpreted as follows:

• On Unix and Unix-like systems, a connection to localhost results in a socket-file connection.

• Otherwise, a connection to localhost results in a TCP/IP connection to 127.0.0.1.

If the transport protocol is specified explicitly, localhost is interpreted with respect to that protocol.
For example, with --protocol=TCP, a connection to localhost results in a TCP/IP connection to
127.0.0.1 on all platforms.

Encryption and Security Characteristics

TCP/IP and socket-file transports are subject to TLS/SSL encryption, using the options described in
Command Options for Encrypted Connections. Named-pipe and shared-memory transports are not
subject to TLS/SSL encryption.

A connection is secure by default if made over a transport protocol that is secure by default. Otherwise,
for protocols that are subject to TLS/SSL encryption, a connection may be made secure using
encryption:

• TCP/IP connections are not secure by default, but can be encrypted to make them secure.

• Socket-file connections are secure by default. They can also be encrypted, but encrypting a socket-

file connection makes it no more secure and increases CPU load.

• Named-pipe connections are not secure by default, and are not subject to encryption to make them
secure. However, the named_pipe_full_access_group system variable is available to control
which MySQL users are permitted to use named-pipe connections.

• Shared-memory connections are secure by default.

If the require_secure_transport system variable is enabled, the server permits only connections
that use some form of secure transport. Per the preceding remarks, connections that use TCP/
IP encrypted using TLS/SSL, a socket file, or shared memory are secure connections. TCP/IP
connections not encrypted using TLS/SSL and named-pipe connections are not secure.

See also Configuring Encrypted Connections as Mandatory.

Connection Compression

All transport protocols are subject to use of compression on the traffic between the client and server.
If both compression and encryption are used for a given connection, compression occurs before
encryption. For more information, see Section 6.2.8, “Connection Compression Control”.

6.2.8 Connection Compression Control

Connections to the server can use compression on the traffic between client and server to reduce the
number of bytes sent over the connection. By default, connections are uncompressed, but can be
compressed if the server and the client agree on a mutually permitted compression algorithm.

324

Connection Compression Control

Compressed connections originate on the client side but affect CPU load on both the client and server
sides because both sides perform compression and decompression operations. Because enabling
compression decreases performance, its benefits occur primarily when there is low network bandwidth,
network transfer time dominates the cost of compression and decompression operations, and result
sets are large.

This section describes the available compression-control configuration parameters and the information
sources available for monitoring use of compression. It applies to classic MySQL protocol connections.

Compression control applies to connections to the server by client programs and by servers
participating in source/replica replication or Group Replication. Compression control does not apply
to connections for FEDERATED tables. In the following discussion, “client connection” is shorthand for
a connection to the server originating from any source for which compression is supported, unless
context indicates a specific connection type.

Note

X Protocol connections to a MySQL Server instance support compression,
but compression for X Protocol connections operates independently from the
compression for classic MySQL protocol connections described here, and is
controlled separately. See Section 22.5.5, “Connection Compression with X
Plugin” for information on X Protocol connection compression.

• Configuring Connection Compression

• Configuring Legacy Connection Compression

• Monitoring Connection Compression

Configuring Connection Compression

These configuration parameters are available for controlling connection compression:

• The protocol_compression_algorithms system variable configures which compression

algorithms the server permits for incoming connections.

• The --compression-algorithms and --zstd-compression-level command-line options

configure permitted compression algorithms and zstd compression level for these client programs:
mysql, mysqladmin, mysqlbinlog, mysqlcheck, mysqldump, mysqlimport, mysqlshow,
mysqlslap, and mysqltest. MySQL Shell also offers these command-line options.

• The MYSQL_OPT_COMPRESSION_ALGORITHMS and MYSQL_OPT_ZSTD_COMPRESSION_LEVEL

options for the mysql_options() function configure permitted compression algorithms and zstd
compression level for client programs that use the MySQL C API.

• The SOURCE_COMPRESSION_ALGORITHMS and SOURCE_ZSTD_COMPRESSION_LEVEL options for
the CHANGE REPLICATION SOURCE TO statement configure permitted compression algorithms
and zstd compression level for replica servers participating in source/replica replication.

• The group_replication_recovery_compression_algorithms and

group_replication_recovery_zstd_compression_level system variables configure
permitted compression algorithms and zstd compression level for Group Replication recovery
connections when a new member joins a group and connects to a donor.

Configuration parameters that enable specifying compression algorithms are string-valued and take
a list of one or more comma-separated compression algorithm names, in any order, chosen from the
following items (not case-sensitive):

• zlib: Permit connections that use the zlib compression algorithm.

• zstd: Permit connections that use the zstd compression algorithm.

• uncompressed: Permit uncompressed connections.

325

Connection Compression Control

Note

Because uncompressed is an algorithm name that may or may not be
configured, it is possible to configure MySQL not to permit uncompressed
connections.

Examples:

• To configure which compression algorithms the server permits for incoming connections, set

the protocol_compression_algorithms system variable. By default, the server permits all
available algorithms. To configure that setting explicitly at startup, use these lines in the server
my.cnf file:

[mysqld]
protocol_compression_algorithms=zlib,zstd,uncompressed

To set and persist the protocol_compression_algorithms system variable to that value at
runtime, use this statement:

SET PERSIST protocol_compression_algorithms='zlib,zstd,uncompressed';

SET PERSIST sets a value for the running MySQL instance. It also saves the value, causing it
to carry over to subsequent server restarts. To change the value for the running MySQL instance
without having it carry over to subsequent restarts, use the GLOBAL keyword rather than PERSIST.
See Section 15.7.6.1, “SET Syntax for Variable Assignment”.

• To permit only incoming connections that use zstd compression, configure the server at startup like

this:

[mysqld]
protocol_compression_algorithms=zstd

Or, to make the change at runtime:

SET PERSIST protocol_compression_algorithms='zstd';

• To permit the mysql client to initiate zlib or uncompressed connections, invoke it like this:

mysql --compression-algorithms=zlib,uncompressed

• To configure replicas to connect to the source using zlib or zstd connections, with a compression

level of 7 for zstd connections, use a CHANGE REPLICATION SOURCE TO statement:

CHANGE REPLICATION SOURCE TO
  SOURCE_COMPRESSION_ALGORITHMS = 'zlib,zstd',
  SOURCE_ZSTD_COMPRESSION_LEVEL = 7;

This assumes that the replica_compressed_protocol system variable is disabled, for reasons
described in Configuring Legacy Connection Compression.

For successful connection setup, both sides of the connection must agree on a mutually permitted
compression algorithm. The algorithm-negotiation process attempts to use zlib, then zstd, then
uncompressed. If the two sides can find no common algorithm, the connection attempt fails.

Because both sides must agree on the compression algorithm, and because uncompressed is an
algorithm value that is not necessarily permitted, fallback to an uncompressed connection does not
necessarily occur. For example, if the server is configured to permit zstd and a client is configured to
permit zlib,uncompressed, the client cannot connect at all. In this case, no algorithm is common to
both sides, so connection attempts fail.

Configuration parameters that enable specifying the zstd compression level take an integer value
from 1 to 22, with larger values indicating increasing levels of compression. The default zstd
compression level is 3. The compression level setting has no effect on connections that do not use
zstd compression.

326

Connection Compression Control

A configurable zstd compression level enables choosing between less network traffic and higher
CPU load versus more network traffic and lower CPU load. Higher compression levels reduce network
congestion but the additional CPU load may reduce server performance.

Configuring Legacy Connection Compression

Prior to MySQL 8.0.18, these configuration parameters are available for controlling connection
compression:

• Client programs support a --compress command-line option to specify use of compression for the

connection to the server.

• For programs that use the MySQL C API, enabling the MYSQL_OPT_COMPRESS option for the
mysql_options() function specifies use of compression for the connection to the server.

• For source/replica replication, enabling the system variable replica_compressed_protocol

specifies use of compression for replica connections to the source.

In each case, when use of compression is specified, the connection uses the zlib compression
algorithm if both sides permit it, with fallback to an uncompressed connection otherwise.

As of MySQL 8.0.18, the compression parameters just described become legacy parameters, due to
the additional compression parameters introduced for more control over connection compression that
are described in Configuring Connection Compression. An exception is MySQL Shell, where the --
compress command-line option remains current, and can be used to request compression without
selecting compression algorithms. For information on MySQL Shell's connection compression control,
see Using Compressed Connections.

The legacy compression parameters interact with the newer parameters and their semantics change as
follows:

• The meaning of the legacy --compress option depends on whether --compression-

algorithms is specified:

• When --compression-algorithms is not specified, --compress is equivalent to specifying a

client-side algorithm set of zlib,uncompressed.

• When --compression-algorithms is specified, --compress is equivalent to specifying

an algorithm set of zlib and the full client-side algorithm set is the union of zlib plus
the algorithms specified by --compression-algorithms. For example, with both --
compress and --compression-algorithms=zlib,zstd, the permitted-algorithm
set is zlib plus zlib,zstd; that is, zlib,zstd. With both --compress and --
compression-algorithms=zstd,uncompressed, the permitted-algorithm set is zlib plus
zstd,uncompressed; that is, zlib,zstd,uncompressed.

• The same type of interaction occurs between the legacy MYSQL_OPT_COMPRESS option and the
MYSQL_OPT_COMPRESSION_ALGORITHMS option for the mysql_options() C API function.

• If the replica_compressed_protocol system variable is enabled, it takes precedence over
SOURCE_COMPRESSION_ALGORITHMS and connections to the source use zlib compression if
both source and replica permit that algorithm. If replica_compressed_protocol is disabled, the
value of SOURCE_COMPRESSION_ALGORITHMS applies.

Monitoring Connection Compression

The Compression status variable is ON or OFF to indicate whether the current connection uses
compression.

The mysql client \status command displays a line that says Protocol: Compressed if
compression is enabled for the current connection. If that line is not present, the connection is
uncompressed.

327

Setting Environment Variables

The MySQL Shell \status command displays a Compression: line that says Disabled or
Enabled to indicate whether the connection is compressed.

These additional sources of information are available for monitoring connection compression:

• To monitor compression in use for client connections, use the Compression_algorithm and
Compression_level status variables. For the current connection, their values indicate the
compression algorithm and compression level, respectively.

• To determine which compression algorithms the server is configured to permit for incoming

connections, check the protocol_compression_algorithms system variable.

• For source/replica replication connections, the configured compression algorithms and compression

level are available from multiple sources:

• The Performance Schema replication_connection_configuration table has

COMPRESSION_ALGORITHMS and ZSTD_COMPRESSION_LEVEL columns.

• The mysql.slave_master_info system table has Master_compression_algorithms and
Master_zstd_compression_level columns. If the master.info file exists, it contains lines
for those values as well.

6.2.9 Setting Environment Variables

Environment variables can be set at the command prompt to affect the current invocation of your
command processor, or set permanently to affect future invocations. To set a variable permanently,
you can set it in a startup file or by using the interface provided by your system for this purpose.
Consult the documentation for your command interpreter for specific details. Section 6.9, “Environment
Variables”, lists all environment variables that affect MySQL program operation.

To specify a value for an environment variable, use the syntax appropriate for your command
processor. For example, on Windows, you can set the USER variable to specify your MySQL account
name. To do so, use this syntax:

SET USER=your_name

The syntax on Unix depends on your shell. Suppose that you want to specify the TCP/IP port number
using the MYSQL_TCP_PORT variable. Typical syntax (such as for sh, ksh, bash, zsh, and so on) is as
follows:

MYSQL_TCP_PORT=3306
export MYSQL_TCP_PORT

The first command sets the variable, and the export command exports the variable to the shell
environment so that its value becomes accessible to MySQL and other processes.

For csh and tcsh, use setenv to make the shell variable available to the environment:

setenv MYSQL_TCP_PORT 3306

The commands to set environment variables can be executed at your command prompt to take effect
immediately, but the settings persist only until you log out. To have the settings take effect each time
you log in, use the interface provided by your system or place the appropriate command or commands
in a startup file that your command interpreter reads each time it starts.

On Windows, you can set environment variables using the System Control Panel (under Advanced).

On Unix, typical shell startup files are .bashrc or .bash_profile for bash, or .tcshrc for tcsh.

Suppose that your MySQL programs are installed in /usr/local/mysql/bin and that you want to
make it easy to invoke these programs. To do this, set the value of the PATH environment variable to
include that directory. For example, if your shell is bash, add the following line to your .bashrc file:

328

Server and Server-Startup Programs

PATH=${PATH}:/usr/local/mysql/bin

bash uses different startup files for login and nonlogin shells, so you might want to add the setting to
.bashrc for login shells and to .bash_profile for nonlogin shells to make sure that PATH is set
regardless.

If your shell is tcsh, add the following line to your .tcshrc file:

setenv PATH ${PATH}:/usr/local/mysql/bin

If the appropriate startup file does not exist in your home directory, create it with a text editor.

After modifying your PATH setting, open a new console window on Windows or log in again on Unix so
that the setting goes into effect.

6.3 Server and Server-Startup Programs

This section describes mysqld, the MySQL server, and several programs that are used to start the
server.

6.3.1 mysqld — The MySQL Server

mysqld, also known as MySQL Server, is a single multithreaded program that does most of the work
in a MySQL installation. It does not spawn additional processes. MySQL Server manages access to
the MySQL data directory that contains databases and tables. The data directory is also the default
location for other information such as log files and status files.

Note

Some installation packages contain a debugging version of the server named
mysqld-debug. Invoke this version instead of mysqld for debugging support,
memory allocation checking, and trace file support (see Section 7.9.1.2,
“Creating Trace Files”).

When MySQL server starts, it listens for network connections from client programs and manages
access to databases on behalf of those clients.

The mysqld program has many options that can be specified at startup. For a complete list of options,
run this command:

mysqld --verbose --help

MySQL Server also has a set of system variables that affect its operation as it runs. System variables
can be set at server startup, and many of them can be changed at runtime to effect dynamic server
reconfiguration. MySQL Server also has a set of status variables that provide information about its
operation. You can monitor these status variables to access runtime performance characteristics.

For a full description of MySQL Server command options, system variables, and status variables, see
Section 7.1, “The MySQL Server”. For information about installing MySQL and setting up the initial
configuration, see Chapter 2, Installing MySQL.

6.3.2 mysqld_safe — MySQL Server Startup Script

mysqld_safe is the recommended way to start a mysqld server on Unix. mysqld_safe adds some
safety features such as restarting the server when an error occurs and logging runtime information to
an error log. A description of error logging is given later in this section.

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown.

329

mysqld_safe — MySQL Server Startup Script

On these platforms, mysqld_safe is not installed because it is unnecessary.
For more information, see Section 2.5.9, “Managing MySQL Server with
systemd”.

One implication of the non-use of mysqld_safe on platforms that use systemd
for server management is that use of [mysqld_safe] or [safe_mysqld]
sections in option files is not supported and might lead to unexpected behavior.

mysqld_safe tries to start an executable named mysqld. To override the default behavior and
specify explicitly the name of the server you want to run, specify a --mysqld or --mysqld-version
option to mysqld_safe. You can also use --ledir to indicate the directory where mysqld_safe
should look for the server.

Many of the options to mysqld_safe are the same as the options to mysqld. See Section 7.1.7,
“Server Command Options”.

Options unknown to mysqld_safe are passed to mysqld if they are specified on the command line,
but ignored if they are specified in the [mysqld_safe] group of an option file. See Section 6.2.2.2,
“Using Option Files”.

mysqld_safe reads all options from the [mysqld], [server], and [mysqld_safe] sections in
option files. For example, if you specify a [mysqld] section like this, mysqld_safe finds and uses
the --log-error option:

[mysqld]
log-error=error.log

For backward compatibility, mysqld_safe also reads [safe_mysqld] sections, but to be current you
should rename such sections to [mysqld_safe].

mysqld_safe accepts options on the command line and in option files, as described in the following
table. For information about option files used by MySQL programs, see Section 6.2.2.2, “Using Option
Files”.

Table 6.7 mysqld_safe Options

Option Name

--basedir

--core-file-size

--datadir

--defaults-extra-file

--defaults-file

--help

--ledir

--log-error

--malloc-lib

--mysqld

Description

Path to MySQL installation directory

Size of core file that mysqld should be able to
create

Path to data directory

Read named option file in addition to usual option
files

Read only named option file

Display help message and exit

Path to directory where server is located

Write error log to named file

Alternative malloc library to use for mysqld

Name of server program to start (in ledir directory)

--mysqld-safe-log-timestamps

Timestamp format for logging

--mysqld-version

--nice

--no-defaults

330

Suffix for server program name

Use nice program to set server scheduling priority

Read no option files

mysqld_safe — MySQL Server Startup Script

Description

Number of files that mysqld should be able to
open

Path name of server process ID file

Directory where plugins are installed

Port number on which to listen for TCP/IP
connections

Do not try to kill stray mysqld processes

Do not write error messages to syslog; use error
log file

Socket file on which to listen for Unix socket
connections

Write error messages to syslog

Tag suffix for messages written to syslog

Set TZ time zone environment variable to named
value

Run mysqld as user having name user_name or
numeric user ID user_id

Option Name

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

Command-Line Format

--help

Display a help message and exit.

• --basedir=dir_name

Command-Line Format

Type

The path to the MySQL installation directory.

• --core-file-size=size

--basedir=dir_name

Directory name

Command-Line Format

--core-file-size=size

Type

String

The size of the core file that mysqld should be able to create. The option value is passed to ulimit
-c.

Note

The innodb_buffer_pool_in_core_file variable can be used to
reduce the size of core files on operating systems that support it. For more
information, see Section 17.8.3.7, “Excluding or Including Buffer Pool Pages
from Core Files”.

• --datadir=dir_name

Command-Line Format

Type

--datadir=dir_name

Directory name

331

mysqld_safe — MySQL Server Startup Script

The path to the data directory.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file in addition to the usual option files. If the file does not exist or is otherwise
inaccessible, the server exits with an error. If file_name is not an absolute path name, it is
interpreted relative to the current directory. This must be the first option on the command line if it is
used.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, the server exits
with an error. If file_name is not an absolute path name, it is interpreted relative to the current
directory. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --ledir=dir_name

Command-Line Format

Type

--ledir=dir_name

Directory name

If mysqld_safe cannot find the server, use this option to indicate the path name to the directory
where the server is located.

This option is accepted only on the command line, not in option files. On platforms that use systemd,
the value can be specified in the value of MYSQLD_OPTS. See Section 2.5.9, “Managing MySQL
Server with systemd”.

• --log-error=file_name

Command-Line Format

--log-error=file_name

Type

File name

Write the error log to the given file. See Section 7.4.2, “The Error Log”.

• --mysqld-safe-log-timestamps

Command-Line Format

--mysqld-safe-log-timestamps=type

Type

Default Value

Valid Values

Enumeration

utc

system

332

mysqld_safe — MySQL Server Startup Script

hyphen

legacy

This option controls the format for timestamps in log output produced by mysqld_safe. The
following list describes the permitted values. For any other value, mysqld_safe logs a warning and
uses UTC format.

• UTC, utc

ISO 8601 UTC format (same as --log_timestamps=UTC for the server). This is the default.

• SYSTEM, system

ISO 8601 local time format (same as --log_timestamps=SYSTEM for the server).

• HYPHEN, hyphen

YY-MM-DD h:mm:ss format, as in mysqld_safe for MySQL 5.6.

• LEGACY, legacy

YYMMDD hh:mm:ss format, as in mysqld_safe prior to MySQL 5.6.

• --malloc-lib=[lib_name]

Command-Line Format

--malloc-lib=[lib-name]

Type

String

The name of the library to use for memory allocation instead of the system malloc() library. The
option value must be one of the directories /usr/lib, /usr/lib64, /usr/lib/i386-linux-
gnu, or /usr/lib/x86_64-linux-gnu.

The --malloc-lib option works by modifying the LD_PRELOAD environment value to affect
dynamic linking to enable the loader to find the memory-allocation library when mysqld runs:

• If the option is not given, or is given without a value (--malloc-lib=), LD_PRELOAD is not

modified and no attempt is made to use tcmalloc.

• Prior to MySQL 8.0.21, if the option is given as --malloc-lib=tcmalloc, mysqld_safe looks
for a tcmalloc library in /usr/lib. If tmalloc is found, its path name is added to the beginning

333

mysqld_safe — MySQL Server Startup Script

of the LD_PRELOAD value for mysqld. If tcmalloc is not found, mysqld_safe aborts with an
error.

As of MySQL 8.0.21, tcmalloc is not a permitted value for the --malloc-lib option.

• If the option is given as --malloc-lib=/path/to/some/library, that full path is added to

the beginning of the LD_PRELOAD value. If the full path points to a nonexistent or unreadable file,
mysqld_safe aborts with an error.

• For cases where mysqld_safe adds a path name to LD_PRELOAD, it adds the path to the

beginning of any existing value the variable already has.

Note

On systems that manage the server using systemd, mysqld_safe is not
available. Instead, specify the allocation library by setting LD_PRELOAD in /
etc/sysconfig/mysql.

Linux users can use the libtcmalloc_minimal.so library on any platform for which a tcmalloc
package is installed in /usr/lib by adding these lines to the my.cnf file:

[mysqld_safe]
malloc-lib=tcmalloc

To use a specific tcmalloc library, specify its full path name. Example:

[mysqld_safe]
malloc-lib=/opt/lib/libtcmalloc_minimal.so

• --mysqld=prog_name

Command-Line Format

--mysqld=file_name

Type

File name

The name of the server program (in the ledir directory) that you want to start. This option is
needed if you use the MySQL binary distribution but have the data directory outside of the binary
distribution. If mysqld_safe cannot find the server, use the --ledir option to indicate the path
name to the directory where the server is located.

This option is accepted only on the command line, not in option files. On platforms that use systemd,
the value can be specified in the value of MYSQLD_OPTS. See Section 2.5.9, “Managing MySQL
Server with systemd”.

• --mysqld-version=suffix

Command-Line Format

--mysqld-version=suffix

Type

String

This option is similar to the --mysqld option, but you specify only the suffix for the server
program name. The base name is assumed to be mysqld. For example, if you use --mysqld-
version=debug, mysqld_safe starts the mysqld-debug program in the ledir directory. If the
argument to --mysqld-version is empty, mysqld_safe uses mysqld in the ledir directory.

This option is accepted only on the command line, not in option files. On platforms that use systemd,
the value can be specified in the value of MYSQLD_OPTS. See Section 2.5.9, “Managing MySQL
Server with systemd”.

334

mysqld_safe — MySQL Server Startup Script

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

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read. This must be the first option on
the command line if it is used.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

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

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The path name of the plugin directory.

• --port=port_num

Command-Line Format

Type

--port=number

Numeric

335

The port number that the server should use when listening for TCP/IP connections. The port number

must be 1024 or higher unless the server is started by the root operating system user.

mysqld_safe — MySQL Server Startup Script

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

--syslog causes error messages to be sent to syslog on systems that support the logger
program. --skip-syslog suppresses the use of syslog; messages are written to an error log file.

When syslog is used for error logging, the daemon.err facility/severity is used for all log
messages.

Using these options to control mysqld logging is deprecated. To write error log output to the system
log, use the instructions at Section 7.4.2.8, “Error Logging to the System Log”. To control the facility,
use the server log_syslog_facility system variable.

• --syslog-tag=tag

Command-Line Format

Deprecated

--syslog-tag=tag

Yes

For logging to syslog, messages from mysqld_safe and mysqld are written with identifiers of
mysqld_safe and mysqld, respectively. To specify a suffix for the identifiers, use --syslog-
tag=tag, which modifies the identifiers to be mysqld_safe-tag and mysqld-tag.

Using this option to control mysqld logging is deprecated. Use the server log_syslog_tag system
variable instead. See Section 7.4.2.8, “Error Logging to the System Log”.

• --timezone=timezone

336

Command-Line Format

--timezone=timezone

Type

String

Set the TZ time zone environment variable to the given option value. Consult your operating system

documentation for legal time zone specification formats.

mysqld_safe — MySQL Server Startup Script

• --user={user_name|user_id}

Command-Line Format

--user={user_name|user_id}

Type

Type

String

Numeric

Run the mysqld server as the user having the name user_name or the numeric user ID user_id.
(“User” in this context refers to a system login account, not a MySQL user listed in the grant tables.)

If you execute mysqld_safe with the --defaults-file or --defaults-extra-file option to
name an option file, the option must be the first one given on the command line or the option file is not
used. For example, this command does not use the named option file:

mysql> mysqld_safe --port=port_num --defaults-file=file_name

Instead, use the following command:

mysql> mysqld_safe --defaults-file=file_name --port=port_num

The mysqld_safe script is written so that it normally can start a server that was installed from either
a source or a binary distribution of MySQL, even though these types of distributions typically install the
server in slightly different locations. (See Section 2.1.5, “Installation Layouts”.) mysqld_safe expects
one of the following conditions to be true:

• The server and databases can be found relative to the working directory (the directory from which

mysqld_safe is invoked). For binary distributions, mysqld_safe looks under its working directory
for bin and data directories. For source distributions, it looks for libexec and var directories. This
condition should be met if you execute mysqld_safe from your MySQL installation directory (for
example, /usr/local/mysql for a binary distribution).

• If the server and databases cannot be found relative to the working directory, mysqld_safe

attempts to locate them by absolute path names. Typical locations are /usr/local/libexec
and /usr/local/var. The actual locations are determined from the values configured into the
distribution at the time it was built. They should be correct if MySQL is installed in the location
specified at configuration time.

Because mysqld_safe tries to find the server and databases relative to its own working directory,
you can install a binary distribution of MySQL anywhere, as long as you run mysqld_safe from the
MySQL installation directory:

cd mysql_installation_directory
bin/mysqld_safe &

If mysqld_safe fails, even when invoked from the MySQL installation directory, specify the --ledir
and --datadir options to indicate the directories in which the server and databases are located on
your system.

mysqld_safe tries to use the sleep and date system utilities to determine how many times per
second it has attempted to start. If these utilities are present and the attempted starts per second is
greater than 5, mysqld_safe waits 1 full second before starting again. This is intended to prevent
excessive CPU usage in the event of repeated failures. (Bug #11761530, Bug #54035)

When you use mysqld_safe to start mysqld, mysqld_safe arranges for error (and notice)
messages from itself and from mysqld to go to the same destination.

There are several mysqld_safe options for controlling the destination of these messages:

• --log-error=file_name: Write error messages to the named error file.

• --syslog: Write error messages to syslog on systems that support the logger program.

337

mysql.server — MySQL Server Startup Script

• --skip-syslog: Do not write error messages to syslog. Messages are written to the default error

log file (host_name.err in the data directory), or to a named file if the --log-error option is
given.

If none of these options is given, the default is --skip-syslog.

When mysqld_safe writes a message, notices go to the logging destination (syslog or the error log
file) and stdout. Errors go to the logging destination and stderr.

Note

Controlling mysqld logging from mysqld_safe is deprecated. Use the server's
native syslog support instead. For more information, see Section 7.4.2.8,
“Error Logging to the System Log”.

6.3.3 mysql.server — MySQL Server Startup Script

MySQL distributions on Unix and Unix-like system include a script named mysql.server, which starts
the MySQL server using mysqld_safe. It can be used on systems such as Linux and Solaris that use
System V-style run directories to start and stop system services. It is also used by the macOS Startup
Item for MySQL.

mysql.server is the script name as used within the MySQL source tree. The installed name might be
different (for example, mysqld or mysql). In the following discussion, adjust the name mysql.server
as appropriate for your system.

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown.
On these platforms, mysql.server and mysqld_safe are not installed
because they are unnecessary. For more information, see Section 2.5.9,
“Managing MySQL Server with systemd”.

To start or stop the server manually using the mysql.server script, invoke it from the command line
with start or stop arguments:

mysql.server start
mysql.server stop

mysql.server changes location to the MySQL installation directory, then invokes mysqld_safe.
To run the server as some specific user, add an appropriate user option to the [mysqld] group of
the global /etc/my.cnf option file, as shown later in this section. (It is possible that you must edit
mysql.server if you've installed a binary distribution of MySQL in a nonstandard location. Modify it
to change location into the proper directory before it runs mysqld_safe. If you do this, your modified
version of mysql.server may be overwritten if you upgrade MySQL in the future; make a copy of
your edited version that you can reinstall.)

mysql.server stop stops the server by sending a signal to it. You can also stop the server
manually by executing mysqladmin shutdown.

To start and stop MySQL automatically on your server, you must add start and stop commands to the
appropriate places in your /etc/rc* files:

• If you use the Linux server RPM package (MySQL-server-VERSION.rpm), or a native Linux

package installation, the mysql.server script may be installed in the /etc/init.d directory with
the name mysqld or mysql. See Section 2.5.4, “Installing MySQL on Linux Using RPM Packages
from Oracle”, for more information on the Linux RPM packages.

• If you install MySQL from a source distribution or using a binary distribution format that does not
install mysql.server automatically, you can install the script manually. It can be found in the
support-files directory under the MySQL installation directory or in a MySQL source tree. Copy
the script to the /etc/init.d directory with the name mysql and make it executable:

338

mysql.server — MySQL Server Startup Script

cp mysql.server /etc/init.d/mysql
chmod +x /etc/init.d/mysql

After installing the script, the commands needed to activate it to run at system startup depend on
your operating system. On Linux, you can use chkconfig:

chkconfig --add mysql

On some Linux systems, the following command also seems to be necessary to fully enable the
mysql script:

chkconfig --level 345 mysql on

• On FreeBSD, startup scripts generally should go in /usr/local/etc/rc.d/. Install the

mysql.server script as /usr/local/etc/rc.d/mysql.server.sh to enable automatic
startup. The rc(8) manual page states that scripts in this directory are executed only if their base
name matches the *.sh shell file name pattern. Any other files or directories present within the
directory are silently ignored.

• As an alternative to the preceding setup, some operating systems also use /etc/rc.local or /
etc/init.d/boot.local to start additional services on startup. To start up MySQL using this
method, append a command like the one following to the appropriate startup file:

/bin/sh -c 'cd /usr/local/mysql; ./bin/mysqld_safe --user=mysql &'

• For other systems, consult your operating system documentation to see how to install startup scripts.

mysql.server reads options from the [mysql.server] and [mysqld] sections of option files. For
backward compatibility, it also reads [mysql_server] sections, but to be current you should rename
such sections to [mysql.server].

You can add options for mysql.server in a global /etc/my.cnf file. A typical my.cnf file might
look like this:

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

Table 6.8 mysql.server Option-File Options

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

service-startup-timeout How long to wait for server

Integer

startup

• basedir=dir_name

The path to the MySQL installation directory.

339

mysqld_multi — Manage Multiple MySQL Servers

• datadir=dir_name

The path to the MySQL data directory.

• pid-file=file_name

The path name of the file in which the server should write its process ID. The server creates the file
in the data directory unless an absolute path name is given to specify a different directory.

If this option is not given, mysql.server uses a default value of host_name.pid. The PID file
value passed to mysqld_safe overrides any value specified in the [mysqld_safe] option file
group. Because mysql.server reads the [mysqld] option file group but not the [mysqld_safe]
group, you can ensure that mysqld_safe gets the same value when invoked from mysql.server
as when invoked manually by putting the same pid-file setting in both the [mysqld_safe] and
[mysqld] groups.

• service-startup-timeout=seconds

How long in seconds to wait for confirmation of server startup. If the server does not start within this
time, mysql.server exits with an error. The default value is 900. A value of 0 means not to wait at
all for startup. Negative values mean to wait forever (no timeout).

6.3.4 mysqld_multi — Manage Multiple MySQL Servers

mysqld_multi is designed to manage several mysqld processes that listen for connections on
different Unix socket files and TCP/IP ports. It can start or stop servers, or report their current status.

Note

For some Linux platforms, MySQL installation from RPM or Debian packages
includes systemd support for managing MySQL server startup and shutdown.
On these platforms, mysqld_multi is not installed because it is unnecessary.
For information about using systemd to handle multiple MySQL instances, see
Section 2.5.9, “Managing MySQL Server with systemd”.

mysqld_multi searches for groups named [mysqldN] in my.cnf (or in the file named by the --
defaults-file option). N can be any positive integer. This number is referred to in the following
discussion as the option group number, or GNR. Group numbers distinguish option groups from one
another and are used as arguments to mysqld_multi to specify which servers you want to start,
stop, or obtain a status report for. Options listed in these groups are the same that you would use in the
[mysqld] group used for starting mysqld. (See, for example, Section 2.9.5, “Starting and Stopping
MySQL Automatically”.) However, when using multiple servers, it is necessary that each one use its
own value for options such as the Unix socket file and TCP/IP port number. For more information on
which options must be unique per server in a multiple-server environment, see Section 7.8, “Running
Multiple MySQL Instances on One Machine”.

To invoke mysqld_multi, use the following syntax:

mysqld_multi [options] {start|stop|reload|report} [GNR[,GNR] ...]

start, stop, reload (stop and restart), and report indicate which operation to perform. You can
perform the designated operation for a single server or multiple servers, depending on the GNR list that
follows the option name. If there is no list, mysqld_multi performs the operation for all servers in the
option file.

Each GNR value represents an option group number or range of group numbers. The value should be
the number at the end of the group name in the option file. For example, the GNR for a group named
[mysqld17] is 17. To specify a range of numbers, separate the first and last numbers by a dash. The
GNR value 10-13 represents groups [mysqld10] through [mysqld13]. Multiple groups or group
ranges can be specified on the command line, separated by commas. There must be no whitespace
characters (spaces or tabs) in the GNR list; anything after a whitespace character is ignored.

340

mysqld_multi — Manage Multiple MySQL Servers

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

• With --defaults-file=file_name, only the named file is read.

Command-Line Format

--defaults-file=filename

Type

Default Value

File name

[none]

• Otherwise, option files in the standard list of locations are read, including any file named by the --
defaults-extra-file=file_name option, if one is given. (If the option is given multiple times,
the last value is used.)

Command-Line Format

--defaults-extra-file=filename

Type

Default Value

File name

[none]

For additional information about these and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

Option files read are searched for [mysqld_multi] and [mysqldN] option groups. The
[mysqld_multi] group can be used for options to mysqld_multi itself. [mysqldN] groups can be
used for options passed to specific mysqld instances.

The [mysqld] or [mysqld_safe] groups can be used for common options read by all instances
of mysqld or mysqld_safe. You can specify a --defaults-file=file_name option to use a
different configuration file for that instance, in which case the [mysqld] or [mysqld_safe] groups
from that file are used for that instance.

mysqld_multi supports the following options.

• --help

Command-Line Format

Type

Default Value

Display a help message and exit.

--help

Boolean

false

341

mysqld_multi — Manage Multiple MySQL Servers

• --example

Command-Line Format

Type

Default Value

Display a sample option file.

• --log=file_name

Command-Line Format

Type

Default Value

--example

Boolean

false

--log=path

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
the descriptions for these options in Section 6.3.2, “mysqld_safe — MySQL Server Startup Script”.)
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

342

mysqld_multi — Manage Multiple MySQL Servers

Type

Default Value

String

[none]

The password of the MySQL account to use when invoking mysqladmin. Note that the password
value is not optional for this option, unlike for other MySQL programs.

• --silent

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

Connect to each MySQL server through the TCP/IP port instead of the Unix socket file. (If a socket
file is missing, the server might still be running, but accessible only through the TCP/IP port.) By
default, connections are made using the Unix socket file. This option affects stop and report
operations.

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

343

mysqld_multi — Manage Multiple MySQL Servers

• Most important: Before using mysqld_multi be sure that you understand the meanings of the

options that are passed to the mysqld servers and why you would want to have separate mysqld
processes. Beware of the dangers of using multiple mysqld servers with the same data directory.
Use separate data directories, unless you know what you are doing. Starting multiple servers with
the same data directory does not give you extra performance in a threaded system. See Section 7.8,
“Running Multiple MySQL Instances on One Machine”.

Important

Make sure that the data directory for each server is fully accessible to the
Unix account that the specific mysqld process is started as. Do not use
the Unix root account for this, unless you know what you are doing. See
Section 8.1.5, “How to Run MySQL as a Normal User”.

• Make sure that the MySQL account used for stopping the mysqld servers (with the mysqladmin

program) has the same user name and password for each server. Also, make sure that the account
has the SHUTDOWN privilege. If the servers that you want to manage have different user names or
passwords for the administrative accounts, you might want to create an account on each server that
has the same user name and password. For example, you might set up a common multi_admin
account by executing the following commands for each server:

$> mysql -u root -S /tmp/mysql.sock -p
Enter password:
mysql> CREATE USER 'multi_admin'@'localhost' IDENTIFIED BY 'multipass';
mysql> GRANT SHUTDOWN ON *.* TO 'multi_admin'@'localhost';

See Section 8.2, “Access Control and Account Management”. You have to do this for each mysqld
server. Change the connection parameters appropriately when connecting to each one. Note that
the host name part of the account name must permit you to connect as multi_admin from the host
where you want to run mysqld_multi.

• The Unix socket file and the TCP/IP port number must be different for every mysqld. (Alternatively, if
the host has multiple network addresses, you can set the bind_address system variable to cause
different servers to listen to different interfaces.)

• The --pid-file option is very important if you are using mysqld_safe to start mysqld (for
example, --mysqld=mysqld_safe) Every mysqld should have its own process ID file. The
advantage of using mysqld_safe instead of mysqld is that mysqld_safe monitors its mysqld
process and restarts it if the process terminates due to a signal sent using kill -9 or for other
reasons, such as a segmentation fault.

• You might want to use the --user option for mysqld, but to do this you need to run the

mysqld_multi script as the Unix superuser (root). Having the option in the option file doesn't
matter; you just get a warning if you are not the superuser and the mysqld processes are started
under your own Unix account.

The following example shows how you might set up an option file for use with mysqld_multi. The
order in which the mysqld programs are started or stopped depends on the order in which they appear
in the option file. Group numbers need not form an unbroken sequence. The first and fifth [mysqldN]
groups were intentionally omitted from the example to illustrate that you can have “gaps” in the option
file. This gives you more flexibility.

# This is an example of a my.cnf file for mysqld_multi.
# Usually this file is located in home dir ~/.my.cnf or /etc/my.cnf

[mysqld_multi]
mysqld     = /usr/local/mysql/bin/mysqld_safe
mysqladmin = /usr/local/mysql/bin/mysqladmin
user       = multi_admin
password   = my_password

[mysqld2]
socket     = /tmp/mysql.sock2

344

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

See Section 6.2.2.2, “Using Option Files”.

6.4 Installation-Related Programs

The programs in this section are used when installing or upgrading MySQL.

6.4.1 comp_err — Compile MySQL Error Message File

comp_err creates the errmsg.sys file that is used by mysqld to determine the error messages
to display for different error codes. comp_err normally is run automatically when MySQL is built. It
compiles the errmsg.sys file from text-format error information in MySQL source distributions:

The error information comes from the messages_to_error_log.txt and
messages_to_clients.txt files in the share directory.

For more information about defining error messages, see the comments within those files, along with
the errmsg_readme.txt file.

comp_err also generates the mysqld_error.h, mysqld_ername.h, and mysqld_errmsg.h
header files.

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

345

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

Write a debugging log. A typical debug_options string is d:t:O,file_name. The default is
d:t:O,/tmp/comp_err.trace.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

false

Print some debugging information when the program exits.

• --errmsg-file=file_name, -H file_name

Command-Line Format

Type

Default Value

--errmsg-file=name

File name

mysqld_errmsg.h

The name of the error message file. The default is mysqld_errmsg.h.

• --header-file=file_name, -H file_name

Command-Line Format

--header-file=name

Type

Default Value

File name

mysqld_error.h

The name of the error header file. The default is mysqld_error.h.

• --in-file-errlog=file_name, -e file_name

Command-Line Format

Type

Default Value

--in-file-errlog

File name

../share/messages_to_error_log.txt

346

mysql_secure_installation — Improve MySQL Installation Security

The name of the input file that defines error messages intended to be written to the error log. The
default is ../share/messages_to_error_log.txt.

• --in-file-toclient=file_name, -c file_name

Command-Line Format

--in-file-toclient=path

Type

Default Value

File name

../share/messages_to_clients.txt

The name of the input file that defines error messages intended to be written to clients. The default is
../share/messages_to_clients.txt.

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

• --version, -V

Command-Line Format

Type

Default Value

Display version information and exit.

--version

Boolean

false

6.4.2 mysql_secure_installation — Improve MySQL Installation Security

This program enables you to improve the security of your MySQL installation in the following ways:

• You can set a password for root accounts.

• You can remove root accounts that are accessible from outside the local host.

347

mysql_secure_installation — Improve MySQL Installation Security

• You can remove anonymous-user accounts.

• You can remove the test database (which by default can be accessed by all users, even

anonymous users), and privileges that permit anyone to access databases with names that start with
test_.

mysql_secure_installation helps you implement security recommendations similar to those
described at Section 2.9.4, “Securing the Initial MySQL Account”.

Normal usage is to connect to the local MySQL server; invoke mysql_secure_installation
without arguments:

mysql_secure_installation

When executed, mysql_secure_installation prompts you to determine which actions to perform.

The validate_password component can be used for password strength checking. If the plugin is
not installed, mysql_secure_installation prompts the user whether to install it. Any passwords
entered later are checked using the plugin if it is enabled.

Most of the usual MySQL client options such as --host and --port can be used on the command
line and in option files. For example, to connect to the local server over IPv6 using port 3307, use this
command:

mysql_secure_installation --host=::1 --port=3307

mysql_secure_installation supports the following options, which can be specified on the
command line or in the [mysql_secure_installation] and [client] groups of an option file.
For information about option files used by MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.9 mysql_secure_installation Options

Option Name

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--help

--host

--no-defaults

--password

--port

--print-defaults

--protocol

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

348

Description

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Display help message and exit

Host on which MySQL server is located

Read no option files

Accepted but always ignored. Whenever
mysql_secure_installation is invoked, the user is
prompted for a password, regardless

TCP/IP port number for connection

Print default options

Transport protocol to use

Unix socket file or Windows named pipe to use

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

mysql_secure_installation — Improve MySQL Installation Security

Option Name

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tls-ciphersuites

--tls-sni-servername

--tls-version

--use-default

--user

• --help, -?

Description

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

Execute with no user interactivity

MySQL user name to use when connecting to
server

Command-Line Format

--help

Display a help message and exit.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

349

mysql_secure_installation — Improve MySQL Installation Security

Read not only the usual option groups, but also groups with the usual names and a suffix
of str. For example, mysql_secure_installation normally reads the [client] and
[mysql_secure_installation] groups. If this option is given as --defaults-group-
suffix=_other, mysql_secure_installation also reads the [client_other] and
[mysql_secure_installation_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --host=host_name, -h host_name

Command-Line Format

--host

Connect to the MySQL server on the given host.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --password=password, -p password

Command-Line Format

--password=password

Type

Default Value

String

[none]

This option is accepted but ignored. Whether or not this option is used,
mysql_secure_installation always prompts the user for a password.

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

350

mysql_secure_installation — Improve MySQL Installation Security

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

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
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the connection must be a member of the
Windows group specified by the named_pipe_full_access_group system variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

351

mysql_secure_installation — Improve MySQL Installation Security

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

352

mysql_tzinfo_to_sql — Load the Time Zone Tables

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

6.4.3 mysql_tzinfo_to_sql — Load the Time Zone Tables

The mysql_tzinfo_to_sql program loads the time zone tables in the mysql database. It is used
on systems that have a zoneinfo database (the set of files describing time zones). Examples of such
systems are Linux, FreeBSD, Solaris, and macOS. One likely location for these files is the /usr/
share/zoneinfo directory (/usr/share/lib/zoneinfo on Solaris). If your system does not have
a zoneinfo database, you can use the downloadable package described in Section 7.1.15, “MySQL
Server Time Zone Support”.

mysql_tzinfo_to_sql can be invoked several ways:

mysql_tzinfo_to_sql tz_dir
mysql_tzinfo_to_sql tz_file tz_name
mysql_tzinfo_to_sql --leap tz_file

For the first invocation syntax, pass the zoneinfo directory path name to mysql_tzinfo_to_sql and
send the output into the mysql program. For example:

mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql

mysql_tzinfo_to_sql reads your system's time zone files and generates SQL statements from
them. mysql processes those statements to load the time zone tables.

The second syntax causes mysql_tzinfo_to_sql to load a single time zone file tz_file that
corresponds to a time zone name tz_name:

mysql_tzinfo_to_sql tz_file tz_name | mysql -u root mysql

If your time zone needs to account for leap seconds, invoke mysql_tzinfo_to_sql using the third
syntax, which initializes the leap second information. tz_file is the name of your time zone file:

mysql_tzinfo_to_sql --leap tz_file | mysql -u root mysql

After running mysql_tzinfo_to_sql, it is best to restart the server so that it does not continue to
use any previously cached time zone data.

6.5 Client Programs

This section describes client programs that connect to the MySQL server.

6.5.1 mysql — The MySQL Command-Line Client

mysql is a simple SQL shell with input line editing capabilities. It supports interactive and
noninteractive use. When used interactively, query results are presented in an ASCII-table format.
When used noninteractively (for example, as a filter), the result is presented in tab-separated format.
The output format can be changed using command options.

353

mysql — The MySQL Command-Line Client

If you have problems due to insufficient memory for large result sets, use the --quick option.
This forces mysql to retrieve results from the server a row at a time rather than retrieving the
entire result set and buffering it in memory before displaying it. This is done by returning the
result set using the mysql_use_result() C API function in the client/server library rather than
mysql_store_result().

Note

Alternatively, MySQL Shell offers access to the X DevAPI. For details, see
MySQL Shell 8.4.

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

On Unix, the mysql client logs statements executed interactively to a history file. See Section 6.5.1.3,
“mysql Client Logging”.

6.5.1.1 mysql Client Options

mysql supports the following options, which can be specified on the command line or in the [mysql]
and [client] groups of an option file. For information about option files used by MySQL programs,
see Section 6.2.2.2, “Using Option Files”.

Table 6.10 mysql Client Options

Option Name

--auto-rehash

--auto-vertical-output

--batch

--binary-as-hex

--binary-mode

--bind-address

--character-sets-dir

--column-names

--column-type-info

Description

Introduced

Enable automatic rehashing

Enable automatic vertical result
set display

Do not use history file

Display binary values in
hexadecimal notation

Disable \r\n - to - \n translation
and treatment of \0 as end-of-
query

Use specified network interface
to connect to MySQL Server

Directory where character sets
are installed

Write column names in results

Display result set metadata

354

mysql — The MySQL Command-Line Client

Option Name

--commands

--comments

--compress

--compression-algorithms

--connect-expired-password

--connect-timeout

--database

--debug

--debug-check

--debug-info

--default-auth

Description

Introduced

Enable or disable processing of
local mysql client commands

8.4.6

Whether to retain or strip
comments in statements sent to
the server

Compress all information sent
between client and server

Permitted compression
algorithms for connections to
server

Indicate to server that client
can handle expired-password
sandbox mode

Number of seconds before
connection timeout

The database to use

Write debugging log; supported
only if MySQL was built with
debugging support

Print debugging information
when program exits

Print debugging information,
memory, and CPU statistics
when program exits

Authentication plugin to use

--default-character-set

Specify default character set

--defaults-extra-file

--defaults-file

Read named option file in
addition to usual option files

Read only named option file

--defaults-group-suffix

Option group suffix value

--delimiter

--dns-srv-name

--enable-cleartext-plugin

--execute

--force

--get-server-public-key

--help

--histignore

--host

--html

Set the statement delimiter

Use DNS SRV lookup for host
information

Enable cleartext authentication
plugin

Execute the statement and quit

Continue even if an SQL error
occurs

Request RSA public key from
server

Display help message and exit

Patterns specifying which
statements to ignore for logging

Host on which MySQL server is
located

Produce HTML output

355

Option Name

--ignore-spaces

--init-command

--init-command-add

--line-numbers

--load-data-local-dir

--local-infile

--login-path

--max-allowed-packet

--max-join-size

mysql — The MySQL Command-Line Client

Description

Introduced

Ignore spaces after function
names

SQL statement to execute after
connecting

Add an additional SQL statement
to execute after connecting or re-
connecting to MySQL server

Write line numbers for errors

Directory for files named in
LOAD DATA LOCAL statements

Enable or disable for LOCAL
capability for LOAD DATA

Read login path options
from .mylogin.cnf

Maximum packet length to send
to or receive from server

The automatic limit for rows in a
join when using --safe-updates

--named-commands

Enable named mysql commands

--net-buffer-length

Buffer size for TCP/IP and socket
communication

--network-namespace

Specify network namespace

--no-auto-rehash

Disable automatic rehashing

--no-beep

--no-defaults

--no-login-paths

--oci-config-file

--one-database

--pager

--password

--password1

--password2

--password3

356

Do not beep when errors occur

Read no option files

Do not read login paths from the
login path file

Defines an alternate location for
the Oracle Cloud Infrastructure
CLI configuration file.

Ignore statements except those
for the default database named
on the command line

Use the given command for
paging query output

Password to use when
connecting to server

First multifactor authentication
password to use when
connecting to server

Second multifactor authentication
password to use when
connecting to server

Third multifactor authentication
password to use when
connecting to server

mysql — The MySQL Command-Line Client

Option Name

--pipe

--plugin-authentication-kerberos-
client-mode

Description

Introduced

Connect to server using named
pipe (Windows only)

Permit GSSAPI pluggable
authentication through the MIT
Kerberos library on Windows

--plugin-authentication-
webauthn-client-preserve-privacy

Permit user to choose a key to
be used for assertion

--plugin-dir

--port

--print-defaults

--prompt

--protocol

--quick

--raw

--reconnect

--register-factor

Directory where plugins are
installed

TCP/IP port number for
connection

Print default options

Set the prompt to the specified
format

Transport protocol to use

Do not cache each query result

Write column values without
escape conversion

If the connection to the server
is lost, automatically try to
reconnect

Multifactor authentication factors
for which registration must be
done

--safe-updates, --i-am-a-dummy Allow only UPDATE and

--select-limit

--server-public-key-path

--shared-memory-base-name

--show-warnings

--sigint-ignore

DELETE statements that specify
key values

The automatic limit for SELECT
statements when using --safe-
updates

Path name to file containing RSA
public key

Shared-memory name for
shared-memory connections
(Windows only)

Show warnings after each
statement if there are any

Ignore SIGINT signals (typically
the result of typing Control+C)

--silent

Silent mode

--skip-auto-rehash

Disable automatic rehashing

--skip-column-names

Do not write column names in
results

--skip-line-numbers

Skip line numbers for errors

--skip-named-commands

Disable named mysql commands

--skip-pager

--skip-reconnect

Disable paging

Disable reconnecting

357

mysql — The MySQL Command-Line Client

Option Name

Description

Introduced

--skip-system-command

Disable system (\!) command

8.4.3

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

Unix socket file or Windows
named pipe to use

File that contains list of trusted
SSL Certificate Authorities

Directory that contains trusted
SSL Certificate Authority
certificate files

File that contains X.509
certificate

Permissible ciphers for
connection encryption

File that contains certificate
revocation lists

Directory that contains certificate
revocation-list files

Whether to enable FIPS mode
on client side

File that contains X.509 key

Desired security state of
connection to server

File that contains SSL session
data

--ssl-session-data-continue-on-
failed-reuse

Whether to establish connections
if session reuse fails

--syslog

--system-command

--table

--tee

Log interactive statements to
syslog

Enable or disable system (\!)
command

8.4.3

Display output in tabular format

Append a copy of output to
named file

--telemetry_client

Enables the telemetry client.

--
otel_bsp_max_export_batch_size

See variable
OTEL_BSP_MAX_EXPORT_BATCH_SIZE.

--otel_bsp_max_queue_size

--otel_bsp_schedule_delay

See variable
OTEL_BSP_MAX_QUEUE_SIZE.

See variable
OTEL_BSP_SCHEDULE_DELAY.

--
otel_exporter_otlp_traces_certificates

Not in use at this time. Reserved
for future development.

--
otel_exporter_otlp_traces_client_certificates

Not in use at this time. Reserved
for future development.

--
otel_exporter_otlp_traces_client_key

Not in use at this time. Reserved
for future development.

--
otel_exporter_otlp_traces_compression

Compression type

358

mysql — The MySQL Command-Line Client

Option Name

Description

Introduced

--
otel_exporter_otlp_traces_endpoint

The trace export endpoint

--
otel_exporter_otlp_traces_headers

Key-value pairs to be used as
headers associated with HTTP
requests

--
otel_exporter_otlp_traces_protocol

The OTLP transport protocol

--
otel_exporter_otlp_traces_timeout

Time OLTP exporter waits for
each batch export

--otel-help

--otel_log_level

--otel_resource_attributes

--otel-trace

--tls-ciphersuites

--tls-sni-servername

--tls-version

--unbuffered

--user

--verbose

--version

--vertical

--wait

--xml

--zstd-compression-level

• --help, -?

When enabled, prints help about
telemetry_client options.

Controls which opentelemetry
logs are printed in the server logs

See corresponding
OpenTelemetry variable
OTEL_RESOURCE_ATTRIBUTES.

This system variable controls
whether telemetry traces are
collected or not.

Permissible TLSv1.3 ciphersuites
for encrypted connections

Server name supplied by the
client

Permissible TLS protocols for
encrypted connections

Flush the buffer after each query

MySQL user name to use when
connecting to server

Verbose mode

Display version information and
exit

Print query output rows vertically
(one line per column value)

If the connection cannot be
established, wait and retry
instead of aborting

Produce XML output

Compression level for
connections to server that use
zstd compression

Command-Line Format

--help

Display a help message and exit.

359

mysql — The MySQL Command-Line Client

• --auto-rehash

Command-Line Format

Disabled by

--auto-rehash

skip-auto-rehash

Enable automatic rehashing. This option is on by default, which enables database, table, and column
name completion. Use --disable-auto-rehash to disable rehashing. That causes mysql to
start faster, but you must issue the rehash command or its \# shortcut if you want to use name
completion.

To complete a name, enter the first part and press Tab. If the name is unambiguous, mysql
completes it. Otherwise, you can press Tab again to see the possible names that begin with what
you have typed so far. Completion does not occur if there is no default database.

Note

This feature requires a MySQL client that is compiled with the readline
library. Typically, the readline library is not available on Windows.

• --auto-vertical-output

Command-Line Format

--auto-vertical-output

Cause result sets to be displayed vertically if they are too wide for the current window, and using
normal tabular format otherwise. (This applies to statements terminated by ; or \G.)

• --batch, -B

Command-Line Format

--batch

Print results using tab as the column separator, with each row on a new line. With this option, mysql
does not use the history file.

Batch mode results in nontabular output format and escaping of special characters. Escaping may be
disabled by using raw mode; see the description for the --raw option.

• --binary-as-hex

Command-Line Format

Type

Default Value

--binary-as-hex

Boolean

FALSE in noninteractive mode

When this option is given, mysql displays binary data using hexadecimal notation (0xvalue). This
occurs whether the overall output display format is tabular, vertical, HTML, or XML.

--binary-as-hex when enabled affects display of all binary strings, including those returned by
functions such as CHAR() and UNHEX(). The following example demonstrates this using the ASCII
code for A (65 decimal, 41 hexadecimal):

360

• --binary-as-hex disabled:

mysql> SELECT CHAR(0x41), UNHEX('41');
+------------+-------------+
| CHAR(0x41) | UNHEX('41') |

+------------+-------------+

| A          | A           |

mysql — The MySQL Command-Line Client

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

When mysql operates in interactive mode, this option is enabled by default. In addition, output from
the status (or \s) command includes this line when the option is enabled implicitly or explicitly:

Binary data as: Hexadecimal

To disable hexadecimal notation, use --skip-binary-as-hex

• --binary-mode

Command-Line Format

--binary-mode

This option helps when processing mysqlbinlog output that may contain BLOB values. By default,
mysql translates \r\n in statement strings to \n and interprets \0 as the statement terminator.
--binary-mode disables both features. It also disables all mysql commands except charset
and delimiter in noninteractive mode (for input piped to mysql or loaded using the source
command).

(MySQL 8.4.6 and later:) --binary-mode, when enabled, causes the server to disregard any
setting for --commands .

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

361

Command-Line Format

--character-sets-dir=dir_name

mysql — The MySQL Command-Line Client

Type

Directory name

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --column-names

Command-Line Format

--column-names

Write column names in results.

• --column-type-info

Command-Line Format

--column-type-info

Display result set metadata. This information corresponds to the contents of C API MYSQL_FIELD
data structures. See C API Basic Data Structures.

• --commands

Command-Line Format

Introduced

Type

--commands

8.4.6

Boolean

362

mysql — The MySQL Command-Line Client

Default Value

TRUE

Whether to enable or disable processing of local mysql client commands. Setting this option to
FALSE disables such processing, and has the effects listed here:

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

• The \C and delimiter commands remain enabled.

• The --system-command option is ignored, and has no effect.

363

mysql — The MySQL Command-Line Client

This option has no effect when --binary-mode is enabled.

When --commands is enabled, it is possible to disable (only) the system command using the --
system-command option.

This option was added in MySQL 8.4.6.

• --comments, -c

Command-Line Format

Type

Default Value

--comments

Boolean

TRUE

Whether to preserve or strip comments in statements sent to the server. The default is to preserve
them; to strip them, start mysql with --skip-comments.

Note

The mysql client always passes optimizer hints to the server, regardless of
whether this option is given.

Comment stripping is deprecated. Expect this feature and the options to
control it to be removed in a future MySQL release.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

364

For more information, see Section 6.2.8, “Connection Compression Control”.

mysql — The MySQL Command-Line Client

• --connect-expired-password

Command-Line Format

--connect-expired-password

Indicate to the server that the client can handle sandbox mode if the account used to connect has an
expired password. This can be useful for noninteractive invocations of mysql because normally the
server disconnects noninteractive clients that attempt to connect using an account with an expired
password. (See Section 8.2.16, “Server Handling of Expired Passwords”.)

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

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/mysql.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

365

mysql — The MySQL Command-Line Client

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set for the client and connection.

This option can be useful if the operating system uses one character set and the mysql client by
default uses another. In this case, output may be formatted incorrectly. You can usually fix such
issues by using this option to force the client to use the system character set instead.

For more information, see Section 12.4, “Connection Character Sets and Collations”, and
Section 12.15, “Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

366

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

mysql — The MySQL Command-Line Client

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of
str. For example, mysql normally reads the [client] and [mysql] groups. If this option is
given as --defaults-group-suffix=_other, mysql also reads the [client_other] and
[mysql_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --delimiter=str

Command-Line Format

--delimiter=str

Type

Default Value

String

;

Set the statement delimiter. The default is the semicolon character (;).

• --disable-named-commands

Disable named commands. Use the \* form only, or use named commands only at the beginning
of a line ending with a semicolon (;). mysql starts with this option enabled by default. However,
even with this option, long-format commands still work from the first line. See Section 6.5.1.2, “mysql
Client Commands”.

• --dns-srv-name=name

Command-Line Format

--dns-srv-name=name

Type

String

Specifies the name of a DNS SRV record that determines the candidate hosts to use for establishing
a connection to a MySQL server. For information about DNS SRV support in MySQL, see
Section 6.2.6, “Connecting to the Server Using DNS SRV Records”.

Suppose that DNS is configured with this SRV information for the example.com domain:

Name                     TTL   Class   Priority Weight Port Target
_mysql._tcp.example.com. 86400 IN SRV  0        5      3306 host1.example.com
_mysql._tcp.example.com. 86400 IN SRV  0        10     3306 host2.example.com
_mysql._tcp.example.com. 86400 IN SRV  10       5      3306 host3.example.com
_mysql._tcp.example.com. 86400 IN SRV  20       5      3306 host4.example.com

To use that DNS SRV record, invoke mysql like this:

mysql --dns-srv-name=_mysql._tcp.example.com

mysql then attempts a connection to each server in the group until a successful connection is
established. A failure to connect occurs only if a connection cannot be established to any of the

367

mysql — The MySQL Command-Line Client

servers. The priority and weight values in the DNS SRV record determine the order in which servers
should be tried.

When invoked with --dns-srv-name, mysql attempts to establish TCP connections only.

The --dns-srv-name option takes precedence over the --host option if both are given. --dns-
srv-name causes connection establishment to use the mysql_real_connect_dns_srv() C API
function rather than mysql_real_connect(). However, if the connect command is subsequently
used at runtime and specifies a host name argument, that host name takes precedence over any --
dns-srv-name option given at mysql startup to specify a DNS SRV record.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

• --execute=statement, -e statement

Command-Line Format

--execute=statement

Type

String

Execute the statement and quit. The default output format is like that produced with --batch. See
Section 6.2.2.1, “Using Options on the Command Line”, for some examples. With this option, mysql
does not use the history file.

• --force, -f

Command-Line Format

--force

Continue even if an SQL error occurs.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

368

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

mysql — The MySQL Command-Line Client

• --histignore

Command-Line Format

--histignore=pattern_list

Type

String

A list of one or more colon-separated patterns specifying statements to ignore for logging purposes.
These patterns are added to the default pattern list ("*IDENTIFIED*:*PASSWORD*"). The value
specified for this option affects logging of statements written to the history file, and to syslog if the
--syslog option is given. For more information, see Section 6.5.1.3, “mysql Client Logging”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Connect to the MySQL server on the given host.

The --dns-srv-name option takes precedence over the --host option if both are given. --dns-
srv-name causes connection establishment to use the mysql_real_connect_dns_srv() C API
function rather than mysql_real_connect(). However, if the connect command is subsequently
used at runtime and specifies a host name argument, that host name takes precedence over any --
dns-srv-name option given at mysql startup to specify a DNS SRV record.

• --html, -H

Command-Line Format

--html

Produce HTML output.

• --ignore-spaces, -i

Command-Line Format

--ignore-spaces

Ignore spaces after function names. The effect of this is described in the discussion for the
IGNORE_SPACE SQL mode (see Section 7.1.11, “Server SQL Modes”).

• --init-command=str

Command-Line Format

--init-command=str

Single SQL statement to execute after connecting to the server. If auto-reconnect is enabled, the
statement is executed again after reconnection occurs. The definition resets existing statements
defined by it or init-command-add.

• --init-command-add=str

369

Command-Line Format

--init-command-add=str

Add an additional SQL statement to execute after connecting or reconnecting to the MySQL server.

It's usable without --init-command but has no effect if used before it because init-command

resets the list of commands to call.

mysql — The MySQL Command-Line Client

• --line-numbers

Command-Line Format

Disabled by

--line-numbers

skip-line-numbers

Write line numbers for errors. Disable this with --skip-line-numbers.

• --load-data-local-dir=dir_name

Command-Line Format

--load-data-local-dir=dir_name

Type

Default Value

Directory name

empty string

This option affects the client-side LOCAL capability for LOAD DATA operations. It specifies the
directory in which files named in LOAD DATA LOCAL statements must be located. The effect of --
load-data-local-dir depends on whether LOCAL data loading is enabled or disabled:

• If LOCAL data loading is enabled, either by default in the MySQL client library or by specifying --

local-infile[=1], the --load-data-local-dir option is ignored.

• If LOCAL data loading is disabled, either by default in the MySQL client library or by specifying --

local-infile=0, the --load-data-local-dir option applies.

When --load-data-local-dir applies, the option value designates the directory in which local
data files must be located. Comparison of the directory path name and the path name of files to be
loaded is case-sensitive regardless of the case sensitivity of the underlying file system. If the option
value is the empty string, it names no directory, with the result that no files are permitted for local
data loading.

For example, to explicitly disable local data loading except for files located in the /my/local/data
directory, invoke mysql like this:

mysql --local-infile=0 --load-data-local-dir=/my/local/data

When both --local-infile and --load-data-local-dir are given, the order in which they
are given does not matter.

Successful use of LOCAL load operations within mysql also requires that the server permits local
loading; see Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”

• --local-infile[={0|1}]

Command-Line Format

--local-infile[={0|1}]

Type

Default Value

Boolean

FALSE

By default, LOCAL capability for LOAD DATA is determined by the default compiled into the MySQL
client library. To enable or disable LOCAL data loading explicitly, use the --local-infile option.
When given with no value, the option enables LOCAL data loading. When given as --local-
infile=0 or --local-infile=1, the option disables or enables LOCAL data loading.

If LOCAL capability is disabled, the --load-data-local-dir option can be used to permit
restricted local loading of files located in a designated directory.

Successful use of LOCAL load operations within mysql also requires that the server permits local
loading; see Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”

370

mysql — The MySQL Command-Line Client

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --max-allowed-packet=value

Command-Line Format

--max-allowed-packet=value

Type

Default Value

Numeric

16777216

The maximum size of the buffer for client/server communication. The default is 16MB, the maximum
is 1GB.

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
commands. For example, quit and \q both are recognized. Use --skip-named-commands to
disable named commands. See Section 6.5.1.2, “mysql Client Commands”.

• --net-buffer-length=value

Command-Line Format

--net-buffer-length=value

371

mysql — The MySQL Command-Line Client

Type

Default Value

Numeric

16384

The buffer size for TCP/IP and socket communication. (Default value is 16KB.)

• --network-namespace=name

Command-Line Format

--network-namespace=name

Type

String

The network namespace to use for TCP/IP connections. If omitted, the connection uses the default
(global) namespace. For information about network namespaces, see Section 7.1.14, “Network
Namespace Support”.

This option is available only on platforms that implement network namespace support.

• --no-auto-rehash, -A

Command-Line Format

Deprecated

--no-auto-rehash

Yes

This has the same effect as --skip-auto-rehash. See the description for --auto-rehash.

• --no-beep, -b

Command-Line Format

--no-beep

Do not beep when errors occur.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --oci-config-file=PATH

372

Command-Line Format

Type

Default Value

--oci-config-file

String

Alternate path to the Oracle Cloud Infrastructure CLI configuration file. Specify the location of the

configuration file. If your existing default profile is the correct one, you do not need to specify this

mysql — The MySQL Command-Line Client

option. However, if you have an existing configuration file, with multiple profiles or a different default
from the tenancy of the user you want to connect with, specify this option.

• --one-database, -o

Command-Line Format

--one-database

Ignore statements except those that occur while the default database is the one named on the
command line. This option is rudimentary and should be used with care. Statement filtering is based
only on USE statements.

Initially, mysql executes statements in the input because specifying a database db_name on the
command line is equivalent to inserting USE db_name at the beginning of the input. Then, for each
USE statement encountered, mysql accepts or rejects following statements depending on whether
the database named is the one on the command line. The content of the statements is immaterial.

Suppose that mysql is invoked to process this set of statements:

DELETE FROM db2.t2;
USE db2;
DROP TABLE db1.t1;
CREATE TABLE db1.t1 (i INT);
USE db1;
INSERT INTO t1 (i) VALUES(1);
CREATE TABLE db2.t1 (j INT);

If the command line is mysql --force --one-database db1, mysql handles the input as
follows:

• The DELETE statement is executed because the default database is db1, even though the

statement names a table in a different database.

• The DROP TABLE and CREATE TABLE statements are not executed because the default database

is not db1, even though the statements name a table in db1.

• The INSERT and CREATE TABLE statements are executed because the default database is db1,

even though the CREATE TABLE statement names a table in a different database.

• --pager[=command]

Command-Line Format

--pager[=command]

Disabled by

Type

skip-pager

String

Use the given command for paging query output. If the command is omitted, the default pager is the
value of your PAGER environment variable. Valid pagers are less, more, cat [> filename],
and so forth. This option works only on Unix and only in interactive mode. To disable paging, use --
skip-pager. Section 6.5.1.2, “mysql Client Commands”, discusses output paging further.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value
is optional. If not given, mysql prompts for one. If given, there must be no space between --

373

mysql — The MySQL Command-Line Client

password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysql should not prompt for one, use the --
skip-password option.

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the
server. The password value is optional. If not given, mysql prompts for one. If given, there must be
no space between --password1= and the password following it. If no password option is specified,
the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysql should not prompt for one, use the --
skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-authentication-kerberos-client-mode=value

Command-Line Format

Type

Default Value

Valid Values

--plugin-authentication-kerberos-
client-mode

String

SSPI

GSSAPI

SSPI

374

mysql — The MySQL Command-Line Client

On Windows, the authentication_kerberos_client authentication plugin supports this plugin
option. It provides two possible values that the client user can set at runtime: SSPI and GSSAPI.

The default value for the client-side plugin option uses Security Support Provider Interface (SSPI),
which is capable of acquiring credentials from the Windows in-memory cache. Alternatively, the
client user can select a mode that supports Generic Security Service Application Program Interface
(GSSAPI) through the MIT Kerberos library on Windows. GSSAPI is capable of acquiring cached
credentials previously generated by using the kinit command.

For more information, see Commands for Windows Clients in GSSAPI Mode.

• --plugin-authentication-webauthn-client-preserve-privacy={OFF|ON}

Command-Line Format

Type

Default Value

--plugin-authentication-webauthn-
client-preserve-privacy

Boolean

OFF

Determines how assertions are sent to server in case there is more than one discoverable credential
stored for a given RP ID (a unique name given to the relying-party server, which is the MySQL
server). If the FIDO2 device contains multiple resident keys for a given RP ID, this option allows the
user to choose a key to be used for assertion. It provides two possible values that the client user can
set. The default value is OFF. If set to OFF, the challenge is signed by all credentials available for a
given RP ID and all signatures are sent to server. If set to ON, the user is prompted to choose the
credential to be used for signature.

Note

This option has no effect if the device does not support the resident-key
feature.

For more information, see Section 8.4.1.11, “WebAuthn Pluggable Authentication”.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is
used to specify an authentication plugin but mysql does not find it. See Section 8.2.17, “Pluggable
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

375

mysql — The MySQL Command-Line Client

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --prompt=format_str

Command-Line Format

--prompt=format_str

Type

Default Value

String

mysql>

Set the prompt to the specified format. The default is mysql>. The special sequences that the
prompt can contain are described in Section 6.5.1.2, “mysql Client Commands”.

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
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --quick, -q

Command-Line Format

--quick

Do not cache each query result, print each row as it is received. This may slow down the server if the
output is suspended. With this option, mysql does not use the history file.

By default, mysql fetches all result rows before producing any output; while storing these, it
calculates a running maximum column length from the actual value of each column in succession.
When printing the output, it uses this maximum to format it. When --quick is specified, mysql
does not have the rows for which to calculate the length before starting, and so uses the maximum
length. In the following example, table t1 has a single column of type BIGINT and containing 4
rows. The default output is 9 characters wide; this width is equal the maximum number of characters
in any of the column values in the rows returned (5), plus 2 characters each for the spaces used
as padding and the | characters used as column delimiters). The output when using the --
quick option is 25 characters wide; this is equal to the number of characters needed to represent
-9223372036854775808, which is the longest possible value that can be stored in a (signed)
BIGINT column, or 19 characters, plus the 4 characters used for padding and column delimiters.
The difference can be seen here:

376

$> mysql -t test -e "SELECT * FROM t1"
+-------+
| c1    |
+-------+

mysql — The MySQL Command-Line Client

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
another. For nontabular output (such as is produced in batch mode or when the --batch or --
silent option is given), special characters are escaped in the output so they can be identified
easily. Newline, tab, NUL, and backslash are written as \n, \t, \0, and \\. The --raw option
disables this character escaping.

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

Disabled by

--reconnect

skip-reconnect

If the connection to the server is lost, automatically try to reconnect. A single reconnect attempt
is made each time the connection is lost. To suppress reconnection behavior, use --skip-
reconnect.

• --register-factor=value

Command-Line Format

--register-factor=value

377

mysql — The MySQL Command-Line Client

Type

String

The factor or factors for which FIDO/FIDO2 device registration must be performed before WebAuthn
device-based authentication can be used. This option value must be a single value, or two values
separated by commas. Each value must be 2 or 3, so the permitted option values are '2', '3',
'2,3' and '3,2'.

For example, an account that requires registration for a third authentication factor invokes the mysql
client as follows:

mysql --user=user_name --register-factor=3

An account that requires registration for second and third authentication factors invokes the mysql
client as follows:

mysql --user=user_name --register-factor=2,3

If registration is successful, a connection is established. If there is an authentication factor with a
pending registration, a connection is placed into pending registration mode when attempting to
connect to the server. In this case, disconnect and reconnect with the correct --register-factor
value to complete the registration.

Registration is a two-step process comprising initiate registration and finish registration steps. The
initiate registration step executes this statement:

ALTER USER user factor INITIATE REGISTRATION

The statement returns a result set containing a 32 byte challenge, the user name, and the relying
party ID (see authentication_webauthn_rp_id).

The finish registration step executes this statement:

ALTER USER user factor FINISH REGISTRATION SET CHALLENGE_RESPONSE AS 'auth_string'

The statement completes the registration and sends the following information to the server as part
of the auth_string: authenticator data, an optional attestation certificate in X.509 format, and a
signature.

The initiate and registration steps must be performed in a single connection, as the challenge
received by the client during the initiate step is saved to the client connection handler. Registration
would fail if the registration step was performed by a different connection. The --register-
factor option executes both the initiate and registration steps, which avoids the failure scenario
described above and prevents having to execute the ALTER USER initiate and registration
statements manually.

The --register-factor option is only available for the mysql and MySQL Shell clients. Other
MySQL client programs do not support it.

For related information, see Using WebAuthn Authentication.

• --safe-updates, --i-am-a-dummy, -U

Command-Line Format

Type

378

--safe-updates

--i-am-a-dummy

Boolean

mysql — The MySQL Command-Line Client

Default Value

FALSE

If this option is enabled, UPDATE and DELETE statements that do not use a key in the WHERE clause
or a LIMIT clause produce an error. In addition, restrictions are placed on SELECT statements that
produce (or are estimated to produce) very large result sets. If you have set this option in an option
file, you can use --skip-safe-updates on the command line to override it. For more information
about this option, see Using Safe-Updates Mode (--safe-updates).

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

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --show-warnings

Command-Line Format

--show-warnings

Cause warnings to be shown after each statement if there are any. This option applies to interactive
and batch mode.

379

mysql — The MySQL Command-Line Client

• --sigint-ignore

Command-Line Format

--sigint-ignore

Ignore SIGINT signals (typically the result of typing Control+C).

Without this option, typing Control+C interrupts the current statement if there is one, or cancels any
partial input line otherwise.

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

Do not write column names in results. Use of this option causes the output to be right-aligned, as
shown here:

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

• --skip-system-command

Command-Line Format

Introduced

--skip-system-command

8.4.3

Disables the system (\!) command. Equivalent to --system-command=OFF.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

380

mysql — The MySQL Command-Line Client

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --syslog, -j

Command-Line Format

--syslog

This option causes mysql to send interactive statements to the system logging facility. On Unix,
this is syslog; on Windows, it is the Windows Event Log. The destination where logged messages
appear is system dependent. On Linux, the destination is often the /var/log/messages file.

Here is a sample of output generated on Linux by using --syslog. This output is formatted for
readability; each logged message actually takes a single line.

381

mysql — The MySQL Command-Line Client

Mar  7 12:39:25 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
  DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
Mar  7 12:39:28 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
  DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'

For more information, see Section 6.5.1.3, “mysql Client Logging”.

• --system-command[={ON|OFF}]

Command-Line Format

--system-command[={ON|OFF}]

Introduced

Disabled by

Type

Default Value

8.4.3

skip-system-command

Boolean

ON

Enable or disable the system (\!) command. When this option is disabled, either by --system-
command=OFF or by --skip-system-command, the system command is rejected with an error.

(MySQL 8.4.6 and later:) --commands, when disabled (set to FALSE), causes the server to
disregard any setting for this option.

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

Append a copy of output to the given file. This option works only in interactive mode. Section 6.5.1.2,
“mysql Client Commands”, discusses tee files further.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

382

Command-Line Format

--tls-sni-servername=server_name

mysql — The MySQL Command-Line Client

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

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

Verbose mode. Produce more output about what the program does. This option can be given
multiple times to produce more and more output. (For example, -v -v -v produces table output
format even in batch mode.)

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --vertical, -E

383

mysql — The MySQL Command-Line Client

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

The output when --xml is used with mysql matches that of mysqldump --xml. See Section 6.5.4,
“mysqldump — A Database Backup Program”, for details.

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

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

384

mysql — The MySQL Command-Line Client

• telemetry_client

Command-Line Format

--telemetry_client

Type

Default Value

Boolean

OFF

Enables the telemetry client plugin (Linux only).

For more information, see Chapter 35, Telemetry.

6.5.1.2 mysql Client Commands

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
query_attributes Sets string parameters (name1 value1 name2 value2 ...)
for the next query to pick up.
ssl_session_data_print Serializes the current SSL session data to stdout
or file.

For server side help, type 'help contents'

If mysql is invoked with the --binary-mode option, all mysql commands are disabled except
charset and delimiter in noninteractive mode (for input piped to mysql or loaded using the
source command). Beginning with MySQL 8.4.6, the --commands option can be used to enable or
disable all commands except /C, delimiter, and use.

Each command has both a long and short form. The long form is not case-sensitive; the short form is.
The long form can be followed by an optional semicolon terminator, but the short form should not.

The use of short-form commands within multiple-line /* ... */ comments is not supported. Short-
form commands do work within single-line /*! ... */ version comments, as do /*+ ... */
optimizer-hint comments, which are stored in object definitions. If there is a concern that optimizer-
hint comments may be stored in object definitions so that dump files when reloaded with mysql would

385

mysql — The MySQL Command-Line Client

result in execution of such commands, either invoke mysql with the --binary-mode option or use a
reload client other than mysql.

•   help [arg], \h [arg], \? [arg], ? [arg]

Display a help message listing the available mysql commands.

If you provide an argument to the help command, mysql uses it as a search string to access
server-side help from the contents of the MySQL Reference Manual. For more information, see
Section 6.5.1.4, “mysql Client Server-Side Help”.

•   charset charset_name, \C charset_name

Change the default character set and issue a SET NAMES statement. This enables the character set
to remain synchronized on the client and server if mysql is run with auto-reconnect enabled (which
is not recommended), because the specified character set is used for reconnects.

•   clear, \c

Clear the current input. Use this if you change your mind about executing the statement that you are
entering.

•   connect [db_name [host_name]], \r [db_name [host_name]]

Reconnect to the server. The optional database name and host name arguments may be given to
specify the default database or the host where the server is running. If omitted, the current values are
used.

If the connect command specifies a host name argument, that host takes precedence over any --
dns-srv-name option given at mysql startup to specify a DNS SRV record.

•   delimiter str, \d str

Change the string that mysql interprets as the separator between SQL statements. The default is
the semicolon character (;).

The delimiter string can be specified as an unquoted or quoted argument on the delimiter
command line. Quoting can be done with either single quote ('), double quote ("), or backtick (`)
characters. To include a quote within a quoted string, either quote the string with a different quote
character or escape the quote with a backslash (\) character. Backslash should be avoided outside
of quoted strings because it is the escape character for MySQL. For an unquoted argument, the
delimiter is read up to the first space or end of line. For a quoted argument, the delimiter is read up to
the matching quote on the line.

mysql interprets instances of the delimiter string as a statement delimiter anywhere it occurs, except
within quoted strings. Be careful about defining a delimiter that might occur within other words. For
example, if you define the delimiter as X, it is not possible to use the word INDEX in statements.
mysql interprets this as INDE followed by the delimiter X.

When the delimiter recognized by mysql is set to something other than the default of ;, instances of
that character are sent to the server without interpretation. However, the server itself still interprets
; as a statement delimiter and processes statements accordingly. This behavior on the server side
comes into play for multiple-statement execution (see Multiple Statement Execution Support), and
for parsing the body of stored procedures and functions, triggers, and events (see Section 27.1,
“Defining Stored Programs”).

•   edit, \e

Edit the current input statement. mysql checks the values of the EDITOR and VISUAL environment
variables to determine which editor to use. The default editor is vi if neither variable is set.

The edit command works only in Unix.

386

mysql — The MySQL Command-Line Client

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

Enable output paging. By using the --pager option when you invoke mysql, it is possible to
browse or search query results in interactive mode with Unix programs such as less, more, or any
other similar program. If you specify no value for the option, mysql checks the value of the PAGER
environment variable and sets the pager to that. Pager functionality works only in interactive mode.

Output paging can be enabled interactively with the pager command and disabled with nopager.
The command takes an optional argument; if given, the paging program is set to that. With no
argument, the pager is set to the pager that was set on the command line, or stdout if no pager
was specified.

Output paging works only in Unix because it uses the popen() function, which does not exist on
Windows. For Windows, the tee option can be used instead to save query output, although it is not
as convenient as pager for browsing output in some situations.

•   print, \p

Print the current input statement without executing it.

•   prompt [str], \R [str]

Reconfigure the mysql prompt to the given string. The special character sequences that can be
used in the prompt are described later in this section.

If you specify the prompt command with no argument, mysql resets the prompt to the default of
mysql>.

•   query_attributes name value [name value ...]

Define query attributes that apply to the next query sent to the server. For discussion of the purpose
and use of query attributes, see Section 11.6, “Query Attributes”.

The query_attributes command follows these rules:

• The format and quoting rules for attribute names and values are the same as for the delimiter

command.

387

mysql — The MySQL Command-Line Client

• The command permits up to 32 attribute name/value pairs. Names and values may be up to 1024

characters long. If a name is given without a value, an error occurs.

• If multiple query_attributes commands are issued prior to query execution, only the last

command applies. After sending the query, mysql clears the attribute set.

• If multiple attributes are defined with the same name, attempts to retrieve the attribute value have

an undefined result.

• An attribute defined with an empty name cannot be retrieved by name.

• If a reconnect occurs while mysql executes the query, mysql restores the attributes after

reconnecting so the query can be executed again with the same attributes.

•   quit, \q

Exit mysql.

•   rehash, \#

Rebuild the completion hash that enables database, table, and column name completion while you
are entering statements. (See the description for the --auto-rehash option.)

•   resetconnection, \x

Reset the connection to clear the session state. This includes clearing any current query attributes
defined using the query_attributes command.

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

Read the named file and executes the statements contained therein. On Windows, specify path
name separators as / or \\.

Quote characters are taken as part of the file name itself. For best results, the name should not
include space characters.

388

mysql — The MySQL Command-Line Client

•   ssl_session_data_print [file_name]

Fetches, serializes, and optionally stores the session data of a successful connection. The optional
file name and arguments may be given to specify the file to store serialized session data. If omitted,
the session data is printed to stdout.

If the MySQL session is configured for reuse, session data from the file is deserialized and supplied
to the connect command to reconnect. When the session is reused successfully, the status
command contains a row showing SSL session reused: true while the client remains
reconnected to the server.

•   status, \s

Provide status information about the connection and the server you are using. If you are running with
--safe-updates enabled, status also prints the values for the mysql variables that affect your
queries.

•   system command, \! command

Execute the given command using your default command interpreter.

In MySQL 8.4.3 and later, this command can be disabled by starting the client with --system-
command=OFF or --skip-system-command.

•   tee [file_name], \T [file_name]

By using the --tee option when you invoke mysql, you can log statements and their output. All the
data displayed on the screen is appended into a given file. This can be very useful for debugging
purposes also. mysql flushes results to the file after each statement, just before it prints its next
prompt. Tee functionality works only in interactive mode.

You can enable this feature interactively with the tee command. Without a parameter, the previous
file is used. The tee file can be disabled with the notee command. Executing tee again re-enables
logging.

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
results. Sometimes a very wide result set is difficult to read on the screen. The -S option to less
can make the result set much more readable because you can scroll it horizontally using the left-
arrow and right-arrow keys. You can also use -S interactively within less to switch the horizontal-
browse mode on and off. For more information, read the less manual page:

man less

• The -F and -X options may be used with less to cause it to exit if output fits on one screen, which

is convenient when no scrolling is necessary:

389

mysql — The MySQL Command-Line Client

mysql> pager less -n -i -S -F -X

• You can specify very complex pager commands for handling query output:

mysql> pager cat | tee /dr1/tmp/res.txt \
          | tee /dr2/tmp/res2.txt | less -n -i -S

In this example, the command would send query results to two files in two different directories on two
different file systems mounted on /dr1 and /dr2, yet still display the results onscreen using less.

You can also combine the tee and pager functions. Have a tee file enabled and pager set to less,
and you are able to browse the results using the less program and still have everything appended
into a file the same time. The difference between the Unix tee used with the pager command and
the mysql built-in tee command is that the built-in tee works even if you do not have the Unix tee
available. The built-in tee also logs everything that is printed on the screen, whereas the Unix tee
used with pager does not log quite that much. Additionally, tee file logging can be turned on and
off interactively from within mysql. This is useful when you want to log some queries to a file, but not
others.

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

\T

\t

\U

\u

\v

\w

\Y

390

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

Print an asterisk (*) if the current session is inside
a transaction block

A tab character

Your full user_name@host_name account name

Your user name

The server version

The current day of the week in three-letter format
(Mon, Tue, …)

The current year, four digits

mysql — The MySQL Command-Line Client

Option

\y

\_

\

\'

\"

\\

\x

Description

The current year, two digits

A space

A space (a space follows the backslash)

Single quote

Double quote

A literal \ backslash character

x, for any “x” not listed above

You can set the prompt in several ways:

• Use an environment variable. You can set the MYSQL_PS1 environment variable to a prompt string.

For example:

export MYSQL_PS1="(\u@\h) [\d]> "

• Use a command-line option. You can set the --prompt option on the command line to mysql. For

example:

$> mysql --prompt="(\u@\h) [\d]> "
(user@host) [database]>

• Use an option file. You can set the prompt option in the [mysql] group of any MySQL option file,

such as /etc/my.cnf or the .my.cnf file in your home directory. For example:

[mysql]
prompt=(\\u@\\h) [\\d]>\\_

In this example, note that the backslashes are doubled. If you set the prompt using the prompt
option in an option file, it is advisable to double the backslashes when using the special prompt
options. There is some overlap in the set of permissible prompt options and the set of special escape
sequences that are recognized in option files. (The rules for escape sequences in option files are
listed in Section 6.2.2.2, “Using Option Files”.) The overlap may cause you problems if you use
single backslashes. For example, \s is interpreted as a space rather than as the current seconds
value. The following example shows how to define a prompt within an option file to include the
current time in hh:mm:ss> format:

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

6.5.1.3 mysql Client Logging

The mysql client can do these types of logging for statements executed interactively:

• On Unix, mysql writes the statements to a history file. By default, this file is named

.mysql_history in your home directory. To specify a different file, set the value of the
MYSQL_HISTFILE environment variable.

• On all platforms, if the --syslog option is given, mysql writes the statements to the system logging
facility. On Unix, this is syslog; on Windows, it is the Windows Event Log. The destination where

391

mysql — The MySQL Command-Line Client

logged messages appear is system dependent. On Linux, the destination is often the /var/log/
messages file.

The following discussion describes characteristics that apply to all logging types and provides
information specific to each logging type.

• How Logging Occurs

• Controlling the History File

• syslog Logging Characteristics

How Logging Occurs

For each enabled logging destination, statement logging occurs as follows:

• Statements are logged only when executed interactively. Statements are noninteractive, for example,

when read from a file or a pipe. It is also possible to suppress statement logging by using the --
batch or --execute option.

• Statements are ignored and not logged if they match any pattern in the “ignore” list. This list is

described later.

• mysql logs each nonignored, nonempty statement line individually.

• If a nonignored statement spans multiple lines (not including the terminating delimiter), mysql
concatenates the lines to form the complete statement, maps newlines to spaces, and logs the
result, plus a delimiter.

Consequently, an input statement that spans multiple lines can be logged twice. Consider this input:

mysql> SELECT
    -> 'Today is'
    -> ,
    -> CURDATE()
    -> ;

In this case, mysql logs the “SELECT”, “'Today is'”, “,”, “CURDATE()”, and “;” lines as it reads them.
It also logs the complete statement, after mapping SELECT\n'Today is'\n,\nCURDATE() to
SELECT 'Today is' , CURDATE(), plus a delimiter. Thus, these lines appear in logged output:

SELECT
'Today is'
,
CURDATE()
;
SELECT 'Today is' , CURDATE();

mysql ignores for logging purposes statements that match any pattern in the “ignore” list. By default,
the pattern list is "*IDENTIFIED*:*PASSWORD*", to ignore statements that refer to passwords.
Pattern matching is not case-sensitive. Within patterns, two characters are special:

• ? matches any single character.

• * matches any sequence of zero or more characters.

To specify additional patterns, use the --histignore option or set the MYSQL_HISTIGNORE
environment variable. (If both are specified, the option value takes precedence.) The value should be a
list of one or more colon-separated patterns, which are appended to the default pattern list.

Patterns specified on the command line might need to be quoted or escaped to prevent your command
interpreter from treating them specially. For example, to suppress logging for UPDATE and DELETE
statements in addition to statements that refer to passwords, invoke mysql like this:

392

mysql — The MySQL Command-Line Client

mysql --histignore="*UPDATE*:*DELETE*"

Controlling the History File

The .mysql_history file should be protected with a restrictive access mode because sensitive
information might be written to it, such as the text of SQL statements that contain passwords. See
Section 8.1.2.1, “End-User Guidelines for Password Security”. Statements in the file are accessible
from the mysql client when the up-arrow key is used to recall the history. See Disabling Interactive
History.

If you do not want to maintain a history file, first remove .mysql_history if it exists. Then use either
of the following techniques to prevent it from being created again:

• Set the MYSQL_HISTFILE environment variable to /dev/null. To cause this setting to take effect

each time you log in, put it in one of your shell's startup files.

• Create .mysql_history as a symbolic link to /dev/null; this need be done only once:

ln -s /dev/null $HOME/.mysql_history

syslog Logging Characteristics

If the --syslog option is given, mysql writes interactive statements to the system logging facility.
Message logging has the following characteristics.

Logging occurs at the “information” level. This corresponds to the LOG_INFO priority for syslog on
Unix/Linux syslog capability and to EVENTLOG_INFORMATION_TYPE for the Windows Event Log.
Consult your system documentation for configuration of your logging capability.

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

Here is a sample of output generated on Linux by using --syslog. This output is formatted for
readability; each logged message actually takes a single line.

Mar  7 12:39:25 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,

393

mysql — The MySQL Command-Line Client

  DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
Mar  7 12:39:28 myhost MysqlClient[20824]:
  SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
  DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'

6.5.1.4 mysql Client Server-Side Help

mysql> help search_string

If you provide an argument to the help command, mysql uses it as a search string to access server-
side help from the contents of the MySQL Reference Manual. The proper operation of this command
requires that the help tables in the mysql database be initialized with help topic information (see
Section 7.1.17, “Server-Side Help Support”).

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

Lists the binary log files on the server. This statement is used as
part of the procedure described in [purge-binary-logs], that shows how
to determine which logs can be purged.

mysql> SHOW BINARY LOGS;
+---------------+-----------+-----------+
| Log_name      | File_size | Encrypted |
+---------------+-----------+-----------+

394

mysql — The MySQL Command-Line Client

| binlog.000015 |    724935 | Yes       |
| binlog.000016 |    733481 | Yes       |
+---------------+-----------+-----------+

The search string can contain the wildcard characters % and _. These have the same meaning as for
pattern-matching operations performed with the LIKE operator. For example, HELP rep% returns a list
of topics that begin with rep:

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

6.5.1.5 Executing SQL Statements from a Text File

The mysql client typically is used interactively, like this:

mysql db_name

However, it is also possible to put your SQL statements in a file and then tell mysql to read its input
from that file. To do so, create a text file text_file that contains the statements you wish to execute.
Then invoke mysql as shown here:

mysql db_name < text_file

If you place a USE db_name statement as the first statement in the file, it is unnecessary to specify the
database name on the command line:

mysql < text_file

If you are already running mysql, you can execute an SQL script file using the source command or
\. command:

mysql> source file_name
mysql> \. file_name

Sometimes you may want your script to display progress information to the user. For this you can insert
statements like this:

SELECT '<info_to_display>' AS ' ';

The statement shown outputs <info_to_display>.

You can also invoke mysql with the --verbose option, which causes each statement to be displayed
before the result that it produces.

mysql ignores Unicode byte order mark (BOM) characters at the beginning of input files. Previously,
it read them and sent them to the server, resulting in a syntax error. Presence of a BOM does not
cause mysql to change its default character set. To do that, invoke mysql with an option such as --
default-character-set=utf8mb4.

For more information about batch mode, see Section 5.5, “Using mysql in Batch Mode”.

6.5.1.6 mysql Client Tips

This section provides information about techniques for more effective use of mysql and about mysql
operational behavior.

• Input-Line Editing

395

mysql — The MySQL Command-Line Client

• Disabling Interactive History

• Unicode Support on Windows

• Displaying Query Results Vertically

• Using Safe-Updates Mode (--safe-updates)

• Disabling mysql Auto-Reconnect

• mysql Client Parser Versus Server Parser

Input-Line Editing

mysql supports input-line editing, which enables you to modify the current input line in place or recall
previous input lines. For example, the left-arrow and right-arrow keys move horizontally within the
current input line, and the up-arrow and down-arrow keys move up and down through the set of
previously entered lines. Backspace deletes the character before the cursor and typing new characters
enters them at the cursor position. To enter the line, press Enter.

On Windows, the editing key sequences are the same as supported for command editing in console
windows. On Unix, the key sequences depend on the input library used to build mysql (for example,
the libedit or readline library).

Documentation for the libedit and readline libraries is available online. To change the set of key
sequences permitted by a given input library, define key bindings in the library startup file. This is a file
in your home directory: .editrc for libedit and .inputrc for readline.

For example, in libedit, Control+W deletes everything before the current cursor position and
Control+U deletes the entire line. In readline, Control+W deletes the word before the cursor and
Control+U deletes everything before the current cursor position. If mysql was built using libedit, a
user who prefers the readline behavior for these two keys can put the following lines in the .editrc
file (creating the file if necessary):

bind "^W" ed-delete-prev-word
bind "^U" vi-kill-line-prev

To see the current set of key bindings, temporarily put a line that says only bind at the end of
.editrc. mysql shows the bindings when it starts.

Disabling Interactive History

The up-arrow key enables you to recall input lines from current and previous sessions. In cases where
a console is shared, this behavior may be unsuitable. mysql supports disabling the interactive history
partially or fully, depending on the host platform.

On Windows, the history is stored in memory. Alt+F7 deletes all input lines stored in memory for the
current history buffer. It also deletes the list of sequential numbers in front of the input lines displayed
with F7 and recalled (by number) with F9. New input lines entered after you press Alt+F7 repopulate
the current history buffer. Clearing the buffer does not prevent logging to the Windows Event Viewer,
if the --syslog option was used to start mysql. Closing the console window also clears the current
history buffer.

To disable interactive history on Unix, first delete the .mysql_history file, if it exists (previous
entries are recalled otherwise). Then start mysql with the --histignore="*" option to ignore all
new input lines. To re-enable the recall (and logging) behavior, restart mysql without the option.

If you prevent the .mysql_history file from being created (see Controlling the History File) and use
--histignore="*" to start the mysql client, the interactive history recall facility is disabled fully.
Alternatively, if you omit the --histignore option, you can recall the input lines entered during the
current session.

396

mysql — The MySQL Command-Line Client

Unicode Support on Windows

Windows provides APIs based on UTF-16LE for reading from and writing to the console; the mysql
client for Windows is able to use these APIs. The Windows installer creates an item in the MySQL
menu named MySQL command line client - Unicode. This item invokes the mysql client with
properties set to communicate through the console to the MySQL server using Unicode.

To take advantage of this support manually, run mysql within a console that uses a compatible
Unicode font and set the default character set to a Unicode character set that is supported for
communication with the server:

1. Open a console window.

2. Go to the console window properties, select the font tab, and choose Lucida Console or some other
compatible Unicode font. This is necessary because console windows start by default using a DOS
raster font that is inadequate for Unicode.

3. Execute mysql.exe with the --default-character-set=utf8mb4 (or utf8mb3) option. This
option is necessary because utf16le is one of the character sets that cannot be used as the client
character set. See Impermissible Client Character Sets.

With those changes, mysql uses the Windows APIs to communicate with the console using
UTF-16LE, and communicate with the server using UTF-8. (The menu item mentioned previously sets
the font and character set as just described.)

To avoid those steps each time you run mysql, you can create a shortcut that invokes mysql.exe.
The shortcut should set the console font to Lucida Console or some other compatible Unicode font, and
pass the --default-character-set=utf8mb4 (or utf8mb3) option to mysql.exe.

Alternatively, create a shortcut that only sets the console font, and set the character set in the [mysql]
group of your my.ini file:

[mysql]
default-character-set=utf8mb4   # or utf8mb3

Displaying Query Results Vertically

Some query results are much more readable when displayed vertically, instead of in the usual
horizontal table format. Queries can be displayed vertically by terminating the query with \G instead of
a semicolon. For example, longer text values that include newlines often are much easier to read with
vertical output:

mysql> SELECT * FROM mails WHERE LENGTH(txt) < 300 LIMIT 300,1\G
*************************** 1. row ***************************
  msg_nro: 3068
     date: 2000-03-01 23:29:50
time_zone: +0200
mail_from: Jones
    reply: jones@example.com
  mail_to: "John Smith" <smith@example.com>
      sbj: UTF-8
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

397

mysql — The MySQL Command-Line Client

For beginners, a useful startup option is --safe-updates (or --i-am-a-dummy, which has the
same effect). Safe-updates mode is helpful for cases when you might have issued an UPDATE or
DELETE statement but forgotten the WHERE clause indicating which rows to modify. Normally, such
statements update or delete all rows in the table. With --safe-updates, you can modify rows only by
specifying the key values that identify them, or a LIMIT clause, or both. This helps prevent accidents.
Safe-updates mode also restricts SELECT statements that produce (or are estimated to produce) very
large result sets.

The --safe-updates option causes mysql to execute the following statement when it connects to
the MySQL server, to set the session values of the sql_safe_updates, sql_select_limit, and
max_join_size system variables:

SET sql_safe_updates=1, sql_select_limit=1000, max_join_size=1000000;

The SET statement affects statement processing as follows:

• Enabling sql_safe_updates causes UPDATE and DELETE statements to produce an error if

they do not specify a key constraint in the WHERE clause, or provide a LIMIT clause, or both. For
example:

UPDATE tbl_name SET not_key_column=val WHERE key_column=val;

UPDATE tbl_name SET not_key_column=val LIMIT 1;

• Setting sql_select_limit to 1,000 causes the server to limit all SELECT result sets to 1,000 rows

unless the statement includes a LIMIT clause.

• Setting max_join_size to 1,000,000 causes multiple-table SELECT statements to produce an error

if the server estimates it must examine more than 1,000,000 row combinations.

To specify result set limits different from 1,000 and 1,000,000, you can override the defaults by using
the --select-limit and --max-join-size options when you invoke mysql:

mysql --safe-updates --select-limit=500 --max-join-size=10000

It is possible for UPDATE and DELETE statements to produce an error in safe-updates mode even with
a key specified in the WHERE clause, if the optimizer decides not to use the index on the key column:

• Range access on the index cannot be used if memory usage exceeds that permitted by the

range_optimizer_max_mem_size system variable. The optimizer then falls back to a table scan.
See Limiting Memory Use for Range Optimization.

• If key comparisons require type conversion, the index may not be used (see Section 10.3.1, “How

MySQL Uses Indexes”). Suppose that an indexed string column c1 is compared to a numeric value
using WHERE c1 = 2222. For such comparisons, the string value is converted to a number and the
operands are compared numerically (see Section 14.3, “Type Conversion in Expression Evaluation”),
preventing use of the index. If safe-updates mode is enabled, an error occurs.

These behaviors are included in safe-updates mode:

• EXPLAIN with UPDATE and DELETE statements does not produce safe-updates errors. This enables
use of EXPLAIN plus SHOW WARNINGS to see why an index is not used, which can be helpful in
cases such as when a range_optimizer_max_mem_size violation or type conversion occurs and
the optimizer does not use an index even though a key column was specified in the WHERE clause.

• When a safe-updates error occurs, the error message includes the first diagnostic that was

produced, to provide information about the reason for failure. For example, the message may
indicate that the range_optimizer_max_mem_size value was exceeded or type conversion
occurred, either of which can preclude use of an index.

• For multiple-table deletes and updates, an error is produced with safe updates enabled only if any

target table uses a table scan.

398

mysqladmin — A MySQL Server Administration Program

Disabling mysql Auto-Reconnect

If the mysql client loses its connection to the server while sending a statement, it immediately and
automatically tries to reconnect once to the server and send the statement again. However, even if
mysql succeeds in reconnecting, your first connection has ended and all your previous session objects
and settings are lost: temporary tables, the autocommit mode, and user-defined and session variables.
Also, any current transaction rolls back. This behavior may be dangerous for you, as in the following
example where the server was shut down and restarted between the first and second statements
without you knowing it:

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

The @a user variable has been lost with the connection, and after the reconnection it is undefined. If it
is important to have mysql terminate with an error if the connection has been lost, you can start the
mysql client with the --skip-reconnect option.

For more information about auto-reconnect and its effect on state information when a reconnection
occurs, see Automatic Reconnection Control.

mysql Client Parser Versus Server Parser

The mysql client uses a parser on the client side that is not a duplicate of the complete parser used by
the mysqld server on the server side. This can lead to differences in treatment of certain constructs.
Examples:

• The server parser treats strings delimited by " characters as identifiers rather than as plain strings if

the ANSI_QUOTES SQL mode is enabled.

The mysql client parser does not take the ANSI_QUOTES SQL mode into account. It treats strings
delimited by ", ', and ` characters the same, regardless of whether ANSI_QUOTES is enabled.

• Within /*! ... */ and /*+ ... */ comments, the mysql client parser interprets short-form

mysql commands. The server parser does not interpret them because these commands have no
meaning on the server side.

If it is desirable for mysql not to interpret short-form commands within comments, a partial
workaround is to use the --binary-mode option, which causes all mysql commands to be
disabled except \C and \d in noninteractive mode (for input piped to mysql or loaded using the
source command).

6.5.2 mysqladmin — A MySQL Server Administration Program

mysqladmin is a client for performing administrative operations. You can use it to check the server's
configuration and current status, to create and drop databases, and more.

Invoke mysqladmin like this:

mysqladmin [options] command [command-arg] [command [command-arg]] ...

399

mysqladmin — A MySQL Server Administration Program

mysqladmin supports the following commands. Some of the commands take an argument following
the command name.

• create db_name

Create a new database named db_name.

• debug

Tells the server to write debug information to the error log. The connected user must have the SUPER
privilege. Format and content of this information is subject to change.

This includes information about the Event Scheduler. See Section 27.4.5, “Event Scheduler Status”.

• drop db_name

Delete the database named db_name and all its tables.

• extended-status

Display the server status variables and their values.

• flush-hosts

Flush all information in the host cache. See Section 7.1.12.3, “DNS Lookups and the Host Cache”.

• flush-logs [log_type ...]

Flush all logs.

The mysqladmin flush-logs command permits optional log types to be given, to specify which
logs to flush. Following the flush-logs command, you can provide a space-separated list of
one or more of the following log types: binary, engine, error, general, relay, slow. These
correspond to the log types that can be specified for the FLUSH LOGS SQL statement.

• flush-privileges

Reload the grant tables (same as reload).

• flush-status

Clear status variables.

• flush-tables

Flush all tables.

• kill id,id,...

Kill server threads. If multiple thread ID values are given, there must be no spaces in the list.

To kill threads belonging to other users, the connected user must have the CONNECTION_ADMIN
privilege (or the deprecated SUPER privilege).

• password new_password

Set a new password. This changes the password to new_password for the account that you use
with mysqladmin for connecting to the server. Thus, the next time you invoke mysqladmin (or any
other client program) using the same account, you must specify the new password.

Warning

Setting a password using mysqladmin should be considered insecure. On
some systems, your password becomes visible to system status programs

400

mysqladmin — A MySQL Server Administration Program

such as ps that may be invoked by other users to display command lines.
MySQL clients typically overwrite the command-line password argument with
zeros during their initialization sequence. However, there is still a brief interval
during which the value is visible. Also, on some systems this overwriting
strategy is ineffective and the password remains visible to ps. (SystemV Unix
systems and perhaps others are subject to this problem.)

If the new_password value contains spaces or other characters that are special to your command
interpreter, you need to enclose it within quotation marks. On Windows, be sure to use double
quotation marks rather than single quotation marks; single quotation marks are not stripped from the
password, but rather are interpreted as part of the password. For example:

mysqladmin password "my new password"

The new password can be omitted following the password command. In this case, mysqladmin
prompts for the password value, which enables you to avoid specifying the password on the
command line. Omitting the password value should be done only if password is the final command
on the mysqladmin command line. Otherwise, the next argument is taken as the password.

Caution

Do not use this command used if the server was started with the --skip-
grant-tables option. No password change is applied. This is true even
if you precede the password command with flush-privileges on
the same command line to re-enable the grant tables because the flush
operation occurs after you connect. However, you can use mysqladmin
flush-privileges to re-enable the grant tables and then use a separate
mysqladmin password command to change the password.

• ping

Check whether the server is available. The return status from mysqladmin is 0 if the server is
running, 1 if it is not. This is 0 even in case of an error such as Access denied, because this
means that the server is running but refused the connection, which is different from the server not
running.

• processlist

Show a list of active server threads. This is like the output of the SHOW PROCESSLIST statement.
If the --verbose option is given, the output is like that of SHOW FULL PROCESSLIST. (See
Section 15.7.7.31, “SHOW PROCESSLIST Statement”.)

• reload

Reload the grant tables.

• refresh

Flush all tables and close and open log files.

• shutdown

Stop the server.

• start-replica

Start replication on a replica server.

• start-slave

This is a deprecated alias for start-replica.

• status

401

mysqladmin — A MySQL Server Administration Program

Display a short server status message.

• stop-replica

Stop replication on a replica server.

• stop-slave

This is a deprecated alias for stop-replica.

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

The mysqladmin status command result displays the following values:

•  Uptime

The number of seconds the MySQL server has been running.

•  Threads

The number of active threads (clients).

•  Questions

The number of questions (queries) from clients since the server was started.

•  Slow queries

The number of queries that have taken more than long_query_time seconds. See Section 7.4.5,
“The Slow Query Log”.

•  Opens

The number of tables the server has opened.

•   Flush tables

The number of flush-*, refresh, and reload commands the server has executed.

•  Open tables

The number of tables that currently are open.

If you execute mysqladmin shutdown when connecting to a local server using a Unix socket file,
mysqladmin waits until the server's process ID file has been removed, to ensure that the server has
stopped properly.

402

mysqladmin — A MySQL Server Administration Program

mysqladmin supports the following options, which can be specified on the command line or in the
[mysqladmin] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.11 mysqladmin Options

Option Name

--bind-address

--character-sets-dir

--compress

--compression-algorithms

Description

Use specified network interface to connect to
MySQL Server

Directory where character sets can be found

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

--connect-timeout

Number of seconds before connection timeout

--count

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--enable-cleartext-plugin

--force

--get-server-public-key

--help

--host

--login-path

--no-beep

--no-defaults

--no-login-paths

--password

--password1

--password2

--password3

--pipe

--plugin-dir

--port

Number of iterations to make for repeated
command execution

Write debugging log

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Specify default character set

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Enable cleartext authentication plugin

Continue even if an SQL error occurs

Request RSA public key from server

Display help message and exit

Host on which MySQL server is located

Read login path options from .mylogin.cnf

Do not beep when errors occur

Read no option files

Do not read login paths from the login path file

Password to use when connecting to server

First multifactor authentication password to use
when connecting to server

Second multifactor authentication password to use
when connecting to server

Third multifactor authentication password to use
when connecting to server

Connect to server using named pipe (Windows
only)

Directory where plugins are installed

TCP/IP port number for connection

403

mysqladmin — A MySQL Server Administration Program

Option Name

--print-defaults

--protocol

--relative

--server-public-key-path

--shared-memory-base-name

--show-warnings

--shutdown-timeout

--silent

--sleep

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tls-ciphersuites

--tls-sni-servername

--tls-version

--user

--verbose

--version

--vertical

--wait

--zstd-compression-level

Description

Print default options

Transport protocol to use

Show the difference between the current and
previous values when used with the --sleep option

Path name to file containing RSA public key

Shared-memory name for shared-memory
connections (Windows only)

Show warnings after statement execution

The maximum number of seconds to wait for
server shutdown

Silent mode

Execute commands repeatedly, sleeping for delay
seconds in between

Unix socket file or Windows named pipe to use

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Print query output rows vertically (one line per
column value)

If the connection cannot be established, wait and
retry instead of aborting

Compression level for connections to server that
use zstd compression

404

mysqladmin — A MySQL Server Administration Program

• --help, -?

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

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

405

For more information, see Section 6.2.8, “Connection Compression Control”.

mysqladmin — A MySQL Server Administration Program

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

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/mysqladmin.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

406

mysqladmin — A MySQL Server Administration Program

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 12.15, “Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqladmin normally reads the [client] and [mysqladmin] groups. If this option is
given as --defaults-group-suffix=_other, mysqladmin also reads the [client_other]
and [mysqladmin_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --enable-cleartext-plugin

407

Command-Line Format

--enable-cleartext-plugin

Type

Boolean

mysqladmin — A MySQL Server Administration Program

Default Value

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

• --force, -f

Command-Line Format

--force

Do not ask for confirmation for the drop db_name command. With multiple commands, continue
even if an error occurs.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

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
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

408

mysqladmin — A MySQL Server Administration Program

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-beep, -b

Command-Line Format

--no-beep

Suppress the warning beep that is emitted by default for errors such as a failure to connect to the
server.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqladmin prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqladmin should not prompt for one, use
the --skip-password option.

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the
server. The password value is optional. If not given, mysql prompts for one. If given, there must be
no space between --password1= and the password following it. If no password option is specified,
the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

409

mysqladmin — A MySQL Server Administration Program

To explicitly specify that there is no password and that mysqladmin should not prompt for one, use
the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

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
to specify an authentication plugin but mysqladmin does not find it. See Section 8.2.17, “Pluggable
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

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

410

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
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --relative, -r

Command-Line Format

--relative

Show the difference between the current and previous values when used with the --sleep option.
This option works only with the extended-status command.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.
411

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

mysqladmin — A MySQL Server Administration Program

• --show-warnings

Command-Line Format

--show-warnings

Show warnings resulting from execution of statements sent to the server.

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

Exit silently if a connection to the server cannot be established.

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

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

412

mysqladmin — A MySQL Server Administration Program

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

413

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

mysqladmin — A MySQL Server Administration Program

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin, grant this user the SKIP_QUERY_REWRITE privilege.

• --verbose, -v

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

If the connection cannot be established, wait and retry instead of aborting. If a count value is given,
it indicates the number of times to retry. The default is one time.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

414

mysqlcheck — A Table Maintenance Program

6.5.3 mysqlcheck — A Table Maintenance Program

The mysqlcheck client performs table maintenance: It checks, repairs, optimizes, or analyzes tables.

Each table is locked and therefore unavailable to other sessions while it is being processed, although
for check operations, the table is locked with a READ lock only (see Section 15.3.6, “LOCK TABLES
and UNLOCK TABLES Statements”, for more information about READ and WRITE locks). Table
maintenance operations can be time-consuming, particularly for large tables. If you use the --
databases or --all-databases option to process all tables in one or more databases, an
invocation of mysqlcheck might take a long time. (This is also true for the MySQL upgrade procedure
if it determines that table checking is needed because it processes tables the same way.)

mysqlcheck must be used when the mysqld server is running, which means that you do not have to
stop the server to perform table maintenance.

mysqlcheck uses the SQL statements CHECK TABLE, REPAIR TABLE, ANALYZE TABLE, and
OPTIMIZE TABLE in a convenient way for the user. It determines which statements to use for the
operation you want to perform, and then sends the statements to the server to be executed. For details
about which storage engines each statement works with, see the descriptions for those statements in
Section 15.7.3, “Table Maintenance Statements”.

All storage engines do not necessarily support all four maintenance operations. In such cases, an error
message is displayed. For example, if test.t is an MEMORY table, an attempt to check it produces this
result:

$> mysqlcheck test t
test.t
note     : The storage engine for the table doesn't support check

If mysqlcheck is unable to repair a table, see Section 3.14, “Rebuilding or Repairing Tables or
Indexes” for manual table repair strategies. This is the case, for example, for InnoDB tables, which can
be checked with CHECK TABLE, but not repaired with REPAIR TABLE.

Caution

It is best to make a backup of a table before performing a table repair operation;
under some circumstances the operation might cause data loss. Possible
causes include but are not limited to file system errors.

There are three general ways to invoke mysqlcheck:

mysqlcheck [options] db_name [tbl_name ...]
mysqlcheck [options] --databases db_name ...
mysqlcheck [options] --all-databases

If you do not name any tables following db_name or if you use the --databases or --all-
databases option, entire databases are checked.

mysqlcheck has a special feature compared to other client programs. The default behavior of
checking tables (--check) can be changed by renaming the binary. If you want to have a tool that
repairs tables by default, you should just make a copy of mysqlcheck named mysqlrepair, or make
a symbolic link to mysqlcheck named mysqlrepair. If you invoke mysqlrepair, it repairs tables.

The names shown in the following table can be used to change mysqlcheck default behavior.

Command

mysqlrepair

mysqlanalyze

mysqloptimize

Meaning

The default option is --repair

The default option is --analyze

The default option is --optimize

415

mysqlcheck — A Table Maintenance Program

mysqlcheck supports the following options, which can be specified on the command line or in the
[mysqlcheck] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.12 mysqlcheck Options

Option Name

--all-databases

--all-in-1

--analyze

--auto-repair

--bind-address

--character-sets-dir

--check

--check-only-changed

--check-upgrade

--compress

--compression-algorithms

--databases

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--enable-cleartext-plugin

--extended

--fast

--force

--get-server-public-key

--help

--host

--login-path

--medium-check

--no-defaults

416

Description

Check all tables in all databases

Execute a single statement for each database that
names all the tables from that database

Analyze the tables

If a checked table is corrupted, automatically fix it

Use specified network interface to connect to
MySQL Server

Directory where character sets are installed

Check the tables for errors

Check only tables that have changed since the
last check

Invoke CHECK TABLE with the FOR UPGRADE
option

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Interpret all arguments as database names

Write debugging log

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Specify default character set

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Enable cleartext authentication plugin

Check and repair tables

Check only tables that have not been closed
properly

Continue even if an SQL error occurs

Request RSA public key from server

Display help message and exit

Host on which MySQL server is located

Read login path options from .mylogin.cnf

Do a check that is faster than an --extended
operation

Read no option files

mysqlcheck — A Table Maintenance Program

Option Name

--no-login-paths

--optimize

--password

--password1

--password2

--password3

--pipe

--plugin-dir

--port

--print-defaults

--protocol

--quick

--repair

--server-public-key-path

--shared-memory-base-name

--silent

--skip-database

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tables

--tls-ciphersuites

Description

Do not read login paths from the login path file

Optimize the tables

Password to use when connecting to server

First multifactor authentication password to use
when connecting to server

Second multifactor authentication password to use
when connecting to server

Third multifactor authentication password to use
when connecting to server

Connect to server using named pipe (Windows
only)

Directory where plugins are installed

TCP/IP port number for connection

Print default options

Transport protocol to use

The fastest method of checking

Perform a repair that can fix almost anything
except unique keys that are not unique

Path name to file containing RSA public key

Shared-memory name for shared-memory
connections (Windows only)

Silent mode

Omit this database from performed operations

Unix socket file or Windows named pipe to use

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Overrides the --databases or -B option

Permissible TLSv1.3 ciphersuites for encrypted
connections

--tls-sni-servername

Server name supplied by the client

417

mysqlcheck — A Table Maintenance Program

Option Name

--tls-version

--use-frm

--user

--verbose

--version

--write-binlog

--zstd-compression-level

• --help, -?

Description

Permissible TLS protocols for encrypted
connections

For repair operations on MyISAM tables

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Log ANALYZE, OPTIMIZE, REPAIR statements
to binary log. --skip-write-binlog adds
NO_WRITE_TO_BINLOG to these statements

Compression level for connections to server that
use zstd compression

Command-Line Format

--help

Display a help message and exit.

• --all-databases, -A

Command-Line Format

--all-databases

Check all tables in all databases. This is the same as using the --databases option and
naming all the databases on the command line, except that the INFORMATION_SCHEMA and
performance_schema databases are not checked. They can be checked by explicitly naming them
with the --databases option.

• --all-in-1, -1

Command-Line Format

--all-in-1

Instead of issuing a statement for each table, execute a single statement for each database that
names all the tables from that database to be processed.

• --analyze, -a

Command-Line Format

--analyze

Analyze the tables.

• --auto-repair

Command-Line Format

--auto-repair

If a checked table is corrupted, automatically fix it. Any necessary repairs are done after all tables
have been checked.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

418

mysqlcheck — A Table Maintenance Program

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

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

Invoke CHECK TABLE with the FOR UPGRADE option to check tables for incompatibilities with the
current version of the server.

• --compress

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

419

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

mysqlcheck — A Table Maintenance Program

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

For more information, see Section 6.2.8, “Connection Compression Control”.

• --databases, -B

Command-Line Format

--databases

Process all tables in the named databases. Normally, mysqlcheck treats the first name argument
on the command line as a database name and any following names as table names. With this option,
it treats all name arguments as database names.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

420

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

mysqlcheck — A Table Maintenance Program

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 12.15, “Character Set Configuration”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqlcheck normally reads the [client] and [mysqlcheck] groups. If this option is
given as --defaults-group-suffix=_other, mysqlcheck also reads the [client_other]
and [mysqlcheck_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --extended, -e

Command-Line Format

--extended

If you are using this option to check tables, it ensures that they are 100% consistent but takes a long
time.

If you are using this option to repair tables, it runs an extended repair that may not only take a long
time to execute, but may produce a lot of garbage rows also!

421

mysqlcheck — A Table Maintenance Program

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

• --fast, -F

Command-Line Format

--fast

Check only tables that have not been closed properly.

• --force, -f

Command-Line Format

--force

Continue even if an SQL error occurs.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

422

mysqlcheck — A Table Maintenance Program

Connect to the MySQL server on the given host.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --medium-check, -m

Command-Line Format

--medium-check

Do a check that is faster than an --extended operation. This finds only 99.99% of all errors, which
should be good enough in most cases.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --optimize, -o

Command-Line Format

--optimize

Optimize the tables.

• --password[=password], -p[password]

423

mysqlcheck — A Table Maintenance Program

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqlcheck prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlcheck should not prompt for one, use
the --skip-password option.

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to
the server. The password value is optional. If not given, mysqlcheck prompts for one. If given, there
must be no space between --password1= and the password following it. If no password option is
specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlcheck should not prompt for one, use
the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

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

424

mysqlcheck — A Table Maintenance Program

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqlcheck does not find it. See Section 8.2.17, “Pluggable
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

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

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
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --quick, -q

Command-Line Format

--quick

If you are using this option to check tables, it prevents the check from scanning the rows to check for
incorrect links. This is the fastest check method.

If you are using this option to repair tables, it tries to repair only the index tree. This is the fastest
repair method.

• --repair, -r

Command-Line Format

--repair

425

mysqlcheck — A Table Maintenance Program

Perform a repair that can fix almost anything except unique keys that are not unique.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --silent, -s

Command-Line Format

--silent

Silent mode. Print only error messages.

• --skip-database=db_name

Command-Line Format

--skip-database=db_name

Do not include the named database (case-sensitive) in the operations performed by mysqlcheck.

• --socket=path, -S path

426

Command-Line Format

--socket={file_name|pipe_name}

mysqlcheck — A Table Maintenance Program

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tables

Command-Line Format

--tables

Override the --databases or -B option. All name arguments following the option are regarded as
table names.

427

mysqlcheck — A Table Maintenance Program

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --use-frm

Command-Line Format

--use-frm

For repair operations on MyISAM tables, get the table structure from the data dictionary so that the
table can be repaired even if the .MYI header is corrupted.

• --user=user_name, -u user_name

428

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

mysqldump — A Database Backup Program

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
statements generated by mysqlcheck are written to the binary log. Use --skip-write-binlog
to cause NO_WRITE_TO_BINLOG to be added to the statements so that they are not logged. Use the
--skip-write-binlog when these statements should not be sent to replicas or run when using
the binary logs for recovery from backup.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

6.5.4 mysqldump — A Database Backup Program

The mysqldump client utility performs logical backups, producing a set of SQL statements that can be
executed to reproduce the original database object definitions and table data. It dumps one or more
MySQL databases for backup or transfer to another SQL server. The mysqldump command can also
generate output in CSV, other delimited text, or XML format.

Tip

Consider using the MySQL Shell dump utilities, which provide parallel
dumping with multiple threads, file compression, and progress information
display, as well as cloud features such as Oracle Cloud Infrastructure Object
Storage streaming, and MySQL HeatWave Service compatibility checks and
modifications. Dumps can be easily imported into a MySQL Server instance
or a MySQL HeatWave Service DB System using the MySQL Shell load dump
utilities. Installation instructions for MySQL Shell can be found here.

• Performance and Scalability Considerations

• Invocation Syntax

• Option Syntax - Alphabetical Summary

429

mysqldump — A Database Backup Program

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
TRIGGER for dumped triggers, LOCK TABLES if the --single-transaction option is not used,
PROCESS if the --no-tablespaces option is not used, and the RELOAD or FLUSH_TABLES privilege
with --single-transaction if both gtid_mode=ON and gtid_purged=ON|AUTO. Certain options
might require other privileges as noted in the option descriptions.

To reload a dump file, you must have the privileges required to execute the statements that it contains,
such as the appropriate CREATE privileges for objects created by those statements.

mysqldump output can include ALTER DATABASE statements that change the database collation.
These may be used when dumping stored programs to preserve their character encodings. To reload a
dump file containing such statements, the ALTER privilege for the affected database is required.

Note

A dump made using PowerShell on Windows with output redirection creates a
file that has UTF-16 encoding:

mysqldump [options] > dump.sql

However, UTF-16 is not permitted as a connection character set (see
Impermissible Client Character Sets), so the dump file cannot be loaded
correctly. To work around this issue, use the --result-file option, which
creates the output in ASCII format:

mysqldump [options] --result-file=dump.sql

It is not recommended to load a dump file when GTIDs are enabled on the server (gtid_mode=ON),
if your dump file includes system tables. mysqldump issues DML instructions for the system tables
which use the non-transactional MyISAM storage engine, and this combination is not permitted when
GTIDs are enabled.

Performance and Scalability Considerations

mysqldump advantages include the convenience and flexibility of viewing or even editing the output
before restoring. You can clone databases for development and DBA work, or produce slight variations

430

mysqldump — A Database Backup Program

of an existing database for testing. It is not intended as a fast or scalable solution for backing up
substantial amounts of data. With large data sizes, even if the backup step takes a reasonable time,
restoring the data can be very slow because replaying the SQL statements involves disk I/O for
insertion, index creation, and so on.

For large-scale backup and restore, a physical backup is more appropriate, to copy the data files in
their original format so that they can be restored quickly.

If your tables are primarily InnoDB tables, or if you have a mix of InnoDB and MyISAM tables,
consider using mysqlbackup, which is available as part of MySQL Enterprise. This tool provides high
performance for InnoDB backups with minimal disruption; it can also back up tables from MyISAM
and other storage engines; it also provides a number of convenient options to accommodate different
backup scenarios. See Section 32.1, “MySQL Enterprise Backup Overview”.

mysqldump can retrieve and dump table contents row by row, or it can retrieve the entire content from
a table and buffer it in memory before dumping it. Buffering in memory can be a problem if you are
dumping large tables. To dump tables row by row, use the --quick option (or --opt, which enables
--quick). The --opt option (and hence --quick) is enabled by default, so to enable memory
buffering, use --skip-quick.

If you are using a recent version of mysqldump to generate a dump to be reloaded into a very old
MySQL server, use the --skip-opt option instead of the --opt or --extended-insert option.

For additional information about mysqldump, see Section 9.4, “Using mysqldump for Backups”.

Invocation Syntax

There are in general three ways to use mysqldump—in order to dump a set of one or more tables, a
set of one or more complete databases, or an entire MySQL server—as shown here:

mysqldump [options] db_name [tbl_name ...]
mysqldump [options] --databases db_name ...
mysqldump [options] --all-databases

To dump entire databases, do not name any tables following db_name, or use the --databases or
--all-databases option.

To see a list of the options your version of mysqldump supports, issue the command mysqldump --
help.

Option Syntax - Alphabetical Summary

mysqldump supports the following options, which can be specified on the command line or in the
[mysqldump] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.13 mysqldump Options

Option Name

--add-drop-database

--add-drop-table

--add-drop-trigger

--add-locks

--all-databases

--allow-keywords

Description

Add DROP DATABASE statement before each
CREATE DATABASE statement

Add DROP TABLE statement before each
CREATE TABLE statement

Add DROP TRIGGER statement before each
CREATE TRIGGER statement

Surround each table dump with LOCK TABLES
and UNLOCK TABLES statements

Dump all tables in all databases

Allow creation of column names that are keywords

431

mysqldump — A Database Backup Program

Option Name

--apply-replica-statements

--apply-slave-statements

--bind-address

--character-sets-dir

--column-statistics

--comments

--compact

--compatible

--complete-insert

--compress

--compression-algorithms

--create-options

--databases

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--delete-master-logs

--delete-source-logs

--disable-keys

--dump-date

--dump-replica

--dump-slave

432

Description

Include STOP REPLICA prior to CHANGE
REPLICATION SOURCE TO statement and
START REPLICA at end of output

Include STOP SLAVE prior to CHANGE MASTER
statement and START SLAVE at end of output

Use specified network interface to connect to
MySQL Server

Directory where character sets are installed

Write ANALYZE TABLE statements to generate
statistics histograms

Add comments to dump file

Produce more compact output

Produce output that is more compatible with other
database systems or with older MySQL servers

Use complete INSERT statements that include
column names

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Include all MySQL-specific table options in
CREATE TABLE statements

Interpret all name arguments as database names

Write debugging log

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Specify default character set

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

On a replication source server, delete the binary
logs after performing the dump operation

On a replication source server, delete the binary
logs after performing the dump operation

For each table, surround INSERT statements with
statements to disable and enable keys

Include dump date as "Dump completed on"
comment if --comments is given

Include CHANGE REPLICATION SOURCE TO
statement that lists binary log coordinates of
replica's source

Include CHANGE MASTER statement that lists
binary log coordinates of replica's source

mysqldump — A Database Backup Program

Option Name

--enable-cleartext-plugin

--events

--extended-insert

--fields-enclosed-by

--fields-escaped-by

--fields-optionally-enclosed-by

--fields-terminated-by

--flush-logs

--flush-privileges

--force

Description

Enable cleartext authentication plugin

Dump events from dumped databases

Use multiple-row INSERT syntax

This option is used with the --tab option and has
the same meaning as the corresponding clause
for LOAD DATA

This option is used with the --tab option and has
the same meaning as the corresponding clause
for LOAD DATA

This option is used with the --tab option and has
the same meaning as the corresponding clause
for LOAD DATA

This option is used with the --tab option and has
the same meaning as the corresponding clause
for LOAD DATA

Flush MySQL server log files before starting dump

Emit a FLUSH PRIVILEGES statement after
dumping mysql database

Continue even if an SQL error occurs during a
table dump

--get-server-public-key

Request RSA public key from server

--help

--hex-blob

--host

--ignore-error

--ignore-table

--ignore-views

--include-master-host-port

--include-source-host-port

--init-command

--init-command-add

--insert-ignore

--lines-terminated-by

--lock-all-tables

--lock-tables

--log-error

Display help message and exit

Dump binary columns using hexadecimal notation

Host on which MySQL server is located

Ignore specified errors

Do not dump given table

Skip dumping table views

Include MASTER_HOST/MASTER_PORT options
in CHANGE MASTER statement produced with --
dump-slave

Include SOURCE_HOST and SOURCE_PORT
options in CHANGE REPLICATION SOURCE TO
statement produced with --dump-replica

Single SQL statement to execute after connecting
or re-connecting to MySQL server; resets existing
defined commands

Add an additional SQL statement to execute after
connecting or re-connecting to MySQL server

Write INSERT IGNORE rather than INSERT
statements

This option is used with the --tab option and has
the same meaning as the corresponding clause
for LOAD DATA

Lock all tables across all databases

Lock all tables before dumping them

Append warnings and errors to named file

433

mysqldump — A Database Backup Program

Option Name

--login-path

--master-data

--max-allowed-packet

Description

Read login path options from .mylogin.cnf

Write the binary log file name and position to the
output

Maximum packet length to send to or receive from
server

--mysqld-long-query-time

Session value for slow query threshold

--net-buffer-length

--network-timeout

--no-autocommit

--no-create-db

--no-create-info

--no-data

--no-defaults

--no-login-paths

--no-set-names

--no-tablespaces

--opt

--order-by-primary

--output-as-version

--password

--password1

--password2

--password3

--pipe

--plugin-authentication-kerberos-client-mode

--plugin-dir

--port

--print-defaults

--protocol

--quick

434

Buffer size for TCP/IP and socket communication

Increase network timeouts to permit larger table
dumps

Enclose the INSERT statements for each dumped
table within SET autocommit = 0 and COMMIT
statements

Do not write CREATE DATABASE statements

Do not write CREATE TABLE statements that re-
create each dumped table

Do not dump table contents

Read no option files

Do not read login paths from the login path file

Same as --skip-set-charset

Do not write any CREATE LOGFILE GROUP or
CREATE TABLESPACE statements in output

Shorthand for --add-drop-table --add-locks --
create-options --disable-keys --extended-insert --
lock-tables --quick --set-charset

Dump each table's rows sorted by its primary key,
or by its first unique index

Determines replica and event terminology used in
dumps; for compatibility with older versions

Password to use when connecting to server

First multifactor authentication password to use
when connecting to server

Second multifactor authentication password to use
when connecting to server

Third multifactor authentication password to use
when connecting to server

Connect to server using named pipe (Windows
only)

Permit GSSAPI pluggable authentication through
the MIT Kerberos library on Windows

Directory where plugins are installed

TCP/IP port number for connection

Print default options

Transport protocol to use

Retrieve rows for a table from the server a row at
a time

mysqldump — A Database Backup Program

Option Name

--quote-names

--replace

--result-file

--routines

Description

Quote identifiers within backtick characters

Write REPLACE statements rather than INSERT
statements

Direct output to a given file

Dump stored routines (procedures and functions)
from dumped databases

--server-public-key-path

Path name to file containing RSA public key

--set-charset

--set-gtid-purged

--shared-memory-base-name

--show-create-skip-secondary-engine

--single-transaction

--skip-add-drop-table

--skip-add-locks

--skip-comments

--skip-compact

--skip-disable-keys

--skip-extended-insert

--skip-generated-invisible-primary-key

--skip-opt

--skip-quick

--skip-quote-names

--skip-set-charset

--skip-triggers

--skip-tz-utc

--socket

--source-data

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

Add SET NAMES default_character_set to output

Whether to add SET
@@GLOBAL.GTID_PURGED to output

Shared-memory name for shared-memory
connections (Windows only)

Exclude SECONDARY ENGINE clause from
CREATE TABLE statements

Issue a BEGIN SQL statement before dumping
data from server

Do not add a DROP TABLE statement before
each CREATE TABLE statement

Do not add locks

Do not add comments to dump file

Do not produce more compact output

Do not disable keys

Turn off extended-insert

Do not include generated invisible primary keys in
dump file

Turn off options set by --opt

Do not retrieve rows for a table from the server a
row at a time

Do not quote identifiers

Do not write SET NAMES statement

Do not dump triggers

Turn off tz-utc

Unix socket file or Windows named pipe to use

Write the binary log file name and position to the
output

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

435

mysqldump — A Database Backup Program

Option Name

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tab

--tables

--tls-ciphersuites

--tls-sni-servername

--tls-version

--triggers

--tz-utc

--user

--verbose

--version

--where

--xml

--zstd-compression-level

Connection Options

Description

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Produce tab-separated data files

Override --databases or -B option

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

Dump triggers for each dumped table

Add SET TIME_ZONE='+00:00' to dump file

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Dump only rows selected by given WHERE
condition

Produce XML output

Compression level for connections to server that
use zstd compression

The mysqldump command logs into a MySQL server to extract information. The following options
specify how to connect to the MySQL server, either on the same machine or a remote system.

• --bind-address=ip_address

Command-Line Format

--bind-address=ip_address

On a computer having multiple network interfaces, use this option to select which interface to use for
connecting to the MySQL server.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

436

mysqldump — A Database Backup Program

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

For more information, see Section 6.2.8, “Connection Compression Control”.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based

437

mysqldump — A Database Backup Program

password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

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
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqldump prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

438

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqldump should not prompt for one, use

the --skip-password option.

mysqldump — A Database Backup Program

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to
the server. The password value is optional. If not given, mysqldump prompts for one. If given, there
must be no space between --password1= and the password following it. If no password option is
specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqldump should not prompt for one, use
the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --pipe, -W

Command-Line Format

Type

--pipe

String

On Windows, connect to the server using a named pipe. This option applies only if the server was
started with the named_pipe system variable enabled to support named-pipe connections. In
addition, the user making the connection must be a member of the Windows group specified by the
named_pipe_full_access_group system variable.

• --plugin-authentication-kerberos-client-mode=value

Command-Line Format

Type

Default Value

Valid Values

--plugin-authentication-kerberos-
client-mode

String

SSPI

GSSAPI

On Windows, the authentication_kerberos_client authentication plugin supports this plugin
option. It provides two possible values that the client user can set at runtime: SSPI and GSSAPI.

The default value for the client-side plugin option uses Security Support Provider Interface (SSPI),
which is capable of acquiring credentials from the Windows in-memory cache. Alternatively, the
client user can select a mode that supports Generic Security Service Application Program Interface
(GSSAPI) through the MIT Kerberos library on Windows. GSSAPI is capable of acquiring cached
credentials previously generated by using the kinit command.

For more information, see Commands for Windows Clients in GSSAPI Mode.

439

mysqldump — A Database Backup Program

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is used
to specify an authentication plugin but mysqldump does not find it. See Section 8.2.17, “Pluggable
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
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

440

mysqldump — A Database Backup Program

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list441

mysqldump — A Database Backup Program

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

Type

String

The user name of the MySQL account to use for connecting to the server.

If you are using the Rewriter plugin, you should grant this user the SKIP_QUERY_REWRITE
privilege.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

442

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.

The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.

mysqldump — A Database Backup Program

The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

Option-File Options

These options are used to control which option files to read.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqldump normally reads the [client] and [mysqldump] groups. If this option
is given as --defaults-group-suffix=_other, mysqldump also reads the [client_other]
and [mysqldump_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults

443

mysqldump — A Database Backup Program

is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

DDL Options

Usage scenarios for mysqldump include setting up an entire new MySQL instance (including database
tables), and replacing data inside an existing instance with existing databases and tables. The following
options let you specify which things to tear down and set up when restoring a dump, by encoding
various DDL statements within the dump file.

• --add-drop-database

Command-Line Format

--add-drop-database

Write a DROP DATABASE statement before each CREATE DATABASE statement. This option is
typically used in conjunction with the --all-databases or --databases option because no
CREATE DATABASE statements are written unless one of those options is specified.

Note

In MySQL 8.4, the mysql schema is considered a system schema that
cannot be dropped by end users. If --add-drop-database is used with
--all-databases or with --databases where the list of schemas to
be dumped includes mysql, the dump file contains a DROP DATABASE
`mysql` statement that causes an error when the dump file is reloaded.

Instead, to use --add-drop-database, use --databases with a list of
schemas to be dumped, where the list does not include mysql.

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

444

mysqldump — A Database Backup Program

Adds to a table dump all SQL statements needed to create any tablespaces used by an NDB table.
This information is not otherwise included in the output from mysqldump. This option is currently
relevant only to NDB Cluster tables.

• --no-create-db, -n

Command-Line Format

--no-create-db

Suppress the CREATE DATABASE statements that are otherwise included in the output if the --
databases or --all-databases option is given.

• --no-create-info, -t

Command-Line Format

--no-create-info

Do not write CREATE TABLE statements that create each dumped table.

Note

This option does not exclude statements creating log file groups or
tablespaces from mysqldump output; however, you can use the --no-
tablespaces option for this purpose.

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

The following options print debugging information, encode debugging information in the dump file, or let
the dump operation proceed regardless of potential problems.

• --allow-keywords

Command-Line Format

--allow-keywords

Permit creation of column names that are keywords. This works by prefixing each column name with
the table name.

• --comments, -i

Command-Line Format

--comments

Write additional information in the dump file such as program version, server version, and host. This
option is enabled by default. To suppress this additional information, use --skip-comments.

445

mysqldump — A Database Backup Program

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o,/tmp/mysqldump.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default value is
d:t:o,/tmp/mysqldump.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

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

446

However, the date causes dump files taken at different times to appear to be different, even if the
data are otherwise identical. --dump-date and --skip-dump-date control whether the date is
added to the comment. The default is --dump-date (include the date in the comment). --skip-
dump-date suppresses date printing.

mysqldump — A Database Backup Program

• --force, -f

Command-Line Format

--force

Ignore all errors; continue even if an SQL error occurs during a table dump.

One use for this option is to cause mysqldump to continue executing even when it encounters a
view that has become invalid because the definition refers to a table that has been dropped. Without
--force, mysqldump exits with an error message. With --force, mysqldump prints the error
message, but it also writes an SQL comment containing the view definition to the dump output and
continues executing.

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

• --version, -V

Command-Line Format

--version

Display version information and exit.

Internationalization Options

The following options change how the mysqldump command represents character data with national
language settings.

• --character-sets-dir=dir_name

447

mysqldump — A Database Backup Program

Command-Line Format

--character-sets-dir=dir_name

Type

Directory name

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

Default Value

String

utf8

Use charset_name as the default character set. See Section 12.15, “Character Set Configuration”.
If no character set is specified, mysqldump uses utf8mb4.

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

The mysqldump command is frequently used to create an empty instance, or an instance including
data, on a replica server in a replication configuration. The following options apply to dumping and
restoring data on replication source servers and replicas.

• --apply-replica-statements

Command-Line Format

--apply-replica-statements

Type

Default Value

Boolean

FALSE

For a replica dump produced with the --dump-replica option, this option adds a STOP REPLICA
statement before the statement with the binary log coordinates, and a START REPLICA statement at
the end of the output.

• --apply-slave-statements

Command-Line Format

--apply-slave-statements

448

Deprecated

Type

Yes

Boolean

mysqldump — A Database Backup Program

Default Value

FALSE

This is a deprecated alias for --apply-replica-statements.

• --delete-source-logs

Command-Line Format

--delete-source-logs

On a replication source server, delete the binary logs by sending a PURGE BINARY LOGS statement
to the server after performing the dump operation. The options require the RELOAD privilege as well
as privileges sufficient to execute that statement. This option automatically enables --source-
data.

• --delete-master-logs

Command-Line Format

Deprecated

--delete-master-logs

Yes

This is a deprecated alias for --delete-source-logs.

• --dump-replica[=value]

Command-Line Format

--dump-replica[=value]

Type

Default Value

Valid Values

Numeric

1

1

2

This option is similar to --source-data, except that it is used to dump a replica server to produce
a dump file that can be used to set up another server as a replica that has the same source as
the dumped server. The option causes the dump output to include a CHANGE REPLICATION
SOURCE TO statement that indicates the binary log coordinates (file name and position) of the
dumped replica's source. The CHANGE REPLICATION SOURCE TO statement reads the values
of Relay_Master_Log_File and Exec_Master_Log_Pos from the SHOW REPLICA STATUS
output and uses them for SOURCE_LOG_FILE and SOURCE_LOG_POS respectively. These are the
replication source server coordinates from which the replica starts replicating.

Note

Inconsistencies in the sequence of transactions from the relay log which
have been executed can cause the wrong position to be used. See

449

mysqldump — A Database Backup Program

Section 19.5.1.34, “Replication and Transaction Inconsistencies” for more
information.

--dump-replica causes the coordinates from the source to be used rather than those of the
dumped server, as is done by the --source-data option. In addition, specifying this option
overrides the --source-data option.

Warning

--dump-replica should not be used if the server where the dump is going
to be applied uses gtid_mode=ON and SOURCE_AUTO_POSITION=1.

The option value is handled the same way as for --source-data. Setting no value or 1 causes
a CHANGE REPLICATION SOURCE TO statement to be written to the dump. Setting 2 causes the
statement to be written but encased in SQL comments. It has the same effect as --source-data in
terms of enabling or disabling other options and in how locking is handled.

--dump-replica causes mysqldump to stop the replication SQL thread before the dump and
restart it again after.

--dump-replica sends a SHOW REPLICA STATUS statement to the server to obtain information,
so they require privileges sufficient to execute that statement.

--apply-replica-statements and --include-source-host-port options can be used in
conjunction with --dump-replica.

• --dump-slave[=value]

Command-Line Format

--dump-slave[=value]

Deprecated

Type

Default Value

Valid Values

Yes

Numeric

1

1

2

This is a deprecated alias for --dump-replica.

• --include-source-host-port

Command-Line Format

--include-source-host-port

Type

Default Value

Boolean

FALSE

Adds the SOURCE_HOST and SOURCE_PORT options for the host name and TCP/IP port number
of the replica's source, to the CHANGE REPLICATION SOURCE TO statement in a replica dump
produced with the --dump-replica option.

• --include-master-host-port

Command-Line Format

--include-master-host-port

Deprecated

Type

Default Value

Yes

Boolean

FALSE

450

mysqldump — A Database Backup Program

This is a deprecated alias for --include-source-host-port.

• --master-data[=value]

Command-Line Format

--master-data[=value]

Deprecated

Type

Default Value

Valid Values

Yes

Numeric

1

1

2

This is a deprecated alias for --source-data.

• --output-as-version=value

Command-Line Format

--output-as-version=value

Type

Default Value

Valid Values

Enumeration

SERVER

BEFORE_8_0_23

BEFORE_8_2_0

Determines the level of terminology used for statements relating to replicas and events, making it
possible to create dumps compatible with older versions of MySQL that do not accept the newer
terminology. This option can take any one of the following values, with effects described as listed
here:

• SERVER: Reads the server version and uses the latest versions of statements compatible with that

version. This is the default value.

• BEFORE_8_0_23: Replication SQL statements using deprecated terms such as “slave” and
“master” are written to the output in place of those using “replica” and “source”, as in MySQL
versions prior to 8.0.23.

This option also duplicates the effects of BEFORE_8_2_0 on the output of SHOW CREATE EVENT.

• BEFORE_8_2_0: This option causes SHOW CREATE EVENT to reflect how the event would have
been created in a MySQL server prior to version 8.2.0, displaying DISABLE ON SLAVE rather
than DISABLE ON REPLICA.

This option affects the output from --events, --dump-replica, --source-data, --apply-
replica-statements, and --include-source-host-port.

• --source-data[=value]

Command-Line Format

--source-data[=value]

Type

Default Value

Valid Values

Numeric

1

1

451

mysqldump — A Database Backup Program

2

Used to dump a replication source server to produce a dump file that can be used to set up
another server as a replica of the source. The options cause the dump output to include a CHANGE
REPLICATION SOURCE TO statement that indicates the binary log coordinates (file name and
position) of the dumped server. These are the replication source server coordinates from which the
replica should start replicating after you load the dump file into the replica.

If the option value is 2, the CHANGE REPLICATION SOURCE TO statement is written as an SQL
comment, and thus is informative only; it has no effect when the dump file is reloaded. If the
option value is 1, the statement is not written as a comment and takes effect when the dump file is
reloaded. If no option value is specified, the default value is 1.

--source-data sends a SHOW BINARY LOG STATUS statement to the server to obtain
information, so they require privileges sufficient to execute that statement. This option also requires
the RELOAD privilege and the binary log must be enabled.

--source-data automatically turns off --lock-tables. They also turn on --lock-all-
tables, unless --single-transaction also is specified, in which case, a global read lock is
acquired only for a short time at the beginning of the dump (see the description for --single-
transaction). In all cases, any action on logs happens at the exact moment of the dump.

It is also possible to set up a replica by dumping an existing replica of the source, using the --dump-
replica option, which overrides --source-data causing it to be ignored.

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

This option is for servers that use GTID-based replication (gtid_mode=ON). It controls the inclusion
of a SET @@GLOBAL.gtid_purged statement in the dump output, which updates the value of
gtid_purged on a server where the dump file is reloaded, to add the GTID set from the source
server's gtid_executed system variable. gtid_purged holds the GTIDs of all transactions that
have been applied on the server, but do not exist on any binary log file on the server. mysqldump
therefore adds the GTIDs for the transactions that were executed on the source server, so that the
target server records these transactions as applied, although it does not have them in its binary
logs. --set-gtid-purged also controls the inclusion of a SET @@SESSION.sql_log_bin=0
statement, which disables binary logging while the dump file is being reloaded. This statement
prevents new GTIDs from being generated and assigned to the transactions in the dump file as they
are executed, so that the original GTIDs for the transactions are used.

If you do not set the --set-gtid-purged option, the default is that a SET
@@GLOBAL.gtid_purged statement is included in the dump output if GTIDs are enabled on the
server you are backing up, and the set of GTIDs in the global value of the gtid_executed system
variable is not empty. A SET @@SESSION.sql_log_bin=0 statement is also included if GTIDs are
enabled on the server.

You can either replace the value of gtid_purged with a specified GTID set, or add a plus
sign (+) to the statement to append a specified GTID set to the GTID set that is already held by

452

mysqldump — A Database Backup Program

gtid_purged. The SET @@GLOBAL.gtid_purged statement recorded by mysqldump includes a
plus sign (+) in a version-specific comment, such that MySQL adds the GTID set from the dump file
to the existing gtid_purged value.

It is important to note that the value that is included by mysqldump for the SET
@@GLOBAL.gtid_purged statement includes the GTIDs of all transactions in the gtid_executed
set on the server, even those that changed suppressed parts of the database, or other databases
on the server that were not included in a partial dump. This can mean that after the gtid_purged
value has been updated on the server where the dump file is replayed, GTIDs are present that do
not relate to any data on the target server. If you do not replay any further dump files on the target
server, the extraneous GTIDs do not cause any problems with the future operation of the server,
but they make it harder to compare or reconcile GTID sets on different servers in the replication
topology. If you do replay a further dump file on the target server that contains the same GTIDs (for
example, another partial dump from the same origin server), any SET @@GLOBAL.gtid_purged
statement in the second dump file fails. In this case, either remove the statement manually before
replaying the dump file, or output the dump file without the statement.

If the SET @@GLOBAL.gtid_purged statement would not have the desired result on your target
server, you can exclude the statement from the output, or include it but comment it out so that it is
not actioned automatically. You can also include the statement but manually edit it in the dump file to
achieve the desired result.

The possible values for the --set-gtid-purged option are as follows:

AUTO

OFF

ON

COMMENTED

The default value. If GTIDs are enabled on the server you
are backing up and gtid_executed is not empty, SET
@@GLOBAL.gtid_purged is added to the output, containing
the GTID set from gtid_executed. If GTIDs are enabled, SET
@@SESSION.sql_log_bin=0 is added to the output. If GTIDs
are not enabled on the server, the statements are not added to
the output.

SET @@GLOBAL.gtid_purged is not added to the output, and
SET @@SESSION.sql_log_bin=0 is not added to the output.
For a server where GTIDs are not in use, use this option or
AUTO. Only use this option for a server where GTIDs are in use
if you are sure that the required GTID set is already present in
gtid_purged on the target server and should not be changed,
or if you plan to identify and add any missing GTIDs manually.

If GTIDs are enabled on the server you are backing
up, SET @@GLOBAL.gtid_purged is added to the
output (unless gtid_executed is empty), and SET
@@SESSION.sql_log_bin=0 is added to the output. An error
occurs if you set this option but GTIDs are not enabled on the
server. For a server where GTIDs are in use, use this option or
AUTO, unless you are sure that the GTIDs in gtid_executed are
not needed on the target server.

If GTIDs are enabled on the server you are backing up, SET
@@GLOBAL.gtid_purged is added to the output (unless
gtid_executed is empty), but it is commented out. This means
that the value of gtid_executed is available in the output, but
no action is taken automatically when the dump file is reloaded.
SET @@SESSION.sql_log_bin=0 is added to the output, and it
is not commented out. With COMMENTED, you can control the use
of the gtid_executed set manually or through automation. For
example, you might prefer to do this if you are migrating data to
another server that already has different active databases.

453

mysqldump — A Database Backup Program

Format Options

The following options specify how to represent the entire dump file or certain kinds of data in the dump
file. They also control whether certain optional information is written to the dump file.

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
The only permitted value for this option is ansi, which has the same meaning as the corresponding
option for setting the server SQL mode. See Section 7.1.11, “Server SQL Modes”.

• --complete-insert, -c

Command-Line Format

--complete-insert

Use complete INSERT statements that include column names.

• --create-options

Command-Line Format

--create-options

454

Include all MySQL-specific table options in the CREATE TABLE statements.

mysqldump — A Database Backup Program

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
FIELDS clauses for LOAD DATA. See Section 15.2.9, “LOAD DATA Statement”.

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
clause for LOAD DATA. See Section 15.2.9, “LOAD DATA Statement”.

• --quote-names, -Q

Command-Line Format

Disabled by

--quote-names

skip-quote-names

Quote identifiers (such as database, table, and column names) within ` characters. If the
ANSI_QUOTES SQL mode is enabled, identifiers are quoted within " characters. This option is
enabled by default. It can be disabled with --skip-quote-names, but this option should be given
after any option such as --compatible that may enable --quote-names.

• --result-file=file_name, -r file_name

Command-Line Format

--result-file=file_name

455

mysqldump — A Database Backup Program

Type

File name

Direct output to the named file. The result file is created and its previous contents overwritten, even if
an error occurs while generating the dump.

This option should be used on Windows to prevent newline \n characters from being converted to
\r\n carriage return/newline sequences.

• --show-create-skip-secondary-engine=value

Command-Line Format

--show-create-skip-secondary-engine

Excludes the SECONDARY ENGINE clause from CREATE TABLE statements. It does
so by enabling the show_create_table_skip_secondary_engine system
variable for the duration of the dump operation. Alternatively, you can enable the
show_create_table_skip_secondary_engine system variable prior to using mysqldump.

• --tab=dir_name, -T dir_name

Command-Line Format

Type

--tab=dir_name

Directory name

Produce tab-separated text-format data files. For each dumped table, mysqldump creates a
tbl_name.sql file that contains the CREATE TABLE statement that creates the table, and the
server writes a tbl_name.txt file that contains its data. The option value is the directory in which to
write the files.

Note

This option should be used only when mysqldump is run on the same
machine as the mysqld server. Because the server creates *.txt files in
the directory that you specify, the directory must be writable by the server
and the MySQL account that you use must have the FILE privilege. Because
mysqldump creates *.sql in the same directory, it must be writable by your
system login account.

By default, the .txt data files are formatted using tab characters between column values and a
newline at the end of each line. The format can be specified explicitly using the --fields-xxx and
--lines-terminated-by options.

Column values are converted to the character set specified by the --default-character-set
option.

• --tz-utc

Command-Line Format

Disabled by

--tz-utc

skip-tz-utc

456

This option enables TIMESTAMP columns to be dumped and reloaded between servers
in different time zones. mysqldump sets its connection time zone to UTC and adds SET
TIME_ZONE='+00:00' to the dump file. Without this option, TIMESTAMP columns are dumped and
reloaded in the time zones local to the source and destination servers, which can cause the values
to change if the servers are in different time zones. --tz-utc also protects against changes due to
daylight saving time. --tz-utc is enabled by default. To disable it, use --skip-tz-utc.

mysqldump — A Database Backup Program

• --xml, -X

Command-Line Format

--xml

Write dump output as well-formed XML.

NULL, 'NULL', and Empty Values: For a column named column_name, the NULL value, an empty
string, and the string value 'NULL' are distinguished from one another in the output generated by
this option as follows.

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
(See Section 6.5.1.1, “mysql Client Options”.)

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

457

mysqldump — A Database Backup Program

Filtering Options

The following options control which kinds of schema objects are written to the dump file: by category,
such as triggers or events; by name, for example, choosing which databases and tables to dump; or
even filtering rows from the table data using a WHERE clause.

• --all-databases, -A

Command-Line Format

--all-databases

Dump all tables in all databases. This is the same as using the --databases option and naming all
the databases on the command line.

Note

See the --add-drop-database description for information about an
incompatibility of that option with --all-databases.

Prior to MySQL 8.4, the --routines and --events options for mysqldump were not required
to include stored routines and events when using the --all-databases option: The dump
included the mysql system database, and therefore also the mysql.proc and mysql.event
tables containing stored routine and event definitions. As of MySQL 8.4, the mysql.event and
mysql.proc tables are not used. Definitions for the corresponding objects are stored in data
dictionary tables, but those tables are not dumped. To include stored routines and events in a dump
made using --all-databases, use the --routines and --events options explicitly.

• --databases, -B

Command-Line Format

--databases

Dump several databases. Normally, mysqldump treats the first name argument on the command
line as a database name and following names as table names. With this option, it treats all name
arguments as database names. CREATE DATABASE and USE statements are included in the output
before each new database.

This option may be used to dump the performance_schema database, which normally is not
dumped even with the --all-databases option. (Also use the --skip-lock-tables option.)

Note

See the --add-drop-database description for information about an
incompatibility of that option with --databases.

• --events, -E

Command-Line Format

--events

Include Event Scheduler events for the dumped databases in the output. This option requires the
EVENT privileges for those databases.

The output generated by using --events contains CREATE EVENT statements to create the events.

• --ignore-error=error[,error]...

Command-Line Format

--ignore-error=error[,error]...

Type

String

458

mysqldump — A Database Backup Program

Ignore the specified errors. The option value is a list of comma-separated error numbers specifying
the errors to ignore during mysqldump execution. If the --force option is also given to ignore all
errors, --force takes precedence.

• --ignore-table=db_name.tbl_name

Command-Line Format

--ignore-table=db_name.tbl_name

Type

String

Do not dump the given table, which must be specified using both the database and table names. To
ignore multiple tables, use this option multiple times. This option also can be used to ignore views.

• --ignore-views=boolean

Command-Line Format

--ignore-views

Type

Default Value

Boolean

FALSE

Skips table views in the dump file.

• --init-command=str

Command-Line Format

--init-command=str

Type

String

Single SQL statement to execute after connecting to the MySQL server. The definition resets existing
statements defined by it or init-command-add.

• --init-command-add=str

Command-Line Format

--init-command-add=str

Type

String

Add an additional SQL statement to execute after connecting or reconnecting to the MySQL server.
It's usable without --init-command but has no effect if used before it because init-command
resets the list of commands to call.

• --no-data, -d

Command-Line Format

--no-data

Do not write any table row information (that is, do not dump table contents). This is useful if you want
to dump only the CREATE TABLE statement for the table (for example, to create an empty copy of
the table by loading the dump file).

459

mysqldump — A Database Backup Program

• --routines, -R

Command-Line Format

--routines

Include stored routines (procedures and functions) for the dumped databases in the output. This
option requires the global SELECT privilege.

The output generated by using --routines contains CREATE PROCEDURE and CREATE
FUNCTION statements to create the routines.

• --skip-generated-invisible-primary-key

Command-Line Format

Type

Default Value

--skip-generated-invisible-primary-
key

Boolean

FALSE

This option causes generated invisible primary keys to be excluded from the output. For more
information, see Section 15.1.20.11, “Generated Invisible Primary Keys”.

• --tables

Command-Line Format

--tables

Override the --databases or -B option. mysqldump regards all name arguments following the
option as table names.

• --triggers

Command-Line Format

Disabled by

--triggers

skip-triggers

Include triggers for each dumped table in the output. This option is enabled by default; disable it with
--skip-triggers.

To be able to dump a table's triggers, you must have the TRIGGER privilege for the table.

Multiple triggers are permitted. mysqldump dumps triggers in activation order so that when the dump
file is reloaded, triggers are created in the same activation order. However, if a mysqldump dump
file contains multiple triggers for a table that have the same trigger event and action time, an error
occurs for attempts to load the dump file into an older server that does not support multiple triggers.
(For a workaround, see Downgrade Notes; you can convert triggers to be compatible with older
servers.)

• --where='where_condition', -w 'where_condition'

Command-Line Format

--where='where_condition'

Dump only rows selected by the given WHERE condition. Quotes around the condition are mandatory
if it contains spaces or other characters that are special to your command interpreter.

Examples:

--where="user='jimf'"
-w"userid>1"

460

mysqldump — A Database Backup Program

-w"userid<1"

Performance Options

The following options are the most relevant for the performance particularly of the restore operations.
For large data sets, restore operation (processing the INSERT statements in the dump file) is the most
time-consuming part. When it is urgent to restore data quickly, plan and test the performance of this
stage in advance. For restore times measured in hours, you might prefer an alternative backup and
restore solution, such as MySQL Enterprise Backup for InnoDB-only and mixed-use databases.

Performance is also affected by the transactional options, primarily for the dump operation.

• --column-statistics

Command-Line Format

--column-statistics

Type

Default Value

Boolean

OFF

Add ANALYZE TABLE statements to the output to generate histogram statistics for dumped tables
when the dump file is reloaded. This option is disabled by default because histogram generation for
large tables can take a long time.

• --disable-keys, -K

Command-Line Format

--disable-keys

For each table, surround the INSERT statements with /*!40000 ALTER TABLE tbl_name
DISABLE KEYS */; and /*!40000 ALTER TABLE tbl_name ENABLE KEYS */; statements.
This makes loading the dump file faster because the indexes are created after all rows are inserted.
This option is effective only for nonunique indexes of MyISAM tables.

• --extended-insert, -e

Command-Line Format

Disabled by

--extended-insert

skip-extended-insert

Write INSERT statements using multiple-row syntax that includes several VALUES lists. This results
in a smaller dump file and speeds up inserts when the file is reloaded.

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

The maximum size of the buffer for client/server communication. The default is 24MB, the maximum
is 1GB.

461

mysqldump — A Database Backup Program

Note

The value of this option is specific to mysqldump and should not be confused
with the MySQL server's max_allowed_packet system variable; the server
value cannot be exceeded by a single packet from mysqldump, regardless of
any setting for the mysqldump option, even if the latter is larger.

• --mysqld-long-query-time=value

Command-Line Format

--mysqld-long-query-time=value

Type

Default Value

Numeric

Server global setting

Set the session value of the long_query_time system variable. Use this option if you want to
increase the time allowed for queries from mysqldump before they are logged to the slow query
log file. mysqldump performs a full table scan, which means its queries can often exceed a global
long_query_time setting that is useful for regular queries. The default global setting is 10
seconds.

You can use --mysqld-long-query-time to specify a session value from 0 (meaning that every
query from mysqldump is logged to the slow query log) to 31536000, which is 365 days in seconds.
For mysqldump’s option, you can only specify whole seconds. When you do not specify this option,
the server’s global setting applies to mysqldump’s queries.

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

• --network-timeout, -M

Command-Line Format

--network-timeout[={0|1}]

Type

Default Value

Boolean

TRUE

Enable large tables to be dumped by setting --max-allowed-packet to its maximum value and
network read and write timeouts to a large value. This option is enabled by default. To disable it, use
--skip-network-timeout.

• --opt

Command-Line Format

Disabled by

--opt

skip-opt

462

This option, enabled by default, is shorthand for the combination of --add-drop-table --add-
locks --create-options --disable-keys --extended-insert --lock-tables --quick

mysqldump — A Database Backup Program

--set-charset. It gives a fast dump operation and produces a dump file that can be reloaded into
a MySQL server quickly.

Because the --opt option is enabled by default, you only specify its converse, the --skip-opt
to turn off several default settings. See the discussion of mysqldump option groups for information
about selectively enabling or disabling a subset of the options affected by --opt.

• --quick, -q

Command-Line Format

Disabled by

--quick

skip-quick

This option is useful for dumping large tables. It forces mysqldump to retrieve rows for a table from
the server a row at a time rather than retrieving the entire row set and buffering it in memory before
writing it out.

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

Surround each table dump with LOCK TABLES and UNLOCK TABLES statements. This results
in faster inserts when the dump file is reloaded. See Section 10.2.5.1, “Optimizing INSERT
Statements”.

• --flush-logs, -F

Command-Line Format

--flush-logs

Flush the MySQL server log files before starting the dump. This option requires the RELOAD
privilege. If you use this option in combination with the --all-databases option, the logs are
flushed for each database dumped. The exception is when using --lock-all-tables, --
source-data, or --single-transaction. In these cases, the logs are flushed only once,
corresponding to the moment that all tables are locked by FLUSH TABLES WITH READ LOCK.
If you want your dump and the log flush to happen at exactly the same moment, you should
use --flush-logs together with --lock-all-tables, --source-data, or --single-
transaction.

• --flush-privileges

Command-Line Format

--flush-privileges

Add a FLUSH PRIVILEGES statement to the dump output after dumping the mysql database. This
option should be used any time the dump contains the mysql database and any other database that
depends on the data in the mysql database for proper restoration.

463

mysqldump — A Database Backup Program

Because the dump file contains a FLUSH PRIVILEGES statement, reloading the file requires
privileges sufficient to execute that statement.

• --lock-all-tables, -x

Command-Line Format

--lock-all-tables

Lock all tables across all databases. This is achieved by acquiring a global read lock for the duration
of the whole dump. This option automatically turns off --single-transaction and --lock-
tables.

• --lock-tables, -l

Command-Line Format

--lock-tables

For each dumped database, lock all tables to be dumped before dumping them. The tables are
locked with READ LOCAL to permit concurrent inserts in the case of MyISAM tables. For transactional
tables such as InnoDB, --single-transaction is a much better option than --lock-tables
because it does not need to lock the tables at all.

Because --lock-tables locks tables for each database separately, this option does not guarantee
that the tables in the dump file are logically consistent between databases. Tables in different
databases may be dumped in completely different states.

Some options, such as --opt, automatically enable --lock-tables. If you want to override this,
use --skip-lock-tables at the end of the option list.

• --no-autocommit

Command-Line Format

--no-autocommit

Enclose the INSERT statements for each dumped table within SET autocommit = 0 and COMMIT
statements.

• --order-by-primary

Command-Line Format

--order-by-primary

Dump each table's rows sorted by its primary key, or by its first unique index, if such an index exists.
This is useful when dumping a MyISAM table to be loaded into an InnoDB table, but makes the
dump operation take considerably longer.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

464

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

mysqldump — A Database Backup Program

• --single-transaction

Command-Line Format

--single-transaction

This option sets the transaction isolation mode to REPEATABLE READ and sends a START
TRANSACTION SQL statement to the server before dumping data. It is useful only with transactional
tables such as InnoDB, because then it dumps the consistent state of the database at the time when
START TRANSACTION was issued without blocking any applications.

The RELOAD or FLUSH_TABLES privilege is required with --single-transaction if both
gtid_mode=ON and gtid_purged=ON|AUTO.

When using this option, you should keep in mind that only InnoDB tables are dumped in a consistent
state. For example, any MyISAM or MEMORY tables dumped while using this option may still change
state.

While a --single-transaction dump is in process, to ensure a valid dump file (correct table
contents and binary log coordinates), no other connection should use the following statements:
ALTER TABLE, CREATE TABLE, DROP TABLE, RENAME TABLE, TRUNCATE TABLE. A consistent
read is not isolated from those statements, so use of them on a table to be dumped can cause the
SELECT that is performed by mysqldump to retrieve the table contents to obtain incorrect contents
or fail.

The --single-transaction option and the --lock-tables option are mutually exclusive
because LOCK TABLES causes any pending transactions to be committed implicitly.

To dump large tables, combine the --single-transaction option with the --quick option.

Option Groups

• The --opt option turns on several settings that work together to perform a fast dump operation.
All of these settings are on by default, because --opt is on by default. Thus you rarely if ever
specify --opt. Instead, you can turn these settings off as a group by specifying --skip-opt, then
optionally re-enable certain settings by specifying the associated options later on the command line.

• The --compact option turns off several settings that control whether optional statements and

comments appear in the output. Again, you can follow this option with other options that re-enable
certain settings, or turn all the settings on by using the --skip-compact form.

When you selectively enable or disable the effect of a group option, order is important because options
are processed first to last. For example, --disable-keys --lock-tables --skip-opt would not
have the intended effect; it is the same as --skip-opt by itself.

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

465

mysqlimport — A Data Import Program

You can dump several databases with one command:

mysqldump --databases db_name1 [db_name2 ...] > my_databases.sql

To dump all databases, use the --all-databases option:

mysqldump --all-databases > all_databases.sql

For InnoDB tables, mysqldump provides a way of making an online backup:

mysqldump --all-databases --source-data --single-transaction > all_databases.sql

This backup acquires a global read lock on all tables (using FLUSH TABLES WITH READ LOCK) at
the beginning of the dump. As soon as this lock has been acquired, the binary log coordinates are read
and the lock is released. If long updating statements are running when the FLUSH statement is issued,
the MySQL server may get stalled until those statements finish. After that, the dump becomes lock free
and does not disturb reads and writes on the tables. If the update statements that the MySQL server
receives are short (in terms of execution time), the initial lock period should not be noticeable, even
with many updates.

For point-in-time recovery (also known as “roll-forward,” when you need to restore an old backup
and replay the changes that happened since that backup), it is often useful to rotate the binary log
(see Section 7.4.4, “The Binary Log”) or at least know the binary log coordinates to which the dump
corresponds:

mysqldump --all-databases --source-data=2 > all_databases.sql

Or:

mysqldump --all-databases --flush-logs --source-data=2 > all_databases.sql

The --source-data option can be used simultaneously with the --single-transaction option,
which provides a convenient way to make an online backup suitable for use prior to point-in-time
recovery if tables are stored using the InnoDB storage engine.

For more information on making backups, see Section 9.2, “Database Backup Methods”, and
Section 9.3, “Example Backup and Recovery Strategy”.

• To select the effect of --opt except for some features, use the --skip option for each feature. To
disable extended inserts and memory buffering, use --opt --skip-extended-insert --skip-
quick. (Actually, --skip-extended-insert --skip-quick is sufficient because --opt is on
by default.)

• To reverse --opt for all features except disabling of indexes and table locking, use --skip-opt --

disable-keys --lock-tables.

Restrictions

mysqldump does not dump the performance_schema or sys schema by default. To dump any of
these, name them explicitly on the command line. You can also name them with the --databases
option. For performance_schema, also use the --skip-lock-tables option.

mysqldump does not dump the INFORMATION_SCHEMA schema.

mysqldump does not dump InnoDB CREATE TABLESPACE statements.

mysqldump does not dump the NDB Cluster ndbinfo information database.

mysqldump includes statements to recreate the general_log and slow_query_log tables for
dumps of the mysql database. Log table contents are not dumped.

If you encounter problems backing up views due to insufficient privileges, see Section 27.9,
“Restrictions on Views” for a workaround.

6.5.5 mysqlimport — A Data Import Program

466

mysqlimport — A Data Import Program

The mysqlimport client provides a command-line interface to the LOAD DATA SQL statement. Most
options to mysqlimport correspond directly to clauses of LOAD DATA syntax. See Section 15.2.9,
“LOAD DATA Statement”.

Invoke mysqlimport like this:

mysqlimport [options] db_name textfile1 [textfile2 ...]

For each text file named on the command line, mysqlimport strips any extension from the file name
and uses the result to determine the name of the table into which to import the file's contents. For
example, files named patient.txt, patient.text, and patient all would be imported into a table
named patient.

mysqlimport supports the following options, which can be specified on the command line or in the
[mysqlimport] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.14 mysqlimport Options

Option Name

--bind-address

--character-sets-dir

--columns

--compress

--compression-algorithms

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--delete

--enable-cleartext-plugin

--fields-enclosed-by

--fields-escaped-by

--fields-optionally-enclosed-by

--fields-terminated-by

--force

--get-server-public-key

--help

Description

Use specified network interface to connect to
MySQL Server

Directory where character sets can be found

This option takes a comma-separated list of
column names as its value

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Write debugging log

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Specify default character set

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Empty the table before importing the text file

Enable cleartext authentication plugin

This option has the same meaning as the
corresponding clause for LOAD DATA

This option has the same meaning as the
corresponding clause for LOAD DATA

This option has the same meaning as the
corresponding clause for LOAD DATA

This option has the same meaning as the
corresponding clause for LOAD DATA

Continue even if an SQL error occurs

Request RSA public key from server

Display help message and exit

467

mysqlimport — A Data Import Program

Option Name

--host

--ignore

--ignore-lines

--lines-terminated-by

--local

--lock-tables

--login-path

--low-priority

--no-defaults

--no-login-paths

--password

--password1

--password2

--password3

--pipe

--plugin-dir

--port

--print-defaults

--protocol

--replace

--server-public-key-path

--shared-memory-base-name

--silent

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

468

Description

Host on which MySQL server is located

See the description for the --replace option

Ignore the first N lines of the data file

This option has the same meaning as the
corresponding clause for LOAD DATA

Read input files locally from the client host

Lock all tables for writing before processing any
text files

Read login path options from .mylogin.cnf

Use LOW_PRIORITY when loading the table

Read no option files

Do not read login paths from the login path file

Password to use when connecting to server

First multifactor authentication password to use
when connecting to server

Second multifactor authentication password to use
when connecting to server

Third multifactor authentication password to use
when connecting to server

Connect to server using named pipe (Windows
only)

Directory where plugins are installed

TCP/IP port number for connection

Print default options

Transport protocol to use

The --replace and --ignore options control
handling of input rows that duplicate existing rows
on unique key values

Path name to file containing RSA public key

Shared-memory name for shared-memory
connections (Windows only)

Produce output only when errors occur

Unix socket file or Windows named pipe to use

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

mysqlimport — A Data Import Program

Option Name

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tls-ciphersuites

--tls-sni-servername

--tls-version

--use-threads

--user

--verbose

--version

--zstd-compression-level

• --help, -?

Description

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

Number of threads for parallel file-loading

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Compression level for connections to server that
use zstd compression

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

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --columns=column_list, -c column_list

Command-Line Format

--columns=column_list

This option takes a list of comma-separated column names as its value. The order of the column
names indicates how to match data file columns with table columns.

• --compress, -C

Command-Line Format

Deprecated

--compress[={OFF|ON}]

Yes

469

mysqlimport — A Data Import Program

Type

Default Value

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

For more information, see Section 6.2.8, “Connection Compression Control”.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info

Command-Line Format

Type

--debug-info

Boolean

470

mysqlimport — A Data Import Program

Default Value

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

Use charset_name as the default character set. See Section 12.15, “Character Set Configuration”.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

471

Command-Line Format

--defaults-group-suffix=str

mysqlimport — A Data Import Program

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlimport normally reads the [client] and [mysqlimport] groups. If
this option is given as --defaults-group-suffix=_other, mysqlimport also reads the
[client_other] and [mysqlimport_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --delete, -D

Command-Line Format

--delete

Empty the table before importing the text file.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

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

472

These options have the same meaning as the corresponding clauses for LOAD DATA. See
Section 15.2.9, “LOAD DATA Statement”.

mysqlimport — A Data Import Program

• --force, -f

Command-Line Format

--force

Ignore errors. For example, if a table for a text file does not exist, continue processing any remaining
files. Without --force, mysqlimport exits if a table does not exist.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

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

Ignore the first N lines of the data file.

• --lines-terminated-by=...

--ignore-lines=#

Numeric

Command-Line Format

--lines-terminated-by=string

Type

String

This option has the same meaning as the corresponding clause for LOAD DATA. For example, to
import Windows files that have lines terminated with carriage return/linefeed pairs, use --lines-

473

mysqlimport — A Data Import Program

terminated-by="\r\n". (You might have to double the backslashes, depending on the escaping
conventions of your command interpreter.) See Section 15.2.9, “LOAD DATA Statement”.

• --local, -L

Command-Line Format

Type

Default Value

--local

Boolean

FALSE

By default, files are read by the server on the server host. With this option, mysqlimport reads
input files locally on the client host.

Successful use of LOCAL load operations within mysqlimport also requires that the server permits
local loading; see Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”

• --lock-tables, -l

Command-Line Format

--lock-tables

Lock all tables for writing before processing any text files. This ensures that all tables are
synchronized on the server.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --low-priority

474

Command-Line Format

--low-priority

Use LOW_PRIORITY when loading the table. This affects only storage engines that use only table-

level locking (such as MyISAM, MEMORY, and MERGE).

mysqlimport — A Data Import Program

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqlimport prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlimport should not prompt for one, use
the --skip-password option.

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to the
server. The password value is optional. If not given, mysqlimport prompts for one. If given, there
must be no space between --password1= and the password following it. If no password option is
specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlimport should not prompt for one, use
the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

475

mysqlimport — A Data Import Program

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

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
used to specify an authentication plugin but mysqlimport does not find it. See Section 8.2.17,
“Pluggable Authentication”.

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

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

--protocol=type

Type

Default Value

Valid Values

476

String

[see text]

TCP

SOCKET

PIPE

MEMORY

mysqlimport — A Data Import Program

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --replace, -r

Command-Line Format

--replace

The --replace and --ignore options control handling of input rows that duplicate existing rows
on unique key values. If you specify --replace, new rows replace existing rows that have the same
unique key value. If you specify --ignore, input rows that duplicate an existing row on a unique key
value are skipped. If you do not specify either option, an error occurs when a duplicate key value is
found, and the rest of the text file is ignored.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --silent, -s

Command-Line Format

--silent

Silent mode. Produce output only when errors occur.

477

mysqlimport — A Data Import Program

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tls-ciphersuites=ciphersuite_list

478

Command-Line Format

--tls-ciphersuites=ciphersuite_list

mysqlimport — A Data Import Program

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

• --use-threads=N

Command-Line Format

Type

Load files in parallel using N threads.

• --verbose, -v

--use-threads=#

Numeric

Command-Line Format

--verbose

479

mysqlshow — Display Database, Table, and Column Information

Verbose mode. Print more information about what the program does.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

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

6.5.6 mysqlshow — Display Database, Table, and Column Information

The mysqlshow client can be used to quickly see which databases exist, their tables, or a table's
columns or indexes.

mysqlshow provides a command-line interface to several SQL SHOW statements. See Section 15.7.7,
“SHOW Statements”. The same information can be obtained by using those statements directly. For
example, you can issue them from the mysql client program.

Invoke mysqlshow like this:

mysqlshow [options] [db_name [tbl_name [col_name]]]

• If no database is given, a list of database names is shown.

• If no table is given, all matching tables in the database are shown.

• If no column is given, all matching columns and column types in the table are shown.

480

mysqlshow — Display Database, Table, and Column Information

The output displays only the names of those databases, tables, or columns for which you have some
privileges.

If the last argument contains shell or SQL wildcard characters (*, ?, %, or _), only those names that are
matched by the wildcard are shown. If a database name contains any underscores, those should be
escaped with a backslash (some Unix shells require two) to get a list of the proper tables or columns.
* and ? characters are converted into SQL % and _ wildcard characters. This might cause some
confusion when you try to display the columns for a table with a _ in the name, because in this case,
mysqlshow shows you only the table names that match the pattern. This is easily fixed by adding an
extra % last on the command line as a separate argument.

mysqlshow supports the following options, which can be specified on the command line or in the
[mysqlshow] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.15 mysqlshow Options

Option Name

--bind-address

--character-sets-dir

--compress

--compression-algorithms

--count

--debug

--debug-check

--debug-info

--default-auth

--default-character-set

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--enable-cleartext-plugin

--get-server-public-key

--help

--host

--keys

--login-path

--no-defaults

--no-login-paths

--password

--password1

--password2

Description

Use specified network interface to connect to
MySQL Server

Directory where character sets can be found

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Show the number of rows per table

Write debugging log

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Specify default character set

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Enable cleartext authentication plugin

Request RSA public key from server

Display help message and exit

Host on which MySQL server is located

Show table indexes

Read login path options from .mylogin.cnf

Read no option files

Do not read login paths from the login path file

Password to use when connecting to server

First multifactor authentication password to use
when connecting to server

Second multifactor authentication password to use
when connecting to server

481

mysqlshow — Display Database, Table, and Column Information

Option Name

--password3

--pipe

--plugin-dir

--port

--print-defaults

--protocol

--server-public-key-path

--shared-memory-base-name

--show-table-type

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--status

--tls-ciphersuites

--tls-sni-servername

--tls-version

--user

--verbose

--version

--zstd-compression-level

Description

Third multifactor authentication password to use
when connecting to server

Connect to server using named pipe (Windows
only)

Directory where plugins are installed

TCP/IP port number for connection

Print default options

Transport protocol to use

Path name to file containing RSA public key

Shared-memory name for shared-memory
connections (Windows only)

Show a column indicating the table type

Unix socket file or Windows named pipe to use

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Display extra information about each table

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Compression level for connections to server that
use zstd compression

482

mysqlshow — Display Database, Table, and Column Information

• --help, -?

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

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

483

For more information, see Section 6.2.8, “Connection Compression Control”.

mysqlshow — Display Database, Table, and Column Information

• --count

Command-Line Format

--count

Show the number of rows per table. This can be slow for non-MyISAM tables.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --default-character-set=charset_name

Command-Line Format

--default-character-set=charset_name

Type

String

484

Use charset_name as the default character set. See Section 12.15, “Character Set Configuration”.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

mysqlshow — Display Database, Table, and Column Information

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlshow normally reads the [client] and [mysqlshow] groups. If this option
is given as --defaults-group-suffix=_other, mysqlshow also reads the [client_other]
and [mysqlshow_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

485

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

mysqlshow — Display Database, Table, and Column Information

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the RSA public key that it uses for key pair-based password exchange.
This option applies to clients that connect to the server using an account that authenticates with the
caching_sha2_password authentication plugin. For connections by such accounts, the server
does not send the public key to the client unless requested. The option is ignored for accounts
that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not
needed, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

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
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

486

mysqlshow — Display Database, Table, and Column Information

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqlshow prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlshow should not prompt for one, use
the --skip-password option.

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to
the server. The password value is optional. If not given, mysqlshow prompts for one. If given, there

487

mysqlshow — Display Database, Table, and Column Information

must be no space between --password1= and the password following it. If no password option is
specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlshow should not prompt for one, use
the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

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
to specify an authentication plugin but mysqlshow does not find it. See Section 8.2.17, “Pluggable
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

488

mysqlshow — Display Database, Table, and Column Information

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

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
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --show-table-type, -t

489

mysqlshow — Display Database, Table, and Column Information

Command-Line Format

--show-table-type

Show a column indicating the table type, as in SHOW FULL TABLES. The type is BASE TABLE or
VIEW.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

490

mysqlshow — Display Database, Table, and Column Information

• --status, -i

Command-Line Format

--status

Display extra information about each table.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

491

The user name of the MySQL account to use for connecting to the server.

mysqlslap — A Load Emulation Client

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This option can be used
multiple times to increase the amount of information.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

6.5.7 mysqlslap — A Load Emulation Client

mysqlslap is a diagnostic program designed to emulate client load for a MySQL server and to report
the timing of each stage. It works as if multiple clients are accessing the server.

Invoke mysqlslap like this:

mysqlslap [options]

Some options such as --create or --query enable you to specify a string containing an SQL
statement or a file containing statements. If you specify a file, by default it must contain one statement
per line. (That is, the implicit statement delimiter is the newline character.) Use the --delimiter
option to specify a different delimiter, which enables you to specify statements that span multiple lines
or place multiple statements on a single line. You cannot include comments in a file; mysqlslap does
not understand them.

mysqlslap runs in three stages:

1. Create schema, table, and optionally any stored programs or data to use for the test. This stage

uses a single client connection.

2. Run the load test. This stage can use many client connections.

3. Clean up (disconnect, drop table if specified). This stage uses a single client connection.

Examples:

Supply your own create and query SQL statements, with 50 clients querying and 200 selects for each
(enter the command on a single line):

mysqlslap --delimiter=";"
  --create="CREATE TABLE a (b int);INSERT INTO a VALUES (23)"
  --query="SELECT * FROM a" --concurrency=50 --iterations=200

492

mysqlslap — A Load Emulation Client

Let mysqlslap build the query SQL statement with a table of two INT columns and three VARCHAR
columns. Use five clients querying 20 times each. Do not create the table or insert the data (that is, use
the previous test's schema and data):

mysqlslap --concurrency=5 --iterations=20
  --number-int-cols=2 --number-char-cols=3
  --auto-generate-sql

Tell the program to load the create, insert, and query SQL statements from the specified files, where
the create.sql file has multiple table creation statements delimited by ';' and multiple insert
statements delimited by ';'. The --query file should contain multiple queries delimited by ';'. Run
all the load statements, then run all the queries in the query file with five clients (five times each):

mysqlslap --concurrency=5
  --iterations=5 --query=query.sql --create=create.sql
  --delimiter=";"

mysqlslap supports the following options, which can be specified on the command line or in the
[mysqlslap] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.16 mysqlslap Options

Option Name

--auto-generate-sql

--auto-generate-sql-add-autoincrement

--auto-generate-sql-execute-number

--auto-generate-sql-guid-primary

Description

Generate SQL statements automatically when
they are not supplied in files or using command
options

Add AUTO_INCREMENT column to automatically
generated tables

Specify how many queries to generate
automatically

Add a GUID-based primary key to automatically
generated tables

--auto-generate-sql-load-type

Specify the test load type

--auto-generate-sql-secondary-indexes

--auto-generate-sql-unique-query-number

--auto-generate-sql-unique-write-number

Specify how many secondary indexes to add to
automatically generated tables

How many different queries to generate for
automatic tests

How many different queries to generate for --auto-
generate-sql-write-number

--auto-generate-sql-write-number

How many row inserts to perform on each thread

--commit

--compress

--compression-algorithms

--concurrency

--create

How many statements to execute before
committing

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Number of clients to simulate when issuing the
SELECT statement

File or string containing the statement to use for
creating the table

--create-schema

Schema in which to run the tests

--csv

--debug

Generate output in comma-separated values
format

Write debugging log

493

mysqlslap — A Load Emulation Client

Option Name

--debug-check

--debug-info

--default-auth

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--delimiter

--detach

Description

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Delimiter to use in SQL statements

Detach (close and reopen) each connection after
each N statements

--enable-cleartext-plugin

Enable cleartext authentication plugin

--engine

--get-server-public-key

--help

--host

--iterations

--login-path

--no-defaults

--no-drop

--no-login-paths

--number-char-cols

--number-int-cols

--number-of-queries

--only-print

--password

--password1

--password2

--password3

--pipe

--plugin-dir

--port

--post-query

--post-system

494

Storage engine to use for creating the table

Request RSA public key from server

Display help message and exit

Host on which MySQL server is located

Number of times to run the tests

Read login path options from .mylogin.cnf

Read no option files

Do not drop any schema created during the test
run

Do not read login paths from the login path file

Number of VARCHAR columns to use if --auto-
generate-sql is specified

Number of INT columns to use if --auto-generate-
sql is specified

Limit each client to approximately this number of
queries

Do not connect to databases. mysqlslap only
prints what it would have done

Password to use when connecting to server

First multifactor authentication password to use
when connecting to server

Second multifactor authentication password to use
when connecting to server

Third multifactor authentication password to use
when connecting to server

Connect to server using named pipe (Windows
only)

Directory where plugins are installed

TCP/IP port number for connection

File or string containing the statement to execute
after the tests have completed

String to execute using system() after the tests
have completed

mysqlslap — A Load Emulation Client

Option Name

--pre-query

--pre-system

--print-defaults

--protocol

--query

--server-public-key-path

--shared-memory-base-name

--silent

--socket

--sql-mode

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tls-ciphersuites

--tls-sni-servername

--tls-version

--user

--verbose

--version

--zstd-compression-level

Description

File or string containing the statement to execute
before running the tests

String to execute using system() before running
the tests

Print default options

Transport protocol to use

File or string containing the SELECT statement to
use for retrieving data

Path name to file containing RSA public key

Shared-memory name for shared-memory
connections (Windows only)

Silent mode

Unix socket file or Windows named pipe to use

Set SQL mode for client session

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Compression level for connections to server that
use zstd compression

495

mysqlslap — A Load Emulation Client

• --help, -?

Command-Line Format

--help

Display a help message and exit.

• --auto-generate-sql, -a

Command-Line Format

--auto-generate-sql

Type

Default Value

Boolean

FALSE

Generate SQL statements automatically when they are not supplied in files or using command
options.

• --auto-generate-sql-add-autoincrement

Command-Line Format

Type

Default Value

--auto-generate-sql-add-
autoincrement

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

496

Type

Default Value

Valid Values

Enumeration

mixed

read

write

key

update

mysqlslap — A Load Emulation Client

mixed

Specify the test load type. The permissible values are read (scan tables), write (insert into tables),
key (read primary keys), update (update primary keys), or mixed (half inserts, half scanning
selects). The default is mixed.

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
performs 1000 selects, you can use this option with a value of 1000 to run 1000 unique queries, or
with a value of 50 to perform 50 different selects. The default is 10.

• --auto-generate-sql-unique-write-number=N

Command-Line Format

Type

Default Value

--auto-generate-sql-unique-write-
number=#

Numeric

10

How many different queries to generate for --auto-generate-sql-write-number. The default
is 10.

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

497

mysqlslap — A Load Emulation Client

How many statements to execute before committing. The default is 0 (no commits are done).

• --compress, -C

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

For more information, see Section 6.2.8, “Connection Compression Control”.

• --concurrency=N, -c N

Command-Line Format

Type

--concurrency=#

Numeric

The number of parallel clients to simulate.

• --create=value

Command-Line Format

Type

--create=value

String

The file or string containing the statement to use for creating the table.

498

• --create-schema=value

Command-Line Format

--create-schema=value

mysqlslap — A Load Emulation Client

Type

String

The schema in which to run the tests.

Note

If the --auto-generate-sql option is also given, mysqlslap drops the
schema at the end of the test run. To avoid this, use the --no-drop option
as well.

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

Default Value

String

d:t:o,/tmp/mysqlslap.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/mysqlslap.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info, -T

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --default-auth=plugin

499

mysqlslap — A Load Emulation Client

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlslap normally reads the [client] and [mysqlslap] groups. If this option
is given as --defaults-group-suffix=_other, mysqlslap also reads the [client_other]
and [mysqlslap_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --delimiter=str, -F str

Command-Line Format

Type

500

--delimiter=str

String

The delimiter to use in SQL statements supplied in files or using command options.

mysqlslap — A Load Emulation Client

• --detach=N

Command-Line Format

Type

Default Value

--detach=#

Numeric

0

Detach (close and reopen) each connection after each N statements. The default is 0 (connections
are not detached).

• --enable-cleartext-plugin

Command-Line Format

--enable-cleartext-plugin

Type

Default Value

Boolean

FALSE

Enable the mysql_clear_password cleartext authentication plugin. (See Section 8.4.1.4, “Client-
Side Cleartext Pluggable Authentication”.)

• --engine=engine_name, -e engine_name

Command-Line Format

--engine=engine_name

Type

String

The storage engine to use for creating tables.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the RSA public key that it uses for key pair-based password exchange.
This option applies to clients that connect to the server using an account that authenticates with the
caching_sha2_password authentication plugin. For connections by such accounts, the server
does not send the public key to the client unless requested. The option is ignored for accounts
that do not authenticate with that plugin. It is also ignored if RSA-based password exchange is not
needed, as is the case when the client connects to the server using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

Connect to the MySQL server on the given host.

• --iterations=N, -i N

501

mysqlslap — A Load Emulation Client

Command-Line Format

Type

--iterations=#

Numeric

The number of times to run the tests.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

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

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --number-char-cols=N, -x N

502

mysqlslap — A Load Emulation Client

Command-Line Format

--number-char-cols=#

Type

Numeric

The number of VARCHAR columns to use if --auto-generate-sql is specified.

• --number-int-cols=N, -y N

Command-Line Format

--number-int-cols=#

Type

Numeric

The number of INT columns to use if --auto-generate-sql is specified.

• --number-of-queries=N

Command-Line Format

--number-of-queries=#

Type

Numeric

Limit each client to approximately this many queries. Query counting takes into account the
statement delimiter. For example, if you invoke mysqlslap as follows, the ; delimiter is recognized
so that each instance of the query string counts as two queries. As a result, 5 rows (not 10) are
inserted.

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

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqlslap prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlslap should not prompt for one, use
the --skip-password option.

503

mysqlslap — A Load Emulation Client

• --password1[=pass_val]

The password for multifactor authentication factor 1 of the MySQL account used for connecting to
the server. The password value is optional. If not given, mysqlslap prompts for one. If given, there
must be no space between --password1= and the password following it. If no password option is
specified, the default is to send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlslap should not prompt for one, use
the --skip-password1 option.

--password1 and --password are synonymous, as are --skip-password1 and --skip-
password.

• --password2[=pass_val]

The password for multifactor authentication factor 2 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

• --password3[=pass_val]

The password for multifactor authentication factor 3 of the MySQL account used for connecting to
the server. The semantics of this option are similar to the semantics for --password1; see the
description of that option for details.

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
to specify an authentication plugin but mysqlslap does not find it. See Section 8.2.17, “Pluggable
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

504

mysqlslap — A Load Emulation Client

Command-Line Format

--post-query=value

Type

String

The file or string containing the statement to execute after the tests have completed. This execution
is not counted for timing purposes.

• --post-system=str

Command-Line Format

--post-system=str

Type

String

The string to execute using system() after the tests have completed. This execution is not counted
for timing purposes.

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

The string to execute using system() before running the tests. This execution is not counted for
timing purposes.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

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

505

mysqlslap — A Load Emulation Client

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

• --query=value, -q value

Command-Line Format

Type

--query=value

String

The file or string containing the SELECT statement to use for retrieving data.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --silent, -s

Command-Line Format

--silent

Silent mode. No output.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

506

mysqlslap — A Load Emulation Client

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --sql-mode=mode

Command-Line Format

Type

--sql-mode=mode

String

Set the SQL mode for the client session.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

507

mysqlslap — A Load Emulation Client

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use for connecting to the server.

• --verbose, -v

Command-Line Format

--verbose

508

Verbose mode. Print more information about what the program does. This option can be used
multiple times to increase the amount of information.

Administrative and Utility Programs

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

6.6 Administrative and Utility Programs

This section describes administrative programs and programs that perform miscellaneous utility
operations.

6.6.1 ibd2sdi — InnoDB Tablespace SDI Extraction Utility

ibd2sdi is a utility for extracting serialized dictionary information (SDI) from InnoDB tablespace files.
SDI data is present in all persistent InnoDB tablespace files.

ibd2sdi can be run on file-per-table tablespace files (*.ibd files), general tablespace files (*.ibd
files), system tablespace files (ibdata* files), and the data dictionary tablespace (mysql.ibd). It is
not supported for use with temporary tablespaces or undo tablespaces.

ibd2sdi can be used at runtime or while the server is offline. During DDL operations, ROLLBACK
operations, and undo log purge operations related to SDI, there may be a short interval of time when
ibd2sdi fails to read SDI data stored in the tablespace.

ibd2sdi performs an uncommitted read of SDI from the specified tablespace. Redo logs and undo
logs are not accessed.

Invoke the ibd2sdi utility like this:

ibd2sdi [options] file_name1 [file_name2 file_name3 ...]

ibd2sdi supports multi-file tablespaces like the InnoDB system tablespace, but it cannot be run on
more than one tablespace at a time. For multi-file tablespaces, specify each file:

ibd2sdi ibdata1 ibdata2

The files of a multi-file tablespace must be specified in order of the ascending page number. If two
successive files have the same space ID, the later file must start with the last page number of the
previous file + 1.

ibd2sdi outputs SDI (containing id, type, and data fields) in JSON format.

ibd2sdi Options

ibd2sdi supports the following options:

• --help, -h

509

ibd2sdi — InnoDB Tablespace SDI Extraction Utility

Command-Line Format

Type

Default Value

--help

Boolean

false

Display a help message and exit. For example:

Usage: ./ibd2sdi [-v] [-c <strict-check>] [-d <dump file name>] [-n] filename1 [filenames]
See http://dev.mysql.com/doc/refman/8.4/en/ibd2sdi.html for usage hints.
  -h, --help          Display this help and exit.
  -v, --version       Display version information and exit.
  -#, --debug[=name]  Output debug log. See
                      http://dev.mysql.com/doc/refman/8.4/en/dbug-package.html
  -d, --dump-file=name
                      Dump the tablespace SDI into the file passed by user.
                      Without the filename, it will default to stdout
  -s, --skip-data     Skip retrieving data from SDI records. Retrieve only id
                      and type.
  -i, --id=#          Retrieve the SDI record matching the id passed by user.
  -t, --type=#        Retrieve the SDI records matching the type passed by
                      user.
  -c, --strict-check=name
                      Specify the strict checksum algorithm by the user.
                      Allowed values are innodb, crc32, none.
  -n, --no-check      Ignore the checksum verification.
  -p, --pretty        Pretty format the SDI output.If false, SDI would be not
                      human readable but it will be of less size
                      (Defaults to on; use --skip-pretty to disable.)

Variables (--variable-name=value)
and boolean options {FALSE|TRUE}  Value (after reading options)
--------------------------------- ----------------------------------------
debug                             (No default value)
dump-file                         (No default value)
skip-data                         FALSE
id                                0
type                              0
strict-check                      crc32
no-check                          FALSE
pretty                            TRUE

• --version, -v

Command-Line Format

Type

Default Value

--version

Boolean

false

Display version information and exit. For example:

ibd2sdi  Ver 8.4.5 for Linux on x86_64 (Source distribution)

• --debug[=debug_options], -# [debug_options]

Command-Line Format

Type

--debug=options

String

510

ibd2sdi — InnoDB Tablespace SDI Extraction Utility

Default Value

[none]

Prints a debug log. For debug options, refer to Section 7.9.4, “The DBUG Package”.

ibd2sdi --debug=d:t /tmp/ibd2sdi.trace

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --dump-file=, -d

Command-Line Format

--dump-file=file

Type

Default Value

File name

[none]

Dumps serialized dictionary information (SDI) into the specified dump file. If a dump file is not
specified, the tablespace SDI is dumped to stdout.

ibd2sdi --dump-file=file_name ../data/test/t1.ibd

• --skip-data, -s

Command-Line Format

Type

Default Value

--skip-data

Boolean

false

Skips retrieval of data field values from the serialized dictionary information (SDI) and only retrieves
the id and type field values, which are primary keys for SDI records.

$> ibd2sdi --skip-data ../data/test/t1.ibd
["ibd2sdi"
,
{
 "type": 1,
 "id": 330
}
,
{
 "type": 2,
 "id": 7
}
]

• --id=#, -i #

Command-Line Format

Type

Default Value

--id=#

Integer

0

Retrieves serialized dictionary information (SDI) matching the specified table or tablespace object
id. An object id is unique to the object type. Table and tablespace object IDs are also found in the
id column of the mysql.tables and mysql.tablespace data dictionary tables. For information
about data dictionary tables, see Section 16.1, “Data Dictionary Schema”.

511

$> ibd2sdi --id=7 ../data/test/t1.ibd
["ibd2sdi"
,

ibd2sdi — InnoDB Tablespace SDI Extraction Utility

{
 "type": 2,
 "id": 7,
 "object":
  {
    "mysqld_version_id": 80003,
    "dd_version": 80003,
    "sdi_version": 1,
    "dd_object_type": "Tablespace",
    "dd_object": {
        "name": "test/t1",
        "comment": "",
        "options": "",
        "se_private_data": "flags=16417;id=2;server_version=80003;space_version=1;",
        "engine": "InnoDB",
        "files": [
            {
                "ordinal_position": 1,
                "filename": "./test/t1.ibd",
                "se_private_data": "id=2;"
            }
        ]
    }
}
}
]

• --type=#, -t #

Command-Line Format

Type

Default Value

Valid Values

--type=#

Enumeration

0

1

2

Retrieves serialized dictionary information (SDI) matching the specified object type. SDI is provided
for table (type=1) and tablespace (type=2) objects.

This example shows output for a tablespace ts1 in the test database:

$> ibd2sdi --type=2 ../data/test/ts1.ibd
["ibd2sdi"
,
{
 "type": 2,
 "id": 7,
 "object":
  {
    "mysqld_version_id": 80003,
    "dd_version": 80003,
    "sdi_version": 1,
    "dd_object_type": "Tablespace",
    "dd_object": {
        "name": "test/ts1",
        "comment": "",
        "options": "",
        "se_private_data": "flags=16417;id=2;server_version=80003;space_version=1;",
        "engine": "InnoDB",
        "files": [
            {
                "ordinal_position": 1,
                "filename": "./test/ts1.ibd",
                "se_private_data": "id=2;"
            }
        ]
    }

512

ibd2sdi — InnoDB Tablespace SDI Extraction Utility

}
}
]

Due to the way in which InnoDB handles default value metadata, a default value may be present
and non-empty in ibd2sdi output for a given table column even if it is not defined using DEFAULT.
Consider the two tables created using the following statements, in the database named i:

CREATE TABLE t1 (c VARCHAR(16) NOT NULL);

CREATE TABLE t2 (c VARCHAR(16) NOT NULL DEFAULT "Sakila");

Using ibd2sdi, we can see that the default_value for column c is nonempty and is in fact
padded to length in both tables, like this:

$> ibd2sdi ../data/i/t1.ibd  | grep -m1 '\"default_value\"' | cut -b34- | sed -e s/,//
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAA="

$> ibd2sdi ../data/i/t2.ibd  | grep -m1 '\"default_value\"' | cut -b34- | sed -e s/,//
"BlNha2lsYQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAA="

Examination of ibd2sdi output may be easier using a JSON-aware utility like jq, as shown here:

$> ibd2sdi ../data/i/t1.ibd  | jq '.[1]["object"]["dd_object"]["columns"][0]["default_value"]'
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAA="

$> ibd2sdi ../data/i/t2.ibd  | jq '.[1]["object"]["dd_object"]["columns"][0]["default_value"]'
"BlNha2lsYQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAA="

For more information, see the MySQL Internals documentation.

• --strict-check, -c

Command-Line Format

--strict-check=algorithm

Type

Default Value

Valid Values

Enumeration

crc32

crc32

innodb

none

Specifies a strict checksum algorithm for validating the checksum of pages that are read. Options
include innodb, crc32, and none.

In this example, the strict version of the innodb checksum algorithm is specified:

ibd2sdi --strict-check=innodb ../data/test/t1.ibd

In this example, the strict version of crc32 checksum algorithm is specified:

ibd2sdi -c crc32 ../data/test/t1.ibd

If you do not specify the --strict-check option, validation is performed against non-strict
innodb, crc32 and none checksums.

• --no-check, -n

Command-Line Format

Type

--no-check

Boolean

513

innochecksum — Offline InnoDB File Checksum Utility

Default Value

false

Skips checksum validation for pages that are read.

ibd2sdi --no-check ../data/test/t1.ibd

• --pretty, -p

Command-Line Format

Type

Default Value

--pretty

Boolean

false

Outputs SDI data in JSON pretty print format. Enabled by default. If disabled, SDI is not human
readable but is smaller in size. Use --skip-pretty to disable.

ibd2sdi --skip-pretty ../data/test/t1.ibd

6.6.2 innochecksum — Offline InnoDB File Checksum Utility

innochecksum prints checksums for InnoDB files. This tool reads an InnoDB tablespace file,
calculates the checksum for each page, compares the calculated checksum to the stored checksum,
and reports mismatches, which indicate damaged pages. It was originally developed to speed up
verifying the integrity of tablespace files after power outages but can also be used after file copies.
Because checksum mismatches cause InnoDB to deliberately shut down a running server, it may be
preferable to use this tool rather than waiting for an in-production server to encounter the damaged
pages.

innochecksum cannot be used on tablespace files that the server already has open. For such
files, you should use CHECK TABLE to check tables within the tablespace. Attempting to run
innochecksum on a tablespace that the server already has open results in an Unable to lock
file error.

If checksum mismatches are found, restore the tablespace from backup or start the server and attempt
to use mysqldump to make a backup of the tables within the tablespace.

Invoke innochecksum like this:

innochecksum [options] file_name

innochecksum Options

innochecksum supports the following options. For options that refer to page numbers, the numbers
are zero-based.

• --help, -?

Command-Line Format

Type

Default Value

--help

Boolean

false

Displays command line help. Example usage:

innochecksum --help

• --info, -I

Command-Line Format

--info

514

innochecksum — Offline InnoDB File Checksum Utility

Type

Default Value

Boolean

false

Synonym for --help. Displays command line help. Example usage:

innochecksum --info

• --version, -V

Command-Line Format

Type

Default Value

Displays version information. Example usage:

innochecksum --version

• --verbose, -v

Command-Line Format

Type

Default Value

--version

Boolean

false

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

--count

515

innochecksum — Offline InnoDB File Checksum Utility

Type

Default Value

Base name

true

Print a count of the number of pages in the file and exit. Example usage:

innochecksum --count ../data/test/tab1.ibd

• --start-page=num, -s num

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

516

Command-Line Format

--strict-check=algorithm

Type

Default Value

Valid Values

Enumeration

crc32

innodb

innochecksum — Offline InnoDB File Checksum Utility

crc32

none

Specify a strict checksum algorithm. Options include innodb, crc32, and none.

In this example, the innodb checksum algorithm is specified:

innochecksum --strict-check=innodb ../data/test/tab1.ibd

In this example, the crc32 checksum algorithm is specified:

innochecksum -C crc32 ../data/test/tab1.ibd

The following conditions apply:

• If you do not specify the --strict-check option, innochecksum validates against innodb,

crc32 and none.

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

Ignore the checksum verification when rewriting a checksum. This option may only be used with
the innochecksum --write option. If the --write option is not specified, innochecksum
terminates.

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

517

innochecksum — Offline InnoDB File Checksum Utility

innochecksum terminates at N+1. When --allow-mismatches is set to 0, innochecksum
terminates on the first checksum mismatch.

In this example, an existing innodb checksum is rewritten to set --allow-mismatches to 1.

innochecksum --allow-mismatches=1 --write innodb ../data/test/tab1.ibd

With --allow-mismatches set to 1, if there is a mismatch at page 600 and another at page 700
on a file with 1000 pages, the checksum is updated for pages 0-599 and 601-699. Because --
allow-mismatches is set to 1, the checksum tolerates the first mismatch and terminates on the
second mismatch, leaving page 600 and pages 700-999 unchanged.

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

Rewrite a checksum. When rewriting an invalid checksum, the --no-check option must be
used together with the --write option. The --no-check option tells innochecksum to ignore
verification of the invalid checksum. You do not have to specify the --no-check option if the current
checksum is valid.

An algorithm must be specified when using the --write option. Possible values for the --write
option are:

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

Type

Boolean

518

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

Dump the page type information for each page in a tablespace to stderr or stdout. Example
usage:

innochecksum --page-type-dump=/tmp/a.txt ../data/test/tab1.ibd

• --log, -l

Command-Line Format

Type

Default Value

--log=path

File name

[none]

Log output for the innochecksum tool. A log file name must be provided. Log output contains
checksum values for each tablespace page. For uncompressed tables, LSN values are also
provided. Example usage:

innochecksum --log=/tmp/log.txt ../data/test/tab1.ibd

or:

innochecksum -l /tmp/log.txt ../data/test/tab1.ibd

519

innochecksum — Offline InnoDB File Checksum Utility

• - option.

Specify the - option to read from standard input. If the - option is missing when “read from standard
in” is expected, innochecksum prints innochecksum usage information indicating that the “-”
option was omitted. Example usages:

cat t1.ibd | innochecksum -

In this example, innochecksum writes the crc32 checksum algorithm to a.ibd without changing
the original t1.ibd file.

cat t1.ibd | innochecksum --write=crc32 - > a.ibd

Running innochecksum on Multiple User-defined Tablespace Files

The following examples demonstrate how to run innochecksum on multiple user-defined tablespace
files (.ibd files).

Run innochecksum for all tablespace (.ibd) files in the “test” database:

innochecksum ./data/test/*.ibd

Run innochecksum for all tablespace files (.ibd files) that have a file name starting with “t”:

innochecksum ./data/test/t*.ibd

Run innochecksum for all tablespace files (.ibd files) in the data directory:

innochecksum ./data/*/*.ibd

Note

Running innochecksum on multiple user-defined tablespace files is not
supported on Windows operating systems, as Windows shells such as
cmd.exe do not support glob pattern expansion. On Windows systems,
innochecksum must be run separately for each user-defined tablespace file.
For example:

innochecksum.exe t1.ibd
innochecksum.exe t2.ibd
innochecksum.exe t3.ibd

Running innochecksum on Multiple System Tablespace Files

By default, there is only one InnoDB system tablespace file (ibdata1) but multiple files for the system
tablespace can be defined using the innodb_data_file_path option. In the following example,
three files for the system tablespace are defined using the innodb_data_file_path option:
ibdata1, ibdata2, and ibdata3.

./bin/mysqld --no-defaults --innodb-data-file-path="ibdata1:10M;ibdata2:10M;ibdata3:10M:autoextend"

The three files (ibdata1, ibdata2, and ibdata3) form one logical system tablespace. To run
innochecksum on multiple files that form one logical system tablespace, innochecksum requires the
- option to read tablespace files in from standard input, which is equivalent to concatenating multiple
files to create one single file. For the example provided above, the following innochecksum command
would be used:

cat ibdata* | innochecksum -

Refer to the innochecksum options information for more information about the “-” option.

Note

Running innochecksum on multiple files in the same tablespace is not
supported on Windows operating systems, as Windows shells such as

520

myisam_ftdump — Display Full-Text Index information

cmd.exe do not support glob pattern expansion. On Windows systems,
innochecksum must be run separately for each system tablespace file. For
example:

innochecksum.exe ibdata1
innochecksum.exe ibdata2
innochecksum.exe ibdata3

6.6.3 myisam_ftdump — Display Full-Text Index information

myisam_ftdump displays information about FULLTEXT indexes in MyISAM tables. It reads the
MyISAM index file directly, so it must be run on the server host where the table is located. Before using
myisam_ftdump, be sure to issue a FLUSH TABLES statement first if the server is running.

myisam_ftdump scans and dumps the entire index, which is not particularly fast. On the other hand,
the distribution of words changes infrequently, so it need not be run often.

Invoke myisam_ftdump like this:

myisam_ftdump [options] tbl_name index_num

The tbl_name argument should be the name of a MyISAM table. You can also specify a table by
naming its index file (the file with the .MYI suffix). If you do not invoke myisam_ftdump in the
directory where the table files are located, the table or index file name must be preceded by the path
name to the table's database directory. Index numbers begin with 0.

Example: Suppose that the test database contains a table named mytexttable that has the
following definition:

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

You can use myisam_ftdump to generate a list of index entries in order of frequency of occurrence
like this on Unix-like systems:

myisam_ftdump -c mytexttable 1 | sort -r

On Windows, use:

myisam_ftdump -c mytexttable 1 | sort /R

myisam_ftdump supports the following options:

• --help, -h -?

Command-Line Format

--help

Display a help message and exit.

• --count, -c

521

myisamchk — MyISAM Table-Maintenance Utility

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

6.6.4 myisamchk — MyISAM Table-Maintenance Utility

The myisamchk utility gets information about your database tables or checks, repairs, or optimizes
them. myisamchk works with MyISAM tables (tables that have .MYD and .MYI files for storing data
and indexes).

You can also use the CHECK TABLE and REPAIR TABLE statements to check and repair MyISAM
tables. See Section 15.7.3.2, “CHECK TABLE Statement”, and Section 15.7.3.5, “REPAIR TABLE
Statement”.

The use of myisamchk with partitioned tables is not supported.

Caution

It is best to make a backup of a table before performing a table repair operation;
under some circumstances the operation might cause data loss. Possible
causes include but are not limited to file system errors.

Invoke myisamchk like this:

myisamchk [options] tbl_name ...

The options specify what you want myisamchk to do. They are described in the following sections.
You can also get a list of options by invoking myisamchk --help.

With no options, myisamchk simply checks your table as the default operation. To get more
information or to tell myisamchk to take corrective action, specify options as described in the following
discussion.

522

myisamchk — MyISAM Table-Maintenance Utility

tbl_name is the database table you want to check or repair. If you run myisamchk somewhere
other than in the database directory, you must specify the path to the database directory, because
myisamchk has no idea where the database is located. In fact, myisamchk does not actually care
whether the files you are working on are located in a database directory. You can copy the files that
correspond to a database table into some other location and perform recovery operations on them
there.

You can name several tables on the myisamchk command line if you wish. You can also specify a
table by naming its index file (the file with the .MYI suffix). This enables you to specify all tables in a
directory by using the pattern *.MYI. For example, if you are in a database directory, you can check all
the MyISAM tables in that directory like this:

myisamchk *.MYI

If you are not in the database directory, you can check all the tables there by specifying the path to the
directory:

myisamchk /path/to/database_dir/*.MYI

You can even check all tables in all databases by specifying a wildcard with the path to the MySQL
data directory:

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
allocation with myisamchk, see Section 6.6.4.6, “myisamchk Memory Usage”.

For additional information about using myisamchk, see Section 9.6, “MyISAM Table Maintenance and
Crash Recovery”.

Important

You must ensure that no other program is using the tables while you are
running myisamchk. The most effective means of doing so is to shut down the
MySQL server while running myisamchk, or to lock all tables that myisamchk
is being used on.

Otherwise, when you run myisamchk, it may display the following error
message:

warning: clients are using or haven't closed the table properly

This means that you are trying to check a table that has been updated by
another program (such as the mysqld server) that hasn't yet closed the file or
that has died without closing the file properly, which can sometimes lead to the
corruption of one or more MyISAM tables.

If mysqld is running, you must force it to flush any table modifications that are
still buffered in memory by using FLUSH TABLES. You should then ensure that
no one is using the tables while you are running myisamchk

523

myisamchk — MyISAM Table-Maintenance Utility

However, the easiest way to avoid this problem is to use CHECK TABLE
instead of myisamchk to check tables. See Section 15.7.3.2, “CHECK TABLE
Statement”.

myisamchk supports the following options, which can be specified on the command line or in the
[myisamchk] group of an option file. For information about option files used by MySQL programs, see
Section 6.2.2.2, “Using Option Files”.

Table 6.17 myisamchk Options

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

524

Description

Analyze the distribution of key values

Make a backup of the .MYD file as file_name-
time.BAK

Find the record that a block at the given offset
belongs to

Directory where character sets can be found

Check the table for errors

Check only tables that have changed since the
last check

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

Do very thorough table check or repair that tries to
recover every possible row from the data file

Check only tables that haven't been closed
properly

Do a repair operation automatically if myisamchk
finds any errors in the table

Overwrite old temporary files. For use with the -r
or -o option

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

myisamchk — MyISAM Table-Maintenance Utility

Option Name

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

Description

Skip rows larger than the given length if
myisamchk cannot allocate memory to hold them

Do a check that is faster than an --extend-check
operation

Block size to be used for MyISAM index pages

The buffer that is allocated when sorting the index
when doing a REPAIR or when creating indexes
with CREATE INDEX or ALTER TABLE

Read no option files

Uses the same technique as -r and -n, but creates
all the keys in parallel, using different threads
(beta)

Print default options

Achieve a faster repair by not modifying the data
file

Each thread that does a sequential scan allocates
a buffer of this size for each table it scans

Do not mark the table as checked

Do a repair that can fix almost any problem except
unique keys that aren't unique

Do a repair using an old recovery method that
reads through all rows in order and updates all
index trees based on the rows found

Force AUTO_INCREMENT numbering for new
records to start at the given value

Specify the collation to use for sorting table
indexes

Silent mode

The buffer that is allocated when sorting the index
when doing a REPAIR or when creating indexes
with CREATE INDEX or ALTER TABLE

Sort the index tree blocks in high-low order

sort_key_blocks

Sort records according to a particular index

Force myisamchk to use sorting to resolve the
keys even if the temporary files would be very
large

Specifies how MyISAM index statistics collection
code should treat NULLs

Directory to be used for storing temporary files

Unpack a table that was packed with myisampack

Store information in the .MYI file to indicate when
the table was checked and whether the table
crashed

Verbose mode

Display version information and exit

525

myisamchk — MyISAM Table-Maintenance Utility

Option Name

--wait

Description

Wait for locked table to be unlocked, instead of
terminating

--write_buffer_size

Write buffer size

6.6.4.1 myisamchk General Options

The options described in this section can be used for any type of table maintenance operation
performed by myisamchk. The sections following this one describe options that pertain only to specific
operations, such as table checking or repairing.

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

Default Value

String

d:t:o,/tmp/myisamchk.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/myisamchk.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

526

Command-Line Format

--defaults-file=file_name

Type

File name

myisamchk — MyISAM Table-Maintenance Utility

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, myisamchk normally reads the [myisamchk] group. If this option is given as --
defaults-group-suffix=_other, myisamchk also reads the [myisamchk_other] group.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --silent, -s

Command-Line Format

--silent

Silent mode. Write output only when errors occur. You can use -s twice (-ss) to make myisamchk
very silent.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This can be used with -d and -
e. Use -v multiple times (-vv, -vvv) for even more output.

527

myisamchk — MyISAM Table-Maintenance Utility

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

9

version-dependent

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

The possible myisamchk variables and their default values can be examined with myisamchk --
help:

myisam_sort_buffer_size is used when the keys are repaired by sorting keys, which is
the normal case when you use --recover. sort_buffer_size is a deprecated synonym for
myisam_sort_buffer_size.

key_buffer_size is used when you are checking the table with --extend-check or when the keys
are repaired by inserting keys row by row into the table (like when doing normal inserts). Repairing
through the key buffer is used in the following cases:

• You use --safe-recover.

• The temporary files needed to sort the keys would be more than twice as big as when creating the

key file directly. This is often the case when you have large key values for CHAR, VARCHAR, or TEXT
columns, because the sort operation needs to store the complete key values as it proceeds. If you
have lots of temporary space and you can force myisamchk to repair by sorting, you can use the --
sort-recover option.

Repairing through the key buffer takes much less disk space than using sorting, but is also much
slower.

528

myisamchk — MyISAM Table-Maintenance Utility

If you want a faster repair, set the key_buffer_size and myisam_sort_buffer_size variables to
about 25% of your available memory. You can set both variables to large values, because only one of
them is used at a time.

myisam_block_size is the size used for index blocks.

stats_method influences how NULL values are treated for index statistics collection when the
--analyze option is given. It acts like the myisam_stats_method system variable. For more
information, see the description of myisam_stats_method in Section 7.1.8, “Server System
Variables”, and Section 10.3.8, “InnoDB and MyISAM Index Statistics Collection”.

ft_min_word_len and ft_max_word_len indicate the minimum and maximum word length for
FULLTEXT indexes on MyISAM tables. ft_stopword_file names the stopword file. These need to
be set under the following circumstances.

If you use myisamchk to perform an operation that modifies table indexes (such as repair or analyze),
the FULLTEXT indexes are rebuilt using the default full-text parameter values for minimum and
maximum word length and the stopword file unless you specify otherwise. This can result in queries
failing.

The problem occurs because these parameters are known only by the server. They are not stored in
MyISAM index files. To avoid the problem if you have modified the minimum or maximum word length
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

An alternative to using myisamchk is to use the REPAIR TABLE, ANALYZE TABLE, OPTIMIZE
TABLE, or ALTER TABLE. These statements are performed by the server, which knows the proper full-
text parameter values to use.

6.6.4.2 myisamchk Check Options

myisamchk supports the following options for table checking operations:

• --check, -c

Command-Line Format

--check

Check the table for errors. This is the default operation if you specify no option that selects an
operation type explicitly.

• --check-only-changed, -C

Command-Line Format

--check-only-changed

Check only tables that have changed since the last check.

• --extend-check, -e

Command-Line Format

--extend-check

529

myisamchk — MyISAM Table-Maintenance Utility

Check the table very thoroughly. This is quite slow if the table has many indexes. This option should
only be used in extreme cases. Normally, myisamchk or myisamchk --medium-check should be
able to determine whether there are any errors in the table.

If you are using --extend-check and have plenty of memory, setting the key_buffer_size
variable to a large value helps the repair operation run faster.

See also the description of this option under table repair options.

For a description of the output format, see Section 6.6.4.5, “Obtaining Table Information with
myisamchk”.

• --fast, -F

Command-Line Format

--fast

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

530

• --update-state, -U

Command-Line Format

--update-state

Store information in the .MYI file to indicate when the table was checked and whether the table

crashed. This should be used to get full benefit of the --check-only-changed option, but you

myisamchk — MyISAM Table-Maintenance Utility

shouldn't use this option if the mysqld server is using the table and you are running it with external
locking disabled.

6.6.4.3 myisamchk Repair Options

myisamchk supports the following options for table repair operations (operations performed when an
option such as --recover or --safe-recover is given):

• --backup, -B

Command-Line Format

--backup

Make a backup of the .MYD file as file_name-time.BAK

• --character-sets-dir=dir_name

Command-Line Format

--character-sets-dir=path

Type

Default Value

String

[none]

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

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

For a description of the output format, see Section 6.6.4.5, “Obtaining Table Information with
myisamchk”.

• --force, -f

Command-Line Format

--force

Overwrite old intermediate files (files with names like tbl_name.TMD) instead of aborting.

• --keys-used=val, -k val

531

myisamchk — MyISAM Table-Maintenance Utility

Command-Line Format

Type

--keys-used=val

Numeric

For myisamchk, the option value is a bit value that indicates which indexes to update. Each binary
bit of the option value corresponds to a table index, where the first index is bit 0. An option value of 0
disables updates to all indexes, which can be used to get faster inserts. Deactivated indexes can be
reactivated by using myisamchk -r.

• --max-record-length=len

Command-Line Format

--max-record-length=len

Type

Numeric

Skip rows larger than the given length if myisamchk cannot allocate memory to hold them.

• --quick, -q

Command-Line Format

--quick

Achieve a faster repair by modifying only the index file, not the data file. You can specify this option
twice to force myisamchk to modify the original data file in case of duplicate keys.

• --recover, -r

Command-Line Format

--recover

Do a repair that can fix almost any problem except unique keys that are not unique (which is an
extremely unlikely error with MyISAM tables). If you want to recover a table, this is the option to try
first. You should try --safe-recover only if myisamchk reports that the table cannot be recovered
using --recover. (In the unlikely case that --recover fails, the data file remains intact.)

If you have lots of memory, you should increase the value of myisam_sort_buffer_size.

• --safe-recover, -o

Command-Line Format

--safe-recover

Do a repair using an old recovery method that reads through all rows in order and updates all index
trees based on the rows found. This is an order of magnitude slower than --recover, but can
handle a couple of very unlikely cases that --recover cannot. This recovery method also uses
much less disk space than --recover. Normally, you should repair first using --recover, and
then with --safe-recover only if --recover fails.

If you have lots of memory, you should increase the value of key_buffer_size.

• --set-collation=name

Command-Line Format

--set-collation=name

Type

String

Specify the collation to use for sorting table indexes. The character set name is implied by the first
part of the collation name.

532

myisamchk — MyISAM Table-Maintenance Utility

• --sort-recover, -n

Command-Line Format

--sort-recover

Force myisamchk to use sorting to resolve the keys even if the temporary files would be very large.

• --tmpdir=dir_name, -t dir_name

Command-Line Format

Type

--tmpdir=dir_name

Directory name

The path of the directory to be used for storing temporary files. If this is not set, myisamchk uses
the value of the TMPDIR environment variable. --tmpdir can be set to a list of directory paths that
are used successively in round-robin fashion for creating temporary files. The separator character
between directory names is the colon (:) on Unix and the semicolon (;) on Windows.

• --unpack, -u

Command-Line Format

--unpack

Unpack a table that was packed with myisampack.

6.6.4.4 Other myisamchk Options

myisamchk supports the following options for actions other than table checks and repairs:

• --analyze, -a

Command-Line Format

--analyze

Analyze the distribution of key values. This improves join performance by enabling the join
optimizer to better choose the order in which to join the tables and which indexes it should use. To
obtain information about the key distribution, use a myisamchk --description --verbose
tbl_name command or the SHOW INDEX FROM tbl_name statement.

• --block-search=offset, -b offset

Command-Line Format

--block-search=offset

Type

Numeric

Find the record that a block at the given offset belongs to.

• --description, -d

Command-Line Format

--description

Print some descriptive information about the table. Specifying the --verbose option once or twice
produces additional information. See Section 6.6.4.5, “Obtaining Table Information with myisamchk”.

• --set-auto-increment[=value], -A[value]

Force AUTO_INCREMENT numbering for new records to start at the given value (or higher, if

there are existing records with AUTO_INCREMENT values this large). If value is not specified,

533

myisamchk — MyISAM Table-Maintenance Utility

AUTO_INCREMENT numbers for new records begin with the largest value currently in the table, plus
one.

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

Sort records according to a particular index. This makes your data much more localized and may
speed up range-based SELECT and ORDER BY operations that use this index. (The first time you
use this option to sort a table, it may be very slow.) To determine a table's index numbers, use SHOW
INDEX, which displays a table's indexes in the same order that myisamchk sees them. Indexes are
numbered beginning with 1.

If keys are not packed (PACK_KEYS=0), they have the same length, so when myisamchk sorts and
moves records, it just overwrites record offsets in the index. If keys are packed (PACK_KEYS=1),
myisamchk must unpack key blocks first, then re-create indexes and pack the key blocks again. (In
this case, re-creating indexes is faster than updating offsets for each index.)

6.6.4.5 Obtaining Table Information with myisamchk

To obtain a description of a MyISAM table or statistics about it, use the commands shown here. The
output from these commands is explained later in this section.

• myisamchk -d tbl_name

Runs myisamchk in “describe mode” to produce a description of your table. If you start the MySQL
server with external locking disabled, myisamchk may report an error for a table that is updated
while it runs. However, because myisamchk does not change the table in describe mode, there is no
risk of destroying data.

• myisamchk -dv tbl_name

Adding -v runs myisamchk in verbose mode so that it produces more information about the table.
Adding -v a second time produces even more information.

• myisamchk -eis tbl_name

Shows only the most important information from a table. This operation is slow because it must read
the entire table.

• myisamchk -eiv tbl_name

This is like -eis, but tells you what is being done.

The tbl_name argument can be either the name of a MyISAM table or the name of its index file, as
described in Section 6.6.4, “myisamchk — MyISAM Table-Maintenance Utility”. Multiple tbl_name
arguments can be given.

Suppose that a table named person has the following structure. (The MAX_ROWS table option is
included so that in the example output from myisamchk shown later, some values are smaller and fit
the output format more easily.)

534

myisamchk — MyISAM Table-Maintenance Utility

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
Character set:       utf8mb4_0900_ai_ci (255)
File-version:        1
Creation time:       2017-03-30 21:21:30
Status:              checked,analyzed,optimized keys,sorted index pages
Auto increment key:              1  Last value:                306688
Data records:               306688  Deleted blocks:                 0
Datafile parts:             306688  Deleted data:                   0
Datafile pointer (bytes):        4  Keyfile pointer (bytes):        3
Datafile length:           9347072  Keyfile length:           6066176
Max datafile length:    4294967294  Max keyfile length:   17179868159
Recordlength:                   54

table description:
Key Start Len Index   Type                     Rec/key         Root  Blocksize
1   2     4   unique  long                           1                    1024
2   6     80  multip. varchar prefix                 0                    1024
    87    80          varchar                        0
3   168   3   multip. uint24 NULL                    0                    1024

Field Start Length Nullpos Nullbit Type
1     1     1
2     2     4                      no zeros
3     6     81                     varchar
4     87    81                     varchar
5     168   3      1       1       no zeros
6     171   3      1       2       no zeros

Explanations for the types of information myisamchk produces are given here. “Keyfile” refers to the
index file. “Record” and “row” are synonymous, as are “field” and “column.”

The initial part of the table description contains these values:

• MyISAM file

Name of the MyISAM (index) file.

• Record format

The format used to store table rows. The preceding examples use Fixed length. Other possible
values are Compressed and Packed. (Packed corresponds to what SHOW TABLE STATUS reports
as Dynamic.)

• Chararacter set

The table default character set.

• File-version

535

myisamchk — MyISAM Table-Maintenance Utility

Version of MyISAM format. Always 1.

• Creation time

When the data file was created.

• Recover time

When the index/data file was last reconstructed.

• Status

Table status flags. Possible values are crashed, open, changed, analyzed, optimized keys,
and sorted index pages.

• Auto increment key, Last value

The key number associated the table's AUTO_INCREMENT column, and the most recently generated
value for this column. These fields do not appear if there is no such column.

• Data records

The number of rows in the table.

• Deleted blocks

How many deleted blocks still have reserved space. You can optimize your table to minimize this
space. See Section 9.6.4, “MyISAM Table Optimization”.

• Datafile parts

For dynamic-row format, this indicates how many data blocks there are. For an optimized table
without fragmented rows, this is the same as Data records.

• Deleted data

How many bytes of unreclaimed deleted data there are. You can optimize your table to minimize this
space. See Section 9.6.4, “MyISAM Table Optimization”.

• Datafile pointer

The size of the data file pointer, in bytes. It is usually 2, 3, 4, or 5 bytes. Most tables manage with
2 bytes, but this cannot be controlled from MySQL yet. For fixed tables, this is a row address. For
dynamic tables, this is a byte address.

• Keyfile pointer

The size of the index file pointer, in bytes. It is usually 1, 2, or 3 bytes. Most tables manage with 2
bytes, but this is calculated automatically by MySQL. It is always a block address.

• Max datafile length

How long the table data file can become, in bytes.

• Max keyfile length

How long the table index file can become, in bytes.

• Recordlength

How much space each row takes, in bytes.

The table description part of the output includes a list of all keys in the table. For each key,
myisamchk displays some low-level information:

536

myisamchk — MyISAM Table-Maintenance Utility

• Key

This key's number. This value is shown only for the first column of the key. If this value is missing,
the line corresponds to the second or later column of a multiple-column key. For the table shown in
the example, there are two table description lines for the second index. This indicates that it is
a multiple-part index with two parts.

• Start

Where in the row this portion of the index starts.

• Len

How long this portion of the index is. For packed numbers, this should always be the full length of the
column. For strings, it may be shorter than the full length of the indexed column, because you can
index a prefix of a string column. The total length of a multiple-part key is the sum of the Len values
for all key parts.

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

This is a statistical value used by the optimizer. It tells how many rows there are per value for this
index. A unique index always has a value of 1. This may be updated after a table is loaded (or
greatly changed) with myisamchk -a. If this is not updated at all, a default value of 30 is given.

The last part of the output provides information about each column:

• Field

The column number.

• Start

The byte position of the column within table rows.

• Length

The length of the column in bytes.

• Nullpos, Nullbit

For columns that can be NULL, MyISAM stores NULL values as a flag in a byte. Depending on
how many nullable columns there are, there can be one or more bytes used for this purpose. The
Nullpos and Nullbit values, if nonempty, indicate which byte and bit contains that flag indicating
whether the column is NULL.

537

myisamchk — MyISAM Table-Maintenance Utility

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

Do not store zeros.

• always zero

Zero values are stored using one bit.

• Huff tree

The number of the Huffman tree associated with the column.

• Bits

The number of bits used in the Huffman tree.

The Huff tree and Bits fields are displayed if the table has been compressed with myisampack.
See Section 6.6.6, “myisampack — Generate Compressed, Read-Only MyISAM Tables”, for an
example of this information.

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

538

myisamchk — MyISAM Table-Maintenance Utility

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

How many deleted blocks still have reserved space. You can optimize your table to minimize this
space. See Section 9.6.4, “MyISAM Table Optimization”.

• Key

The key number.

• Keyblocks used

What percentage of the keyblocks are used. When a table has just been reorganized with
myisamchk, the values are very high (very near theoretical maximum).

• Packed

MySQL tries to pack key values that have a common suffix. This can only be used for indexes on
CHAR and VARCHAR columns. For long indexed strings that have similar leftmost parts, this can
significantly reduce the space used. In the preceding example, the second key is 40 bytes long and a
97% reduction in space is achieved.

• Max levels

How deep the B-tree for this key is. Large tables with long key values get high values.

• Records

How many rows are in the table.

• M.recordlength

The average row length. This is the exact row length for tables with fixed-length rows, because all
rows have the same length.

• Packed

MySQL strips spaces from the end of strings. The Packed value indicates the percentage of savings
achieved by doing this.

• Recordspace used

539

myisamchk — MyISAM Table-Maintenance Utility

What percentage of the data file is used.

• Empty space

What percentage of the data file is unused.

• Blocks/Record

Average number of blocks per row (that is, how many links a fragmented row is composed of). This
is always 1.0 for fixed-format tables. This value should stay as close to 1.0 as possible. If it gets too
large, you can reorganize the table. See Section 9.6.4, “MyISAM Table Optimization”.

• Recordblocks

How many blocks (links) are used. For fixed-format tables, this is the same as the number of rows.

• Deleteblocks

How many blocks (links) are deleted.

• Recorddata

How many bytes in the data file are used.

• Deleted data

How many bytes in the data file are deleted (unused).

• Lost space

If a row is updated to a shorter length, some space is lost. This is the sum of all such losses, in
bytes.

• Linkdata

When the dynamic table format is used, row fragments are linked with pointers (4 to 7 bytes each).
Linkdata is the sum of the amount of storage used by all such pointers.

6.6.4.6 myisamchk Memory Usage

Memory allocation is important when you run myisamchk. myisamchk uses no more memory than
its memory-related variables are set to. If you are going to use myisamchk on very large tables, you
should first decide how much memory you want it to use. The default is to use only about 3MB to
perform repairs. By using larger values, you can get myisamchk to operate faster. For example, if you
have more than 512MB RAM available, you could use options such as these (in addition to any other
options you might specify):

myisamchk --myisam_sort_buffer_size=256M \
           --key_buffer_size=512M \
           --read_buffer_size=64M \
           --write_buffer_size=64M ...

Using --myisam_sort_buffer_size=16M is probably enough for most cases.

Be aware that myisamchk uses temporary files in TMPDIR. If TMPDIR points to a memory file system,
out of memory errors can easily occur. If this happens, run myisamchk with the --tmpdir=dir_name
option to specify a directory located on a file system that has more space.

When performing repair operations, myisamchk also needs a lot of disk space:

• Twice the size of the data file (the original file and a copy). This space is not needed if you do a

repair with --quick; in this case, only the index file is re-created. This space must be available on
the same file system as the original data file, as the copy is created in the same directory as the
original.

540

myisamlog — Display MyISAM Log File Contents

• Space for the new index file that replaces the old one. The old index file is truncated at the start of

the repair operation, so you usually ignore this space. This space must be available on the same file
system as the original data file.

• When using --recover or --sort-recover (but not when using --safe-recover), you need

space on disk for sorting. This space is allocated in the temporary directory (specified by TMPDIR or
--tmpdir=dir_name). The following formula yields the amount of space required:

(largest_key + row_pointer_length) * number_of_rows * 2

You can check the length of the keys and the row_pointer_length with myisamchk -
dv tbl_name (see Section 6.6.4.5, “Obtaining Table Information with myisamchk”). The
row_pointer_length and number_of_rows values are the Datafile pointer and Data
records values in the table description. To determine the largest_key value, check the Key
lines in the table description. The Len column indicates the number of bytes for each key part. For a
multiple-column index, the key size is the sum of the Len values for all key parts.

If you have a problem with disk space during repair, you can try --safe-recover instead of --
recover.

6.6.5 myisamlog — Display MyISAM Log File Contents

myisamlog processes the contents of a MyISAM log file. To create such a file, start the server with a
--log-isam=log_file option.

Invoke myisamlog like this:

myisamlog [options] [file_name [tbl_name] ...]

The default operation is update (-u). If a recovery is done (-r), all writes and possibly updates
and deletes are done and errors are only counted. The default log file name is myisam.log if no
log_file argument is given. If tables are named on the command line, only those tables are updated.

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

541

myisampack — Generate Compressed, Read-Only MyISAM Tables

Perform a recovery operation.

• -R record_pos_file record_pos

Specify record position file and record position.

• -u

Perform an update operation.

• -v

Verbose mode. Print more output about what the program does. This option can be given multiple
times to produce more and more output.

• -w write_file

Specify the write file.

• -V

Display version information.

6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables

The myisampack utility compresses MyISAM tables. myisampack works by compressing each column
in the table separately. Usually, myisampack packs the data file 40% to 70%.

When the table is used later, the server reads into memory the information needed to decompress
columns. This results in much better performance when accessing individual rows, because you only
have to uncompress exactly one row.

MySQL uses mmap() when possible to perform memory mapping on compressed tables. If mmap()
does not work, MySQL falls back to normal read/write file operations.

Please note the following:

• If the mysqld server was invoked with external locking disabled, it is not a good idea to invoke

myisampack if the table might be updated by the server during the packing process. It is safest to
compress tables with the server stopped.

• After packing a table, it becomes read only. This is generally intended (such as when accessing

packed tables on a CD).

• myisampack does not support partitioned tables.

Invoke myisampack like this:

myisampack [options] file_name ...

Each file name argument should be the name of an index (.MYI) file. If you are not in the database
directory, you should specify the path name to the file. It is permissible to omit the .MYI extension.

After you compress a table with myisampack, use myisamchk -rq to rebuild its indexes.
Section 6.6.4, “myisamchk — MyISAM Table-Maintenance Utility”.

myisampack supports the following options. It also reads option files and supports the options
for processing them described at Section 6.2.2.3, “Command-Line Options that Affect Option-File
Handling”.

• --help, -?

Command-Line Format

--help

542

myisampack — Generate Compressed, Read-Only MyISAM Tables

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

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --force, -f

Command-Line Format

--force

Produce a packed table even if it becomes larger than the original or if the intermediate file from
an earlier invocation of myisampack exists. (myisampack creates an intermediate file named
tbl_name.TMD in the database directory while it compresses the table. If you kill myisampack,
the .TMD file might not be deleted.) Normally, myisampack exits with an error if it finds that
tbl_name.TMD exists. With --force, myisampack packs the table anyway.

• --join=big_tbl_name, -j big_tbl_name

Command-Line Format

--join=big_tbl_name

Type

String

Join all tables named on the command line into a single packed table big_tbl_name. All tables that
are to be combined must have identical structure (same column names and types, same indexes,
and so forth).

big_tbl_name must not exist prior to the join operation. All source tables named on the command
line to be merged into big_tbl_name must exist. The source tables are read for the join operation
but not modified.

• --silent, -s

Command-Line Format

--silent

543

myisampack — Generate Compressed, Read-Only MyISAM Tables

Silent mode. Write output only when errors occur.

• --test, -t

Command-Line Format

--test

Do not actually pack the table, just test packing it.

• --tmpdir=dir_name, -T dir_name

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

Wait and retry if the table is in use. If the mysqld server was invoked with external locking disabled,
it is not a good idea to invoke myisampack if the table might be updated by the server during the
packing process.

The following sequence of commands illustrates a typical table compression session:

$> ls -l station.*
-rw-rw-r--   1 jones    my         994128 Apr 17 19:00 station.MYD
-rw-rw-r--   1 jones    my          53248 Apr 17 19:00 station.MYI

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

544

myisampack — Generate Compressed, Read-Only MyISAM Tables

2   32    30  multip. text                10240       1024          1

Field Start Length Type
1     1     1
2     2     4
3     6     4
4     10    1
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

545

myisampack — Generate Compressed, Read-Only MyISAM Tables

$> myisamchk -rq station
- check record delete-chain
- recovering (with sort) MyISAM-table 'station'
Data records: 1192
- Fixing index 1
- Fixing index 2

$> mysqladmin -uroot flush-tables

$> ls -l station.*
-rw-rw-r--   1 jones    my         127874 Apr 17 19:00 station.MYD
-rw-rw-r--   1 jones    my          55296 Apr 17 19:04 station.MYI

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
37    404   1                                           2     9
38    405   4      no zeros                             2     9
39    409   4      always zero                          2     9
40    413   4      no zeros                             2     9

546

myisampack — Generate Compressed, Read-Only MyISAM Tables

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

The number of integer columns that do not occupy the full byte range of their type. These are
changed to a smaller type. For example, a BIGINT column (eight bytes) can be stored as a
TINYINT column (one byte) if all its values are in the range from -128 to 127.

• pre-space

The number of decimal columns that are stored with leading spaces. In this case, each value
contains a count for the number of leading spaces.

• end-space

The number of columns that have a lot of trailing spaces. In this case, each value contains a count
for the number of trailing spaces.

• table-lookup

The column had only a small number of different values, which were converted to an ENUM before
Huffman compression.

• zero

The number of columns for which all values are zero.

• Original trees

The initial number of Huffman trees.

• After join

The number of distinct Huffman trees left after joining trees to save some header space.

After a table has been compressed, the Field lines displayed by myisamchk -dvv include additional
information about each column:

547

mysql_config_editor — MySQL Configuration Utility

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

After you run myisampack, use myisamchk to re-create any indexes. At this time, you can also sort
the index blocks and create statistics needed for the MySQL optimizer to work more efficiently:

myisamchk -rq --sort-index --analyze tbl_name.MYI

After you have installed the packed table into the MySQL database directory, you should execute
mysqladmin flush-tables to force mysqld to start using the new table.

To unpack a packed table, use the --unpack option to myisamchk.

6.6.7 mysql_config_editor — MySQL Configuration Utility

The mysql_config_editor utility enables you to store authentication credentials in an obfuscated
login path file named .mylogin.cnf. The file location is the %APPDATA%\MySQL directory on
Windows and the current user's home directory on non-Windows systems. The file can be read later by
MySQL client programs to obtain authentication credentials for connecting to MySQL Server.

The unobfuscated format of the .mylogin.cnf login path file consists of option groups, similar
to other option files. Each option group in .mylogin.cnf is called a “login path,” which is a group

548

mysql_config_editor — MySQL Configuration Utility

that permits only certain options: host, user, password, port and socket. Think of a login path
option group as a set of options that specify which MySQL server to connect to and which account to
authenticate as. Here is an unobfuscated example:

[client]
user = mydefaultname
password = mydefaultpass
host = 127.0.0.1
[mypath]
user = myothername
password = myotherpass
host = localhost

When you invoke a client program to connect to the server, the client uses .mylogin.cnf in
conjunction with other option files. Its precedence is higher than other option files, but less than options
specified explicitly on the client command line. For information about the order in which option files are
used, see Section 6.2.2.2, “Using Option Files”.

To specify an alternate login path file name, set the MYSQL_TEST_LOGIN_FILE environment
variable. This variable is recognized by mysql_config_editor, by standard MySQL clients (mysql,
mysqladmin, and so forth), and by the mysql-test-run.pl testing utility.

Programs use groups in the login path file as follows:

• mysql_config_editor operates on the client login path by default if you specify no --login-

path=name option to indicate explicitly which login path to use.

• Without a --login-path option, client programs read the same option groups from the login path

file that they read from other option files. Consider this command:

mysql

By default, the mysql client reads the [client] and [mysql] groups from other option files, so it
reads them from the login path file as well.

• With a --login-path option, client programs additionally read the named login path from the login
path file. The option groups read from other option files remain the same. Consider this command:

mysql --login-path=mypath

The mysql client reads [client] and [mysql] from other option files, and [client], [mysql],
and [mypath] from the login path file.

• Client programs read the login path file even when the --no-defaults option is used, unless
--no-login-paths is set. This permits passwords to be specified in a safer way than on the
command line even if --no-defaults is present.

mysql_config_editor obfuscates the .mylogin.cnf file so it cannot be read as cleartext, and
its contents when unobfuscated by client programs are used only in memory. In this way, passwords
can be stored in a file in non-cleartext format and used later without ever needing to be exposed on the
command line or in an environment variable. mysql_config_editor provides a print command for
displaying the login path file contents, but even in this case, password values are masked so as never
to appear in a way that other users can see them.

The obfuscation used by mysql_config_editor prevents passwords from appearing in
.mylogin.cnf as cleartext and provides a measure of security by preventing inadvertent password
exposure. For example, if you display a regular unobfuscated my.cnf option file on the screen,
any passwords it contains are visible for anyone to see. With .mylogin.cnf, that is not true, but
the obfuscation used is not likely to deter a determined attacker and you should not consider it
unbreakable. A user who can gain system administration privileges on your machine to access your
files could unobfuscate the .mylogin.cnf file with some effort.

The login path file must be readable and writable to the current user, and inaccessible to other users.
Otherwise, mysql_config_editor ignores it, and client programs do not use it, either.

549

mysql_config_editor — MySQL Configuration Utility

Invoke mysql_config_editor like this:

mysql_config_editor [program_options] command [command_options]

If the login path file does not exist, mysql_config_editor creates it.

Command arguments are given as follows:

• program_options consists of general mysql_config_editor options.

• command indicates what action to perform on the .mylogin.cnf login path file. For example, set

writes a login path to the file, remove removes a login path, and print displays login path contents.

• command_options indicates any additional options specific to the command, such as the login path

name and the values to use in the login path.

The position of the command name within the set of program arguments is significant. For example,
these command lines have the same arguments, but produce different results:

mysql_config_editor --help set
mysql_config_editor set --help

The first command line displays a general mysql_config_editor help message, and ignores the
set command. The second command line displays a help message specific to the set command.

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

mysql_config_editor uses the client login path by default, so the --login-path=client
option can be omitted from the first command without changing its effect.

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

The print command displays each login path as a set of lines beginning with a group header
indicating the login path name in square brackets, followed by the option values for the login path.
Password values are masked and do not appear as cleartext.

If you do not specify --all to display all login paths or --login-path=name to display a named
login path, the print command displays the client login path by default, if there is one.

As shown by the preceding example, the login path file can contain multiple login paths. In this way,
mysql_config_editor makes it easy to set up multiple “personalities” for connecting to different
MySQL servers, or for connecting to a given server using different accounts. Any of these can be

550

mysql_config_editor — MySQL Configuration Utility

selected by name later using the --login-path option when you invoke a client program. For
example, to connect to the remote server, use this command:

mysql --login-path=remote

Here, mysql reads the [client] and [mysql] option groups from other option files, and the
[client], [mysql], and [remote] groups from the login path file.

To connect to the local server, use this command:

mysql --login-path=client

Because mysql reads the client and mysql login paths by default, the --login-path option does
not add anything in this case. That command is equivalent to this one:

mysql

Options read from the login path file take precedence over options read from other option files. Options
read from login path groups appearing later in the login path file take precedence over options read
from groups appearing earlier in the file.

mysql_config_editor adds login paths to the login path file in the order you create them, so you
should create more general login paths first and more specific paths later. If you need to move a login
path within the file, you can remove it, then recreate it to add it to the end. For example, a client
login path is more general because it is read by all client programs, whereas a mysqldump login path
is read only by mysqldump. Options specified later override options specified earlier, so putting the
login paths in the order client, mysqldump enables mysqldump-specific options to override client
options.

When you use the set command with mysql_config_editor to create a login path, you need
not specify all possible option values (host name, user name, password, port, socket). Only those
values given are written to the path. Any missing values required later can be specified when you
invoke a client path to connect to the MySQL server, either in other option files or on the command
line. Any options specified on the command line override those specified in the login path file or
other option files. For example, if the credentials in the remote login path also apply for the host
remote2.example.com, connect to the server on that host like this:

mysql --login-path=remote --host=remote2.example.com

mysql_config_editor General Options

mysql_config_editor supports the following general options, which may be used preceding
any command named on the command line. For descriptions of command-specific options, see
mysql_config_editor Commands and Command-Specific Options.

Table 6.18 mysql_config_editor General Options

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

To see a command-specific help message, invoke mysql_config_editor as follows, where
command is a command other than help:

551

mysql_config_editor — MySQL Configuration Utility

mysql_config_editor command --help

• --debug[=debug_options], -# debug_options

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/mysql_config_editor.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does. This option may be helpful in
diagnosing problems if an operation does not have the effect you expect.

• --version, -V

Command-Line Format

--version

Display version information and exit.

mysql_config_editor Commands and Command-Specific Options

This section describes the permitted mysql_config_editor commands, and, for each one, the
command-specific options permitted following the command name on the command line.

In addition, mysql_config_editor supports general options that can be used preceding any
command. For descriptions of these options, see mysql_config_editor General Options.

mysql_config_editor supports these commands:

• help

Display a general help message and exit. This command takes no following options.

To see a command-specific help message, invoke mysql_config_editor as follows, where
command is a command other than help:

mysql_config_editor command --help

• print [options]

Print the contents of the login path file in unobfuscated form, with the exception that passwords are
displayed as *****.

The default login path name is client if no login path is named. If both --all and --login-path
are given, --all takes precedence.

The print command permits these options following the command name:

• --help, -?

552

mysql_config_editor — MySQL Configuration Utility

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

553

mysql_config_editor — MySQL Configuration Utility

removes the entire login path. For example, this command removes only the user option from the
mypath login path rather than the entire mypath login path:

mysql_config_editor remove --login-path=mypath --user

This command removes the entire mypath login path:

mysql_config_editor remove --login-path=mypath

The remove command permits these options following the command name:

• --help, -?

Display a help message for the remove command and exit.

To see a general help message, use mysql_config_editor --help.

• --host, -h

Remove the host name from the login path.

• --login-path=name, -G name

The login path to remove or modify. The default login path name is client if this option is not
given.

• --password, -p

Remove the password from the login path.

• --port, -P

Remove the TCP/IP port number from the login path.

• --socket, -S

Remove the Unix socket file name from the login path.

• --user, -u

Remove the user name from the login path.

• --warn, -w

Warn and prompt the user for confirmation if the command attempts to remove the default login
path (client) and --login-path=client was not specified. This option is enabled by default;
use --skip-warn to disable it.

• reset [options]

Empty the contents of the login path file.

The reset command permits these options following the command name:

• --help, -?

Display a help message for the reset command and exit.

To see a general help message, use mysql_config_editor --help.

554

mysql_migrate_keyring — Keyring Key Migration Utility

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

To specify an empty password, press Enter at the password prompt. The resulting login path
written to the login path file includes a line like this:

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

6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility

The mysql_migrate_keyring utility migrates keys between one keyring component and another. It
supports offline and online migrations.

Invoke mysql_migrate_keyring like this (enter the command on a single line):

mysql_migrate_keyring
  --component-dir=dir_name
  --source-keyring=name
  --destination-keyring=name

555

mysql_migrate_keyring — Keyring Key Migration Utility

  [other options]

For information about key migrations and instructions describing how to perform them using
mysql_migrate_keyring and other methods, see Section 8.4.4.11, “Migrating Keys Between
Keyring Keystores”.

mysql_migrate_keyring supports the following options, which can be specified on the command
line or in the [mysql_migrate_keyring] group of an option file. For information about option files
used by MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.19 mysql_migrate_keyring Options

Option Name

--component-dir

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--destination-keyring

--destination-keyring-configuration-dir

Description

Directory for keyring components

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Destination keyring component name

Destination keyring component configuration
directory

--get-server-public-key

Request RSA public key from server

--help

--host

--login-path

--no-defaults

--no-login-paths

--online-migration

--password

--port

--print-defaults

Display help message and exit

Host on which MySQL server is located

Read login path options from .mylogin.cnf

Read no option files

Do not read login paths from the login path file

Migration source is an active server

Password to use when connecting to server

TCP/IP port number for connection

Print default options

--server-public-key-path

Path name to file containing RSA public key

--socket

--source-keyring

Unix socket file or Windows named pipe to use

Source keyring component name

--source-keyring-configuration-dir

Source keyring component configuration directory

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

--ssl-key

--ssl-mode

556

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

File that contains X.509 key

Desired security state of connection to server

mysql_migrate_keyring — Keyring Key Migration Utility

Option Name

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--tls-ciphersuites

--tls-sni-servername

--tls-version

--user

--verbose

--version

• --help, -h

Description

File that contains SSL session data

Whether to establish connections if session reuse
fails

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

MySQL user name to use when connecting to
server

Verbose mode

Display version information and exit

Command-Line Format

--help

Display a help message and exit.

• --component-dir=dir_name

Command-Line Format

--component-dir=dir_name

Type

Directory name

The directory where keyring components are located. This is typically the value of the plugin_dir
system variable for the local MySQL server.

Note

--component-dir, --source-keyring, and --destination-
keyring are mandatory for all keyring migration operations performed
by mysql_migrate_keyring. In addition, the source and destination
components must differ, and both components must be properly configured
so that mysql_migrate_keyring can load and use them.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

557

mysql_migrate_keyring — Keyring Key Migration Utility

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysql_migrate_keyring normally reads the [mysql_migrate_keyring] group. If
this option is given as --defaults-group-suffix=_other, mysql_migrate_keyring also
reads the [mysql_migrate_keyring_other] group.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --destination-keyring=name

Command-Line Format

--destination-keyring=name

Type

String

The destination keyring component for key migration. The format and interpretation of the option
value is the same as described for the --source-keyring option.

Note

--component-dir, --source-keyring, and --destination-
keyring are mandatory for all keyring migration operations performed
by mysql_migrate_keyring. In addition, the source and destination
components must differ, and both components must be properly configured
so that mysql_migrate_keyring can load and use them.

• --destination-keyring-configuration-dir=dir_name

Command-Line Format

--destination-keyring-configuration-
dir=dir_name

Type

Directory name

This option applies only if the destination keyring component global configuration file contains
"read_local_config": true, indicating that component configuration is contained in the local
configuration file. The option value specifies the directory containing that local file.

• --get-server-public-key

558

Command-Line Format

--get-server-public-key

mysql_migrate_keyring — Keyring Key Migration Utility

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

The host location of the running server that is currently using one of the key migration keystores.
Migration always occurs on the local host, so the option always specifies a value for connecting to a
local server, such as localhost, 127.0.0.1, ::1, or the local host IP address or host name.

• --login-path=name

Command-Line Format

--login-path=name

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

559

mysql_migrate_keyring — Keyring Key Migration Utility

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --online-migration

Command-Line Format

--online-migration

Type

Default Value

Boolean

FALSE

This option is mandatory when a running server is using the keyring. It tells
mysql_migrate_keyring to perform an online key migration. The option has these effects:

• mysql_migrate_keyring connects to the server using any connection options specified; these

options are otherwise ignored.

• After mysql_migrate_keyring connects to the server, it tells the server to pause keyring

operations. When key copying is complete, mysql_migrate_keyring tells the server it can
resume keyring operations before disconnecting.

• --password[=password], -p[password]

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the running server that is currently
using one of the key migration keystores. The password value is optional. If not given,
mysql_migrate_keyring prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysql_migrate_keyring should not
prompt for one, use the --skip-password option.

• --port=port_num, -P port_num

560

Command-Line Format

Type

--port=port_num

Numeric

mysql_migrate_keyring — Keyring Key Migration Utility

Default Value

0

For TCP/IP connections, the port number for connecting to the running server that is currently using
one of the key migration keystores.

• --print-defaults

Command-Line Format

--print-defaults

Print the program name and all options that it gets from option files.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For Unix socket file or Windows named pipe connections, the socket file or named pipe for
connecting to the running server that is currently using one of the key migration keystores.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --source-keyring=name

Command-Line Format

--source-keyring=name

561

mysql_migrate_keyring — Keyring Key Migration Utility

Type

String

The source keyring component for key migration. This is the component library file name specified
without any platform-specific extension such as .so or .dll. For example, to use the component
for which the library file is component_keyring_file.so, specify the option as --source-
keyring=component_keyring_file.

Note

--component-dir, --source-keyring, and --destination-
keyring are mandatory for all keyring migration operations performed
by mysql_migrate_keyring. In addition, the source and destination
components must differ, and both components must be properly configured
so that mysql_migrate_keyring can load and use them.

• --source-keyring-configuration-dir=dir_name

Command-Line Format

--source-keyring-configuration-
dir=dir_name

Type

Directory name

This option applies only if the source keyring component global configuration file contains
"read_local_config": true, indicating that component configuration is contained in the local
configuration file. The option value specifies the directory containing that local file.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

562

mysql_migrate_keyring — Keyring Key Migration Utility

• STRICT: Enable “strict” FIPS mode.

Note

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON
or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name

563

mysqlbinlog — Utility for Processing Binary Log Files

Type

String

The user name of the MySQL account used for connecting to the running server that is currently
using one of the key migration keystores.

• --verbose, -v

Command-Line Format

--verbose

Verbose mode. Produce more output about what the program does.

• --version, -V

Command-Line Format

--version

Display version information and exit.

6.6.9 mysqlbinlog — Utility for Processing Binary Log Files

The server's binary log consists of files containing “events” that describe modifications to database
contents. The server writes these files in binary format. To display their contents in text format, use the
mysqlbinlog utility. You can also use mysqlbinlog to display the contents of relay log files written
by a replica server in a replication setup because relay logs have the same format as binary logs. The
binary log and relay log are discussed further in Section 7.4.4, “The Binary Log”, and Section 19.2.4,
“Relay Log and Replication Metadata Repositories”.

Invoke mysqlbinlog like this:

mysqlbinlog [options] log_file ...

For example, to display the contents of the binary log file named binlog.000003, use this command:

mysqlbinlog binlog.000003

The output includes events contained in binlog.000003. For statement-based logging, event
information includes the SQL statement, the ID of the server on which it was executed, the timestamp
when the statement was executed, how much time it took, and so forth. For row-based logging,
the event indicates a row change rather than an SQL statement. See Section 19.2.1, “Replication
Formats”, for information about logging modes.

Events are preceded by header comments that provide additional information. For example:

# at 141
#100309  9:28:36 server id 123  end_log_pos 245
  Query thread_id=3350  exec_time=11  error_code=0

In the first line, the number following at indicates the file offset, or starting position, of the event in the
binary log file.

The second line starts with a date and time indicating when the statement started on the server where
the event originated. For replication, this timestamp is propagated to replica servers. server id is the
server_id value of the server where the event originated. end_log_pos indicates where the next
event starts (that is, it is the end position of the current event + 1). thread_id indicates which thread
executed the event. exec_time is the time spent executing the event, on a replication source server.
On a replica, it is the difference of the end execution time on the replica minus the beginning execution
time on the source. The difference serves as an indicator of how much replication lags behind the
source. error_code indicates the result from executing the event. Zero means that no error occurred.

564

mysqlbinlog — Utility for Processing Binary Log Files

Note

When using event groups, the file offsets of events may be grouped together
and the comments of events may be grouped together. Do not mistake these
grouped events for blank file offsets.

The output from mysqlbinlog can be re-executed (for example, by using it as input to mysql)
to redo the statements in the log. This is useful for recovery operations after an unexpected
server exit. For other usage examples, see the discussion later in this section and in Section 9.5,
“Point-in-Time (Incremental) Recovery”. To execute the internal-use BINLOG statements used by
mysqlbinlog, the user requires the BINLOG_ADMIN privilege (or the deprecated SUPER privilege), or
the REPLICATION_APPLIER privilege plus the appropriate privileges to execute each log event.

You can use mysqlbinlog to read binary log files directly and apply them to the local MySQL server.
You can also read binary logs from a remote server by using the --read-from-remote-server
option. To read remote binary logs, the connection parameter options can be given to indicate how to
connect to the server. These options are --host, --password, --port, --protocol, --socket,
and --user.

When binary log files have been encrypted, mysqlbinlog cannot read them directly, but can read
them from the server using the --read-from-remote-server option. Binary log files are encrypted
when the server's binlog_encryption system variable is set to ON. The SHOW BINARY LOGS
statement shows whether a particular binary log file is encrypted or unencrypted. Encrypted and
unencrypted binary log files can also be distinguished using the magic number at the start of the file
header for encrypted log files (0xFD62696E), which differs from that used for unencrypted log files
(0xFE62696E). Note that mysqlbinlog returns a suitable error if you attempt to read an encrypted
binary log file directly, but older versions of mysqlbinlog do not recognise the file as a binary log file
at all. For more information on binary log encryption, see Section 19.3.2, “Encrypting Binary Log Files
and Relay Log Files”.

When binary log transaction payloads have been compressed, mysqlbinlog automatically
decompresses and decodes the transaction payloads, and prints them as it would uncompressed
events. When binlog_transaction_compression is set to ON, transaction payloads
are compressed and then written to the server's binary log file as a single event (a
Transaction_payload_event). With the --verbose option, mysqlbinlog adds comments
stating the compression algorithm used, the compressed payload size that was originally received, and
the resulting payload size after decompression.

Note

The end position (end_log_pos) that mysqlbinlog states for an individual
event that was part of a compressed transaction payload is the same as the end
position of the original compressed payload. Multiple decompressed events can
therefore have the same end position.

mysqlbinlog's own connection compression does less if transaction payloads
are already compressed, but still operates on uncompressed transactions and
headers.

For more information on binary log transaction compression, see Section 7.4.4.5, “Binary Log
Transaction Compression”.

When running mysqlbinlog against a large binary log, be careful that the filesystem has enough
space for the resulting files. To configure the directory that mysqlbinlog uses for temporary files, use
the TMPDIR environment variable.

mysqlbinlog sets the value of pseudo_replica_mode to true before executing
any SQL statements. This system variable affects the handling of XA transactions, the
original_commit_timestamp replication delay timestamp and the original_server_version
system variable, and unsupported SQL modes.

565

mysqlbinlog — Utility for Processing Binary Log Files

mysqlbinlog supports the following options, which can be specified on the command line or in the
[mysqlbinlog] and [client] groups of an option file. For information about option files used by
MySQL programs, see Section 6.2.2.2, “Using Option Files”.

Table 6.20 mysqlbinlog Options

Option Name

--base64-output

--bind-address

Description

Print binary log entries using base-64 encoding

Use specified network interface to connect to
MySQL Server

--binlog-row-event-max-size

Binary log max event size

--character-sets-dir

--compress

--compression-algorithms

--connection-server-id

--database

--debug

--debug-check

--debug-info

--default-auth

--defaults-extra-file

--defaults-file

--defaults-group-suffix

--disable-log-bin

--exclude-gtids

--force-if-open

--force-read

Directory where character sets are installed

Compress all information sent between client and
server

Permitted compression algorithms for connections
to server

Used for testing and debugging. See text for
applicable default values and other particulars

List entries for just this database

Write debugging log

Print debugging information when program exits

Print debugging information, memory, and CPU
statistics when program exits

Authentication plugin to use

Read named option file in addition to usual option
files

Read only named option file

Option group suffix value

Disable binary logging

Do not show any of the groups in the GTID set
provided

Read binary log files even if open or not closed
properly

If mysqlbinlog reads a binary log event that it does
not recognize, it prints a warning

--get-server-public-key

Request RSA public key from server

--help

--hexdump

--host

--idempotent

--include-gtids

--local-load

--login-path

--no-defaults

--no-login-paths

566

Display help message and exit

Display a hex dump of the log in comments

Host on which MySQL server is located

Cause the server to use idempotent mode while
processing binary log updates from this session
only

Show only the groups in the GTID set provided

Prepare local temporary files for LOAD DATA in
the specified directory

Read login path options from .mylogin.cnf

Read no option files

Do not read login paths from the login path file

mysqlbinlog — Utility for Processing Binary Log Files

Option Name

--offset

--password

--plugin-dir

--port

--print-defaults

--print-table-metadata

--protocol

--raw

--read-from-remote-master

--read-from-remote-server

--read-from-remote-source

Description

Skip the first N entries in the log

Password to use when connecting to server

Directory where plugins are installed

TCP/IP port number for connection

Print default options

Print table metadata

Transport protocol to use

Write events in raw (binary) format to output files

Read the binary log from a MySQL replication
source server rather than reading a local log file

Read binary log from MySQL server rather than
local log file

Read the binary log from a MySQL replication
source server rather than reading a local log file

--require-row-format

Require row-based binary logging format

--result-file

--rewrite-db

--server-id

--server-id-bits

--server-public-key-path

--set-charset

--shared-memory-base-name

--short-form

--skip-gtids

--socket

--ssl-ca

--ssl-capath

--ssl-cert

--ssl-cipher

--ssl-crl

--ssl-crlpath

--ssl-fips-mode

Direct output to named file

Create rewrite rules for databases when playing
back from logs written in row-based format. Can
be used multiple times

Extract only those events created by the server
having the given server ID

Tell mysqlbinlog how to interpret server IDs in
binary log when log was written by a mysqld
having its server-id-bits set to less than the
maximum; supported only by MySQL Cluster
version of mysqlbinlog

Path name to file containing RSA public key

Add a SET NAMES charset_name statement to
the output

Shared-memory name for shared-memory
connections (Windows only)

Display only the statements contained in the log

Do not include the GTIDs from the binary log files
in the output dump file

Unix socket file or Windows named pipe to use

File that contains list of trusted SSL Certificate
Authorities

Directory that contains trusted SSL Certificate
Authority certificate files

File that contains X.509 certificate

Permissible ciphers for connection encryption

File that contains certificate revocation lists

Directory that contains certificate revocation-list
files

Whether to enable FIPS mode on client side

567

mysqlbinlog — Utility for Processing Binary Log Files

Option Name

--ssl-key

--ssl-mode

--ssl-session-data

--ssl-session-data-continue-on-failed-reuse

--start-datetime

--start-position

--stop-datetime

--stop-never

--stop-never-slave-server-id

--stop-position

--tls-ciphersuites

--tls-sni-servername

--tls-version

--to-last-log

--user

--verbose

Description

File that contains X.509 key

Desired security state of connection to server

File that contains SSL session data

Whether to establish connections if session reuse
fails

Read binary log from first event with timestamp
equal to or later than datetime argument

Decode binary log from first event with position
equal to or greater than argument

Stop reading binary log at first event with
timestamp equal to or greater than datetime
argument

Stay connected to server after reading last binary
log file

Slave server ID to report when connecting to
server

Stop decoding binary log at first event with
position equal to or greater than argument

Permissible TLSv1.3 ciphersuites for encrypted
connections

Server name supplied by the client

Permissible TLS protocols for encrypted
connections

Do not stop at the end of requested binary log
from a MySQL server, but rather continue printing
to end of last binary log

MySQL user name to use when connecting to
server

Reconstruct row events as SQL statements

--verify-binlog-checksum

Verify checksums in binary log

--version

--zstd-compression-level

• --help, -?

Display version information and exit

Compression level for connections to server that
use zstd compression

Command-Line Format

--help

Display a help message and exit.

• --base64-output=value

Command-Line Format

--base64-output=value

Type

Default Value

Valid Values

568

String

AUTO

AUTO

NEVER

mysqlbinlog — Utility for Processing Binary Log Files

DECODE-ROWS

This option determines when events should be displayed encoded as base-64 strings using BINLOG
statements. The option has these permissible values (not case-sensitive):

• AUTO ("automatic") or UNSPEC ("unspecified") displays BINLOG statements automatically when

necessary (that is, for format description events and row events). If no --base64-output option
is given, the effect is the same as --base64-output=AUTO.

Note

Automatic BINLOG display is the only safe behavior if you intend to use the
output of mysqlbinlog to re-execute binary log file contents. The other
option values are intended only for debugging or testing purposes because
they may produce output that does not include all events in executable
form.

• NEVER causes BINLOG statements not to be displayed. mysqlbinlog exits with an error if a row

event is found that must be displayed using BINLOG.

• DECODE-ROWS specifies to mysqlbinlog that you intend for row events to be decoded and

displayed as commented SQL statements by also specifying the --verbose option. Like NEVER,
DECODE-ROWS suppresses display of BINLOG statements, but unlike NEVER, it does not exit with
an error if a row event is found.

For examples that show the effect of --base64-output and --verbose on row event output, see
Section 6.6.9.2, “mysqlbinlog Row Event Display”.

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

The directory where character sets are installed. See Section 12.15, “Character Set Configuration”.

• --compress

569

mysqlbinlog — Utility for Processing Binary Log Files

Command-Line Format

--compress[={OFF|ON}]

Deprecated

Type

Default Value

Yes

Boolean

OFF

Compress all information sent between the client and the server if possible. See Section 6.2.8,
“Connection Compression Control”.

This option is deprecated. Expect it to be removed in a future version of MySQL. See Configuring
Legacy Connection Compression.

• --compression-algorithms=value

Command-Line Format

--compression-algorithms=value

Type

Default Value

Valid Values

Set

uncompressed

zlib

zstd

uncompressed

The permitted compression algorithms for connections to the server. The available algorithms are
the same as for the protocol_compression_algorithms system variable. The default value is
uncompressed.

For more information, see Section 6.2.8, “Connection Compression Control”.

• --connection-server-id=server_id

Command-Line Format

--connection-server-id=#]

Type

Default Value

Minimum Value

Maximum Value

Integer

0 (1)

0 (1)

4294967295

--connection-server-id specifies the server ID that mysqlbinlog reports when it connects to
the server. It can be used to avoid a conflict with the ID of a replica server or another mysqlbinlog
process.

If the --read-from-remote-server option is specified, mysqlbinlog reports a server ID of 0,
which tells the server to disconnect after sending the last log file (nonblocking behavior). If the --
stop-never option is also specified to maintain the connection to the server, mysqlbinlog reports
a server ID of 1 by default instead of 0, and --connection-server-id can be used to replace
that server ID if required. See Section 6.6.9.4, “Specifying the mysqlbinlog Server ID”.

• --database=db_name, -d db_name

Command-Line Format

--database=db_name

570

mysqlbinlog — Utility for Processing Binary Log Files

Type

String

This option causes mysqlbinlog to output entries from the binary log (local log only) that occur
while db_name is been selected as the default database by USE.

The --database option for mysqlbinlog is similar to the --binlog-do-db option for mysqld,
but can be used to specify only one database. If --database is given multiple times, only the last
instance is used.

The effects of this option depend on whether the statement-based or row-based logging format is in
use, in the same way that the effects of --binlog-do-db depend on whether statement-based or
row-based logging is in use.

Statement-based logging.

 The --database option works as follows:

• While db_name is the default database, statements are output whether they modify tables in

db_name or a different database.

• Unless db_name is selected as the default database, statements are not output, even if they

modify tables in db_name.

• There is an exception for CREATE DATABASE, ALTER DATABASE, and DROP DATABASE. The
database being created, altered, or dropped is considered to be the default database when
determining whether to output the statement.

Suppose that the binary log was created by executing these statements using statement-based-
logging:

INSERT INTO test.t1 (i) VALUES(100);
INSERT INTO db2.t2 (j)  VALUES(200);
USE test;
INSERT INTO test.t1 (i) VALUES(101);
INSERT INTO t1 (i)      VALUES(102);
INSERT INTO db2.t2 (j)  VALUES(201);
USE db2;
INSERT INTO test.t1 (i) VALUES(103);
INSERT INTO db2.t2 (j)  VALUES(202);
INSERT INTO t2 (j)      VALUES(203);

mysqlbinlog --database=test does not output the first two INSERT statements because there
is no default database. It outputs the three INSERT statements following USE test, but not the
three INSERT statements following USE db2.

mysqlbinlog --database=db2 does not output the first two INSERT statements because there
is no default database. It does not output the three INSERT statements following USE test, but
does output the three INSERT statements following USE db2.

 mysqlbinlog outputs only entries that change tables belonging to

Row-based logging.
db_name. The default database has no effect on this. Suppose that the binary log just described
was created using row-based logging rather than statement-based logging. mysqlbinlog --
database=test outputs only those entries that modify t1 in the test database, regardless of
whether USE was issued or what the default database is.

If a server is running with binlog_format set to MIXED and you want it to be possible to use
mysqlbinlog with the --database option, you must ensure that tables that are modified are in the
database selected by USE. (In particular, no cross-database updates should be used.)

When used together with the --rewrite-db option, the --rewrite-db option is applied first;
then the --database option is applied, using the rewritten database name. The order in which the
options are provided makes no difference in this regard.

571

mysqlbinlog — Utility for Processing Binary Log Files

• --debug[=debug_options], -# [debug_options]

Command-Line Format

--debug[=debug_options]

Type

Default Value

String

d:t:o,/tmp/mysqlbinlog.trace

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/mysqlbinlog.trace.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-check

Command-Line Format

--debug-check

Type

Default Value

Boolean

FALSE

Print some debugging information when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --debug-info

Command-Line Format

--debug-info

Type

Default Value

Boolean

FALSE

Print debugging information and memory and CPU usage statistics when the program exits.

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• --default-auth=plugin

Command-Line Format

--default-auth=plugin

Type

String

A hint about which client-side authentication plugin to use. See Section 8.2.17, “Pluggable
Authentication”.

• --defaults-extra-file=file_name

Command-Line Format

--defaults-extra-file=file_name

572

mysqlbinlog — Utility for Processing Binary Log Files

Type

File name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it
is interpreted relative to the current directory.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-file=file_name

Command-Line Format

--defaults-file=file_name

Type

File name

Use only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Exception: Even with --defaults-file, client programs read .mylogin.cnf.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Command-Line Format

--defaults-group-suffix=str

Type

String

Read not only the usual option groups, but also groups with the usual names and a suffix of str.
For example, mysqlbinlog normally reads the [client] and [mysqlbinlog] groups. If
this option is given as --defaults-group-suffix=_other, mysqlbinlog also reads the
[client_other] and [mysqlbinlog_other] groups.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --disable-log-bin, -D

Command-Line Format

--disable-log-bin

Disable binary logging. This is useful for avoiding an endless loop if you use the --to-last-
log option and are sending the output to the same MySQL server. This option also is useful when
restoring after an unexpected exit to avoid duplication of the statements you have logged.

This option causes mysqlbinlog to include a SET sql_log_bin = 0 statement in its output to
disable binary logging of the remaining output. Manipulating the session value of the sql_log_bin
system variable is a restricted operation, so this option requires that you have privileges sufficient to
set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

• --exclude-gtids=gtid_set

Command-Line Format

--exclude-gtids=gtid_set

Type

String

573

mysqlbinlog — Utility for Processing Binary Log Files

Default Value

Do not display any of the groups listed in the gtid_set.

• --force-if-open, -F

Command-Line Format

--force-if-open

Read binary log files even if they are open or were not closed properly (IN_USE flag is set); do not
fail if the file ends with a truncated event.

The IN_USE flag is set only for the binary log that is currently written by the server; if the server has
crashed, the flag remains set until the server is started up again and recovers the binary log. Without
this option, mysqlbinlog refuses to process a file with this flag set. Since the server may be in the
process of writing the file, truncation of the last event is considered normal.

• --force-read, -f

Command-Line Format

--force-read

With this option, if mysqlbinlog reads a binary log event that it does not recognize, it prints a
warning, ignores the event, and continues. Without this option, mysqlbinlog stops if it reads such
an event.

• --get-server-public-key

Command-Line Format

--get-server-public-key

Type

Boolean

Request from the server the public key required for RSA key pair-based password exchange. This
option applies to clients that authenticate with the caching_sha2_password authentication
plugin. For that plugin, the server does not send the public key unless requested. This option
is ignored for accounts that do not authenticate with that plugin. It is also ignored if RSA-based
password exchange is not used, as is the case when the client connects to the server using a secure
connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For information about the caching_sha2_password plugin, see Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --hexdump, -H

Command-Line Format

--hexdump

Display a hex dump of the log in comments, as described in Section 6.6.9.1, “mysqlbinlog Hex Dump
Format”. The hex output can be helpful for replication debugging.

• --host=host_name, -h host_name

Command-Line Format

--host=host_name

Type

Default Value

String

localhost

574

mysqlbinlog — Utility for Processing Binary Log Files

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
processing updates. This option may prove useful whenever it is desirable or necessary to replay
one or more binary logs to a MySQL Server which may not contain all of the data to which the logs
refer.

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

Type

Directory name

For data loading operations corresponding to LOAD DATA statements, mysqlbinlog extracts the
files from the binary log events, writes them as temporary files to the local file system, and writes
LOAD DATA LOCAL statements to cause the files to be loaded. By default, mysqlbinlog writes
these temporary files to an operating system-specific directory. The --local-load option can be
used to explicitly specify the directory where mysqlbinlog should prepare local temporary files.

Because other processes can write files to the default system-specific directory, it is advisable to
specify the --local-load option to mysqlbinlog to designate a different directory for data files,
and then designate that same directory by specifying the --load-data-local-dir option to
mysql when processing the output from mysqlbinlog. For example:

mysqlbinlog --local-load=/my/local/data ...
    | mysql --load-data-local-dir=/my/local/data ...

Important

These temporary files are not automatically removed by mysqlbinlog or
any other MySQL program.

• --login-path=name

Command-Line Format

--login-path=name

575

mysqlbinlog — Utility for Processing Binary Log Files

Type

String

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Command-Line Format

--no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-defaults

Command-Line Format

--no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option
file, --no-defaults can be used to prevent them from being read.

The exception is that the .mylogin.cnf file is read in all cases, if it exists. This permits
passwords to be specified in a safer way than on the command line even when --no-defaults
is used. To create .mylogin.cnf, use the mysql_config_editor utility. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --offset=N, -o N

Command-Line Format

Type

Skip the first N entries in the log.

• --open-files-limit=N

--offset=#

Numeric

Command-Line Format

--open-files-limit=#

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

576

mysqlbinlog — Utility for Processing Binary Log Files

Command-Line Format

--password[=password]

Type

String

The password of the MySQL account used for connecting to the server. The password value is
optional. If not given, mysqlbinlog prompts for one. If given, there must be no space between --
password= or -p and the password following it. If no password option is specified, the default is to
send no password.

Specifying a password on the command line should be considered insecure. To avoid giving the
password on the command line, use an option file. See Section 8.1.2.1, “End-User Guidelines for
Password Security”.

To explicitly specify that there is no password and that mysqlbinlog should not prompt for one, use
the --skip-password option.

• --plugin-dir=dir_name

Command-Line Format

--plugin-dir=dir_name

Type

Directory name

The directory in which to look for plugins. Specify this option if the --default-auth option is
used to specify an authentication plugin but mysqlbinlog does not find it. See Section 8.2.17,
“Pluggable Authentication”.

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

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --print-table-metadata

Command-Line Format

--print-table-metadata

Print table related metadata from the binary log. Configure the amount of table related metadata
binary logged using binlog-row-metadata.

577

• --protocol={TCP|SOCKET|PIPE|MEMORY}

Command-Line Format

Type

--protocol=type

String

mysqlbinlog — Utility for Processing Binary Log Files

Default Value

Valid Values

[see text]

TCP

SOCKET

PIPE

MEMORY

The transport protocol to use for connecting to the server. It is useful when the other connection
parameters normally result in use of a protocol other than the one you want. For details on the
permissible values, see Section 6.2.7, “Connection Transport Protocols”.

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
one output file for each file read from the server. The --raw option can be used to make a backup
of a server's binary log. With the --stop-never option, the backup is “live” because mysqlbinlog
stays connected to the server. By default, output files are written in the current directory with the
same names as the original log files. Output file names can be modified using the --result-file
option. For more information, see Section 6.6.9.3, “Using mysqlbinlog to Back Up Binary Log Files”.

• --read-from-remote-source=type

Command-Line Format

--read-from-remote-source=type

This option reads binary logs from a MySQL server with the COM_BINLOG_DUMP or
COM_BINLOG_DUMP_GTID commands by setting the option value to either BINLOG-DUMP-NON-
GTIDS or BINLOG-DUMP-GTIDS, respectively. If --read-from-remote-source=BINLOG-
DUMP-GTIDS is combined with --exclude-gtids, transactions can be filtered out on the source,
avoiding unnecessary network traffic.

The connection parameter options are used with these options or the --read-from-remote-
server option. These options are --host, --password, --port, --protocol, --socket, and
--user. If none of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use these options.

• --read-from-remote-master=type

Command-Line Format

Deprecated

--read-from-remote-master=type

Yes

Deprecated synonym for --read-from-remote-source.

• --read-from-remote-server=file_name, -R

Command-Line Format

--read-from-remote-server=file_name

578

mysqlbinlog — Utility for Processing Binary Log Files

Read the binary log from a MySQL server rather than reading a local log file. This option requires
that the remote server be running. It works only for binary log files on the remote server and not relay
log files. This accepts the binary log file name (including the numeric suffix) without the file path.

The connection parameter options are used with this option or the --read-from-remote-source
option. These options are --host, --password, --port, --protocol, --socket, and --user.
If neither of the remote options is specified, the connection parameter options are ignored.

The REPLICATION SLAVE privilege is required to use this option.

This option is like --read-from-remote-source=BINLOG-DUMP-NON-GTIDS.

• --result-file=name, -r name

Command-Line Format

--result-file=name

Without the --raw option, this option indicates the file to which mysqlbinlog writes text output.
With --raw, mysqlbinlog writes one binary output file for each log file transferred from the server,
writing them by default in the current directory using the same names as the original log file. In this
case, the --result-file option value is treated as a prefix that modifies output file names.

• --require-row-format

Command-Line Format

--require-row-format

Type

Default Value

Boolean

false

Require row-based binary logging format for events. This option enforces row-based replication
events for mysqlbinlog output. The stream of events produced with this option would be
accepted by a replication channel that is secured using the REQUIRE_ROW_FORMAT option of
the CHANGE REPLICATION SOURCE TO statement. binlog_format=ROW must be set on the
server where the binary log was written. When you specify this option, mysqlbinlog stops with an
error message if it encounters any events that are disallowed under the REQUIRE_ROW_FORMAT
restrictions, including LOAD DATA INFILE instructions, creating or dropping temporary tables,
INTVAR, RAND, or USER_VAR events, and non-row-based events within a DML transaction.
mysqlbinlog also prints a SET @@session.require_row_format statement at the start
of its output to apply the restrictions when the output is executed, and does not print the SET
@@session.pseudo_thread_id statement.

• --rewrite-db='from_name->to_name'

Command-Line Format

--rewrite-db='oldname->newname'

Type

String

579

mysqlbinlog — Utility for Processing Binary Log Files

Default Value

[none]

When reading from a row-based or statement-based log, rewrite all occurrences of from_name
to to_name. Rewriting is done on the rows, for row-based logs, as well as on the USE clauses, for
statement-based logs.

Warning

Statements in which table names are qualified with database names are not
rewritten to use the new name when using this option.

The rewrite rule employed as a value for this option is a string having the form 'from_name-
>to_name', as shown previously, and for this reason must be enclosed by quotation marks.

To employ multiple rewrite rules, specify the option multiple times, as shown here:

mysqlbinlog --rewrite-db='dbcurrent->dbold' --rewrite-db='dbtest->dbcurrent' \
    binlog.00001 > /tmp/statements.sql

When used together with the --database option, the --rewrite-db option is applied first; then
--database option is applied, using the rewritten database name. The order in which the options
are provided makes no difference in this regard.

This means that, for example, if mysqlbinlog is started with --rewrite-db='mydb->yourdb'
--database=yourdb, then all updates to any tables in databases mydb and yourdb are included
in the output. On the other hand, if it is started with --rewrite-db='mydb->yourdb' --
database=mydb, then mysqlbinlog outputs no statements at all: since all updates to mydb are
first rewritten as updates to yourdb before applying the --database option, there remain no
updates that match --database=mydb.

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

This option is supported only by the version of mysqlbinlog supplied with the NDB Cluster
distribution, or built with NDB Cluster support.

580

• --server-public-key-path=file_name

Command-Line Format

--server-public-key-path=file_name

mysqlbinlog — Utility for Processing Binary Log Files

Type

File name

The path name to a file in PEM format containing a client-side copy of the public key required by the
server for RSA key pair-based password exchange. This option applies to clients that authenticate
with the sha256_password (deprecated) or caching_sha2_password authentication plugin. This
option is ignored for accounts that do not authenticate with one of those plugins. It is also ignored if
RSA-based password exchange is not used, as is the case when the client connects to the server
using a secure connection.

If --server-public-key-path=file_name is given and specifies a valid public key file, it takes
precedence over --get-server-public-key.

For sha256_password (deprecated), this option applies only if MySQL was built using OpenSSL.

For information about the sha256_password and caching_sha2_password plugins, see
Section 8.4.1.3, “SHA-256 Pluggable Authentication”, and Section 8.4.1.2, “Caching SHA-2
Pluggable Authentication”.

• --set-charset=charset_name

Command-Line Format

--set-charset=charset_name

Type

String

Add a SET NAMES charset_name statement to the output to specify the character set to be used
for processing log files.

• --shared-memory-base-name=name

Command-Line Format

Platform Specific

--shared-memory-base-name=name

Windows

On Windows, the shared-memory name to use for connections made using shared memory to a local
server. The default value is MYSQL. The shared-memory name is case-sensitive.

This option applies only if the server was started with the shared_memory system variable enabled
to support shared-memory connections.

• --short-form, -s

Command-Line Format

--short-form

Display only the statements contained in the log, without any extra information or row-based events.
This is for testing only, and should not be used in production systems. It is deprecated, and you
should expect it to be removed in a future release.

• --skip-gtids[=(true|false)]

Command-Line Format

--skip-gtids[=true|false]

Type

Default Value

Boolean

false

Do not include the GTIDs from the binary log files in the output dump file. For example:

mysqlbinlog --skip-gtids binlog.000001 >  /tmp/dump.sql

581

mysqlbinlog — Utility for Processing Binary Log Files

mysql -u root -p -e "source /tmp/dump.sql"

You should not normally use this option in production or in recovery, except in the specific, and rare,
scenarios where the GTIDs are actively unwanted. For example, an administrator might want to
duplicate selected transactions (such as table definitions) from a deployment to another, unrelated,
deployment that will not replicate to or from the original. In that scenario, --skip-gtids can be
used to enable the administrator to apply the transactions as if they were new, and ensure that
the deployments remain unrelated. However, you should only use this option if the inclusion of the
GTIDs causes a known issue for your use case.

• --socket=path, -S path

Command-Line Format

--socket={file_name|pipe_name}

Type

String

For connections to localhost, the Unix socket file to use, or, on Windows, the name of the named
pipe to use.

On Windows, this option applies only if the server was started with the named_pipe system variable
enabled to support named-pipe connections. In addition, the user making the connection must be
a member of the Windows group specified by the named_pipe_full_access_group system
variable.

• --ssl*

Options that begin with --ssl specify whether to connect to the server using encryption and indicate
where to find SSL keys and certificates. See Command Options for Encrypted Connections.

• --ssl-fips-mode={OFF|ON|STRICT}

Command-Line Format

--ssl-fips-mode={OFF|ON|STRICT}

Deprecated

Type

Default Value

Valid Values

Yes

Enumeration

OFF

OFF

ON

STRICT

Controls whether to enable FIPS mode on the client side. The --ssl-fips-mode option differs
from other --ssl-xxx options in that it is not used to establish encrypted connections, but rather to
affect which cryptographic operations to permit. See Section 8.8, “FIPS Support”.

These --ssl-fips-mode values are permitted:

• OFF: Disable FIPS mode.

• ON: Enable FIPS mode.

• STRICT: Enable “strict” FIPS mode.

Note

582

If the OpenSSL FIPS Object Module is not available, the only permitted value
for --ssl-fips-mode is OFF. In this case, setting --ssl-fips-mode to ON

mysqlbinlog — Utility for Processing Binary Log Files

or STRICT causes the client to produce a warning at startup and to operate in
non-FIPS mode.

This option is deprecated. Expect it to be removed in a future version of MySQL.

• --start-datetime=datetime

Command-Line Format

--start-datetime=datetime

Type

Datetime

Start reading the binary log at the first event having a timestamp equal to or later than the datetime
argument. The datetime value is relative to the local time zone on the machine where you run
mysqlbinlog. The value should be in a format accepted for the DATETIME or TIMESTAMP data
types. For example:

mysqlbinlog --start-datetime="2005-12-25 11:25:56" binlog.000003

This option is useful for point-in-time recovery. See Section 9.5, “Point-in-Time (Incremental)
Recovery”.

• --start-position=N, -j N

Command-Line Format

--start-position=#

Type

Numeric

Start decoding the binary log at the log position N, including in the output any events that begin at
position N or after. The position is a byte point in the log file, not an event counter; it needs to point
to the starting position of an event to generate useful output. This option applies to the first log file
named on the command line.

The maximum value supported for this option is 18446744073709551616 (264-1), unless --read-
from-remote-server or --read-from-remote-source is also used, in which case the
maximum is 4294967295.

This option is useful for point-in-time recovery. See Section 9.5, “Point-in-Time (Incremental)
Recovery”.

• --stop-datetime=datetime

Command-Line Format

--stop-datetime=datetime

Stop reading the binary log at the first event having a timestamp equal to or later than the datetime
argument. See the description of the --start-datetime option for information about the
datetime value.

This option is useful for point-in-time recovery. See Section 9.5, “Point-in-Time (Incremental)
Recovery”.

• --stop-never

Command-Line Format

Type

--stop-never

Boolean

583

mysqlbinlog — Utility for Processing Binary Log Files

Default Value

FALSE

This option is used with --read-from-remote-server. It tells mysqlbinlog to remain
connected to the server. Otherwise mysqlbinlog exits when the last log file has been transferred
from the server. --stop-never implies --to-last-log, so only the first log file to transfer need
be named on the command line.

--stop-never is commonly used with --raw to make a live binary log backup, but also can be
used without --raw to maintain a continuous text display of log events as the server generates
them.

With --stop-never, by default, mysqlbinlog reports a server ID of 1 when it connects to the
server. Use --connection-server-id to explicitly specify an alternative ID to report. It can
be used to avoid a conflict with the ID of a replica server or another mysqlbinlog process. See
Section 6.6.9.4, “Specifying the mysqlbinlog Server ID”.

• --stop-never-slave-server-id=id

Command-Line Format

--stop-never-slave-server-id=#

Type

Default Value

Minimum Value

Numeric

65535

1

This option is deprecated; expect it to be removed in a future release. Use the --connection-
server-id option instead to specify a server ID for mysqlbinlog to report.

• --stop-position=N

Command-Line Format

--stop-position=#

Type

Numeric

Stop decoding the binary log at the log position N, excluding from the output any events that begin at
position N or after. The position is a byte point in the log file, not an event counter; it needs to point to
a spot after the starting position of the last event you want to include in the output. The event starting
before position N and finishing at or after the position is the last event to be processed. This option
applies to the last log file named on the command line.

This option is useful for point-in-time recovery. See Section 9.5, “Point-in-Time (Incremental)
Recovery”.

• --tls-ciphersuites=ciphersuite_list

Command-Line Format

--tls-ciphersuites=ciphersuite_list

Type

String

The permissible ciphersuites for encrypted connections that use TLSv1.3. The value is a list of one
or more colon-separated ciphersuite names. The ciphersuites that can be named for this option
depend on the SSL library used to compile MySQL. For details, see Section 8.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

584

• --tls-sni-servername=server_name

Command-Line Format

--tls-sni-servername=server_name

mysqlbinlog — Utility for Processing Binary Log Files

Type

String

When specified, the name is passed to the libmysqlclient C API library using the
MYSQL_OPT_TLS_SNI_SERVERNAME option of mysql_options(). The server name is not case-
sensitive. To show which server name the client specified for the current session, if any, check the
Tls_sni_server_name status variable.

Server Name Indication (SNI) is an extension to the TLS protocol (OpenSSL must be compiled using
TLS extensions for this option to function). The MySQL implementation of SNI represents the client-
side only.

• --tls-version=protocol_list

Command-Line Format

--tls-version=protocol_list

Type

Default Value

String

TLSv1,TLSv1.1,TLSv1.2,TLSv1.3
(OpenSSL 1.1.1 or higher)

TLSv1,TLSv1.1,TLSv1.2 (otherwise)

The permissible TLS protocols for encrypted connections. The value is a list of one or more comma-
separated protocol names. The protocols that can be named for this option depend on the SSL
library used to compile MySQL. For details, see Section 8.3.2, “Encrypted Connection TLS Protocols
and Ciphers”.

• --to-last-log, -t

Command-Line Format

--to-last-log

Do not stop at the end of the requested binary log from a MySQL server, but rather continue printing
until the end of the last binary log. If you send the output to the same MySQL server, this may lead to
an endless loop. This option requires --read-from-remote-server.

• --user=user_name, -u user_name

Command-Line Format

--user=user_name,

Type

String

The user name of the MySQL account to use when connecting to a remote server.

If you are using the Rewriter plugin, you should grant this user the SKIP_QUERY_REWRITE
privilege.

• --verbose, -v

Command-Line Format

--verbose

Reconstruct row events and display them as commented SQL statements, with table partition
information where applicable. If this option is given twice (by passing in either "-vv" or "--verbose --
verbose"), the output includes comments to indicate column data types and some metadata, and

585

mysqlbinlog — Utility for Processing Binary Log Files

informational log events such as row query log events if the binlog_rows_query_log_events
system variable is set to TRUE.

For examples that show the effect of --base64-output and --verbose on row event output, see
Section 6.6.9.2, “mysqlbinlog Row Event Display”.

• --verify-binlog-checksum, -c

Command-Line Format

--verify-binlog-checksum

Verify checksums in binary log files.

• --version, -V

Command-Line Format

--version

Display version information and exit.

• --zstd-compression-level=level

Command-Line Format

--zstd-compression-level=#

Type

Integer

The compression level to use for connections to the server that use the zstd compression algorithm.
The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression.
The default zstd compression level is 3. The compression level setting has no effect on connections
that do not use zstd compression.

For more information, see Section 6.2.8, “Connection Compression Control”.

You can pipe the output of mysqlbinlog into the mysql client to execute the events contained in the
binary log. This technique is used to recover from an unexpected exit when you have an old backup
(see Section 9.5, “Point-in-Time (Incremental) Recovery”). For example:

mysqlbinlog binlog.000001 | mysql -u root -p

Or:

mysqlbinlog binlog.[0-9]* | mysql -u root -p

If the statements produced by mysqlbinlog may contain BLOB values, these may cause problems
when mysql processes them. In this case, invoke mysql with the --binary-mode option.

You can also redirect the output of mysqlbinlog to a text file instead, if you need to modify the
statement log first (for example, to remove statements that you do not want to execute for some
reason). After editing the file, execute the statements that it contains by using it as input to the mysql
program:

mysqlbinlog binlog.000001 > tmpfile
... edit tmpfile ...
mysql -u root -p < tmpfile

586

When mysqlbinlog is invoked with the --start-position option, it displays only those events
with an offset in the binary log greater than or equal to a given position (the given position must match
the start of one event). It also has options to stop and start when it sees an event with a given date and
time. This enables you to perform point-in-time recovery using the --stop-datetime option (to be
able to say, for example, “roll forward my databases to how they were today at 10:30 a.m.”).

mysqlbinlog — Utility for Processing Binary Log Files

Processing multiple files.
the safe method is to process them all using a single connection to the server. Here is an example that
demonstrates what may be unsafe:

 If you have more than one binary log to execute on the MySQL server,

mysqlbinlog binlog.000001 | mysql -u root -p # DANGER!!
mysqlbinlog binlog.000002 | mysql -u root -p # DANGER!!

Processing binary logs this way using multiple connections to the server causes problems if the first log
file contains a CREATE TEMPORARY TABLE statement and the second log contains a statement that
uses the temporary table. When the first mysql process terminates, the server drops the temporary
table. When the second mysql process attempts to use the table, the server reports “unknown table.”

To avoid problems like this, use a single mysql process to execute the contents of all binary logs that
you want to process. Here is one way to do so:

mysqlbinlog binlog.000001 binlog.000002 | mysql -u root -p

Another approach is to write all the logs to a single file and then process the file:

mysqlbinlog binlog.000001 >  /tmp/statements.sql
mysqlbinlog binlog.000002 >> /tmp/statements.sql
mysql -u root -p -e "source /tmp/statements.sql"

You can also supply multiple binary log files to mysqlbinlog as streamed input using a shell pipe. An
archive of compressed binary log files can be decompressed and provided directly to mysqlbinlog.
In this example, binlog-files_1.gz contains multiple binary log files for processing. The pipeline
extracts the contents of binlog-files_1.gz, pipes the binary log files to mysqlbinlog as standard
input, and pipes the output of mysqlbinlog into the mysql client for execution:

gzip -cd binlog-files_1.gz | ./mysqlbinlog - | ./mysql -uroot  -p

You can specify more than one archive file, for example:

gzip -cd binlog-files_1.gz binlog-files_2.gz | ./mysqlbinlog - | ./mysql -uroot  -p

For streamed input, do not use --stop-position, because mysqlbinlog cannot identify the last
log file to apply this option.

LOAD DATA operations.
operation without the original data file. mysqlbinlog copies the data to a temporary file and writes a
LOAD DATA LOCAL statement that refers to the file. The default location of the directory where these
files are written is system-specific. To specify a directory explicitly, use the --local-load option.

 mysqlbinlog can produce output that reproduces a LOAD DATA

Because mysqlbinlog converts LOAD DATA statements to LOAD DATA LOCAL statements (that
is, it adds LOCAL), both the client and the server that you use to process the statements must be
configured with the LOCAL capability enabled. See Section 8.1.6, “Security Considerations for LOAD
DATA LOCAL”.

Warning

The temporary files created for LOAD DATA LOCAL statements are not
automatically deleted because they are needed until you actually execute those
statements. You should delete the temporary files yourself after you no longer
need the statement log. The files can be found in the temporary file directory
and have names like original_file_name-#-#.

6.6.9.1 mysqlbinlog Hex Dump Format

The --hexdump option causes mysqlbinlog to produce a hex dump of the binary log contents:

mysqlbinlog --hexdump source-bin.000001

The hex output consists of comment lines beginning with #, so the output might look like this for the
preceding command:

587

mysqlbinlog — Utility for Processing Binary Log Files

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

Hex dump output currently contains the elements in the following list. This format is subject to change.
For more information about binary log format, see MySQL Internals: The Binary Log.

• Position: The byte position within the log file.

• Timestamp: The event timestamp. In the example shown, '9d fc 5c 43' is the representation of

'051024 17:24:13' in hexadecimal.

• Type: The event type code.

• Master ID: The server ID of the replication source server that created the event.

• Size: The size in bytes of the event.

• Master Pos: The position of the next event in the original source's binary log file.

• Flags: Event flag values.

6.6.9.2 mysqlbinlog Row Event Display

The following examples illustrate how mysqlbinlog displays row events that specify data
modifications. These correspond to events with the WRITE_ROWS_EVENT, UPDATE_ROWS_EVENT, and
DELETE_ROWS_EVENT type codes. The --base64-output=DECODE-ROWS and --verbose options
may be used to affect row event output.

Suppose that the server is using row-based binary logging and that you execute the following
sequence of statements:

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
Omitting extraneous lines, the output for the row events produced by the preceding statement
sequence looks like this:

$> mysqlbinlog log_file
...
# at 218
#080828 15:03:08 server id 1  end_log_pos 258   Write_rows: table id 17 flags: STMT_END_F

BINLOG '

588

mysqlbinlog — Utility for Processing Binary Log Files

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

To see the row events as comments in the form of “pseudo-SQL” statements, run mysqlbinlog with
the --verbose or -v option. This output level also shows table partition information where applicable.
The output contains lines beginning with ###:

$> mysqlbinlog -v log_file
...
# at 218
#080828 15:03:08 server id 1  end_log_pos 258   Write_rows: table id 17 flags: STMT_END_F

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

Specify --verbose or -v twice to also display data types and some metadata for each column, and
informational log events such as row query log events if the binlog_rows_query_log_events

589

mysqlbinlog — Utility for Processing Binary Log Files

system variable is set to TRUE. The output contains an additional comment following each column
change:

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

You can tell mysqlbinlog to suppress the BINLOG statements for row events by using the --
base64-output=DECODE-ROWS option. This is similar to --base64-output=NEVER but does not
exit with an error if a row event is found. The combination of --base64-output=DECODE-ROWS and
--verbose provides a convenient way to see row events only as SQL statements:

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

590

mysqlbinlog — Utility for Processing Binary Log Files

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

• The original column names are lost and replaced by @N, where N is a column number.

• Character set information is not available in the binary log, which affects string column display:

• There is no distinction made between corresponding binary and nonbinary string types (BINARY
and CHAR, VARBINARY and VARCHAR, BLOB and TEXT). The output uses a data type of STRING
for fixed-length strings and VARSTRING for variable-length strings.

• For multibyte character sets, the maximum number of bytes per character is not present in the
binary log, so the length for string types is displayed in bytes rather than in characters. For
example, STRING(4) is used as the data type for values from either of these column types:

CHAR(4) CHARACTER SET latin1
CHAR(2) CHARACTER SET ucs2

• Due to the storage format for events of type UPDATE_ROWS_EVENT, UPDATE statements are

displayed with the WHERE clause preceding the SET clause.

Proper interpretation of row events requires the information from the format description event at the
beginning of the binary log. Because mysqlbinlog does not know in advance whether the rest of the
log contains row events, by default it displays the format description event using a BINLOG statement
in the initial part of the output.

If the binary log is known not to contain any events requiring a BINLOG statement (that is, no row
events), the --base64-output=NEVER option can be used to prevent this header from being written.

6.6.9.3 Using mysqlbinlog to Back Up Binary Log Files

By default, mysqlbinlog reads binary log files and displays their contents in text format. This enables
you to examine events within the files more easily and to re-execute them (for example, by using the
output as input to mysql). mysqlbinlog can read log files directly from the local file system, or, with
the --read-from-remote-server option, it can connect to a server and request binary log contents
from that server. mysqlbinlog writes text output to its standard output, or to the file named as the
value of the --result-file=file_name option if that option is given.

• mysqlbinlog Backup Capabilities

• mysqlbinlog Backup Options

• Static and Live Backups

• Output File Naming

591

mysqlbinlog — Utility for Processing Binary Log Files

• Example: mysqldump + mysqlbinlog for Backup and Restore

• mysqlbinlog Backup Restrictions

mysqlbinlog Backup Capabilities

mysqlbinlog can read binary log files and write new files containing the same content—that is,
in binary format rather than text format. This capability enables you to easily back up a binary log
in its original format. mysqlbinlog can make a static backup, backing up a set of log files and
stopping when the end of the last file is reached. It can also make a continuous (“live”) backup, staying
connected to the server when it reaches the end of the last log file and continuing to copy new events
as they are generated. In continuous-backup operation, mysqlbinlog runs until the connection ends
(for example, when the server exits) or mysqlbinlog is forcibly terminated. When the connection
ends, mysqlbinlog does not wait and retry the connection, unlike a replica server. To continue a live
backup after the server has been restarted, you must also restart mysqlbinlog.

Important

mysqlbinlog can back up both encrypted and unencrypted binary log
files . However, copies of encrypted binary log files that are generated using
mysqlbinlog are stored in an unencrypted format.

mysqlbinlog Backup Options

Binary log backup requires that you invoke mysqlbinlog with two options at minimum:

• The --read-from-remote-server (or -R) option tells mysqlbinlog to connect to a server and
request its binary log. (This is similar to a replica server connecting to its replication source server.)

• The --raw option tells mysqlbinlog to write raw (binary) output, not text output.

Along with --read-from-remote-server, it is common to specify other options: --host indicates
where the server is running, and you may also need to specify connection options such as --user and
--password.

Several other options are useful in conjunction with --raw:

• --stop-never: Stay connected to the server after reaching the end of the last log file and continue

to read new events.

• --connection-server-id=id: The server ID that mysqlbinlog reports when it connects to a
server. When --stop-never is used, the default reported server ID is 1. If this causes a conflict
with the ID of a replica server or another mysqlbinlog process, use --connection-server-id
to specify an alternative server ID. See Section 6.6.9.4, “Specifying the mysqlbinlog Server ID”.

• --result-file: A prefix for output file names, as described later.

Static and Live Backups

To back up a server's binary log files with mysqlbinlog, you must specify file names that actually
exist on the server. If you do not know the names, connect to the server and use the SHOW BINARY
LOGS statement to see the current names. Suppose that the statement produces this output:

mysql> SHOW BINARY LOGS;
+---------------+-----------+-----------+
| Log_name      | File_size | Encrypted |
+---------------+-----------+-----------+
| binlog.000130 |     27459 | No        |
| binlog.000131 |     13719 | No        |
| binlog.000132 |     43268 | No        |
+---------------+-----------+-----------+

With that information, you can use mysqlbinlog to back up the binary log to the current directory as
follows (enter each command on a single line):

592

mysqlbinlog — Utility for Processing Binary Log Files

• To make a static backup of binlog.000130 through binlog.000132, use either of these

commands:

mysqlbinlog --read-from-remote-server --host=host_name --raw
  binlog.000130 binlog.000131 binlog.000132

mysqlbinlog --read-from-remote-server --host=host_name --raw
  --to-last-log binlog.000130

The first command specifies every file name explicitly. The second names only the first file and uses
--to-last-log to read through the last. A difference between these commands is that if the server
happens to open binlog.000133 before mysqlbinlog reaches the end of binlog.000132, the
first command does not read it, but the second command does.

• To make a live backup in which mysqlbinlog starts with binlog.000130 to copy existing log

files, then stays connected to copy new events as the server generates them:

mysqlbinlog --read-from-remote-server --host=host_name --raw
  --stop-never binlog.000130

With --stop-never, it is not necessary to specify --to-last-log to read to the last log file
because that option is implied.

Output File Naming

Without --raw, mysqlbinlog produces text output and the --result-file option, if given,
specifies the name of the single file to which all output is written. With --raw, mysqlbinlog writes
one binary output file for each log file transferred from the server. By default, mysqlbinlog writes
the files in the current directory with the same names as the original log files. To modify the output file
names, use the --result-file option. In conjunction with --raw, the --result-file option value
is treated as a prefix that modifies the output file names.

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

The following example describes a simple scenario that shows how to use mysqldump and
mysqlbinlog together to back up a server's data and binary log, and how to use the backup to
restore the server if data loss occurs. The example assumes that the server is running on host
host_name and its first binary log file is named binlog.000999. Enter each command on a single
line.

Use mysqlbinlog to make a continuous backup of the binary log:

mysqlbinlog --read-from-remote-server --host=host_name --raw
  --stop-never binlog.000999

Use mysqldump to create a dump file as a snapshot of the server's data. Use --all-databases, --
events, and --routines to back up all data, and --source-data=2 to include the current binary
log coordinates in the dump file.

mysqldump --host=host_name --all-databases --events --routines --source-data=2> dump_file

Execute the mysqldump command periodically to create newer snapshots as desired.

593

mysqldumpslow — Summarize Slow Query Log Files

If data loss occurs (for example, if the server unexpectedly exits), use the most recent dump file to
restore the data:

mysql --host=host_name -u root -p < dump_file

Then use the binary log backup to re-execute events that were written after the coordinates listed in the
dump file. Suppose that the coordinates in the file look like this:

-- CHANGE REPLICATION SOURCE TO SOURCE_LOG_FILE='binlog.001002', SOURCE_LOG_POS=27284;

If the most recent backed-up log file is named binlog.001004, re-execute the log events like this:

mysqlbinlog --start-position=27284 binlog.001002 binlog.001003 binlog.001004
  | mysql --host=host_name -u root -p

You might find it easier to copy the backup files (dump file and binary log files) to the server host to
make it easier to perform the restore operation, or if MySQL does not allow remote root access.

mysqlbinlog Backup Restrictions

Binary log backups with mysqlbinlog are subject to these restrictions:

• mysqlbinlog does not automatically reconnect to the MySQL server if the connection is lost (for

example, if a server restart occurs or there is a network outage).

• The delay for a backup is similar to the delay for a replica server.

6.6.9.4 Specifying the mysqlbinlog Server ID

When invoked with the --read-from-remote-server option, mysqlbinlog connects to a MySQL
server, specifies a server ID to identify itself, and requests binary log files from the server. You can use
mysqlbinlog to request log files from a server in several ways:

• Specify an explicitly named set of files: For each file, mysqlbinlog connects and issues a Binlog

dump command. The server sends the file and disconnects. There is one connection per file.

• Specify the beginning file and --to-last-log: mysqlbinlog connects and issues a Binlog

dump command for all files. The server sends all files and disconnects.

• Specify the beginning file and --stop-never (which implies --to-last-log): mysqlbinlog

connects and issues a Binlog dump command for all files. The server sends all files, but does not
disconnect after sending the last one.

With --read-from-remote-server only, mysqlbinlog connects using a server ID of 0, which
tells the server to disconnect after sending the last requested log file.

With --read-from-remote-server and --stop-never, mysqlbinlog connects using a nonzero
server ID, so the server does not disconnect after sending the last log file. The server ID is 1 by default,
but this can be changed with --connection-server-id.

Thus, for the first two ways of requesting files, the server disconnects because mysqlbinlog specifies
a server ID of 0. It does not disconnect if --stop-never is given because mysqlbinlog specifies a
nonzero server ID.

6.6.10 mysqldumpslow — Summarize Slow Query Log Files

The MySQL slow query log contains information about queries that take a long time to execute (see
Section 7.4.5, “The Slow Query Log”). mysqldumpslow parses MySQL slow query log files and
summarizes their contents.

Normally, mysqldumpslow groups queries that are similar except for the particular values of number
and string data values. It “abstracts” these values to N and 'S' when displaying summary output. To
modify value abstracting behavior, use the -a and -n options.

594

mysqldumpslow — Summarize Slow Query Log Files

Invoke mysqldumpslow like this:

mysqldumpslow [options] [log_file ...]

Example output with no options given:

Reading mysql slow query log from /usr/local/mysql/data/mysqld84-slow.log
Count: 1  Time=4.32s (4s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1

Count: 3  Time=2.53s (7s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1 limit N

Count: 3  Time=2.13s (6s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t1 select * from t1

mysqldumpslow supports the following options.

Table 6.21 mysqldumpslow Options

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

This option is available only if MySQL was built using WITH_DEBUG. MySQL release binaries
provided by Oracle are not built using this option.

• -g pattern

Type

String

595

mysqldumpslow — Summarize Slow Query Log Files

Consider only queries that match the (grep-style) pattern.

• -h host_name

Type

Default Value

String

*

Host name of MySQL server for *-slow.log file name. The value can contain a wildcard. The
default is * (match all).

• -i name

Type

String

Name of server instance (if using mysql.server startup script).

• -l

Do not subtract lock time from total time.

• -n N

Type

Numeric

Abstract numbers with at least N digits within names.

• -r

Reverse the sort order.

• -s sort_type

Type

Default Value

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

Display only the first N queries in the output.

• --verbose, -v

596

Program Development Utilities

Command-Line Format

--verbose

Verbose mode. Print more information about what the program does.

6.7 Program Development Utilities

This section describes some utilities that you may find useful when developing MySQL programs.

In shell scripts, you can use the my_print_defaults program to parse option files and see
what options would be used by a given program. The following example shows the output that
my_print_defaults might produce when asked to show the options found in the [client] and
[mysql] groups:

$> my_print_defaults client mysql
--port=3306
--socket=/tmp/mysql.sock
--no-auto-rehash

Note for developers: Option file handling is implemented in the C client library simply by processing
all options in the appropriate group or groups before any command-line arguments. This works well
for programs that use the last instance of an option that is specified multiple times. If you have a C or
C++ program that handles multiply specified options this way but that doesn't read option files, you
need add only two lines to give it that capability. Check the source code of any of the standard MySQL
clients to see how to do this.

Several other language interfaces to MySQL are based on the C client library, and some of them
provide a way to access option file contents. These include Perl and Python. For details, see the
documentation for your preferred interface.

6.7.1 mysql_config — Display Options for Compiling Clients

mysql_config provides you with useful information for compiling your MySQL client and connecting it
to MySQL. It is a shell script, so it is available only on Unix and Unix-like systems.

Note

pkg-config can be used as an alternative to mysql_config for obtaining
information such as compiler flags or link libraries required to compile MySQL
applications. For more information, see Building C API Client Programs Using
pkg-config.

mysql_config supports the following options.

• --cflags

C Compiler flags to find include files and critical compiler flags and defines used when compiling the
libmysqlclient library. The options returned are tied to the specific compiler that was used when
the library was created and might clash with the settings for your own compiler. Use --include for
more portable options that contain only include paths.

• --cxxflags

Like --cflags, but for C++ compiler flags.

• --include

Compiler options to find MySQL include files.

• --libs

Libraries and options required to link with the MySQL client library.

597

my_print_defaults — Display Options from Option Files

• --libs_r

Libraries and options required to link with the thread-safe MySQL client library. In MySQL 8.4, all
client libraries are thread-safe, so this option need not be used. The --libs option can be used in
all cases.

• --plugindir

The default plugin directory path name, defined when configuring MySQL.

• --port

The default TCP/IP port number, defined when configuring MySQL.

• --socket

The default Unix socket file, defined when configuring MySQL.

• --variable=var_name

Display the value of the named configuration variable. Permitted var_name values are
pkgincludedir (the header file directory), pkglibdir (the library directory), and plugindir (the
plugin directory).

• --version

Version number for the MySQL distribution.

If you invoke mysql_config with no options, it displays a list of all options that it supports, and their
values:

$> mysql_config
Usage: ./mysql_config [OPTIONS]
Compiler: GNU 10.4.0

Options:
  --cflags         [-I/usr/local/mysql/include/mysql]
  --cxxflags       [-I/usr/local/mysql/include/mysql]
  --include        [-I/usr/local/mysql/include/mysql]
  --libs           [-L/usr/local/mysql/lib/mysql -lmysqlclient -lpthread -ldl
                    -lssl  -lcrypto -lresolv -lm -lrt]
  --libs_r         [-L/usr/local/mysql/lib/mysql -lmysqlclient -lpthread -ldl
                    -lssl  -lcrypto -lresolv -lm -lrt]
  --plugindir      [/usr/local/mysql/lib/plugin]
  --socket         [/tmp/mysql.sock]
  --port           [3306]
  --version        [8.4.0]
  --variable=VAR   VAR is one of:
          pkgincludedir [/usr/local/mysql/include]
          pkglibdir     [/usr/local/mysql/lib]
          plugindir     [/usr/local/mysql/lib/plugin]

You can use mysql_config within a command line using backticks to include the output that it
produces for particular options. For example, to compile and link a MySQL client program, use
mysql_config as follows:

gcc -c `mysql_config --cflags` progname.c
gcc -o progname progname.o `mysql_config --libs`

6.7.2 my_print_defaults — Display Options from Option Files

my_print_defaults displays the options that are present in option groups of option files. The output
indicates what options are used by programs that read the specified option groups. For example, the
mysqlcheck program reads the [mysqlcheck] and [client] option groups. To see what options
are present in those groups in the standard option files, invoke my_print_defaults like this:

598

my_print_defaults — Display Options from Option Files

$> my_print_defaults mysqlcheck client
--user=myusername
--password=password
--host=localhost

The output consists of options, one per line, in the form that they would be specified on the command
line.

my_print_defaults supports the following options.

• --help, -?

Display a help message and exit.

• --config-file=file_name, --defaults-file=file_name, -c file_name

Read only the given option file.

• --debug=debug_options, -# debug_options

Write a debugging log. A typical debug_options string is d:t:o,file_name. The default is
d:t:o,/tmp/my_print_defaults.trace.

• --defaults-extra-file=file_name, --extra-file=file_name, -e file_name

Read this option file after the global option file but (on Unix) before the user option file.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --defaults-group-suffix=suffix, -g suffix

In addition to the groups named on the command line, read groups that have the given suffix.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --login-path=name, -l name

Read options from the named login path in the .mylogin.cnf login path file. A “login path” is an
option group containing options that specify which MySQL server to connect to and which account to
authenticate as. To create or modify a login path file, use the mysql_config_editor utility. See
Section 6.6.7, “mysql_config_editor — MySQL Configuration Utility”.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-login-paths

Skips reading options from the login path file.

See --login-path for related information.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --no-defaults, -n

Return an empty string.

For additional information about this and other option-file options, see Section 6.2.2.3, “Command-
Line Options that Affect Option-File Handling”.

• --show, -s

599

Miscellaneous Programs

my_print_defaults masks passwords by default. Use this option to display passwords as
cleartext.

• --verbose, -v

Verbose mode. Print more information about what the program does.

• --version, -V

Display version information and exit.

6.8 Miscellaneous Programs

6.8.1 perror — Display MySQL Error Message Information

perror displays the error message for MySQL or operating system error codes. Invoke perror like
this:

perror [options] errorcode ...

perror attempts to be flexible in understanding its arguments. For example, for the
ER_WRONG_VALUE_FOR_VAR error, perror understands any of these arguments: 1231, 001231,
MY-1231, or MY-001231, or ER_WRONG_VALUE_FOR_VAR.

$> perror 1231
MySQL error code MY-001231 (ER_WRONG_VALUE_FOR_VAR): Variable '%-.64s'
can't be set to the value of '%-.200s'

If an error number is in the range where MySQL and operating system errors overlap, perror displays
both error messages:

$> perror 1 13
OS error code   1:  Operation not permitted
MySQL error code MY-000001: Can't create/write to file '%s' (OS errno %d - %s)
OS error code  13:  Permission denied
MySQL error code MY-000013: Can't get stat of '%s' (OS errno %d - %s)

To obtain the error message for a MySQL Cluster error code, use the ndb_perror utility.

The meaning of system error messages may be dependent on your operating system. A given error
code may mean different things on different operating systems.

perror supports the following options.

• --help, --info, -I, -?

Display a help message and exit.

• --silent, -s

Silent mode. Print only the error message.

• --verbose, -v

Verbose mode. Print error code and message. This is the default behavior.

• --version, -V

Display version information and exit.

6.9 Environment Variables

600

Environment Variables

This section lists environment variables that are used directly or indirectly by MySQL. Most of these
can also be found in other places in this manual.

Options on the command line take precedence over values specified in option files and environment
variables, and values in option files take precedence over values in environment variables. In many
cases, it is preferable to use an option file instead of environment variables to modify the behavior of
MySQL. See Section 6.2.2.2, “Using Option Files”.

Variable

Description

AUTHENTICATION_KERBEROS_CLIENT_LOG

Kerberos authentication logging level.

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

MYSQL_PS1

MYSQL_PWD

MYSQL_TCP_PORT

MYSQL_TEST_LOGIN_FILE

MYSQL_TEST_TRACE_CRASH

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
plugin; see Section 8.4.1.4, “Client-Side Cleartext
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
not log to $HOME/.mysql_history, or syslog
if --syslog is given.

The path to the directory in which the server-
specific my.cnf file resides.

The default host name used by the mysql
command-line client.

The command prompt to use in the mysql
command-line client.

The default password when connecting to
mysqld. Using this is insecure. See note following
table.

The default TCP/IP port number.

The name of the .mylogin.cnf login path file.

Whether the test protocol trace plugin crashes
clients. See note following table.

601

Environment Variables

Variable

MYSQL_TEST_TRACE_DEBUG

MYSQL_UNIX_PORT

MYSQLX_TCP_PORT

MYSQLX_UNIX_PORT

NOTIFY_SOCKET

PATH

PKG_CONFIG_PATH

TMPDIR

TZ

UMASK

UMASK_DIR

USER

Description

Whether the test protocol trace plugin produces
output. See note following table.

The default Unix socket file name; used for
connections to localhost.

The X Plugin default TCP/IP port number.

The X Plugin default Unix socket file name; used
for connections to localhost.

Socket used by mysqld to communicate with
systemd.

Used by the shell to find MySQL programs.

Location of mysqlclient.pc pkg-config file.
See note following table.

The directory in which temporary files are created.

This should be set to your local time zone. See
Section B.3.3.7, “Time Zone Problems”.

The user-file creation mode when creating files.
See note following table.

The user-directory creation mode when creating
directories. See note following table.

The default user name on Windows when
connecting to mysqld.

For information about the mysql history file, see Section 6.5.1.3, “mysql Client Logging”.

Use of MYSQL_PWD to specify a MySQL password must be considered extremely insecure and should
not be used. Some versions of ps include an option to display the environment of running processes.
On some systems, if you set MYSQL_PWD, your password is exposed to any other user who runs ps.
Even on systems without such a version of ps, it is unwise to assume that there are no other methods
by which users can examine process environments.

MYSQL_PWD is deprecated as of MySQL 8.4; expect it to be removed in a future version of MySQL.

MYSQL_TEST_LOGIN_FILE is the path name of the login path file (the file created by
mysql_config_editor). If not set, the default value is %APPDATA%\MySQL\.mylogin.cnf
directory on Windows and $HOME/.mylogin.cnf on non-Windows systems. See Section 6.6.7,
“mysql_config_editor — MySQL Configuration Utility”.

The MYSQL_TEST_TRACE_DEBUG and MYSQL_TEST_TRACE_CRASH variables control the test protocol
trace client plugin, if MySQL is built with that plugin enabled. For more information, see Using the Test
Protocol Trace Plugin.

The default UMASK and UMASK_DIR values are 0640 and 0750, respectively. MySQL assumes that the
value for UMASK or UMASK_DIR is in octal if it starts with a zero. For example, setting UMASK=0600 is
equivalent to UMASK=384 because 0600 octal is 384 decimal.

The UMASK and UMASK_DIR variables, despite their names, are used as modes, not masks:

• If UMASK is set, mysqld uses ($UMASK | 0600) as the mode for file creation, so that newly

created files have a mode in the range from 0600 to 0666 (all values octal).

• If UMASK_DIR is set, mysqld uses ($UMASK_DIR | 0700) as the base mode for directory

creation, which then is AND-ed with ~(~$UMASK & 0666), so that newly created directories have
a mode in the range from 0700 to 0777 (all values octal). The AND operation may remove read and
write permissions from the directory mode, but not execute permissions.

602

Unix Signal Handling in MySQL

See also Section B.3.3.1, “Problems with File Permissions”.

It may be necessary to set PKG_CONFIG_PATH if you use pkg-config for building MySQL programs.
See Building C API Client Programs Using pkg-config.

6.10 Unix Signal Handling in MySQL

On Unix and Unix-like systems, a process can be the recipient of signals sent to it by the root system
account or the system account that owns the process. Signals can be sent using the kill command.
Some command interpreters associate certain key sequences with signals, such as Control+C to
send a SIGINT signal. This section describes how the MySQL server and client programs respond to
signals.

• Server Response to Signals

• Client Response to Signals

Server Response to Signals

mysqld responds to signals as follows:

• SIGTERM causes the server to shut down. This is like executing a SHUTDOWN statement without
having to connect to the server (which for shutdown requires an account that has the SHUTDOWN
privilege).

• SIGHUP causes the server to reload the grant tables and to flush tables, logs, the thread cache, and
the host cache. These actions are like various forms of the FLUSH statement. Sending the signal
enables the flush operations to be performed without having to connect to the server, which requires
a MySQL account that has privileges sufficient for those operations.

• SIGUSR1 causes the server to flush the error log, general query log, and slow query log. One use
for SIGUSR1 is to implement log rotation without having to connect to the server, which requires a
MySQL account that has privileges sufficient for those operations. For information about log rotation,
see Section 7.4.6, “Server Log Maintenance”.

The server response to SIGUSR1 is a subset of the response to SIGHUP, enabling SIGUSR1 to be
used as a more “lightweight” signal that flushes certain logs without the other SIGHUP effects such
as flushing the thread and host caches and writing a status report to the error log.

• SIGINT normally is ignored by the server. Starting the server with the --gdb option installs an

interrupt handler for SIGINT for debugging purposes. See Section 7.9.1.4, “Debugging mysqld under
gdb”.

Client Response to Signals

MySQL client programs respond to signals as follows:

• The mysql client interprets SIGINT (typically the result of typing Control+C) as instruction to
interrupt the current statement if there is one, or to cancel any partial input line otherwise. This
behavior can be disabled using the --sigint-ignore option to ignore SIGINT signals.

• Client programs that use the MySQL client library block SIGPIPE signals by default. These

variations are possible:

• Client can install their own SIGPIPE handler to override the default behavior. See Writing C API

Threaded Client Programs.

• Clients can prevent installation of SIGPIPE handlers by specifying the

CLIENT_IGNORE_SIGPIPE option to mysql_real_connect() at connect time. See
mysql_real_connect().

603

604

