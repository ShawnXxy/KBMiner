MySQL Enterprise Security Overview

backup operations, you can designate InnoDB as the default storage engine for new tables, or convert
existing tables to use the InnoDB storage engine.

32.2 MySQL Enterprise Security Overview

MySQL Enterprise Edition provides plugins that implement security features using external services:

• MySQL Enterprise Edition includes an authentication plugin that enables MySQL Server to use

LDAP (Lightweight Directory Access Protocol) to authenticate MySQL users. LDAP Authentications
supports user name and password, SASL, and GSSAPI/Kerberos authentication methods to LDAP
services. For more information, see Section 8.4.1.7, “LDAP Pluggable Authentication”.

• MySQL Enterprise Edition includes an authentication plugin that enables MySQL Server to use

Native Kerberos to authenticate MySQL users using there Kerberos Principals. For more information,
see Section 8.4.1.8, “Kerberos Pluggable Authentication”.

• MySQL Enterprise Edition includes an authentication plugin that enables MySQL Server to use PAM
(Pluggable Authentication Modules) to authenticate MySQL users. PAM enables a system to use a
standard interface to access various kinds of authentication methods, such as Unix passwords or an
LDAP directory. For more information, see Section 8.4.1.5, “PAM Pluggable Authentication”.

• MySQL Enterprise Edition includes an authentication plugin that performs external authentication

on Windows, enabling MySQL Server to use native Windows services to authenticate client
connections. Users who have logged in to Windows can connect from MySQL client programs to the
server based on the information in their environment without specifying an additional password. For
more information, see Section 8.4.1.6, “Windows Pluggable Authentication”.

• MySQL Enterprise Edition includes a suite of masking and de-identification functions that perform
subsetting, random generation, and dictionary replacement to de-identify strings, numerics, phone
numbers, emails and more. These functions enable masking existing data using several methods
such as obfuscation (removing identifying characteristics), generation of formatted random data, and
data replacement or substitution. For more information, see Section 8.5, “MySQL Enterprise Data
Masking and De-Identification”.

• MySQL Enterprise Edition includes a set of encryption functions based on the OpenSSL library that
expose OpenSSL capabilities at the SQL level. For more information, see Section 32.3, “MySQL
Enterprise Encryption Overview”.

• MySQL Enterprise Edition 5.7 and higher includes a keyring plugin that uses Oracle Key Vault as a

backend for keyring storage. For more information, see Section 8.4.4, “The MySQL Keyring”.

• MySQL Transparent Data Encryption (TDE) provides at-rest encryption for MySQL Server for all files
that might contain sensitive data. For more information, see Section 17.13, “InnoDB Data-at-Rest
Encryption”, Section 19.3.2, “Encrypting Binary Log Files and Relay Log Files”, and Encrypting Audit
Log Files.

For other related Enterprise security features, see Section 32.3, “MySQL Enterprise Encryption
Overview”.

32.3 MySQL Enterprise Encryption Overview

MySQL Enterprise Edition includes a set of encryption functions based on the OpenSSL library that
expose OpenSSL capabilities at the SQL level. These functions enable Enterprise applications to
perform the following operations:

• Implement added data protection using public-key asymmetric cryptography

• Create public and private keys and digital signatures

• Perform asymmetric encryption and decryption

5446

MySQL Telemetry

• MySQL Enterprise Monitor Service Manager for Windows x86 (64-bit)

• MySQL Enterprise Monitor Agent for Microsoft Windows x86 (64-bit)

• MySQL Enterprise Monitor Service Manager for Mac OS X x86 (64-bit)

• MySQL Enterprise Monitor Agent for Mac OS X x86 (64-bit)

32.9 MySQL Telemetry

The MySQL telemetry component is based on the OpenTelemetry (OTel) project, an open-source,
vendor-neutral observability framework providing a common observability standard. It enables users
to instrument their applications in order to export observability data: traces, metrics and logs, enabling
increased granularity of debugging and testing.

For more information, see Telemetry.

5449

5450

