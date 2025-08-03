Using the sys Schema

Certain Performance Schema instruments and consumers must be enabled and (for instruments) timed
to take full advantage of sys schema capabilities:

• All wait instruments

• All stage instruments

• All statement instruments

• xxx_current and xxx_history_long consumers for all events

You can use the sys schema itself to enable all of the additional instruments and consumers:

CALL sys.ps_setup_enable_instrument('wait');
CALL sys.ps_setup_enable_instrument('stage');
CALL sys.ps_setup_enable_instrument('statement');
CALL sys.ps_setup_enable_consumer('current');
CALL sys.ps_setup_enable_consumer('history_long');

Note

For many uses of the sys schema, the default Performance Schema is
sufficient for data collection. Enabling all the instruments and consumers just
mentioned has a performance impact, so it is preferable to enable only the
additional configuration you need. Also, remember that if you enable additional
configuration, you can easily restore the default configuration like this:

CALL sys.ps_setup_reset_to_default(TRUE);

30.2 Using the sys Schema

You can make the sys schema the default schema so that references to its objects need not be
qualified with the schema name:

mysql> USE sys;
Database changed
mysql> SELECT * FROM version;
+-------------+---------------+
| sys_version | mysql_version |
+-------------+---------------+
| 2.1.1       | 8.4.0-tr      |
+-------------+---------------+

(The version view shows the sys schema and MySQL server versions.)

To access sys schema objects while a different schema is the default (or simply to be explicit), qualify
object references with the schema name:

mysql> SELECT * FROM sys.version;
+-------------+---------------+
| sys_version | mysql_version |
+-------------+---------------+
| 2.1.1       | 8.4.0-tr      |
+-------------+---------------+

The sys schema contains many views that summarize Performance Schema tables in various ways.
Most of these views come in pairs, such that one member of the pair has the same name as the other
member, plus a x$ prefix. For example, the host_summary_by_file_io view summarizes file I/
O grouped by host and displays latencies converted from picoseconds to more readable values (with
units);

mysql> SELECT * FROM sys.host_summary_by_file_io;
+------------+-------+------------+
| host       | ios   | io_latency |
+------------+-------+------------+
| localhost  | 67570 | 5.38 s     |
| background |  3468 | 4.18 s     |

4972

sys Schema Tables and Triggers

Function Name

version_minor()

version_patch()

Description

Deprecated

MySQL server minor version
number

MySQL server patch release
version number

30.4.2 sys Schema Tables and Triggers

The following sections describe sys schema tables and triggers.

30.4.2.1 The sys_config Table

This table contains sys schema configuration options, one row per option. Configuration changes
made by updating this table persist across client sessions and server restarts.

The sys_config table has these columns:

• variable

The configuration option name.

• value

The configuration option value.

• set_time

The timestamp of the most recent modification to the row.

• set_by

The account that made the most recent modification to the row. The value is NULL if the row has not
been changed since the sys schema was installed.

As an efficiency measure to minimize the number of direct reads from the sys_config table,
sys schema functions that use a value from this table check for a user-defined variable with a
corresponding name, which is the user-defined variable having the same name plus a @sys.
prefix. (For example, the variable corresponding to the diagnostics.include_raw option is
@sys.diagnostics.include_raw.) If the user-defined variable exists in the current session
and is non-NULL, the function uses its value in preference to the value in the sys_config table.
Otherwise, the function reads and uses the value from the table. In the latter case, the calling function
conventionally also sets the corresponding user-defined variable to the table value so that further
references to the configuration option within the same session use the variable and need not read the
table again.

For example, the statement_truncate_len option controls the maximum length of statements
returned by the format_statement() function. The default is 64. To temporarily change the value
to 32 for your current session, set the corresponding @sys.statement_truncate_len user-defined
variable:

mysql> SET @stmt = 'SELECT variable, value, set_time, set_by FROM sys_config';
mysql> SELECT sys.format_statement(@stmt);
+----------------------------------------------------------+
| sys.format_statement(@stmt)                              |
+----------------------------------------------------------+
| SELECT variable, value, set_time, set_by FROM sys_config |
+----------------------------------------------------------+
mysql> SET @sys.statement_truncate_len = 32;
mysql> SELECT sys.format_statement(@stmt);
+-----------------------------------+
| sys.format_statement(@stmt)       |
+-----------------------------------+

4979

sys Schema Views

• statement_truncate_len, @sys.statement_truncate_len

The maximum length of statements returned by the format_statement() function. Longer
statements are truncated to this length. The default is 64.

Other options can be added to the sys_config table. For example, the diagnostics() and
execute_prepared_stmt() procedures use the debug option if it exists, but this option is not part
of the sys_config table by default because debug output normally is enabled only temporarily, by
setting the corresponding @sys.debug user-defined variable. To enable debug output without having
to set that variable in individual sessions, add the option to the table:

mysql> INSERT INTO sys.sys_config (variable, value) VALUES('debug', 'ON');

To change the debug setting in the table, do two things. First, modify the value in the table itself:

mysql> UPDATE sys.sys_config
       SET value = 'OFF'
       WHERE variable = 'debug';

Second, to also ensure that procedure invocations within the current session use the changed value
from the table, set the corresponding user-defined variable to NULL:

mysql> SET @sys.debug = NULL;

30.4.2.2 The sys_config_insert_set_user Trigger

For rows added to the sys_config table by INSERT statements, the
sys_config_insert_set_user trigger sets the set_by column to the current user.

30.4.2.3 The sys_config_update_set_user Trigger

The sys_config_update_set_user trigger for the sys_config table is similar to the
sys_config_insert_set_user trigger, but for UPDATE statements.

30.4.3 sys Schema Views

The following sections describe sys schema views.

The sys schema contains many views that summarize Performance Schema tables in various ways.
Most of these views come in pairs, such that one member of the pair has the same name as the other
member, plus a x$ prefix. For example, the host_summary_by_file_io view summarizes file I/
O grouped by host and displays latencies converted from picoseconds to more readable values (with
units);

mysql> SELECT * FROM sys.host_summary_by_file_io;
+------------+-------+------------+
| host       | ios   | io_latency |
+------------+-------+------------+
| localhost  | 67570 | 5.38 s     |
| background |  3468 | 4.18 s     |
+------------+-------+------------+

The x$host_summary_by_file_io view summarizes the same data but displays unformatted
picosecond latencies:

mysql> SELECT * FROM sys.x$host_summary_by_file_io;
+------------+-------+---------------+
| host       | ios   | io_latency    |
+------------+-------+---------------+
| localhost  | 67574 | 5380678125144 |
| background |  3474 | 4758696829416 |
+------------+-------+---------------+

The view without the x$ prefix is intended to provide output that is more user friendly and easier to
read. The view with the x$ prefix that displays the same values in raw form is intended more for use
with other tools that perform their own processing on the data.

4981

sys Schema Views

Views without the x$ prefix differ from the corresponding x$ views in these ways:

• Byte counts are formatted with size units using format_bytes().

• Time values are formatted with temporal units using format_time().

• SQL statements are truncated to a maximum display width using format_statement().

• Path name are shortened using format_path().

30.4.3.1 The host_summary and x$host_summary Views

These views summarize statement activity, file I/O, and connections, grouped by host.

The host_summary and x$host_summary views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• statements

The total number of statements for the host.

• statement_latency

The total wait time of timed statements for the host.

• statement_avg_latency

The average wait time per timed statement for the host.

• table_scans

The total number of table scans for the host.

• file_ios

The total number of file I/O events for the host.

• file_io_latency

The total wait time of timed file I/O events for the host.

• current_connections

The current number of connections for the host.

• total_connections

The total number of connections for the host.

• unique_users

The number of distinct users for the host.

• current_memory

The current amount of allocated memory for the host.

• total_memory_allocated

4982

sys Schema Views

The total amount of allocated memory for the host.

30.4.3.2 The host_summary_by_file_io and x$host_summary_by_file_io Views

These views summarize file I/O, grouped by host. By default, rows are sorted by descending total file I/
O latency.

The host_summary_by_file_io and x$host_summary_by_file_io views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• ios

The total number of file I/O events for the host.

• io_latency

The total wait time of timed file I/O events for the host.

30.4.3.3 The host_summary_by_file_io_type and x$host_summary_by_file_io_type
Views

These views summarize file I/O, grouped by host and event type. By default, rows are sorted by host
and descending total I/O latency.

The host_summary_by_file_io_type and x$host_summary_by_file_io_type views have
these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• event_name

The file I/O event name.

• total

The total number of occurrences of the file I/O event for the host.

• total_latency

The total wait time of timed occurrences of the file I/O event for the host.

• max_latency

The maximum single wait time of timed occurrences of the file I/O event for the host.

30.4.3.4 The host_summary_by_stages and x$host_summary_by_stages Views

These views summarize statement stages, grouped by host. By default, rows are sorted by host and
descending total latency.

The host_summary_by_stages and x$host_summary_by_stages views have these columns:

• host

4983

sys Schema Views

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• event_name

The stage event name.

• total

The total number of occurrences of the stage event for the host.

• total_latency

The total wait time of timed occurrences of the stage event for the host.

• avg_latency

The average wait time per timed occurrence of the stage event for the host.

30.4.3.5 The host_summary_by_statement_latency and x
$host_summary_by_statement_latency Views

These views summarize overall statement statistics, grouped by host. By default, rows are sorted by
descending total latency.

The host_summary_by_statement_latency and x$host_summary_by_statement_latency
views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• total

The total number of statements for the host.

• total_latency

The total wait time of timed statements for the host.

• max_latency

The maximum single wait time of timed statements for the host.

• lock_latency

The total time waiting for locks by timed statements for the host.

• cpu_latency

The time spent on CPU for the current thread.

• rows_sent

The total number of rows returned by statements for the host.

• rows_examined

The total number of rows read from storage engines by statements for the host.

4984

sys Schema Views

• rows_affected

The total number of rows affected by statements for the host.

• full_scans

The total number of full table scans by statements for the host.

30.4.3.6 The host_summary_by_statement_type and x
$host_summary_by_statement_type Views

These views summarize information about statements executed, grouped by host and statement type.
By default, rows are sorted by host and descending total latency.

The host_summary_by_statement_type and x$host_summary_by_statement_type views
have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• statement

The final component of the statement event name.

• total

The total number of occurrences of the statement event for the host.

• total_latency

The total wait time of timed occurrences of the statement event for the host.

• max_latency

The maximum single wait time of timed occurrences of the statement event for the host.

• lock_latency

The total time waiting for locks by timed occurrences of the statement event for the host.

• cpu_latency

The time spent on CPU for the current thread.

• rows_sent

The total number of rows returned by occurrences of the statement event for the host.

• rows_examined

The total number of rows read from storage engines by occurrences of the statement event for the
host.

• rows_affected

The total number of rows affected by occurrences of the statement event for the host.

• full_scans

The total number of full table scans by occurrences of the statement event for the host.

4985

sys Schema Views

The schema name for the object, or InnoDB System if the table belongs to the InnoDB storage
engine.

• object_name

The table name.

• allocated

The total number of bytes allocated for the table.

• data

The number of data bytes allocated for the table.

• pages

The total number of pages allocated for the table.

• pages_hashed

The number of hashed pages allocated for the table.

• pages_old

The number of old pages allocated for the table.

• rows_cached

The number of cached rows for the table.

30.4.3.9 The innodb_lock_waits and x$innodb_lock_waits Views

These views summarize the InnoDB locks that transactions are waiting for. By default, rows are sorted
by descending lock age.

The innodb_lock_waits and x$innodb_lock_waits views have these columns:

• wait_started

The time at which the lock wait started.

• wait_age

How long the lock has been waited for, as a TIME value.

• wait_age_secs

How long the lock has been waited for, in seconds.

• locked_table_schema

The schema that contains the locked table.

• locked_table_name

The name of the locked table.

• locked_table_partition

The name of the locked partition, if any; NULL otherwise.

• locked_table_subpartition

4987

sys Schema Views

• blocking_lock_mode

The mode of the lock that is blocking the waiting lock.

• blocking_trx_started

The time at which the blocking transaction started.

• blocking_trx_age

How long the blocking transaction has been executing, as a TIME value.

• blocking_trx_rows_locked

The number of rows locked by the blocking transaction.

• blocking_trx_rows_modified

The number of rows modified by the blocking transaction.

• sql_kill_blocking_query

The KILL statement to execute to kill the blocking statement.

• sql_kill_blocking_connection

The KILL statement to execute to kill the session running the blocking statement.

30.4.3.10 The io_by_thread_by_latency and x$io_by_thread_by_latency Views

These views summarize I/O consumers to display time waiting for I/O, grouped by thread. By default,
rows are sorted by descending total I/O latency.

The io_by_thread_by_latency and x$io_by_thread_by_latency views have these columns:

• user

For foreground threads, the account associated with the thread. For background threads, the thread
name.

• total

The total number of I/O events for the thread.

• total_latency

The total wait time of timed I/O events for the thread.

• min_latency

The minimum single wait time of timed I/O events for the thread.

• avg_latency

The average wait time per timed I/O event for the thread.

• max_latency

The maximum single wait time of timed I/O events for the thread.

• thread_id

The thread ID.

4989

sys Schema Views

• processlist_id

For foreground threads, the processlist ID of the thread. For background threads, NULL.

30.4.3.11 The io_global_by_file_by_bytes and x$io_global_by_file_by_bytes Views

These views summarize global I/O consumers to display amount of I/O, grouped by file. By default,
rows are sorted by descending total I/O (bytes read and written).

The io_global_by_file_by_bytes and x$io_global_by_file_by_bytes views have these
columns:

• file

The file path name.

• count_read

The total number of read events for the file.

• total_read

The total number of bytes read from the file.

• avg_read

The average number of bytes per read from the file.

• count_write

The total number of write events for the file.

• total_written

The total number of bytes written to the file.

• avg_write

The average number of bytes per write to the file.

• total

The total number of bytes read and written for the file.

• write_pct

The percentage of total bytes of I/O that were writes.

30.4.3.12 The io_global_by_file_by_latency and x$io_global_by_file_by_latency Views

These views summarize global I/O consumers to display time waiting for I/O, grouped by file. By
default, rows are sorted by descending total latency.

The io_global_by_file_by_latency and x$io_global_by_file_by_latency views have
these columns:

• file

The file path name.

• total

The total number of I/O events for the file.

4990

sys Schema Views

• total_latency

The total wait time of timed I/O events for the file.

• count_read

The total number of read I/O events for the file.

• read_latency

The total wait time of timed read I/O events for the file.

• count_write

The total number of write I/O events for the file.

• write_latency

The total wait time of timed write I/O events for the file.

• count_misc

The total number of other I/O events for the file.

• misc_latency

The total wait time of timed other I/O events for the file.

30.4.3.13 The io_global_by_wait_by_bytes and x$io_global_by_wait_by_bytes Views

These views summarize global I/O consumers to display amount of I/O and time waiting for I/O,
grouped by event. By default, rows are sorted by descending total I/O (bytes read and written).

The io_global_by_wait_by_bytes and x$io_global_by_wait_by_bytes views have these
columns:

• event_name

The I/O event name, with the wait/io/file/ prefix stripped.

• total

The total number of occurrences of the I/O event.

• total_latency

The total wait time of timed occurrences of the I/O event.

• min_latency

The minimum single wait time of timed occurrences of the I/O event.

• avg_latency

The average wait time per timed occurrence of the I/O event.

• max_latency

The maximum single wait time of timed occurrences of the I/O event.

• count_read

The number of read requests for the I/O event.

4991

sys Schema Views

• total_read

The number of bytes read for the I/O event.

• avg_read

The average number of bytes per read for the I/O event.

• count_write

The number of write requests for the I/O event.

• total_written

The number of bytes written for the I/O event.

• avg_written

The average number of bytes per write for the I/O event.

• total_requested

The total number of bytes read and written for the I/O event.

30.4.3.14 The io_global_by_wait_by_latency and x$io_global_by_wait_by_latency Views

These views summarize global I/O consumers to display amount of I/O and time waiting for I/O,
grouped by event. By default, rows are sorted by descending total latency.

The io_global_by_wait_by_latency and x$io_global_by_wait_by_latency views have
these columns:

• event_name

The I/O event name, with the wait/io/file/ prefix stripped.

• total

The total number of occurrences of the I/O event.

• total_latency

The total wait time of timed occurrences of the I/O event.

• avg_latency

The average wait time per timed occurrence of the I/O event.

• max_latency

The maximum single wait time of timed occurrences of the I/O event.

• read_latency

The total wait time of timed read occurrences of the I/O event.

• write_latency

The total wait time of timed write occurrences of the I/O event.

• misc_latency

The total wait time of timed other occurrences of the I/O event.

4992

sys Schema Views

• count_read

The number of read requests for the I/O event.

• total_read

The number of bytes read for the I/O event.

• avg_read

The average number of bytes per read for the I/O event.

• count_write

The number of write requests for the I/O event.

• total_written

The number of bytes written for the I/O event.

• avg_written

The average number of bytes per write for the I/O event.

30.4.3.15 The latest_file_io and x$latest_file_io Views

These views summarize file I/O activity, grouped by file and thread. By default, rows are sorted with
most recent I/O first.

The latest_file_io and x$latest_file_io views have these columns:

• thread

For foreground threads, the account associated with the thread (and port number for TCP/IP
connections). For background threads, the thread name and thread ID

• file

The file path name.

• latency

The wait time of the file I/O event.

• operation

The type of operation.

• requested

The number of data bytes requested for the file I/O event.

30.4.3.16 The memory_by_host_by_current_bytes and x
$memory_by_host_by_current_bytes Views

These views summarize memory use, grouped by host. By default, rows are sorted by descending
amount of memory used.

The memory_by_host_by_current_bytes and x$memory_by_host_by_current_bytes views
have these columns:

• host

4993

sys Schema Views

The host from which the client connected. Rows for which the HOST column in the underlying
Performance Schema table is NULL are assumed to be for background threads and are reported with
a host name of background.

• current_count_used

The current number of allocated memory blocks that have not been freed yet for the host.

• current_allocated

The current number of allocated bytes that have not been freed yet for the host.

• current_avg_alloc

The current number of allocated bytes per memory block for the host.

• current_max_alloc

The largest single current memory allocation in bytes for the host.

• total_allocated

The total memory allocation in bytes for the host.

30.4.3.17 The memory_by_thread_by_current_bytes and x
$memory_by_thread_by_current_bytes Views

These views summarize memory use, grouped by thread. By default, rows are sorted by descending
amount of memory used.

The memory_by_thread_by_current_bytes and x$memory_by_thread_by_current_bytes
views have these columns:

• thread_id

The thread ID.

• user

The thread user or thread name.

• current_count_used

The current number of allocated memory blocks that have not been freed yet for the thread.

• current_allocated

The current number of allocated bytes that have not been freed yet for the thread.

• current_avg_alloc

The current number of allocated bytes per memory block for the thread.

• current_max_alloc

The largest single current memory allocation in bytes for the thread.

• total_allocated

The total memory allocation in bytes for the thread.

30.4.3.18 The memory_by_user_by_current_bytes and x
$memory_by_user_by_current_bytes Views

4994

sys Schema Views

These views summarize memory use, grouped by user. By default, rows are sorted by descending
amount of memory used.

The memory_by_user_by_current_bytes and x$memory_by_user_by_current_bytes views
have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

• current_count_used

The current number of allocated memory blocks that have not been freed yet for the user.

• current_allocated

The current number of allocated bytes that have not been freed yet for the user.

• current_avg_alloc

The current number of allocated bytes per memory block for the user.

• current_max_alloc

The largest single current memory allocation in bytes for the user.

• total_allocated

The total memory allocation in bytes for the user.

30.4.3.19 The memory_global_by_current_bytes and x
$memory_global_by_current_bytes Views

These views summarize memory use, grouped by allocation type (that is, by event). By default, rows
are sorted by descending amount of memory used.

The memory_global_by_current_bytes and x$memory_global_by_current_bytes views
have these columns:

• event_name

The memory event name.

• current_count

The total number of occurrences of the event.

• current_alloc

The current number of allocated bytes that have not been freed yet for the event.

• current_avg_alloc

The current number of allocated bytes per memory block for the event.

• high_count

The high-water mark for number of memory blocks allocated for the event.

• high_alloc

4995

sys Schema Views

The high-water mark for number of bytes allocated for the event.

• high_avg_alloc

The high-water mark for average number of bytes per memory block allocated for the event.

30.4.3.20 The memory_global_total and x$memory_global_total Views

These views summarize total memory use within the server.

The memory_global_total and x$memory_global_total views have these columns:

• total_allocated

The total bytes of memory allocated within the server.

30.4.3.21 The metrics View

This view summarizes MySQL server metrics to show variable names, values, types, and whether they
are enabled. By default, rows are sorted by variable type and name.

The metrics view includes this information:

• Global status variables from the Performance Schema global_status table

• InnoDB metrics from the INFORMATION_SCHEMA INNODB_METRICS table

• Current and total memory allocation, based on the Performance Schema memory instrumentation

• The current time (human readable and Unix timestamp formats)

There is some duplication of information between the global_status and INNODB_METRICS tables,
which the metrics view eliminates.

The metrics view has these columns:

• Variable_name

The metric name. The metric type determines the source from which the name is taken:

• For global status variables: The VARIABLE_NAME column of the global_status table

• For InnoDB metrics: The NAME column of the INNODB_METRICS table

• For other metrics: A view-provided descriptive string

• Variable_value

The metric value. The metric type determines the source from which the value is taken:

• For global status variables: The VARIABLE_VALUE column of the global_status table

• For InnoDB metrics: The COUNT column of the INNODB_METRICS table

• For memory metrics: The relevant column from the Performance Schema

memory_summary_global_by_event_name table

• For the current time: The value of NOW(3) or UNIX_TIMESTAMP(NOW(3))

• Type

The metric type:

4996

sys Schema Views

• For global status variables: Global Status

• For InnoDB metrics: InnoDB Metrics - %, where % is replaced by the value of the SUBSYSTEM

column of the INNODB_METRICS table

• For memory metrics: Performance Schema

• For the current time: System Time

• Enabled

Whether the metric is enabled:

• For global status variables: YES

• For InnoDB metrics: YES if the STATUS column of the INNODB_METRICS table is enabled, NO

otherwise

• For memory metrics: NO, YES, or PARTIAL (currently, PARTIAL occurs only for memory metrics
and indicates that not all memory/% instruments are enabled; Performance Schema memory
instruments are always enabled)

• For the current time: YES

30.4.3.22 The processlist and x$processlist Views

The MySQL process list indicates the operations currently being performed by the set of threads
executing within the server. The processlist and x$processlist views summarize process
information. They provide more complete information than the SHOW PROCESSLIST statement and the
INFORMATION_SCHEMA PROCESSLIST table, and are also nonblocking. By default, rows are sorted by
descending process time and descending wait time. For a comparison of process information sources,
see Sources of Process Information.

The column descriptions here are brief. For additional information, see the description of the
Performance Schema threads table at Section 29.12.22.8, “The threads Table”.

The processlist and x$processlist views have these columns:

• thd_id

The thread ID.

• conn_id

The connection ID.

• user

The thread user or thread name.

• db

The default database for the thread, or NULL if there is none.

• command

For foreground threads, the type of command the thread is executing on behalf of the client, or
Sleep if the session is idle.

• state

An action, event, or state that indicates what the thread is doing.

4997

sys Schema Views

• time

The time in seconds that the thread has been in its current state.

• current_statement

The statement the thread is executing, or NULL if it is not executing any statement.

• execution_engine

The query execution engine. The value is either PRIMARY or SECONDARY. For use with HeatWave
Service and HeatWave, where the PRIMARY engine is InnoDB and SECONDARY engine is HeatWave
(RAPID). For MySQL Community Edition Server, MySQL Enterprise Edition Server (on-premise), and
HeatWave Service without HeatWave, the value is always PRIMARY.

• statement_latency

How long the statement has been executing.

• progress

The percentage of work completed for stages that support progress reporting. See Section 30.3, “sys
Schema Progress Reporting”.

• lock_latency

The time spent waiting for locks by the current statement.

• cpu_latency

The time spent on CPU for the current thread.

• rows_examined

The number of rows read from storage engines by the current statement.

• rows_sent

The number of rows returned by the current statement.

• rows_affected

The number of rows affected by the current statement.

• tmp_tables

The number of internal in-memory temporary tables created by the current statement.

• tmp_disk_tables

The number of internal on-disk temporary tables created by the current statement.

• full_scan

The number of full table scans performed by the current statement.

• last_statement

The last statement executed by the thread, if there is no currently executing statement or wait.

• last_statement_latency

How long the last statement executed.

4998

sys Schema Views

• current_memory

The number of bytes allocated by the thread.

• last_wait

The name of the most recent wait event for the thread.

• last_wait_latency

The wait time of the most recent wait event for the thread.

• source

The source file and line number containing the instrumented code that produced the event.

• trx_latency

The wait time of the current transaction for the thread.

• trx_state

The state for the current transaction for the thread.

• trx_autocommit

Whether autocommit mode was enabled when the current transaction started.

• pid

The client process ID.

• program_name

The client program name.

30.4.3.23 The ps_check_lost_instrumentation View

This view returns information about lost Performance Schema instruments, to indicate whether the
Performance Schema is unable to monitor all runtime data.

The ps_check_lost_instrumentation view has these columns:

• variable_name

The Performance Schema status variable name indicating which type of instrument was lost.

• variable_value

The number of instruments lost.

30.4.3.24 The schema_auto_increment_columns View

This view indicates which tables have AUTO_INCREMENT columns and provides information about
those columns, such as the current and maximum column values and the usage ratio (ratio of used to
possible values). By default, rows are sorted by descending usage ratio and maximum column value.

Tables in these schemas are excluded from view output: mysql, sys, INFORMATION_SCHEMA,
performance_schema.

The schema_auto_increment_columns view has these columns:

• table_schema

4999

sys Schema Views

The schema that contains the table.

• table_name

The table that contains the AUTO_INCREMENT column.

• column_name

The name of the AUTO_INCREMENT column.

• data_type

The data type of the column.

• column_type

The column type of the column, which is the data type plus possibly other information. For example,
for a column with a bigint(20) unsigned column type, the data type is just bigint.

• is_signed

Whether the column type is signed.

• is_unsigned

Whether the column type is unsigned.

• max_value

The maximum permitted value for the column.

• auto_increment

The current AUTO_INCREMENT value for the column.

• auto_increment_ratio

The ratio of used to permitted values for the column. This indicates how much of the sequence of
values is “used up.”

30.4.3.25 The schema_index_statistics and x$schema_index_statistics Views

These views provide index statistics. By default, rows are sorted by descending total index latency.

The schema_index_statistics and x$schema_index_statistics views have these columns:

• table_schema

The schema that contains the table.

• table_name

The table that contains the index.

• index_name

The name of the index.

• rows_selected

The total number of rows read using the index.

• select_latency

5000

sys Schema Views

The total wait time of timed reads using the index.

• rows_inserted

The total number of rows inserted into the index.

• insert_latency

The total wait time of timed inserts into the index.

• rows_updated

The total number of rows updated in the index.

• update_latency

The total wait time of timed updates in the index.

• rows_deleted

The total number of rows deleted from the index.

• delete_latency

The total wait time of timed deletes from the index.

30.4.3.26 The schema_object_overview View

This view summarizes the types of objects within each schema. By default, rows are sorted by schema
and object type.

Note

For MySQL instances with a large number of objects, this view might take a
long time to execute.

The schema_object_overview view has these columns:

• db

The schema name.

• object_type

The object type: BASE TABLE, INDEX (index_type), EVENT, FUNCTION, PROCEDURE, TRIGGER,
VIEW.

• count

The number of objects in the schema of the given type.

30.4.3.27 The schema_redundant_indexes and x$schema_flattened_keys Views

The schema_redundant_indexes view displays indexes that duplicate other indexes or
are made redundant by them. The x$schema_flattened_keys view is a helper view for
schema_redundant_indexes.

In the following column descriptions, the dominant index is the one that makes the redundant index
redundant.

The schema_redundant_indexes view has these columns:

• table_schema

5001

sys Schema Views

The schema that contains the table.

• table_name

The table that contains the index.

• redundant_index_name

The name of the redundant index.

• redundant_index_columns

The names of the columns in the redundant index.

• redundant_index_non_unique

The number of nonunique columns in the redundant index.

• dominant_index_name

The name of the dominant index.

• dominant_index_columns

The names of the columns in the dominant index.

• dominant_index_non_unique

The number of nonunique columns in the dominant index.

• subpart_exists

Whether the index indexes only part of a column.

• sql_drop_index

The statement to execute to drop the redundant index.

The x$schema_flattened_keys view has these columns:

• table_schema

The schema that contains the table.

• table_name

The table that contains the index.

• index_name

An index name.

• non_unique

The number of nonunique columns in the index.

• subpart_exists

Whether the index indexes only part of a column.

• index_columns

The name of the columns in the index.

5002

sys Schema Views

30.4.3.28 The schema_table_lock_waits and x$schema_table_lock_waits Views

These views display which sessions are blocked waiting on metadata locks, and what is blocking them.

The column descriptions here are brief. For additional information, see the description of the
Performance Schema metadata_locks table at Section 29.12.13.3, “The metadata_locks Table”.

The schema_table_lock_waits and x$schema_table_lock_waits views have these columns:

• object_schema

The schema containing the object to be locked.

• object_name

The name of the instrumented object.

• waiting_thread_id

The thread ID of the thread that is waiting for the lock.

• waiting_pid

The processlist ID of the thread that is waiting for the lock.

• waiting_account

The account associated with the session that is waiting for the lock.

• waiting_lock_type

The type of the waiting lock.

• waiting_lock_duration

How long the waiting lock has been waiting.

• waiting_query

The statement that is waiting for the lock.

• waiting_query_secs

How long the statement has been waiting, in seconds.

• waiting_query_rows_affected

The number of rows affected by the statement.

• waiting_query_rows_examined

The number of rows read from storage engines by the statement.

• blocking_thread_id

The thread ID of the thread that is blocking the waiting lock.

• blocking_pid

The processlist ID of the thread that is blocking the waiting lock.

• blocking_account

The account associated with the thread that is blocking the waiting lock.

5003

sys Schema Views

• blocking_lock_type

The type of lock that is blocking the waiting lock.

• blocking_lock_duration

How long the blocking lock has been held.

• sql_kill_blocking_query

The KILL statement to execute to kill the blocking statement.

• sql_kill_blocking_connection

The KILL statement to execute to kill the session running the blocking statement.

30.4.3.29 The schema_table_statistics and x$schema_table_statistics Views

These views summarize table statistics. By default, rows are sorted by descending total wait time
(tables with most contention first).

These views user a helper view, x$ps_schema_table_statistics_io.

The schema_table_statistics and x$schema_table_statistics views have these columns:

• table_schema

The schema that contains the table.

• table_name

The table name.

• total_latency

The total wait time of timed I/O events for the table.

• rows_fetched

The total number of rows read from the table.

• fetch_latency

The total wait time of timed read I/O events for the table.

• rows_inserted

The total number of rows inserted into the table.

• insert_latency

The total wait time of timed insert I/O events for the table.

• rows_updated

The total number of rows updated in the table.

• update_latency

The total wait time of timed update I/O events for the table.

• rows_deleted

The total number of rows deleted from the table.

5004

sys Schema Views

• delete_latency

The total wait time of timed delete I/O events for the table.

• io_read_requests

The total number of read requests for the table.

• io_read

The total number of bytes read from the table.

• io_read_latency

The total wait time of reads from the table.

• io_write_requests

The total number of write requests for the table.

• io_write

The total number of bytes written to the table.

• io_write_latency

The total wait time of writes to the table.

• io_misc_requests

The total number of miscellaneous I/O requests for the table.

• io_misc_latency

The total wait time of miscellaneous I/O requests for the table.

30.4.3.30 The schema_table_statistics_with_buffer and x
$schema_table_statistics_with_buffer Views

These views summarize table statistics, including InnoDB buffer pool statistics. By default, rows are
sorted by descending total wait time (tables with most contention first).

These views user a helper view, x$ps_schema_table_statistics_io.

The schema_table_statistics_with_buffer and x
$schema_table_statistics_with_buffer views have these columns:

• table_schema

The schema that contains the table.

• table_name

The table name.

• rows_fetched

The total number of rows read from the table.

• fetch_latency

The total wait time of timed read I/O events for the table.

• rows_inserted

5005

sys Schema Views

The total number of rows inserted into the table.

• insert_latency

The total wait time of timed insert I/O events for the table.

• rows_updated

The total number of rows updated in the table.

• update_latency

The total wait time of timed update I/O events for the table.

• rows_deleted

The total number of rows deleted from the table.

• delete_latency

The total wait time of timed delete I/O events for the table.

• io_read_requests

The total number of read requests for the table.

• io_read

The total number of bytes read from the table.

• io_read_latency

The total wait time of reads from the table.

• io_write_requests

The total number of write requests for the table.

• io_write

The total number of bytes written to the table.

• io_write_latency

The total wait time of writes to the table.

• io_misc_requests

The total number of miscellaneous I/O requests for the table.

• io_misc_latency

The total wait time of miscellaneous I/O requests for the table.

• innodb_buffer_allocated

The total number of InnoDB buffer bytes allocated for the table.

• innodb_buffer_data

The total number of InnoDB data bytes allocated for the table.

• innodb_buffer_free

5006

sys Schema Views

The total number of InnoDB nondata bytes allocated for the table (innodb_buffer_allocated −
innodb_buffer_data).

• innodb_buffer_pages

The total number of InnoDB pages allocated for the table.

• innodb_buffer_pages_hashed

The total number of InnoDB hashed pages allocated for the table.

• innodb_buffer_pages_old

The total number of InnoDB old pages allocated for the table.

• innodb_buffer_rows_cached

The total number of InnoDB cached rows for the table.

30.4.3.31 The schema_tables_with_full_table_scans and x
$schema_tables_with_full_table_scans Views

These views display which tables are being accessed with full table scans. By default, rows are sorted
by descending rows scanned.

The schema_tables_with_full_table_scans and x
$schema_tables_with_full_table_scans views have these columns:

• object_schema

The schema name.

• object_name

The table name.

• rows_full_scanned

The total number of rows scanned by full scans of the table.

• latency

The total wait time of full scans of the table.

30.4.3.32 The schema_unused_indexes View

These views display indexes for which there are no events, which indicates that they are not being
used. By default, rows are sorted by schema and table.

This view is most useful when the server has been up and processing long enough that its workload is
representative. Otherwise, presence of an index in this view may not be meaningful.

The schema_unused_indexes view has these columns:

• object_schema

The schema name.

• object_name

The table name.

5007

sys Schema Views

• index_name

The unused index name.

30.4.3.33 The session and x$session Views

These views are similar to processlist and x$processlist, but they filter out background
processes to display only user sessions. For descriptions of the columns, see Section 30.4.3.22, “The
processlist and x$processlist Views”.

30.4.3.34 The session_ssl_status View

For each connection, this view displays the SSL version, cipher, and count of reused SSL sessions.

The session_ssl_status view has these columns:

• thread_id

The thread ID for the connection.

• ssl_version

The version of SSL used for the connection.

• ssl_cipher

The SSL cipher used for the connection.

• ssl_sessions_reused

The number of reused SSL sessions for the connection.

30.4.3.35 The statement_analysis and x$statement_analysis Views

These views list normalized statements with aggregated statistics. The content mimics the MySQL
Enterprise Monitor Query Analysis view. By default, rows are sorted by descending total latency.

The statement_analysis and x$statement_analysis views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• full_scan

The total number of full table scans performed by occurrences of the statement.

• exec_count

The total number of times the statement has executed.

• err_count

The total number of errors produced by occurrences of the statement.

• warn_count

The total number of warnings produced by occurrences of the statement.

• total_latency

5008

sys Schema Views

The total wait time of timed occurrences of the statement.

• max_latency

The maximum single wait time of timed occurrences of the statement.

• avg_latency

The average wait time per timed occurrence of the statement.

• lock_latency

The total time waiting for locks by timed occurrences of the statement.

• cpu_latency

The time spent on CPU for the current thread.

• rows_sent

The total number of rows returned by occurrences of the statement.

• rows_sent_avg

The average number of rows returned per occurrence of the statement.

• rows_examined

The total number of rows read from storage engines by occurrences of the statement.

• rows_examined_avg

The average number of rows read from storage engines per occurrence of the statement.

• rows_affected

The total number of rows affected by occurrences of the statement.

• rows_affected_avg

The average number of rows affected per occurrence of the statement.

• tmp_tables

The total number of internal in-memory temporary tables created by occurrences of the statement.

• tmp_disk_tables

The total number of internal on-disk temporary tables created by occurrences of the statement.

• rows_sorted

The total number of rows sorted by occurrences of the statement.

• sort_merge_passes

The total number of sort merge passes by occurrences of the statement.

• max_controlled_memory

The maximum amount of controlled memory (bytes) used by the statement.

• max_total_memory

5009

sys Schema Views

The maximum amount of memory (bytes) used by the statement.

• digest

The statement digest.

• first_seen

The time at which the statement was first seen.

• last_seen

The time at which the statement was most recently seen.

30.4.3.36 The statements_with_errors_or_warnings and x
$statements_with_errors_or_warnings Views

These views display normalized statements that have produced errors or warnings. By default, rows
are sorted by descending error and warning counts.

The statements_with_errors_or_warnings and x
$statements_with_errors_or_warnings views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec_count

The total number of times the statement has executed.

• errors

The total number of errors produced by occurrences of the statement.

• error_pct

The percentage of statement occurrences that produced errors.

• warnings

The total number of warnings produced by occurrences of the statement.

• warning_pct

The percentage of statement occurrences that produced warnings.

• first_seen

The time at which the statement was first seen.

• last_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

5010

sys Schema Views

30.4.3.37 The statements_with_full_table_scans and x
$statements_with_full_table_scans Views

These views display normalized statements that have done full table scans. By default, rows are sorted
by descending percentage of time a full scan was done and descending total latency.

The statements_with_full_table_scans and x$statements_with_full_table_scans
views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec_count

The total number of times the statement has executed.

• total_latency

The total wait time of timed statement events for the statement.

• no_index_used_count

The total number of times no index was used to scan the table.

• no_good_index_used_count

The total number of times no good index was used to scan the table.

• no_index_used_pct

The percentage of the time no index was used to scan the table.

• rows_sent

The total number of rows returned from the table.

• rows_examined

The total number of rows read from the storage engine for the table.

• rows_sent_avg

The average number of rows returned from the table.

• rows_examined_avg

The average number of rows read from the storage engine for the table.

• first_seen

The time at which the statement was first seen.

• last_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

5011

sys Schema Views

30.4.3.38 The statements_with_runtimes_in_95th_percentile and x
$statements_with_runtimes_in_95th_percentile Views

These views list statements with runtimes in the 95th percentile. By default, rows are sorted by
descending average latency.

Both views use two helper views, x$ps_digest_avg_latency_distribution and x
$ps_digest_95th_percentile_by_avg_us.

The statements_with_runtimes_in_95th_percentile and x
$statements_with_runtimes_in_95th_percentile views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• full_scan

The total number of full table scans performed by occurrences of the statement.

• exec_count

The total number of times the statement has executed.

• err_count

The total number of errors produced by occurrences of the statement.

• warn_count

The total number of warnings produced by occurrences of the statement.

• total_latency

The total wait time of timed occurrences of the statement.

• max_latency

The maximum single wait time of timed occurrences of the statement.

• avg_latency

The average wait time per timed occurrence of the statement.

• rows_sent

The total number of rows returned by occurrences of the statement.

• rows_sent_avg

The average number of rows returned per occurrence of the statement.

• rows_examined

The total number of rows read from storage engines by occurrences of the statement.

• rows_examined_avg

The average number of rows read from storage engines per occurrence of the statement.

5012

sys Schema Views

• first_seen

The time at which the statement was first seen.

• last_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

30.4.3.39 The statements_with_sorting and x$statements_with_sorting Views

These views list normalized statements that have performed sorts. By default, rows are sorted by
descending total latency.

The statements_with_sorting and x$statements_with_sorting views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec_count

The total number of times the statement has executed.

• total_latency

The total wait time of timed occurrences of the statement.

• sort_merge_passes

The total number of sort merge passes by occurrences of the statement.

• avg_sort_merges

The average number of sort merge passes per occurrence of the statement.

• sorts_using_scans

The total number of sorts using table scans by occurrences of the statement.

• sort_using_range

The total number of sorts using range accesses by occurrences of the statement.

• rows_sorted

The total number of rows sorted by occurrences of the statement.

• avg_rows_sorted

The average number of rows sorted per occurrence of the statement.

• first_seen

The time at which the statement was first seen.

• last_seen

5013

sys Schema Views

The time at which the statement was most recently seen.

• digest

The statement digest.

30.4.3.40 The statements_with_temp_tables and x$statements_with_temp_tables Views

These views list normalized statements that have used temporary tables. By default, rows are sorted
by descending number of on-disk temporary tables used and descending number of in-memory
temporary tables used.

The statements_with_temp_tables and x$statements_with_temp_tables views have
these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec_count

The total number of times the statement has executed.

• total_latency

The total wait time of timed occurrences of the statement.

• memory_tmp_tables

The total number of internal in-memory temporary tables created by occurrences of the statement.

• disk_tmp_tables

The total number of internal on-disk temporary tables created by occurrences of the statement.

• avg_tmp_tables_per_query

The average number of internal temporary tables created per occurrence of the statement.

• tmp_tables_to_disk_pct

The percentage of internal in-memory temporary tables that were converted to on-disk tables.

• first_seen

The time at which the statement was first seen.

• last_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

30.4.3.41 The user_summary and x$user_summary Views

These views summarize statement activity, file I/O, and connections, grouped by user. By default, rows
are sorted by descending total latency.

5014

sys Schema Views

The user_summary and x$user_summary views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

• statements

The total number of statements for the user.

• statement_latency

The total wait time of timed statements for the user.

• statement_avg_latency

The average wait time per timed statement for the user.

• table_scans

The total number of table scans for the user.

• file_ios

The total number of file I/O events for the user.

• file_io_latency

The total wait time of timed file I/O events for the user.

• current_connections

The current number of connections for the user.

• total_connections

The total number of connections for the user.

• unique_hosts

The number of distinct hosts from which connections for the user have originated.

• current_memory

The current amount of allocated memory for the user.

• total_memory_allocated

The total amount of allocated memory for the user.

30.4.3.42 The user_summary_by_file_io and x$user_summary_by_file_io Views

These views summarize file I/O, grouped by user. By default, rows are sorted by descending total file I/
O latency.

The user_summary_by_file_io and x$user_summary_by_file_io views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

5015

sys Schema Views

• ios

The total number of file I/O events for the user.

• io_latency

The total wait time of timed file I/O events for the user.

30.4.3.43 The user_summary_by_file_io_type and x$user_summary_by_file_io_type
Views

These views summarize file I/O, grouped by user and event type. By default, rows are sorted by user
and descending total latency.

The user_summary_by_file_io_type and x$user_summary_by_file_io_type views have
these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

• event_name

The file I/O event name.

• total

The total number of occurrences of the file I/O event for the user.

• latency

The total wait time of timed occurrences of the file I/O event for the user.

• max_latency

The maximum single wait time of timed occurrences of the file I/O event for the user.

30.4.3.44 The user_summary_by_stages and x$user_summary_by_stages Views

These views summarize stages, grouped by user. By default, rows are sorted by user and descending
total stage latency.

The user_summary_by_stages and x$user_summary_by_stages views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

• event_name

The stage event name.

• total

The total number of occurrences of the stage event for the user.

• total_latency

The total wait time of timed occurrences of the stage event for the user.

5016

sys Schema Views

• avg_latency

The average wait time per timed occurrence of the stage event for the user.

30.4.3.45 The user_summary_by_statement_latency and x
$user_summary_by_statement_latency Views

These views summarize overall statement statistics, grouped by user. By default, rows are sorted by
descending total latency.

The user_summary_by_statement_latency and x$user_summary_by_statement_latency
views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

• total

The total number of statements for the user.

• total_latency

The total wait time of timed statements for the user.

• max_latency

The maximum single wait time of timed statements for the user.

• lock_latency

The total time waiting for locks by timed statements for the user.

• cpu_latency

The time spent on CPU for the current thread.

• rows_sent

The total number of rows returned by statements for the user.

• rows_examined

The total number of rows read from storage engines by statements for the user.

• rows_affected

The total number of rows affected by statements for the user.

• full_scans

The total number of full table scans by statements for the user.

30.4.3.46 The user_summary_by_statement_type and x
$user_summary_by_statement_type Views

These views summarize information about statements executed, grouped by user and statement type.
By default, rows are sorted by user and descending total latency.

The user_summary_by_statement_type and x$user_summary_by_statement_type views
have these columns:

5017

sys Schema Views

• user

The client user name. Rows for which the USER column in the underlying Performance Schema
table is NULL are assumed to be for background threads and are reported with a host name of
background.

• statement

The final component of the statement event name.

• total

The total number of occurrences of the statement event for the user.

• total_latency

The total wait time of timed occurrences of the statement event for the user.

• max_latency

The maximum single wait time of timed occurrences of the statement event for the user.

• lock_latency

The total time waiting for locks by timed occurrences of the statement event for the user.

• cpu_latency

The time spent on CPU for the current thread.

• rows_sent

The total number of rows returned by occurrences of the statement event for the user.

• rows_examined

The total number of rows read from storage engines by occurrences of the statement event for the
user.

• rows_affected

The total number of rows affected by occurrences of the statement event for the user.

• full_scans

The total number of full table scans by occurrences of the statement event for the user.

30.4.3.47 The version View

This view provides the current sys schema and MySQL server versions.

Note

This view is deprecated, and subject to removal in a future MySQL version.
Applications that use it should be migrated to use an alternative instead. For
example, use the VERSION() function to retrieve the MySQL server version.

The version view has these columns:

• sys_version

The sys schema version.

• mysql_version

5018

sys Schema Views

The MySQL server version.

30.4.3.48 The wait_classes_global_by_avg_latency and x
$wait_classes_global_by_avg_latency Views

These views summarize wait class average latencies, grouped by event class. By default, rows are
sorted by descending average latency. Idle events are ignored.

An event class is determined by stripping from the event name everything after the first three
components. For example, the class for wait/io/file/sql/slow_log is wait/io/file.

The wait_classes_global_by_avg_latency and x
$wait_classes_global_by_avg_latency views have these columns:

• event_class

The event class.

• total

The total number of occurrences of events in the class.

• total_latency

The total wait time of timed occurrences of events in the class.

• min_latency

The minimum single wait time of timed occurrences of events in the class.

• avg_latency

The average wait time per timed occurrence of events in the class.

• max_latency

The maximum single wait time of timed occurrences of events in the class.

30.4.3.49 The wait_classes_global_by_latency and x$wait_classes_global_by_latency
Views

These views summarize wait class total latencies, grouped by event class. By default, rows are sorted
by descending total latency. Idle events are ignored.

An event class is determined by stripping from the event name everything after the first three
components. For example, the class for wait/io/file/sql/slow_log is wait/io/file.

The wait_classes_global_by_latency and x$wait_classes_global_by_latency views
have these columns:

• event_class

The event class.

• total

The total number of occurrences of events in the class.

• total_latency

The total wait time of timed occurrences of events in the class.

• min_latency

5019

sys Schema Views

The minimum single wait time of timed occurrences of events in the class.

• avg_latency

The average wait time per timed occurrence of events in the class.

• max_latency

The maximum single wait time of timed occurrences of events in the class.

30.4.3.50 The waits_by_host_by_latency and x$waits_by_host_by_latency Views

These views summarize wait events, grouped by host and event. By default, rows are sorted by host
and descending total latency. Idle events are ignored.

The waits_by_host_by_latency and x$waits_by_host_by_latency views have these
columns:

• host

The host from which the connection originated.

• event

The event name.

• total

The total number of occurrences of the event for the host.

• total_latency

The total wait time of timed occurrences of the event for the host.

• avg_latency

The average wait time per timed occurrence of the event for the host.

• max_latency

The maximum single wait time of timed occurrences of the event for the host.

30.4.3.51 The waits_by_user_by_latency and x$waits_by_user_by_latency Views

These views summarize wait events, grouped by user and event. By default, rows are sorted by user
and descending total latency. Idle events are ignored.

The waits_by_user_by_latency and x$waits_by_user_by_latency views have these
columns:

• user

The user associated with the connection.

• event

The event name.

• total

The total number of occurrences of the event for the user.

• total_latency

5020

sys Schema Stored Procedures

The total wait time of timed occurrences of the event for the user.

• avg_latency

The average wait time per timed occurrence of the event for the user.

• max_latency

The maximum single wait time of timed occurrences of the event for the user.

30.4.3.52 The waits_global_by_latency and x$waits_global_by_latency Views

These views summarize wait events, grouped by event. By default, rows are sorted by descending total
latency. Idle events are ignored.

The waits_global_by_latency and x$waits_global_by_latency views have these columns:

• events

The event name.

• total

The total number of occurrences of the event.

• total_latency

The total wait time of timed occurrences of the event.

• avg_latency

The average wait time per timed occurrence of the event.

• max_latency

The maximum single wait time of timed occurrences of the event.

30.4.4 sys Schema Stored Procedures

The following sections describe sys schema stored procedures.

30.4.4.1 The create_synonym_db() Procedure

Given a schema name, this procedure creates a synonym schema containing views that refer to all the
tables and views in the original schema. This can be used, for example, to create a shorter name by
which to refer to a schema with a long name (such as info rather than INFORMATION_SCHEMA).

Parameters

• in_db_name VARCHAR(64): The name of the schema for which to create the synonym.

• in_synonym VARCHAR(64): The name to use for the synonym schema. This schema must not

already exist.

Example

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |

5021

sys Schema Stored Procedures

| world              |
+--------------------+
mysql> CALL sys.create_synonym_db('INFORMATION_SCHEMA', 'info');
+---------------------------------------+
| summary                               |
+---------------------------------------+
| Created 63 views in the info database |
+---------------------------------------+
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| info               |
| mysql              |
| performance_schema |
| sys                |
| world              |
+--------------------+
mysql> SHOW FULL TABLES FROM info;
+---------------------------------------+------------+
| Tables_in_info                        | Table_type |
+---------------------------------------+------------+
| character_sets                        | VIEW       |
| collation_character_set_applicability | VIEW       |
| collations                            | VIEW       |
| column_privileges                     | VIEW       |
| columns                               | VIEW       |
...

30.4.4.2 The diagnostics() Procedure

Creates a report of the current server status for diagnostic purposes.

This procedure disables binary logging during its execution by manipulating the session value of the
sql_log_bin system variable. That is a restricted operation, so the procedure requires privileges
sufficient to set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

Data collected for diagnostics() includes this information:

• Information from the metrics view (see Section 30.4.3.21, “The metrics View”)

• Information from other relevant sys schema views, such as the one that determines queries in the

95th percentile

• Information from the ndbinfo schema, if the MySQL server is part of NDB Cluster

• Replication status (both source and replica)

Some of the sys schema views are calculated as initial (optional), overall, and delta values:

• The initial view is the content of the view at the start of the diagnostics() procedure. This
output is the same as the start values used for the delta view. The initial view is included if the
diagnostics.include_raw configuration option is ON.

• The overall view is the content of the view at the end of the diagnostics() procedure. This output

is the same as the end values used for the delta view. The overall view is always included.

• The delta view is the difference from the beginning to the end of procedure execution. The minimum
and maximum values are the minimum and maximum values from the end view, respectively. They
do not necessarily reflect the minimum and maximum values in the monitored period. Except for the
metrics view, the delta is calculated only between the first and last outputs.

Parameters

• in_max_runtime INT UNSIGNED: The maximum data collection time in seconds. Use NULL to

collect data for the default of 60 seconds. Otherwise, use a value greater than 0.

5022

sys Schema Stored Procedures

• in_interval INT UNSIGNED: The sleep time between data collections in seconds. Use NULL to

sleep for the default of 30 seconds. Otherwise, use a value greater than 0.

• in_auto_config ENUM('current', 'medium', 'full'): The Performance Schema

configuration to use. Permitted values are:

• current: Use the current instrument and consumer settings.

• medium: Enable some instruments and consumers.

• full: Enable all instruments and consumers.

Note

The more instruments and consumers enabled, the more impact on MySQL
server performance. Be careful with the medium setting and especially the
full setting, which has a large performance impact.

Use of the medium or full setting requires the SUPER privilege.

If a setting other than current is chosen, the current settings are restored at the end of the
procedure.

Configuration Options

diagnostics() operation can be modified using the following configuration options or their
corresponding user-defined variables (see Section 30.4.2.1, “The sys_config Table”):

• debug, @sys.debug

If this option is ON, produce debugging output. The default is OFF.

• diagnostics.allow_i_s_tables, @sys.diagnostics.allow_i_s_tables

If this option is ON, the diagnostics() procedure is permitted to perform table scans on the
Information Schema TABLES table. This can be expensive if there are many tables. The default is
OFF.

• diagnostics.include_raw, @sys.diagnostics.include_raw

If this option is ON, the diagnostics() procedure output includes the raw output from querying the
metrics view. The default is OFF.

• statement_truncate_len, @sys.statement_truncate_len

The maximum length of statements returned by the format_statement() function. Longer
statements are truncated to this length. The default is 64.

Example

Create a diagnostics report that starts an iteration every 30 seconds and runs for at most 120 seconds
using the current Performance Schema settings:

mysql> CALL sys.diagnostics(120, 30, 'current');

To capture the output from the diagnostics() procedure in a file as it runs, use the mysql client
tee filename and notee commands (see Section 6.5.1.2, “mysql Client Commands”):

mysql> tee diag.out;
mysql> CALL sys.diagnostics(120, 30, 'current');
mysql> notee;

30.4.4.3 The execute_prepared_stmt() Procedure

5023

sys Schema Stored Procedures

Given an SQL statement as a string, executes it as a prepared statement. The prepared statement
is deallocated after execution, so it is not subject to reuse. Thus, this procedure is useful primarily for
executing dynamic statements on a one-time basis.

This procedure uses sys_execute_prepared_stmt as the prepared statement name. If that
statement name exists when the procedure is called, its previous content is destroyed.

Parameters

• in_query LONGTEXT CHARACTER SET utf8mb3: The statement string to execute.

Configuration Options

execute_prepared_stmt() operation can be modified using the following configuration options or
their corresponding user-defined variables (see Section 30.4.2.1, “The sys_config Table”):

• debug, @sys.debug

If this option is ON, produce debugging output. The default is OFF.

Example

mysql> CALL sys.execute_prepared_stmt('SELECT COUNT(*) FROM mysql.user');
+----------+
| COUNT(*) |
+----------+
|       15 |
+----------+

30.4.4.4 The ps_setup_disable_background_threads() Procedure

Disables Performance Schema instrumentation for all background threads. Produces a result set
indicating how many background threads were disabled. Already disabled threads do not count.

Parameters

None.

Example

mysql> CALL sys.ps_setup_disable_background_threads();
+--------------------------------+
| summary                        |
+--------------------------------+
| Disabled 24 background threads |
+--------------------------------+

30.4.4.5 The ps_setup_disable_consumer() Procedure

Disables Performance Schema consumers with names that contain the argument. Produces a result
set indicating how many consumers were disabled. Already disabled consumers do not count.

Parameters

• consumer VARCHAR(128): The value used to match consumer names, which are identified by

using %consumer% as an operand for a LIKE pattern match.

A value of '' matches all consumers.

Disable all statement consumers:

Example

5024

sys Schema Stored Procedures

mysql> CALL sys.ps_setup_disable_consumer('statement');
+----------------------+
| summary              |
+----------------------+
| Disabled 4 consumers |
+----------------------+

30.4.4.6 The ps_setup_disable_instrument() Procedure

Disables Performance Schema instruments with names that contain the argument. Produces a result
set indicating how many instruments were disabled. Already disabled instruments do not count.

Parameters

• in_pattern VARCHAR(128): The value used to match instrument names, which are identified by

using %in_pattern% as an operand for a LIKE pattern match.

A value of '' matches all instruments.

Example

Disable a specific instrument:

mysql> CALL sys.ps_setup_disable_instrument('wait/lock/metadata/sql/mdl');
+-----------------------+
| summary               |
+-----------------------+
| Disabled 1 instrument |
+-----------------------+

Disable all mutex instruments:

mysql> CALL sys.ps_setup_disable_instrument('mutex');
+--------------------------+
| summary                  |
+--------------------------+
| Disabled 177 instruments |
+--------------------------+

30.4.4.7 The ps_setup_disable_thread() Procedure

Given a connection ID, disables Performance Schema instrumentation for the thread. Produces a result
set indicating how many threads were disabled. Already disabled threads do not count.

Parameters

• in_connection_id BIGINT: The connection ID. This is a value of the type given in the

PROCESSLIST_ID column of the Performance Schema threads table or the Id column of SHOW
PROCESSLIST output.

Example

Disable a specific connection by its connection ID:

mysql> CALL sys.ps_setup_disable_thread(225);
+-------------------+
| summary           |
+-------------------+
| Disabled 1 thread |
+-------------------+

Disable the current connection:

5025

sys Schema Stored Procedures

mysql> CALL sys.ps_setup_disable_thread(CONNECTION_ID());
+-------------------+
| summary           |
+-------------------+
| Disabled 1 thread |
+-------------------+

30.4.4.8 The ps_setup_enable_background_threads() Procedure

Enables Performance Schema instrumentation for all background threads. Produces a result set
indicating how many background threads were enabled. Already enabled threads do not count.

Parameters

None.

Example

mysql> CALL sys.ps_setup_enable_background_threads();
+-------------------------------+
| summary                       |
+-------------------------------+
| Enabled 24 background threads |
+-------------------------------+

30.4.4.9 The ps_setup_enable_consumer() Procedure

Enables Performance Schema consumers with names that contain the argument. Produces a result set
indicating how many consumers were enabled. Already enabled consumers do not count.

Parameters

• consumer VARCHAR(128): The value used to match consumer names, which are identified by

using %consumer% as an operand for a LIKE pattern match.

A value of '' matches all consumers.

Example

Enable all statement consumers:

mysql> CALL sys.ps_setup_enable_consumer('statement');
+---------------------+
| summary             |
+---------------------+
| Enabled 4 consumers |
+---------------------+

30.4.4.10 The ps_setup_enable_instrument() Procedure

Enables Performance Schema instruments with names that contain the argument. Produces a result
set indicating how many instruments were enabled. Already enabled instruments do not count.

Parameters

• in_pattern VARCHAR(128): The value used to match instrument names, which are identified by

using %in_pattern% as an operand for a LIKE pattern match.

A value of '' matches all instruments.

Enable a specific instrument:

Example

5026

sys Schema Stored Procedures

mysql> CALL sys.ps_setup_enable_instrument('wait/lock/metadata/sql/mdl');
+----------------------+
| summary              |
+----------------------+
| Enabled 1 instrument |
+----------------------+

Enable all mutex instruments:

mysql> CALL sys.ps_setup_enable_instrument('mutex');
+-------------------------+
| summary                 |
+-------------------------+
| Enabled 177 instruments |
+-------------------------+

30.4.4.11 The ps_setup_enable_thread() Procedure

Given a connection ID, enables Performance Schema instrumentation for the thread. Produces a result
set indicating how many threads were enabled. Already enabled threads do not count.

Parameters

• in_connection_id BIGINT: The connection ID. This is a value of the type given in the

PROCESSLIST_ID column of the Performance Schema threads table or the Id column of SHOW
PROCESSLIST output.

Example

Enable a specific connection by its connection ID:

mysql> CALL sys.ps_setup_enable_thread(225);
+------------------+
| summary          |
+------------------+
| Enabled 1 thread |
+------------------+

Enable the current connection:

mysql> CALL sys.ps_setup_enable_thread(CONNECTION_ID());
+------------------+
| summary          |
+------------------+
| Enabled 1 thread |
+------------------+

30.4.4.12 The ps_setup_reload_saved() Procedure

Reloads a Performance Schema configuration saved earlier within the same session using
ps_setup_save(). For more information, see the description of ps_setup_save().

This procedure disables binary logging during its execution by manipulating the session value of the
sql_log_bin system variable. That is a restricted operation, so the procedure requires privileges
sufficient to set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

Parameters

None.

30.4.4.13 The ps_setup_reset_to_default() Procedure

Resets the Performance Schema configuration to its default settings.

5027

sys Schema Stored Procedures

Parameters

• in_verbose BOOLEAN: Whether to display information about each setup stage during procedure

execution. This includes the SQL statements executed.

Example

mysql> CALL sys.ps_setup_reset_to_default(TRUE)\G
*************************** 1. row ***************************
status: Resetting: setup_actors
DELETE
FROM performance_schema.setup_actors
WHERE NOT (HOST = '%' AND USER = '%' AND ROLE = '%')

*************************** 1. row ***************************
status: Resetting: setup_actors
INSERT IGNORE INTO performance_schema.setup_actors
VALUES ('%', '%', '%')

...

30.4.4.14 The ps_setup_save() Procedure

Saves the current Performance Schema configuration. This enables you to alter the configuration
temporarily for debugging or other purposes, then restore it to the previous state by invoking the
ps_setup_reload_saved() procedure.

To prevent other simultaneous calls to save the configuration, ps_setup_save() acquires an
advisory lock named sys.ps_setup_save by calling the GET_LOCK() function. ps_setup_save()
takes a timeout parameter to indicate how many seconds to wait if the lock already exists (which
indicates that some other session has a saved configuration outstanding). If the timeout expires without
obtaining the lock, ps_setup_save() fails.

It is intended you call ps_setup_reload_saved() later within the same session as
ps_setup_save() because the configuration is saved in TEMPORARY tables. ps_setup_save()
drops the temporary tables and releases the lock. If you end your session without invoking
ps_setup_save(), the tables and lock disappear automatically.

This procedure disables binary logging during its execution by manipulating the session value of the
sql_log_bin system variable. That is a restricted operation, so the procedure requires privileges
sufficient to set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

Parameters

• in_timeout INT: How many seconds to wait to obtain the sys.ps_setup_save lock. A negative

timeout value means infinite timeout.

Example

mysql> CALL sys.ps_setup_save(10);

... make Performance Schema configuration changes ...

mysql> CALL sys.ps_setup_reload_saved();

30.4.4.15 The ps_setup_show_disabled() Procedure

Displays all currently disabled Performance Schema configuration.

Parameters

• in_show_instruments BOOLEAN: Whether to display disabled instruments. This might be a long

list.

• in_show_threads BOOLEAN: Whether to display disabled threads.

5028

sys Schema Stored Procedures

Example

mysql> CALL sys.ps_setup_show_disabled(TRUE, TRUE);
+----------------------------+
| performance_schema_enabled |
+----------------------------+
|                          1 |
+----------------------------+

+---------------+
| enabled_users |
+---------------+
| '%'@'%'       |
+---------------+

+-------------+----------------------+---------+-------+
| object_type | objects              | enabled | timed |
+-------------+----------------------+---------+-------+
| EVENT       | mysql.%              | NO      | NO    |
| EVENT       | performance_schema.% | NO      | NO    |
| EVENT       | information_schema.% | NO      | NO    |
| FUNCTION    | mysql.%              | NO      | NO    |
| FUNCTION    | performance_schema.% | NO      | NO    |
| FUNCTION    | information_schema.% | NO      | NO    |
| PROCEDURE   | mysql.%              | NO      | NO    |
| PROCEDURE   | performance_schema.% | NO      | NO    |
| PROCEDURE   | information_schema.% | NO      | NO    |
| TABLE       | mysql.%              | NO      | NO    |
| TABLE       | performance_schema.% | NO      | NO    |
| TABLE       | information_schema.% | NO      | NO    |
| TRIGGER     | mysql.%              | NO      | NO    |
| TRIGGER     | performance_schema.% | NO      | NO    |
| TRIGGER     | information_schema.% | NO      | NO    |
+-------------+----------------------+---------+-------+

...

30.4.4.16 The ps_setup_show_disabled_consumers() Procedure

Displays all currently disabled Performance Schema consumers.

Parameters

None.

Example

mysql> CALL sys.ps_setup_show_disabled_consumers();
+----------------------------------+
| disabled_consumers               |
+----------------------------------+
| events_stages_current            |
| events_stages_history            |
| events_stages_history_long       |
| events_statements_history        |
| events_statements_history_long   |
| events_transactions_history      |
| events_transactions_history_long |
| events_waits_current             |
| events_waits_history             |
| events_waits_history_long        |
+----------------------------------+

30.4.4.17 The ps_setup_show_disabled_instruments() Procedure

Displays all currently disabled Performance Schema instruments. This might be a long list.

Parameters

None.

5029

sys Schema Stored Procedures

Example

mysql> CALL sys.ps_setup_show_disabled_instruments()\G
*************************** 1. row ***************************
disabled_instruments: wait/synch/mutex/sql/TC_LOG_MMAP::LOCK_tc
               timed: NO
*************************** 2. row ***************************
disabled_instruments: wait/synch/mutex/sql/THD::LOCK_query_plan
               timed: NO
*************************** 3. row ***************************
disabled_instruments: wait/synch/mutex/sql/MYSQL_BIN_LOG::LOCK_commit
               timed: NO
...

30.4.4.18 The ps_setup_show_enabled() Procedure

Displays all currently enabled Performance Schema configuration.

Parameters

• in_show_instruments BOOLEAN: Whether to display enabled instruments. This might be a long

list.

• in_show_threads BOOLEAN: Whether to display enabled threads.

Example

mysql> CALL sys.ps_setup_show_enabled(FALSE, FALSE);
+----------------------------+
| performance_schema_enabled |
+----------------------------+
|                          1 |
+----------------------------+
1 row in set (0.01 sec)

+---------------+
| enabled_users |
+---------------+
| '%'@'%'       |
+---------------+
1 row in set (0.01 sec)

+-------------+---------+---------+-------+
| object_type | objects | enabled | timed |
+-------------+---------+---------+-------+
| EVENT       | %.%     | YES     | YES   |
| FUNCTION    | %.%     | YES     | YES   |
| PROCEDURE   | %.%     | YES     | YES   |
| TABLE       | %.%     | YES     | YES   |
| TRIGGER     | %.%     | YES     | YES   |
+-------------+---------+---------+-------+
5 rows in set (0.02 sec)

+-----------------------------+
| enabled_consumers           |
+-----------------------------+
| events_statements_current   |
| events_statements_history   |
| events_transactions_current |
| events_transactions_history |
| global_instrumentation      |
| statements_digest           |
| thread_instrumentation      |
+-----------------------------+

30.4.4.19 The ps_setup_show_enabled_consumers() Procedure

Displays all currently enabled Performance Schema consumers.

5030

sys Schema Stored Procedures

Parameters

None.

Example

mysql> CALL sys.ps_setup_show_enabled_consumers();
+-----------------------------+
| enabled_consumers           |
+-----------------------------+
| events_statements_current   |
| events_statements_history   |
| events_transactions_current |
| events_transactions_history |
| global_instrumentation      |
| statements_digest           |
| thread_instrumentation      |
+-----------------------------+

30.4.4.20 The ps_setup_show_enabled_instruments() Procedure

Displays all currently enabled Performance Schema instruments. This might be a long list.

Parameters

None.

Example

mysql> CALL sys.ps_setup_show_enabled_instruments()\G
*************************** 1. row ***************************
enabled_instruments: wait/io/file/sql/map
              timed: YES
*************************** 2. row ***************************
enabled_instruments: wait/io/file/sql/binlog
              timed: YES
*************************** 3. row ***************************
enabled_instruments: wait/io/file/sql/binlog_cache
              timed: YES
...

30.4.4.21 The ps_statement_avg_latency_histogram() Procedure

Displays a textual histogram graph of the average latency values across all normalized statements
tracked within the Performance Schema events_statements_summary_by_digest table.

This procedure can be used to display a very high-level picture of the latency distribution of statements
running within this MySQL instance.

Parameters

None.

Example

The histogram output in statement units. For example, * = 2 units in the histogram legend means
that each * character represents 2 statements.

mysql> CALL sys.ps_statement_avg_latency_histogram()\G
*************************** 1. row ***************************
Performance Schema Statement Digest Average Latency Histogram:

  . = 1 unit
  * = 2 units
  # = 3 units

5031

sys Schema Stored Procedures

(0 - 66ms)     88  | #############################
(66 - 133ms)   14  | ..............
(133 - 199ms)  4   | ....
(199 - 265ms)  5   | **
(265 - 332ms)  1   | .
(332 - 398ms)  0   |
(398 - 464ms)  1   | .
(464 - 531ms)  0   |
(531 - 597ms)  0   |
(597 - 663ms)  0   |
(663 - 730ms)  0   |
(730 - 796ms)  0   |
(796 - 863ms)  0   |
(863 - 929ms)  0   |
(929 - 995ms)  0   |
(995 - 1062ms) 0   |

  Total Statements: 114; Buckets: 16; Bucket Size: 66 ms;

30.4.4.22 The ps_trace_statement_digest() Procedure

Traces all Performance Schema instrumentation for a specific statement digest.

If you find a statement of interest within the Performance Schema
events_statements_summary_by_digest table, specify its DIGEST column MD5 value to this
procedure and indicate the polling duration and interval. The result is a report of all statistics tracked
within Performance Schema for that digest for the interval.

The procedure also attempts to execute EXPLAIN for the longest running example of the digest during
the interval. This attempt might fail because the Performance Schema truncates long SQL_TEXT
values. Consequently, EXPLAIN fails, due to parse errors.

This procedure disables binary logging during its execution by manipulating the session value of the
sql_log_bin system variable. That is a restricted operation, so the procedure requires privileges
sufficient to set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

Parameters

• in_digest VARCHAR(32): The statement digest identifier to analyze.

• in_runtime INT: How long to run the analysis in seconds.

• in_interval DECIMAL(2,2): The analysis interval in seconds (which can be fractional) at which

to try to take snapshots.

• in_start_fresh BOOLEAN: Whether to truncate the Performance Schema

events_statements_history_long and events_stages_history_long tables before
starting.

• in_auto_enable BOOLEAN: Whether to automatically enable required consumers.

Example

5032

mysql> CALL sys.ps_trace_statement_digest('891ec6860f98ba46d89dd20b0c03652c', 10, 0.1, TRUE, TRUE);
+--------------------+
| SUMMARY STATISTICS |
+--------------------+
| SUMMARY STATISTICS |
+--------------------+
1 row in set (9.11 sec)

+------------+-----------+-----------+-----------+---------------+------------+------------+
| executions | exec_time | lock_time | rows_sent | rows_examined | tmp_tables | full_scans |
+------------+-----------+-----------+-----------+---------------+------------+------------+
|         21 | 4.11 ms   | 2.00 ms   |         0 |            21 |          0 |          0 |

sys Schema Stored Procedures

+------------+-----------+-----------+-----------+---------------+------------+------------+
1 row in set (9.11 sec)

+------------------------------------------+-------+-----------+
| event_name                               | count | latency   |
+------------------------------------------+-------+-----------+
| stage/sql/statistics                     |    16 | 546.92 us |
| stage/sql/freeing items                  |    18 | 520.11 us |
| stage/sql/init                           |    51 | 466.80 us |
...
| stage/sql/cleaning up                    |    18 | 11.92 us  |
| stage/sql/executing                      |    16 | 6.95 us   |
+------------------------------------------+-------+-----------+
17 rows in set (9.12 sec)

+---------------------------+
| LONGEST RUNNING STATEMENT |
+---------------------------+
| LONGEST RUNNING STATEMENT |
+---------------------------+
1 row in set (9.16 sec)

+-----------+-----------+-----------+-----------+---------------+------------+-----------+
| thread_id | exec_time | lock_time | rows_sent | rows_examined | tmp_tables | full_scan |
+-----------+-----------+-----------+-----------+---------------+------------+-----------+
|    166646 | 618.43 us | 1.00 ms   |         0 |             1 |          0 |         0 |
+-----------+-----------+-----------+-----------+---------------+------------+-----------+
1 row in set (9.16 sec)

# Truncated for clarity...
+-----------------------------------------------------------------+
| sql_text                                                        |
+-----------------------------------------------------------------+
| select hibeventhe0_.id as id1382_, hibeventhe0_.createdTime ... |
+-----------------------------------------------------------------+
1 row in set (9.17 sec)

+------------------------------------------+-----------+
| event_name                               | latency   |
+------------------------------------------+-----------+
| stage/sql/init                           | 8.61 us   |
| stage/sql/init                           | 331.07 ns |
...
| stage/sql/freeing items                  | 30.46 us  |
| stage/sql/cleaning up                    | 662.13 ns |
+------------------------------------------+-----------+
18 rows in set (9.23 sec)

+----+-------------+--------------+-------+---------------+-----------+---------+-------------+------+-------+
| id | select_type | table        | type  | possible_keys | key       | key_len | ref         | rows | Extra |
+----+-------------+--------------+-------+---------------+-----------+---------+-------------+------+-------+
|  1 | SIMPLE      | hibeventhe0_ | const | fixedTime     | fixedTime | 775     | const,const |    1 | NULL  |
+----+-------------+--------------+-------+---------------+-----------+---------+-------------+------+-------+
1 row in set (9.27 sec)

Query OK, 0 rows affected (9.28 sec)

30.4.4.23 The ps_trace_thread() Procedure

Dumps all Performance Schema data for an instrumented thread to a .dot formatted graph file (for the
DOT graph description language). Each result set returned from the procedure should be used for a
complete graph.

This procedure disables binary logging during its execution by manipulating the session value of the
sql_log_bin system variable. That is a restricted operation, so the procedure requires privileges
sufficient to set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

Parameters

• in_thread_id INT: The thread to trace.

5033

sys Schema Stored Procedures

• in_outfile VARCHAR(255): The name to use for the .dot output file.

• in_max_runtime DECIMAL(20,2): The maximum number of seconds (which can be fractional) to

collect data. Use NULL to collect data for the default of 60 seconds.

• in_interval DECIMAL(20,2): The number of seconds (which can be fractional) to sleep

between data collections. Use NULL to sleep for the default of 1 second.

• in_start_fresh BOOLEAN: Whether to reset all Performance Schema data before tracing.

• in_auto_setup BOOLEAN: Whether to disable all other threads and enable all instruments and

consumers. This also resets the settings at the end of the run.

• in_debug BOOLEAN: Whether to include file:lineno information in the graph.

Example

mysql> CALL sys.ps_trace_thread(25, CONCAT('/tmp/stack-', REPLACE(NOW(), ' ', '-'), '.dot'), NULL, NULL, TRUE, TRUE, TRUE);
+-------------------+
| summary           |
+-------------------+
| Disabled 1 thread |
+-------------------+
1 row in set (0.00 sec)

+---------------------------------------------+
| Info                                        |
+---------------------------------------------+
| Data collection starting for THREAD_ID = 25 |
+---------------------------------------------+
1 row in set (0.03 sec)

+-----------------------------------------------------------+
| Info                                                      |
+-----------------------------------------------------------+
| Stack trace written to /tmp/stack-2014-02-16-21:18:41.dot |
+-----------------------------------------------------------+
1 row in set (60.07 sec)

+-------------------------------------------------------------------+
| Convert to PDF                                                    |
+-------------------------------------------------------------------+
| dot -Tpdf -o /tmp/stack_25.pdf /tmp/stack-2014-02-16-21:18:41.dot |
+-------------------------------------------------------------------+
1 row in set (60.07 sec)

+-------------------------------------------------------------------+
| Convert to PNG                                                    |
+-------------------------------------------------------------------+
| dot -Tpng -o /tmp/stack_25.png /tmp/stack-2014-02-16-21:18:41.dot |
+-------------------------------------------------------------------+
1 row in set (60.07 sec)

+------------------+
| summary          |
+------------------+
| Enabled 1 thread |
+------------------+
1 row in set (60.32 sec)

30.4.4.24 The ps_truncate_all_tables() Procedure

Truncates all Performance Schema summary tables, resetting all aggregated instrumentation as a
snapshot. Produces a result set indicating how many tables were truncated.

Parameters

• in_verbose BOOLEAN: Whether to display each TRUNCATE TABLE statement before executing it.

5034

sys Schema Stored Procedures

Example

mysql> CALL sys.ps_truncate_all_tables(FALSE);
+---------------------+
| summary             |
+---------------------+
| Truncated 49 tables |
+---------------------+

30.4.4.25 The statement_performance_analyzer() Procedure

Creates a report of the statements running on the server. The views are calculated based on the
overall and/or delta activity.

This procedure disables binary logging during its execution by manipulating the session value of the
sql_log_bin system variable. That is a restricted operation, so the procedure requires privileges
sufficient to set restricted session variables. See Section 7.1.9.1, “System Variable Privileges”.

Parameters

• in_action ENUM('snapshot', 'overall', 'delta', 'create_tmp',

'create_table', 'save', 'cleanup'): The action to take. These values are permitted:

• snapshot: Store a snapshot. The default is to make a snapshot of the current content of the

Performance Schema events_statements_summary_by_digest table. By setting in_table,
this can be overwritten to copy the content of the specified table. The snapshot is stored in the sys
schema tmp_digests temporary table.

• overall: Generate an analysis based on the content of the table specified by in_table.
For the overall analysis, in_table can be NOW() to use a fresh snapshot. This overwrites
an existing snapshot. Use NULL for in_table to use the existing snapshot. If in_table is
NULL and no snapshot exists, a new snapshot is created. The in_views parameter and the
statement_performance_analyzer.limit configuration option affect the operation of this
procedure.

• delta: Generate a delta analysis. The delta is calculated between the reference table
specified by in_table and the snapshot, which must exist. This action uses the sys
schema tmp_digests_delta temporary table. The in_views parameter and the
statement_performance_analyzer.limit configuration option affect the operation of this
procedure.

• create_table: Create a regular table suitable for storing the snapshot for later use (for example,

for calculating deltas).

• create_tmp: Create a temporary table suitable for storing the snapshot for later use (for

example, for calculating deltas).

• save: Save the snapshot in the table specified by in_table. The table must exist and have the

correct structure. If no snapshot exists, a new snapshot is created.

• cleanup: Remove the temporary tables used for the snapshot and delta.

• in_table VARCHAR(129): The table parameter used for some of the actions specified by the
in_action parameter. Use the format db_name.tbl_name or tbl_name without using any
backtick (`) identifier-quoting characters. Periods (.) are not supported in database and table
names.

The meaning of the in_table value for each in_action value is detailed in the individual
in_action value descriptions.

• in_views SET ('with_runtimes_in_95th_percentile', 'analysis',

'with_errors_or_warnings', 'with_full_table_scans', 'with_sorting',

5035

sys Schema Stored Procedures

'with_temp_tables', 'custom'): Which views to include. This parameter is a SET value, so
it can contain multiple view names, separated by commas. The default is to include all views except
custom. The following values are permitted:

• with_runtimes_in_95th_percentile: Use the

statements_with_runtimes_in_95th_percentile view.

• analysis: Use the statement_analysis view.

• with_errors_or_warnings: Use the statements_with_errors_or_warnings view.

• with_full_table_scans: Use the statements_with_full_table_scans view.

• with_sorting: Use the statements_with_sorting view.

• with_temp_tables: Use the statements_with_temp_tables view.

• custom: Use a custom view. This view must be specified using the

statement_performance_analyzer.view configuration option to name a query or an
existing view.

Configuration Options

statement_performance_analyzer() operation can be modified using the following configuration
options or their corresponding user-defined variables (see Section 30.4.2.1, “The sys_config Table”):

• debug, @sys.debug

If this option is ON, produce debugging output. The default is OFF.

• statement_performance_analyzer.limit,

@sys.statement_performance_analyzer.limit

The maximum number of rows to return for views that have no built-in limit. The default is 100.

• statement_performance_analyzer.view,

@sys.statement_performance_analyzer.view

The custom query or view to be used. If the option value contains a space, it is interpreted as a
query. Otherwise, it must be the name of an existing view that queries the Performance Schema
events_statements_summary_by_digest table. There cannot be any LIMIT clause in the
query or view definition if the statement_performance_analyzer.limit configuration option
is greater than 0. If specifying a view, use the same format as for the in_table parameter. The
default is NULL (no custom view defined).

Example

To create a report with the queries in the 95th percentile since the last truncation of
events_statements_summary_by_digest and with a one-minute delta period:

1. Create a temporary table to store the initial snapshot.

2. Create the initial snapshot.

3. Save the initial snapshot in the temporary table.

4. Wait one minute.

5. Create a new snapshot.

6. Perform analysis based on the new snapshot.

7. Perform analysis based on the delta between the initial and new snapshots.

5036

sys Schema Stored Procedures

mysql> CALL sys.statement_performance_analyzer('create_tmp', 'mydb.tmp_digests_ini', NULL);
Query OK, 0 rows affected (0.08 sec)

mysql> CALL sys.statement_performance_analyzer('snapshot', NULL, NULL);
Query OK, 0 rows affected (0.02 sec)

mysql> CALL sys.statement_performance_analyzer('save', 'mydb.tmp_digests_ini', NULL);
Query OK, 0 rows affected (0.00 sec)

mysql> DO SLEEP(60);
Query OK, 0 rows affected (1 min 0.00 sec)

mysql> CALL sys.statement_performance_analyzer('snapshot', NULL, NULL);
Query OK, 0 rows affected (0.02 sec)

mysql> CALL sys.statement_performance_analyzer('overall', NULL, 'with_runtimes_in_95th_percentile');
+-----------------------------------------+
| Next Output                             |
+-----------------------------------------+
| Queries with Runtime in 95th Percentile |
+-----------------------------------------+
1 row in set (0.05 sec)

...

mysql> CALL sys.statement_performance_analyzer('delta', 'mydb.tmp_digests_ini', 'with_runtimes_in_95th_percentile');
+-----------------------------------------+
| Next Output                             |
+-----------------------------------------+
| Queries with Runtime in 95th Percentile |
+-----------------------------------------+
1 row in set (0.03 sec)

...

Create an overall report of the 95th percentile queries and the top 10 queries with full table scans:

mysql> CALL sys.statement_performance_analyzer('snapshot', NULL, NULL);
Query OK, 0 rows affected (0.01 sec)

mysql> SET @sys.statement_performance_analyzer.limit = 10;
Query OK, 0 rows affected (0.00 sec)

mysql> CALL sys.statement_performance_analyzer('overall', NULL, 'with_runtimes_in_95th_percentile,with_full_table_scans');
+-----------------------------------------+
| Next Output                             |
+-----------------------------------------+
| Queries with Runtime in 95th Percentile |
+-----------------------------------------+
1 row in set (0.01 sec)

...

+-------------------------------------+
| Next Output                         |
+-------------------------------------+
| Top 10 Queries with Full Table Scan |
+-------------------------------------+
1 row in set (0.09 sec)

...

Use a custom view showing the top 10 queries sorted by total execution time, refreshing the view every
minute using the watch command in Linux:

mysql> CREATE OR REPLACE VIEW mydb.my_statements AS
       SELECT sys.format_statement(DIGEST_TEXT) AS query,
              SCHEMA_NAME AS db,
              COUNT_STAR AS exec_count,
              sys.format_time(SUM_TIMER_WAIT) AS total_latency,
              sys.format_time(AVG_TIMER_WAIT) AS avg_latency,
              ROUND(IFNULL(SUM_ROWS_SENT / NULLIF(COUNT_STAR, 0), 0)) AS rows_sent_avg,

5037

sys Schema Stored Procedures

              ROUND(IFNULL(SUM_ROWS_EXAMINED / NULLIF(COUNT_STAR, 0), 0)) AS rows_examined_avg,
              ROUND(IFNULL(SUM_ROWS_AFFECTED / NULLIF(COUNT_STAR, 0), 0)) AS rows_affected_avg,
              DIGEST AS digest
         FROM performance_schema.events_statements_summary_by_digest
       ORDER BY SUM_TIMER_WAIT DESC;
Query OK, 0 rows affected (0.10 sec)

mysql> CALL sys.statement_performance_analyzer('create_table', 'mydb.digests_prev', NULL);
Query OK, 0 rows affected (0.10 sec)

$> watch -n 60 "mysql sys --table -e \"
> SET @sys.statement_performance_analyzer.view = 'mydb.my_statements';
> SET @sys.statement_performance_analyzer.limit = 10;
> CALL statement_performance_analyzer('snapshot', NULL, NULL);
> CALL statement_performance_analyzer('delta', 'mydb.digests_prev', 'custom');
> CALL statement_performance_analyzer('save', 'mydb.digests_prev', NULL);
> \""

Every 60.0s: mysql sys --table -e "        ...  Mon Dec 22 10:58:51 2014

+----------------------------------+
| Next Output                      |
+----------------------------------+
| Top 10 Queries Using Custom View |
+----------------------------------+
+-------------------+-------+------------+---------------+-------------+---------------+-------------------+-------------------+----------------------------------+
| query             | db    | exec_count | total_latency | avg_latency | rows_sent_avg | rows_examined_avg | rows_affected_avg | digest                           |
+-------------------+-------+------------+---------------+-------------+---------------+-------------------+-------------------+----------------------------------+
...

30.4.4.26 The table_exists() Procedure

Tests whether a given table exists as a regular table, a TEMPORARY table, or a view. The procedure
returns the table type in an OUT parameter. If both a temporary and a permanent table exist with the
given name, TEMPORARY is returned.

Parameters

• in_db VARCHAR(64): The name of the database in which to check for table existence.

• in_table VARCHAR(64): The name of the table to check the existence of.

• out_exists ENUM('', 'BASE TABLE', 'VIEW', 'TEMPORARY'): The return value. This
is an OUT parameter, so it must be a variable into which the table type can be stored. When the
procedure returns, the variable has one of the following values to indicate whether the table exists:

• '': The table name does not exist as a base table, TEMPORARY table, or view.

• BASE TABLE: The table name exists as a base (permanent) table.

• VIEW: The table name exists as a view.

• TEMPORARY: The table name exists as a TEMPORARY table.

Example

5038

mysql> CREATE DATABASE db1;
Query OK, 1 row affected (0.01 sec)

mysql> USE db1;
Database changed

mysql> CREATE TABLE t1 (id INT PRIMARY KEY);
Query OK, 0 rows affected (0.03 sec)

mysql> CREATE TABLE t2 (id INT PRIMARY KEY);
Query OK, 0 rows affected (0.20 sec)

sys Schema Stored Functions

mysql> CREATE view v_t1 AS SELECT * FROM t1;
Query OK, 0 rows affected (0.02 sec)

mysql> CREATE TEMPORARY TABLE t1 (id INT PRIMARY KEY);
Query OK, 0 rows affected (0.00 sec)

mysql> CALL sys.table_exists('db1', 't1', @exists); SELECT @exists;
Query OK, 0 rows affected (0.01 sec)

+-----------+
| @exists   |
+-----------+
| TEMPORARY |
+-----------+
1 row in set (0.00 sec)

mysql> CALL sys.table_exists('db1', 't2', @exists); SELECT @exists;
Query OK, 0 rows affected (0.02 sec)

+------------+
| @exists    |
+------------+
| BASE TABLE |
+------------+
1 row in set (0.00 sec)

mysql> CALL sys.table_exists('db1', 'v_t1', @exists); SELECT @exists;
Query OK, 0 rows affected (0.02 sec)

+---------+
| @exists |
+---------+
| VIEW    |
+---------+
1 row in set (0.00 sec)

mysql> CALL sys.table_exists('db1', 't3', @exists); SELECT @exists;
Query OK, 0 rows affected (0.00 sec)

+---------+
| @exists |
+---------+
|         |
+---------+
1 row in set (0.00 sec)

30.4.5 sys Schema Stored Functions

The following sections describe sys schema stored functions.

30.4.5.1 The extract_schema_from_file_name() Function

Given a file path name, returns the path component that represents the schema name. This function
assumes that the file name lies within the schema directory. For this reason, it does not work with
partitions or tables defined using their own DATA_DIRECTORY table option.

This function is useful when extracting file I/O information from the Performance Schema that includes
file path names. It provides a convenient way to display schema names, which can be more easily
understood than full path names, and can be used in joins against object schema names.

Parameters

• path VARCHAR(512): The full path to a data file from which to extract the schema name.

Return Value

A VARCHAR(64) value.

5039

sys Schema Stored Functions

Example

mysql> SELECT sys.extract_schema_from_file_name('/usr/local/mysql/data/world/City.ibd');
+---------------------------------------------------------------------------+
| sys.extract_schema_from_file_name('/usr/local/mysql/data/world/City.ibd') |
+---------------------------------------------------------------------------+
| world                                                                     |
+---------------------------------------------------------------------------+

30.4.5.2 The extract_table_from_file_name() Function

Given a file path name, returns the path component that represents the table name.

This function is useful when extracting file I/O information from the Performance Schema that includes
file path names. It provides a convenient way to display table names, which can be more easily
understood than full path names, and can be used in joins against object table names.

Parameters

• path VARCHAR(512): The full path to a data file from which to extract the table name.

Return Value

A VARCHAR(64) value.

Example

mysql> SELECT sys.extract_table_from_file_name('/usr/local/mysql/data/world/City.ibd');
+--------------------------------------------------------------------------+
| sys.extract_table_from_file_name('/usr/local/mysql/data/world/City.ibd') |
+--------------------------------------------------------------------------+
| City                                                                     |
+--------------------------------------------------------------------------+

30.4.5.3 The format_bytes() Function

Note

format_bytes() is deprecated, and subject to removal in a future MySQL
version. Applications that use it should be migrated to use the built-in
FORMAT_BYTES() function instead. See Section 14.21, “Performance Schema
Functions”

Given a byte count, converts it to human-readable format and returns a string consisting of a value
and a units indicator. Depending on the size of the value, the units part is bytes, KiB (kibibytes), MiB
(mebibytes), GiB (gibibytes), TiB (tebibytes), or PiB (pebibytes).

Parameters

• bytes TEXT: The byte count to format.

Return Value

A TEXT value.

Example

mysql> SELECT sys.format_bytes(512), sys.format_bytes(18446644073709551615);
+-----------------------+----------------------------------------+
| sys.format_bytes(512) | sys.format_bytes(18446644073709551615) |
+-----------------------+----------------------------------------+
| 512 bytes             | 16383.91 PiB                           |
+-----------------------+----------------------------------------+

30.4.5.4 The format_path() Function

5040

sys Schema Stored Functions

Given a path name, returns the modified path name after replacing subpaths that match the values of
the following system variables, in order:

datadir
tmpdir
replica_load_tmpdir
innodb_data_home_dir
innodb_log_group_home_dir
innodb_undo_directory
basedir

A value that matches the value of system variable sysvar is replaced with the string
@@GLOBAL.sysvar.

Parameters

• path VARCHAR(512): The path name to format.

Return Value

A VARCHAR(512) CHARACTER SET utf8mb3 value.

Example

mysql> SELECT sys.format_path('/usr/local/mysql/data/world/City.ibd');
+---------------------------------------------------------+
| sys.format_path('/usr/local/mysql/data/world/City.ibd') |
+---------------------------------------------------------+
| @@datadir/world/City.ibd                                |
+---------------------------------------------------------+

30.4.5.5 The format_statement() Function

Given a string (normally representing an SQL statement), reduces it to the length given by the
statement_truncate_len configuration option, and returns the result. No truncation occurs if the
string is shorter than statement_truncate_len. Otherwise, the middle part of the string is replaced
by an ellipsis (...).

This function is useful for formatting possibly lengthy statements retrieved from Performance Schema
tables to a known fixed maximum length.

Parameters

• statement LONGTEXT: The statement to format.

Configuration Options

format_statement() operation can be modified using the following configuration options or their
corresponding user-defined variables (see Section 30.4.2.1, “The sys_config Table”):

• statement_truncate_len, @sys.statement_truncate_len

The maximum length of statements returned by the format_statement() function. Longer
statements are truncated to this length. The default is 64.

Return Value

A LONGTEXT value.

Example

By default, format_statement() truncates statements to be no more than 64 characters. Setting
@sys.statement_truncate_len changes the truncation length for the current session:

mysql> SET @stmt = 'SELECT variable, value, set_time, set_by FROM sys_config';

5041

sys Schema Stored Functions

mysql> SELECT sys.format_statement(@stmt);
+----------------------------------------------------------+
| sys.format_statement(@stmt)                              |
+----------------------------------------------------------+
| SELECT variable, value, set_time, set_by FROM sys_config |
+----------------------------------------------------------+
mysql> SET @sys.statement_truncate_len = 32;
mysql> SELECT sys.format_statement(@stmt);
+-----------------------------------+
| sys.format_statement(@stmt)       |
+-----------------------------------+
| SELECT variabl ... ROM sys_config |
+-----------------------------------+

30.4.5.6 The format_time() Function

Note

format_time() is deprecated, and subject to removal in a future MySQL
version. Applications that use it should be migrated to use the built-in
FORMAT_PICO_TIME() function instead. See Section 14.21, “Performance
Schema Functions”

Given a Performance Schema latency or wait time in picoseconds, converts it to human-readable
format and returns a string consisting of a value and a units indicator. Depending on the size of the
value, the units part is ps (picoseconds), ns (nanoseconds), us (microseconds), ms (milliseconds), s
(seconds), m (minutes), h (hours), d (days), or w (weeks).

Parameters

• picoseconds TEXT: The picoseconds value to format.

Return Value

A TEXT value.

Example

mysql> SELECT sys.format_time(3501), sys.format_time(188732396662000);
+-----------------------+----------------------------------+
| sys.format_time(3501) | sys.format_time(188732396662000) |
+-----------------------+----------------------------------+
| 3.50 ns               | 3.15 m                           |
+-----------------------+----------------------------------+

30.4.5.7 The list_add() Function

Adds a value to a comma-separated list of values and returns the result.

This function and list_drop() can be useful for manipulating the value of system variables such as
sql_mode and optimizer_switch that take a comma-separated list of values.

Parameters

• in_list TEXT: The list to be modified.

• in_add_value TEXT: The value to add to the list.

Return Value

A TEXT value.

Example

5042

sys Schema Stored Functions

mysql> SELECT @@sql_mode;
+----------------------------------------+
| @@sql_mode                             |
+----------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES |
+----------------------------------------+
mysql> SET @@sql_mode = sys.list_add(@@sql_mode, 'NO_ENGINE_SUBSTITUTION');
mysql> SELECT @@sql_mode;
+---------------------------------------------------------------+
| @@sql_mode                                                    |
+---------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION |
+---------------------------------------------------------------+
mysql> SET @@sql_mode = sys.list_drop(@@sql_mode, 'ONLY_FULL_GROUP_BY');
mysql> SELECT @@sql_mode;
+--------------------------------------------+
| @@sql_mode                                 |
+--------------------------------------------+
| STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION |
+--------------------------------------------+

30.4.5.8 The list_drop() Function

Removes a value from a comma-separated list of values and returns the result. For more information,
see the description of list_add()

Parameters

• in_list TEXT: The list to be modified.

• in_drop_value TEXT: The value to drop from the list.

Return Value

A TEXT value.

30.4.5.9 The ps_is_account_enabled() Function

Returns YES or NO to indicate whether Performance Schema instrumentation for a given account is
enabled.

Parameters

• in_host VARCHAR(60): The host name of the account to check.

• in_user VARCHAR(32): The user name of the account to check.

Return Value

An ENUM('YES','NO') value.

Example

mysql> SELECT sys.ps_is_account_enabled('localhost', 'root');
+------------------------------------------------+
| sys.ps_is_account_enabled('localhost', 'root') |
+------------------------------------------------+
| YES                                            |
+------------------------------------------------+

30.4.5.10 The ps_is_consumer_enabled() Function

Returns YES or NO to indicate whether a given Performance Schema consumer is enabled, or NULL if
the argument is NULL. If the argument is not a valid consumer name, an error occurs.

5043

sys Schema Stored Functions

| sys.ps_is_instrument_default_timed('memory/innodb/row_log_buf') |
+-----------------------------------------------------------------+
| NO                                                              |
+-----------------------------------------------------------------+
mysql> SELECT sys.ps_is_instrument_default_timed('statement/sql/alter_user');
+----------------------------------------------------------------+
| sys.ps_is_instrument_default_timed('statement/sql/alter_user') |
+----------------------------------------------------------------+
| YES                                                            |
+----------------------------------------------------------------+

30.4.5.13 The ps_is_thread_instrumented() Function

Returns YES or NO to indicate whether Performance Schema instrumentation for a given connection ID
is enabled, UNKNOWN if the ID is unknown, or NULL if the ID is NULL.

Parameters

• in_connection_id BIGINT UNSIGNED: The connection ID. This is a value of the type given

in the PROCESSLIST_ID column of the Performance Schema threads table or the Id column of
SHOW PROCESSLIST output.

Return Value

An ENUM('YES','NO','UNKNOWN') value.

Example

mysql> SELECT sys.ps_is_thread_instrumented(43);
+-----------------------------------+
| sys.ps_is_thread_instrumented(43) |
+-----------------------------------+
| UNKNOWN                           |
+-----------------------------------+
mysql> SELECT sys.ps_is_thread_instrumented(CONNECTION_ID());
+------------------------------------------------+
| sys.ps_is_thread_instrumented(CONNECTION_ID()) |
+------------------------------------------------+
| YES                                            |
+------------------------------------------------+

30.4.5.14 The ps_thread_account() Function

Given a Performance Schema thread ID, returns the user_name@host_name account associated with
the thread.

Parameters

• in_thread_id BIGINT UNSIGNED: The thread ID for which to return the account. The value
should match the THREAD_ID column from some Performance Schema threads table row.

Return Value

A TEXT value.

Example

mysql> SELECT sys.ps_thread_account(sys.ps_thread_id(CONNECTION_ID()));
+----------------------------------------------------------+
| sys.ps_thread_account(sys.ps_thread_id(CONNECTION_ID())) |
+----------------------------------------------------------+
| root@localhost                                           |
+----------------------------------------------------------+

30.4.5.15 The ps_thread_id() Function

5045

sys Schema Stored Functions

Note

ps_thread_id() is deprecated, and subject to removal in a future MySQL
version. Applications that use it should be migrated to use the built-in
PS_THREAD_ID() and PS_CURRENT_THREAD_ID() functions instead. See
Section 14.21, “Performance Schema Functions”

Returns the Performance Schema thread ID assigned to a given connection ID, or the thread ID for the
current connection if the connection ID is NULL.

Parameters

• in_connection_id BIGINT UNSIGNED: The ID of the connection for which to return the thread
ID. This is a value of the type given in the PROCESSLIST_ID column of the Performance Schema
threads table or the Id column of SHOW PROCESSLIST output.

Return Value

A BIGINT UNSIGNED value.

Example

mysql> SELECT sys.ps_thread_id(260);
+-----------------------+
| sys.ps_thread_id(260) |
+-----------------------+
|                   285 |
+-----------------------+

30.4.5.16 The ps_thread_stack() Function

Returns a JSON formatted stack of all statements, stages, and events within the Performance Schema
for a given thread ID.

Parameters

• in_thread_id BIGINT: The ID of the thread to trace. The value should match the THREAD_ID

column from some Performance Schema threads table row.

• in_verbose BOOLEAN: Whether to include file:lineno information in the events.

Return Value

A LONGTEXT CHARACTER SET latin1 value.

Example

mysql> SELECT sys.ps_thread_stack(37, FALSE) AS thread_stack\G
*************************** 1. row ***************************
thread_stack: {"rankdir": "LR","nodesep": "0.10",
"stack_created": "2014-02-19 13:39:03", "mysql_version": "8.4.0-tr",
"mysql_user": "root@localhost","events": [{"nesting_event_id": "0",
"event_id": "10", "timer_wait": 256.35, "event_info": "sql/select",
"wait_info": "select @@version_comment limit 1\nerrors: 0\nwarnings: 0\nlock time:
...

30.4.5.17 The ps_thread_trx_info() Function

Returns a JSON object containing information about a given thread. The information includes the
current transaction, and the statements it has already executed, derived from the Performance Schema
events_transactions_current and events_statements_history tables. (The consumers for
those tables must be enabled to obtain full data in the JSON object.)

5046

sys Schema Stored Functions

If the output exceeds the truncation length (65535 by default), a JSON error object is returned, such as:

{ "error": "Trx info truncated: Row 6 was cut by GROUP_CONCAT()" }

Similar error objects are returned for other warnings and exceptions raised during function execution.

Parameters

• in_thread_id BIGINT UNSIGNED: The thread ID for which to return transaction information. The
value should match the THREAD_ID column from some Performance Schema threads table row.

Configuration Options

ps_thread_trx_info() operation can be modified using the following configuration options or their
corresponding user-defined variables (see Section 30.4.2.1, “The sys_config Table”):

• ps_thread_trx_info.max_length, @sys.ps_thread_trx_info.max_length

The maximum length of the output. The default is 65535.

Return Value

A LONGTEXT value.

Example

mysql> SELECT sys.ps_thread_trx_info(48)\G
*************************** 1. row ***************************
sys.ps_thread_trx_info(48): [
  {
    "time": "790.70 us",
    "state": "COMMITTED",
    "mode": "READ WRITE",
    "autocommitted": "NO",
    "gtid": "AUTOMATIC",
    "isolation": "REPEATABLE READ",
    "statements_executed": [
      {
        "sql_text": "INSERT INTO info VALUES (1, \'foo\')",
        "time": "471.02 us",
        "schema": "trx",
        "rows_examined": 0,
        "rows_affected": 1,
        "rows_sent": 0,
        "tmp_tables": 0,
        "tmp_disk_tables": 0,
        "sort_rows": 0,
        "sort_merge_passes": 0
      },
      {
        "sql_text": "COMMIT",
        "time": "254.42 us",
        "schema": "trx",
        "rows_examined": 0,
        "rows_affected": 0,
        "rows_sent": 0,
        "tmp_tables": 0,
        "tmp_disk_tables": 0,
        "sort_rows": 0,
        "sort_merge_passes": 0
      }
    ]
  },
  {
    "time": "426.20 us",
    "state": "COMMITTED",
    "mode": "READ WRITE",
    "autocommitted": "NO",
    "gtid": "AUTOMATIC",

5047

sys Schema Stored Functions

    "isolation": "REPEATABLE READ",
    "statements_executed": [
      {
        "sql_text": "INSERT INTO info VALUES (2, \'bar\')",
        "time": "107.33 us",
        "schema": "trx",
        "rows_examined": 0,
        "rows_affected": 1,
        "rows_sent": 0,
        "tmp_tables": 0,
        "tmp_disk_tables": 0,
        "sort_rows": 0,
        "sort_merge_passes": 0
      },
      {
        "sql_text": "COMMIT",
        "time": "213.23 us",
        "schema": "trx",
        "rows_examined": 0,
        "rows_affected": 0,
        "rows_sent": 0,
        "tmp_tables": 0,
        "tmp_disk_tables": 0,
        "sort_rows": 0,
        "sort_merge_passes": 0
      }
    ]
  }
]

30.4.5.18 The quote_identifier() Function

Given a string argument, this function produces a quoted identifier suitable for inclusion in SQL
statements. This is useful when a value to be used as an identifier is a reserved word or contains
backtick (`) characters.

Parameters

in_identifier TEXT: The identifier to quote.

Return Value

A TEXT value.

Example

mysql> SELECT sys.quote_identifier('plain');
+-------------------------------+
| sys.quote_identifier('plain') |
+-------------------------------+
| `plain`                       |
+-------------------------------+
mysql> SELECT sys.quote_identifier('trick`ier');
+-----------------------------------+
| sys.quote_identifier('trick`ier') |
+-----------------------------------+
| `trick``ier`                      |
+-----------------------------------+
mysql> SELECT sys.quote_identifier('integer');
+---------------------------------+
| sys.quote_identifier('integer') |
+---------------------------------+
| `integer`                       |
+---------------------------------+

30.4.5.19 The sys_get_config() Function

Given a configuration option name, returns the option value from the sys_config table, or the
provided default value (which may be NULL) if the option does not exist in the table.

5048

sys Schema Stored Functions

If sys_get_config() returns the default value and that value is NULL, it is expected that the caller is
able to handle NULL for the given configuration option.

By convention, routines that call sys_get_config() first check whether the corresponding user-
defined variable exists and is non-NULL. If so, the routine uses the variable value without reading the
sys_config table. If the variable does not exist or is NULL, the routine reads the option value from
the table and sets the user-defined variable to that value. For more information about the relationship
between configuration options and their corresponding user-defined variables, see Section 30.4.2.1,
“The sys_config Table”.

If you want to check whether the configuration option has already been set and, if not, use the return
value of sys_get_config(), you can use IFNULL(...) (see example later). However, this should
not be done inside a loop (for example, for each row in a result set) because for repeated calls where
the assignment is needed only in the first iteration, using IFNULL(...) is expected to be significantly
slower than using an IF (...) THEN ... END IF; block (see example later).

Parameters

• in_variable_name VARCHAR(128): The name of the configuration option for which to return the

value.

• in_default_value VARCHAR(128): The default value to return if the configuration option is not

found in the sys_config table.

Return Value

A VARCHAR(128) value.

Example

Get a configuration value from the sys_config table, falling back to 128 as the default if the option is
not present in the table:

mysql> SELECT sys.sys_get_config('statement_truncate_len', 128) AS Value;
+-------+
| Value |
+-------+
| 64    |
+-------+

One-liner example: Check whether the option is already set; if not, assign the IFNULL(...) result
(using the value from the sys_config table):

mysql> SET @sys.statement_truncate_len =
       IFNULL(@sys.statement_truncate_len,
              sys.sys_get_config('statement_truncate_len', 64));

IF (...) THEN ... END IF; block example: Check whether the option is already set; if not,
assign the value from the sys_config table:

IF (@sys.statement_truncate_len IS NULL) THEN
  SET @sys.statement_truncate_len = sys.sys_get_config('statement_truncate_len', 64);
END IF;

30.4.5.20 The version_major() Function

This function returns the major version of the MySQL server.

Parameters

None.

Return Value

A TINYINT UNSIGNED value.

5049

sys Schema Stored Functions

Example

mysql> SELECT VERSION(), sys.version_major();
+-----------+---------------------+
| VERSION() | sys.version_major() |
+-----------+---------------------+
| 8.4.2     |                   8 |
+-----------+---------------------+

30.4.5.21 The version_minor() Function

This function returns the minor version of the MySQL server.

Parameters

None.

Return Value

A TINYINT UNSIGNED value.

Example

mysql> SELECT VERSION(), sys.version_minor();
+-----------+---------------------+
| VERSION() | sys.version_minor() |
+-----------+---------------------+
| 8.4.2     |                   4 |
+-----------+---------------------+

30.4.5.22 The version_patch() Function

This function returns the patch release version of the MySQL server.

Parameters

None.

Return Value

A TINYINT UNSIGNED value.

Example

mysql> SELECT VERSION(), sys.version_patch();
+-----------+---------------------+
| VERSION() | sys.version_patch() |
+-----------+---------------------+
| 8.4.2     |                   2 |
+-----------+---------------------+

5050

