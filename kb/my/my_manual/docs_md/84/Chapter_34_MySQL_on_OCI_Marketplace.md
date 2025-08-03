MySQL Configuration

The Create Compute Instance dialog is displayed.

See To create a Linux instance for information on how to complete the fields.

By default, the MySQL server listens on port 3306 and is configured with a single user, root.

Important

When the deployment is complete, and the MySQL server is started, you must
connect to the compute instance and retrieve the default root password which
was written to the MySQL log file.

See Connecting with SSH for more information.

The following MySQL software is installed:

• MySQL Server EE

• MySQL Enterprise Backup

• MySQL Shell

• MySQL Router

MySQL Configuration

For security, the following are enabled:

• SELinux: for more information, see Configuring and Using SELinux

• firewalld: for more information, see Controlling the firewalld Firewall Service

The following MySQL plugins are enabled:

• thread_pool

• validate_password

On startup, the following occurs:

• MySQL Server reads /etc/my.cnf and all files named *.cnf in /etc/my.cnf.d/.

• /etc/my.cnf.d/perf-tuning.cnf is created by /usr/bin/mkcnf based on the selected OCI

shape.

Note

To disable this mechanism, remove /etc/systemd/system/
mysqld.service.d/perf-tuning.conf.

Performance tuning is configured for the following shapes:

• VM.Standard2.1

• VM.Standard2.2

• VM.Standard2.4

• VM.Standard2.8

• VM.Standard2.16

5066

Configuring Network Access

• VM.Standard2.24

• VM.Standard.E2.1

• VM.Standard.E2.2

• VM.Standard.E2.4

• VM.Standard.E2.8

• VM.Standard.E3.Flex

• VM.Standard.E4.Flex

• BM.Standard2.52

Important

For all other shapes, the tuning for VM.Standard2.1 is used.

34.3 Configuring Network Access

For information on OCI Security Rules, see Security Rules.

Important

You must enable ingress on the following ports:

• 22: SSH

• 3306: MySQL

• 33060: (optional) MySQL X Protocol. Used by MySQL Shell.

34.4 Connecting

This section describes the various connection methods for connecting to the deployed MySQL server
on the OCI Compute Instance.

Connecting with SSH

This section gives some detail on connecting from a UNIX-like platform to the OCI Compute. For
more information on connecting with SSH, see Accessing an Oracle Linux Instance Using SSH and
Connecting to Your Instance.

To connect to the Oracle Linux running on the Compute Instance with SSH, run the following
command:

ssh opc@computeIP

where opc is the compute user and computeIP is the IP address of your Compute Instance.

To find the temporary root password created for the root user, run the following command:

sudo grep 'temporary password' /var/log/mysqld.log

To change your default password, log in to the server using the generated, temporary password, using
the following command: mysql -uroot -p. Then run the following:

ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';

5067

Connecting with MySQL Client

Connecting with MySQL Client

Note

To connect from your local MySQL client, you must first create on the MySQL
server a user which allows remote login.

To connect to the MySQL Server from your local MySQL client, run the following command from your
shell session:

mysql -uroot -p -hcomputeIP

where computeIP is the IP address of your Compute Instance.

Connecting with MySQL Shell

To connect to the MySQL Server from your local MySQL Shell, run the following command to start your
shell session:

mysqlsh root@computeIP

where computeIP is the IP address of your Compute Instance.

For more information on MySQL Shell connections, see MySQL Shell Connections.

Connecting with Workbench

To connect to the MySQL Server from MySQL Workbench, see Connections in MySQL Workbench.

34.5 Maintenance

This product is user-managed, meaning you are responsible for upgrades and maintenance.

Upgrading MySQL

The existing installation is RPM-based, to upgrade the MySQL server, see Section 3.7, “Upgrading
MySQL Binary or Package-based Installations on Unix/Linux”.

You can use scp to copy the required RPM to the OCI Compute Instance, or copy it from OCI Object
Storage, if you have configured access to it. File Storage is also an option. For more information, see
File Storage and NFS.

Backup and Restore

MySQL Enterprise Backup is the preferred backup and restore solution. For more information, see
Backing Up to Cloud Storage.

For information on MySQL Enterprise Backup, see Getting Started with MySQL Enterprise Backup.

For information on the default MySQL backup and restore, see Chapter 9, Backup and Recovery.

5068

