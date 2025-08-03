Key Concepts

X DevAPI. X DevAPI offers a modern programming interface with a simple yet powerful design which
provides support for established industry standard concepts. See X DevAPI User Guide for in-depth
tutorials on using X DevAPI.

• The following MySQL products support the X Protocol and enable you to use X DevAPI in your chosen
language to develop applications that communicate with a MySQL Server functioning as a document
store.

• MySQL Shell provides implementations of X DevAPI in JavaScript and Python.

• Connector/C++

• Connector/J

• Connector/Node.js

• Connector/NET

• Connector/Python

19.1 Key Concepts

This section explains the concepts introduced as part of using MySQL as a document store.

Document

A Document is a set of key and value pairs, as represented by a JSON object. A Document is represented
internally using the MySQL binary JSON object, through the JSON MySQL datatype. The values of fields
can contain other documents, arrays, and lists of documents.

{
    "GNP": 4834,
    "_id": "00005de917d80000000000000023",
    "Code": "BWA",
    "Name": "Botswana",
    "IndepYear": 1966,
    "geography": {
        "Region": "Southern Africa",
        "Continent": "Africa",
        "SurfaceArea": 581730
    },
    "government": {
        "HeadOfState": "Festus G. Mogae",
        "GovernmentForm": "Republic"
    },
    "demographics": {
        "Population": 1622000,
        "LifeExpectancy": 39.29999923706055
    }
}

Collection

A Collection is a container that may be used to store Documents in a MySQL database.

CRUD Operations

Create, Read, Update and Delete (CRUD) operations are the four basic operations that can be performed
on a database Collection or Table. In terms of MySQL this means:

3254

X Plugin

• Create a new entry (insertion or addition)

• Read entries (queries)

• Update entries

• Delete entries

X Plugin

The MySQL Server plugin which enables communication using X Protocol. Supports clients that implement
X DevAPI and enables you to use MySQL as a document store.

X Protocol

A protocol to communicate with a MySQL Server running X Plugin. X Protocol supports both CRUD and
SQL operations, authentication via SASL, allows streaming (pipelining) of commands and is extensible on
the protocol and the message layer.

19.2 Setting Up MySQL as a Document Store

To use MySQL 5.7 as a document store, the X Plugin needs to be installed. Then you can use X Protocol
to communicate with the server. Without the X Plugin running, X Protocol clients cannot connect to the
server. The X Plugin is supplied with MySQL (5.7.12 or higher) — installing it does not involve a separate
download. This section describes how to install X Plugin.

Follow the steps outlined here:

1.

Install or upgrade to MySQL 5.7.12 or higher.

When the installation or upgrade is done, start the server. For server startup instructions, see
Section 2.9.2, “Starting the Server”.

Note

MySQL Installer enables you to perform this and the next step (Install the X
Plugin) at the same time for new installations on Microsoft Windows. In the
Plugin and Extensions screen, check mark the Enable X Protocol/MySQL as
a Document Store check box. After the installation, verify that the X Plugin has
been installed.

2.

Install the X Plugin. A non-root account can be used to install the plugin as long as the account has
INSERT privilege for the mysql.plugin table.

Always save your existing configuration settings before reconfiguring the server.

To install the built-in X Plugin, do one of the following:

• Using MySQL Installer for Windows:

a. Launch MySQL Installer for Windows. MySQL Installer dashboard opens.

b. Click the Reconfigure quick action for MySQL Server. Use Next and Back to configure the

following items:

• In Accounts and Roles, confirm the current root account password.

3255

mysqlxsys@localhost User Account

3. Verify that the X Plugin has been installed.

When the X Plugin is installed properly, it shows up in the list when you query for active plugins on the
server with one of the following commands:

• MySQL Shell command:

mysqlsh -u user --sqlc -e "show plugins"

• MySQL Client program command:

mysql -u user -p -e "show plugins"

If you encounter problems with the X Plugin installation, or if you want to learn about alternative ways
of installing, configuring, or uninstalling server plugins, see Section 5.5.1, “Installing and Uninstalling
Plugins”.

mysqlxsys@localhost User Account

Installing the X Plugin creates a mysqlxsys@localhost user account. If, for some reason,
creating the user account fails, the X Plugin installation fails, too. Here is an explanation on what the
mysqlxsys@localhost user account is for and what to do when its creation fails.

The X Plugin installation process uses the MySQL root user to create an internal account for the
mysqlxsys@localhost user. The mysqlxsys@localhost account is used by the X Plugin for
authentication of external users against the MySQL account system and for killing sessions when
requested by a privileged user. The mysqlxsys@localhost account is created as locked, so it cannot be
used to log in by external users. If for some reason the MySQL root account is not available, before you
start the X Plugin installation you must manually create the mysqlxsys@localhost user by issuing the
following statements in the mysql command-line client:

CREATE USER IF NOT EXISTS mysqlxsys@localhost IDENTIFIED WITH
mysql_native_password AS 'password' ACCOUNT LOCK;
GRANT SELECT ON mysql.user TO mysqlxsys@localhost;
GRANT SUPER ON *.* TO mysqlxsys@localhost;

Uninstalling the X Plugin

If you ever want to uninstall (deactivate) the X Plugin, issue the following statement in the mysql
command-line client:

UNINSTALL PLUGIN mysqlx;

Do not use MySQL Shell to issue the previous statement. It works from MySQL Shell, but you get an error
(code 1130). Also, uninstalling the plugin removes the mysqlxsys user.

19.2.1 Installing MySQL Shell

This section describes how to download, install, and start MySQL Shell, which is an interactive JavaScript,
Python, or SQL interface supporting development and administration for the MySQL Server. MySQL Shell
is a component that you can install separately.

Requirements

MySQL Shell is available on Microsoft Windows, Linux, and macOS for 64-bit platforms. MySQL Shell
requires that the built-in X Plugin be active. You can install the server plugin before or after you install
MySQL Shell. For instructions, see Installing the X Plugin.

3257

Installing MySQL Shell

19.2.1.1 Installing MySQL Shell on Microsoft Windows

Important

The Community version of MySQL Shell requires the Visual C++ Redistributable for
Visual Studio 2013 (available at the Microsoft Download Center) to work; make sure
that is installed on your Windows system before installing MySQL Shell.

Note

MySQL Shell is currently not supplied with an MSI Installer. See Installing MySQL
Shell Binaries for the manual install procedure.

To install MySQL Shell on Microsoft Windows using the MSI Installer, do the following:

1. Download the Windows (x86, 64-bit), MSI Installer package from http://dev.mysql.com/downloads/

shell/.

2. When prompted, click Run.

3. Follow the steps in the Setup Wizard.

Figure 19.1 Installation of MySQL Shell on Windows

If you have installed MySQL without enabling the X Plugin, then later on decide you want to install the X
Plugin, or if you are installing MySQL without using MySQL Installer, see Installing the X Plugin.

Installing MySQL Shell Binaries

To install MySQL Shell binaries:

1. Unzip the content of the Zip file to the MySQL products directory, for example C:\Program Files

\MySQL\.

2. To be able to start MySQL Shell from a command prompt add the bin directory C:\Program Files
\MySQL\mysql-shell-1.0.8-rc-windows-x86-64bit\bin to the PATH system variable.

3258

Installing MySQL Shell

19.2.1.2 Installing MySQL Shell on Linux

Note

Installation packages for MySQL Shell are available only for a limited number of
Linux distributions, and only for 64-bit systems.

For supported Linux distributions, the easiest way to install MySQL Shell on Linux is to use the MySQL
APT repository or MySQL Yum repository. For systems not using the MySQL repositories, MySQL Shell
can also be downloaded and installed directly.

Installing MySQL Shell with the MySQL APT Repository

For Linux distributions supported by the MySQL APT repository, follow one of the paths below:

• If you do not yet have the MySQL APT repository as a software repository on your system, do the

following:

• Follow the steps given in Adding the MySQL APT Repository, paying special attention to the following:

• During the installation of the configuration package, when asked in the dialogue box to configure the
repository, make sure you choose MySQL 5.7 (which is the default option) as the release series you
want, and enable the MySQL Preview Packages component.

• Make sure you do not skip the step for updating package information for the MySQL APT repository:

sudo apt-get update

• Install MySQL Shell with this command:

sudo apt-get install mysql-shell

• If you already have the MySQL APT repository as a software repository on your system, do the following:

• Update package information for the MySQL APT repository:

sudo apt-get update

• Update the MySQL APT repository configuration package with the following command:

sudo apt-get install mysql-apt-config

When asked in the dialogue box to configure the repository, make sure you choose MySQL 5.7 (which
is the default option) as the release series you want, and enable the MySQL Preview Packages
component.

• Install MySQL Shell with this command:

sudo apt-get install mysql-shell

Installing MySQL Shell with the MySQL Yum Repository

For Linux distributions supported by the MySQL Yum repository, follow these steps to install MySQL Shell:

• Do one of the following:

• If you already have the MySQL Yum repository as a software repository on your system and the

repository was configured with the new release package mysql57-community-release, skip to the
next step (“Enable the MySQL Tools Preview subrepository...”).

3259

Installing MySQL Shell

• If you already have the MySQL Yum repository as a software repository on your system but have

configured the repository with the old release package mysql-community-release, it is easiest
to install MySQL Shell by first reconfiguring the MySQL Yum repository with the new mysql57-
community-release package. To do so, you need to remove your old release package first, with
the following command :

sudo yum remove mysql-community-release

For dnf-enabled systems, do this instead:

sudo dnf erase mysql-community-release

Then, follow the steps given in Adding the MySQL Yum Repository to install the new release package,
mysql57-community-release.

• If you do not yet have the MySQL Yum repository as a software repository on your system, follow the

steps given in Adding the MySQL Yum Repository.

• Enable the MySQL Tools Preview subrepository. You can do that by editing manually the /etc/

yum.repos.d/mysql-community.repo file. This is an example of the subrepository's default entry in
the file (the baseurl entry in your file might look different, depending on your Linux distribution):

[mysql-tools-preview]
name=MySQL Tools Preview
baseurl=http://repo.mysql.com/yum/mysql-tools-preview/el/6/$basearch/
enabled=0
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

Change the entry enabled=0 to enabled=1 to enable the subrepository.

• Install MySQL Shell with this command:

sudo yum install mysql-shell

For dnf-enabled systems, do this instead:

sudo dnf install mysql-shell

Installing MySQL Shell from Direct Downloads from the MySQL Developer Zone

RPM, Debian, and source packages for installing MySQL Shell are also available for download at
Download MySQL Shell.

19.2.1.3 Installing MySQL Shell on macOS

To install MySQL Shell on macOS, do the following:

1. Download the package from http://dev.mysql.com/downloads/shell/.

2. Double-click the downloaded DMG to mount it. Finder opens.

3. Double-click the .pkg file shown in the Finder window.

4. Follow the steps in the installation wizard.

3260

Starting MySQL Shell

Figure 19.2 Installation of MySQL Shell on macOS

5. When the installer finishes, eject the DMG. (It can be deleted.)

19.2.2 Starting MySQL Shell

You need an account name and password to establish a session using MySQL Shell. Replace user with
your account name.

On the same system where the server instance is running, open a terminal window (command prompt on
Windows) and start MySQL Shell with the following command:

mysqlsh --uri user@localhost

You are prompted to input your password and then this establishes an X Session.

For instructions to get you started using MySQL as a document store, see the following quick-start guides:

• Quick-Start Guide: MySQL Shell for JavaScript

• Quick-Start Guide: MySQL Shell for Python

19.3 Quick-Start Guide: MySQL for Visual Studio

This section explains how to use MySQL Shell to script a server using MySQL for Visual Studio.

Introduction

MySQL for Visual Studio provides access to MySQL objects and data without forcing developers to leave
Visual Studio. Designed and developed as a Visual Studio package, MySQL for Visual Studio integrates
directly into Server Explorer providing a seamless experience for setting up new connections and working
with database objects.

The following MySQL for Visual Studio features are available as of version 2.0.2:

• JavaScript and Python code editors, where scripts in those languages can be executed to query data

from a MySQL database.

3261

Getting Started

• Better integration with the Server Explorer to open MySQL, JavaScript, and Python code editors directly

from a connected MySQL instance.

• A newer user interface for displaying query results, where different views are presented from result sets

returned by a MySQL Server like:

• Multiple tabs for each result set returned by an executed query.

• Results view, where the information can be seen in grid, tree, or text representation for JSON results.

• Field types view, where information about the columns of a result set is shown, such as names, data

types, character sets, and more.

• Query statistics view, displaying information about the executed query such as execution times,

processed rows, index and temporary tables usage, and more.

• Execution plan view, displaying an explanation of the query execution done internally by the MySQL

Server.

Getting Started

The requirements are MySQL for Visual Studio 2.0.2 or higher, and Visual Studio 2010 or higher. X
DevAPI support requires MySQL Server 5.7.12 or higher with the X plugin enabled.

Opening a Code Editor

Before opening a code editor that can execute queries against a MySQL server, a connection needs to be
established:

1. Open the Server Explorer pane through the View menu, or with Control + W, K.

2. Right-click on the Data Connections node, select Add Connection....

3.

In the Add Connection dialog, make sure the MySQL Data Provider is being used and fill in all the
information.

Note

To enter the port number, click Advanced... and set the Port among the list of
connection properties.

4. Click Test Connection to ensure you have a valid connection, then click OK.

5. Right-click your newly created connection, select New MySQL Script and then the language for the

code editor you want to open.

For existing MySQL connections, to create a new editor you need only to do the last step.

Using the Code Editor

The MySQL script editors have a toolbar at the start where information about the session is displayed,
along with the actions that can be executed.

Note

Note the first two buttons in the toolbar represent a way to connect or disconnect
from a MySQL server. If the editor was opened from the Server Explorer, the
connection should be already established for the new editor window.

3262

X Plugin Options and Variables

The option value should be one of those available for plugin-loading options, as described in
Section 5.5.1, “Installing and Uninstalling Plugins”. For example, --mysqlx=FORCE_PLUS_PERMANENT
tells the server to load the plugin and prevent it from being removed while the server is running.

If X Plugin is enabled, it exposes several system variables that permit control over its operation:

• mysqlx_bind_address

Command-Line Format

--mysqlx-bind-address=addr

Introduced

System Variable

Scope

Dynamic

Type

Default Value

5.7.17

mysqlx_bind_address

Global

No

String

*

The network address on which X Plugin listens for TCP/IP connections. This variable is not dynamic and
can be configured only at startup. This is the X Plugin equivalent of the bind_address system variable;
see that variable description for more information.

mysqlx_bind_address accepts a single address value, which may specify a single non-wildcard IP
address or host name, or one of the wildcard address formats that permit listening on multiple network
interfaces (*, 0.0.0.0, or ::).

An IP address can be specified as an IPv4 or IPv6 address. If the value is a host name, X Plugin
resolves the name to an IP address and binds to that address. If a host name resolves to multiple IP
addresses, X Plugin uses the first IPv4 address if there are any, or the first IPv6 address otherwise.

X Plugin treats different types of addresses as follows:

• If the address is *, X Plugin accepts TCP/IP connections on all server host IPv4 interfaces, and, if

the server host supports IPv6, on all IPv6 interfaces. Use this address to permit both IPv4 and IPv6
connections for X Plugin. This value is the default.

• If the address is 0.0.0.0, X Plugin accepts TCP/IP connections on all server host IPv4 interfaces.

• If the address is ::, X Plugin accepts TCP/IP connections on all server host IPv4 and IPv6 interfaces.

• If the address is an IPv4-mapped address, X Plugin accepts TCP/IP connections for that address, in

either IPv4 or IPv6 format. For example, if X Plugin is bound to ::ffff:127.0.0.1, a client such as
MySQL Shell can connect using --host=127.0.0.1 or --host=::ffff:127.0.0.1.

• If the address is a “regular” IPv4 or IPv6 address (such as 127.0.0.1 or ::1), X Plugin accepts TCP/

IP connections only for that IPv4 or IPv6 address.

If binding to the address fails, X Plugin produces an error and the server does not load it.

• mysqlx_connect_timeout

Command-Line Format

--mysqlx-connect-timeout=#

Introduced

System Variable

5.7.12

mysqlx_connect_timeout

3267

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

X Plugin Options and Variables

Global

Yes

Integer

30

1

1000000000

seconds

The number of seconds X Plugin waits for the first packet to be received from newly connected clients.
This is the X Plugin equivalent of connect_timeout; see that variable description for more information.

• mysqlx_idle_worker_thread_timeout

Command-Line Format

--mysqlx-idle-worker-thread-timeout=#

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

5.7.12

mysqlx_idle_worker_thread_timeout

Global

Yes

Integer

60

0

3600

seconds

The number of seconds after which idle worker threads are terminated.

• mysqlx_max_allowed_packet

Command-Line Format

--mysqlx-max-allowed-packet=#

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

5.7.12

mysqlx_max_allowed_packet

Global

Yes

Integer

67108864

512

1073741824

bytes

The maximum size of network packets that can be received by X Plugin. This is the X Plugin equivalent
of max_allowed_packet; see that variable description for more information.

• mysqlx_max_connections

Command-Line Format

--mysqlx-max-connections=#

3268

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

X Plugin Options and Variables

5.7.12

mysqlx_max_connections

Global

Yes

Integer

100

1

65535

The maximum number of concurrent client connections X Plugin can accept. This is the X Plugin
equivalent of max_connections; see that variable description for more information.

For modifications to this variable, if the new value is smaller than the current number of connections, the
new limit is taken into account only for new connections.

• mysqlx_min_worker_threads

Command-Line Format

--mysqlx-min-worker-threads=#

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

5.7.12

mysqlx_min_worker_threads

Global

Yes

Integer

2

1

100

The minimum number of worker threads used by X Plugin for handling client requests.

• mysqlx_port

Command-Line Format

--mysqlx-port=port_num

Introduced

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

5.7.12

mysqlx_port

Global

No

Integer

33060

1

65535

The network port on which X Plugin listens for TCP/IP connections. This is the X Plugin equivalent of
port; see that variable description for more information.

3269

X Plugin Options and Variables

• mysqlx_ssl_cipher

Command-Line Format

--mysqlx-ssl-cipher=name

Introduced

System Variable

Scope

Dynamic

Type

Default Value

5.7.12

mysqlx_ssl_cipher

Global

No

String

NULL

The mysqlx_ssl_cipher system variable is like ssl_cipher, except that it applies to X Plugin rather
than the MySQL Server main connection interface. For information about configuring encryption support
for X Plugin, see Section 19.4.1, “Using Encrypted Connections with X Plugin”.

• mysqlx_ssl_crl

Command-Line Format

--mysqlx-ssl-crl=file_name

Introduced

System Variable

Scope

Dynamic

Type

Default Value

5.7.12

mysqlx_ssl_crl

Global

No

File name

NULL

The mysqlx_ssl_crl system variable is like ssl_crl, except that it applies to X Plugin rather than
the MySQL Server main connection interface. For information about configuring encryption support for X
Plugin, see Section 19.4.1, “Using Encrypted Connections with X Plugin”.

• mysqlx_ssl_crlpath

Command-Line Format

--mysqlx-ssl-crlpath=dir_name

Introduced

System Variable

Scope

Dynamic

Type

Default Value

5.7.12

mysqlx_ssl_crlpath

Global

No

Directory name

NULL

The mysqlx_ssl_crlpath system variable is like ssl_crlpath, except that it applies to X Plugin
rather than the MySQL Server main connection interface. For information about configuring encryption
support for X Plugin, see Section 19.4.1, “Using Encrypted Connections with X Plugin”.

• mysqlx_ssl_key

Command-Line Format

--mysqlx-ssl-key=file_name

Introduced

System Variable

5.7.12

mysqlx_ssl_key

3272

Scope

Dynamic

Type

Default Value

X Plugin Options and Variables

Global

No

File name

NULL

The mysqlx_ssl_key system variable is like ssl_key, except that it applies to X Plugin rather than
the MySQL Server main connection interface. For information about configuring encryption support for X
Plugin, see Section 19.4.1, “Using Encrypted Connections with X Plugin”.

19.4.2.3 X Plugin Status Variables

The X Plugin status variables have the following meanings.

• Mysqlx_address

The network address which X Plugin is bound to. If the bind has failed, or if the skip_networking
option has been used, the value shows UNDEFINED.

• Mysqlx_bytes_received

The number of bytes received through the network.

• Mysqlx_bytes_sent

The number of bytes sent through the network.

• Mysqlx_connection_accept_errors

The number of connections which have caused accept errors.

• Mysqlx_connection_errors

The number of connections which have caused errors.

• Mysqlx_connections_accepted

The number of connections which have been accepted.

• Mysqlx_connections_closed

The number of connections which have been closed.

• Mysqlx_connections_rejected

The number of connections which have been rejected.

• Mysqlx_crud_create_view

The number of create view requests received.

• Mysqlx_crud_delete

The number of delete requests received.

• Mysqlx_crud_drop_view

The number of drop view requests received.

3273

X Plugin Options and Variables

• Mysqlx_crud_find

The number of find requests received.

• Mysqlx_crud_insert

The number of insert requests received.

• Mysqlx_crud_modify_view

The number of modify view requests received.

• Mysqlx_crud_update

The number of update requests received.

• Mysqlx_errors_sent

The number of errors sent to clients.

• Mysqlx_errors_unknown_message_type

The number of unknown message types that have been received.

• Mysqlx_expect_close

The number of expectation blocks closed.

• Mysqlx_expect_open

The number of expectation blocks opened.

• Mysqlx_init_error

The number of errors during initialisation.

• Mysqlx_notice_other_sent

The number of other types of notices sent back to clients.

• Mysqlx_notice_warning_sent

The number of warning notices sent back to clients.

• Mysqlx_port

The TCP port which X Plugin is listening to. If a network bind has failed, or if the skip_networking
system variable is enabled, the value shows UNDEFINED.

• Mysqlx_rows_sent

The number of rows sent back to clients.

• Mysqlx_sessions

The number of sessions that have been opened.

• Mysqlx_sessions_accepted

The number of session attempts which have been accepted.

3274

X Plugin Options and Variables

• Mysqlx_sessions_closed

The number of sessions that have been closed.

• Mysqlx_sessions_fatal_error

The number of sessions that have closed with a fatal error.

• Mysqlx_sessions_killed

The number of sessions which have been killed.

• Mysqlx_sessions_rejected

The number of session attempts which have been rejected.

• Mysqlx_socket

The Unix socket which X Plugin is listening to.

• Mysqlx_ssl_accept_renegotiates

The number of negotiations needed to establish the connection.

• Mysqlx_ssl_accepts

The number of accepted SSL connections.

• Mysqlx_ssl_active

If SSL is active.

• Mysqlx_ssl_cipher

The current SSL cipher (empty for non-SSL connections).

• Mysqlx_ssl_cipher_list

A list of possible SSL ciphers (empty for non-SSL connections).

• Mysqlx_ssl_ctx_verify_depth

The certificate verification depth limit currently set in ctx.

• Mysqlx_ssl_ctx_verify_mode

The certificate verification mode currently set in ctx.

• Mysqlx_ssl_finished_accepts

The number of successful SSL connections to the server.

• Mysqlx_ssl_server_not_after

The last date for which the SSL certificate is valid.

• Mysqlx_ssl_server_not_before

The first date for which the SSL certificate is valid.

3275

X Plugin Options and Variables

• Mysqlx_ssl_verify_depth

The certificate verification depth for SSL connections.

• Mysqlx_ssl_verify_mode

The certificate verification mode for SSL connections.

• Mysqlx_ssl_version

The name of the protocol used for SSL connections.

• Mysqlx_stmt_create_collection

The number of create collection statements received.

• Mysqlx_stmt_create_collection_index

The number of create collection index statements received.

• Mysqlx_stmt_disable_notices

The number of disable notice statements received.

• Mysqlx_stmt_drop_collection

The number of drop collection statements received.

• Mysqlx_stmt_drop_collection_index

The number of drop collection index statements received.

• Mysqlx_stmt_enable_notices

The number of enable notice statements received.

• Mysqlx_stmt_ensure_collection

The number of ensure collection statements received.

• Mysqlx_stmt_execute_mysqlx

The number of StmtExecute messages received with namespace set to mysqlx.

• Mysqlx_stmt_execute_sql

The number of StmtExecute requests received for the SQL namespace.

• Mysqlx_stmt_execute_xplugin

The number of StmtExecute requests received for the X Plugin namespace.

• Mysqlx_stmt_kill_client

The number of kill client statements received.

• Mysqlx_stmt_list_clients

The number of list client statements received.

3276

Monitoring X Plugin

• Mysqlx_stmt_list_notices

The number of list notice statements received.

• Mysqlx_stmt_list_objects

The number of list object statements received.

• Mysqlx_stmt_ping

The number of ping statements received.

• Mysqlx_worker_threads

The number of worker threads available.

• Mysqlx_worker_threads_active

The number of worker threads currently used.

19.4.3 Monitoring X Plugin

To monitor X Plugin, use the status variables that it exposes. See Section 19.4.2.3, “X Plugin Status
Variables”.

3277

3278

