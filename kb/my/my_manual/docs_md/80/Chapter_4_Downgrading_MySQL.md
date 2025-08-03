Chapter 4 Downgrading MySQL

Downgrading from MySQL 8.0 to MySQL 5.7 is not supported.

In-place downgrades are supported from within the MySQL 8.0 series as of MySQL 8.0.35. In-place
means starting and running a new MySQL server binary on an existing MySQL data directory that was
created by a different MySQL server version.

Attempting to downgrade below MySQL 8.0.35 yields an error similar to:

[ERROR] [MY-013171] [InnoDB] Cannot boot server version 80034 on data directory built by version 80035. Downgrade is not supported

Here's a successful log message from an in-place MySQL 8.0.36 to 8.0.35 downgrade:

[System] [MY-014064] [Server] Server downgrade from '80036' to '80035' started.
[System] [MY-014064] [Server] Server downgrade from '80036' to '80035' completed.

An alternative is to restore a backup taken before an upgrade.

327

328

