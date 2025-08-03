General Installation Guidance

initial MySQL root user account, which has no password until you assign one. The section applies
whether you install MySQL using a binary or source distribution.

7.

If you want to run the MySQL benchmark scripts, Perl support for MySQL must be available. See
Section 2.10, “Perl Installation Notes”.

Instructions for installing MySQL on different platforms and environments is available on a platform by
platform basis:

• Unix, Linux

For instructions on installing MySQL on most Linux and Unix platforms using a generic binary (for
example, a .tar.gz package), see Section 2.2, “Installing MySQL on Unix/Linux Using Generic
Binaries”.

For information on building MySQL entirely from the source code distributions or the source code
repositories, see Section 2.8, “Installing MySQL from Source”

For specific platform help on installation, configuration, and building from source see the
corresponding platform section:

• Linux, including notes on distribution specific methods, see Section 2.5, “Installing MySQL on

Linux”.

• IBM AIX, see Section 2.7, “Installing MySQL on Solaris”.

• Microsoft Windows

For instructions on installing MySQL on Microsoft Windows, using either the MySQL Installer or
Zipped binary, see Section 2.3, “Installing MySQL on Microsoft Windows”.

For details and instructions on building MySQL from source code using Microsoft Visual Studio, see
Section 2.8, “Installing MySQL from Source”.

• macOS

For installation on macOS, including using both the binary package and native PKG formats, see
Section 2.4, “Installing MySQL on macOS”.

For information on making use of an macOS Launch Daemon to automatically start and stop MySQL,
see Section 2.4.3, “Installing and Using the MySQL Launch Daemon”.

For information on the MySQL Preference Pane, see Section 2.4.4, “Installing and Using the MySQL
Preference Pane”.

2.1 General Installation Guidance

The immediately following sections contain the information necessary to choose, download, and verify
your distribution. The instructions in later sections of the chapter describe how to install the distribution
that you choose. For binary distributions, see the instructions at Section 2.2, “Installing MySQL on
Unix/Linux Using Generic Binaries” or the corresponding section for your platform if available. To build
MySQL from source, use the instructions in Section 2.8, “Installing MySQL from Source”.

2.1.1 Supported Platforms

MySQL platform support evolves over time; please refer to https://www.mysql.com/support/
supportedplatforms/database.html for the latest updates.

2.1.2 Which MySQL Version and Distribution to Install

When preparing to install MySQL, decide which version and distribution format (binary or source) to
use.

107

Verifying Package Integrity Using MD5 Checksums or GnuPG

To verify the signature for a specific package, you first need to obtain a copy of our public GPG build
key, which you can download from http://pgp.mit.edu/. The key that you want to obtain is named
mysql-build@oss.oracle.com. The keyID for MySQL 8.0.36 packages and higher, and MySQL
8.3.0 and higher, is A8D3785C. After obtaining this key, you should compare it with the key following
value before using it verify MySQL packages. Alternatively, you can copy and paste the key directly
from the text below.

Note

The public GPG build key for earlier MySQL release packages (keyID
5072E1F5 or 3A79BD29), see Section 2.1.4.5, “GPG Public Build Key for
Archived Packages”.

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: SKS 1.1.6
Comment: Hostname: pgp.mit.edu

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
cAZUlaj3id3TxquAlud4lWDz
=h5nH
-----END PGP PUBLIC KEY BLOCK-----

To import the build key into your personal public GPG keyring, use gpg --import. For example, if
you have saved the key in a file named mysql_pubkey.asc, the import command looks like this:

$> gpg --import mysql_pubkey.asc
gpg: key B7B3B788A8D3785C: public key "MySQL Release Engineering
<mysql-build@oss.oracle.com>" imported

110

Verifying Package Integrity Using MD5 Checksums or GnuPG

gpg: Total number processed: 1
gpg:               imported: 1

You can also download the key from the public keyserver using the public key id, A8D3785C:

$> gpg --recv-keys A8D3785C
gpg: requesting key A8D3785C from hkp server keys.gnupg.net
gpg: key A8D3785C: "MySQL Release Engineering <mysql-build@oss.oracle.com>"
1 new user ID
gpg: key A8D3785C: "MySQL Release Engineering <mysql-build@oss.oracle.com>"
53 new signatures
gpg: no ultimately trusted keys found
gpg: Total number processed: 1
gpg:           new user IDs: 1
gpg:         new signatures: 53

If you want to import the key into your RPM configuration to validate RPM install packages, you should
be able to import the key directly:

$> rpm --import mysql_pubkey.asc

If you experience problems or require RPM specific information, see Section 2.1.4.4, “Signature
Checking Using RPM”.

After you have downloaded and imported the public build key, download your desired MySQL package
and the corresponding signature, which also is available from the download page. The signature file
has the same name as the distribution file with an .asc extension, as shown by the examples in the
following table.

Table 2.1 MySQL Package and Signature Files for Source files

File Type

Distribution file

Signature file

File Name

mysql-8.0.42-linux-glibc2.28-
x86_64.tar.xz

mysql-8.0.42-linux-glibc2.28-
x86_64.tar.xz.asc

Make sure that both files are stored in the same directory and then run the following command to verify
the signature for the distribution file:

$> gpg --verify package_name.asc

If the downloaded package is valid, you should see a Good signature message similar to this:

$> gpg --verify mysql-8.0.42-linux-glibc2.28-x86_64.tar.xz.asc
gpg: Signature made Fri 15 Dec 2023 06:55:13 AM EST
gpg:                using RSA key BCA43417C3B485DD128EC6D4B7B3B788A8D3785C
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"

The Good signature message indicates that the file signature is valid, when compared to the
signature listed on our site. But you might also see warnings, like so:

$> gpg --verify mysql-8.0.42-linux-glibc2.28-x86_64.tar.xz.asc
gpg: Signature made Fri 15 Dec 2023 06:55:13 AM EST
gpg:                using RSA key BCA43417C3B485DD128EC6D4B7B3B788A8D3785C
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: BCA4 3417 C3B4 85DD 128E  C6D4 B7B3 B788 A8D3 785C

That is normal, as they depend on your setup and configuration. Here are explanations for these
warnings:

• gpg: no ultimately trusted keys found: This means that the specific key is not "ultimately trusted" by

you or your web of trust, which is okay for the purposes of verifying file signatures.

111

Verifying Package Integrity Using MD5 Checksums or GnuPG

• WARNING: This key is not certified with a trusted signature! There is no indication that the signature
belongs to the owner.: This refers to your level of trust in your belief that you possess our real public
key. This is a personal decision. Ideally, a MySQL developer would hand you the key in person,
but more commonly, you downloaded it. Was the download tampered with? Probably not, but this
decision is up to you. Setting up a web of trust is one method for trusting them.

See the GPG documentation for more information on how to work with public keys.

2.1.4.3 Signature Checking Using Gpg4win for Windows

The Section 2.1.4.2, “Signature Checking Using GnuPG” section describes how to verify MySQL
downloads using GPG. That guide also applies to Microsoft Windows, but another option is to use a
GUI tool like Gpg4win. You may use a different tool but our examples are based on Gpg4win, and
utilize its bundled Kleopatra GUI.

Download and install Gpg4win, and then load Kleopatra. The dialog should look similar to:

Figure 2.1 Kleopatra: Initial Screen

Next, add the MySQL Release Engineering certificate. Do this by clicking File, Lookup Certificates on
Server. Type "Mysql Release Engineering" into the search box and press Search.

Figure 2.2 Kleopatra: Lookup Certificates on Server Wizard: Finding a Certificate

112

Verifying Package Integrity Using MD5 Checksums or GnuPG

Select the "MySQL Release Engineering" certificate. The Fingerprint and Key-ID must be "3A79BD29"
for MySQL 8.0.28 and higher or "5072E1F5" for MySQL 8.0.27 and earlier, or choose Details... to
confirm the certificate is valid. Now, import it by clicking Import. When the import dialog is displayed,
choose Okay, and this certificate should now be listed under the Imported Certificates tab.

Next, configure the trust level for our certificate. Select our certificate, then from the main menu select
Certificates, Change Owner Trust.... We suggest choosing I believe checks are very accurate for
our certificate, as otherwise you might not be able to verify our signature. Select I believe checks are
very accurate to enable "full trust" and then press OK.

Figure 2.3 Kleopatra: Change Trust level for MySQL Release Engineering

Next, verify the downloaded MySQL package file. This requires files for both the packaged file, and
the signature. The signature file must have the same name as the packaged file but with an appended
.asc extension, as shown by the example in the following table. The signature is linked to on the
downloads page for each MySQL product. You must create the .asc file with this signature.

Table 2.2 MySQL Package and Signature Files for MySQL Installer for Microsoft Windows

File Type

Distribution file

Signature file

File Name

mysql-installer-community-8.0.42.msi

mysql-installer-
community-8.0.42.msi.asc

Make sure that both files are stored in the same directory and then run the following command to verify
the signature for the distribution file. Either drag and drop the signature (.asc) file into Kleopatra, or
load the dialog from File, Decrypt/Verify Files..., and then choose either the .msi or .asc file.

113

Verifying Package Integrity Using MD5 Checksums or GnuPG

Figure 2.4 Kleopatra: The Decrypt and Verify Files Dialog

Click Decrypt/Verify to check the file. The two most common results look like the following figure;
although the yellow warning may look problematic, the following means that the file check passed with
success. You may now run this installer.

Figure 2.5 Kleopatra: the Decrypt and Verify Results Dialog: All operations completed

Seeing a red The signature is bad error means the file is invalid. Do not execute the MSI file if
you see this error.

114

Verifying Package Integrity Using MD5 Checksums or GnuPG

Figure 2.6 Kleopatra: the Decrypt and Verify Results Dialog: Bad

The Section 2.1.4.2, “Signature Checking Using GnuPG”, section explains why you do not see a green
Good signature result.

2.1.4.4 Signature Checking Using RPM

For RPM packages, there is no separate signature. RPM packages have a built-in GPG signature and
MD5 checksum. You can verify a package by running the following command:

$> rpm --checksig package_name.rpm

Example:

$> rpm --checksig mysql-community-server-8.0.42-1.el8.x86_64.rpm
mysql-community-server-8.0.42-1.el8.x86_64.rpm: digests signatures OK

Note

If you are using RPM 4.1 and it complains about (GPG) NOT OK (MISSING
KEYS: GPG#3a79bd29), even though you have imported the MySQL public
build key into your own GPG keyring, you need to import the key into the RPM
keyring first. RPM 4.1 no longer uses your personal GPG keyring (or GPG
itself). Rather, RPM maintains a separate keyring because it is a system-wide
application and a user's GPG public keyring is a user-specific file. To import the
MySQL public key into the RPM keyring, first obtain the key, then use rpm --
import to import the key. For example:

$> gpg --export -a 3a79bd29 > 3a79bd29.asc
$> rpm --import 3a79bd29.asc

Alternatively, rpm also supports loading the key directly from a URL:

$> rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2023

You can also obtain the MySQL public key from this manual page: Section 2.1.4.2, “Signature
Checking Using GnuPG”.

115

Verifying Package Integrity Using MD5 Checksums or GnuPG

2.1.4.5 GPG Public Build Key for Archived Packages

The following GPG public build key (keyID 3A79BD29) can be used to verify the authenticity and
integrity of MySQL packages versions 8.0.28 through 8.0.35, 8.1.0, and 8.2.0. For signature checking
instructions, see Section 2.1.4.2, “Signature Checking Using GnuPG”. It expired on December 14,
2023.

GPG Public Build Key for MySQL 8.0.28 through 8.0.35, and 8.1.0/8.2.0 Packages

-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBGG4urcBEACrbsRa7tSSyxSfFkB+KXSbNM9rxYqoB78u107skReefq4/+Y72
TpDvlDZLmdv/lK0IpLa3bnvsM9IE1trNLrfi+JES62kaQ6hePPgn2RqxyIirt2se
Si3Z3n3jlEg+mSdhAvW+b+hFnqxo+TY0U+RBwDi4oO0YzHefkYPSmNPdlxRPQBMv
4GPTNfxERx6XvVSPcL1+jQ4R2cQFBryNhidBFIkoCOszjWhm+WnbURsLheBp757l
qEyrpCufz77zlq2gEi+wtPHItfqsx3rzxSRqatztMGYZpNUHNBJkr13npZtGW+kd
N/xu980QLZxN+bZ88pNoOuzD6dKcpMJ0LkdUmTx5z9ewiFiFbUDzZ7PECOm2g3ve
Jrwr79CXDLE1+39Hr8rDM2kDhSr9tAlPTnHVDcaYIGgSNIBcYfLmt91133klHQHB
IdWCNVtWJjq5YcLQJ9TxG9GQzgABPrm6NDd1t9j7w1L7uwBvMB1wgpirRTPVfnUS
Cd+025PEF+wTcBhfnzLtFj5xD7mNsmDmeHkF/sDfNOfAzTE1v2wq0ndYU60xbL6/
yl/Nipyr7WiQjCG0m3WfkjjVDTfs7/DXUqHFDOu4WMF9v+oqwpJXmAeGhQTWZC/Q
hWtrjrNJAgwKpp263gDSdW70ekhRzsok1HJwX1SfxHJYCMFs2aH6ppzNsQARAQAB
tDZNeVNRTCBSZWxlYXNlIEVuZ2luZWVyaW5nIDxteXNxbC1idWlsZEBvc3Mub3Jh
Y2xlLmNvbT6JAlQEEwEIAD4WIQSFm+jXxYb1OEMLGcJGe5QtOnm9KQUCYbi6twIb
AwUJA8JnAAULCQgHAgYVCgkICwIEFgIDAQIeAQIXgAAKCRBGe5QtOnm9KUewD/99
2sS31WLGoUQ6NoL7qOB4CErkqXtMzpJAKKg2jtBGG3rKE1/0VAg1D8AwEK4LcCO4
07wohnH0hNiUbeDck5x20pgS5SplQpuXX1K9vPzHeL/WNTb98S3H2Mzj4o9obED6
Ey52tTupttMF8pC9TJ93LxbJlCHIKKwCA1cXud3GycRN72eqSqZfJGdsaeWLmFmH
f6oee27d8XLoNjbyAxna/4jdWoTqmp8oT3bgv/TBco23NzqUSVPi+7ljS1hHvcJu
oJYqaztGrAEf/lWIGdfl/kLEh8IYx8OBNUojh9mzCDlwbs83CBqoUdlzLNDdwmzu
34Aw7xK14RAVinGFCpo/7EWoX6weyB/zqevUIIE89UABTeFoGih/hx2jdQV/NQNt
hWTW0jH0hmPnajBVAJPYwAuO82rx2pnZCxDATMn0elOkTue3PCmzHBF/GT6c65aQ
C4aojj0+Veh787QllQ9FrWbwnTz+4fNzU/MBZtyLZ4JnsiWUs9eJ2V1g/A+RiIKu
357Qgy1ytLqlgYiWfzHFlYjdtbPYKjDaScnvtY8VO2Rktm7XiV4zKFKiaWp+vuVY
pR0/7Adgnlj5Jt9lQQGOr+Z2VYx8SvBcC+by3XAtYkRHtX5u4MLlVS3gcoWfDiWw
CpvqdK21EsXjQJxRr3dbSn0HaVj4FJZX0QQ7WZm6WLkCDQRhuLq3ARAA6RYjqfC0
YcLGKvHhoBnsX29vy9Wn1y2JYpEnPUIB8X0VOyz5/ALv4Hqtl4THkH+mmMuhtndo
q2BkCCk508jWBvKS1S+Bd2esB45BDDmIhuX3ozu9Xza4i1FsPnLkQ0uMZJv30ls2
pXFmskhYyzmo6aOmH2536LdtPSlXtywfNV1HEr69V/AHbrEzfoQkJ/qvPzELBOjf
jwtDPDePiVgW9LhktzVzn/BjO7XlJxw4PGcxJG6VApsXmM3t2fPN9eIHDUq8ocbH
dJ4en8/bJDXZd9ebQoILUuCg46hE3p6nTXfnPwSRnIRnsgCzeAz4rxDR4/Gv1Xpz
v5wqpL21XQi3nvZKlcv7J1IRVdphK66De9GpVQVTqC102gqJUErdjGmxmyCA1OOO
RqEPfKTrXz5YUGsWwpH+4xCuNQP0qmreRw3ghrH8potIr0iOVXFic5vJfBTgtcuE
B6E6ulAN+3jqBGTaBML0jxgj3Z5VC5HKVbpg2DbB/wMrLwFHNAbzV5hj2Os5Zmva
0ySP1YHB26pAW8dwB38GBaQvfZq3ezM4cRAo/iJ/GsVE98dZEBO+Ml+0KYj+ZG+v
yxzo20sweun7ZKT+9qZM90f6cQ3zqX6IfXZHHmQJBNv73mcZWNhDQOHs4wBoq+FG
QWNqLU9xaZxdXw80r1viDAwOy13EUtcVbTkAEQEAAYkCPAQYAQgAJhYhBIWb6NfF
hvU4QwsZwkZ7lC06eb0pBQJhuLq3AhsMBQkDwmcAAAoJEEZ7lC06eb0pSi8P/iy+
dNnxrtiENn9vkkA7AmZ8RsvPXYVeDCDSsL7UfhbS77r2L1qTa2aB3gAZUDIOXln5
1lSxMeeLtOequLMEV2Xi5km70rdtnja5SmWfc9fyExunXnsOhg6UG872At5CGEZU
0c2Nt/hlGtOR3xbt3O/Uwl+dErQPA4BUbW5K1T7OC6oPvtlKfF4bGZFloHgt2yE9
YSNWZsTPe6XJSapemHZLPOxJLnhs3VBirWE31QS0bRl5AzlO/fg7ia65vQGMOCOT
LpgChTbcZHtozeFqva4IeEgE4xN+6r8WtgSYeGGDRmeMEVjPM9dzQObf+SvGd58u
2z9f2agPK1H32c69RLoA0mHRe7Wkv4izeJUc5tumUY0e8OjdenZZjT3hjLh6tM+m
rp2oWnQIoed4LxUw1dhMOj0rYXv6laLGJ1FsW5eSke7ohBLcfBBTKnMCBohROHy2
E63Wggfsdn3UYzfqZ8cfbXetkXuLS/OM3MXbiNjg+ElYzjgWrkayu7yLakZx+mx6
sHPIJYm2hzkniMG29d5mGl7ZT9emP9b+CfqGUxoXJkjs0gnDl44bwGJ0dmIBu3aj
VAaHODXyY/zdDMGjskfEYbNXCAY2FRZSE58tgTvPKD++Kd2KGplMU2EIFT7JYfKh
HAB5DGMkx92HUMidsTSKHe+QnnnoFmu4gnmDU31i
=Xqbo
-----END PGP PUBLIC KEY BLOCK-----

The following GPG public build key (keyID 5072E1F5) can be used to verify the authenticity
and integrity of MySQL 8.0.27 packages and earlier. For signature checking instructions, see
Section 2.1.4.2, “Signature Checking Using GnuPG”.

GPG Public Build Key for MySQL 8.0.27 Packages and Earlier

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: SKS 1.1.6

116

Verifying Package Integrity Using MD5 Checksums or GnuPG

Comment: Hostname: pgp.mit.edu

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

117

Verifying Package Integrity Using MD5 Checksums or GnuPG

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

118

Verifying Package Integrity Using MD5 Checksums or GnuPG

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

119

Verifying Package Integrity Using MD5 Checksums or GnuPG

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

120

Verifying Package Integrity Using MD5 Checksums or GnuPG

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

121

Verifying Package Integrity Using MD5 Checksums or GnuPG

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

122

Verifying Package Integrity Using MD5 Checksums or GnuPG

AgECF4AACgkQjHGNO1By4fVxjgCeKVTBNefwxq1A6IbRr9s/Gu8r+AIAniiKdI1lFhOduUKH
AVprO3s8XerMiF0EExECAB0FAkeslLQFCQ0wWKgFCwcKAwQDFQMCAxYCAQIXgAAKCRCMcY07
UHLh9a6SAJ9/PgZQSPNeQ6LvVVzCALEBJOBt7QCffgs+vWP18JutdZc7XiawgAN9vmmIXQQT
EQIAHQUCR6yUzwUJDTBYqAULBwoDBAMVAwIDFgIBAheAAAoJEIxxjTtQcuH1dCoAoLC6RtsD
9K3N7NOxcp3PYOzH2oqzAKCFHn0jSqxk7E8by3sh+Ay8yVv0BYhdBBMRAgAdBQsHCgMEAxUD
AgMWAgECF4AFAkequSEFCQ0ufRUACgkQjHGNO1By4fUdtwCfRNcueXikBMy7tE2BbfwEyTLB
TFAAnifQGbkmcARVS7nqauGhe1ED/vdgiF0EExECAB0FCwcKAwQDFQMCAxYCAQIXgAUCS3Au
ZQUJEPPyWQAKCRCMcY07UHLh9aA+AKCHDkOBKBrGb8tOg9BIub3LFhMvHQCeIOOot1hHHUls
TIXAUrD8+ubIeZaIZQQTEQIAHQUCPj6jDAUJCWYBgAULBwoDBAMVAwIDFgIBAheAABIJEIxx
jTtQcuH1B2VHUEcAAQFxjgCeKVTBNefwxq1A6IbRr9s/Gu8r+AIAniiKdI1lFhOduUKHAVpr
O3s8XerMiGUEExECAB0FAkeslLQFCQ0wWKgFCwcKAwQDFQMCAxYCAQIXgAASCRCMcY07UHLh
9QdlR1BHAAEBrpIAn38+BlBI815Dou9VXMIAsQEk4G3tAJ9+Cz69Y/Xwm611lzteJrCAA32+
aYhlBBMRAgAdBQsHCgMEAxUDAgMWAgECF4AFAktwL8oFCRDz86cAEgdlR1BHAAEBCRCMcY07
UHLh9bDbAJ4mKWARqsvx4TJ8N1hPJF2oTjkeSgCeMVJljxmD+Jd4SscjSvTgFG6Q1WCIbwQw
EQIALwUCTnc9rSgdIGJ1aWxkQG15c3FsLmNvbSB3aWxsIHN0b3Agd29ya2luZyBzb29uAAoJ
EIxxjTtQcuH1tT0An3EMrSjEkUv29OX05JkLiVfQr0DPAJwKtL1ycnLPv15pGMvSzav8JyWN
3Ih7BDARAgA7BQJCdzX1NB0AT29wcy4uLiBzaG91bGQgaGF2ZSBiZWVuIGxvY2FsISBJJ20g
KnNvKiBzdHVwaWQuLi4ACgkQOcor9D1qil/vRwCdFo08f66oKLiuEAqzlf9iDlPozEEAn2Eg
vCYLCCHjfGosrkrU3WK5NFVgiI8EMBECAE8FAkVvAL9IHQBTaG91bGQgaGF2ZSBiZWVuIGEg
bG9jYWwgc2lnbmF0dXJlLCBvciBzb21ldGhpbmcgLSBXVEYgd2FzIEkgdGhpbmtpbmc/AAoJ
EDnKK/Q9aopfoPsAn3BVqKOalJeF0xPSvLR90PsRlnmGAJ44oisY7Tl3NJbPgZal8W32fbqg
bIkBHAQSAQIABgUCS8IiAwAKCRDc9Osew28OLx5CB/91LHRH0qWjPPyIrv3DTQ06x2gljQ1r
Q1MWZNuoeDfRcmgbrZxdiBzf5Mmd36liFiLmDIGLEX8vyT+Q9U/Nf1bRh/AKFkOx9PDSINWY
bE6zCI2PNKjSWFarzr+cQvfQqGX0CEILVcU1HDxZlir1nWpRcccnasMBFp52+koc6PNFjQ13
HpHbM3IcPHaaV8JD3ANyFYS4l0C/S4etDQdX37GruVb9Dcv9XkC5TS2KjDIBsEs89isHrH2+
3ZlxdLsE7LxJ9DWLxbZAND9OiiuThjAGK/pYJb+hyLLuloCg85ZX81/ZLqEOKyl55xuTvCql
tSPmSUObCuWAH+OagBdYSduxiQEiBBABAgAMBQJJKmigBQMAEnUAAAoJEJcQuJvKV618U4wI
AKk/45VnuUf9w1j7fvdzgWdIjT9Lk9dLQAGB13gEVZEVYqtYF5cEZzyxl8c7NUTCTNX3qLId
ul114A4CQQDg5U9bUwwUKaUfGLaz380mtKtM9V9A4fl9H2Gfsdumr8RPDQihfUUqju+d0ycd
mcUScj48Nctx0xhCCWNjOFPERHi9hjRQq7x6RKyFTLjM5ftdInHCo9S+mzyqz9O+iMgX68Mm
+AVgdWSC9L6yGnw6H97GD28oRMGWBTzsmCyqf9I3YutH8mGXRot3QbSJD7/AeZVh1BQwVoJn
CT8Eo1pc/OYZkRRndE1thrX0yjuFwTeOzvqeHlgzEW/FtOCBW7iR0WSJASIEEAECAAwFAkoz
TogFAwASdQAACgkQlxC4m8pXrXwXiAf+Ked6Mgd98YyTyNiLHhllPulboCnKgj430jLzkfgv
7ytVCu1xMfKrRWRw3fA9LC19mzNQX/So/o/ywsk0nUG2sfEs5FiMk+aC957Ic/MDagmXqKap
ZROJbzbZ/KNj9rPCG9kXPGa9sUn6vk39nnv4hri30tNKpM0fMxRhpcoNoCrNl4rs/QTpdRpp
7KBuNaMEtDU7R7OjMDL4qT+BcCmYMIYW4dIV7tmaC0VxtcszZcVCkxSigRMPZHwxSx37GdCx
9/+TqlA4vGL6NQSxZKv+Kqa+WTqBngOl6YGO6FxdiXEliNRpf1mafmz6h8XgYXFGpehjuX1n
60Iz0BffuWbpL4kBIgQQAQIADAUCSkRyCgUDABJ1AAAKCRCXELibyletfPaaB/9FCSmYwz7m
vzOfHZOlEAYeLnCS290XGW89o4FYTbw0PBOulygyqj2TMCK68RCNU2KFs/bXBHeS+dDzitMA
fSaULYi7LJuCCmrDM5SX5aLSj6+TxkDQDR1K1ZE3y6qd4Kx3VeeoN7Wu+oLj/3Jjbbe0uYCQ
+/PniRra9f0Z0neTExZ7CGtVBIsKS1CnKBTR26MZMOom2eTRZwGFUX1PzuW/dbZ4Z0+J6XMd
Tm2td7OYYWPbV3noblkUrxyjtGtO3ip3Oe3zSCWHUFMaaEuXOMw8tN51wy6ybcPVAH0hOiBw
b3iCFJ/20QqaZEno6edYzkqf0pwvrcTmiPb+Vj0fnjBJiQEiBBABAgAMBQJKVj5HBQMAEnUA
AAoJEJcQuJvKV61845AH/R3IkGIGOB/7x3fI0gOkOS0uFljDxysiM8FV06BfXbFpRgFMZxAh
NFUdKCDN98MDkFBd5S5aGkvhAHS7PVwQ8/BIyJaJeUG3AXmrpFV/c9kYn1+YW5OQ9E7tKu5l
5UOj1Y/weNtC04u6Rh/nrp6CvMBhH2nvhSBZ+2kO2auqtFOhuK6+wUHGixt5EK8RAKs3Sf6n
kP2EJUHzy1Q8ec5YDiaV24AVkPFBZMCkpD3Z+seIGrL4zUkV7PPY4zd9g34Oqj8JvtnA4AD/
Z1vBLujLixcQdt9aieOySA9DAVgHbe2wVS4zi5nBURsmD5u96CUOwNK1sOV+ACtdIv/T5qSU
VweJASIEEAECAAwFAkpoCoQFAwASdQAACgkQlxC4m8pXrXysfQf+IJyIPhTphk0kGPQY3v9e
3znW30VahyZxoL6q25eeQWGmVeTFlU4JThUEyzgYGip8i9qBsFPJ9XgOL5bxTGv7/WOK7eX8
e+gXHB3A2QYbrM0GFZKN3BCkbA++HmvJXU58tf+aBCB0ObG+rPn6QUNSPibu4tp65TaPVPSV
HjNTTICxu3sneHB+okJcc5z1ubme8nAytKb6x0JM/keNSXAev2ZN7zG5m+Pqw7/DQ/gCogzG
ML1bulP2rSh8bYpJPC3vAVuHTmxsbhRBg4l7j5KiHf4qMBrVzRy+YiHhwpf2p8JbCGF141+H
UD1VMeGeXnNO/9SO+dC2OGUf8WrV4FIpxIkBIgQQAQIADAUCSnkuCgUDABJ1AAAKCRCXELib
yletfBjrCACDd/zvoveoNlNiUUBazelcGXwaxSvUMSROUQNkxkoMzfA+aFpYFHWEwDfLqndp
oJTIkgkESd5fODJT26oLFekLvx3mpzfGz8l39KzDM1i6+7Mtg7DnA3kvfVIuZBNDwqoTS6hH
KcGa0MJDgzZQqJ9Ke/7T7eY+HzktUBLjzUY2kv5VV8Ji0p6xY27jT73xiDov00ZbBFN+xBtx
2iRmjjgnPtjt/zU5sLiv9fUOA+Pb53gBT+mXMNx2tsg07Kmuz7vfjR5ydoY7guyB3X1vUK9y
AmCW1Gq67eRG934SujZFikO/oZUrwRrQu2jj5v8B7xwtcCFCdpZAIRabD4BTglvPiQEiBBAB
AgAMBQJKjl+9BQMAEnUAAAoJEJcQuJvKV618DTwH/3DzIl1zwr6TTtTfTBH9FSDdhvaUEPKC
bLT3WZWzIHREaLEENcQ85cGoYoBeJXVBIwBczZUpGy4pqFjYcWQ9vKFm2Nt1Nrs+v9tKc+9G
ECH0Y1a+9GDYqnepcN2O/3HLASCEpXFwQhVe01G+lupGgqYfMgTG9RByTkMzVXB9ER5gijGC
zjTflYAOFUx2eBBLYa3w/ZZpT+nwRmEUaDpfwq06UPrzMZuhol7SGPZUNz4lz4p2NF8Td9bk
hOiJ3+gORRohbq0HdaRdvSDoP/aGsQltfeF5p0KEcpIHx5B05H1twIkOGFTxyx3nTWqauEJy
2a+Wl5ZBl0hB2TqwAE9Z54KJASIEEAECAAwFAkqgEkcFAwASdQAACgkQlxC4m8pXrXwyXwf/
UPzz+D+n19JWivha7laUxuDzMQCKTcEjFCu4QVZ1rqcBFPoz0Tt74/X75QdmxZizqX1E6lbF
EsbVjL2Mt5zZjedS1vbSbrmn4hV4pHZr08dbflZkNX105g8ZlpsqQ7VyUt5YtWCn0tGNn4B5
Eb6WMeqxQteujV3B7AtMH+CD0ja+A2/p0rHIpqScz8aupksBMCrYqhoT+7/qXNEVkjNmcu2N
mHxfv6dL5Xy/0iJjie2umStu8WTfRTpYmnv2gEhbCdb/zhFvG61GgTBJqv9MvBVGRxnJFd4l
NqlucsadD+UM7WjV3v5VuN2r9KD9wocd/s22ELCRA2wKccvR/nWBkIkBIgQQAQIADAUCSqgQ
AAUDABJ1AAAKCRCXELibyletfAT8B/9cPhH8DlHoiv+cK8rAJMomZqVqOyy4BwsRrakycVlg
7/yvMs74anynSoUf0LgsXADQ29Hmrpf+zC5E5/jPGWNK81x2VBVoB8nZkMSAnkZfOw+mWu9I

123

Verifying Package Integrity Using MD5 Checksums or GnuPG

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

124

Create a mysql User and Group

To install a compressed tar file binary distribution, unpack it at the installation location you choose
(typically /usr/local/mysql). This creates the directories shown in the following table.

Table 2.3 MySQL Installation Layout for Generic Unix/Linux Binary Package

Directory

bin

docs

man

include

lib

share

Contents of Directory

mysqld server, client and utility programs

MySQL manual in Info format

Unix manual pages

Include (header) files

Libraries

Error messages, dictionary, and SQL for database
installation

support-files

Miscellaneous support files

Debug versions of the mysqld binary are available as mysqld-debug. To compile your own debug
version of MySQL from a source distribution, use the appropriate configuration options to enable
debugging support. See Section 2.8, “Installing MySQL from Source”.

To install and use a MySQL binary distribution, the command sequence looks like this:

$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql
$> cd /usr/local
$> tar xvf /path/to/mysql-VERSION-OS.tar.xz
$> ln -s full-path-to-mysql-VERSION-OS mysql
$> cd mysql
$> mkdir mysql-files
$> chown mysql:mysql mysql-files
$> chmod 750 mysql-files
$> bin/mysqld --initialize --user=mysql
$> bin/mysql_ssl_rsa_setup
$> bin/mysqld_safe --user=mysql &
# Next command is optional
$> cp support-files/mysql.server /etc/init.d/mysql.server

Note

This procedure assumes that you have root (administrator) access to your
system. Alternatively, you can prefix each command using the sudo (Linux) or
pfexec (Solaris) command.

The mysql-files directory provides a convenient location to use as the value for the
secure_file_priv system variable, which limits import and export operations to a specific directory.
See Section 7.1.8, “Server System Variables”.

A more detailed version of the preceding description for installing a binary distribution follows.

Create a mysql User and Group

If your system does not already have a user and group to use for running mysqld, you may need to
create them. The following commands add the mysql group and the mysql user. You might want to
call the user and group something else instead of mysql. If so, substitute the appropriate name in the
following instructions. The syntax for useradd and groupadd may differ slightly on different versions
of Unix/Linux, or they may have different names such as adduser and addgroup.

$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql

127

Obtain and Unpack the Distribution

Note

Because the user is required only for ownership purposes, not login purposes,
the useradd command uses the -r and -s /bin/false options to create
a user that does not have login permissions to your server host. Omit these
options if your useradd does not support them.

Obtain and Unpack the Distribution

Pick the directory under which you want to unpack the distribution and change location into it. The
example here unpacks the distribution under /usr/local. The instructions, therefore, assume that
you have permission to create files and directories in /usr/local. If that directory is protected, you
must perform the installation as root.

$> cd /usr/local

Obtain a distribution file using the instructions in Section 2.1.3, “How to Get MySQL”. For a given
release, binary distributions for all platforms are built from the same MySQL source distribution.

Unpack the distribution, which creates the installation directory. tar can uncompress and unpack the
distribution if it has z option support:

$> tar xvf /path/to/mysql-VERSION-OS.tar.xz

The tar command creates a directory named mysql-VERSION-OS.

To install MySQL from a compressed tar file binary distribution, your system must have GNU XZ
Utils to uncompress the distribution and a reasonable tar to unpack it.

Note

The compression algorithm changed from Gzip to XZ in MySQL Server 8.0.12;
and the generic binary's file extension changed from .tar.gz to .tar.xz.

GNU tar is known to work. The standard tar provided with some operating systems is not able to
unpack the long file names in the MySQL distribution. You should download and install GNU tar, or if
available, use a preinstalled version of GNU tar. Usually this is available as gnutar, gtar, or as tar
within a GNU or Free Software directory, such as /usr/sfw/bin or /usr/local/bin. GNU tar is
available from http://www.gnu.org/software/tar/.

If your tar does not support the xz format then use the xz command to unpack the distribution and
tar to unpack it. Replace the preceding tar command with the following alternative command to
uncompress and extract the distribution:

$> xz -dc /path/to/mysql-VERSION-OS.tar.xz | tar x

Next, create a symbolic link to the installation directory created by tar:

$> ln -s full-path-to-mysql-VERSION-OS mysql

The ln command makes a symbolic link to the installation directory. This enables you to refer more
easily to it as /usr/local/mysql. To avoid having to type the path name of client programs always
when you are working with MySQL, you can add the /usr/local/mysql/bin directory to your PATH
variable:

$> export PATH=$PATH:/usr/local/mysql/bin

Perform Postinstallation Setup

The remainder of the installation process involves setting distribution ownership and access
permissions, initializing the data directory, starting the MySQL server, and setting up the configuration
file. For instructions, see Section 2.9, “Postinstallation Setup and Testing”.

128

Installing MySQL on Microsoft Windows

2.3 Installing MySQL on Microsoft Windows

Important

MySQL 8.0 Server requires the Microsoft Visual C++ 2019 Redistributable
Package to run on Windows platforms. Users should make sure the package
has been installed on the system before installing the server. The package is
available at the Microsoft Download Center. Additionally, MySQL debug binaries
require Visual Studio 2019 to be installed.

MySQL is available for Microsoft Windows 64-bit operating systems only. For supported Windows
platform information, see https://www.mysql.com/support/supportedplatforms/database.html.

There are different methods to install MySQL on Microsoft Windows.

MySQL Installer Method

The simplest and recommended method is to download MySQL Installer (for Windows) and let it install
and configure a specific version of MySQL Server as follows:

1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/ and execute it.

Note

Unlike the standard MySQL Installer, the smaller web-community version
does not bundle any MySQL applications, but downloads only the MySQL
products you choose to install.

2. Determine the setup type to use for the initial installation of MySQL products. For example:

• Developer Default: Provides a setup type that includes the selected version of MySQL Server

and other MySQL tools related to MySQL development, such as MySQL Workbench.

• Server Only: Provides a setup for the selected version of MySQL Server without other products.

• Custom: Enables you to select any version of MySQL Server and other MySQL products.

3.

Install the server instance (and products) and then begin the server configuration by following
the onscreen instructions. For more information about each individual step, see MySQL Server
Configuration with MySQL Installer.

MySQL is now installed. If you configured MySQL as a service, then Windows automatically starts
the MySQL server every time you restart the system. Also, this process installs the MySQL Installer
application on the local host, which you can use later to upgrade or reconfigure MySQL server.

Note

If you installed MySQL Workbench on your system, consider using it to check
your new MySQL server connection. By default, the program automatically start
after installing MySQL.

Additional Installation Information

It is possible to run MySQL as a standard application or as a Windows service. By using a service,
you can monitor and control the operation of the server through the standard Windows service
management tools. For more information, see Section 2.3.4.8, “Starting MySQL as a Windows
Service”.

To accommodate the RESTART statement, the MySQL server forks when run as a service or
standalone, to enable a monitor process to supervise the server process. In this case, there are two
mysqld processes. If RESTART capability is not required, the server can be started with the --no-
monitor option. See Section 15.7.8.8, “RESTART Statement”.

129

MySQL Installation Layout on Microsoft Windows

If you need tables with a size larger than 4GB, install MySQL on an NTFS or newer file system. Do
not forget to use MAX_ROWS and AVG_ROW_LENGTH when you create tables. See Section 15.1.20,
“CREATE TABLE Statement”.

• MySQL and Virus Checking Software

Virus-scanning software such as Norton/Symantec Anti-Virus on directories containing MySQL data
and temporary tables can cause issues, both in terms of the performance of MySQL and the virus-
scanning software misidentifying the contents of the files as containing spam. This is due to the
fingerprinting mechanism used by the virus-scanning software, and the way in which MySQL rapidly
updates different files, which may be identified as a potential security risk.

After installing MySQL Server, it is recommended that you disable virus scanning on the main
directory (datadir) used to store your MySQL table data. There is usually a system built into the
virus-scanning software to enable specific directories to be ignored.

In addition, by default, MySQL creates temporary files in the standard Windows temporary directory.
To prevent the temporary files also being scanned, configure a separate temporary directory for
MySQL temporary files and add this directory to the virus scanning exclusion list. To do this, add
a configuration option for the tmpdir parameter to your my.ini configuration file. For more
information, see Section 2.3.4.2, “Creating an Option File”.

2.3.1 MySQL Installation Layout on Microsoft Windows

For MySQL 8.0 on Windows, the default installation directory is C:\Program Files\MySQL\MySQL
Server 8.0 for installations performed with MySQL Installer. If you use the ZIP archive method
to install MySQL, you may prefer to install in C:\mysql. However, the layout of the subdirectories
remains the same.

All of the files are located within this parent directory, using the structure shown in the following table.

Table 2.4 Default MySQL Installation Layout for Microsoft Windows

Directory

bin

%PROGRAMDATA%\MySQL
\MySQL Server 8.0\

Contents of Directory

Notes

mysqld server, client and utility
programs

Log files, databases

docs

Release documentation

include

lib

share

Include (header) files

Libraries

Miscellaneous support files,
including error messages,
character set files, sample
configuration files, SQL for
database installation

The Windows system variable
%PROGRAMDATA% defaults to C:
\ProgramData.

With MySQL Installer, use the
Modify operation to select this
optional folder.

Silent Installation Methods

Use MySQL Installer, see Section 2.3.3.5, “MySQL Installer Console Reference”.

2.3.2 Choosing an Installation Package

For MySQL 8.0, there are multiple installation package formats to choose from when installing MySQL
on Windows. The package formats described in this section are:

131

Choosing an Installation Package

• MySQL Installer

• MySQL noinstall ZIP Archives

• MySQL Docker Images

Program Database (PDB) files (with file name extension pdb) provide information for debugging your
MySQL installation in the event of a problem. These files are included in ZIP Archive distributions (but
not MSI distributions) of MySQL.

MySQL Installer

This package has a file name similar to mysql-installer-community-8.0.42.0.msi or mysql-
installer-commercial-8.0.42.0.msi, and utilizes MSIs to install MySQL server and other
products automatically. MySQL Installer downloads and applies updates to itself, and to each of the
installed products. It also configures the installed MySQL server (including a sandbox InnoDB cluster
test setup) and MySQL Router. MySQL Installer is recommended for most users.

MySQL Installer can install and manage (add, modify, upgrade, and remove) many other MySQL
products, including:

• Applications – MySQL Workbench, MySQL for Visual Studio, MySQL Shell, and MySQL Router (see

https://dev.mysql.com/doc/mysql-compat-matrix/en/)

• Connectors – MySQL Connector/C++, MySQL Connector/NET, Connector/ODBC, MySQL

Connector/Python, MySQL Connector/J, MySQL Connector/Node.js

• Documentation – MySQL Manual (PDF format), samples and examples

MySQL Installer operates on all MySQL supported versions of Windows (see https://www.mysql.com/
support/supportedplatforms/database.html).

Note

Because MySQL Installer is not a native component of Microsoft Windows and
depends on .NET, it does not work with minimal installation options like the
Server Core version of Windows Server.

For instructions on how to install MySQL using MySQL Installer, see Section 2.3.3, “MySQL Installer for
Windows”.

MySQL noinstall ZIP Archives

These packages contain the files found in the complete MySQL Server installation package, with the
exception of the GUI. This format does not include an automated installer, and must be manually
installed and configured.

The noinstall ZIP archives are split into two separate compressed files. The main package is
named mysql-VERSION-winx64.zip. This contains the components needed to use MySQL on your
system. The optional MySQL test suite, MySQL benchmark suite, and debugging binaries/information
components (including PDB files) are in a separate compressed file named mysql-VERSION-
winx64-debug-test.zip.

If you choose to install a noinstall ZIP archive, see Section 2.3.4, “Installing MySQL on Microsoft
Windows Using a noinstall ZIP Archive”.

MySQL Docker Images

For information on using the MySQL Docker images provided by Oracle on Windows platform, see
Section 2.5.6.3, “Deploying MySQL on Windows and Other Non-Linux Platforms with Docker”.

132

MySQL Installer for Windows

Warning

The MySQL Docker images provided by Oracle are built specifically for Linux
platforms. Other platforms are not supported, and users running the MySQL
Docker images from Oracle on them are doing so at their own risk.

2.3.3 MySQL Installer for Windows

MySQL Installer is a standalone application designed to ease the complexity of installing and
configuring MySQL products that run on Microsoft Windows. It is downloaded with and supports the
following MySQL products:

• MySQL Servers

MySQL Installer can install and manage multiple, separate MySQL server instances on the same
host at the same time. For example, MySQL Installer can install, configure, and upgrade separate
instances of MySQL 5.7 and MySQL 8.0 on the same host. MySQL Installer does not permit server
upgrades between major and minor version numbers, but does permit upgrades within a release
series (such as 8.0.36 to 8.0.37).

Note

MySQL Installer cannot install both Community and Commercial releases of
MySQL server on the same host. If you require both releases on the same
host, consider using the ZIP archive distribution to install one of the releases.

• MySQL Applications

MySQL Workbench, MySQL Shell, and MySQL Router.

• MySQL Connectors

These are not supported, instead install from https://dev.mysql.com/downloads/. These connectors
include MySQL Connector/NET, MySQL Connector/Python, MySQL Connector/ODBC, MySQL
Connector/J, MySQL Connector/Node.js, and MySQL Connector/C++.

Note

The connectors were bundled before MySQL Installer 1.6.7 (MySQL Server
8.0.34), and MySQL Installer could install each connector up to version 8.0.33
until MySQL Installer 1.6.11 (MySQL Server 8.0.37). MySQL Installer now
only detects these old connector versions to uninstall them.

Installation Requirements

MySQL Installer requires Microsoft .NET Framework 4.5.2 or later. If this version is not installed on the
host computer, you can download it by visiting the Microsoft website.

To invoke MySQL Installer after a successful installation:

1. Right-click Windows Start, select Run, and then click Browse. Navigate to Program Files

(x86) > MySQL > MySQL Installer for Windows to open the program folder.

2. Select one of the following files:

• MySQLInstaller.exe to open the graphical application.

• MySQLInstallerConsole.exe to open the command-line application.

3. Click Open and then click OK in the Run window. If you are prompted to allow the application to

make changes to the device, select Yes.

133

MySQL Installer for Windows

Each time you invoke MySQL Installer, the initialization process looks for the presence of an internet
connection and prompts you to enable offline mode if it finds no internet access (and offline mode
is disabled). Select Yes to run MySQL Installer without internet-connection capabilities. MySQL
product availability is limited to only those products currently in the product cache when you enable
offline mode. To download MySQL products, click the offline mode Disable quick action shown on the
dashboard.

An internet connection is required to download a manifest containing metadata for the latest MySQL
products that are not part of a full bundle. MySQL Installer attempts to download the manifest when
you start the application for the first time and then periodically in configurable intervals (see MySQL
Installer options). Alternatively, you can retrieve an updated manifest manually by clicking Catalog in
the MySQL Installer dashboard.

Note

If the first-time or subsequent manifest download is unsuccessful, an error
is logged and you may have limited access to MySQL products during your
session. MySQL Installer attempts to download the manifest with each startup
until the initial manifest structure is updated. For help finding a product, see
Locating Products to Install.

MySQL Installer Community Release

Download software from https://dev.mysql.com/downloads/installer/ to install the Community release of
all MySQL products for Windows. Select one of the following MySQL Installer package options:

• Web: Contains MySQL Installer and configuration files only. The web package option downloads only
the MySQL products you select to install, but it requires an internet connection for each download.
The size of this file is approximately 2 MB. The file name has the form mysql-installer-
community-web-VERSION.N.msi in which VERSION is the MySQL server version number such
as 8.0 and N is the package number, which begins at 0.

• Full or Current Bundle: Bundles all of the MySQL products for Windows (including the MySQL

server). The file size is over 300 MB, and the name has the form mysql-installer-
community-VERSION.N.msi in which VERSION is the MySQL Server version number such as 8.0
and N is the package number, which begins at 0.

MySQL Installer Commercial Release

Download software from https://edelivery.oracle.com/ to install the Commercial release (Standard or
Enterprise Edition) of MySQL products for Windows. If you are logged in to your My Oracle Support
(MOS) account, the Commercial release includes all of the current and previous GA versions available
in the Community release, but it excludes development-milestone versions. When you are not logged
in, you see only the list of bundled products that you downloaded already.

The Commercial release also includes the following products:

• Workbench SE/EE

• MySQL Enterprise Backup

• MySQL Enterprise Firewall

The Commercial release integrates with your MOS account. For knowledge-base content and patches,
see My Oracle Support.

2.3.3.1 MySQL Installer Initial Setup

• Choosing a Setup Type

• Path Conflicts

• Check Requirements

134

MySQL Installer for Windows

• MySQL Installer Configuration Files

When you download MySQL Installer for the first time, a setup wizard guides you through the initial
installation of MySQL products. As the following figure shows, the initial setup is a one-time activity in
the overall process. MySQL Installer detects existing MySQL products installed on the host during its
initial setup and adds them to the list of products to be managed.

Figure 2.7 MySQL Installer Process Overview

MySQL Installer extracts configuration files (described later) to the hard drive of the host during the
initial setup. Although MySQL Installer is a 32-bit application, it can install both 32-bit and 64-bit
binaries.

The initial setup adds a link to the Start menu under the MySQL folder group. Click Start, MySQL, and
MySQL Installer - [Community | Commercial] to open the community or commercial release of the
graphical tool.

Choosing a Setup Type

During the initial setup, you are prompted to select the MySQL products to be installed on the host.
One alternative is to use a predetermined setup type that matches your setup requirements. By default,
both GA and pre-release products are included in the download and installation with the Client only
and Full setup types. Select the Only install GA products option to restrict the product set to include
GA products only when using these setup types.

Note

Commercial-only MySQL products, such as MySQL Enterprise Backup, are
available to select and install if you are using the Commercial version of MySQL
Installer (see MySQL Installer Commercial Release).

Choosing one of the following setup types determines the initial installation only and does not limit your
ability to install or update MySQL products for Windows later:

• Server only: Only install the MySQL server. This setup type installs the general availability (GA) or
development release server that you selected when you downloaded MySQL Installer. It uses the
default installation and data paths.

• Client only: Only install the most recent MySQL applications (such as MySQL Shell, MySQL Router,
and MySQL Workbench). This setup type excludes MySQL server or the client programs typically
bundled with the server, such as mysql or mysqladmin.

• Full: Install all available MySQL products, excluding MySQL connectors.

• Custom: The custom setup type enables you to filter and select individual MySQL products from the

MySQL Installer catalog.

Use the Custom setup type to install:

• A product or product version that is not available from the usual download locations. The catalog
contains all product releases, including the other releases between pre-release (or development)
and GA.

135

MySQL Installer for Windows

• An instance of MySQL server using an alternative installation path, data path, or both. For

instructions on how to adjust the paths, see Section 2.3.3.2, “Setting Alternative Server Paths with
MySQL Installer”.

• Two or more MySQL server versions on the same host at the same time (for example, 5.7 and

8.0).

• A specific combination of products and features not offered as a predetermine setup type. For
example, you can install a single product, such as MySQL Workbench, instead of installing all
client applications for Windows.

Path Conflicts

When the default installation or data folder (required by MySQL server) for a product to be installed
already exists on the host, the wizard displays the Path Conflict step to identify each conflict and
enable you to take action to avoid having files in the existing folder overwritten by the new installation.
You see this step in the initial setup only when MySQL Installer detects a conflict.

To resolve the path conflict, do one of the following:

• Select a product from the list to display the conflict options. A warning symbol indicates which path is

in conflict. Use the browse button to choose a new path and then click Next.

• Click Back to choose a different setup type or product version, if applicable. The Custom setup type

enables you to select individual product versions.

• Click Next to ignore the conflict and overwrite files in the existing folder.

• Delete the existing product. Click Cancel to stop the initial setup and close MySQL Installer. Open
MySQL Installer again from the Start menu and delete the installed product from the host using the
Delete operation from the MySQL Installer dashboard.

Check Requirements

MySQL Installer uses entries in the package-rules.xml file to determine whether the prerequisite
software for each product is installed on the host. When the requirements check fails, MySQL Installer
displays the Check Requirements step to help you update the host. Requirements are evaluated
each time you download a new product (or version) for installation. The following figure identifies and
describes the key areas of this step.

Figure 2.8 Check Requirements

136

MySQL Installer for Windows

Description of Check Requirements Elements

1. Shows the current step in the initial setup. Steps in this list may change slightly depending on the
products already installed on the host, the availability of prerequisite software, and the products to
be installed on the host.

2. Lists all pending installation requirements by product and indicates the status as follows:

• A blank space in the Status column means that MySQL Installer can attempt to download and

install the required software for you.

• The word Manual in the Status column means that you must satisfy the requirement manually.

Select each product in the list to see its requirement details.

3. Describes the requirement in detail to assist you with each manual resolution. When possible, a
download URL is provided. After you download and install the required software, click Check to
verify that the requirement has been met.

4. Provides the following set operations to proceed:

• Back – Return to the previous step. This action enables you to select a different the setup type.

• Execute – Have MySQL Installer attempt to download and install the required software for all

items without a manual status. Manual requirements are resolved by you and verified by clicking
Check.

• Next – Do not execute the request to apply the requirements automatically and proceed to the

installation without including the products that fail the check requirements step.

• Cancel – Stop the installation of MySQL products. Because MySQL Installer is already installed,
the initial setup begins again when you open MySQL Installer from the Start menu and click Add
from the dashboard. For a description of the available management operations, see Product
Catalog.

MySQL Installer Configuration Files

All MySQL Installer files are located within the C:\Program Files (x86) and C:\ProgramData
folders. The following table describes the files and folders that define MySQL Installer as a standalone
application.

Note

Installed MySQL products are neither altered nor removed when you update or
uninstall MySQL Installer.

Table 2.5 MySQL Installer Configuration Files

File or Folder

Description

Folder Hierarchy

MySQL Installer for
Windows

Templates

C:\Program Files (x86)

This folder contains all
of the files needed to
run MySQL Installer and
MySQLInstallerConsole.exe,
a command-line program with
similar functionality.

The Templates folder has one
file for each version of MySQL
server. Template files contain
keys and formulas to calculate
some values dynamically.

C:\ProgramData\MySQL
\MySQL Installer for
Windows\Manifest

137

MySQL Installer for Windows

File or Folder

Description

Folder Hierarchy

package-rules.xml

products.xml

Product Cache

This file contains the
prerequisites for every product to
be installed.

C:\ProgramData\MySQL
\MySQL Installer for
Windows\Manifest

The products file (or product
catalog) contains a list of all
products available for download.

C:\ProgramData\MySQL
\MySQL Installer for
Windows\Manifest

The Product Cache folder
contains all standalone .msi
files bundled with the full
package or downloaded
afterward.

C:\ProgramData\MySQL
\MySQL Installer for
Windows

2.3.3.2 Setting Alternative Server Paths with MySQL Installer

You can change the default installation path, the data path, or both when you install MySQL server.
After you have installed the server, the paths cannot be altered without removing and reinstalling the
server instance.

Note

Starting with MySQL Installer 1.4.39, if you move the data directory of an
installed server manually, MySQL Installer identifies the change and can
process a reconfiguration operation without errors.

To change paths for MySQL server

1.

Identify the MySQL server to change and enable the Advanced Options link as follows:

a. Navigate to the Select Products page by doing one of the following:

i.

ii.

If this is an initial setup of MySQL Installer, select the Custom setup type and click Next.

If MySQL Installer is installed on your computer, click Add from the dashboard.

b. Click Edit to apply a filter on the product list shown in Available Products (see Locating

Products to Install).

c. With the server instance selected, use the arrow to move the selected server to the Products

To Be Installed list.

d. Click the server to select it. When you select the server, the Advanced Options link is

enabled below the list of products to be installed (see the following figure).

2. Click Advanced Options to open a dialog box where you can enter alternative path names. After

the path names are validated, click Next to continue with the configuration steps.

138

MySQL Installer for Windows

Figure 2.9 Change MySQL Server Path

2.3.3.3 Installation Workflows with MySQL Installer

MySQL Installer provides a wizard-like tool to install and configure new MySQL products for Windows.
Unlike the initial setup, which runs only once, MySQL Installer invokes the wizard each time you
download or install a new product. For first-time installations, the steps of the initial setup proceed
directly into the steps of the installation. For assistance with product selection, see Locating Products to
Install.

Note

Full permissions are granted to the user executing MySQL Installer to all
generated files, such as my.ini. This does not apply to files and directories for
specific products, such as the MySQL server data directory in %ProgramData%
that is owned by SYSTEM.

Products installed and configured on a host follow a general pattern that might require your input during
the various steps. If you attempt to install a product that is incompatible with the existing MySQL server
version (or a version selected for upgrade), you are alerted about the possible mismatch.

MySQL Installer provides the following sequence of actions that apply to different workflows:

• Select Products.

 If you selected the Custom setup type during the initial setup or clicked Add

from the MySQL Installer dashboard, MySQL Installer includes this action in the sidebar. From
this page, you can apply a filter to modify the Available Products list and then select one or more
products to move (using arrow keys) to the Products To Be Installed list.

Select the check box on this page to activate the Select Features action where you can customize
the products features after the product is downloaded.

• Download.

 If you installed the full (not web) MySQL Installer package, all .msi files were loaded

to the Product Cache folder during the initial setup and are not downloaded again. Otherwise, click
Execute to begin the download. The status of each product changes from Ready to Download, to
Downloading, and then to Downloaded.

To retry a single unsuccessful download, click the Try Again link.

To retry all unsuccessful downloads, click Try All.

139

MySQL Installer for Windows

• Select Features To Install (disabled by default).

 After MySQL Installer downloads a product's

.msi file, you can customize the features if you enabled the optional check box previously during the
Select Products action.

To customize product features after the installation, click Modify in the MySQL Installer dashboard.

• Installation.

 The status of each product in the list changes from Ready to Install, to

Installing, and lastly to Complete. During the process, click Show Details to view the
installation actions.

If you cancel the installation at this point, the products are installed, but the server (if installed) is not
yet configured. To restart the server configuration, open MySQL Installer from the Start menu and
click Reconfigure next to the appropriate server in the dashboard.

• Product configuration.

 This step applies to MySQL Server, MySQL Router, and samples only.
The status for each item in the list should indicate Ready to Configure. Click Next to start the
configuration wizard for all items in the list. The configuration options presented during this step are
specific to the version of database or router that you selected to install.

Click Execute to begin applying the configuration options or click Back (repeatedly) to return to each
configuration page.

• Installation complete.

 This step finalizes the installation for products that do not require

configuration. It enables you to copy the log to a clipboard and to start certain applications, such as
MySQL Workbench and MySQL Shell. Click Finish to open the MySQL Installer dashboard.

MySQL Server Configuration with MySQL Installer

MySQL Installer performs the initial configuration of the MySQL server. For example:

• It creates the configuration file (my.ini) that is used to configure the MySQL server. The values

written to this file are influenced by choices you make during the installation process. Some
definitions are host dependent.

• By default, a Windows service for the MySQL server is added.

• Provides default installation and data paths for MySQL server. For instructions on how to change the

default paths, see Section 2.3.3.2, “Setting Alternative Server Paths with MySQL Installer”.

• It can optionally create MySQL server user accounts with configurable permissions based on general
roles, such as DB Administrator, DB Designer, and Backup Admin. It optionally creates a Windows
user named MysqlSys with limited privileges, which would then run the MySQL Server.

User accounts may also be added and configured in MySQL Workbench.

• Checking Show Advanced Options enables additional Logging Options to be set. This includes

defining custom file paths for the error log, general log, slow query log (including the configuration of
seconds it requires to execute a query), and the binary log.

During the configuration process, click Next to proceed to the next step or Back to return to the
previous step. Click Execute at the final step to apply the server configuration.

The sections that follow describe the server configuration options that apply to MySQL server on
Windows. The server version you installed will determine which steps and options you can configure.
Configuring MySQL server may include some or all of the steps.

Type and Networking

• Server Configuration Type

Choose the MySQL server configuration type that describes your setup. This setting defines the
amount of system resources (memory) to assign to your MySQL server instance.

140

MySQL Installer for Windows

Click Add User or Edit User to create or modify MySQL user accounts with predefined roles. Next,
enter the required account credentials:

• User Name: MySQL user names can be up to 32 characters long.

• Host: Select localhost for local connections only or <All Hosts (%)> when remote

connections to the server are required.

• Role: Each predefined role, such as DB Admin, is configured with its own set of privileges. For
example, the DB Admin role has more privileges than the DB Designer role. The Role drop-
down list contains a description of each role.

• Password: Password strength assessment is performed while you type the password. Passwords

must be confirmed. MySQL permits a blank or empty password (considered to be insecure).

MySQL Installer Commercial Release Only:
commercial product, also supports an authentication method that performs external authentication on
Windows. Accounts authenticated by the Windows operating system can access the MySQL server
without providing an additional password.

 MySQL Enterprise Edition for Windows, a

To create a new MySQL account that uses Windows authentication, enter the user name
and then select a value for Host and Role. Click Windows authentication to enable the
authentication_windows plugin. In the Windows Security Tokens area, enter a token for each
Windows user (or group) who can authenticate with the MySQL user name. MySQL accounts can
include security tokens for both local Windows users and Windows users that belong to a domain.
Multiple security tokens are separated by the semicolon character (;) and use the following format
for local and domain accounts:

• Local account

Enter the simple Windows user name as the security token for each local user or group; for
example, finley;jeffrey;admin.

• Domain account

Use standard Windows syntax (domain\domainuser) or MySQL syntax (domain\
\domainuser) to enter Windows domain users and groups.

For domain accounts, you may need to use the credentials of an administrator within the domain
if the account running MySQL Installer lacks the permissions to query the Active Directory. If this
is the case, select Validate Active Directory users with to activate the domain administrator
credentials.

Windows authentication permits you to test all of the security tokens each time you add or modify
a token. Click Test Security Tokens to validate (or revalidate) each token. Invalid tokens generate
a descriptive error message along with a red X icon and red token text. When all tokens resolve as
valid (green text without an X icon), you can click OK to save the changes.

Windows Service

On the Windows platform, MySQL server can run as a named service managed by the operating
system and be configured to start up automatically when Windows starts. Alternatively, you can
configure MySQL server to run as an executable program that requires manual configuration.

• Configure MySQL server as a Windows service (Selected by default.)

When the default configuration option is selected, you can also select the following:

• Start the MySQL Server at System Startup

143

MySQL Installer for Windows

Advanced Options

This step is available if the Show Advanced Configuration check box was selected during the Type
and Networking step. To enable this step now, click Back to return to the Type and Networking step
and select the check box.

The advanced-configuration options include:

• Server ID

Set the unique identifier used in a replication topology. If binary logging is enabled, you must specify
a server ID. The default ID value depends on the server version. For more information, see the
description of the server_id system variable.

• Table Names Case

You can set the following options during the initial and subsequent configuration the server. For the
MySQL 8.0 release series, these options apply only to the initial configuration of the server.

• Lower Case

Sets the lower_case_table_names option value to 1 (default), in which table names are stored
in lowercase on disk and comparisons are not case-sensitive.

• Preserve Given Case

Sets the lower_case_table_names option value to 2, in which table names are stored as given
but compared in lowercase.

Apply Server Configuration

All configuration settings are applied to the MySQL server when you click Execute. Use the
Configuration Steps tab to follow the progress of each action; the icon for each toggles from white to
green (with a check mark) on success. Otherwise, the process stops and displays an error message if
an individual action times out. Click the Log tab to view the log.

When the installation completes successfully and you click Finish, MySQL Installer and the installed
MySQL products are added to the Microsoft Windows Start menu under the MySQL group. Opening
MySQL Installer loads the dashboard where installed MySQL products are listed and other MySQL
Installer operations are available.

MySQL Router Configuration with MySQL Installer

During the initial setup, choose any predetermined setup type, except Server only, to install the
latest GA version of the tools. Use the Custom setup type to install an individual tool or specific
version. If MySQL Installer is installed on the host already, use the Add operation to select and install
tools from the MySQL Installer dashboard.

MySQL Router Configuration

MySQL Installer provides a configuration wizard that can bootstrap an installed instance of MySQL
Router 8.0 to direct traffic between MySQL applications and an InnoDB Cluster. When configured,
MySQL Router runs as a local Windows service.

Note

You are prompted to configure MySQL Router after the initial installation and
when you reconfigure an installed router explicitly. In contrast, the upgrade
operation does not require or prompt you to configure the upgraded product.

To configure MySQL Router, do the following:

145

MySQL Installer for Windows

1. Set up InnoDB Cluster.

2. Using MySQL Installer, download and install the MySQL Router application. After the installation
finishes, the configuration wizard prompts you for information. Select the Configure MySQL
Router for InnoDB Cluster check box to begin the configuration and provide the following
configuration values:

• Hostname: Host name of the primary (seed) server in the InnoDB Cluster (localhost by

default).

• Port: The port number of the primary (seed) server in the InnoDB Cluster (3306 by default).

• Management User: An administrative user with root-level privileges.

• Password: The password for the management user.

• Classic MySQL protocol connections to InnoDB Cluster

Read/Write: Set the first base port number to one that is unused (between 80 and 65532) and
the wizard will select the remaining ports for you.

The figure that follows shows an example of the MySQL Router configuration page, with the first
base port number specified as 6446 and the remaining ports set by the wizard to 6447, 6448, and
6449.

Figure 2.10 MySQL Router Configuration

3. Click Next and then Execute to apply the configuration. Click Finish to close MySQL Installer or

return to the MySQL Installer dashboard.

After configuring MySQL Router, the root account exists in the user table as root@localhost (local)
only, instead of root@% (remote). Regardless of where the router and client are located, even if both
are located on the same host as the seed server, any connection that passes through the router is
viewed by server as being remote, not local. As a result, a connection made to the server using the
local host (see the example that follows), does not authenticate.

$> \c root@localhost:6446

2.3.3.4 MySQL Installer Product Catalog and Dashboard

This section describes the MySQL Installer product catalog, the dashboard, and other actions related to
product selection and upgrades.

146

MySQL Installer for Windows

• Product Catalog

• MySQL Installer Dashboard

• Locating Products to Install

• Upgrading MySQL Server

• Removing MySQL Server

• Upgrading MySQL Installer

Product Catalog

The product catalog stores the complete list of released MySQL products for Microsoft Windows that
are available to download from MySQL Downloads. By default, and when an Internet connection is
present, MySQL Installer attempts to update the catalog at startup every seven days. You can also
update the catalog manually from the dashboard (described later).

An up-to-date catalog performs the following actions:

• Populates the Available Products pane of the Select Products page. This step appears when you

select:

• The Custom setup type during the initial setup.

• The Add operation from the dashboard.

• Identifies when product updates are available for the installed products listed in the dashboard.

The catalog includes all development releases (Pre-Release), general releases (Current GA), and
minor releases (Other Releases). Products in the catalog will vary somewhat, depending on the
MySQL Installer release that you download.

MySQL Installer Dashboard

The MySQL Installer dashboard is the default view that you see when you start MySQL Installer after
the initial setup finishes. If you closed MySQL Installer before the setup was finished, MySQL Installer
resumes the initial setup before it displays the dashboard.

Note

Products covered under Oracle Lifetime Sustaining Support, if installed, may
appear in the dashboard. These products, such as MySQL for Excel and
MySQL Notifier, can be modified or removed only.

147

MySQL Installer for Windows

Figure 2.11 MySQL Installer Dashboard Elements

Description of MySQL Installer Dashboard Elements

1. MySQL Installer dashboard operations provide a variety of actions that apply to installed products

or products listed in the catalog. To initiate the following operations, first click the operation link and
then select the product or products to manage:

• Add: This operation opens the Select Products page. From there you can adjust the filter, select
one or more products to download (as needed), and begin the installation. For hints about using
the filter, see Locating Products to Install.

Use the directional arrows to move each product from the Available Products column to
the Products To Be Installed column. To enable the Product Features page where you can
customize features, click the related check box (disabled by default).

• Modify: Use this operation to add or remove the features associated with installed products.

Features that you can modify vary in complexity by product. When the Program Shortcut check
box is selected, the product appears in the Start menu under the MySQL group.

• Upgrade: This operation loads the Select Products to Upgrade page and populates it with all
the upgrade candidates. An installed product can have more than one upgrade version and
the operation requires a current product catalog. MySQL Installer upgrades all of the selected
products in one action. Click Show Details to view the actions performed by MySQL Installer.

• Remove: This operation opens the Remove Products page and populates it with the MySQL
products installed on the host. Select the MySQL products you want to remove (uninstall) and
then click Execute to begin the removal process. During the operation, an indicator shows the
number of steps that are executed as a percentage of all steps.

To select products to remove, do one of the following:

• Select the check box for one or more products.

• Select the Product check box to select all products.

2. The Reconfigure link in the Quick Action column next to each installed server loads the current

configuration values for the server and then cycles through all configuration steps enabling you to
change the options and values. You must provide credentials with root privileges to reconfigure

148

MySQL Installer for Windows

these items. Click the Log tab to show the output of each configuration step performed by MySQL
Installer.

On completion, MySQL Installer stops the server, applies the configuration changes, and restarts
the server for you. For a description of each configuration option, see MySQL Server Configuration
with MySQL Installer. Installed Samples and Examples associated with a specific MySQL server
version can be also be reconfigured to apply new feature settings, if any.

3. The Catalog link enables you to download the latest catalog of MySQL products manually and

then to integrate those product changes with MySQL Installer. The catalog-download action does
not perform an upgrade of the products already installed on the host. Instead, it returns to the
dashboard and adds an arrow icon to the Version column for each installed product that has a
newer version. Use the Upgrade operation to install the newer product version.

You can also use the Catalog link to display the current change history of each product without
downloading the new catalog. Select the Do not update at this time check box to view the change
history only.

4.

5.

The MySQL Installer About icon (
information about MySQL. The version number is located above the Back button.

) shows the current version of MySQL Installer and general

Tip

Always include this version number when reporting a problem with MySQL
Installer.

In addition to the About MySQL information (
side panel:

), you can also select the following icons from the

•

•

License icon (

) for MySQL Installer.

This product may include third-party software, used under license. If you are using a Commercial
release of MySQL Installer, the icon opens the MySQL Installer Commercial License Information
User Manual for licensing information, including licensing information relating to third-party
software that may be included in this Commercial release. If you are using a Community release
of MySQL Installer, the icon opens the MySQL Installer Community License Information User
Manual for licensing information, including licensing information relating to third-party software
that may be included in this Community release.

Resource links icon (
more.

) to the latest MySQL product documentation, blogs, webinars, and

The MySQL Installer Options icon (

) includes the following tabs:

• General: Enables or disables the Offline mode option. If selected, this option configures

MySQL Installer to run without depending on internet-connection capabilities. When running
MySQL Installer in offline mode, you see a warning together with a Disable quick action on
the dashboard. The warning serves to remind you that running MySQL Installer in offline mode
prevents you from downloading the latest MySQL products and product catalog updates. Offline
mode persists until you disable the option.

At startup, MySQL Installer determines whether an internet connection is present, and, if not,
prompts you to enable offline mode to resume working without a connection.

• Product Catalog: Manages the automatic catalog updates. By default, MySQL Installer checks
for catalog updates at startup every seven days. When new products or product versions are

149

MySQL Installer for Windows

available, MySQL Installer adds them to the catalog and then inserts an arrow icon (
the version number of installed products listed in the dashboard.

) next to

Use the product catalog option to enable or disable automatic updates and to reset the number of
days between automatic catalog downloads. At startup, MySQL Installer uses the number of days
you set to determine whether a download should be attempted. This action is repeated during
next startup if MySQL Installer encounters an error downloading the catalog.

• Connectivity Settings: Several operations performed by MySQL Installer require internet
access. This option enables you to use a default value to validate the connection or to use
a different URL, one selected from a list or added by you manually. With the Manual option
selected, new URLs can be added and all URLs in the list can be moved or deleted. When the
Automatic option is selected, MySQL Installer attempts to connect to each default URL in the list
(in order) until a connection is made. If no connection can be made, it raises an error.

• Proxy: MySQL Installer provides multiple proxy modes that enable you to download MySQL

products, updates, or even the product catalog in most network environments. The mode are:

• No proxy

Select this mode to prevent MySQL Installer from looking for system settings. This mode
disables any proxy settings.

• Automatic

Select this mode to have MySQL Installer look for system settings and to use those settings if
found, or to use no proxy if nothing is found. This mode is the default.

• Manual

Select this mode to have MySQL Installer use your authentication details to configuration proxy
access to the internet. Specifically:

• A proxy-server address (http://address-to-server) and port number

• A user name and password for authentication

Locating Products to Install

MySQL products in the catalog are listed by category: MySQL Servers, Applications, MySQL
Connectors, and Documentation. Only the latest GA versions appear in the Available Products pane
by default. If you are looking for a pre-release or older version of a product, it may not be visible in the
default list.

Note

Keep the product catalog up-to-date. Click Catalog on the MySQL Installer
dashboard to download the latest manifest.

To change the default product list, click Add in the dashboard to open the Select Products page, and
then click Edit to open the dialog box shown in the figure that follows. Modify the settings and then click
Filter.

150

MySQL Installer for Windows

Figure 2.12 Filter Available Products

Reset one or more of the following fields to modify the list of available products:

• Text: Filter by text.

• Category: All Software (default), MySQL Servers, Applications, MySQL Connectors, or

Documentation (for samples and documentation).

• Maturity: Current Bundle (appears initially with the full package only), Pre-Release, Current GA, or
Other Releases. If you see a warning, confirm that you have the most recent product manifest by
clicking Catalog on the MySQL Installer dashboard. If MySQL Installer is unable to download the
manifest, the range of products you see is limited to bundled products, standalone product MSIs
located in the Product Cache folder already, or both.

Note

The Commercial release of MySQL Installer does not display any MySQL
products when you select the Pre-Release maturity filter. Products in
development are available from the Community release of MySQL Installer
only.

• Already Downloaded (the check box is deselected by default). Permits you to view and manage

downloaded products only.

• Architecture: Any (default), 32-bit, or 64-bit.

Upgrading MySQL Server

Important server upgrade conditions:

• MySQL Installer does not permit server upgrades between major release versions or minor release

versions, but does permit upgrades within a release series, such as an upgrade from 8.0.36 to
8.0.37.

• Upgrades between milestone releases (or from a milestone release to a GA release) are not
supported. Significant development changes take place in milestone releases and you may
encounter compatibility issues or problems starting the server.

• For upgrades, a check box enables you to skip the upgrade check and process for system tables,
while checking and processing data dictionary tables normally. MySQL Installer does not prompt
you with the check box when the previous server upgrade was skipped or when the server was
configured as a sandbox InnoDB Cluster. This behavior represents a change in how MySQL Server
performs an upgrade (see Section 3.4, “What the MySQL Upgrade Process Upgrades”) and it alters
the sequence of steps that MySQL Installer applies to the configuration process.

If you select Skip system tables upgrade check and process. (Not recommended), MySQL
Installer starts the upgraded server with the --upgrade=MINIMAL server option, which upgrades
the data dictionary only. If you stop and then restart the server without the --upgrade=MINIMAL
option, the server upgrades the system tables automatically, if needed.

151

MySQL Installer for Windows

4. Click Execute to begin the process. If the installed version of MySQL Installer can be upgraded,

you will be prompted to start the upgrade.

5. Click Next to review all changes to the catalog and then click Finish to return to the dashboard.

6. Verify the (new) installed version of MySQL Installer (see the previous procedure).

2.3.3.5 MySQL Installer Console Reference

MySQLInstallerConsole.exe provides command-line functionality that is similar to MySQL
Installer. This reference includes:

• MySQL Product Names

• Command Syntax

• Command Actions

The console is installed when MySQL Installer is initially executed and then available within the MySQL
Installer for Windows directory. By default, the directory location is C:\Program Files
(x86)\MySQL\MySQL Installer for Windows. You must run the console as administrator.

To use the console:

1. Open a command prompt with administrative privileges by selecting Windows System from Start,

then right-click Command Prompt, select More, and select Run as administrator.

2. From the command line, optionally change the directory to where the

MySQLInstallerConsole.exe command is located. For example, to use the default installation
location:

cd Program Files (x86)\MySQL\MySQL Installer for Windows

3. Type MySQLInstallerConsole.exe (or mysqlinstallerconsole) followed by a command

action to perform a task. For example, to show the console's help:

MySQLInstallerConsole.exe --help

=================== Start Initialization ===================
MySQL Installer is running in Community mode

Attempting to update manifest.
Initializing product requirements.
Loading product catalog.
Checking for product packages in the bundle.
Categorizing product catalog.
Finding all installed packages.
Your product catalog was last updated at 23/08/2022 12:41:05 p. m.
Your product catalog has version number 671.
=================== End Initialization ===================

The following actions are available:

Configure - Configures one or more of your installed programs.
Help      - Provides list of available command actions.
Install   - Installs and configures one or more available MySQL programs.
List      - Lists all available MySQL products.
Modify    - Modifies the features of installed products.
Remove    - Removes one or more products from your system.
Set       - Configures the general options of MySQL Installer.
Status    - Shows the status of all installed products.
Update    - Updates the current product catalog.
Upgrade   - Upgrades one or more of your installed programs.

The basic syntax for using MySQL Installer command actions. Brackets denote optional entities.
Curly braces denote a list of possible entities.

...

153

MySQL Installer for Windows

MySQL Product Names

Many of the MySQLInstallerConsole command actions accept one or more abbreviated phrases
that can match a MySQL product (or products) in the catalog. The current set of valid short phrases for
use with commands is shown in the following table.

Note

Starting with MySQL Installer 1.6.7 (8.0.34), the install, list, and upgrade
command options no longer apply to MySQL for Visual Studio (now EOL),
MySQL Connector/NET, MySQL Connector/ODBC, MySQL Connector/C++,
MySQL Connector/Python, and MySQL Connector/J. To install newer MySQL
connectors, visit https://dev.mysql.com/downloads/.

Table 2.6 MySQL Product Phrases for use with the MySQLInstallerConsole.exe command

Phrase

server

workbench

shell

visual

router

backup

net

odbc

c++

python

j

documentation

samples

Command Syntax

MySQL Product

MySQL Server

MySQL Workbench

MySQL Shell

MySQL for Visual Studio

MySQL Router

MySQL Enterprise Backup (requires the
commercial release)

MySQL Connector/NET

MySQL Connector/ODBC

MySQL Connector/C++

MySQL Connector/Python

MySQL Connector/J

MySQL Server Documentation

MySQL Samples (sakila and world databases)

The MySQLInstallerConsole.exe command can be issued with or without the file extension
(.exe) and the command is not case-sensitive.

mysqlinstallerconsole[.exe] [[[--]action] [action_blocks_list] [options_list]]

Description:

action

One of the permitted operational actions. If omitted, the default
action is equivalent to the --status action. Using the -- prefix is
optional for all actions.

Possible actions are: [--]configure, [--]help, [--]install,
[--]list, [--]modify, [--]remove, [--]set, [--]status, [--]update,
and [--]upgrade.

action_blocks_list

A list of blocks in which each represents a different item depending
on the selected action. Blocks are separated by commas.

The --remove and --upgrade actions permit specifying an
asterisk character (*) to indicate all products. If the * character is
detected at the start of this block, it is assumed all products are to
be processed and the remainder of the block is ignored.

154

MySQL Installer for Windows

Syntax: *|action_block[,action_block]
[,action_block]...

action_block: Contains a product selector followed by an
indefinite number of argument blocks that behave differently
depending on the selected action (see Command Actions).

Zero or more options with possible values separated by spaces.
See Command Actions to identify the options permitted for the
corresponding action.

Syntax: option_value_pair[ option_value_pair][
option_value_pair]...

option_value_pair: A single option (for example, --silent)
or a tuple of a key and a corresponding value with an options prefix.
The key-value pair is in the form of --key[=value].

options_list

Command Actions

MySQLInstallerConsole.exe supports the following command actions:

Note

Configuration block (or arguments_block) values that contain a colon character
(:) must be wrapped in quotation marks. For example, install_dir="C:
\MySQL\MySQL Server 8.0".

• [--]configure [product1]:[configuration_argument]=[value], [product2]:

[configuration_argument]=[value], [...]

Configures one or more MySQL products on your system. Multiple
configuration_argument=value pairs can be configured for each product.

Options:

--continue

--help

Continues processing the next product when an error is caught
while processing the action blocks containing arguments for each
product. If not specified the whole operation is aborted in case of
an error.

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

--show-settings

Displays the available options for the selected product by passing
in the product name after --show-settings.

--silent

Examples:

Disables confirmation prompts.

MySQLInstallerConsole --configure --show-settings server

mysqlinstallerconsole.exe --configure server:port=3307

• [--]help

Displays a help message with usage examples and then exits. Pass in an additional command action
to receive help specific to that action.

Options:

155

MySQL Installer for Windows

--action=[action]

Shows the help for a specific action. Same as using the --help
option with an action.

Permitted values are: all, configure, help (default),
install, list, modify, remove, status, update, upgrade,
and set.

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

--help

Examples:

MySQLInstallerConsole help

MySQLInstallerConsole help --action=install

• [--]install [product1]:[features]:[config block]:[config block],

[product2]:[config block], [...]

Installs one or more MySQL products on your system. If pre-release products are available, both
GA and pre-release products are installed when the value of the --type option value is Client or
Full. Use the --only_ga_products option to restrict the product set to GA products only when
using these setup types.

Description:

[product]

[features]

[config block]

Each product can be specified by a product phrase with or without
a semicolon-separated version qualifier. Passing in a product
keyword alone selects the latest version of the product. If multiple
architectures are available for that version of the product, the
command returns the first one in the manifest list for interactive
confirmation. Alternatively, you can pass in the exact version and
architecture (x86 or x64) after the product keyword using the --
silent option.

All features associated with a MySQL product are installed by
default. The feature block is a semicolon-separated list of features
or an asterisk character (*) that selects all features. To remove a
feature, use the modify command.

One or more configuration blocks can be specified. Each
configuration block is a semicolon-separated list of key-value
pairs. A block can include either a config or user type key;
config is the default type if one is not defined.

Configuration block values that contain a colon character (:) must
be wrapped in quotation marks. For example, installdir="C:
\MySQL\MySQL Server 8.0". Only one configuration type

156

MySQL Installer for Windows

block can be defined for each product. A user block should be
defined for each user to be created during the product installation.

Note

The user type key is not supported when
a product is being reconfigured.

If present, MySQL Installer attempts to download and install some
software prerequisites, not currently present. that can be resolved
with minimal intervention. If the --silent option is not present,
you are presented with installation pages for each prerequisite. If
the --auto-handle-prereqs options is omitted, packages with
missing prerequisites are not installed.

Continues processing the next product when an error is caught
while processing the action blocks containing arguments for each
product. If not specified the whole operation is aborted in case of
an error.

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

Options:

--auto-handle-prereqs

--continue

--help

--mos-password=password

Sets the My Oracle Support (MOS) user's password for
commercial versions of the MySQL Installer.

--mos-user=user_name

Specifies the My Oracle Support (MOS) user name for access to
the commercial version of MySQL Installer. If not present, only the
products in the bundle, if any, are available to be installed.

157

MySQL Installer for Windows

--only-ga-products

Restricts the product set to include GA products only.

--setup-type=setup_type

Installs a predefined set of software. The setup type can be one of
the following:

• Server: Installs a single MySQL server

• Client: Installs client programs and libraries (excludes MySQL

connectors)

• Full: Installs everything (excludes MySQL connectors)

• Custom: Installs user-selected products. This is the default

option.

Note

Non-custom setup types are valid only
when no other MySQL products are
installed.

--show-settings

Displays the available options for the selected product, by passing
in the product name after -showsettings.

--silent

Examples:

Disable confirmation prompts.

mysqlinstallerconsole.exe --install j;8.0.29, net;8.0.28 --silent

MySQLInstallerConsole install server;8.0.30:*:port=3307;server_id=2:type=user;user=foo

An example that passes in additional configuration blocks, separated by ^ to fit:

MySQLInstallerConsole --install server;8.0.30;x64:*:type=config;open_win_firewall=true; ^
   general_log=true;bin_log=true;server_id=3306;tcp_ip=true;port=3306;root_passwd=pass; ^
   install_dir="C:\MySQL\MySQL Server 8.0":type=user;user_name=foo;password=bar;role=DBManager

158

MySQL Installer for Windows

• [--]list

When this action is used without options, it activates an interactive list from which all of the available
MySQL products can be searched. Enter MySQLInstallerConsole --list and specify a
substring to search.

Options:

--all

--arch=architecture

--help

--name=package_name

--version=version

Examples:

Lists all available products. If this option is used, all other options
are ignored.

Lists that contain the specified architecture. Permitted values are:
x86, x64, and any (default). This option can be combined with
the --name and --version options.

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

Lists products that contain the specified name (see product
phrase), This option can be combined with the --version and
--arch options.

Lists products that contain the specified version, such as 8.0 or
5.7. This option can be combined with the --name and --arch
options.

MySQLInstallerConsole --list --name=net --version=8.0

• [--]modify [product1:-removelist|+addlist], [product2:-removelist|

+addlist] [...]

Modifies or displays features of a previously installed MySQL product. To display the features of a
product, append the product keyword to the command, for example:

MySQLInstallerConsole --modify server

Options:

--help

--silent

Examples:

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

Disable confirmation prompts.

MySQLInstallerConsole --modify server:+documentation

MySQLInstallerConsole modify server:-debug

159

MySQL Installer for Windows

• [--]remove [product1], [product2] [...]

Removes one ore more products from your system. An asterisk character (*) can be passed in to
remove all MySQL products with one command.

Options:

--continue

--help

Continue the operation even if an error occurs.

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

--keep-datadir

Skips the removal of the data directory when removing MySQL
Server products.

--silent

Examples:

Disable confirmation prompts.

mysqlinstallerconsole.exe remove *

MySQLInstallerConsole --remove server --continue

• [--]set

Sets one or more configurable options that affect how the MySQL Installer program connects to the
internet and whether the automatic products-catalog updates feature is activated.

Options:

--catalog-
update=bool_value

--catalog-update-
days=int_value

Enables (true, default) or disables (false) the automatic
products catalog update. This option requires an active
connection to the internet.

Accepts an integer between 1 (default) and 365 to indicate the
number of days between checks for a new catalog update when
MySQL Installer is started. If --catalog-update is false, this
option is ignored.

--connection-
validation=validation_type

Sets how MySQL Installer performs the check for an internet
connection. Permitted values are automatic (default) and
manual.

--connection-validation-
urls=url_list

A double-quote enclosed and comma-separated string that
defines the list of URLs to use for checking the internet
connection when --connection-validation is set to

160

MySQL Installer for Windows

manual. Checks are made in the same order provided. If the first
URL fails, the next URL in the list is used and so on.

--offline-
mode=bool_value

Enables MySQL Installer to run with or without internet
capabilities. Valid modes are:

• True to enable offline mode (run without an internet

connection).

• False (default) to disable offline mode (run with an internet
connection). Set this mode before downloading the product
catalog or any products to install.

--proxy-mode

Specifies the proxy mode. Valid modes are:

• Automatic to automatically identify the proxy based on the

system settings.

• None to ensure that no proxy is configured.

• Manual to set the proxy details manually (--proxy-server,

--proxy-port, --proxy-username, --proxy-password).

--proxy-password

The password used to authenticate to the proxy server.

--proxy-port

The port used for the proxy server.

--proxy-server

The URL that point to the proxy server.

--proxy-username

The user name used to authenticate to the proxy server.

--reset-defaults

Resets the MySQL Installer options associated with the --set
action to the default values.

Examples:

MySQLIntallerConsole.exe set --reset-defaults

mysqlintallerconsole.exe --set --catalog-update=false

MySQLIntallerConsole --set --catalog-update-days=3

mysqlintallerconsole --set --connection-validation=manual
--connection-validation-urls="https://www.bing.com,http://www.google.com"

• [--]status

Provides a quick overview of the MySQL products that are installed on the system. Information
includes product name and version, architecture, date installed, and install location.

Options:

--help

Examples:

MySQLInstallerConsole status

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

161

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

• [--]update

Downloads the latest MySQL product catalog to your system. On success, the catalog is applied the
next time either MySQLInstaller or MySQLInstallerConsole.exe is executed.

MySQL Installer automatically checks for product catalog updates when it is started if n days
have passed since the last check. Starting with MySQL Installer 1.6.4, the default value is 1 day.
Previously, the default value was 7 days.

Options:

--help

Examples:

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

MySQLInstallerConsole update

• [--]upgrade [product1:version], [product2:version] [...]

Upgrades one or more products on your system. The following characters are permitted for this
action:

*

!

Options:

--continue

--help

Pass in * to upgrade all products to the latest version, or pass in
specific products.

Pass in ! as a version number to upgrade the MySQL product to
its latest version.

Continue the operation even if an error occurs.

Shows the options and available arguments for the corresponding
action. If present the action is not executed, only the help is
shown, so other action-related options are ignored as well.

--mos-password=password

Sets the My Oracle Support (MOS) user's password for
commercial versions of the MySQL Installer.

--mos-user=user_name

Specifies the My Oracle Support (MOS) user name for access to
the commercial version of MySQL Installer. If not present, only the
products in the bundle, if any, are available to be installed.

--silent

Examples:

Disable confirmation prompts.

MySQLInstallerConsole upgrade *

MySQLInstallerConsole upgrade workbench:8.0.31

MySQLInstallerConsole upgrade workbench:!

MySQLInstallerConsole --upgrade server;8.0.30:!, j;8.0.29:!

2.3.4 Installing MySQL on Microsoft Windows Using a noinstall ZIP
Archive

Users who are installing from the noinstall package can use the instructions in this section to
manually install MySQL. The process for installing MySQL from a ZIP Archive package is as follows:

162

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

boot drive, your only option is to use the my.ini file. Whichever option file you use, it must be a plain
text file.

Note

When using the MySQL Installer to install MySQL Server, it creates the my.ini
at the default location, and the user executing MySQL Installer is granted full
permissions to this new my.ini file.

In other words, be sure that the MySQL Server user has permission to read the
my.ini file.

You can also make use of the example option files included with your MySQL distribution; see
Section 7.1.2, “Server Configuration Defaults”.

An option file can be created and modified with any text editor, such as Notepad. For example, if
MySQL is installed in E:\mysql and the data directory is in E:\mydata\data, you can create an
option file containing a [mysqld] section to specify values for the basedir and datadir options:

[mysqld]
# set basedir to your installation path
basedir=E:/mysql
# set datadir to the location of your data directory
datadir=E:/mydata/data

Microsoft Windows path names are specified in option files using (forward) slashes rather than
backslashes. If you do use backslashes, double them:

[mysqld]
# set basedir to your installation path
basedir=E:\\mysql
# set datadir to the location of your data directory
datadir=E:\\mydata\\data

The rules for use of backslash in option file values are given in Section 6.2.2.2, “Using Option Files”.

The ZIP archive does not include a data directory. To initialize a MySQL installation by creating the
data directory and populating the tables in the mysql system database, initialize MySQL using either --
initialize or --initialize-insecure. For additional information, see Section 2.9.1, “Initializing
the Data Directory”.

If you would like to use a data directory in a different location, you should copy the entire contents
of the data directory to the new location. For example, if you want to use E:\mydata as the data
directory instead, you must do two things:

1. Move the entire data directory and all of its contents from the default location (for example C:

\Program Files\MySQL\MySQL Server 8.0\data) to E:\mydata.

2. Use a --datadir option to specify the new data directory location each time you start the server.

2.3.4.3 Selecting a MySQL Server Type

The following table shows the available servers for Windows in MySQL 8.0.

Binary

mysqld

mysqld-debug

Description

Optimized binary with named-pipe support

Like mysqld, but compiled with full debugging
and automatic memory allocation checking

All of the preceding binaries are optimized for modern Intel processors, but should work on any Intel
i386-class or higher processor.

164

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

Each of the servers in a distribution support the same set of storage engines. The SHOW ENGINES
statement displays which engines a given server supports.

All Windows MySQL 8.0 servers have support for symbolic linking of database directories.

MySQL supports TCP/IP on all Windows platforms. MySQL servers on Windows also support named
pipes, if you start the server with the named_pipe system variable enabled. It is necessary to enable
this variable explicitly because some users have experienced problems with shutting down the MySQL
server when named pipes were used. The default is to use TCP/IP regardless of platform because
named pipes are slower than TCP/IP in many Windows configurations.

2.3.4.4 Initializing the Data Directory

If you installed MySQL using the noinstall package, no data directory is included. To initialize the
data directory, use the instructions at Section 2.9.1, “Initializing the Data Directory”.

2.3.4.5 Starting the Server for the First Time

This section gives a general overview of starting the MySQL server. The following sections provide
more specific information for starting the MySQL server from the command line or as a Windows
service.

The information here applies primarily if you installed MySQL using the noinstall version, or if you
wish to configure and test MySQL manually rather than with the MySQL Installer.

The examples in these sections assume that MySQL is installed under the default location of C:
\Program Files\MySQL\MySQL Server 8.0. Adjust the path names shown in the examples if
you have MySQL installed in a different location.

Clients have two options. They can use TCP/IP, or they can use a named pipe if the server supports
named-pipe connections.

MySQL for Windows also supports shared-memory connections if the server is started with the
shared_memory system variable enabled. Clients can connect through shared memory by using the
--protocol=MEMORY option.

For information about which server binary to run, see Section 2.3.4.3, “Selecting a MySQL Server
Type”.

Testing is best done from a command prompt in a console window (or “DOS window”). In this way you
can have the server display status messages in the window where they are easy to see. If something is
wrong with your configuration, these messages make it easier for you to identify and fix any problems.

Note

The database must be initialized before MySQL can be started. For additional
information about the initialization process, see Section 2.9.1, “Initializing the
Data Directory”.

To start the server, enter this command:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --console

You should see messages similar to those following as it starts (the path names and sizes may
differ). The ready for connections messages indicate that the server is ready to service client
connections.

[Server] C:\mysql\bin\mysqld.exe (mysqld 8.0.30) starting as process 21236
[InnoDB] InnoDB initialization has started.
[InnoDB] InnoDB initialization has ended.
[Server] CA certificate ca.pem is self signed.

165

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

[Server] Channel mysql_main configured to support TLS.
Encrypted connections are now supported for this channel.
[Server] X Plugin ready for connections. Bind-address: '::' port: 33060
[Server] C:\mysql\bin\mysqld.exe: ready for connections.
Version: '8.0.30'  socket: ''  port: 3306  MySQL Community Server - GPL.

You can now open a new console window in which to run client programs.

If you omit the --console option, the server writes diagnostic output to the error log in the data
directory (C:\Program Files\MySQL\MySQL Server 8.0\data by default). The error log is the
file with the .err extension, and may be set using the --log-error option.

Note

The initial root account in the MySQL grant tables has no password. After
starting the server, you should set up a password for it using the instructions in
Section 2.9.4, “Securing the Initial MySQL Account”.

2.3.4.6 Starting MySQL from the Windows Command Line

The MySQL server can be started manually from the command line. This can be done on any version
of Windows.

To start the mysqld server from the command line, you should start a console window (or “DOS
window”) and enter this command:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld"

The path to mysqld may vary depending on the install location of MySQL on your system.

You can stop the MySQL server by executing this command:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqladmin" -u root shutdown

Note

If the MySQL root user account has a password, you need to invoke
mysqladmin with the -p option and supply the password when prompted.

This command invokes the MySQL administrative utility mysqladmin to connect to the server and tell
it to shut down. The command connects as the MySQL root user, which is the default administrative
account in the MySQL grant system.

Note

Users in the MySQL grant system are wholly independent from any operating
system users under Microsoft Windows.

If mysqld doesn't start, check the error log to see whether the server wrote any messages there to
indicate the cause of the problem. By default, the error log is located in the C:\Program Files
\MySQL\MySQL Server 8.0\data directory. It is the file with a suffix of .err, or may be specified
by passing in the --log-error option. Alternatively, you can try to start the server with the --
console option; in this case, the server may display some useful information on the screen to help
solve the problem.

The last option is to start mysqld with the --standalone and --debug options. In this case, mysqld
writes a log file C:\mysqld.trace that should contain the reason why mysqld doesn't start. See
Section 7.9.4, “The DBUG Package”.

Use mysqld --verbose --help to display all the options that mysqld supports.

2.3.4.7 Customizing the PATH for MySQL Tools

166

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

Warning

You must exercise great care when editing your system PATH by hand;
accidental deletion or modification of any portion of the existing PATH value can
leave you with a malfunctioning or even unusable system.

To make it easier to invoke MySQL programs, you can add the path name of the MySQL bin directory
to your Windows system PATH environment variable:

• On the Windows desktop, right-click the My Computer icon, and select Properties.

• Next select the Advanced tab from the System Properties menu that appears, and click the

Environment Variables button.

• Under System Variables, select Path, and then click the Edit button. The Edit System Variable

dialogue should appear.

• Place your cursor at the end of the text appearing in the space marked Variable Value. (Use the

End key to ensure that your cursor is positioned at the very end of the text in this space.) Then enter
the complete path name of your MySQL bin directory (for example, C:\Program Files\MySQL
\MySQL Server 8.0\bin)

Note

There must be a semicolon separating this path from any values present in
this field.

Dismiss this dialogue, and each dialogue in turn, by clicking OK until all of the dialogues that were
opened have been dismissed. The new PATH value should now be available to any new command
shell you open, allowing you to invoke any MySQL executable program by typing its name at the
DOS prompt from any directory on the system, without having to supply the path. This includes
the servers, the mysql client, and all MySQL command-line utilities such as mysqladmin and
mysqldump.

You should not add the MySQL bin directory to your Windows PATH if you are running multiple
MySQL servers on the same machine.

2.3.4.8 Starting MySQL as a Windows Service

On Windows, the recommended way to run MySQL is to install it as a Windows service, so that MySQL
starts and stops automatically when Windows starts and stops. A MySQL server installed as a service
can also be controlled from the command line using NET commands, or with the graphical Services
utility. Generally, to install MySQL as a Windows service you should be logged in using an account that
has administrator rights.

The Services utility (the Windows Service Control Manager) can be found in the Windows
Control Panel. To avoid conflicts, it is advisable to close the Services utility while performing server
installation or removal operations from the command line.

Installing the service

Before installing MySQL as a Windows service, you should first stop the current server if it is running
by using the following command:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqladmin"
          -u root shutdown

Note

If the MySQL root user account has a password, you need to invoke
mysqladmin with the -p option and supply the password when prompted.

167

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

This command invokes the MySQL administrative utility mysqladmin to connect to the server and tell
it to shut down. The command connects as the MySQL root user, which is the default administrative
account in the MySQL grant system.

Note

Users in the MySQL grant system are wholly independent from any operating
system users under Windows.

Install the server as a service using this command:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --install

The service-installation command does not start the server. Instructions for that are given later in this
section.

To make it easier to invoke MySQL programs, you can add the path name of the MySQL bin directory
to your Windows system PATH environment variable:

• On the Windows desktop, right-click the My Computer icon, and select Properties.

• Next select the Advanced tab from the System Properties menu that appears, and click the

Environment Variables button.

• Under System Variables, select Path, and then click the Edit button. The Edit System Variable

dialogue should appear.

• Place your cursor at the end of the text appearing in the space marked Variable Value. (Use the

End key to ensure that your cursor is positioned at the very end of the text in this space.) Then enter
the complete path name of your MySQL bin directory (for example, C:\Program Files\MySQL
\MySQL Server 8.0\bin), and there should be a semicolon separating this path from any values
present in this field. Dismiss this dialogue, and each dialogue in turn, by clicking OK until all of the
dialogues that were opened have been dismissed. You should now be able to invoke any MySQL
executable program by typing its name at the DOS prompt from any directory on the system, without
having to supply the path. This includes the servers, the mysql client, and all MySQL command-line
utilities such as mysqladmin and mysqldump.

You should not add the MySQL bin directory to your Windows PATH if you are running multiple
MySQL servers on the same machine.

Warning

You must exercise great care when editing your system PATH by hand;
accidental deletion or modification of any portion of the existing PATH value can
leave you with a malfunctioning or even unusable system.

The following additional arguments can be used when installing the service:

• You can specify a service name immediately following the --install option. The default service

name is MySQL.

• If a service name is given, it can be followed by a single option. By convention, this should be --
defaults-file=file_name to specify the name of an option file from which the server should
read options when it starts.

The use of a single option other than --defaults-file is possible but discouraged. --
defaults-file is more flexible because it enables you to specify multiple startup options for the
server by placing them in the named option file.

• You can also specify a --local-service option following the service name. This causes the

server to run using the LocalService Windows account that has limited system privileges. If both
--defaults-file and --local-service are given following the service name, they can be in
any order.

168

Installing MySQL on Microsoft Windows Using a noinstall ZIP Archive

For a MySQL server that is installed as a Windows service, the following rules determine the service
name and option files that the server uses:

• If the service-installation command specifies no service name or the default service name (MySQL)

following the --install option, the server uses the service name of MySQL and reads options from
the [mysqld] group in the standard option files.

• If the service-installation command specifies a service name other than MySQL following the --
install option, the server uses that service name. It reads options from the [mysqld] group
and the group that has the same name as the service in the standard option files. This enables you
to use the [mysqld] group for options that should be used by all MySQL services, and an option
group with the service name for use by the server installed with that service name.

• If the service-installation command specifies a --defaults-file option after the service name,

the server reads options the same way as described in the previous item, except that it reads options
only from the named file and ignores the standard option files.

As a more complex example, consider the following command:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld"
          --install MySQL --defaults-file=C:\my-opts.cnf

Here, the default service name (MySQL) is given after the --install option. If no --defaults-
file option had been given, this command would have the effect of causing the server to read the
[mysqld] group from the standard option files. However, because the --defaults-file option is
present, the server reads options from the [mysqld] option group, and only from the named file.

Note

On Windows, if the server is started with the --defaults-file and --
install options, --install must be first. Otherwise, mysqld.exe attempts
to start the MySQL server.

You can also specify options as Start parameters in the Windows Services utility before you start the
MySQL service.

Finally, before trying to start the MySQL service, make sure the user variables %TEMP% and %TMP%
(and also %TMPDIR%, if it has ever been set) for the operating system user who is to run the service are
pointing to a folder to which the user has write access. The default user for running the MySQL service
is LocalSystem, and the default value for its %TEMP% and %TMP% is C:\Windows\Temp, a directory
LocalSystem has write access to by default. However, if there are any changes to that default setup
(for example, changes to the user who runs the service or to the mentioned user variables, or the --
tmpdir option has been used to put the temporary directory somewhere else), the MySQL service
might fail to run because write access to the temporary directory has not been granted to the proper
user.

Starting the service

After a MySQL server instance has been installed as a service, Windows starts the service
automatically whenever Windows starts. The service also can be started immediately from
the Services utility, or by using an sc start mysqld_service_name or NET START
mysqld_service_name command. SC and NET commands are not case-sensitive.

When run as a service, mysqld has no access to a console window, so no messages can be seen
there. If mysqld does not start, check the error log to see whether the server wrote any messages
there to indicate the cause of the problem. The error log is located in the MySQL data directory (for
example, C:\Program Files\MySQL\MySQL Server 8.0\data). It is the file with a suffix of
.err.

When a MySQL server has been installed as a service, and the service is running, Windows stops
the service automatically when Windows shuts down. The server also can be stopped manually

169

Troubleshooting a Microsoft Windows MySQL Server Installation

using the Services utility, the sc stop mysqld_service_name command, the NET STOP
mysqld_service_name command, or the mysqladmin shutdown command.

You also have the choice of installing the server as a manual service if you do not wish for the service
to be started automatically during the boot process. To do this, use the --install-manual option
rather than the --install option:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --install-manual

Removing the service

To remove a server that is installed as a service, first stop it if it is running by executing SC STOP
mysqld_service_name or NET STOP mysqld_service_name. Then use SC DELETE
mysqld_service_name to remove it:

C:\> SC DELETE mysql

Alternatively, use the mysqld --remove option to remove the service.

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --remove

If mysqld is not running as a service, you can start it from the command line. For instructions, see
Section 2.3.4.6, “Starting MySQL from the Windows Command Line”.

If you encounter difficulties during installation, see Section 2.3.5, “Troubleshooting a Microsoft
Windows MySQL Server Installation”.

For more information about stopping or removing a Windows service, see Section 7.8.2.2, “Starting
Multiple MySQL Instances as Windows Services”.

2.3.4.9 Testing The MySQL Installation

You can test whether the MySQL server is working by executing any of the following commands:

C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqlshow"
C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqlshow" -u root mysql
C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqladmin" version status proc
C:\> "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" test

If mysqld is slow to respond to TCP/IP connections from client programs, there is probably a problem
with your DNS. In this case, start mysqld with the skip_name_resolve system variable enabled and
use only localhost and IP addresses in the Host column of the MySQL grant tables. (Be sure that
an account exists that specifies an IP address or you may not be able to connect.)

You can force a MySQL client to use a named-pipe connection rather than TCP/IP by specifying the --
pipe or --protocol=PIPE option, or by specifying . (period) as the host name. Use the --socket
option to specify the name of the pipe if you do not want to use the default pipe name.

If you have set a password for the root account, deleted the anonymous account, or created a new
user account, then to connect to the MySQL server you must use the appropriate -u and -p options
with the commands shown previously. See Section 6.2.4, “Connecting to the MySQL Server Using
Command Options”.

For more information about mysqlshow, see Section 6.5.7, “mysqlshow — Display Database, Table,
and Column Information”.

2.3.5 Troubleshooting a Microsoft Windows MySQL Server Installation

When installing and running MySQL for the first time, you may encounter certain errors that prevent the
MySQL server from starting. This section helps you diagnose and correct some of these errors.

Your first resource when troubleshooting server issues is the error log. The MySQL server uses the
error log to record information relevant to the error that prevents the server from starting. The error log
is located in the data directory specified in your my.ini file. The default data directory location is C:
\Program Files\MySQL\MySQL Server 8.0\data, or C:\ProgramData\Mysql on Windows

170

Troubleshooting a Microsoft Windows MySQL Server Installation

7 and Windows Server 2008. The C:\ProgramData directory is hidden by default. You need to
change your folder options to see the directory and contents. For more information on the error log and
understanding the content, see Section 7.4.2, “The Error Log”.

For information regarding possible errors, also consult the console messages displayed when
the MySQL service is starting. Use the SC START mysqld_service_name or NET START
mysqld_service_name command from the command line after installing mysqld as a service to
see any error messages regarding the starting of the MySQL server as a service. See Section 2.3.4.8,
“Starting MySQL as a Windows Service”.

The following examples show other common error messages you might encounter when installing
MySQL and starting the server for the first time:

• If the MySQL server cannot find the mysql privileges database or other critical files, it displays these

messages:

System error 1067 has occurred.
Fatal error: Can't open and lock privilege tables:
Table 'mysql.user' doesn't exist

These messages often occur when the MySQL base or data directories are installed in different
locations than the default locations (C:\Program Files\MySQL\MySQL Server 8.0 and C:
\Program Files\MySQL\MySQL Server 8.0\data, respectively).

This situation can occur when MySQL is upgraded and installed to a new location, but the
configuration file is not updated to reflect the new location. In addition, old and new configuration files
might conflict. Be sure to delete or rename any old configuration files when upgrading MySQL.

If you have installed MySQL to a directory other than C:\Program Files\MySQL\MySQL Server
8.0, ensure that the MySQL server is aware of this through the use of a configuration (my.ini)
file. Put the my.ini file in your Windows directory, typically C:\WINDOWS. To determine its exact
location from the value of the WINDIR environment variable, issue the following command from the
command prompt:

C:\> echo %WINDIR%

You can create or modify an option file with any text editor, such as Notepad. For example, if MySQL
is installed in E:\mysql and the data directory is D:\MySQLdata, you can create the option file and
set up a [mysqld] section to specify values for the basedir and datadir options:

[mysqld]
# set basedir to your installation path
basedir=E:/mysql
# set datadir to the location of your data directory
datadir=D:/MySQLdata

Microsoft Windows path names are specified in option files using (forward) slashes rather than
backslashes. If you do use backslashes, double them:

[mysqld]
# set basedir to your installation path
basedir=C:\\Program Files\\MySQL\\MySQL Server 8.0
# set datadir to the location of your data directory
datadir=D:\\MySQLdata

The rules for use of backslash in option file values are given in Section 6.2.2.2, “Using Option Files”.

If you change the datadir value in your MySQL configuration file, you must move the contents of
the existing MySQL data directory before restarting the MySQL server.

See Section 2.3.4.2, “Creating an Option File”.

• If you reinstall or upgrade MySQL without first stopping and removing the existing MySQL service

and install MySQL using the MySQL Installer, you might see this error:

171

Windows Postinstallation Procedures

Error: Cannot create Windows service for MySql. Error: 0

This occurs when the Configuration Wizard tries to install the service and finds an existing service
with the same name.

One solution to this problem is to choose a service name other than mysql when using the
configuration wizard. This enables the new service to be installed correctly, but leaves the outdated
service in place. Although this is harmless, it is best to remove old services that are no longer in use.

To permanently remove the old mysql service, execute the following command as a user with
administrative privileges, on the command line:

C:\> SC DELETE mysql
[SC] DeleteService SUCCESS

If the SC utility is not available for your version of Windows, download the delsrv utility from http://
www.microsoft.com/windows2000/techinfo/reskit/tools/existing/delsrv-o.asp and use the delsrv
mysql syntax.

2.3.6 Windows Postinstallation Procedures

GUI tools exist that perform most of the tasks described in this section, including:

• MySQL Installer: Used to install and upgrade MySQL products.

• MySQL Workbench: Manages the MySQL server and edits SQL statements.

If necessary, initialize the data directory and create the MySQL grant tables. Windows installation
operations performed by MySQL Installer initialize the data directory automatically. For installation from
a ZIP Archive package, initialize the data directory as described at Section 2.9.1, “Initializing the Data
Directory”.

Regarding passwords, if you installed MySQL using the MySQL Installer, you may have already
assigned a password to the initial root account. (See Section 2.3.3, “MySQL Installer for Windows”.)
Otherwise, use the password-assignment procedure given in Section 2.9.4, “Securing the Initial MySQL
Account”.

Before assigning a password, you might want to try running some client programs to make sure that
you can connect to the server and that it is operating properly. Make sure that the server is running
(see Section 2.3.4.5, “Starting the Server for the First Time”). You can also set up a MySQL service
that runs automatically when Windows starts (see Section 2.3.4.8, “Starting MySQL as a Windows
Service”).

These instructions assume that your current location is the MySQL installation directory and that it has
a bin subdirectory containing the MySQL programs used here. If that is not true, adjust the command
path names accordingly.

If you installed MySQL using MySQL Installer (see Section 2.3.3, “MySQL Installer for Windows”), the
default installation directory is C:\Program Files\MySQL\MySQL Server 8.0:

C:\> cd "C:\Program Files\MySQL\MySQL Server 8.0"

A common installation location for installation from a ZIP archive is C:\mysql:

C:\> cd C:\mysql

Alternatively, add the bin directory to your PATH environment variable setting. That enables your
command interpreter to find MySQL programs properly, so that you can run a program by typing only
its name, not its path name. See Section 2.3.4.7, “Customizing the PATH for MySQL Tools”.

172

Windows Postinstallation Procedures

With the server running, issue the following commands to verify that you can retrieve information from
the server. The output should be similar to that shown here.

Use mysqlshow to see what databases exist:

C:\> bin\mysqlshow
+--------------------+
|     Databases      |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+

The list of installed databases may vary, but always includes at least mysql and
information_schema.

The preceding command (and commands for other MySQL programs such as mysql) may not work
if the correct MySQL account does not exist. For example, the program may fail with an error, or you
may not be able to view all databases. If you install MySQL using MySQL Installer, the root user is
created automatically with the password you supplied. In this case, you should use the -u root and -
p options. (You must use those options if you have already secured the initial MySQL accounts.) With -
p, the client program prompts for the root password. For example:

C:\> bin\mysqlshow -u root -p
Enter password: (enter root password here)
+--------------------+
|     Databases      |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+

If you specify a database name, mysqlshow displays a list of the tables within the database:

C:\> bin\mysqlshow mysql
Database: mysql
+---------------------------+
|          Tables           |
+---------------------------+
| columns_priv              |
| component                 |
| db                        |
| default_roles             |
| engine_cost               |
| func                      |
| general_log               |
| global_grants             |
| gtid_executed             |
| help_category             |
| help_keyword              |
| help_relation             |
| help_topic                |
| innodb_index_stats        |
| innodb_table_stats        |
| ndb_binlog_index          |
| password_history          |
| plugin                    |
| procs_priv                |
| proxies_priv              |
| role_edges                |
| server_cost               |
| servers                   |
| slave_master_info         |
| slave_relay_log_info      |
| slave_worker_info         |
| slow_log                  |

173

Windows Platform Restrictions

| tables_priv               |
| time_zone                 |
| time_zone_leap_second     |
| time_zone_name            |
| time_zone_transition      |
| time_zone_transition_type |
| user                      |
+---------------------------+

Use the mysql program to select information from a table in the mysql database:

C:\> bin\mysql -e "SELECT User, Host, plugin FROM mysql.user" mysql
+------+-----------+-----------------------+
| User | Host      | plugin                |
+------+-----------+-----------------------+
| root | localhost | caching_sha2_password |
+------+-----------+-----------------------+

For more information about mysql and mysqlshow, see Section 6.5.1, “mysql — The MySQL
Command-Line Client”, and Section 6.5.7, “mysqlshow — Display Database, Table, and Column
Information”.

2.3.7 Windows Platform Restrictions

The following restrictions apply to use of MySQL on the Windows platform:

• Process memory

On Windows 32-bit platforms, it is not possible by default to use more than 2GB of RAM within a
single process, including MySQL. This is because the physical address limit on Windows 32-bit
is 4GB and the default setting within Windows is to split the virtual address space between kernel
(2GB) and user/applications (2GB).

Some versions of Windows have a boot time setting to enable larger applications by reducing the
kernel application. Alternatively, to use more than 2GB, use a 64-bit version of Windows.

• File system aliases

When using MyISAM tables, you cannot use aliases within Windows link to the data files on another
volume and then link back to the main MySQL datadir location.

This facility is often used to move the data and index files to a RAID or other fast solution.

• Limited number of ports

Windows systems have about 4,000 ports available for client connections, and after a connection on
a port closes, it takes two to four minutes before the port can be reused. In situations where clients
connect to and disconnect from the server at a high rate, it is possible for all available ports to be
used up before closed ports become available again. If this happens, the MySQL server appears to
be unresponsive even though it is running. Ports may be used by other applications running on the
machine as well, in which case the number of ports available to MySQL is lower.

For more information about this problem, see https://support.microsoft.com/kb/196271.

• DATA DIRECTORY and INDEX DIRECTORY

The DATA DIRECTORY clause of the CREATE TABLE statement is supported on Windows for
InnoDB tables only, as described in Section 17.6.1.2, “Creating Tables Externally”. For MyISAM and
other storage engines, the DATA DIRECTORY and INDEX DIRECTORY clauses for CREATE TABLE
are ignored on Windows and any other platforms with a nonfunctional realpath() call.

• DROP DATABASE

You cannot drop a database that is in use by another session.

174

Installing MySQL on macOS

• Case-insensitive names

File names are not case-sensitive on Windows, so MySQL database and table names are also not
case-sensitive on Windows. The only restriction is that database and table names must be specified
using the same case throughout a given statement. See Section 11.2.3, “Identifier Case Sensitivity”.

• Directory and file names

On Windows, MySQL Server supports only directory and file names that are compatible with the
current ANSI code pages. For example, the following Japanese directory name does not work in the
Western locale (code page 1252):

datadir="C:/私たちのプロジェクトのデータ"

The same limitation applies to directory and file names referred to in SQL statements, such as the
data file path name in LOAD DATA.

• The \ path name separator character

Path name components in Windows are separated by the \ character, which is also the escape
character in MySQL. If you are using LOAD DATA or SELECT ... INTO OUTFILE, use Unix-style
file names with / characters:

mysql> LOAD DATA INFILE 'C:/tmp/skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:/tmp/skr.txt' FROM skr;

Alternatively, you must double the \ character:

mysql> LOAD DATA INFILE 'C:\\tmp\\skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:\\tmp\\skr.txt' FROM skr;

• Problems with pipes

Pipes do not work reliably from the Windows command-line prompt. If the pipe includes the character
^Z / CHAR(24), Windows thinks that it has encountered end-of-file and aborts the program.

This is mainly a problem when you try to apply a binary log as follows:

C:\> mysqlbinlog binary_log_file | mysql --user=root

If you have a problem applying the log and suspect that it is because of a ^Z / CHAR(24) character,
you can use the following workaround:

C:\> mysqlbinlog binary_log_file --result-file=/tmp/bin.sql
C:\> mysql --user=root --execute "source /tmp/bin.sql"

The latter command also can be used to reliably read any SQL file that may contain binary data.

2.4 Installing MySQL on macOS

For a list of macOS versions that the MySQL server supports, see https://www.mysql.com/support/
supportedplatforms/database.html.

MySQL for macOS is available in a number of different forms:

• Native Package Installer, which uses the native macOS installer (DMG) to walk you through the

installation of MySQL. For more information, see Section 2.4.2, “Installing MySQL on macOS Using
Native Packages”. You can use the package installer with macOS. The user you use to perform the
installation must have administrator privileges.

• Compressed TAR archive, which uses a file packaged using the Unix tar and gzip commands.

To use this method, you need to open a Terminal window. You do not need administrator
privileges using this method; you can install the MySQL server anywhere using this method. For

175

Installing MySQL on macOS Using Native Packages

2.4.2 Installing MySQL on macOS Using Native Packages

The package is located inside a disk image (.dmg) file that you first need to mount by double-clicking
its icon in the Finder. It should then mount the image and display its contents.

Note

Before proceeding with the installation, be sure to stop all running MySQL
server instances by using either the MySQL Manager Application (on macOS
Server), the preference pane, or mysqladmin shutdown on the command
line.

To install MySQL using the package installer:

1. Download the disk image (.dmg) file (the community version is available here) that contains the
MySQL package installer. Double-click the file to mount the disk image and see its contents.

Double-click the MySQL installer package from the disk. It is named according to the version
of MySQL you have downloaded. For example, for MySQL server 8.0.42 it might be named
mysql-8.0.42-macos-10.13-x86_64.pkg.

2. The initial wizard introduction screen references the MySQL server version to install. Click

Continue to begin the installation.

The MySQL community edition shows a copy of the relevant GNU General Public License. Click
Continue and then Agree to continue.

3. From the Installation Type page you can either click Install to execute the installation wizard using
all defaults, click Customize to alter which components to install (MySQL server, MySQL Test,
Preference Pane, Launchd Support -- all but MySQL Test are enabled by default).

Note

Although the Change Install Location option is visible, the installation
location cannot be changed.

177

Installing MySQL on macOS Using Native Packages

Figure 2.13 MySQL Package Installer Wizard: Installation Type

Figure 2.14 MySQL Package Installer Wizard: Customize

178

Installing MySQL on macOS Using Native Packages

4. Click Install to install MySQL Server. The installation process ends here if upgrading a current

MySQL Server installation, otherwise follow the wizard's additional configuration steps for your new
MySQL Server installation.

5. After a successful new MySQL Server installation, complete the configuration steps by choosing
the default encryption type for passwords, define the root password, and also enable (or disable)
MySQL server at startup.

6. The default MySQL 8.0 password mechanism is caching_sha2_password (Strong), and this

step allows you to change it to mysql_native_password (Legacy).

Figure 2.15 MySQL Package Installer Wizard: Choose a Password Encryption Type

Choosing the legacy password mechanism alters the generated launchd file to set --
default_authentication_plugin=mysql_native_password under ProgramArguments.
Choosing strong password encryption does not set --default_authentication_plugin
because the default MySQL Server value is used, which is caching_sha2_password.

179

Installing MySQL on macOS Using Native Packages

7. Define a password for the root user, and also toggle whether MySQL Server should start after the

configuration step is complete.

Figure 2.16 MySQL Package Installer Wizard: Define Root Password

8. Summary is the final step and references a successful and complete MySQL Server installation.

Close the wizard.

Figure 2.17 MySQL Package Installer Wizard: Summary

180

Installing and Using the MySQL Launch Daemon

MySQL server is now installed. If you chose to not start MySQL, then use either launchctl from the
command line or start MySQL by clicking "Start" using the MySQL preference pane. For additional
information, see Section 2.4.3, “Installing and Using the MySQL Launch Daemon”, and Section 2.4.4,
“Installing and Using the MySQL Preference Pane”. Use the MySQL Preference Pane or launchd to
configure MySQL to automatically start at bootup.

When installing using the package installer, the files are installed into a directory within /usr/
local matching the name of the installation version and platform. For example, the installer file
mysql-8.0.42-macos10.15-x86_64.dmg installs MySQL into /usr/local/mysql-8.0.42-
macos10.15-x86_64/  with a symlink to /usr/local/mysql. The following table shows the layout
of this MySQL installation directory.

Note

The macOS installation process does not create nor install a sample my.cnf
MySQL configuration file.

Table 2.7 MySQL Installation Layout on macOS

Directory

bin

data

docs

include

lib

man

mysql-test

share

support-files

Contents of Directory

mysqld server, client and utility programs

Log files, databases, where /usr/local/
mysql/data/mysqld.local.err is the default
error log

Helper documents, like the Release Notes and
build information

Include (header) files

Libraries

Unix manual pages

MySQL test suite ('MySQL Test' is disabled by
default during the installation process when using
the installer package (DMG))

Miscellaneous support files, including error
messages, dictionary.txt, and rewriter SQL

Support scripts, such as
mysqld_multi.server, mysql.server, and
mysql-log-rotate.

/tmp/mysql.sock

Location of the MySQL Unix socket

2.4.3 Installing and Using the MySQL Launch Daemon

macOS uses launch daemons to automatically start, stop, and manage processes and applications
such as MySQL.

By default, the installation package (DMG) on macOS installs a launchd file named /Library/
LaunchDaemons/com.oracle.oss.mysql.mysqld.plist that contains a plist definition similar
to:

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>             <string>com.oracle.oss.mysql.mysqld</string>
    <key>ProcessType</key>       <string>Interactive</string>
    <key>Disabled</key>          <false/>

181

Installing and Using the MySQL Launch Daemon

    <key>RunAtLoad</key>         <true/>
    <key>KeepAlive</key>         <true/>
    <key>SessionCreate</key>     <true/>
    <key>LaunchOnlyOnce</key>    <false/>
    <key>UserName</key>          <string>_mysql</string>
    <key>GroupName</key>         <string>_mysql</string>
    <key>ExitTimeOut</key>       <integer>600</integer>
    <key>Program</key>           <string>/usr/local/mysql/bin/mysqld</string>
    <key>ProgramArguments</key>
        <array>
            <string>/usr/local/mysql/bin/mysqld</string>
            <string>--user=_mysql</string>
            <string>--basedir=/usr/local/mysql</string>
            <string>--datadir=/usr/local/mysql/data</string>
            <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
            <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
            <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
            <string>--keyring-file-data=/usr/local/mysql/keyring/keyring</string>
            <string>--early-plugin-load=keyring_file=keyring_file.so</string>
        </array>
    <key>WorkingDirectory</key>  <string>/usr/local/mysql</string>
</dict>
</plist>

Note

Some users report that adding a plist DOCTYPE declaration causes the
launchd operation to fail, despite it passing the lint check. We suspect it's a
copy-n-paste error. The md5 checksum of a file containing the above snippet is
d925f05f6d1b6ee5ce5451b596d6baed.

To enable the launchd service, you can either:

• Open macOS system preferences and select the MySQL preference panel, and then execute Start

MySQL Server.

182

Installing and Using the MySQL Launch Daemon

Figure 2.18 MySQL Preference Pane: Location

The Instances page includes an option to start or stop MySQL, and Initialize Database recreates
the data/ directory. Uninstall uninstalls MySQL Server and optionally the MySQL preference panel
and launchd information.

183

Installing and Using the MySQL Launch Daemon

Figure 2.19 MySQL Preference Pane: Instances

• Or, manually load the launchd file.

$> cd /Library/LaunchDaemons
$> sudo launchctl load -F com.oracle.oss.mysql.mysqld.plist

• To configure MySQL to automatically start at bootup, you can:

$> sudo launchctl load -w com.oracle.oss.mysql.mysqld.plist

Note

When upgrading MySQL server, the launchd installation process removes the
old startup items that were installed with MySQL server 5.7.7 and below.

Upgrading also replaces your existing launchd file named
com.oracle.oss.mysql.mysqld.plist.

Additional launchd related information:

• The plist entries override my.cnf entries, because they are passed in as command line arguments.
For additional information about passing in program options, see Section 6.2.2, “Specifying Program
Options”.

• The ProgramArguments section defines the command line options that are passed into the

program, which is the mysqld binary in this case.

184

Installing and Using the MySQL Preference Pane

• The default plist definition is written with less sophisticated use cases in mind. For more complicated
setups, you may want to remove some of the arguments and instead rely on a MySQL configuration
file, such as my.cnf.

• If you edit the plist file, then uncheck the installer option when reinstalling or upgrading MySQL.

Otherwise, your edited plist file is overwritten, and all edits are lost.

Because the default plist definition defines several ProgramArguments, you might remove most of
these arguments and instead rely upon your my.cnf MySQL configuration file to define them. For
example:

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>             <string>com.oracle.oss.mysql.mysqld</string>
    <key>ProcessType</key>       <string>Interactive</string>
    <key>Disabled</key>          <false/>
    <key>RunAtLoad</key>         <true/>
    <key>KeepAlive</key>         <true/>
    <key>SessionCreate</key>     <true/>
    <key>LaunchOnlyOnce</key>    <false/>
    <key>UserName</key>          <string>_mysql</string>
    <key>GroupName</key>         <string>_mysql</string>
    <key>ExitTimeOut</key>       <integer>600</integer>
    <key>Program</key>           <string>/usr/local/mysql/bin/mysqld</string>
    <key>ProgramArguments</key>
        <array>
            <string>/usr/local/mysql/bin/mysqld</string>
            <string>--user=_mysql</string>
            <string>--basedir=/usr/local/mysql</string>
            <string>--datadir=/usr/local/mysql/data</string>
            <string>--plugin-dir=/usr/local/mysql/lib/plugin</string>
            <string>--log-error=/usr/local/mysql/data/mysqld.local.err</string>
            <string>--pid-file=/usr/local/mysql/data/mysqld.local.pid</string>
            <string>--keyring-file-data=/usr/local/mysql/keyring/keyring</string>
            <string>--early-plugin-load=keyring_file=keyring_file.so</string>
        </array>
    <key>WorkingDirectory</key>  <string>/usr/local/mysql</string>
</dict>
</plist>

In this case, the basedir, datadir, plugin_dir, log_error, pid_file, keyring_file_data,
and --early-plugin-load options were removed from the default plist ProgramArguments
definition, which you might have defined in my.cnf instead.

2.4.4 Installing and Using the MySQL Preference Pane

The MySQL Installation Package includes a MySQL preference pane that enables you to start, stop,
and control automated startup during boot of your MySQL installation.

This preference pane is installed by default, and is listed under your system's System Preferences
window.

185

Installing and Using the MySQL Preference Pane

Figure 2.20 MySQL Preference Pane: Location

The MySQL preference pane is installed with the same DMG file that installs MySQL Server. Typically
it is installed with MySQL Server but it can be installed by itself too.

To install the MySQL preference pane:

1. Go through the process of installing the MySQL server, as described in the documentation at

Section 2.4.2, “Installing MySQL on macOS Using Native Packages”.

2. Click Customize at the Installation Type step. The "Preference Pane" option is listed there and

enabled by default; make sure it is not deselected. The other options, such as MySQL Server, can
be selected or deselected.

186

Installing and Using the MySQL Preference Pane

Figure 2.21 MySQL Package Installer Wizard: Customize

3. Complete the installation process.

Note

The MySQL preference pane only starts and stops MySQL installation installed
from the MySQL package installation that have been installed in the default
location.

Once the MySQL preference pane has been installed, you can control your MySQL server instance
using this preference pane.

The Instances page includes an option to start or stop MySQL, and Initialize Database recreates the
data/ directory. Uninstall uninstalls MySQL Server and optionally the MySQL preference panel and
launchd information.

187

Installing and Using the MySQL Preference Pane

Figure 2.22 MySQL Preference Pane: Instances

188

Installing and Using the MySQL Preference Pane

Figure 2.23 MySQL Preference Pane: Initialize Database

The Configuration page shows MySQL Server options including the path to the MySQL configuration
file.

189

Installing MySQL on Linux

Figure 2.24 MySQL Preference Pane: Configuration

The MySQL Preference Pane shows the current status of the MySQL server, showing stopped (in
red) if the server is not running and running (in green) if the server has already been started. The
preference pane also shows the current setting for whether the MySQL server has been set to start
automatically.

2.5 Installing MySQL on Linux

Linux supports a number of different solutions for installing MySQL. We recommend that you use one
of the distributions from Oracle, for which several methods for installation are available:

Table 2.8 Linux Installation Methods and Information

Type

Apt

Yum

Zypper

RPM

DEB

Generic

190

Setup Method

Additional Information

Enable the MySQL Apt
repository

Enable the MySQL Yum
repository

Enable the MySQL SLES
repository

Documentation

Documentation

Documentation

Download a specific package

Documentation

Download a specific package

Documentation

Download a generic package

Documentation

Installing MySQL on Linux Using the MySQL Yum Repository

Type

Source

Docker

Setup Method

Compile from source

Use the Oracle Container
Registry. You can also use My
Oracle Support for the MySQL
Enterprise Edition.

Additional Information

Documentation

Documentation

Oracle Unbreakable Linux
Network

Use ULN channels

Documentation

As an alternative, you can use the package manager on your system to automatically download and
install MySQL with packages from the native software repositories of your Linux distribution. These
native packages are often several versions behind the currently available release. You are also
normally unable to install innovation releases, since these are not usually made available in the native
repositories. For more information on using the native package installers, see Section 2.5.7, “Installing
MySQL on Linux from the Native Software Repositories”.

Note

For many Linux installations, you want to set up MySQL to be started
automatically when your machine starts. Many of the native package
installations perform this operation for you, but for source, binary and RPM
solutions you may need to set this up separately. The required script,
mysql.server, can be found in the support-files directory under the
MySQL installation directory or in a MySQL source tree. You can install it
as /etc/init.d/mysql for automatic MySQL startup and shutdown. See
Section 6.3.3, “mysql.server — MySQL Server Startup Script”.

2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository

The MySQL Yum repository for Oracle Linux, Red Hat Enterprise Linux, CentOS, and Fedora provides
RPM packages for installing the MySQL server, client, MySQL Workbench, MySQL Utilities, MySQL
Router, MySQL Shell, Connector/ODBC, Connector/Python and so on (not all packages are available
for all the distributions; see Installing Additional MySQL Products and Components with Yum for
details).

Before You Start

As a popular, open-source software, MySQL, in its original or re-packaged form, is widely installed on
many systems from various sources, including different software download sites, software repositories,
and so on. The following instructions assume that MySQL is not already installed on your system
using a third-party-distributed RPM package; if that is not the case, follow the instructions given
in Section 3.8, “Upgrading MySQL with the MySQL Yum Repository” or Replacing a Third-Party
Distribution of MySQL Using the MySQL Yum Repository.

Important

Repository setup RPM file names begin with mysql-84-lts-community to
highlight the default active MySQL subrepository, which is MySQL 8.4 today.
MySQL 8.0 must be manually enabled via your local repository configuration to
install MySQL 8.0 instead of MySQL 8.4.

Steps for a Fresh Installation of MySQL

Follow the steps below to install the latest GA version of MySQL with the MySQL Yum repository:

Adding the MySQL Yum Repository

1.

First, add the MySQL Yum repository to your system's repository list. This is a one-time operation,
which can be performed by installing an RPM provided by MySQL. Follow these steps:

191

Installing MySQL on Linux Using the MySQL Yum Repository

a. Go to the Download MySQL Yum Repository page (https://dev.mysql.com/downloads/repo/

yum/) in the MySQL Developer Zone.

b. Select and download the release package for your platform.

c.

Install the downloaded release package with the following command, replacing platform-
and-version-specific-package-name with the name of the downloaded RPM package:

$> sudo yum install platform-and-version-specific-package-name.rpm

For an EL6-based system, the command is in the form of (note the mysql80 prefix instead of
mysql84 because EL6-based systems do not support MySQL 8.4):

$> sudo yum install mysql80-community-release-el6-{version-number}.noarch.rpm

For an EL7-based system:

$> sudo yum install mysql84-community-release-el7-{version-number}.noarch.rpm

Fpr EL8 or later, change el7 to the version number of your Enterprise Linux.

For Fedora 41 and 42:

$> sudo dnf install mysql84-community-release-fcnn-{rpm-version-number}.noarch.rpm

Replace nn with the Fedora version and {rpm-version-number} with the rpm's version
number. For example, for:

mysql84-community-release-fc42-1.noarch.rpm

The installation command adds the MySQL Yum repository to your system's repository list and
downloads the GnuPG key to check the integrity of the software packages. See Section 2.1.4.2,
“Signature Checking Using GnuPG” for details on GnuPG key checking.

You can check that the MySQL Yum repository has been successfully added by the following
command (for dnf-enabled systems, replace yum in the command with dnf):

$> yum repolist enabled | grep "mysql.*-community.*"

Note

Once the MySQL Yum repository is enabled on your system, any system-
wide update by the yum update command (or dnf upgrade for dnf-
enabled systems) upgrades MySQL packages on your system and replaces
any native third-party packages, if Yum finds replacements for them in
the MySQL Yum repository; see Section 3.8, “Upgrading MySQL with the
MySQL Yum Repository”, for a discussion on some possible effects of that
on your system, see Upgrading the Shared Client Libraries.

Selecting a Release Series

2.

When using the MySQL Yum repository, the latest LTS series (currently MySQL 8.4) is selected for
installation by default. If you want to install MySQL 8.4 instead of 8.0 then skip this step.

Within the MySQL Yum repository, different release series of the MySQL Community Server are
hosted in different subrepositories. The subrepository for the latest GA series (currently MySQL
8.4) is enabled by default, and the subrepositories for all other series (for example, the MySQL 8.0
series) are disabled by default. Use this command to see all the subrepositories in the MySQL Yum

192

Installing MySQL on Linux Using the MySQL Yum Repository

repository, and see which of them are enabled or disabled (for dnf-enabled systems, replace yum in
the command with dnf):

$> yum repolist all | grep mysql

To install the latest release from the latest LTS series, no configuration is needed. To install the
latest release from a specific series other than the latest LTS series, disable the subrepository
for the latest LTS series and enable the subrepository for the specific series before running the
installation command. If your platform supports yum-config-manager, you can do that by issuing
these commands, which disable the subrepository for the 8.4 series and enable the one for the 8.0
series:

$> sudo yum-config-manager --disable mysql-8.4-lts-community
$> sudo yum-config-manager --disable mysql-tools-8.4-lts-community

$> sudo yum-config-manager --enable mysql80-community
$> sudo yum-config-manager --enable mysql-tools-community

For dnf-enabled platforms:

$> sudo dnf config-manager --disable mysql-8.4-lts-community
$> sudo dnf config-manager --disable mysql-tools-8.4-lts-community

$> sudo dnf config-manager --enable mysql80-community
$> sudo dnf config-manager --enable mysql-tools-community

Besides using yum-config-manager or the dnf config-manager command, you can also
select a release series by editing manually the /etc/yum.repos.d/mysql-community.repo
file. This is a typical entry for a MySQL 8.0 subrepository:

[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/9/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql-2023

Find the entry for the subrepository you want to configure, and edit the enabled option. Specify
enabled=0 to disable a subrepository, or enabled=1 to enable a subrepository. For example,
to install MySQL 8.0, make sure you have enabled=0 for the other MySQL series entries and
enabled=1 for MySQL 8.0.

You should only enable subrepository for one release series at any time. When subrepositories for
more than one release series are enabled, Yum uses the latest series.

Verify that the correct subrepositories have been enabled and disabled by running the following
command and checking its output (for dnf-enabled systems, replace yum in the command with
dnf):

$> yum repolist enabled | grep mysql

Disabling the Default MySQL Module

3.

(EL8 systems only) EL8-based systems such as RHEL8 and Oracle Linux 8 include a MySQL
module that is enabled by default. Unless this module is disabled, it masks packages provided by
MySQL repositories. To disable the included module and make the MySQL repository packages
visible, use the following command (for dnf-enabled systems, replace yum in the command with
dnf):

$> sudo yum module disable mysql

193

Installing MySQL on Linux Using the MySQL Yum Repository

4.
Installing MySQL

Install MySQL by the following command (for dnf-enabled systems, replace yum in the command
with dnf):

$> sudo yum install mysql-community-server

This installs the package for MySQL server (mysql-community-server) and also packages for
the components required to run the server, including packages for the client (mysql-community-
client), the common error messages and character sets for client and server (mysql-
community-common), and the shared client libraries (mysql-community-libs).

Starting the MySQL Server

5.

Start the MySQL server with the following command:

$> systemctl start mysqld

You can check the status of the MySQL server with the following command:

$> systemctl status mysqld

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the
arguments reversed) commands such as stop, start, status, and restart should be used to
manage the MySQL server service. The mysqld service is enabled by default, and it starts at system
reboot. See Section 2.5.9, “Managing MySQL Server with systemd” for additional information.

At the initial start up of the server, the following happens, given that the data directory of the server is
empty:

• The server is initialized.

• SSL certificate and key files are generated in the data directory.

• validate_password is installed and enabled.

• A superuser account 'root'@'localhost is created. A password for the superuser is set and

stored in the error log file. To reveal it, use the following command:

$> sudo grep 'temporary password' /var/log/mysqld.log

Change the root password as soon as possible by logging in with the generated, temporary
password and set a custom password for the superuser account:

$> mysql -uroot -p

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';

Note

validate_password is installed by default. The default password policy
implemented by validate_password requires that passwords contain at
least one uppercase letter, one lowercase letter, one digit, and one special
character, and that the total password length is at least 8 characters.

For more information on the postinstallation procedures, see Section 2.9, “Postinstallation Setup and
Testing”.

Note

Compatibility Information for EL7-based platforms: The following RPM packages
from the native software repositories of the platforms are incompatible with the
package from the MySQL Yum repository that installs the MySQL server. Once

194

Installing MySQL on Linux Using the MySQL APT Repository

you have installed MySQL using the MySQL Yum repository, you cannot install
these packages (and vice versa).

• akonadi-mysql

Installing Additional MySQL Products and Components with Yum

You can use Yum to install and manage individual components of MySQL. Some of these components
are hosted in sub-repositories of the MySQL Yum repository: for example, the MySQL Connectors
are to be found in the MySQL Connectors Community sub-repository, and the MySQL Workbench in
MySQL Tools Community. You can use the following command to list the packages for all the MySQL
components available for your platform from the MySQL Yum repository (for dnf-enabled systems,
replace yum in the command with dnf):

$> sudo yum --disablerepo=\* --enablerepo='mysql*-community*' list available

Install any packages of your choice with the following command, replacing package-name with name
of the package (for dnf-enabled systems, replace yum in the command with dnf):

$> sudo yum install package-name

For example, to install MySQL Workbench on Fedora:

$> sudo dnf install mysql-workbench-community

To install the shared client libraries (for dnf-enabled systems, replace yum in the command with dnf):

$> sudo yum install mysql-community-libs

Platform Specific Notes

ARM Support

ARM 64-bit (aarch64) is supported on Oracle Linux 7 and requires the Oracle Linux 7 Software
Collections Repository (ol7_software_collections). For example, to install the server:

$> yum-config-manager --enable ol7_software_collections
$> yum install mysql-community-server

Note

ARM 64-bit (aarch64) is supported on Oracle Linux 7 as of MySQL 8.0.12.

Known Limitation

The 8.0.12 release requires you to adjust the libstdc++7 path by executing ln
-s /opt/oracle/oracle-armtoolset-1/root/usr/lib64 /usr/
lib64/gcc7 after executing the yum install step.

Updating MySQL with Yum

Besides installation, you can also perform updates for MySQL products and components using the
MySQL Yum repository. See Section 3.8, “Upgrading MySQL with the MySQL Yum Repository” for
details.

2.5.2 Installing MySQL on Linux Using the MySQL APT Repository

The MySQL APT repository provides deb packages for installing and managing the MySQL server,
client, and other components on the current Debian and Ubuntu releases.

Instructions for using the MySQL APT Repository are available in A Quick Guide to Using the MySQL
APT Repository.

195

Installing MySQL on Linux Using the MySQL SLES Repository

2.5.3 Installing MySQL on Linux Using the MySQL SLES Repository

The MySQL SLES repository provides RPM packages for installing and managing the MySQL server,
client, and other components on SUSE Enterprise Linux Server.

Instructions for using the MySQL SLES repository are available in A Quick Guide to Using the MySQL
SLES Repository.

2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle

The recommended way to install MySQL on RPM-based Linux distributions is by using the RPM
packages provided by Oracle. There are two sources for obtaining them, for the Community Edition of
MySQL:

• From the MySQL software repositories:

• The MySQL Yum repository (see Section 2.5.1, “Installing MySQL on Linux Using the MySQL Yum

Repository” for details).

• The MySQL SLES repository (see Section 2.5.3, “Installing MySQL on Linux Using the MySQL

SLES Repository” for details).

• From the  Download MySQL Community Server page in the MySQL Developer Zone.

Note

RPM distributions of MySQL are also provided by other vendors. Be aware
that they may differ from those built by Oracle in features, capabilities,
and conventions (including communication setup), and that the installation
instructions in this manual do not necessarily apply to them. The vendor's
instructions should be consulted instead.

MySQL RPM Packages

Table 2.9 RPM Packages for MySQL Community Edition

Package Name

Summary

mysql-community-client

MySQL client applications and tools

mysql-community-client-plugins

Shared plugins for MySQL client applications

mysql-community-common

mysql-community-devel

mysql-community-embedded-compat

mysql-community-icu-data-files

mysql-community-libs

mysql-community-libs-compat

Common files for server and client libraries

Development header files and libraries for MySQL
database client applications

MySQL server as an embedded library with
compatibility for applications using version 18 of
the library

MySQL packaging of ICU data files needed by
MySQL regular expressions

Shared libraries for MySQL database client
applications

Shared compatibility libraries for previous MySQL
installations; only present if previous MySQL
versions are supported by the platform

mysql-community-server

Database server and related tools

mysql-community-server-debug

Debug server and plugin binaries

mysql-community-test

Test suite for the MySQL server

196

Installing MySQL on Linux Using RPM Packages from Oracle

Package Name

mysql-community

Additional *debuginfo* RPMs

Summary

The source code RPM looks similar to mysql-
community-8.0.42-1.el7.src.rpm, depending on
selected OS

There are several debuginfo packages: mysql-
community-client-debuginfo, mysql-community-
libs-debuginfo mysql-community-server-debug-
debuginfo mysql-community-server-debuginfo,
and mysql-community-test-debuginfo.

Table 2.10 RPM Packages for the MySQL Enterprise Edition

Package Name

mysql-commercial-backup

mysql-commercial-client

Summary

MySQL Enterprise Backup (added in 8.0.11)

MySQL client applications and tools

mysql-commercial-client-plugins

Shared plugins for MySQL client applications

mysql-commercial-common

mysql-commercial-devel

mysql-commercial-embedded-compat

mysql-commercial-icu-data-files

mysql-commercial-libs

mysql-commercial-libs-compat

Common files for server and client libraries

Development header files and libraries for MySQL
database client applications

MySQL server as an embedded library with
compatibility for applications using version 18 of
the library

MySQL packaging of ICU data files needed by
MySQL regular expressions

Shared libraries for MySQL database client
applications

Shared compatibility libraries for previous MySQL
installations; only present if previous MySQL
versions are supported by the platform. The
version of the libraries matches the version of the
libraries installed by default by the distribution you
are using.

mysql-commercial-server

Database server and related tools

mysql-commercial-test

Additional *debuginfo* RPMs

Test suite for the MySQL server

There are several debuginfo packages: mysql-
commercial-client-debuginfo, mysql-commercial-
libs-debuginfo mysql-commercial-server-debug-
debuginfo mysql-commercial-server-debuginfo,
and mysql-commercial-test-debuginfo.

The full names for the RPMs have the following syntax:

packagename-version-distribution-arch.rpm

The distribution and arch values indicate the Linux distribution and the processor type for which
the package was built. See the table below for lists of the distribution identifiers:

Table 2.11 MySQL Linux RPM Package Distribution Identifiers

Distribution Value

Intended Use

el{version} where {version} is the major
Enterprise Linux version, such as el8

EL6 (8.0), EL7, EL8, EL9, and EL10-based
platforms (for example, the corresponding

197

Installing MySQL on Linux Using RPM Packages from Oracle

Distribution Value

Intended Use
versions of Oracle Linux, Red Hat Enterprise
Linux, and CentOS)

fc{version} where {version} is the major
Fedora version, such as fc37

Fedora 41 and 42

sles12

SUSE Linux Enterprise Server 12

To see all files in an RPM package (for example, mysql-community-server), use the following
command:

$> rpm -qpl mysql-community-server-version-distribution-arch.rpm

The discussion in the rest of this section applies only to an installation process using the RPM
packages directly downloaded from Oracle, instead of through a MySQL repository.

Dependency relationships exist among some of the packages. If you plan to install many of the
packages, you may wish to download the RPM bundle tar file instead, which contains all the RPM
packages listed above, so that you need not download them separately.

In most cases, you need to install the mysql-community-server, mysql-community-client,
mysql-community-client-plugins, mysql-community-libs, mysql-community-icu-
data-files, mysql-community-common, and mysql-community-libs-compat packages to
get a functional, standard MySQL installation. To perform such a standard, basic installation, go to the
folder that contains all those packages (and, preferably, no other RPM packages with similar names),
and issue the following command:

$> sudo yum install mysql-community-{server,client,client-plugins,icu-data-files,common,libs}-*

Replace yum with zypper for SLES, and with dnf for Fedora.

While it is much preferable to use a high-level package management tool like yum to install the
packages, users who prefer direct rpm commands can replace the yum install command with the
rpm -Uvh command; however, using rpm -Uvh instead makes the installation process more prone to
failure, due to potential dependency issues the installation process might run into.

To install only the client programs, you can skip mysql-community-server in your list of packages
to install; issue the following command:

$> sudo yum install mysql-community-{client,client-plugins,common,libs}-*

Replace yum with zypper for SLES, and with dnf for Fedora.

A standard installation of MySQL using the RPM packages result in files and resources created under
the system directories, shown in the following table.

Table 2.12 MySQL Installation Layout for Linux RPM Packages from the MySQL Developer Zone

Files or Resources

Client programs and scripts

mysqld server

Configuration file

Data directory

Error log file

198

Location

/usr/bin

/usr/sbin

/etc/my.cnf

/var/lib/mysql

For RHEL, Oracle Linux, CentOS or Fedora
platforms: /var/log/mysqld.log

For SLES: /var/log/mysql/mysqld.log

Installing MySQL on Linux Using RPM Packages from Oracle

Files or Resources

Location

Value of secure_file_priv

/var/lib/mysql-files

System V init script

Systemd service

Pid file

Socket

Keyring directory

Unix manual pages

Include (header) files

Libraries

Miscellaneous support files (for example, error
messages, and character set files)

For RHEL, Oracle Linux, CentOS or Fedora
platforms: /etc/init.d/mysqld

For SLES: /etc/init.d/mysql

For RHEL, Oracle Linux, CentOS or Fedora
platforms: mysqld

For SLES: mysql

/var/run/mysql/mysqld.pid

/var/lib/mysql/mysql.sock

/var/lib/mysql-keyring

/usr/share/man

/usr/include/mysql

/usr/lib/mysql

/usr/share/mysql

The installation also creates a user named mysql and a group named mysql on the system.

Notes

• The mysql user is created using the -r and -s /bin/false options of the
useradd command, so that it does not have login permissions to your server
host (see Creating the mysql User and Group for details). To switch to the
mysql user on your OS, use the --shell=/bin/bash option for the su
command:

su - mysql --shell=/bin/bash

• Installation of previous versions of MySQL using older packages might have
created a configuration file named /usr/my.cnf. It is highly recommended
that you examine the contents of the file and migrate the desired settings
inside to the file /etc/my.cnf file, then remove /usr/my.cnf.

MySQL is NOT automatically started at the end of the installation process. For Red Hat Enterprise
Linux, Oracle Linux, CentOS, and Fedora systems, use the following command to start MySQL:

$> systemctl start mysqld

For SLES systems, the command is the same, but the service name is different:

$> systemctl start mysql

If the operating system is systemd enabled, standard systemctl (or alternatively, service with the
arguments reversed) commands such as stop, start, status, and restart should be used to
manage the MySQL server service. The mysqld service is enabled by default, and it starts at system
reboot. Notice that certain things might work differently on systemd platforms: for example, changing
the location of the data directory might cause issues. See Section 2.5.9, “Managing MySQL Server with
systemd” for additional information.

During an upgrade installation using RPM and DEB packages, if the MySQL server is running when
the upgrade occurs then the MySQL server is stopped, the upgrade occurs, and the MySQL server
is restarted. One exception: if the edition also changes during an upgrade (such as community to
commercial, or vice-versa), then MySQL server is not restarted.

199

Installing MySQL on Linux Using RPM Packages from Oracle

At the initial start up of the server, the following happens, given that the data directory of the server is
empty:

• The server is initialized.

• An SSL certificate and key files are generated in the data directory.

• validate_password is installed and enabled.

• A superuser account 'root'@'localhost' is created. A password for the superuser is set and

stored in the error log file. To reveal it, use the following command for RHEL, Oracle Linux, CentOS,
and Fedora systems:

$> sudo grep 'temporary password' /var/log/mysqld.log

Use the following command for SLES systems:

$> sudo grep 'temporary password' /var/log/mysql/mysqld.log

The next step is to log in with the generated, temporary password and set a custom password for the
superuser account:

$> mysql -uroot -p

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';

Note

validate_password is installed by default. The default password policy
implemented by validate_password requires that passwords contain at least
one uppercase letter, one lowercase letter, one digit, and one special character,
and that the total password length is at least 8 characters.

If something goes wrong during installation, you might find debug information in the error log file /var/
log/mysqld.log.

For some Linux distributions, it might be necessary to increase the limit on number of file descriptors
available to mysqld. See Section B.3.2.16, “File Not Found and Similar Errors”

Installing Client Libraries from Multiple MySQL Versions.
library versions, such as for the case that you want to maintain compatibility with older applications
linked against previous libraries. To install an older client library, use the --oldpackage option
with rpm. For example, to install mysql-community-libs-5.5 on an EL6 system that has
libmysqlclient.21 from MySQL 8.0, use a command like this:

 It is possible to install multiple client

$> rpm --oldpackage -ivh mysql-community-libs-5.5.50-2.el6.x86_64.rpm

 A special variant of MySQL Server compiled with the debug package has been

Debug Package.
included in the server RPM packages. It performs debugging and memory allocation checks and
produces a trace file when the server is running. To use that debug version, start MySQL with /
usr/sbin/mysqld-debug, instead of starting it as a service or with /usr/sbin/mysqld. See
Section 7.9.4, “The DBUG Package” for the debug options you can use.

Note

The default plugin directory for debug builds changed from /usr/lib64/
mysql/plugin to /usr/lib64/mysql/plugin/debug in MySQL 8.0.4.
Previously, it was necessary to change plugin_dir to /usr/lib64/mysql/
plugin/debug for debug builds.

Rebuilding RPMs from source SRPMs.
 Source code SRPM packages for MySQL are available for
download. They can be used as-is to rebuild the MySQL RPMs with the standard rpmbuild tool chain.

200

Installing MySQL on Linux Using Debian Packages from Oracle

2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle

Oracle provides Debian packages for installing MySQL on Debian or Debian-like Linux systems. The
packages are available through two different channels:

• The MySQL APT Repository. This is the preferred method for installing MySQL on Debian-like

systems, as it provides a simple and convenient way to install and update MySQL products. For
details, see Section 2.5.2, “Installing MySQL on Linux Using the MySQL APT Repository”.

• The MySQL Developer Zone's Download Area. For details, see Section 2.1.3, “How to Get MySQL”.
The following are some information on the Debian packages available there and the instructions for
installing them:

• Various Debian packages are provided in the MySQL Developer Zone for installing different

components of MySQL on the current Debian and Ubuntu platforms. The preferred method is
to use the tarball bundle, which contains the packages needed for a basic setup of MySQL.
The tarball bundles have names in the format of mysql-server_MVER-DVER_CPU.deb-
bundle.tar. MVER is the MySQL version and DVER is the Linux distribution version. The CPU
value indicates the processor type or family for which the package is built, as shown in the
following table:

Table 2.13 MySQL Debian and Ubuntu Installation Packages CPU Identifiers

CPU Value

i386

amd64

Intended Processor Type or Family

Pentium processor or better, 32 bit

64-bit x86 processor

• After downloading the tarball, unpack it with the following command:

$> tar -xvf mysql-server_MVER-DVER_CPU.deb-bundle.tar

•  You may need to install the libaio library if it is not already present on your system:

$> sudo apt-get install libaio1

• Preconfigure the MySQL server package with the following command:

$> sudo dpkg-preconfigure mysql-community-server_*.deb

You are asked to provide a password for the root user for your MySQL installation. You might also
be asked other questions regarding the installation.

Important

Make sure you remember the root password you set. Users who want
to set a password later can leave the password field blank in the
dialogue box and just press OK; in that case, root access to the server is
authenticated using the MySQL Socket Peer-Credential Authentication
Plugin for connections using a Unix socket file. You can set the root
password later using mysql_secure_installation.

• For a basic installation of the MySQL server, install the database common files package, the client
package, the client metapackage, the server package, and the server metapackage (in that order);
you can do that with a single command:

$> sudo dpkg -i mysql-{common,community-client-plugins,community-client-core,community-client,client,community-server-core,community-server,server}_*.deb

There are also packages with server-core and client-core in the package names. These
contain binaries only and are installed automatically by the standard packages. Installing them by
themselves does not result in a functioning MySQL setup.

201

Deploying MySQL on Linux with Docker Containers

If you are being warned of unmet dependencies by dpkg (such as libmecab2), you can fix them
using apt-get:

sudo apt-get -f install

Here are where the files are installed on the system:

• All configuration files (like my.cnf) are under /etc/mysql

• All binaries, libraries, headers, etc., are under /usr/bin and /usr/sbin

• The data directory is under /var/lib/mysql

Note

Debian distributions of MySQL are also provided by other vendors. Be aware
that they may differ from those built by Oracle in features, capabilities, and
conventions (including communication setup), and that the instructions in this
manual do not necessarily apply to installing them. The vendor's instructions
should be consulted instead.

2.5.6 Deploying MySQL on Linux with Docker Containers

This section explains how to deploy MySQL Server using Docker containers.

While the docker client is used in the following instructions for demonstration purposes, in general, the
MySQL container images provided by Oracle work with any container tools that are compliant with the
OCI 1.0 specification.

Warning

Before deploying MySQL with Docker containers, make sure you understand
the security risks of running containers and mitigate them properly.

2.5.6.1 Basic Steps for MySQL Server Deployment with Docker

Warning

The MySQL Docker images maintained by the MySQL team are built
specifically for Linux platforms. Other platforms are not supported, and users
using these MySQL Docker images on them are doing so at their own risk. See
the discussion here for some known limitations for running these containers on
non-Linux operating systems.

• Downloading a MySQL Server Docker Image

• Starting a MySQL Server Instance

• Connecting to MySQL Server from within the Container

• Container Shell Access

• Stopping and Deleting a MySQL Container

• Upgrading a MySQL Server Container

• More Topics on Deploying MySQL Server with Docker

202

Deploying MySQL on Linux with Docker Containers

Downloading a MySQL Server Docker Image

Important

For users of MySQL Enterprise Edition: A subscription is required to use the
Docker images for MySQL Enterprise Edition. Subscriptions work by a Bring
Your Own License model; see How to Buy MySQL Products and Services for
details.

Downloading the server image in a separate step is not strictly necessary; however, performing this
step before you create your Docker container ensures your local image is up to date. To download the
MySQL Community Edition image from the Oracle Container Registry (OCR), run this command:

docker pull container-registry.oracle.com/mysql/community-server:tag

The tag is the label for the image version you want to pull (for example, 5.7, 8.0, or latest). If :tag
is omitted, the latest label is used, and the image for the latest GA version of MySQL Community
Server is downloaded.

To download the MySQL Enterprise Edition image from the OCR, you need to first accept the license
agreement on the OCR and log in to the container repository with your Docker client. Follow these
steps:

• Visit the OCR at https://container-registry.oracle.com/ and choose MySQL.

• Under the list of MySQL repositories, choose enterprise-server.

• If you have not signed in to the OCR yet, click the Sign in button on the right of the page, and then

enter your Oracle account credentials when prompted to.

• Follow the instructions on the right of the page to accept the license agreement.

• Log in to the OCR with your container client using, for example, the docker login command:

# docker login container-registry.oracle.com
Username: Oracle-Account-ID
Password: password
Login successful.

Download the Docker image for MySQL Enterprise Edition from the OCR with this command:

docker pull  container-registry.oracle.com/mysql/enterprise-server:tag

To download the MySQL Enterprise Edition image from My Oracle Support website, go onto the
website, sign in to your Oracle account, and perform these steps once you are on the landing page:

• Select the Patches and Updates tab.

• Go to the Patch Search region and, on the Search tab, switch to the Product or Family

(Advanced) subtab.

• Enter “MySQL Server” for the Product field, and the desired version number in the Release field.

• Use the dropdowns for additional filters to select Description—contains, and enter “Docker” in the

text field.

The following figure shows the search settings for the MySQL Enterprise Edition image for MySQL
Server 8.0:

203

Deploying MySQL on Linux with Docker Containers

• Click the Search button and, from the result list, select the version you want, and click the Download

button.

• In the File Download dialogue box that appears, click and download the .zip file for the Docker

image.

Unzip the downloaded .zip archive to obtain the tarball inside (mysql-enterprise-
server-version.tar), and then load the image by running this command:

docker load -i mysql-enterprise-server-version.tar

You can list downloaded Docker images with this command:

$> docker images
REPOSITORY                                             TAG       IMAGE ID       CREATED        SIZE
container-registry.oracle.com/mysql/community-server   latest    1d9c2219ff69   2 months ago   496MB

Starting a MySQL Server Instance

To start a new Docker container for a MySQL Server, use the following command:

docker run --name=container_name  --restart on-failure -d image_name:tag

image_name is the name of the image to be used to start the container; see Downloading a MySQL
Server Docker Image for more information.

The --name option, for supplying a custom name for your server container, is optional; if no container
name is supplied, a random one is generated.

The --restart option is for configuring the restart policy for your container; it should be set to the
value on-failure, to enable support for server restart within a client session (which happens, for
example, when the RESTART statement is executed by a client or during the configuration of an
InnoDB cluster instance). With the support for restart enabled, issuing a restart within a client session
causes the server and the container to stop and then restart. Support for server restart is available for
MySQL 8.0.21 and later.

For example, to start a new Docker container for the MySQL Community Server, use this command:

docker run --name=mysql1 --restart on-failure -d container-registry.oracle.com/mysql/community-server:latest

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded
from the OCR, use this command:

docker run --name=mysql1 --restart on-failure -d container-registry.oracle.com/mysql/enterprise-server:latest

To start a new Docker container for the MySQL Enterprise Server with a Docker image downloaded
from My Oracle Support, use this command:

docker run --name=mysql1 --restart on-failure -d mysql/enterprise-server:latest

If the Docker image of the specified name and tag has not been downloaded by an earlier docker
pull or docker run command, the image is now downloaded. Initialization for the container begins,

204

Deploying MySQL on Linux with Docker Containers

and the container appears in the list of running containers when you run the docker ps command.
For example:

$> docker ps
CONTAINER ID   IMAGE                                                         COMMAND                  CREATED          STATUS                    PORTS                       NAMES
4cd4129b3211   container-registry.oracle.com/mysql/community-server:latest   "/entrypoint.sh mysq…"   8 seconds ago    Up 7 seconds (health: starting)   3306/tcp, 33060-33061/tcp   mysql1

The container initialization might take some time. When the server is ready for use, the STATUS of
the container in the output of the docker ps command changes from (health: starting) to
(healthy).

The -d option used in the docker run command above makes the container run in the background.
Use this command to monitor the output from the container:

docker logs mysql1

Once initialization is finished, the command's output is going to contain the random password
generated for the root user; check the password with, for example, this command:

$> docker logs mysql1 2>&1 | grep GENERATED
GENERATED ROOT PASSWORD: Axegh3kAJyDLaRuBemecis&EShOs

Connecting to MySQL Server from within the Container

Once the server is ready, you can run the mysql client within the MySQL Server container you just
started, and connect it to the MySQL Server. Use the docker exec -it command to start a mysql
client inside the Docker container you have started, like the following:

docker exec -it mysql1 mysql -uroot -p

When asked, enter the generated root password (see the last step in Starting a MySQL Server
Instance above on how to find the password). Because the MYSQL_ONETIME_PASSWORD option is
true by default, after you have connected a mysql client to the server, you must reset the server root
password by issuing this statement:

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';

Substitute password with the password of your choice. Once the password is reset, the server is
ready for use.

Container Shell Access

To have shell access to your MySQL Server container, use the docker exec -it command to start
a bash shell inside the container:

$> docker exec -it mysql1 bash
bash-4.2#

You can then run Linux commands inside the container. For example, to view contents in the server's
data directory inside the container, use this command:

bash-4.2# ls /var/lib/mysql
auto.cnf    ca.pem      client-key.pem  ib_logfile0  ibdata1  mysql       mysql.sock.lock    private_key.pem  server-cert.pem  sys
ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile1  ibtmp1   mysql.sock  performance_schema  public_key.pem   server-key.pem

Stopping and Deleting a MySQL Container

To stop the MySQL Server container we have created, use this command:

docker stop mysql1

docker stop sends a SIGTERM signal to the mysqld process, so that the server is shut down
gracefully.

Also notice that when the main process of a container (mysqld in the case of a MySQL Server
container) is stopped, the Docker container stops automatically.

To start the MySQL Server container again:

205

Deploying MySQL on Linux with Docker Containers

docker start mysql1

To stop and start again the MySQL Server container with a single command:

docker restart mysql1

To delete the MySQL container, stop it first, and then use the docker rm command:

docker stop mysql1

docker rm mysql1

If you want the Docker volume for the server's data directory to be deleted at the same time, add the -
v option to the docker rm command.

Upgrading a MySQL Server Container

Important

• Before performing any upgrade to MySQL, follow carefully the instructions in
Chapter 3, Upgrading MySQL. Among other instructions discussed there, it is
especially important to back up your database before the upgrade.

• The instructions in this section require that the server's data and configuration

have been persisted on the host. See Persisting Data and Configuration
Changes for details.

Follow these steps to upgrade a Docker installation of MySQL 5.7 to 8.0:

• Stop the MySQL 5.7 server (container name is mysql57 in this example):

docker stop mysql57

• Download the MySQL 8.0 Server Docker image. See instructions in Downloading a MySQL Server

Docker Image. Make sure you use the right tag for MySQL 8.0.

• Start a new MySQL 8.0 Docker container (named mysql80 in this example) with the old server data
and configuration (with proper modifications if needed—see Chapter 3, Upgrading MySQL) that have
been persisted on the host (by bind-mounting in this example). For the MySQL Community Server,
run this command:

docker run --name=mysql80 \
   --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
   --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
   -d container-registry.oracle.com/mysql/community-server:8.0

If needed, adjust container-registry.oracle.com/mysql/community-server to the
correct image name—for example, replace it with container-registry.oracle.com/mysql/
enterprise-server for MySQL Enterprise Edition images downloaded from the OCR, or mysql/
enterprise-server for MySQL Enterprise Edition images downloaded from My Oracle Support.

• Wait for the server to finish startup. You can check the status of the server using the docker ps

command (see Starting a MySQL Server Instance for how to do that).

Follow the same steps for upgrading within the 8.0 series (that is, from release 8.0.x to 8.0.y): stop the
original container, and start a new one with a newer image on the old server data and configuration.
If you used the 8.0 or the latest tag when starting your original container and there is now a new
MySQL 8.0 release you want to upgrade to it, you must first pull the image for the new release with the
command:

docker pull container-registry.oracle.com/mysql/community-server:8.0

You can then upgrade by starting a new container with the same tag on the old data and configuration
(adjust the image name if you are using the MySQL Enterprise Edition; see Downloading a MySQL
Server Docker Image):

206

Deploying MySQL on Linux with Docker Containers

docker run --name=mysql80new \
   --mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
   --mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
   -d container-registry.oracle.com/mysql/community-server:8.0

Note

For MySQL 8.0.15 and earlier: You need to complete the upgrade process by
running the mysql_upgrade utility in the MySQL 8.0 Server container (the step is
not required for MySQL 8.0.16 and later):

• docker exec -it mysql80 mysql_upgrade -uroot -p

When prompted, enter the root password for your old server.

• Finish the upgrade by restarting the new container:

docker restart mysql80

More Topics on Deploying MySQL Server with Docker

For more topics on deploying MySQL Server with Docker like server configuration, persisting data and
configuration, server error log, and container environment variables, see Section 2.5.6.2, “More Topics
on Deploying MySQL Server with Docker”.

2.5.6.2 More Topics on Deploying MySQL Server with Docker

Note

Most of the following sample commands have container-
registry.oracle.com/mysql/community-server as the Docker image
being used (like with the docker pull and docker run commands); change
that if your image is from another repository—for example, replace it with
container-registry.oracle.com/mysql/enterprise-server for
MySQL Enterprise Edition images downloaded from the Oracle Container
Registry (OCR), or mysql/enterprise-server for MySQL Enterprise
Edition images downloaded from My Oracle Support.

• The Optimized MySQL Installation for Docker

• Configuring the MySQL Server

• Persisting Data and Configuration Changes

• Running Additional Initialization Scripts

• Connect to MySQL from an Application in Another Docker Container

• Server Error Log

• Using MySQL Enterprise Backup with Docker

• Using mysqldump with Docker

• Known Issues

• Docker Environment Variables

The Optimized MySQL Installation for Docker

Docker images for MySQL are optimized for code size, which means they only include crucial
components that are expected to be relevant for the majority of users who run MySQL instances in

207

Deploying MySQL on Linux with Docker Containers

Docker containers. A MySQL Docker installation is different from a common, non-Docker installation in
the following aspects:

• Only a limited number of binaries are included.

• All binaries are stripped; they contain no debug information.

Warning

Any software updates or installations users perform to the Docker container
(including those for MySQL components) may conflict with the optimized
MySQL installation created by the Docker image. Oracle does not provide
support for MySQL products running in such an altered container, or a container
created from an altered Docker image.

Configuring the MySQL Server

When you start the MySQL Docker container, you can pass configuration options to the server through
the docker run command. For example:

docker run --name mysql1 -d container-registry.oracle.com/mysql/community-server:tag --character-set-server=utf8mb4 --collation-server=utf8mb4_col

The command starts the MySQL Server with utf8mb4 as the default character set and utf8mb4_col
as the default collation for databases.

Another way to configure the MySQL Server is to prepare a configuration file and mount it at the
location of the server configuration file inside the container. See Persisting Data and Configuration
Changes for details.

Persisting Data and Configuration Changes

Docker containers are in principle ephemeral, and any data or configuration are expected to be lost if
the container is deleted or corrupted (see discussions here). Docker volumes provides a mechanism to
persist data created inside a Docker container. At its initialization, the MySQL Server container creates
a Docker volume for the server data directory. The JSON output from the docker inspect command
on the container includes a Mount key, whose value provides information on the data directory volume:

$> docker inspect mysql1
...
 "Mounts": [
            {
                "Type": "volume",
                "Name": "4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652",
                "Source": "/var/lib/docker/volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/_data",
                "Destination": "/var/lib/mysql",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
        ],
...

The output shows that the source directory /var/lib/docker/
volumes/4f2d463cfc4bdd4baebcb098c97d7da3337195ed2c6572bc0b89f7e845d27652/
_data, in which data is persisted on the host, has been mounted at /var/lib/mysql, the server
data directory inside the container.

Another way to preserve data is to bind-mount a host directory using the --mount option when
creating the container. The same technique can be used to persist the configuration of the server. The
following command creates a MySQL Server container and bind-mounts both the data directory and
the server configuration file:

docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \

208

Deploying MySQL on Linux with Docker Containers

--mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \
-d container-registry.oracle.com/mysql/community-server:tag

The command mounts path-on-host-machine/my.cnf at /etc/my.cnf (the server configuration
file inside the container), and path-on-host-machine/datadir at /var/lib/mysql (the data
directory inside the container). The following conditions must be met for the bind-mounting to work:

• The configuration file path-on-host-machine/my.cnf must already exist, and it must contain the

specification for starting the server by the user mysql:

[mysqld]
user=mysql

You can also include other server configuration options in the file.

• The data directory path-on-host-machine/datadir must already exist. For server initialization
to happen, the directory must be empty. You can also mount a directory prepopulated with data
and start the server with it; however, you must make sure you start the Docker container with the
same configuration as the server that created the data, and any host files or directories required are
mounted when starting the container.

Running Additional Initialization Scripts

If there are any .sh or .sql scripts you want to run on the database immediately after it has
been created, you can put them into a host directory and then mount the directory at /docker-
entrypoint-initdb.d/ inside the container. For example:

docker run --name=mysql1 \
--mount type=bind,src=/path-on-host-machine/scripts/,dst=/docker-entrypoint-initdb.d/ \
-d container-registry.oracle.com/mysql/community-server:tag

Connect to MySQL from an Application in Another Docker Container

By setting up a Docker network, you can allow multiple Docker containers to communicate with each
other, so that a client application in another Docker container can access the MySQL Server in the
server container. First, create a Docker network:

docker network create my-custom-net

Then, when you are creating and starting the server and the client containers, use the --network
option to put them on network you created. For example:

docker run --name=mysql1 --network=my-custom-net -d container-registry.oracle.com/mysql/community-server

docker run --name=myapp1 --network=my-custom-net -d myapp

The myapp1 container can then connect to the mysql1 container with the mysql1 hostname and
vice versa, as Docker automatically sets up a DNS for the given container names. In the following
example, we run the mysql client from inside the myapp1 container to connect to host mysql1 in its
own container:

docker exec -it myapp1 mysql --host=mysql1 --user=myuser --password

For other networking techniques for containers, see the Docker container networking section in the
Docker Documentation.

Server Error Log

When the MySQL Server is first started with your server container, a server error log is NOT generated
if either of the following conditions is true:

• A server configuration file from the host has been mounted, but the file does not contain the system
variable log_error (see Persisting Data and Configuration Changes on bind-mounting a server
configuration file).

209

Deploying MySQL on Linux with Docker Containers

• A server configuration file from the host has not been mounted, but the Docker environment

variable MYSQL_LOG_CONSOLE is true (which is the variable's default state for MySQL 8.0 server
containers). The MySQL Server's error log is then redirected to stderr, so that the error log goes
into the Docker container's log and is viewable using the docker logs mysqld-container
command.

To make MySQL Server generate an error log when either of the two conditions is true, use the --
log-error option to configure the server to generate the error log at a specific location inside the
container. To persist the error log, mount a host file at the location of the error log inside the container
as explained in Persisting Data and Configuration Changes. However, you must make sure your
MySQL Server inside its container has write access to the mounted host file.

Using MySQL Enterprise Backup with Docker

MySQL Enterprise Backup is a commercially-licensed backup utility for MySQL Server, available with
MySQL Enterprise Edition. MySQL Enterprise Backup is included in the Docker installation of MySQL
Enterprise Edition.

In the following example, we assume that you already have a MySQL Server running in a Docker
container (see Section 2.5.6.1, “Basic Steps for MySQL Server Deployment with Docker” on how to
start a MySQL Server instance with Docker). For MySQL Enterprise Backup to back up the MySQL
Server, it must have access to the server's data directory. This can be achieved by, for example, bind-
mounting a host directory on the data directory of the MySQL Server when you start the server:

docker run --name=mysqlserver \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
-d mysql/enterprise-server:8.0

With this command, the MySQL Server is started with a Docker image of the MySQL Enterprise
Edition, and the host directory /path-on-host-machine/datadir/ has been mounted onto the
server's data directory (/var/lib/mysql) inside the server container. We also assume that, after the
server has been started, the required privileges have also been set up for MySQL Enterprise Backup to
access the server (see Grant MySQL Privileges to Backup Administrator, for details). Use the following
steps to back up and restore a MySQL Server instance.

To back up a MySQL Server instance running in a Docker container using MySQL Enterprise Backup
with Docker, follow the steps listed here:

1. On the same host where the MySQL Server container is running, start another container with

an image of MySQL Enterprise Edition to perform a back up with the MySQL Enterprise Backup
command backup-to-image. Provide access to the server's data directory using the bind mount
we created in the last step. Also, mount a host directory (/path-on-host-machine/backups/
in this example) onto the storage folder for backups in the container (/data/backups in the
example) to persist the backups we are creating. Here is a sample command for this step, in which
MySQL Enterprise Backup is started with a Docker image downloaded from My Oracle Support:

$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm mysql/enterprise-server:8.0 \
mysqlbackup -umysqlbackup -ppassword --backup-dir=/tmp/backup-tmp --with-timestamp \
--backup-image=/data/backups/db.mbi backup-to-image

[Entrypoint] MySQL Docker Image 8.0.11-1.1.5
MySQL Enterprise Backup version 8.0.11 Linux-4.1.12-61.1.16.el7uek.x86_64-x86_64 [2018-04-08  07:06:45]
Copyright (c) 2003, 2018, Oracle and/or its affiliates. All Rights Reserved.

180921 17:27:25 MAIN    INFO: A thread created with Id '140594390935680'
180921 17:27:25 MAIN    INFO: Starting with following command line ...
...

-------------------------------------------------------------
   Parameters Summary
-------------------------------------------------------------

210

Deploying MySQL on Linux with Docker Containers

   Start LSN                  : 29615616
   End LSN                    : 29651854
-------------------------------------------------------------

mysqlbackup completed OK!

It is important to check the end of the output by mysqlbackup to make sure the backup has been
completed successfully.

2. The container exits once the backup job is finished and, with the --rm option used to start it, it is
removed after it exits. An image backup has been created, and can be found in the host directory
mounted in the last step for storing backups, as shown here:

$> ls /tmp/backups
db.mbi

To restore a MySQL Server instance in a Docker container using MySQL Enterprise Backup with
Docker, follow the steps listed here:

1. Stop the MySQL Server container, which also stops the MySQL Server running inside:

docker stop mysqlserver

2. On the host, delete all contents in the bind mount for the MySQL Server data directory:

rm -rf /path-on-host-machine/datadir/*

3. Start a container with an image of MySQL Enterprise Edition to perform the restore with the

MySQL Enterprise Backup command copy-back-and-apply-log. Bind-mount the server's data
directory and the storage folder for the backups, like what we did when we backed up the server:

$> docker run \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm mysql/enterprise-server:8.0 \
mysqlbackup --backup-dir=/tmp/backup-tmp --with-timestamp \
--datadir=/var/lib/mysql --backup-image=/data/backups/db.mbi copy-back-and-apply-log

[Entrypoint] MySQL Docker Image 8.0.11-1.1.5
MySQL Enterprise Backup version 8.0.11 Linux-4.1.12-61.1.16.el7uek.x86_64-x86_64 [2018-04-08  07:06:45]
Copyright (c) 2003, 2018, Oracle and/or its affiliates. All Rights Reserved.

180921 22:06:52 MAIN    INFO: A thread created with Id '139768047519872'
180921 22:06:52 MAIN    INFO: Starting with following command line ...
...
180921 22:06:52 PCR1    INFO: We were able to parse ibbackup_logfile up to
          lsn 29680612.
180921 22:06:52 PCR1    INFO: Last MySQL binlog file position 0 155, file name binlog.000003
180921 22:06:52 PCR1    INFO: The first data file is '/var/lib/mysql/ibdata1'
                              and the new created log files are at '/var/lib/mysql'
180921 22:06:52 MAIN    INFO: No Keyring file to process.
180921 22:06:52 MAIN    INFO: Apply-log operation completed successfully.
180921 22:06:52 MAIN    INFO: Full Backup has been restored successfully.

mysqlbackup completed OK! with 3 warnings

The container exits once the backup job is finished and, with the --rm option used when starting it,
it is removed after it exits.

4. Restart the server container, which also restarts the restored server, using the following command:

docker restart mysqlserver

Or, start a new MySQL Server on the restored data directory, as shown here:

docker run --name=mysqlserver2 \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
-d mysql/enterprise-server:8.0

211

Deploying MySQL on Linux with Docker Containers

Log on to the server to check that the server is running with the restored data.

Using mysqldump with Docker

Besides using MySQL Enterprise Backup to back up a MySQL Server running in a Docker container,
you can perform a logical backup of your server by using the mysqldump utility, run inside a Docker
container.

The following instructions assume that you already have a MySQL Server running in a Docker
container and, when the container was first started, a host directory /path-on-host-machine/
datadir/ has been mounted onto the server's data directory /var/lib/mysql (see bind-mounting
a host directory on the data directory of the MySQL Server for details), which contains the Unix socket
file by which mysqldump and mysql can connect to the server. We also assume that, after the server
has been started, a user with the proper privileges (admin in this example) has been created, with
which mysqldump can access the server. Use the following steps to back up and restore MySQL
Server data:

Backing up MySQL Server data using mysqldump with Docker:

1. On the same host where the MySQL Server container is running, start another container with an
image of MySQL Server to perform a backup with the mysqldump utility (see documentation of
the utility for its functionality, options, and limitations). Provide access to the server's data directory
by bind mounting /path-on-host-machine/datadir/. Also, mount a host directory (/path-
on-host-machine/backups/ in this example) onto a storage folder for backups inside the
container (/data/backups is used in this example) to persist the backups you are creating. Here
is a sample command for backing up all databases on the server using this setup:

$> docker run --entrypoint "/bin/sh" \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0 \
-c "mysqldump -uadmin --password='password' --all-databases > /data/backups/all-databases.sql"

In the command, the --entrypoint option is used so that the system shell is invoked after the
container is started, and the -c option is used to specify the mysqldump command to be run in the
shell, whose output is redirected to the file all-databases.sql in the backup directory.

2. The container exits once the backup job is finished and, with the --rm option used to start it, it
is removed after it exits. A logical backup been created, and can be found in the host directory
mounted for storing the backup, as shown here:

$> ls /path-on-host-machine/backups/
all-databases.sql

Restoring MySQL Server data using mysqldump with Docker:

1. Make sure you have a MySQL Server running in a container, onto which you want your backed-up

data to be restored.

2. Start a container with an image of MySQL Server to perform the restore with a mysql client. Bind-

mount the server's data directory, as well as the storage folder that contains your backup:

$> docker run  \
--mount type=bind,src=/path-on-host-machine/datadir/,dst=/var/lib/mysql \
--mount type=bind,src=/path-on-host-machine/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0 \
mysql -uadmin --password='password' -e "source /data/backups/all-databases.sql"

The container exits once the backup job is finished and, with the --rm option used when starting it,
it is removed after it exits.

3. Log on to the server to check that the restored data is now on the server.

212

Deploying MySQL on Linux with Docker Containers

Known Issues

• When using the server system variable audit_log_file to configure the audit log file name, use

the loose option modifier with it; otherwise, Docker cannot start the server.

Docker Environment Variables

When you create a MySQL Server container, you can configure the MySQL instance by using the --
env option (short form -e) and specifying one or more environment variables. No server initialization is
performed if the mounted data directory is not empty, in which case setting any of these variables has
no effect (see Persisting Data and Configuration Changes), and no existing contents of the directory,
including server settings, are modified during container startup.

Environment variables which can be used to configure a MySQL instance are listed here:

• The boolean variables including MYSQL_RANDOM_ROOT_PASSWORD, MYSQL_ONETIME_PASSWORD,
MYSQL_ALLOW_EMPTY_PASSWORD, and MYSQL_LOG_CONSOLE are made true by setting them with
any strings of nonzero lengths. Therefore, setting them to, for example, “0”, “false”, or “no” does not
make them false, but actually makes them true. This is a known issue.

• MYSQL_RANDOM_ROOT_PASSWORD: When this variable is true (which is its default state, unless
MYSQL_ROOT_PASSWORD is set or MYSQL_ALLOW_EMPTY_PASSWORD is set to true), a random
password for the server's root user is generated when the Docker container is started. The password
is printed to stdout of the container and can be found by looking at the container’s log (see Starting
a MySQL Server Instance).

• MYSQL_ONETIME_PASSWORD: When the variable is true (which is its default state, unless

MYSQL_ROOT_PASSWORD is set or MYSQL_ALLOW_EMPTY_PASSWORD is set to true), the root user's
password is set as expired and must be changed before MySQL can be used normally.

• MYSQL_DATABASE: This variable allows you to specify the name of a database to be

created on image startup. If a user name and a password are supplied with MYSQL_USER
and MYSQL_PASSWORD, the user is created and granted superuser access to this database
(corresponding to GRANT ALL). The specified database is created by a CREATE DATABASE IF
NOT EXIST statement, so that the variable has no effect if the database already exists.

• MYSQL_USER, MYSQL_PASSWORD: These variables are used in conjunction to create a user and set
that user's password, and the user is granted superuser permissions for the database specified by
the MYSQL_DATABASE variable. Both MYSQL_USER and MYSQL_PASSWORD are required for a user
to be created—if any of the two variables is not set, the other is ignored. If both variables are set but
MYSQL_DATABASE is not, the user is created without any privileges.

Note

There is no need to use this mechanism to create the root
superuser, which is created by default with the password set by
either one of the mechanisms discussed in the descriptions for
MYSQL_ROOT_PASSWORD and MYSQL_RANDOM_ROOT_PASSWORD, unless
MYSQL_ALLOW_EMPTY_PASSWORD is true.

• MYSQL_ROOT_HOST: By default, MySQL creates the 'root'@'localhost' account. This account
can only be connected to from inside the container as described in Connecting to MySQL Server
from within the Container. To allow root connections from other hosts, set this environment variable.
For example, the value 172.17.0.1, which is the default Docker gateway IP, allows connections
from the host machine that runs the container. The option accepts only one entry, but wildcards are
allowed (for example, MYSQL_ROOT_HOST=172.*.*.* or MYSQL_ROOT_HOST=%).

• MYSQL_LOG_CONSOLE: When the variable is true (which is its default state for MySQL 8.0 server

containers), the MySQL Server's error log is redirected to stderr, so that the error log goes into the
Docker container's log and is viewable using the docker logs mysqld-container command.

213

Installing MySQL on Linux from the Native Software Repositories

Note

The variable has no effect if a server configuration file from the host has been
mounted (see Persisting Data and Configuration Changes on bind-mounting a
configuration file).

• MYSQL_ROOT_PASSWORD: This variable specifies a password that is set for the MySQL root account.

Warning

Setting the MySQL root user password on the command line is insecure. As
an alternative to specifying the password explicitly, you can set the variable
with a container file path for a password file, and then mount a file from
your host that contains the password at the container file path. This is still
not very secure, as the location of the password file is still exposed. It is
preferable to use the default settings of MYSQL_RANDOM_ROOT_PASSWORD
and MYSQL_ONETIME_PASSWORD both being true.

• MYSQL_ALLOW_EMPTY_PASSWORD. Set it to true to allow the container to be started with a blank

password for the root user.

Warning

Setting this variable to true is insecure, because it is going to leave
your MySQL instance completely unprotected, allowing anyone to gain
complete superuser access. It is preferable to use the default settings of
MYSQL_RANDOM_ROOT_PASSWORD and MYSQL_ONETIME_PASSWORD both
being true.

2.5.6.3 Deploying MySQL on Windows and Other Non-Linux Platforms with Docker

Warning

The MySQL Docker images provided by Oracle are built specifically for Linux
platforms. Other platforms are not supported, and users running the MySQL
Docker images from Oracle on them are doing so at their own risk. This
section discusses some known issues for the images when used on non-Linux
platforms.

Known Issues for using the MySQL Server Docker images from Oracle on Windows include:

• If you are bind-mounting on the container's MySQL data directory (see Persisting Data and

Configuration Changes for details), you have to set the location of the server socket file with the --
socket option to somewhere outside of the MySQL data directory; otherwise, the server fails to
start. This is because the way Docker for Windows handles file mounting does not allow a host file
from being bind-mounted on the socket file.

2.5.7 Installing MySQL on Linux from the Native Software Repositories

Many Linux distributions include a version of the MySQL server, client tools, and development
components in their native software repositories and can be installed with the platforms' standard
package management systems. This section provides basic instructions for installing MySQL using
those package management systems.

Important

Native packages are often several versions behind the currently available
release. You are also normally unable to install development milestone releases
(DMRs), since these are not usually made available in the native repositories.

214

Installing MySQL on Linux from the Native Software Repositories

Before proceeding, we recommend that you check out the other installation
options described in Section 2.5, “Installing MySQL on Linux”.

Distribution specific instructions are shown below:

• Red Hat Linux, Fedora, CentOS

Note

For a number of Linux distributions, you can install MySQL using the MySQL
Yum repository instead of the platform's native software repository. See
Section 2.5.1, “Installing MySQL on Linux Using the MySQL Yum Repository”
for details.

For Red Hat and similar distributions, the MySQL distribution is divided into a number of separate
packages, mysql for the client tools, mysql-server for the server and associated tools, and
mysql-libs for the libraries. The libraries are required if you want to provide connectivity from
different languages and environments such as Perl, Python and others.

To install, use the yum command to specify the packages that you want to install. For example:

#> yum install mysql mysql-server mysql-libs mysql-server
Loaded plugins: presto, refresh-packagekit
Setting up Install Process
Resolving Dependencies
--> Running transaction check
---> Package mysql.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-libs.x86_64 0:5.1.48-2.fc13 set to be updated
---> Package mysql-server.x86_64 0:5.1.48-2.fc13 set to be updated
--> Processing Dependency: perl-DBD-MySQL for package: mysql-server-5.1.48-2.fc13.x86_64
--> Running transaction check
---> Package perl-DBD-MySQL.x86_64 0:4.017-1.fc13 set to be updated
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package               Arch          Version               Repository      Size
================================================================================
Installing:
 mysql                 x86_64        5.1.48-2.fc13         updates        889 k
 mysql-libs            x86_64        5.1.48-2.fc13         updates        1.2 M
 mysql-server          x86_64        5.1.48-2.fc13         updates        8.1 M
Installing for dependencies:
 perl-DBD-MySQL        x86_64        4.017-1.fc13          updates        136 k

Transaction Summary
================================================================================
Install       4 Package(s)
Upgrade       0 Package(s)

Total download size: 10 M
Installed size: 30 M
Is this ok [y/N]: y
Downloading Packages:
Setting up and reading Presto delta metadata
Processing delta metadata
Package(s) data still to download: 10 M
(1/4): mysql-5.1.48-2.fc13.x86_64.rpm                    | 889 kB     00:04
(2/4): mysql-libs-5.1.48-2.fc13.x86_64.rpm               | 1.2 MB     00:06
(3/4): mysql-server-5.1.48-2.fc13.x86_64.rpm             | 8.1 MB     00:40
(4/4): perl-DBD-MySQL-4.017-1.fc13.x86_64.rpm            | 136 kB     00:00
--------------------------------------------------------------------------------
Total                                           201 kB/s |  10 MB     00:52
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
  Installing     : mysql-libs-5.1.48-2.fc13.x86_64                          1/4

215

Installing MySQL on Linux from the Native Software Repositories

  Installing     : mysql-5.1.48-2.fc13.x86_64                               2/4
  Installing     : perl-DBD-MySQL-4.017-1.fc13.x86_64                       3/4
  Installing     : mysql-server-5.1.48-2.fc13.x86_64                        4/4

Installed:
  mysql.x86_64 0:5.1.48-2.fc13            mysql-libs.x86_64 0:5.1.48-2.fc13
  mysql-server.x86_64 0:5.1.48-2.fc13

Dependency Installed:
  perl-DBD-MySQL.x86_64 0:4.017-1.fc13

Complete!

MySQL and the MySQL server should now be installed. A sample configuration file is installed into /
etc/my.cnf. To start the MySQL server use systemctl:

$> systemctl start mysqld

The database tables are automatically created for you, if they do not already exist. You should,
however, run mysql_secure_installation to set the root passwords on your server.

• Debian, Ubuntu, Kubuntu

Note

For supported Debian and Ubuntu versions, MySQL can be installed
using the MySQL APT Repository instead of the platform's native software
repository. See Section 2.5.2, “Installing MySQL on Linux Using the MySQL
APT Repository” for details.

On Debian and related distributions, there are two packages for MySQL in their software
repositories, mysql-client and mysql-server, for the client and server components
respectively. You should specify an explicit version, for example mysql-client-5.1, to ensure
that you install the version of MySQL that you want.

To download and install, including any dependencies, use the apt-get command, specifying the
packages that you want to install.

Note

Before installing, make sure that you update your apt-get index files to
ensure you are downloading the latest available version.

Note

The apt-get command installs a number of packages, including the MySQL
server, in order to provide the typical tools and application environment. This
can mean that you install a large number of packages in addition to the main
MySQL package.

During installation, the initial database is created, and you are prompted for the MySQL root
password (and confirmation). A configuration file is created in /etc/mysql/my.cnf. An init script is
created in /etc/init.d/mysql.

The server should already be started. You can manually start and stop the server using:

#> service mysql [start|stop]

The service is automatically added to the 2, 3 and 4 run levels, with stop scripts in the single,
shutdown and restart levels.

216

Installing MySQL on Linux with Juju

2.5.8 Installing MySQL on Linux with Juju

The Juju deployment framework supports easy installation and configuration of MySQL servers. For
instructions, see https://jujucharms.com/mysql/.

2.5.9 Managing MySQL Server with systemd

If you install MySQL using an RPM or Debian package on the following Linux platforms, server startup
and shutdown is managed by systemd:

• RPM package platforms:

• Enterprise Linux variants version 7 and higher

• SUSE Linux Enterprise Server 12 and higher

• Fedora 29 and higher

• Debian family platforms:

• Debian platforms

• Ubuntu platforms

If you install MySQL from a generic binary distribution on a platform that uses systemd, you can
manually configure systemd support for MySQL following the instructions provided in the post-
installation setup section of the MySQL Secure Deployment Guide.

If you install MySQL from a source distribution on a platform that uses systemd, obtain systemd
support for MySQL by configuring the distribution using the -DWITH_SYSTEMD=1 CMake option. See
Section 2.8.7, “MySQL Source-Configuration Options”.

The following discussion covers these topics:

• Overview of systemd

• Configuring systemd for MySQL

• Configuring Multiple MySQL Instances Using systemd

• Migrating from mysqld_safe to systemd

Note

On platforms for which systemd support for MySQL is installed, scripts such
as mysqld_safe and the System V initialization script are unnecessary and
are not installed. For example, mysqld_safe can handle server restarts, but
systemd provides the same capability, and does so in a manner consistent
with management of other services rather than by using an application-specific
program.

One implication of the non-use of mysqld_safe on platforms that use systemd
for server management is that use of [mysqld_safe] or [safe_mysqld]
sections in option files is not supported and might lead to unexpected behavior.

Because systemd has the capability of managing multiple MySQL instances on
platforms for which systemd support for MySQL is installed, mysqld_multi
and mysqld_multi.server are unnecessary and are not installed.

Overview of systemd

systemd provides automatic MySQL server startup and shutdown. It also enables manual server
management using the systemctl command. For example:

217

Managing MySQL Server with systemd

$> systemctl {start|stop|restart|status} mysqld

Alternatively, use the service command (with the arguments reversed), which is compatible with
System V systems:

$> service mysqld {start|stop|restart|status}

Note

For the systemctl command (and the alternative service command), if
the MySQL service name is not mysqld then use the appropriate name. For
example, use mysql rather than mysqld on Debian-based and SLES systems.

Support for systemd includes these files:

• mysqld.service (RPM platforms), mysql.service (Debian platforms): systemd service unit

configuration file, with details about the MySQL service.

• mysqld@.service (RPM platforms), mysql@.service (Debian platforms): Like

mysqld.service or mysql.service, but used for managing multiple MySQL instances.

• mysqld.tmpfiles.d: File containing information to support the tmpfiles feature. This file is

installed under the name mysql.conf.

• mysqld_pre_systemd (RPM platforms), mysql-system-start (Debian platforms): Support

script for the unit file. This script assists in creating the error log file only if the log location matches
a pattern (/var/log/mysql*.log for RPM platforms, /var/log/mysql/*.log for Debian
platforms). In other cases, the error log directory must be writable or the error log must be present
and writable for the user running the mysqld process.

Configuring systemd for MySQL

To add or change systemd options for MySQL, these methods are available:

• Use a localized systemd configuration file.

• Arrange for systemd to set environment variables for the MySQL server process.

• Set the MYSQLD_OPTS systemd variable.

To use a localized systemd configuration file, create the /etc/systemd/system/
mysqld.service.d directory if it does not exist. In that directory, create a file that contains a
[Service] section listing the desired settings. For example:

[Service]
LimitNOFILE=max_open_files
Nice=nice_level
LimitCore=core_file_limit
Environment="LD_PRELOAD=/path/to/malloc/library"
Environment="TZ=time_zone_setting"

The discussion here uses override.conf as the name of this file. Newer versions of systemd
support the following command, which opens an editor and permits you to edit the file:

systemctl edit mysqld  # RPM platforms
systemctl edit mysql   # Debian platforms

Whenever you create or change override.conf, reload the systemd configuration, then tell systemd
to restart the MySQL service:

systemctl daemon-reload
systemctl restart mysqld  # RPM platforms
systemctl restart mysql   # Debian platforms

With systemd, the override.conf configuration method must be used for certain parameters, rather
than settings in a [mysqld], [mysqld_safe], or [safe_mysqld] group in a MySQL option file:

218

Managing MySQL Server with systemd

• For some parameters, override.conf must be used because systemd itself must know their

values and it cannot read MySQL option files to get them.

• Parameters that specify values otherwise settable only using options known to mysqld_safe must

be specified using systemd because there is no corresponding mysqld parameter.

For additional information about using systemd rather than mysqld_safe, see Migrating from
mysqld_safe to systemd.

You can set the following parameters in override.conf:

• To set the number of file descriptors available to the MySQL server, use LimitNOFILE in

override.conf rather than the open_files_limit system variable for mysqld or --open-
files-limit option for mysqld_safe.

• To set the maximum core file size, use LimitCore in override.conf rather than the --core-

file-size option for mysqld_safe.

• To set the scheduling priority for the MySQL server, use Nice in override.conf rather than the

--nice option for mysqld_safe.

Some MySQL parameters are configured using environment variables:

• LD_PRELOAD: Set this variable if the MySQL server should use a specific memory-allocation library.

• NOTIFY_SOCKET: This environment variable specifies the socket that mysqld uses to communicate
notification of startup completion and service status change with systemd. It is set by systemd when
the mysqld service is started. The mysqld service reads the variable setting and writes to the
defined location.

In MySQL 8.0, mysqld uses the Type=notify process startup type. (Type=forking was used
in MySQL 5.7.) With Type=notify, systemd automatically configures a socket file and exports the
path to the NOTIFY_SOCKET environment variable.

• TZ: Set this variable to specify the default time zone for the server.

There are multiple ways to specify environment variable values for use by the MySQL server process
managed by systemd:

• Use Environment lines in the override.conf file. For the syntax, see the example in the

preceding discussion that describes how to use this file.

• Specify the values in the /etc/sysconfig/mysql file (create the file if it does not exist). Assign

values using the following syntax:

LD_PRELOAD=/path/to/malloc/library
TZ=time_zone_setting

After modifying /etc/sysconfig/mysql, restart the server to make the changes effective:

systemctl restart mysqld  # RPM platforms
systemctl restart mysql   # Debian platforms

To specify options for mysqld without modifying systemd configuration files directly, set or unset the
MYSQLD_OPTS systemd variable. For example:

systemctl set-environment MYSQLD_OPTS="--general_log=1"
systemctl unset-environment MYSQLD_OPTS

MYSQLD_OPTS can also be set in the /etc/sysconfig/mysql file.

After modifying the systemd environment, restart the server to make the changes effective:

systemctl restart mysqld  # RPM platforms
systemctl restart mysql   # Debian platforms

219

Managing MySQL Server with systemd

For platforms that use systemd, the data directory is initialized if empty at server startup. This might be
a problem if the data directory is a remote mount that has temporarily disappeared: The mount point
would appear to be an empty data directory, which then would be initialized as a new data directory.
To suppress this automatic initialization behavior, specify the following line in the /etc/sysconfig/
mysql file (create the file if it does not exist):

NO_INIT=true

Configuring Multiple MySQL Instances Using systemd

This section describes how to configure systemd for multiple instances of MySQL.

Note

Because systemd has the capability of managing multiple MySQL instances
on platforms for which systemd support is installed, mysqld_multi and
mysqld_multi.server are unnecessary and are not installed.

To use multiple-instance capability, modify the my.cnf option file to include configuration of key
options for each instance. These file locations are typical:

• /etc/my.cnf or /etc/mysql/my.cnf (RPM platforms)

• /etc/mysql/mysql.conf.d/mysqld.cnf (Debian platforms)

For example, to manage two instances named replica01 and replica02, add something like this to
the option file:

RPM platforms:

[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysqld-replica01.log

[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysqld-replica02.log

Debian platforms:

[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysql/replica01.log

[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysql/replica02.log

The replica names shown here use @ as the delimiter because that is the only delimiter supported by
systemd.

Instances then are managed by normal systemd commands, such as:

systemctl start mysqld@replica01
systemctl start mysqld@replica02

To enable instances to run at boot time, do this:

systemctl enable mysqld@replica01
systemctl enable mysqld@replica02

220

Managing MySQL Server with systemd

Use of wildcards is also supported. For example, this command displays the status of all replica
instances:

systemctl status 'mysqld@replica*'

For management of multiple MySQL instances on the same machine, systemd automatically uses a
different unit file:

• mysqld@.service rather than mysqld.service (RPM platforms)

• mysql@.service rather than mysql.service (Debian platforms)

In the unit file, %I and %i reference the parameter passed in after the @ marker and are used to
manage the specific instance. For a command such as this:

systemctl start mysqld@replica01

systemd starts the server using a command such as this:

mysqld --defaults-group-suffix=@%I ...

The result is that the [server], [mysqld], and [mysqld@replica01] option groups are read and
used for that instance of the service.

Note

On Debian platforms, AppArmor prevents the server from reading or writing /
var/lib/mysql-replica*, or anything other than the default locations. To
address this, you must customize or disable the profile in /etc/apparmor.d/
usr.sbin.mysqld.

Note

On Debian platforms, the packaging scripts for MySQL uninstallation cannot
currently handle mysqld@ instances. Before removing or upgrading the
package, you must stop any extra instances manually first.

Migrating from mysqld_safe to systemd

Because mysqld_safe is not installed on platforms that use systemd to manage MySQL, options
previously specified for that program (for example, in an [mysqld_safe] or [safe_mysqld] option
group) must be specified another way:

• Some mysqld_safe options are also understood by mysqld and can be moved from the
[mysqld_safe] or [safe_mysqld] option group to the [mysqld] group. This does not
include --pid-file, --open-files-limit, or --nice. To specify those options, use the
override.conf systemd file, described previously.

Note

On systemd platforms, use of [mysqld_safe] and [safe_mysqld] option
groups is not supported and may lead to unexpected behavior.

• For some mysqld_safe options, there are alternative mysqld procedures. For example, the

mysqld_safe option for enabling syslog logging is --syslog, which is deprecated. To write error
log output to the system log, use the instructions at Section 7.4.2.8, “Error Logging to the System
Log”.

• mysqld_safe options not understood by mysqld can be specified in override.conf or

environment variables. For example, with mysqld_safe, if the server should use a specific memory
allocation library, this is specified using the --malloc-lib option. For installations that manage the
server with systemd, arrange to set the LD_PRELOAD environment variable instead, as described
previously.

221

Installing MySQL Using Unbreakable Linux Network (ULN)

2.6 Installing MySQL Using Unbreakable Linux Network (ULN)

Linux supports a number of different solutions for installing MySQL, covered in Section 2.5,
“Installing MySQL on Linux”. One of the methods, covered in this section, is installing from Oracle's
Unbreakable Linux Network (ULN). You can find information about Oracle Linux and ULN under http://
linux.oracle.com/.

To use ULN, you need to obtain a ULN login and register the machine used for installation with
ULN. This is described in detail in the ULN FAQ. The page also describes how to install and update
packages.

Both Community and Commercial packages are supported, and each offers three MySQL channels:

• Server: MySQL Server

• Connectors: MySQL Connector/C++, MySQL Connector/J, MySQL Connector/ODBC, and MySQL

Connector/Python.

• Tools: MySQL Router, MySQL Shell, and MySQL Workbench

The Community channels are available to all ULN users.

Accessing commercial MySQL ULN packages at oracle.linux.com requires you to provide a CSI with
a valid commercial license for MySQL (Enterprise or Standard). As of this writing, valid purchases
are 60944, 60945, 64911, and 64912. The appropriate CSI makes commercial MySQL subscription
channels available in your ULN GUI interface.

Once MySQL has been installed using ULN, you can find information on starting and stopping the
server, and more, at Section 2.5.7, “Installing MySQL on Linux from the Native Software Repositories”,
particularly under Section 2.5.4, “Installing MySQL on Linux Using RPM Packages from Oracle”.

If you are changing your package source to use ULN and not changing which build of MySQL you are
using, then back up your data, remove your existing binaries, and replace them with those from ULN.
If a change of build is involved, we recommend the backup be a dump (mysqldump or mysqlpump
or from MySQL Shell's backup utility) just in case you need to rebuild your data after the new binaries
are in place. If this shift to ULN crosses a version boundary, consult this section before proceeding:
Chapter 3, Upgrading MySQL.

Note

Oracle Linux 8 is supported as of MySQL 8.0.17, and the community Tools and
Connectors channels were added with the MySQL 8.0.24 release.

2.7 Installing MySQL on Solaris

Note

MySQL 8.0 supports Solaris 11.4 and higher

MySQL on Solaris is available in a number of different formats.

• For information on installing using the native Solaris PKG format, see Section 2.7.1, “Installing

MySQL on Solaris Using a Solaris PKG”.

• To use a standard tar binary installation, use the notes provided in Section 2.2, “Installing MySQL

on Unix/Linux Using Generic Binaries”. Check the notes and hints at the end of this section for
Solaris specific notes that you may need before or after installation.

Note

MySQL 5.7 has a dependency on the Oracle Developer Studio Runtime
Libraries; but this does not apply to MySQL 8.0.

222

Installing MySQL on Solaris Using a Solaris PKG

To obtain a binary MySQL distribution for Solaris in tarball or PKG format, https://dev.mysql.com/
downloads/mysql/8.0.html.

Additional notes to be aware of when installing and using MySQL on Solaris:

• If you want to use MySQL with the mysql user and group, use the groupadd and useradd

commands:

groupadd mysql
useradd -g mysql -s /bin/false mysql

• If you install MySQL using a binary tarball distribution on Solaris, because the Solaris tar cannot

handle long file names, use GNU tar (gtar) to unpack the distribution. If you do not have GNU tar
on your system, install it with the following command:

pkg install archiver/gnu-tar

• You should mount any file systems on which you intend to store InnoDB files with the

forcedirectio option. (By default mounting is done without this option.) Failing to do so causes a
significant drop in performance when using the InnoDB storage engine on this platform.

• If you would like MySQL to start automatically, you can copy support-files/mysql.server to /

etc/init.d and create a symbolic link to it named /etc/rc3.d/S99mysql.server.

• If too many processes try to connect very rapidly to mysqld, you should see this error in the MySQL

log:

Error in accept: Protocol error

You might try starting the server with the --back_log=50 option as a workaround for this.

• To configure the generation of core files on Solaris you should use the coreadm command. Because

of the security implications of generating a core on a setuid() application, by default, Solaris
does not support core files on setuid() programs. However, you can modify this behavior using
coreadm. If you enable setuid() core files for the current user, they are generated using mode
600 and are owned by the superuser.

2.7.1 Installing MySQL on Solaris Using a Solaris PKG

You can install MySQL on Solaris using a binary package of the native Solaris PKG format instead of
the binary tarball distribution.

Note

MySQL 5.7 has a dependency on the Oracle Developer Studio Runtime
Libraries; but this does not apply to MySQL 8.0.

To use this package, download the corresponding mysql-VERSION-solaris11-
PLATFORM.pkg.gz file, then uncompress it. For example:

$> gunzip mysql-8.0.42-solaris11-x86_64.pkg.gz

To install a new package, use pkgadd and follow the onscreen prompts. You must have root privileges
to perform this operation:

$> pkgadd -d mysql-8.0.42-solaris11-x86_64.pkg

The following packages are available:
  1  mysql     MySQL Community Server (GPL)
               (i86pc) 8.0.42

Select package(s) you wish to process (or 'all' to process
all packages). (default: all) [?,??,q]:

223

Installing MySQL from Source

The PKG installer installs all of the files and tools needed, and then initializes your database if
one does not exist. To complete the installation, you should set the root password for MySQL
as provided in the instructions at the end of the installation. Alternatively, you can run the
mysql_secure_installation script that comes with the installation.

By default, the PKG package installs MySQL under the root path /opt/mysql. You can change only
the installation root path when using pkgadd, which can be used to install MySQL in a different Solaris
zone. If you need to install in a specific directory, use a binary tar file distribution.

The pkg installer copies a suitable startup script for MySQL into /etc/init.d/mysql. To enable
MySQL to startup and shutdown automatically, you should create a link between this file and the init
script directories. For example, to ensure safe startup and shutdown of MySQL you could use the
following commands to add the right links:

$> ln /etc/init.d/mysql /etc/rc3.d/S91mysql
$> ln /etc/init.d/mysql /etc/rc0.d/K02mysql

To remove MySQL, the installed package name is mysql. You can use this in combination with the
pkgrm command to remove the installation.

To upgrade when using the Solaris package file format, you must remove the existing installation
before installing the updated package. Removal of the package does not delete the existing database
information, only the server, binaries and support files. The typical upgrade sequence is therefore:

$> mysqladmin shutdown
$> pkgrm mysql
$> pkgadd -d mysql-8.0.42-solaris11-x86_64.pkg
$> mysqld_safe &
$> mysql_upgrade   # prior to MySQL 8.0.16 only

You should check the notes in Chapter 3, Upgrading MySQL before performing any upgrade.

2.8 Installing MySQL from Source

Building MySQL from the source code enables you to customize build parameters, compiler
optimizations, and installation location. For a list of systems on which MySQL is known to run, see
https://www.mysql.com/support/supportedplatforms/database.html.

Before you proceed with an installation from source, check whether Oracle produces a precompiled
binary distribution for your platform and whether it works for you. We put a great deal of effort into
ensuring that our binaries are built with the best possible options for optimal performance. Instructions
for installing binary distributions are available in Section 2.2, “Installing MySQL on Unix/Linux Using
Generic Binaries”.

If you are interested in building MySQL from a source distribution using build options the same as
or similar to those use by Oracle to produce binary distributions on your platform, obtain a binary
distribution, unpack it, and look in the docs/INFO_BIN file, which contains information about how that
MySQL distribution was configured and compiled.

Warning

Building MySQL with nonstandard options may lead to reduced functionality,
performance, or security.

The MySQL source code contains internal documentation written using Doxygen. The generated
Doxygen content is available at https://dev.mysql.com/doc/index-other.html. It is also possible to
generate this content locally from a MySQL source distribution using the instructions at Section 2.8.10,
“Generating MySQL Doxygen Documentation Content”.

2.8.1 Source Installation Methods

There are two methods for installing MySQL from source:

224

Source Installation Prerequisites

• Use a standard MySQL source distribution. To obtain a standard distribution, see Section 2.1.3,

“How to Get MySQL”. For instructions on building from a standard distribution, see Section 2.8.4,
“Installing MySQL Using a Standard Source Distribution”.

Standard distributions are available as compressed tar files, Zip archives, or RPM packages.
Distribution files have names of the form mysql-VERSION.tar.gz, mysql-VERSION.zip,
or mysql-VERSION.rpm, where VERSION is a number like 8.0.42. File names for source
distributions can be distinguished from those for precompiled binary distributions in that source
distribution names are generic and include no platform name, whereas binary distribution names
include a platform name indicating the type of system for which the distribution is intended (for
example, pc-linux-i686 or winx64).

• Use a MySQL development tree. For information on building from one of the development trees, see

Section 2.8.5, “Installing MySQL Using a Development Source Tree”.

2.8.2 Source Installation Prerequisites

Installation of MySQL from source requires several development tools. Some of these tools are needed
no matter whether you use a standard source distribution or a development source tree. Other tool
requirements depend on which installation method you use.

To install MySQL from source, the following system requirements must be satisfied, regardless of
installation method:

• CMake, which is used as the build framework on all platforms. CMake can be downloaded from http://

www.cmake.org.

• A good make program. Although some platforms come with their own make implementations, it

is highly recommended that you use GNU make 3.75 or later. It may already be available on your
system as gmake. GNU make is available from http://www.gnu.org/software/make/.

On Unix-like systems, including Linux, you can check your system's version of make like this:

$> make --version
GNU Make 4.2.1

• As of MySQL 8.0.26, MySQL 8.0 source code permits use of C++17 features. To enable the

necessary level of C++17 support across all supported platforms, the following minimum compiler
versions apply:

• Linux: GCC 10 or Clang 5

• macOS: XCode 10

• Solaris: (MySQL 8.0.40 and earlier) GCC 10; (MySQL 8.0.41 and later) GCC 11.4

• Windows: Visual Studio 2019

• Building MySQL on Windows requires Windows version 10 or later. (MySQL binaries built on recent

versions of Windows can generally be run on older versions.) You can determine the Windows
version by executing WMIC.exe os get version in the Windows Command Prompt.

• The MySQL C API requires a C++ or C99 compiler to compile.

• An SSL library is required for support of encrypted connections, entropy for random number

generation, and other encryption-related operations. By default, the build uses the OpenSSL library
installed on the host system. To specify the library explicitly, use the WITH_SSL option when you
invoke CMake. For additional information, see Section 2.8.6, “Configuring SSL Library Support”.

• The Boost C++ libraries are required to build MySQL (but not to use it). MySQL compilation requires

a particular Boost version. Typically, that is the current Boost version, but if a specific MySQL
source distribution requires a different version, the configuration process stops with a message

225

Source Installation Prerequisites

indicating the Boost version that it requires. To obtain Boost and its installation instructions, visit the
official Boost web site. After Boost is installed, tell the build system where the Boost files are placed
according to the value set for the WITH_BOOST option when you invoke CMake. For example:

cmake . -DWITH_BOOST=/usr/local/boost_version_number

Adjust the path as necessary to match your installation.

• The ncurses library.

• Sufficient free memory. If you encounter build errors such as internal compiler error when

compiling large source files, it may be that you have too little memory. If compiling on a virtual
machine, try increasing the memory allocation.

• Perl is needed if you intend to run test scripts. Most Unix-like systems include Perl. For Windows,

you can use ActiveState Perl. or Strawberry Perl.

To install MySQL from a standard source distribution, one of the following tools is required to unpack
the distribution file:

• For a .tar.gz compressed tar file: GNU gunzip to uncompress the distribution and a reasonable
tar to unpack it. If your tar program supports the z option, it can both uncompress and unpack the
file.

GNU tar is known to work. The standard tar provided with some operating systems is not able to
unpack the long file names in the MySQL distribution. You should download and install GNU tar, or
if available, use a preinstalled version of GNU tar. Usually this is available as gnutar, gtar, or as
tar within a GNU or Free Software directory, such as /usr/sfw/bin or /usr/local/bin. GNU
tar is available from https://www.gnu.org/software/tar/.

• For a .zip Zip archive: WinZip or another tool that can read .zip files.

• For an .rpm RPM package: The rpmbuild program used to build the distribution unpacks it.

To install MySQL from a development source tree, the following additional tools are required:

• The Git revision control system is required to obtain the development source code. GitHub Help

provides instructions for downloading and installing Git on different platforms.

• bison 2.1 or later, available from http://www.gnu.org/software/bison/. (Version 1 is no longer

supported.) Use the latest version of bison where possible; if you experience problems, upgrade to
a later version, rather than revert to an earlier one.

bison is available from http://www.gnu.org/software/bison/. bison for Windows can be downloaded
from http://gnuwin32.sourceforge.net/packages/bison.htm. Download the package labeled “Complete
package, excluding sources”. On Windows, the default location for bison is the C:\Program
Files\GnuWin32 directory. Some utilities may fail to find bison because of the space in the
directory name. Also, Visual Studio may simply hang if there are spaces in the path. You can
resolve these problems by installing into a directory that does not contain a space (for example C:
\GnuWin32).

• On Solaris Express, m4 must be installed in addition to bison. m4 is available from http://

www.gnu.org/software/m4/.

Note

If you have to install any programs, modify your PATH environment variable to
include any directories in which the programs are located. See Section 6.2.9,
“Setting Environment Variables”.

If you run into problems and need to file a bug report, please use the instructions in Section 1.5, “How
to Report Bugs or Problems”.

226

MySQL Layout for Source Installation

2.8.3 MySQL Layout for Source Installation

By default, when you install MySQL after compiling it from source, the installation step installs files
under /usr/local/mysql. The component locations under the installation directory are the same
as for binary distributions. See Table 2.3, “MySQL Installation Layout for Generic Unix/Linux Binary
Package”, and Section 2.3.1, “MySQL Installation Layout on Microsoft Windows”. To configure
installation locations different from the defaults, use the options described at Section 2.8.7, “MySQL
Source-Configuration Options”.

2.8.4 Installing MySQL Using a Standard Source Distribution

To install MySQL from a standard source distribution:

1. Verify that your system satisfies the tool requirements listed at Section 2.8.2, “Source Installation

Prerequisites”.

2. Obtain a distribution file using the instructions in Section 2.1.3, “How to Get MySQL”.

3. Configure, build, and install the distribution using the instructions in this section.

4. Perform postinstallation procedures using the instructions in Section 2.9, “Postinstallation Setup

and Testing”.

MySQL uses CMake as the build framework on all platforms. The instructions given here should enable
you to produce a working installation. For additional information on using CMake to build MySQL, see
How to Build MySQL Server with CMake.

If you start from a source RPM, use the following command to make a binary RPM that you can install.
If you do not have rpmbuild, use rpm instead.

$> rpmbuild --rebuild --clean MySQL-VERSION.src.rpm

The result is one or more binary RPM packages that you install as indicated in Section 2.5.4, “Installing
MySQL on Linux Using RPM Packages from Oracle”.

The sequence for installation from a compressed tar file or Zip archive source distribution is similar to
the process for installing from a generic binary distribution (see Section 2.2, “Installing MySQL on Unix/
Linux Using Generic Binaries”), except that it is used on all platforms and includes steps to configure
and compile the distribution. For example, with a compressed tar file source distribution on Unix, the
basic installation command sequence looks like this:

# Preconfiguration setup
$> groupadd mysql
$> useradd -r -g mysql -s /bin/false mysql
# Beginning of source-build specific instructions
$> tar zxvf mysql-VERSION.tar.gz
$> cd mysql-VERSION
$> mkdir bld
$> cd bld
$> cmake ..
$> make
$> make install
# End of source-build specific instructions
# Postinstallation setup
$> cd /usr/local/mysql
$> mkdir mysql-files
$> chown mysql:mysql mysql-files
$> chmod 750 mysql-files
$> bin/mysqld --initialize --user=mysql
$> bin/mysql_ssl_rsa_setup
$> bin/mysqld_safe --user=mysql &
# Next command is optional
$> cp support-files/mysql.server /etc/init.d/mysql.server

A more detailed version of the source-build specific instructions is shown following.

227

Installing MySQL Using a Standard Source Distribution

Note

The procedure shown here does not set up any passwords for MySQL
accounts. After following the procedure, proceed to Section 2.9, “Postinstallation
Setup and Testing”, for postinstallation setup and testing.

• Perform Preconfiguration Setup

• Obtain and Unpack the Distribution

• Configure the Distribution

• Build the Distribution

• Install the Distribution

• Perform Postinstallation Setup

Perform Preconfiguration Setup

On Unix, set up the mysql user that owns the database directory and that should be used to run and
execute the MySQL server, and the group to which this user belongs. For details, see Create a mysql
User and Group. Then perform the following steps as the mysql user, except as noted.

Obtain and Unpack the Distribution

Pick the directory under which you want to unpack the distribution and change location into it.

Obtain a distribution file using the instructions in Section 2.1.3, “How to Get MySQL”.

Unpack the distribution into the current directory:

• To unpack a compressed tar file, tar can decompress and unpack the distribution if it has z option

support:

$> tar zxvf mysql-VERSION.tar.gz

If your tar does not have z option support, use gunzip to decompress the distribution and tar to
unpack it:

$> gunzip < mysql-VERSION.tar.gz | tar xvf -

Alternatively, CMake can decompress and unpack the distribution:

$> cmake -E tar zxvf mysql-VERSION.tar.gz

• To unpack a Zip archive, use WinZip or another tool that can read .zip files.

Unpacking the distribution file creates a directory named mysql-VERSION.

Configure the Distribution

Change location into the top-level directory of the unpacked distribution:

$> cd mysql-VERSION

Build outside of the source tree to keep the tree clean. If the top-level source directory is named
mysql-src under your current working directory, you can build in a directory named build at the
same level. Create the directory and go there:

$> mkdir bld
$> cd bld

Configure the build directory. The minimum configuration command includes no options to override
configuration defaults:

228

Installing MySQL Using a Standard Source Distribution

$> cmake ../mysql-src

The build directory need not be outside the source tree. For example, you can build in a directory
named build under the top-level source tree. To do this, starting with mysql-src as your current
working directory, create the directory build and then go there:

$> mkdir build
$> cd build

Configure the build directory. The minimum configuration command includes no options to override
configuration defaults:

$> cmake ..

If you have multiple source trees at the same level (for example, to build multiple versions of MySQL),
the second strategy can be advantageous. The first strategy places all build directories at the same
level, which requires that you choose a unique name for each. With the second strategy, you can use
the same name for the build directory within each source tree. The following instructions assume this
second strategy.

On Windows, specify the development environment. For example, the following commands configure
MySQL for 32-bit or 64-bit builds, respectively:

$> cmake .. -G "Visual Studio 12 2013"

$> cmake .. -G "Visual Studio 12 2013 Win64"

On macOS, to use the Xcode IDE:

$> cmake .. -G Xcode

When you run Cmake, you might want to add options to the command line. Here are some examples:

• -DBUILD_CONFIG=mysql_release: Configure the source with the same build options used by

Oracle to produce binary distributions for official MySQL releases.

• -DCMAKE_INSTALL_PREFIX=dir_name: Configure the distribution for installation under a

particular location.

• -DCPACK_MONOLITHIC_INSTALL=1: Cause make package to generate a single installation file

rather than multiple files.

• -DWITH_DEBUG=1: Build the distribution with debugging support.

For a more extensive list of options, see Section 2.8.7, “MySQL Source-Configuration Options”.

To list the configuration options, use one of the following commands:

$> cmake .. -L   # overview

$> cmake .. -LH  # overview with help text

$> cmake .. -LAH # all params with help text

$> ccmake ..     # interactive display

If CMake fails, you might need to reconfigure by running it again with different options. If you do
reconfigure, take note of the following:

• If CMake is run after it has previously been run, it may use information that was gathered during its

previous invocation. This information is stored in CMakeCache.txt. When CMake starts, it looks for
that file and reads its contents if it exists, on the assumption that the information is still correct. That
assumption is invalid when you reconfigure.

• Each time you run CMake, you must run make again to recompile. However, you may want to
remove old object files from previous builds first because they were compiled using different
configuration options.

229

Installing MySQL Using a Standard Source Distribution

To prevent old object files or configuration information from being used, run these commands in the
build directory on Unix before re-running CMake:

$> make clean
$> rm CMakeCache.txt

Or, on Windows:

$> devenv MySQL.sln /clean
$> del CMakeCache.txt

Before asking on the MySQL Community Slack, check the files in the CMakeFiles directory for useful
information about the failure. To file a bug report, please use the instructions in Section 1.5, “How to
Report Bugs or Problems”.

Build the Distribution

On Unix:

$> make
$> make VERBOSE=1

The second command sets VERBOSE to show the commands for each compiled source.

Use gmake instead on systems where you are using GNU make and it has been installed as gmake.

On Windows:

$> devenv MySQL.sln /build RelWithDebInfo

If you have gotten to the compilation stage, but the distribution does not build, see Section 2.8.8,
“Dealing with Problems Compiling MySQL”, for help. If that does not solve the problem, please enter it
into our bugs database using the instructions given in Section 1.5, “How to Report Bugs or Problems”.
If you have installed the latest versions of the required tools, and they crash trying to process our
configuration files, please report that also. However, if you get a command not found error or a
similar problem for required tools, do not report it. Instead, make sure that all the required tools are
installed and that your PATH variable is set correctly so that your shell can find them.

Install the Distribution

On Unix:

$> make install

This installs the files under the configured installation directory (by default, /usr/local/mysql). You
might need to run the command as root.

To install in a specific directory, add a DESTDIR parameter to the command line:

$> make install DESTDIR="/opt/mysql"

Alternatively, generate installation package files that you can install where you like:

$> make package

This operation produces one or more .tar.gz files that can be installed like generic binary distribution
packages. See Section 2.2, “Installing MySQL on Unix/Linux Using Generic Binaries”. If you run CMake
with -DCPACK_MONOLITHIC_INSTALL=1, the operation produces a single file. Otherwise, it produces
multiple files.

On Windows, generate the data directory, then create a .zip archive installation package:

$> devenv MySQL.sln /build RelWithDebInfo /project initial_database
$> devenv MySQL.sln /build RelWithDebInfo /project package

230

Installing MySQL Using a Development Source Tree

You can install the resulting .zip archive where you like. See Section 2.3.4, “Installing MySQL on
Microsoft Windows Using a noinstall ZIP Archive”.

Perform Postinstallation Setup

The remainder of the installation process involves setting up the configuration file, creating the core
databases, and starting the MySQL server. For instructions, see Section 2.9, “Postinstallation Setup
and Testing”.

Note

The accounts that are listed in the MySQL grant tables initially have no
passwords. After starting the server, you should set up passwords for them
using the instructions in Section 2.9, “Postinstallation Setup and Testing”.

2.8.5 Installing MySQL Using a Development Source Tree

This section describes how to install MySQL from the latest development source code, which is hosted
on GitHub. To obtain the MySQL Server source code from this repository hosting service, you can set
up a local MySQL Git repository.

On GitHub, MySQL Server and other MySQL projects are found on the MySQL page. The MySQL
Server project is a single repository that contains branches for several MySQL series.

• Prerequisites for Installing from Development Source

• Setting Up a MySQL Git Repository

Prerequisites for Installing from Development Source

To install MySQL from a development source tree, your system must satisfy the tool requirements
listed at Section 2.8.2, “Source Installation Prerequisites”.

Setting Up a MySQL Git Repository

To set up a MySQL Git repository on your machine:

1. Clone the MySQL Git repository to your machine. The following command clones the MySQL

Git repository to a directory named mysql-server. The initial download may take some time to
complete, depending on the speed of your connection.

$> git clone https://github.com/mysql/mysql-server.git
Cloning into 'mysql-server'...
remote: Counting objects: 1198513, done.
remote: Total 1198513 (delta 0), reused 0 (delta 0), pack-reused 1198513
Receiving objects: 100% (1198513/1198513), 1.01 GiB | 7.44 MiB/s, done.
Resolving deltas: 100% (993200/993200), done.
Checking connectivity... done.
Checking out files: 100% (25510/25510), done.

2. When the clone operation completes, the contents of your local MySQL Git repository appear

similar to the following:

~> cd mysql-server
~/mysql-server> ls
client             extra                mysys              storage
cmake              include              packaging          strings
CMakeLists.txt     INSTALL              plugin             support-files
components         libbinlogevents      README             testclients
config.h.cmake     libchangestreams     router             unittest
configure.cmake    libmysql             run_doxygen.cmake  utilities
Docs               libservices          scripts            VERSION
Doxyfile-ignored   LICENSE              share              vio
Doxyfile.in        man                  sql                win
doxygen_resources  mysql-test           sql-common

231

Configuring SSL Library Support

3. Use the git branch -r command to view the remote tracking branches for the MySQL

repository.

~/mysql-server> git branch -r
  origin/5.7
  origin/8.0
  origin/HEAD -> origin/trunk
  origin/cluster-7.4
  origin/cluster-7.5
  origin/cluster-7.6
  origin/trunk

4. To view the branch that is checked out in your local repository, issue the git branch command.
When you clone the MySQL Git repository, the latest MySQL branch is checked out automatically.
The asterisk identifies the active branch.

~/mysql-server$ git branch
* trunk

5. To check out an earlier MySQL branch, run the git checkout command, specifying the branch

name. For example, to check out the MySQL 5.7 branch:

~/mysql-server$ git checkout 5.7
Checking out files: 100% (9600/9600), done.
Branch 5.7 set up to track remote branch 5.7 from origin.
Switched to a new branch '5.7'

6. To obtain changes made after your initial setup of the MySQL Git repository, switch to the branch

you want to update and issue the git pull command:

~/mysql-server$ git checkout 8.0
~/mysql-server$ git pull

To examine the commit history, use the git log command:

~/mysql-server$ git log

You can also browse commit history and source code on the GitHub MySQL site.

If you see changes or code that you have a question about, ask on MySQL Community Slack.

7. After you have cloned the MySQL Git repository and have checked out the branch you want to

build, you can build MySQL Server from the source code. Instructions are provided in Section 2.8.4,
“Installing MySQL Using a Standard Source Distribution”, except that you skip the part about
obtaining and unpacking the distribution.

Be careful about installing a build from a distribution source tree on a production machine. The
installation command may overwrite your live release installation. If you already have MySQL
installed and do not want to overwrite it, run CMake with values for the CMAKE_INSTALL_PREFIX,
MYSQL_TCP_PORT, and MYSQL_UNIX_ADDR options different from those used by your production
server. For additional information about preventing multiple servers from interfering with each other,
see Section 7.8, “Running Multiple MySQL Instances on One Machine”.

Play hard with your new installation. For example, try to make new features crash. Start by running
make test. See The MySQL Test Suite.

2.8.6 Configuring SSL Library Support

An SSL library is required for support of encrypted connections, entropy for random number
generation, and other encryption-related operations.

If you compile MySQL from a source distribution, CMake configures the distribution to use the installed
OpenSSL library by default.

To compile using OpenSSL, use this procedure:

232

MySQL Source-Configuration Options

1. Ensure that OpenSSL 1.0.1 or newer is installed on your system. If the installed OpenSSL version
is older than 1.0.1, CMake produces an error at MySQL configuration time. If it is necessary to
obtain OpenSSL, visit http://www.openssl.org.

2. The WITH_SSL CMake option determines which SSL library to use for compiling MySQL (see
Section 2.8.7, “MySQL Source-Configuration Options”). The default is -DWITH_SSL=system,
which uses OpenSSL. To make this explicit, specify that option. For example:

cmake . -DWITH_SSL=system

That command configures the distribution to use the installed OpenSSL library. Alternatively, to
explicitly specify the path name to the OpenSSL installation, use the following syntax. This can
be useful if you have multiple versions of OpenSSL installed, to prevent CMake from choosing the
wrong one:

cmake . -DWITH_SSL=path_name

Alternative OpenSSL system packages are supported as of MySQL 8.0.30 by using
WITH_SSL=openssl11 on EL7 or WITH_SSL=openssl3 on EL8. Authentication plugins, such as
LDAP and Kerberos, are disabled since they do not support these alternative versions of OpenSSL.

3. Compile and install the distribution.

To check whether a mysqld server supports encrypted connections, examine the value of the
have_ssl system variable:

mysql> SHOW VARIABLES LIKE 'have_ssl';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| have_ssl      | YES   |
+---------------+-------+

If the value is YES, the server supports encrypted connections. If the value is DISABLED, the server
is capable of supporting encrypted connections but was not started with the appropriate --ssl-xxx
options to enable encrypted connections to be used; see Section 8.3.1, “Configuring MySQL to Use
Encrypted Connections”.

2.8.7 MySQL Source-Configuration Options

The CMake program provides a great deal of control over how you configure a MySQL source
distribution. Typically, you do this using options on the CMake command line. For information about
options supported by CMake, run either of these commands in the top-level source directory:

$> cmake . -LH

$> ccmake .

You can also affect CMake using certain environment variables. See Section 6.9, “Environment
Variables”.

For boolean options, the value may be specified as 1 or ON to enable the option, or as 0 or OFF to
disable the option.

Many options configure compile-time defaults that can be overridden at server startup. For example,
the CMAKE_INSTALL_PREFIX, MYSQL_TCP_PORT, and MYSQL_UNIX_ADDR options that configure the
default installation base directory location, TCP/IP port number, and Unix socket file can be changed at
server startup with the --basedir, --port, and --socket options for mysqld. Where applicable,
configuration option descriptions indicate the corresponding mysqld startup option.

The following sections provide more information about CMake options.

• CMake Option Reference

233

MySQL Source-Configuration Options

• General Options

• Installation Layout Options

• Storage Engine Options

• Feature Options

• Compiler Flags

• CMake Options for Compiling NDB Cluster

CMake Option Reference

The following table shows the available CMake options. In the Default column, PREFIX stands for
the value of the CMAKE_INSTALL_PREFIX option, which specifies the installation base directory. This
value is used as the parent location for several of the installation subdirectories.

Table 2.14 MySQL Source-Configuration Option Reference (CMake)

Formats

Description

Default

Introduced

Removed

ADD_GDB_INDEX Whether to

8.0.18

BUILD_CONFIG

enable generation
of .gdb_index
section in binaries

Use same build
options as official
releases

BUNDLE_RUNTIME_LIBRARIES
Bundle runtime
libraries with
server MSI and
Zip packages for
Windows

OFF

CMAKE_BUILD_TYPEType of build to

RelWithDebInfo

produce

CMAKE_CXX_FLAGS Flags for C++

CMAKE_C_FLAGS

Compiler

Flags for C
Compiler

CMAKE_INSTALL_PREFIX

Installation base
directory

/usr/local/
mysql

COMPILATION_COMMENTComment about

compilation
environment

COMPILATION_COMMENT_SERVER

Comment about
compilation
environment for
use by mysqld

COMPRESS_DEBUG_SECTIONS

Compress debug
sections of binary
executables

CPACK_MONOLITHIC_INSTALL

Whether package
build produces
single file

OFF

OFF

DEFAULT_CHARSET The default server

utf8mb4

character set

8.0.14

8.0.22

234

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

DEFAULT_COLLATIONThe default server

utf8mb4_0900_ai_ci

collation

DISABLE_PSI_CONDExclude

OFF

Performance
Schema condition
instrumentation

DISABLE_PSI_DATA_LOCK

Exclude the
performance
schema data lock
instrumentation

DISABLE_PSI_ERRORExclude the
performance
schema
server error
instrumentation

OFF

OFF

DISABLE_PSI_FILEExclude

OFF

Performance
Schema file
instrumentation

DISABLE_PSI_IDLEExclude

OFF

Performance
Schema idle
instrumentation

DISABLE_PSI_MEMORYExclude

OFF

Performance
Schema memory
instrumentation

DISABLE_PSI_METADATA

Exclude
Performance
Schema metadata
instrumentation

OFF

DISABLE_PSI_MUTEXExclude

OFF

Performance
Schema mutex
instrumentation

DISABLE_PSI_PS Exclude the
performance
schema prepared
statements

OFF

DISABLE_PSI_RWLOCKExclude

OFF

Performance
Schema rwlock
instrumentation

DISABLE_PSI_SOCKETExclude

OFF

Performance
Schema socket
instrumentation

DISABLE_PSI_SP Exclude

OFF

Performance
Schema stored

235

MySQL Source-Configuration Options

Formats

Description
program
instrumentation

Default

Introduced

Removed

DISABLE_PSI_STAGEExclude

OFF

Performance
Schema stage
instrumentation

DISABLE_PSI_STATEMENT
Exclude
Performance
Schema statement
instrumentation

DISABLE_PSI_STATEMENT_DIGEST

Exclude
Performance
Schema
statements_digest
instrumentation

OFF

OFF

DISABLE_PSI_TABLEExclude

OFF

Performance
Schema table
instrumentation

DISABLE_PSI_THREADExclude the
performance
schema thread
instrumentation

DISABLE_PSI_TRANSACTION

Exclude the
performance
schema transaction
instrumentation

OFF

OFF

DISABLE_SHARED Do not build shared

OFF

8.0.18

libraries, compile
position-dependent
code

DOWNLOAD_BOOST Whether to

OFF

download the
Boost library

DOWNLOAD_BOOST_TIMEOUT

Timeout in seconds
for downloading
the Boost library

ENABLED_LOCAL_INFILEWhether to enable
LOCAL for LOAD
DATA

600

OFF

ENABLED_PROFILINGWhether to enable

ON

query profiling
code

ENABLE_DOWNLOADSWhether to

OFF

8.0.26

download optional
files

ENABLE_EXPERIMENTAL_SYSVARS

Whether
to enabled
experimental
InnoDB system
variables

OFF

236

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

ENABLE_GCOV

ENABLE_GPROF

Whether to include
gcov support

Enable gprof
(optimized Linux
builds only)

OFF

FORCE_COLORED_OUTPUTWhether to colorize

OFF

compiler output

FORCE_INSOURCE_BUILDWhether to force
an in-source build

FORCE_UNSUPPORTED_COMPILER

Whether to permit
unsupported
compilers

OFF

OFF

8.0.33

8.0.14

FPROFILE_GENERATEWhether to

OFF

8.0.19

FPROFILE_USE

generate profile
guided optimization
data

Whether to use
profile guided
optimization data

HAVE_PSI_MEMORY_INTERFACE
Enable
performance
schema memory
tracing module for
memory allocation
functions used in
dynamic storage of
over-aligned types

OFF

OFF

8.0.19

8.0.26

IGNORE_AIO_CHECKWith -

OFF

DBUILD_CONFIG=mysql_release,
ignore libaio check

INSTALL_BINDIR User executables

PREFIX/bin

directory

INSTALL_DOCDIR Documentation

PREFIX/docs

directory

INSTALL_DOCREADMEDIR

README file
directory

PREFIX

INSTALL_INCLUDEDIRHeader file

PREFIX/include

directory

INSTALL_INFODIR Info file directory

PREFIX/docs

INSTALL_LAYOUT Select predefined
installation layout

STANDALONE

INSTALL_LIBDIR Library file

PREFIX/lib

directory

INSTALL_MANDIR Manual page

PREFIX/man

directory

INSTALL_MYSQLKEYRINGDIR

Directory for
keyring_file plugin
data file

platform
specific

237

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

INSTALL_MYSQLSHAREDIR
Shared data
directory

PREFIX/share

INSTALL_MYSQLTESTDIRmysql-test directory PREFIX/mysql-

INSTALL_PKGCONFIGDIR

Directory for
mysqlclient.pc pkg-
config file

INSTALL_PLUGINDIRPlugin directory

test

INSTALL_LIBDIR/
pkgconfig

PREFIX/lib/
plugin

INSTALL_PRIV_LIBDIR

Installation private
library directory

8.0.18

INSTALL_SBINDIR Server executable

PREFIX/bin

directory

INSTALL_SECURE_FILE_PRIVDIR
secure_file_priv
default value

platform
specific

INSTALL_SHAREDIRaclocal/mysql.m4

PREFIX/share

installation
directory

INSTALL_STATIC_LIBRARIES

Whether to install
static libraries

ON

INSTALL_SUPPORTFILESDIR

Extra support files
directory

PREFIX/
support-files

LINK_RANDOMIZE Whether to

OFF

randomize order of
symbols in mysqld
binary

LINK_RANDOMIZE_SEEDSeed value for

mysql

MAX_INDEXES

LINK_RANDOMIZE
option

Maximum indexes
per table

64

MEMCACHED_HOME Path to

[none]

8.0.23

MSVC_CPPCHECK

memcached;
obsolete

Enable MSVC
code analysis.

OFF

8.0.33

MUTEX_TYPE

InnoDB mutex type event

MYSQLX_TCP_PORT TCP/IP port

33060

number used by X
Plugin

MYSQLX_UNIX_ADDRUnix socket file

used by X Plugin

/tmp/
mysqlx.sock

MYSQL_DATADIR Data directory

MYSQL_MAINTAINER_MODE

Whether to
enable MySQL
maintainer-specific
development
environment

OFF

238

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

MYSQL_PROJECT_NAMEWindows/macOS

MySQL

project name

MYSQL_TCP_PORT TCP/IP port

3306

number

MYSQL_UNIX_ADDR Unix socket file

/tmp/
mysql.sock

8.0.22

ON

8.0.34

NDB_UTILS_LINK_DYNAMIC

Cause NDB tools
to be dynamically
linked to ndbclient

ODBC_INCLUDES ODBC includes

ODBC_LIB_DIR

directory

ODBC library
directory

OPTIMIZER_TRACE Whether to support

optimizer tracing

OPTIMIZE_SANITIZER_BUILDS

Whether to
optimize sanitizer
builds

REPRODUCIBLE_BUILDTake extra care
to create a build
result independent
of build location
and time

SHOW_SUPPRESSED_COMPILER_WARNING

OFF

Whether to show
suppressed
compiler warnings
and not fail with -
Werror.

SYSCONFDIR

Option file directory

SYSTEMD_PID_DIR Directory for PID

file under systemd

SYSTEMD_SERVICE_NAME

Name of MySQL
service under
systemd

/var/run/
mysqld

mysqld

TMPDIR

USE_LD_GOLD

USE_LD_LLD

tmpdir default
value

Whether to use
GNU gold linker

Whether to use
LLVM lld linker

ON

ON

WIN_DEBUG_NO_INLINEWhether to disable

OFF

function inlining

WITHOUT_SERVER Do not build the

OFF

server; internal use
only

WITHOUT_xxx_STORAGE_ENGINE

Exclude storage
engine xxx from
build

8.0.30

8.0.31

8.0.16

239

MySQL Source-Configuration Options

Description

Default

Introduced

Removed

Formats

WITH_ANT

WITH_ASAN

Path to Ant for
building GCS Java
wrapper

Enable
AddressSanitizer

OFF

OFF

WITH_ASAN_SCOPE Enable

AddressSanitizer -
fsanitize-address-
use-after-scope
Clang flag

8.0.26

8.0.31

8.0.23

8.0.23

WITH_AUTHENTICATION_CLIENT_PLUGINS

Enabled
automatically if
any corresponding
server
authentication
plugins are built

OFF

OFF

ON

ON

ON

WITH_AUTHENTICATION_LDAP

Whether to report
error if LDAP
authentication
plugins cannot be
built

WITH_AUTHENTICATION_PAM
Build PAM
authentication
plugin

WITH_AWS_SDK

WITH_BOOST

Location of
Amazon Web
Services software
development kit

The location of
the Boost library
sources

WITH_BUILD_ID On Linux systems,
generate a unique
build ID

WITH_BUNDLED_LIBEVENT
Use bundled
libevent
when building
ndbmemcache;
obsolete

WITH_BUNDLED_MEMCACHED

Use bundled
memcached
when building
ndbmemcache;
obsolete

WITH_CLASSPATH Classpath to use

when building
MySQL Cluster
Connector for
Java. Default is an
empty string.

240

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

WITH_CLIENT_PROTOCOL_TRACING

Build client-side
protocol tracing
framework

ON

WITH_CURL

WITH_DEBUG

Location of curl
library

Whether to include
debugging support

OFF

ON

ON

OFF

WITH_DEFAULT_COMPILER_OPTIONS

Whether to use
default compiler
options

WITH_DEFAULT_FEATURE_SET

Whether to use
default feature set

WITH_DEVELOPER_ENTITLEMENTS
Whether to add
the 'get-task-allow'
entitlement to all
executables on
macOS to generate
a core dump in
the event of an
unexpected server
halt

WITH_EDITLINE Which libedit/

bundled

editline library to
use

WITH_ERROR_INSERTEnable error

OFF

8.0.22

8.0.30

injection in the
NDB storage
engine. Should
not be used for
building binaries
intended for
production.

Type of FIDO
library support

Path to
googlemock
distribution

Type of ICU
support

WITH_FIDO

WITH_GMOCK

WITH_ICU

WITH_INNODB_EXTRA_DEBUG

Whether to include
extra debugging
support for InnoDB.

WITH_INNODB_MEMCACHED
Whether to
generate
memcached
shared libraries.

WITH_JEMALLOC Whether to link
with -ljemalloc

bundled

8.0.27

8.0.26

bundled

OFF

OFF

OFF

8.0.16

WITH_KEYRING_TESTBuild the keyring

OFF

test program

241

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

8.0.16

WITH_LIBEVENT Which libevent

bundled

WITH_LIBWRAP

library to use

Whether to include
libwrap (TCP
wrappers) support

OFF

WITH_LOCK_ORDER Whether to enable

OFF

8.0.17

WITH_LSAN

WITH_LTO

WITH_LZ4

WITH_LZMA

LOCK_ORDER
tooling

Whether to run
LeakSanitizer,
without
AddressSanitizer

Enable link-time
optimizer

OFF

8.0.16

OFF

8.0.13

Type of LZ4 library
support

bundled

Type of LZMA
library support

bundled

WITH_MECAB

Compiles MeCab

WITH_MSAN

Enable
MemorySanitizer

OFF

WITH_MSCRT_DEBUGEnable Visual

OFF

Studio CRT
memory leak
tracing

WITH_MYSQLX

Whether to disable
X Protocol

ON

WITH_NDB

Build MySQL NDB
Cluster, including
NDB storage
engine and all NDB
programs

OFF

8.0.31

WITH_NDBAPI_EXAMPLES

Build API example
programs.

OFF

WITH_NDBCLUSTER NDB 8.0.30 and

OFF

earlier: Build NDB
storage engine.
NDB 8.0.31 and
later: Deprecated;
use WITH_NDB
instead

ON

WITH_NDBCLUSTER_STORAGE_ENGINE

Prior to NDB
8.0.31, this was
for internal use
only. NDB 8.0.31
and later: toggles
(only) inclusion of
NDBCLUSTER
storage engine

242

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

WITH_NDBMTD

Build multithreaded
data node binary

ON

OFF

ON

[none]

WITH_NDB_DEBUG Produce a debug
build for testing or
troubleshooting.

WITH_NDB_JAVA

Enable building
of Java and
ClusterJ support.
Enabled by default.
Supported in
MySQL Cluster
only.

WITH_NDB_PORT Default port used
by a management
server built with
this option. If this
option was not
used to build it,
the management
server's default
port is 1186.

WITH_NDB_TEST

WITH_NUMA

Include NDB API
test programs.

OFF

Set NUMA memory
allocation policy

WITH_PACKAGE_FLAGSFor flags typically

8.0.26

used for RPM/DEB
packages, whether
to add them to
standalone builds
on those platforms

WITH_PLUGIN_NDBCLUSTER

For internal use;
may not work as
expected in all
circumstances.
Instead, users
should employ
WITH_NDBCLUSTER

WITH_PROTOBUF Which Protocol

bundled

WITH_RAPID

Buffers package to
use

Whether to build
rapid development
cycle plugins

ON

8.0.13

8.0.31

WITH_RAPIDJSON Type of

bundled

8.0.13

RapidJSON
support

WITH_RE2

Type of RE2 library
support

bundled

8.0.18

WITH_ROUTER

Whether to build
MySQL Router

ON

8.0.16

243

MySQL Source-Configuration Options

Formats

Description

Default

Introduced

Removed

WITH_SASL

Internal use only

WITH_SSL

WITH_SYSTEMD

Type of SSL
support

system

Enable installation
of systemd support
files

OFF

WITH_SYSTEMD_DEBUGEnable additional

OFF

8.0.22

8.0.22

systemd debug
information

WITH_SYSTEM_LIBSSet system value
of library options
not set explicitly

WITH_TCMALLOC Whether to link
with -ltcmalloc.
BUNDLED is
supported on Linux
only

WITH_TEST_TRACE_PLUGIN

Build test protocol
trace plugin

WITH_TSAN

WITH_UBSAN

Enable
ThreadSanitizer

Enable Undefined
Behavior Sanitizer

OFF

OFF

OFF

OFF

OFF

WITH_UNIT_TESTS Compile MySQL

ON

WITH_UNIXODBC

with unit tests

Enable unixODBC
support

WITH_VALGRIND Whether to compile
in Valgrind header
files

OFF

OFF

WITH_WIN_JEMALLOCPath to directory

8.0.29

bundled

bundled

8.0.18

WITH_ZLIB

WITH_ZSTD

containing
jemalloc.dll

Type of zlib
support

Type of zstd
support

WITH_xxx_STORAGE_ENGINE
Compile storage
engine xxx
statically into
server

General Options

• -DBUILD_CONFIG=mysql_release

This option configures a source distribution with the same build options used by Oracle to produce
binary distributions for official MySQL releases.

• -DWITH_BUILD_ID=bool

244

MySQL Source-Configuration Options

On Linux systems, generates a unique build ID which is used as the value of the build_id system
variable and written to the MySQL server log on startup. Set this option to OFF to disable this feature.

Added in MySQL 8.0.31, this option has no effect on platforms other than Linux.

• -DBUNDLE_RUNTIME_LIBRARIES=bool

Whether to bundle runtime libraries with server MSI and Zip packages for Windows.

• -DCMAKE_BUILD_TYPE=type

The type of build to produce:

• RelWithDebInfo: Enable optimizations and generate debugging information. This is the default

MySQL build type.

• Release: Enable optimizations but omit debugging information to reduce the build size. This build

type was added in MySQL 8.0.13.

• Debug: Disable optimizations and generate debugging information. This build type is also used
if the WITH_DEBUG option is enabled. That is, -DWITH_DEBUG=1 has the same effect as -
DCMAKE_BUILD_TYPE=Debug.

The option values None and MinSizeRel are not supported.

• -DCPACK_MONOLITHIC_INSTALL=bool

This option affects whether the make package operation produces multiple installation package
files or a single file. If disabled, the operation produces multiple installation package files, which may
be useful if you want to install only a subset of a full MySQL installation. If enabled, it produces a
single file for installing everything.

• -DFORCE_INSOURCE_BUILD=bool

Defines whether to force an in-source build. Out-of-source builds are recommended, as they permit
multiple builds from the same source, and cleanup can be performed quickly by removing the build
directory. To force an in-source build, invoke CMake with -DFORCE_INSOURCE_BUILD=ON.

• -DFORCE_COLORED_OUTPUT=bool

Defines whether to enable colorized compiler output for gcc and clang when compiling on the
command line. Defaults to OFF.

Installation Layout Options

The CMAKE_INSTALL_PREFIX option indicates the base installation directory. Other options with
names of the form INSTALL_xxx that indicate component locations are interpreted relative to the
prefix and their values are relative pathnames. Their values should not include the prefix.

• -DCMAKE_INSTALL_PREFIX=dir_name

The installation base directory.

This value can be set at server startup using the --basedir option.

• -DINSTALL_BINDIR=dir_name

Where to install user programs.

• -DINSTALL_DOCDIR=dir_name

Where to install documentation.

245

MySQL Source-Configuration Options

• -DINSTALL_DOCREADMEDIR=dir_name

Where to install README files.

• -DINSTALL_INCLUDEDIR=dir_name

Where to install header files.

• -DINSTALL_INFODIR=dir_name

Where to install Info files.

• -DINSTALL_LAYOUT=name

Select a predefined installation layout:

• STANDALONE: Same layout as used for .tar.gz and .zip packages. This is the default.

• RPM: Layout similar to RPM packages.

• SVR4: Solaris package layout.

• DEB: DEB package layout (experimental).

You can select a predefined layout but modify individual component installation locations by
specifying other options. For example:

cmake . -DINSTALL_LAYOUT=SVR4 -DMYSQL_DATADIR=/var/mysql/data

The INSTALL_LAYOUT value determines the default value of the secure_file_priv,
keyring_encrypted_file_data, and keyring_file_data system variables. See the
descriptions of those variables in Section 7.1.8, “Server System Variables”, and Section 8.4.4.19,
“Keyring System Variables”.

• -DINSTALL_LIBDIR=dir_name

Where to install library files.

• -DINSTALL_MANDIR=dir_name

Where to install manual pages.

• -DINSTALL_MYSQLKEYRINGDIR=dir_path

The default directory to use as the location of the keyring_file plugin data file. The default
value is platform specific and depends on the value of the INSTALL_LAYOUT CMake option; see
the description of the keyring_file_data system variable in Section 7.1.8, “Server System
Variables”.

• -DINSTALL_MYSQLSHAREDIR=dir_name

Where to install shared data files.

• -DINSTALL_MYSQLTESTDIR=dir_name

Where to install the mysql-test directory. To suppress installation of this directory, explicitly set the
option to the empty value (-DINSTALL_MYSQLTESTDIR=).

• -DINSTALL_PKGCONFIGDIR=dir_name

The directory in which to install the mysqlclient.pc file for use by pkg-config. The default
value is INSTALL_LIBDIR/pkgconfig, unless INSTALL_LIBDIR ends with /mysql, in which
case that is removed first.

246

MySQL Source-Configuration Options

• -DINSTALL_PLUGINDIR=dir_name

The location of the plugin directory.

This value can be set at server startup with the --plugin_dir option.

• -DINSTALL_PRIV_LIBDIR=dir_name

The location of the dynamic library directory.

Default location.
lib/mysql/private/, and for TAR it is lib/private/.

 For RPM builds, this is /usr/lib64/mysql/private/, for DEB it is /usr/

 Because this is a private location, the loader (such as ld-linux.so on Linux) may

Protobuf.
not find the libprotobuf.so files without help. To guide the loader, RPATH=$ORIGIN/../
$INSTALL_PRIV_LIBDIR is added to mysqld and mysqlxtest. This works for most cases but
when using the Resource Group feature, mysqld is setsuid, and the loader ignores any RPATH
which contains $ORIGIN. To overcome this, an explicit full path to the directory is set in the DEB
and RPM versions of mysqld, since the target destination is known. For tarball installs, patching of
mysqld with a tool like patchelf is required.

This option was added in MySQL 8.0.18.

• -DINSTALL_SBINDIR=dir_name

Where to install the mysqld server.

• -DINSTALL_SECURE_FILE_PRIVDIR=dir_name

The default value for the secure_file_priv system variable. The default value is platform
specific and depends on the value of the INSTALL_LAYOUT CMake option; see the description of the
secure_file_priv system variable in Section 7.1.8, “Server System Variables”.

• -DINSTALL_SHAREDIR=dir_name

Where to install aclocal/mysql.m4.

• -DINSTALL_STATIC_LIBRARIES=bool

Whether to install static libraries. The default is ON. If set to OFF, these library files are not installed:
libmysqlclient.a, libmysqlservices.a.

• -DINSTALL_SUPPORTFILESDIR=dir_name

Where to install extra support files.

• -DLINK_RANDOMIZE=bool

Whether to randomize the order of symbols in the mysqld binary. The default is OFF. This option
should be enabled only for debugging purposes.

• -DLINK_RANDOMIZE_SEED=val

Seed value for the LINK_RANDOMIZE option. The value is a string. The default is mysql, an
arbitrary choice.

• -DMYSQL_DATADIR=dir_name

The location of the MySQL data directory.

This value can be set at server startup with the --datadir option.

• -DODBC_INCLUDES=dir_name

247

MySQL Source-Configuration Options

The location of the ODBC includes directory, which may be used while configuring Connector/ODBC.

• -DODBC_LIB_DIR=dir_name

The location of the ODBC library directory, which may be used while configuring Connector/ODBC.

• -DSYSCONFDIR=dir_name

The default my.cnf option file directory.

This location cannot be set at server startup, but you can start the server with a given option file
using the --defaults-file=file_name option, where file_name is the full path name to the
file.

• -DSYSTEMD_PID_DIR=dir_name

The name of the directory in which to create the PID file when MySQL is managed by systemd. The
default is /var/run/mysqld; this might be changed implicitly according to the INSTALL_LAYOUT
value.

This option is ignored unless WITH_SYSTEMD is enabled.

• -DSYSTEMD_SERVICE_NAME=name

The name of the MySQL service to use when MySQL is managed by systemd. The default is
mysqld; this might be changed implicitly according to the INSTALL_LAYOUT value.

This option is ignored unless WITH_SYSTEMD is enabled.

• -DTMPDIR=dir_name

The default location to use for the tmpdir system variable. If unspecified, the value defaults to
P_tmpdir in <stdio.h>.

Storage Engine Options

Storage engines are built as plugins. You can build a plugin as a static module (compiled into the
server) or a dynamic module (built as a dynamic library that must be installed into the server using the
INSTALL PLUGIN statement or the --plugin-load option before it can be used). Some plugins
might not support static or dynamic building.

The InnoDB, MyISAM, MERGE, MEMORY, and CSV engines are mandatory (always compiled into the
server) and need not be installed explicitly.

To compile a storage engine statically into the server, use -DWITH_engine_STORAGE_ENGINE=1.
Some permissible engine values are ARCHIVE, BLACKHOLE, EXAMPLE, and FEDERATED. Examples:

-DWITH_ARCHIVE_STORAGE_ENGINE=1
-DWITH_BLACKHOLE_STORAGE_ENGINE=1

To build MySQL with support for NDB Cluster, use the WITH_NDB option. (NDB 8.0.30 and earlier: Use
WITH_NDBCLUSTER.)

Note

It is not possible to compile without Performance Schema support. If it is desired
to compile without particular types of instrumentation, that can be done with the
following CMake options:

DISABLE_PSI_COND
DISABLE_PSI_DATA_LOCK
DISABLE_PSI_ERROR
DISABLE_PSI_FILE

248

MySQL Source-Configuration Options

DISABLE_PSI_IDLE
DISABLE_PSI_MEMORY
DISABLE_PSI_METADATA
DISABLE_PSI_MUTEX
DISABLE_PSI_PS
DISABLE_PSI_RWLOCK
DISABLE_PSI_SOCKET
DISABLE_PSI_SP
DISABLE_PSI_STAGE
DISABLE_PSI_STATEMENT
DISABLE_PSI_STATEMENT_DIGEST
DISABLE_PSI_TABLE
DISABLE_PSI_THREAD
DISABLE_PSI_TRANSACTION

For example, to compile without mutex instrumentation, configure MySQL using
-DDISABLE_PSI_MUTEX=1.

To exclude a storage engine from the build, use -DWITH_engine_STORAGE_ENGINE=0. Examples:

-DWITH_ARCHIVE_STORAGE_ENGINE=0
-DWITH_EXAMPLE_STORAGE_ENGINE=0
-DWITH_FEDERATED_STORAGE_ENGINE=0

It is also possible to exclude a storage engine from the build using -
DWITHOUT_engine_STORAGE_ENGINE=1 (but -DWITH_engine_STORAGE_ENGINE=0 is preferred).
Examples:

-DWITHOUT_ARCHIVE_STORAGE_ENGINE=1
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1
-DWITHOUT_FEDERATED_STORAGE_ENGINE=1

If neither -DWITH_engine_STORAGE_ENGINE nor -DWITHOUT_engine_STORAGE_ENGINE are
specified for a given storage engine, the engine is built as a shared module, or excluded if it cannot be
built as a shared module.

Feature Options

• -DADD_GDB_INDEX=bool

This option determines whether to enable generation of a .gdb_index section in binaries, which
makes loading them in a debugger faster. The option is disabled by default. lld linker is used, and is
disabled by It has no effect if a linker other than lld or GNU gold is used.

This option was added in MySQL 8.0.18.

• -DCOMPILATION_COMMENT=string

A descriptive comment about the compilation environment. As of MySQL 8.0.14, mysqld uses
COMPILATION_COMMENT_SERVER. Other programs continue to use COMPILATION_COMMENT.

• -DCOMPRESS_DEBUG_SECTIONS=bool

Whether to compress the debug sections of binary executables (Linux only). Compressing
executable debug sections saves space at the cost of extra CPU time during the build process.

The default is OFF. If this option is not set explicitly but the COMPRESS_DEBUG_SECTIONS
environment variable is set, the option takes its value from that variable.

This option was added in MySQL 8.0.22.

• -DCOMPILATION_COMMENT_SERVER=string

A descriptive comment about the compilation environment for use by mysqld (for example, to set
the version_comment system variable). This option was added in MySQL 8.0.14. Prior to 8.0.14,
the server uses COMPILATION_COMMENT.

249

MySQL Source-Configuration Options

• -DDEFAULT_CHARSET=charset_name

The server character set. By default, MySQL uses the utf8mb4 character set.

charset_name may be one of binary, armscii8, ascii, big5, cp1250, cp1251, cp1256,
cp1257, cp850, cp852, cp866, cp932, dec8, eucjpms, euckr, gb2312, gbk, geostd8, greek,
hebrew, hp8, keybcs2, koi8r, koi8u, latin1, latin2, latin5, latin7, macce, macroman,
sjis, swe7, tis620, ucs2, ujis, utf8mb3, utf8mb4, utf16, utf16le, utf32.

This value can be set at server startup with the --character-set-server option.

• -DDEFAULT_COLLATION=collation_name

The server collation. By default, MySQL uses utf8mb4_0900_ai_ci. Use the SHOW COLLATION
statement to determine which collations are available for each character set.

This value can be set at server startup with the --collation_server option.

• -DDISABLE_PSI_COND=bool

Whether to exclude the Performance Schema condition instrumentation. The default is OFF (include).

• -DDISABLE_PSI_FILE=bool

Whether to exclude the Performance Schema file instrumentation. The default is OFF (include).

• -DDISABLE_PSI_IDLE=bool

Whether to exclude the Performance Schema idle instrumentation. The default is OFF (include).

• -DDISABLE_PSI_MEMORY=bool

Whether to exclude the Performance Schema memory instrumentation. The default is OFF (include).

• -DDISABLE_PSI_METADATA=bool

Whether to exclude the Performance Schema metadata instrumentation. The default is OFF
(include).

• -DDISABLE_PSI_MUTEX=bool

Whether to exclude the Performance Schema mutex instrumentation. The default is OFF (include).

• -DDISABLE_PSI_RWLOCK=bool

Whether to exclude the Performance Schema rwlock instrumentation. The default is OFF (include).

• -DDISABLE_PSI_SOCKET=bool

Whether to exclude the Performance Schema socket instrumentation. The default is OFF (include).

• -DDISABLE_PSI_SP=bool

Whether to exclude the Performance Schema stored program instrumentation. The default is OFF
(include).

• -DDISABLE_PSI_STAGE=bool

Whether to exclude the Performance Schema stage instrumentation. The default is OFF (include).

• -DDISABLE_PSI_STATEMENT=bool

Whether to exclude the Performance Schema statement instrumentation. The default is OFF
(include).

250

MySQL Source-Configuration Options

• -DDISABLE_PSI_STATEMENT_DIGEST=bool

Whether to exclude the Performance Schema statement digest instrumentation. The default is OFF
(include).

• -DDISABLE_PSI_TABLE=bool

Whether to exclude the Performance Schema table instrumentation. The default is OFF (include).

• -DDISABLE_SHARED=bool

Whether to disable building build shared libraries and compile position-dependent code. The default
is OFF (compile position-independent code).

This option is unused, and was removed in MySQL 8.0.18.

• -DDISABLE_PSI_PS=bool

Exclude the Performance Schema prepared statements instances instrumentation. The default is
OFF (include).

• -DDISABLE_PSI_THREAD=bool

Exclude the Performance Schema thread instrumentation. The default is OFF (include).

Only disable threads when building without any instrumentation, because other instrumentations
have a dependency on threads.

• -DDISABLE_PSI_TRANSACTION=bool

Exclude the Performance Schema transaction instrumentation. The default is OFF (include).

• -DDISABLE_PSI_DATA_LOCK=bool

Exclude the performance schema data lock instrumentation. The default is OFF (include).

• -DDISABLE_PSI_ERROR=bool

Exclude the performance schema server error instrumentation. The default is OFF (include).

• -DDOWNLOAD_BOOST=bool

Whether to download the Boost library. The default is OFF.

See the WITH_BOOST option for additional discussion about using Boost.

• -DDOWNLOAD_BOOST_TIMEOUT=seconds

The timeout in seconds for downloading the Boost library. The default is 600 seconds.

See the WITH_BOOST option for additional discussion about using Boost.

• -DENABLE_DOWNLOADS=bool

Whether to download optional files. For example, with this option enabled, CMake downloads the
Google Test distribution that is used by the test suite to run unit tests, or Ant and JUnit, required for
building the GCS Java wrapper.

As of MySQL 8.0.26, MySQL source distributions bundle the Google Test source code used to run
unit tests. Consequently, as of that version the WITH_GMOCK and ENABLE_DOWNLOADS CMake
options are removed and are ignored if specified.

• -DENABLE_EXPERIMENTAL_SYSVARS=bool

251

MySQL Source-Configuration Options

Whether to enable experimental InnoDB system variables. Experimental system variables are
intended for those engaged in MySQL development, should only be used in a development or
test environment, and may be removed without notice in a future MySQL release. For information
about experimental system variables, refer to /storage/innobase/handler/ha_innodb.cc
in the MySQL source tree. Experimental system variables can be identified by searching for
“PLUGIN_VAR_EXPERIMENTAL”.

• -DENABLE_GCOV=bool

Whether to include gcov support (Linux only).

• -DENABLE_GPROF=bool

Whether to enable gprof (optimized Linux builds only).

• -DENABLED_LOCAL_INFILE=bool

This option controls the compiled-in default LOCAL capability for the MySQL client library. Clients that
make no explicit arrangements therefore have LOCAL capability disabled or enabled according to the
ENABLED_LOCAL_INFILE setting specified at MySQL build time.

By default, the client library in MySQL binary distributions is compiled with
ENABLED_LOCAL_INFILE disabled. If you compile MySQL from source, configure it with
ENABLED_LOCAL_INFILE disabled or enabled based on whether clients that make no explicit
arrangements should have LOCAL capability disabled or enabled, respectively.

ENABLED_LOCAL_INFILE controls the default for client-side LOCAL capability. For the server, the
local_infile system variable controls server-side LOCAL capability. To explicitly cause the server
to refuse or permit LOAD DATA LOCAL statements (regardless of how client programs and libraries
are configured at build time or runtime), start mysqld with --local-infile disabled or enabled,
respectively. local_infile can also be set at runtime. See Section 8.1.6, “Security Considerations
for LOAD DATA LOCAL”.

• -DENABLED_PROFILING=bool

Whether to enable query profiling code (for the SHOW PROFILE and SHOW PROFILES statements).

• -DFORCE_UNSUPPORTED_COMPILER=bool

By default, CMake checks for minimum versions of supported compilers; to disable this check, use -
DFORCE_UNSUPPORTED_COMPILER=ON.

• -DFPROFILE_GENERATE=bool

Whether to generate profile guided optimization (PGO) data. This option is available for
experimenting with PGO with GCC. See cmake/fprofile.cmake in the MySQL source
distribution for information about using FPROFILE_GENERATE and FPROFILE_USE. These options
have been tested with GCC 8 and 9.

This option was added in MySQL 8.0.19.

• -DFPROFILE_USE=bool

Whether to use profile guided optimization (PGO) data. This option is available for experimenting
with PGO with GCC. See the cmake/fprofile.cmake file in a MySQL source distribution for
information about using FPROFILE_GENERATE and FPROFILE_USE. These options have been
tested with GCC 8 and 9.

Enabling FPROFILE_USE also enables WITH_LTO.

This option was added in MySQL 8.0.19.

252

MySQL Source-Configuration Options

• -DHAVE_PSI_MEMORY_INTERFACE=bool

Whether to enable the performance schema memory tracing module for memory allocation functions
(ut::aligned_name library functions) used in dynamic storage of over-aligned types.

• -DIGNORE_AIO_CHECK=bool

If the -DBUILD_CONFIG=mysql_release option is given on Linux, the libaio library must be
linked in by default. If you do not have libaio or do not want to install it, you can suppress the
check for it by specifying -DIGNORE_AIO_CHECK=1.

• -DMAX_INDEXES=num

The maximum number of indexes per table. The default is 64. The maximum is 255. Values smaller
than 64 are ignored and the default of 64 is used.

• -DMYSQL_MAINTAINER_MODE=bool

Whether to enable a MySQL maintainer-specific development environment. If enabled, this option
causes compiler warnings to become errors.

• -DWITH_DEVELOPER_ENTITLEMENTS=bool

Whether to add the get-task-allow entitlement to all executables to generate a core dump in the
event of an unexpected server halt.

On macOS 11+, core dumps are limited to processes with the com.apple.security.get-task-
allow entitlement, which this CMake option enables. The entitlement allows other processes to
attach and read/modify the processes memory, and allows --core-file to function as expected.

This option was added in MySQL 8.0.30.

• -DMUTEX_TYPE=type

The mutex type used by InnoDB. Options include:

• event: Use event mutexes. This is the default value and the original InnoDB mutex

implementation.

• sys: Use POSIX mutexes on UNIX systems. Use CRITICAL_SECTION objects on Windows, if

available.

• futex: Use Linux futexes instead of condition variables to schedule waiting threads.

• -DMYSQLX_TCP_PORT=port_num

The port number on which X Plugin listens for TCP/IP connections. The default is 33060.

This value can be set at server startup with the mysqlx_port system variable.

• -DMYSQLX_UNIX_ADDR=file_name

The Unix socket file path on which the server listens for X Plugin socket connections. This must be
an absolute path name. The default is /tmp/mysqlx.sock.

This value can be set at server startup with the mysqlx_port system variable.

• -DMYSQL_PROJECT_NAME=name

For Windows or macOS, the project name to incorporate into the project file name.

253

MySQL Source-Configuration Options

• -DMYSQL_TCP_PORT=port_num

The port number on which the server listens for TCP/IP connections. The default is 3306.

This value can be set at server startup with the --port option.

• -DMYSQL_UNIX_ADDR=file_name

The Unix socket file path on which the server listens for socket connections. This must be an
absolute path name. The default is /tmp/mysql.sock.

This value can be set at server startup with the --socket option.

• -DOPTIMIZER_TRACE=bool

Whether to support optimizer tracing. See Section 10.15, “Tracing the Optimizer”.

• -DREPRODUCIBLE_BUILD=bool

For builds on Linux systems, this option controls whether to take extra care to create a build result
independent of build location and time.

This option was added in MySQL 8.0.11. As of MySQL 8.0.12, it defaults to ON for
RelWithDebInfo builds.

• -DSHOW_SUPPRESSED_COMPILER_WARNINGS=bool

Show suppressed compiler warnings, and do so without failing with -Werror. Defaults to OFF.

This option was added in MySQL 8.0.30.

• -DUSE_LD_GOLD=bool

GNU gold linker support was removed in MySQL 8.0.31; this CMake option was also removed.

CMake causes the build process to link with the GNU gold linker if it is available and not explicitly
disabled. To disable use of this linker, specify the -DUSE_LD_GOLD=OFF option.

• -DUSE_LD_LLD=bool

CMake causes the build process to link using the LLVM lld linker for Clang if it is available and not
explicitly disabled. To disable use of this linker, specify the -DUSE_LD_LLD=OFF option.

This option was added in MySQL 8.0.16.

• -DWIN_DEBUG_NO_INLINE=bool

Whether to disable function inlining on Windows. The default is OFF (inlining enabled).

• -DWITH_ANT=path_name

Set the path to Ant, required when building GCS Java wrapper. Set WITH_ANT to the path of a
directory where the Ant tarball or unpacked archive is saved. When WITH_ANT is not set, or is set
with the special value system, the build process assumes a binary ant exists in $PATH.

• -DWITH_ASAN=bool

Whether to enable the AddressSanitizer, for compilers that support it. The default is OFF.

• -DWITH_ASAN_SCOPE=bool

Whether to enable the AddressSanitizer -fsanitize-address-use-after-scope Clang flag
for use-after-scope detection. The default is off. To use this option, -DWITH_ASAN must also be
enabled.

254

MySQL Source-Configuration Options

• -DWITH_AUTHENTICATION_CLIENT_PLUGINS=bool

This option is enabled automatically if any corresponding server authentication plugins are built. Its
value thus depends on other CMake options and it should not be set explicitly.

This option was added in MySQL 8.0.26.

• -DWITH_AUTHENTICATION_LDAP=bool

Whether to report an error if the LDAP authentication plugins cannot be built:

• If this option is disabled (the default), the LDAP plugins are built if the required header files and

libraries are found. If they are not, CMake displays a note about it.

• If this option is enabled, a failure to find the required header file and libraries causes CMake to

produce an error, preventing the server from being built.

For information about LDAP authentication, see Section 8.4.1.7, “LDAP Pluggable Authentication”.

• -DWITH_AUTHENTICATION_PAM=bool

Whether to build the PAM authentication plugin, for source trees that include this plugin. (See
Section 8.4.1.5, “PAM Pluggable Authentication”.) If this option is specified and the plugin cannot be
compiled, the build fails.

• -DWITH_AWS_SDK=path_name

The location of the Amazon Web Services software development kit.

• -DWITH_BOOST=path_name

The Boost library is required to build MySQL. These CMake options enable control over the library
source location, and whether to download it automatically:

• -DWITH_BOOST=path_name specifies the Boost library directory location. It is also possible to
specify the Boost location by setting the BOOST_ROOT or WITH_BOOST environment variable.

-DWITH_BOOST=system is also permitted and indicates that the correct version of Boost is
installed on the compilation host in the standard location. In this case, the installed version of
Boost is used rather than any version included with a MySQL source distribution.

• -DDOWNLOAD_BOOST=bool specifies whether to download the Boost source if it is not present in

the specified location. The default is OFF.

• -DDOWNLOAD_BOOST_TIMEOUT=seconds the timeout in seconds for downloading the Boost

library. The default is 600 seconds.

For example, if you normally build MySQL placing the object output in the bld subdirectory of your
MySQL source tree, you can build with Boost like this:

mkdir bld
cd bld
cmake .. -DDOWNLOAD_BOOST=ON -DWITH_BOOST=$HOME/my_boost

This causes Boost to be downloaded into the my_boost directory under your home directory. If the
required Boost version is already there, no download is done. If the required Boost version changes,
the newer version is downloaded.

If Boost is already installed locally and your compiler finds the Boost header files on its own, it may
not be necessary to specify the preceding CMake options. However, if the version of Boost required

255

MySQL Source-Configuration Options

by MySQL changes and the locally installed version has not been upgraded, you may have build
problems. Using the CMake options should give you a successful build.

With the above settings that allow Boost download into a specified location, when the required Boost
version changes, you need to remove the bld folder, recreate it, and perform the cmake step again.
Otherwise, the new Boost version might not get downloaded, and compilation might fail.

• -DWITH_CLIENT_PROTOCOL_TRACING=bool

Whether to build the client-side protocol tracing framework into the client library. By default, this
option is enabled.

For information about writing protocol trace client plugins, see Writing Protocol Trace Plugins.

See also the WITH_TEST_TRACE_PLUGIN option.

• -DWITH_CURL=curl_type

The location of the curl library. curl_type can be system (use the system curl library) or a path
name to the curl library.

• -DWITH_DEBUG=bool

Whether to include debugging support.

Configuring MySQL with debugging support enables you to use the --debug="d,parser_debug"
option when you start the server. This causes the Bison parser that is used to process SQL
statements to dump a parser trace to the server's standard error output. Typically, this output is
written to the error log.

Sync debug checking for the InnoDB storage engine is defined under UNIV_DEBUG and is available
when debugging support is compiled in using the WITH_DEBUG option. When debugging support
is compiled in, the innodb_sync_debug configuration option can be used to enable or disable
InnoDB sync debug checking.

Enabling WITH_DEBUG also enables Debug Sync. This facility is used for testing and debugging.
When compiled in, Debug Sync is disabled by default at runtime. To enable it, start mysqld with the
--debug-sync-timeout=N option, where N is a timeout value greater than 0. (The default value is
0, which disables Debug Sync.) N becomes the default timeout for individual synchronization points.

Sync debug checking for the InnoDB storage engine is available when debugging support is
compiled in using the WITH_DEBUG option.

For a description of the Debug Sync facility and how to use synchronization points, see MySQL
Internals: Test Synchronization.

• -DWITH_DEFAULT_FEATURE_SET=bool

Whether to use the flags from cmake/build_configurations/feature_set.cmake. This
option was removed in MySQL 8.0.22.

• -DWITH_EDITLINE=value

Which libedit/editline library to use. The permitted values are bundled (the default) and
system.

256

MySQL Source-Configuration Options

• -DWITH_FIDO=fido_type

The authentication_fido authentication plugin is implemented using a FIDO library (see
Section 8.4.1.11, “FIDO Pluggable Authentication”). The WITH_FIDO option indicates the source of
FIDO support:

• bundled: Use the FIDO library bundled with the distribution. This is the default.

As of MySQL 8.0.30, MySQL includes fido2 version 1.8.0. (Prior releases used fido2 1.5.0).

• system: Use the system FIDO library.

WITH_FIDO is disabled (set to none) if all authentication plugins are disabled.

This option was added in MySQL 8.0.27.

• -DWITH_GMOCK=path_name

The path to the googlemock distribution, for use with Google Test-based unit tests. The option value
is the path to the distribution zip file. Alternatively, set the WITH_GMOCK environment variable to
the path name. It is also possible to use -DENABLE_DOWNLOADS=1, so that CMake downloads the
distribution from GitHub.

If you build MySQL without the Google Test unit tests (by configuring without WITH_GMOCK), CMake
displays a message indicating how to download it.

As of MySQL 8.0.26, MySQL source distributions bundle the Google Test source code.
Consequently, as of that version, the WITH_GMOCK and ENABLE_DOWNLOADS CMake options are
removed and are ignored if specified.

• -DWITH_ICU={icu_type|path_name}

MySQL uses International Components for Unicode (ICU) to support regular expression operations.
The WITH_ICU option indicates the type of ICU support to include or the path name to the ICU
installation to use.

• icu_type can be one of the following values:

• bundled: Use the ICU library bundled with the distribution. This is the default, and is the only

supported option for Windows.

• system: Use the system ICU library.

• path_name is the path name to the ICU installation to use. This can be preferable to using the

icu_type value of system because it can prevent CMake from detecting and using an older or
incorrect ICU version installed on the system. (Another permitted way to do the same thing is to
set WITH_ICU to system and set the CMAKE_PREFIX_PATH option to path_name.)

• -DWITH_INNODB_EXTRA_DEBUG=bool

Whether to include extra InnoDB debugging support.

Enabling WITH_INNODB_EXTRA_DEBUG turns on extra InnoDB debug checks. This option can only
be enabled when WITH_DEBUG is enabled.

• -DWITH_INNODB_MEMCACHED=bool

Whether to generate memcached shared libraries (libmemcached.so and innodb_engine.so).

257

MySQL Source-Configuration Options

• -DWITH_JEMALLOC=bool

Whether to link with -ljemalloc. If enabled, built-in malloc(), calloc(), realloc(), and
free() routines are disabled. The default is OFF.

WITH_JEMALLOC and WITH_TCMALLOC are mutually exclusive.

This option was added in MySQL 8.0.16.

• -DWITH_KEYRING_TEST=bool

Whether to build the test program that accompanies the keyring_file plugin. The default is OFF.
Test file source code is located in the plugin/keyring/keyring-test directory.

• -DWITH_LIBEVENT=string

Which libevent library to use. Permitted values are bundled (default) and system. Prior to
MySQL 8.0.21, if you specify system, the system libevent library is used if present, and an error
occurs otherwise. In MySQL 8.0.21 and later, if system is specified and no system libevent
library can be found, an error occurs regardless, and the bundled libevent is not used.

The libevent library is required by InnoDB memcached, X Plugin, and MySQL Router.

• -DWITH_LIBWRAP=bool

Whether to include libwrap (TCP wrappers) support.

• -DWITH_LOCK_ORDER=bool

Whether to enable LOCK_ORDER tooling. By default, this option is disabled and server builds
contain no tooling. If tooling is enabled, the LOCK_ORDER tool is available and can be used as
described in Section 7.9.3, “The LOCK_ORDER Tool”.

Note

With the WITH_LOCK_ORDER option enabled, MySQL builds require the flex
program.

This option was added in MySQL 8.0.17.

• -DWITH_LSAN=bool

Whether to run LeakSanitizer, without AddressSanitizer. The default is OFF.

This option was added in MySQL 8.0.16.

• -DWITH_LTO=bool

Whether to enable the link-time optimizer, if the compiler supports it. The default is OFF unless
FPROFILE_USE is enabled.

This option was added in MySQL 8.0.13.

• -DWITH_LZ4=lz4_type

The WITH_LZ4 option indicates the source of zlib support:

• bundled: Use the lz4 library bundled with the distribution. This is the default.

• system: Use the system lz4 library. If WITH_LZ4 is set to this value, the lz4_decompress utility

is not built. In this case, the system lz4 command can be used instead.

• -DWITH_LZMA=lzma_type

258

MySQL Source-Configuration Options

The type of LZMA library support to include. lzma_type can be one of the following values:

• bundled: Use the LZMA library bundled with the distribution. This is the default.

• system: Use the system LZMA library.

This option was removed in MySQL 8.0.16.

• -DWITH_MECAB={disabled|system|path_name}

Use this option to compile the MeCab parser. If you have installed MeCab to its default installation
directory, set -DWITH_MECAB=system. The system option applies to MeCab installations
performed from source or from binaries using a native package management utility. If you installed
MeCab to a custom installation directory, specify the path to the MeCab installation, for example, -
DWITH_MECAB=/opt/mecab. If the system option does not work, specifying the MeCab installation
path should work in all cases.

For related information, see Section 14.9.9, “MeCab Full-Text Parser Plugin”.

• -DWITH_MSAN=bool

Whether to enable MemorySanitizer, for compilers that support it. The default is off.

For this option to have an effect if enabled, all libraries linked to MySQL must also have been
compiled with the option enabled.

• -DWITH_MSCRT_DEBUG=bool

Whether to enable Visual Studio CRT memory leak tracing. The default is OFF.

• -DMSVC_CPPCHECK=bool

Whether to enable MSVC code analysis. The default is OFF.

• -DWITH_MYSQLX=bool

Whether to build with support for X Plugin. The default is ON. See Chapter 22, Using MySQL as a
Document Store.

• -DWITH_NUMA=bool

Explicitly set the NUMA memory allocation policy. CMake sets the default WITH_NUMA value based
on whether the current platform has NUMA support. For platforms without NUMA support, CMake
behaves as follows:

• With no NUMA option (the normal case), CMake continues normally, producing only this warning:

NUMA library missing or required version not available.

• With -DWITH_NUMA=ON, CMake aborts with this error: NUMA library missing or required

version not available.

• -DWITH_PACKAGE_FLAGS=bool

For flags typically used for RPM and Debian packages, whether to add them to standalone builds on
those platforms. The default is ON for nondebug builds.

This option was added in MySQL 8.0.26.

259

MySQL Source-Configuration Options

• -DWITH_PROTOBUF=protobuf_type

Which Protocol Buffers package to use. protobuf_type can be one of the following values:

• bundled: Use the package bundled with the distribution. This is the default. Optionally use

INSTALL_PRIV_LIBDIR to modify the dynamic Protobuf library directory.

• system: Use the package installed on the system.

Other values are ignored, with a fallback to bundled.

• -DWITH_RAPID=bool

Whether to build the rapid development cycle plugins. When enabled, a rapid directory is created
in the build tree containing these plugins. When disabled, no rapid directory is created in the build
tree. The default is ON, unless the rapid directory is removed from the source tree, in which case
the default becomes OFF.

• -DWITH_RAPIDJSON=rapidjson_type

The type of RapidJSON library support to include. rapidjson_type can be one of the following
values:

• bundled: Use the RapidJSON library bundled with the distribution. This is the default.

• system: Use the system RapidJSON library. Version 1.1.0 or later is required.

This option was added in MySQL 8.0.13.

• -DWITH_RE2=re2_type

The type of RE2 library support to include. re2_type can be one of the following values:

• bundled: Use the RE2 library bundled with the distribution. This is the default.

• system: Use the system RE2 library.

As of MySQL 8.0.18, MySQL no longer uses the RE2 library, and this option has been removed.

• -DWITH_ROUTER=bool

Whether to build MySQL Router. The default is ON.

This option was added in MySQL 8.0.16.

• -DWITH_SASL=value

Internal use only. This option was added in 8.0.20. Not supported on Windows.

• -DWITH_SSL={ssl_type|path_name}

For support of encrypted connections, entropy for random number generation, and other encryption-
related operations, MySQL must be built using an SSL library. This option specifies which SSL library
to use.

• ssl_type can be one of the following values:

• system: Use the system OpenSSL library. This is the default.

On macOS and Windows, using system configures MySQL to build as if CMake was invoked
with path_name points to a manually installed OpenSSL library. This is because they do not
have system SSL libraries. On macOS, brew install openssl installs to /usr/local/opt/
openssl so that system can find it. On Windows, it checks %ProgramFiles%/OpenSSL,

260

MySQL Source-Configuration Options

%ProgramFiles%/OpenSSL-Win32, %ProgramFiles%/OpenSSL-Win64, C:/OpenSSL,
C:/OpenSSL-Win32, and C:/OpenSSL-Win64.

• yes: This is a synonym for system.

• opensslversion: (MySQL 8.0.30 and later:) Use an alternate OpenSSL system package such

as openssl11 on EL7, or openssl3 on EL8.

Authentication plugins, such as LDAP and Kerberos, are disabled as they do not support these
alternative versions of OpenSSL.

• path_name is the path name to the OpenSSL installation to use. This can be preferable to using
the ssl_type value of system because it can prevent CMake from detecting and using an older
or incorrect OpenSSL version installed on the system. (Another permitted way to do the same
thing is to set WITH_SSL to system and set the CMAKE_PREFIX_PATH option to path_name.)

For additional information about configuring the SSL library, see Section 2.8.6, “Configuring SSL
Library Support”.

• -DWITH_SYSTEMD=bool

Whether to enable installation of systemd support files. By default, this option is disabled. When
enabled, systemd support files are installed, and scripts such as mysqld_safe and the System
V initialization script are not installed. On platforms where systemd is not available, enabling
WITH_SYSTEMD results in an error from CMake.

For more information about using systemd, see Section 2.5.9, “Managing MySQL Server with
systemd”. That section also includes information about specifying options otherwise specified in
[mysqld_safe] option groups. Because mysqld_safe is not installed when systemd is used,
such options must be specified another way.

• -DWITH_SYSTEM_LIBS=bool

This option serves as an “umbrella” option to set the system value of any of the following CMake
options that are not set explicitly: WITH_CURL, WITH_EDITLINE, WITH_FIDO, WITH_ICU,
WITH_LIBEVENT, WITH_LZ4, WITH_LZMA, WITH_PROTOBUF, WITH_RE2, WITH_SSL, WITH_ZSTD.

WITH_ZLIB was included here priot MySQL 8.0.30.

• -DWITH_SYSTEMD_DEBUG=bool

Whether to produce additional systemd debugging information, for platforms on which systemd is
used to run MySQL. The default is OFF.

This option was added in MySQL 8.0.22.

• -DWITH_TCMALLOC=bool

Whether to link with -ltcmalloc. If enabled, built-in malloc(), calloc(), realloc(), and
free() routines are disabled. The default is OFF.

Beginning with MySQL 8.0.38, a tcmalloc library is included in the source; you can cause the
build to use the bundled version by setting this option to BUNDLED. BUNDLED is supported on Linux
systems only.

WITH_TCMALLOC and WITH_JEMALLOC are mutually exclusive.

This option was added in MySQL 8.0.22.

261

MySQL Source-Configuration Options

• -DWITH_TEST_TRACE_PLUGIN=bool

Whether to build the test protocol trace client plugin (see Using the Test Protocol Trace
Plugin). By default, this option is disabled. Enabling this option has no effect unless the
WITH_CLIENT_PROTOCOL_TRACING option is enabled. If MySQL is configured with both options
enabled, the libmysqlclient client library is built with the test protocol trace plugin built in, and all
the standard MySQL clients load the plugin. However, even when the test plugin is enabled, it has no
effect by default. Control over the plugin is afforded using environment variables; see Using the Test
Protocol Trace Plugin.

Note

Do not enable the WITH_TEST_TRACE_PLUGIN option if you want to use
your own protocol trace plugins because only one such plugin can be loaded
at a time and an error occurs for attempts to load a second one. If you have
already built MySQL with the test protocol trace plugin enabled to see how
it works, you must rebuild MySQL without it before you can use your own
plugins.

For information about writing trace plugins, see Writing Protocol Trace Plugins.

• -DWITH_TSAN=bool

Whether to enable the ThreadSanitizer, for compilers that support it. The default is off.

• -DWITH_UBSAN=bool

Whether to enable the Undefined Behavior Sanitizer, for compilers that support it. The default is off.

• -DWITH_UNIT_TESTS={ON|OFF}

If enabled, compile MySQL with unit tests. The default is ON unless the server is not being compiled.

• -DWITH_UNIXODBC=1

Enables unixODBC support, for Connector/ODBC.

• -DWITH_VALGRIND=bool

Whether to compile in the Valgrind header files, which exposes the Valgrind API to MySQL code.
The default is OFF.

To generate a Valgrind-aware debug build, -DWITH_VALGRIND=1 normally is combined with -
DWITH_DEBUG=1. See Building Debug Configurations.

• -DWITH_WIN_JEMALLOC=string

On Windows, pass in a path to a directory containing jemalloc.dll to enable jemalloc
functionality. The build system copies jemalloc.dll to the same directory as mysqld.exe and/
or mysqld-debug.exe and utilizes it for memory management operations. Standard memory
functions are used if jemalloc.dll is not found or does not export the required functions. An
INFORMATION level log message records whether or not jemalloc is found and used.

This option is enabled for official MySQL binaries for Windows.

This option was added in MySQL 8.0.29.

• -DWITH_ZLIB=zlib_type

Some features require that the server be built with compression library support, such as the
COMPRESS() and UNCOMPRESS() functions, and compression of the client/server protocol. The
WITH_ZLIB option indicates the source of zlib support:

262

MySQL Source-Configuration Options

In MYSQL 8.0.32 and later, the minimum supported version of zlib is 1.2.13.

• bundled: Use the zlib library bundled with the distribution. This is the default.

• system: Use the system zlib library. If WITH_ZLIB is set to this value, the zlib_decompress

utility is not built. In this case, the system openssl zlib command can be used instead.

• -DWITH_ZSTD=zstd_type

Connection compression using the zstd algorithm (see Section 6.2.8, “Connection Compression
Control”) requires that the server be built with zstd library support. The WITH_ZSTD option indicates
the source of zstd support:

• bundled: Use the zstd library bundled with the distribution. This is the default.

• system: Use the system zstd library.

This option was added in MySQL 8.0.18.

• -DWITHOUT_SERVER=bool

Whether to build without MySQL Server. The default is OFF, which does build the server.

This is considered an experimental option; it is preferred to build with the server.

This option also prevents building of the NDB storage engine or any NDB binaries including
management and data node programs.

Compiler Flags

• -DCMAKE_C_FLAGS="flags"

Flags for the C compiler.

• -DCMAKE_CXX_FLAGS="flags"

Flags for the C++ compiler.

• -DWITH_DEFAULT_COMPILER_OPTIONS=bool

Whether to use the flags from cmake/build_configurations/compiler_options.cmake.

Note

All optimization flags are carefully chosen and tested by the MySQL build
team. Overriding them can lead to unexpected results and is done at your
own risk.

• -DOPTIMIZE_SANITIZER_BUILDS=bool

Whether to add -O1 -fno-inline to sanitizer builds. The default is ON.

To specify your own C and C++ compiler flags, for flags that do not affect optimization, use the
CMAKE_C_FLAGS and CMAKE_CXX_FLAGS CMake options.

When providing your own compiler flags, you might want to specify CMAKE_BUILD_TYPE as well.

For example, to create a 32-bit release build on a 64-bit Linux machine, do this:

$> mkdir build
$> cd build
$> cmake .. -DCMAKE_C_FLAGS=-m32 \
  -DCMAKE_CXX_FLAGS=-m32 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo

263

MySQL Source-Configuration Options

If you set flags that affect optimization (-Onumber), you must set the CMAKE_C_FLAGS_build_type
and/or CMAKE_CXX_FLAGS_build_type options, where build_type corresponds
to the CMAKE_BUILD_TYPE value. To specify a different optimization for the default
build type (RelWithDebInfo) set the CMAKE_C_FLAGS_RELWITHDEBINFO and
CMAKE_CXX_FLAGS_RELWITHDEBINFO options. For example, to compile on Linux with -O3 and with
debug symbols, do this:

$> cmake .. -DCMAKE_C_FLAGS_RELWITHDEBINFO="-O3 -g" \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-O3 -g"

CMake Options for Compiling NDB Cluster

To compile with support for NDB Cluster, you can use -DWITH_NDB, which causes the build to include
the NDB storage engine and all NDB programs. This option is enabled by default. To prevent building
of the NDB storage engine plugin, use -DWITH_NDBCLUSTER_STORAGE_ENGINE=OFF. Other aspects
of the build can be controlled using the other options listed in this section.

The following options apply when building the MySQL sources with NDB Cluster support.

• -DMEMCACHED_HOME=dir_name

NDB support for memcached was removed in NDB 8.0.23; thus, this option is no longer supported for
building NDB in this or later versions.

• -DNDB_UTILS_LINK_DYNAMIC={ON|OFF}

Controls whether NDB utilities such as ndb_drop_table are linked with ndbclient statically
(OFF) or dynamically (ON); OFF (static linking) is the default. Normally static linking is used when
building these to avoid problems with LD_LIBRARY_PATH, or when multiple versions of ndbclient
are installed. This option is intended for creating Docker images and possibly other cases in which
the target environment is subject to precise control and it is desirable to reduce image size.

Added in NDB 8.0.22.

• -DWITH_BUNDLED_LIBEVENT={ON|OFF}

NDB support for memcached was removed in NDB 8.0.23; thus, this option is no longer supported for
building NDB in this or later versions.

• -DWITH_BUNDLED_MEMCACHED={ON|OFF}

NDB support for memcached was removed in NDB 8.0.23; thus, this option is no longer supported for
building NDB in this or later versions.

• -DWITH_CLASSPATH=path

Sets the classpath for building MySQL NDB Cluster Connector for Java. The default is empty. This
option is ignored if -DWITH_NDB_JAVA=OFF is used.

• -DWITH_ERROR_INSERT={ON|OFF}

Enables error injection in the NDB kernel. For testing only; not intended for use in building production
binaries. The default is OFF.

• -DWITH_NDB={ON|OFF}

Build MySQL NDB Cluster; build the NDB plugin and all NDB Cluster programs.

Added in NDB 8.0.31.

• -DWITH_NDBAPI_EXAMPLES={ON|OFF}

264

Dealing with Problems Compiling MySQL

Build NDB API example programs in storage/ndb/ndbapi-examples/. See NDB API
Examples, for information about these.

• -DWITH_NDBCLUSTER_STORAGE_ENGINE={ON|OFF}

NDB 8.0.30 and earlier: For internal use only; may not always work as expected. To build with NDB
support, use WITH_NDBCLUSTER instead.

NDB 8.0.31 and later: Controls (only) whether the NDBCLUSTER storage engine is included in the
build; WITH_NDB enables this option automatically, so it is recommended that you use WITH_NDB
instead.

• -DWITH_NDBCLUSTER={ON|OFF} (DEPRECATED)

Build and link in support for the NDB storage engine in mysqld.

This option is deprecated as of NDB 8.0.31, and subject to eventual removal; use WITH_NDB
instead.

• -DWITH_NDBMTD={ON|OFF}

Build the multithreaded data node executable ndbmtd. The default is ON.

• -DWITH_NDB_DEBUG={ON|OFF}

Enable building the debug versions of the NDB Cluster binaries. This is OFF by default.

• -DWITH_NDB_JAVA={ON|OFF}

Enable building NDB Cluster with Java support, including support for ClusterJ (see MySQL NDB
Cluster Connector for Java).

This option is ON by default. If you do not wish to compile NDB Cluster with Java support, you must
disable it explicitly by specifying -DWITH_NDB_JAVA=OFF when running CMake. Otherwise, if Java
cannot be found, configuration of the build fails.

• -DWITH_NDB_PORT=port

Causes the NDB Cluster management server (ndb_mgmd) that is built to use this port by default. If
this option is unset, the resulting management server tries to use port 1186 by default.

• -DWITH_NDB_TEST={ON|OFF}

If enabled, include a set of NDB API test programs. The default is OFF.

• -DWITH_PLUGIN_NDBCLUSTER={ON|OFF}

For internal use only; may not always work as expected. This option was removed in NDB
8.0.31; use WITH_NDB instead to build MySQL NDB Cluster. (NDB 8.0.30 and earlier: Use
WITH_NDBCLUSTER.)

2.8.8 Dealing with Problems Compiling MySQL

The solution to many problems involves reconfiguring. If you do reconfigure, take note of the following:

• If CMake is run after it has previously been run, it may use information that was gathered during its

previous invocation. This information is stored in CMakeCache.txt. When CMake starts, it looks for
that file and reads its contents if it exists, on the assumption that the information is still correct. That
assumption is invalid when you reconfigure.

265

Dealing with Problems Compiling MySQL

• Each time you run CMake, you must run make again to recompile. However, you may want to
remove old object files from previous builds first because they were compiled using different
configuration options.

To prevent old object files or configuration information from being used, run the following commands
before re-running CMake:

On Unix:

$> make clean
$> rm CMakeCache.txt

On Windows:

$> devenv MySQL.sln /clean
$> del CMakeCache.txt

If you build outside of the source tree, remove and recreate your build directory before re-running
CMake. For instructions on building outside of the source tree, see How to Build MySQL Server with
CMake.

On some systems, warnings may occur due to differences in system include files. The following list
describes other problems that have been found to occur most often when compiling MySQL:

•     To define which C and C++ compilers to use, you can define the CC and CXX environment

variables. For example:

$> CC=gcc
$> CXX=g++
$> export CC CXX

While this can be done on the command line, as just shown, you may prefer to define these values in
a build script, in which case the export command is not needed.

To specify your own C and C++ compiler flags, use the CMAKE_C_FLAGS and CMAKE_CXX_FLAGS
CMake options. See Compiler Flags.

To see what flags you might need to specify, invoke mysql_config with the --cflags and --
cxxflags options.

• To see what commands are executed during the compile stage, after using CMake to configure

MySQL, run make VERBOSE=1 rather than just make.

• If compilation fails, check whether the MYSQL_MAINTAINER_MODE option is enabled. This mode
causes compiler warnings to become errors, so disabling it may enable compilation to proceed.

• If your compile fails with errors such as any of the following, you must upgrade your version of make

to GNU make:

make: Fatal error in reader: Makefile, line 18:
Badly formed macro assignment

Or:

make: file `Makefile' line 18: Must be a separator (:

Or:

pthread.h: No such file or directory

Solaris and FreeBSD are known to have troublesome make programs.

GNU make 3.75 is known to work.

266

MySQL Configuration and Third-Party Tools

• The sql_yacc.cc file is generated from sql_yacc.yy. Normally, the build process does not need
to create sql_yacc.cc because MySQL comes with a pregenerated copy. However, if you do need
to re-create it, you might encounter this error:

"sql_yacc.yy", line xxx fatal: default action causes potential...

This is a sign that your version of yacc is deficient. You probably need to install a recent version of
bison (the GNU version of yacc) and use that instead.

Versions of bison older than 1.75 may report this error:

sql_yacc.yy:#####: fatal error: maximum table size (32767) exceeded

The maximum table size is not actually exceeded; the error is caused by bugs in older versions of
bison.

For information about acquiring or updating tools, see the system requirements in Section 2.8,
“Installing MySQL from Source”.

2.8.9 MySQL Configuration and Third-Party Tools

Third-party tools that need to determine the MySQL version from the MySQL source can read the
MYSQL_VERSION file in the top-level source directory. The file lists the pieces of the version separately.
For example, if the version is MySQL 8.0.36, the file looks like this:

MYSQL_VERSION_MAJOR=8
MYSQL_VERSION_MINOR=0
MYSQL_VERSION_PATCH=36
MYSQL_VERSION_EXTRA=
MYSQL_VERSION_STABILITY="LTS"

Note

In MySQL 5.7 and earlier, this file was named VERSION.

To construct a five-digit number from the version components, use this formula:

MYSQL_VERSION_MAJOR*10000 + MYSQL_VERSION_MINOR*100 + MYSQL_VERSION_PATCH

2.8.10 Generating MySQL Doxygen Documentation Content

The MySQL source code contains internal documentation written using Doxygen. The generated
Doxygen content is available at https://dev.mysql.com/doc/index-other.html. It is also possible to
generate this content locally from a MySQL source distribution using the following procedure:

1.

Install doxygen 1.9.2 or later. Distributions are available here at http://www.doxygen.nl/.

After installing doxygen, verify the version number:

$> doxygen --version
1.9.2

2.

Install PlantUML.

When you install PlantUML on Windows (tested on Windows 10), you must run it at least once as
administrator so it creates the registry keys. Open an administrator console and run this command:

$> java -jar path-to-plantuml.jar

The command should open a GUI window and return no errors on the console.

3. Set the PLANTUML_JAR_PATH environment to the location where you installed PlantUML. For

example:

267

Postinstallation Setup and Testing

$> export PLANTUML_JAR_PATH=path-to-plantuml.jar

4.

Install the Graphviz dot command.

After installing Graphviz, verify dot availability. For example:

$> which dot
/usr/bin/dot

$> dot -V
dot - graphviz version 2.40.1 (20161225.0304)

5. Change location to the top-level directory of your MySQL source distribution and do the following:

First, execute cmake:

$> cd mysql-source-directory
$> mkdir build
$> cd build
$> cmake ..

Next, generate the doxygen documentation:

$> make doxygen

Inspect the error log, which is available in the doxyerror.log file in the top-level directory.
Assuming that the build executed successfully, view the generated output using a browser. For
example:

$> firefox doxygen/html/index.html

2.9 Postinstallation Setup and Testing

This section discusses tasks that you should perform after installing MySQL:

• If necessary, initialize the data directory and create the MySQL grant tables. For some MySQL

installation methods, data directory initialization may be done for you automatically:

• Windows installation operations performed by MySQL Installer.

• Installation on Linux using a server RPM or Debian distribution from Oracle.

• Installation using the native packaging system on many platforms, including Debian Linux, Ubuntu

Linux, Gentoo Linux, and others.

• Installation on macOS using a DMG distribution.

For other platforms and installation types, you must initialize the data directory manually. These
include installation from generic binary and source distributions on Unix and Unix-like system, and
installation from a ZIP Archive package on Windows. For instructions, see Section 2.9.1, “Initializing
the Data Directory”.

• Start the server and make sure that it can be accessed. For instructions, see Section 2.9.2, “Starting

the Server”, and Section 2.9.3, “Testing the Server”.

• Assign passwords to the initial root account in the grant tables, if that was not already done during

data directory initialization. Passwords prevent unauthorized access to the MySQL server. For
instructions, see Section 2.9.4, “Securing the Initial MySQL Account”.

• Optionally, arrange for the server to start and stop automatically when your system starts and stops.

For instructions, see Section 2.9.5, “Starting and Stopping MySQL Automatically”.

• Optionally, populate time zone tables to enable recognition of named time zones. For instructions,

see Section 7.1.15, “MySQL Server Time Zone Support”.

268

Initializing the Data Directory

When you are ready to create additional user accounts, you can find information on the MySQL access
control system and account management in Section 8.2, “Access Control and Account Management”.

2.9.1 Initializing the Data Directory

After MySQL is installed, the data directory must be initialized, including the tables in the mysql
system schema:

• For some MySQL installation methods, data directory initialization is automatic, as described in

Section 2.9, “Postinstallation Setup and Testing”.

• For other installation methods, you must initialize the data directory manually. These include
installation from generic binary and source distributions on Unix and Unix-like systems, and
installation from a ZIP Archive package on Windows.

This section describes how to initialize the data directory manually for MySQL installation methods for
which data directory initialization is not automatic. For some suggested commands that enable testing
whether the server is accessible and working properly, see Section 2.9.3, “Testing the Server”.

Note

In MySQL 8.0, the default authentication plugin has changed from
mysql_native_password to caching_sha2_password,
and the 'root'@'localhost' administrative account uses
caching_sha2_password by default. If you prefer that the root account use
the previous default authentication plugin (mysql_native_password), see
caching_sha2_password and the root Administrative Account.

The mysql_native_password plugin is deprecated as of MySQL 8.0.34,
disabled by default as of MySQL 8.4.0, and removed as of MySQL 9.0.0.

• Data Directory Initialization Overview

• Data Directory Initialization Procedure

• Server Actions During Data Directory Initialization

• Post-Initialization root Password Assignment

Data Directory Initialization Overview

In the examples shown here, the server is intended to run under the user ID of the mysql login
account. Either create the account if it does not exist (see Create a mysql User and Group), or
substitute the name of a different existing login account that you plan to use for running the server.

1. Change location to the top-level directory of your MySQL installation, which is typically /usr/

local/mysql (adjust the path name for your system as necessary):

cd /usr/local/mysql

Within this directory you can find several files and subdirectories, including the bin subdirectory
that contains the server, as well as client and utility programs.

2. The secure_file_priv system variable limits import and export operations to a specific
directory. Create a directory whose location can be specified as the value of that variable:

mkdir mysql-files

Grant directory user and group ownership to the mysql user and mysql group, and set the
directory permissions appropriately:

chown mysql:mysql mysql-files
chmod 750 mysql-files

269

Initializing the Data Directory

3. Use the server to initialize the data directory, including the mysql schema containing the initial

MySQL grant tables that determine how users are permitted to connect to the server. For example:

bin/mysqld --initialize --user=mysql

For important information about the command, especially regarding command options you might
use, see Data Directory Initialization Procedure. For details about how the server performs
initialization, see Server Actions During Data Directory Initialization.

Typically, data directory initialization need be done only after you first install MySQL. (For upgrades
to an existing installation, perform the upgrade procedure instead; see Chapter 3, Upgrading
MySQL.) However, the command that initializes the data directory does not overwrite any existing
mysql schema tables, so it is safe to run in any circumstances.

4.

If you want to deploy the server with automatic support for secure connections, use the
mysql_ssl_rsa_setup utility to create default SSL and RSA files:

bin/mysql_ssl_rsa_setup

For more information, see Section 6.4.3, “mysql_ssl_rsa_setup — Create SSL/RSA Files”.

Note

The mysql_ssl_rsa_setup utility is deprecated as of MySQL 8.0.34.

5.

In the absence of any option files, the server starts with its default settings. (See Section 7.1.2,
“Server Configuration Defaults”.) To explicitly specify options that the MySQL server should
use at startup, put them in an option file such as /etc/my.cnf or /etc/mysql/my.cnf.
(See Section 6.2.2.2, “Using Option Files”.) For example, you can use an option file to set the
secure_file_priv system variable.

6. To arrange for MySQL to start without manual intervention at system boot time, see Section 2.9.5,

“Starting and Stopping MySQL Automatically”.

7. Data directory initialization creates time zone tables in the mysql schema but does not populate
them. To do so, use the instructions in Section 7.1.15, “MySQL Server Time Zone Support”.

Data Directory Initialization Procedure

Change location to the top-level directory of your MySQL installation, which is typically /usr/local/
mysql (adjust the path name for your system as necessary):

cd /usr/local/mysql

To initialize the data directory, invoke mysqld with the --initialize or --initialize-insecure
option, depending on whether you want the server to generate a random initial password for the
'root'@'localhost' account, or to create that account with no password:

• Use --initialize for “secure by default” installation (that is, including generation of a random

initial root password). In this case, the password is marked as expired and you must choose a new
one.

• With --initialize-insecure, no root password is generated. This is insecure; it is assumed

that you intend to assign a password to the account in a timely fashion before putting the server into
production use.

For instructions on assigning a new 'root'@'localhost' password, see Post-Initialization root
Password Assignment.

Note

The server writes any messages (including any initial password) to its standard
error output. This may be redirected to the error log, so look there if you do not

270

Initializing the Data Directory

see the messages on your screen. For information about the error log, including
where it is located, see Section 7.4.2, “The Error Log”.

On Windows, use the --console option to direct messages to the console.

On Unix and Unix-like systems, it is important for the database directories and files to be owned by
the mysql login account so that the server has read and write access to them when you run it later.
To ensure this, start mysqld from the system root account and include the --user option as shown
here:

bin/mysqld --initialize --user=mysql
bin/mysqld --initialize-insecure --user=mysql

Alternatively, execute mysqld while logged in as mysql, in which case you can omit the --user
option from the command.

On Windows, use one of these commands:

bin\mysqld --initialize --console
bin\mysqld --initialize-insecure --console

Note

Data directory initialization might fail if required system libraries are missing. For
example, you might see an error like this:

bin/mysqld: error while loading shared libraries:
libnuma.so.1: cannot open shared object file:
No such file or directory

If this happens, you must install the missing libraries manually or with your
system's package manager. Then retry the data directory initialization
command.

It might be necessary to specify other options such as --basedir or --datadir if mysqld cannot
identify the correct locations for the installation directory or data directory. For example (enter the
command on a single line):

bin/mysqld --initialize --user=mysql
  --basedir=/opt/mysql/mysql
  --datadir=/opt/mysql/mysql/data

Alternatively, put the relevant option settings in an option file and pass the name of that file to mysqld.
For Unix and Unix-like systems, suppose that the option file name is /opt/mysql/mysql/etc/
my.cnf. Put these lines in the file:

[mysqld]
basedir=/opt/mysql/mysql
datadir=/opt/mysql/mysql/data

Then invoke mysqld as follows (enter the command on a single line, with the --defaults-file
option first):

bin/mysqld --defaults-file=/opt/mysql/mysql/etc/my.cnf
  --initialize --user=mysql

On Windows, suppose that C:\my.ini contains these lines:

[mysqld]
basedir=C:\\Program Files\\MySQL\\MySQL Server 8.0
datadir=D:\\MySQLdata

Then invoke mysqld as follows (again, you should enter the command on a single line, with the --
defaults-file option first):

bin\mysqld --defaults-file=C:\my.ini

271

Initializing the Data Directory

   --initialize --console

Important

When initializing the data directory, you should not specify any options other
than those used for setting directory locations such as --basedir or --
datadir, and the --user option if needed. Options to be employed by
the MySQL server during normal use can be set when restarting it following
initialization. See the description of the --initialize option for further
information.

Server Actions During Data Directory Initialization

Note

The data directory initialization sequence performed by the server does not
substitute for the actions performed by mysql_secure_installation and
mysql_ssl_rsa_setup. See Section 6.4.2, “mysql_secure_installation —
Improve MySQL Installation Security”, and Section 6.4.3, “mysql_ssl_rsa_setup
— Create SSL/RSA Files”.

When invoked with the --initialize or --initialize-insecure option, mysqld performs the
following actions during the data directory initialization sequence:

1. The server checks for the existence of the data directory as follows:

• If no data directory exists, the server creates it.

• If the data directory exists but is not empty (that is, it contains files or subdirectories), the server

exits after producing an error message:

[ERROR] --initialize specified but the data directory exists. Aborting.

In this case, remove or rename the data directory and try again.

An existing data directory is permitted to be nonempty if every entry has a name that begins with
a period (.).

2. Within the data directory, the server creates the mysql system schema and its tables, including the
data dictionary tables, grant tables, time zone tables, and server-side help tables. See Section 7.3,
“The mysql System Schema”.

3. The server initializes the system tablespace and related data structures needed to manage InnoDB

tables.

Note

After mysqld sets up the InnoDB system tablespace, certain
changes to tablespace characteristics require setting up a whole
new instance. Qualifying changes include the file name of the first
file in the system tablespace and the number of undo logs. If you
do not want to use the default values, make sure that the settings
for the innodb_data_file_path and innodb_log_file_size
configuration parameters are in place in the MySQL configuration file
before running mysqld. Also make sure to specify as necessary other
parameters that affect the creation and location of InnoDB files, such as
innodb_data_home_dir and innodb_log_group_home_dir.

If those options are in your configuration file but that file is not in a location
that MySQL reads by default, specify the file location using the --
defaults-extra-file option when you run mysqld.

272

Initializing the Data Directory

4. The server creates a 'root'@'localhost' superuser account and other reserved accounts (see
Section 8.2.9, “Reserved Accounts”). Some reserved accounts are locked and cannot be used by
clients, but 'root'@'localhost' is intended for administrative use and you should assign it a
password.

Server actions with respect to a password for the 'root'@'localhost' account depend on how
you invoke it:

• With --initialize but not --initialize-insecure, the server generates a random

password, marks it as expired, and writes a message displaying the password:

[Warning] A temporary password is generated for root@localhost:
iTag*AfrH5ej

• With --initialize-insecure, (either with or without --initialize because --

initialize-insecure implies --initialize), the server does not generate a password or
mark it expired, and writes a warning message:

[Warning] root@localhost is created with an empty password ! Please
consider switching off the --initialize-insecure option.

For instructions on assigning a new 'root'@'localhost' password, see Post-Initialization root
Password Assignment.

5. The server populates the server-side help tables used for the HELP statement (see Section 15.8.3,
“HELP Statement”). The server does not populate the time zone tables. To do so manually, see
Section 7.1.15, “MySQL Server Time Zone Support”.

6.

If the init_file system variable was given to name a file of SQL statements, the server executes
the statements in the file. This option enables you to perform custom bootstrapping sequences.

When the server operates in bootstrap mode, some functionality is unavailable that limits the
statements permitted in the file. These include statements that relate to account management (such
as CREATE USER or GRANT), replication, and global transaction identifiers.

7. The server exits.

Post-Initialization root Password Assignment

After you initialize the data directory by starting the server with --initialize or --initialize-
insecure, start the server normally (that is, without either of those options) and assign the
'root'@'localhost' account a new password:

1. Start the server. For instructions, see Section 2.9.2, “Starting the Server”.

2. Connect to the server:

• If you used --initialize but not --initialize-insecure to initialize the data directory,

connect to the server as root:

mysql -u root -p

Then, at the password prompt, enter the random password that the server generated during the
initialization sequence:

Enter password: (enter the random root password here)

Look in the server error log if you do not know this password.

• If you used --initialize-insecure to initialize the data directory, connect to the server as

root without a password:

mysql -u root --skip-password

273

Starting the Server

3. After connecting, use an ALTER USER statement to assign a new root password:

ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';

See also Section 2.9.4, “Securing the Initial MySQL Account”.

Note

Attempts to connect to the host 127.0.0.1 normally resolve to the localhost
account. However, this fails if the server is run with skip_name_resolve
enabled. If you plan to do that, make sure that an account exists that can
accept a connection. For example, to be able to connect as root using --
host=127.0.0.1 or --host=::1, create these accounts:

CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';

It is possible to put those statements in a file to be executed using the
init_file system variable, as discussed in Server Actions During Data
Directory Initialization.

2.9.2 Starting the Server

This section describes how start the server on Unix and Unix-like systems. (For Windows, see
Section 2.3.4.5, “Starting the Server for the First Time”.) For some suggested commands that you
can use to test whether the server is accessible and working properly, see Section 2.9.3, “Testing the
Server”.

Start the MySQL server like this if your installation includes mysqld_safe:

$> bin/mysqld_safe --user=mysql &

Note

For Linux systems on which MySQL is installed using RPM packages, server
startup and shutdown is managed using systemd rather than mysqld_safe,
and mysqld_safe is not installed. See Section 2.5.9, “Managing MySQL
Server with systemd”.

Start the server like this if your installation includes systemd support:

$> systemctl start mysqld

Substitute the appropriate service name if it differs from mysqld (for example, mysql on SLES
systems).

It is important that the MySQL server be run using an unprivileged (non-root) login account. To ensure
this, run mysqld_safe as root and include the --user option as shown. Otherwise, you should
execute the program while logged in as mysql, in which case you can omit the --user option from the
command.

For further instructions for running MySQL as an unprivileged user, see Section 8.1.5, “How to Run
MySQL as a Normal User”.

If the command fails immediately and prints mysqld ended, look for information in the error log (which
by default is the host_name.err file in the data directory).

If the server is unable to access the data directory it starts or read the grant tables in the mysql
schema, it writes a message to its error log. Such problems can occur if you neglected to create the
grant tables by initializing the data directory before proceeding to this step, or if you ran the command
that initializes the data directory without the --user option. Remove the data directory and run the
command with the --user option.

274

Starting the Server

If you have other problems starting the server, see Section 2.9.2.1, “Troubleshooting Problems Starting
the MySQL Server”. For more information about mysqld_safe, see Section 6.3.2, “mysqld_safe
— MySQL Server Startup Script”. For more information about systemd support, see Section 2.5.9,
“Managing MySQL Server with systemd”.

2.9.2.1 Troubleshooting Problems Starting the MySQL Server

This section provides troubleshooting suggestions for problems starting the server. For additional
suggestions for Windows systems, see Section 2.3.5, “Troubleshooting a Microsoft Windows MySQL
Server Installation”.

If you have problems starting the server, here are some things to try:

• Check the error log to see why the server does not start. Log files are located in the data directory
(typically C:\Program Files\MySQL\MySQL Server 8.0\data on Windows, /usr/local/
mysql/data for a Unix/Linux binary distribution, and /usr/local/var for a Unix/Linux source
distribution). Look in the data directory for files with names of the form host_name.err and
host_name.log, where host_name is the name of your server host. Then examine the last few
lines of these files. Use tail to display them:

$> tail host_name.err
$> tail host_name.log

• Specify any special options needed by the storage engines you are using. You can create a my.cnf
file and specify startup options for the engines that you plan to use. If you are going to use storage
engines that support transactional tables (InnoDB, NDB), be sure that you have them configured the
way you want before starting the server. If you are using InnoDB tables, see Section 17.8, “InnoDB
Configuration” for guidelines and Section 17.14, “InnoDB Startup Options and System Variables” for
option syntax.

Although storage engines use default values for options that you omit, Oracle recommends that
you review the available options and specify explicit values for any options whose defaults are not
appropriate for your installation.

• Make sure that the server knows where to find the data directory. The mysqld server uses this

directory as its current directory. This is where it expects to find databases and where it expects to
write log files. The server also writes the pid (process ID) file in the data directory.

The default data directory location is hardcoded when the server is compiled. To determine what
the default path settings are, invoke mysqld with the --verbose and --help options. If the data
directory is located somewhere else on your system, specify that location with the --datadir option
to mysqld or mysqld_safe, on the command line or in an option file. Otherwise, the server does
not work properly. As an alternative to the --datadir option, you can specify mysqld the location
of the base directory under which MySQL is installed with the --basedir, and mysqld looks for the
data directory there.

To check the effect of specifying path options, invoke mysqld with those options followed by the --
verbose and --help options. For example, if you change location to the directory where mysqld
is installed and then run the following command, it shows the effect of starting the server with a base
directory of /usr/local:

$> ./mysqld --basedir=/usr/local --verbose --help

You can specify other options such as --datadir as well, but --verbose and --help must be
the last options.

Once you determine the path settings you want, start the server without --verbose and --help.

If mysqld is currently running, you can find out what path settings it is using by executing this
command:

$> mysqladmin variables

275

Starting the Server

Or:

$> mysqladmin -h host_name variables

host_name is the name of the MySQL server host.

• Make sure that the server can access the data directory. The ownership and permissions of the data

directory and its contents must allow the server to read and modify them.

If you get Errcode 13 (which means Permission denied) when starting mysqld, this means
that the privileges of the data directory or its contents do not permit server access. In this case, you
change the permissions for the involved files and directories so that the server has the right to use
them. You can also start the server as root, but this raises security issues and should be avoided.

Change location to the data directory and check the ownership of the data directory and its contents
to make sure the server has access. For example, if the data directory is /usr/local/mysql/var,
use this command:

$> ls -la /usr/local/mysql/var

If the data directory or its files or subdirectories are not owned by the login account that you use
for running the server, change their ownership to that account. If the account is named mysql, use
these commands:

$> chown -R mysql /usr/local/mysql/var
$> chgrp -R mysql /usr/local/mysql/var

Even with correct ownership, MySQL might fail to start up if there is other security software running
on your system that manages application access to various parts of the file system. In this case,
reconfigure that software to enable mysqld to access the directories it uses during normal operation.

• Verify that the network interfaces the server wants to use are available.

If either of the following errors occur, it means that some other program (perhaps another mysqld
server) is using the TCP/IP port or Unix socket file that mysqld is trying to use:

Can't start server: Bind on TCP/IP port: Address already in use
Can't start server: Bind on unix socket...

Use ps to determine whether you have another mysqld server running. If so, shut down the server
before starting mysqld again. (If another server is running, and you really want to run multiple
servers, you can find information about how to do so in Section 7.8, “Running Multiple MySQL
Instances on One Machine”.)

If no other server is running, execute the command telnet your_host_name
tcp_ip_port_number. (The default MySQL port number is 3306.) Then press Enter a couple
of times. If you do not get an error message like telnet: Unable to connect to remote
host: Connection refused, some other program is using the TCP/IP port that mysqld is trying
to use. Track down what program this is and disable it, or tell mysqld to listen to a different port with
the --port option. In this case, specify the same non-default port number for client programs when
connecting to the server using TCP/IP.

Another reason the port might be inaccessible is that you have a firewall running that blocks
connections to it. If so, modify the firewall settings to permit access to the port.

If the server starts but you cannot connect to it, make sure that you have an entry in /etc/hosts
that looks like this:

127.0.0.1       localhost

• If you cannot get mysqld to start, try to make a trace file to find the problem by using the --debug

option. See Section 7.9.4, “The DBUG Package”.

276

Testing the Server

2.9.3 Testing the Server

After the data directory is initialized and you have started the server, perform some simple tests to
make sure that it works satisfactorily. This section assumes that your current location is the MySQL
installation directory and that it has a bin subdirectory containing the MySQL programs used here. If
that is not true, adjust the command path names accordingly.

Alternatively, add the bin directory to your PATH environment variable setting. That enables your shell
(command interpreter) to find MySQL programs properly, so that you can run a program by typing only
its name, not its path name. See Section 6.2.9, “Setting Environment Variables”.

Use mysqladmin to verify that the server is running. The following commands provide simple tests to
check whether the server is up and responding to connections:

$> bin/mysqladmin version
$> bin/mysqladmin variables

If you cannot connect to the server, specify a -u root option to connect as root. If you have
assigned a password for the root account already, you'll also need to specify -p on the command line
and enter the password when prompted. For example:

$> bin/mysqladmin -u root -p version
Enter password: (enter root password here)

The output from mysqladmin version varies slightly depending on your platform and version of
MySQL, but should be similar to that shown here:

$> bin/mysqladmin version
mysqladmin  Ver 14.12 Distrib 8.0.42, for pc-linux-gnu on i686
...

Server version          8.0.42
Protocol version        10
Connection              Localhost via UNIX socket
UNIX socket             /var/lib/mysql/mysql.sock
Uptime:                 14 days 5 hours 5 min 21 sec

Threads: 1  Questions: 366  Slow queries: 0
Opens: 0  Flush tables: 1  Open tables: 19
Queries per second avg: 0.000

To see what else you can do with mysqladmin, invoke it with the --help option.

Verify that you can shut down the server (include a -p option if the root account has a password
already):

$> bin/mysqladmin -u root shutdown

Verify that you can start the server again. Do this by using mysqld_safe or by invoking mysqld
directly. For example:

$> bin/mysqld_safe --user=mysql &

If mysqld_safe fails, see Section 2.9.2.1, “Troubleshooting Problems Starting the MySQL Server”.

Run some simple tests to verify that you can retrieve information from the server. The output should be
similar to that shown here.

Use mysqlshow to see what databases exist:

$> bin/mysqlshow
+--------------------+
|     Databases      |
+--------------------+
| information_schema |

277

Securing the Initial MySQL Account

| mysql              |
| performance_schema |
| sys                |
+--------------------+

The list of installed databases may vary, but always includes at least mysql and
information_schema.

If you specify a database name, mysqlshow displays a list of the tables within the database:

$> bin/mysqlshow mysql
Database: mysql
+---------------------------+
|          Tables           |
+---------------------------+
| columns_priv              |
| component                 |
| db                        |
| default_roles             |
| engine_cost               |
| func                      |
| general_log               |
| global_grants             |
| gtid_executed             |
| help_category             |
| help_keyword              |
| help_relation             |
| help_topic                |
| innodb_index_stats        |
| innodb_table_stats        |
| ndb_binlog_index          |
| password_history          |
| plugin                    |
| procs_priv                |
| proxies_priv              |
| role_edges                |
| server_cost               |
| servers                   |
| slave_master_info         |
| slave_relay_log_info      |
| slave_worker_info         |
| slow_log                  |
| tables_priv               |
| time_zone                 |
| time_zone_leap_second     |
| time_zone_name            |
| time_zone_transition      |
| time_zone_transition_type |
| user                      |
+---------------------------+

Use the mysql program to select information from a table in the mysql schema:

$> bin/mysql -e "SELECT User, Host, plugin FROM mysql.user" mysql
+------+-----------+-----------------------+
| User | Host      | plugin                |
+------+-----------+-----------------------+
| root | localhost | caching_sha2_password |
+------+-----------+-----------------------+

At this point, your server is running and you can access it. To tighten security if you have not yet
assigned a password to the initial account, follow the instructions in Section 2.9.4, “Securing the Initial
MySQL Account”.

For more information about mysql, mysqladmin, and mysqlshow, see Section 6.5.1, “mysql —
The MySQL Command-Line Client”, Section 6.5.2, “mysqladmin — A MySQL Server Administration
Program”, and Section 6.5.7, “mysqlshow — Display Database, Table, and Column Information”.

2.9.4 Securing the Initial MySQL Account

278

Securing the Initial MySQL Account

The MySQL installation process involves initializing the data directory, including the grant tables in the
mysql system schema that define MySQL accounts. For details, see Section 2.9.1, “Initializing the
Data Directory”.

This section describes how to assign a password to the initial root account created during the MySQL
installation procedure, if you have not already done so.

Note

Alternative means for performing the process described in this section:

• On Windows, you can perform the process during installation with MySQL

Installer (see Section 2.3.3, “MySQL Installer for Windows”).

• On all platforms, the MySQL distribution includes

mysql_secure_installation, a command-line utility that automates
much of the process of securing a MySQL installation.

• On all platforms, MySQL Workbench is available and offers the ability to

manage user accounts (see Chapter 33, MySQL Workbench ).

A password may already be assigned to the initial account under these circumstances:

• On Windows, installations performed using MySQL Installer give you the option of assigning a

password.

• Installation using the macOS installer generates an initial random password, which the installer

displays to the user in a dialog box.

• Installation using RPM packages generates an initial random password, which is written to the server

error log.

• Installations using Debian packages give you the option of assigning a password.

• For data directory initialization performed manually using mysqld --initialize, mysqld

generates an initial random password, marks it expired, and writes it to the server error log. See
Section 2.9.1, “Initializing the Data Directory”.

The mysql.user grant table defines the initial MySQL user account and its access privileges.
Installation of MySQL creates only a 'root'@'localhost' superuser account that has all privileges
and can do anything. If the root account has an empty password, your MySQL installation is
unprotected: Anyone can connect to the MySQL server as root without a password and be granted all
privileges.

The 'root'@'localhost' account also has a row in the mysql.proxies_priv table that enables
granting the PROXY privilege for ''@'', that is, for all users and all hosts. This enables root to set
up proxy users, as well as to delegate to other accounts the authority to set up proxy users. See
Section 8.2.19, “Proxy Users”.

To assign a password for the initial MySQL root account, use the following procedure. Replace
root-password in the examples with the password that you want to use.

Start the server if it is not running. For instructions, see Section 2.9.2, “Starting the Server”.

The initial root account may or may not have a password. Choose whichever of the following
procedures applies:

• If the root account exists with an initial random password that has been expired, connect to the
server as root using that password, then choose a new password. This is the case if the data
directory was initialized using mysqld --initialize, either manually or using an installer that

279

Starting and Stopping MySQL Automatically

does not give you the option of specifying a password during the install operation. Because the
password exists, you must use it to connect to the server. But because the password is expired, you
cannot use the account for any purpose other than to choose a new password, until you do choose
one.

1.

If you do not know the initial random password, look in the server error log.

2. Connect to the server as root using the password:

$> mysql -u root -p
Enter password: (enter the random root password here)

3. Choose a new password to replace the random password:

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';

• If the root account exists but has no password, connect to the server as root using no password,

then assign a password. This is the case if you initialized the data directory using mysqld --
initialize-insecure.

1. Connect to the server as root using no password:

$> mysql -u root --skip-password

2. Assign a password:

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root-password';

After assigning the root account a password, you must supply that password whenever you connect
to the server using the account. For example, to connect to the server using the mysql client, use this
command:

$> mysql -u root -p
Enter password: (enter root password here)

To shut down the server with mysqladmin, use this command:

$> mysqladmin -u root -p shutdown
Enter password: (enter root password here)

Note

For additional information about setting passwords, see Section 8.2.14,
“Assigning Account Passwords”. If you forget your root password after setting
it, see Section B.3.3.2, “How to Reset the Root Password”.

To set up additional accounts, see Section 8.2.8, “Adding Accounts, Assigning
Privileges, and Dropping Accounts”.

2.9.5 Starting and Stopping MySQL Automatically

This section discusses methods for starting and stopping the MySQL server.

Generally, you start the mysqld server in one of these ways:

• Invoke mysqld directly. This works on any platform.

• On Windows, you can set up a MySQL service that runs automatically when Windows starts. See

Section 2.3.4.8, “Starting MySQL as a Windows Service”.

• On Unix and Unix-like systems, you can invoke mysqld_safe, which tries to determine the proper
options for mysqld and then runs it with those options. See Section 6.3.2, “mysqld_safe — MySQL
Server Startup Script”.

280

Perl Installation Notes

• On Linux systems that support systemd, you can use it to control the server. See Section 2.5.9,

“Managing MySQL Server with systemd”.

• On systems that use System V-style run directories (that is, /etc/init.d and run-level specific

directories), invoke mysql.server. This script is used primarily at system startup and shutdown. It
usually is installed under the name mysql. The mysql.server script starts the server by invoking
mysqld_safe. See Section 6.3.3, “mysql.server — MySQL Server Startup Script”.

• On macOS, install a launchd daemon to enable automatic MySQL startup at system startup. The

daemon starts the server by invoking mysqld_safe. For details, see Section 2.4.3, “Installing and
Using the MySQL Launch Daemon”. A MySQL Preference Pane also provides control for starting
and stopping MySQL through the System Preferences. See Section 2.4.4, “Installing and Using the
MySQL Preference Pane”.

• On Solaris, use the service management framework (SMF) system to initiate and control MySQL

startup.

systemd, the mysqld_safe and mysql.server scripts, Solaris SMF, and the macOS Startup Item
(or MySQL Preference Pane) can be used to start the server manually, or automatically at system
startup time. systemd, mysql.server, and the Startup Item also can be used to stop the server.

The following table shows which option groups the server and startup scripts read from option files.

Table 2.15 MySQL Startup Scripts and Supported Server Option Groups

Script

mysqld

mysqld_safe

mysql.server

Option Groups

[mysqld], [server],
[mysqld-major_version]

[mysqld], [server], [mysqld_safe]

[mysqld], [mysql.server], [server]

[mysqld-major_version] means that groups with names like [mysqld-5.7] and
[mysqld-8.0] are read by servers having versions 5.7.x, 8.0.x, and so forth. This feature can be
used to specify options that can be read only by servers within a given release series.

For backward compatibility, mysql.server also reads the [mysql_server] group and
mysqld_safe also reads the [safe_mysqld] group. To be current, you should update your option
files to use the [mysql.server] and [mysqld_safe] groups instead.

For more information on MySQL configuration files and their structure and contents, see
Section 6.2.2.2, “Using Option Files”.

2.10 Perl Installation Notes

The Perl DBI module provides a generic interface for database access. You can write a DBI script
that works with many different database engines without change. To use DBI, you must install the DBI
module, as well as a DataBase Driver (DBD) module for each type of database server you want to
access. For MySQL, this driver is the DBD::mysql module.

Note

Perl support is not included with MySQL distributions. You can obtain the
necessary modules from http://search.cpan.org for Unix, or by using the
ActiveState ppm program on Windows. The following sections describe how to
do this.

The DBI/DBD interface requires Perl 5.6.0, and 5.6.1 or later is preferred. DBI does not work if you
have an older version of Perl. You should use DBD::mysql 4.009 or higher. Although earlier versions
are available, they do not support the full functionality of MySQL 8.0.

281

Installing Perl on Unix

2.10.1 Installing Perl on Unix

MySQL Perl support requires that you have installed MySQL client programming support (libraries and
header files). Most installation methods install the necessary files. If you install MySQL from RPM files
on Linux, be sure to install the developer RPM as well. The client programs are in the client RPM, but
client programming support is in the developer RPM.

The files you need for Perl support can be obtained from the CPAN (Comprehensive Perl Archive
Network) at http://search.cpan.org.

The easiest way to install Perl modules on Unix is to use the CPAN module. For example:

$> perl -MCPAN -e shell
cpan> install DBI
cpan> install DBD::mysql

The DBD::mysql installation runs a number of tests. These tests attempt to connect to the local
MySQL server using the default user name and password. (The default user name is your login name
on Unix, and ODBC on Windows. The default password is “no password.”) If you cannot connect to
the server with those values (for example, if your account has a password), the tests fail. You can use
force install DBD::mysql to ignore the failed tests.

DBI requires the Data::Dumper module. It may be installed; if not, you should install it before
installing DBI.

It is also possible to download the module distributions in the form of compressed tar archives and
build the modules manually. For example, to unpack and build a DBI distribution, use a procedure such
as this:

1. Unpack the distribution into the current directory:

$> gunzip < DBI-VERSION.tar.gz | tar xvf -

This command creates a directory named DBI-VERSION.

2. Change location into the top-level directory of the unpacked distribution:

$> cd DBI-VERSION

3. Build the distribution and compile everything:

$> perl Makefile.PL
$> make
$> make test
$> make install

The make test command is important because it verifies that the module is working. Note that when
you run that command during the DBD::mysql installation to exercise the interface code, the MySQL
server must be running or the test fails.

It is a good idea to rebuild and reinstall the DBD::mysql distribution whenever you install a new
release of MySQL. This ensures that the latest versions of the MySQL client libraries are installed
correctly.

If you do not have access rights to install Perl modules in the system directory or if you want to install
local Perl modules, the following reference may be useful: http://learn.perl.org/faq/perlfaq8.html#How-
do-I-keep-my-own-module-library-directory-

2.10.2 Installing ActiveState Perl on Windows

On Windows, you should do the following to install the MySQL DBD module with ActiveState Perl:

1. Get ActiveState Perl from http://www.activestate.com/Products/ActivePerl/ and install it.

282

Problems Using the Perl DBI/DBD Interface

2. Open a console window.

3.

If necessary, set the HTTP_proxy variable. For example, you might try a setting like this:

C:\> set HTTP_proxy=my.proxy.com:3128

4. Start the PPM program:

C:\> C:\perl\bin\ppm.pl

5.

If you have not previously done so, install DBI:

ppm> install DBI

6.

If this succeeds, run the following command:

ppm> install DBD-mysql

This procedure should work with ActiveState Perl 5.6 or higher.

If you cannot get the procedure to work, you should install the ODBC driver instead and connect to the
MySQL server through ODBC:

use DBI;
$dbh= DBI->connect("DBI:ODBC:$dsn",$user,$password) ||
  die "Got error $DBI::errstr when connecting to $dsn\n";

2.10.3 Problems Using the Perl DBI/DBD Interface

If Perl reports that it cannot find the ../mysql/mysql.so module, the problem is probably that Perl
cannot locate the libmysqlclient.so shared library. You should be able to fix this problem by one
of the following methods:

• Copy libmysqlclient.so to the directory where your other shared libraries are located (probably

/usr/lib or /lib).

• Modify the -L options used to compile DBD::mysql to reflect the actual location of

libmysqlclient.so.

• On Linux, you can add the path name of the directory where libmysqlclient.so is located to the

/etc/ld.so.conf file.

•     Add the path name of the directory where libmysqlclient.so is located to the LD_RUN_PATH

environment variable. Some systems use LD_LIBRARY_PATH instead.

Note that you may also need to modify the -L options if there are other libraries that the linker fails to
find. For example, if the linker cannot find libc because it is in /lib and the link command specifies -
L/usr/lib, change the -L option to -L/lib or add -L/lib to the existing link command.

If you get the following errors from DBD::mysql, you are probably using gcc (or using an old binary
compiled with gcc):

/usr/bin/perl: can't resolve symbol '__moddi3'
/usr/bin/perl: can't resolve symbol '__divdi3'

Add -L/usr/lib/gcc-lib/... -lgcc to the link command when the mysql.so library gets built
(check the output from make for mysql.so when you compile the Perl client). The -L option should
specify the path name of the directory where libgcc.a is located on your system.

Another cause of this problem may be that Perl and MySQL are not both compiled with gcc. In this
case, you can solve the mismatch by compiling both with gcc.

283

284

