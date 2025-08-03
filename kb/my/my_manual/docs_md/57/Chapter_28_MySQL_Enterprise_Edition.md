MySQL Enterprise Security Overview

MySQL Enterprise Backup does a hot backup of all tables that use the InnoDB storage engine. For tables
using MyISAM or other non-InnoDB storage engines, it does a “warm” backup, where the database
continues to run, but those tables cannot be modified while being backed up. For efficient backup
operations, you can designate InnoDB as the default storage engine for new tables, or convert existing
tables to use the InnoDB storage engine.

28.2 MySQL Enterprise Security Overview

MySQL Enterprise Edition provides plugins that implement security features using external services:

• MySQL Enterprise Edition includes an authentication plugin that enables MySQL Server to use LDAP
(Lightweight Directory Access Protocol) to authenticate MySQL users. LDAP Authentications supports
user name and password, SASL, and GSSAPI/Kerberos authentication methods to LDAP services. For
more information, see Section 6.4.1.9, “LDAP Pluggable Authentication”.

• MySQL Enterprise Edition includes an authentication plugin that enables MySQL Server to use Native
Kerberos to authenticate MySQL users using there Kerberos Principals. For more information, see
Kerberos Pluggable Authentication.

• MySQL Enterprise Edition includes an authentication plugin that enables MySQL Server to use PAM
(Pluggable Authentication Modules) to authenticate MySQL users. PAM enables a system to use a
standard interface to access various kinds of authentication methods, such as Unix passwords or an
LDAP directory. For more information, see Section 6.4.1.7, “PAM Pluggable Authentication”.

• MySQL Enterprise Edition includes an authentication plugin that performs external authentication on

Windows, enabling MySQL Server to use native Windows services to authenticate client connections.
Users who have logged in to Windows can connect from MySQL client programs to the server based on
the information in their environment without specifying an additional password. For more information, see
Section 6.4.1.8, “Windows Pluggable Authentication”.

• MySQL Enterprise Edition includes a suite of masking and de-identification functions that perform
subsetting, random generation, and dictionary replacement to de-identify strings, numerics, phone
numbers, emails and more. These functions enable masking existing data using several methods such
as obfuscation (removing identifying characteristics), generation of formatted random data, and data
replacement or substitution. For more information, see Section 6.5, “MySQL Enterprise Data Masking
and De-Identification”.

• MySQL Enterprise Edition includes a set of encryption functions based on the OpenSSL library that
expose OpenSSL capabilities at the SQL level. For more information, see Section 28.3, “MySQL
Enterprise Encryption Overview”.

• MySQL Enterprise Edition 5.7 and higher includes a keyring plugin that uses Oracle Key Vault as a

backend for keyring storage. For more information, see Section 6.4.4, “The MySQL Keyring”.

• MySQL Transparent Data Encryption (TDE) provides at-rest encryption for MySQL Server for all files
that might contain sensitive data. For more information, see Section 14.14, “InnoDB Data-at-Rest
Encryption”, Encrypting Binary Log Files and Relay Log Files, and Encrypting Audit Log Files.

For other related Enterprise security features, see Section 28.3, “MySQL Enterprise Encryption Overview”.

28.3 MySQL Enterprise Encryption Overview

MySQL Enterprise Edition includes a set of encryption functions based on the OpenSSL library that expose
OpenSSL capabilities at the SQL level. These functions enable Enterprise applications to perform the
following operations:

4486

MySQL Enterprise Monitor Overview

sensitive information by replacing real values with substitutes. MySQL Enterprise Data Masking and De-
Identification functions enable masking existing data using several methods such as obfuscation (removing
identifying characteristics), generation of formatted random data, and data replacement or substitution.

For more information, see Section 6.5, “MySQL Enterprise Data Masking and De-Identification”.

28.8 MySQL Enterprise Monitor Overview

For information about MySQL Enterprise Monitor behavior, see the MySQL Enterprise Monitor manual:
https://dev.mysql.com/doc/mysql-monitor/en/.

Important

MySQL Enterprise Monitor will be end of life and deprecated with obsolescence as
of January 1, 2025.

After this date, MySQL Enterprise Monitor will no longer receive security updates, non-security updates,
bug fixes, or online technical content updates. It will transition to the Sustaining Support model.

What to expect when MySQL Enterprise Monitor reaches the end of life (EOL):

• MySQL will cease all bug fix activities for the product

• MySQL will cease all security fix activities for the product

• MySQL will cease all new feature work for the product

Sustaining Support does not include:

• New program updates, fixes, security alerts, and critical patch updates

• New tax, legal, or regulatory updates

• New upgrade scripts

• Certification with new third-party products/versions

• 24 hour commitment and response guidelines for Severity 1 service requests as defined in "Section 9 -

Severity Definitions" in the document titled "Oracle Software Technical Support Policies"

• Previously released fixes or updates that Oracle has withdrawn from publication. Older or existing

published software bundles will remain available as archived content.

For the set of Oracle Technical Support Policies, visit: https://www.oracle.com/support/policies.html

For an explanation of the different support models (like Sustaining Support), visit: https://www.oracle.com/
support/lifetime-support/

For customers that are currently using earlier versions of MySQL Enterprise Monitor, your options include:

• Use Enterprise Manager for MySQL. This is a free product for customers with a valid Oracle Support
Contract. For more information, visit Comprehensive Monitoring and Compliance Management for
MySQL Databases using Enterprise Manager.

• Use the database monitoring capabilities of the OCI Database Management service. For MySQL

on-premises customers, this is a paid feature that will be released soon. For more information, visit
Database Management for MySQL HeatWave.

4488

Affected deployments

Affected deployments

• MySQL Enterprise Monitor Service Manager for Linux x86 (64-bit)

• MySQL Enterprise Monitor Agent for Linux x86 (64-bit)

• MySQL Enterprise Monitor Service Manager for Windows x86 (64-bit)

• MySQL Enterprise Monitor Agent for Microsoft Windows x86 (64-bit)

• MySQL Enterprise Monitor Service Manager for Mac OS X x86 (64-bit)

• MySQL Enterprise Monitor Agent for Mac OS X x86 (64-bit)

28.9 MySQL Telemetry

The MySQL telemetry component is based on the OpenTelemetry (OTel) project, an open-source, vendor-
neutral observability framework providing a common observability standard. It enables users to instrument
their applications in order to export observability data: traces, metrics and logs, enabling increased
granularity of debugging and testing.

For more information, see Telemetry.

4489

4490

